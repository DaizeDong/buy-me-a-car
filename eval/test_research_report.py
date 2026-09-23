"""Buyer research contracts, using generated fictional data only."""
import copy
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.fixture_recipes.research_report import build, demo_config
from tools import runtime_paths

SCRIPT = ROOT / "skills/orchestrator/scripts/generate_research_report.py"


class ResearchReportTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "Buyer research generator has not been implemented")
        spec = importlib.util.spec_from_file_location("research_report", SCRIPT)
        self.report = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.report)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def test_demo_cli_zero_quotes_has_substantive_numbered_sections(self):
        config = self.base / "generated.json"
        config.write_bytes(next(iter(build().values())))
        output = self.base / "report.html"
        result = subprocess.run([sys.executable, str(SCRIPT), "--mode", "demo", "--config", str(config),
                                 "--output", str(output)], capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        rendered = output.read_text(encoding="utf-8")
        self.assertGreaterEqual(rendered.count('<section id="section-'), 11)
        self.assertGreater(len(rendered), 12000)
        self.assertIn("0 份书面 OTD 报价", rendered)
        self.assertIn("挂牌价（非 OTD）", rendered)
        self.assertIn("内部买方研究", rendered)
        self.assertIn("counter(page)", rendered)
        self.assertNotIn("break-before: page", rendered)

    def test_demo_rejects_modified_data_in_imported_api(self):
        config = demo_config()
        config["title"] = "User supplied custom title"
        path = self.base / "input.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "generated synthetic"):
            self.report.generate_report(path, self.base / "output.html", mode="demo")
        with self.assertRaisesRegex(ValueError, "generated synthetic"):
            self.report.render_report(config, mode="demo")

    def live_config(self):
        private = self.base / "companion" / "data"
        private.mkdir(parents=True, exist_ok=True)
        guard = patch.object(runtime_paths, "_guard_data_dir", return_value=private)
        proof = patch.object(runtime_paths, "_private_repo_identity", return_value="example/private-fixture")
        guard.start()
        proof.start()
        self.addCleanup(guard.stop)
        self.addCleanup(proof.stop)
        config = demo_config()
        config.update(synthetic=False, date=date.today().isoformat())
        for source in config["sources"]:
            source["observed_date"] = config["date"]
            if source["status"] == "captured":
                artifact = private / "evidence" / (source["id"] + ".json")
                artifact.parent.mkdir(exist_ok=True)
                artifact.write_text(json.dumps({"synthetic_test_only": True, "source": source}), encoding="utf-8")
                source.update(artifact=str(artifact), sha256=hashlib.sha256(artifact.read_bytes()).hexdigest())
        path = private / "config.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        return config, path, private

    def test_live_imported_api_validates_input_output_and_artifact_paths(self):
        config, path, private = self.live_config()
        output = private / "reports" / "research.html"
        self.report.generate_report(path, output, mode="live")
        self.assertTrue(output.is_file())
        outside = self.base / "outside.json"
        outside.write_text(json.dumps(config), encoding="utf-8")
        for input_path, output_path in ((outside, output), (path, self.base / "outside.html")):
            with self.subTest(input_path=input_path, output_path=output_path), self.assertRaises(RuntimeError):
                self.report.generate_report(input_path, output_path, mode="live")
        config["sources"][0]["artifact"] = str(outside)
        with self.assertRaisesRegex((ValueError, RuntimeError), "private|DATA"):
            self.report.render_report(config, mode="live", config_path=path)

    def test_live_render_api_requires_private_config_and_matching_contents(self):
        config, path, private = self.live_config()
        with self.assertRaisesRegex(ValueError, "config_path"):
            self.report.render_report(config, mode="live")
        config["title"] = "Changed synthetic test input"
        with self.assertRaisesRegex(ValueError, "match"):
            self.report.render_report(config, mode="live", config_path=path)

    def test_hash_mismatch_and_unbound_refs_are_rejected(self):
        original, path, _ = self.live_config()
        mutations = [
            (lambda c: c["sources"][0].update(sha256="0" * 64), "SHA-256"),
            (lambda c: c["candidates"][0].update(source_id="missing"), "source"),
            (lambda c: c["sections"][0]["blocks"][0].update(refs=["candidate:missing"]), "reference"),
            (lambda c: c["sections"][0]["blocks"][0].update(refs=["section:missing"]), "reference"),
            (lambda c: c["coverage"][0].update(source_ids=["missing"]), "source"),
        ]
        for mutate, message in mutations:
            config = copy.deepcopy(original)
            mutate(config)
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.report.render_report(config, mode="live", config_path=path)

    def test_unknown_costs_are_retained_and_never_become_an_otd_total(self):
        config, path, _ = self.live_config()
        rendered = self.report.render_report(config, mode="live", config_path=path)
        self.assertIn("未知", rendered)
        self.assertIn("完整交付成本未知", rendered)
        self.assertIn("已填项目情景小计", rendered)
        self.assertNotIn("已知项目小计", rendered)
        self.assertNotIn("USD 0.00", rendered)
        self.assertNotIn("估计 OTD：", rendered)

    def test_all_untrusted_text_is_escaped_and_raw_html_blocks_rejected(self):
        config, path, _ = self.live_config()
        payload = '<img src=x onerror="alert(1)">'
        config["decision_summary"] = payload
        config["sections"][0]["blocks"][0]["text"] = payload
        config["candidates"][0]["location"] = payload
        path.write_text(json.dumps(config), encoding="utf-8")
        rendered = self.report.render_report(config, mode="live", config_path=path)
        self.assertIn("&lt;img", rendered)
        self.assertNotIn("<img", rendered)
        config["sections"][0]["blocks"] = [{"type": "html", "html": payload}]
        path.write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "block"):
            self.report.render_report(config, mode="live", config_path=path)

    def test_vin_dedup_retains_every_conflicting_offer_and_id(self):
        config, path, _ = self.live_config()
        self.assertEqual(config["candidates"][0]["vin"], config["candidates"][1]["vin"])
        groups = self.report.group_candidates(config["candidates"])
        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0]), 2)
        rendered = self.report.render_report(config, mode="live", config_path=path)
        self.assertIn("同一 VIN 的不同记录", rendered)
        for candidate in config["candidates"]:
            self.assertIn(f'id="candidate-{candidate["id"]}"', rendered)
        self.assertIn("USD 28,900.00", rendered)
        self.assertIn("USD 29,200.00", rendered)

    def test_blocked_source_is_visible_but_cannot_support_a_candidate(self):
        config, path, _ = self.live_config()
        rendered = self.report.render_report(config, mode="live", config_path=path)
        self.assertIn("访问受阻", rendered)
        config["candidates"][0]["source_id"] = "blocked-search"
        path.write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "captured"):
            self.report.render_report(config, mode="live", config_path=path)

    def test_empty_intake_or_undocumented_search_is_rejected(self):
        original, path, _ = self.live_config()
        for collection in ("criteria", "coverage"):
            config = copy.deepcopy(original)
            config[collection] = []
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.subTest(collection=collection), self.assertRaisesRegex(ValueError, collection):
                self.report.render_report(config, mode="live", config_path=path)

    def test_partial_coverage_is_explicit_and_blocked_evidence_cannot_support_analysis(self):
        config, path, _ = self.live_config()
        rendered = self.report.render_report(config, mode="live", config_path=path)
        self.assertIn("研究状态：证据覆盖尚不完整", rendered)
        section = next(row for row in config["sections"] if row["topic"] == "suitability")
        section["blocks"][0]["refs"] = ["source:blocked-search"]
        path.write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "uncaptured"):
            self.report.render_report(config, mode="live", config_path=path)

    def test_incomplete_sections_unknown_keys_and_invalid_amounts_fail_closed(self):
        original, path, _ = self.live_config()
        mutations = [lambda c: c["sections"].pop(),
                     lambda c: c.update(raw_html="<b>unsupported</b>"),
                     lambda c: c["candidates"][0].update(asking_price=True),
                     lambda c: c["costs"][0].update(transport="NaN"),
                     lambda c: c["sources"][0].update(url="javascript:alert(1)"),
                     lambda c: c["sections"][0]["blocks"][0].update(refs=[[]])]
        for mutate in mutations:
            config = copy.deepcopy(original)
            mutate(config)
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                self.report.render_report(config, mode="live", config_path=path)

    def test_written_quote_requires_its_own_captured_quote_source(self):
        config, path, _ = self.live_config()
        config["written_quotes"] = [{"id": "q1", "candidate_id": "offer-a", "otd": "31000.00",
                                      "currency": "USD", "source_id": "listing-a", "conditions": "Synthetic test only"}]
        path.write_text(json.dumps(config), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "dealer_quote"):
            self.report.render_report(config, mode="live", config_path=path)

    def test_demo_cannot_write_inside_public_repository(self):
        config = self.base / "generated.json"
        config.write_bytes(next(iter(build().values())))
        with self.assertRaisesRegex(ValueError, "public"):
            self.report.generate_report(config, ROOT / "report.html", mode="demo")

    def test_no_candidates_and_no_quotes_field_remains_an_honest_research_report(self):
        config, path, _ = self.live_config()
        config["candidates"] = []
        config["costs"] = []
        config.pop("written_quotes")
        for section in config["sections"]:
            for block in section["blocks"]:
                block["refs"] = [reference for reference in block.get("refs", []) if not reference.startswith("candidate:")]
        path.write_text(json.dumps(config), encoding="utf-8")
        rendered = self.report.render_report(config, mode="live", config_path=path)
        self.assertIn("尚无可列示的候选记录", rendered)
        self.assertIn("0 份书面 OTD 报价", rendered)
        self.assertEqual(rendered.count('<section id="section-'), 11)

    def test_output_cannot_overwrite_a_captured_source(self):
        config, path, _ = self.live_config()
        artifact = Path(config["sources"][0]["artifact"])
        previous = artifact.read_bytes()
        with self.assertRaisesRegex(ValueError, "paths must be different"):
            self.report.generate_report(path, artifact, mode="live")
        self.assertEqual(artifact.read_bytes(), previous)


if __name__ == "__main__":
    unittest.main()
