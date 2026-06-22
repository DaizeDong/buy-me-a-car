---
name: State Fee Lookup
description: Use to look up sales tax rate, doc fee cap, title fee, registration fee, and trade-in credit eligibility for any of 50 US states + DC. Returns the fees in seconds rather than searching DMV websites. Triggers include "what's the doc fee in X", "NJ sales tax rate", "Texas DMV fees", "州的税率", "doc fee cap", "trade-in credit", and Spanish phrase "cual es la tasa de impuesto del estado".
---

# State Fee Lookup

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> last_verified: 2026-05-18
> Scope: narrow per-state fee retrieval. For OTD math see `../otd-calculator/SKILL.md`. For full negotiation/closing flow see `../orchestrator/SKILL.md`.

## Lookup pattern

Given a state code + buyer ZIP, return the 6-field summary:

```
State    : XX
RateBase : N.NNN% (state-level)
RateLocal: N.NN%  (county/city stack at ZIP, 0 if state has no local stacking)
DocCap   : $NNN or "no cap" (statutory legal max)
Title    : $NN
Reg(1yr) : $NN  (sedan/SUV; weight-based variants noted)
TradeCr  : YES / NO / partial
```

## All-state summary

| State | Base rate | Local typ | Doc cap | Title | Reg | Trade credit |
|-------|-----------|-----------|---------|-------|-----|--------------|
| AL | 2% | 2-4% | none | $20 | $30 | Yes |
| AK | 0% | 0-7.5% | none | $15 | $100 | N/A |
| AZ | 5.6% | 1-5% | none | $4 | $50 | Yes |
| AR | 6.5% | 1-5% | none | $10 | $25 | Yes |
| CA | 7.25% | 1-2% | $85 | $25 | $250 | NO |
| CO | 2.9% | 1-5% | none | $7 | $90 | Yes |
| CT | 6.35% (7.75% >$50k) | 0% | none | $25 | $80 | Yes |
| DE | 0% (4.25% doc fee) | 0% | n/a structure | $35 | $50 | N/A |
| DC | 6-9% excise weight | 0% | none | $26 | $70 | Yes |
| FL | 6% | 0.5-2% on first $5k | none | $77 | $225 | Yes |
| GA | 6.6% TAVT one-time | n/a | none | $18 | $20 | Yes (TAVT) |
| HI | 4% GET | 0-0.5% | none | $5 | $45 | Yes |
| ID | 6% | 0-3% | none | $14 | $70 | Yes |
| IL | 6.25% | 0-4.75% | $347 | $155 | $151 | Yes |
| IN | 7% | 0% | $251.05 | $15 | $40 | Yes |
| IA | 6% | 0-1% | none | $25 | $100 | Yes |
| KS | 6.5% | 0-4% | none | $10 | $40 | Yes |
| KY | 6% | 0% | none | $9 | $65 | NO |
| LA | 4.45% | 1-5% | $436 | $69 | $50 | Yes |
| ME | 5.5% | 0% | none | $33 | $35 | Yes |
| MD | 6% | 0% | $800 (eff. July 1 2024) | $499-799 | $135 | Yes |
| MA | 6.25% | 0% | none | $75 | $60 | Yes |
| MI | 6% | 0% | $230 | $15 | $100 | Yes (capped $9k 2025) |
| MN | 6.5% | 0-1.5% | $350 | $11 | $100 | Yes |
| MS | 7% (5% trucks) | 0% | none | $9 | $25 | Yes |
| MO | 4.225% | 0-5.5% | $604.47 | $11 | $50 | Yes |
| MT | 0% | 0% | none | $10 | $90 | N/A |
| NE | 5.5% | 0-2% | none | $10 | $30 | Yes |
| NV | 6.85% | 0-1.5% | none | $29 | $33 | Yes |
| NH | 0% | 0% | $27 | $25 | $90 | N/A |
| NJ | 6.625% | 0% | $799 | $85 | $70 | Yes |
| NM | 4% excise | 0% | none | $5 | $35 | Yes |
| NY | 4% | 4-4.875% | $175 | $50 | $100 | Yes |
| NC | 3% HUT | 0% | $129 | $52 | $36 | Yes (HUT) |
| ND | 5% | 0-3% | none | $5 | $90 | Yes |
| OH | 5.75% | 0.25-2.25% | $250 | $15 | $31 | Yes |
| OK | 4.5% (excise 3.25%) | 0-7% | none | $11 | $96 | Partial |
| OR | 0% | 0% | $250 | $122 | $100 | N/A |
| PA | 6% (8% Philly, 7% Allegheny) | varies by ZIP | none | $58 | $39 | Yes |
| RI | 7% | 0% | $250 | $52 | $30 | Yes |
| SC | 5% IMF cap $500 | 0% | none | $15 | $40 | Yes |
| SD | 4.5% excise | 0-2% | none | $10 | $75 | Yes |
| TN | 7% | 1.5-2.75% | none | $11 | $24 | Yes |
| TX | 6.25% | 0% | $225 | $33 | $50 (+$200 EV) | Yes |
| UT | 4.85% | 1-3% | none | $6 | $44 | Yes |
| VT | 6% | 0% | none | $35 | $70 | Yes |
| VA | 4.15% min $75 | 0-1% | $599 | $15 | $41 | NO |
| WA | 6.5% +MVET | 0.5-3.5% | $200 | $15 | $80 | Yes |
| WV | 6% privilege | 0% | $575 | $15 | $30 | Yes |
| WI | 5% | 0-0.5% | none | $164 | $75 | Yes |
| WY | 4% | 0-2% | none | $15 | $30 | Yes |

## 22 states with detail stubs (one-liner each)

