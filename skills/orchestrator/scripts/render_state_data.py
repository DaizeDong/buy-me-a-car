#!/usr/bin/env python3
"""Render reviewed state fields; unknown values never appear as authoritative fees."""
import argparse
from decimal import Decimal
from pathlib import Path
import sys

from check_freshness import DEFAULT_JSON, REFERENCE_FIELDS, load, validate_dataset

ROOT = Path(__file__).resolve().parents[3]
START = "<!-- state-data:start -->"
END = "<!-- state-data:end -->"
SURFACES = (
    ROOT / "skills/orchestrator/references/state_fees.md",
    ROOT / "skills/otd-calculator/SKILL.md",
    ROOT / "skills/state-fee-lookup/SKILL.md",
)


def fmt_pct(rate):
    return f"{Decimal(str(rate)) * 100:f}".rstrip("0").rstrip(".") + "%"


def fmt_cap(cap):
    return f"${cap:g}" if cap is not None else "No numeric cap verified"


def fmt_trade(rule):
    schedule = rule.get("annual_schedule")
    if schedule:
        return f"Up to ${rule['cap']:,} ({rule['cap_year']}); annual schedule"
    if rule["posture"] == "yes":
        return "Full eligible allowance"
    if rule["posture"] == "no":
        return "No tax credit"
    if rule.get("cap") is not None:
        return f"Up to ${rule['cap']:,}"
    return "Not applicable"


def reviewed(rec, field, formatter=str):
    proof = rec["field_provenance"][field]
    if proof["status"] != "verified":
        return "Unverified"
    return formatter(rec[field])


def reviewed_rate(rec):
    rate = reviewed(rec, "tax_state", fmt_pct)
    rules = rec.get("tax_rules", {})
    if rec["field_provenance"].get("tax_rules", {}).get("status") == "verified":
        if "luxury_rate" in rules:
            rate += f"; {fmt_pct(rules['luxury_rate'])} over ${rules['luxury_threshold']:,}"
        if rules.get("local") == "required":
            rate += " + supplied local rate"
    return rate


def render_table(records, only_unverified=False):
    rows = sorted(records, key=lambda r: r["state"])
    if only_unverified:
        rows = [r for r in rows if any(r["field_provenance"][f]["status"] != "verified" for f in REFERENCE_FIELDS)]
    lines = ["| State | Reviewed tax rate | Doc cap | Title | Registration | Trade credit | Calculator profile |",
             "|---|---|---|---|---|---|---|"]
    for rec in rows:
        profile = rec["calculator"]["status"]
        if profile == "supported" and rec["tax_rules"].get("conditions"):
            profile += " (" + "/".join(rec["tax_rules"]["conditions"]) + " only)"
        cells = [rec["state"], reviewed_rate(rec),
                 reviewed(rec, "doc_cap", fmt_cap), reviewed(rec, "title", lambda v: f"${v:g}"),
                 reviewed(rec, "reg_1yr", lambda v: f"${v:g}"), reviewed(rec, "trade_credit", fmt_trade),
                 profile]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def replace_table(text, table):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Exactly one state-data marker pair is required")
    before, remainder = text.split(START)
    _, after = remainder.split(END)
    return before + START + "\n" + table + "\n" + END + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", default=DEFAULT_JSON, help="State dataset path")
    parser.add_argument("--unverified", action="store_true")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write-references", action="store_true")
    action.add_argument("--check", action="store_true", help="Verify all three generated tables match JSON")
    args = parser.parse_args()
    try:
        data = load(args.json)
        errors = validate_dataset(data)
        if errors:
            raise ValueError("; ".join(errors))
        if args.unverified and (args.check or args.write_references):
            raise ValueError("Reference tables always contain all 51 states; omit --unverified")
        table = render_table(data["states"], args.unverified)
        if args.write_references or args.check:
            drift = []
            for path in SURFACES:
                old = path.read_text(encoding="utf-8")
                new = replace_table(old, table)
                if args.write_references:
                    path.write_text(new, encoding="utf-8")
                elif old != new:
                    drift.append(path.relative_to(ROOT).as_posix())
            if drift:
                raise ValueError("Generated state tables differ: " + ", ".join(drift))
            print("Three state tables " + ("updated" if args.write_references else "verified"))
        else:
            print("Reviewed values only; source dates and applicability are in field_provenance. A supported tax profile still needs a runtime freshness check and explicit fees.\n")
            print(table)
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
