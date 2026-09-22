"""Keep shipped tax reference tables and field provenance consistent."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/orchestrator/scripts"
sys.path.insert(0, str(SCRIPTS))
import check_freshness as freshness
import render_state_data as renderer


class StateDataIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "data/state_fees.json").read_text(encoding="utf-8"))
        cls.states = {r["state"]: r for r in cls.data["states"]}

    def test_all_51_states_and_schema(self):
        self.assertEqual(set(self.states), freshness.STATE_CODES)
        self.assertEqual(freshness.validate_dataset(self.data), [])

    def test_generated_reference_surfaces_match(self):
        table = renderer.render_table(self.data["states"])
        for path in renderer.SURFACES:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(text, renderer.replace_table(text, table))

    def test_unknown_caps_are_not_rendered_as_no_cap(self):
        for state in ("NJ", "VA", "NC", "TX"):
            with self.subTest(state=state):
                self.assertIsNone(self.states[state]["doc_cap"])
                self.assertEqual(self.states[state]["field_provenance"]["doc_cap"]["status"], "unverified")
                self.assertEqual(renderer.reviewed(self.states[state], "doc_cap", renderer.fmt_cap), "Unverified")

    def test_legacy_verification_claims_do_not_survive_as_current_proof(self):
        for rec in self.states.values():
            if rec["verified"]:
                self.assertTrue(all(rec["field_provenance"][field]["status"] == "verified" for field in freshness.REFERENCE_FIELDS))
            else:
                self.assertIsNone(rec["source_verified_date"])

    def test_md_correct_values_have_distinct_field_evidence(self):
        md = self.states["MD"]
        self.assertEqual(md["tax_state"], 0.065)
        self.assertEqual(md["title"], 200)
        self.assertEqual(md["doc_cap"], 800)
        self.assertEqual(md["field_provenance"]["tax_state"]["effective_from"], "2025-07-01")
        self.assertEqual(md["field_provenance"]["title"]["effective_from"], "2025-07-01")
        self.assertEqual(md["field_provenance"]["doc_cap"]["effective_from"], "2024-07-01")

    def test_fixture_generator_reproduces_tax_oracles(self):
        sys.path.insert(0, str(ROOT / "tools"))
        import make_fixtures
        payload = make_fixtures.build()["eval/golden/otd_cases.json"]
        self.assertEqual((ROOT / "eval/golden/otd_cases.json").read_bytes().replace(b"\r\n", b"\n"), payload.replace(b"\r\n", b"\n"))

    def test_installed_path_resolution_matches_real_data(self):
        self.assertEqual(freshness.DEFAULT_JSON, ROOT / "data/state_fees.json")
        self.assertEqual(renderer.DEFAULT_JSON, ROOT / "data/state_fees.json")


if __name__ == "__main__":
    unittest.main()
