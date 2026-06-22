---
name: Trade-in Valuator
description: Use to valuate the buyer's trade-in vehicle (KBB / private party / wholesale / dealer allowance), compute state trade-in tax credit, handle lien payoff timing, and decide separate-sell vs trade-in. Triggers include "valuate my trade", "what's my Civic worth", "KBB vs private party", "trade-in tax credit", "lien payoff", "评估置换车", "卖给 dealer 还是私卖".
---

# Trade-in Valuator

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.

last_verified: 2026-05-18

Narrow-trigger skill: produce a defensible trade-in valuation, decide
separate-sell vs trade-in, and stage lien-payoff timing. Defers full reference
content to `../orchestrator/references/trade_in.md` and state-specific tax
mechanics to `../orchestrator/references/state_fees.md`.

## When to invoke

User says any of: "valuate my trade", "what's my Civic worth", "KBB vs private
party", "trade-in tax credit", "lien payoff", or the CN triggers in the
frontmatter. Skip this skill if there is no trade (Phase 1 trade gate = NO).

## 5-anchor valuation framework

Per `../orchestrator/references/trade_in.md` Section 1: every trade vehicle has
four book/market valuations -- and for **EVs and PHEVs, a fifth anchor: battery
State of Health (SoH)**. Capture every applicable anchor at Phase 1 --
misreading them is the #1 source of buyer loss in trade-in deals.

| # | Anchor | What it is | Typical relationship | Role |
|---|---|---|---|---|
| 1 | KBB Instant Cash Offer | Real cash a participating dealer will pay TODAY, no negotiation | Lowest of the four (dealer floor) | Walk-floor outside option. Any dealer trade offer below this is asking buyer to subsidize. |
| 2 | KBB Trade-In Value (Fair condition mid) | KBB book trade-in value at stated condition | $600-$1,300 above KBB Instant Offer | Mid; fair dealer trade target. Use as primary anchor. |
| 3 | KBB Private Party Value | What buyer can realistically sell for on Craigslist / FB Marketplace | $1,500-$3,000 above KBB Trade-In; transacts 7-14 days for clean 1-owner | Upper bound; the price the buyer trades convenience for. |
| 4 | Wholesale (Manheim MMR / Black Book) | Dealer auction acquisition floor | Lowest; dealer-internal | Internal benchmark only; buyers rarely see MMR. Estimate ~5-10% below KBB Instant Offer for popular models. |
| **5** | **Battery State of Health (SoH)** -- **EV/PHEV only** | **Verified pack capacity retention (%) from OBD-II / dealer scan / mfr app -- NOT the dashboard range estimate** | **Cross-cutting modifier on anchors 1-4, not a standalone $ figure** | **The dominant EV factor: for a used EV the pack is the most expensive component, so SoH moves resale more than paint/trim/often mileage. Books usually ignore it -- so treat books as a soft ceiling and adjust for SoH.** |

Also useful: NADA Trade-In Clean is often $300-$700 above KBB Trade-In on
popular Hondas/Toyotas; treat as higher-of-two-books anchor when negotiating.

### Anchor 5 -- battery SoH (EV/PHEV trades)

For any EV or PHEV trade, books (KBB/NADA/Black Book) systematically miss the
battery: they often apply **no SoH adjustment**, lag fast EV price swings by
months, and lump EVs onto an ICE depreciation curve. So anchors 1-4 are
necessary but not sufficient -- layer SoH on top. Approximate market behavior
(verify; no rigid formula -- dealers apply an invisible adjustment table):

| SoH band | Effect vs. a healthy peer (same model/age/miles) |
|---|---|
| 90-95%+ | Premium / supports book |
| ~85-89% | Roughly book; minor or no deduct |
| ~80-84% | Begins to discount |
| < ~80% | Market discounts ~10-20% |
| < ~70% | Steep discount; hard to move |

Magnitudes seen in market commentary (verify): 92% vs. 82% SoH on a 5-yr-old EV
can differ **$3,000-$5,000**; below ~82% SoH add another **$2,000-$5,000** risk
discount; **non-transferable factory battery warranty ≈ another ~$5,000 of
discount**, while transferable remaining warranty is a buyer premium lever.

