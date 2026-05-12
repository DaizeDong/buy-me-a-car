# buy-me-a-car 🚗💸

[English](README.md) | [中文版](README_CN.md)

> 🛒 **Let Claude Code buy your car.** 9 sites scraped in parallel, 30+ dealer emails sent, cron monitors your inbox, drafts the counter-offers, generates a professional OTD proposal PDF. Fully automated.
>
> 🪶 **Zero dependencies, zero lock-in.** Pure Markdown skill + Python scripts + HTML templates. Swap to Codex, Cursor, Trae, or your own agent and the workflow still runs. Fork it, adapt it to your market.
>
> _💡 This is not a platform. It is a workflow. Take it with you to the next person's car purchase. 🌱_

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![All 50 States](https://img.shields.io/badge/Tax%20Data-50%20States%20%2B%20DC-green?style=flat)](skills/buy-me-a-car/references/state_fees.md)
[![Roadmap](https://img.shields.io/badge/Roadmap-35%2B%20Ideas-purple?style=flat)](ROADMAP.md)

---

## 🎯 Three Modes, Same Skill

**Quick mode** — one sentence kicks off the full workflow:

```
help me buy a used compact SUV this week, budget $25k OTD, under 60k miles, near <ZIP>
```

Claude confirms criteria, dispatches 9 parallel subagents (Carfax / CarMax / Carvana / Cars.com / AutoTrader / Edmunds / TrueCar / CarGurus / Enterprise), consolidates the top 30 candidates, submits lead forms, and sets up a 15-minute cron to monitor your Gmail.

**Negotiation mode** — dealer sent an OTD? Anchor and counter:

```
the dealer asking $32,200 OTD, target $30k — write me a counter
```

Claude drafts a plain-ASCII reply using 3 anchors: (1) the dealer's own concurrent inventory price spread, (2) regional market comp (AutoTrader / KBB / CarGurus), and (3) your other locked OTDs.

**Dossier mode** — print a professional market-research dossier before the test drive:

```bash
cp assets/dossier_config_template.yaml my_offer.yaml
$EDITOR my_offer.yaml   # buyer + target vehicle + competing OTDs + sources

python scripts/generate_dossier.py \
  --config my_offer.yaml \
  --output my_offer.html \
  --to-pdf my_offer.pdf
```

An 8-page PDF (English or Chinese template) covering market averages, trim comparison, CPO embedded value, internal anchor analysis, proposed OTD structure, and sale conditions. Buyer-quality, dealer-shareable.

---

## 🚀 Install

```
/plugin install github:DaizeDong/buy-me-a-car
```

Or clone manually:

```bash
git clone https://github.com/DaizeDong/buy-me-a-car.git ~/.claude/plugins/buy-me-a-car
```

The skill auto-activates when you say "help me buy a car", "buy me a car", "research used cars", etc.

---

## ✨ What's in the box

| | |
|---|---|
| 🔍 **Multi-site research** | 9 sites in parallel subagent dispatch, Carfax as primary aggregator |
| 📧 **Mass email outreach** | Plain-ASCII templates, strict no-markdown / no-em-dash rule |
| ⏰ **Cron inbox monitoring** | 15-min Gmail scan, drafts replies, tracks threads, skips auto-responders |
| 💰 **OTD calculator** | Tax / doc / title / reg data for all **50 states + DC** |
| 📐 **Mileage adjustment** | Black Book / Manheim standard, segmented by SUV / sedan / luxury |
| 📄 **PDF analysis** | CARFAX / service records / dealer quote auto-review checklist |
| 🎨 **Dossier generation** | YAML config → HTML → Chrome headless PDF (English + Chinese) |
| 🚫 **Anti-bot handling** | Playwright MCP integration (CarGurus / Cars.com / AutoTrader / Edmunds / TrueCar) |

---

## 🛠 Inside the skill

```
buy-me-a-car/
├── skills/buy-me-a-car/
│   ├── SKILL.md                          # 8-phase workflow definition
│   ├── references/                       # loaded on-demand
│   │   ├── outreach_strategy.md          # multi-site + anti-bot
│   │   ├── negotiation_playbook.md       # 3 anchors + walk-away lines
│   │   ├── pdf_review_checklist.md       # CARFAX / service / quote review
│   │   ├── cron_monitoring.md            # cron prompt template
│   │   ├── state_fees.md                 # all 50 states + DC
│   │   ├── email_format_rules.md         # plain-ASCII rules
│   │   └── subaru_cpo_program.md         # CPO embedded value
│   ├── assets/                           # copy-and-edit templates
│   │   ├── dealer_reply_template.md      # 10+ reply templates
│   │   ├── tracker_template.md           # tracker skeleton
│   │   ├── dossier_template.html         # English dossier template
│   │   ├── dossier_template_cn.html      # Chinese dossier template
│   │   ├── dossier_config_template.yaml  # 80+ placeholders config
│   │   └── negotiation_prep_template.md  # private negotiation prep
│   └── scripts/                          # utilities
│       ├── otd_calculator.py             # 50-state OTD calculator
│       ├── mileage_adjustment.py         # mileage depreciation
│       ├── generate_dossier.py           # YAML → HTML/PDF
│       └── html_to_pdf.sh                # standalone HTML → PDF
├── ROADMAP.md                            # 35+ future feature ideas
└── LICENSE                               # MIT
```

---

## 📈 Real-world results

> Used this skill to complete the full outreach + negotiation phase of a real used-car purchase in 2 days. Outcomes:

- **38 dealers** contacted, cron tracked every reply
- **4 written OTDs** received, ranging $20,348 to $32,200
- **2 dealers** politely walked away from after counter-offer rejection (no time wasted)
- **1 local dealer** found through non-aggregator channels (community network value)
- **Estimated $5-9k saved** vs walking into a single dealer cold (conservative estimate)

---

## 🔄 8-phase workflow

```
1. Define requirements        criteria + model + miles + budget + ZIP
2. Multi-site research        9 parallel subagents → top 30 candidates
3. Mass email outreach        Carfax-first, playwright for anti-bot sites
4. Cron inbox monitoring      15-min Gmail scan, drafts, autoresponder skip
5. OTD negotiation            3 anchors + walk-away + add-on refusal
6. PDF analysis               CARFAX / service records / dealer quotes
7. Dossier generation         YAML → HTML → PDF (English / Chinese)
8. Test drive + close         checklist + decision matrix + closing
```

Full phase documentation in [`SKILL.md`](skills/buy-me-a-car/SKILL.md).

---

## 🤝 Contributing

[ROADMAP.md](ROADMAP.md) lists **35+ feature ideas** across 7 categories:

- A. Workflow phase enhancements (6 items) — thread dedup, playwright bundle, attachment extraction
- B. New vehicle categories (5 items) — lease, new car, EV, trade-in tax
- C. Tooling & infrastructure (7 items) — OEM CPO database, NHTSA recall API, VIN decoder
- D. Data & community (5 items) — shared transaction dataset, dealer ratings
- E. Multi-market & multi-language (4 items) — Spanish, Canadian, EU
- F. Post-purchase phase 9 (4 items) — closing day, 30-day guide, insurance
- G. Stretch / speculative (4 items) — voice negotiation, multi-buyer collaboration

Pick one, open a GitHub issue, ship a PR.

---

## 📝 License

MIT — Fork it, ship it, save someone money.

---

## ✍️ Author

[@DaizeDong](https://github.com/DaizeDong) — built from a real purchase cycle. 12 hours from idea to published plugin. If it saves you money, a 🌟 on the repo is the best thanks.
