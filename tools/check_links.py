"""Quarterly link checker: every external URL in shipped data, threaded.

Classifies: OK, MOVED (cross-host redirect: portal migrations!), BROKEN (404/410),
BLOCKED (403/429/proxy: inconclusive), UNREACHABLE (timeout/DNS). Exit 1 only when
BROKEN links exist. Network only runs inside main().

Usage: python tools/check_links.py [--limit N] [--only substring]
"""
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ms.labidi.eu link checker"
TIMEOUT = 15
SAME_FAMILY = {  # redirect targets that do not count as a move
    "login.microsoftonline.com", "login.microsoft.com", "aka.ms",
    "learn.microsoft.com", "go.microsoft.com",
}


def is_auth_wall(host):
    return host.startswith("login.") or host.startswith("adfs.")


def collect_urls():
    urls = {}
    for path in sorted((ROOT / "data").glob("*.js")):
        text = path.read_text(encoding="utf-8")
        m = re.search(r"concat\((\[.*\])\);", text, re.S) or \
            re.search(r"=(\[.*\]);", text, re.S)
        if not m:
            continue
        for row in json.loads(m.group(1)):
            for field in ("url", "docs"):
                val = row.get(field)
                if val and val.startswith("http"):
                    urls.setdefault(val, []).append(f"{row['id']}.{field}")
            for cloud_url in (row.get("clouds") or {}).values():
                urls.setdefault(cloud_url, []).append(f"{row['id']}.clouds")
    return urls


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            final_host = urlsplit(res.url).netloc.lower()
            orig_host = urlsplit(url).netloc.lower()
            if is_auth_wall(final_host):
                return ("OK", "auth wall (portal exists)")
            if final_host != orig_host and final_host not in SAME_FAMILY:
                return ("MOVED", f"-> {res.url[:90]}")
            return ("OK", str(res.status))
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return ("BROKEN", str(e.code))
        if e.code in (401, 403, 429):
            return ("BLOCKED", str(e.code))
        return ("ERROR", str(e.code))
    except Exception as e:  # noqa: BLE001 - report tool
        return ("UNREACHABLE", str(e)[:60])


def main(argv):
    limit = 0
    only = ""
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    if "--only" in argv:
        only = argv[argv.index("--only") + 1]
    urls = collect_urls()
    todo = sorted(u for u in urls if only in u)
    if limit:
        todo = todo[:limit]
    print(f"checking {len(todo)} of {len(urls)} unique URLs...")
    results = {}
    with ThreadPoolExecutor(max_workers=12) as pool:
        for url, res in zip(todo, pool.map(probe, todo)):
            results.setdefault(res[0], []).append((url, res[1]))
    for status in ("BROKEN", "MOVED", "ERROR", "UNREACHABLE", "BLOCKED"):
        rows = results.get(status, [])
        if not rows:
            continue
        print(f"\n== {status} ({len(rows)}) ==")
        for url, detail in sorted(rows):
            refs = ", ".join(urls[url][:4])
            print(f"  {url}\n    {detail}  [{refs}]")
    ok = len(results.get("OK", []))
    print(f"\nOK: {ok}/{len(todo)}")
    return 1 if results.get("BROKEN") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
