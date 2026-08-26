"""Build data/*.js from vendor + content sources. Stdlib only; fails loudly.

Contract: docs/12-data-model-import.md. Emits deterministic, LF, UTF-8 (no BOM).
"""
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

SUBJECTS = ["entra", "intune", "defender", "sentinel", "azure", "m365", "purview",
            "power", "windows", "automation", "licensing", "msp", "toolbox", "mypages"]
KINDS = ["portal", "setting", "tool", "docs", "enduser", "concept"]
CLOUDS = ["gcc", "gcch", "dod", "cn"]
STANDARDS = {"cis", "scuba", "securescore", "essential8", "ce"}
BLAST = {"low", "med", "high"}
CATMAP = {"Entra": "entra", "Intune": "intune", "Defender": "defender", "Azure": "azure",
          "Microsoft 365": "m365", "Purview": "purview", "My Pages": "mypages",
          "General": "licensing", "XDR Sentinel": "sentinel", "Power Platform": "power"}
ID_RE = re.compile(r"^[a-z0-9-]{1,32}$")

errors, warnings = [], []


def read_csv(path):
    text = path.read_bytes().decode("utf-8-sig")
    rows = [r for r in text.splitlines() if r.strip() and not r.lstrip().startswith("#")]
    return list(csv.DictReader(rows))


def split_multi(value, sep="|"):
    return [x.strip() for x in (value or "").split(sep) if x.strip()]


def load_upstream():
    records = {}
    for row in read_csv(ROOT / "vendor" / "cmdms-commands.csv"):
        rid = row["Command"].strip().lower()
        cat = CATMAP.get(row["Category"].strip())
        if cat is None:
            errors.append(f"upstream {rid}: unknown category {row['Category']!r}")
            continue
        records[rid] = {
            "id": rid,
            "kind": "enduser" if row["Category"].strip() == "My Pages" else "portal",
            "aliases": [a.lower() for a in split_multi(row["Alias"])],
            "name": row["Description"].strip(),
            "category": cat,
            "url": row["Url"].strip(),
            "clouds": {},
            "aliasClouds": {},
            "keywords": sorted(set(row["Keywords"].strip().lower().split())),
            "related": [],
            "source": "cmdms",
        }
    return records


def load_enrich(records):
    files = sorted(ROOT.glob("content/enrich-*.csv")) + \
        sorted(ROOT.glob("content/settings-*.csv"))
    for path in files:
        is_settings = path.name.startswith("settings-")
        for row in read_csv(path):
            rid = row["id"].strip().lower()
            new = rid not in records
            rec = records.setdefault(rid, {
                "id": rid, "kind": "setting" if is_settings else "portal",
                "aliases": [], "name": "", "category": "",
                "url": "", "clouds": {}, "aliasClouds": {}, "keywords": [],
                "related": [], "source": "own",
            })
            for field in ("kind", "name", "url", "path", "desc", "license",
                          "docs", "ps", "verified", "shareText", "blastRadius"):
                val = (row.get(field) or "").strip()
                if val:
                    rec[field] = val
            if (row.get("group") or "").strip():
                rec["group"] = row["group"].strip()
            if new:
                rec["category"] = (row.get("category") or "").strip() or infer_category(path)
            for field, sep in (("aliases", "|"), ("keywords", "|"),
                               ("roles", "|"), ("related", "|"),
                               ("standards", "|")):
                vals = split_multi(row.get(field) or "")
                if vals:
                    rec[field] = sorted(set(rec.get(field, []) + [v.lower() for v in vals]))


def infer_category(path):
    return path.stem.split("-", 1)[1]


