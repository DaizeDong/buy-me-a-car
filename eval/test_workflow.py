"""Offline replay, policy and crash tests; no Gmail connection is exercised."""

import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "skills/orchestrator/scripts"
sys.path.insert(0, str(SCRIPTS))
import email_policy
import inbox_state
from eval import test_rubric

FIXTURE = REPO / "eval/fixtures/workflow.json"


def corpus():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class TestEmailPolicy(unittest.TestCase):
    def setUp(self):
        data = corpus()
        self.policy, self.plan = data["policy"], data["plan"]
        self.now = datetime.fromisoformat(data["_meta"]["now"])

    def render(self):
        return email_policy.render_draft(self.plan, self.policy, now=self.now)

    def test_authorized_offer_is_distinct_from_private_ceiling(self):
        body = self.render()
        self.assertIn("$30,750.00", body)
        self.assertNotIn("31,500", body)
        result = email_policy.validate_draft(body, self.plan, self.policy, now=self.now)
        self.assertEqual(result["status"], "verified")
        self.assertFalse(result["send_authorized"])
        self.assertEqual(result["qualitative_review"], "unavailable")

    def test_unapproved_and_ceiling_offers_fail(self):
        for amount, approved in [("31500", True), ("32000", True), ("30750", False)]:
            with self.subTest(amount=amount, approved=approved):
                self.policy["authorized_offer"] = {"amount": amount, "authorized_by_user": approved}
                with self.assertRaises(email_policy.PolicyError):
                    self.render()

    def test_body_mutation_and_hidden_values_fail(self):
        body = self.render()
        for extra in ["My budget is $31,500.", "My budget is 31.5k.", "user1@example.com",
                      "EXAMPLE PRIVATE ACCOUNT", "Another dealer quoted $29,000.", "We have a deal."]:
            with self.subTest(extra=extra):
                result = email_policy.validate_draft(body + extra, self.plan, self.policy, now=self.now)
                self.assertEqual(result["status"], "blocked")

    def test_unknown_anchor_and_extra_model_keys_fail(self):
        self.plan["anchor_ids"] = ["invented"]
        with self.assertRaisesRegex(email_policy.PolicyError, "anchor_not_found"):
            self.render()
        self.plan["body"] = "model prose"
        with self.assertRaisesRegex(email_policy.PolicyError, "invalid_plan"):
            self.render()

    def test_evidence_hash_fields_confirmation_expiry_and_class_fail(self):
        changes = [("sha256", "incorrect"), ("text", "replacement"), ("confirmed_by_user", False),
                   ("expires_at", "2026-09-21T00:00:00Z")]
        for key, value in changes:
            with self.subTest(field=key):
                policy = copy.deepcopy(self.policy)
                policy["anchors"][0]["evidence"][key] = value
                with self.assertRaises(email_policy.PolicyError):
                    email_policy.render_draft(self.plan, policy, now=self.now)
        self.policy["anchors"][0]["vehicle_class"] = "new"
        with self.assertRaisesRegex(email_policy.PolicyError, "class_mismatch"):
            self.render()

    def test_matching_hash_is_insufficient_when_evidence_fields_differ(self):
        evidence = self.policy["anchors"][0]["evidence"]
        evidence["text"] = "Acme Motors: 2024 Example SUV; ask $30,900.00; synthetic listing."
        evidence["sha256"] = hashlib.sha256(evidence["text"].encode()).hexdigest()
        with self.assertRaisesRegex(email_policy.PolicyError, "fields_mismatch"):
            self.render()

    def test_private_ceiling_in_approved_ask_still_fails(self):
        self.policy["approved_asks"][0]["text"] = "Please meet my $31,500 limit."
        with self.assertRaisesRegex(email_policy.PolicyError, "private_ceiling"):
            self.render()

    def test_no_anchor_no_offer_followup_is_valid(self):
        self.plan = {"ask_ids": ["breakdown"], "anchor_ids": [], "include_offer": False}
        self.assertNotIn("$", self.render())


