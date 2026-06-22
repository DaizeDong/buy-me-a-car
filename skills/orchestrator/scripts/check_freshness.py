#!/usr/bin/env python3
"""
check_freshness.py — data-freshness gate for the single-source-of-truth
state-fees dataset (and, by extension, the broader fee universe).

Reads data/state_fees.json and reports records that are STALE, meaning either:
  - `verified` is false (never web-confirmed in Round 2), or
  - `source_verified_date` is missing, unparseable, or older than the staleness
    window (default 12 months).

This script is a *reporter*, not a gate that blocks: it always exits 0 so it can
be wired into refresh cron / pre-flight checks without breaking pipelines. Use
the printed report (or --json) to decide what to re-verify. Pass --strict to
make it exit 1 when any stale record is found (useful in CI).

It NEVER edits state_fees.json — it only reads.

Usage:
  python check_freshness.py                  # human report to stdout, exit 0
  python check_freshness.py --months 6       # use a 6-month staleness window
  python check_freshness.py --json           # machine-readable JSON report
  python check_freshness.py --strict         # exit 1 if anything is stale
  python check_freshness.py --json-path PATH # point at an alternate dataset
  python check_freshness.py --quiet          # suppress the fresh-records list
"""
import argparse
import datetime as _dt
import json
import os
import sys

# repo root is three levels up from skills/orchestrator/scripts/
DEFAULT_JSON = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "state_fees.json")
)

DEFAULT_STALE_MONTHS = 12


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_date(value):
    """Parse an ISO YYYY-MM-DD date. Return a date or None if unparseable."""
    if not value or not isinstance(value, str):
        return None
    try:
        return _dt.date.fromisoformat(value.strip())
    except ValueError:
        # tolerate a leading/trailing timestamp or extra tokens
        token = value.strip().split()[0] if value.strip() else ""
        try:
            return _dt.date.fromisoformat(token)
        except ValueError:
            return None


def months_between(older, newer):
    """Approximate whole-month gap between two dates (newer - older)."""
    return (newer.year - older.year) * 12 + (newer.month - older.month) - (
        1 if newer.day < older.day else 0
    )


def assess_record(rec, today, stale_months):
    """
    Classify a single record. Returns (status, reason) where status is one of
    'fresh' | 'unverified' | 'stale_date' | 'no_date'.
    """
    if not rec.get("verified"):
        return "unverified", "verified flag is false (never R2 web-confirmed)"

    raw = rec.get("source_verified_date")
    d = parse_date(raw)
    if d is None:
        return "no_date", f"verified=true but source_verified_date is missing/unparseable ({raw!r})"

    age = months_between(d, today)
    if age >= stale_months:
        return "stale_date", f"source_verified_date {d.isoformat()} is ~{age} months old (>= {stale_months})"
    return "fresh", f"source_verified_date {d.isoformat()} (~{age} months old)"


def main():
    p = argparse.ArgumentParser(
        description="Flag stale / unverified records in state_fees.json (always exits 0 unless --strict)."
    )
    p.add_argument("--json-path", default=DEFAULT_JSON, help="Path to state_fees.json")
    p.add_argument(
        "--months",
        type=int,
        default=DEFAULT_STALE_MONTHS,
        help=f"Staleness window in months (default {DEFAULT_STALE_MONTHS}).",
    )
    p.add_argument("--json", action="store_true", help="Emit a machine-readable JSON report instead of prose.")
    p.add_argument("--strict", action="store_true", help="Exit 1 if any record is stale/unverified.")
    p.add_argument("--quiet", action="store_true", help="Do not list the fresh records.")
    args = p.parse_args()

    if not os.path.exists(args.json_path):
        print(f"ERROR: data file not found: {args.json_path}", file=sys.stderr)
        # still exit 0 per contract unless strict
        sys.exit(1 if args.strict else 0)

    data = load(args.json_path)
    records = data.get("states", [])
    today = _dt.date.today()

    buckets = {"fresh": [], "unverified": [], "stale_date": [], "no_date": []}
    for rec in records:
        status, reason = assess_record(rec, today, args.months)
        buckets[status].append(
            {
                "state": rec.get("state", "??"),
                "status": status,
                "reason": reason,
                "verified": bool(rec.get("verified")),
                "source_verified_date": rec.get("source_verified_date"),
                "detail_depth": rec.get("detail_depth"),
            }
        )

    stale = buckets["unverified"] + buckets["stale_date"] + buckets["no_date"]
    stale_states = sorted(s["state"] for s in stale)

    if args.json:
        report = {
            "checked_at": today.isoformat(),
            "json_path": args.json_path,
            "stale_window_months": args.months,
            "total_records": len(records),
            "counts": {k: len(v) for k, v in buckets.items()},
            "stale_states": stale_states,
            "records": {k: v for k, v in buckets.items()},
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        sys.exit(1 if (args.strict and stale) else 0)

    # human-readable report
    print(f"# Data Freshness Report — {os.path.basename(args.json_path)}")
    print(f"> checked_at: {today.isoformat()} | stale window: {args.months} months | total records: {len(records)}")
    print()
    print(
        f"counts: fresh={len(buckets['fresh'])} "
        f"unverified={len(buckets['unverified'])} "
        f"stale_date={len(buckets['stale_date'])} "
        f"no_date={len(buckets['no_date'])}"
    )
    print()

    if stale:
        print(f"## STALE / UNVERIFIED ({len(stale)} records) — re-verify these")
        for label, key in (
            ("Unverified (verified=false)", "unverified"),
            ("Verified but date is stale", "stale_date"),
            ("Verified but no usable date", "no_date"),
        ):
            rows = buckets[key]
            if not rows:
                continue
            print(f"\n### {label} ({len(rows)})")
            for r in sorted(rows, key=lambda x: x["state"]):
                print(f"  - {r['state']}: {r['reason']}")
        print(f"\nstale_states: {', '.join(stale_states)}")
    else:
        print("## All records fresh — nothing to re-verify.")

    if not args.quiet and buckets["fresh"]:
        print(f"\n## FRESH ({len(buckets['fresh'])})")
        for r in sorted(buckets["fresh"], key=lambda x: x["state"]):
            print(f"  - {r['state']}: {r['reason']}")

    sys.exit(1 if (args.strict and stale) else 0)


if __name__ == "__main__":
    main()
