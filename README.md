# buy-me-a-car

A set of 16 skills for researching a US car purchase, comparing written offers,
preparing dealer replies and reviewing a decision dossier. A broad buying request
includes a market comparison and buyer research HTML/PDF by default. The agent
reuses known criteria and prepares the report input; buyers do not need to ask
again for a longer report, request a PDF separately or fill a JSON template.
The repository ships
an uninitialized tool with generated synthetic examples. Real purchase records
belong in a separate, verified private companion repository.

[中文说明](README_CN.md) · [Main skill](skills/orchestrator/SKILL.md) ·
[Roadmap](ROADMAP.md)

## What works locally

- OTD calculations use decimal arithmetic, dated state-rule evidence and explicit
  applicability checks. Unknown or unsupported profiles refuse calculation.
- Dealer replies are rendered from approved asks, supported anchors and an
  authorized offer. The private maximum is kept separate.
- Inbox imports retain stable account/message IDs, cursors and operation receipts.
  Interrupted or uncertain draft exports cannot be replayed silently.
- Buyer research reports cover requirements, search coverage, model alternatives,
  listings, costs, suitability, winter use, ownership, recommendations, next steps
  and sources. Missing quotes and unknown costs remain visible. The current
  research renderer supports Chinese; dealer proposals support English, Chinese
  and Spanish and retain their complete-quote requirements.
- Report generation validates evidence dates and hashes, escapes inserted text
  and checks PDF output. Source archives establish what was captured, not whether
  a listing is still available or a seller's claims are true.
- Installation registers all 16 skills, detects conflicts before applying, and
  works through Windows directory junctions.
- Public fixtures can be regenerated; real inputs and outputs must resolve into
  a companion whose GitHub origin is verifiably PRIVATE.

Inventory research uses available search/browser tools. Gmail access, unattended
scheduling, dealer delivery and bookings require actual host integrations and
authorization. The package does not install those integrations. A successful
local test or synthetic example is not evidence of purchase savings.

## Install

Requires Python 3.10 or newer, Git and the pinned submodules. YAML/PDF utilities
need the dependencies below. Chromium or Edge is recommended for PDF rendering.

```sh
git clone --recurse-submodules https://github.com/DaizeDong/buy-me-a-car.git
cd buy-me-a-car
python -m pip install -r requirements.txt
git config core.hooksPath .githooks
python tools/install.py
python tools/install.py --apply
python tools/doctor.py
```

The installer previews by default, then links skills under `~/.agents/skills`.
Use `--target <skill-directory>` for another host. It refuses unrelated existing
skills rather than replacing them. Start a new agent session to discover newly
registered skills. Claude plugin hosts can load this repository as a local plugin;
its `.claude-plugin/plugin.json` exposes the bundled skill tree.

For an existing clone, initialize submodules with
`git submodule update --init --recursive`. Missing guards must fail explicitly;
do not bypass the hooks.

## Initialize private storage

Clone or initialize a **private GitHub companion repository** outside this public
worktree and create its `data` directory. Set `BUY_ME_A_CAR_CONFIG` to the companion
root, authenticate GitHub CLI (`gh`), and run:

```sh
python tools/runtime_paths.py --write
```

The resolver reports the verified private repository and DATA path. It rejects
public, unknown, missing and unversioned destinations. An optional read without
initialization reports `UNINITIALIZED`; a write fails. Real criteria, inventory,
quotes, PDFs, inbox state, feedback and evaluation receipts stay in this private
Git repository and its normal commit/backup workflow. They are not public test
fixtures. There is no in-repository fallback.

Before capturing data, resolve a private path:

```sh
python tools/runtime_paths.py cycles/example/criteria.md --write
```

The path is relative to private DATA. Copy a blank template to the returned
location before filling it. Run browser/scrape captures from the verified private
cycle directory, so relative output flags cannot write into this repository.

## Try the executable helpers

A synthetic Maryland ordinary dealer calculation with explicit fees:

```sh
python skills/orchestrator/scripts/otd_calculator.py --state MD --sales 30000 --doc 800 --title 200 --reg 120.50 --forward --json
python skills/orchestrator/scripts/otd_calculator.py --list-states
python skills/orchestrator/scripts/check_freshness.py --report-only
```

The supplied fees are demonstration inputs, not a personalized fee quote.
Supported profiles expire when their evidence becomes stale. See
[state-fee-lookup](skills/state-fee-lookup/SKILL.md) for support boundaries.
`--estimate` performs explicitly requested generic algebra and cannot establish
jurisdictional correctness.

