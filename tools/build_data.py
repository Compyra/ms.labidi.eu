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
    for path in sorted(ROOT.glob("content/enrich-*.csv")):
        for row in read_csv(path):
            rid = row["id"].strip().lower()
            new = rid not in records
            rec = records.setdefault(rid, {
                "id": rid, "kind": "portal", "aliases": [], "name": "", "category": "",
                "url": "", "clouds": {}, "aliasClouds": {}, "keywords": [],
                "related": [], "source": "own",
            })
            for field in ("kind", "name", "url", "path", "desc", "license",
                          "docs", "ps", "verified"):
                if row.get(field, "").strip():
                    rec[field] = row[field].strip()
            if row.get("group", "").strip():
                rec["group"] = row["group"].strip()
            if new:
                rec["category"] = row.get("category", "").strip() or infer_category(path)
            for field, sep in (("aliases", "|"), ("keywords", "|"),
                               ("roles", "|"), ("related", "|")):
                vals = split_multi(row.get(field, ""))
                if vals:
                    rec[field] = sorted(set(rec.get(field, []) + [v.lower() for v in vals]))


def infer_category(path):
    return path.stem.replace("enrich-", "")


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
                "verified", "shareText"):
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
    validate(records, load_registry("roles"), load_registry("licenses"))
    synonyms = load_synonyms(set(records))

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
    meta_out = {"built": date.today().isoformat(), "records": len(records),
                "upstreamCommands": upstream_count, "counts": counts,
                "upstream": {"commit": meta["commit"], "committedAt": meta["committedAt"],
                             "rows": meta["rows"], "license": meta["license"],
                             "source": meta["source"]}}
    write_js(DATA / "data-meta.js", banner,
             "(window.MSHUB=window.MSHUB||{}).meta="
             + json.dumps(meta_out, ensure_ascii=False, separators=(",", ":")) + ";")
    print(f"ok: {len(records)} records from {upstream_count} upstream rows; "
          f"{len(synonyms)} synonyms; per subject: "
          + ", ".join(f"{s}={n}" for s, n in counts.items() if n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
