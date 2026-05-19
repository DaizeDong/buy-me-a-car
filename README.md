# buy-me-a-car

15 Claude Code skills that turn a used-car weekend into a 2-hour decision: scrape 9 sites in parallel, draft counter-offers, print a buyer-grade dossier.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![All 50 States](https://img.shields.io/badge/Tax%20Data-50%20States%20%2B%20DC-green?style=flat)](skills/orchestrator/references/state_fees.md)
[![Roadmap](https://img.shields.io/badge/Roadmap-v0.2.1%20alpha-purple?style=flat)](ROADMAP.md)

[English](README.md) | [中文版](README_CN.md)

---

## Install

```
/plugin install github:DaizeDong/buy-me-a-car
```

Or clone manually:

```bash
git clone https://github.com/DaizeDong/buy-me-a-car.git ~/.claude/plugins/buy-me-a-car
```

Skills auto-activate on phrases like `help me buy a car`, `draft a reply to dealer`, `compute OTD`, `review CARFAX`, etc.

---

## 60-second tour

You say:

```
help me buy a used compact SUV this week, budget $25k OTD, under 60k miles, near <ZIP>
```

What runs automatically:

1. Confirms 9 criteria + buyer-type router (cash / financing / trade-in / EV / pickup)
2. Parallel subagents scrape **9 sites** (Carfax, CarMax, Carvana, Cars.com, AutoTrader, Edmunds, TrueCar, CarGurus, Enterprise) and dedupe by VIN
3. Submits lead forms to top 30 candidates via Playwright MCP (anti-bot aware)
4. **15-min cron** monitors Gmail; triages dealer replies into 4 buckets (real / OOO / CRM / spam)
5. Drafts plain-ASCII counter-offers using **3-anchor logic** (dealer's own price spread + regional comp + your locked OTDs)
6. Extracts red flags from dealer-attached **CARFAX / proposal PDFs**
7. Generates **8-page dossier** (HTML → headless-Chrome PDF, EN or CN template)
8. Close-day checklist with verbatim **F&I add-on hard-no script**

Output: typically **$5-9k saved** vs walking in cold.

---

## Skills at a glance

15 skills total: 1 broad orchestrator + 14 narrow-trigger sub-skills. Sub-skills work standalone; the orchestrator routes to them inside the 9-phase pipeline.

| Bucket | Skills |
|---|---|
| **Research & shortlist** | [orchestrator](#orchestrator) · [inbox-triage](#inbox-triage) · [quote-evidence-collector](#quote-evidence-collector) |
| **Price math & paperwork** | [otd-calculator](#otd-calculator) · [state-fee-lookup](#state-fee-lookup) · [trade-in-valuator](#trade-in-valuator) |
| **Negotiate** | [dealer-reply-drafter](#dealer-reply-drafter) · [dossier-builder](#dossier-builder) |
| **Decide & verify** | [lease-vs-cash-analyzer](#lease-vs-cash-analyzer) · [payment-method-decider](#payment-method-decider) · [ev-buyer-helper](#ev-buyer-helper) · [cpo-eligibility](#cpo-eligibility) · [carfax-pdf-review](#carfax-pdf-review) |
| **Close** | [ppi-scheduler](#ppi-scheduler) · [close-day-checklist](#close-day-checklist) |

---

## How to invoke each skill

Each block: when to use, trigger phrases, one-line example, what comes back.

### orchestrator
- **Use when**: you want the full 9-phase pipeline from scratch.
- **Triggers**: `buy me a car`, `find me a car`, `帮我找车`, `买车`
- **Example**: `help me buy a 2022-2024 Outback Premium under 60k miles within 50mi of <ZIP>, budget $32k OTD`
- **Output**: phase-by-phase artifacts under a `car_buying_<YEAR>/` working dir.

### otd-calculator
- **Use when**: convert sale price → OTD, or reverse-engineer max sale from target OTD.
- **Triggers**: `compute OTD`, `OTD math`, `算 OTD`, `算总价`
- **Example**: `compute OTD for $30k sale in NJ with $499 doc fee`
- **Output**: itemized OTD (tax / doc / title / reg / DMV) for all 50 states + DC.

### state-fee-lookup
- **Use when**: pull the 6-field summary (rate / local / doc cap / title / reg / trade credit) for any state.
- **Triggers**: `doc fee in NJ`, `state 税率`, `trade-in credit`
- **Example**: `what's TX doc fee cap and EV reg surcharge`
- **Output**: state summary + "Does NOT have" leak-detection list (catches NJ tire fee on a CT quote, etc.).

### cpo-eligibility
- **Use when**: verify factory CPO eligibility + embedded $ value before paying the CPO premium.
- **Triggers**: `is this car CPO`, `Subaru CPO`, `Honda Certified`, `CPO 资格`
- **Example**: `check CPO on 2021 Kia Telluride @ 55k miles`
- **Output**: eligibility verdict (8-brand matrix), embedded $1-3k value, fake-CPO red flags.

### carfax-pdf-review
- **Use when**: dealer sent you CARFAX / service-record / F&I-proposal PDFs.
- **Triggers**: `review this CARFAX`, `审 PDF`, `F&I add-on detection`
- **Example**: `review the CARFAX dealer just emailed`
- **Output**: structured red-flag report (accidents, service gaps with $ ranges, 12 challengeable F&I add-ons).

### dealer-reply-drafter
- **Use when**: draft ONE outbound reply — counter / follow-up / walk-away.
- **Triggers**: `draft counter to dealer`, `回复 dealer`, `对 dealer 报价做 counter`
- **Example**: `draft a counter to this Honda dealer's $33k OTD, target $30.75k`
- **Output**: Gmail draft (saved, not sent), ~10 lines, plain ASCII, 3 asks + 1 anchor + 1 walk-away.

### inbox-triage
- **Use when**: dealer inbox piling up — separate real replies from CRM noise.
- **Triggers**: `check my dealer inbox`, `看下邮箱`, `dealer 回复了吗`
- **Example**: `triage today's dealer inbox`
- **Output**: per-bucket counts (real / OOO / CRM / spam), Gmail labels applied, handoff list to dealer-reply-drafter.

### dossier-builder
- **Use when**: print a buyer-grade research packet before the test drive.
- **Triggers**: `build dossier`, `生成 PDF`, `make dossier`
- **Example**: `generate the dossier PDF in Chinese template`
- **Output**: 8-page HTML + headless-Chrome PDF (EN or CN), covering market avg / OTD / CPO embedded value / dealer anchor analysis.

### ev-buyer-helper
- **Use when**: buyer is going EV — federal §30D POS transfer, §25E used, §45W lease, state stack.
- **Triggers**: `EV federal credit`, `$7,500 POS`, `电车补贴`
- **Example**: `is the Ioniq 5 SEL eligible for $7,500 POS in NJ`
- **Output**: net price after credits + dealer IRS-reg verification + NACS/CCS1 adapter guidance.

### payment-method-decider
- **Use when**: choose close-day instrument — cashier's check / credit card / wire / lease cap reduction.
- **Triggers**: `cash or CC for car`, `支付方式`, `Visa for $30k car`
- **Example**: `should I put $30k on my 3% cashback Visa or cashier's check`
- **Output**: method recommendation with CC-rewards-vs-surcharge break-even math.

### lease-vs-cash-analyzer
- **Use when**: dealer offered a lease — verify MF / residual / acquisition / disposition.
- **Triggers**: `lease or buy`, `money factor markup`, `租还是买`
- **Example**: `is this Ioniq 5 SEL lease quote at $575/mo honest`
- **Output**: monthly breakdown + LEASE / BUY / BREAK-EVEN verdict by ownership horizon.

### trade-in-valuator
- **Use when**: trading in — 4-anchor valuation + lien payoff workflow.
- **Triggers**: `valuate my trade`, `评估置换车`, `trade-in tax credit`
- **Example**: `what's my 2017 Civic worth as trade in NJ`
- **Output**: 4-anchor table (KBB Instant / Trade-in / Private / Wholesale) + TRADE vs SEPARATE-SELL decision.

### quote-evidence-collector
- **Use when**: collect REAL dealer-quote screenshots from XHS / Reddit / FB as negotiation anchors.
- **Triggers**: `find quote screenshots`, `搜集报价截图`, `find dealer evidence`
- **Example**: `find XHS quotes for 2024 Outback Premium in <your state>`
- **Output**: REAL-tagged compressed `_FINAL_*.jpg` (1300px, 100-300 KB) ready for manual paperclip.

### ppi-scheduler
- **Use when**: ready to book pre-purchase inspection — mobile-PPI services by region.
- **Triggers**: `book PPI`, `提车前检车`, `mobile inspector`
- **Example**: `book a mobile PPI tomorrow for a 2022 Outback at a local dealer`
- **Output**: bookings (ID + cancel deadline) + post-inspection PROCEED / COUNTER / WALK matrix.

### close-day-checklist
- **Use when**: tomorrow is close day — buyer-type checklists + F&I add-on hard-no script.
- **Triggers**: `ready to close`, `F&I add-on refusal`, `提车清单`
- **Example**: `give me the close-day checklist for tomorrow cash buyer with trade-in`
- **Output**: pre / on-site / post checklists + verbatim F&I scripts.

---

## Five iron rules

Non-negotiable. Each one comes from a specific dollar-loss incident:

1. **OTD only** — never negotiate sale price / tax / fee separately, only the total out-the-door number.
2. **Plain ASCII emails** — no markdown, em-dash, smart quotes. Dealer mail clients render them as literal characters.
3. **3-anchor counters** — every reply cites (a) dealer's own internal price spread, (b) regional market comp, (c) your locked competitor OTD.
4. **15-min cron sweep** — Gmail polled automatically; never let a human manually refresh.
5. **Walk-away threshold** — over budget or counter rejected = polite walk. Preserving optionality beats grabbing one deal.

Full rule set in [`SKILL.md`](skills/orchestrator/SKILL.md).

---

## Trigger routing

When a query could activate multiple skills, the **most narrow + specific** trigger wins:

| If user says | Activates | Not |
|---|---|---|
| "help me buy a car" | `orchestrator` | sub-skills |
| "draft reply to dealer" | `dealer-reply-drafter` | `orchestrator` |
| "compute OTD" | `otd-calculator` | `orchestrator` |
| "doc fee in NJ" | `state-fee-lookup` | `otd-calculator` |
| "lease or buy" | `lease-vs-cash-analyzer` | `payment-method-decider` |
| "Visa for $30k car" | `payment-method-decider` | `lease-vs-cash-analyzer` |
| "find quote screenshots" | `quote-evidence-collector` | `orchestrator` |
| "$7,500 EV credit" | `ev-buyer-helper` | `payment-method-decider` |
| "book PPI" | `ppi-scheduler` | `orchestrator` |
| "review this CARFAX" | `carfax-pdf-review` | `orchestrator` |
| "is this car CPO" | `cpo-eligibility` | `carfax-pdf-review` |
| "build dossier PDF" | `dossier-builder` | `orchestrator` |
| "check inbox" | `inbox-triage` | `orchestrator` |
| "valuate trade-in" | `trade-in-valuator` | `otd-calculator` |
| "ready to close" | `close-day-checklist` | `orchestrator` |

If ambiguous, name the skill explicitly: `use dealer-reply-drafter to draft this`. Unsure which one? Call `orchestrator` — it routes internally.

---

## Example output

![market matrix + dedup](./examples/market_en.png)

What Phase 2 produces: a 9-site capability matrix (top) + VIN-deduped candidate list with deal tags (bottom), auto-rendered as Markdown tables.

---

## Self-check

Verify the install:

```bash
ls skills/   # should show 15 directories
python skills/orchestrator/scripts/otd_calculator.py --state NJ --sale-price 25000
python skills/orchestrator/scripts/generate_dossier.py \
  --config skills/orchestrator/assets/dossier_config_template.yaml \
  --output /tmp/test.html
```

Any failure → open an issue with the traceback. Most failures are Python deps (`PyYAML`, `Jinja2`) or Chrome headless path.

---

## Limitations

- **Single-author alpha** — workflow based on one real purchase cycle + 5 stress-test scenarios. Not multi-market validated.
- **Data drifts** — state fees, CPO terms, and EV credits were last verified 2026-05-18; major bills may have passed since.
- **Anti-bot fragile** — CarGurus / Cars.com / AutoTrader / Edmunds / TrueCar depend on Playwright MCP and may break with site redesigns.
- **Not tax / legal / financial advice** — verify with licensed professionals before signing.

---

## Roadmap · Contributing · License

[ROADMAP.md](ROADMAP.md) tracks v0.3.0 / v1.0.0 plans (multi-author data, adversarial dealer tests, 50-state fill-in, more brand CPO). Pick one → open issue → PR.

MIT — fork it, ship it, save someone money.

_last_verified: 2026-05-18_
