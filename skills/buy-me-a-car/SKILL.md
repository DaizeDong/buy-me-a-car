---
name: Buy Me a Car
description: This skill should be used when the user asks to "help me buy a car", "buy me a car", "research used cars", "find a used SUV", "email dealers for OTD", "buy a used Subaru/Toyota/Honda", "compare dealers", "negotiate with car dealers", "buy a car this week", or in Chinese says "帮我找车", "买车", "选车", "砍价", "对比经销商". Runs the complete pre-purchase used-car research and dealer-outreach workflow: multi-site inventory search, mass dealer email outreach, recurring inbox monitoring, OTD negotiation with market-data-backed counters, CARFAX/service-record analysis, and consolidated decision tracking.
---

# Buy Me a Car

This skill encodes a proven end-to-end pre-purchase workflow for used cars (primarily Subaru/Honda/Toyota SUVs in the NJ tri-state area, but the structure generalizes). It coordinates research across 9+ used-car sites, sends written OTD requests to 30+ dealers via email, monitors inbox replies on a cron loop, and produces a market-research dossier for the buyer to use at test-drive negotiations.

## Workflow Phases

### Phase 1: Define Requirements

Collect from the user (in one or two messages, not a barrage):

- Make, model, trim acceptable (e.g., "Subaru Forester Premium or Limited")
- Year range (e.g., "2019-2024")
- Mileage cap (e.g., "under 60,000")
- Budget OTD range (e.g., "$20-30k OTD")
- Geographic radius from ZIP (e.g., "within 50 mi of <ZIP>")
- Payment method (cash / financing / trade-in)
- Timeline (this week / this month / casual browsing)
- Must-have features (AWD / heated seats / CarPlay / etc.)

Save these criteria to a working directory file (e.g., `criteria.md`) for later reference. Confirm criteria with user before proceeding.

### Phase 2: Multi-Site Research

Dispatch parallel subagents to research these sites, one per agent:

- Carfax (primary aggregator, best dedup)
- CarMax (no-haggle, single dealer chain)
- Carvana (online-only, returns OTD directly)
- Cars.com
- AutoTrader
- Edmunds
- TrueCar
- CarGurus
- Enterprise Car Sales (rental returns, no-haggle, 12mo/12k warranty)
- Hertz (rental returns)
- EchoPark (no-haggle chain)

Each subagent produces a `report_SITENAME.md` file with: top N candidates matching criteria, VIN/Stock #, miles, price, dealer name + location, any deal indicators ("Good Price"/"Great Deal" tags), and direct links.

After all subagents return, generate `master_comparison.md` deduplicating by VIN across sites. See `references/outreach_strategy.md` for the deduplication and ranking logic.

### Phase 3: Mass Email Outreach

For the top 30-50 candidates across sites, submit lead forms or send direct emails to dealers. Use playwright MCP (browser tool) for sites with anti-bot protection (CarGurus, Cars.com, AutoTrader, Edmunds, TrueCar — all 403 to non-browser fetches). Carfax has a native "Send Email" button that works reliably.

For each dealer, capture:
- Dealer name + address + phone
- Sales rep contact (if known)
- VIN being inquired about
- Lead form submission timestamp
- Anti-bot result (success / blocked / requires manual)

Track submissions in `tracker.md`. See `references/outreach_strategy.md` for the multi-channel strategy (form / email / call / SMS).

**Mass-email format rule (applies to every outbound email — initial inquiry, OTD ask, follow-up):** Use plain ASCII only. NO em-dash (the long dash character), NO en-dash, NO markdown bold or italic markers, NO backticks, NO link syntax. Replace any em-dash with a comma, colon, or period and new sentence. See `references/email_format_rules.md` for the full substitution table. This rule applies to bulk lead-form submissions and all subsequent reply drafts.

### Phase 4: Recurring Inbox Monitoring

Set up a CronCreate job to scan the buyer's Gmail every 15 minutes. The cron prompt should:

- Search inbox for dealer replies (use a keyword filter for makes/models + dealer names)
- Skip Carfax confirmation emails (`from:CARFAX@event.carfax.com`)
- Skip autoresponders ("currently closed" / "will be in touch")
- Skip non-dealer email (banking / academic / personal)
- For each real dealer reply: read full thread, draft reply, save Gmail draft, log to tracker

See `references/cron_monitoring.md` for the exact cron prompt template and Gmail search patterns. See `assets/dealer_reply_template.md` for reply templates.

