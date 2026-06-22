# Lease Structure Playbook

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)
> **Data refresh schedule**: state rates / CPO programs / EV incentives / lease parameters should be re-verified annually or upon any user-cited deal that contradicts. The 2026-05-18 timestamp marks last full audit.

Comprehensive lease mechanics for buyers considering leasing as an alternative to financing or cash purchase. Covers core math, captive-lender rules, EV-specific lease arbitrage, lease assumption, and mileage tactics.

This file is the source of truth for any "should I lease?" question; for the `cash → lease conversion` trick on the rebate side, see `payment_methods.md`. **NOTE: the EV-specific lease arbitrage of the $7,500 §45W commercial credit is DEAD — §45W is TERMINATED for vehicles acquired after 2025-09-30 (OBBBA / P.L. 119-21). See § 8 and `ev_buyer_playbook.md` for the terminated-credit details; do not count any §45W pass-through in current lease math.**

## 1. Core Lease Math — Field Definitions

A lease quote without all five core fields is incomplete and unactionable. Demand all five in writing before scoring.

| Field | Definition | Typical range |
|---|---|---|
| **Capitalized Cost (Cap Cost)** | The agreed-upon sale price of the vehicle that the lease is built on. This is the negotiable number — equivalent to "sales price" on a purchase. Includes acquisition fee if rolled in. | Negotiated; often MSRP minus dealer discount minus rebates minus lease cash. |
| **Residual Value** | The vehicle's projected wholesale value at lease end, expressed as % of MSRP. Set by the captive lender, NOT negotiable. Higher residual = lower monthly payment. | 24 mo: 65-75% MSRP; 36 mo: 55-65%; 39 mo: 52-60%; 48 mo: 45-52%. Toyota / Lexus / Subaru / Porsche residuals run 3-7 points higher than industry average; Mazda / Mitsubishi / Stellantis (Jeep / Ram / Dodge / Chrysler) run 3-7 points below. |
| **Money Factor (MF)** | The lease equivalent of interest rate, expressed as a small decimal (e.g., 0.00150). **MF × 2400 = approximate APR** (e.g., 0.00150 × 2400 = 3.6% APR). Captive's "buy-rate" MF is the wholesale rate; dealer can mark up (see § 4). | Tier 1+ credit on captive: 0.00080 - 0.00250 (1.9% - 6% APR equivalent). Non-captive bank lease (Ally / US Bank / Chase): 0.00250+ typical. |
| **Term** | Lease length in months. | 24 / 27 / 36 / 39 / 48. 36 mo is most common. 39 mo is a "stretch" — same residual as 36 mo at some captives, lower monthly. 24 mo lets you pull a higher residual but doesn't always beat 36 mo monthly. |
| **Mileage Allowance** | Annual miles included; over-mileage charged at end. | 10k / 12k / 15k / 18k / 20k. 12k default; 15k for commuters. 7,500/yr "low-miles" leases exist at some captives, lower monthly. |

## 2. Standard Lease Fees

These appear on most lease contracts. Know which are mandatory and which are negotiable.

| Fee | Range | Negotiable? |
|---|---|---|
| **Acquisition fee** | $595 - $895 (Toyota / Honda / Subaru ~$595-$650; BMW / Mercedes / Audi ~$795-$925; Hyundai / Kia ~$650; GM ~$595) | Generally NOT negotiable — set by captive lender. Can be capitalized (rolled into Cap Cost — increases monthly) or paid up front. |
| **Disposition fee** | $350 - $495 | NOT negotiable, charged at lease END if buyer doesn't purchase or re-lease. Waived if buyer purchases vehicle at lease end OR signs another lease/purchase from same captive within ~6 months (loyalty rule). |
| **Security deposit** | 0 - 1 month payment | Often waived (Tier 1+ credit). Some captives offer "MSDs" (Multiple Security Deposits) — pay 5-9 refundable MSDs up front, captive reduces money factor by 0.00007-0.00010 per MSD. BMW Financial historically the leader; effective MF reduction 0.00040 - 0.00080. Not all captives offer. |
| **First month payment** | 1 monthly payment | Always required at signing. |
| **DMV / title / registration** | State-specific | Per `state_fees.md` — usually capitalized. |
| **Doc fee** | Per state cap | Per `state_fees.md` § doc fee caps. |
| **Sales tax** | State-specific (see § 3) | See § 3. |

