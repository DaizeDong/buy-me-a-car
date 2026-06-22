---
name: Buy Me a Car
description: Use when the user wants help researching, contacting dealers about, negotiating, or finalizing a car purchase (used or new). Triggers include "buy me a car", "find me a car", "research cars", "email dealers", "compare quotes", "negotiate OTD", "buy a Subaru/Toyota/Honda/Mazda", and Chinese phrases "帮我找车", "买车", "选车", "砍价", "对比经销商". Runs end-to-end: multi-site inventory search, mass dealer outreach, Gmail reply monitoring on a cron, OTD negotiation with market-data anchors, CARFAX/service-record PDF analysis, and decision dossiers for test drives.
---

# Buy Me a Car

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **Caveat (cont)**: This is a 0.2.0 alpha release. Sub-skills handle narrow tasks; this orchestrator runs the full pipeline.

End-to-end pre-purchase workflow for new and used cars. Tuned for Subaru/Honda/Toyota/Mazda SUVs in the NJ tri-state area but the structure generalizes.

## When To Use

- Buyer wants to evaluate inventory across multiple dealers / sites
- Buyer wants written OTD by email before stepping on a lot
- Buyer needs a market-data-backed anchor for a counter-offer
- Buyer wants a CARFAX, service-record, or dealer-proposal PDF analyzed
- Buyer is comparing 2-4 final candidates and needs a decision dossier
- Buyer is mid-cycle and needs replies drafted to dealer emails

## When NOT To Use

- Purchase is already closed (paperwork signed) — direct user to a delivery checklist instead
- Pure mechanical-repair, EV-charging, lease-return, or insurance questions
- "Just tell me what car to buy" with no constraints — go back to Phase 1 and gather requirements first
- Quick price-check that does NOT require dealer outreach — answer directly with `references/deal_data_sources.md` Firecrawl pipeline only

## Critical Rules (Non-Negotiable)

Violations of these have caused real-world deal damage. Apply automatically.

1. **Plain ASCII in every outbound email.** No `**bold**`, no em-dash `—`, no markdown links, no backticks. Strip before saving any Gmail draft. See `references/email_format_rules.md`.
2. **Data before estimates.** Pull `references/deal_data_sources.md` Firecrawl pipeline BEFORE quoting any OTD, discount, or "is $X reasonable" answer. Heuristics are wrong by $1-3k.
3. **Written OTD before any in-person visit.** If a dealer refuses to send the full breakdown by email, decline the visit and pivot.
4. **Read the actual CARFAX PDF/URL yourself.** Verbal "clean 1-owner" claims have a real failure rate. See gotcha V2.
5. **Never mix used-car and new-car anchors in the same dealer email.** Used and new desks have different incentive structures; mixing kills negotiation. See gotcha D5.
6. **Verify tracker history against Gmail before acting on it.** Past sessions may have invented dealer dialogue. See gotcha H1.
7. **Phase 4 emails may only cite REAL-tagged baseline rows.** Synthesized / placeholder rows are for internal reasoning only. Never paste a synthesized Reddit anecdote, fabricated dealer number, or generic "buyers report X" into a dealer email — it converts internal-reasoning data into a fabricated citation, which is unrecoverable if challenged.

## Workflow Phases

### Phase 1: Define Requirements

Collect from the user in one focused message (not a barrage):

| Field | Example |
|---|---|
| Make / model / trim | "Subaru Forester Premium or Limited" |
| Year range | "2019-2024" |
| Mileage cap | "under 60,000" |
| Budget (mark OTD vs sales-price) | "$20-30k **OTD** (all-in: price + tax + doc + reg + DMV)" |
| ZIP + radius | "within 50 mi of <ZIP>" |
| **Payment method** (with detail) | "3% cashback Visa, $50k monthly cap" |
| Timeline | "this week" / "this month" / "casual" |
| Must-haves | "AWD, heated seats, CarPlay" |
| **Walk-away ceiling** (single number, hard stop) | "$30,500 OTD — above this I walk no matter what; distinct from the range upper bound" |