- **Get VERIFIED SoH**, not the dash "guess-o-meter" (that's based on recent
  driving, not pack capacity). OBD-II scan / third-party battery report / dealer
  scan. Math: a 75 kWh pack now holding 64 kWh = ~15% loss.
- **Bring the SoH report to the negotiation proactively** -- a healthy-pack
  report supports premium pricing; silence lets the desk assume worst-case.
- **PHEVs:** smaller pack → smaller absolute swing, same direction; a PHEV that
  no longer holds meaningful EV-only range gets discounted toward an equivalent
  hybrid/ICE.

> **§ 25E is a separate transaction.** The federal Used Clean Vehicle Credit
> (IRC § 25E, up to $4,000) attaches to the buyer **purchasing** a qualifying
> used EV, NOT to the EV being **traded away**. Its $25,000 price cap is
> measured **before** trade-in value, so a big trade allowance does not slip a
> car under the cap. Full mechanics (price cap, MY≥2yr, dealer point-of-sale
> transfer + IRS ECO reporting, MAGI caps, repeal after 2025-09-30) live in
> `../orchestrator/references/ev_buyer_playbook.md` § 25E and `trade_in.md`
> Section 13e. Do not conflate the two.

## Capture-all-four checklist (12 fields)

Per trade_in.md, the prior 6-field placeholder is insufficient. At Phase 1
capture: (1) Year/make/model/trim, (2) Mileage, (3) Title status, (4) Lien
holder + payoff balance, (5) Key count, (6) Cosmetic issues, (7) Mechanical
issues, (8) KBB Instant Cash Offer + screenshot, (9) KBB Trade-In Value at
stated condition, (10) KBB Private Party Value, (11) NADA Trade-In Clean,
(12) Wholesale estimate (MMR or Black Book if available). **EV/PHEV adds
(13) verified battery SoH % + report source (OBD-II / dealer scan / mfr app) +
report date, and (14) does the factory battery warranty transfer to the next
owner? (Y/N + remaining term).**

## State trade-in tax credit matrix

Excerpt from `../orchestrator/references/state_fees.md`. In states allowing
trade credit, sales tax applies to NET (sale price minus trade allowance), not
gross.

| Trade credit status | States |
|---|---|
| YES (full, uncapped) | NJ, NY, PA, TX, OH, NC, GA, WA, DC, MD, FL |
| YES (capped first $10k) | IL |
| YES (capped first $9k) | MI |
| NO | CA, KY, VA |
| N/A (no sales tax on vehicles) | OR, MT, NH, AK, DE |

Worked example -- NJ $25k sale + $10k trade:
- Tax base = $25,000 - $10,000 = $15,000
- NJ sales tax 6.625% on $15k = $993.75
- Without trade credit: 6.625% on $25,000 = $1,656.25
- Trade credit saves $662.50

Same deal in CA (no credit): tax base stays $25k, savings = $0. Move the trade
to a separate private-party sale if the state-loss is large.

## Separate-sell vs trade-in decision

Decision rule:

- Private-party premium = (KBB Private Party) - (Dealer Trade Allowance)
- Trade-credit value = (Trade Allowance) * (State combined tax rate, if credit)
- If private-party premium > trade-credit value + buyer's convenience price
  ($1,000-$3,000 typical), sell separately.
- Else trade in.

In NJ at 6.625% with a $15k trade allowance vs $17k private party: premium =
$2,000; trade-credit value = $993; net cost of trading = $2,000 - $993 = $1,007.
If buyer values convenience > $1,007, trade in; otherwise sell separately.

In CA same numbers: premium $2,000; trade-credit value $0. Sell separately
almost always wins.

## Lien payoff workflow

Per trade_in.md Section 4 (a-d):

| When | Step | Detail |
|---|---|---|
| T-7 days | Request 10-day payoff letter from lien holder | Letter states exact dollar amount valid through a date 10 days out. Some lien holders charge a $25 admin fee. |
| T-3 days | Dealer cuts payoff check, overnights to lien holder | Clearance typically 5-10 business days. Get a copy of the check + tracking number from dealer F&I. |
| T+0 (delivery) | Title transfer pending lien release | Dealer holds title work until lien release arrives. Buyer drives away on temp tag. |
| T+14-30 | Lien release filed with state DMV | New title issued to dealer (or assigned to next buyer). Confirm release was filed; some lien holders are slow. |

