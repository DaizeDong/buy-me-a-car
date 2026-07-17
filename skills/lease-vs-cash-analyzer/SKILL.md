---
name: Lease vs Cash Analyzer
description: Use to compute lease structure (cap cost / money factor / residual / acquisition / disposition), compare lease total cost vs cash purchase, decide lease vs buy given buyer's ownership horizon, and check captive lender early-buyout policy. Triggers include "lease or buy", "lease 数学", "compute lease monthly", "money factor markup", "lease cash incentive", "lease vs cash break-even", and Spanish phrase "leasing o compra al contado".
---

# Lease vs Cash Analyzer

> **Caveat**: this skill is one author's playbook + 5-scenario stress test. Verify state fees / CPO terms / EV credits / dealer practices against current sources before quoting numbers to a dealer or making financial decisions. Not tax, legal, or financial advice.
> **last_verified**: 2026-05-18 (Phase 3C sub-skill split from orchestrator)

Narrow helper: lease structure math, lease-vs-cash break-even, captive lender
policy lookup. Defers the full theory + worked tables to
`../orchestrator/references/lease_playbook.md`.

## When To Use

- Buyer asks "should I lease or buy?" with a concrete vehicle + horizon
- Need to verify a dealer-quoted lease monthly is honest (MF buy-rate check)
- Need lease-end disposition / early-buyout policy for one OEM captive

> **NOTE, federal §45W lease pass-through is TERMINATED (acquired after 2025-09-30, OBBBA).**
> The "EV buyer fails §30D AGI cap, so route to §45W lease pass-through" play is **dead**
> for any 2026 lease. Lessor captives can no longer capture the federal $7,500 commercial
> credit, so it is not available as cap cost reduction. Any "EV lease credit" a dealer
> advertises in 2026 is ordinary OEM lease cash / marketing money, NOT a federal credit ,
> do not present it as §45W pass-through or count it as a federal incentive. See the
> CRITICAL banner in `ev-buyer-helper`. §45W content below is HISTORICAL only.

## When NOT To Use

- General OTD cash math - delegate to `otd-calculator`
- EV federal credit status / state rebate stacking - delegate to `ev-buyer-helper` first (federal §30D/§25E/§45W all terminated 2025-09-30; state rebates are the only live layer)
- Pure CPO eligibility - delegate to `cpo-eligibility`

## Core Lease Formula

```
Monthly = ((CapCost - Residual) / Term) + (CapCost + Residual) * MF + Tax
```

Variables:

- `CapCost` = MSRP - CapCostReduction - LeaseCash - ManufacturerRebate
              + AcquisitionFee + DealerAddOns
- `Residual` = MSRP * Residual%   (typical 50-65% at 36 mo)
- `MF` = APR / 2400   (money factor; dealer can mark up buy-rate)
- `Term` = 24 / 36 / 39 mo most common

## Money Factor Markup Detection

Always ask the dealer for the BUY-RATE money factor explicitly. If quoted MF
exceeds prevailing captive buy-rate by more than 0.00040 (~ 1% APR), the dealer
is marking up. Markup converts to dealer reserve, paid to dealer monthly over
the lease term. Push back: "what is the buy-rate from {captive} on this
vehicle and tier?" If they refuse to share, assume markup.

## State Tax-on-Lease Mechanics (4 buckets)

| Bucket | States | Mechanics |
|---|---|---|
| Lease-friendly | NJ, FL, CA, NV, WA | Tax on monthly payment only, not on residual buyout |
| Upfront-load (capitalizable) | NY, IL | Full-term tax due at signing; can be capitalized into cap cost |
| Heavy upfront | TX, DC | Tax on FULL cap cost up front, regardless of residual |
| Mixed | most others | Local rules vary; check `state_fees.md` |

For TX/DC the cash-purchase math frequently wins because the lease tax penalty
front-loads ~$3,500-5,000 on a $40k vehicle.

## Lease vs Buy Decision Rules

| Ownership horizon | Mileage | Lean |
|---|---|---|
| < 3 yr | 10-12k mi/yr | Lease often wins (low residual exposure) |
| 3-5 yr | 10-12k mi/yr | Break-even; depends on MF vs cash APR + residual % |
| > 5 yr | any | Buy always wins (lease compounding monthly never stops) |
| any | > 15k mi/yr | Buy wins (excess-mileage penalty $0.15-0.30/mi) |

## EV Lease §45W $7,500 Captured by Lessor, TERMINATED 2025-09-30 (HISTORICAL)

> **No longer available.** OBBBA (Public Law 119-21) terminated the federal §45W
> Commercial Clean Vehicle Credit for any vehicle **acquired after 2025-09-30**, on the
> same date as §30D / §25E. A lessor can no longer capture a federal $7,500 credit on a
> 2026 EV lease, so the lease pass-through below is **$0 of federal money** and must NOT
> be added to cap cost math or presented to a buyer as a federal incentive. Any 2026
> "EV lease credit" line is ordinary OEM lease cash / marketing money, treat it as a
> negotiable OEM incentive, not a federal credit. Retained below for pre-cutoff
> (acquired on/before 2025-09-30) reference only. See the CRITICAL banner in
> `ev-buyer-helper`.

Historically, the lessor (captive finance company) captured the federal Commercial Clean
Vehicle Credit, NOT the lessee. Pass-through varied by OEM (pre-cutoff only):

| OEM | Typical pass-through (HISTORICAL) | Notes |
|---|---|---|
| Hyundai / Kia / GM | Full $7,500 via cap cost reduction | Standard, advertised |
| Toyota / Honda / Ford | $4,500 - $7,500 | Varies by trim, region, promo |
| BMW / MB / Audi | $3,500 - $5,000 | Lowest pass-through |