class TestInboxReplay(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.patch = patch.object(inbox_state, "data_path", self.path)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.fixture = corpus()
        self.store = inbox_state.InboxState(self.fixture["batch"]["account_id"])

    def path(self, relative, *, for_write=False):
        path = self.directory / relative
        if for_write:
            path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def prepare(self):
        self.store.import_batch(self.fixture["batch"])
        self.store.record_triage("message-1", "real_reply")
        plan = {"ask_ids": ["breakdown"], "anchor_ids": [], "include_offer": False}
        return self.store.prepare_draft("message-1", plan, self.fixture["policy"])["operation_id"]

    def receipt(self, operation):
        return {"account_id": operation["account_id"], "operation_id": operation["operation_id"],
                "body_sha256": operation["body_sha256"], "status": "draft_saved",
                "external_draft_id": "synthetic-draft-1", "provider_receipt_id": "synthetic-receipt-1"}

    def test_duplicate_page_and_restart_preserve_cursor_and_processed_ids(self):
        self.store.import_batch(self.fixture["batch"])
        self.store.record_triage("message-1", "crm")
        restarted = inbox_state.InboxState(self.fixture["batch"]["account_id"])
        self.assertEqual(restarted.import_batch(self.fixture["batch"])["status"], "duplicate")
        state = restarted.snapshot()
        self.assertEqual(state["cursor"], "cursor-1")
        self.assertEqual(state["messages"]["message-1"]["status"], "processed")

    def test_uninitialized_status_does_not_create_a_ledger_or_claim_a_mail_scan(self):
        output = io.StringIO()
        with patch.object(inbox_state, "data_path", return_value=None), \
             patch.object(sys, "argv", ["inbox_state.py", "status", "--account-id", "synthetic-account"]), \
             redirect_stdout(output):
            code = inbox_state.main()
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["status"], "uninitialized")
        self.assertFalse(result["live_gmail"])
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_conflicting_id_cursor_account_or_incomplete_page_never_advance(self):
        self.store.import_batch(self.fixture["batch"])
        before = self.store.snapshot()
        for change in ["id", "cursor", "account", "page", "body"]:
            with self.subTest(change=change):
                batch = copy.deepcopy(self.fixture["batch"])
                if change == "id": batch["messages"][0]["text"] = "different"
                if change == "cursor": batch["cursor_before"] = "wrong"; batch["cursor_after"] = "cursor-2"
                if change == "account": batch["account_id"] = "wrong"
                if change == "page": batch["complete"] = False
                if change == "body": batch["messages"][0]["body_complete"] = False
                with self.assertRaises(inbox_state.StateError):
                    self.store.import_batch(batch)
                self.assertEqual(self.store.snapshot(), before)

    def test_receipt_is_idempotent_and_bound_to_body_and_account(self):
        ident = self.prepare()
        operation = self.store.export_operation(ident)
        receipt = self.receipt(operation)
        for field in ["account_id", "body_sha256"]:
            invalid = dict(receipt, **{field: "wrong"})
            with self.assertRaises(inbox_state.StateError):
                self.store.import_receipt(invalid)
        self.assertEqual(self.store.import_receipt(receipt)["status"], "draft_saved")
        self.assertTrue(self.store.import_receipt(receipt)["duplicate"])
        with self.assertRaises(inbox_state.StateError):
            self.store.export_operation(ident)

    def test_provider_timeout_and_restart_do_not_repeat(self):
        ident = self.prepare()
        calls = []

        class Adapter:
            def create_draft(self, operation):
                calls.append(operation)
                raise TimeoutError("provider result unknown")

        with self.assertRaises(TimeoutError):
            self.store.execute_once(ident, Adapter())
        restarted = inbox_state.InboxState(self.fixture["batch"]["account_id"])
        with self.assertRaises(inbox_state.StateError):
            restarted.execute_once(ident, Adapter())
        self.assertEqual(len(calls), 1)
        self.assertEqual(restarted.snapshot()["operations"][ident]["status"], "uncertain")

    def test_failed_atomic_replace_leaves_previous_valid_state(self):
        self.store.import_batch(self.fixture["batch"])
        before = self.store.snapshot()
        with patch.object(inbox_state.os, "replace", side_effect=OSError("replace failed")):
            with self.assertRaises(OSError):
                self.store.record_triage("message-1", "crm")
        self.assertEqual(self.store.snapshot(), before)

    def test_live_lock_blocks_concurrent_writer(self):
        self.store.import_batch(self.fixture["batch"])
        with inbox_state._locked(self.path("inbox/state.json.lock")):
            with self.assertRaises(inbox_state.StateBusy):
                self.store.record_triage("message-1", "crm")

    def test_process_death_after_export_keeps_uncertain_and_releases_lock(self):
        ident = self.prepare()
        code = """
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import inbox_state
root = Path(sys.argv[2])
inbox_state.data_path = lambda relative, **kwargs: root / relative
store = inbox_state.InboxState(sys.argv[3])
store.export_operation(sys.argv[4])
os._exit(23)
"""
        result = subprocess.run([sys.executable, "-c", code, str(SCRIPTS), str(self.directory),
                                 self.fixture["batch"]["account_id"], ident], capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 23, result.stderr.decode())
        self.assertEqual(self.store.snapshot()["operations"][ident]["status"], "uncertain")
        with self.assertRaises(inbox_state.StateError):
            self.store.export_operation(ident)

    def test_crash_during_atomic_transaction_never_leaves_partial_json(self):
        self.store.import_batch(self.fixture["batch"])
        for point in ["before", "after"]:
            with self.subTest(point=point):
                code = """
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import inbox_state
root = Path(sys.argv[2])
inbox_state.data_path = lambda relative, **kwargs: root / relative
replace = inbox_state.os.replace
def crash(source, target):
    if sys.argv[4] == 'after': replace(source, target)
    os._exit(24)
inbox_state.os.replace = crash
inbox_state.InboxState(sys.argv[3]).record_triage('message-1', 'crm')
"""
                result = subprocess.run([sys.executable, "-c", code, str(SCRIPTS), str(self.directory),
                                         self.fixture["batch"]["account_id"], point], capture_output=True, timeout=15)
                self.assertEqual(result.returncode, 24, result.stderr.decode())
                state = self.store.snapshot()
                self.assertEqual(state["messages"]["message-1"]["status"], "received" if point == "before" else "processed")


