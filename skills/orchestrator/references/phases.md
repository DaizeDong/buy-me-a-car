# Phase references

Begin in a verified private cycle directory. All capture paths in these phases
refer to that directory. The source repository contains only the tool and
generated synthetic fixtures.

## Phase 3: Inventory

Run independent site research in parallel when tools permit, assigning one owner
per source and separate output paths. Browser sessions must be isolated; do not
drive the same page from concurrent workers. Host-specific browser authentication
and export rules apply. An HTTP 200 response, visible page title or count of VIN
strings alone does not prove successful extraction.

For each site, save the query/filter URL, requested filters, observation time,
pages attempted, pages retrieved, visible total if present, pagination stop
reason and raw artifact. Report `complete`, `partial`, `blocked` or
`unavailable` with an explicit reason.

Extract each vehicle as one connected record from a listing card, JSON-LD object
or detail page: VIN/stock ID, year/make/model/trim, new/used class, mileage, asking
price, dealer, location, listing URL and conditional pricing. Never join separate
global arrays of prices and VINs by position. Preserve missing fields as unknown;
do not infer an all-in price from an advertised price.

The read-only browser snippet `scripts/extract_inventory.js` extracts connected Cars.com cards and generic vehicle JSON-LD. Run it through the host browser code tool with the script filename, then store its returned payload under verified private DATA. It explicitly reports one-page partial coverage and missing fields. Other DOM layouts need an adapter; zero records is not success.

Paginate until the site signals the end, a verified duplicate page occurs, or a
documented budget/block stops the run. Retain the coverage boundary. Open detail
pages for shortlisted candidates to verify identity and availability. Deduplicate
by normalized VIN while retaining multiple sources and conflicting dealer/price
claims. Missing VIN records remain separate candidates, not guessed duplicates.

Return a source coverage table followed by the candidate table. Keep new, used,
CPO, private-seller and lease offers distinguishable. Read
[deal sources](deal_data_sources.md) for evidence classes.

## Phase 4: Outreach

Read [outreach strategy](outreach_strategy.md) and
[email SOP](outbound_email_sop.md). Choose recipients only from verified seller
contacts. Record group ownership so two stores in one group are not described as
independent competition. Do not submit multiple forms for the same vehicle to
compensate for an uncertain response. A private seller follows
[private-party steps](private_party_playbook.md).

Prepare exact recipients, text and attachments. A research request alone does
not authorize sending or lead-form submission. When authorized, preserve the
provider response and confirmation. A local draft or button click alone is not
proof of delivery.

## Phase 5: Cron

Use [durable monitoring](cron_monitoring.md). The shipped inbox ledger supports
account-bound imports, stable message IDs, cursor continuity, classification,
draft operation preparation and receipts. It does not install a Gmail connector
or operating-system scheduler.

If a scheduler is available and authorized, configure timezone, main inbox,
Spam/Promotions and startup catch-up coverage. Test a real tick and a restart.
State clearly when monitoring runs only while the current session is open.
OOO detection suppresses automatic reply without discarding useful quote content.

## Phase 6: Negotiation

Use [dealer-reply-drafter](../../dealer-reply-drafter/SKILL.md) and
[negotiation playbook](negotiation_playbook.md). Preserve sale, tax, doc, title,
registration, add-ons, rebates, finance conditions, trade and payoff as separate
lines. Confirm comparable class, registration location and conditions before
using a competing quote.

The buyer's internal maximum never becomes a counteroffer automatically.
The constrained renderer selects approved ask and evidence IDs and an explicitly
authorized outward offer. Draft validation and external operation receipts are
separate gates.

## Phase 7: PDF

Read [PDF checklist](pdf_review_checklist.md). Extract all pages and tables from
quotes, vehicle history, service records, CPO and inspection reports. Mark OCR or
missing-page limitations. Recompute financial totals, verify VIN and dates, and
distinguish absent evidence from evidence of no issue. A vehicle history report
cannot replace an independent mechanical inspection.

## Phase 8: Dossier

Follow [dossier-builder](../../dossier-builder/SKILL.md) for the current schema
and CLI. Do not maintain a second field list here. Live mode requires private
input/output, complete written quotes, evidence artifacts and consistent amounts.
Demo mode accepts exact generated fixtures only.

Review every PDF page after generation, including tables, headers, long text and
sources. Report actual page count and language. No fixed page count is promised.
Keep private limits and internal negotiation notes out of the dealer document.

## Phase 9: Close

Use [close-day checklist](../../close-day-checklist/SKILL.md) and the confirmed
private criteria revision. Reconfirm VIN, availability, inspection result,
written OTD, lender terms, title/lien process, insurance and payment logistics.

Review the final buyer's order and finance/lease contract line by line. Resolve
added charges or changed terms before signing. For an inspection issue, record
the finding and repair evidence; the buyer chooses proceed, counter or walk.
Bookings, deposits, signatures and payments require the corresponding explicit
authorization and a receipt. Finish with private feedback and archive the final
evidence in the companion.