**Payment method is load-bearing.** A $32k cash OTD becomes $32,960 with a 3% CC surcharge. Without explicit payment detail, OTD targets are not actionable. See `references/payment_methods.md` for the decision matrix (cashier's check, debit, CC tiers, lease cash conversion).

**OTD vs sales-price clarifier (mandatory).** If the buyer's budget answer does NOT contain "OTD" / "out-the-door" / "all-in", you MUST ask back: *"Is that out-the-door (all in: price + tax + doc + reg + DMV) or sales-price only?"* before saving `criteria.md`. A $28k sales-price target and a $28k OTD target are ~$2-3k apart and drive different dealer asks.

**Walk-away ceiling note.** This number is what Phase 6 enforces as the absolute stop. Do not negotiate above it for any reason.

**Buyer-type router (mandatory).** Before saving `criteria.md`, ask three Y/N gates. Each YES unlocks a sub-question block layered ON TOP of the 9-field core table. The 9-field core covers the cash-buyer + used-car + single-state default; the router branches handle the common non-default axes.

| Gate | If YES, ask the sub-question set from |
|---|---|
| **Financing?** (auto loan, lease, or captive — anything other than full cash / cashier's check / debit) | `references/payment_methods.md` § **"Financing buyer sub-questions"** — 9 fields: lender + product, APR (locked vs quoted), term in months, max financed cap, cash down on hand, max monthly payment willing to carry, pre-approval expiry date, captive-financing openness (TFS / SMF / HFS) if rebate-tied, pre-approval document on hand (hard-pull-locked vs soft-pull-quoted) |
| **Trade-in present?** | Full reference: `references/trade_in.md` (12-field P1 capture set). Ask the structured 12 fields: year/make/model/trim, mileage, title status (clean/branded/salvage), **lien holder + current payoff balance + per-diem interest + payoff letter validity**, key count, cosmetic issues, mechanical issues, KBB Instant Cash Offer (screenshot), KBB Trade-In Value, KBB Private Party Value, estimated Manheim wholesale floor, state trade-in tax credit posture. If buyer has an active lien, ALSO ask: **"Title in hand or held by lien-holder?"** (most states lien-holder holds; NY/MN/PA/MD/KY are exceptions). Routes to `trade_in.md` § 4a-4d lien payoff workflow. |
| **EV?** (battery-electric or PHEV) | EV sub-questions: charging at home (Y/N + L1/L2)? federal $7,500 tax credit eligible (income cap, dealer point-of-sale assignment)? range minimum (mi)? (Full reference covered in `references/ev_buyer_playbook.md`; for Phase 1 capture, ask the 3 fields inline and record on `criteria.md`.) |

If a gate fires YES, append the sub-question answers as a dedicated section in `criteria.md` BELOW the core 9-field table, NOT as additional rows in the core table. Keep the core table stable across buyer types.

**Financing buyer routine — auto-derive the binding constraint.** If the financing gate fires YES AND the answers fill in (max monthly, term, APR, cash down), automatically compute the binding-constraint OTD using:

```
financed_cap_from_monthly = monthly × (1 - (1 + APR/12)^-n) / (APR/12)
effective_OTD_cap        = cash_down + financed_cap_from_monthly
```

Compare `effective_OTD_cap` against the stated walk-away ceiling. If the math lands within $500 of the walk-away, surface in the heads-up block: *"Your monthly cap is the real binding constraint, not your OTD ceiling — real negotiation room is $X, not the apparent $Y."* See worked example in `references/payment_methods.md` § "Financing buyer sub-questions". This routine is **financing-only** — leases use the residual + money-factor math in the Lease Conversion section, not this formula.

**Cross-state surfacing (mandatory when radius spans 2+ states).** If the buyer's ZIP + radius covers more than one state, add a one-paragraph note to the heads-up block: *"Your radius covers [state A, state B, state C]. You'll register in [registering state] so [registering-state]'s tax + reg apply regardless of dealer state. Out-of-state dealers must collect [registering-state] tax, not their home tax. Doc fees vary by dealer state — [state X] caps doc at $[N], [state Y] has no cap. I will force-correct every quote against `references/state_fees.md`."* Also include a 1-line cross-state arbitrage hint when a no-tax / low-doc state is in the radius: *"No-tax states (DE, NH, OR) and low-doc-cap states (NY $175, MD $499, RI $250, IL $347, CA $85) sometimes offer better OTD because they don't reach for fee padding — worth a quote if your radius reaches one."* Reference `references/state_fees.md` cross-state titling table for state-pair specifics; if a row is missing, derive inferentially using the general rule (tax follows registering state).

**DC / VA / MD commuter-corridor sub-case (mandatory when ZIP is in the DC metro).** The DC metro is the most common 3-state commuter corridor in the US: a buyer's daytime address (work, mail) may be in DC while their nighttime address (home, registration) is in VA or MD, or vice versa. The registering-state rule still applies (tax + reg follow the registering state, not the dealer state or commute pattern), but cross-corridor edge cases are real: (a) DC residents must register with DC DMV — DC tax is excise-based (6% under $40k MSRP, scaling up by weight; no traditional sales tax on vehicles) and DC has no doc cap, but VA / MD dealers' CRM defaults often collect VA 4.15% / MD 6% sales tax instead. This is a state-template leak (gotcha D8) — demand re-quote at DC excise. (b) VA residents register with VA DMV at 4.15% Motor Vehicle Sales and Use Tax (capped at min $75, no max) + $899-1,000 typical doc; MD dealers default to MD 6% — also a leak. (c) MD residents register at 6% with $499 statutory doc cap; VA dealers default to VA 4.15% + $899 doc, also a leak (this case the buyer might appear to come out ahead, but at MD DMV titling the 6% will be collected as use tax — buyer ends up paying twice unless dealer re-quotes correctly). (d) **Plate question.** DC residents do NOT carry "VA tags" or "MD tags"; if buyer's daily-drive plates are DC plates but the dealer assumes VA, the registration paperwork goes to the wrong DMV. Confirm at P1 close-day logistics: registering state = the DMV where buyer's driver's license is issued (in 99% of cases). Reference `references/state_fees.md` for VA and MD detail (DC stub may not yet exist; if missing, default to DC = 6% excise on first $40k MSRP, no sales tax, no doc cap, but apply gotcha D8 leak detection against the standard "Has" set since DC's fee structure is distinct from VA / MD).

Save to `criteria.md` in the working directory. Then, BEFORE asking the buyer to confirm, surface a **"Heads-up before you confirm"** block — at most 3 items surfaced to the buyer, but the agent MUST evaluate all 14 checks below internally and pick the top-3 by priority rule.

| Check | Surface when |
|---|---|
| (a) Factual misconception in stated rationale | The buyer's "why" contains a claim that's wrong or partial (e.g., "I want Limited because EyeSight is only on Limited" — wrong, EyeSight is standard on all 2020+ Outback trims). State the correction in one line. |
| (b) Filter that eats >70% of supply | Any single filter (year + miles + trim + color + radius) likely culls supply below ~30% of regional listings. Either run a Carfax-style supply check or flag explicitly: *"This filter combination may leave <N candidates in your radius — consider widening X."* |
| (c) Timeline violates dependency-chain minimums | **Hard threshold: buyer's close target < 5 days from first outreach.** Dependency chain: dealer reply lag (gotcha I1, 12+ hr typical, occasionally 24-48 hr) + cross-bid round 2 negotiation (24-48 hr) + PPI scheduling (gotcha P1, mobile PPI parallel booking needs same-day-plus slots, often T+2) + insurance binder + bank cashier's-check issuance (same-day after 9-10 AM cutoff). Minimum realistic = 5-7 days; 3-day rush forces verbal-only OTD (violates Critical Rule #3) or skipping PPI. Flag as *"Your stated close date is [X] days from first outreach — dependency chain (dealer reply 12-48 hr + cross-bid round 2 + PPI + binder + cashier's check) needs 5-7 days minimum. Either extend close by [N] days or accept skipping PPI / written-OTD verification (NOT recommended)."* |
| (d) Budget-vs-aspirations mismatch | Stated OTD ceiling is materially below the dream-vehicle's typical OTD (e.g., $30k OTD target but desired vehicle is $48k MSRP volume trim). Flag as: *"Your $30k OTD ceiling and your stated target [Year Make Model Trim] don't overlap — typical OTD on this config in your radius is $52-55k. Either widen budget to $50k+ OTD, drop to a lower trim / older MY (typical $30k OTD config: [example]), or pivot to a different model."* |
| (e) Timeline-vs-financing mismatch | Buyer needs financing pre-approval (financing gate fired) but timeline is <5 days, AND pre-approval not yet in hand. Pre-approval pulls: CU = 1-3 business days (typical credit unions), bank = same-day to 2 days, captive = same-day at dealer (locks rate to dealer ecosystem). Flag as: *"Your timeline is [X] days but pre-approval not yet pulled. CU pre-approval takes 1-3 business days; without it, you arrive at the dealer with only captive financing as an option (which means no rate competition). Either pull CU pre-approval today (Phase 1) or extend close by [N] days, or accept captive-only financing."* |
| (f) Stale anchor citation | Buyer cites a benchmark deal that's >6 months old (e.g., "my friend got a 2023 RAV4 XLE for $32k in March 2024" — 14 months old at time of P1). Manufacturer incentives shift quarterly; 6-month-old anchors are unreliable. Flag: *"Your anchor [$X on Y] is [N] months old. Incentive stack and market have shifted since then; I'll pull current Phase 2 baseline at [today's date], expect [+/- $X] vs your anchor. Don't lock to the old number until we see today's data."* |
| (g) Cash buyer pushed to finance | Buyer is paying cash (cash = financing gate NO) but somewhere in their stated rationale they mention "the dealer said I should finance for the rebate" or similar dealer-to-buyer push. Flag: *"Be aware — dealer-financing-tied rebates are sometimes real (see `payment_methods.md` cash-to-lease conversion + captive-vs-CU rebate playbook), but they only win when (a) the captive offers a rebate-tied incentive that exceeds the interest cost, AND (b) early payoff has no prepayment penalty. Don't accept 'finance for the rebate' without running the math; in 50%+ of cases dealer claims the rebate is finance-tied when it isn't."* |
| (h) Trade mentioned without numbers | Buyer mentions a trade-in vehicle but has not provided payoff balance, title status (clean / branded / salvage), lien holder, or KBB Instant Cash Offer screenshot. Flag: *"You mentioned trading in your [vehicle]. Before I can build any OTD math I need: current odometer, title status (clean / branded / salvage), lien holder + payoff balance + per-diem interest if applicable, KBB Instant Cash Offer screenshot, KBB Trade-In Value, KBB Private Party Value. Without these the trade is a placeholder, not a number. See `trade_in.md` for the 12-field set."* |
| (i) High-mileage trade trap | Buyer's trade has >100k mi OR known mechanical issues OR known accident history (per `trade_in.md` fields). KBB Instant Cash Offer often DECLINES at >120k mi or with declared mechanical issues; CarMax / Carvana / dealer wholesale may be substantially lower than KBB trade-in value. Flag: *"Your trade at [N]k mi / [condition] is at high risk of KBB Instant Cash Offer declining and dealer-wholesale being $X below KBB trade-in. Set trade expectation at 70-80% of KBB Trade-In Value (not 100%) and budget for the gap. Consider Private Party sale at $[Y] before dealer trade-in."* |
| (j) EV / Hybrid with no charging plan | EV gate fires YES but buyer reports no home L1 outlet OR no home L2 install path OR no charging address at all (e.g., apartment renter without dedicated parking). Flag: *"You're targeting an EV but charging access is unclear. Without home L1 minimum (10-15 hrs/charge for daily commute), you depend on public DCFC, which runs 3-5x the cost per kWh of home charging ($0.40-$0.60/kWh public vs $0.10-$0.15/kWh home) and adds 30-45 min per session to your routine. If apartment rental, confirm building's L2 install policy OR check public L2 availability within walking distance. May make a hybrid or PHEV (charges on L1) a structurally better fit. See `ev_buyer_playbook.md` § Charging Access."* |
| (k) Cross-state purchase with title-jumping risk | Buyer is purchasing in a no-tax / low-tax state (DE / NH / MT / OR) to register in a tax state (NJ / NY / CA), thinking they'll capture the tax savings. **They will not.** The registering state collects use tax at DMV titling — buyer pays full registering-state rate regardless of where they bought. Flag: *"Buying in [no-tax state] to register in [tax state] does NOT save sales tax. Your registering state ([tax state]) collects [X]% use tax at DMV when you title. The legitimate cross-state advantages are (a) doc fee differentials, (b) inventory access, (c) dealer competition — sales tax avoidance is not one of them. Title-jumping (registering in a no-tax state without actually living there) is fraud and can result in back-taxes + penalties + criminal charges. See `state_fees.md` cross-state titling section."* |
| (l) Rebuilt / salvage / branded title | Buyer's target listing has a rebuilt / salvage / branded title OR buyer's trade does. Buyer often doesn't realize the downstream impact. Flag: *"This vehicle has a [rebuilt / salvage / branded] title. Insurance implications: most carriers only write liability (not comprehensive / collision); a few (State Farm, Geico in some states) refuse coverage. Financing implications: most banks / CUs decline; only specialized lenders (CarFinance, Credit Acceptance) at sub-prime rates. Resale implications: 30-50% discount to clean-title comparable at resale; many dealers won't take in trade. Verify acceptability with your insurer and bank BEFORE confirming."* |
| (m) Fake CPO label | Buyer is targeting a used vehicle the dealer markets as "Certified" but the dealer is NOT the brand's authorized dealer OR no factory CPO certificate is provided. Flag: *"The dealer's 'Certified' label may be dealer-internal marketing, NOT manufacturer CPO. Verify: (a) is the inspecting dealer an authorized [Brand] dealer? (b) request the CPO certificate with manufacturer letterhead. (c) confirm warranty is registered in [Brand]'s CRM under your name. Independent shops' 'Certified' inspections do not carry factory-backed extended warranty, do not include the 150-200-point factory checklist, and do not offer manufacturer roadside / loaner programs. See `subaru_cpo_program.md` / `honda_cpo_program.md` / `toyota_cpo_program.md` for what real factory CPO includes; `vertical_playbooks.md#part-2--heavy--commercial--luxury` § 3.6 for luxury-specific fake-CPO traps."* |
| (n) Filter combination = zero supply | More aggressive than (b) — when the AGGREGATE combination of filters (year + miles + trim + color + interior + radius + payment) likely yields zero candidates. Run a quick supply check on Cars.com / Carfax / AutoTrader before confirming. Flag: *"Your filter combination ([trim X] + [color Y] + [miles <Z] + [radius W mi] + [MY range]) is likely sub-1 listing across your radius. Either widen one filter aggressively (color most-common-relaxed: 4x supply; radius: 2x supply per 50 mi expansion) OR confirm okay to wait for an inbound matching VIN at 4-12 weeks."* |

**Priority rule when >3 fire**: surface the top 3 by impact, in this descending order:

1. (d) Budget-vs-aspirations mismatch — highest impact, often invalidates entire downstream workflow
2. (n) Filter combination = zero supply — wastes Phase 3 dispatch if not flagged
3. (k) Cross-state purchase with title-jumping risk — legal exposure
4. (l) Rebuilt / salvage / branded title — legal / insurance / financing exposure
5. (c) Timeline violates dependency-chain minimums
6. (e) Timeline-vs-financing mismatch
7. (j) EV / Hybrid with no charging plan
8. (i) High-mileage trade trap
9. (h) Trade mentioned without numbers
10. (m) Fake CPO label
11. (a) Factual misconception
12. (b) Filter eats >70% supply
13. (f) Stale anchor citation
14. (g) Cash buyer pushed to finance

When more than 3 fire, surface the top 3 by impact rank. The remaining firings go into a single trailing line: *"Additional minor heads-up items: [list by name; ask for detail on any]."* This keeps the surfaced block scannable while ensuring no detected issue is silently dropped.

Cap at 3 items surfaced. If none apply, say so explicitly ("No heads-up items — filters and timeline look feasible.") and proceed. Then ask for confirmation.

**Close-day logistics — capture once at P1, re-confirm at P9.** Phase 9 close-day execution depends on 6 logistics inputs that re-asking at the last minute often delays close by 24-48 hours. Capture them at Phase 1 sign-off, store in `criteria.md`, and re-confirm verbatim at P9 close-day kickoff. The mini-table below is shared across all buyer-type branches (cash / financing / trade / EV / pickup).

| Field | Example | Why captured at P1 |
|---|---|---|
| **Bank cut-off + branch + hours** | "Chase, local branch, cashier's checks issued M-F 9 AM-5 PM, same-day issuance before 3 PM" | Cashier's check is the gating P9 instrument for cash buyers; bank hours and same-day-issuance window drive close-day morning sequencing. |
| **Insurance carrier (for binder)** | "GEICO policy #12345, agent direct line (xxx) xxx-xxxx; new-vehicle binder needs VIN + closing date, 1-hour turnaround during business hours" | Dealer will not release the vehicle without an active binder; cold-call to a generic carrier on close-day adds 1-3 hours. |
| **Plate decision** | "Transfer existing plate $26 (preferred) vs new plate $151" or "New plate" | Plate transfer math depends on registering state (`state_fees.md`) and saves $25-150 in most states; the decision drives DMV paperwork at close. |
| **Available time windows on close day** | "Wed Apr 24, between 10 AM and 3 PM; hard stop at 3:30 PM for school pickup" | Time-boxes the close; sets when the cashier's check must be ready and which time-window slot to lock with the dealer. |
| **ID set** | "Driver's license (current), Social Security card OR passport, recent utility bill for proof of residence, marriage certificate if name-change since DL issued" | Captives + state DMV both require multiple ID forms; missing items force a re-trip. |
| **Captive vs CU vs cash funding instrument** (if not pure cash) | "Credit-union pre-approval letter (in hand), $X cap, expires May 1; cashier's check issued from the credit union to dealer in dealer name" | Funding instrument determines whether dealer F&I needs to wait on a wire (24-72 hr captive) vs accepts an instant cashier's check (same-day). |

Add this mini-table as a section in `criteria.md` BELOW the Heads-up block. **At Phase 9 close-day kickoff, the agent's first action is to re-read this section from `criteria.md` and confirm each line with the buyer.** Any change since P1 (carrier switched, branch closed for holiday, plate decision flipped) cascades into close-day execution and must be caught BEFORE the buyer drives to the dealer.

**Inline jargon glossing rule.** When `criteria.md`, outbound dealer email, or any buyer-facing artifact emits one of the following terms for the FIRST time in that artifact, include a brief parenthetical gloss. Subsequent uses can drop the gloss.

| Term | Gloss |
|---|---|
| **OTD** | out-the-door (all-in: sale price + tax + doc + title + reg + add-ons) |
| **NA** | Not Applicable (or, in context, North America) |
| **F&I** | Finance & Insurance (the dealer office where add-ons, extended warranties, and financing paperwork are signed) |
| **anchor** | a market data point cited to set the negotiating range (e.g., "Edmunds TMV anchor at $28,500") |
| **walk-away** | the absolute-stop price above which the buyer will not buy; distinct from the budget range upper bound |
| **cross-bid** | a parallel outreach to 3-4 dealers asking for OTDs on the same VIN class so each offer is leverage against the others |
| **ADM** | Additional Dealer Markup (a line item above MSRP — Market Adjustment, Hybrid Premium, Allocation Fee; see gotcha D9) |
| **CPO** | Certified Pre-Owned (a manufacturer-program-certified used vehicle with extended powertrain + B2B warranty — see Subaru/Honda/Toyota CPO refs) |
| **NACS** | North American Charging Standard (Tesla's connector, becoming the EV charging standard 2025-26; replaces CCS1 on Ford/GM/Hyundai/Kia/Rivian/VW/Volvo OEMs) |

The rule is **first-use only**, not every use. Glossing a term twice in one email is more confusing than glossing it zero times. Goal: make buyer-facing artifacts comprehensible without forcing the buyer to look up acronyms mid-decision.

### Phase 2: Baseline Market Data

BEFORE Phase 3 outreach, run the 5-query Firecrawl pipeline to produce `.firecrawl/{model}-deal-baseline.md`:

1. National baseline (CarEdge + Edmunds)
2. State-specific dealer Internet Pricing (top 5 dealers in radius)
3. Recent buyer reports (Reddit / XHS via browser session)
4. Current month manufacturer incentive stack
5. State-specific buyer evidence: **XHS with state keyword** for NJ/NY/CA-concentrated buyer communities (see gotcha S5); **Reddit r/{Make}{Model} + r/{State}Cars** for other states; **Facebook owner groups** (e.g., "F-150 Owners") for older-skew makes/models.

This is the source of truth every subsequent counter cites. Re-pull whenever the buyer references a new external claim ("friend got $X off"). See `references/deal_data_sources.md` for query recipes + source catalog.

### Phase 3: Multi-Site Inventory Research

Dispatch parallel subagents across inventory sites (Carfax / Cars.com / AutoTrader / Edmunds / TrueCar / CarGurus / CarMax / Carvana / OEM SmartPath). Each subagent produces `report_<site>.md` with top-N candidates (VIN, miles, price, dealer, deal tags, link, Delivery Mode for new cars). After all return, generate `master_comparison.md` as the buyer-facing market scan in two sections: a **Site Capability Matrix** on top (one role-tagged row per site — which source to trust for what, ranked Primary / Secondary / Negotiation-lever / Research-only / Plan-B / Skip) and the **VIN-deduplicated candidate list** on the bottom. New-car vs used-car router gate fires before dispatch and changes site set + history-PDF requirement.

**Full details**: see `references/phases.md#phase-3--inventory`.

### Phase 4: Mass Email Outreach

Submit lead forms or send direct emails to the top 30-50 candidates. Capture per dealer: name, address, phone, sales rep, VIN, submission timestamp, anti-bot result. Track in `tracker.md`. Email format per Critical Rule #1; REAL-tagged citation only per Critical Rule #7. Dealer group ownership check (gotcha D11) BEFORE treating multiple stores as independent cross-bids. See SKILL.md § Outbound Email SOP for the full step-by-step ordered procedure.

**Full details**: see `references/phases.md#phase-4--outreach`.

### Phase 5: Recurring Inbox Monitoring

Three scheduled CronCreate jobs (not one): main 15-min inbox cron, 6-hour spam+promotions sweep, 7 AM morning catch-up. OOO autoresponder detection skips drafting and flags tracker until parsed return date. See `references/cron_monitoring.md` for full prompt templates, Gmail search patterns, OOO keyword list. Reply templates in `assets/dealer_reply_template.md`.

**Full details**: see `references/phases.md#phase-5--cron` (stub pointing to `cron_monitoring.md`).

### Phase 6: OTD Negotiation

Always-written, never-verbal OTD ask format with required line items (sales price + state tax + doc fee + title + reg + add-ons). Anchoring techniques: internal-trim, market-comp, cross-dealer (gotcha N1). ADM kill list (gotcha D9) demands removal as precondition, not middle-meet. Escalation Ladder when dealer delays. Bait-and-switch protocol (gotcha D10). Buyer-type specific notes for financing / lease / trade / EV / pickup / heavy-duty / luxury / CPO. See `references/negotiation_playbook.md` for full math + walk-away lines.

**Full details**: see `references/phases.md#phase-6--negotiation`.

### Phase 7: PDF Analysis

For every dealer-attached PDF (CARFAX, service records, OTD proposal, PPI report), open with Read tool and extract: VIN match, owner count, accident / damage / structural / odometer, service record completeness, active recalls. Per-brand expected service tables + ADAS recal by brand + OTD Proposal Add-On Anti-Pattern Detection. See `references/pdf_review_checklist.md` for the full checklist.

**Full details**: see `references/phases.md#phase-7--pdf` (stub pointing to `pdf_review_checklist.md`).

### Phase 8: Decision Dossier

Before test drive, generate a 7-10 page HTML+PDF dossier the buyer brings to the dealer:

```bash
cp assets/dossier_config_template.yaml my_dossier.yaml
$EDITOR my_dossier.yaml
python scripts/generate_dossier.py --config my_dossier.yaml \
  --output my_dossier.html --to-pdf my_dossier.pdf
```

For Chinese-speaking dealers: `--template assets/dossier_template_cn.html`. Placeholders documented in `assets/dossier_config_template.yaml`. Generator validates load-bearing fields + placeholder substitution; auto-detects Chromium-family browsers.

**Full details**: see `references/phases.md#phase-8--dossier`.

### Phase 9: Test Drive + Close

Maintain a PRIVATE `{dealer}_negotiation_prep.md` (buyer-only, never shared) with the dynamic OTD ladder, test-drive checklist, post-drive questions, decision matrix. Re-confirm the close-day logistics mini-table from `criteria.md` (Phase 1 capture) at close-day kickoff. Close-day routing branches by buyer type (cash / financing / trade / EV / pickup) — execute all relevant sub-checklists if multiple apply. F&I close-day hard-no script (gotcha P3) is mandatory.

**Full details**: see `references/phases.md#phase-9--close` (includes all 5 buyer-type sub-checklists + universal close-day cross-references).

## Working Directory Convention

```
C:\Users\<user>\car_buying_<year>\
├── README.md                       index
├── criteria.md                     Phase 1 output
├── dealer_outreach_tracker.md      master tracker (dialogs, OTD log, decisions)
├── <model>_negotiation_prep.md     PRIVATE — buyer-only
├── <model>_dossier.{md,html,pdf}   shareable
├── dealer_pdfs/                    CARFAX / service / proposals
├── market_research/                subagent reports
│   └── reports/
├── .firecrawl/                     Firecrawl outputs
│   ├── {model}-deal-baseline.md
│   └── quote-images/               XHS / dealer screenshots
```

All dealer-related files belong here. No scattering across home / Downloads.

## Mid-Cycle Pivot Protocol

Mid-cycle = the buyer is somewhere between Phase 3 and Phase 9 and changes a load-bearing field that invalidates the in-flight artifacts. Common pivots:

- **Used to new** (or new to used) — different desks, different incentive stacks, mileage adjustments no longer apply.
- **Cash to financing** (or financing to cash) — binding-constraint changes from OTD ceiling to monthly cap; pre-approval / captive paths must be re-asked.
- **Model A to model B** — entire Phase 2 baseline, Phase 3 inventory pull, and Phase 4 outreach become irrelevant; new cross-bid set must be assembled.
- **ZIP / radius change** — registering state may change → tax rate, doc cap, "Has" / "Does NOT have" lists shift; in-flight quotes are state-template-leak suspects.
- **Walk-away ceiling change** — entire OTD ladder + Phase 6 counter-math is rooted in this number.
- **Trade-in added or removed mid-cycle** — separates-the-negotiation tactic must be reset; payoff workflow restarts.
- **EV-eligibility flip** — federal §30D / §25E credit, NACS / CCS1 port, SoH thresholds re-enter; ICE OTD math no longer applies.

When the buyer changes any of these mid-cycle, the protocol is:

1. **STOP all in-flight drafting immediately.** Do not append new context to existing dealer threads. Do not save another draft. Do not send another counter. The next dealer reply that arrives during the pivot is held without drafting until the reset is complete.

2. **Enumerate ALL stale artifacts** in a single message to the buyer. Buyer needs the full list to clean up Gmail drafts, tracker rows, and baseline files. Use this template:

   ```
   Pivot detected: [old value] -> [new value] on field [X].
   The following artifacts are now stale and must be cleaned up
   before we resume:

   Gmail drafts:
     - in:drafts subject:[OLD_MODEL] before:[TODAY]
       (estimated [N] drafts — use this Gmail search string to
       bulk-select for trash)
     - any reply drafts referencing [old payment method / old ZIP /
       old walk-away]

   Working-directory files (review + delete or rename with .STALE
   suffix):
     - criteria.md (entire P1 capture is rooted in the old field)
     - .firecrawl/[OLD_MODEL]-deal-baseline.md (entire Phase 2
       baseline)
     - market_research/reports/report_*.md (Phase 3 site reports
       on the old model)
     - master_comparison.md (Phase 3 dedup)
     - dealer_outreach_tracker.md rows for outreach sent under old
       criteria (do not delete the file; mark rows with
       STATUS=STALE_PIVOT)
     - [old_model]_negotiation_prep.md
     - [old_model]_dossier.{md,html,pdf}

   Dealer-side cleanup:
     - For each dealer with an active thread on the old criteria,
       send a polite walk-away (see assets/dealer_reply_template.md
       "Walk-Away (Polite Close)") OR a pivot note ("Changing
       targets, will be back in touch if [new model] inventory
       overlaps your store"). Do NOT leave dealers hanging — they
       remember and it costs leverage on the next outreach.
   ```

3. **Re-run Phase 1.** Full criteria.md regeneration. Do NOT copy-paste from the old file and edit — the buyer-type router gates (financing / trade / EV), heads-up block, close-day logistics table, and walk-away ceiling all interact, and partial edits leave field-level inconsistencies that surface as bugs later (e.g., old financing fields stay populated after a financing-to-cash pivot, then trigger a binding-constraint computation that no longer applies). Restart from `assets/criteria_template.md`.

4. **Re-pull Phase 2 baseline.** New 5-query Firecrawl pipeline against the new model / state / incentive stack. Save to `.firecrawl/[NEW_MODEL]-deal-baseline.md`. Do NOT reuse the old baseline; manufacturer incentives and regional deal data shift weekly.

5. **Resume Phase 3 and onward** with the new criteria. New inventory pull, new mass outreach, new tracker (or new STATUS=ACTIVE rows in the existing tracker below the STALE_PIVOT rows).

Pivot frequency: empirically, ~30% of buying cycles see at least one load-bearing pivot between Phase 1 and Phase 9. Without this protocol, the agent silently keeps appending new context to stale artifacts, dealer drafts go out with mixed criteria (gotcha D5 firing pattern), tracker rows multiply with no clear cut-line, and the close-day execution operates on wrong assumptions (wrong walk-away, wrong payment instrument, wrong registering state). The protocol forces a hard reset.

**Mini-pivot exception** — changes to non-load-bearing fields (must-haves list edit, color preference, mileage cap ±5k mi, trim swap within same model + same MY + same financing posture) do NOT trigger the full reset. Update criteria.md inline, mark the change in the heads-up block, and proceed. The reset is reserved for the load-bearing axes listed above.

## Resources

### References (load on demand)

| File | Purpose |
|---|---|
| `phases.md` | Combined detail for Phases 3-9 (use anchors `#phase-3--inventory` through `#phase-9--close`): new-vs-used router gate + site table (P3); tracker capture + D11 dealer-group (P4); three-cron architecture + OOO handling (P5, stub → `cron_monitoring.md`); anchors + ADM kill list + escalation ladder + bait-and-switch + buyer-type notes (P6); PDF extraction targets (P7, stub → `pdf_review_checklist.md`); dossier generation pipeline + Chromium auto-detect + CN template (P8); close-day re-confirm + 5 buyer-type sub-checklists (P9) |
| `outreach_strategy.md` | Multi-site outreach, anti-bot handling, multi-channel (email/SMS/phone) |
| `negotiation_playbook.md` | Internal-anchor logic, market-comp anchoring, walk-away lines, cash leverage |
| `pdf_review_checklist.md` | CARFAX / service records / proposal PDF red flags |
| `cron_monitoring.md` | Cron prompt template + Gmail search patterns |
| `email_format_rules.md` | ASCII substitution table, draft hygiene rules |
| `state_fees.md` | All-state summary + detail stubs at CT/CA/TX/IL depth for NJ / NY / PA / CT / MA / RI / NH / ME / VT / CA / TX / IL; cross-state titling; "Does NOT have" leak lists per gotcha D8 |
| `subaru_cpo_program.md` | Subaru CPO eligibility + embedded value math |
| `ppi_booking.md` | PPI parallel-booking, mobile services in NY/NJ/CT, Subaru checklist |
| `deal_data_sources.md` | Firecrawl pipeline, source catalog, Playwright MCP browser workflow, XHS image extraction, image attachment workflow |
| `payment_methods.md` | Cashier's check / debit / CC tiers (Amex/Chase/3% cashback cards), lease cash conversion, pre-close confirmation template |
| `trade_in.md` | Trade-in valuation, ACV-vs-allowance, separate-the-negotiation, state trade-credit, lien payoff workflow, key/cosmetic deducts |
| `ev_buyer_playbook.md` | Federal $7,500 + $4,000 used EV credits, dealer IRS registration, state EV rebate matrix, NACS vs CCS1, charging, range planning, used-EV SoH, EV dealer tactics |
| `honda_cpo_program.md` | Honda True Certified / Certified+ eligibility, coverage, embedded value, CR-V notes |
| `toyota_cpo_program.md` | Toyota Certified Used Vehicle (TCUV) — 160-pt inspection, 7yr/100k powertrain + 1yr/12k B2B + **10yr/150k Hybrid Component coverage** (RAV4 Hybrid / Camry Hybrid / Highlander Hybrid / Sienna / Prius / RAV4 Prime), embedded value $1,000-$2,000 ICE / $2,500-$4,000 Hybrid, market premium $1,000-$2,000 |
| `hyundai_cpo_program.md` | Hyundai CPO — 173-pt inspection, **10yr/100k powertrain from in-service (industry-longest, tied with Kia)** + 1yr/12k B2B + **10yr/100k HV battery coverage on Ioniq 5/6 / Kona Electric**, SmartSense ADAS recal $400-$1,200, embedded value $1,500-$2,500 ICE / $3,000-$4,500 EV, market premium $800-$1,500. Note Genesis CPO separate (P3.5). |
| `kia_cpo_program.md` | Kia CPO — 165-pt inspection, **10yr/100k powertrain from in-service** + 1yr/12k B2B + **8yr/100k Hybrid Component coverage (Sorento/Sportage/Niro/Carnival Hybrid)** + **10yr/100k HV battery on EV6/Niro EV/EV9**, $50 B2B deductible, embedded value $1,200-$2,000 ICE / $2,000-$3,000 Hybrid / $2,800-$4,200 EV, market premium $700-$1,500 |
| `ford_bluecert_program.md` | Ford Blue Advantage **two-tier** — Gold (172-pt, 6yr/80k, 7yr/100k powertrain + 12mo/12k B2B + **PowerStroke diesel 7/100k tier** + 8/100k EV battery on Lightning/Mach-E) vs Blue (139-pt, 10yr/120k, 90day/4k only — marketing-grade not factory-backed). $100 deductible. Gold embedded value $1,500-$2,500 ICE / $2,500-$4,000 diesel; Blue $400-$800 |
| `gm_cpo_program.md` | GM CPO (Chevy / GMC / Buick) — 172-pt inspection, 6yr/100k powertrain + 12mo/12k B2B + **Duramax diesel 5/100k tier** + 8yr/100k HV battery on Bolt/Hummer EV/Lyriq/Blazer EV/Equinox EV/Silverado EV (10/150k in CA-emission states); 2 included maintenance visits. **Bolt 2017-2022 LG Chem recall remedy verification mandatory at CPO close**. Embedded value $1,500-$2,500 ICE / $2,500-$3,500 diesel / $2,000-$3,200 EV. Cadillac CPO separate (P3.5). |
| `mazda_cpo_program.md` | Mazda CPO — 150-pt inspection, 7yr/100k powertrain + 12mo/12k B2B; no separate diesel / hybrid / EV tier (CX-50 Hybrid & CX-90 PHEV roll into powertrain). All-CarPlay-standard-since-2018. CX-50 built at MTMUS Huntsville AL JV with Toyota. **Narrowest CPO-win-zone ($800 break-even) due to Mazda reliability**. MX-5 Miata: CPO premium often justified by resale persistence above embedded warranty value. Embedded value $1,000-$1,800, market premium $600-$1,200 |
| `vertical_playbooks.md#part-1--pickup-truck-specifics` | Tow rating dependency (engine × axle × pkg), factory vs aftermarket tow, payload, pickup PPI items (frame/suspension/exhaust/turbo), depreciation, pickup dealer tactics |
| `lease_playbook.md` | Lease math (Cap Cost / Residual / MF / Term / Allowance), state lease-tax mechanics (NJ vs CA vs TX vs IL up-front load), money factor markup + buy-rate counter, captive-by-captive rules (TFS / SMF / HFS / Ford / GM / BMW / MB / Audi / Lexus / Stellantis), EV lease arbitrage ($7,500 § 45W pass-through), lease assumption, walk-away vs pre-purchase miles, lease conversion (cash-to-lease) decision math |
| `vertical_playbooks.md#part-2--heavy--commercial--luxury` | Heavy-duty pickups (F-250+ / RAM 2500+ / GM 2500HD+: GCWR, diesel emissions LEGAL warning, commercial registration), commercial vans (Transit / Sprinter / ProMaster / Express: § 179 + bonus depreciation, fleet pricing, upfit), luxury brand defaults (BMW / MB / Audi / Lexus / Genesis / Acura / Infiniti / Cadillac / Lincoln: 60-70% lease penetration, included service plans, MSDs, performance-trim premium, fake-CPO detection), sub-axes (ultra-luxury / exotic / high-end performance) |

### Assets (templates — copy and edit)

| File | Use |
|---|---|
| `criteria_template.md` | Phase 1 criteria skeleton (walk-away ceiling, OTD-vs-sales-price marker, heads-up block) |
| `dealer_reply_template.md` | OTD ask / anti-pressure / walk-away / add-on refusal templates |
| `tracker_template.md` | Tracker file skeleton |
| `negotiation_prep_template.md` | Private prep file with OTD ladder |
| `dossier_template.html` / `dossier_template_cn.html` | Print-ready 8-page dossier (EN / CN) |
| `dossier_config_template.yaml` | YAML for dossier placeholder substitution |

### Scripts (utilities)

| Script | Purpose |
|---|---|
| `otd_calculator.py` | Reverse-engineer sales price from OTD target + state tax + fees |
| `mileage_adjustment.py` | $/mile depreciation comp adjustments |
| `generate_dossier.py` | YAML → HTML + PDF dossier (Chrome/Edge auto-detect) |
| `html_to_pdf.sh` | Chrome headless HTML to PDF |

## Outbound Email SOP (Composition + Attachment)

This is the ordered procedure for any dealer outreach — first-touch, counter, or follow-up. Following the order prevents the most common failure modes (draft accumulation, illegible inline images, mixed anchors).

### Step 0: Gather requirements ONCE before opening a draft

Ask in a single message (not piecemeal):

- Exact trim / option package (e.g., "Premium with Option Package 15", not "Premium Hybrid or Premium gas")
- Payment method with detail (card name + monthly cashback cap if CC, see `references/payment_methods.md`)
- Attachment plan: which screenshots, manual or inline (default: manual)
- Used-car vs new-car context: which thread is this? Do NOT mix in counters.
- Deadline / close date for inclusion in walk-away line

If buyer answers vaguely, ask follow-ups before drafting. Drafting before this is locked = inevitable iteration = clutter (see E4).

**Email-type branching (pick ONE before drafting).** First-touch / counter / follow-up have different shapes; lumping them is the root of most line-count and citation errors.

| Type | Line count | Body skeleton |
|---|---|---|
| First-touch | 15-20 lines | Greeting + buyer profile (1-2 lines: city/state, cash-or-financing, close-window) + vehicle ID + 5-line OTD breakdown ask + walk-away line + sign-off |
| Counter | ~10 lines (E3 hard cap) | Greeting + 3 numbered asks + 1 anchor sentence + 1 walk-away line + sign-off. NO buyer-profile recap (dealer already has it). |
| Follow-up / nudge | 4-6 lines | Greeting + reference to prior thread + 1 specific ask (e.g., "any update on the OTD?") + deadline + sign-off |

**Pre-draft mandatory Y/N checklist (5 items).** Run this BEFORE the first `create_draft` call in any session. If ANY item answers N, STOP and ask the buyer. Do not draft.

| # | Gate | What "Y" looks like |
|---|---|---|
| 1 | Trim + option package locked? | "Forester Limited with Option Package 25" — not "Limited or Touring" |
| 2 | Payment method locked? | "3% cashback Visa, $50k monthly cap" — not "cash or card" |
| 3 | Attachments planned? | "_FINAL_xhs-25500.jpg + _FINAL_cargurus-good-deal.jpg, manual paperclip" — not "some screenshots" |
| 4 | Anchor strategy + new-vs-used context locked? | "Cross-dealer anchor citing Rep A $X,XXX / Rep B $X,XXX; NEW MY thread, no used candidates referenced" — not "I'll cite something" |
| 5 | Walk-away deadline + dollar amount confirmed? | "$30,500 OTD walk-away, close by Wed May 22" — not "close this week" |

If any gate is N, the correct action is a single clarifying message back to the buyer, NOT a "best guess and iterate" draft. Iteration with `create_draft` only creates new drafts (no edit mode); 4 dealers × 3 rounds = 12 stale drafts the buyer must manually trash (see E4).

### Step 1: Prepare attachment files at FULL resolution (no MCP)

In the working directory:

```bash
mkdir -p .firecrawl/quote-images/
```

For each evidence image (XHS post screenshot, Reddit quote, dealer worksheet):

```python
from PIL import Image
img = Image.open('source.png')
if img.size[0] > 1300:
    h = int(img.size[1] * 1300 / img.size[0])
    img = img.resize((1300, h), Image.LANCZOS)
if img.mode == 'RGBA': img = img.convert('RGB')
img.save('_FINAL_<dealer>-<trim>-<datapoint>.jpg', 'JPEG', quality=88, optimize=True)
```

Target: 100-300KB JPGs at 1080-1300px width, fully legible. Use `_FINAL_` prefix so the user can find them at a glance.

### Step 2: Compose drafts via MCP with NO attachments field

```python
create_draft(
    to=[...],
    subject=...,
    body=...,  # plain ASCII, ~15 lines first-touch / ~10 lines counter
    # NO attachments key
)
```

In the body, reference attachments by name: "Screenshots attached." Do not include URLs or markdown link syntax.

If buyer asks to "insert" or "attach" images, push back ONCE:

> "Per E5: manual paperclip is the only way to send legible attachments. The MCP inline path forces ~16KB images that arrive blurry. I'll prepare the files at full resolution and you paperclip them in Gmail UI. Sound good?"

Default to manual. Only inline if buyer explicitly overrides.

### Step 3: Hand off to buyer with a per-draft attachment recipe

In the summary to buyer, output a table like:

| Dealer | Draft ID | Files to paperclip | Why |
|---|---|---|---|
| Dealer A | `r-xxxx` | `_FINAL_A.jpg`, `_FINAL_B.jpg` | NJ benchmark + ceiling reference |
| Dealer B | `r-yyyy` | `_FINAL_A.jpg`, `_FINAL_B.jpg` | Same; skip Dealer B's own ad |
| ... | ... | ... | ... |

Tell buyer: "Open each draft in Gmail web UI → paperclip → folder path → select listed files → leave as draft → I will tell you when to send."

### Step 4: Verify before send (buyer-side checks)

Buyer's pre-send checklist:
- ASCII body (no `**bold**`, no em-dashes)
- Attachments named clearly
- Subject line matches across all 4 emails in the cross-bid
- Walk-away deadline date is correct (especially after time has passed since drafting)
- Used-car / new-car threads not mixed

### Step 4.5: Mid-cycle pivot protocol (when a load-bearing field changes)

If the buyer changes a load-bearing field AFTER drafts have been created (trim, payment method, walk-away ceiling, anchor strategy, used-vs-new context, deadline), do NOT layer 4 new drafts on top of the 4 stale ones. Run this 4-step protocol:

1. **STOP drafting immediately.** No new `create_draft` calls until the protocol completes.
2. **Surface the stale drafts to the buyer with a bulk-delete Gmail search string** (per E4). Example: `in:drafts subject:"2024 Forester Limited" before:2026/05/18 -subject:"final batch"` selects the exact stale set. Tell the buyer: "These 4 drafts are now stale because trim/payment/X changed. Open Gmail web UI, paste this search, Select All, Move to Trash, then I'll create the new batch."
3. **Re-run Step 0** in full (gather + 5-item Y/N gate + email-type pick). The load-bearing change may cascade (e.g., trim change → anchor strategy needs re-lock; payment change → walk-away ceiling math shifts).
4. **Resume from Step 1** (full-res attachments may need regen if the screenshot set changed) → Step 2 (new drafts) → Step 3 → Step 4 → Step 5.

Never assume "the buyer will sort the stale drafts themselves." MCP Gmail cannot delete drafts. Without the bulk-delete search string, stale Premium drafts and new Limited drafts coexist in the Drafts folder and the buyer's risk of accidentally sending a stale one is real.

### Step 5: Send all 4 in a single 5-minute window

Cross-bids work because dealers feel parallel pressure. Sending them an hour apart loses leverage. Buyer hits Send on all 4 within 5 minutes.

**Send-window advisory (dealer-local time).** Recommend send between **9 AM and 5 PM Mon-Thu dealer-local time**. Reasoning:

| Window | Reply timing | Recommendation |
|---|---|---|
| Mon-Thu 9 AM - 12 PM | Same-day reply most likely; sales desk fresh | BEST |
| Mon-Thu 12 PM - 5 PM | Same-day or next-morning reply | GOOD |
| Mon-Thu 5 PM - 9 AM (overnight) | Lands at bottom of next-day inbox; rep replies in inbox-surface order | AVOID — lose first-mover edge on cross-bid |
| Friday after 12 PM | Lands in weekend autoresponder bucket; Mon reply | AVOID — 3-day reply lag |
| Sat - Sun | Read Monday morning behind weekend backlog | AVOID |
| 11 PM-7 AM dealer-local | Lands at bottom of inbox; rep treats as low-priority | AVOID |

If buyer asks to send outside the recommended window, push back ONCE with reasoning: *"Send at [time] will land at bottom of [day]'s inbox — sales rep works through inbox top-down, so we lose first-mover edge on the parallel cross-bid. Recommend hold until [next 9-10 AM dealer-local slot]."* Then comply if buyer overrides. The advisory is guidance, not a hard block — but the buyer should know the trade-off before sending.

Multi-state cross-bid: use the EARLIEST dealer-local 9 AM among the 4 dealers as the cohort send time (e.g., NJ + NY + CT + PA → all Eastern, 9 AM ET works; if MI dealer added, 9 AM ET = 8 AM CT — wait until 9 AM CT so the MI dealer also sees it in morning prime).

### Step 6: Cron monitoring kicks in

After send, the cron job (Phase 5) picks up replies. See `references/cron_monitoring.md`.

### Common deviations and corrections

| Deviation | Correction |
|---|---|
| Buyer says "just attach images for me" | Push back once (Step 2). Only inline if overridden. |
| Drafts created before trim is finalized | Stop. Re-ask Step 0. Don't iterate. |
| New car email cites used car offer | Discard draft, recompose without used anchor (gotcha D5). |
| Image looks tiny in draft preview | Confirm: was it inlined via MCP? If yes, regenerate at full res + manual attach. |
| 12+ stale drafts in Gmail Drafts folder | Give buyer one search string for bulk delete (gotcha E4). |

## Gotchas (Grouped by Topic)

Each gotcha is rooted in a real past incident. Use the topic groupings to find what's relevant. Where a workflow phase obviously triggers a gotcha, the gotcha is also referenced inline in the phase.

### E. Email & Drafting Hygiene

**E1. Plain ASCII required in every draft.** Dealers see literal `**bold**` and `—` characters that did not render. Strip markdown markers, em-dashes, en-dashes, backticks, and link syntax before saving any draft. See `references/email_format_rules.md`.

**E2. Empty `plaintextBody` on HTML-only emails hides inline OTD data.** Many dealer CRM platforms send HTML-only. Snippet truncates at ~200 chars, sometimes mid-sentence before the actual numbers. When `plaintextBody` is empty, alert the buyer that data may exist past the snippet boundary and ask them to verify in Gmail directly.

**E3. Keep dealer replies tight — ~10 content lines max.** Sales reps skim. Skeleton: 3 numbered asks + 1 anchor sentence + 1 walk-away line + sign-off. Cut without mercy: dealer knows their own car, can compute tax themselves, buyer profile only needs full restatement on first-touch. First-touch can be 15-20 lines; all subsequent counters compress to ~10.

**E4. MCP Gmail integration is read+create scope only — cannot edit, delete, or relabel anything.** `create_draft` makes a NEW draft on every call (no update mode). Both `label_message` and `label_thread` exist as tool surfaces but return "insufficient authentication scopes" when invoked, so even "add TRASH label" doesn't work. Iterating 3 rounds × 4 dealers creates 12 stale drafts that ONLY the user can manually trash via Gmail web UI. Protocol: ask 2-3 clarifying questions upfront (trim, payment method, attachments, what to include/exclude) BEFORE first draft. If iteration is unavoidable, give the user one Gmail search string that selects exactly the stale set for bulk delete (e.g., `in:drafts subject:Forester before:YYYY/MM/DD -subject:"final batch marker"`).

**E5. NEVER inline image attachments via MCP `create_draft` — the constraint chain forces 16-20KB tiny images that dealers can't read.** Why this is a hard rule, not a preference:
- MCP schema requires `attachments[].content` as inline base64 string.
- To pass base64 to MCP, must first Read it into context.
- Read tool has 25K-token output cap.
- Max base64 = ~25KB chars → max raw image ≈ 18-20KB.
- 18KB JPEG = ~360x400 px, dealer sees a blurry illegible square instead of a quote.
- Iterating to fit triggers 4-5 progressively smaller compressions, burning ~100K tokens on dead-end base64 reads.

**Correct workflow ALWAYS**:
1. Compose drafts via `create_draft` with NO `attachments` field.
2. Generate full-res JPGs (1080-1300px wide, quality 85-90, 100-300KB each) in `<workdir>/.firecrawl/quote-images/` with `_FINAL_` filename prefix.
3. List the exact files + per-dealer recommendation in a summary message.
4. User opens each draft in Gmail web UI → paperclip → selects files from local folder → saves → sends.

If the buyer asks to "insert images" or "attach screenshots", do NOT interpret as a request to inline via MCP. Push back once: "Per E5 the right play is high-res files + manual paperclip. The MCP inline path produces tiny unreadable images. Confirm you want manual attach (recommended) or the inline-tiny path." Default to manual unless explicitly overridden.

Per-dealer attachment etiquette:
- NEVER attach a dealer's own Internet Pricing screenshot back to them (shows you shop their own ad → kills negotiation).
- Safe to attach 3rd-party aggregator screenshots (CarGurus, Cars.com, Edmunds) to anyone.
- Safe to attach Competitor Dealer Y's quote to Dealer X (the "your competitor advertised this" play).
- Same attachment set across all 4 dealers in a parallel cross-bid is the simplest and works fine.

### I. Inbox & Cron Monitoring

**I1. Carfax submissions look successful but dealers often delay 12+ hours.** Schedule cron monitoring at 15-min intervals starting the morning AFTER submission, not within minutes.

**I2. Dealer email lands in Promotions AND occasionally Spam.** Search must be tab-agnostic or include `category:promotions`. Run a separate `in:spam` sweep at least once per buying-cycle day (eDealerHub / VinSolutions CRM platforms get spam-flagged often).

**I3. `newer_than:25m` sliding window misses backlog during pauses.** Overnight / meeting gaps make dealer mail permanently invisible to subsequent runs. Run one `newer_than:3d is:unread` full sweep per buying-cycle day.

**I4. Templated CRM emails are not always skippable.** A CRM email that embeds specific inventory data (stock, VIN, sales price, miles, color) IS actionable, even if the wrapper is boilerplate. Test: "does it contain vehicle-specific data?" not "does it look like a template?". Skip only pure marketing taglines.

**I5. Do not trash the dealer's original email or sent replies — it breaks future thread anchors.** When cleaning drafts, only delete items in `DRAFT` label state; never trash items with `INBOX` or `SENT` labels. Recovery if accidentally trashed: send a fresh email with `Re: <original subject> - <small qualifier>` so it threads in dealer's inbox.

### D. Dealer Behavior & Communication

**D1. "Best price upfront" dealers will not negotiate.** Recognize quickly (rental-return chains like Enterprise, no-haggle independents, some volume Subaru stores at MSRP) and pivot rather than waste cycles.

**D2. The 72-hour urgency claim is sometimes real, sometimes pressure.** Confirm by asking about the hold/deposit mechanism.

**D3. Local relationship dealers (Chinese, family, community) value direct over aggressive.** Do not deploy multi-round anchor tactics; one fair counter is enough.

**D4. Verify dealer hours and rep availability before scheduling.** A Wednesday test drive with a rep who is off Wednesday wastes everyone's time.

**D5. NEVER mention competing USED car offers when inquiring NEW car pricing (and vice versa).** Used and new desks have different incentive structures; mixing closes off negotiation ("if you have used at $32k, just buy that, we cannot match"). Keep negotiations completely separate.

**D6. When asking for multiple trim quotes, specify ONE "preferred" + ONE "alternative".** Lumping 4 trims yields generic "starting from $X" pitches. The 1+1 pattern yields two real labeled quotes.

**D7. Dealer-attached `proposal.pdf` hides actual OTD numbers from Claude.** Ask the user to open the PDF, OR ask the dealer to paste the OTD breakdown inline in the email body for "side-by-side comparison". Many dealers happily comply.

**D8. Dealer state-fee-template leak = full re-quote leverage, not single-line tweak.** When a dealer quote contains a fee that does not exist in the buyer's REGISTERING state, treat it as evidence that the entire OTD was generated from an out-of-state CRM template. Cross-check the rest of the line items against the registering state's "Does NOT have" list in `references/state_fees.md`. The correct response is to demand a full re-quote ("please re-issue the OTD using CT line items"), not just deletion of the leaking line. Other defaults in the same template — wrong reg fee structure, wrong tax rate tier, wrong title fee — are likely also wrong but harder to spot once the obvious leak is patched.
Example from the CT Outback case: dealer quote on a CT registration carried an NJ $7.50 tire fee (5 tires × $1.50 NJ rate). CT has no per-tire fee on retail dealer sales. The leak also coincided with an under-collected CT 2-year reg ($80 vs ~$120) — second template error caught only because the first one triggered full-quote review. Single-line deletion would have left the under-collected reg in place.

**D9. ADM kill list — demand removal in first counter, do NOT negotiate around it.** When a dealer quote contains any Additional Dealer Markup line on NEW MY inventory (see `references/outreach_strategy.md` § New-Car ADM Detection — full kill list: Market Adjustment, Hybrid Premium / Hybrid Adjustment / Toyota Premium, Dealer Markup / Dealer Adjustment, Allocation Fee / Allocation Premium / Protection Plus when bundled with MSRP-overage), the FIRST counter must demand removal as a precondition, not propose a counter-amount or middle-meet. ADM is dealer-side margin theater dressed as a fee; trying to "split the difference" implicitly accepts that ADM is a real line item. It is not.

Exact email language (paste-ready, paraphrase the line name to match the dealer's quote):

> *"Please remove the $X [exact ADM line name as it appears on the quote] line. Per current market on [Year Make Model Trim], MSRP is the ceiling, not the floor; [Edmunds/CarGurus] [region] shows the fair-price band at or under MSRP. If the ADM stays, OTD walks above my ceiling and this unit cannot win."*

Three rules:
1. **Do not couple ADM removal to any other concession** (captive financing, F&I add-ons, faster close). ADM is its own line; coupling lets the dealer trade a fake concession for a real one. The captive-vs-CU rebate question (`references/payment_methods.md` § Captive-vs-credit-union rebate playbook) is decided on its own merits AFTER ADM is killed.
2. **One ask, one round.** If dealer refuses ADM removal in the reply, mark dead and route to the next-best MSRP-clean candidate. Do not negotiate to a smaller ADM ($1,495 → $750); a $750 phantom line is still phantom. The Phase 3 ADM Tier-3 ranking already pre-positions Tier-1/2 MSRP-clean alternatives for exactly this pivot.
3. **Cross-state-net override stays the Phase 3 decision, not Phase 6 leverage.** If a DE/NH/OR ADM dealer's net OTD still beats a PA MSRP-clean offer (per `outreach_strategy.md` § Cross-state ADM nuance), that decision was already made at Tier-2 promotion in Phase 3. Phase 6 still demands removal first — the cross-state arbitrage is the back-up, not the opening ask.

Example from the RAV4 Hybrid PA case: a PA Toyota dealer opened at ~$40k OTD with $1,495 "Toyota Market Adjustment" baked in. ADM removal alone drops OTD to ~$39k (well inside the buyer's ceiling and binding cap). Counter-coupling ADM removal with captive-lender financing would have lost ~$1,000 in interest savings the captive rebate-rate offer was offering independently.

**D10. "Listing disappeared" / bait-and-switch protocol.** When a dealer claims the original VIN-X you asked about is "just sold" / "in the wash bay being prepped for another buyer" / "in transit and never made it to the lot" and pivots to VIN-Y at a higher price OR more miles OR with ADM, treat this as a bait-and-switch attempt by default. The original-listing-still-active rate after a "just sold" claim is empirically ~40-60% (the listing reappears 24-72h later at higher price), and the pivoted VIN-Y is almost never at the same OTD-per-config as the original VIN-X anchor.

Required defenses (all three, not pick-one):

1. **Proof-of-sale ask.** Reply in writing: *"Can you forward the sold-date confirmation (bill of sale screenshot, CRM `STATUS=Sold` timestamp, or the listing-removed date from your inventory system)? I want to make sure I'm not still racing the same VIN with the next dealer."* Refusal or vagueness = bait-and-switch confirmed. Compliance = legitimate. If listing reappears within 7 days on Carfax / Cars.com / dealer website, the dealer lied — walk and log permanently as a low-trust counterparty.

2. **Same-or-better OTD on the substitute, no upgrade markup.** If the dealer pivots to VIN-Y, the substitute must come in at the same or lower OTD as the original VIN-X benchmark, adjusted ONLY for legitimate config delta (trim, miles, color) using `references/negotiation_playbook.md` mileage and trim adjustments. The dealer cannot use the bait-and-switch as a free upgrade-markup opportunity. Reply: *"For the substitute to work, the OTD needs to land at or under $X (the locked OTD on the original VIN, adjusted for [Y miles delta x $0.10-0.15/mi] / [trim premium of $A] / [no other variables])."*

3. **Pause and re-anchor — treat the pivot as a NEW dealer engagement.** Do NOT let the dealer pivot mid-conversation to a different VIN as if it's the same negotiation. If the pivot is forced (buyer wants the substitute), restart the engagement: re-run Phase 3 single-VIN anchor analysis on the new VIN against `references/deal_data_sources.md` market data, re-pull cross-bid quotes from the other dealers for the same config, and re-anchor before sending any counter. A 5-line "OK what's the OTD on VIN-Y?" reply without re-anchoring concedes the entire negotiation.

Real-world pattern: dealer's original VIN-X listed at $26,500 (great deal, low miles, in-state, MSRP-clean). Buyer responds same day, dealer replies T+24h "just sold to another buyer this morning, but I have VIN-Y at $29,200 with 8k more miles, same trim, fresh on the lot." Without D10, buyer accepts the pivot and pays $2,700 over the anchor; with D10, buyer demands sold-confirmation (dealer cannot produce), waits 5 days, sees the original VIN-X relisted at $27,900 — confirms the pivot was theater, walks.

**D11. Dealer group ownership check — same parent = 1 anchor, not 2.** Before treating two dealer OTD quotes as "independent cross-bids", check the parent group. Many large auto groups own multiple dealers per region, and inter-group coordination on pricing is routine (the same regional GM sets the OTD floor for sibling stores). Two quotes from sibling stores are NOT real cross-bid leverage — they're a single anchor presented twice with inflated room for "competing" theater.

Check method (run BEFORE Phase 6 cross-bid disclosure, ideally at Phase 4 outreach time):

1. **Google "[dealer name] Auto Group ownership" or "[dealer name] parent company".** Public-corp dealer groups disclose ownership; mid-tier groups have it on About pages. DealerInspire partner directory + dealer.com partner listings also surface parent groups.
2. **Common parent groups to memorize (US, 2024-2026):**
   - **Penske Automotive Group** (NYSE: PAG) — ~150 US dealers across Honda, Toyota, BMW, Mercedes, Audi, VW, Porsche, Land Rover, Lexus, Acura. Sibling-store dense in CA, FL, NY, NJ, TX.
   - **Berkshire Hathaway Automotive (BHA)** — ~100 US dealers; concentrated in TX (former Van Tuyl), AZ, CO, GA, FL, IL, IN, MS, OK. Operates as "Berkshire Hathaway Automotive" but local stores often retain founder names (e.g., "Sewell" in TX).
   - **Asbury Automotive Group** (NYSE: ABG) — ~150 US dealers; concentrated in FL, GA, TX, NC, MO, IN, CO, NJ.
   - **AutoNation** (NYSE: AN) — ~315 US dealers; concentrated in FL, TX, CA, AZ, NV, CO, IL.
   - **Sonic Automotive** (NYSE: SAH) — ~110 US dealers; concentrated in CA, TX, NC, GA, FL.
   - **Lithia Motors / Driveway** (NYSE: LAD) — ~290+ US dealers; nationwide, fastest-growing roll-up 2020-2026.
   - **Group 1 Automotive** (NYSE: GPI) — ~150 US dealers; concentrated in TX, OK, FL, GA, LA, MA, NJ, NH, NY, MS.
   - **Hendrick Automotive Group** — ~140 US dealers (private); concentrated in NC, SC, VA, TN, GA, AL, FL, CA, KS, MO.
   - **Holman / Holman Automotive** — ~40 US dealers; concentrated in NJ, PA, FL.
   - **Ken Garff Automotive Group** — ~60+ US dealers; concentrated in UT, NV, CA, AZ, TX, IA, MI.

Treatment when sibling-store overlap found:

- **Collapse the duplicate.** Treat both quotes as a single anchor representing the parent group's floor. Use the lower of the two as your reference number.
- **Do NOT cite the sibling quote as a competitor.** Citing Penske-Honda-of-Old-Bridge against Penske-Honda-of-East-Brunswick to a Penske rep is comedy — they share an internal pricing dashboard. The dealer will laugh and price will not move.
- **Replace the duplicate with a true cross-group anchor.** Phase 4 outreach should target 3-4 different parent groups in radius, not 3-4 stores from the same group. If radius is sibling-store-saturated (common in FL, TX, CA metro areas with Penske / AutoNation / Asbury density), expand radius or accept fewer truly-independent anchors.

Real-world pattern: buyer in FL gets 4 quotes for a 2023 Camry XLE — <Dealer A>, <Dealer B>, <Dealer C>, <Dealer D>. First two are both AutoNation (same regional GM). Phase 6 buyer cites the Pinellas Park $32,400 OTD to Clearwater rep, expecting a $200-500 drop. Clearwater rep replies "that's our sister store, our system shows the same floor — best I can do is match $32,400." The two AutoNation quotes are 1 anchor, not 2. Real cross-bid leverage comes from <Dealer D> (independent) and <Dealer C> (an independent dealer group). With D11, buyer routes outreach correctly from the start.

### S. Data Sourcing & Sources

**S1. Pull real-time deal data BEFORE quoting any discount or OTD estimate.** Heuristics are reliably wrong by $1-3k in either direction. The 5-query Firecrawl pipeline takes ~5 minutes and corrects baselines that would otherwise misdirect the entire negotiation. See `references/deal_data_sources.md`.

**S2. For login-required sites (XHS / Facebook / Instagram), Playwright MCP local browser beats Firecrawl Live View URL.** Playwright pops a browser window on the user's screen — they log in via QR/SMS in 30 seconds. Subsequent navigation, snapshot, evaluate, screenshot all operate on that logged-in session. Cookies persist in user's local Chrome profile.

**S3. XHS `/explore/{id}` direct URLs 404 without an access token.** The same post works via `/search_result/{id}?xsec_token={token}&xsec_source=` where token comes from a fresh search-page anchor's `href`. Tokens may expire after ~24h. Always source XHS URLs from a current search-page `browser_evaluate`, never from memory or old links.

**S4. ~80% of XHS post images are NOT quote evidence.** Stock photos, delivery selfies, Apple Notes title cards, decorative emoji covers. Protocol: extract all img URLs via `browser_evaluate`, download all candidates, Read each one, `rm` the non-evidence files immediately. Useful keepers: dealer worksheets, sales-rep email/SMS screenshots, Costco quote sheets.

**S5. For regional anchor evidence, XHS search MUST include the state/region keyword.** Generic `forester 报价` returns posts from CA/TX/MI/PA/WV — wrong regional market. Adding `NJ` / `新泽西` / `纽约` exposes posts from the buyer's tri-state area with same-dealer same-trim quotes. Run two parallel searches when buyer's state is known: generic for national anchor + state-specific for regional anchor.

### N. Negotiation Mechanics

**N1. Use OTD anchors transparently across multiple dealers.** Once 2+ written OTDs exist, cite them by dollar amount in counters: "My locked benchmarks are X at $X,XXX and Y at $X,XXX — for your unit to switch me, OTD needs to land near those." Converts each competitor offer into a market data point. Pulls subsequent offers down reliably.

**N2. Parallel "drop $X" asks elicit counter-offers within 1-3 hours when framed correctly.** Formula: "Your X at $A vs locked alternative at $B with [advantage]. For your unit to win, OTD needs to land near $TARGET. If math does not pencil, I will go with the locked alternative by [deadline]." In practice, 3 dealers in one metro each dropped OTD within 1-3h (Rep A -$X,XXX, Rep B -$X,XXX, Rep C -$X,XXX). Run dealers in parallel, never sequentially.

### V. Vehicle Verification

**V1. CARFAX 1-owner is necessary but not sufficient.** Service records reveal whether the 1 owner actually maintained the car. Missing CVT fluid service at 60k is a $300-400 inherited cost.

**V2. Require dealer-provided full CARFAX PDF or live URL before accepting OTD or scheduling PPI.** Verbal "clean carfax, 1-owner" has a real failure rate. Real incident: <Dealer C> claim in writing turned out to hide a an earlier date minor damage event with front + left + right impact zones. Buyer revised target down by $1.5-2k AND requested body-shop docs + EyeSight recalibration + structural report. Never accept OTD on verbal CARFAX summary.

### P. PPI & Test Drive

**P1. With 2-4 final candidates, book mobile PPI in parallel and cancel after dealer choice finalized.** Mobile services (Lemon Protector $139+ in NY/NJ/CT, YourMechanic, Pep Boys Mobile) eliminate dealer-side transport coordination. Stagger times (9 AM / 10 / 11 / 12 PM) to avoid form conflicts. Each NOTES field: "BOOKING X OF N - TENTATIVE, finalizing by [time]". Inspector phone gets dealer phone + VIN + address per slot.

**P2. Online PPI booking forms have predictable quirks.** Year dropdowns cap at current/-1 year (newer vehicles need NOTES annotation). DATE inputs are `<input type="date">` requiring ISO YYYY-MM-DD. State defaults to service's HQ state. Phone TYPE defaults to "Cell" but dealer phone should be "Work". Always re-snapshot after `fill_form` before Submit.

**P3. Close-day F&I (Finance & Insurance) hard-no script.** After OTD is locked in writing and the agreement is signed, the F&I office is the highest-frequency point of last-minute margin recovery: GAP coverage ($795-$1,295), VSC / extended service contracts ($1,495-$3,000), tire-and-wheel protection ($399-$799), paint / fabric protection ($499-$1,299), key replacement ($299-$499), nitrogen tires ($199), dent / ding ($499). Each is presented as "small monthly add" ($25/mo) hiding the lump-sum capitalization. F&I officers are paid on attach rate; expect 3-5 distinct pitches in a 30-45 minute close, often with paperwork shuffled so add-ons appear pre-initialed.

Paste-ready hard-no script (read verbatim if pressured, or hand over the printed copy):

```
Per my signed agreement dated [DATE] with [GM/Sales Manager name],
the OTD is locked at $[X]. I decline GAP, VSC, tire-and-wheel,
paint protection, key replacement, nitrogen, dent / ding, and any
other add-on not in the original agreement. Please process the
close at the agreed OTD, or I will exit and we will both lose
time. Repeat: NO add-ons. I will sign only the original
agreement.
```

Operational rules:

1. **Do NOT initial any new line item without a 5-minute pause to re-read.** F&I officers shuffle paperwork; a "just initial here for the title work" is sometimes a GAP authorization slipped into the stack. If anything is newly initialed-for, pause, take the page out of the folder, read every line, and verify it matches the agreement. The pause itself is a tactic — it slows the close and signals the buyer is not in a hurry.
2. **Mandatory add-on response.** If F&I claims an add-on is "required by the dealership" (it is not, with the rare exception of state-mandated docs), reply: *"Please show me the line item in my signed agreement that authorizes this charge. If it's not there, remove it; if you cannot remove it, I will exit and the deal is dead. Per my OTD lock at $[X], adding anything constitutes a new deal that I have not agreed to."*
3. **Monthly-payment-shift trick.** F&I will sometimes say "we can add GAP and your monthly only goes up $18". Reply: *"My agreement is OTD-locked, not monthly-locked. Adding $18/mo for 72 months is $1,296. I decline."* The monthly-shift framing exploits financing-buyer focus on monthly cap; D9-style ADM-vs-financing decoupling applies here too.
4. **Recourse if F&I refuses to honor the locked OTD.** Walk to the sales floor and ask for the GM by name (the one on the signed agreement). The GM signed off; the F&I officer is breaking the agreement. If the GM also refuses, the deal is dead. State law in most jurisdictions allows buyer to recover the deposit if the dealer materially changes the terms.
5. **Pre-close communication.** At Phase 6 close-day kickoff (before driving to dealer), re-confirm with the GM in writing: *"Confirming the OTD at $[X] per our agreement dated [DATE]. I will decline any F&I add-ons at close per my no-add-ons posture from Day 1. Please brief your F&I officer so we don't burn time on add-on pitches."* This pre-empts ~70% of close-day F&I friction by routing the no-add-ons signal to F&I before the buyer walks in.

Cross-references: `assets/dealer_reply_template.md` § "Add-On Refusal" + the new F&I close-day hard-no template; `references/negotiation_playbook.md` § "Add-On Refusal" pricing detail. See also gotcha D9 for the structurally identical ADM-removal protocol — F&I add-ons are ADM in a different uniform.

### H. Session & State Hygiene

**H1. A previous Claude Code session may have invented fictitious dealer dialogue.** Always cross-check any "tracker log" entry against actual Gmail thread before acting. Counter-offers built on hallucinated context are how deals fall apart.

**H2. Cleaning drafts: only delete `DRAFT`-label items.** See I5 — accidentally trashing INBOX/SENT items breaks future reply threading.

## Language and Audience Separation

The skill operates in two language registers simultaneously. Drift between them causes either confusion (buyer sees an internal jargon dump) or unprofessionalism (dealer sees Chinese characters in a counter-offer email). Hold the separation strictly.

| Surface | Language | ASCII required | Notes |
|---|---|---|---|
| Internal reasoning + agent-to-buyer dialogue (chat window) | Buyer's preferred language (English / Chinese / Spanish / etc.) | No | Render math, gotcha names, anchor citations in whatever language the buyer is using. The bilingual triggers in this skill's description ("buy me a car" / "帮我找车") signal acceptable buyer-side languages. |
| Buyer-facing artifacts: `criteria.md`, dossier (`*.md`, `*.html`, `*.pdf`), tracker, negotiation prep | Buyer's preferred language | No (HTML/PDF can carry Unicode CJK glyphs; see `dossier_template_cn.html` for the CN variant) | The CN dossier template exists for this reason. Confirm the language with the buyer at Phase 1 close; default to English if not stated. |
| Dealer-facing emails (every Gmail draft, every counter, every walk-away, every follow-up) | **ALWAYS English** | **ALWAYS ASCII** (Rule #1) | Plain English only. No Chinese, Spanish, or other non-English content under any circumstance. No emojis. No markdown. See `references/email_format_rules.md` and `assets/dealer_reply_template.md` § Voice Specification. Dealer reps in US markets read English; CRM systems may strip or mangle non-ASCII Unicode silently. |
| Skill metadata (gotchas, references, SKILL.md, phase files) | English (source of truth) | N/A (markdown source, not transmitted to dealer) | All gotcha IDs, rule numbers, section names, and code-like identifiers are English. Translations of these into other languages happen at the agent-to-buyer surface only, never in the source files. |

**Verification at draft time.** Before saving any Gmail draft via `create_draft`, scan the body for non-ASCII characters and any non-English content. If the buyer's preferred language is Chinese and an internal note about the dealer email leaked into the draft body, strip it. The draft is the dealer-facing surface; English-only, ASCII-only, no exceptions.

**Mixed-language criteria.md handling.** If the buyer prefers Chinese, `criteria.md` may be rendered in Chinese for the buyer's review. When Phase 4 outreach drafts pull values from `criteria.md` (buyer name, city, state, walk-away ceiling), translate any Chinese fields to English at draft-creation time. The values are buyer profile data, not buyer voice — they go into the dealer email in English regardless of which language `criteria.md` was authored in. See `assets/criteria_template.md` (default English) and the buyer-facing surface rule above.

## Post-Cycle Feedback

After every completed (or aborted) cycle, fill `assets/feedback_log.md` to capture what failed, what surprised the buyer, and what skill-specific gap surfaced. This is the structured input to the next skill iteration.

The log is append-only — older cycles stay for trend analysis. If the same gap appears in 3+ cycles, it becomes a Tier-1 fix in the next iteration wave.

Concrete = actionable. "P1 was OK" produces no skill change. "P1 (h) trade-without-numbers fired correctly on explicit 'I want to trade' but did NOT fire on 'I have an old Civic'" is a specific Phase 1 trigger-phrase expansion that the next iteration can implement.

Trigger this step:
- At cycle close (after PPI passes, after deposit, after cashier's check, OR after walk-away)
- At cycle abort (after Mid-Cycle Pivot Protocol fires AND buyer changes target so significantly that the cycle does not resume)
- After every Gotcha violation (D5, D8, D9, D10, D11, P3, etc.) — log even if the cycle continues; gotcha violations are the highest-leverage learning surface

The fill takes 10-15 minutes. Skipping it means the next iteration has nothing concrete to act on.

## Quick Start

To begin a new car search:

1. Read this SKILL.md (already loaded if skill triggered).
2. Phase 1: gather requirements from user, save to `criteria.md`.
3. Phase 2: pull baseline market data (`references/deal_data_sources.md` pipeline).
4. Create working directory `C:\Users\<user>\car_buying_<year>\` and copy `assets/tracker_template.md` → `dealer_outreach_tracker.md`.
5. Phase 3: dispatch parallel research subagents.
6. Phase 4-5: outreach + cron monitoring.
7. Phase 6 onward: reply drafting, PDF review, dossier, close.
