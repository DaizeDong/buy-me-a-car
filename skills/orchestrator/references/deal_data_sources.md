# Deal sources and evidence

Source availability changes by location, browser session and time. Try the
current page, inspect the returned content, and record what was recovered.
Historical success does not establish present coverage, and a browser is not a
guaranteed solution to a blocked site.

## What a source can establish

| Source | Useful evidence | Boundary |
|---|---|---|
| Manufacturer | MSRP, current incentive terms, program dates, CPO/warranty terms | Check exact trim, ZIP, acquisition date and eligibility |
| Registering-state DMV/revenue authority | Tax mechanism, fees, exemptions and effective dates | Verify local/vehicle/transaction applicability |
| Dealer listing/detail page | Advertised vehicle, price, location and conditions | Availability and all-in OTD still need confirmation |
| Written dealer quote | Itemized offer for a vehicle and registration location | Preserve expiry, financing/trade conditions and source |
| Inventory aggregator | Candidate discovery and cross-source comparison | Syndicated records can be delayed or duplicated |
| Valuation guide | Its dated methodology and estimate | It is not a binding offer or verified transaction |
| Owner forum/social post | A self-reported experience or lead | Never call it a verified quote or copy private buyer data |
| Archived page | What a source said on the archive date | It is not a current incentive or market price |

## Capture contract

Before saving any page, screenshot or extracted record, resolve private DATA
with `tools/runtime_paths.py` and work in the private cycle directory.
Record source URL/provenance, query filters, observation date/time, original
artifact, hash, extraction method, and missing fields. Keep raw and interpreted
records separate so a later reviewer can inspect the original.

For market comparisons, retain model year, trim, new/used/CPO class, mileage,
registration jurisdiction, price basis and conditions. Never label an asking
price or a synthesized estimate as a written OTD. Do not invent mileage rates
or tax assumptions to force unrelated offers into one table.

## Collection procedure

1. Check current manufacturer and official jurisdiction sources.
2. Search multiple inventory sources for the buyer's actual filters.
3. Extract linked records and pagination coverage using the
   [inventory procedure](phases.md#phase-3-inventory).
4. Confirm shortlisted vehicles on seller detail pages and obtain written quotes
   only through authorized contact.
5. Recheck price, availability and incentive expiry before citing an anchor.

Use available search/scrape tools for public pages and a real isolated browser
when rendering is needed. Inspect tool help instead of assuming an old CLI flag
still exists. If a page is blocked, login-gated, empty or throws an application
error, record that state; offer another source or an authorized manual import.
Never classify the source as complete just because navigation returned 200.

## Browser state

Follow the host's actual isolation and authentication policy. For a host using
a shared storage-state seed, launch an isolated context from the full union.
After use, export the entire context, including IndexedDB, to a unique incoming
file and invoke the host's merge/absorb entrypoint before closing. Never replace
the shared union with one session's partial state. Keep bearer credentials out
of both the public tool and the private purchase evidence repository.

## Research output

Return a coverage table, deduplicated candidates, dated current incentives,
evidence-backed comparisons and unresolved questions. Cite the original source
for every material numeric claim. Store private source artifacts with the cycle.
Do not publish actual inventory choices, buyer negotiations or source-account
details in examples or a changelog.