These have ZIP-level or quirk-level breakdowns in `../orchestrator/references/state_fees.md`:

- **NJ** - flat 6.625%, $799 doc cap, no local stacking
- **NY** - 4% + 4-4.875% local, $175 doc cap (2nd strongest US), MCTD $50 NYC
- **PA** - 6% flat except Philly 8% / Allegheny 7%; no doc cap, dealers run high
- **CT** - 6.35% standard, 7.75% luxury tier >$50k
- **MA** - 6.25% flat, no local stacking, $75 title
- **RI** - 7% flat, $250 doc cap, narrow buyer-friendly profile
- **NH** - zero sales tax; any tax line on quote is template leak
- **ME** - 5.5%, excise tax via town based on MSRP age curve
- **VT** - 6% Purchase & Use Tax, simple flat
- **CA** - 7.25% + 1-2% local, $85 doc cap (strongest US), no trade credit
- **TX** - 6.25% MVST flat, $150 doc cap, $200/yr EV surcharge
- **IL** - 6.25% + 0-4.75% local (Chicago 10.25% top US), $347 doc cap
- **FL** - 6% + 0.5-2% on first $5k only, $77 title, no doc cap
- **OH** - 5.75% + 0.25-2.25% local, $250 doc cap
- **NC** - 3% HUT in lieu of sales tax, $129 doc cap
- **GA** - 6.6% TAVT one-time in lieu of sales+ad valorem, no traditional sales tax
- **MI** - 6%, $230 doc cap, trade credit capped at first $9k (2025; rises $1k/yr)
- **VA** - 4.15% SUT min $75, $599 doc cap, NO trade credit
- **WA** - 6.5% + MVET 0.3% + 0.5-3.5% local, $200 doc cap
- **DC** - 6-9% excise by weight class on first $40k MSRP, weight-tiered
- **MD** - 6% flat, $800 doc cap (eff. July 1 2024, raised from $500; now HIGHER than VA's $599 — not a low-doc state)
- **PA-by-ZIP** - Bryn Mawr 19010 / KoP 19406 / West Chester 19380 all flat 6%

## Cross-state titling shortcuts

Tax is paid based on **buyer's residence state**, not dealer state. Common patterns:

| Buyer | Dealer | Tax | Doc |
|-------|--------|-----|-----|
| NJ | NY | NJ 6.625% | NY $175 (better) |
| NJ | PA | NJ 6.625% | PA $499-999 (worse) |
| NJ | DE | NJ 6.625% | DE $299-499 (best) |
| NJ | CT | NJ 6.625% | CT $499-699 |
| PA | NJ | PA 6/7/8% | NJ <=$799 cap |
| PA | DE | PA 6/7/8% | DE typ $299-499 (sweet spot) |
| PA | MD | PA 6/7/8% | MD <=$800 cap (no advantage) |
| CA | NV | CA 8.75-9.5% | NV $499-799 |
| CA | OR | CA 8.75-9.5% | OR ~$115 |
| CA | AZ | CA 8.75-9.5% | AZ $499-799 |
| TX | OK | TX 6.25% | OK $499-799 |
| FL | GA | FL 6% | GA $499-799 |
| NY | NJ | NY 8-8.875% | NJ <=$799 |

Out-of-state dealers should NOT charge their own state's sales tax for cars going out of state. If they try, demand re-quote.

## "Does NOT have" leak detection (gotcha D8)

Dealer CRM templates frequently leak fees from OTHER states. Use these absence lists to catch template bugs:

- **NJ should NOT have**: NY MCTD, CA smog, RI $250 doc cap text, per-battery fee, environmental impact fee, NY $175 doc cap
- **NY should NOT have**: NJ supplemental titling, NJ $799 doc, CT luxury 7.75%, RI $250 doc cap, FL $77 title
- **PA should NOT have**: NJ supplemental titling, NJ $799 doc, NY $175 doc cap, CT luxury 7.75%, RI $250 cap, CA smog
- **CT should NOT have**: per-tire/battery, NJ supplemental titling, NY MCTD, RI $250 doc cap
- **CA should NOT have**: trade-in credit on tax (CA explicitly disallows), NJ doc fees, OR-style zero-tax
- **NH should NOT have**: ANY sales tax line (zero sales tax state)
- **TX should NOT have**: local sales tax (TX is flat 6.25% statewide), CA-style smog fee
- **OR/MT/NH/DE should NOT have**: any sales tax line on the quote

Any of the above appearing on a quote is grounds to demand a full re-quote.

## Worked examples

### NJ — example county
```
RateBase : 6.625%
RateLocal: 0%  (NJ has no local-rate stacking on motor vehicles)
DocCap   : $799 (legal max)
Title    : $85
Reg      : $70
TradeCr  : YES
```

### CA 94703 (Berkeley, Alameda County)
```
RateBase : 7.25%
RateLocal: 2.00% (Alameda 1% + city 0.5% + special 0.5%)
Combined : 9.25%
DocCap   : $85 (strongest US cap)
Title    : $25
Reg      : ~1% of MSRP first year (e.g. $250 on $25k MSRP)
TradeCr  : NO (CA does not grant trade credit)
```

### TX 78704 (Austin, Travis County)
```
RateBase : 6.25%
RateLocal: 0% (TX has no local motor-vehicle sales tax)
DocCap   : $150 (legal max)
Title    : $33
Reg      : $50 + $200/yr EV surcharge
TradeCr  : YES
```

## Links

- Full per-state breakdown (registration formulas, county quirks, dealer-typical practices): `../orchestrator/references/state_fees.md`
- OTD math (forward and reverse) using these fees: `../otd-calculator/SKILL.md`
- Negotiation use of state fees (anchor math, D8 leak detection): `../orchestrator/SKILL.md`
