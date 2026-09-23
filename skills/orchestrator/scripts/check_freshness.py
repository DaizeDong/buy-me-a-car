#!/usr/bin/env python3
"""Gate state-data structure and field evidence. --report-only permits unverified fields.

Malformed, empty, duplicate, or incomplete datasets always fail.
"""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

DEFAULT_JSON = Path(__file__).resolve().parents[3] / "data/state_fees.json"
DEFAULT_STALE_MONTHS = 3
STATE_CODES = frozenset("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
REFERENCE_FIELDS = ("tax_state", "tax_mechanism", "doc_cap", "title", "reg_1yr", "trade_credit", "ev_reg_surcharge")
REQUIRED_RULE_FIELDS = ("tax_state", "tax_mechanism", "trade_credit", "tax_rules")


def load(path):
    with open(path, encoding="utf-8") as source:
        return json.load(source)


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def months_between(older, newer):
    return (newer.year - older.year) * 12 + newer.month - older.month - (newer.day < older.day)


def valid_number(value, maximum=1000000000):
    return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= maximum


def valid_source(item):
    if not isinstance(item, dict) or not isinstance(item.get("source_url"), str) or not isinstance(item.get("source_quote"), str):
        return False
    try:
        url = urlparse(item["source_url"])
        return url.scheme == "https" and bool(url.hostname) and bool(item["source_quote"].strip())
    except ValueError:
        return False


def valid_sources(item):
    supporting = item.get("supporting_sources", [])
    return valid_source(item) and isinstance(supporting, list) and all(valid_source(source) for source in supporting)


def validate_dataset(data):
    """Return structural errors independently of freshness or coverage."""
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("_meta"), dict):
        return ["dataset must contain _meta and states"]
    if data["_meta"].get("schema_version") != 2:
        errors.append("schema_version must be 2 (field provenance required)")
    records = data.get("states")
    if not isinstance(records, list) or not records:
        return errors + ["states must be a nonempty list containing all 51 jurisdictions"]
    codes = [r.get("state") for r in records if isinstance(r, dict) and isinstance(r.get("state"), str)]
    if len(codes) != len(records) or len(set(codes)) != len(codes):
        errors.append("states must contain objects with unique state codes")
    if set(codes) != STATE_CODES or data["_meta"].get("records") != 51:
        errors.append("dataset must contain exactly the 50 states and DC; records must be 51")
    for rec in records:
        if not isinstance(rec, dict):
            continue
        code = rec.get("state", "?")
        evidence = rec.get("field_provenance")
        if not isinstance(evidence, dict):
            errors.append(f"{code}: missing field_provenance")
            continue
        for field in ("tax_state", "doc_cap", "title", "reg_1yr", "ev_reg_surcharge"):
            value = rec.get(field)
            if value is not None and not valid_number(value, 1 if field == "tax_state" else 1000000000):
                errors.append(f"{code}.{field}: invalid finite nonnegative number")
        if not isinstance(rec.get("tax_mechanism"), str) or not rec["tax_mechanism"]:
            errors.append(f"{code}.tax_mechanism: nonempty string required")
        trade = rec.get("trade_credit")
        if not isinstance(trade, dict) or trade.get("posture") not in {"yes", "no", "partial", "na"}:
            errors.append(f"{code}.trade_credit: invalid rule")
        elif trade.get("posture") == "partial":
            if not valid_number(trade.get("cap")) or type(trade.get("cap_year")) is not int:
                errors.append(f"{code}.trade_credit: partial credit requires a numeric cap and year")
            schedule = trade.get("annual_schedule")
            if schedule is not None:
                if (not isinstance(schedule, dict)
                        or type(schedule.get("base_year")) is not int
                        or type(schedule.get("unlimited_from_year")) is not int
                        or not valid_number(schedule.get("base_cap"))
                        or not valid_number(schedule.get("yearly_increase"))
                        or schedule["unlimited_from_year"] <= schedule["base_year"]):
                    errors.append(f"{code}.trade_credit: invalid annual schedule")
                elif type(trade.get("cap_year")) is int:
                    year = trade["cap_year"]
                    expected = schedule["base_cap"] + schedule["yearly_increase"] * (year - schedule["base_year"])
                    if not schedule["base_year"] <= year < schedule["unlimited_from_year"] or trade.get("cap") != expected:
                        errors.append(f"{code}.trade_credit: displayed cap/year disagrees with annual schedule")
        profile = rec.get("calculator")
        if not isinstance(profile, dict) or profile.get("status") not in {"supported", "unsupported"}:
            errors.append(f"{code}.calculator: explicit support status required")
        elif profile["status"] == "supported":
            if profile.get("required_fields") != list(REQUIRED_RULE_FIELDS):
                errors.append(f"{code}.calculator: required evidence fields cannot be omitted")
            rules = rec.get("tax_rules")
            if not isinstance(rules, dict):
                errors.append(f"{code}.tax_rules: supported calculator requires rules")
            else:
                if type(rules.get("doc_taxable")) is not bool or rules.get("local") not in {"none", "required", "capped"}:
                    errors.append(f"{code}.tax_rules: invalid documentary/local treatment")
                for key in ("minimum_tax", "minimum_supported_base"):
                    value = rules.get(key)
                    if not valid_number(value):
                        errors.append(f"{code}.tax_rules.{key}: invalid amount")
                for key in ("local_base_cap", "doc_exemption_limit", "luxury_threshold", "luxury_rate", "warranty_rate"):
                    if key in rules and not valid_number(rules[key], 1 if key.endswith("rate") else 1000000000):
                        errors.append(f"{code}.tax_rules.{key}: invalid amount or rate")
                if ("luxury_threshold" in rules) != ("luxury_rate" in rules):
                    errors.append(f"{code}.tax_rules: luxury threshold and rate must occur together")
                if rules.get("local") == "capped" and "local_base_cap" not in rules:
                    errors.append(f"{code}.tax_rules: capped local tax requires a base cap")
                if "conditions" in rules:
                    conditions = rules["conditions"]
                    if not isinstance(conditions, list) or not conditions or any(c not in ("new", "used") for c in conditions):
                        errors.append(f"{code}.tax_rules: invalid supported vehicle conditions")
        for field in REFERENCE_FIELDS:
            if field not in rec or field not in evidence:
                errors.append(f"{code}.{field}: value and provenance are required")
        for field, item in evidence.items():
            if not isinstance(item, dict) or item.get("status") not in {"verified", "unverified"}:
                errors.append(f"{code}.{field}: invalid provenance status")
            elif item["status"] == "unverified" and not item.get("reason"):
                errors.append(f"{code}.{field}: unverified field needs a reason")
            elif item["status"] == "verified":
                if field not in rec or "value" not in item or item["value"] != rec[field]:
                    errors.append(f"{code}.{field}: verified value does not match stored value")
                for key in ("source_url", "source_quote", "verified_on", "applicability"):
                    if not isinstance(item.get(key), str) or not item[key].strip():
                        errors.append(f"{code}.{field}: {key} must be a nonempty string")
                if not valid_sources(item):
                    errors.append(f"{code}.{field}: all source citations require an HTTPS URL and quote")
    return errors