**Critical email draft format rule:** Gmail drafts must be plain ASCII. See `references/email_format_rules.md` for the complete substitution table (markdown markers, em-dashes, backticks, link syntax must all be stripped before saving any draft).

### Phase 5: OTD Negotiation Strategy

When dealers reply, push hard for **written OTD** before any in-person visit. The OTD ask includes:

- Sales price
- State sales tax (NJ 6.625%, NY 8.875%, PA 6%)
- Doc fee (NJ legal cap $799, common $499-799)
- Title fee
- Registration fee
- Any add-ons (paint protection, nitrogen tires, etching — refuse these)

If a dealer refuses to send OTD by email, decline the visit and walk away. There are always more dealers.

Once OTD numbers are received, use **internal dealer anchor logic**: compare the dealer's own concurrent inventory listings to derive a fair price. Example: if Dealer X lists a base trim at $25k and the target Limited trim at $30k, the $5k spread should equal (Limited trim premium $2-3k) - (mileage delta $1-1.5k) = $1-2k fair spread, not $5k.

Use **market-comp anchoring**: AutoTrader / CarGurus / Edmunds / KBB regional averages. CarGurus deal ratings ("Good"/"Great Deal") correspond to specific price thresholds.

See `references/negotiation_playbook.md` for full anchoring math, walk-away lines, and cash-buyer leverage. Use `assets/dealer_reply_template.md` for the actual reply text patterns (initial OTD ask, counter-offer with anchors, walk-away close, add-on refusal).

### Phase 6: PDF Analysis (CARFAX / Service Records / Quotes)

When dealers attach PDFs (CARFAX reports, service records, OTD proposals), open them with the Read tool. Extract:

- VIN match with listing
- 1-owner / multi-owner
- Accident / damage / structural / odometer issues
- Service record completeness (gaps in maintenance = red flag)
- CVT fluid / spark plug / coolant / brake service intervals (Subaru: 60k mi for major service)
- Active recalls

See `references/pdf_review_checklist.md` for what to check in each PDF type.

### Phase 7: Decision Dossier

Before any test drive, generate a professional 7-10 page market-research dossier (HTML + PDF) that the buyer can show the dealer if needed.

The dossier covers:

