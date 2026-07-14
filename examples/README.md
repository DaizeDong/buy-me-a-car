# Examples

This folder holds eight worked scenarios that fixed the buy-me-a-car skill
into its current shape. Each one is a buyer profile, a target vehicle, a
set of constraints, and a record of which sub-skills fired in what order.

Scenarios 01-05 are the foundation set (cash / financing / trade / EV /
pickup on the dealer path). Scenarios 06-08 are regression fixtures for
paths that were already supported in the reference files but had no
end-to-end example: leasing, the private-party (FSBO) path, and Stellantis
CPO.

You can read them as standalone stories (~2-minute narratives each) or as
fixtures you replay against the skill to verify that your local copy still
handles the cases.

## What is in each scenario file

Each `0X_<name>.md` file has two sections:

- **Scenario** — the buyer profile, the target, the constraints, and the
  ask. Standalone-readable.
- **Outcome** — which sub-skills fired in what order, what artifacts the
  workflow produced, which gotchas / Critical Rules fired, and what the
  scenario surfaced as a reference-file or SKILL.md delta.

The scenarios are synthetic. No real outreach was sent. Numbers, dealers,
and counterparty names are stand-ins.

## Recommended reading order

Read in numeric order — each one stacks one new structural axis on top
of the last.

| # | Scenario | New axis | Sub-skills stressed |
|---|---|---|---|
| 01 | Used Outback CT cash | (baseline) cash + used + single state | `state-fee-lookup`, `otd-calculator`, `cpo-eligibility`, `dealer-reply-drafter` |
| 02 | New RAV4 Hybrid PA financing | + financing + new car + cross-state radius | `payment-method-decider`, `state-fee-lookup` (PA), `dealer-reply-drafter` (ADM kill) |
| 03 | Used CR-V CA cash + trade | + trade-in + California fee depth + Honda CPO | `trade-in-valuator`, `state-fee-lookup` (CA), `cpo-eligibility` (Honda) |
| 04 | New Ioniq 5 EV TX cash | + EV credit mechanics + §30D POS transfer + NACS-vs-CCS1 | `ev-buyer-helper`, `lease-vs-cash-analyzer`, `state-fee-lookup` (TX) |
| 05 | Used F-150 IL financing + trade-with-lien | + pickup specifics + lien payoff + IL $10k trade cap | `trade-in-valuator` (lien), `payment-method-decider`, `state-fee-lookup` (IL), `ppi-scheduler` (pickup), `close-day-checklist` (pickup) |
| 06 | New GLC 300 lease NY 36/12k | + lease path + OTD-calc suppression + NY lump-sum lease tax | `lease-vs-cash-analyzer` (MBFS captive, buy-rate MF), `state-fee-lookup` (NY), `dealer-reply-drafter` (lease counter) |
| 07 | Used Civic private-party (FSBO) NJ cash | + dealer-vs-private-party router + no-OTD/no-F&I model + curbstoner threat model | `state-fee-lookup` (NJ tax/title/reg only), `ppi-scheduler` (gating), `carfax-pdf-review` (no F&I detector), `dealer-reply-drafter` (single-seller) |
| 08 | CPO Grand Cherokee Stellantis TX cash | + Stellantis SPOTiCAR CPO + age-sensitive embedded value + TX $225 doc-cap truth | `cpo-eligibility` (Stellantis branch), `state-fee-lookup` (TX), `otd-calculator`, `dealer-reply-drafter` (CPO-premium counter) |

If you only have time for one, read 01 to see the clean baseline path.
If you only have time for two, read 01 + 03 — those two cover the most
common buyer types. For the path-coverage regression fixtures, read
06 (lease), 07 (private-party), and 08 (Stellantis CPO).

## How to replay a scenario

Pick a scenario file. Copy the buyer profile and constraints from the
Scenario section into your own prompt to Claude Code. The skill should
trigger the same sub-skill firing order described in the Outcome section.
Any material divergence is a regression in the skill or a drift in source
data (state fees update annually; CPO terms shift mid-year; EV credits
change with federal Treasury guidance).

If you find a regression, open a GitHub issue. The scenarios are the
canonical fixtures for verifying skill state.

## Caveats

- These are **synthetic** scenarios. The skill has not been broadly
  validated end-to-end across multiple real purchases yet. The author
  has used the skill on a single real purchase only.
- State fee data drifts over time. Fee numbers in the fixtures trace to
  `data/state_fees.json`; that file's per-record `verified` flag matters.
  In scenarios 06-07 the NY and NJ records are seed values
  (`verified: false`) pending Round 2 web confirmation; in scenario 08 the
  TX record is ground-truth verified (`verified: true`, with `source_url`
  and `source_verified_date: 2026-06-22`). Re-verify any unverified record
  before quoting a live buyer.
- CPO terms vary by region; what the reference file claims for "Honda
  True Certified+ premium tier" or the Stellantis SPOTiCAR embedded-value
  range may not match your local dealer's current offering. CPO
  embedded-value dollar figures are negotiating anchors derived from
  extended-warranty quote data, not published OEM list prices.
- EV credit mechanics (§30D, §25E, §45W) are subject to Treasury
  rulemaking and may change without warning.

Verify against current sources before quoting numbers to a dealer or
making a financial decision. Not tax, legal, or financial advice.

## Related

- [Top-level README](../README.md) for the broader skill overview.
- [`skills/orchestrator/SKILL.md`](../skills/orchestrator/SKILL.md) for
  the full 9-phase workflow.
- [`ROADMAP.md`](../ROADMAP.md) for what is still missing (e.g. the
  commercial-vehicle axis). Lease (06), private-party (07), and Stellantis
  CPO (08) scenarios are now covered by the fixtures above.
