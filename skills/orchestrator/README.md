# Buy Me a Car

Claude Code skill that runs the full pre-purchase workflow: research → outreach → negotiate → close.

Trigger: `help me buy a car` / `帮我找车` / `买车` / `find me an SUV` / `negotiate OTD`

## What it does

| Phase | What you get |
|---|---|
| 1. Requirements | criteria.md with walk-away ceiling + buyer-type router (cash / finance / trade / EV) |
| 2. Baseline data | Market price baseline pulled live (REAL/SYNTHESIZED tagged) |
| 3. Inventory | Playwright-first scrape of 11 sites (paginated, deduped by VIN) -> Site Capability Matrix + candidate list |
| 4. Outreach | 30-50 plain-ASCII dealer emails with cross-bid anchors |
| 5. Gmail monitoring | Cron scans every 15min + spam/promo + morning catch-up |
| 6. OTD negotiation | Round 1 Cold Open, ADM kill list, escalation ladder, state-parameterized math |
| 7. PDF review | CARFAX accident detail, service gaps, buried F&I add-ons |
| 8. Dossier | 8-page HTML + PDF (EN or CN) buyer takes to dealer |
| 9. Close | Buyer-type checklist (cash / finance / trade / EV / pickup) + F&I hard-no script |

## Coverage

- **22 states** at depth (NJ/NY/PA/CT/MA/RI/NH/ME/VT/CA/TX/IL/FL/OH/NC/GA/MI/VA/WA/DC/MD + 50-state base)
- **8 CPO programs** (Subaru/Honda/Toyota/Hyundai/Kia/Ford/GM/Mazda)
- **5 buyer paths** (cash / finance / lease / trade / EV — note: federal §30D/§25E/§45W EV credits terminated 2025-09-30 per OBBBA; EV path is now state-rebate + charging/SoH diligence only)
- **6 vehicle classes** including pickup, heavy-duty, commercial, luxury
- **14 anti-patterns** auto-detected at Phase 1
- **English** (dealer-facing); **Chinese / other** (buyer-facing)

## Quick start

```
You: 帮我买车
Skill: <8 questions for vehicle/budget/payment/walk-away/timeline...>
You: <answer>
Skill: <Heads-up if any of 14 anti-patterns fire>
You: confirm
Skill: <runs P2-P9 with subagents + cron, drafts emails, you paperclip
       attachments + send>
```

## Critical Rules (non-negotiable)

1. Plain ASCII in every outbound email
2. Market data before any OTD estimate
3. Written OTD before any in-person visit
4. Read the actual CARFAX PDF — don't trust verbal "clean 1-owner"
5. Never mix used-car and new-car anchors in same email
6. Verify tracker history against Gmail before acting on it
7. Cite only REAL-tagged baseline rows to dealers — synthesized data is internal only

## Self-test

```bash
cd skills/orchestrator
python scripts/skill_smoke_test.py
```

5 checks, <1 sec. Run after any skill edit.

## Limits

Built from one author's NJ 2026-05 buying cycle + 5 synthetic stress tests. State fees, CPO terms, EV credits change — re-verify annually (`last_verified: 2026-05-18`). Not tax, legal, or financial advice. Test on low-stakes scenarios first.
