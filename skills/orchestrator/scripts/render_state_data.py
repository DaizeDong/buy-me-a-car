#!/usr/bin/env python3
"""
render_state_data.py — render the single-source-of-truth state_fees.json as a
markdown summary table, for cross-checking against the prose in
references/state_fees.md.

The JSON at data/state_fees.json is authoritative. This script never edits it;
it only renders. Use it to detect drift between the structured data and the
hand-written reference prose.

Usage:
  python render_state_data.py                 # full markdown table to stdout
  python render_state_data.py --unverified    # only rows still needing R2 web verify
  python render_state_data.py --json PATH      # point at an alternate json
"""
import argparse
import json
import os
import sys

DEFAULT_JSON = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "state_fees.json")
)
# repo root is three levels up from skills/orchestrator/scripts/
REPO_ROOT_JSON = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "state_fees.json")
)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fmt_pct(rate):
    return f"{rate * 100:.4f}".rstrip("0").rstrip(".") + "%"


def fmt_cap(cap):
    return f"${cap:g}" if cap is not None else "None"


def fmt_trade(tc):
    posture = tc.get("posture", "?")
    cap = tc.get("cap")
    if cap is not None:
        return f"{posture} (cap ${cap:,})"
    return posture


def fmt_ev(ev):
    return f"${ev:g}" if ev is not None else "-"


def render_table(records, only_unverified=False):
    rows = records
    if only_unverified:
        rows = [r for r in records if not r.get("verified")]
    rows = sorted(rows, key=lambda r: r["state"])

    out = []
    out.append(
        "| State | Tax (state) | Local Typ | Mechanism | Doc Cap | Doc Eff | Title | Reg 1yr | Trade Credit | EV Surcharge | Depth | Verified |"
    )
    out.append(
        "|-------|-------------|-----------|-----------|---------|---------|-------|---------|--------------|--------------|-------|----------|"
    )
    for r in rows:
        out.append(
            "| {state} | {tax} | {local} | {mech} | {cap} | {eff} | ${title} | ${reg} | {trade} | {ev} | {depth} | {ver} |".format(
                state=r["state"],
                tax=fmt_pct(r["tax_state"]),
                local=r.get("tax_local_typ", "") or "",
                mech=r.get("tax_mechanism", ""),
                cap=fmt_cap(r.get("doc_cap")),
                eff=r.get("doc_cap_effective_date") or "-",
                title=r.get("title"),
                reg=r.get("reg_1yr"),
                trade=fmt_trade(r.get("trade_credit", {})),
                ev=fmt_ev(r.get("ev_reg_surcharge")),
                depth=r.get("detail_depth", ""),
                ver="yes" if r.get("verified") else "NO",
            )
        )
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Render state_fees.json as a markdown table")
    p.add_argument("--json", default=REPO_ROOT_JSON, help="Path to state_fees.json")
    p.add_argument("--unverified", action="store_true", help="Only show rows where verified=false")
    args = p.parse_args()

    if not os.path.exists(args.json):
        print(f"ERROR: data file not found: {args.json}", file=sys.stderr)
        sys.exit(1)

    data = load(args.json)
    records = data["states"]
    meta = data.get("_meta", {})

    print(f"# State Fees — rendered from {os.path.basename(args.json)}")
    print()
    print(f"> records: {len(records)} | seed_date: {meta.get('seed_date', '?')}")
    verified_states = [r["state"] for r in records if r.get("verified")]
    print(f"> verified (R2-confirmed): {', '.join(verified_states) if verified_states else 'none'}")
    print()
    print(render_table(records, only_unverified=args.unverified))
    print()
    print("Doc cap history / statute (where recorded):")
    for r in sorted(records, key=lambda x: x["state"]):
        if r.get("doc_cap_statute") or r.get("doc_cap_history"):
            print(
                f"- {r['state']}: cap {fmt_cap(r.get('doc_cap'))}"
                f"{' eff ' + r['doc_cap_effective_date'] if r.get('doc_cap_effective_date') else ''}"
                f"{' | ' + r['doc_cap_statute'] if r.get('doc_cap_statute') else ''}"
                f"{' | history: ' + r['doc_cap_history'] if r.get('doc_cap_history') else ''}"
            )


if __name__ == "__main__":
    main()
