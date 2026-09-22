---
name: dossier-builder
description: Generate complete buyer research reports and dealer proposals as HTML and PDF. Use for vehicle comparisons, market research, shortlists and default report delivery during a car-buying workflow. Triggers include "build dossier", "generate market research PDF", "dealer dossier", "decision document", "make dossier for dealer", "生成 dossier", "制作 PDF", "完整购车报告", "generar el dossier para el concesionario", and "crear el PDF de investigacion de mercado".
---

# Decision Dossier Builder

Deliver the buying report from the evidence already collected. A broad buying
workflow includes this artifact without a separate request for detail or a PDF.
The agent prepares the config; do not ask the buyer to populate schema fields.

## Choose the document purpose first

| Purpose | Generator | Evidence needed |
|---|---|---|
| Buyer research and shortlisting | `generate_research_report.py` | Dated source coverage, candidate listings, analysis and explicit unknowns. Zero written dealer quotes is allowed. |
| Dealer-facing purchase proposal | `generate_dossier.py` | Complete competing written OTD quotes, supported facts and an itemized authorized proposal. |

The first is the default during market research. The second is a later outward
document. Do not make the proposal's two-quote or complete-fee requirement block
useful research. Both have separate demo/live privacy modes; research versus
proposal is not the same choice as synthetic versus real data.

## Generate the buyer research packet

Follow [report delivery](../orchestrator/references/report_delivery.md). Reuse the
current private cycle, criteria and captured evidence. Produce substantive
comparisons, configuration tradeoffs, delivered-cost uncertainties, suitability,
ownership risks, shortlist rationale and next actions, rather than a long intake
questionnaire or validation log. Use the
[research schema](references/research_schema.md) to assemble structured input.

```sh
python skills/orchestrator/scripts/generate_research_report.py --mode live --config cycles/session/research_config.json --output cycles/session/buyer_research.html --to-pdf cycles/session/buyer_research.pdf
```

Live relative paths resolve under verified private DATA. Keep
`master_comparison.md` alongside the report. When a scenario has fictional buyer
criteria but real source observations, use live private storage and label every
fictional criterion as an assumption; never turn observed inventory into public
demo fixtures. List asking prices as asking prices, leave missing fees unknown,
and explain what evidence would change the shortlist.

Inspect every generated PDF page and the substance checklist before delivering
the HTML/PDF links. Do not request extra permission to render local artifacts
already implied by the buying task. Source/PDF problems must be visible; preserve
useful partial work and resolve the remaining dependency where possible.

The remainder of this document describes the stricter dealer proposal.
Its generator checks arithmetic, required fields, source dates and evidence
integrity. Those checks cannot determine whether a source supports a claim or
whether a dealer still honors its terms. Read the sources before making claims.

## Choose the mode

- `demo` accepts only the generated synthetic EN/CN/ES fixtures. Every page is
  labeled as a synthetic demonstration that must not be presented as real.
  Changing a fixture to include personal information is rejected.
- `live` requires a current config, evidence files, and output files under the
  proven private companion DATA directory. Missing initialization, public or
  unknown repository visibility, and paths outside that directory fail.

Do not turn the demo into a real proposal by changing only its mode. Replace
fictional input with researched facts and buyer-approved statements, and bind
those fields to the actual source artifacts. Do not claim a confirmed quote,
clean history, active warranty, certification, payment method, or closing
commitment without the matching evidence. Keep the buyer's private walk-away
ceiling out of this dealer-facing document.

## Build a synthetic demonstration

From the repository root, choose an output directory outside the public tool
repository. For example, replace `<temporary-directory>` below with a system
temporary directory:

```sh
python skills/orchestrator/scripts/generate_dossier.py --mode demo --config skills/orchestrator/assets/dossier_config_template.yaml --output <temporary-directory>/dossier.html --to-pdf <temporary-directory>/dossier.pdf
```

For Chinese or Spanish, select `dossier_config_template_cn.yaml` or
`dossier_config_template_es.yaml`. `LANGUAGE` chooses the corresponding shipped
HTML template. `--template` may explicitly select a shipped EN/CN/ES template.
The localized templates translate fixed labels; arbitrary input prose is not
translated. The public fixtures are formatting demonstrations and contain some
English sample content.

Fixtures are regenerated by `python tools/make_fixtures.py`; do not edit their
output files manually. Python needs PyYAML for YAML input and pypdf to verify PDF
output. Use Chromium 131 or newer for printed page-margin notices. An available
wkhtmltopdf fallback is attempted when Chromium is absent, but output still
fails verification if that renderer cannot print the required notice on every
page.

## Build a real proposal

1. Resolve the private DATA directory with `tools/runtime_paths.py`. Create and
   store the config and source artifacts there. Never use a path in the public
   repository for real buyer information or source observations.
2. Read each source. Record its date, provenance, hash, and the fields it supports.
   Require written OTD quotes for the same registration jurisdiction, with their
   conditions and expiration dates. A listing price is not a written OTD quote.
3. Fill every placeholder field used by the chosen template, including buyer
   payment, financing, trade-in, and plate plans. Use `DOSSIER_MODE: live`,
   `SYNTHETIC: false`, and today's quoted `DATE`.
4. Run the generator. Relative live paths resolve under private DATA, so the
   following paths are not relative to the public working tree:

