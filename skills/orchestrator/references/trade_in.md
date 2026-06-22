# Trade-In Reference

> **last_verified**: 2026-05-18 (skill stress test iteration 5 + P0-P5 consolidation)

This reference covers used-vehicle trade-in mechanics: valuation methodology, the ACV-vs-trade-allowance distinction, the separate-the-negotiation rule, state-specific trade-in tax credit interactions, payoff handling, lien release timing, and key-count and cosmetic-deduct mechanics.

Loaded from SKILL.md Phase 1 trade-in router branch when the buyer answers YES to the trade-in gate. Also referenced from Phase 6 negotiation when trade is in play, and Phase 9 closing for paperwork.

---

## 1. Trade Valuation Methodology — Four Anchors

A trade-in vehicle has at least four distinct valuations. Misreading them is the #1 source of buyer loss in trade-in deals. Always capture all four during Phase 1.

| Anchor | What it is | Typical relationship | Use |
|---|---|---|---|
| **Manheim wholesale floor (MMR)** | Dealer's auction acquisition cost; the absolute floor | Lowest of the four | Internal benchmark only; buyers do not usually see MMR. Estimate: ~5-10% below KBB Instant Offer for popular models. |
| **KBB Instant Cash Offer** | Real cash a participating KBB dealer will pay TODAY, no negotiation | Slightly above wholesale floor; treated as dealer-walk-in floor | **Buyer's walk-floor outside option.** The CR-V buyer's $11,200 KBB Instant Offer is the no-negotiation alternative; any dealer trade offer below this is asking the buyer to subsidize. |
| **KBB Trade-In Value (Fair condition mid)** | KBB's "book" trade-in value at the buyer's stated condition | $600-$1,300 above KBB Instant Offer for most popular models | Fair dealer trade-in target. Use for negotiation anchor. |
| **KBB Private Party Value** | What the buyer can realistically sell to a private party on Craigslist/FB Marketplace | $1,500-$3,000 above KBB Trade-In; transacts 7-14 days for clean 1-owner | Upper-bound; the price the buyer trades convenience for. |

Also useful:
- **NADA Trade-In Clean** — often $300-$700 above KBB Trade-In on popular Hondas/Toyotas; treat as the higher-of-two-books anchor when negotiating
- **Black Book Wholesale** — close to MMR; mostly dealer-internal

### Capture all four at Phase 1

The prior P1 trade-in placeholder (6 inline fields: vehicle, miles, condition, payoff, keys, expected) is insufficient. Use the **12-field set**:

| # | Field | Purpose |
|---|---|---|
| 1 | Year/make/model/trim | Identify VIN |
| 2 | Mileage | Anchor depreciation comp |
| 3 | Title status (clean / branded / salvage) | Eligibility for trade |
| 4 | Lien/payoff (and current balance) | Net cash flow to buyer |
| 5 | Key count | $200-$500 deduct if missing 2nd key |
| 6 | Cosmetic issues (curb rash, dents, paint) | $150-$1,000 deduct typical |
| 7 | Mechanical issues (CEL, transmission, AC, suspension) | $200-$3,000 deduct or walk |
| 8 | **KBB Instant Cash Offer** (with screenshot/URL) | **Walk-floor anchor #1** |
| 9 | **KBB Trade-In Value** at stated condition | **Fair dealer trade anchor #2** |
| 10 | **KBB Private Party Value** | **Outside-option anchor #3** |
| 11 | **Estimated Manheim wholesale floor** | Internal sanity-check anchor |
| 12 | **State trade-in tax credit posture** (yes / no / partial / capped) | Affects OTD math by 5-10% of trade allowance |

This is the structured set referenced from SKILL.md Phase 1.

---

## 2. ACV vs Trade-Allowance Distinction (the shell-game trade)

**ACV (Actual Cash Value)** = what the dealer would actually pay at auction for the trade. This is the dealer's internal number, usually 2-5% above MMR. The dealer rarely says ACV out loud.

