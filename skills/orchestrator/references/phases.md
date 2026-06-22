# Phase References (3-9)

This file is the combined reference for phases 3 through 9 of the 9-phase orchestrator workflow. Phases 1 and 2 are inline in `orchestrator/SKILL.md`; everything from inventory through close-day lives here.

## Table of contents

- [Phase 3 — Inventory](#phase-3--inventory)
- [Phase 4 — Outreach](#phase-4--outreach)
- [Phase 5 — Cron](#phase-5--cron)
- [Phase 6 — Negotiation](#phase-6--negotiation)
- [Phase 7 — PDF](#phase-7--pdf)
- [Phase 8 — Dossier](#phase-8--dossier)
- [Phase 9 — Close](#phase-9--close)

## Phase 3 — Inventory

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: AFTER Phase 1 (criteria locked) and Phase 2 (baseline market data pulled). BEFORE Phase 4 mass outreach.

**Purpose**: Produce a deduplicated, ranked candidate list across all major inventory sources so Phase 4 mass outreach is targeted at the top 30-50 VINs (or new-MY allocations), not the entire market.

### New-car vs used-car router gate (run BEFORE dispatch)

If `criteria.md` indicates NEW car (no mileage history, current MY, or buyer answer to Phase 1 vehicle target says "new"):

- **SKIP CARFAX-as-history-source.** A never-titled vehicle has no CARFAX worth reading. See gotcha V2 and `pdf_review_checklist.md`.
- **Require the Monroney window sticker PDF** and **dealer PDI (Pre-Delivery Inspection) checklist** instead.
- **Capture a Delivery Mode column per listing** — one of:
  - `in-stock` (dealer lot, 0-7 day delivery)
  - `in-transit` (allocation from port, 1-3 weeks)
  - `dealer-trade` (sister-store lot, 3-10 days, 1-2wk cross-state)
  - `factory-order` (8-16 weeks, last resort, blows tight timelines)
- **SKIP no-haggle chains and rental returns** (CarMax / Carvana / EchoPark / Enterprise / Hertz) — they do not stock new-MY OEM inventory.
- **Apply new-car miles bands as a sort modifier**:
  - 0-20 mi = normal delivery
  - 20-100 mi = test-drive only (flag for PDI confirm)
  - 100-500 mi = presumptive demo/loaner (confirm not previously titled)
  - >500 mi = presumptive-used-disguised-as-new (negotiate as used)

If USED car: keep the CARFAX-centric workflow below as-is.

### Dispatch parallel subagents, one per site

| Site | Notes |
|---|---|
| Carfax | Primary aggregator, best dedup, native "Send Email" works. **Used-only history; for new MY, treat Carfax as inventory listing source only, ignore history section.** |
| CarMax | No-haggle single chain. **SKIP for new-MY inventory.** |
| Carvana | Online-only, OTD returned directly. **SKIP for new-MY inventory.** |
| Cars.com / AutoTrader / Edmunds / TrueCar / CarGurus | Anti-bot 403s — use Playwright MCP |
| Enterprise / Hertz | Rental returns, no-haggle, 12mo/12k warranty. **SKIP for new-MY inventory.** |
| EchoPark | No-haggle chain. **SKIP for new-MY inventory.** |
| Toyota.com SmartPath / OEM-brand national inventory locators | **New-car only.** Native VIN-level Monroney PDF access, per-dealer SmartPath pages. |

Each subagent produces `report_<site>.md` with top-N candidates (VIN, miles, price, dealer, deal tags, link, **Delivery Mode for new cars**).

### After all subagents return

Generate `master_comparison.md` with TWO sections, in this order. This is the buyer-facing market-scan artifact shown in the README "Example output" (`examples/market_en.png` / `market_cn.png`).

#### Section 1 (top): Site Capability Matrix

One row per site dispatched, so the buyer sees at a glance which source to trust for what. Do NOT skip this section because it feels redundant with the candidate list — it is the part buyers reuse across the whole cycle to decide where to re-search and which quote to treat as an anchor. Fixed columns:

| Column | Content |
|---|---|
| Site | Site name (Carfax, CarGurus, Cars.com, ...) |
| Listings (radius) | Count this site's subagent returned inside the buyer's ZIP + radius (`0` if blocked / none) |
| Price posture | Relative to the Phase 2 baseline: `below-market` / `at-market` / `above-market` / `fixed-no-haggle` |
| Price tier | Typical deal quality this site surfaces for THIS search (e.g. "GREAT/GOOD deal flags", "MSRP-anchored", "rental-fleet flat") |
| Key differentiator | One line — pull from the per-site notes in the dispatch table above (best dedup / native email / anti-bot / OTD-direct / rental-warranty / OEM-Monroney) |
| Buyer role | One role tag from the taxonomy below |

**Buyer-role taxonomy** (this is the categorization the matrix exists to deliver):

| Role tag | Meaning | Default sites |
|---|---|---|
| `Primary #N` | Main search source — dispatch first, native email + best dedup; rank `#1`, `#2`... | Carfax (`#1` used), OEM SmartPath / national locator (`#1` new), CarGurus |
| `Secondary #N` | Supplementary supply behind the primaries | Cars.com, AutoTrader |
| `Negotiation lever` | No-haggle but returns a hard OTD number usable as a cross-bid anchor | Carvana |
| `Research-only` | Market-data / TMV reference, not an inventory source to email | Edmunds, TrueCar |
| `Plan B fallback` | Real inventory but no-haggle / fleet — use only if the primaries run thin | CarMax, EchoPark, Enterprise, Hertz |
| `Skip` | Excluded for this buyer type — always append the reason in parentheses | new-MY → CarMax / Carvana / EchoPark / Enterprise / Hertz per the router gate |

Role-assignment rules:

- Honor the **new-vs-used router gate** above first. For a NEW-MY search, the no-haggle / rental sites (CarMax, Carvana, EchoPark, Enterprise, Hertz) are `Skip (no new-MY inventory)` and OEM SmartPath / national locator becomes `Primary #1`.
- A site that returned **0 listings or was anti-bot-blocked** still gets a row — mark `Listings (radius) = 0` and either keep its role with a `(blocked, retry via Playwright)` note or downgrade to `Plan B fallback`. Never silently drop a dispatched site; the buyer needs to know it was checked.
- Rank the `Primary` / `Secondary` numbers by listings-in-radius x price posture, not by brand prestige.

#### Section 2 (bottom): VIN-deduplicated candidate list

Generate the candidate table deduplicated by VIN. See `references/outreach_strategy.md` for the column set + dedup + ranking logic (including the **New-Car ADM Detection and Filtering** section that fires on positive `Internet Price − MSRP` deltas — gotcha D9).

### Cross-references

- `references/outreach_strategy.md` — dedup + ranking + ADM detection
- `references/pdf_review_checklist.md` — V2 CARFAX requirement; new-car Monroney/PDI handling
- `references/vertical_playbooks.md#part-2--heavy--commercial--luxury` — luxury-specific inventory sources (ultra-luxury allocation-driven, route to brand specialist for exotics)
- `references/ev_buyer_playbook.md` — EV-specific inventory considerations (SoH for used EV, NACS vs CCS1 port)
- `references/vertical_playbooks.md#part-1--pickup-truck-specifics` — pickup-specific listing red flags (ex-plow, ex-fleet, factory tow package)
- Gotcha D9 (ADM kill list), V2 (CARFAX PDF requirement)

## Phase 4 — Outreach

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: AFTER Phase 3 has produced `master_comparison.md` with deduplicated top-N candidates. BEFORE Phase 5 cron monitoring begins.

**Purpose**: Get written OTD breakdowns (or written first responses) from the top 30-50 candidate dealers in parallel so cross-bid leverage is established by the time the cron starts collecting replies.

### Core mechanics

Submit lead forms or send direct emails to the top 30-50 candidates. Each outbound touch is sent in a 5-minute window so dealers feel parallel pressure (see `outreach_strategy.md` § parallel cross-bid).

### Capture per dealer

Per dealer row in `tracker.md`:

- Dealer name + address + phone
- Sales rep name (if known from listing or lead-form auto-assignment)
- VIN (used) or stock number + Delivery Mode (new — see Phase 3 detail)
- Submission timestamp (dealer-local time)
- Anti-bot result (lead form success / Carfax confirmation / direct-email-only fallback)
- Channel used (lead form / direct email / SMS / phone — see `outreach_strategy.md` § multi-channel)

Track in `tracker.md` using `assets/tracker_template.md` as the skeleton.

### Email format

Critical Rule #1 applies absolutely. Plain ASCII, no markdown, no em-dashes, no backticks. See `references/email_format_rules.md` for the ASCII substitution table.

Critical Rule #7 applies absolutely. Phase 4 emails may only cite REAL-tagged baseline rows from `.firecrawl/{model}-deal-baseline.md`. Synthesized / placeholder rows are for internal reasoning only. Never paste a synthesized Reddit anecdote, fabricated dealer number, or generic "buyers report X" into a dealer email.

### Email-type branching (mandatory before drafting)

See SKILL.md § Outbound Email SOP for the full first-touch / counter / follow-up branching table and 5-item pre-draft Y/N checklist.

### Send-window advisory

Recommend send between 9 AM and 5 PM Mon-Thu dealer-local time (see SKILL.md § Outbound Email SOP Step 5). Multi-state cross-bid: use the EARLIEST dealer-local 9 AM among the 4 dealers as the cohort send time.

### Dealer group ownership check (gotcha D11)

Before treating two dealer OTD quotes as "independent cross-bids", check the parent group. Phase 4 outreach should target 3-4 different parent groups in radius, not 3-4 stores from the same group. See gotcha D11 for the 10-parent-group roster.

### Cross-references

- `references/outreach_strategy.md` — multi-channel strategy (form / email / call / SMS), anti-bot handling, dedup
- `references/email_format_rules.md` — ASCII substitution table, draft hygiene
- `assets/tracker_template.md` — tracker skeleton
- `assets/dealer_reply_template.md` — first-touch + OTD ask templates
- SKILL.md § Outbound Email SOP — full step-by-step ordered procedure
- Gotchas E1-E5 (email + drafting hygiene), D5 (used/new mixing), D11 (dealer group), N1 (transparent anchor citation)

## Phase 5 — Cron

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: AFTER Phase 4 outreach is sent. RUNS CONCURRENTLY with Phase 6 negotiation and Phase 7 PDF analysis until the close.

**Purpose**: Catch dealer replies across all inbox surfaces (Primary / Promotions / Spam / overnight backlog) and draft responses without missing any thread.

### Three scheduled crons (not one)

Set up THREE scheduled CronCreate jobs. The 15-min main cron alone reliably misses spam, promotions, and overnight backlog — those three failure modes are mechanically closed by the two auxiliary sweeps.

#### 1. Main inbox cron — `*/15 * * * *` (every 15 minutes)

- Searches inbox tab for dealer replies in the past ~20 minutes
- Skips Carfax confirmations (`from:CARFAX@event.carfax.com`), templated marketing autoresponders, and OOO autoresponders
- For each real reply: read thread, draft response, save Gmail draft, log to tracker

#### 2. Spam + Promotions sweep — `0 */6 * * *` (every 6 hours)

- Runs `in:spam newer_than:24h` AND `category:promotions newer_than:24h` over the same dealer-name + make + OTD keyword set
- Catches CRM-template dealer mail that lands outside the Primary Inbox tab (eDealerHub / VinSolutions / eLead are recurring offenders)
- On match, advises buyer to apply Gmail "Not Spam" / "Move to Primary" rule and processes the reply normally

#### 3. Morning catch-up sweep — `0 7 * * *` (7 AM ET daily; adjust to buyer's stated wake time)

- Runs `newer_than:12h is:unread` over the full keyword set
- Recovers overnight backlog the 15-min main cron can't see because the Claude harness's CronCreate doesn't fire when the Claude session is closed
- Cross-references against tracker; any unread + important thread not yet logged is a backlog miss, processed immediately

### OOO autoresponder handling

When an Out-of-Office autoresponder is detected (keyword list in `references/cron_monitoring.md` § Out-of-Office subsection), the cron MUST NOT draft a reply. Instead:

- Flag the dealer's tracker row with the OOO detection timestamp + parsed return date (if present)
- Suppress all re-pings to that rep until the return date passes
- Drafting into an OOO inbox creates 3-7 days of stale negotiation drift

### Full reference

See `references/cron_monitoring.md` for:

- Full prompt templates and Gmail search patterns for all three crons
- 13-keyword OOO detection list + RFC 3834 `Auto-Submitted: auto-replied` header signal + 6-step OOO action protocol
- Skip keyword list (Carfax confirmations + templated marketing autoresponders)

Reply templates: `assets/dealer_reply_template.md`.

### Cross-references

- `references/cron_monitoring.md` — full prompt templates, search patterns, OOO detection
- `assets/dealer_reply_template.md` — reply templates (first-touch / counter / walk-away / OOO-safe)
- Gotchas I1-I5 (inbox + cron monitoring), H1-H2 (session hygiene)

## Phase 6 — Negotiation

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: AFTER Phase 5 cron has collected the first round of dealer replies with written numbers. RUNS CONCURRENTLY with Phase 5 (cron continues), Phase 7 (PDFs as they arrive), and the cross-bid escalation cadence in `negotiation_playbook.md`.

**Purpose**: Push the cross-bid field toward the buyer's walk-away ceiling using market-data anchors, internal-trim anchors, and competitor OTD citations.

### The ask format (always written, never verbal)

Critical Rule #3: Written OTD before any in-person visit. If a dealer refuses to send the full breakdown by email, decline the visit and pivot.

Required line items on every dealer OTD:

- Sales price
- State sales tax (NJ 6.625%, NY 8.875%, PA 6%; full state-by-state in `references/state_fees.md`)
- Doc fee (NJ legal cap $799; state-by-state caps in `state_fees.md`)
- Title + registration fees
- Add-ons (refuse paint protection / nitrogen / etching — see gotcha P3 close-day F&I hard-no script + `negotiation_playbook.md` § Add-On Refusal)

If any line item appears that does NOT exist in the buyer's REGISTERING state (gotcha D8), demand a full re-quote — not just deletion of the leaking line.

### Anchoring techniques

- **Internal anchor**: compare dealer's own concurrent inventory (e.g., base trim $25k → Limited should not be $5k over; fair spread is $2-3k trim + $1-1.5k mileage)
- **Market-comp anchor**: cite CarGurus "Good Deal" thresholds, Edmunds TMV, recent Reddit/XHS reports (REAL-tagged only per Critical Rule #7)
- **Cross-dealer anchor**: once 2+ written OTDs exist, cite by dollar amount in counters (see gotcha N1 — "My locked benchmarks are X at $X,XXX and Y at $X,XXX")

### ADM kill list (gotcha D9)

When a dealer quote contains any Additional Dealer Markup line on NEW MY inventory, the FIRST counter must demand removal as a precondition, not propose a counter-amount or middle-meet. ADM is dealer-side margin theater dressed as a fee. See gotcha D9 for full kill list + paste-ready email language + three rules (do not couple with other concessions; one ask one round; cross-state-net stays a Phase 3 decision).

### Escalation when dealer delays ("let me check with my manager")

See `references/negotiation_playbook.md` § Escalation Ladder When Dealer Delays — T+24h polite reminder, T+48h firm walk-away signal citing locked competitor anchor, T+72h silent walk-away with tracker COLD-log entry. 4 special cases: OOO autoresponder mid-cycle, opening-move "let me check" on same-day reply (not a delay yet), buyer-side timeline compression, multi-rep parallel push.

### Bait-and-switch protocol (gotcha D10)

When a dealer claims the original VIN-X is "just sold" and pivots to VIN-Y at higher price / more miles / with ADM, treat as bait-and-switch by default. Required defenses: proof-of-sale ask, same-or-better OTD on substitute, pause and re-anchor as a NEW dealer engagement. See gotcha D10.

### Buyer-type specific Phase 6 notes

- **Financing buyer**: binding-constraint OTD computed at Phase 1 (cash_down + financed_cap_from_monthly). Re-verify at every Phase 6 counter that effective OTD cap still holds against the proposed counter. See `references/payment_methods.md` § financing.
- **Lease buyer**: anchor on Money Factor markup buy-rate, not OTD — see `references/lease_playbook.md` § MF markup + paste-ready buy-rate counter language.
- **Trade buyer**: SEPARATE the trade negotiation from the new-car negotiation (gotcha — see `references/trade_in.md` § 8 separate-the-negotiation). Lock new-car OTD first, then evaluate trade allowance independently against KBB Instant Cash Offer.
- **EV buyer**: federal $7,500 credit (POS transfer or tax filing) and § 45W lease pass-through enter the math. See `references/ev_buyer_playbook.md` § 1 and `references/lease_playbook.md` § 8.
- **Pickup buyer**: verify factory tow package via VIN decode before Phase 6 OTD lock — see `references/vertical_playbooks.md#part-1--pickup-truck-specifics` § 7.
- **Heavy-duty / commercial / luxury**: see `references/vertical_playbooks.md#part-2--heavy--commercial--luxury` § 3 luxury pricing dynamics (sticker rarely budges MSRP - 4-7% on volume; lease incentives MORE aggressive).
- **CPO buyer**: embedded value calculation per brand — see Subaru/Honda/Toyota/Hyundai/Kia/Ford/GM/Mazda CPO references.

### Cross-references

- `references/negotiation_playbook.md` — full math, walk-away lines, cash leverage, Escalation Ladder, Sequential Dealer Pricing Disclosure
- `references/state_fees.md` — all-state tax/doc/reg detail + cross-state titling + gotcha D8 "Does NOT have" leak lists
- `references/payment_methods.md` — Captive-vs-credit-union rebate playbook, financing decision matrix
- `references/lease_playbook.md` — lease-specific Phase 6 framework (MF buy-rate counter, captive markup ceilings, EV § 45W)
- `references/trade_in.md` § 4 + § 8 — separate-the-negotiation, lien payoff workflow
- `assets/dealer_reply_template.md` — counter / walk-away / add-on refusal / ADM removal templates
- Gotchas D5 (used/new mixing), D8 (state-template leak), D9 (ADM kill list), D10 (bait-and-switch), D11 (dealer group), N1 (transparent anchors), N2 (parallel drop-X asks), P3 (close-day F&I hard-no)

## Phase 7 — PDF

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: WHENEVER a dealer attaches a PDF (CARFAX, service records, OTD proposal, PPI report). RUNS CONCURRENTLY with Phase 5 cron and Phase 6 negotiation.

**Purpose**: Mechanically scan dealer-attached PDFs for the data dealers commonly hide in PDF form (full OTD breakdown, full accident history, full service-record gaps), which is intentionally harder to grep than inline email text.

### Core extraction targets

For every dealer-attached PDF, open with Read tool and extract:

- VIN match (does the PDF VIN match the listing VIN?)
- Owner count
- Accident / damage / structural / odometer issues
- Service record completeness (CVT fluid at 60k, spark plugs, coolant, brakes)
- Active recalls

### Full reference

See `references/pdf_review_checklist.md` for:

- 4 PDF types covered (CARFAX, service records, OTD proposal, PPI report — PPI partial)
- OTD Proposal Add-On Anti-Pattern Detection (12-line F&I add-on kill list + Protection Package bundle detection + math-check + paste-ready buyer challenge language)
- CARFAX Accident Detail Extraction Template (7-field structured: date / severity / impact zones / repair facility / photos / structural flag / airbag flag / post-accident inspection)
- ADAS recal by-brand table (10 brands, Subaru EyeSight / Honda Sensing / Toyota Safety Sense / Hyundai SmartSense / Ford Co-Pilot360 / GM Driver Assistance + SuperCruise / Mazda i-Activsense / Nissan ProPILOT / Tesla Autopilot/FSD / VW Audi Travel Assist) with recal costs $250-$1,500
- Service Record Gap Detection — Per-Brand Expected Service Table (Subaru / Toyota / Honda / Ford / Mazda) with 30k/60k/90k/120k expected services + cost-if-missed + per-brand red flags

### Cross-references

- `references/pdf_review_checklist.md` — full PDF review checklist (all 4 PDF types)
- `references/negotiation_playbook.md` — using PDF findings as Phase 6 negotiation lever (inherited-cost quantification)
- Gotchas V1 (CARFAX 1-owner necessary but not sufficient), V2 (require dealer-provided full CARFAX PDF or live URL, not verbal), D7 (proposal.pdf hides OTD numbers)
- Critical Rule #4 (Read the actual CARFAX PDF/URL yourself)

## Phase 8 — Dossier

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: AFTER Phase 6 has narrowed to 2-4 final candidates with locked OTDs. BEFORE Phase 9 test drive + close.

**Purpose**: Produce a 7-10 page HTML+PDF dossier that the buyer brings to the dealer if helpful — comparison tables, OTD ladders, candidate side-by-side, walk-away ceilings, decision matrix. The buyer reads it before going on-site so the in-person visit is verification-only, not analysis.

### Generation pipeline

```bash
cp assets/dossier_config_template.yaml my_dossier.yaml
$EDITOR my_dossier.yaml
python scripts/generate_dossier.py --config my_dossier.yaml \
  --output my_dossier.html --to-pdf my_dossier.pdf
```

For Chinese-speaking dealers / Chinese-speaking buyer: `--template assets/dossier_template_cn.html`.

### Required config fields (load-bearing)

The `generate_dossier.py` script validates these fields and fails fast if any are missing or `{{KEY}}` placeholders remain unresolved:

- `BUYER_ADDRESS` — buyer city + state for tax/registration display
- `DATE` — dossier generation date
- `YEAR` / `MAKE_MODEL` — vehicle identity block
- `TARGET_OTD` — buyer's target OTD (load-bearing for ladder display)
- `STATE` / `TAX_RATE` — registering-state context for OTD breakdown
- `>=2 COMP_VEH` rows — at minimum two comparison candidates (single-candidate dossier is structurally weak)

Use `--allow-missing` to opt out of strict validation (back-compat only).

### Template architecture

- `assets/dossier_template.html` — English template (default)
- `assets/dossier_template_cn.html` — Chinese template
- `assets/dossier_config_template.yaml` — 84-placeholder skeleton (83 in CN due to one EN-only field)

Placeholders are documented inline in `assets/dossier_config_template.yaml`.

### PDF rendering chain

`generate_dossier.py` auto-detects Chromium-family browsers (Chrome / Edge / Brave / Vivaldi / Chromium) across Windows system + user + x86 paths + Linux flatpak + macOS user-Applications. Falls back to `CHROME_BIN` env variable. Final fallback: wkhtmltopdf. If none found, emits diagnostic error listing every probed path.

### Worked example

`<working-dir>/skill-test/p0_p5_execution/sample_dossier.yaml` / `.html` / `.pdf` (EN) + `sample_dossier_cn.html` / `.pdf` (CN) demonstrate the full pipeline end-to-end on the CT Outback example.

### Cross-references

- `assets/dossier_template.html` / `dossier_template_cn.html` — print-ready 8-page templates
- `assets/dossier_config_template.yaml` — placeholder skeleton
- `scripts/generate_dossier.py` — generator with Chromium auto-detect, field validator, placeholder validator
- `scripts/html_to_pdf.sh` — Chrome headless HTML to PDF (lower-level helper)

## Phase 9 — Close

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

**When this runs**: AFTER Phase 8 dossier produced + buyer reviewed. THIS IS THE FINAL PHASE.

**Purpose**: Execute the locked OTD with no slippage. Close-day F&I office is the highest-frequency point of last-minute margin recovery; the buyer needs a hard script (see gotcha P3) and a sub-checklist matched to their buyer type.

### Private prep file

Maintain a PRIVATE `{dealer}_negotiation_prep.md` (buyer-only, NEVER shared with dealer) with:

- Dynamic OTD ladder (stretch / realistic / walk-away)
- Test-drive checklist (cold start, CVT smoothness, brake feel, panel alignment)
- Post-drive questions (battery test, lien release, 2 key fobs, plate decision)
- Decision matrix (drive result x dealer response -> action)

### Close-day re-confirmation (from Phase 1)

At Phase 9 close-day kickoff, the agent's FIRST action is to re-read the close-day logistics mini-table from `criteria.md` and confirm each line with the buyer:

- Bank cut-off + branch + hours
- Insurance carrier (for binder)
- Plate decision
- Available time windows on close day
- ID set
- Captive vs CU vs cash funding instrument (if not pure cash)

Any change since P1 (carrier switched, branch closed for holiday, plate decision flipped) cascades into close-day execution and must be caught BEFORE the buyer drives to the dealer.

### Close-day routing by buyer type

The close checklist branches by buyer type. Use the relevant sub-checklist below; if multiple branches apply (e.g., financing + trade + pickup), execute all of them.

#### Cash buyer close-day sub-checklist

- [ ] Cashier's check ready by bank cut-off (~9-10 AM); buffer for same-day issuance
- [ ] OTD breakdown in writing matches counter-locked numbers (no shell-game per `trade_in.md` § 8 if trade also present)
- [ ] All line items verified against `state_fees.md` registering-state "Does NOT have" list (per gotcha D8)
- [ ] Sale price + doc + tax + title + reg verified; no padded add-ons (paint protection / nitrogen / etching)
- [ ] PPI complete (mobile inspector preferred — `references/ppi_booking.md`)
- [ ] Insurance binder issued before drive-off
- [ ] Plate transfer vs new-plate decision made (saves $25-150 in most states)
- [ ] Temp permit issued at close; permanent title in mail 4-8 weeks

#### Financing buyer close-day sub-checklist

- [ ] Captive-vs-CU question resolved per `references/payment_methods.md` Captive-vs-CU comparator (D9 sub-rule: not coupled to ADM or other concessions)
- [ ] If CU (any credit union): funding instrument (cashier's check or wire) confirmed pre-close; first-payment date confirmed
- [ ] If captive (TFS/Ford Credit/Honda Financial/HMF/etc.): no rebate clawback on early payoff; lender lien notation on title; first payment due ~30-45 days post-funding
- [ ] Pre-approval re-pulled if approaching 30-day expiry
- [ ] Down payment instrument confirmed (cash, debit, or cashier's check)
- [ ] Monthly payment math verified at close matches the binding-constraint formula
- [ ] If credit-union loan: title issued to buyer with CU lien notation; CU receives title via mail
- [ ] If captive: title typically goes to captive direct; buyer's name on registration

#### Trade-in buyer close-day sub-checklist

- [ ] Cross-ref `references/trade_in.md` § 4a-4d (lien payoff workflow) if active lien
- [ ] If lien: 10-day payoff letter from lien-holder in hand (NOT dealer's quote)
- [ ] Lien-holder auto-pay cancelled pre-close (avoid double-charge cycles)
- [ ] Bill-of-sale shows: trade allowance, lien payoff routing, dealer commitment date
- [ ] KBB Instant Cash Offer screenshot brought as walk-floor anchor
- [ ] Key count verified (matches Phase 1 capture)
- [ ] State trade-in tax credit applied to gross trade allowance (NOT net of payoff) per `state_fees.md` registering state
- [ ] Calendar reminder set: Day 5, Day 10, Day 14, Day 21 post-close monitoring (lien release confirmation)

#### EV buyer close-day sub-checklist

- [ ] POS credit transfer at signing if eligible: dealer is IRS Energy Credits Online registered (verify); Form 8936 signed; $7,500 reduction shown as separate line item per `references/ev_buyer_playbook.md` § 1
- [ ] Time of Sale report copy retained (required at tax filing)
- [ ] Battery warranty registered to buyer at delivery (new EV) OR SoH report obtained (used EV) per `ev_buyer_playbook.md` § 6
- [ ] NACS vs CCS1 port confirmed; adapter present if CCS1 vehicle
- [ ] L1 OEM charge cable included (factory accessory)
- [ ] No EV Prep / Battery Conditioning / Charge Cable / EV Delivery Setup ADM line items per gotcha D9 + `outreach_strategy.md` § New-Car ADM Detection
- [ ] Home L2 install scheduled (Qmerit/Treehouse/ChargePoint) if not already

#### Pickup-truck buyer close-day sub-checklist

- [ ] Factory tow package verified at delivery via VIN decode + door-jamb option codes (Ford 53A/535, Ram AHT, GM NHT)
- [ ] Real tow capacity matches buyer's stated use case (engine x axle x package per `vertical_playbooks.md#part-1--pickup-truck-specifics` § 1)
- [ ] Payload capacity NOT exceeded by buyer's actual use (tongue + passenger + gear math per § 3)
- [ ] Factory vs aftermarket hitch distinction confirmed
- [ ] Integrated trailer brake controller functional test (dash-mounted gain knob; green LED on 7-pin connect)
- [ ] PPI included pickup-specific items: frame inspection, transmission cooler, hitch wear, body mounts, exhaust manifold (V8 specifically), turbo seals (EcoBoost)
- [ ] No ex-plow / ex-fleet posture concealed (CARFAX commercial fleet = $1-2k off; plow prep = $1.5-3k off)
- [ ] Lift kit / oversized tires inspected for warranty + insurance impact (see `vertical_playbooks.md#part-1--pickup-truck-specifics` § 6)

#### Universal close-day cross-references

- `references/trade_in.md` § 4 + § 11 for trade documentation
- `references/vertical_playbooks.md#part-1--pickup-truck-specifics` § 7 for pickup-specific Phase 6/9 items
- `references/ev_buyer_playbook.md` § 9-10 for EV-specific items
- `references/subaru_cpo_program.md` / `references/honda_cpo_program.md` / `references/toyota_cpo_program.md` / `references/hyundai_cpo_program.md` / `references/kia_cpo_program.md` / `references/ford_bluecert_program.md` / `references/gm_cpo_program.md` / `references/mazda_cpo_program.md` for CPO enrollment at close
- `references/ppi_booking.md` for mobile PPI parallel-booking
- `references/state_fees.md` registering-state stub for fee verification
- `references/payment_methods.md` for financing close-day instruments
- `references/vertical_playbooks.md#part-2--heavy--commercial--luxury` § 6 close-day routing matrix (HD pickup / commercial van / luxury loan-cash / luxury lease / ultra-luxury)
- `references/lease_playbook.md` § Lease-end options (return / buy out / pull-ahead / extension) for lease-end timing

### F&I close-day hard-no

Gotcha P3 is mandatory reading at Phase 9. F&I add-ons are the highest-frequency margin-recovery surface — GAP / VSC / tire-and-wheel / paint / fabric / key / nitrogen / dent / ding can add $3-7k if buyer doesn't say no. Paste-ready hard-no script in SKILL.md gotcha P3 + `assets/dealer_reply_template.md` § Close-Day F&I Hard-No.
