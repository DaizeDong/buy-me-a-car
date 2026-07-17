# Multi-Site Dealer Outreach Strategy

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

## Site-by-Site Submission Methods

### High-Success (Direct Email or Native Form)

**Carfax**, Best for first-pass volume. The "Send Email" button on each listing opens a form that submits directly to the dealer with the buyer's contact info. The default Carfax message is generic ("I'm interested in this vehicle"). To include OTD ask in the initial inquiry, type a custom message before submitting. Carfax sends a confirmation email per submission to the buyer.

**Enterprise Car Sales**, Native lead form submits cleanly. Enterprise emails are typically a no-haggle OTD directly in the first response. Their structure: sales price + 6.625% NJ tax + $250 DMV flat = OTD.

**Direct dealer websites**, Most NJ Subaru / Honda / Toyota dealers have an "Email this vehicle" or "Get e-Price" form. Works without anti-bot interference.

### Anti-Bot Blocked Sites (Require Browser MCP or Manual)

The following return 403 to direct fetches and require playwright MCP or manual browser submission:

- CarGurus
- Cars.com (URL paths do not accept direct VIN)
- AutoTrader (search-only URLs)
- Edmunds
- TrueCar (regional averages only, not specific listings)

For these, use the playwright MCP tool to drive a real browser session: navigate to the listing detail page, locate the contact form, fill it, submit. Capture the confirmation page screenshot.

### Online-Retailer (No Dealer Email)

Carvana, Vroom, Shift, purely online retailers. No dealer email exists. Their price IS the OTD basis. Compare directly without email outreach.

## Multi-Channel Coordination

A single inquiry typically generates dealer responses across 3 channels:

1. **Email**, Primary. Best for OTD breakdown, written records, PDF attachments (CARFAX, quotes, service records).
2. **SMS**, Often a duplicate of the email message. May come from a different number than the rep's office line. Skip unless email channel is silent.
3. **Phone call**, Dealers prefer this for "come in and discuss." Let calls go to voicemail. Reply via email saying "I do all evaluation in writing, please email."

Centralize dialog in email. SMS and phone calls without email follow-up should be reverse-channeled back to email.

## Submission Deduplication

For a 30-50 candidate batch, deduplicate by VIN before submitting. Some listings appear on multiple sites (a single car listed on Carfax + AutoTrader + CarGurus). One submission per VIN is sufficient.

If two different dealers have the same VIN listed (rare but happens via inventory feeds), submit to both. The responsive one wins.

## Mandatory Format for All Outbound Emails

Every outbound dealer email, including the initial inquiry sent via lead form custom message field, must use plain ASCII only:

- No em-dash (the long dash, U+2014)
- No en-dash (U+2013)
- No markdown bold or italic markers (no double-asterisks, no underscores around words)
- No backticks for code or values
- No `[text](url)` link syntax (write the URL plain)
- No curly quotes; use straight quotes

Replace any em-dash with one of: comma, colon, period and new sentence, or ASCII hyphen-minus. Most dealers use eDealerHub or VinSolutions CRMs that render these characters literally and degrade the buyer's professional appearance.

See `references/email_format_rules.md` for the full substitution table.

## Submission Tracking

Per submission, capture in `tracker.md`:

- Date and time of submission
- Site used (Carfax / direct dealer / manual)
- Dealer name + address + phone
- VIN
- Asking price at time of submission
- Lead form confirmation (yes / no)
- Anti-bot result (success / blocked / 403)

This forms the audit trail for which dealers responded vs not. After 24-48 hours, dealers who have not replied are dropped from active monitoring.

## Subagent Dispatch (Phase 3 Inventory)

For each site, dispatch one subagent in parallel with a prompt like:

> Search Carfax for {Year-Range} {Make} {Model} {Trim} within {Radius} of {ZIP}, max {Mileage} mi, budget {OTD Max}. Return top 15 candidates with VIN, miles, asking price, dealer name, dealer location, deal rating, direct listing URL. Save output to `report_carfax.md`. Note any listings flagged "Great Deal" or "Good Price" at the top.

Run all subagents in a single message (parallel), they are independent and gain ~5-10x wall clock improvement from concurrency.

