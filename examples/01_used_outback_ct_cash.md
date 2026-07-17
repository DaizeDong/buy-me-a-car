# Scenario 1: Used Subaru Outback, Connecticut, cash, one week to close

## The buyer

The buyer is a software engineer in Connecticut (<ZIP>). This is
their second car. They have a cashier's check ready and want
to close by the end of the week, Thursday or Friday at the latest. No trade,
no financing, no lease.

## The target

A 2022-2024 Subaru Outback, Premium or Limited trim (Limited preferred for the
leather + EyeSight + nav combo). Under 40,000 miles. Any color except white
or black. AWD is the Subaru default; the must-haves are heated seats, Apple
CarPlay, a backup camera, and EyeSight (standard on 2020+).

Reliability and AWD for Connecticut winters drive the choice. Resale value
(Outbacks hold strong) and a clean one-owner CARFAX are secondary anchors.

## The constraints

- Budget: $25,000 to $30,000 **out-the-door**.
- Geographic radius: 50 miles of <ZIP>, which sweeps in nearby tri-state metros,
  and parts of New York.
- Payment: cash via cashier's check. The buyer prefers cash because they do not
  hold a high-tier rewards credit card.
- Timeline: this week. Ready to close Thursday or Friday.

## The ask

The buyer wants the buy-me-a-car workflow to:

1. Confirm criteria (Phase 1), especially the "is the $25-30k figure OTD or
   sales price?" question, since dealers love to quote sale-price and bury fees.
2. Produce a real-data baseline for a 2023 Outback Limited in Connecticut in
   under five minutes, KBB, CarGurus, AutoTrader, regional Reddit/XHS comps.
3. Given a synthetic dealer reply with a high OTD, draft an effective counter
   with anchors that hold up under cross-examination.

Cross-state surfacing matters: the 50-mile radius covers four tax regimes
(CT, MA, NY, parts of NJ). Connecticut also has a $50,000 "luxury tier" tax
quirk that a Limited trim with options can flirt with.

## What makes this scenario interesting

- Cash + used + single-state buyer is the **baseline** for the skill, if the
  workflow can't nail this case clean, nothing downstream matters.
- New England fee structures (CT, MA, RI, NH, ME, VT) historically were
  stubbed at All-State Summary depth only, this case forces real per-state
  detail.
- Dealer template leaks (a CT buyer being quoted an NJ tire fee, for example)
  are a frequent $30-$200 leverage point that requires a "Does NOT have" list
  per state.
- Round 1 of negotiation, with one bid in hand, needs a structured Cold Open
  recipe, not a single freeform paragraph.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md), Phases 1, 2, 6.
- [otd-calculator](../skills/otd-calculator/SKILL.md), Connecticut math.
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md), CT detail stub
  plus tri-state cross-radius (MA, NY, RI).
- [cpo-eligibility](../skills/cpo-eligibility/SKILL.md), Subaru Certified
  embedded value on 2022-2024 Outbacks.
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md), the
  Round 1 Cold Open counter.

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1, captured the 9-field core (vehicle / trim / year
   window / mileage cap / color / budget / radius / payment / timeline).
2. **state-fee-lookup**, pulled the Connecticut detail (6.35% base, $50k
   luxury tier at 7.75%, $75 doc, $25 title, ~$120/yr reg).
3. **otd-calculator**, computed gross OTD for a $26,500 sale Limited at
   $28,925 (under the $30k ceiling).
4. **cpo-eligibility**, confirmed 2022-2024 Outbacks fall inside Subaru
   Certified (7yr/100k powertrain from in-service); embedded value ~$2,000-2,500.
5. **dealer-reply-drafter**, drafted the Round 1 Cold Open counter against a
   synthetic dealer OTD of $31,400.

### Artifacts produced

- `criteria.md`, Phase 1 criteria with explicit walk-away ceiling, OTD-vs-
  sales-price marker, and the 3-row "Heads-up before you confirm" block.
- `outback-ct-baseline.md`, regional median anchors (CarGurus, KBB, AutoTrader,
  XHS, Reddit) with REAL/SYNTHESIZED provenance flags.
- `p6_counter_to_synthetic_dealer.md`, paste-ready counter under 12 lines,
  three asks, all anchored.

### Gotchas and Critical Rules that fired

- **Critical Rule #1 (plain ASCII)**, counter email contains no em-dashes,
  no smart quotes, no markdown bold.
- **Critical Rule #7 (REAL-tagged citations only)**, the baseline file uses
  one REAL row (a live KBB Instant Offer query) and four SYNTHESIZED regional
  comps; the counter email cites only the REAL row by URL + timestamp.
- **Gotcha D8 (state-fee-template leak)**, caught a synthetic dealer quote
  that included an "NJ supplemental titling fee $13.50" line on a Connecticut
  registration. Full re-quote demanded.
- **Cold Open recipe**, five elements present (acknowledgement, anchor, three
  asks, walk-away, professional close).

### What this scenario surfaced for the skill

Scenario 1 was the foundation pass. Ten concrete deltas landed:

- OTD-vs-sales-price mandatory clarifier at Phase 1.
- Walk-away ceiling field added to the criteria template.
- Critical Rule #7 created (REAL-tagged citations only in dealer-facing emails).
- REAL/SYNTHESIZED provenance schema added to the Data Synthesis Worksheet.
- New England state stubs (CT/MA/RI/NH/ME/VT) added at detail depth.
- Negative-space "Does NOT have" lists per state to mechanize leak detection.
- Cold Open module + worked Connecticut example in the negotiation playbook.
- Gotcha D8 (state-fee-template-leak = full re-quote leverage) codified.

### Reading takeaway

This is the simplest scenario in the set. If you are new to the skill, read
this one first, it shows the clean baseline path with no financing, no trade,
no EV, no pickup. Scenarios 2 through 5 each add one structural axis on top
of this foundation.
