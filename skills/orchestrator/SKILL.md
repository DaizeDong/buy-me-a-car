---
name: buy-me-a-car
description: Use when the user wants help researching, contacting dealers about, negotiating, or finalizing a car purchase (used or new). Triggers include "buy me a car", "find me a car", "research cars", "email dealers", "compare quotes", "negotiate OTD", "buy a Subaru/Toyota/Honda/Mazda", Chinese phrases "帮我找车", "买车", "选车", "砍价", "对比经销商", and Spanish phrases "ayudame a comprar un carro", "ayudame a comprar un coche", "encuentrame un auto", "negociar el precio del carro", "comparar concesionarios". Runs end-to-end: multi-site inventory search, mass dealer outreach, Gmail reply monitoring on a cron, OTD negotiation with market-data anchors, CARFAX/service-record PDF analysis, and decision dossiers for test drives.
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

- Purchase is already closed (paperwork signed), direct user to a delivery checklist instead
- Pure mechanical-repair, EV-charging, lease-return, or insurance questions
- "Just tell me what car to buy" with no constraints, go back to Phase 1 and gather requirements first
- Quick price-check that does NOT require dealer outreach, answer directly with `references/deal_data_sources.md` Firecrawl pipeline only

## Critical Rules (Non-Negotiable)

Violations of these have caused real-world deal damage. Apply automatically.

1. **Plain ASCII in every outbound email.** No `**bold**`, no em-dash `—`, no markdown links, no backticks. Strip before saving any Gmail draft. See `references/email_format_rules.md`.
2. **Data before estimates.** Pull `references/deal_data_sources.md` Firecrawl pipeline BEFORE quoting any OTD, discount, or "is $X reasonable" answer. Heuristics are wrong by $1-3k.
3. **Written OTD before any in-person visit.** If a dealer refuses to send the full breakdown by email, decline the visit and pivot.
4. **Read the actual CARFAX PDF/URL yourself.** Verbal "clean 1-owner" claims have a real failure rate. See gotcha V2.
5. **Never mix used-car and new-car anchors in the same dealer email.** Used and new desks have different incentive structures; mixing kills negotiation. See gotcha D5.
6. **Verify tracker history against Gmail before acting on it.** Past sessions may have invented dealer dialogue. See gotcha H1.
7. **Phase 4 emails may only cite REAL-tagged baseline rows.** Synthesized / placeholder rows are for internal reasoning only. Never paste a synthesized Reddit anecdote, fabricated dealer number, or generic "buyers report X" into a dealer email, it converts internal-reasoning data into a fabricated citation, which is unrecoverable if challenged.

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
| **Walk-away ceiling** (single number, hard stop) | "$30,500 OTD, above this I walk no matter what; distinct from the range upper bound" |

