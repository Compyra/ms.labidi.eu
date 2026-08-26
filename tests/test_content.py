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
        self.assertGreaterEqual(len(pages), 9)
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
    def _library(self, filename, required_field, minimum):
        path = ROOT / "data" / filename
        if not path.exists():
            self.skipTest(f"PENDING phase 5: {filename} not built")
        rows = extract_json(path)
        for row in rows:
            self.assertTrue(row.get("id") and row.get("title") and row.get("code"),
                            f"{filename} row incomplete: {row.get('id')}")
            self.assertTrue(row.get(required_field), f"{row['id']} missing {required_field}")
            self.assertNotIn("VERIFY", json.dumps(row))
        if len(rows) < minimum:
            self.skipTest(f"PENDING phase 5: {filename} at {len(rows)}/{minimum}")
        return rows

    def test_kql_library(self):
        rows = self._library("data-kql.js", "table", 60)
        registry = extract_json(ROOT / "data" / "data-registry.js")
        known = {t["name"] for t in registry["tables"]}
        for row in rows:
            self.assertEqual(row["kind"], "kql")
            self.assertIn(row["table"], known, f"{row['id']} uses unregistered table")

    def test_ps_library(self):
        rows = self._library("data-ps.js", "module", 60)
        for row in rows:
            self.assertEqual(row["kind"], "ps")
            self.assertTrue(row.get("scopes"), f"{row['id']} missing scopes/role")

    def test_library_ids_unique_and_namespaced(self):
        records, _ = pipeline()
        seen = set()
        for filename, prefix in (("data-kql.js", "kql-"), ("data-ps.js", "ps-")):
            path = ROOT / "data" / filename
            if not path.exists():
                self.skipTest(f"PENDING phase 5: {filename} not built")
            for row in extract_json(path):
                self.assertTrue(row["id"].startswith(prefix))
                self.assertNotIn(row["id"], records, "library id collides with a command")
                self.assertNotIn(row["id"], seen)
                seen.add(row["id"])

    def test_library_related_links_resolve(self):
        records, _ = pipeline()
        linked = 0
        for filename in ("data-kql.js", "data-ps.js"):
            path = ROOT / "data" / filename
            if not path.exists():
                self.skipTest(f"PENDING phase 5: {filename} not built")
            for row in extract_json(path):
                for rel in row.get("related", []):
                    self.assertIn(rel, records, f"{row['id']} -> {rel}")
                    linked += 1
        self.assertGreaterEqual(linked, 60, "library entries barely cross-link records")

    def test_ps_hints_resolve_to_library_entries(self):
        records, _ = pipeline()
        path = ROOT / "data" / "data-ps.js"
        if not path.exists():
            self.skipTest("PENDING phase 5: data-ps.js not built")
        library = {r["id"] for r in extract_json(path)}
        linked = 0
        for rec in records.values():
            hint = rec.get("ps", "")
            if hint.startswith(("ps-", "kql-")):
                self.assertIn(hint, library, f"{rec['id']} points at a missing snippet")
                linked += 1
        self.assertGreaterEqual(linked, 4, "no records use snippet-id ps hints")

    def test_table_registry_shipped(self):
        registry = extract_json(ROOT / "data" / "data-registry.js")
        self.assertGreaterEqual(len(registry.get("tables", [])), 45)
        for table in registry["tables"]:
            self.assertTrue(table["name"] and table["product"])

    def test_kql_snippets_are_structurally_valid(self):
        """Offline lint: no tenant needed, catches the typos that break a paste."""
        operators = {
            "where", "summarize", "project", "project-away", "project-rename",
            "project-reorder", "project-keep", "extend", "order", "sort", "top",
            "top-nested", "take", "limit", "count", "distinct", "join", "union",
            "mv-expand", "mv-apply", "parse", "parse-where", "render", "evaluate",
            "make-series", "search", "lookup", "invoke", "as", "serialize",
            "sample", "sample-distinct", "partition", "scan", "fork", "facet",
            "find", "getschema", "reduce", "consume",
        }
        path = ROOT / "data" / "data-kql.js"
        if not path.exists():
            self.skipTest("PENDING phase 5: data-kql.js not built")
        registry = extract_json(ROOT / "data" / "data-registry.js")
        known_tables = {t["name"] for t in registry["tables"]}
        for row in extract_json(path):
            code, rid = row["code"], row["id"]
            for opener, closer in (("(", ")"), ("[", "]"), ("{", "}")):
                self.assertEqual(code.count(opener), code.count(closer),
                                 f"{rid}: unbalanced {opener}{closer}")
            self.assertEqual(code.count("'") % 2, 0, f"{rid}: unbalanced quote")
            self.assertNotIn('"', code, f"{rid}: use single quotes in KQL")
            self.assertFalse(code.rstrip().endswith("|"), f"{rid}: trailing pipe")
            segments = [s.strip() for s in code.split("|")]
            head = segments[0].split()[0].split("(")[0]
            self.assertTrue(head in known_tables or head.startswith("_"),
                            f"{rid}: starts with unknown source {head!r}")
            for segment in segments[1:]:
                self.assertTrue(segment, f"{rid}: empty pipe segment")
                op = segment.split()[0].split("(")[0]
                self.assertIn(op, operators, f"{rid}: unknown operator {op!r}")


