# Rubric: Negotiation Counter Email (dealer-reply-drafter)

Judge a drafted dealer counter email. The draft is the model output under
test; the dealer quote it replies to is the fixture. Score each criterion
PASS/FAIL. A counter is ACCEPTED only if ALL hard-gate (HG) criteria pass.
SOFT criteria (SC) are advisory quality signals; report them but they do not
by themselves fail the draft.

Grounded in: skills/dealer-reply-drafter/SKILL.md, references/negotiation_playbook.md
(Round 1 Cold Open + Counter-Offer Tactics), references/email_format_rules.md,
and gotchas D5/D8/D9/D10/E1/E3.

## Hard gates

- **HG1 - Line cap (E3).** Body is <= 10 content lines (count non-blank lines
  between the greeting and the sign-off; greeting, blank lines, "Thanks,",
  and the signature name do not count). FAIL if > 10.

- **HG2 - Three numbered asks.** Exactly 3 explicitly numbered asks
  (`1)`/`1.` ... `3)`/`3.`). Not 2, not 4. Each ask is a concrete imperative
  request (remove X / re-quote without Y / hit $Z OTD). FAIL if the count is
  off or an "ask" is vague filler.

- **HG3 - One anchor line, REAL-tagged.** Exactly one anchor sentence citing
  a verifiable data point: a named source regional median (Edmunds/CarGurus/KBB
  with city + sample where possible), a named single-comp listing
  (`{Dealer} has a comparable {trim} at ${ask}`), OR a locked competitor OTD by
  dollar amount. FAIL if the anchor is fabricated, a round-numbered placeholder,
  a synthesized anecdote ("a buyer on Reddit got..."), or "national average"
  with no name. (Critical Rule #7.)

- **HG4 - One walk-away line.** Exactly one explicit walk-away / ceiling
  statement ("Above $X OTD I will move forward with my other anchors" or
  equivalent). FAIL if absent, or if there are multiple competing walk lines.

- **HG5 - Pure ASCII (E1).** Body contains NO non-ASCII characters and NO
  markdown markers: no em-dash, en-dash, curly quotes/apostrophes, unicode
  bullets, `**bold**`, backticks, `[text](url)`, `#` headings, `---`/`***`
  dividers. FAIL on any occurrence. (This is also checked deterministically by
  test_rubric.py; the judge confirms it reads clean to a human.)

- **HG6 - English-only.** No Chinese, Spanish, or any non-English content in
  the dealer-facing body. FAIL on any non-English text.

- **HG7 - No used/new anchor mixing (D5).** A counter on a NEW-car quote must
  anchor only to new-car / MSRP-band evidence; a counter on a USED-car quote
  must anchor only to used comps. FAIL if the draft cites an off-class anchor.

## Gotcha-specific gates (apply only when the fixture carries that gotcha)

- **HG8-D8 - State-fee leak => full re-quote.** If the fixture has a state-fee
  template leak, the draft must (a) name the leaked line(s) as not legitimate
  for the registering state and (b) demand a FULL re-quote, not merely "remove
  this one line". FAIL if it only asks to delete the single line, or misses a
  leaked line.

- **HG9-D9 - ADM removal as precondition, decoupled.** If the fixture has an
  ADM line on new inventory, the draft must demand removal as a precondition.
  FAIL if it proposes a middle-meet / smaller ADM, OR couples ADM removal to
  financing or any other concession.

- **HG10-D10 - Bait-and-switch handling.** If the fixture is a "just sold"
  pivot, the draft must (a) ask for sold-date proof in writing AND (b) require
  the substitute VIN to land at or under the original OTD adjusted only for
  legitimate config delta. FAIL if it blindly accepts the pivot ("ok, what's
  the OTD on the new one?") with no proof ask and no re-anchor.

## Soft criteria (advisory)

- **SC1 - One thank-you, at the open only.** Single thank-you in the greeting
  region; no repeated gratitude/softeners ("just", "I hope you're well").

- **SC2 - Imperative voice.** "Please remove" not "I would appreciate if you
  could possibly".

- **SC3 - Cash/close posture present.** Mentions buyer posture (cash buyer,
  cashier's check, close window) to add leverage, when applicable.

- **SC4 - Sign-off form.** Ends with `Thanks,` then buyer first name only; no
  leading dash, no em-dash, consistent name.

## Scoring output (for the LLM judge)

Return JSON:

```json
{
  "fixture_id": "D8_ct_tire_fee",
  "hard_gates": {"HG1": true, "HG2": true, "...": true},
  "soft_criteria": {"SC1": true, "...": false},
  "accepted": true,
  "failed_gates": [],
  "rationale": "one short paragraph"
}
```

`accepted` = true iff every applicable hard gate is true.