**Payment method is load-bearing.** A $32k cash OTD becomes $32,960 with a 3% CC surcharge. Without explicit payment detail, OTD targets are not actionable. See `references/payment_methods.md` for the decision matrix (cashier's check, debit, CC tiers, lease cash conversion).

**OTD vs sales-price clarifier (mandatory).** If the buyer's budget answer does NOT contain "OTD" / "out-the-door" / "all-in", you MUST ask back: *"Is that out-the-door (all in: price + tax + doc + reg + DMV) or sales-price only?"* before saving `criteria.md`. A $28k sales-price target and a $28k OTD target are ~$2-3k apart and drive different dealer asks.

**Walk-away ceiling note.** This number is what Phase 6 enforces as the absolute stop. Do not negotiate above it for any reason.

**Buyer-type router (mandatory).** Before saving `criteria.md`, ask three Y/N gates. Each YES unlocks a sub-question block layered ON TOP of the 9-field core table. The 9-field core covers the cash-buyer + used-car + single-state default; the router branches handle the common non-default axes.

| Gate | If YES, ask the sub-question set from |
|---|---|
| **Financing?** (auto loan, lease, or captive, anything other than full cash / cashier's check / debit) | `references/payment_methods.md` § **"Financing buyer sub-questions"**, 9 fields: lender + product, APR (locked vs quoted), term in months, max financed cap, cash down on hand, max monthly payment willing to carry, pre-approval expiry date, captive-financing openness (TFS / SMF / HFS) if rebate-tied, pre-approval document on hand (hard-pull-locked vs soft-pull-quoted) |
| **Trade-in present?** | Full reference: `references/trade_in.md` (12-field P1 capture set). Ask the structured 12 fields: year/make/model/trim, mileage, title status (clean/branded/salvage), **lien holder + current payoff balance + per-diem interest + payoff letter validity**, key count, cosmetic issues, mechanical issues, KBB Instant Cash Offer (screenshot), KBB Trade-In Value, KBB Private Party Value, estimated Manheim wholesale floor, state trade-in tax credit posture. If buyer has an active lien, ALSO ask: **"Title in hand or held by lien-holder?"** (most states lien-holder holds; NY/MN/PA/MD/KY are exceptions). Routes to `trade_in.md` § 4a-4d lien payoff workflow. |
| **EV?** (battery-electric or PHEV) | EV sub-questions: charging at home (Y/N + L1/L2)? range minimum (mi)? state/local EV rebate (federal §30D/§25E/§45W credits TERMINATED for vehicles acquired after 2025-09-30 per OBBBA, do NOT promise a federal $7,500/$4,000 credit on a current purchase; only state rebates remain)? (Full reference covered in `references/ev_buyer_playbook.md` and `skills/ev-buyer-helper/SKILL.md`; for Phase 1 capture, ask the fields inline and record on `criteria.md`.) |

If a gate fires YES, append the sub-question answers as a dedicated section in `criteria.md` BELOW the core 9-field table, NOT as additional rows in the core table. Keep the core table stable across buyer types.

**Seller-type gate (mandatory, ask in Phase 1 before Phase 3 dispatch).** The three gates above ask the BUYER side (cash / financing / trade-in / EV / pickup). This gate asks the SELLER side, because a private seller removes the entire OTD/F&I/outreach apparatus. Ask: *"Is the seller a dealer, or a private individual (for-sale-by-owner)?"*

- **Dealer** -> existing 9-phase dealer pipeline unchanged.
- **Private individual (FSBO)** -> **PRIVATE-PARTY PATH** (the 6th buyer path). Load `references/private_party_playbook.md` and apply these overrides for the rest of the run:
  - **No OTD stack, no F&I.** Cost model = `sale_price + state_tax + title_fee + reg/plates`. There is no doc fee and no dealer fee; suppress those lines in otd-calculator. Buyer remits tax + title + reg **at the DMV**, not to the seller.
  - **Tax basis is state-variable - verify before quoting.** Three archetypes: purchase-price (CA, NJ, most states; book-value backstop if declared price looks low), book/fair-market default (buyer must prove a lower real price), and **fixed age/value table (Illinois RUT-50: ignores price for most cars)**. If the state isn't pinned in `state_fees.md`, web-verify the basis.
  - **Risk moves to title / tax / payment / seller legitimacy** - run the curbstoner + payment-fraud checks (playbook sec 4-6) in place of dealer inbox CRM/spam triage.
  - **PPI priority up** (no return window). Seller refusing an independent PPI is a red flag.

Mixed runs (some dealer listings, some FSBO) are allowed: tag each candidate `seller=dealer|private` in Phase 3 and route per-candidate. The private-party Phase-4 / Phase-6 branch overrides are documented in `references/phases.md` (Phase 4 = single-seller contact, skip mass outreach; Phase 6 = single-seller negotiation on private-party comps + safe-close mechanics).

**Financing buyer routine, auto-derive the binding constraint.** If the financing gate fires YES AND the answers fill in (max monthly, term, APR, cash down), automatically compute the binding-constraint OTD using:

```
financed_cap_from_monthly = monthly × (1 - (1 + APR/12)^-n) / (APR/12)
effective_OTD_cap        = cash_down + financed_cap_from_monthly
```

Compare `effective_OTD_cap` against the stated walk-away ceiling. If the math lands within $500 of the walk-away, surface in the heads-up block: *"Your monthly cap is the real binding constraint, not your OTD ceiling, real negotiation room is $X, not the apparent $Y."* See worked example in `references/payment_methods.md` § "Financing buyer sub-questions". This routine is **financing-only**, leases use the residual + money-factor math in the Lease Conversion section, not this formula.

**Cross-state surfacing (MANDATORY when radius spans 2+ states).** Add the buyer-facing note to the heads-up block: tax and registration follow the **registering** state, not the dealer state, and out-of-state dealers must collect the registering state's tax. Doc-fee caps vary by dealer state, so **force-correct every quote against `references/state_fees.md`**, which also holds the note's wording, the low-doc / no-tax arbitrage hint, and the cross-state titling table.

**DC / VA / MD commuter-corridor sub-case (MANDATORY when ZIP is in the DC metro).** Daytime and nighttime addresses routinely straddle three states here, and dealer CRMs default to their own state's tax, which is a state-template leak (gotcha D8). The registering state still governs. **Confirm the registering state at P1 close-day logistics** (it is the DMV that issued the buyer's license in almost every case) and demand a re-quote on any leak. Per-state rates, the four corridor edge cases and the DC excise structure: `references/state_fees.md`.

Save to `criteria.md` in the working directory. Then, BEFORE asking the buyer to confirm, surface a **"Heads-up before you confirm"** block, at most 3 items surfaced to the buyer, but the agent MUST evaluate all 14 checks below internally and pick the top-3 by priority rule.

| Check | Surface when |
|---|---|
| (a) Factual misconception in stated rationale | The buyer's "why" contains a claim that's wrong or partial (e.g., "I want Limited because EyeSight is only on Limited", wrong, EyeSight is standard on all 2020+ Outback trims). State the correction in one line. |
| (b) Filter that eats >70% of supply | Any single filter (year + miles + trim + color + radius) likely culls supply below ~30% of regional listings. Either run a Carfax-style supply check or flag explicitly: *"This filter combination may leave <N candidates in your radius, consider widening X."* |
| (c) Timeline violates dependency-chain minimums | **Hard threshold: buyer's close target < 5 days from first outreach.** Dependency chain: dealer reply lag (gotcha I1, 12+ hr typical, occasionally 24-48 hr) + cross-bid round 2 negotiation (24-48 hr) + PPI scheduling (gotcha P1, mobile PPI parallel booking needs same-day-plus slots, often T+2) + insurance binder + bank cashier's-check issuance (same-day after 9-10 AM cutoff). Minimum realistic = 5-7 days; 3-day rush forces verbal-only OTD (violates Critical Rule #3) or skipping PPI. Flag as *"Your stated close date is [X] days from first outreach, dependency chain (dealer reply 12-48 hr + cross-bid round 2 + PPI + binder + cashier's check) needs 5-7 days minimum. Either extend close by [N] days or accept skipping PPI / written-OTD verification (NOT recommended)."* |
| (d) Budget-vs-aspirations mismatch | Stated OTD ceiling is materially below the dream-vehicle's typical OTD (e.g., $30k OTD target but desired vehicle is $48k MSRP volume trim). Flag as: *"Your $30k OTD ceiling and your stated target [Year Make Model Trim] don't overlap, typical OTD on this config in your radius is $52-55k. Either widen budget to $50k+ OTD, drop to a lower trim / older MY (typical $30k OTD config: [example]), or pivot to a different model."* |
| (e) Timeline-vs-financing mismatch | Buyer needs financing pre-approval (financing gate fired) but timeline is <5 days, AND pre-approval not yet in hand. Pre-approval pulls: CU = 1-3 business days (typical credit unions), bank = same-day to 2 days, captive = same-day at dealer (locks rate to dealer ecosystem). Flag as: *"Your timeline is [X] days but pre-approval not yet pulled. CU pre-approval takes 1-3 business days; without it, you arrive at the dealer with only captive financing as an option (which means no rate competition). Either pull CU pre-approval today (Phase 1) or extend close by [N] days, or accept captive-only financing."* |
| (f) Stale anchor citation | Buyer cites a benchmark deal that's >6 months old (e.g., "my friend got a 2023 RAV4 XLE for $32k in March 2024", 14 months old at time of P1). Manufacturer incentives shift quarterly; 6-month-old anchors are unreliable. Flag: *"Your anchor [$X on Y] is [N] months old. Incentive stack and market have shifted since then; I'll pull current Phase 2 baseline at [today's date], expect [+/- $X] vs your anchor. Don't lock to the old number until we see today's data."* |
| (g) Cash buyer pushed to finance | Buyer is paying cash (cash = financing gate NO) but somewhere in their stated rationale they mention "the dealer said I should finance for the rebate" or similar dealer-to-buyer push. Flag: *"Be aware, dealer-financing-tied rebates are sometimes real (see `payment_methods.md` cash-to-lease conversion + captive-vs-CU rebate playbook), but they only win when (a) the captive offers a rebate-tied incentive that exceeds the interest cost, AND (b) early payoff has no prepayment penalty. Don't accept 'finance for the rebate' without running the math; in 50%+ of cases dealer claims the rebate is finance-tied when it isn't."* |
| (h) Trade mentioned without numbers | Buyer mentions a trade-in vehicle but has not provided payoff balance, title status (clean / branded / salvage), lien holder, or KBB Instant Cash Offer screenshot. Flag: *"You mentioned trading in your [vehicle]. Before I can build any OTD math I need: current odometer, title status (clean / branded / salvage), lien holder + payoff balance + per-diem interest if applicable, KBB Instant Cash Offer screenshot, KBB Trade-In Value, KBB Private Party Value. Without these the trade is a placeholder, not a number. See `trade_in.md` for the 12-field set."* |
| (i) High-mileage trade trap | Buyer's trade has >100k mi OR known mechanical issues OR known accident history (per `trade_in.md` fields). KBB Instant Cash Offer often DECLINES at >120k mi or with declared mechanical issues; CarMax / Carvana / dealer wholesale may be substantially lower than KBB trade-in value. Flag: *"Your trade at [N]k mi / [condition] is at high risk of KBB Instant Cash Offer declining and dealer-wholesale being $X below KBB trade-in. Set trade expectation at 70-80% of KBB Trade-In Value (not 100%) and budget for the gap. Consider Private Party sale at $[Y] before dealer trade-in."* |
| (j) EV / Hybrid with no charging plan | EV gate fires YES but buyer reports no home L1 outlet OR no home L2 install path OR no charging address at all (e.g., apartment renter without dedicated parking). Flag: *"You're targeting an EV but charging access is unclear. Without home L1 minimum (10-15 hrs/charge for daily commute), you depend on public DCFC, which runs 3-5x the cost per kWh of home charging ($0.40-$0.60/kWh public vs $0.10-$0.15/kWh home) and adds 30-45 min per session to your routine. If apartment rental, confirm building's L2 install policy OR check public L2 availability within walking distance. May make a hybrid or PHEV (charges on L1) a structurally better fit. See `ev_buyer_playbook.md` § Charging Access."* |
| (k) Cross-state purchase with title-jumping risk | Buyer is purchasing in a no-tax / low-tax state (DE / NH / MT / OR) to register in a tax state (NJ / NY / CA), thinking they'll capture the tax savings. **They will not.** The registering state collects use tax at DMV titling, buyer pays full registering-state rate regardless of where they bought. Flag: *"Buying in [no-tax state] to register in [tax state] does NOT save sales tax. Your registering state ([tax state]) collects [X]% use tax at DMV when you title. The legitimate cross-state advantages are (a) doc fee differentials, (b) inventory access, (c) dealer competition, sales tax avoidance is not one of them. Title-jumping (registering in a no-tax state without actually living there) is fraud and can result in back-taxes + penalties + criminal charges. See `state_fees.md` cross-state titling section."* |
| (l) Rebuilt / salvage / branded title | Buyer's target listing has a rebuilt / salvage / branded title OR buyer's trade does. Buyer often doesn't realize the downstream impact. Flag: *"This vehicle has a [rebuilt / salvage / branded] title. Insurance implications: most carriers only write liability (not comprehensive / collision); a few (State Farm, Geico in some states) refuse coverage. Financing implications: most banks / CUs decline; only specialized lenders (CarFinance, Credit Acceptance) at sub-prime rates. Resale implications: 30-50% discount to clean-title comparable at resale; many dealers won't take in trade. Verify acceptability with your insurer and bank BEFORE confirming."* |
| (m) Fake CPO label | Buyer is targeting a used vehicle the dealer markets as "Certified" but the dealer is NOT the brand's authorized dealer OR no factory CPO certificate is provided. Flag: *"The dealer's 'Certified' label may be dealer-internal marketing, NOT manufacturer CPO. Verify: (a) is the inspecting dealer an authorized [Brand] dealer? (b) request the CPO certificate with manufacturer letterhead. (c) confirm warranty is registered in [Brand]'s CRM under your name. Independent shops' 'Certified' inspections do not carry factory-backed extended warranty, do not include the 150-200-point factory checklist, and do not offer manufacturer roadside / loaner programs. See `subaru_cpo_program.md` / `honda_cpo_program.md` / `toyota_cpo_program.md` for what real factory CPO includes; `vertical_playbooks.md#part-2-heavy--commercial--luxury` § 3.6 for luxury-specific fake-CPO traps."* |
| (n) Filter combination = zero supply | More aggressive than (b), when the AGGREGATE combination of filters (year + miles + trim + color + interior + radius + payment) likely yields zero candidates. Run a quick supply check on Cars.com / Carfax / AutoTrader before confirming. Flag: *"Your filter combination ([trim X] + [color Y] + [miles <Z] + [radius W mi] + [MY range]) is likely sub-1 listing across your radius. Either widen one filter aggressively (color most-common-relaxed: 4x supply; radius: 2x supply per 50 mi expansion) OR confirm okay to wait for an inbound matching VIN at 4-12 weeks."* |

**Priority rule when >3 fire**: surface the top 3 by impact, in this descending order:

1. (d) Budget-vs-aspirations mismatch, highest impact, often invalidates entire downstream workflow
2. (n) Filter combination = zero supply, wastes Phase 3 dispatch if not flagged
3. (k) Cross-state purchase with title-jumping risk, legal exposure
4. (l) Rebuilt / salvage / branded title, legal / insurance / financing exposure
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

Cap at 3 items surfaced. If none apply, say so explicitly ("No heads-up items, filters and timeline look feasible.") and proceed. Then ask for confirmation.

**Close-day logistics, capture once at P1, re-confirm at P9.** Phase 9 close-day execution depends on 6 logistics inputs that re-asking at the last minute often delays close by 24-48 hours. Capture them at Phase 1 sign-off, store in `criteria.md`, and re-confirm verbatim at P9 close-day kickoff. The mini-table below is shared across all buyer-type branches (cash / financing / trade / EV / pickup).

| Field | Example | Why captured at P1 |
|---|---|---|
| **Bank cut-off + branch + hours** | "Chase, local branch, cashier's checks issued M-F 9 AM-5 PM, same-day issuance before 3 PM" | Cashier's check is the gating P9 instrument for cash buyers; bank hours and same-day-issuance window drive close-day morning sequencing. |
| **Insurance carrier (for binder)** | "GEICO policy #12345, agent direct line (xxx) xxx-xxxx; new-vehicle binder needs VIN + closing date, 1-hour turnaround during business hours" | Dealer will not release the vehicle without an active binder; cold-call to a generic carrier on close-day adds 1-3 hours. |
| **Plate decision** | "Transfer existing plate $26 (preferred) vs new plate $151" or "New plate" | Plate transfer math depends on registering state (`state_fees.md`) and saves $25-150 in most states; the decision drives DMV paperwork at close. |
| **Available time windows on close day** | "Wed Apr 24, between 10 AM and 3 PM; hard stop at 3:30 PM for school pickup" | Time-boxes the close; sets when the cashier's check must be ready and which time-window slot to lock with the dealer. |
| **ID set** | "Driver's license (current), Social Security card OR passport, recent utility bill for proof of residence, marriage certificate if name-change since DL issued" | Captives + state DMV both require multiple ID forms; missing items force a re-trip. |
| **Captive vs CU vs cash funding instrument** (if not pure cash) | "Credit-union pre-approval letter (in hand), $X cap, expires May 1; cashier's check issued from the credit union to dealer in dealer name" | Funding instrument determines whether dealer F&I needs to wait on a wire (24-72 hr captive) vs accepts an instant cashier's check (same-day). |

Add this mini-table as a section in `criteria.md` BELOW the Heads-up block. **Phase 9 re-reads and re-confirms it with the buyer before they drive anywhere**, because a change since Phase 1 cascades into close-day execution. Procedure: `references/phases.md` Phase 9.

**Inline jargon glossing rule.** When `criteria.md`, outbound dealer email, or any buyer-facing artifact emits one of the following terms for the FIRST time in that artifact, include a brief parenthetical gloss. Subsequent uses can drop the gloss.

| Term | Gloss (EN) |
|---|---|
| **OTD** | out-the-door (all-in: sale price + tax + doc + title + reg + add-ons) |
| **NA** | Not Applicable (or, in context, North America) |
| **F&I** | Finance & Insurance (the dealer office where add-ons, extended warranties, and financing paperwork are signed) |
| **anchor** | a market data point cited to set the negotiating range (e.g., "Edmunds TMV anchor at $28,500") |
| **walk-away** | the absolute-stop price above which the buyer will not buy; distinct from the budget range upper bound |
| **cross-bid** | a parallel outreach to 3-4 dealers asking for OTDs on the same VIN class so each offer is leverage against the others |
| **ADM** | Additional Dealer Markup (a line item above MSRP, Market Adjustment, Hybrid Premium, Allocation Fee; see gotcha D9) |
| **CPO** | Certified Pre-Owned (a manufacturer-program-certified used vehicle with extended powertrain + B2B warranty, see Subaru/Honda/Toyota CPO refs) |
| **NACS** | North American Charging Standard (Tesla's connector, becoming the EV charging standard 2025-26; replaces CCS1 on Ford/GM/Hyundai/Kia/Rivian/VW/Volvo OEMs) |

**Spanish buyers:** the ES column, the ES-only finance terms, the carro/coche regional note and the ES style rules live in [`references/glossary_es.md`](references/glossary_es.md) (translations are drafts, native sign-off pending). Load it when producing any Spanish buyer-facing surface.




The rule is **first-use only**, not every use. Glossing a term twice in one email is more confusing than glossing it zero times. Goal: make buyer-facing artifacts comprehensible without forcing the buyer to look up acronyms mid-decision. Per § Language and Audience Separation, the ES gloss is a **buyer-facing chat / `criteria.md`** surface only, it never enters a Gmail draft, counter, or signed line item (those stay English + ASCII, Rule #1).

### Phase 2: Baseline Market Data

BEFORE Phase 3 outreach, run the 5-query Firecrawl pipeline to produce `.firecrawl/{model}-deal-baseline.md`:

1. National baseline (CarEdge + Edmunds)
2. State-specific dealer Internet Pricing (top 5 dealers in radius)
3. Recent buyer reports (Reddit / XHS via browser session)
4. Current month manufacturer incentive stack
5. State-specific buyer evidence: **XHS with state keyword** for NJ/NY/CA-concentrated buyer communities (see gotcha S5); **Reddit r/{Make}{Model} + r/{State}Cars** for other states; **Facebook owner groups** (e.g., "F-150 Owners") for older-skew makes/models.

This is the source of truth every subsequent counter cites. Re-pull whenever the buyer references a new external claim ("friend got $X off"). See `references/deal_data_sources.md` for query recipes + source catalog.

### Phase 3: Multi-Site Inventory Research

Dispatch parallel subagents across inventory sites; each returns `report_<site>.md`, then merge into `master_comparison.md` (Site Capability Matrix on top, VIN-deduplicated candidates below). The new-car vs used-car router gate fires BEFORE dispatch and changes both the site set and the history-PDF requirement. Site list, role tagging and merge rules: `references/phases.md` Phase 3 and `references/outreach_strategy.md`.

**Full details**: see `references/phases.md#phase-3-inventory`.

### Phase 4: Mass Email Outreach

Submit lead forms or direct emails to the top 30-50 candidates, tracking per-dealer fields in `tracker.md`. **Run the dealer-group ownership check (gotcha D11) BEFORE treating multiple stores as independent cross-bids.** Email format per Critical Rule #1, REAL-tagged citations only per Critical Rule #7. Full procedure: § Outbound Email SOP and `references/phases.md` Phase 4.

**Full details**: see `references/phases.md#phase-4-outreach`.

### Phase 5: Recurring Inbox Monitoring

Three scheduled CronCreate jobs (not one): main 15-min inbox cron, 6-hour spam+promotions sweep, 7 AM morning catch-up. OOO autoresponder detection skips drafting and flags tracker until parsed return date. See `references/cron_monitoring.md` for full prompt templates, Gmail search patterns, OOO keyword list. Reply templates in `assets/dealer_reply_template.md`.

**Full details**: see `references/phases.md#phase-5-cron` (stub pointing to `cron_monitoring.md`).

### Phase 6: OTD Negotiation

Always-written, never-verbal OTD ask format with required line items (sales price + state tax + doc fee + title + reg + add-ons). Anchoring techniques: internal-trim, market-comp, cross-dealer (gotcha N1). ADM kill list (gotcha D9) demands removal as precondition, not middle-meet. Escalation Ladder when dealer delays. Bait-and-switch protocol (gotcha D10). Buyer-type specific notes for financing / lease / trade / EV / pickup / heavy-duty / luxury / CPO. See `references/negotiation_playbook.md` for full math + walk-away lines.

**Full details**: see `references/phases.md#phase-6-negotiation`.

### Phase 7: PDF Analysis

For every dealer-attached PDF (CARFAX, service records, OTD proposal, PPI report), open with Read tool and extract: VIN match, owner count, accident / damage / structural / odometer, service record completeness, active recalls. Per-brand expected service tables + ADAS recal by brand + OTD Proposal Add-On Anti-Pattern Detection. See `references/pdf_review_checklist.md` for the full checklist.

**Full details**: see `references/phases.md#phase-7-pdf` (stub pointing to `pdf_review_checklist.md`).

### Phase 8: Decision Dossier

Before test drive, generate a 7-10 page HTML+PDF dossier the buyer brings to the dealer:

```bash
cp assets/dossier_config_template.yaml my_dossier.yaml
$EDITOR my_dossier.yaml
python scripts/generate_dossier.py --config my_dossier.yaml \
  --output my_dossier.html --to-pdf my_dossier.pdf
```

For Chinese-speaking dealers: `--template assets/dossier_template_cn.html`. Placeholders documented in `assets/dossier_config_template.yaml`. Generator validates load-bearing fields + placeholder substitution; auto-detects Chromium-family browsers.

**Full details**: see `references/phases.md#phase-8-dossier`.

### Phase 9: Test Drive + Close

Maintain a PRIVATE `{dealer}_negotiation_prep.md` (buyer-only, never shared) with the dynamic OTD ladder, test-drive checklist, post-drive questions, decision matrix. Re-confirm the close-day logistics mini-table from `criteria.md` (Phase 1 capture) at close-day kickoff. Close-day routing branches by buyer type (cash / financing / trade / EV / pickup), execute all relevant sub-checklists if multiple apply. F&I close-day hard-no script (gotcha P3) is mandatory.

**Full details**: see `references/phases.md#phase-9-close` (includes all 5 buyer-type sub-checklists + universal close-day cross-references).

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

**Full protocol: [`references/pivot_protocol.md`](references/pivot_protocol.md).** It fires on roughly
one cycle in three, so it is loaded on demand, but the trigger is checked on every cycle.

**Load-bearing fields. If any of these changes mid-cycle, STOP and load the protocol before sending
anything else:**

1. Budget or financing structure (cash / finance / lease)
2. Target vehicle set (model, trim, model year)
3. Geography or search radius
4. Trade-in presence or its valuation
5. Timeline or close date
6. Plate / registration state

A changed load-bearing field invalidates quotes already in flight. **Do not let a stale quote enter
the dossier**, and do not simply send a correction on top: the protocol exists because a partial
re-quote produces two dealers answering two different questions.
## Resources

### References (load on demand)

This is an index of load conditions, not a summary of contents. It answers "do I need to open this
file right now", nothing else. Deliberately: a summary here is a second copy of the shard that no
one updates when the shard changes, and a stale summary the agent trusts instead of opening the
file is worse than no summary at all. If you want to know what is in a shard, open the shard.

| File | Load when |
|---|---|
| `phases.md` | Entering any phase from 3 through 9. Anchors `#phase-3-inventory` through `#phase-9-close`. |
| `gotchas.md` | A phase summary or another reference cites a gotcha ID. Also unconditionally at session start (group H), before drafting any dealer email (E), and before any counter (N, D). |
| `pivot_protocol.md` | Any load-bearing field changed mid-cycle. Trigger list is in § Mid-Cycle Pivot Protocol. |
| `deal_data_sources.md` | Phase 2 baseline pull, and every re-pull triggered by a new buyer claim. |
| `outreach_strategy.md` | Phase 3 site dispatch, and Phase 4 channel selection. |
| `outbound_email_sop.md` | Before composing Phase 4 outreach or any counter. |
| `email_format_rules.md` | Before saving any Gmail draft. |
| `cron_monitoring.md` | Phase 5, creating or debugging the three inbox crons. |
| `negotiation_playbook.md` | Phase 6, before sending any counter or walk-away line. |
| `pdf_review_checklist.md` | Phase 7, any dealer PDF in hand (CARFAX, service records, OTD proposal, PPI report). |
| `ppi_booking.md` | Booking a PPI, Phase 6 or Phase 9. |
| `state_fees.md` | Quoting any tax, doc, title or reg number; radius spans 2 or more states; plate-transfer decision. |
| `payment_methods.md` | Capturing the Phase 1 payment method, or the financing gate fires YES. |
| `trade_in.md` | Trade-in gate fires YES. |
| `lease_playbook.md` | Buyer is leasing, or a cash-to-lease conversion is on the table. |
| `private_party_playbook.md` | Seller-type gate answers private individual (FSBO). |
| `ev_buyer_playbook.md` | EV gate fires YES (battery-electric or PHEV). |
| `vertical_playbooks.md#part-1-pickup-truck-specifics` | Candidate is a light-duty pickup. |
| `vertical_playbooks.md#part-2-heavy--commercial--luxury` | Candidate is heavy-duty, a commercial van, or a luxury brand. |
| `glossary_es.md` | Producing any Spanish buyer-facing surface. |
| `subaru_cpo_program.md`, `honda_cpo_program.md`, `toyota_cpo_program.md`, `mazda_cpo_program.md`, `hyundai_cpo_program.md`, `kia_cpo_program.md`, `lexus_cpo_program.md`, `genesis_cpo_program.md`, `acura_cpo_program.md` | Candidate is CPO, or is marketed as certified, for that brand. Load only the brand in play. |
| `ford_bluecert_program.md` | Candidate is a Ford marketed as Blue Advantage Certified, either tier. |
| `gm_cpo_program.md` | Candidate is a CPO Chevrolet, GMC or Buick. |
| `stellantis_cpo_program.md` | Candidate is a CPO Ram, Jeep, Chrysler, Dodge or Fiat (SPOTiCAR). |

### Assets (templates, copy and edit)

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

## Outbound Email SOP

**Full procedure: [`references/outbound_email_sop.md`](references/outbound_email_sop.md).** Load it
before composing Phase 4 outreach or any counter. Two things stay here because they are checkable
before you open a draft.

**Pre-draft gate, all five must be Y or do not open a draft:**
1. Every load-bearing field in `criteria.md` confirmed current (see Mid-Cycle Pivot Protocol)?
2. Target vehicle list final, with stock number and VIN per dealer?
3. Attachment files already prepared at full resolution on disk?
4. Buyer's send window agreed?
5. Walk-away number set, and NOT going into the email?

**Length limits, hard:**

| email type | content lines |
|---|---|
| first outreach to a dealer | <= 10 |
| counter / reply | <= 10 |
| close-day confirmation | <= 14 |

**NEVER inline image attachments via MCP `create_draft`** (gotcha E5), the constraint chain forces
unreadable 16-20KB images. Attachments are handed to the buyer as a per-draft recipe instead.
## Gotchas (index only, full incidents in `references/gotchas.md`)

Cited by ID from the phase summaries and from other references. **Load `references/gotchas.md` when a phase points at one**, or before drafting dealer email (group E), before any counter (N, D), and at session start (H).

- **E. Email & Drafting Hygiene**, E1, E2, E3, E4, E5
- **I. Inbox & Cron Monitoring**, I1, I2, I3, I4, I5
- **D. Dealer Behavior & Communication**, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11
- **S. Data Sourcing & Sources**, S1, S2, S3, S4, S5
- **N. Negotiation Mechanics**, N1, N2
- **V. Vehicle Verification**, V1, V2
- **P. PPI & Test Drive**, P1, P2, P3
- **H. Session & State Hygiene**, H1, H2
## Language and Audience Separation

The skill operates in two language registers simultaneously. Drift between them causes either confusion (buyer sees an internal jargon dump) or unprofessionalism (dealer sees Chinese characters in a counter-offer email). Hold the separation strictly.

| Surface | Language | ASCII required | Notes |
|---|---|---|---|
| Internal reasoning + agent-to-buyer dialogue (chat window) | Buyer's preferred language (English / Chinese / Spanish / etc.) | No | Render math, gotcha names, anchor citations in whatever language the buyer is using. The bilingual triggers in this skill's description ("buy me a car" / "帮我找车") signal acceptable buyer-side languages. |
| Buyer-facing artifacts: `criteria.md`, dossier (`*.md`, `*.html`, `*.pdf`), tracker, negotiation prep | Buyer's preferred language | No (HTML/PDF can carry Unicode CJK glyphs; see `dossier_template_cn.html` for the CN variant) | The CN dossier template exists for this reason. Confirm the language with the buyer at Phase 1 close; default to English if not stated. |
| Dealer-facing emails (every Gmail draft, every counter, every walk-away, every follow-up) | **ALWAYS English** | **ALWAYS ASCII** (Rule #1) | Plain English only. No Chinese, Spanish, or other non-English content under any circumstance. No emojis. No markdown. See `references/email_format_rules.md` and `assets/dealer_reply_template.md` § Voice Specification. Dealer reps in US markets read English; CRM systems may strip or mangle non-ASCII Unicode silently. |
| Skill metadata (gotchas, references, SKILL.md, phase files) | English (source of truth) | N/A (markdown source, not transmitted to dealer) | All gotcha IDs, rule numbers, section names, and code-like identifiers are English. Translations of these into other languages happen at the agent-to-buyer surface only, never in the source files. |

**Buyer-spoken refusal carve-out.** A buyer may *speak* the F&I hard-no refusal at the desk in their own native language (Spanish / Chinese / etc.), speech is the agent-to-buyer surface, not a dealer-facing artifact. Everything *written* or *transmitted* to the dealer (Gmail drafts, counters, signed-agreement line items, the printed hard-no card you hand across the desk) stays English + ASCII per Rule #1, with no exception. Translated verbatim scripts live in `skills/close-day-checklist/SKILL.md` § "Verbatim Refusal Script (buyer-spoken language)" and are labeled spoken-only; they are never pasted into an email body or handed to F&I as a written document.

**Verification at draft time.** Before saving any Gmail draft via `create_draft`, scan the body for non-ASCII characters and any non-English content. If the buyer's preferred language is Chinese and an internal note about the dealer email leaked into the draft body, strip it. The draft is the dealer-facing surface; English-only, ASCII-only, no exceptions.

**Mixed-language `criteria.md`.** `criteria.md` may be authored in the buyer's language, but values pulled into dealer email are buyer profile data, not buyer voice: translate them to English at draft-creation time. Rules: `references/email_format_rules.md`.

## Post-Cycle Feedback

Fill `assets/feedback_log.md` at every cycle close OR abort, **and after every gotcha violation even if the cycle continues**. Append-only; a gap recurring in 3+ cycles becomes a skill change. Concrete entries only, "P1 was OK" produces nothing actionable. Takes 10-15 minutes, and skipping it means the next iteration has nothing to act on.

Protocol: [`assets/_feedback_protocol.md`](assets/_feedback_protocol.md).
## Quick Start

To begin a new car search:

1. Read this SKILL.md (already loaded if skill triggered).
2. Phase 1: gather requirements from user, save to `criteria.md`.
3. Phase 2: pull baseline market data (`references/deal_data_sources.md` pipeline).
4. Create working directory `C:\Users\<user>\car_buying_<year>\` and copy `assets/tracker_template.md` → `dealer_outreach_tracker.md`.
5. Phase 3: dispatch parallel research subagents.
6. Phase 4-5: outreach + cron monitoring.
7. Phase 6 onward: reply drafting, PDF review, dossier, close.