Generate a synthetic research report outside the public repository; replace the temporary
path with an actual system temporary directory:

```sh
python skills/orchestrator/scripts/generate_research_report.py --mode demo --config skills/orchestrator/assets/research_report_config_template.json --output <temporary-directory>/research.html --to-pdf <temporary-directory>/research.pdf
```

For an outward dealer proposal supported by complete written quotes:

```sh
python skills/orchestrator/scripts/generate_dossier.py --mode demo --config skills/orchestrator/assets/dossier_config_template.yaml --output <temporary-directory>/demo.html --to-pdf <temporary-directory>/demo.pdf
```

Demo mode accepts exact generated fixtures only. Real input uses
[dossier live mode](skills/dossier-builder/SKILL.md), private source artifacts and
the evidence required for that document type. Inspect every PDF page; page count
depends on the content. See the [default delivery workflow](skills/orchestrator/references/report_delivery.md)
for how one buying request becomes a private comparison, HTML and PDF package.

## Skills and routing

Choose the narrow helper for a single task; use the orchestrator for a buying
cycle. These are intended routing descriptions, not a claim that every host
model routes every paraphrase correctly.

| Request | Skill |
|---|---|
| help me buy a car | [orchestrator](skills/orchestrator/SKILL.md) |
| compute OTD | [otd-calculator](skills/otd-calculator/SKILL.md) |
| state fee lookup | [state-fee-lookup](skills/state-fee-lookup/SKILL.md) |
| draft counter to dealer | [dealer-reply-drafter](skills/dealer-reply-drafter/SKILL.md) |
| triage dealer replies | [inbox-triage](skills/inbox-triage/SKILL.md) |
| review this CARFAX | [carfax-pdf-review](skills/carfax-pdf-review/SKILL.md) |
| build dossier | [dossier-builder](skills/dossier-builder/SKILL.md) |
| CPO eligibility | [cpo-eligibility](skills/cpo-eligibility/SKILL.md) |
| EV purchase advice | [ev-buyer-helper](skills/ev-buyer-helper/SKILL.md) |
| choose payment method | [payment-method-decider](skills/payment-method-decider/SKILL.md) |
| lease vs cash | [lease-vs-cash-analyzer](skills/lease-vs-cash-analyzer/SKILL.md) |
| value my trade-in | [trade-in-valuator](skills/trade-in-valuator/SKILL.md) |
| collect quote evidence | [quote-evidence-collector](skills/quote-evidence-collector/SKILL.md) |
| shop car insurance | [insurance-shopper](skills/insurance-shopper/SKILL.md) |
| book pre-purchase inspection | [ppi-scheduler](skills/ppi-scheduler/SKILL.md) |
| close day checklist | [close-day-checklist](skills/close-day-checklist/SKILL.md) |

## Validation

```sh
python tools/make_fixtures.py --check
python tools/check_repository.py
python skills/orchestrator/scripts/render_state_data.py --check
python -m unittest discover -s eval -p "test_*.py" -v
python eval/test_rubric.py
```

The offline rubric checks deterministic contracts. `python eval/test_rubric.py --llm`
separately runs actual model tasks and fresh-context review through installed
`llmcall` defaults, with input snapshots and receipts in private DATA. Unavailable,
failed or timed-out model work is reported as such, never counted as a pass.
Do not retry an uncertain execution without reconciliation.

`python eval/run_scenarios.py --llm` tests actual Chinese responses to an Alaska
pickup purchase and a tax/towing follow-up, using a separate reviewer. See
[evaluation instructions](eval/README.md) for scope and result interpretation.

Functional CI covers the business tests on Windows and Linux. Existing PII/data
and style workflows remain in place. Fixtures and local regressions do not test
live email delivery, real tax-office acceptance, or negotiation success.

## Scope and evidence limits

The state dataset includes all states and DC, with explicit unknown fields;
complete verified calculation support is narrower. Manufacturer terms, inventory,
incentives and prices need current verification. Historical reference notes
cannot override current official rules.

EN/CN/ES dossier layouts are available. Localized fixed labels do not translate
arbitrary user prose, and translations need contextual review. The shipped
dealer-email renderer supports ASCII English.

The nine [scenarios](examples/README.md) are generated synthetic inputs and
expected behaviors. They contain no measured purchase outcomes. No savings,
response-time, site-access or fixed-page-count guarantee is made.

MIT. See [LICENSE](LICENSE) and [CHANGELOG.md](CHANGELOG.md).
