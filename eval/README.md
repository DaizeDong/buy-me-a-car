# Evaluation and regression checks

Run the offline suite from the repository root after installing
`requirements.txt`. Tests use `unittest`; PDF and YAML checks use the declared
runtime dependencies. Offline tests do not call models or contact sellers.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s eval -p "test_*.py" -v
python eval/test_rubric.py -v
python tools/make_fixtures.py --check
python skills/orchestrator/scripts/render_state_data.py --check
python tools/check_repository.py
```

`bash eval/run.sh` is an alternative runner for the individual test scripts.
The functional CI runs the offline checks on Windows and Ubuntu.

## What the checks establish

- Purchase calculation tests cover the supported state rules, forward/reverse
  arithmetic, trade/payoff separation, input validation and CLI failure behavior.
  Unsupported jurisdictions, including Alaska, must reject automated OTD
  calculations even when the state-level sales-tax rate is zero. The current
  `data/state_fees.json` calculator status and field provenance define support;
  a state row alone does not.
- Data integrity checks verify that generated reference tables agree with the
  canonical records. Agreement does not independently verify current law.
- Workflow tests exercise constrained drafts, private-budget protection,
  inventory normalization, durable inbox state and uncertain-operation recovery.
- Runtime, installer, dossier and repository checks cover private DATA resolution,
  installed resource paths, schema/financial consistency, PDF outputs and exact
  synthetic fixture reproduction.
- Model harness tests inject synthetic provider responses to test receipts,
  validation and failure handling. They do not measure a model's response quality.
- Research report regressions exercise the actual renderer with incomplete costs,
  zero quotes, duplicate VIN observations, source integrity and required topics.
  Section coverage and successful rendering alone do not establish analytical
  quality; actual reports still require content review and inspection of every
  PDF page.

## Actual model evaluations

The installed `llmcall` package and a verified PRIVATE companion repository are
required. Configure the companion as described in the root README; receipts
resolve through `tools/runtime_paths.py`. Raw inputs, replies, provider identities
and review decisions are written under private `eval/model-runs/` only.

```bash
python eval/test_rubric.py --llm -v
python eval/run_scenarios.py --llm -v
```

The first command evaluates structured draft decisions and the routing corpus.
The second produces actual Chinese buyer-facing answers for two generated Alaska
pickup cases, then invokes a separate reviewer:

- `AK01`: an initial, underspecified purchase request. Check registration
  municipality, budget basis, towing/payload and cab/bed needs, winter conditions,
  and local versus Lower 48 sourcing.
- `AK02`: a follow-up with supplied budget, location and loaded trailer weight.
  Challenge the zero-tax total shortcut and the universal `GCWR - GVWR` towing
  formula; require configuration-specific evidence and landed-cost accounting.

The scenario actor reads the shipped skill/reference text and user prompts, but
not the grading criteria. The reviewer sees the actual answers and must quote
answer text for every positive gate. Routing, complete case coverage, strict
boolean gates and evidence substrings are checked deterministically. A separate
model review is still a qualitative judgment, not independent vehicle or tax
verification. These closed-input scenarios do not exercise host skill discovery,
live inventory, transport quotes, dealer communications or a completed purchase.

The scenario harness uses `llmcall.call(prompt, mode="agent")` with current
routing/defaults and no model pin. It saves an uncertain receipt before each
call and never retries an uncertain execution. Missing capability or uncertain
execution exits 2; invalid output or a failed criterion exits 1; passing checks
exit 0. Without `--llm`, model behavior is explicitly NOT RUN.

## Research report delivery acceptance

The response scenarios above do not generate a research report. To test the
delivery path after actual source collection, the agent prepares a private
packet with `user_prompt`, `research_data` and `notes`, then runs:

```sh
python eval/run_report_pipeline.py --packet dossiers/example/pipeline_packet.json --llm -v
```

`research_data` uses the [research schema](../skills/dossier-builder/references/research_schema.md)
without `title`, `decision_summary` or `sections`. All source captures must already
have verified private artifact paths and hashes. Keep the user prompt as the
ordinary buying request; do not add an expansion or PDF request for this test.

The planner reads the shipped workflow and selects the default deliverables.
Three independent topic writers receive compact records and generate the
analysis in parallel, each with its own receipt. Missing or uncertain batches
prevent a success claim. The runner preserves all supplied facts and invokes the production
HTML/PDF renderer, verifies that the analysis appears in both artifacts, then a
separate model reviews its decision value and consistency with the supplied
packet. This model review does not independently re-read captured originals.
The runner records artifacts, hashes and write-ahead receipts
in a unique private run. Existing or uncertain work cannot silently replay.

If all writing finished and a known rendering check failed before review, repair
and reverify the deterministic artifacts, then resume only the first review:

```sh
python eval/run_report_pipeline.py --resume-review eval/model-runs/report-example --llm -v
```

Resume requires unchanged config/packet evidence and successful, hash-matching
planner/writer receipts. It binds the analysis and candidate identities to HTML,
PDF and Markdown again, preserves the prior failure, and refuses any run with an
existing review attempt. It does not replay a model call or regenerate files.

If the planner and some writers completed but another writer failed or timed
out, first reconcile that pure-analysis attempt. An explicit continuation can
preserve completed work in a new run:

```sh
python eval/run_report_pipeline.py --continue-writers eval/model-runs/report-example --llm -v
```

This mode locks and validates the terminal parent, its unchanged packet and
source evidence, and every child receipt hash. It requires a valid planner and
at least one valid completed writer. Active, rendered, reviewed or successful
runs, changed evidence and corrupt receipts are rejected. The parent stays
unchanged. The new receipt records its parent hashes and marks each reused
response separately from fresh model calls. Saved prompt payloads must match
the unchanged packet and current schema; reused responses retain their original
prompts, with any current wrapper differences recorded explicitly. Only missing writers and the final
review call the model; rendering and all three artifact-content checks still
run. This is explicit continuation after reconciliation, never an automatic
retry of uncertain work.

If all writing and artifact checks passed, but the final reviewer timed out
without returning text, explicitly continue that reconciled attempt in a new run:

```sh
python eval/run_report_pipeline.py --continue-review eval/model-runs/report-example --llm -v
```

This requires a terminal `review_uncertain` receipt with an uncertainty error and
explicitly empty review text. Every planner/writer response, saved prompt payload, config and
artifact hash must still match the frozen evidence. HTML, PDF and Markdown
content are checked again before any new run. All writing is reused with its
original provenance, then the child renders fresh artifacts and calls only the
final reviewer. The parent stays unchanged, including its failed attempt.
Active calls, partial text, failed reviews and passed reviews are rejected as
continuation sources. The review still assesses all six gates and provides one
short report excerpt and one concise reason per gate. Continuation is an explicit
recovery action, not an automatic retry or a mechanism for overturning a recorded
qualitative decision.

Older receipts discarded text when the caller returned an error. Missing text in
those receipts is insufficient proof of an empty reply. Use the optional
`--review-reconciliation` argument only after checking the original call ledger
and confirming that the caller exited. Its private JSON must contain
`schema_version: 1`, `kind: "llmcall_zero_reply_reconciliation"`, the absolute
`parent_run`, `parent_receipt_sha256`, `review_prompt_sha256`, `caller_exited: true`,
`response_text: ""`, a nonempty `binding_method`, and the original `ledger_record`.
The ledger must record agent mode, a failed call with an error, exactly zero reply
characters, and a prompt length matching the saved review prompt. This is an
explicit local operator reconciliation, not signed provider proof. Its path and
hash are recorded in the child. It never overrides nonempty stored review text.

Before starting a review child, the runner writes a one-use claim under private
`eval/model-runs/review-continuations/`, keyed by the parent receipt hash. A later
attempt to use that same parent is rejected even if the child was rejected or the
process stopped before starting it. Inspect the recorded child and reconcile its
state; do not delete a claim to obtain another review. No claim or output is
written inside the original parent run.

This is a bounded test of synthesis and delivery after research. It does not
establish automatic host skill discovery, autonomous source collection, visual
PDF quality or purchase outcomes. Independently inspect every PDF page and
check the selected source records. Synthetic harness tests only establish the
runner's acceptance and failure behavior.

## Synthetic inputs

Edit recipes under `tools/fixture_recipes/`, then regenerate:

```bash
python tools/make_fixtures.py
python tools/make_fixtures.py --check
```

Every generated output must be declared as FIXTURE in `.dataclass.json`.
Hand-check expected monetary results and behavioral criteria when changing a
recipe. Never derive an expected answer by calling the implementation under test,
copy an actual buyer record, or paste real model output into public fixtures.
