# Private-Party (Person-to-Person) Buyer Playbook

> **Buyer path #6**, the missing path. The other five (cash / financing / trade-in / EV / pickup)
> all assume a **dealer** on the other side of the table: an OTD line-item stack, an F&I office,
> a doc fee, mass outreach to 30+ listings. A private-party (FSBO, "for sale by owner") purchase
> has **none of that**. This playbook is the dealer-path's mirror image: no OTD build, no F&I
> add-on script, no batch outreach. Instead the risk moves to **title, tax, payment fraud, and
> seller legitimacy**.
>
> **last_verified**: 2026-06-22
> **tax/title rules web-verified this cycle**: CA, NJ, IL (see "State tax & title, verified" below).
> All other states: treat the rules here as the *shape* of the problem and verify the specific
> state at close via `state_fees.md` + the state DMV/revenue site. **Tax basis is the single most
> state-variable fact in this entire playbook, never quote a number without state-specific
> verification.**

---

## 1. What changes vs the dealer path (the orchestrator's branch map)

| Pipeline element | Dealer path | Private-party path |
|---|---|---|
| OTD build (otd-calculator) | Full stack: sale + tax + doc + title + reg + dealer fees | **No doc fee, no dealer fees.** Buyer pays tax + title + reg **at the DMV**, not to the seller. Seller is paid the **bare sale price** only. |
| F&I office / add-ons | hard-no script (carfax-pdf-review) | **N/A, there is no F&I office.** No VSC, no GAP, no nitrogen, no etch upsell. Skip the add-on detector entirely. |
| Phase 4 mass outreach | Lead forms to top 30 VINs | **N/A, single seller.** No lead forms. One thread, one human. See Phase-4 branch below. |
| Phase 6 negotiation | 3-anchor counter, dealer spread + regional comp + locked OTDs | **Single-seller negotiation.** No dealer-pricing spread to exploit; anchor on regional private-party comps + condition deductions. See Phase-6 branch. |
| Inbox triage (4 buckets) | real / OOO / CRM / spam | mostly N/A, one seller, no CRM blasts. Watch instead for **curbstoner / scam** signals (§4). |
| Tax remitted to | dealer collects, remits | **buyer remits at DMV registration** (use tax, not sales tax in many states). |
| Title delivered by | dealer handles DMV paperwork | **buyer must complete title transfer themselves** within the state deadline (§3). |
| Warranty | CPO / dealer / factory remainder | **as-is, no implied warranty** in nearly all states for casual sales. Factory remainder may still transfer; CPO does not exist on a private sale. |
| PPI (ppi-scheduler) | dealer-lot PPI | **PPI is MORE important, not less**, no dealer reputation, no return window. Insist on independent shop PPI; a seller who refuses is a red flag (§4). |

**One-line gate for the orchestrator:** *If the seller is a private individual (FSBO), there is no OTD
stack and no F&I office. The buyer's real adversaries are a bad title, an under- or over-stated tax
basis, and a fraudulent payment/seller. Route accordingly.*

---

## 2. The no-OTD / no-F&I cost model

A private-party total cost has only four buckets:

```
TOTAL = sale_price
      + state_tax            (use tax / sales tax — basis is state-variable, see §3)
      + title_transfer_fee   (small flat, e.g. NJ $60)
      + registration + plates (private buyer usually needs NEW plates; seller keeps/surrenders theirs)
```

There is **no doc fee, no dealer prep, no advertising fee, no F&I product**. If anyone in the chain
asks the buyer to pay a "doc fee" or "dealer fee" on a private sale, that itself is a curbstoner
flag (§4), only a licensed dealer charges those.

**Do NOT run the standard OTD calculator's dealer-fee lines.** Reuse only its tax + title + reg
engine, and feed it the **private-party tax basis** for the state (which can differ from the dealer
sales-tax basis, see Illinois below).

---

## 3. State tax & title, the basis question

The headline trap: **some states tax a private-party sale on the actual purchase price; some can
substitute book value if the declared price looks low; and at least one (Illinois) ignores the
purchase price for most cars and charges a fixed amount off a model-year / value table.** Getting
this wrong mis-states total cost by hundreds to thousands of dollars.

### 3a. Verified this cycle (web-checked 2026-06-22)