**Trade allowance** = the headline number the dealer offers on the paperwork. It can be **inflated above ACV** and offset by a matching **sale price markup**.

### Example shell-game

Dealer says: "We'll give you $13,000 for your trade and the car is $27,500."
Dealer's internal ACV on trade: $11,000
Dealer's actual desired sale price: $25,500

Both deals net the same to the dealer ($14,500 gross), but the buyer thinks the trade is generous because the headline number is $13,000.

### Counter: SEPARATE THE NEGOTIATION

**The rule:** Negotiate sale price WITHOUT mentioning the trade, then introduce the trade as a separate transaction AFTER the sale price is locked in writing.

Phase 6 sequence:
1. Email/call dealer: "What is your best OTD on this VIN with no trade?"
2. Lock the sale price + tax + doc + title + reg in writing
3. THEN say: "I also have a 2018 Civic LX 67k mi clean 1-owner. What is your best trade allowance? KBB Instant Offer for this VIN is $X."
4. If dealer raises sale price after introducing trade: walk back to step 2, re-lock sale price, do not let them shell-game.

This is the **single most important Phase 6 rule** for trade-in buyers. Codify in any prep file when trade is in play.

### How to detect the shell game

After the dealer quotes trade + sale together, compute:
```
Implied ACV = headline trade allowance - (sale price - sale price you were quoted no-trade)
```

If implied ACV is far below KBB Trade-In, the trade allowance is shell.

---

## 3. State Trade-In Tax Credit Matrix

Most states give a tax credit on the net (sale - trade) instead of taxing the full sale. This saves the buyer **(combined tax rate) × (trade allowance)** in tax.

Quick reference (full table in `state_fees.md`):

| State | Trade-in tax credit | OTD impact on $12k trade |
|---|---|---|
| NJ | Yes | -$795 tax (6.625%) |
| NY | Yes | -$960-$1,065 tax (8-8.875%) |
| PA | Yes | -$720-$960 tax (6-8% with Philly) |
| **CA** | **NO — CA does NOT grant trade-in tax credit** (CDTFA taxes gross sale price; trade is a separate transaction). See `references/state_fees.md` for authoritative posture. | $0 savings; full sale taxed regardless of trade |
| TX | Yes | -$750 tax (6.25%) |
| IL | Yes (capped at $10k of trade through 2024; $10k cap continues 2025+ — verify current legislation) | -$700-$870 tax |
| CT | Yes | -$762-$930 tax (6.35-7.75%) |
| MA | Yes | -$750 tax (6.25%) |
| KY | No | $0 savings; full sale taxed |
| DC | No | $0 savings; full sale taxed |
| **CA** (listed twice for emphasis) | **No** | $0 savings; full sale taxed |
| MT, NH, OR, DE, AK | N/A (no sales tax) | N/A |

**States that do NOT grant trade-in tax credit** (full sale price taxed regardless of trade): **CA, KY, DC**, plus VA via the SUT 4.15% structure historically (verify per `state_fees.md`), and MD partial-handling historically. **`references/state_fees.md` is the source of truth** for the trade-in tax credit column; if there is ever a conflict between this matrix and `state_fees.md`, defer to `state_fees.md`.