def apply_overrides(records):
    for row in read_csv(ROOT / "content" / "overrides.csv"):
        rid, op = row["id"].strip().lower(), row["op"].strip()
        arg1 = row.get("arg1", "").strip().lower()
        arg2 = row.get("arg2", "").strip().lower()
        if rid not in records:
            errors.append(f"override {op} on unknown id {rid}")
            continue
        if op == "keep":
            continue
        if op == "category":
            if arg1 not in SUBJECTS:
                errors.append(f"override {rid}: unknown category {arg1}")
            else:
                records[rid]["category"] = arg1
        elif op == "kind":
            if arg1 not in KINDS:
                errors.append(f"override {rid}: unknown kind {arg1}")
            else:
                records[rid]["kind"] = arg1
        elif op == "deprecated":
            records[rid]["deprecated"] = True
            if arg1:
                records[rid]["related"] = [arg1] + [
                    r for r in records[rid]["related"] if r != arg1]
        elif op == "fold":
            if arg1 not in records:
                errors.append(f"fold {rid}: target {arg1} missing")
                continue
            if arg2 not in CLOUDS:
                errors.append(f"fold {rid}: unknown cloud {arg2}")
                continue
            twin, target = records.pop(rid), records[arg1]
            if arg2 in target["clouds"]:
                errors.append(f"fold {rid}: {arg1} already has cloud {arg2}")
            target["clouds"][arg2] = twin["url"]
            for name in [twin["id"]] + twin["aliases"]:
                target["aliases"].append(name)
                target["aliasClouds"][name] = arg2
            target["keywords"] = sorted(set(target["keywords"] + twin["keywords"]))
        else:
            errors.append(f"override {rid}: unknown op {op}")


def load_registry(name):
    return {r["id"].strip().lower() for r in read_csv(ROOT / "content" / f"{name}.csv")}


def load_full_registries():
    roles = {}
    for r in read_csv(ROOT / "content" / "roles.csv"):
        roles[r["id"].strip().lower()] = r["name"].strip()
    lics = {}
    for r in read_csv(ROOT / "content" / "licenses.csv"):
        inc = [x.strip().lower() for x in (r.get("includes") or "").split("|") if x.strip()]
        lics[r["id"].strip().lower()] = {"n": r["name"].strip(), "inc": inc}
    for lid, entry in lics.items():
        for i in entry["inc"]:
            if i not in lics:
                errors.append(f"licenses.csv {lid}: unknown include {i}")
    tables = []
    for r in read_csv(ROOT / "content" / "tables.csv"):
        tables.append({"name": r["name"].strip(), "product": (r.get("product") or "").strip(),
                       "costTier": (r.get("costTier") or "").strip(),
                       "retention": (r.get("retention") or "").strip(),
                       "notes": (r.get("notes") or "").strip()})
    return {"roles": roles, "licenses": lics,
            "tables": sorted(tables, key=lambda t: t["name"].lower())}


def load_synonyms(known_ids):
    out = []
    for row in read_csv(ROOT / "content" / "synonyms.csv"):
        boost = [b.strip().lower() for b in row.get("boostIds", "").split(";") if b.strip()]
        for b in boost:
            if b not in known_ids:
                warnings.append(f"synonym {row['term']}: boost id {b} not yet a record")
        out.append({"term": row["term"].strip().lower(),
                    "expandsTo": row["expandsTo"].strip().lower(),
                    "boostIds": [b for b in boost if b in known_ids]})
    return sorted(out, key=lambda s: s["term"])


