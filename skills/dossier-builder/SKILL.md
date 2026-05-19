---
name: Decision Dossier Builder
description: Use to generate a printed market-research dossier (8-page HTML + PDF) the buyer brings to the dealer at test drive, summarizing buyer profile, regional comps, target OTD, and cross-bid anchors. Triggers include "build dossier", "generate market research PDF", "dealer dossier", "decision document", "make dossier for dealer", "生成 dossier", "制作 PDF".
---

# Decision Dossier Builder

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 3C sub-skill split from orchestrator)

Narrow helper: drive `generate_dossier.py` to produce the 8-page HTML + PDF
dossier the buyer hands the salesperson at test drive. Defers the script,
templates, and YAML schema to the orchestrator's `scripts/` and `assets/`.

## When To Use

- Buyer is ready for the in-store visit and wants a printable evidence packet
- Need EN or CN version (CJK template available)
- Buyer has comp anchors collected (XHS / Reddit / cross-bids) and wants
  them formalized into a single document

## When NOT To Use

- Still in Phase 1 (criteria not locked) - too early; orchestrator first
- Quote evidence not yet collected - delegate to `quote-evidence-collector`
- Just need an OTD calculation - delegate to `otd-calculator`

## 3-Step Workflow

1. Copy `../orchestrator/assets/dossier_config_template.yaml` to a working
   file (e.g. `my_dossier.yaml`) and fill in 8-15 fields.
2. Run:
   ```
   python ../orchestrator/scripts/generate_dossier.py \
     --config my_dossier.yaml \
     --output dossier.html \
     --to-pdf dossier.pdf
   ```
3. (Optional) Chinese template:
   ```
   python ../orchestrator/scripts/generate_dossier.py \
     --config my_dossier.yaml \
     --template ../orchestrator/assets/dossier_template_cn.html \
     --output dossier_cn.html \
     --to-pdf dossier_cn.pdf
   ```

## Required YAML Fields

- `BUYER_NAME`, `BUYER_ADDRESS`, `DATE`
- `YEAR`, `MAKE_MODEL`, `TRIM`, `MSRP`
- `TARGET_OTD`, `TARGET_SALE`
- `STATE`, `TAX_RATE`
- At least 2 `COMP_VEH_N` entries (other dealer listings as comp anchors)

## Optional YAML Fields

- `WALK_AWAY_CEILING` - recommended; gives the buyer a clear stop number
- `REGIONAL_AVERAGE` - Edmunds / TrueCar reference price
- `REDDIT_OTD_REPORT_1`, `_2`, `_3` - real buyer-reported OTDs (up to 3)
- `CPO_PROGRAM` - if vehicle is CPO; populates p3 with program benefits
- `INCENTIVE_STACK` - manufacturer rebates + state credits (EV, loyalty, etc.)

## 8-Page Dossier Structure

| Page | Contents |
|---|---|
| 1 | Buyer profile + target summary + close-timing claim |
| 2 | Regional market average (Edmunds / TrueCar) |
| 3 | Trim / option breakdown + MSRP anchors |
| 4 | Competing OTD quotes - first 2-3 cross-bid evidence rows |
| 5 | Competing OTD quotes - continued, plus Reddit reports |
| 6 | Internal anchor analysis (dealer's own concurrent inventory) |
| 7 | Proposed OTD with structured paths (best / target / walk) |
| 8 | Conditions of sale (CARFAX request, PPI booked, plate transfer decision) |

## Script Behaviors

From `../orchestrator/scripts/generate_dossier.py`:

- Cross-platform Chrome / Edge auto-detection (Windows / macOS / Linux); uses
  headless Chrome for HTML-to-PDF
- Placeholder validation: scans template for ALL `{{KEY}}` tokens BEFORE
  substitution, fails loudly if any required key is missing
- `--allow-missing` opt-out for incomplete configs (PDF will render
  `{{KEY}}` literal text for missing keys - useful for drafts)
- Auto-detects `CHROME_BIN` environment variable as override

## Template Variants

- EN (default): `../orchestrator/assets/dossier_template.html`
- CN: `../orchestrator/assets/dossier_template_cn.html` (CJK glyph support)

The CN template is field-for-field equivalent; same YAML config drives both.
Useful when buyer is Chinese-American and wants to share with parents /
spouse before signing.

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `Chrome not found` | Headless renderer can't locate browser | Install Chrome OR set `CHROME_BIN=/path/to/chrome` env var |
| `Missing required field: TARGET_OTD` | YAML key missing | Add to YAML; re-run |
| PDF blank / missing CSS | Chrome version too old | Upgrade Chrome to >= 90 |
| Garbled CJK glyphs in CN PDF | Font missing | Install Noto Sans CJK or use system font |
| YAML parse error at line N | Quoting issue | Wrap value in double quotes; commas need quoting |

## Use Case

Bring the printed dossier to the test drive. Hand the salesperson page 1
(buyer profile + target) at the start. Show pages 4-5 (cross-bid evidence)
when the dealer counters. Show page 8 (conditions of sale) when negotiating
the final deal sheet. Signals to the dealer:

- You've done your market research
- Your target OTD is anchored to comps, not pulled from thin air
- You will close fast if the terms match (close-timing claim on page 1)
- You will walk if the conditions of sale (CARFAX, PPI) are denied

Per orchestrator Critical Rule #3: never leave the dossier behind. Take it
back to your car. The dealer can photograph but cannot keep the physical
copy.

## Cross-References

- `../orchestrator/scripts/generate_dossier.py` - the renderer
- `../orchestrator/assets/dossier_template.html` - EN template
- `../orchestrator/assets/dossier_template_cn.html` - CN template
- `../orchestrator/assets/dossier_config_template.yaml` - YAML template
  starter (copy and fill)
- `../orchestrator/SKILL.md` Phase 8 - dossier-prep phase in the master flow
- `../orchestrator/SKILL.md` Critical Rule #3 - never leave dossier behind
- `../quote-evidence-collector/SKILL.md` - upstream step that produces the
  `COMP_VEH_N` and `REDDIT_OTD_REPORT_N` raw inputs
- `../otd-calculator/SKILL.md` - upstream step that produces `TARGET_OTD`
  and `WALK_AWAY_CEILING`

## Sample Artifacts (Phase 0 / 5 test run, CT Outback example)

- `<working-dir>/skill-test/p0_p5_execution/sample_dossier.html`
- `<working-dir>/skill-test/p0_p5_execution/sample_dossier.pdf`

These are the reference outputs to diff against when changing templates.

## Output Contract

After every dossier build, return to the operator:

```
Dossier build - <timestamp>
  Vehicle: <year make model trim>
  Config YAML: <path>
  Template: EN / CN
  Required fields supplied: <n>/<n>
  Optional fields supplied: <n>
  Output HTML: <path>
  Output PDF: <path>
  Pages rendered: 8
  Placeholder validation: PASS / FAIL <missing keys>
  Chrome used: <version>
```
