"""Regression tests for monetary validation and fail-closed tax metadata."""
import datetime as dt
import copy
import json
from pathlib import Path
import sys
import unittest
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/orchestrator/scripts"))
import check_freshness as freshness
import otd_calculator as otd


class MoneyValidationTests(unittest.TestCase):
    def test_nonfinite_and_negative_money_rejected(self):
        for value in (float("nan"), float("inf"), -1, True, -0.01):
            with self.subTest(value=value), self.assertRaises(ValueError):
                otd.compute_otd(value, 0, 0.06, 0, 0)

    def test_fractional_cent_input_rejected(self):
        with self.assertRaises(ValueError):
            otd.compute_otd(100.001, 0, 0.06, 0, 0)

    def test_half_cent_tax_uses_decimal_half_up(self):
        result = otd.compute_otd(0.10, 0, 0.05, 0, 0)
        self.assertEqual(result["tax"], Decimal("0.01"))
        self.assertEqual(result["otd"], Decimal("0.11"))

    def test_impossible_reverse_target_rejected(self):
        with self.assertRaises(ValueError):
            otd.reverse_otd(10, 100, 0.06, 50, 20)


class ProvenanceRegressionTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "data/state_fees.json").read_text(encoding="utf-8"))

    def test_empty_duplicate_and_nonrecord_datasets_fail_schema(self):
        for records in ([], self.data["states"] + [self.data["states"][0]], [None]):
            with self.subTest(records=len(records)):
                data = copy.deepcopy(self.data)
                data["states"] = records
                self.assertTrue(freshness.validate_dataset(data))

    def test_nonfinite_negative_and_boolean_reference_values_fail_schema(self):
        for field, value in (("tax_state", float("nan")), ("tax_state", 2), ("title", -1), ("doc_cap", True)):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data["states"][0][field] = value
                self.assertTrue(freshness.validate_dataset(data))

    def test_calculator_rule_schema_cannot_skip_evidence(self):
        data = copy.deepcopy(self.data)
        md = next(r for r in data["states"] if r["state"] == "MD")
        md["calculator"]["required_fields"] = []
        self.assertTrue(freshness.validate_dataset(data))

    def test_state_specific_rules_and_supporting_sources_are_validated(self):
        changes = (
            ("CT", lambda r: r["tax_rules"].update(luxury_rate=float("nan"))),
            ("CT", lambda r: r["tax_rules"].pop("luxury_rate")),
            ("NJ", lambda r: r["tax_rules"].update(conditions="used")),
            ("NY", lambda r: r["field_provenance"]["tax_rules"]["supporting_sources"][0].update(source_url="")),
            ("MI", lambda r: r["trade_credit"]["annual_schedule"].update(yearly_increase=-1)),
            ("MI", lambda r: r["trade_credit"].update(cap=13000)),
        )
        for state, edit in changes:
            with self.subTest(state=state):
                data = copy.deepcopy(self.data)
                rec = next(r for r in data["states"] if r["state"] == state)
                edit(rec)
                # Matching copied values must not conceal an invalid rule shape.
                for field in ("tax_rules", "trade_credit"):
                    if field in rec:
                        rec["field_provenance"][field]["value"] = copy.deepcopy(rec[field])
                self.assertTrue(freshness.validate_dataset(data))

    def test_supporting_source_failure_blocks_runtime_evidence(self):
        ny = next(r for r in self.data["states"] if r["state"] == "NY")
        ny["field_provenance"]["tax_rules"]["supporting_sources"][0]["source_quote"] = ""
        status, _ = freshness.assess_field(ny, "tax_rules", dt.date(2026, 9, 22))
        self.assertEqual(status, "invalid")

    def test_changed_value_and_missing_source_invalidate_evidence(self):
        md = next(r for r in self.data["states"] if r["state"] == "MD")
        for edit in (lambda r: r.update(tax_state=0.06), lambda r: r["field_provenance"]["tax_state"].update(source_url="")):
            rec = copy.deepcopy(md)
            edit(rec)
            status, _ = freshness.assess_field(rec, "tax_state", dt.date(2026, 9, 22))
            self.assertNotEqual(status, "fresh")

    def test_stale_field_cannot_authorize_calculation(self):
        md = next(r for r in self.data["states"] if r["state"] == "MD")
        with self.assertRaisesRegex(ValueError, "Recheck"):
            freshness.require_fields(md, ["tax_state"], today=dt.date(2027, 1, 1))

    def test_md_current_tax_and_title(self):
        states = {r["state"]: r for r in json.loads((ROOT / "data/state_fees.json").read_text(encoding="utf-8"))["states"]}
        self.assertEqual(states["MD"]["tax_state"], 0.065)
        self.assertEqual(states["MD"]["title"], 200)

    def test_record_boolean_cannot_replace_field_evidence(self):
        rec = {"state": "MD", "verified": True, "source_verified_date": "2026-06-22"}
        status, _ = freshness.assess_record(rec, dt.date(2026, 9, 22), 12)
        self.assertNotEqual(status, "fresh")

    def test_future_verification_date_never_fresh(self):
        rec = {"state": "MD", "verified": True, "source_verified_date": "2027-01-01"}
        status, _ = freshness.assess_record(rec, dt.date(2026, 9, 22), 12)
        self.assertNotEqual(status, "fresh")


if __name__ == "__main__":
    unittest.main()
