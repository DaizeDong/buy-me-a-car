# Rubric: Leak / Gotcha Detection

Judge whether the model correctly DETECTED the planted gotcha in a dealer
quote, independent of how it later drafts the reply. Input: the fixture
(leak_quotes/*.md) plus the model's analysis output. Score PASS/FAIL per
criterion against the fixture's `expected_judge_flags` block.

Grounded in gotchas D8 (state-fee leak), D9 (ADM kill list), D10
(bait-and-switch) and references/state_fees.md "Does NOT have" lists.

## D8 - state-fee-template leak

- **L1.** Identifies EVERY leaked line in the fixture (e.g. both the NJ
  supplemental titling fee AND the per-tire fee on a CT quote). FAIL if any
  leaked line is missed.
- **L2.** Correctly justifies the leak by registering-state law (the line is
  not in the registering state's "Has" list). FAIL on a wrong reason.
- **L3.** Does NOT false-positive on legitimate lines (CT 6.35% tax, doc fee,
  $25 title, ~$120 reg are all valid). FAIL if it flags a legitimate line.
- **L4.** Prescribes a FULL re-quote, not a single-line deletion (D8 rule).

## D9 - ADM kill list

- **L5.** Identifies the ADM line by its exact name as it appears on the quote
  (e.g. "Toyota Hybrid Adjustment $1,495"). FAIL if missed or mislabeled.
- **L6.** Classifies it as ADM / margin theater above MSRP, not a legitimate
  state or processing fee. FAIL on misclassification.
- **L7.** Does NOT treat the financing-rate offer as a fair trade for the ADM
  (recognizes the coupling trap). FAIL if it accepts the coupling framing.

## D10 - bait-and-switch

- **L8.** Flags the "just sold" + higher-priced pivot as a bait-and-switch
  pattern (not as a neutral inventory update). FAIL if taken at face value.
- **L9.** Quantifies the unjustified markup on the pivot VIN beyond legitimate
  config delta (miles/trim). FAIL if it ignores the price-per-config jump.
- **L10.** Calls for sold-date proof AND re-anchoring before engaging on the
  substitute. FAIL if it would proceed on the pivot without both.

## Cross-cutting

- **L11 - No hallucinated leaks.** Does not invent a leak that is not in the
  fixture, and does not fabricate state law. FAIL on any invented flag.

## Scoring output

```json
{
  "fixture_id": "D9_rav4_adm",
  "gotcha": "D9",
  "criteria": {"L5": true, "L6": true, "L7": true},
  "detected": true,
  "missed_or_wrong": [],
  "rationale": "one short paragraph"
}
```

`detected` = true iff every criterion applicable to that fixture's gotcha
passes (plus L11).
