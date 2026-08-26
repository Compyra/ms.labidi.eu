"""Pipeline + generated-output invariants for phases 0-2 (stdlib only).

Run: python -m unittest discover -s tests -v
"""
import json
import re
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_data as bd  # noqa: E402

_records = None
_registries = None


def pipeline():
    global _records, _registries
    if _records is None:
        bd.errors.clear()
        bd.warnings.clear()
        _records = bd.load_upstream()
        bd.load_enrich(_records)
        bd.apply_overrides(_records)
        _registries = bd.load_full_registries()
        bd.validate(_records, set(_registries["roles"]), set(_registries["licenses"]))
    return _records, _registries


def extract_json(js_path):
    text = js_path.read_bytes().decode("utf-8")
    m = re.search(r"\.concat\((\[.*\])\);\s*$", text, re.S) or \
        re.search(r"=(\[.*\]|\{.*\});\s*$", text, re.S)
    return json.loads(m.group(1))


class TestPhase0Sources(unittest.TestCase):
    def test_vendor_matches_meta(self):
        meta = json.loads((ROOT / "vendor" / "cmdms-commands.meta.json").read_bytes())
        raw = (ROOT / "vendor" / "cmdms-commands.csv").read_bytes()
        self.assertEqual(len(raw), meta["bytes"])
        self.assertEqual(len(bd.read_csv(ROOT / "vendor" / "cmdms-commands.csv")),
                         meta["rows"])

    def test_registries_parse_and_bundle_links_resolve(self):
        _, reg = pipeline()
        self.assertGreaterEqual(len(reg["roles"]), 50)
        self.assertGreaterEqual(len(reg["licenses"]), 38)
        for lid, entry in reg["licenses"].items():
            for inc in entry["inc"]:
                self.assertIn(inc, reg["licenses"], f"{lid} includes unknown {inc}")

    def test_docs_and_license_files_exist(self):
        for name in ["PLAN.md", "LICENSE", "todo.md", "README.md"]:
            self.assertTrue((ROOT / name).is_file(), name)
        numbered = sorted(p.name[:2] for p in (ROOT / "docs").glob("[0-9][0-9]-*.md"))
        self.assertGreaterEqual(len(numbered), 17)
        self.assertEqual(numbered, [f"{i:02d}" for i in range(len(numbered))],
                         "docs must be numbered sequentially with no gaps or duplicates")


class TestPhase1Pipeline(unittest.TestCase):
    def test_validation_is_clean(self):
        pipeline()
        self.assertEqual(bd.errors, [])

    def test_upstream_import_and_folds(self):
        records, _ = pipeline()
        cmdms = [r for r in records.values() if r["source"] == "cmdms"]
        self.assertEqual(len(cmdms), 306)
        defender = records["defender"]
        self.assertEqual(defender["clouds"]["gcch"], "https://security.microsoft.us")
        self.assertEqual(defender["aliasClouds"]["defenderg"], "gcch")
        for kept in ("enpimg", "azpg", "azpgh"):
            self.assertIn(kept, records, f"heuristic exception {kept} must survive")
        self.assertEqual(set(records["ppage"]["clouds"]) , {"gcc", "gcch"})

    def test_every_upstream_command_resolvable(self):
        records, _ = pipeline()
        names = set(records)
        for rec in records.values():
            names.update(rec["aliases"])
        for row in bd.read_csv(ROOT / "vendor" / "cmdms-commands.csv"):
            rid = row["Command"].strip().lower()
            self.assertIn(rid, names, f"upstream {rid} lost")

    def test_ids_and_aliases_unique(self):
        records, _ = pipeline()
        seen = {}
        for rec in records.values():
            for alias in rec["aliases"]:
                self.assertNotIn(alias, records, f"alias {alias} shadows id")
                self.assertNotIn(alias, seen,
                                 f"alias {alias}: {seen.get(alias)} vs {rec['id']}")
                seen[alias] = rec["id"]

    def test_synonym_boosts_resolve(self):
        records, _ = pipeline()
        for syn in bd.load_synonyms(set(records)):
            for b in syn["boostIds"]:
                self.assertIn(b, records)


class TestGeneratedOutput(unittest.TestCase):
    def test_build_is_deterministic_and_clean(self):
        def run():
            res = subprocess.run([sys.executable, str(ROOT / "tools" / "build_data.py")],
                                 capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            return {p.name: sha256(p.read_bytes()).hexdigest()
                    for p in (ROOT / "data").glob("*.js")}
        first, second = run(), run()
        self.assertEqual(first, second)

    def test_emitted_files_are_lf_utf8_json(self):
        for p in (ROOT / "data").glob("*.js"):
            raw = p.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), f"{p.name} has BOM")
            self.assertNotIn(b"\r\n", raw, f"{p.name} has CRLF")
            extract_json(p)

    def test_asset_versions_in_lockstep(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        sw = (ROOT / "sw.js").read_text(encoding="utf-8")
        notfound = (ROOT / "404.html").read_text(encoding="utf-8")
        versions = set(re.findall(r"\?v=(\d+)", index + sw + notfound))
        self.assertEqual(len(versions), 1, f"mixed versions: {versions}")
        v = versions.pop()
        self.assertIn(f'CACHE = "mshub-v{v}"', sw)
        for src in re.findall(r'src="(data/[^"?]+)\?v=\d+"', index):
            self.assertIn(f"{src}?v={v}", sw, f"{src} missing from SW precache")
        for emitted in (ROOT / "data").glob("*.js"):
            self.assertIn(f'data/{emitted.name}?v={v}', index,
                          f"{emitted.name} generated but not loaded by index.html")

    def test_selftest_harness_loads_all_data(self):
        harness = (ROOT / "dev" / "selftest.html").read_text(encoding="utf-8")
        for emitted in (ROOT / "data").glob("*.js"):
            self.assertIn(f"../data/{emitted.name}", harness,
                          f"{emitted.name} missing from the selftest harness")

    def test_meta_counts_match_records(self):
        records, _ = pipeline()
        meta = extract_json(ROOT / "data" / "data-meta.js")
        self.assertEqual(meta["records"], len(records))
        self.assertEqual(sum(meta["counts"].values()), len(records))


if __name__ == "__main__":
    unittest.main()