This was historically useful for EV buyers who failed §30D AGI cap (single > $150k /
MFJ > $300k) or for vehicles that failed §30D MSRP / final-assembly tests (no AGI / MSRP
cap on §45W). All three credits are now terminated, so this routing no longer exists.
See `../orchestrator/references/ev_buyer_playbook.md` § §45W.

## Captive Lender Rules

| Captive | Early buyout | Mileage purchase | Lease assumption |
|---|---|---|---|
| Subaru Motors Finance (SMF) | After 1 payment | $0.15/mi at signing | Allowed; $500 fee |
| Toyota Financial Services (TFS) | After 6 mo | $0.15/mi | Allowed; ~$50 fee |
| Honda Financial Services (HFS) | After 6 mo | $0.15/mi | Allowed |
| Hyundai Capital | Day 1 (most flexible) | $0.20/mi | Allowed |
| Ford Credit | After 6 mo | $0.20/mi | Allowed |
| GM Financial | After 6 mo | $0.25/mi | Allowed |
| Chrysler Capital | After 90 days | $0.25/mi | Allowed |
| BMW Financial | After 4 payments | $0.25/mi | $500 fee |

Disposition fee at lease-end: $350-$495 typical. Often WAIVED if buyer leases
or buys another vehicle from the same OEM within 30 days of return.

Acquisition fee at signing: $595-$895. Sometimes capitalizable, sometimes paid
out of pocket - depends on captive. Always shown on the lease worksheet.

## Lease Cash Conversion Trick

When the manufacturer offers lease cash but no cash-buyer rebate of comparable
size, the lease-then-buyout path captures the lease cash. Pattern:

1. Lease the vehicle for 24 mo with manufacturer lease cash applied as cap
   cost reduction.
2. Confirm captive allows early buyout from day 1 (Hyundai) or after the
   minimum waiting period.
3. Exercise buyout at lease-end residual (or earlier per captive policy).
4. Net cost = (24 mo of lease payments) + (residual buyout) + (taxes per
   state); compare against a hypothetical cash purchase day 0.

Often saves $1,500-$3,500 on Hyundai/Kia/Subaru where lease cash > cash
rebate. Watch for: acquisition fee, disposition fee (waived if you buy out),
and any "lease loyalty" lockouts the captive may apply.

## Worked Example

2026 Ioniq 5 SEL, 36mo / 12k mi lease (2026 acquisition, federal §45W is $0,
TERMINATED 2025-09-30):

- MSRP: $51,150
- Residual (55%): $28,133
- Money factor: 0.00125 (~3.0% APR equivalent)
- Federal §45W pass-through: **$0 (TERMINATED 2025-09-30, not available in 2026)**
- OEM lease cash (if advertised, ordinary marketing money, verify on worksheet): varies;
  treat as a negotiable OEM incentive, NOT a federal credit. Assume $0 for this example.
- Acquisition fee: $650
- Adjusted CapCost: 51,150 + 650 = $51,800

Monthly base = (51,800 - 28,133) / 36 = $657.42
Rent charge = (51,800 + 28,133) * 0.00125 = $99.92
Pre-tax monthly = $757.34

Apply NJ tax (lease-friendly, monthly only) at 6.625%: $50.17
Final monthly: ~$808

> Historical contrast (pre-2025-10-01 acquisition only): with the §45W -$7,500 cap cost
> reduction that used to exist, adjusted CapCost was $44,300, pre-tax monthly ~$540,
> final ~$575. That ~$233/mo gap is the value the now-terminated federal credit used to
> deliver. It is gone for any 2026 lease.

Cash alternative for same buyer:
- MSRP $51,150, negotiated to $48,000, plus TTL ~$3,000 = ~$51,000 OTD
- No federal credit on either side (§30D / §25E / §45W all terminated 2025-09-30)
- 36-mo TCO at lease (2026): 36 * $808 = $29,088 + $0 residual exposure (return car)
- 36-mo TCO at cash: $51,000 - resale ~$30,000 = $21,000 net depreciation

Without the federal credit the lease's monthly is much higher, so cash purchase now
generally wins on 36-mo TCO and clearly wins at 6+ years. Check live state rebates
(via `ev-buyer-helper`) as the only remaining incentive layer.

## Cross-References

- `../orchestrator/references/lease_playbook.md` - full formulas, residual
  tables by OEM, region-specific MF charts, all 50-state tax mechanics
- `../orchestrator/references/ev_buyer_playbook.md` § §45W commercial credit
  - full pass-through tables and lessor list (HISTORICAL: §45W terminated 2025-09-30;
  see `ev-buyer-helper` CRITICAL banner, no federal lease credit on 2026 acquisitions)
- `../orchestrator/references/state_fees.md` - state TTL components for the
  cash-comparison side
- `../orchestrator/SKILL.md` Critical Rule #4 - never quote a lease monthly
  to the buyer without showing the MF + residual + cap cost breakdown

## Output Contract

After every lease analysis, return to the operator:

```
Lease vs Cash analysis - <timestamp>
  Vehicle: <year make model trim>, MSRP $<n>
  Lease offer:
    Term: <n> mo / <n>k mi
    MF: 0.<nnnnn> (buy-rate <n>.<n>0%, markup <yes/no>)
    Residual: <n>% = $<n>
    CapCost (adjusted): $<n>
    Monthly (pre-tax): $<n>
    Monthly (with state tax): $<n>
  Cash alt: $<n> OTD, 36mo NPV $<n>
  Verdict: LEASE / BUY / BREAK-EVEN
  Captive policy: early buyout <when>, disposition $<n>
```
