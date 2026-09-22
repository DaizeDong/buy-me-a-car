"""Dossier financial, evidence, HTML safety, and PDF regression tests."""
import importlib.util
import copy
from datetime import date
import json
import hashlib
import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/orchestrator/scripts/generate_dossier.py"
ASSETS = ROOT / "skills/orchestrator/assets"
spec = importlib.util.spec_from_file_location("generate_dossier", SCRIPT)
dossier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dossier)
sys.path.insert(0, str(ROOT))
from tools.fixture_recipes.dossier import demo_config
from tools import runtime_paths


class DossierRegressionTests(unittest.TestCase):
    def test_inconsistent_offer_is_rejected(self):
        config = demo_config()
        config.update(PROPOSED_SALES="1", TAX_AMOUNT="999999", TARGET_OTD="30000")
        errors = dossier.validate_config_sanity(config)
        self.assertTrue(any("offer components total" in error for error in errors), errors)

    def test_empty_competitor_prices_are_rejected(self):
        config = demo_config()
        for quote in config["QUOTES"]:
            quote["otd"] = ""
        self.assertTrue(any("otd" in error for error in dossier.validate_config_sanity(config)))

    def test_generated_example_has_consistent_arithmetic_and_complete_sources(self):
        self.assertEqual(dossier.validate_config_sanity(demo_config()), [])

    def test_tax_half_cent_rounds_up_and_trade_reduces_total(self):
        config = demo_config()
        config.update(PROPOSED_SALES="100.05", TAX_BASE="100.05", TAX_RATE="10", TAX_AMOUNT="10.01",
                      REG_AMOUNT="0", TITLE_AMOUNT="0", TRADE_IN_CREDIT="10", TARGET_OTD="100.06")
        self.assertEqual(dossier.validate_config_sanity(config), [])
        config["TAX_AMOUNT"] = "10.00"
        errors = dossier.validate_config_sanity(config)
        self.assertTrue(any("rounded TAX_BASE" in error for error in errors), errors)

    def test_malformed_money_is_rejected(self):
        for value in ("NaN", "Infinity", "1e3", "-1", "1,00", "0.001", True, [], "$30,000"):
            with self.subTest(value=value):
                config = demo_config()
                config["TARGET_OTD"] = value
                self.assertTrue(any("TARGET_OTD" in error for error in dossier.validate_config_sanity(config)))

    def test_all_quote_columns_are_required(self):
        for key in ("vehicle", "vehicle_id", "dealer", "mileage", "source_id", "otd", "status", "registration_state", "conditions", "expires_on"):
            with self.subTest(key=key):
                config = demo_config()
                del config["QUOTES"][0][key]
                self.assertTrue(dossier.validate_config_sanity(config))

    def test_quote_tax_jurisdiction_and_expiration_are_checked(self):
        for updates in ({"registration_state": "CA"}, {"expires_on": "2026-09-01"}):
            config = demo_config()
            config["QUOTES"][0].update(updates)
            self.assertTrue(dossier.validate_config_sanity(config))

    def test_duplicate_quotes_do_not_inflate_comparison_count(self):
        config = demo_config()
        config["QUOTES"][1].update(vehicle=config["QUOTES"][0]["vehicle"], dealer=config["QUOTES"][0]["dealer"])
        self.assertTrue(any("duplicate" in error for error in dossier.validate_config_sanity(config)))

    def test_missing_future_and_unbound_evidence_fail(self):
        for mutate in (lambda c: c.update(EVIDENCE=[]),
                       lambda c: c["EVIDENCE"][0].update(source_date="2099-01-01"),
                       lambda c: c["EVIDENCE"][0].update(supports=["quote:unknown"])):
            config = demo_config()
            mutate(config)
            self.assertTrue(dossier.validate_config_sanity(config))

    def test_inherited_synthetic_claims_cannot_be_live(self):
        config = demo_config()
        config.update(DOSSIER_MODE="live", SYNTHETIC=False, DATE=date.today().isoformat())
        errors = dossier.validate_config_sanity(config)
        self.assertTrue(any("inherited synthetic" in error for error in errors), errors)

    def test_demo_rejects_custom_personal_content(self):
        config = demo_config()
        config["BUYER_NAME"] = "User provided text"
        with self.assertRaisesRegex(ValueError, "only generated synthetic"):
            dossier._demo_config_allowed(config)

    def test_malformed_structures_return_validation_errors(self):
        for mutate in (lambda c: c["EVIDENCE"][0].update(supports=None),
                       lambda c: c["QUOTES"][0].update(source_id=[]),
                       lambda c: c.update({1: "invalid key"})):
            config = demo_config()
            mutate(config)
            self.assertTrue(dossier.validate_config_sanity(config))

    def test_all_quotes_and_source_dates_are_rendered(self):
        config = demo_config()
        quote = copy.deepcopy(config["QUOTES"][0])
        quote.update(id="third", vehicle="Third fictional vehicle")
        config["QUOTES"].append(quote)
        config["EVIDENCE"][0]["supports"].append("quote:third")
        result = dossier.render_dossier((ASSETS / "dossier_template.html").read_text(encoding="utf-8"), config)
        self.assertIn("Third fictional vehicle", result)
        self.assertIn("2026-09-22", result)
        self.assertIn("SYNTHETIC DEMO", result)
        self.assertNotIn("{{", result)

    def test_text_is_escaped_and_template_markup_remains(self):
        result, missing, _ = dossier.substitute("<p><strong>{{TEXT}}</strong></p>",
                                               {"TEXT": '<img src=x onerror="alert(1)">'})
        self.assertEqual(missing, set())
        self.assertIn("<strong>&lt;img", result)
        self.assertNotIn("<img", result)

    def test_success_exit_without_new_pdf_cannot_accept_stale_output(self):
        with tempfile.TemporaryDirectory() as temp:
            html = Path(temp) / "input.html"
            pdf = Path(temp) / "output.pdf"
            html.write_text("<p>example</p>", encoding="utf-8")
            pdf.write_bytes(b"%PDF-1.7\nold output\n%%EOF\n")
            with patch.object(dossier, "find_chrome", return_value=("fake-chrome", "chromium")), \
                 patch.object(dossier.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, b"", b"")):
                with self.assertRaises((RuntimeError, SystemExit)):
                    dossier.html_to_pdf(html, pdf)
            self.assertEqual(pdf.read_bytes(), b"%PDF-1.7\nold output\n%%EOF\n")

    def test_pdf_failure_and_timeout_preserve_old_output(self):
        with tempfile.TemporaryDirectory() as temp:
            html_path = Path(temp) / "input with spaces.html"
            pdf_path = Path(temp) / "existing.pdf"
            html_path.write_text("<p>synthetic</p>", encoding="utf-8")
            pdf_path.write_bytes(b"old file")
            for response in (subprocess.CompletedProcess([], 1, b"", b"failed"),
                             subprocess.TimeoutExpired("fake-chrome", 1)):
                with self.subTest(response=response), \
                     patch.object(dossier, "find_chrome", return_value=("fake-chrome", "chromium")), \
                     patch.object(dossier.subprocess, "run", **({"side_effect": response} if isinstance(response, Exception) else {"return_value": response})):
                    with self.assertRaises(RuntimeError):
                        dossier.html_to_pdf(html_path, pdf_path, timeout=1)
                    self.assertEqual(pdf_path.read_bytes(), b"old file")

    def test_invalid_pdf_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.pdf"
            path.write_bytes(b"%PDF-1.7\n" + b"x" * 200 + b"\n%%EOF\n")
            with self.assertRaisesRegex(RuntimeError, "could not be parsed"):
                dossier._verify_pdf(path)

    def test_pdf_without_required_demo_notice_is_rejected(self):
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as temp:
            html_path = Path(temp) / "input.html"
            pdf_path = Path(temp) / "output.pdf"
            html_path.write_text('<div class="document-mode">SYNTHETIC DEMO</div>', encoding="utf-8")
            def fake_renderer(command, **kwargs):
                target = Path(next(arg.split("=", 1)[1] for arg in command if arg.startswith("--print-to-pdf=")))
                writer = PdfWriter()
                writer.add_blank_page(width=612, height=792)
                writer.write(target)
                return subprocess.CompletedProcess(command, 0, b"", b"")
            with patch.object(dossier, "find_chrome", return_value=("fake-chrome", "chromium")), \
                 patch.object(dossier.subprocess, "run", side_effect=fake_renderer):
                with self.assertRaisesRegex(RuntimeError, "notice"):
                    dossier.html_to_pdf(html_path, pdf_path)
            self.assertFalse(pdf_path.exists())

    def test_bad_explicit_browser_override_does_not_silently_fall_back(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(dossier.os.environ, {"CHROME_BIN": str(Path(temp) / "missing-browser")}):
            with self.assertRaisesRegex(ValueError, "CHROME_BIN"):
                dossier.find_chrome()

    def test_cli_requires_explicit_mode_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "result.html"
            result = subprocess.run([sys.executable, str(SCRIPT), "--config", str(ASSETS / "dossier_config_template.yaml"),
                                     "--output", str(output)], capture_output=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())


class LiveDossierBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.private_data = Path(self.temp.name) / "companion" / "data"
        self.private_data.mkdir(parents=True)
        # Mock only the external private-repository proof. Production path,
        # containment, file loading, hashing, validation, and rendering run.
        self.guard = patch.object(runtime_paths, "_guard_data_dir", return_value=self.private_data)
        self.proof = patch.object(runtime_paths, "_private_repo_identity", return_value="example/private-fixture")
        self.guard.start()
        self.proof.start()
        self.addCleanup(self.guard.stop)
        self.addCleanup(self.proof.stop)
        config = demo_config()
        for key, value in list(config.items()):
            if isinstance(value, str) and key not in dossier.MONEY_KEYS + ("TAX_ADJUSTMENT", "TAX_RATE", "YEAR", "MILES", "MSRP"):
                config[key] = "Recorded test input for " + key
        config.update(DOSSIER_MODE="live", SYNTHETIC=False, LANGUAGE="en", STATE="NY", DATE=date.today().isoformat())
        config["QUOTES"] = [dict(id=f"q{i}", vehicle=f"Test vehicle {i}", vehicle_id=f"TEST-{i}",
                                 dealer=f"Test dealer {i}", otd="30100.00", mileage="20000 miles", status="written_quote",
                                 registration_state="NY", conditions="Cash, no trade-in", expires_on=date.today().isoformat(), source_id="record")
                            for i in (1, 2)]
        evidence = self.private_data / "evidence" / "quote.json"
        evidence.parent.mkdir()
        evidence.write_text(json.dumps({"test_only": True, "recorded_values": config}), encoding="utf-8")
        config["EVIDENCE"] = [dict(id="record", kind="dealer_quote", source="https://dealer.invalid/quote", source_date=date.today().isoformat(),
                                   artifact="evidence/quote.json", sha256=hashlib.sha256(evidence.read_bytes()).hexdigest(),
                                   supports=list(config) + ["quote:q1", "quote:q2"])]
        self.config = config
        self.config_path = self.private_data / "config.json"
        self.config_path.write_text(json.dumps(config), encoding="utf-8")

    def run_cli(self, *args):
        argv = [str(SCRIPT), "--mode", "live", "--config", "config.json", "--output", "dossiers/result.html", *args]
        with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            dossier.main()

    def test_live_config_artifact_and_html_use_real_boundary_code(self):
        self.assertEqual(dossier.validate_config_sanity(self.config), [])
        self.run_cli()
        output = self.private_data / "dossiers" / "result.html"
        self.assertTrue(output.is_file())
        result = output.read_text(encoding="utf-8")
        self.assertIn("Test vehicle 1", result)
        self.assertIn("Written quote; evidence recorded", result)
        self.assertNotIn("{{", result)

    def test_missing_or_changed_source_artifact_blocks_output(self):
        artifact = self.private_data / "evidence" / "quote.json"
        for mutate in (lambda: artifact.write_text("changed", encoding="utf-8"), lambda: artifact.unlink()):
            mutate()
            with self.assertRaises(SystemExit) as raised:
                self.run_cli()
            self.assertNotEqual(raised.exception.code, 0)
            self.assertFalse((self.private_data / "dossiers" / "result.html").exists())

    def test_unproven_claim_and_stale_quote_block_output(self):
        for mutate in (lambda: self.config["EVIDENCE"][0]["supports"].remove("CPO_STATUS"),
                       lambda: self.config["EVIDENCE"][0].update(source_date="2000-01-01")):
            mutate()
            self.config_path.write_text(json.dumps(self.config), encoding="utf-8")
            with self.assertRaises(SystemExit):
                self.run_cli()
            self.assertFalse((self.private_data / "dossiers" / "result.html").exists())

    def test_live_cannot_write_outside_private_data(self):
        outside = Path(self.temp.name) / "outside.html"
        with self.assertRaises(SystemExit):
            self.run_cli("--output", str(outside))
        self.assertFalse(outside.exists())

    def test_live_cannot_read_config_outside_private_data(self):
        with self.assertRaises(SystemExit):
            self.run_cli("--config", str(ASSETS / "dossier_config_template.yaml"))
        self.assertFalse((self.private_data / "dossiers" / "result.html").exists())

    def test_live_evidence_cannot_escape_private_data(self):
        self.config["EVIDENCE"][0]["artifact"] = "../quote.json"
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.run_cli()
        self.assertFalse((self.private_data / "dossiers" / "result.html").exists())

    def test_actual_synthetic_leather_term_is_not_mistaken_for_demo(self):
        self.config["HIGHER_1"] = "Synthetic leather upholstery"
        self.assertEqual(dossier.validate_config_sanity(self.config), [])


if __name__ == "__main__":
    unittest.main()