**Scraping method + pagination (mandatory read):** these inventory SRPs return 403/DataDome/Akamai to headless `WebFetch` for every site except CarGurus, use **Playwright-first** fallback and **paginate to exhaustion** (loop-until-dry), not page-1-only. The full per-site extraction recipe (JSON-LD / embedded state / DOM+VIN-regex) and pagination method (URL param vs in-app click vs infinite scroll, plus anti-bot pacing) live in `phases.md#phase-3--inventory`. Do not re-derive here.

After subagents return, merge their outputs into `master_comparison.md`. The file has two sections: a **Site Capability Matrix** on top (one role-tagged row per site, see `phases.md#phase-3--inventory` for the fixed columns + role taxonomy) and, below it, the **VIN-deduplicated candidate list** with columns: site, year/trim, miles, price, dealer, location, deal-rating, VIN, URL, notes.

## Identifying Top Candidates

Rank candidates by composite score:

1. **Price competitiveness** (most weight): below regional average is good; "Great Deal" on CarGurus is very good
2. **Mileage** (heavy): under buyer's cap is mandatory; lower is better
3. **Trim match** (medium): exact match preferred; one-up trim acceptable
4. **Distance** (medium): under 20 mi local preferred for service relationship
5. **CARFAX deal indicators** (light): "Hot Car" or recently price-dropped
6. **Dealer reputation** (light): brand-direct preferred over independent multi-brand

Pull top 30-50 by combined score for outreach phase.

## New-Car ADM Detection and Filtering

For NEW-MY listings, compute a derived column `ADM_delta = Internet_Price − MSRP` per candidate. The Phase 3 inventory pull MUST surface this delta before ranking; agents have repeatedly missed ADM in past runs by treating Internet Price as the comparable.

**Auto-flag a listing as ADM-present when ANY of the following fire:**

- `ADM_delta > 0` (Internet Price exceeds MSRP, regardless of line-item naming)
- Listing copy / itemized quote contains any of the four common ADM line names:
  - **Market Adjustment** (most common; also "Hybrid Market Adjustment", "EV Market Adjustment")
  - **Hybrid Premium** / **Hybrid Adjustment** / **Toyota Premium**
  - **Dealer Markup** / **Dealer Adjustment**
  - **Allocation Fee** / **Allocation Premium** / **Protection Plus** (when bundled with MSRP-overage)
- Free-text listing fields mention "ADM", "ADP" (additional dealer profit), "MAP override", or "above MSRP"

**Ranking rule:** ADM-flagged listings are **Tier 3 by default**, held back from first-touch outreach unless the buyer's preferred trim+color is otherwise scarce in radius (<3 MSRP-clean alternatives). In Phase 4 outreach, the first-touch email to a Tier-3 ADM dealer MUST open with "remove the [exact ADM line name] line and re-quote at MSRP", do not negotiate around ADM, demand removal. If dealer refuses ADM removal in their reply, mark dead and reroute to next-best candidate. ADM listings may be promoted to Tier 2 IF (a) preferred-trim scarcity is binding AND (b) post-ADM-removal net would still land under the walk-away OTD.

**Cross-state ADM nuance:** A DE / NH / OR (no-tax) dealer with $1,500 ADM can still net below a PA / NY MSRP-clean offer because the structural tax advantage dominates. Compute net OTD with state_fees.md cross-state rows BEFORE applying the Tier-3 rule. The Tier-3 default holds, but the per-listing OTD math is what actually decides outreach order.

**Heads-up to buyer:** When ADM is detected on 2+ listings in the radius, surface in Phase 3 output: *"X of N listings carry $A-$B ADM under names [list]. Phase 6 first ask on each: removal. If dealer holds, walk to MSRP-clean alternative."* This is the Phase-3 mechanical complement to the Phase-1 ADM heads-up.

## Common Pitfalls

- **Listing already sold but still showing online.** Always confirm availability in first dealer reply before deep negotiation.
- **VIN typo on aggregator.** When dealer responds with a different VIN, that is the truth. Update tracker.
- **"Internet price" vs "Sale price" confusion.** Some dealers list lower "internet price" requiring email/form submission to "unlock." Same OTD, just gating.
- **Doc fee buried in subtotal.** Always ask dealers to itemize: sales price, tax, doc fee, title, registration, add-ons.