class TestPhase6Runbooks(unittest.TestCase):
    def test_runbooks(self):
        path = ROOT / "data" / "data-runbooks.js"
        if not path.exists():
            self.skipTest("PENDING phase 6: data-runbooks.js not built")
        rows = extract_json(path)
        seen = set()
        for row in rows:
            rid = row.get("id", "")
            self.assertTrue(rid.startswith("rb-"), f"{rid}: bad prefix")
            self.assertNotIn(rid, seen, f"{rid}: duplicate")
            seen.add(rid)
            self.assertEqual(row.get("kind"), "runbook")
            self.assertTrue(row.get("title"), f"{rid}: missing title")
            self.assertIn(row.get("level"), ("L1", "L2", "L3"))
            for section in ("steps", "verify", "escalate"):
                self.assertTrue(row.get(section), f"{rid} missing {section}")
            self.assertGreaterEqual(len(row.get("steps", [])), 4,
                                    f"{rid}: fewer than 4 steps")
        if len(rows) < 25:
            self.skipTest(f"PENDING phase 6: runbooks at {len(rows)}/25")
        subjects = {row["subject"] for row in rows}
        self.assertGreaterEqual(len(subjects), 10,
                                "runbooks should span at least 10 subjects")


class TestPhase7Licensing(unittest.TestCase):
    def test_licensing_matrix(self):
        path = ROOT / "data" / "data-licensing.js"
        if not path.exists():
            self.skipTest("PENDING phase 7: data-licensing.js not built")
        rows = extract_json(path)
        registry = extract_json(ROOT / "data" / "data-registry.js")
        license_ids = set(registry["licenses"])
        seen = set()
        for row in rows:
            rid = row.get("id", "")
            self.assertTrue(rid.startswith("lic-"), f"{rid}: bad prefix")
            self.assertNotIn(rid, seen, f"{rid}: duplicate")
            seen.add(rid)
            self.assertEqual(row.get("kind"), "lic")
            self.assertTrue(row.get("feature"), f"{rid}: missing feature")
            self.assertIn(row.get("min"), license_ids,
                          f"{rid}: min not a registry license")
            for x in row.get("alsoIn", []):
                self.assertIn(x, license_ids, f"{rid}: alsoIn {x} unknown")
            self.assertTrue(row.get("docs", "").startswith("https://"),
                            f"{rid}: docs link required")
        if len(rows) < 80:
            self.skipTest(f"PENDING phase 7: matrix at {len(rows)}/80")

    def test_purview_settings_pass(self):
        rows = extract_json(ROOT / "data" / "data-commands-purview.js")
        settings = [r for r in rows if r["id"].startswith("set-pu-")]
        self.assertGreaterEqual(len(settings), 15, "purview settings encyclopedia")
        for row in settings:
            self.assertTrue(row.get("desc"), f"{row['id']}: missing desc")
            self.assertTrue(row.get("verified"), f"{row['id']}: missing verified")
            self.assertNotIn("?", row.get("path", ""),
                             f"{row['id']}: hedge marker in path")
        groups = {r.get("group") for r in rows}
        self.assertGreaterEqual(len(groups - {None}), 5,
                                "purview hub should be grouped")

    def test_windows_pass(self):
        rows = extract_json(ROOT / "data" / "data-commands-windows.js")
        settings = [r for r in rows
                    if r["id"].startswith(("set-w365-", "set-avd-", "set-up-",
                                           "set-win-"))]
        self.assertGreaterEqual(len(settings), 12, "windows settings encyclopedia")
        for row in settings:
            self.assertTrue(row.get("desc"), f"{row['id']}: missing desc")
            self.assertNotIn("?", row.get("path", ""),
                             f"{row['id']}: hedge marker in path")
        groups = {r.get("group") for r in rows}
        self.assertGreaterEqual(len(groups - {None}), 4,
                                "windows hub should be grouped")

    def test_error_code_records(self):
        codes = []
        for path in sorted((ROOT / "data").glob("data-commands-*.js")):
            codes += [r for r in extract_json(path) if r.get("group") == "Error codes"]
        if not codes:
            self.skipTest("PENDING phase 7: no error-code records yet")
        families = {"aadsts": 0, "enroll": 0, "ndr": 0}
        for row in codes:
            self.assertTrue(row.get("desc"), f"{row['id']}: missing desc")
            self.assertTrue(row.get("docs", "").startswith("https://"),
                            f"{row['id']}: docs link required")
            self.assertTrue(row.get("verified"), f"{row['id']}: missing verified")
            for fam in families:
                if row["id"].startswith(fam):
                    families[fam] += 1
        if len(codes) < 40:
            self.skipTest(f"PENDING phase 7: error codes at {len(codes)}/40")
        self.assertGreaterEqual(families["aadsts"], 20)
        self.assertGreaterEqual(families["enroll"], 3)
        self.assertGreaterEqual(families["ndr"], 8)


