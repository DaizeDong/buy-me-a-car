# Deliver a useful buying report without extra prompting

Broad vehicle-selection requests include a buyer research packet. The user need
not say "make it detailed", "compare candidates" or "generate a PDF" separately.
Use the current private cycle and keep the same artifact paths when updating it.

## Progress from one request

1. Reuse known preferences. Group material missing inputs once, separating facts,
   buyer-authorized assumptions and unknowns. Research what does not depend on
   the answer instead of restarting intake or inventing preferences.
   Carry prior approval context into every delegated task. An assumption the
   buyer authorized for this report remains an assumption, but is no longer an
   unanswered intake question. Do not put reconfirming that scenario in the
   report's narrative or next-action checklist. Separate unresolved vehicle,
   price, tax or logistics evidence from settled scenario inputs.
2. Research appropriate local, regional and remote sources. Record each query,
   observed date, pages examined, access blocks and coverage limits. Search result
   snippets locate evidence; read the actual listing or official page before
   describing a specific price, configuration or rule as verified.
3. Preserve listing records and source artifacts in private DATA. Deduplicate
   known VINs while preserving multiple seller/platform records and disagreements.
   Unidentified vehicles remain distinct provisional records. Never treat a
   site's global result count as the number of vehicles actually examined.
4. Build `master_comparison.md` and the research config from those records. Use
   [dossier-builder](../../dossier-builder/SKILL.md) to render
   `buyer_research.html` and `buyer_research.pdf`. Do this during initial
   selection, without waiting for competing written OTD quotes.
5. Inspect the rendered report, revise content or layout defects, then deliver
   clickable artifacts with the decision, strongest alternatives, important
   unknowns and next action. Preserve research receipts separately from the
   buyer-facing report. Implementation logs are not the report itself.

## Substance required

Use as much space as the evidence requires; page count alone is not quality.
Each applicable topic needs evidence, a decision implication or a specific
unresolved question. Empty headings and generic advice do not satisfy it.

| Topic | What the buyer should learn |
|---|---|
| Requirements | Confirmed needs, explicit assumptions, private budget basis and material unknowns |
| Coverage | Which markets/sites were examined and how incomplete access limits the result |
| Vehicle alternatives | Why a class, model, powertrain or configuration fits the actual use |
| Candidate inventory | Identity, asking price, mileage/configuration, location, source and status |
| Price and delivered cost | Comparable price basis, included charges, missing costs and conditional affordability |
| Suitability | VIN/configuration evidence needed; pickup payload/tow limits or EV route/charging needs |
| Local logistics | Weather, service access, transport route, inspection and delivery constraints |
| Ownership risks | Warranty/CPO/title/recall/inspection evidence and unresolved ownership costs |
| Shortlist | Ordered next candidates with reasons, rejection reasons and what would change the decision |
| Next actions | A prioritized buyer checklist, evidence requests and choices requiring authorization |
| Sources | Clickable provenance, observation dates, coverage and uncertainty labels |

Compare only comparable records. Separate asking price, quoted OTD, proposed
offer, known-cost subtotal and the buyer's final delivered cost. Missing tax,
shipping or inspection costs remain unknown; do not substitute zero or label a
subtotal as affordable. Explain conditional ranking instead of inventing price
adjustments, savings or a numerical score unsupported by the data.

## Appropriate progress with gaps

- No written quotes: deliver listings-based research and a quote request plan.
- One candidate: explain the narrow coverage; compare configuration alternatives
  and describe the next search, without manufacturing competitors.
- No accessible inventory: deliver a clearly partial report with the actual
  sources attempted, useful official guidance and the specific access gap.
- Missing locality or budget: keep those criteria unknown. Present conditional
  choices and defer location-dependent totals or affordability conclusions.
- Missing PDF renderer: deliver the HTML and comparison with a specific PDF
  failure status. Fix or install the dependency within authorized scope; do not
  claim PDF completion merely because an older file exists.

## Keep generation manageable

Use a shared criteria record, source registry and candidate IDs throughout the
report. Keep full captures in private storage; analysis only needs the relevant
excerpts and normalized records, with their source bindings and limitations.
Large packets can be divided into independent analysis tasks: market and
alternatives; costs and suitability; recommendations and next steps. Run those
in parallel when the host supports it, then reconcile their assumptions and
references before rendering one coherent report.

This division is internal work. Do not ask the buyer to request each part.
Preserve completed stages and failure receipts; a timeout is not permission to
replay uncertain work. Verify the finished HTML/PDF contains the intended
analysis and candidate records, then inspect its actual pages.

## Keep audiences distinct

The research packet is for the buyer and may contain private decision limits.
It does not authorize dealer contact, lead forms, appointments or payments.
Before an outward proposal, apply the dealer-proposal evidence and authorization
contract and exclude internal ceilings. Retain the complete buyer packet rather
than replacing it with an outward negotiation summary.
