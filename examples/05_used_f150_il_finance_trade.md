# Scenario 5: Used Ford F-150, Chicago metro IL, credit-union financing + trade with lien

## The buyer

The buyer is a construction project manager in the Chicago metro
(<ZIP>). They are a second-time pickup-truck owner. They
test-drove two F-150 XLTs at a local Ford dealer last weekend.

## The target

A 2021-2023 Ford F-150 XLT or Lariat SuperCrew 4x4. Engine: 3.5L EcoBoost
preferred (13,000 lb tow rating with Max Trailer Tow), 5.0L V8 acceptable.
Bed: 5.5' standard preferred. Under 60,000 miles. Must-haves: tow package,
heated seats, SYNC 4, BLIS blind spot, rear backup camera. Colors: Iconic
Silver, Antimatter Blue, or Carbonized Gray; no white.

## The constraints

- Budget: $38,000 to $44,000 OTD. Walk-away ceiling: $45,500 hard stop.
- Geographic radius: 75 miles of <ZIP> — covers the Chicago metro + adjacent IL/IN/WI.
- **Payment: financing through a military-affiliated credit union** (via
  spouse).
  - Pre-approved 4.99% APR for 72 months.
  - Max financed: $40,000.
  - Max monthly: $625.
  - Down payment: $5,000 cash.
- **Trade-in: 2015 Ram 1500 Big Horn Crew Cab 5.7L Hemi 4x4**, 142,000
  miles, clean title, **$2,800 payoff to Ally Bank (lien)**, all keys,
  minor bedliner wear + 1 small driver-door dent, brakes need pads soon
  (~$400 fix).
- Timeline: close by end of month (2026-06-30, ~4 weeks).

## The ask

The buyer wants the workflow to:

1. Filter inventory with **pickup-specific rigor**: tow rating depends on
   engine × axle ratio × tow package. A 3.5L EcoBoost without the Max
   Trailer Tow package tows 11,300 lb, not 13,000. The Phase 3 listing
   filter must verify the factory tow option code (53A / 535 / AHT / NHT
   depending on year) — not just check that "tow package" appears in the
   description.
2. Handle the **trade with lien**: the dealer must overnight a check to
   Ally Bank to release the title; this stretches the close-day timeline
   by 5-14 days and creates a specific T-10 to T+30 sequence.
3. Apply the **Illinois trade-in tax credit correctly**: post Rivian-vs-
   Ford lobbying (SB-690, 2020+), Illinois caps the trade-tax credit at
   the **first $10,000 of trade value**. The buyer's $7,000-target trade is
   below this cap so the full credit applies. The gross-vs-net distinction
   is easy to muff at close.
4. Catch a high-mileage trade lowball: at 142k miles, KBB Instant Offer
   may decline outright or come in at $4,000-$5,500. Walk-floor is
   Manheim wholesale (~$5,800-$6,500) — anchor the trade ask off the
   wholesale floor, not the dealer's first number.
5. Counter a synthetic dealer reply with five distinct issues (sale price
   too high, trade lowball, lien not addressed, captive financing not
   mentioned, OTD line-item math off by $769).

## What makes this scenario interesting

- This is the **first pickup-truck case**. Before this scenario, the skill
  had no codified knowledge of tow-rating dependency, factory-vs-aftermarket
  tow packages, payload-vs-tow distinction, or pickup-specific PPI items.
- Illinois has the highest doc fee cap in the U.S. ($347.26, statutory,
  CPI-linked), the highest title fee ($155), and county tax stacking up
  to 10.25% (Chicago) — but the buyer's Illinois county is a more moderate 7.5%.
- The **trade has a lien**, which compounds with the financing path:
  the lender (the credit union) needs the trade-in payoff structure resolved before
  funding the F-150 loan. Phase 9 close-day needs a T-10 to T+30 timeline.
- Cross-brand trade (Ram → Ford): no loyalty rebate possible across
  brands. Phase 6 should not waste an ask on this.
- The combination — financing + trade-with-lien + pickup specifics + IL
  fees — is the most operationally complex scenario in the set. If the
  skill handles this, it covers most of the U.S. F-150 buyer population.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md) — Phases 1, 3, 6, 9.
- [trade-in-valuator](../skills/trade-in-valuator/SKILL.md) — four-anchor
  valuation for a high-mileage Ram + lien payoff workflow (§ 4a-4d).
- [payment-method-decider](../skills/payment-method-decider/SKILL.md) —
  credit-union vs Ford's captive financing arm comparator.
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md) — Illinois
  detail stub (ZIP-disambiguated county rates, $347.26 doc cap, $155
  title, $151 reg, $10k trade-credit cap) plus IL→IN / IL→WI cross-state
  rows.
- [ppi-scheduler](../skills/ppi-scheduler/SKILL.md) — pickup-specific
  PPI (frame rust, transmission cooler, EcoBoost turbo seals, hitch wear).
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md) — 5-ask
  counter against the synthetic dealer.
- [close-day-checklist](../skills/close-day-checklist/SKILL.md) — pickup
  buyer-type sub-checklist with lien-payoff timing.

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1 — fired both the financing branch and the
   trade-in branch of the buyer-type router simultaneously. Captured 9
   financing fields + 12 trade-in fields + lien-specific sub-questions
   ("Title in hand or held by lien-holder?" branch).
2. **state-fee-lookup** — Illinois detail (state 6.25% + the buyer's Illinois county 1.25%
   for 7.5%; $347.26 doc cap; $155 title; $151 reg; $10k
   trade-credit cap unique to IL).
3. **payment-method-decider** — credit-union 4.99%/72mo vs Ford's captive
   financing arm; flagged that Ford's captive sometimes unlocks $500-$1,000
   customer cash that the credit union cannot match.
