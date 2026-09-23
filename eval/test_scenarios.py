"""Regression checks for scenario evaluation receipts and failure handling."""
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_scenarios as scenario
from test_rubric import Result, run_llm_cases
from tools.runtime_paths import DataBoundaryError


class TestScenarioHarness(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'receipt.json'
        self.cases = scenario.corpus()['cases']
        self.actor = {'answers': [
            {'id': case['id'], 'skill': 'buy-me-a-car', 'reply': 'Synthetic answer for ' + case['id']}
            for case in self.cases]}
        self.review = {'cases': [
            {'id': case['id'], 'accepted': True, 'gates': {
                key: {'passed': True, 'evidence': 'Synthetic answer', 'reason': 'Synthetic reviewer decision.'}
                for key in case['criteria']}}
            for case in self.cases]}

    @staticmethod
    def response(payload, error=None):
        class Response:
            provider = 'configured-provider'

            def __str__(self):
                return json.dumps(payload)
        response = Response()
        response.error = error
        return response

    def run_case(self, responses):
        calls = []

        def caller(prompt, **kwargs):
            receipt = json.loads(self.path.read_text(encoding='utf-8'))
            self.assertIn(receipt['status'], {'actor_uncertain', 'review_uncertain'})
            calls.append({'prompt': prompt, 'kwargs': kwargs})
            response = responses[len(calls) - 1]
            if isinstance(response, Exception):
                raise response
            return response

        result = Result()
        with redirect_stdout(io.StringIO()):
            scenario.run(result, caller=caller, report_path=self.path)
        return result, calls, json.loads(self.path.read_text(encoding='utf-8'))

    def test_independent_review_uses_actual_reply_and_actor_does_not_see_grading_keys(self):
        result, calls, report = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(report['status'], 'passed')
        self.assertEqual([call['kwargs'] for call in calls], [{'mode': 'agent'}, {'mode': 'agent'}])
        self.assertNotIn('criteria', report['input'])
        self.assertEqual(set(report['input']['cases'][0]), {'id', 'prompt'})
        self.assertIn('Synthetic answer for AK01', calls[1]['prompt'])
        self.assertEqual(report['input_sha256'], hashlib.sha256(
            json.dumps(report['input'], sort_keys=True).encode()).hexdigest())

    def test_failed_substantive_gate_is_not_a_pass(self):
        self.review['cases'][0]['gates']['registration']['passed'] = False
        self.review['cases'][0]['accepted'] = False
        result, calls, report = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report['status'], 'failed')

    def test_reviewer_cannot_quote_text_absent_from_the_actual_answer(self):
        self.review['cases'][0]['gates']['registration']['evidence'] = 'Invented answer evidence'
        result, calls, report = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report['status'], 'review_failed')

    def test_missing_actor_reply_stops_before_review(self):
        self.actor['answers'][0]['reply'] = ''
        result, calls, report = self.run_case([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(len(calls), 1)
        self.assertEqual(report['status'], 'actor_failed')

    def test_missing_reviewer_is_unavailable(self):
        result, calls, report = self.run_case([
            self.response(self.actor), self.response({}, error='unavailable')])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(report['status'], 'review_unavailable')

    def test_timeout_and_existing_receipt_never_trigger_replay(self):
        result, calls, report = self.run_case([TimeoutError('uncertain')])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(report['status'], 'actor_uncertain')
        result, calls, report = self.run_case([])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(calls, [])

    def test_real_caller_rejects_explicit_nonprivate_destination_before_writing(self):
        with tempfile.TemporaryDirectory() as outside:
            unsafe = Path(outside) / 'receipt.json'
            fake_module = SimpleNamespace(call=lambda *a, **kw: self.fail('must not invoke model'))
            with patch('tools.runtime_paths.resolve_data_dir', return_value=Path(self.temp.name)), \
                    patch.dict(sys.modules, {'llmcall': fake_module}), \
                    redirect_stdout(io.StringIO()):
                for runner in (scenario.run, run_llm_cases):
                    with self.subTest(runner=runner.__name__):
                        with self.assertRaises(DataBoundaryError):
                            runner(Result(), report_path=unsafe)
            self.assertFalse(unsafe.exists())

    def test_inconsistent_reviewer_acceptance_fails(self):
        self.review['cases'][0]['accepted'] = False
        result, calls, report = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(report['status'], 'review_failed')

    def test_duplicate_answers_and_unknown_routes_fail(self):
        for mutation in ['duplicate', 'unknown']:
            with self.subTest(mutation=mutation):
                if self.path.exists():
                    self.path.unlink()
                if mutation == 'duplicate':
                    self.actor['answers'][1]['id'] = 'AK01'
                else:
                    self.actor['answers'][1]['id'] = 'AK02'
                    self.actor['answers'][0]['skill'] = 'invented'
                result, calls, report = self.run_case([self.response(self.actor)])
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
