# Scenario 2: New RAV4 Hybrid, Philadelphia metro PA, credit-union financing

## The buyer

The buyer is a healthcare administrator in the Philadelphia metro
(<ZIP>). She lives with her spouse and a toddler and
is buying her first new car. She test-drove a RAV4 Hybrid at her local dealer
last weekend and is decided.

## The target

A 2025 Toyota RAV4 Hybrid. XLE preferred (the sweet spot for budget), LE
acceptable, XSE a stretch. New, not used. She prefers Silver Sky, Blueprint,
or Cavalry Blue; she will take white if the savings clear $300. Must-haves
include AWD (default on the Hybrid), heated seats, blind-spot monitor
(standard on XLE), Apple CarPlay, and roof rails for a cargo box.

Her priorities: fuel economy (40+ mpg combined makes the Hybrid premium worth
it for her commute), Toyota reliability, child + dog safety, resale value,
and **no dealer markup** — she knows the RAV4 Hybrid has been MSRP-plus in
some markets.

## The constraints

- Budget: $35,000 to $40,000 OTD. Walk-away ceiling: $41,500 hard stop.
- Geographic radius: 60 miles of <ZIP> — covers the Philadelphia metro covering parts of PA, NJ, DE, and MD.
- **Payment: pre-approved financing through a Pennsylvania credit union**.
  - Rate locked: 5.49% APR for 60 months.
  - Max financed amount: $36,000.
  - Max monthly payment willing: $700.
  - Down payment available: $5,000 cash.
- Timeline: three weeks (close by 2026-06-09).
- Trade: none.

## The ask

The buyer wants the workflow to:

1. Capture her financing parameters cleanly at Phase 1 — not just "I'm
   financing" but lender, rate, term, max monthly, max financed, down payment.
2. Inventory across four tax regimes (PA, NJ, DE, MD) and surface
   cross-state arbitrage if it exists.
3. Counter a dealer reply that includes a $1,495 "Toyota Hybrid Adjustment"
   line item — demand removal, do not couple to financing concessions.
4. Compare Toyota's captive financing arm (which sometimes
   unlocks an MSRP discount the credit union cannot match) against her
   locked credit-union rate.

## What makes this scenario interesting

- This is the **first financing case** the skill encounters — without a
  structured financing branch at Phase 1, the workflow falls back to "cash
  buyer with a loan attached" which loses every downstream comparison.
- The buyer-type router at P1 needs to exist before this scenario can be
  handled mechanically rather than by agent improvisation.
- The RAV4 Hybrid has historically carried "ADM" (additional dealer markup)
  with line names like "Market Adjustment", "Hybrid Premium", "Allocation
  Fee", or "Protection Plus". Phase 3 inventory triage must detect these
  mechanically (`ADM_delta = Internet_Price - MSRP`) and Phase 6 must counter
  them without coupling to financing.
- Cross-state radius means a Wilmington DE dealer might quote zero state tax
  but the buyer still owes PA's 6% on titling — easy gotcha to miss.
- First-time new-car buyer needs more hand-holding around the "did the
  dealer show you the buyers order versus the line-item breakdown?" question.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md) — Phases 1, 3, 6.
- [payment-method-decider](../skills/payment-method-decider/SKILL.md) —
  Toyota's captive lender vs credit union comparator.
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md) — PA detail plus
  PA→DE / PA→NJ / PA→MD cross-state titling rows.
- [otd-calculator](../skills/otd-calculator/SKILL.md) — financed
  binding-constraint formula (max monthly drives max financed at known APR).
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md) — ADM
  kill list applied with the single-ask, single-round, no-coupling rule.

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1 — fired the financing branch of the buyer-type
   router for the first time, capturing 9 sub-fields beyond the core (lender,
   APR, term, max monthly, max financed, down payment, captive option,
   binding constraint, refinance plan).
2. **state-fee-lookup** — PA detail (6% state, +1% Allegheny, +2% Philly, $79
   doc cap, $58 title, $39 reg) plus PA→DE / PA→NJ / PA→MD cross-state rows.
3. **payment-method-decider** — produced a both-branches comparator: credit-union
   5.49% / 60mo vs Toyota's captive financing arm 4.9% / 60mo if dealer unlocks
   $1,500 customer cash on captive only.
4. **orchestrator** Phase 3 — inventory pull across PA / NJ / DE / MD;
   `ADM_delta = Internet_Price - MSRP` flagged 4 of 12 candidates with
   $1,000-$2,200 markup under various line names.
5. **dealer-reply-drafter** — counter to a synthetic dealer email quoting a
   $1,495 "Toyota Hybrid Adjustment". Demanded removal under gotcha D9; did
   not couple to financing concession; single ask, single round.

### Artifacts produced

- `criteria.md` with the 9-field financing sub-block.
- `rav4-hybrid-pa-baseline.md` with MSRP ladder + Toyota Q2 2026 incentive
  stack (Customer Cash + captive lease cash + military / college grad rebate).
- `payment_compare.md` — credit-union vs captive lender, both branches, with the
  binding-constraint formula
  `payment = principal × (APR/12) / (1 - (1 + APR/12)^-n)`.
- `p6_counter_to_synthetic_dealer.md` — paste-ready counter, ADM line item
  rejected with one specific anchor sentence.

### Gotchas and Critical Rules that fired

- **Critical Rule #7** — only one REAL row (credit-union rate sheet screenshot)
  among five baseline anchors; all others SYNTHESIZED and not cited to
  dealer.
- **Gotcha D9 (ADM kill list)** — fired on "Toyota Hybrid Adjustment"
  $1,495. Counter sentence: "Please remove the Toyota Hybrid Adjustment;
  three concurrent listings in our radius at MSRP-or-below confirm this is
  not market-wide." Sub-rule applied: do **not** couple ADM removal to
  financing or trade concessions.
- **Cross-state surfacing rule** — flagged that titling in DE saves zero
  for a PA resident (PA collects use tax on titling regardless).
- **Cold Open recipe** — five elements present.

### What this scenario surfaced for the skill

Eight concrete deltas landed:

- **Buyer-type router at Phase 1** (the highest-leverage architectural
  change of the whole stress test) — converted P1 from a flat 9-field core
  into a 3-axis router (financing? / trade-in? / EV?) with sub-question
  blocks that layer on top of the stable core.
- Financing sub-questions (9 fields) — captures lender, rate, term, monthly
  cap, financed cap, down payment, captive option, binding constraint,
  refinance plan.
- Captive-vs-credit-union comparator added to `payment_methods.md` with
  both branches and a worked Pennsylvania example.
- Binding-constraint formula codified (max monthly determines max financed
  at known APR for known term).
- Cross-state surfacing rule (when radius covers 2+ tax regimes, surface
  the cross-state arbitrage check at Phase 1 — not Phase 6).
- PA stub expanded with PA→DE / PA→NJ / PA→MD cross-state titling rows.
- New-car-vs-used-car router gate added at Phase 3.
- **Gotcha D9 ADM kill list** with sub-rules (no coupling, one ask one
  round, cross-state-net override is a P3 decision not P6).

### Reading takeaway

This scenario unlocks the financing path. The router architecture it
introduced is what makes scenarios 3, 4, and 5 plug-in-compatible rather
than requiring full refactors. Read after scenario 1.
