# Rubric: Skill Routing

Judge whether the model dispatched the correct skill for a user prompt.
Input: one case from fixtures/routing_prompts.json plus the model's chosen
skill name. This is a single-label classification check.

## Criteria

- **RT1 - Correct dispatch.** PASS if the model's chosen skill is in the
  case's `acceptable_skills` list (which always includes `expected_skill`).
  FAIL otherwise.

- **RT2 - Single skill.** The model commits to ONE skill, not a menu
  ("maybe X or Y"). Picking a defensible single skill from a genuinely
  ambiguous prompt is correct; hedging across all of them is not. Advisory:
  note it but RT1 governs pass/fail.

- **RT3 - No phantom skill.** The chosen skill exists in `_meta.skill_universe`.
  FAIL on a hallucinated skill name.

## Discriminations the judge should reward

- Full lifecycle intent ("buy me a car", "帮我找车") => `orchestrator`, NOT a
  narrow sub-skill.
- One dealer email in hand to answer => `dealer-reply-drafter`, NOT
  `orchestrator`.
- Hunting for online quote screenshots to use as anchors =>
  `quote-evidence-collector`, NOT `dealer-reply-drafter` (which consumes
  anchors already in hand).
- A planted gotcha (D8/D9/D10) inside a quote that needs a reply =>
  `dealer-reply-drafter`, because the gotcha logic lives there as a sub-skill;
  it does not require spinning up the 9-phase orchestrator.
- Pure fee/tax fact question with no draft requested => `state-fee-lookup`.
- Close imminent ("signing tomorrow") => `close-day-checklist`.

## Scoring output

```json
{
  "case_id": "R03",
  "chosen_skill": "dealer-reply-drafter",
  "RT1": true,
  "RT3": true,
  "pass": true
}
```

Aggregate: routing accuracy = (# cases with RT1 true) / (total cases).
