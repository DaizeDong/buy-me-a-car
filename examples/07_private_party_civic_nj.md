# Scenario 7: Used Honda Civic, private-party (FSBO), New Jersey, cash

## The buyer

The buyer is a graduate student in central New Jersey (<ZIP>). This is
their first car bought without a parent co-signing. They are
budget-constrained, mechanically cautious, and found the car on a
peer-to-peer marketplace listed by a private individual, **not a
dealer**. Cash, no trade, no financing, no lease.

## The target

A 2019-2022 Honda Civic, EX or Touring sedan (Touring preferred for the
leather + sunroof + nav). Under 60,000 miles. Any color except white.
Must-haves: Apple CarPlay, Honda Sensing, backup camera, heated seats.
Reliability and fuel economy drive the choice; the Civic's resale
strength is a secondary anchor. The seller is the original owner with a
clean CARFAX and full Honda dealer service history.

## The constraints

- Budget: $18,000 to $22,000 **total cost** (sale price + tax + title +
  reg paid at the NJ MVC, since there is no dealer collecting fees).
- Walk-away ceiling: $23,000 total, OR any title/seller red flag.
- Geographic radius: 30 miles of <ZIP>, the seller is local, so this is
  a single-seller transaction, not a 30-listing radius sweep.
- Payment: **cash via cashier's check drawn at the seller's own bank,
  executed in person at that branch** (private-party safe-payment
  default).
- Timeline: flexible, two to three weeks; contingent on a clean
  independent PPI.

## The ask

The buyer wants the buy-me-a-car workflow to:

