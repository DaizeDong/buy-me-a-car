# Fixture D10 - "Just sold" bait-and-switch pivot to higher-priced VIN

> Source gotcha: D10 (bait-and-switch protocol). Dealer claims the original
> low-priced VIN-X "just sold" and pivots to a higher-priced, higher-mileage
> VIN-Y. A correct judge must (1) ask for sold-date proof in writing, (2)
> require the substitute to land at or under the original OTD adjusted ONLY
> for legitimate config delta (no upgrade markup), and (3) treat the pivot
> as a NEW engagement / re-anchor -- NOT a 5-line "ok what's the OTD on
> VIN-Y" concession.

## Scenario metadata (not part of the dealer email)

- registering_state: MA
- vehicle_class: used
- vehicle_original: 2022 Honda CR-V EX-L, VIN ...A26500, 28,000 mi, listed $26,500
- vehicle_pivot:    2022 Honda CR-V EX-L, VIN ...B29200, 36,000 mi, quoted $29,200
- buyer_walk_otd: 29000
- pivot_markup: 2700                 # $29,200 - $26,500 on +8k miles, same trim
- expected_judge_flags:
  - flag_bait_switch: true
  - demand_sold_proof: true          # D10 rule 1
  - require_same_or_better_otd: true # D10 rule 2, config-delta only
  - treat_as_new_engagement: true    # D10 rule 3, re-anchor
  - no_blind_pivot_accept: true      # must NOT just ask OTD on VIN-Y
- expected_email_type: counter       # (re-anchor counter, not walk yet)
- correct_skill_route: dealer-reply-drafter

## Dealer email (verbatim paste)

From: Greg D. <gregd@example-ma-honda.com>
Subject: RE: 2022 CR-V EX-L availability

Hey,

Bad news and good news. The CR-V EX-L you asked about (the $26,500 one)
just sold this morning to another buyer who was already in the showroom,
sorry about that, it moved fast.

Good news is I have another 2022 CR-V EX-L that just came in, same trim,
same color basically. It is at 36,000 miles and we have it at $29,200.
Fresh on the lot, hasn't even hit the website yet, so you'd be first in
line. Want me to start paperwork on this one before it gets posted?

Greg
