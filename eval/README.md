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
