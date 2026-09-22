# Dealer Reply Templates

This file is an uninitialized template. Real sentences, names, policies and quote
evidence belong in the private companion data directory, never in this file.

## Voice Specification

Use direct ASCII English, one to three numbered asks, at most one evidence-backed
anchor, and a consistent greeting/sign-off. Avoid flattery, invented urgency and
claims that documents are attached before attachment verification. A draft must
remain under ten content lines, excluding greeting, sign-off and blank lines.

`WALK_AWAY` / `walk_away` is private, in every round. Do not disclose a derived range,
monthly ceiling, internal financing capacity or a "hard cap". `authorized_offer`
is a separate user-approved proposal. Do not populate it from the private ceiling.
Use a nonnumeric exit; it does not need to claim an existing competing offer.

## Executable plan

The model selects IDs from a private approved policy:

```json
{
  "ask_ids": ["breakdown"],
  "anchor_ids": [],
  "include_offer": false
}
```

This is a schema example with symbolic IDs. It contains no scenario data.
`scripts/email_policy.py` renders and validates the plan. Any modified freeform
body is blocked until its content is incorporated into approved inputs.

## Rendered structure

```text
Hi {REP_NAME},

1) {APPROVED_ASK_1}
2) {APPROVED_ASK_2_IF_SELECTED}
3) {APPROVED_ASK_3_IF_SELECTED}

{AUTHORIZED_OFFER_IF_SELECTED}

{CONFIRMED_ANCHOR_IF_SELECTED}

If that does not work, I will continue my search.

Thanks,
{BUYER_FIRST_NAME}
```

The renderer omits unselected lines; it never prints placeholders. A listing
anchor names the seller, vehicle and asking price. A written OTD anchor explicitly
labels the amount out-the-door and says it was quoted in writing. Do not convert
between the two labels without new evidence.

## Common plans

| Situation | Selection |
|---|---|
| Missing quote details | One approved breakdown ask; no price or anchor required |
| Counter | Approved correction asks, optional confirmed anchor and authorized offer |
| Markup removal | Removal ask independent of financing concessions |
| Replacement vehicle | Availability confirmation and complete substitute quote asks |
| Walk-away | Use a separately buyer-approved closing sentence; no private budget |

## Saving and review

Follow `references/outbound_email_sop.md`. Local preparation is not a Gmail save.
Report a saved draft only after importing the provider receipt matching its account,
operation ID and body hash. Preserve uncertain execution for reconciliation and
never replay it automatically. Sending requires the buyer's authorization and is
outside the ledger's supported operations.
