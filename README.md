# Buy Me a Car — Claude Code Plugin

> An end-to-end used car pre-purchase workflow: multi-site research, mass dealer outreach, OTD negotiation, CARFAX analysis, and decision tracking.

A complete pre-purchase workflow for used cars (Subaru, Honda, Toyota, Ford, etc.), packaged as a Claude Code plugin.

This skill turns Claude Code into a specialized car-buying agent that:

- Researches inventory across 9+ used-car sites in parallel
- Sends mass dealer outreach with written OTD requests
- Monitors your Gmail inbox on a 15-minute cron for replies
- Drafts negotiation responses with market-data-backed anchors
- Analyzes CARFAX, service records, and dealer quote PDFs
- Generates a print-ready market research dossier
- Maintains a single decision tracker so nothing falls through

Built from real used-car purchase experience and refined into a reusable workflow.

## Installation

In Claude Code:

```
/plugin install github:DaizeDong/buy-me-a-car
```

Or clone manually:

```bash
git clone https://github.com/DaizeDong/buy-me-a-car.git
mv buy-me-a-car ~/.claude/plugins/buy-me-a-car
```

## Activation

The skill auto-triggers when you ask Claude Code anything like:

- "Help me buy a used car"
- "Research a 2024 Subaru Forester near me"
- "Email dealers for OTD"
- "Compare dealers for a Honda CR-V"
- "Negotiate with car dealers"
- (Chinese) "帮我找车", "买车", "选车", "砍价", "对比经销商"

## What's Included

### Skill body (`skills/buy-me-a-car/SKILL.md`)

8-phase workflow definition:

1. Define requirements
2. Multi-site research (parallel subagent dispatch)
3. Mass email outreach (with anti-bot handling)
4. Recurring inbox monitoring (Gmail + cron)
5. OTD negotiation strategy
6. PDF analysis (CARFAX, service records, quotes)
7. Decision dossier generation
8. Test drive + close

### References (loaded as needed)

- `outreach_strategy.md` — Multi-site outreach, anti-bot bypass, multi-channel coordination
- `negotiation_playbook.md` — Internal-anchor logic, market-comp anchoring, walk-away lines
- `pdf_review_checklist.md` — CARFAX / service records / quote PDF red flag detection
- `cron_monitoring.md` — Cron prompt template + Gmail search patterns
- `state_fees.md` — All 50 US states + DC tax/doc/title/reg fee data
- `email_format_rules.md` — Plain ASCII email rules for dealer outreach
- `subaru_cpo_program.md` — Subaru CPO eligibility + embedded value math

### Templates (`assets/`)

- `dealer_reply_template.md` — 10+ reply templates (OTD ask, counter, walk-away, etc.)
- `tracker_template.md` — Master tracker file skeleton
- `dossier_template.html` — 8-page print-ready market research dossier
- `negotiation_prep_template.md` — Private prep with dynamic OTD ladder + decision matrix

### Scripts (`scripts/`)

- `otd_calculator.py` — OTD <-> sales price math for all 50 states + DC
- `mileage_adjustment.py` — Black Book / Manheim mileage depreciation calculator
- `html_to_pdf.sh` — Chrome headless HTML-to-PDF conversion

## Example Workflow

```
You: "Help me buy a used Subaru Forester this week, budget $25k OTD, under 60k miles, near 90210"

Claude (loads skill, follows Phase 1):
  Confirms criteria. Creates car_buying_2026/ working folder.

Claude (Phase 2):
  Dispatches 9 parallel subagents (Carfax, CarMax, Cars.com, AutoTrader, etc.).
  Consolidates into master_comparison.md with top 30 candidates ranked by composite score.

Claude (Phase 3):
  For top 30, submits Carfax lead forms or uses playwright MCP for anti-bot sites.

Claude (Phase 4):
  Sets up CronCreate to monitor your Gmail every 15 minutes.

Claude (Phases 5-8 as replies arrive):
  Drafts OTD asks. Reviews CARFAX PDFs. Negotiates with internal anchors.
  Generates dossier_cn.pdf for the test drive.
  Maintains tracker.md with all live state.
```

## Requirements

- Claude Code 2.x (sept 2025+)
- Gmail with Claude.ai Gmail connector authorized (for inbox monitoring)
- Chrome or Edge installed (for HTML-to-PDF generation)
- Python 3.7+ (for OTD calculator and mileage scripts)
- `playwright` MCP (optional, for anti-bot site submissions)
- `firecrawl` (optional, for market comp scraping)

## Tested Use Cases

- Multi-site research for Subaru Forester / Outback / Crosstrek
- 30+ dealer email batch outreach
- OTD negotiation from $20k to $30k+ range
- Cross-state (NY -> NJ, PA -> NJ) titling math
- Subaru CPO eligibility analysis
- Enterprise Car Sales no-haggle workflow
- Independent dealer relationship-based purchase (e.g., Chinese dealer)

The skill is built for used cars but most components apply to new car purchases too.

## License

MIT

## Contributing

Issues and PRs welcome. See [ROADMAP.md](ROADMAP.md) for the full list of future features grouped into 7 categories (workflow enhancements, new vehicle types, tooling, community data, multi-language, post-purchase, speculative).

To pick up an item, open a GitHub issue saying "I'm working on X." To suggest a new idea, open an issue with a concrete use case.

## Acknowledgments

- Built on the Claude Code skill framework
- References Anthropic's plugin-dev `skill-development` meta-skill
- Inspired by real-world used-car-buying friction points

## Author

[Buyer name] — built this after going through a real purchase cycle and realizing the entire workflow was reusable.
