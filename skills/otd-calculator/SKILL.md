---
name: OTD Calculator
description: Use to compute out-the-door (OTD) cost from sale price + state + fees, or reverse-engineer a sales price ceiling from a target OTD. Handles trade-in tax credit if state grants it. Triggers include "compute OTD", "OTD math", "what's my OTD", "reverse OTD to sale price", "算 OTD", "算总价", and any sale-price-vs-OTD disambiguation question.
---

# OTD Calculator

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> last_verified: 2026-05-18
> Scope: narrow OTD math only. For full negotiation flow see `../orchestrator/SKILL.md`. For state fee data see `../state-fee-lookup/SKILL.md`.

## Core formula (forward: Sale -> OTD)

```
Taxable = Sale + Doc  (in most states; CA is a notable exception, see gotchas)
Tax     = Taxable * (StateRate + LocalRate)
OTD     = Sale + Doc + Tax + Title + Reg + Other
```

`Other` covers tire/battery/environmental fees, EV reg surcharge, lien recording, and any add-ons that survived F&I. Should be a short itemized list, not a black box.

## Reverse formula (target OTD -> Sale ceiling)

Given a target OTD you will pay, solve for the maximum Sale price you can accept:

```
Sale = (TargetOTD - Doc * (1 + Rate) - Title - Reg - Other) / (1 + Rate)
```

Where `Rate = StateRate + LocalRate`. Doc is taxed in most states, hence the `(1 + Rate)` factor on Doc inside the bracket. Verify per-state in the state-fee-lookup skill.

## Trade-in case

In states granting trade-in tax credit (most; CA, KY, DC do NOT), trade value reduces the taxable base:

```
Taxable = (Sale + Doc - Trade)
```

Forward with trade:
```
OTD = Sale + Doc + (Sale + Doc - Trade) * Rate + Title + Reg + Other
```

Reverse with trade (solve for Sale given target OTD):
```
Sale = (TargetOTD + Trade*Rate - Doc*(1+Rate) - Title - Reg - Other) / (1+Rate)
```

If state does NOT grant credit, drop the `Trade` term from the taxable base.

## State quick rates (15 most-common)

| State | Combined typical | Doc cap | Title | Reg (1yr) | Trade credit |
|-------|------------------|---------|-------|-----------|--------------|
| NJ | 6.625% | $799 | $85 | $70 | Yes |
| NY | 8.875% (NYC) / 8% (most) | $175 | $50 | $100 | Yes |
| PA | 6% (8% Philly, 7% Allegheny) | none | $58 | $45 | Yes |
| CT | 6.35% (7.75% >$50k) | none | $25 | $80 | Yes |
| MA | 6.25% | none | $75 | $60 | Yes |
| CA | 8.75-9.5% (combined) | $85 | $25 | ~1%/yr MSRP | NO |
| TX | 6.25% (no local) | $225 | $33 | $50 + $200 EV | Yes |
| FL | 6-7.5% (combined) | none | $77 | $225 | Yes |
| IL | 7.5-10.25% (combined) | $347 | $155 | $151 | Yes |
| OH | 6-7.5% (combined) | $250 | $15 | $31 | Yes |
| MI | 6% | $230 | $15 | $100 | Yes capped 9k (2025) |
| GA | 6.6% TAVT one-time | none | $18 | $20 | Yes (on TAVT) |
| WA | 8-10% (combined) | $200 | $15 | $80 | Yes |
| MD | 6% | $800 | $100 | $135 | Yes |
| VA | 4.15% min $75 | $599 | $15 | $41 | NO |

Full 50-state + DC data: `../orchestrator/references/state_fees.md`.

## Worked examples

### Example 1: NJ example county, cash buyer, no trade

Sale $25,000, Doc $499, NJ 6.625%, Title $85, Reg $70.

```
Taxable = 25000 + 499 = 25499
Tax     = 25499 * 0.06625 = 1689.31
OTD     = 25000 + 499 + 1689.31 + 85 + 70 = 27343.31
```

### Example 2: CA Alameda 94703, trade-in, financed

Sale $28,000, Trade $8,000, Doc $85 (CA cap), CA combined 9.25% (Bay Area). CA does NOT grant trade credit.

```
Taxable = 28000 + 85 = 28085  (trade IGNORED - CA rule)
Tax     = 28085 * 0.0925 = 2597.86
Title   = 25
Reg     = ~280 (~1% of MSRP first year)
OTD     = 28000 + 85 + 2597.86 + 25 + 280 = 30987.86
```

Trade still reduces cash-out-of-pocket by $8,000 but not the tax bill.

### Example 3: TX Austin 78704, EV, no trade

Sale $32,000, Doc $150 (TX cap), TX 6.25% (no local), Title $33, Reg $50, EV surcharge $200/yr.

```
Taxable = 32000 + 150 = 32150
Tax     = 32150 * 0.0625 = 2009.38
Other   = 200 (EV reg premium)
OTD     = 32000 + 150 + 2009.38 + 33 + 50 + 200 = 34442.38
```

## Common gotchas

- **Doc-fee taxability**: most states tax Doc. CA explicitly does not. Florida varies by dealer. When in doubt assume taxed (conservative for buyer in reverse math).
- **Local rate stacking**: about 35 states have local tax. Use the buyer's residence ZIP, not dealer ZIP - the state collects tax based on registration address.
- **EV registration premium**: TX +$200/yr, IL +$100/yr, OH +$200/yr, WA +$225/yr. Adds to `Other`.
- **CA trade-in**: never reduces tax. KY and DC same. All others usually do.
- **GA TAVT**: 6.6% one-time title ad valorem tax in lieu of sales+ad valorem. Trade reduces TAVT base.
- **NC HUT**: 3% Highway Use Tax in lieu of sales tax; doc capped at $129.
- **NH/OR/MT/DE no sales tax**: any sales-tax line on a quote to these buyers is a template leak - demand re-quote.
- **MD doc cap**: $800 effective July 1 2024 (cap history $200 -> $300 -> $500 -> $800; older references citing $300/$499/$500 will mislead). MD's $800 cap is now HIGHER than VA's $599 - MD is no longer a low-doc state.

## Python helper

Use the existing script for forward or reverse math across all 50 states + DC:

```bash
# Forward: Sale -> OTD
python ../orchestrator/scripts/otd_calculator.py \
    --sales 25000 --state NJ --doc 499 --forward

# Reverse: target OTD -> Sale ceiling
python ../orchestrator/scripts/otd_calculator.py \
    --target 27500 --state NJ --doc 499

# CA with local stacking
python ../orchestrator/scripts/otd_calculator.py \
    --sales 28000 --state CA --doc 85 --local 2

# List all 50 states + their default rates / doc caps
python ../orchestrator/scripts/otd_calculator.py --list-states
```

Flags: `--target` (reverse) OR `--sales --forward`; `--state` two-letter code; `--doc` doc fee; `--local` extra local percentage (e.g. `1` = 1% extra); `--title --reg --addons` overrides.

## Sale vs OTD disambiguation

If a dealer quote or buyer message is ambiguous (e.g. "out the door at $28,000"), default to OTD interpretation and confirm. The classic trap: dealer says "$27,500" meaning Sale, buyer hears OTD, $1,800 surprise at signing. Always pin OTD explicitly in writing before any deposit.

## Links

- Full state fee table + cross-state titling math: `../orchestrator/references/state_fees.md`
- State-by-state lookup skill (narrower scope, faster): `../state-fee-lookup/SKILL.md`
- Negotiation playbook (escalation ladder, ADM kills): `../orchestrator/references/negotiation_playbook.md`
