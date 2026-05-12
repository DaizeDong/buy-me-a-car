# Roadmap

A running list of future feature ideas for `buy-me-a-car`. Not tied to versions. Each item gets done if and when it earns its slot.

**Complexity tags:** S = small (hours), M = medium (1-2 days), L = large (1+ week), XL = significant project.

Open a GitHub issue if you want to pick one up or have a new idea.

---

## A. Workflow Phase Enhancements

Improvements to the existing 8 phases without expanding scope.

### A1. Thread-ID dedup in cron prompt (S)
**Problem:** The cron prompt scans threads newer than 1 hour and may re-process already-drafted threads.
**Fix:** Track processed thread IDs in a small state file or in the tracker, and exclude them in subsequent runs.

### A2. 24h stale-offer detection (M)
**Problem:** A locked OTD without follow-up can lapse silently if the buyer commits to a different dealer.
**Fix:** Add a daily check that flags any "locked but no activity in 24h" offer in the tracker and produces a polite walk-away draft.

### A3. Playwright MCP bundling for anti-bot sites (M)
**Problem:** CarGurus, Cars.com, AutoTrader, Edmunds, TrueCar return 403 to direct fetches. Currently Phase 3 just says "use playwright MCP."
**Fix:** Bundle a playwright workflow that knows how to navigate each of these sites end-to-end and submit a lead form with the buyer's info pre-filled.

### A4. Gmail attachment text extraction (M)
**Problem:** Dealers send OTD proposals as PDF attachments. Claude cannot read attachments via Gmail API; user must manually open and share.
**Fix:** A script that fetches Gmail message attachments via OAuth and extracts text via `pdfplumber` or similar, returning structured fields.

### A5. Auto-generated dealer reply on receipt (S)
**Problem:** Cron drafts replies, but the draft style depends on the user's manual selection of which template.
**Fix:** Add a classifier that detects the dealer's message intent (generic intro / OTD provided / wants-to-visit / price-firm / walk-away) and picks the right template automatically.

### A6. Per-state cron prompt presets (S)
**Problem:** Each buyer types out the cron prompt with their state's tax info and dealer list manually.
**Fix:** A `scripts/setup_cron.py` that builds the cron prompt from the buyer's state + makes-of-interest.

---

## B. New Vehicle Categories

Expand beyond used-car purchase.

### B1. New car workflow (L)
**Why:** Many users want a new car; current skill only does used.
**Scope:** New-car-specific phases: invoice price discovery, manufacturer rebates, dealer holdback, regional incentive lookup, financing rate negotiation.

### B2. Lease workflow (L)
**Why:** Lease has its own math: money factor, residual value, cap cost reduction, lease vs buy break-even.
**Scope:** Lease-specific calculator + negotiation framework + total cost vs purchase comparison.

### B3. Trade-in tax credit calculator (S)
**Why:** Most states allow trade-in value to be subtracted from taxable price; not currently handled.
**Fix:** Extend `otd_calculator.py` with `--trade-in` flag that adjusts the taxable base per state law (CA, KY, DC are exceptions).

### B4. EV-specific workflow (M)
**Why:** EVs have federal tax credit ($7,500 IRS), state rebates, charger install costs, home electricity rate considerations.
**Scope:** Add EV-specific dossier section + tax credit eligibility check + total cost of ownership comparison.

### B5. Salvage / rebuilt title workflow (M)
**Why:** Some buyers want salvage cars for ~50% off; the workflow is very different (heavy inspection, insurance issues).
**Scope:** Separate flow with stronger PPI emphasis, insurance limitations, resale value warnings.

---

## C. Tooling & Infrastructure

Behind-the-scenes improvements.

### C1. State fee data freshness check (S)
**Problem:** State sales tax / doc fee caps change. The `references/state_fees.md` snapshot may go stale.
**Fix:** Annual data-refresh script that pulls from NCSL (National Conference of State Legislatures) or state DMV APIs.

### C2. OEM CPO programs beyond Subaru (M)
**Currently in skill:** Subaru CPO program details.
**Missing:** Toyota Certified Used Vehicles, Honda Certified, Mazda Certified, Ford Blue Advantage, Hyundai H Promise, etc.
**Fix:** Add one `references/cpo_<manufacturer>.md` per major OEM.

### C3. Recall and TSB database integration (M)
**Why:** NHTSA + manufacturer TSBs (Technical Service Bulletins) reveal known issues per VIN. Buyer should know before purchase.
**Fix:** Integrate `vpic.nhtsa.dot.gov` API for recall lookup; cross-reference with common TSBs per make/model.

### C4. VIN decoder script (S)
**Why:** Decoding VIN reveals year, make, model, plant, engine code, equipment. Useful for verifying dealer-claimed specs.
**Fix:** Implement or wrap `vinpy` / NHTSA VIN decoder API; output structured spec.