## 3. Monthly Payment Formula

```
Depreciation  = (Cap Cost - Residual) / Term
Rent (finance) = (Cap Cost + Residual) × Money Factor
Monthly       = Depreciation + Rent + Tax
```

### Worked example — 2026 Toyota RAV4 XLE Hybrid AWD 36-month lease

- MSRP $36,500; negotiated Cap Cost $34,200 (after $1,500 discount + $800 lease cash from TFS).
- Residual at 36 mo / 12k miles: 60% of MSRP = $21,900.
- Money Factor: 0.00150 (3.6% APR equivalent).
- Term: 36 months.

```
Depreciation  = (34,200 - 21,900) / 36 = $341.67
Rent          = (34,200 + 21,900) × 0.00150 = $84.15
Pre-tax monthly = $425.82
```

State tax handling differs (see § 3.1 below). At NJ 6.625% on monthly:

```
Tax-included monthly = 425.82 × 1.06625 = $454.04
```

### 3.1 State-by-state lease tax handling

| State | Tax mechanism | Implication |
|---|---|---|
| **NJ** | Tax on monthly payment + tax on optional lease-end buyout | Standard. Monthly stays modest; if you buy out at lease end, pay 6.625% on residual. |
| **NY** | Tax up-front on sum-of-all-payments at signing (lump-sum at signing) | At signing, write a check for tax on (monthly × term). NY $3,200 lease for 36 mo @ $400/mo: 8.875% × $14,400 = $1,278 tax at signing. Captives let you capitalize this into Cap Cost (rolls into monthly, but you pay interest on the tax — adds ~$30-40 over 36 mo). |
| **CA** | Tax on monthly payment only; tax on cap reductions (down payment) up-front | If you put $3,000 down, you pay 7.25-10.25% on that $3,000 at signing. Monthly tax applies normally. **Lease buyout: tax on residual at buyout time, separate from monthly tax.** |
| **TX** | **Tax up-front on full Cap Cost at signing** (treats lease as a sale for tax purposes) | The single worst state for leasing. TX 6.25% on $35k Cap Cost = $2,188 tax at signing. Plus tax-again on $0 at lease end (no further tax). Many TX dealers obscure this; demand "first-pay" + "drive-off" sheet. |
| **FL / NV / WA** | Tax on monthly payment only | Standard. |
| **IL** | Tax on cap reductions + tax on monthly (effective: tax on full cap cost over lease term + tax on residual at buyout) | Heavy. Often more than TX over a 36-mo period. |
| **MA / CT / PA / OH / VA / NC / GA / MI / WI** | Tax on monthly | Standard. |
| **DC** | DC excise tax up-front on cap cost (similar to TX) | Up-front load; not common to lease in DC. |

**Rule of thumb**: NJ / FL / CA / NV / WA = lease-friendly tax states. NY / IL = up-front load (capitalize-able). TX / DC = up-front lump-sum, lease economics significantly worse than nominal monthly suggests.

## 4. Money Factor Markup — Demand the Buy-Rate

The captive sets a "buy-rate" MF for each credit tier. The dealer can mark up the MF that's quoted to the buyer by up to ~0.00040 (≈ 0.96% APR) on most captives (some allow more). The markup is dealer reserve / kickback from the captive — pure dealer profit, no service to the buyer.

**Counter language (paste-ready)**:

> *"Please confirm the buy-rate money factor on this lease (Tier 1+ credit). I'm asking because dealer mark-up on MF is standard practice and I'd like to be at buy-rate, not marked-up. If your captive's current Tier 1+ MF is 0.00080 and you've quoted 0.00150, that's a 0.00070 markup = $39/month over 36 months × $35k Cap Cost — please reset to buy-rate."*

Buy-rate references:

- **Edmunds Lease Forums** ("Ask Edmunds for Money Factor") — Edmunds users post current buy-rate MF + residual by make / model / trim / region / term / miles, refreshed monthly. Free, no login. Single best source.
- **LeaseHackr Forums** — high-signal lease buyer community; deal-of-the-month threads cite buy-rate.
- **CarsDirect "current lease incentive" pages** — manufacturer-disclosed lease cash + MF estimates.

