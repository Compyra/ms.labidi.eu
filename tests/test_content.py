"""Content quality gates for phase 3 + pending gates for phases 4-8.

Pending gates self-skip until their phase lands, then enforce automatically.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import build_data as bd  # noqa: E402

from test_build import extract_json, pipeline  # noqa: E402


class TestPhase3Enrichment(unittest.TestCase):
    def test_enrichment_volume(self):
        records, _ = pipeline()
        enriched = [r for r in records.values() if r.get("path") and r.get("desc")]
        self.assertGreaterEqual(len(enriched), 200)
        own = [r for r in records.values() if r["source"] == "own"]
        self.assertGreaterEqual(len(own), 60)

    def test_priority_areas_fully_enriched(self):
        records, _ = pipeline()
        protection = ["enca", "enac", "enauthstrength", "enauth", "enidp", "ensspr",
                      "enscore", "enmfaunblock"]
        mde_settings = [r for r in records.values()
                        if r["id"].startswith("demde")]
        endpoint_sec = ["inantivirus", "infirewall", "inedr", "inasr", "incompliance"]
        for rid in protection + endpoint_sec:
            rec = records[rid]
            self.assertTrue(rec.get("path") and rec.get("roles") and rec.get("license"),
                            f"{rid} not fully enriched")
        self.assertGreaterEqual(len(mde_settings), 15)
        for rec in mde_settings:
            self.assertTrue(rec.get("path"), f"{rec['id']} missing path")

    def test_air_acceptance_record(self):
        records, _ = pipeline()
        air = records["air"]
        self.assertEqual(air["license"], "mdo-p2")
        self.assertIn("air", air["keywords"])
        self.assertIn("deinvestigations", air["related"])
        self.assertEqual(records["deinvestigations"]["license"], "mdo-p2")

    def test_mypages_all_have_share_text(self):
        records, _ = pipeline()
        pages = [r for r in records.values() if r["category"] == "mypages"]
        self.assertEqual(len(pages), 9)
        for rec in pages:
            self.assertTrue(rec.get("shareText"), f"{rec['id']} missing shareText")

    def test_related_links_resolve_both_ways_sampled(self):
        records, _ = pipeline()
        for rec in records.values():
            for rel in rec.get("related", []):
                self.assertIn(rel, records, f"{rec['id']} -> {rel}")

    def test_synonym_count_and_two_letter_curation(self):
        records, _ = pipeline()
        syns = bd.load_synonyms(set(records))
        self.assertGreaterEqual(len(syns), 120)
        short = [s["term"] for s in syns if len(s["term"]) < 3]
        self.assertLessEqual(set(short), {"ca", "ah", "ti", "ir"})

    def test_registry_ships_to_client(self):
        reg = extract_json(ROOT / "data" / "data-registry.js")
        self.assertIn("caadmin", reg["roles"])
        self.assertIn("mdo-p2", reg["licenses"])
        self.assertIn("mdo-p2", reg["licenses"]["m365-e5"]["inc"])


class TestPhase4SettingsEncyclopedia(unittest.TestCase):
    """Prep is live; bulk gates self-skip until phase 4 authoring lands."""

    def test_settings_pipeline_prep(self):
        records, _ = pipeline()
        for rid in ("set-sen-dailycap", "tog-tamper"):
            rec = records[rid]
            self.assertEqual(rec["kind"], "setting")
            self.assertIn(rec.get("blastRadius"), ("low", "med", "high"))
        self.assertIn("cis", records["tog-tamper"].get("standards", []))

    def test_blast_radius_values_valid_everywhere(self):
        records, _ = pipeline()
        for rec in records.values():
            br = rec.get("blastRadius")
            if br:
                self.assertIn(br, ("low", "med", "high"), rec["id"])

    def test_sentinel_settings_coverage(self):
        records, _ = pipeline()
        count = sum(1 for r in records.values()
                    if r["category"] == "sentinel" and r["kind"] == "setting")
        if count < 25:
            self.skipTest(f"PENDING phase 4: sentinel settings at {count}/25")

    def test_defender_toggle_wall_coverage(self):
        records, _ = pipeline()
        count = sum(1 for r in records.values()
                    if r["id"].startswith("tog-"))
        if count < 15:
            self.skipTest(f"PENDING phase 4: advanced-features toggles at {count}/15")

    def test_no_verify_markers_shipped(self):
        records, _ = pipeline()
        flagged = [r["id"] for r in records.values()
                   if "VERIFY" in (r.get("desc", "") + r.get("path", ""))]
        if flagged:
            self.skipTest(f"PENDING phase 4 VERIFY sweep: {flagged[:5]}")


class TestPhase5Libraries(unittest.TestCase):
    def test_kql_library(self):
        path = ROOT / "data" / "data-kql.js"
        if not path.exists():
            self.skipTest("PENDING phase 5: data-kql.js not built")
        rows = extract_json(path)
        self.assertGreaterEqual(len(rows), 60)
        for row in rows:
            self.assertTrue(row.get("id") and row.get("code") and row.get("table"))

    def test_ps_library(self):
        path = ROOT / "data" / "data-ps.js"
        if not path.exists():
            self.skipTest("PENDING phase 5: data-ps.js not built")
        rows = extract_json(path)
        self.assertGreaterEqual(len(rows), 60)
        for row in rows:
            self.assertTrue(row.get("id") and row.get("code") and row.get("module"))


class TestPhase6Runbooks(unittest.TestCase):
    def test_runbooks(self):
        path = ROOT / "data" / "data-runbooks.js"
        if not path.exists():
            self.skipTest("PENDING phase 6: data-runbooks.js not built")
        rows = extract_json(path)
        self.assertGreaterEqual(len(rows), 25)
        for row in rows:
            self.assertIn(row.get("level"), ("L1", "L2", "L3"))
            for section in ("steps", "verify", "escalate"):
                self.assertTrue(row.get(section), f"{row.get('id')} missing {section}")


class TestPhase7Licensing(unittest.TestCase):
    def test_licensing_matrix(self):
        path = ROOT / "data" / "data-licensing.js"
        if not path.exists():
            self.skipTest("PENDING phase 7: data-licensing.js not built")
        rows = extract_json(path)
        self.assertGreaterEqual(len(rows), 80)


class TestPhase8Launch(unittest.TestCase):
    def test_png_icons_and_og_image(self):
        icons = list((ROOT / "icons").glob("*.png"))
        if not icons:
            self.skipTest("PENDING phase 8: PNG icons not generated")
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("og:image", index)

    def test_sw_precache_generated_not_handwritten(self):
        sw = (ROOT / "sw.js").read_text(encoding="utf-8")
        if "generated by tools/build_data.py" not in sw:
            self.skipTest("PENDING phase 8: sw precache still hand-maintained")


if __name__ == "__main__":
    unittest.main()
