"""Fetch the current upstream cmd.ms CSV and diff it against the vendor pin.

Never writes anything: prints added/removed/changed rows so a human decides
what to import (per docs/12: never auto-merge). Network only inside main().

Usage: python tools/sync_upstream.py
"""
import csv
import io
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ms.labidi.eu upstream sync"


def load_meta():
    return json.loads((ROOT / "vendor" / "cmdms-commands.meta.json").read_bytes())


def raw_url(meta):
    repo = meta["source"].rstrip("/").replace("https://github.com/", "")
    return f"https://raw.githubusercontent.com/{repo}/main/{meta['file']}"


def rows_by_command(text):
    return {r["Command"].strip().lower(): r
            for r in csv.DictReader(io.StringIO(text)) if r.get("Command")}


def main():
    meta = load_meta()
    url = raw_url(meta)
    print(f"pin: commit {meta['commit'][:7]} ({meta['committedAt']}, "
          f"{meta['rows']} rows, fetched {meta['fetchedAt']})")
    print(f"fetching {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            fresh_text = res.read().decode("utf-8-sig")
    except Exception as e:  # noqa: BLE001 - report tool
        print(f"FETCH FAILED: {e}\nIf the path moved, fix 'file' in "
              "vendor/cmdms-commands.meta.json.")
        return 2
    pinned = rows_by_command(
        (ROOT / "vendor" / "cmdms-commands.csv").read_bytes().decode("utf-8-sig"))
    fresh = rows_by_command(fresh_text)
    added = sorted(set(fresh) - set(pinned))
    removed = sorted(set(pinned) - set(fresh))
    changed = []
    for cid in sorted(set(fresh) & set(pinned)):
        diffs = [f"{k}: {pinned[cid].get(k, '')!r} -> {fresh[cid].get(k, '')!r}"
                 for k in ("Url", "Description", "Category", "Alias", "Keywords")
                 if (pinned[cid].get(k) or "") != (fresh[cid].get(k) or "")]
        if diffs:
            changed.append((cid, diffs))
    print(f"\nupstream now: {len(fresh)} rows (pin: {len(pinned)})")
    if added:
        print(f"\n== ADDED upstream ({len(added)}) ==")
        for cid in added:
            print(f"  {cid}: {fresh[cid].get('Description', '')[:70]}")
    if removed:
        print(f"\n== REMOVED upstream ({len(removed)}) == (check our overrides/folds)")
        for cid in removed:
            print(f"  {cid}")
    if changed:
        print(f"\n== CHANGED upstream ({len(changed)}) ==")
        for cid, diffs in changed:
            print(f"  {cid}")
            for d in diffs:
                print(f"    {d}")
    if not (added or removed or changed):
        print("\nno upstream drift: pin is current.")
    print("\nTo adopt changes: refresh vendor/cmdms-commands.csv + meta.json "
          "manually, review overrides.csv, run the build and full tests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