- Buyer profile (cash buyer, no trade, ready-this-week)
- Regional market average (AutoTrader / Edmunds / CarGurus)
- Trim-specific MSRP anchors
- CPO (or equivalent program) embedded value
- Competing OTD quotes from other dealers
- Internal anchor analysis (dealer's own inventory)
- Proposed OTD with structured paths to get there
- Conditions of sale (CARFAX, PPI, no recalls, plate transfer)

Workflow (1 command):

```bash
# Edit a copy of dossier_config_template.yaml with the buyer + vehicle + comp data
cp assets/dossier_config_template.yaml my_dossier.yaml
$EDITOR my_dossier.yaml

# Generate HTML + PDF in one step
python scripts/generate_dossier.py \
  --config my_dossier.yaml \
  --output my_dossier.html \
  --to-pdf my_dossier.pdf
```

For Chinese-speaking dealers, point `--template` at the Chinese template:

```bash
python scripts/generate_dossier.py \
  --config my_dossier.yaml \
  --template assets/dossier_template_cn.html \
  --output my_dossier_cn.html \
  --to-pdf my_dossier_cn.pdf
```

The generator substitutes `{{KEY}}` placeholders in the template using the YAML config. It auto-detects Chrome or Edge on Windows / macOS / Linux for the PDF conversion. See `assets/dossier_config_template.yaml` for the full list of supported placeholders.

### Phase 8: Test Drive + Close

Maintain a private negotiation prep file (e.g., `{dealer}_negotiation_prep.md` — buyer-only, do NOT share with dealer) with:

- Dynamic OTD target ladder (stretch / realistic / walk-away)
- Test-drive checklist (cold start, CVT smoothness, brake feel, body panel alignment, interior wear)
- Post-drive questions (CARFAX, service records, current battery test, lien release, 2 key fobs, plates)
- Decision matrix (test-drive result × dealer response → action)

After commit, request:
- PPI by independent ASE-certified mechanic
- Subaru CPO enrollment if eligible
- Plate transfer vs new plates decision
- Cashier's check delivery timing

## Working Directory Convention

For each car search, create a project folder:

```
C:\Users\<user>\car_buying_<year>\
├── README.md                       (index)
├── dealer_outreach_tracker.md      (master tracker — all dialogs, OTD log, decision framework)
├── dealer_reply_template.md        (reusable reply templates)
├── <model>_negotiation_prep.md     (private)
├── <model>_dossier.md / .html / .pdf  (shareable)
├── dealer_pdfs/                    (CARFAX, service records, dealer proposals)
└── market_research/                (subagent reports + comparison)
    └── reports/
```

Save all dealer-related files to this folder. Avoid scattering across home / Downloads.

## Reusable Resources

### References (load as needed)

- `references/outreach_strategy.md` — Multi-site outreach playbook, anti-bot handling, multi-channel (email/SMS/phone)
- `references/negotiation_playbook.md` — Internal-anchor logic, market-comp anchoring, walk-away lines, cash leverage
- `references/pdf_review_checklist.md` — CARFAX / service records / quote PDF red flags
- `references/cron_monitoring.md` — Cron prompt template + Gmail search patterns
- `references/state_fees.md` — NJ / NY / PA tax + doc + reg fees + cross-state titling
- `references/subaru_cpo_program.md` — Subaru CPO eligibility + embedded value math

### Assets (templates to copy and edit)

- `assets/dealer_reply_template.md` — OTD ask / anti-pressure / walk-away templates
- `assets/tracker_template.md` — Tracker file skeleton with sections
- `assets/dossier_template.html` — Print-ready market research dossier (8-page format)
- `assets/negotiation_prep_template.md` — Private prep file with dynamic OTD target ladder

### Scripts (utilities)

- `scripts/otd_calculator.py` — Reverse-engineer sales price from OTD target + state tax + fees
- `scripts/mileage_adjustment.py` — Compute $/mile depreciation comp adjustments
- `scripts/html_to_pdf.sh` — Chrome headless HTML to PDF conversion

## Gotchas (Learned the Hard Way)

1. **Carfax submissions look successful but dealers often do not reply for 12+ hours.** This is normal. Schedule cron monitoring at 15-min intervals starting the morning after submission, not within minutes.

2. **A previous Claude Code session may invent fictitious dealer conversations.** Always verify any "tracker log" entry against the actual Gmail inbox before acting on it. Cross-check claimed dealer responses against the email trace before drafting counters that depend on them.

3. **Email drafts ABSOLUTELY require plain ASCII.** Dealers see literal `**bold**` and `—` characters that did not render. Strip markdown and Unicode dashes before saving any draft. See `references/email_format_rules.md`.

4. **Gmail puts dealer email in Promotions tab, not Inbox.** Search must be tab-agnostic or include `category:promotions`. Spam folder is usually empty.

5. **"Best price upfront" dealers will not negotiate.** Recognize the policy quickly (rental-return chains like Enterprise, no-haggle independent retailers, some volume Subaru dealers at MSRP) and pivot to other dealers rather than waste cycles.

6. **Dealer-attached PDF (proposal.pdf) hides actual OTD numbers.** Gmail attachments cannot be read in-context by Claude; ask user to open the PDF and share numbers, then draft counter based on real data.

7. **The 72-hour urgency claim is sometimes real (Enterprise rental returns) and sometimes pressure tactic.** Confirm by asking about hold/deposit mechanism.

8. **Local relationship dealers (Chinese, family, community) value direct communication over aggressive haggling.** Do not deploy multi-round anchor tactics on them; one fair counter is sufficient.

9. **Always verify dealer hours and rep availability before scheduling.** A Wednesday test drive with a rep who is off Wednesday wastes everyone's time.

10. **CARFAX 1-owner is necessary but not sufficient.** Service records reveal whether the 1 owner actually maintained the car. Absence of CVT fluid service at 60k mi is a $300-400 inherited cost.

## Quick Start

To start a new car search:

1. Read this SKILL.md (already loaded if skill triggered).
2. Ask user for the requirements (Phase 1).
3. Create the working directory `C:\Users\<user>\car_buying_<year>\`.
4. Copy `assets/tracker_template.md` to `dealer_outreach_tracker.md` and edit.
5. Dispatch parallel research subagents (Phase 2).
6. Review subagent outputs, generate shortlist.
7. Begin mass outreach (Phase 3) and cron monitoring (Phase 4).
8. As replies come in, draft responses per `assets/dealer_reply_template.md` and reference Phase 5.
9. Analyze any attached PDFs per `references/pdf_review_checklist.md`.
10. Before test drive, generate `<model>_dossier.html` and convert to PDF.
11. Maintain private negotiation prep separately from public dossier.
12. After commit, walk through Phase 8 closing checklist.