Pull buy-rate from Edmunds Lease Forum before opening lease negotiation; cite it in writing in your first counter.

### 4.1 Money factor markup — captive-by-captive limits

| Captive | Typical MF markup ceiling | Notes |
|---|---|---|
| Toyota Financial Services (TFS) | 0.00040 | Aggressive markups common in TX / FL volume markets. |
| Honda Financial Services (HFS) | 0.00040 | Standard. |
| Subaru Motors Finance (SMF, serviced by Chase) | 0.00050 | Chase admin layer makes MF slightly opaque; demand the Subaru.com lease estimator screenshot. |
| Hyundai Capital | 0.00075 (high) | Hyundai/Kia historically allow more markup; demand buy-rate harder. |
| Kia Finance | 0.00075 (high) | Same. |
| Ford Credit | 0.00040 | Standard. |
| GM Financial | 0.00040 | Standard. |
| BMW Financial Services | 0.00040 | Plus MSD program reduces effective rate. |
| Mercedes-Benz Financial Services | 0.00040 | Plus MSD program. |
| Audi Financial Services | 0.00040 | Plus MSD program (more limited than BMW). |
| Lexus Financial Services | 0.00040 | Same family as TFS, similar dynamics. |
| Stellantis Capital (Jeep/Ram/Chrysler/Dodge) | 0.00050 | Stellantis residuals already weak; MF markup compounds the disadvantage. |
| Mazda Financial Services (serviced by Toyota) | 0.00040 | Mazda residuals already weak. |

## 5. Lease Cash Incentive Flow — The Cash-to-Lease Conversion Trick

Manufacturer **lease cash** (sometimes called "Lease Cash", "Lease Loyalty", "Captive Lease Allowance") is rebate money the OEM gives to the captive lender, who then passes it through to the lessee as a **Cap Cost reduction**. Lease cash often exceeds purchase cash incentives by $500-$3,000.

**The conversion trick**: If you're a cash buyer and the captive is offering lease cash > purchase cash, the math sometimes favors:

1. Sign the lease, capture the lease cash via Cap Cost reduction.
2. Buy out the lease immediately at the residual + tax + early-payoff calculation (varies by captive — see § 6).
3. Net cost can be lower than the pure-cash purchase by the lease-cash differential, MINUS lease admin costs (acquisition fee + early-buyout fee + tax-twice in some states).

**Decision math** (paste-ready calculation):

```
Cash purchase OTD                                = $35,000 (Cap Cost) + tax + doc + reg
Lease-then-buyout OTD                            = Cap Cost - $2,000 lease cash + $895 acq fee
                                                   + (1-3 months of monthly while waiting for
                                                   buyout) + early-buyout admin fee + tax-twice
                                                   in NJ/CA/TX
Net advantage of conversion                       = lease_cash - acq_fee - (months × monthly)
                                                   - admin_fee - extra_tax_if_state_taxes_twice
```

State-by-state pass-through nuances:

- **NJ**: Tax on monthly + tax on buyout = effectively tax-twice on the depreciation portion. Conversion only wins if lease_cash > acq_fee + extra_tax + 1-2 months payments.
- **CA**: Tax on monthly + tax on residual at buyout = also tax-twice. Same calculus.
- **TX**: Tax up-front on full Cap Cost; buyout taxed only on early-buyout admin amount. Conversion sometimes wins big because the up-front tax is on the REDUCED Cap Cost (after lease cash).
- **FL / NV / WA**: Tax on monthly only; buyout is on residual untaxed (FL untaxed; NV / WA tax on buyout). Conversion math is favorable if lease cash > $1,000.

**Run the math at Phase 2 baseline** if lease cash > $1,500 on the target VIN, even for cash buyers. The conversion is often the single highest-leverage incentive lever, but state tax mechanics determine whether it actually wins.

## 6. Captive-Lender Rules by Manufacturer

Each captive has different early-buyout, mileage purchase, lease assumption, and disposition fee policies. Know your captive before signing.