class TestModelHarness(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.report = Path(self.temp.name) / "report.json"
        data = corpus()
        routes = json.loads(test_rubric.ROUTING_JSON.read_text(encoding="utf-8"))
        self.actor = {
            "drafts": [{"id": case["id"], "plan": case["expected"]} for case in data["model_cases"]],
            "routes": [{"id": case["id"], "skill": case["expected_skill"]} for case in routes["cases"]],
        }
        self.review = {"accepted": True, "gates": {
            "request_fidelity": True, "privacy": True, "evidence": True,
            "no_unapproved_commitments": True, "routing": True}, "rationale": "Synthetic review passed."}

    @staticmethod
    def response(payload, *, available=True):
        class Response:
            provider = "configured-provider" if available else None
            error = None if available else "unavailable"

            def __bool__(self):
                return available

            def __str__(self):
                return json.dumps(payload)
        return Response()

    def run_harness(self, responses):
        calls = []

        def call(prompt, **kwargs):
            calls.append({"prompt": prompt, "kwargs": kwargs})
            response = responses[len(calls) - 1]
            if isinstance(response, Exception):
                raise response
            return response

        result = test_rubric.Result()
        with redirect_stdout(io.StringIO()):
            test_rubric.run_llm_cases(result, caller=call, report_path=self.report)
        return result, calls, json.loads(self.report.read_text(encoding="utf-8"))

    def test_actual_outputs_are_verified_and_review_is_a_fresh_default_call(self):
        result, calls, report = self.run_harness([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(calls), 2)
        self.assertEqual([call["kwargs"] for call in calls], [{}, {}])
        self.assertNotEqual(calls[0]["prompt"], calls[1]["prompt"])
        self.assertEqual(report["qualitative_review"], "passed")
        self.assertFalse(report["live_gmail"])
        self.assertEqual(report["input_sha256"], hashlib.sha256(json.dumps(report["input"], sort_keys=True).encode()).hexdigest())

    def test_missing_actor_is_unavailable_and_not_retried(self):
        result, calls, report = self.run_harness([self.response({}, available=False)])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(len(calls), 1)
        self.assertEqual(report["status"], "actor_unavailable")
        self.assertEqual(report["qualitative_review"], "unavailable")

    def test_missing_reviewer_never_masquerades_as_a_pass(self):
        result, calls, report = self.run_harness([self.response(self.actor), self.response({}, available=False)])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(report["status"], "review_unavailable")
        self.assertEqual(report["qualitative_review"], "unavailable")

    def test_timeout_remains_uncertain_and_existing_report_is_not_replayed(self):
        result, calls, report = self.run_harness([TimeoutError("execution uncertain")])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(report["status"], "actor_uncertain")
        with patch.object(test_rubric, "_response", side_effect=AssertionError("must not retry")):
            repeated = test_rubric.Result()
            with redirect_stdout(io.StringIO()):
                test_rubric.run_llm_cases(repeated, caller=lambda prompt: None, report_path=self.report)
        self.assertEqual(repeated.exit_code, 2)

    def test_bad_model_plan_fails_before_review(self):
        self.actor["drafts"][0]["plan"]["anchor_ids"] = ["invented"]
        result, calls, report = self.run_harness([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(len(calls), 1)
        self.assertEqual(report["status"], "actor_failed")

    def test_reviewer_acceptance_must_match_every_boolean_gate(self):
        self.review["gates"]["privacy"] = False
        result, calls, report = self.run_harness([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report["qualitative_review"], "failed")

    def test_returned_provider_timeout_is_uncertain(self):
        response = self.response({}, available=False)
        response.error = "timeout after 18s"
        result, calls, report = self.run_harness([response])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(report["status"], "actor_uncertain")
        self.assertEqual(len(calls), 1)

    def test_registered_frontmatter_name_maps_to_directory_without_guessing(self):
        for row in self.actor["routes"]:
            if row["skill"] == "orchestrator":
                row["skill"] = "buy-me-a-car"
        result, calls, report = self.run_harness([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(test_rubric.canonical_skill("invented", {"orchestrator": "name: buy-me-a-car"}))
        self.assertIsNone(test_rubric.canonical_skill("shared-name", {"one": "name: shared-name", "two": "name: shared-name"}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
