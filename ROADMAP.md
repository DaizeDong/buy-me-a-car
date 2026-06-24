# Roadmap

Current: **v0.2.2**

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
- All 50 US states + DC covered at fee-detail depth (30 full + 21 stub),
  34 of them web-verified. Rendered from `data/state_fees.json` via
  `skills/orchestrator/scripts/render_state_data.py`.
- 16-brand CPO coverage across 12 programs (Subaru, Toyota, Honda, Mazda,
  Hyundai, Kia, Ford, GM, Stellantis SPOTiCAR [Ram/Jeep/Chrysler/Dodge/Fiat
  = 5 brands in one program], Lexus, Genesis, Acura).
- 6 buyer paths supported (cash / finance / lease / trade / EV /
  private-party). Private-party (FSBO) path keyed off the seller-type gate,
  with its own `private_party_playbook.md`.
- Trilingual surface: EN / CN / ES triggers, EN + CN dossier templates, and
  an explanatory ES glossary for load-bearing terms, under a strict
  language-and-audience separation (dealer emails stay English + ASCII).
- `examples/` directory with 8 end-to-end worked scenarios (01-05 dealer
  cash/finance/trade/EV/pickup foundation set; 06-08 lease, private-party,
  Stellantis CPO regression fixtures).
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
- EV-credit reinstatement watch: federal §30D / §25E / §45W are TERMINATED
  for vehicles acquired after 2025-09-30 (OBBBA); track any legislative
  reinstatement and re-enable the federal-credit math the moment it lands.
- ES glossary native-speaker sign-off: current ES strings are working
  translations pending review before production use.
- Trigger-conflict stress test: verify the orchestrator doesn't fight
  sub-skills when both could fire on the same user prompt.

---

## Future (1.0.0)

- Data auto-refresh script: pull state fee + tax data from NCSL / state
  DMV sources annually so `data/state_fees.json` doesn't go stale, and lift
  the 21 stub states to full depth + raise the web-verified count past 34.
- Buyer-style router: detect aggressive / relationship / passive buyer
  style and tune outreach + counter-offer tone.
- Add brand CPO programs for remaining luxury / niche makes (BMW, MB, Audi,
  Porsche, Infiniti, Cadillac, Lincoln, Volvo). (Subaru, Toyota, Honda,
  Mazda, Hyundai, Kia, Ford, GM, Stellantis SPOTiCAR [Ram/Jeep/Chrysler/
  Dodge/Fiat], Lexus, Genesis, Acura already shipped.)

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