| Captive | Early buyout penalty | Mileage purchase rate | Lease assumption | Disposition fee | GAP coverage |
|---|---|---|---|---|---|
| **Subaru Motors Finance** (Chase-serviced) | Residual + remaining payments (no discount); admin fee $250 | $0.10-0.15/mile pre-purchased at signing; $0.15/mile end-of-lease | Allowed via Swapalease / LeaseTrader; $595 transfer fee; co-signer credit check; residual + MF unchanged | $300 | Standard (included) |
| **Toyota Financial Services** | Residual + early-payoff discount applied via "lease-end settlement" formula; admin fee $300 | $0.15/mile pre-purchase at signing; $0.20/mile end | Allowed; $300 transfer fee; new lessee credit check | $350 | Included on TFS lease only; not on purchase |
| **Honda Financial Services** | Residual + early-payoff penalty (~3-5% of remaining rent); admin fee $250 | $0.15/mile pre-purchase; $0.20/mile end | Allowed; $350 transfer fee | $350 | Included |
| **Hyundai Capital** | Residual + remaining payments × 50% (50% discount on rent portion); admin fee $200 | $0.15/mile pre-purchase; $0.25/mile end | Allowed; $400 transfer fee | $400 | Included |
| **Kia Finance** | Same as Hyundai Capital (same parent) | Same | Same | Same | Included |
| **Ford Credit** | Residual + remaining payments (no discount); admin fee $200 | $0.15/mile pre-purchase; $0.20/mile end | Allowed; $300 transfer fee | $395 | Optional add-on |
| **GM Financial** | Residual + remaining payments (no discount); admin fee $200 | $0.20/mile pre-purchase; $0.25/mile end (high) | Allowed; $375 transfer fee | $495 (highest among mainstream) | Optional add-on |
| **BMW Financial Services** | Residual + early-payoff calc (3% of remaining); admin fee $250 | $0.20/mile pre-purchase; $0.25/mile end | Allowed; $500 transfer fee + dealer concurrence | $350 | Included |
| **Mercedes-Benz Financial Services** | Residual + early-payoff calc; admin fee $300 | $0.20/mile pre-purchase; $0.25/mile end | Allowed; $595 transfer fee | $595 | Included |
| **Audi Financial Services** | Residual + remaining payments; admin fee $300 | $0.20/mile pre-purchase; $0.25/mile end | Allowed (limited); $500 transfer fee | $495 | Included |
| **Lexus Financial Services** | Same as TFS | Same as TFS | Same as TFS | $350 | Included |
| **Stellantis Capital** (Jeep / Ram / Chrysler) | Residual + remaining payments; admin fee $250 | $0.15/mile pre-purchase; $0.25/mile end | Allowed; $395 transfer fee | $450 | Optional |

**Wear-and-tear handling at lease end**: All captives perform a pre-return inspection (~30 days before lease end). Standard wear (door dings <2 inches, tire wear within tread, interior <coin-sized stains) is forgiven. Damage beyond wear: documented and billed. Common over-charges: tire replacement (if tread <4/32), windshield chips, body panel dents > 2 inches. **Pre-emptive fix is almost always cheaper than captive's billed price**: e.g., tire set independent $600 vs captive $1,200; windshield independent $300 vs captive $850.

## 7. Lease vs Buy Decision Math

Quick decision: under what conditions does leasing beat buying?

### Lease usually WINS when:
- Buyer plans to drive vehicle 2-4 years (matches lease term)
- Buyer drives 10k-12k miles/year (within standard allowance)
- Money factor's APR-equivalent < buyer's actual purchase APR (e.g., MF 0.00080 = 1.92% APR, vs purchase auto loan 6.5%)
- Lease cash > purchase cash (e.g., $2,500 lease cash vs $1,000 purchase cash)
- Buyer values the option to walk away at lease end (e.g., uncertain about depreciation, residual risk, or future life changes)
- High-residual brand (Toyota / Lexus / Subaru / Porsche / Honda) where residual is 5-7 points above market projection — captive eats the depreciation risk
- Buyer can deduct lease payments as business expense (mileage method vs actual expense — leasing more favorable for high-cost vehicles used >50% business)