**California, purchase price, with book-value backstop.**
A private-party sale is **use tax**, not sales tax (no dealer collected it). It is owed at DMV
registration, at the buyer's local **sales-tax rate**, computed on the **actual purchase price**
documented on the title back or a bill of sale. **Book value only substitutes** when (a) no price
is stated, (b) there is a price discrepancy (resolve via Statement of Facts REG 256, else DMV uses
the higher figure), or (c) the declared price is suspiciously low, the DMV/CDTFA can challenge it
and assess at fair market value. 2026 enforcement is reportedly tighter: the system cross-references
the declared price against CDTFA's fair-market database and flags gaps; "$1 gift" paperwork to dodge
tax is effectively dead.
- Sources:
  [CDTFA Tax Guide for Purchasers of Vehicles](https://cdtfa.ca.gov/industry/vehicles-vessels-aircraft/vehicles.htm),
  [CA DMV 4.010 Calculating Use Tax Amount](https://www.dmv.ca.gov/portal/handbook/vehicle-industry-registration-procedures-manual-2/use-tax/calculating-use-tax-amount/),
  [CA DMV 4.040 Transactions Subject to Use Tax](https://www.dmv.ca.gov/portal/handbook/vehicle-industry-registration-procedures-manual-2/use-tax/transactions-subject-to-use-tax/).
  *Takeaway: declare the real price + keep a bill of sale; a price far under book invites review.*

**New Jersey, purchase price, with fair-market-value backstop.**
Statewide **6.625%** on the purchase price of a used vehicle, paid to the NJ MVC at transfer
(no local add-on). The MVC **can substitute the vehicle's fair market value (KBB etc.) if it
believes the stated price is below market**, and by law the Division of Taxation must certify the
correct tax was paid; ignore a "casual sales notice" and they assess on value. Title transfer fee
**$60** (+$25 per lien, max 2 liens). **10-day** transfer deadline or a **$25** late fee. Seller
removes plates; buyer buys new plates. Gift of a lien-free vehicle = no sales tax (Seller's
Affidavit), though income-tax may apply.
- Sources:
  [NJ Division of Taxation, Motor Vehicle Casual Sales Q&A](https://www.nj.gov/treasury/taxation/moveqa.shtml),
  [NJ Consumer Automotive Tax Guide (PDF)](https://www.nj.gov/treasury/taxation/documents/pdf/guides/New-Jersey-Consumer-Automotive-Tax-Guide.pdf),
  [NJ MVC, Vehicles Exempt From Sales Tax](https://www.nj.gov/mvc/vehicletopics/taxexempt.htm).

**Illinois, fixed table, NOT the purchase price (for most cars).**
This is the big exception. Illinois **Private Party Vehicle Use Tax (Form RUT-50)** is filed by the
buyer within **30 days**. The 2026 chart is **Form RUT-5**.
- **Under $15,000 selling price → Table A**, which is keyed to the **vehicle's age (model year)**,
  not the price. Older cars owe a small flat amount per the age bracket.
- **$15,000 or more → Table B**, keyed to **value brackets**.
- **Motorcycle / ATV → flat $25.**
- **No trade-in deduction** on this tax. Local (Cook County / Chicago) private-party use taxes may
  stack on top and have their own age-based amounts.
- Because Table A is age-based, the declared price is largely irrelevant for sub-$15k older cars ,
  do **not** model Illinois as "rate × price" the way you would NJ/CA.
- Sources:
  [IL DoR Private Party Vehicle Use Tax](https://tax.illinois.gov/research/taxinformation/sales/vehicle.html),
  [RUT-5 2026 Chart (PDF)](https://tax.illinois.gov/content/dam/soi/en/web/tax/forms/sales/documents/vehicleusetax/rut-5.pdf),
  [RUT-50 Instructions (PDF)](https://tax.illinois.gov/content/dam/soi/en/web/tax/forms/sales/documents/vehicleusetax/rut-50-instr.pdf).

### 3b. The three basis archetypes (use to classify any unverified state at close)

1. **Purchase-price states (most common):** tax = local rate × declared price; bill of sale is the
   proof. Backstop = book value if declared price looks artificially low (CA, NJ, and most others).
2. **Book-value / fair-market states:** the DMV defaults to a guidebook value (NADA/KBB/Black Book)
   and the buyer must affirmatively prove a lower real price to be taxed on it. Always check whether
   the target state assesses private sales on **NADA book value rather than the actual sale price** ,
   several do, and a low real price won't help unless documented.
3. **Fixed-schedule states (Illinois archetype):** tax is read off an age/value table; the actual
   price barely matters for older/cheaper cars.

**Rule for the orchestrator:** for any state not in §3a, do NOT assume purchase-price basis. Pull the
state's private-party rule from `state_fees.md`, and if it isn't pinned there, **web-verify the basis
(price vs book value vs fixed table) before quoting any tax number.**

### 3c. Title transfer mechanics (state-variable, common shape)

- **Both parties complete the title:** odometer reading, sale date, **purchase price**, signatures.
  In many states a separate **bill of sale** is also required (and is the buyer's tax-basis proof).
- **Deadline + late fee** are real (NJ 10 days/$25; IL RUT-50 30 days). Miss it and the buyer eats a
  penalty and possibly a value-based reassessment.
- **Plates:** in most states the **seller keeps or surrenders their plates**; the buyer registers and
  gets **new plates**. Do not let the buyer drive off assuming the seller's plates convey.
- **Lien on title (see §6):** a title showing a lienholder is **not clear**, the buyer cannot
  register until the lien is released.
- **Curbstoner tell:** if the title is **not in the seller's name** ("open title" / "title jumping"),
  stop. That is the single strongest illegal-dealer signal (§4).

---

## 4. Curbstoner & scam detection (replaces inbox-triage's CRM/spam buckets)

A **curbstoner** is an unlicensed dealer posing as a private seller to dodge licensing, consumer-
protection law, and disclosure duties, flipping salvage/flood/lemon cars with washed titles. On the
private-party path, curbstoner + payment fraud detection **replaces** the dealer inbox's CRM/spam
triage. Red flags, in rough order of severity:

**Title / ownership red flags (hardest stops):**
- Title **not in the seller's name**, or seller "will sign it over later" / hands you an unsigned
  ("open") title, classic **title jumping**. Walk.
- Seller dodges showing the **physical title** before money moves.
- Title is a **rebuilt / salvage / flood / junk** brand the listing didn't mention.
- VIN on the title ≠ VIN on the dash/door-jamb.

**Seller-behavior red flags:**
- Same phone number appears across **multiple "private" listings** (reverse-search it), a curbstoner
  inventory.
- Seller wants to meet **away from their home address** / won't show where the car lives; can't
  produce matching ID and registration.
- Vague on the car's history, pushes a fast close, "another buyer is coming."
- **Refuses an independent PPI** or won't let you take it to a shop, on a private sale this is close
  to disqualifying (no return window to fall back on).
- Asks the buyer to pay a "doc fee" / "dealer fee" (only licensed dealers charge those).

**Payment-fraud red flags (see §5):**
- Pressure to **wire money before** seeing title/car, or to a third party / out-of-state escrow the
  seller chose.
- "Shipping company will deliver, pay them first" (no in-person inspection), almost always a scam.
- Overpayment / "I'll send extra, refund the difference", fake-check fraud.

**Action:** any single hard title flag = walk. Two or more behavior flags = treat as curbstoner,
disengage, do not send money.

---

## 5. Payment & escrow safety (the dealer path has no analog)

The buyer is handing a large sum to a stranger. Defaults:

- **Pay with a cashier's check drawn at the SELLER'S OWN BANK, executed in person at that branch.**
  Going to the seller's bank lets the teller verify the seller's identity/account and the seller
  confirm the check is real on the spot, the title can change hands at the counter. This is the
  single safest structure for a mid-four to five-figure private sale.
- **Do NOT pre-wire funds** to a seller you haven't met or to an escrow service the *seller* picked.
  Most "vehicle escrow" sites pushed by a seller are fake. If escrow is genuinely warranted (remote
  high-value sale), the **buyer** selects a reputable, independently verified escrow agent, never a
  link the seller sends.
- **Cash** only for low-value sales and only in a safe public place (many police stations offer
  "safe exchange zones"); large cash is its own risk.
- **Never** pay by gift card, crypto, Zelle/peer-app to a stranger, or "refund the overpayment."
- **No money moves until** the buyer has the physical title in the seller's name, VINs match, the
  odometer statement is signed, and (ideally) the PPI is clean.

---

## 6. Odometer disclosure & private cars with a lien

**Odometer (federal + state):** the seller must provide a written **odometer disclosure** at
transfer. Since 2021 the federal odometer-disclosure requirement extends to vehicles **up to 20
model years** old (older exemption shrank). A blank, "exempt," or implausible odometer statement, or
a reading that doesn't track the title/service history, is both a legal gap and a fraud flag. Capture
the disclosed mileage on the title/bill of sale; it is the buyer's protection against rollback.

**Private car that still has a lien (very common):** the seller owes money on it, so the
**lienholder holds the title**, the seller can't hand the buyer a clear title until the loan is paid
off. Safe payoff structures:
- **Best:** meet the seller at the **lienholder's bank/credit-union branch**; buyer's funds pay the
  loan **directly to the lienholder**, any equity goes to the seller, and the lien is released so the
  clear title (or lien-release + title) issues to the buyer.
- **Split payment:** cashier's check to the **lienholder for the payoff amount** + separate payment
  to the **seller for the equity**, never one lump sum to the seller and "trust me, I'll pay it off."
- Get a **10-day payoff letter** from the lienholder so the exact figure (with per-diem interest) is
  documented before money moves.
- **Never** pay the full price to the seller and hope they clear the lien afterward, the title may
  never come, and the buyer has no recourse.

---

## 7. Handoff to other skills (what still applies)

- **state-fee-lookup / otd-calculator:** reuse the **tax + title + reg** engine only; **suppress
  doc-fee and dealer-fee lines**; feed the **private-party tax basis** for the state (§3).
- **ppi-scheduler:** elevated priority, independent-shop PPI is the buyer's only inspection
  backstop. Seller refusal = red flag.
- **carfax-pdf-review:** still run it on the **CARFAX/title history** (accidents, brands, odometer
  rollback, lien records), but **skip the F&I add-on detector** (no F&I office exists).
- **dealer-reply-drafter:** repurpose for **single-seller** messages (PPI request, payoff/escrow
  logistics, price counter). Keep it short and human; there's no dealer CRM on the other end.
- **insurance-shopper / close-day-checklist:** still apply, buyer needs coverage bound before
  driving off and a close-day list (title signed correctly, odometer captured, payment structured
  safely, plates handled, DMV deadline diaried).
- **cpo-eligibility / lease-vs-cash / trade-in / dossier:** **N/A or downgraded**, no CPO on a
  private sale, no lease, no dealer trade-in (the buyer may still sell their old car privately as a
  separate transaction).
