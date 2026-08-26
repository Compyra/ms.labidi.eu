"""Phase 7 integration audit: matrix vs records vs registry vs libraries."""
import json
import re
from pathlib import Path

ROOT = Path(r'c:\Temp\Git\ms.labidi.eu')


def blob(name):
    txt = (ROOT / 'data' / name).read_text(encoding='utf-8')
    m = re.search(r'concat\((\[.*\])\);', txt, re.S) or \
        re.search(r'=(\[.*\]);', txt, re.S)
    return json.loads(m.group(1))


records = {}
for f in sorted((ROOT / 'data').glob('data-commands-*.js')):
    for r in blob(f.name):
        records[r['id']] = r
lic = blob('data-licensing.js')
reg = json.loads(re.search(r'=({.*});', (ROOT / 'data' / 'data-registry.js')
                           .read_text(encoding='utf-8'), re.S).group(1))
licreg = reg['licenses']

def covered(base, target):
    """target license reachable from base via includes[] closure."""
    stack, seen = [base], set()
    while stack:
        x = stack.pop()
        if x == target:
            return True
        if x in seen:
            continue
        seen.add(x)
        stack.extend(licreg.get(x, {}).get('inc', []))
    return False

print('== A. matrix min vs related-record license ==')
issues = 0
for row in lic:
    skus = [row['min']] + row.get('alsoIn', [])
    for rid in row.get('related', []):
        rec = records.get(rid)
        if not rec or not rec.get('license') or rec['license'] == 'free':
            continue
        rl = rec['license']
        ok = any(covered(s, rl) or covered(rl, s) or s == rl for s in skus)
        if not ok:
            issues += 1
            print(f"  {row['id']} (min {row['min']}, also {row.get('alsoIn', [])})"
                  f" vs {rid}.license={rl}")
print(f'  mismatches: {issues}')

print('== B. deprecated targets in phase-7 related ==')
bad = [(row['id'], rid) for row in lic for rid in row.get('related', [])
       if records.get(rid, {}).get('deprecated')]
print(f'  {bad or "none"}')

print('== C. error-code records: id/family/desc sanity ==')
codes = [r for r in records.values() if r.get('group') == 'Error codes']
fams = {}
for r in codes:
    fam = re.match(r'^[a-z]+', r['id']).group(0)
    fams[fam] = fams.get(fam, 0) + 1
    if not r.get('desc', '').strip() or len(r['desc']) < 80:
        print(f"  thin desc: {r['id']}")
    if r.get('url'):
        print(f"  unexpected url on {r['id']} (concepts should be url-less)")
print(f'  {len(codes)} codes, families {fams}')

print('== D. lic ids referenced anywhere they cannot resolve ==')
kql = blob('data-kql.js'); ps = blob('data-ps.js'); rbs = blob('data-runbooks.js')
for group, rows in (('kql/ps', kql + ps), ('runbooks', rbs)):
    hits = [(r['id'], x) for r in rows for x in r.get('related', [])
            if x.startswith('lic-')]
    print(f'  {group}: {hits or "none"}')

print('== E. registry SKUs never referenced by matrix or records ==')
used = {s for row in lic for s in [row['min']] + row.get('alsoIn', [])}
used |= {r.get('license') for r in records.values() if r.get('license')}
for inc_of in licreg.values():
    used |= set(inc_of.get('inc', []))
print(f"  orphans: {sorted(set(licreg) - used) or 'none'}")