### Buy usually WINS when:
- Buyer plans to keep vehicle 5+ years (lease's "rent the depreciation" math no longer applies)
- Buyer drives 15k+ miles/year and won't pre-purchase miles (overage fees stack)
- Low-residual brand (Mazda / Stellantis / Mitsubishi) where leasing transfers extra depreciation cost to the buyer via MF rent
- Buyer has cash and wants to avoid the acquisition fee + disposition fee + interest costs ($1,500-$3,000 total on a 36-month lease)
- Buyer wants to modify the vehicle (paint, tint > 35%, lift, wheels — lease prohibits permanent modifications)
- Buyer wants high mileage flexibility (no over-mileage exposure)

### Worked decision example — 2026 Honda CR-V EX-L

| Scenario | Lease | Buy (6.5% APR, 60 mo, 20% down) |
|---|---|---|
| Cap Cost / Sale Price | $33,500 | $33,500 |
| Acquisition / Doc + tax | $695 acq + tax-on-monthly | doc + tax up-front |
| Residual @ 36 mo / 12k | $20,100 (60%) | N/A |
| MF / APR | 0.00130 (3.1%) | 6.5% |
| Monthly | $375 (pre-tax) | $552 (incl. interest) |
| 36 mo total cost | $13,500 (lease) + drive-off ~$2,000 + disposition $350 = $15,850 | $19,872 (3 yrs of payments out of 5 + $6,700 down) |
| Remaining asset (after 36 mo) | $0 (walk away) OR buyout $20,100 | Vehicle equity worth ~$22,000 retail; loan balance $14,200; net equity ~$7,800 |
| 5-yr net cost | ~$26,000-$30,000 (lease then lease again) | ~$33,100 (total payments, then own outright) |

If buyer keeps the bought CR-V for 8-10 years total, buy clearly wins. If buyer turns over every 3 years, lease wins by $3-5k cumulatively.

## 8. EV Lease Structure — Federal Commercial Vehicle Credit Pass-Through — TERMINATED 2025-09-30 (HISTORICAL)

> ## ⚠️ CRITICAL — THE §45W LEASE LOOPHOLE IS CLOSED (as of 2026-06)
>
> OBBBA (Public Law 119-21, signed 2025-07-04) **terminated §45W** for any vehicle **acquired
> after 2025-09-30**, on the same date as §30D/§25E. Lessor captives can **no longer** capture a
> $7,500 commercial credit on a current EV lease, so the historical "lease to capture the credit
> you can't get on purchase" arbitrage **no longer exists**.
>
> **For any current (2026) EV lease: do NOT count a §45W pass-through in Cap Cost reduction,
> conversion math, or any net-cost calculation.** Any lease cash an OEM offers today is ordinary
> manufacturer lease cash (§ 5), not a federal credit. Source: IRS Clean Vehicle Credit Fact Sheet
> (2025-05) + OBBBA (P.L. 119-21). The mechanics below are retained as **HISTORICAL** reference
> for pre-cutoff (on-or-before 2025-09-30) lease acquisitions only.

Historically (while §45W was live): the Inflation Reduction Act § 30D (purchase) required income caps, MSRP caps, and domestic assembly. The § 45W (commercial vehicle credit) did NOT — and lessor captives qualified for the full $7,500 on lease deals because the captive was the legal owner. **This was the EV lease trick (now dead).**

Many ineligible-for-§30D vehicles (foreign-assembled EVs, MSRP > $80k SUVs, high-income buyers) WERE eligible if leased. The captive captured the $7,500 and chose how much to pass through to the lessee as Cap Cost reduction.

**Pass-through rate by OEM (HISTORICAL — all $0 for vehicles acquired after 2025-09-30):**

| OEM / Captive | Pass-through 2024-2026 | Notes |
|---|---|---|
| **Hyundai Capital** (Ioniq 5 / Ioniq 6 / Kona EV) | $7,500 full pass-through | Most aggressive; advertised heavily |
| **Kia Finance** (EV6 / EV9 / Niro EV) | $7,500 full pass-through | Same as Hyundai |
| **GM Financial** (Equinox EV / Blazer EV / Silverado EV / Cadillac LYRIQ) | $7,500 typical full | Some lease promotions stack additional GM lease cash on top |
| **Ford Credit** (Mach-E / F-150 Lightning) | $4,500 - $7,500 (varies by model + month) | Less consistent than HMG/GM |
| **Tesla** (Model 3 / Y / S / X) | Tesla does not transparently disclose; effective pass-through historically $5,000-$7,500 via monthly reduction | Tesla leases are non-buyout (forced return at end) — major drawback |
| **Toyota Financial** (bZ4X) | $5,000 - $7,500 (less aggressive than HMG) | Toyota historically conservative on EV incentives |
| **Honda Financial** (Prologue) | $5,000 - $7,500 | Same as Toyota |
| **BMW / Mercedes / Audi** | $3,500 - $5,000 typical (less aggressive — premium brand captives keep more credit) | iX / EQS / Q4 e-tron leases — luxury captives capture more |
| **Stellantis Capital** (Wagoneer S / Charger Daytona EV) | $7,500 typical | Aggressive — Stellantis pushing EV adoption |

**Practical implication (HISTORICAL):** While §45W was live, for an ineligible-for-§30D buyer (foreign EV, high income, MSRP > caps), leasing then buying out (per § 5) was often the only way to capture the $7,500 credit. **This no longer applies — §45W is terminated, so there is no federal credit to capture via lease for any current purchase. Do not run §45W conversion math on a 2026 EV lease.** (The cash-to-lease conversion in § 5 still works for ordinary OEM *lease cash*, just not for a federal credit.)

**Lease-only restriction on some leases**: A handful of captive lease deals have non-purchase clauses (lease MUST be returned at end, no buyout) — Tesla is the notable example. (This mattered for the now-dead §45W conversion play; still worth confirming buyout-allowed if any lease-cash conversion is the goal.)

Cross-reference `ev_buyer_playbook.md` (Federal Credits) for the underlying § 30D vs § 45W rules — **all now terminated as of 2025-09-30.**

## 9. Lease Assumption (Transfer to Another Party)

Lease assumption is the process of transferring an active lease to a third party who takes over the remaining payments. Most captives allow it; mechanics:

- **Listing services**: Swapalease.com, LeaseTrader.com — the two dominant marketplaces. Average listing fee $90-$130 to seller. Buyers browse free.
- **Transfer fee**: $300-$595 (captive-by-captive — see § 6 table). Paid by either party (negotiable).
- **Credit check on assumee**: All captives require the assumee to pass the same credit tier the original lessee did. If assumee fails, no transfer.
- **Original lessee liability**: Most captives release the original lessee fully on transfer (BMW, MB, Toyota, Honda, Hyundai, Kia, Ford, GM all release). A few keep "secondary liability" (Chrysler / Audi historically — verify current policy at signing).
- **Residual / MF stay the same**: The assumee inherits the original lease terms. Cannot renegotiate MF or residual on transfer.
- **Common reason to assume**: Cash incentive on listing — original lessee pays the assumee $1,500-$5,000 to take over remaining payments, often because lessee's life circumstances changed (moved, job change, sold a second car). For an assumee, this is below-market-rate leasing.
- **Common reason to list**: Avoid the early-buyout penalty (see § 6 — which is often $5,000-$15,000 on a 36-month lease 24+ months in). Lease assumption is cheaper than early buyout in 90%+ of cases.

**Practical buyer use**: If buyer is "lease-curious" and wants a 12-18 month commitment instead of 24-39, browsing Swapalease for an assumption with 12-18 months remaining is often the cheapest entry point into a luxury lease (BMW / MB / Audi). Effective cost-per-month = monthly + (transfer fee / months remaining) ≈ $30-$45/mo overhead.

## 10. Walk-Away Mileage vs Mileage Purchase

Mileage handling at lease end:

| Scenario | Cost / mile | When to use |
|---|---|---|
| **Walk-away overage** | $0.15 - $0.30/mile (varies by captive; § 6 table). Subaru / Toyota / Honda / Ford / Stellantis: $0.20 typical. GM / Hyundai / Kia: $0.25 typical. BMW / MB / Audi: $0.25-$0.30. | Default — pay at lease end if a few hundred miles over. |
| **Pre-purchase miles at signing** | $0.10 - $0.20/mile (40-50% cheaper than walk-away). Often only refundable if NOT used (some captives refund, some keep — verify). | If you know at signing you'll drive 14k/yr but lease only allows 12k, pre-purchase the 6,000 mile overage (3 yrs × 2k extra/yr). Saves $400-$800 over 36 months. |
| **Mid-lease miles purchase** | Some captives allow buying additional miles mid-lease at a price between pre-purchase and walk-away (e.g., $0.13/mile). Most don't. | Limited use. |

**Decision rule**: If buyer drives ≥15k/yr but quoted lease has 12k/yr allowance, pre-purchase miles at signing OR step up to 15k allowance (often only $10-$15/mo more). Walk-away at $0.20+/mile compounds: 9k miles over = $1,800+ at lease end.

## 11. Lease Cap Cost Reduction vs Monthly Reduction — Where to Apply Money

When the buyer has cash to put into a lease, it can flow into:

1. **Cap Cost Reduction** (= effective down payment on a lease) — directly reduces the capitalized cost. Lowers depreciation AND rent portion of monthly. Best mathematical move.
2. **Multiple Security Deposits (MSDs)** — reduces MF (rate). Refundable at lease end IF no over-mileage / wear charges. Best when MF is high and credit is good.
3. **First month / drive-off fees** — flat one-time payments. No leverage.

**Rule of thumb**: Avoid putting more than first-month-plus-fees down on a lease.

- If vehicle is totaled in month 1 with $5,000 Cap Cost reduction, GAP refunds the lender but DOES NOT refund the $5,000. Lost.
- Same $5,000 invested in MSDs is refundable at lease end (assuming lease completes normally).
- Same $5,000 left in buyer's bank account = liquidity for the next car cycle.

The classic dealer pitch — "put $4,000 down to lower your monthly to $299 instead of $410" — is a poor financial move except when (a) lease cash from OEM exists in the form of a manufacturer-mandated Cap Cost reduction (in which case buyer doesn't actually pay, the OEM does), or (b) buyer is in a tax state that benefits from Cap Cost reduction not being taxable (rare).

## 12. Lease-End Options

T-90 days before lease end, captive sends pre-return inspection notice. Buyer's options:

| Option | Best when | Mechanics |
|---|---|---|
| **Walk away (return)** | Vehicle is at or under mileage; market value ≈ residual | Schedule return at any same-brand dealer. Pay disposition fee. Done. |
| **Buy out (purchase)** | Market value > residual + tax + admin fee | Pay residual + sales tax (state-dependent — NJ / CA / NY tax buyout; TX / FL no double tax) + admin fee ($150-$400). Captive sends payoff letter; finance via captive, CU, or cash. |
| **Sell to 3rd party (lease equity sale)** | Market value MUCH > residual; lessee has positive equity | NOTE: Many captives in 2024+ tightened rules to prohibit 3rd-party buyouts (Ally, Honda, Hyundai have done this since 2022; allow only lessee or same-brand dealer). Verify in lease contract before relying on this option. Where allowed, sell to CarMax / Carvana — they pay residual to captive, buyer gets equity check. |
| **Re-lease (lease pull-ahead)** | Brand is offering pull-ahead incentives (manufacturer credits last 3-6 months of payments as incentive to sign a new lease) | Common 2-4 months before end. Captive waives final payments if lessee re-leases same brand. |
| **Lease extension** | Need 1-6 more months; new vehicle not yet available | Extend monthly @ current rate, month-to-month, up to 6 months. Some captives charge $50/mo admin fee. |

## 13. Decision Workflow Tied to Phase 1

When financing gate fires (Phase 1 buyer-type router), ask one more sub-question: **"Loan or lease?"** If lease, this playbook applies.

Phase 1 lease-specific sub-questions (in addition to financing 9-field set):

1. **Annual miles** — single most important lease input. Cap allowance bands.
2. **Term preference** — 24 / 27 / 36 / 39 / 48 mo.
3. **Plan after lease** — keep (buyout) / return (walk-away) / re-lease / unsure.
4. **Down payment posture** — § 11 default is $0 down beyond drive-off; ask if buyer wants Cap Cost reduction (mostly NO) or MSDs (limited captives).
5. ~~**Conversion-eligible?** — if EV, ineligible-for-§30D direct purchase, $7,500 lease pass-through applies (per § 8).~~ **HISTORICAL — §45W terminated 2025-09-30; no federal $7,500 lease pass-through on any current EV. Do not ask or factor this for 2026 purchases.**
6. **Pre-purchase miles?** — if estimated annual > allowance, recommend pre-purchase (per § 10).

Save to `criteria.md` as a sub-section under the Financing block.

Phase 6 lease-specific counter framework (in addition to standard OTD ask):

1. Demand buy-rate Money Factor (paste § 4 language).
2. Demand current residual % (cite Edmunds Lease Forum if dealer's quote is below market).
3. Confirm Cap Cost = MSRP - manufacturer discount - lease cash - dealer discount; reject "Cap Cost = MSRP" quotes outright (a common opening tactic).
4. Confirm acquisition fee is the captive's standard (§ 2 table), not a dealer markup.
5. Demand all lease incentives in writing (lease cash, loyalty, conquest, military, college grad — refresh monthly).
6. ~~Run conversion math for EV leases (§ 8).~~ **HISTORICAL — no §45W credit to capture on current EV leases; evaluate any EV lease on ordinary lease cash / MF / residual only.**

## 14. When Not to Lease

Common scenarios where leasing is structurally wrong:

- **Driving > 18k miles/year** consistently. Lease overage compounds; 20k buyer pays $2,400/yr in overage (12k allowance × $0.20 over).
- **Vehicle modifications planned** — lifts, tint, paint, wheel/tire upgrades, performance mods. Lease prohibits. Removing at lease end = damage charges.
- **Sub-prime credit** (FICO < 650) — MF markups extreme (often 0.00600+ = 14.4% APR), monthly becomes punitive. Buy a used vehicle with sub-prime auto loan instead.
- **Brand with weak residual** (Mazda / Stellantis / Mitsubishi / non-Honda Korean ICE) — lease math worse than purchase even at same APR, because MF is built on full Cap Cost + low Residual.
- **Buyer wants to skip GAP / wear coverage** — these are bundled into most captive leases at the captive's discretion. Cannot opt out on most.
- **Buyer's state taxes lease unfavorably** (TX / DC / IL up-front tax states) — see § 3.1. Lease economics worse than nominal suggest.

For these buyers, route back to financing or cash purchase per Phase 1 Buyer-Type Router.

## 15. References and Cross-Links

- `payment_methods.md` — Lease conversion (cash-to-lease) inline trick; Captive-vs-CU rebate playbook.
- `ev_buyer_playbook.md` — Federal §30D / §25E / §45W rules (**all TERMINATED for vehicles acquired after 2025-09-30 per OBBBA — historical only**); state EV rebates (still live); lease-then-buyout EV mechanics (historical, §45W-dependent).
- `state_fees.md` — State-specific lease tax handling; doc cap; trade-in credit (does NOT apply to leases in most states).
- `negotiation_playbook.md` — OTD math (cash) — does not include lease math; this file is the source of truth.
- `outreach_strategy.md` — Lease-specific first-touch email language; cross-bid leverage when both lease + purchase incentives exist.

## 16. Glossary

- **Cap Cost (Capitalized Cost)** — agreed-upon sale price the lease is built on.
- **Cap Reduction** — money applied to reduce Cap Cost (down payment on a lease).
- **MF (Money Factor)** — lease rate, MF × 2400 = approximate APR.
- **Residual** — projected end-of-lease value, set by captive, in % MSRP.
- **Acquisition fee** — captive's lease setup fee, $595-$895.
- **Disposition fee** — captive's lease-end return fee, $350-$595.
- **MSD (Multiple Security Deposit)** — refundable deposits that lower MF, BMW pioneered.
- **Lease cash** — manufacturer rebate that flows to lessee as Cap Cost reduction.
- **Buy-rate MF** — captive's wholesale MF; dealer can mark up 0.00040-0.00075.
- **§ 45W** — federal commercial vehicle EV tax credit, historically captured by lessor (**TERMINATED for vehicles acquired after 2025-09-30 per OBBBA — historical only**).
- **§ 30D** — federal personal EV tax credit, historically captured by buyer on purchase (**TERMINATED for vehicles acquired after 2025-09-30 per OBBBA — historical only**).
- **Pull-ahead** — manufacturer waives 2-4 final lease payments if lessee signs new lease early.
- **Walk-away** — return vehicle at lease end with no buyout.
- **Buyout** — purchase vehicle at lease end for residual + tax.
- **Wear-and-tear inspection** — captive's pre-return assessment of vehicle condition.

last_verified: 2026-05-18