4. **orchestrator** Phase 3 — inventory pull across IL / IN / WI; surfaced
   5 pickup-specific gaps (tow rating dependency on engine × axle ratio
   × tow package code, factory-vs-aftermarket distinction, pickup PPI
   items, used-pickup depreciation, IL doc-cap arbitrage against IN $279
   doc cap).
5. **trade-in-valuator** — four-anchor for the 142k-mile Ram: KBB
   Instant Offer declined (high miles), KBB Trade-In Fair $6,500-$7,200,
   KBB Private Party $7,800-$8,500, Manheim wholesale $5,800-$6,500.
   Plus lien-payoff workflow (T-10 to T+30 sequence).
6. **dealer-reply-drafter** — counter to a synthetic sales rep at a
   Chicago-area Ford dealer. 5 distinct issues identified.
7. **close-day-checklist** — pickup buyer sub-checklist + trade sub-
   checklist + financing sub-checklist merged.

### Artifacts produced

- `criteria.md` with financing + trade + lien sub-questions.
- `inventory.md` — 8 F-150 candidates filtered to 3 primary tier (a
  Chicago-area Ford dealer #1, an Illinois Ford dealer #3, a Wisconsin
  dealer #6) by tow-config + ADM detection.
- `p6_counter_to_dealer.md` — 5-ask counter:
  - Sale price: $41,495 → $40,495 (regional comps, mileage adjust).
  - Trade allowance: $5,800 → $7,000 (KBB Trade-In Fair + private-party
    range; high-mileage discount acknowledged).
  - Lien: surface $2,800 Ally payoff in counter; demand dealer overnight
    check to Ally.
  - Captive financing: ask independently per D9 sub-rule (no coupling).
  - Line-item math: the rep's $46,613 OTD is $769 above the line-item sum
    of $45,843; demand itemization (D8).
- `p9_close_checklist.md` — T-7 / T-3 / T-0 / T+1 to T+30 timeline with
  pickup PPI, lien payoff handoff, IL paperwork, credit-union funding sequence.

### Gotchas and Critical Rules that fired

- **Gotcha D8 (state-fee-template leak / OTD math leak)** — fired on
  the rep's $769 itemization gap.
- **Gotcha D9 (ADM kill list)** — fired on two flagged Chicago-area and
  Wisconsin listings during Phase 3 filter.
- **Critical Rule #1 (plain ASCII)** — counter is ~12 lines, no markdown,
  no em-dashes.
- **Separate-the-negotiation 5-round protocol** (from `trade_in.md` § 8)
  — sale and trade asked as independent transactions.
- **Cold Open recipe** — five elements present in counter.
- **Illinois $10k trade-credit cap** — load-bearing for OTD math.
  The buyer's $7,000 trade is below the cap so full credit applies; at close,
  buyer should verify the **gross** trade allowance (not net-of-payoff)
  appears on the bill of sale's tax line.

### What this scenario surfaced for the skill

Four concrete deltas landed:

- **Illinois detail stub at CT/CA/TX depth** — ZIP-disambiguated county
  rates (5+ tiers from Chicago 10.25% to DuPage 7.5%), $347.26 doc cap
  (highest in U.S., statutory + CPI-linked), $155 title (highest in
  U.S.), $151 reg, $26 plate transfer, $20 LE emissions inspection,
  trade-tax credit YES but **capped at first $10,000 of trade value**
  (Rivian-vs-Ford SB-690 outcome since 2020), "Has" + "Does NOT have"
  leak lists, 2 worked OTD examples (no-trade and with-$7k-trade +
  $2.8k-lien), IL→IN / IL→WI / IL→MO / IL→IA cross-state titling rows.
- **`vertical_playbooks.md#part-1--pickup-truck-specifics` (NEW reference file)** — 8 sections:
  tow rating dependency table (F-150 / Ram / Silverado-Sierra / Tundra
  2021-2024 engine × axle × tow package combinations with real tow
  capacity in lb), factory-vs-aftermarket distinction (integrated TBC,
  transmission cooler, axle upgrade, sway control software, hitch
  class), payload capacity (separate from tow; the #1 pickup-buyer
  mistake), pickup-specific PPI items (frame rust, transmission cooler,
  exhaust manifold on V8 / Hemi MDS lifters / EcoBoost turbo seals,
  hitch wear, body mounts, plow-truck flags), used-pickup depreciation
  patterns (55-60% retained value year 3 for domestic 1500-class, 70-75%
  Tacoma), pickup dealer tactics, Phase 6 pickup checklist (verify VIN
  decode for tow option code 53A/535/AHT/NHT before deposit), pickup
  walk conditions.
- **`trade_in.md` § 4a-4d lien payoff workflow** — full 4-step T-10 to
  T+30 timeline, title-in-hand vs title-with-lien-holder state matrix
  (NY/MN/PA/MD/KY hold title with lien notation; others lien-holder
  holds), payoff routing dispute resolution, 5 mandatory dealer questions
  in writing.
- **Phase 9 expansion to buyer-type sub-checklists** — previously a
  single 8-line paragraph; now 5 routed sub-checklists (cash / financing
  / trade / EV / pickup) each 6-10 items with cross-references to
  `trade_in.md` § 4 + § 11, `vertical_playbooks.md#part-1--pickup-truck-specifics` § 7,
  `ev_buyer_playbook.md` § 9-10, the CPO refs, `ppi_booking.md`,
  `state_fees.md`, `payment_methods.md`.

### Reading takeaway

This is the most operationally complex scenario in the set. If you can
work through this one, you understand the full surface area: financing
+ trade-with-lien + state-specific quirk (the $10k cap) + pickup
specifics + close-day execution with a 5-14 day lien-release window.
Read last.