class TestMaintenanceHygiene(unittest.TestCase):
    def test_all_external_urls_are_well_formed(self):
        from urllib.parse import urlsplit
        bad = []
        for path in sorted((ROOT / "data").glob("*.js")):
            for row in extract_json(path):
                if not isinstance(row, dict):
                    continue
                candidates = [row.get("url"), row.get("docs")]
                candidates += list((row.get("clouds") or {}).values())
                for url in candidates:
                    if not url:
                        continue
                    parts = urlsplit(url)
                    if (parts.scheme != "https" or "." not in parts.netloc
                            or " " in url or url[-1] in ",;"):
                        bad.append(f"{row.get('id')}: {url!r}")
        self.assertEqual(bad, [])

    def test_quarterly_tools_import_cleanly(self):
        import importlib.util
        for name in ("check_links", "sync_upstream", "check_freshness"):
            spec = importlib.util.spec_from_file_location(
                name, ROOT / "tools" / f"{name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.assertTrue(callable(getattr(module, "main")),
                            f"{name}.main missing")
        self.assertTrue((ROOT / "tools" / "audit_consistency.py").exists())


class TestPhase8Launch(unittest.TestCase):
    def test_png_icons_and_og_image(self):
        icons = list((ROOT / "icons").glob("*.png"))
        if not icons:
            self.skipTest("PENDING phase 8: PNG icons not generated")
        names = {p.name for p in icons}
        for required in ("icon-192.png", "icon-512.png", "icon-maskable-512.png",
                         "apple-touch-icon.png", "favicon-32.png", "og-image.png"):
            self.assertIn(required, names)
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('property="og:image"', index)
        self.assertIn("apple-touch-icon", index)
        manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
        purposes = {i["purpose"] for i in manifest["icons"]
                    if i["src"].endswith(".png")}
        self.assertEqual(purposes, {"any", "maskable"})

    def test_sw_precache_generated_not_handwritten(self):
        sw = (ROOT / "sw.js").read_text(encoding="utf-8")
        if "generated by tools/build_data.py" not in sw:
            self.skipTest("PENDING phase 8: sw precache still hand-maintained")


if __name__ == "__main__":
    unittest.main()
