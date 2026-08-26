"""Offline freshness report: stale verified stamps + upstream pin age.

The quarterly ritual (docs/13 phase 9) is:
  1. python tools/check_freshness.py     (this: what needs attention, offline)
  2. python tools/sync_upstream.py       (upstream drift, network)
  3. python tools/check_links.py         (link rot + portal moves, network)
  4. python tools/audit_consistency.py   (cross-layer meaning check, offline)

Exit 0 always; it reports, humans decide.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STALE_DAYS = 184  # two quarters


def parse_stamp(stamp):
    m = re.match(r"^(\d{4})-(\d{2})$", stamp or "")
    if not m:
        return None
    return date(int(m.group(1)), int(m.group(2)), 1)


def main():
    today = date.today()
    stale, unstamped, total = {}, 0, 0
    for path in sorted((ROOT / "data").glob("*.js")):
        text = path.read_text(encoding="utf-8")
        m = re.search(r"concat\((\[.*\])\);", text, re.S) or \
            re.search(r"=(\[.*\]);", text, re.S)
        if not m:
            continue
        for row in json.loads(m.group(1)):
            if not isinstance(row, dict) or "id" not in row:
                continue
            total += 1
            if row.get("source") == "cmdms" and "verified" not in row:
                continue  # upstream rows age with the vendor pin instead
            stamp = parse_stamp(row.get("verified"))
            if stamp is None:
                unstamped += 1
                continue
            age = (today - stamp).days
            if age > STALE_DAYS:
                stale.setdefault(row["verified"], []).append(row["id"])
    print(f"rows scanned: {total}; stale threshold: {STALE_DAYS} days")
    if stale:
        print(f"\n== STALE verified stamps ==")
        for stamp in sorted(stale):
            ids = stale[stamp]
            print(f"  {stamp}: {len(ids)} rows, e.g. {', '.join(ids[:8])}")
        print("Re-verify against current docs, then refresh the stamps you touched.")
    else:
        print("no stale verified stamps.")
    print(f"unstamped own rows: {unstamped}")
    meta = json.loads((ROOT / "vendor" / "cmdms-commands.meta.json").read_bytes())
    fetched = date.fromisoformat(meta["fetchedAt"])
    pin_age = (today - fetched).days
    print(f"\nupstream pin fetched {meta['fetchedAt']} ({pin_age} days ago)")
    if pin_age > 90:
        print("pin older than a quarter: run tools/sync_upstream.py")
    print("\nnext: sync_upstream.py, check_links.py, audit_consistency.py "
          "(see docstring).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