**Always quantify the trade-in tax credit in writing in the Phase 6 OTD ask.** Dealers sometimes "forget" to apply it (or use a CRM template that doesn't apply it automatically) in states where it IS granted. **In CA**, the opposite gotcha applies: a dealer CRM template from a trade-credit state (NJ/NY/IL/TX) leaking into a CA quote may incorrectly show a trade-credit reduction the buyer is NOT legally entitled to; this looks like a "free $1,000+" but it will be reversed at CDTFA filing — the buyer ends up owing the back tax. Force-correct CA quotes to gross-sale-price tax base per `state_fees.md` CA detail stub.

---

## 4. Payoff Handling (Trade with Outstanding Loan)

If the trade vehicle has an active loan, the workflow changes:

| Scenario | Buyer action |
|---|---|
| **Loan balance < trade allowance** (positive equity) | Dealer pays off lien, buyer gets difference applied to new sale OR refunded cash |
| **Loan balance > trade allowance** (negative equity / underwater) | Buyer must (a) bring cash to cover gap, OR (b) roll negative equity into the new loan (worsens financing math; only acceptable with strong APR), OR (c) sell private-party first and pay off separately |
| **Loan balance ≈ trade allowance** (washed) | Dealer pays off lien; buyer brings $0 trade equity to the deal |

**Critical:** Get the **current payoff quote in writing from the lien-holder** within 10 days of close. Payoff balances change daily with interest accrual. The dealer pays the lien-holder directly via wire/check at close.

Capture at Phase 1:
- Lien-holder name
- Current balance (from a recent statement)
- Per-diem interest (usually $2-$8/day on used-car loans)
- Payoff quote validity period (usually 10 days)

If buyer states "loan paid off, title in hand," verify title physically exists in buyer's possession before assuming. Lost titles require a duplicate from DMV (~$25-$30 fee, 2-3 weeks).

### 4a. Trade-in with active lien — full workflow

When the trade has an outstanding loan, the buyer is exposed to a 3-4 week window between dealer-side payoff dispatch and lien-holder release. Mechanical workflow:

**Step 1 — Payoff verification (T-10 to T-7 days before close)**
- Buyer calls lien-holder DIRECTLY (NOT through dealer). Dealer's quoted payoff is sometimes a stale month-old figure or a dealer-side estimate; only the lien-holder's official payoff is binding.
- Request **10-day payoff letter** in writing (PDF or fax). This is the lien-holder's guaranteed payoff amount valid for 10 days.
- Capture: lien-holder name, current balance, per-diem interest accrual ($1-$8/day depending on rate), payoff valid-through date, lien-holder's wire/check receipt instructions.
- If lien-holder is a captive (Ford Credit / Ally / Toyota Financial / GM Financial / Honda Financial Services / Capital One Auto / Chase Auto): payoff process is standardized; 10-day letter via online portal or 800-number request.
- If lien-holder is a community bank or credit union: may require an in-branch visit to get the letter; allow extra 1-2 days.
- **Auto-pay cancellation**: Cancel auto-pay on the lien-holder's account BEFORE close. Auto-pay continues for 1-2 cycles post-close otherwise, charging the buyer's account for a loan that's been paid off.

**Step 2 — Dealer-side payoff timing (T-0 close day through T+10)**
- Most franchise dealers will cut a check to the lien-holder within 1-5 business days of close. Some same-day-wire-capable F&I departments wire payoff within 24-48 hours.
- Get **written confirmation** at close of:
  - Payoff amount the dealer will send
  - Routing instructions (check vs wire)
  - Date dealer commits to send payoff
  - Sales contract clause indicating the dealer is responsible for any per-diem interest accruing beyond the payoff date due to delay
- If dealer is small (independent or low-volume franchise), confirm capability before deposit. Some small dealers route payoff through their bank's overnight clearance which takes 5-10 business days from close.

**Step 3 — Lien-holder receipt + release (T+5 to T+30)**
- Lien-holder receives dealer's payoff check/wire
- Lien-holder posts payoff to loan account (1-3 business days)
- Lien-holder mails lien release documentation to dealer (5-21 business days)
- Lien release arrives at state DMV (varies; in IL through Secretary of State; in NJ through MVC); state updates title (5-15 business days)
- **Total window**: 14-30 days from close before the buyer's name is fully off the lien-holder's books.

**Step 4 — Buyer post-close monitoring**
- Day 5 post-close: Call dealer F&I; confirm payoff has been sent.
- Day 10 post-close: Call lien-holder; confirm payoff received and applied.
- Day 14 post-close: Watch for lien release confirmation by mail.
- Day 21 post-close: Final lien-holder call. Confirm loan account is fully closed; request closure letter (some states require this for resale-of-trade workflow).
- Day 30 post-close: If still pending, escalate. Per-diem interest is accruing if lien-holder hasn't received payoff yet; dealer is on hook per the close-day contract clause.

### 4b. Title in hand vs title with lien-holder (close-day risk)

Most state DMVs require the title at close. With an active lien:
- **Title physical location**: held by lien-holder (most states; NY/MN/PA/MD/KY are exceptions — buyer holds title with lien notation)
- **Close-day workflow**:
  - Buyer brings the lien-holder's 10-day payoff letter (not the title itself, which the lien-holder holds)
  - Dealer prepares the trade-in paperwork with payoff routing
  - State DMV issues the new vehicle's registration via the dealer; OLD trade title processed through lien-release once payoff clears
  - Buyer drives the new vehicle from the lot with new temp-tag / 30-day permit
- **Risk window**: Buyer no longer owns the trade (dealer does, contractually) BUT buyer's name remains on the old lien-holder's records until lien release processes. If buyer needs to take action on the trade pre-lien-release (refinance, sell elsewhere, etc.), they can't — the trade is dealer-owned but lien-encumbered.

### 4c. Lien payoff routing dispute (rare but real)

If the dealer-quoted payoff differs from the lien-holder's 10-day payoff letter:
- Dealer's quote is usually low by $50-$300 (missed a per-diem interest cycle or a late fee). Resolve in favor of the lien-holder's letter.
- Buyer must NOT cover the gap. The dealer pays the lien-holder's actual payoff; if it's higher than dealer-quoted, that's the dealer's miscalculation, not the buyer's.

### 4d. Phase 6 questions to ask dealer (in writing) when trade has lien

Mandatory questions before deposit on any trade-with-lien deal:

1. "Lien-holder: [name]. Payoff balance per 10-day letter: $[X]. Confirm you can pay off [lien-holder] directly via [wire/check] at close."
2. "What's the dealer-side timing on payoff dispatch — within 1 day, within 5 days, or within 10 days?"
3. "If lien-holder takes longer than 14 days to release lien, who covers any per-diem interest delta?" (Dealer should answer: dealer covers.)
4. "Provide written confirmation of payoff dispatch date and routing on the bill of sale."
5. "Confirm [registering state, e.g., IL] trade-in tax credit applied correctly to the trade ALLOWANCE (not the net-of-payoff)." (Important: IL/NJ/NY/PA trade-in tax credit applies to gross trade allowance, BEFORE lien payoff deduction. Some dealer CRMs incorrectly apply credit to net equity, costing buyer $200-$700. **NOTE: CA does NOT grant trade-in tax credit at all** per `state_fees.md` — if registering in CA, ask instead: "Confirm tax base equals the gross sale price; no trade-credit reduction shown.")

---

## 5. Lien Release Timing

When the buyer's trade has a lien, the new dealer typically:

1. Inspects trade and confirms allowance at close
2. Wires payoff to lien-holder same-day or next business day
3. Lien-holder mails lien release to dealer (5-14 days typical)
4. Dealer registers the now-clean trade for resale OR sends to auction

Buyer is **not** on the hook for the trade after close — the dealer owns the trade once paperwork signs. But the buyer's name stays on the old loan's lien until the lien-holder processes the release. Set a calendar reminder for day 21 post-close to verify with the old lien-holder that the loan is fully closed.

**Common gotcha:** Auto-pay on the old loan keeps charging the buyer's account for 1-2 months post-close. Cancel auto-pay manually before close.

---

## 6. Key Count Check

| Configuration | Trade impact |
|---|---|
| 2 keys (both fobs working) | Standard; $0 deduct |
| 1 key + 1 valet | $100-$200 deduct |
| 1 key only | $200-$400 deduct (depending on make; Honda/Toyota replacement fob ~$250) |
| 0 keys (lost both) | $400-$700 deduct + dealer must re-key |
| Programmer/key for push-button start vehicles | Higher: Honda HR-V/CR-V smart key replacement $300-$500 |

Verify key count before quoting trade. A "2 keys" buyer who shows up with 1 key gets re-quoted at close.

---

## 7. Cosmetic Deductions

Standard dealer deducts (estimates; varies by vehicle and region):

| Issue | Typical deduct |
|---|---|
| Curb rash on 1 wheel | $50-$150 |
| Curb rash on 2+ wheels | $150-$400 |
| Door ding (golf-ball-sized) | $75-$200 each, PDR-able |
| Hood ding / deeper dent | $200-$500 |
| Paint scratch (key, surface, sub-clearcoat) | $100-$300 PDR / $400-$1,500 panel respray |
| Cracked windshield | $300-$600 (rock chip $50-$100) |
| Headlight oxidation | $50-$100 (polish service) |
| Interior wear / stains | $100-$400 detail |
| Cigarette smoke smell | $500-$1,500 deduct (ozone + replace cabin filter) |
| Aftermarket wheels (non-OEM) | $0-$500 deduct depending on quality |

The CR-V buyer's "minor curb rash on 2 wheels" suggests $150-$400 deduct — already roughly baked into KBB Instant Offer condition assessment.

---

## 8. Separate the Negotiation — The Tactical Sequence

This is the load-bearing rule. Worth its own section.

### Phase 6 sequence with trade

1. **Round 1 (no trade mentioned):**
   > Subject: 2022 CR-V EX-L AWD VIN xxx — written OTD request
   >
   > Hi [Sales rep], I am a cash buyer in [ZIP], ready to close this week. What is your best OTD on this VIN with no trade? Please itemize sales price, doc, [state] [rate]% tax, title, reg, any add-ons. No financing, no trade in this number.

2. **Round 2 (counter sale price only):**
   Apply Cold Open recipe (regional anchor + named comp + in-flight signal + soft ceiling + deadline) — see `negotiation_playbook.md`. Lock sale price in writing.

3. **Round 3 (introduce trade as separate transaction):**
   > Thanks, that lands. Separately, I also have a 2018 Civic LX Sedan 67k mi clean 1-owner, 2 keys, clean title in hand. KBB Instant Offer on this VIN is $X (attached screenshot, valid through [date]). What is your best trade allowance? I would like to keep the sale-price OTD we agreed on regardless.

4. **Round 4 (verify dealer didn't shell-game the sale):**
   Compare the post-trade-introduction quote against the locked Round 2 OTD. Sale price MUST be identical. If dealer raises sale price after introducing trade, walk back to "We agreed on $X sale price; please re-quote with the trade on that locked sale price."

5. **Round 5 (state trade-in tax credit verification):**
   For trade-credit states, verify the OTD line items show:
   ```
   Sale price: $X
   - Trade allowance: -$Y
   = Taxable base: $X - $Y
   × State combined rate
   = Tax
   ```
   NOT:
   ```
   Sale price tax: $X × rate (taxing full sale)
   - Trade allowance: -$Y (flat credit after tax)
   ```
   The first is correct (trade-in tax credit applied). The second leaves money on the table. **Demand the correct math in writing.**

---

## 9. Outside Option: KBB Instant Offer (the walk-floor mechanism)

KBB Instant Cash Offer is the buyer's leverage. For any popular brand (Honda, Toyota, Subaru, Mazda compact/midsize sedans and SUVs 2015-2022), it consistently lands within 5-10% of MMR and is honored by KBB-participating dealers for 7 days.

**Pre-Phase-6 workflow:**
1. Buyer pulls KBB Instant Cash Offer at kbb.com
2. Screenshots the offer (VIN, value, expiration date)
3. Attaches to Phase 1 tracker as the walk-floor anchor

**During Phase 6:**
- If lead dealer's trade allowance < KBB Instant Offer: push lead dealer to match-or-beat, citing the screenshot
- If lead dealer refuses to match: pull trade entirely, close the new-car sale solo, route trade to a KBB-participating dealer separately
- This decouples the new-car negotiation from the trade negotiation entirely

KBB Instant Offer is structurally the buyer's BATNA (Best Alternative To Negotiated Agreement). Use it.

---

## 10. State-Specific Trade Mechanics Quirks

- **CA**: **CA does NOT grant trade-in tax credit.** CDTFA taxes the gross sale price; trade is treated as a separate transaction. A $30k sale with a $12k trade in Alameda (9.25%) is taxed on the full $30k → $2,775 tax, NOT $1,665 (which would be the trade-credit-adjusted figure). Source of truth: `state_fees.md` All-State Summary CA row + CA detail stub. Doc fee capped at $85. Title $25. Reg by value (~1% per year first 3 years).
- **IL**: Trade-in tax credit capped at $10,000 of trade allowance for 2024 transactions; $10k cap continues through 2025+ per current legislation (verify). A $12,000 trade in IL caps the credit at $10k × 6.25-10.25% = $625-$1,025.
- **NJ**: Trade-in tax credit unlimited; one of the strongest buyer protections.
- **TX**: Trade-in tax credit unlimited; 6.25% rate makes it modest in dollar terms.
- **NY**: Trade-in tax credit unlimited; high combined rate (8-8.875%) makes it valuable.
- **KY, DC, CA**: NO trade-in tax credit. Full sale taxed. A $30k sale with $10k trade in KY (or DC, or CA) is taxed on the full $30k.

---

## 11. Documentation at Close

Bring to close:
- [ ] Vehicle title (clean, in buyer's name)
- [ ] All keys (count matches Phase 1 capture)
- [ ] Owner's manual + service records
- [ ] Current registration (proves vehicle is legally registered)
- [ ] Recent payoff statement (if lien)
- [ ] KBB Instant Offer screenshot (if used as anchor)

Dealer provides at close:
- [ ] Trade-in receipt with allowance amount
- [ ] Bill of sale showing sale price, trade credit, tax base
- [ ] Lien payoff confirmation (if applicable, mailed within 10 days)
- [ ] Power of attorney for title transfer (some states)
- [ ] 30-day permit if registration paperwork delayed

---

## 12. When NOT to Trade

Skip the trade and sell private-party (or KBB Instant Offer separately) when:
- Dealer's best offer is at or below Manheim wholesale floor
- Private-party premium is $2,500+ above dealer trade offer AND buyer has 7-14 days flexibility
- Trade has bad CARFAX (accident history) that the dealer will discount heavily but private buyer may accept
- Trade is desirable enthusiast car (manual transmission, rare color, low miles) that dealer cannot resell quickly

Skip private-party and trade-in when:
- Trade is hard-to-sell (over 100k mi, branded title, rare with thin buyer pool, mechanical issues)
- Buyer's state has zero or capped trade-in tax credit AND trade allowance is below KBB Trade-In
- Buyer values 1-stop closing more than $1,000-$2,000 of marginal trade value

---

## 13. EV / PHEV Trade-In — Battery SoH Discount + §25E Sub-Path

EV and PHEV trades follow the same four-anchor / separate-the-negotiation mechanics above, **plus a battery overlay that the books (KBB/NADA/Black Book) systematically miss.** For any EV or PHEV trade, run this sub-path in addition to Sections 1-12.

> Cross-reference: `references/ev_buyer_playbook.md` is the source of truth for EV battery health, the federal § 30D ($7,500 new) and § 25E ($4,000 used) credits (**both TERMINATED for vehicles acquired after 2025-09-30 per OBBBA — historical only; do not quote on current purchases**), and EV-specific dealer tactics. This section covers only the **trade-in side** (valuing the buyer's outgoing EV/PHEV); the buyer's *acquisition* of a used EV (formerly claiming § 25E) lives in the EV playbook.

### 13a. Why the books miss EVs

Traditional valuation tools were built on a gas-car depreciation curve. For EVs they have three failure modes (verify per current sources):

- They often **ignore battery State of Health (SoH) entirely** — a generic book value applies no SoH adjustment, so two identical-VIN/identical-mileage EVs get the same book number even if one pack is at 95% and the other at 78%.
- They **lag fast-moving EV price swings by months** — used-EV pricing has been more volatile than ICE; a stale book is worse leverage on an EV than on a Honda.
- They **lump EVs onto an ICE depreciation curve** — EVs have historically depreciated faster than gas cars in years 2-3 (some EVs lose 25-35% vs. 15-20% for gas as newer, longer-range models enter the market). A book that under-models this *over*-values the buyer's trade on paper but the dealer's desk will not honor it.

**Consequence:** the four-anchor table (Section 1) is necessary but NOT sufficient for an EV/PHEV. Add SoH as a fifth anchor (see `trade-in-valuator/SKILL.md`) and treat book numbers as a soft ceiling, not a floor.

### 13b. Battery SoH as the dominant valuation factor

For a used EV, the **battery pack is the single most expensive component**, so SoH usually moves resale value more than paint, trim, or even mileage. Treat SoH like "mileage for the pack." Approximate market behavior (verify; no rigid formula — dealers apply an invisible adjustment table):

| SoH band | Meaning | Trade-value effect (relative to a healthy peer of same model/age/miles) |
|---|---|---|
| 90-95%+ | Near-original capacity | Premium / supports book |
| ~85-89% | Solid for a multi-year-old EV | Roughly book; minor or no deduct |
| ~80-84% | Noticeable loss; ~"warranty threshold" zone | Begins to discount |
| < ~80% | ≥20% capacity lost | Market discounts **~10-20%** vs. a healthy example |
| < ~70% | Real range loss | Steep discount; can be hard to move |

Real-world magnitudes seen in market commentary (verify, not a guarantee): a 5-yr-old EV at 92% SoH vs. 82% SoH can differ by **$3,000-$5,000**; below ~82% SoH, dealers add another **$2,000-$5,000** risk discount for sooner replacement. **If the factory battery warranty does NOT transfer to the next owner, that is worth roughly another $5,000 of dealer discount** — and conversely, transferable remaining warranty is a premium lever for the buyer.

### 13c. Get verified SoH — not the dashboard guess

- The dash "guess-o-meter" range estimate is based on recent driving, **not** actual pack capacity. Do not quote it.
- Pull **verified SoH** via an OBD-II scan (or a third-party EV battery report / dealer scan). The math: a 75 kWh pack now holding 64 kWh = ~15% loss regardless of the screen.
- **Bring the SoH report to the trade negotiation proactively.** Battery data is real leverage — market commentary reports buyers who brought a battery-health report saved meaningfully more on EV transactions than those who didn't. Transparency on a *healthy* pack supports a premium; silence lets the dealer assume worst-case.
- Capture SoH as **field 13** in the Phase 1 trade capture for any EV/PHEV (Section 1's 12-field set + SoH), with the report date and source (OBD-II vs. dealer scan vs. manufacturer app).

### 13d. PHEV note

PHEVs carry a much smaller pack, so the absolute dollar SoH swing is smaller than a BEV's — but the same direction holds, and a degraded PHEV pack that no longer holds meaningful electric-only range is discounted toward an equivalent hybrid/ICE. Still pull SoH; still treat books as a soft ceiling.

### 13e. § 25E annotation — TERMINATED 2025-09-30; credit lived on the *acquisition*, not the trade

> **⚠️ §25E is TERMINATED.** OBBBA (Public Law 119-21, signed 2025-07-04) terminated the federal §25E Used Clean Vehicle Credit ($4,000) for any vehicle **acquired after 2025-09-30** (same date as §30D / §45W). For any 2026 used-EV purchase there is **NO** federal $4,000 credit — do NOT enter it in OTD / net-price math and do NOT cite it as a buyer-side benefit. Only still-funded **state/local rebates** remain (see `ev_buyer_playbook.md` state EV rebate matrix). Sources: IRS FAQ Fact Sheet 2025-05; IRS accelerated-termination FAQ under OBBB. The mechanics below are retained as **HISTORICAL** reference for pre-2025-10-01 acquisitions only.

A frequent buyer confusion (HISTORICAL, pre-2025-10-01 only): the federal **Used Clean Vehicle Credit under IRC § 25E** attached to the buyer **purchasing** a qualifying used EV/PHEV — it did **NOT** attach to the EV the buyer is trading *away*. Keep the two transactions mentally separate (which also reinforces Section 2's separate-the-negotiation rule). Historical mechanics (now terminated — do not apply to current purchases):

- **Who/what:** 30% of sale price, **max $4,000** credit, on a used clean vehicle bought from a **licensed dealer**.
- **$25,000 price cap (strict):** sale price must be **≤ $25,000**, measured **after incentives but BEFORE trade-in value**, and **dealer doc fees count toward the cap** (regs explicitly refused to exclude doc fees, to stop price-shifting around the cap). One dollar over → credit drops to $0.
  - **Trade-in interaction (the load-bearing point):** because the cap is measured **before** trade-in, a large trade-in allowance does **not** help you slip under $25k — the gating number is the vehicle's sale price itself. Do not let a dealer claim "your trade brings it under $25k."
- **Model-year rule:** model year must be **at least 2 years before** the calendar year of sale (e.g., for a 2025 sale, MY 2023 or older).
- **First-transfer rule:** must be the **first transfer** of that vehicle since 2022-08-16 to someone other than the original owner.
- **Dealer point-of-sale transfer (since 2024):** the buyer may **transfer the credit to a registered dealer** for an equivalent up-front price reduction (cash / down-payment / partial payment) at point of sale. Transferring also makes it **refundable** (can exceed the buyer's tax liability), unlike the nonrefundable claim-at-filing path.
  - **Transfer does not change the sale price.** Dealers may **not** raise the sale price because the buyer elects to transfer — the $25k cap is tested on the unchanged sale price.
  - **Dealer reporting:** dealer must be registered on IRS **Energy Credits Online (ECO)** and file the seller report **within 3 days** of sale; without that report the vehicle is **not** credit-eligible. Get the IRS time-of-sale report copy at delivery.
- **Buyer caps (claim or transfer):** MAGI ≤ **$75,000** single / **$150,000** MFJ (lesser of current/prior year); not a dependent; not for resale; no other § 25E credit claimed in the prior 3 years.

When the buyer is *both* trading in an old EV/PHEV and buying a used EV/PHEV, run **this section (13a-13d) for the trade** and **`ev_buyer_playbook.md` § 25E for the purchase** — two independent transactions, negotiated separately. (Note: the §25E purchase credit itself is TERMINATED for acquisitions after 2025-09-30 — the trade-in valuation mechanics in 13a-13d still apply regardless.)

---

## Cross-References

- `references/ev_buyer_playbook.md` — **EV/PHEV source of truth**: battery health, § 30D ($7,500 new) and § 25E ($4,000 used) credits (**both TERMINATED for vehicles acquired after 2025-09-30 per OBBBA — historical only**), charging/range, EV dealer tactics. This file's Section 13 covers only the trade-in (outgoing-EV) side.
- `references/state_fees.md` — full trade-in tax credit table (column 7 in All-State Summary)
- `references/negotiation_playbook.md` — Cold Open formula (use Round 1 cold open on no-trade ask first); add-on refusal list
- SKILL.md Phase 1 — trade-in router gate (this file is loaded when gate fires YES)
- SKILL.md Phase 6 — trade negotiation steps reference this file's "Separate the negotiation" rule
- SKILL.md Phase 9 — closing checklist references this file's documentation checklist