def load_runbooks(records, extra_ids=frozenset()):
    """content/runbooks/*.md -> list of dicts, or None before phase 6 starts."""
    folder = ROOT / "content" / "runbooks"
    if not folder.exists():
        return None
    section_map = {"preconditions": "pre", "steps": "steps", "verify": "verify",
                   "rollback": "rollback", "escalate when": "escalate"}
    out, seen = [], set()
    for path in sorted(folder.glob("*.md")):
        text = path.read_bytes().decode("utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        if not m:
            errors.append(f"runbook {path.name}: missing frontmatter")
            continue
        fm = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                fm[key.strip()] = val.strip()
        rid = fm.get("id", "").lower()
        if not rid.startswith("rb-"):
            errors.append(f"runbook {path.name}: id must start with 'rb-'")
        if rid in seen or rid in records:
            errors.append(f"runbook {rid}: duplicate or collides with a command id")
        seen.add(rid)
        if fm.get("level") not in ("L1", "L2", "L3"):
            errors.append(f"runbook {rid}: bad level {fm.get('level')!r}")
        if fm.get("subject") not in SUBJECTS:
            errors.append(f"runbook {rid}: bad subject {fm.get('subject')!r}")
        entry = {"id": rid, "kind": "runbook", "title": fm.get("title", ""),
                 "level": fm.get("level"), "subject": fm.get("subject")}
        if fm.get("verified"):
            entry["verified"] = fm["verified"]
        tags = split_multi(fm.get("tags", ""))
        if tags:
            entry["tags"] = [t.lower() for t in tags]
        rel = split_multi(fm.get("related", ""))
        if rel:
            unknown = [r for r in rel
                       if r.lower() not in records and r.lower() not in extra_ids]
            if unknown:
                errors.append(f"runbook {rid}: related {unknown} not a record")
            entry["related"] = [r.lower() for r in rel]
        for chunk in re.split(r"^## +", m.group(2), flags=re.M):
            if not chunk.strip():
                continue
            header, _, body = chunk.partition("\n")
            key = section_map.get(header.strip().lower())
            if key is None:
                errors.append(f"runbook {rid}: unknown section {header.strip()!r}")
                continue
            lines = [re.sub(r"^\s*(?:[-*]|\d+\.)\s*", "", ln).strip()
                     for ln in body.splitlines() if ln.strip()]
            if lines:
                entry[key] = lines
        for required in ("steps", "verify", "escalate"):
            if not entry.get(required):
                errors.append(f"runbook {rid}: missing section {required}")
        if not entry["title"]:
            errors.append(f"runbook {rid}: missing title")
        if "VERIFY" in text.replace(fm.get("verified", ""), ""):
            errors.append(f"runbook {rid}: contains a VERIFY marker")
        out.append(entry)
    return sorted(out, key=lambda r: r["id"])


def load_library(name, extra_fields, records, table_names=None):
    """content/<name>.csv -> list of dicts, or None when the phase has not started.

    Single-line code only: read_csv is line-based, so multiline quoted CSV
    fields are unsupported by design.
    """
    path = ROOT / "content" / f"{name}.csv"
    if not path.exists():
        return None
    rows, seen = [], set()
    prefix = name + "-"
    for row in read_csv(path):
        rid = (row.get("id") or "").strip().lower()
        if not rid.startswith(prefix):
            errors.append(f"{name} {rid}: id must start with '{prefix}'")
        if rid in seen or rid in records:
            errors.append(f"{name} {rid}: duplicate or collides with a command id")
        seen.add(rid)
        entry = {"id": rid, "kind": name}
        for field in ("title", "subject", "code", "docs", "verified") + extra_fields:
            val = (row.get(field) or "").strip()
            if val:
                entry[field] = val
        tags = split_multi(row.get("tags") or "")
        if tags:
            entry["tags"] = [t.lower() for t in tags]
        rel = split_multi(row.get("related") or "")
        if rel:
            unknown = [r for r in rel if r.lower() not in records]
            if unknown:
                errors.append(f"{name} {rid}: related {unknown} not a record")
            entry["related"] = [r.lower() for r in rel]
        if not entry.get("title") or not entry.get("code"):
            errors.append(f"{name} {rid}: missing title or code")
        subject = entry.get("subject")
        if subject and subject not in SUBJECTS:
            errors.append(f"{name} {rid}: bad subject {subject!r}")
        if table_names is not None:
            if entry.get("table") and entry["table"] not in table_names:
                errors.append(f"{name} {rid}: table {entry['table']!r} not in tables.csv")
        rows.append(entry)
    return sorted(rows, key=lambda r: r["id"])


def validate(records, roles, licenses):
    seen_alias = {}
    for rec in records.values():
        rid = rec["id"]
        if not ID_RE.match(rid):
            errors.append(f"{rid}: bad id format")
        if not rec["name"]:
            errors.append(f"{rid}: empty name")
        if len(rec["name"]) > 120:
            errors.append(f"{rid}: name too long")
        if rec["category"] not in SUBJECTS:
            errors.append(f"{rid}: bad category {rec['category']!r}")
        if rec["kind"] not in KINDS:
            errors.append(f"{rid}: bad kind {rec['kind']!r}")
        if rec["kind"] in ("portal", "tool", "docs", "enduser"):
            if not rec["url"].startswith("https://"):
                errors.append(f"{rid}: url must be https ({rec['url'][:40]!r})")
        for a in rec["aliases"]:
            if a in records:
                errors.append(f"{rid}: alias {a} shadows a record id")
            if a in seen_alias and seen_alias[a] != rid:
                errors.append(f"alias {a} used by both {seen_alias[a]} and {rid}")
            seen_alias[a] = rid
        for r in rec["related"]:
            if r not in records:
                errors.append(f"{rid}: related {r} does not exist")
        for role in rec.get("roles", []):
            if role not in roles:
                errors.append(f"{rid}: unknown role {role}")
        lic = rec.get("license")
        if lic and lic not in licenses:
            errors.append(f"{rid}: unknown license {lic}")
        br = rec.get("blastRadius")
        if br and br not in BLAST:
            errors.append(f"{rid}: bad blastRadius {br!r}")
        for s in rec.get("standards", []):
            if s not in STANDARDS:
                errors.append(f"{rid}: unknown standard {s}")


def compact(rec):
    out = {"id": rec["id"], "kind": rec["kind"], "name": rec["name"],
           "category": rec["category"]}
    if rec.get("url"):
        out["url"] = rec["url"]
    for key in ("aliases", "keywords", "related"):
        if rec.get(key):
            out[key] = rec[key]
    for key in ("clouds", "aliasClouds"):
        if rec.get(key):
            out[key] = dict(sorted(rec[key].items()))
    for key in ("group", "path", "desc", "roles", "license", "docs", "ps",
                "verified", "shareText", "blastRadius", "standards"):
        if rec.get(key):
            out[key] = rec[key]
    if rec.get("deprecated"):
        out["deprecated"] = True
    out["source"] = rec["source"]
    return out


def write_js(path, banner, statement):
    body = f"/* generated by tools/build_data.py; do not edit. {banner} */\n{statement}\n"
    path.write_bytes(body.encode("utf-8"))


def main():
    meta = json.loads((ROOT / "vendor" / "cmdms-commands.meta.json").read_bytes())
    records = load_upstream()
    upstream_count = len(records)
    load_enrich(records)
    apply_overrides(records)
    registries = load_full_registries()
    validate(records, set(registries["roles"]), set(registries["licenses"]))
    synonyms = load_synonyms(set(records))
    table_names = {r["name"].strip() for r in read_csv(ROOT / "content" / "tables.csv")}
    kql = load_library("kql", ("table",), records, table_names)
    ps = load_library("ps", ("module", "scopes"), records)
    library_ids = {r["id"] for r in (kql or [])} | {r["id"] for r in (ps or [])}
    for rec in records.values():
        hint = rec.get("ps", "")
        if hint.startswith(("ps-", "kql-")) and hint not in library_ids:
            errors.append(f"{rec['id']}: ps hint {hint!r} is not a library entry")
    runbooks = load_runbooks(records, library_ids)

    for w in warnings:
        print(f"warn: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    DATA.mkdir(exist_ok=True)
    banner = f"data incl. cmd.ms (MIT) commit {meta['commit'][:7]}"
    counts = {}
    for subject in SUBJECTS:
        subset = sorted((compact(r) for r in records.values()
                         if r["category"] == subject), key=lambda r: r["id"])
        counts[subject] = len(subset)
        payload = json.dumps(subset, ensure_ascii=False, separators=(",", ":"))
        write_js(DATA / f"data-commands-{subject}.js", banner,
                 "(window.MSHUB=window.MSHUB||{}).commands="
                 f"(window.MSHUB.commands||[]).concat({payload});")
    write_js(DATA / "data-synonyms.js", banner,
             "(window.MSHUB=window.MSHUB||{}).synonyms="
             + json.dumps(synonyms, ensure_ascii=False, separators=(",", ":")) + ";")
    write_js(DATA / "data-registry.js", banner,
             "(window.MSHUB=window.MSHUB||{}).registry="
             + json.dumps(registries, ensure_ascii=False, separators=(",", ":")) + ";")
    libraries = {}
    for lib_name, rows in (("kql", kql), ("ps", ps), ("runbooks", runbooks)):
        if rows is not None:
            libraries[lib_name] = len(rows)
            write_js(DATA / f"data-{lib_name}.js", banner,
                     f"(window.MSHUB=window.MSHUB||{{}}).{lib_name}="
                     + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";")
    meta_out = {"built": date.today().isoformat(), "records": len(records),
                "upstreamCommands": upstream_count, "counts": counts,
                "libraries": libraries,
                "upstream": {"commit": meta["commit"], "committedAt": meta["committedAt"],
                             "rows": meta["rows"], "license": meta["license"],
                             "source": meta["source"]}}
    write_js(DATA / "data-meta.js", banner,
             "(window.MSHUB=window.MSHUB||{}).meta="
             + json.dumps(meta_out, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"ok: {len(records)} records from {upstream_count} upstream rows; "
          f"{len(synonyms)} synonyms; libraries: {libraries or 'none'}; per subject: "
          + ", ".join(f"{s}={n}" for s, n in counts.items() if n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
