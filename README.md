# buy-me-a-car 🚗💸

[English](README.md) | [中文版](README_CN.md)

> **Alpha release v0.2.0** — this is one author's playbook backed by 5-scenario stress tests + ~80 root-cause-attributed deltas. Not production-validated; sub-skill content (state fees, CPO terms, EV credits) was last verified 2026-05-18 and may drift. Verify before relying for real purchases. Not tax/legal/financial advice.

> 🛒 **Let Claude Code buy your car.** 9 sites scraped in parallel, 30+ dealer emails sent, cron monitors your inbox, drafts the counter-offers, generates a professional OTD proposal PDF. Fully automated.
>
> 🪶 **Zero dependencies, zero lock-in.** Pure Markdown skill + Python scripts + HTML templates. Swap to Codex, Cursor, Trae, or your own agent and the workflow still runs. Fork it, adapt it to your market.
>
> _💡 This is not a platform. It is a workflow. Take it with you to the next person's car purchase. 🌱_

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-orange?style=flat)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![All 50 States](https://img.shields.io/badge/Tax%20Data-50%20States%20%2B%20DC-green?style=flat)](skills/orchestrator/references/state_fees.md)
[![Roadmap](https://img.shields.io/badge/Roadmap-v0.2.0%20alpha-purple?style=flat)](ROADMAP.md)

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

## Trigger conflicts (which sub-skill activates?)

When a user query could match multiple skills, the most narrow + specific trigger wins. Common cases:

| If user says | Activates | Not |
|---|---|---|
| "help me buy a car" / 帮我买车 | `orchestrator` (full pipeline) | sub-skills |
| "draft reply to dealer" / 回复 dealer | `dealer-reply-drafter` | orchestrator |
| "compute OTD" / 算总价 | `otd-calculator` | orchestrator |
| "doc fee in NJ" / NJ 州税 | `state-fee-lookup` | otd-calculator |
| "lease or buy" / lease 还是 cash | `lease-vs-cash-analyzer` | payment-method-decider |
| "Visa for $30k car" / 刷卡买车 | `payment-method-decider` | lease-vs-cash-analyzer |
| "find quote screenshots" / 找证据图 | `quote-evidence-collector` | orchestrator |
| "$7,500 EV credit" / EV 补贴 | `ev-buyer-helper` | payment-method-decider |
| "book PPI" / 检车 | `ppi-scheduler` | orchestrator |
| "review this CARFAX" / 看 CARFAX | `carfax-pdf-review` | orchestrator |
| "is this car CPO" / Honda Certified | `cpo-eligibility` | carfax-pdf-review |
| "build dossier PDF" / 生成 PDF | `dossier-builder` | orchestrator |
| "check inbox" / 看下邮箱 | `inbox-triage` | orchestrator |
| "valuate trade-in" / 评估置换 | `trade-in-valuator` | otd-calculator |
| "ready to close" / 提车清单 | `close-day-checklist` | orchestrator |

If ambiguous, the user can explicitly name the skill: e.g., "use `dealer-reply-drafter` to draft this".

If you're not sure which to invoke, call `orchestrator` — it routes internally.

---

## 🛠 Inside the plugin

This plugin ships **15 skills**: `orchestrator` (broad trigger, full 9-phase pipeline) plus 14 narrow-trigger sub-skills covering OTD math, state fees, CPO eligibility, CARFAX review, dealer-reply drafting, inbox triage, dossier building, EV credits, payment-method decisions, lease-vs-cash analysis, PPI scheduling, quote-evidence collection, trade-in valuation, and close-day checklists. See the trigger table above for routing. Sub-skills share references with the orchestrator and can be invoked directly. Tree: `skills/<skill-name>/{SKILL.md, references/, assets/, scripts/}` under repo root, plus `ROADMAP.md` and `LICENSE`.

---

## 🤝 Contributing

[ROADMAP.md](ROADMAP.md) tracks what shipped in v0.2.0 and what's next for v0.3.0 / v1.0.0 (multi-author data, adversarial dealer tests, 50-state fill-in, more brand CPO programs). Pick one, open a GitHub issue, ship a PR.

---

## 📝 License

MIT — fork it, ship it, save someone money.
