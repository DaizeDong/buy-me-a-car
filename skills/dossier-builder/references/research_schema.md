# Buyer research input

The agent assembles this input from existing private cycle records. The buyer
should not be asked to write JSON, find schema keys, or request each section.
Use the generated `research_report_config_template.json` only to understand the
schema or run a synthetic demo; real observations belong in live private DATA.

## Header and evidence

Required header fields: `document_type: buyer_research`, `synthetic` (boolean),
`date` (`YYYY-MM-DD`), `language: cn`, `title`, and `decision_summary`.
Use `synthetic: false` for real source captures even when the buyer criteria are
explicit scenario assumptions. Explain that scope in the summary.

| Collection | Fields |
|---|---|
| `criteria` | `id`, `label`, `value` (text or null), `status` (`confirmed`, `assumed`, `unknown`), `source_ids`, `notes` |
| `sources` | `id`, `title`, HTTPS `url`, `observed_date`, `status` (`captured`, `blocked`, `unavailable`), `kind`, `limitations` |
| `coverage` | `id`, `label`, `status` (`complete`, `partial`, `blocked`, `not_searched`), `source_ids`, `query`, `limitations` |
| `candidates` | `id`, `vehicle`, `configuration`, `asking_price` (decimal text or null), `currency: USD`, `location`, `source_id`, `limitations`; optional `vin`, `stock` |

`criteria.status` describes factual status, not whether the buyer has approved
using an assumption. Keep user-authorized scenario values `assumed`; do not
upgrade them to facts about the real buyer. Preserve the approval and its scope
in criterion `notes` and shared context. Once approved for the report, these
values are settled inputs: do not ask again or make reconfirmation a next action
unless a material change occurs. This approval does not authorize contacting
sellers, booking services, paying or purchasing. Actual vehicle specifications,
costs and other missing evidence still require verification.

Source kinds are `listing`, `official`, `guide`, `dealer_quote`, and
`buyer_statement`. Captured live sources also require `artifact` and `sha256`
pointing to the inspected bytes under private DATA. Blocked sources document
coverage limitations; they cannot substantiate a vehicle or financial claim.
Preserve exact VIN/configuration data and source disagreements. Do not infer a
verified tow rating, current warranty or final quote from a badge or listing.
`criteria` and `coverage` must be nonempty. When research cannot proceed, record
the attempted or unsearched scope and limitation explicitly. Zero candidates,
zero quotes and zero captured sources are allowed if accurately described;
incomplete coverage is labeled visibly in the report.

## Optional financial records

`costs` records reference `candidate_id`, contain `source_ids` and `limitations`,
and may supply decimal text or null for `tax`, `title_registration`,
`dealer_fees`, `transport`, `inspection`, and `other`. Missing values stay
unknown. An already-included doc fee must not be added again. The filled-component
scenario subtotal can include explicitly documented assumptions and is not a
confirmed cost, final OTD or delivered-cost quote.

`written_quotes` may be omitted or empty. If present, records use `id`,
`candidate_id`, `otd`, `currency`, `source_id`, and `conditions`. Supply only
actual written quotations with matching evidence. Their absence never blocks a
buyer research report.

## Analysis sections

`sections` cover these topics: `requirements`, `coverage`, `alternatives`,
`listings`, `costs`, `suitability`, `winter`, `ownership`, `recommendation`,
`next_actions`, and `sources`. The `winter` topic covers applicable local
weather/service/transport logistics; explain when cold-weather detail is not
relevant. Each section has `id`, `topic`, `title`, and nonempty `blocks`.

Supported blocks:

- Paragraph: `type: paragraph`, `text`.
- Bullets: `type: bullets`, `items` containing text.
- Table: `type: table`, `columns`, and `rows` of matching length; null is unknown.

Blocks may have `refs` using `source:<id>`, `candidate:<id>` and `section:<id>`.
Every reference must resolve. Use references for factual comparisons and explain
uncertainties in the prose.
Uncaptured source references may occur only in `coverage`, `sources` and
`next_actions`, where they document gaps rather than substantiate claims.
The renderer adds core data tables for requirements,
coverage, listings, costs and sources; analysis should interpret those tables
rather than repeat every row. No raw HTML is accepted from config values.
Use the buyer's language in narrative text. Field names such as `asking_price`
and `title_registration`, and the literal `null`, belong in structured data;
the report should say asking price, registration costs and unknown amounts in
ordinary language. Candidate/source IDs may remain as traceable references.

## Reproduce and deliver

Run the command in the skill, then inspect each PDF page. Confirm every selected
candidate and source remains present, the conclusions follow from the evidence,
and missing data stays visible. The output is an internal buyer report and may
contain private decision limits. Do not send it to a dealer as an outward offer.