If payoff balance > trade allowance (underwater trade): the difference is rolled
into the new loan principal (cheapest financing) OR paid out of pocket. Disclose
to dealer at Phase 1 -- hiding negative equity blows up Phase 9.

## High-mileage trap

For vehicles over 100,000 miles:
- KBB Instant Cash Offer often returns "no offer" or unrealistically low.
- Private party is the realistic-only path; expect 14-30 days on market.
- If buyer cannot wait, accept dealer wholesale offer is essentially MMR.

## Separate-the-negotiation 5-round protocol

NEVER let the dealer shell-game sale price against trade allowance.

1. Round 1: Agree the new-car OTD (no trade mentioned). Lock in writing.
2. Round 2: Introduce trade. Ask for dealer's blind trade offer.
3. Round 3: Compare dealer offer to KBB Instant Cash Offer (anchor #1). If
   dealer offer < KBB Instant Cash Offer, push back with the KBB screenshot.
4. Round 4: Target KBB Trade-In Value (anchor #2). Acceptable landing zone:
   anywhere between KBB Instant Cash Offer and KBB Trade-In.
5. Round 5: If dealer drops new-car OTD to "compensate" for low trade, reject.
   The lock from Round 1 stands; trade allowance is its own line.

Per orchestrator gotcha D5: NEVER mix new vs used anchors. Used desk and new
desk have different incentive structures; mixing closes off negotiation.

## Trade-walk gotchas

- Unknown mechanical issues (CEL on, transmission slip, AC weak): request a
  1-2 week PPI window. Dealers will undervalue $1,000-$3,000 to cover risk.
  Independent shop inspection ($150) often saves more than it costs.
- Aftermarket modifications (lift, wheels, audio, tune): KBB does NOT count
  them. Dealers undervalue or refuse. Either restore stock parts and sell those
  separately, or accept the hit.
- Cosmetic damage: dealer deducts $200-$500 per item (curb rash per wheel,
  paint chip, dent). Touch-up + wheel refurb pre-trade is high-ROI if buyer has
  time.
- Missing 2nd key: $200-$500 deduct. Get key cut+programmed pre-trade
  ($150-$300) when worth it.

## Cross-references

- `../orchestrator/references/trade_in.md` -- full reference (4-anchor table,
  12-field capture, lien payoff details, ACV vs trade allowance; **Section 13 =
  EV/PHEV battery-SoH trade discount + § 25E annotation**).
- `../orchestrator/references/ev_buyer_playbook.md` -- **EV/PHEV source of
  truth**: battery health, § 30D ($7,500 new) and § 25E ($4,000 used) credits,
  charging/range, EV dealer tactics. Use for the buyer's *acquisition* of a used
  EV (§ 25E); this skill's anchor 5 covers the *outgoing* EV trade.
- `../orchestrator/references/state_fees.md` -- per-state Trade-In Tax Credit
  column, worked OTD examples with trade.
- `../orchestrator/SKILL.md` gotcha D5 -- never mix new vs used anchors.

## Output contract

```
Trade valuation pass -- <timestamp>
  Vehicle: <Y/M/M/T, miles, condition, powertrain: ICE/HEV/PHEV/BEV>
  Anchors: KBB-Instant $X / KBB-Trade $Y / KBB-Private $Z / NADA $N
  Battery (EV/PHEV only): SoH <%> via <OBD-II/dealer/app> on <date>;
    warranty transfers? <Y/N, term>; SoH adj to book: <+/-$ or band note>
  Lien: $payoff balance, holder, 10-day letter on file? (Y/N)
  State: <ST>, trade credit: <YES/NO/CAP>
  Tax savings if traded: $<amount>
  Decision: TRADE-IN vs SEPARATE-SELL (with reasoning)
  Walk-floor: $<KBB Instant Offer>
  Negotiation target: $<KBB Trade-In Value>
```

Hand off to Phase 6 negotiation when traded; hand off to private-party listing
help when separate-sell.
