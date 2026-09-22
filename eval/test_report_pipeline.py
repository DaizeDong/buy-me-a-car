"""Report-pipeline contracts using reproducibly generated fictional evidence."""
from contextlib import ExitStack, redirect_stdout
import copy
from datetime import date
import hashlib
import html
import io
import json
from pathlib import Path
import sys
import tempfile
from threading import Barrier, Lock
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "eval"))
import run_report_pipeline as pipeline
from test_rubric import Result
from tools import runtime_paths
from tools.fixture_recipes.research_report import demo_config


class ReportPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.private = self.base / "companion" / "data"
        self.private.mkdir(parents=True)
        for guard in (
            patch.object(runtime_paths, "_guard_data_dir", return_value=self.private),
            patch.object(runtime_paths, "_private_repo_identity", return_value="example/private-fixture"),
        ):
            guard.start()
            self.addCleanup(guard.stop)
        config = demo_config()
        config.update(synthetic=False, date=date.today().isoformat())
        for source in config["sources"]:
            source["observed_date"] = config["date"]
            if source["status"] == "captured":
                artifact = self.private / (source["id"] + ".json")
                artifact.write_text(json.dumps({"synthetic_test_only": True, "source": source}), encoding="utf-8")
                source.update(artifact=str(artifact), sha256=hashlib.sha256(artifact.read_bytes()).hexdigest())
        self.actor = {key: config.pop(key) for key in pipeline.REPORT_FIELDS}
        sections = self.actor.pop("sections")
        for section in sections:
            section["id"] = section["topic"]
        self.writers = {f"writer_{index}": {"sections": [section for section in sections if section["topic"] in topics]}
                        for index, topics in enumerate(pipeline.BATCHES, 1)}
        self.actor.update(deliverables=sorted(pipeline.DELIVERABLES), clarification_questions=[])
        self.packet = {"user_prompt": "Help me choose a vehicle using these existing preferences.",
                       "research_data": config, "notes": "Generated fictional research for a harness test only."}
        self.packet_path = self.private / "packet.json"
        self.packet_path.write_text(json.dumps(self.packet), encoding="utf-8")
        self.output = self.private / "eval" / "report-fixture"
        self.receipt = self.output / "receipt.json"
        self.review = {"accepted": True, "gates": {
            key: {"passed": True, "evidence": self.actor["decision_summary"],
                  "reason": "Generated reviewer response tests validation, not model quality."}
            for key in pipeline.GATES}}

    @staticmethod
    def response(value, error=None):
        class Response(str):
            pass
        response = Response(json.dumps(value))
        response.provider = "synthetic-harness"
        response.error = error
        return response

    def run_case(self, responses, *, render_mode="success", writer_overrides=None, concurrent=False):
        calls, renders = [], []
        extracted_pdf = []
        lock = Lock()
        barrier = Barrier(3) if concurrent else None
        stage_responses = {stage: self.response(value) for stage, value in self.writers.items()}
        stage_responses.update(writer_overrides or {})
        stage_responses.update(dict(zip(("actor", "review"), responses)))

        def caller(prompt, **kwargs):
            stage = prompt.splitlines()[0].removeprefix("Report pipeline stage: ")
            receipt_path = self.output / (stage + ".json") if stage.startswith("writer_") else self.receipt
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["status"], stage + "_uncertain")
            if stage.startswith("writer_"):
                self.assertEqual(json.loads(self.receipt.read_text(encoding="utf-8"))["status"], "writers_uncertain")
                self.assertEqual(receipt["stage"], stage)
                if barrier:
                    barrier.wait(timeout=3)
            with lock:
                calls.append({"stage": stage, "prompt": prompt, "kwargs": kwargs})
            response = stage_responses[stage]
            if isinstance(response, Exception):
                raise response
            return response

        def renderer(config, output, *, mode, to_pdf):
            self.assertEqual(json.loads(self.receipt.read_text(encoding="utf-8"))["status"], "render_uncertain")
            self.assertEqual(mode, "live")
            actual_config = json.loads(config.read_text(encoding="utf-8"))
            renders.append(actual_config)
            if render_mode == "error":
                raise RuntimeError("synthetic renderer unavailable")
            strings = [pipeline.LIVE_NOTICE, *pipeline.analysis_strings(actual_config)]
            strings.extend(str(candidate[key]) for candidate in actual_config["candidates"]
                           for key in ("id", "vehicle", "configuration", "location", "vin", "stock")
                           if key in candidate)
            content = "\n".join(strings)
            pdf_content = content.replace(actual_config["decision_summary"], "") if render_mode == "dropped_pdf_analysis" else content
            if render_mode in {"radical_footer", "radical_footer_dropped"}:
                summary = actual_config["decision_summary"]
                middle = len(summary) // 2
                tail = summary[middle:-1] if render_mode == "radical_footer_dropped" else summary[middle:]
                pdf_content = content.replace(summary, summary[:middle] + "\n" + pipeline.LIVE_NOTICE + "\n第13\u2eda\n" + tail)
            extracted_pdf.append(pdf_content)
            if render_mode in {"dropped_html_analysis", "analysis_only_in_style"}:
                content = content.replace(actual_config["decision_summary"], "")
            if render_mode == "dropped_candidate":
                content = content.replace(actual_config["candidates"][0]["stock"], "")
            rendered = "<!doctype html><body>" + "".join("<p>" + html.escape(value) + "</p>"
                                                       for value in content.splitlines())
            if render_mode == "analysis_only_in_style":
                rendered += "<style>" + actual_config["decision_summary"] + "</style>"
            output.write_text(rendered + "</body>", encoding="utf-8")
            if render_mode != "missing_pdf":
                to_pdf.write_bytes(b"%PDF-1.7\n" + b"Generated renderer fixture only\n" * 5 + b"%%EOF\n")
            return {"html": output, "pdf": to_pdf}

        result = Result()
        with redirect_stdout(io.StringIO()), ExitStack() as stack:
            if render_mode != "corrupt_pdf":
                verifier = stack.enter_context(patch.object(pipeline, "_verify_pdf", return_value=1))
                extractor = stack.enter_context(patch.object(pipeline, "_pdf_text", side_effect=lambda path: extracted_pdf[0]))
            output = pipeline.run(result, self.packet_path, caller=caller, renderer=renderer, output_dir=self.output)
            if render_mode == "success" and renders:
                verifier.assert_called_once_with(self.output / "buyer_research.pdf", expected_notice=pipeline.LIVE_NOTICE)
                extractor.assert_called_once_with(self.output / "buyer_research.pdf")
        self.assertEqual(output, self.output)
        return result, calls, renders, json.loads(self.receipt.read_text(encoding="utf-8"))

    def test_plain_request_selects_renders_and_reviews_full_report_without_fact_mutation(self):
        original = copy.deepcopy(self.packet)
        result, calls, renders, receipt = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual([call["kwargs"] for call in calls], [{"mode": "agent"}] * 5)
        self.assertNotIn('"gates":', calls[0]["prompt"])
        self.assertEqual(set(receipt["input"]["instructions"]), set(pipeline.REFERENCES))
        self.assertEqual(receipt["input_sha256"], pipeline._hash(receipt["input"]))
        self.assertIn(self.actor["decision_summary"], calls[-1]["prompt"])
        self.assertEqual(json.loads(self.packet_path.read_text(encoding="utf-8")), original)
        for key, value in original["research_data"].items():
            self.assertEqual(renders[0][key], value)
        self.assertEqual(set(receipt["artifacts"]), pipeline.DELIVERABLES)
        self.assertGreater(receipt["render_verification"]["analysis_strings_checked"], 11)
        self.assertGreater(receipt["render_verification"]["candidate_fields_checked"], 0)
        self.assertIn("packet_consistency", receipt["review_prompt"])
        self.assertIn("cannot independently verify", receipt["review_prompt"])
        self.assertNotIn("source_fidelity", receipt["review_prompt"])
        for name, artifact in receipt["artifacts"].items():
            self.assertEqual(artifact["sha256"], hashlib.sha256((self.output / name).read_bytes()).hexdigest())
        comparison = (self.output / "master_comparison.md").read_text(encoding="utf-8")
        self.assertIn("未知", comparison)
        self.assertIn("不按零计算", comparison)
        for candidate in original["research_data"]["candidates"]:
            self.assertIn(candidate["id"], comparison)

    def test_missing_pdf_selection_fails_before_render_or_review(self):
        self.actor["deliverables"].remove("buyer_research.pdf")
        result, calls, renders, receipt = self.run_case([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "actor_failed")
        self.assertEqual(len(calls), 1)
        self.assertEqual(renders, [])

    def test_reasking_existing_criteria_is_not_success(self):
        self.actor["clarification_questions"] = ["Please repeat all existing preferences."]
        result, calls, renders, receipt = self.run_case([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "actor_failed")
        self.assertEqual(renders, [])

    def test_actor_cannot_replace_evidence_collections(self):
        self.actor["candidates"] = []
        result, calls, renders, receipt = self.run_case([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "actor_failed")
        self.assertEqual(renders, [])

    def test_empty_analysis_is_rejected_even_with_injected_renderer(self):
        self.writers["writer_1"]["sections"][0]["blocks"] = []
        result, calls, renders, receipt = self.run_case([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "writers_failed")
        self.assertEqual(renders, [])

    def test_missing_rendered_pdf_fails_before_reviewer(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="missing_pdf")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "render_failed")
        self.assertEqual(len(calls), 4)
        self.assertEqual(len(renders), 1)

    def test_renderer_error_retains_receipt_and_stops(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="error")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "render_failed")
        self.assertEqual(len(calls), 4)
        self.assertTrue((self.output / "research_config.json").is_file())

    def test_corrupt_pdf_cannot_pass_even_when_header_footer_and_html_exist(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="corrupt_pdf")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "render_failed")
        self.assertIn("parsed as a PDF", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def test_dropped_html_analysis_cannot_reach_reviewer(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="dropped_html_analysis")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("HTML missing expected", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def test_dropped_pdf_analysis_cannot_reach_reviewer(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="dropped_pdf_analysis")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("PDF missing expected", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def test_text_only_in_html_style_does_not_count_as_report_content(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="analysis_only_in_style")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("HTML missing expected", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def test_candidate_identity_must_survive_rendering(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="dropped_candidate")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("HTML missing expected", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def test_dropped_markdown_analysis_prevents_model_review(self):
        original = pipeline.comparison_markdown
        with patch.object(pipeline, "comparison_markdown", side_effect=lambda config:
                          original(config).replace(config["decision_summary"], "")):
            result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="dropped_md_analysis")
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "render_failed")
        self.assertIn("Markdown missing expected", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def test_radical_page_footer_does_not_break_paragraph_binding(self):
        result, calls, renders, receipt = self.run_case(
            [self.response(self.actor), self.response(self.review)], render_mode="radical_footer")
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual(len(calls), 5)

    def test_radical_footer_handling_does_not_hide_missing_content(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="radical_footer_dropped")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("PDF missing expected", receipt["render_error"])
        self.assertEqual(len(calls), 4)

    def prepare_resume(self):
        result, calls, renders, receipt = self.run_case([self.response(self.actor)], render_mode="dropped_pdf_analysis")
        self.assertEqual(receipt["status"], "render_failed")
        parser = pipeline._BodyText()
        parser.feed((self.output / "buyer_research.html").read_text(encoding="utf-8"))
        return receipt, "\n".join(parser.parts)

    def test_explicit_resume_rechecks_completed_stages_and_calls_only_new_review(self):
        original, pdf_text = self.prepare_resume()
        original_children = {path: path.read_bytes() for path in self.output.glob("writer_*.json")}
        calls = []

        def caller(prompt, **kwargs):
            self.assertTrue(prompt.startswith("Report pipeline stage: review\n"))
            self.assertEqual(kwargs, {"mode": "agent"})
            pending = json.loads(self.receipt.read_text(encoding="utf-8"))
            self.assertEqual(pending["status"], "review_uncertain")
            self.assertEqual(pending["history"][-1]["previous_status"], "render_failed")
            calls.append(prompt)
            return self.response(self.review)

        result = Result()
        with patch.object(pipeline, "_verify_pdf", return_value=1), \
                patch.object(pipeline, "_pdf_text", return_value=pdf_text), \
                patch.object(pipeline, "generate_report", side_effect=AssertionError("must not rerender")), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(pipeline.resume_review(result, self.output, caller=caller), self.output)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(calls), 1)
        resumed = json.loads(self.receipt.read_text(encoding="utf-8"))
        self.assertEqual(resumed["status"], "passed")
        self.assertEqual(resumed["actor"], original["actor"])
        self.assertEqual(resumed["writer_receipts"], original["writer_receipts"])
        for path, contents in original_children.items():
            self.assertEqual(path.read_bytes(), contents)
        with self.assertRaisesRegex(ValueError, "no_previous_review"):
            pipeline.resume_review(Result(), self.output, caller=lambda *a, **k: self.fail("must not replay"))

    def test_resume_rejects_tampered_config_or_child_receipt_before_call(self):
        self.prepare_resume()
        for name in ("research_config.json", "writer_2.json"):
            path = self.output / name
            original = path.read_bytes()
            if name == "research_config.json":
                changed = json.loads(original)
                changed["title"] += " changed synthetic title"
                path.write_text(json.dumps(changed), encoding="utf-8")
            else:
                path.write_bytes(original + b"\n")
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "hash"):
                pipeline.resume_review(Result(), self.output, caller=lambda *a, **k: self.fail("must not call"))
            path.write_bytes(original)

    def test_resume_rejects_any_existing_uncertain_review_without_replay(self):
        original, _ = self.prepare_resume()
        for marker in ({"review_prompt": "Synthetic prior attempt"}, {"review": None}, {"status": "review_uncertain"}):
            record = dict(original, **marker)
            self.receipt.write_text(json.dumps(record), encoding="utf-8")
            before = self.receipt.read_bytes()
            with self.subTest(marker=marker), self.assertRaisesRegex(ValueError, "no_previous_review"):
                pipeline.resume_review(Result(), self.output, caller=lambda *a, **k: self.fail("must not replay"))
            self.assertEqual(self.receipt.read_bytes(), before)

    def test_failed_review_gate_preserves_artifacts_but_fails_acceptance(self):
        self.review["gates"]["costs"].update(passed=False, evidence="")
        self.review["accepted"] = False
        result, calls, renders, receipt = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "failed")
        self.assertEqual(set(receipt["artifacts"]), pipeline.DELIVERABLES)

    def test_reviewer_cannot_quote_packet_only_evidence_as_report_analysis(self):
        self.review["gates"]["costs"]["evidence"] = self.packet["notes"]
        result, calls, renders, receipt = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "review_failed")

    def test_review_requires_exact_gates_strict_booleans_and_consistent_acceptance(self):
        mutations = [lambda review: review["gates"].pop("costs"),
                     lambda review: review["gates"]["costs"].update(passed="true"),
                     lambda review: review.update(accepted=1),
                     lambda review: review.update(accepted=False),
                     lambda review: review["gates"]["costs"].update(evidence="")]
        for mutate in mutations:
            review = copy.deepcopy(self.review)
            mutate(review)
            with self.subTest(review=review), self.assertRaises(ValueError):
                pipeline.validate_review(review, self.actor["decision_summary"])

    def test_uncertain_call_is_never_replayed(self):
        result, calls, renders, receipt = self.run_case([TimeoutError("synthetic uncertain execution")])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(receipt["status"], "actor_uncertain")
        result, calls, renders, receipt = self.run_case([])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(calls, [])
        self.assertEqual(renders, [])

    def test_parallel_writers_use_isolated_receipts_and_compact_inputs(self):
        result, calls, renders, receipt = self.run_case(
            [self.response(self.actor), self.response(self.review)], concurrent=True)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(len(calls), 5)
        self.assertEqual(receipt["strategy"], "bounded_parallel_topics")
        planner = receipt["input"]
        self.assertNotIn("research_data", planner)
        self.assertNotIn("sources", planner)
        self.assertNotIn("notes", planner)
        self.assertEqual(planner["research_notes"], self.packet["notes"])
        self.assertEqual(planner["candidate_count"], len(self.packet["research_data"]["candidates"]))
        for call in calls:
            if not call["stage"].startswith("writer_"):
                continue
            supplied = json.loads(call["prompt"].splitlines()[-1])
            self.assertEqual(supplied["schema"], pipeline.analysis_schema(
                (ROOT / pipeline.WRITER_SCHEMA).read_text(encoding="utf-8")))
            self.assertLess(len(supplied["schema"]), len((ROOT / pipeline.WRITER_SCHEMA).read_text(encoding="utf-8")))
            self.assertEqual(supplied["packet"], pipeline.compact_packet(self.packet))
            for source in supplied["packet"]["records"]["sources"]:
                self.assertNotIn("artifact", source)
                self.assertNotIn("sha256", source)
            child = self.output / (call["stage"] + ".json")
            recorded = json.loads(child.read_text(encoding="utf-8"))
            self.assertEqual(recorded["status"], "returned")
            self.assertEqual(recorded["topics"], supplied["assigned_topics"])
            self.assertEqual(receipt["writer_receipts"][call["stage"]]["sha256"],
                             hashlib.sha256(child.read_bytes()).hexdigest())
            self.assertNotIn("gates", supplied)
        review_input = json.loads(calls[-1]["prompt"].splitlines()[-1])
        self.assertEqual(set(review_input), {"source_packet", "actual_analysis_text", "gates"})
        self.assertEqual(self.packet["research_data"]["sources"], renders[0]["sources"])

    def test_analysis_schema_extracts_only_one_complete_writer_section(self):
        block_schema = json.dumps({"type": "paragraph", "text": "string", "refs": ["source:ID"]})
        source = ("# Input\n\n## Header and evidence\nHEADER_ONLY\n\n"
                  "## Analysis sections\n" + block_schema + "\n\n"
                  "### References\nREFERENCE_RULES\n\n## Reproduce and deliver\nDELIVERY_ONLY\n")
        extracted = pipeline.analysis_schema(source)
        self.assertIn(block_schema, extracted)
        self.assertIn("### References", extracted)
        self.assertNotIn("HEADER_ONLY", extracted)
        self.assertNotIn("DELIVERY_ONLY", extracted)

    def test_analysis_schema_missing_empty_or_ambiguous_sections_fail_closed(self):
        invalid = ["## Header and evidence\ntext\n", "## Analysis sections\n\n## Other\ntext\n",
                   "## Analysis sections\nfirst\n## Analysis sections\nsecond\n"]
        for source in invalid:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "exactly one nonempty"):
                pipeline.analysis_schema(source)

    def test_invalid_writer_schema_stops_before_any_model_execution(self):
        with patch.object(pipeline, "analysis_schema", side_effect=ValueError("invalid writer section")):
            with self.assertRaisesRegex(ValueError, "writer section"):
                pipeline.run(Result(), self.packet_path, caller=lambda *a, **k: self.fail("must not call"),
                             output_dir=self.output)
        self.assertFalse(self.output.exists())

    def test_approved_scenario_context_reaches_all_stages_without_changing_factual_status(self):
        # This verifies context transport and persisted records, not model judgment.
        context = ("Generated scenario: the buyer approved the existing assumed criteria for this report. "
                   "Use them without repeating intake. They are not real buyer facts or transaction authorization.")
        self.packet["notes"] = context
        for criterion in self.packet["research_data"]["criteria"]:
            if criterion["status"] == "assumed":
                criterion["notes"] = "Synthetic assumption approved for this report only."
        before = copy.deepcopy(self.packet["research_data"])
        self.packet_path.write_text(json.dumps(self.packet), encoding="utf-8")
        result, calls, renders, receipt = self.run_case([self.response(self.actor), self.response(self.review)])
        self.assertEqual(result.exit_code, 0)
        for call in calls:
            supplied = json.loads(call["prompt"].splitlines()[-1])
            if call["stage"] == "actor":
                self.assertEqual(supplied["research_notes"], context)
                observed_criteria = supplied["criteria"]
            else:
                packet = supplied["source_packet"] if call["stage"] == "review" else supplied["packet"]
                self.assertEqual(packet["notes"], context)
                observed_criteria = packet["records"]["criteria"]
            self.assertEqual(observed_criteria, before["criteria"])
        saved = json.loads((self.output / "research_config.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["criteria"], before["criteria"])
        self.assertEqual(renders[0]["criteria"], before["criteria"])
        self.assertEqual(saved["sources"], before["sources"])
        self.assertIn("Synthetic assumption approved for this report only.",
                      (self.output / "master_comparison.md").read_text(encoding="utf-8"))
        self.assertTrue(any(criterion["status"] == "assumed" for criterion in saved["criteria"]))

    def test_uncertain_writer_collects_every_batch_without_partial_delivery_or_replay(self):
        result, calls, renders, receipt = self.run_case(
            [self.response(self.actor)], writer_overrides={"writer_2": TimeoutError("synthetic uncertain writer")},
            concurrent=True)
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(receipt["status"], "writers_unavailable")
        self.assertEqual({call["stage"] for call in calls}, {"actor", "writer_1", "writer_2", "writer_3"})
        self.assertEqual(receipt["writer_receipts"]["writer_1"]["status"], "returned")
        self.assertEqual(receipt["writer_receipts"]["writer_2"]["status"], "writer_2_uncertain")
        self.assertEqual(receipt["writer_receipts"]["writer_3"]["status"], "returned")
        self.assertEqual(renders, [])
        self.assertFalse((self.output / "research_config.json").exists())
        original = self.receipt.read_bytes()
        result, calls, renders, receipt = self.run_case([])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(calls, [])
        self.assertEqual(self.receipt.read_bytes(), original)

    def test_writer_cannot_replace_facts_or_supply_unassigned_topics(self):
        self.writers["writer_1"]["candidates"] = []
        result, calls, renders, receipt = self.run_case([self.response(self.actor)])
        self.assertEqual(result.exit_code, 1)
        self.assertEqual(receipt["status"], "writers_failed")
        self.assertEqual(receipt["writer_receipts"]["writer_1"]["status"], "failed")
        self.assertEqual(len(calls), 4)
        self.assertEqual(renders, [])

    def test_missing_reviewer_is_unavailable_not_accepted(self):
        result, calls, renders, receipt = self.run_case([
            self.response(self.actor), self.response({}, error="unavailable")])
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(receipt["status"], "review_unavailable")

    def test_packet_and_output_must_be_private_even_with_injected_dependencies(self):
        outside = self.base / "outside.json"
        outside.write_text(json.dumps(self.packet), encoding="utf-8")
        for packet, output in ((outside, self.output), (self.packet_path, self.base / "outside-output")):
            with self.subTest(packet=packet), self.assertRaises(runtime_paths.DataBoundaryError):
                pipeline.run(Result(), packet, caller=lambda *a, **k: self.fail("must not call model"),
                             renderer=lambda *a, **k: self.fail("must not render"), output_dir=output)
        self.assertFalse(self.output.exists())
        self.assertFalse((self.base / "outside-output").exists())

    def test_modified_source_artifact_fails_before_call_or_receipt(self):
        artifact = Path(self.packet["research_data"]["sources"][0]["artifact"])
        artifact.write_text("Synthetic changed evidence", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            pipeline.run(Result(), self.packet_path, caller=lambda *a, **k: self.fail("must not call model"),
                         output_dir=self.output)
        self.assertFalse(self.output.exists())

    def test_packet_cannot_seed_preapproved_analysis(self):
        self.packet["research_data"]["decision_summary"] = "Synthetic prewritten result"
        self.packet_path.write_text(json.dumps(self.packet), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "actor_analysis"):
            pipeline.load_packet(self.packet_path)

    def test_model_execution_is_opt_in(self):
        output = io.StringIO()
        with redirect_stdout(output), patch.object(pipeline, "run", side_effect=AssertionError("must not run")):
            self.assertEqual(pipeline.main([]), 0)
        self.assertIn("NOT RUN", output.getvalue())


if __name__ == "__main__":
    unittest.main()
