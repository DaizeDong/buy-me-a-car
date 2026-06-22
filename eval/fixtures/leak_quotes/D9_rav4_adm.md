# Fixture D9 - New RAV4 Hybrid quote with ADM leak

> Source gotcha: D9 (ADM kill list). New MY inventory carries a "Toyota
> Hybrid Adjustment" ADM line above MSRP. A correct judge must demand
> removal as a PRECONDITION in the first counter, must NOT propose a
> middle-meet / smaller ADM, must NOT couple removal to financing or any
> other concession, and must treat used-car anchors as off-class (do not
> mix used + new per D5).

## Scenario metadata (not part of the dealer email)

- registering_state: PA
- vehicle_class: new
- vehicle: 2026 Toyota RAV4 Hybrid XLE Premium (MSRP $37,180)
- buyer_walk_otd: 40000
- adm_lines:
  - "Toyota Hybrid Adjustment $1,495"      (ADM above MSRP)
- expected_judge_flags:
  - flag_adm: true
  - demand_removal_as_precondition: true   # D9 rule 1
  - no_middle_meet: true                    # do not negotiate $1495 -> $750
  - no_coupling_to_financing: true          # D9 rule: ADM is its own line
  - one_ask_one_round: true
  - no_used_anchor_mixing: true             # D5: new desk, MSRP-band anchor only
- expected_email_type: counter
- correct_skill_route: dealer-reply-drafter

## Dealer email (verbatim paste)

From: Marisa P. <internet@example-pa-toyota.com>
Subject: 2026 RAV4 Hybrid XLE Premium - pricing

Good afternoon,

Congrats on picking the RAV4 Hybrid, great choice and we have one in
Blueprint arriving next week. Here is where the numbers land:

  MSRP:                              $37,180
  Toyota Hybrid Adjustment:           $1,495
  Doc fee:                              $399
  PA sales tax (6%):                  $2,344
  Title:                                 $58
  Registration:                          $39
  -----------------------------------------
  Estimated OTD:                     $41,515

The Hybrid Adjustment reflects current demand on hybrids; these are moving
fast. If you finance through Toyota Financial we can talk about getting you
into a better rate to offset some of that. Want me to hold it with a
deposit?

Marisa
