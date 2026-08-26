"""One-shot + reusable analysis of vendor/cmdms-commands.csv.

Prints the facts the import pipeline (docs/12) depends on: counts, categories,
duplicate ids/aliases, URL hosts, sovereign-twin fold candidates.
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "vendor" / "cmdms-commands.csv"

def main():
    raw = CSV_PATH.read_bytes()
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    fields = list(rows[0].keys()) if rows else []
    print(f"rows={len(rows)} fields={fields}")

    ids = [r["Command"].strip().lower() for r in rows]
    dup_ids = [i for i, c in Counter(ids).items() if c > 1]
    print(f"duplicate ids: {dup_ids or 'none'}")

    alias_owner = {}
    alias_dupes = defaultdict(set)
    for r in rows:
        for a in filter(None, (x.strip().lower() for x in r["Alias"].split("|"))):
            if a in alias_owner and alias_owner[a] != r["Command"]:
                alias_dupes[a].update([alias_owner[a], r["Command"]])
            alias_owner[a] = r["Command"]
    shadows = sorted(set(alias_owner) & set(ids))
    print(f"alias duplicated across rows: {dict(alias_dupes) or 'none'}")
    print(f"aliases shadowing an id: {shadows or 'none'}")

    print("\ncategories:")
    for cat, n in Counter(r["Category"].strip() for r in rows).most_common():
        print(f"  {cat!r}: {n}")

    print("\nurl hosts (top 25):")
    hosts = Counter(re.sub(r"^https?://([^/]+).*", r"\1", r["Url"].strip()) for r in rows)
    for h, n in hosts.most_common(25):
        print(f"  {h}: {n}")

    bad = [r["Command"] for r in rows if not r["Url"].strip().startswith("https://")]
    print(f"\nnon-https or empty urls: {bad or 'none'}")
    iconed = sum(1 for r in rows if (r.get("Icon") or "").strip())
    print(f"rows with Icon set: {iconed}")

    print("\nsovereign twin candidates (id endswith g/gh/dod/gcc and base exists):")
    idset = set(ids)
    for r in rows:
        i = r["Command"].strip().lower()
        for suf, cloud in (("gh", "gcch"), ("dod", "dod"), ("gcc", "gcc"), ("g", "gcch")):
            base = i[: -len(suf)] if i.endswith(suf) else None
            if base and base in idset and base != i:
                print(f"  {i} -> {base} [{cloud}]  name={r['Description']!r} url={r['Url'][:60]}")
                break

    print("\nnames containing GCC/DoD/High without base-id match (manual fold review):")
    for r in rows:
        i = r["Command"].strip().lower()
        if re.search(r"GCC|DoD", r["Description"]):
            print(f"  {i}: {r['Description']!r}")

if __name__ == "__main__":
    sys.exit(main())
