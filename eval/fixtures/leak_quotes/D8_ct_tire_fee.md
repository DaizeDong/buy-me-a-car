# Fixture D8 - CT quote with NJ state-fee-template leak

> Source gotcha: D8 (state-fee-template leak). Registering state CT has NO
> per-tire fee and NO NJ-style supplemental titling fee (see state_fees.md
> CT "Does NOT have" list). A correct judge must flag BOTH leaked lines and
> require a FULL re-quote, not a single-line deletion.

## Scenario metadata (not part of the dealer email)

- registering_state: CT
- vehicle_class: used
- vehicle: 2023 Subaru Outback Limited, 31,400 mi
- buyer_walk_otd: 30000
- leaked_lines:
  - "NJ Supplemental Titling Fee $13.50"   (NJ-only; CT does not have it)
  - "Tire Fee (5 @ $1.50) $7.50"           (NJ-style per-tire; CT does not have it)
- legitimate_lines:
  - CT sales tax 6.35%
  - Doc fee $599 (CT has no statutory cap; $499-699 typical)
  - Title $25
  - 2-year passenger reg ~$120
- expected_judge_flags:
  - flag_state_fee_leak: true
  - require_full_requote: true        # D8 rule: NOT single-line deletion
  - leaked_terms_named: ["supplemental titling", "tire fee"]
- expected_email_type: counter
- correct_skill_route: dealer-reply-drafter

## Dealer email (verbatim paste)

From: Tony R. <tony@example-ct-subaru.com>
Subject: Your OTD on the 2023 Outback Limited (Stock #U24-8841)

Hi there,

Thanks for reaching out. Here is the out-the-door breakdown on the 2023
Outback Limited, 31,400 miles, stock #U24-8841:

  Sale price:                      $28,990.00
  CT sales tax (6.35%):             $1,841.00
  Doc fee:                            $599.00
  Title:                               $25.00
  Registration (2-yr passenger):      $120.00
  NJ Supplemental Titling Fee:         $13.50
  Tire Fee (5 @ $1.50):                 $7.50
  --------------------------------------------
  OTD total:                       $31,596.00

This is a clean one-owner car, CARFAX attached. It is getting a lot of
attention, so let me know quickly if you want to lock it in.

Tony