### C5. Carfax pulled-data parser (M)
**Why:** Currently the skill reads CARFAX PDFs reactively. A parser that extracts structured fields (VIN, owner count, accident history, service records summary) would feed downstream analysis.

### C6. Test framework for skill scripts (S)
**Why:** Manual end-to-end testing on every change is slow. Currently we have a 21-test bash suite.
**Fix:** Promote it to a proper `tests/` folder + GitHub Actions CI on PR.

### C7. Per-state OTD calculator web UI (M)
**Why:** Some users want to use the calculator without running Python.
**Fix:** A simple HTML+JS page hosted via GitHub Pages that calls a local copy of the rates.

---

## D. Data & Community

Building a community around the skill.

### D1. Shared transaction dataset (XL)
**Goal:** Real-world final OTD data from completed transactions to anchor negotiations.
**Design:** PR-based dataset at `data/transactions.jsonl`; users contribute via GitHub Issue template or PR; CI validates schema; aggregated stats fed into Phase 5.
**Concerns:** Privacy (re-identification in low-volume areas), data quality (self-reported noise), adoption (likely < 5% contribute back).
**Wait until:** 100+ active users; until then, public data sources (Carfax, AutoTrader, CarGurus) suffice.

### D2. Anonymous benchmarks dashboard (XL)
**Depends on:** D1 dataset.
**Goal:** A public GitHub Pages dashboard showing region/make/model price benchmarks.

### D3. Community-contributed dealer ratings (L)
**Goal:** A `data/dealer_ratings.jsonl` that buyers contribute to: responsiveness, transparency, willingness to negotiate, hidden fees encountered.
**Concerns:** Defamation risk; needs clear "facts only" template; not subjective.

### D4. Contribution guidelines (S)
**Goal:** A `CONTRIBUTING.md` that explains how to add data, fix bugs, propose features.

### D5. Issue templates and PR templates (S)
**Goal:** Templates that route new ideas / bugs / data contributions to the right format.

---

## E. Multi-Market & Multi-Language

Expand reach beyond NJ tri-state English buyers.

### E1. Spanish dealer interaction templates (M)
**Why:** Many US Hispanic communities have Spanish-speaking dealers.
**Fix:** Spanish version of `dealer_reply_template.md`, `dossier_template_es.html`.

### E2. Canadian provincial fee data (M)
**Why:** Cross-border or Canadian buyers have different tax structures.
**Scope:** Add `references/canadian_fees.md` covering 10 provinces + 3 territories (PST/GST/HST/QST varieties).

### E3. UK / EU fee structures (XL)
**Why:** Some users in EU also buy used cars; tax + VAT + registration vary by country.
**Scope:** Country-specific fee references for major markets (UK, Germany, France, etc.).

### E4. Translation pipeline for dossier (S)
**Currently:** EN and CN templates exist.
**Fix:** Add other languages via translation; or build a script that calls an LLM to translate the EN template at runtime.

---

## F. Post-Purchase Phase 9

Extend the workflow beyond closing.

### F1. Closing day checklist (S)
**Why:** First-time buyers don't know what to look for at signing: payment, paperwork, plates, insurance.
**Fix:** A `references/closing_day_checklist.md` covering bill of sale, title transfer, insurance binder, temp tags.

### F2. First 30 days post-purchase guide (S)
**Topics:** Registration completion, state MVI inspection, plate transfer paperwork, CPO enrollment if eligible, first oil change, tire rotation schedule.

### F3. Resale prep workflow (M)
**Why:** When the buyer wants to sell this car later (3-5 years out), how to maximize resale.
**Scope:** Maintenance schedule guidance, photo/listing tips, pricing strategy.

### F4. Insurance shopping integration (M)
**Why:** Insurance is a major TCO line item not currently addressed.
**Scope:** Compare top 5 insurers via API where available + manual quote-gathering script.

---

## G. Stretch / Speculative

Ideas that may or may not work.

### G1. Voice-driven negotiation (XL)
**Why:** A buyer at the dealer could speak into their phone and Claude listens, suggests counters.
**Concerns:** Privacy, latency, dealer might not consent to recording.

### G2. Auto-dispatching follow-ups (M)
**Why:** Cron monitors inbox; could also auto-send polite "still interested?" pings after 48h silence.
**Concerns:** Dealers may flag as spam; needs careful pacing.

### G3. Multi-buyer collaboration (L)
**Why:** Couples or families negotiate together; sharing the tracker would help.
**Scope:** A shared-tracker mode where two Claude sessions work the same project folder.

### G4. Dealer-side perspective (XL)
**Why:** Understand the dealer's incentives more deeply (allocation, holdback, manufacturer incentives, fiscal year end).
**Scope:** A `references/dealer_economics.md` explaining margin structures.

---

## How to Contribute

Pick any item, open a GitHub issue saying "I'm working on X," then PR. Or open an issue with a new idea and tag it with the right category.

The current authors are reachable through GitHub issues on this repo.