1. Recognize at Phase 1 that this is the **private-party (FSBO) path**,
   not the dealer path, and route to `private_party_playbook.md`
   (buyer path #6) instead of the dealer pipeline.
2. Use the **no-OTD / no-F&I cost model**: a private sale has no doc fee,
   no dealer fees, no F&I office. Total = sale price + NJ tax + title +
   reg, with tax and title/reg paid by the buyer at the NJ MVC.
3. Get the **NJ private-party tax basis right**: NJ taxes the **purchase
   price** at 6.625% statewide (no local add-on), with a fair-market-value
   backstop if the MVC believes the stated price is below market.
4. Elevate **PPI to a gating requirement**, on a private sale there is
   no dealer reputation and no return window, so an independent-shop PPI
   is the buyer's only inspection backstop; seller refusal is a red flag.
5. Run **curbstoner / scam and payment-fraud detection** in place of the
   dealer inbox-triage buckets: title-in-seller's-name check, VIN match,
   physical-title-before-money, no-wire-before-inspection.

## What makes this scenario interesting

- This is the **first private-party scenario**. Every other example
  assumes a dealer on the other side, an OTD line-item stack, an F&I
  office, mass outreach to 30+ VINs. The FSBO path is the dealer
  pipeline's mirror image: no OTD build, no add-on script, no batch
  outreach. The risk moves entirely to **title, tax basis, payment
  fraud, and seller legitimacy**.
- The **OTD-calculator must be partially suppressed**: reuse only its
  tax + title + reg engine, and turn off every doc-fee and dealer-fee
  line. If anyone in the chain asks the buyer to pay a "doc fee" on a
  private sale, that itself is a curbstoner flag, only licensed dealers
  charge those.
- **CPO does not exist on a private sale.** `cpo-eligibility` is N/A here
  even though a 2019-2022 Civic would be Honda-CPO-eligible at a dealer.
  The factory powertrain remainder may still transfer, but there is no
  certified-warranty layer to negotiate.
- The dealer inbox-triage four-bucket model (real / OOO / CRM / spam)
  is replaced by **curbstoner + payment-fraud detection**, a structurally
  different threat model.

## Skills exercised

- [orchestrator](../skills/orchestrator/SKILL.md), Phases 1, 2, then the
  private-party branch (single-seller negotiation, no Phase 3/4 mass
  outreach).
- [state-fee-lookup](../skills/state-fee-lookup/SKILL.md), New Jersey
  detail (6.625% state, no local add-on, $85 title, $70 reg) feeding only
  the **tax + title + reg** engine; doc-fee line suppressed.
- [ppi-scheduler](../skills/ppi-scheduler/SKILL.md), **elevated to
  gating priority**; independent-shop PPI is the only inspection backstop
  and seller refusal is a walk condition.
- [carfax-pdf-review](../skills/carfax-pdf-review/SKILL.md), run on the
  CARFAX/title history (accidents, brands, rollback, lien records) with
  the **F&I add-on detector skipped** (no F&I office exists).
- [dealer-reply-drafter](../skills/dealer-reply-drafter/SKILL.md),
  repurposed for **single-seller** messages (PPI request, payment/branch
  logistics, price counter); short and human, no dealer CRM on the other
  end.

> **Not exercised (deliberately):** `otd-calculator` runs only its
> tax/title/reg engine with dealer-fee lines suppressed;
> `cpo-eligibility` is N/A (no CPO on a private sale);
> `trade-in-valuator`, `lease-vs-cash-analyzer`, `payment-method-decider`,
> `dossier-builder` are N/A or downgraded; Phase 3 inventory and Phase 4
> mass outreach do not run (single seller).

---

## Outcome

### Skill firing order

1. **orchestrator** Phase 1, captured the 9-field core, then the
   buyer-type router resolved to **private-party (FSBO)** on the
   "seller is a private individual, not a dealer" signal. Routed to
   `private_party_playbook.md` (buyer path #6). Suppressed the dealer OTD
   stack and the Phase 4 mass-outreach branch up front.
2. **state-fee-lookup**, New Jersey detail from `data/state_fees.json`:
   state tax **6.625%** (`tax_state: 0.06625`), local **0%**
   (`tax_local_typ: "0%"`), **title $85** (`title: 85`), **reg/yr $70**
   (`reg_1yr: 70`), no EV surcharge. Fed only the tax + title + reg
   engine; the doc-fee line ($799 NJ dealer cap) was **suppressed**,
   irrelevant on a private sale.
3. **private-party cost model**, total = sale price + NJ tax + title +
   reg, all buyer-paid at the NJ MVC. Applied the NJ private-party tax
   basis (`private_party_playbook.md` section 3a): 6.625% on the
   **purchase price**, with a fair-market-value backstop if the MVC
   thinks the stated price is below market.
4. **ppi-scheduler**, elevated to gating: independent-shop PPI scheduled
   as a pre-payment condition; seller refusal flagged as a walk trigger.
5. **carfax-pdf-review**, run on the seller's CARFAX + title (clean,
   one owner confirmed); F&I add-on detector skipped.
6. **dealer-reply-drafter**, single-seller counter to the private seller
   (price counter on regional private-party comps + PPI request + payment
   logistics at the seller's bank branch).

### Artifacts produced

- `criteria.md`, Phase 1 core 9 fields + a private-party sub-block
  (title-in-seller's-name confirmation, PPI-as-gate, safe-payment
  structure, NJ MVC tax/title deadline).
- `civic-nj-pp-baseline.md`, regional **private-party** comps (not
  dealer asking prices) with REAL/SYNTHESIZED provenance flags, plus the
  no-OTD total-cost build (sale + NJ tax + title + reg, dealer-fee lines
  absent).
- `p6_seller_message.md`, single-seller message under 12 lines: price
  counter anchored on private-party comps + condition, PPI request,
  cashier's-check-at-your-bank logistics. No dealer CRM language.

### Numbers and their provenance

Every dollar figure traces to a truth source, no invented fees:

- NJ state tax 6.625%, no local add-on, title $85, reg $70:
  `data/state_fees.json` -> states[] -> NJ (`tax_state` 0.06625,
  `tax_local_typ` "0%", `title` 85, `reg_1yr` 70). NJ record is
  `verified: false` in the seed (no `source_url`), so usable as fixture
  truth but re-verify before quoting a live NJ buyer.
- NJ doc cap $799 exists in the record (`doc_cap: 799`) but is
  **deliberately not applied**, private sales have no doc fee
  (`private_party_playbook.md` section 2).
- NJ private-party tax basis = purchase price at 6.625% with FMV
  backstop: `private_party_playbook.md` section 3a (NJ row, web-verified
  2026-06-22).
- No-OTD / no-F&I cost model (sale + tax + title + reg only):
  `private_party_playbook.md` section 2.

> **Title-fee cross-reference note:** `private_party_playbook.md`
> section 3a cites a NJ **title transfer fee of $60** (MVC transfer
> action), while `data/state_fees.json` carries `title: 85` as the NJ
> title fee. The fixture uses the **state_fees.json $85** value as the
> truth source per the data-of-record rule; the $60 figure in the
> playbook is the narrower title-transfer-action fee. Both should be
> reconciled in a future data pass, flagged, not silently averaged.

### Gotchas and Critical Rules that fired

- **Critical Rule #1 (plain ASCII)**, seller message contains no
  em-dashes, no smart quotes, no markdown bold.
- **Critical Rule #7 (REAL-tagged citations only)**, the baseline uses
  REAL private-party comp rows by URL + timestamp; synthesized regional
  anecdotes stay internal and are never pasted to the seller.
- **OTD-calculator partial suppression**, only the tax/title/reg engine
  ran; all doc-fee and dealer-fee lines were turned off. (Load-bearing
  routing decision the fixture verifies.)
- **Doc-fee-on-private-sale = curbstoner flag**, if the seller asked for
  a "doc fee," the workflow would flag it as an unlicensed-dealer signal
  (`private_party_playbook.md` section 4).
- **PPI-as-gate**, seller refusal of an independent PPI is close to
  disqualifying on a private sale; treated as a walk condition.
- **Safe-payment structure**, cashier's check at the seller's own bank
  branch, title in hand and VINs matched before money moves; no wire,
  no escrow link the seller chose (`private_party_playbook.md`
  sections 4-5).

### What this scenario surfaced for the skill

The private-party path (buyer path #6) existed as a reference file but
had no end-to-end fixture. This scenario pins:

- The Phase 1 **dealer-vs-private-party router** as an explicit, testable
  branch, and the consequence that Phase 3 inventory + Phase 4 mass
  outreach do not run for a single private seller.
- The **OTD-calculator partial-suppression** rule (tax/title/reg engine
  only, dealer-fee lines off) as a concrete regression check.
- The **NJ private-party tax basis** (purchase price + FMV backstop) as
  the worked example distinct from the dealer sales-tax basis.
- The **curbstoner/payment-fraud threat model** replacing inbox-triage
  for the FSBO path.
- A surfaced **data-of-record discrepancy** (NJ title $60 in the playbook
  vs $85 in state_fees.json) for a future reconciliation pass.

### Reading takeaway

Read this after scenario 1 (the cash baseline) for the cleanest
dealer-vs-private-party contrast. The single most important thing this
fixture verifies is that the workflow does **not** run a dealer OTD stack
or mass outreach on a private sale, and that it routes the NJ tax through
the purchase-price basis rather than a dealer sales-tax line. If your
local copy invents a doc fee or runs Phase 4 outreach here, that is a
routing regression.
