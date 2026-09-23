# buy-me-a-car

Research a US car purchase with 16 skills, from the first request to a compared shortlist, buyer report and closing checklist.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-16-green?style=flat)](#orchestrator)
[![Languages](https://img.shields.io/badge/Languages-EN%20%2F%20CN-blue?style=flat)](#languages)
[![Roadmap](https://img.shields.io/badge/Roadmap-v0.2.2%20alpha-purple?style=flat)](ROADMAP.md)

[English](README.md) | [中文版](README_CN.md)

---

## ⭐ Read this first, the design philosophy

A useful buying decision needs comparable costs, vehicle evidence and a next step the buyer can act on. A low advertised price, an incomplete quote or a long list of search results cannot establish that on its own. Five principles guide this workflow:

1. **Compare the whole cost.** Confirm whether the budget means sale price or out-the-door (OTD) total. Show supported taxes, fees and delivery costs separately; leave unknown amounts visible.
2. **Finish the research delivery.** Reuse known requirements, ask for material missing inputs together, and turn the research into a comparison and HTML/PDF report without another prompt.
3. **Keep the buyer in control.** Separate the private ceiling from an authorized outward offer. Draft from actual evidence; obtain authorization for seller contact, bookings or other external commitments.
4. **Make evidence traceable.** Retain source dates, original artifacts, access gaps and conflicting observations. A captured listing is evidence of what was seen, not a guarantee of current availability.
5. **Keep purchase records private.** The public repository is an uninitialized tool. Real requirements, quotes and reports belong in the buyer's verified private companion Git repository.

The operating rules live in the [main skill](skills/orchestrator/SKILL.md) and [default report workflow](skills/orchestrator/references/report_delivery.md).

## What it is (and isn't)

One orchestrator coordinates a US buying cycle; 15 focused skills handle individual jobs such as OTD math, CARFAX review, trade-in valuation, lease comparisons, dealer drafts and closing checks. Use a narrow skill for a single question, or let the orchestrator carry the cycle forward.

A broad buying request includes a market comparison and buyer research HTML/PDF by default. Research can proceed before written dealer quotes exist. An outward dealer proposal has a separate, stricter complete-quote requirement.

This is an agent skill package. It uses search, browser and mailbox tools supplied by the host; it does not install Gmail access, a background scheduler or a booking service. Availability and authorization determine which external actions can run.

## Install

Requires Python 3.10 or newer, Git and the pinned submodules. Install the YAML/PDF dependencies below; use Chromium or Edge for PDF rendering. GitHub CLI (`gh`) is required to verify private storage.

```sh
git clone --recurse-submodules https://github.com/DaizeDong/buy-me-a-car.git
cd buy-me-a-car
python -m pip install -r requirements.txt
git config core.hooksPath .githooks
python tools/install.py
python tools/install.py --apply
python tools/doctor.py
```

The installer previews first, then `--apply` registers all 16 skills under `~/.agents/skills`. Use `--target <skill-directory>` for another host. Existing unrelated skills are preserved through a conflict check. Start a new agent session after installation. Claude plugin hosts can also load the repository as a local plugin through `.claude-plugin/plugin.json`.

For an existing clone, run `git submodule update --init --recursive`. Missing guards must fail explicitly; do not bypass the hooks.

## Config

Create or clone a **private GitHub companion repository** outside this public worktree, create its `data` directory, and authenticate `gh`. Set `BUY_ME_A_CAR_CONFIG` to that companion's root:

```powershell
$env:BUY_ME_A_CAR_CONFIG = "<private-companion-root>"
```

On a POSIX shell, use `export BUY_ME_A_CAR_CONFIG="<private-companion-root>"`. Verify the destination:

```sh
python tools/runtime_paths.py --write
```

The resolver reports the verified private repository and DATA path. Public, unknown, missing and unversioned destinations are rejected. An optional read may report `UNINITIALIZED`; writes require proof of private storage.

Real criteria, captures, quotes, inbox state, PDFs, feedback and evaluation receipts stay in this private Git repository and its normal versioning and backup workflow. There is no public-worktree fallback. To prepare a record, resolve its destination before copying a blank template or filling it:

```sh
python tools/runtime_paths.py cycles/example/criteria.md --write
```

This path is relative to private DATA. Run browser and scraping captures from the verified private cycle directory too.

## 60-second tour

After installation and private-storage setup, describe the car you want and whatever constraints you already know. This starter comes from the [generated synthetic routing corpus](eval/fixtures/routing_prompts.json):

> Help me buy a used compact SUV, ZIP 10001, budget $30000 OTD, cash, within two months.

The workflow then:

1. **Reuses what you supplied.** It groups material missing questions, such as registration location, whether the budget is OTD, seating/cargo needs, payment method and timeline. It keeps researching anything that does not depend on an answer.
2. **Compares actual evidence.** It searches suitable sources, records what could be accessed, deduplicates known VINs and checks vehicle suitability and comparable costs.
3. **Delivers the buying report.** It prepares the report input and renders the comparison, HTML and PDF during initial selection. You do not need to fill a JSON template or ask separately for a longer report.
4. **Continues from the same criteria.** New quotes, inspections and buyer decisions update the private cycle. Approved assumptions stay marked as assumptions without being asked again as unanswered questions.

Your private research package includes:

| Artifact in private DATA | What it helps you decide |
|---|---|
| `master_comparison.md` | Compare candidates, sources, known costs and unresolved evidence. |
| `buyer_research.html` | Review requirements, search coverage, model alternatives, listings, suitability, logistics, ownership risks and recommendations. |
| `buyer_research.pdf` | Read or print the checked report, including next steps and sources. |

The current research renderer produces Chinese reports. Missing quotes and unknown costs remain visible; they do not prevent an initial research report. Seller outreach, bookings and commitments require the relevant authorization and working integrations. See the [delivery workflow](skills/orchestrator/references/report_delivery.md).

## Skills at a glance

There are 16 skills: one orchestrator and 15 focused helpers. Each helper can also be used independently.

| Stage | Skills |
|---|---|
| Research and evidence | [orchestrator](#orchestrator), [quote-evidence-collector](#quote-evidence-collector) |
| Costs and alternatives | [otd-calculator](#otd-calculator), [state-fee-lookup](#state-fee-lookup), [lease-vs-cash-analyzer](#lease-vs-cash-analyzer), [trade-in-valuator](#trade-in-valuator) |
| Vehicle checks | [carfax-pdf-review](#carfax-pdf-review), [cpo-eligibility](#cpo-eligibility), [ev-buyer-helper](#ev-buyer-helper) |
| Replies and reports | [dealer-reply-drafter](#dealer-reply-drafter), [inbox-triage](#inbox-triage), [dossier-builder](#dossier-builder) |
| Payment and collection | [payment-method-decider](#payment-method-decider), [insurance-shopper](#insurance-shopper), [ppi-scheduler](#ppi-scheduler), [close-day-checklist](#close-day-checklist) |

## How to invoke each skill

These are intended routing cues, not a guarantee that every host model routes every paraphrase correctly. The example sentences below are copied from the [generated synthetic routing corpus](eval/fixtures/routing_prompts.json); they are not real buyer records.

### orchestrator

- **Use when**: Plan a purchase from requirements through research, comparison and closing.
- **Triggers**: buy me a car / 帮我买车
- **Synthetic example**: Help me buy a used compact SUV, ZIP 10001, budget $30000 OTD, cash, within two months.
- **Output**: A private buying cycle, market comparison and buyer research HTML/PDF; later actions follow the buyer's authorization.
- **Instructions**: [SKILL.md](skills/orchestrator/SKILL.md)

### otd-calculator

- **Use when**: Calculate OTD from a sale price, or work back from a target OTD.
- **Triggers**: compute OTD / 算落地价
- **Synthetic example**: Compute OTD from a $30000 sale, explicit fees, and a confirmed registering state.
- **Output**: Itemized decimal calculations for supported, current registration and transaction profiles; explicit refusal when unsupported.
- **Instructions**: [SKILL.md](skills/otd-calculator/SKILL.md)

### state-fee-lookup

- **Use when**: Check state tax, fee and trade-in rules before applying them.
- **Triggers**: state fee lookup / 查州税费
- **Synthetic example**: Look up the current state fee rules and tell me which fields still need official verification.
- **Output**: Dated rule evidence, applicability limits and fields still requiring official verification.
- **Instructions**: [SKILL.md](skills/state-fee-lookup/SKILL.md)

### quote-evidence-collector

- **Use when**: Turn listing pages and written quotes into traceable evidence.
- **Triggers**: collect quote evidence / 整理报价证据
- **Synthetic example**: Collect quote evidence from these source links and retain dates and original artifacts.
- **Output**: Dated source records, original artifacts and unresolved discrepancies in private storage.
- **Instructions**: [SKILL.md](skills/quote-evidence-collector/SKILL.md)

### dealer-reply-drafter

- **Use when**: Prepare a reply to a dealer using approved requests and supported offers.
- **Triggers**: draft a counter / 起草还价邮件
- **Synthetic example**: Draft a counter to this dealer email using only my approved offer and documented competing quote.
- **Output**: An ASCII English draft with the authorized offer; the private budget ceiling stays private.
- **Instructions**: [SKILL.md](skills/dealer-reply-drafter/SKILL.md)

### inbox-triage

- **Use when**: Classify dealer replies and track processing without duplicate actions.
- **Triggers**: triage dealer replies / 整理经销商邮件
- **Synthetic example**: Triage dealer replies, identify out-of-office messages, and record processed message IDs.
- **Output**: Message classifications, stable IDs, cursors and operation receipts; host mailbox integration is required.
- **Instructions**: [SKILL.md](skills/inbox-triage/SKILL.md)

### dossier-builder

- **Use when**: Produce a buyer research report or a supported outward dealer proposal.
- **Triggers**: build a dossier / 生成购车报告
- **Synthetic example**: Build a private decision dossier from my verified quotes and inspection evidence.
- **Output**: Validated HTML/PDF. Research permits missing quotes and explicit unknown costs; dealer proposals require complete quotes.
- **Instructions**: [SKILL.md](skills/dossier-builder/SKILL.md)

### carfax-pdf-review

- **Use when**: Review a vehicle-history report or dealer-attached PDF.
- **Triggers**: review CARFAX / 看车辆历史报告
- **Synthetic example**: Review this CARFAX PDF for accident entries and gaps in service records.
- **Output**: Accident, title and service-history findings with document references and follow-up questions.
- **Instructions**: [SKILL.md](skills/carfax-pdf-review/SKILL.md)

### cpo-eligibility

- **Use when**: Verify a factory certified pre-owned claim and its coverage.
- **Triggers**: check CPO / 核实原厂认证
- **Synthetic example**: Check factory CPO eligibility and current coverage for this used vehicle.
- **Output**: Eligibility and warranty checks against current manufacturer terms and the actual vehicle.
- **Instructions**: [SKILL.md](skills/cpo-eligibility/SKILL.md)

### ev-buyer-helper

- **Use when**: Evaluate an EV or plug-in hybrid for charging, battery and incentive fit.
- **Triggers**: EV purchase advice / 电动车购车建议
- **Synthetic example**: Help me check current EV purchase incentives and whether I can charge at home.
- **Output**: Charging and battery checks, dated incentive eligibility and unresolved purchase conditions.
- **Instructions**: [SKILL.md](skills/ev-buyer-helper/SKILL.md)

### lease-vs-cash-analyzer

- **Use when**: Compare quoted lease terms with a cash purchase.
- **Triggers**: lease vs cash / 租赁还是现金买
- **Synthetic example**: Compare lease vs cash purchase using the quoted money factor and residual.
- **Output**: Comparable cost calculations with term, mileage, residual and money-factor assumptions exposed.
- **Instructions**: [SKILL.md](skills/lease-vs-cash-analyzer/SKILL.md)

### trade-in-valuator

- **Use when**: Separate a trade-in's value from its loan balance and purchase terms.
- **Triggers**: value my trade-in / 估算置换价
- **Synthetic example**: Value my trade-in separately from its lien payoff and purchase tax treatment.
- **Output**: Valuation evidence, lien-payoff treatment and any supported tax-credit effect.
- **Instructions**: [SKILL.md](skills/trade-in-valuator/SKILL.md)

### payment-method-decider

- **Use when**: Choose a payment method accepted for the actual transaction.
- **Triggers**: choose payment method / 选付款方式
- **Synthetic example**: Choose payment method: cashier check or credit card with a 3 percent surcharge.
- **Output**: A payment plan covering limits, surcharges, timing and verified recipient details.
- **Instructions**: [SKILL.md](skills/payment-method-decider/SKILL.md)

### insurance-shopper

- **Use when**: Compare insurance and confirm coverage before collection.
- **Triggers**: shop car insurance / 比较车险
- **Synthetic example**: Shop car insurance and confirm the coverage binder required before collection.
- **Output**: Comparable coverage questions and a binder checklist; binding coverage requires authorization and an insurer.
- **Instructions**: [SKILL.md](skills/insurance-shopper/SKILL.md)

### ppi-scheduler

- **Use when**: Arrange an independent pre-purchase inspection.
- **Triggers**: book pre-purchase inspection / 安排购前检查
- **Synthetic example**: Plan how to book pre-purchase inspection with an independent mechanic.
- **Output**: Mechanic options, inspection scope, booking preparation and receipt tracking for authorized actions.
- **Instructions**: [SKILL.md](skills/ppi-scheduler/SKILL.md)

### close-day-checklist

- **Use when**: Review the contract, payment and handover before signing.
- **Triggers**: close day checklist / 签约交车清单
- **Synthetic example**: Give me the close day checklist before I sign the purchase contract.
- **Output**: Buyer-type checklists, add-on refusal language, stop conditions and required handover documents.
- **Instructions**: [SKILL.md](skills/close-day-checklist/SKILL.md)

## Trigger routing

When a request spans several tasks, the orchestrator coordinates the helpers. The requested output determines the entry point.

| Request | Entry point |
|---|---|
| Find a car and help me choose | [orchestrator](#orchestrator), including default research delivery |
| Calculate OTD or check a fee rule | [otd-calculator](#otd-calculator) and [state-fee-lookup](#state-fee-lookup) |
| Review a vehicle-history document | [carfax-pdf-review](#carfax-pdf-review) |
| Reply to a dealer using existing evidence | [dealer-reply-drafter](#dealer-reply-drafter) |
| Build a research report or supported dealer proposal | [dossier-builder](#dossier-builder), with the matching document requirements |
| Plan an inspection or prepare to sign | [ppi-scheduler](#ppi-scheduler) or [close-day-checklist](#close-day-checklist) |

## Example output

The [nine worked scenarios](examples/README.md) contain generator-produced fictional inputs and expected behavior. They illustrate how the tool should respond; they are not measured buying outcomes.

To inspect sample documents, replace `<temporary-directory>` below with an actual system temporary directory outside the public repository:

```sh
python skills/orchestrator/scripts/generate_research_report.py --mode demo --config skills/orchestrator/assets/research_report_config_template.json --output <temporary-directory>/research.html --to-pdf <temporary-directory>/research.pdf
python skills/orchestrator/scripts/generate_dossier.py --mode demo --config skills/orchestrator/assets/dossier_config_template.yaml --output <temporary-directory>/proposal.html --to-pdf <temporary-directory>/proposal.pdf
```

Demo mode accepts only exact generated fixtures. Real input uses [live mode](skills/dossier-builder/SKILL.md), private source artifacts and the evidence required for that document type. Buyer research permits zero written quotes; outward dealer proposals require complete written quotes. Inspect every PDF page; report length follows the evidence.

A synthetic Maryland ordinary-dealer calculation with explicit demonstration fees:

```sh
python skills/orchestrator/scripts/otd_calculator.py --state MD --sales 30000 --doc 800 --title 200 --reg 120.50 --forward --json
python skills/orchestrator/scripts/otd_calculator.py --list-states
python skills/orchestrator/scripts/check_freshness.py --report-only
```

These fees are demonstration inputs, not a personalized quote. Supported profiles expire when their evidence becomes stale. `--estimate` performs explicitly requested generic algebra without establishing jurisdictional correctness.

## Validation

Run the deterministic checks from the repository root:

```sh
python tools/make_fixtures.py --check
python tools/check_repository.py
python skills/orchestrator/scripts/render_state_data.py --check
python -m unittest discover -s eval -p "test_*.py" -v
python eval/test_rubric.py
```

The offline rubric checks program contracts. `python eval/test_rubric.py --llm` separately runs actual model tasks and fresh-context review through the installed `llmcall` defaults, preserving inputs and receipts in private DATA. Failed, unavailable and timed-out model work is reported explicitly; uncertain actions must be reconciled before retry.

`python eval/run_scenarios.py --llm` tests generated Alaska pickup requests and a tax/towing follow-up with a separate reviewer. See the [evaluation guide](eval/README.md) for scope and result interpretation.

Functional CI covers Windows and Linux, alongside PII/data, style and loading-budget checks. Offline fixtures do not test live delivery, tax-office acceptance or negotiation success.

## Limitations

- The state dataset covers all states and DC with explicit unknown fields. Verified calculation support is narrower and depends on the registration locality and transaction profile.
- Inventory, incentives, warranty terms and fees require current verification. Source dates and hashes establish captured evidence, not seller truth or continued availability.
- Search/browser access, Gmail, scheduling, delivery and booking depend on the host and authorization. An unavailable integration cannot be made usable by a passing local test.
- The shipped dealer-email renderer supports ASCII English. Document language support is listed below; fixed labels do not translate arbitrary user prose.
- Synthetic scenarios establish neither purchase savings nor real-world outcomes. There is no guaranteed response time, site coverage or page count.

## Languages

English (`README.md`, authoritative) and Chinese (`README_CN.md`) mirror the same guide.

| Surface | Current support |
|---|---|
| Buying conversation and routing cues | English, Chinese and Spanish; routing depends on the host model. |
| Buyer research renderer | Chinese. |
| Dealer-proposal layouts | English, Chinese and Spanish fixed labels; supplied prose needs its own translation and contextual review. |
| Dealer-email renderer | ASCII English. |

## Roadmap · Contributing · License

See [ROADMAP.md](ROADMAP.md) for remaining work and [CHANGELOG.md](CHANGELOG.md) for changes. Contributions should include reproducible synthetic cases, current sources where applicable and the relevant validation results. Open an [issue](https://github.com/DaizeDong/buy-me-a-car/issues) or a [pull request](https://github.com/DaizeDong/buy-me-a-car/pulls) without private purchase records.

Released under the [MIT license](LICENSE).
