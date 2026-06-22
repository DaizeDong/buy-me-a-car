# Roadmap

Snapshot of where `buy-me-a-car` stands and where it goes next.

---

## What shipped (through 0.2.2)

- Multi-skill plugin restructure: one orchestrator + 15 narrow sub-skills.
- 16 skills total covering the full 9-phase pipeline (research -> outreach
  -> negotiate -> close) and single-task entry points (OTD math, state fee
  lookup, dealer reply drafting, CARFAX/PDF review, inbox triage, close-day
  checklist, quote-evidence collection, trade-in valuation, EV federal
  credit, payment method, lease vs cash, PPI booking, dossier generation,
  CPO eligibility, insurance shopping).
- Phase 3 inventory hardening: Playwright-first multi-site scraping (real
  browser bypasses the 403/DataDome/Akamai blocks that headless fetch hits),
  per-site extraction recipes + pagination guide, and a buyer-facing Site
  Capability Matrix on top of the VIN-deduped candidate list.
- 22 US states + DC covered at fee-detail depth.
- 8 brand CPO programs (Subaru, Toyota, Honda, Mazda, Hyundai, Kia, Ford,
  GM).
- 5 buyer paths supported (cash / finance / lease / trade / EV).
- ~80 deltas resolved with root-cause attribution across iterations 1-5
  and P0-P5 fix rounds.
- Smoke test 6/6 passing.

---

## Next (0.3.0)

- Multi-author cycle data: collect real-buyer transcripts from more than
  one buyer profile to de-bias the dealer-reply templates.
- Adversarial dealer testing: red-team the negotiation flow against
  realistic high-pressure dealer scripts (pre-approval push, four-square,
  payment-only framing).
- `examples/` directory with 3-5 end-to-end runs (used Subaru cash, new
  Toyota lease, used EV with trade) checked in as reference transcripts.
- Trigger-conflict stress test: verify the orchestrator doesn't fight
  sub-skills when both could fire on the same user prompt.

---

## Future (1.0.0)

- Data auto-refresh script: pull state fee + tax data from NCSL / state
  DMV sources annually so `references/state_fees.md` doesn't go stale.
- Buyer-style router: detect aggressive / relationship / passive buyer
  style and tune outreach + counter-offer tone.
- Expand state coverage from 22 to 50 (currently stubbed states need
  fee-detail fill-in).
- Add brand CPO programs for Ram, Jeep, Chrysler, Lexus, Genesis, Acura.
  (Hyundai, Kia, Ford, GM, Mazda, Subaru, Toyota, Honda already shipped.)

---

## Out of scope

- Exotic / ultra-luxury (Ferrari, Lamborghini, Rolls-Royce) - different
  buying process, allocation-driven.
- Commercial fleet sales - separate negotiation model, volume pricing.
- Dealer-side workflow - this plugin is buyer-side only.

---

## How to contribute

Open a GitHub issue for bugs, new ideas, or data contributions. PRs
welcome for state stubs, CPO programs, and example runs.