def assess_field(rec, field, today, stale_months=DEFAULT_STALE_MONTHS, as_of=None):
    """Check evidence for the exact stored value used by a calculation."""
    if stale_months <= 0:
        return "invalid", "stale window must be positive"
    item = rec.get("field_provenance", {}).get(field)
    if not isinstance(item, dict) or item.get("status") != "verified":
        return "unverified", f"{field}: no verified field-level evidence"
    if field not in rec or "value" not in item or item["value"] != rec[field]:
        return "invalid", f"{field}: evidence value differs from stored value"
    if not valid_sources(item):
        return "invalid", f"{field}: every source requires an HTTPS URL and supporting quote"
    verified = parse_date(item.get("verified_on"))
    if verified is None:
        return "invalid", f"{field}: invalid verification date"
    if verified > today:
        return "invalid", f"{field}: verification date is in the future"
    if months_between(verified, today) >= stale_months:
        return "stale_date", f"{field}: evidence last checked {verified}"
    effective = item.get("effective_from")
    expiry = item.get("effective_until")
    start = parse_date(effective) if effective is not None else verified
    end = parse_date(expiry) if expiry is not None else None
    if start is None or (expiry is not None and end is None) or (end and start > end):
        return "invalid", f"{field}: invalid effective interval"
    target = as_of or today
    if target < start or (end and target > end):
        return "outside_effective_period", f"{field}: transaction date {target} is outside supported effective dates"
    return "fresh", f"{field}: exact value checked {verified}"


def assess_record(rec, today, stale_months, fields=None, as_of=None):
    fields = fields or REFERENCE_FIELDS
    failures = [assess_field(rec, f, today, stale_months, as_of) for f in fields]
    failures = [(status, reason) for status, reason in failures if status != "fresh"]
    if failures:
        return failures[0][0], "; ".join(reason for _, reason in failures)
    return "fresh", "all requested fields have current evidence for their stored values"


def require_fields(rec, fields, *, today=None, as_of=None):
    today = today or dt.date.today()
    status, reason = assess_record(rec, today, DEFAULT_STALE_MONTHS, fields, as_of)
    if status != "fresh":
        raise ValueError(f"{rec.get('state', '?')}: {reason}. Recheck the official source and update field provenance before calculating.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-path", default=DEFAULT_JSON)
    parser.add_argument("--months", type=int, default=DEFAULT_STALE_MONTHS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--strict", action="store_true", help="Fail on any unverified/stale field (default)")
    mode.add_argument("--report-only", action="store_true", help="Allow incomplete verification, never invalid structure")
    parser.add_argument("--state", choices=sorted(STATE_CODES))
    parser.add_argument("--calculator", action="store_true", help="Check only fields required by enabled calculation profiles")
    args = parser.parse_args()
    if args.months <= 0:
        parser.error("--months must be positive")
    try:
        data = load(args.json_path)
        errors = validate_dataset(data)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if errors:
        parser.error("; ".join(errors))
    records = [r for r in data["states"] if not args.state or r["state"] == args.state]
    today = dt.date.today()
    results = []
    for rec in records:
        if args.calculator:
            profile = rec.get("calculator", {})
            if profile.get("status") != "supported":
                if args.state:
                    results.append({"state": rec["state"], "status": "unsupported", "reason": profile.get("reason", "no supported profile")})
                continue
            fields = profile["required_fields"]
        else:
            fields = None
        status, reason = assess_record(rec, today, args.months, fields)
        results.append({"state": rec["state"], "status": status, "reason": reason})
    if not results:
        parser.error("no supported records were checked")
    counts = {status: sum(r["status"] == status for r in results) for status in sorted({r["status"] for r in results})}
    report = {"checked_at": today.isoformat(), "total_records": len(records), "checked_records": len(results), "counts": counts, "records": results}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Field evidence checked {today}: {counts}")
        for row in results:
            if not args.quiet or row["status"] != "fresh":
                print(f"{row['state']}: {row['status']}: {row['reason']}")
    return 1 if any(r["status"] != "fresh" for r in results) and not args.report_only else 0


if __name__ == "__main__":
    sys.exit(main())