```sh
python skills/orchestrator/scripts/generate_dossier.py --mode live --config dossiers/session/config.yaml --output dossiers/session/proposal.html --to-pdf dossiers/session/proposal.pdf
```

5. Open the PDF and inspect every page for legibility, clipping, broken tables,
   and untranslated text. Recheck amounts and source references. Report the
   actual page count; length changes with the supplied content.

The shell entrypoint `html_to_pdf.sh` takes the same generator arguments. It
regenerates the validated dossier instead of accepting arbitrary input HTML.
`--allow-missing` was removed: missing or unresolved content must be completed
before a dossier is emitted.

## Monetary contract

Use decimal strings such as `"27500.00"`. Dollar signs, scientific notation,
negative charges, malformed separators, nonfinite numbers, and fractions of a
cent are rejected. The generator checks:

```
TARGET_OTD = PROPOSED_SALES + TAX_AMOUNT + REG_AMOUNT + TITLE_AMOUNT
             + DOC_AMOUNT + OTHER_FEES - TRADE_IN_CREDIT - REBATE_AMOUNT
TAX_AMOUNT = round_half_up(TAX_BASE * TAX_RATE / 100, 2) + TAX_ADJUSTMENT
```

Supply every field, including explicit zero values. `TAX_RATE` is a percentage:
`"8"` means 8%. `TAX_ADJUSTMENT` is signed and must be supported when used for a
fixed adjustment. Derive the taxable base, credits, title, and registration
charges from current applicable rules; this arithmetic check does not decide
which jurisdictional tax mechanism or exemptions apply. Consult the
`otd-calculator` and `state-fee-lookup` helpers first. The tax basis and adjustment
row in the PDF is informational and is not added to the total a second time.

## Quote and evidence contract

`QUOTES` contains at least two distinct complete offers. Every record requires:

| Field | Required meaning |
|---|---|
| `id` | Unique letters, digits, hyphens, or underscores |
| `vehicle`, `vehicle_id` | Vehicle description plus VIN or dealer stock identifier |
| `dealer`, `mileage` | Dealer identity and vehicle mileage |
| `otd` | Positive final amount, including the quoted taxes and fees |
| `registration_state` | Same jurisdiction as the buyer's `STATE` |
| `conditions` | Financing, trade-in, rebates, and other conditions affecting this amount |
| `expires_on` | Quoted expiration date; an expired quote is rejected |
| `status` | `written_quote` for live input; `synthetic` only in demos |
| `source_id` | ID of the matching `EVIDENCE` record |

All quote records are rendered. Do not provide legacy `COMP_*` fields or a
manually asserted count of confirmed offers; those display values are derived.

Each `EVIDENCE` record requires `id`, `kind`, `source`, `source_date`, and
`supports`. Dates use quoted `YYYY-MM-DD` strings. Live evidence additionally
requires `artifact` (a private DATA path) and `sha256` (the actual file hash).
Supported live kinds are `dealer_quote`, `listing`, `official`, and
`buyer_statement`. Use an HTTPS provenance URL, or a descriptive provenance
label for a buyer statement; the artifact preserves the inspected content.

`supports` lists exact scalar field names and `quote:<id>` references. Each
nonempty live scalar fact or buyer statement needs coverage, except proposal
metadata and the buyer's proposed sales price and target. Each written quote
must reference `dealer_quote` evidence supporting that quote ID. Offer/listing
sources must be no older than 14 days; official documents and buyer statements
must have been reviewed within 90 days. Future dates are rejected. Keep original
source publication dates inside the artifact when `source_date` records a fresh
review of an older policy.

Record sources for warranty, certification, regional statistics, and narrative
claims as carefully as for quotes. Presence and matching SHA-256 establish that
the stored artifact has not changed; they do not prove its truth or the accuracy
of the operator's interpretation. The PDF displays source IDs, dates, and
provenance without printing local artifact paths.

## PDF and output checks

- Chromium runs with a fresh temporary profile and `--no-pdf-header-footer`.
- The default rendering timeout is 60 seconds; `--pdf-timeout` accepts values
  above zero through 300 seconds.
- A new staging PDF must parse, contain pages, repeat the exact mode notice on
  every page, and have no printed `file:///` URL before it replaces the requested
  output. A renderer failure or timeout
  cannot be mistaken for success because an old PDF exists.
- Inserted config text is HTML-escaped. Deliberate markup belongs in the shipped
  templates; arbitrary templates and raw config HTML are not accepted.

Return the mode, private config path, HTML/PDF paths, actual page count, monetary
validation result, evidence completeness result, and scope of visual inspection.
For a demo, explicitly say that no real quote or negotiation was performed. For
live work, distinguish source review from the generator's mechanical checks.

## Related helpers

- `../orchestrator/scripts/generate_dossier.py`: validation and rendering
- `../orchestrator/assets/dossier_template*.html`: EN/CN/ES layout
- `../quote-evidence-collector/SKILL.md`: source collection
- `../otd-calculator/SKILL.md`: supported OTD calculations
- `../state-fee-lookup/SKILL.md`: jurisdictional tax and fee verification

When installed through directory links, resolve this SKILL.md to its source directory before following relative file paths. Those paths refer to the repository layout.
