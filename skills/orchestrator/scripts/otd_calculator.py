#!/usr/bin/env python3
"""
OTD Calculator — reverse-engineer sales price from target OTD given state tax and fees.

Supports all 50 US states + DC.

State tax rates, doc-fee caps, title fees, and registration fees are loaded from
the single source of truth at data/state_fees.json (NOT inlined here). Edit that
file to change any state value; this calculator only consumes it.

Usage:
  python otd_calculator.py --target 30000 --state NJ --doc 499
  python otd_calculator.py --target 30000 --state CA --doc 85 --local 1
  python otd_calculator.py --sales 25000 --state TX --doc 150 --forward
  python otd_calculator.py --list-states

Note: Tax rates are state-level base rates. For accurate combined rates including
local sales tax, pass --local <pct> for buyer's county/city additional tax.
"""
import argparse
import json
import os
import sys

# data/state_fees.json lives at the repo root; this file is at
# skills/orchestrator/scripts/otd_calculator.py -> repo root is three levels up.
DATA_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "state_fees.json")
)


def _load_state_data(path=DATA_PATH):
    """Load state_fees.json and project it into the lookup dicts the calculator uses.

    Returns (tax_rates, default_reg, default_title, doc_fee_cap), each keyed by
    state code, preserving the structure the rest of this module expects.
    """
    if not os.path.exists(path):
        sys.exit(f"ERROR: state data file not found: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    tax_rates, default_reg, default_title, doc_fee_cap = {}, {}, {}, {}
    for rec in data["states"]:
        s = rec["state"]
        tax_rates[s] = rec["tax_state"]
        default_reg[s] = rec["reg_1yr"]
        default_title[s] = rec["title"]
        doc_fee_cap[s] = rec.get("doc_cap")  # None when no statutory cap
    return tax_rates, default_reg, default_title, doc_fee_cap


STATE_TAX_RATES, STATE_DEFAULT_REG, STATE_DEFAULT_TITLE, STATE_DOC_FEE_CAP = _load_state_data()


def compute_otd(sales, doc, tax_rate, title, reg, addons=0):
    """Forward: compute OTD from components."""
    taxable = sales + doc
    tax = taxable * tax_rate
    otd = sales + doc + tax + title + reg + addons
    return {
        "sales": sales, "doc": doc, "tax": tax,
        "title": title, "reg": reg, "addons": addons, "otd": otd,
    }


def reverse_otd(target_otd, doc, tax_rate, title, reg, addons=0):
    """Reverse: compute required sales price given target OTD."""
    sales = (target_otd - doc * (1 + tax_rate) - title - reg - addons) / (1 + tax_rate)
    return compute_otd(sales, doc, tax_rate, title, reg, addons)


def main():
    p = argparse.ArgumentParser(
        description="OTD calculator (all 50 states + DC)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--target", type=float, help="Target OTD (reverse mode)")
    p.add_argument("--sales", type=float, help="Sales price (forward mode)")
    p.add_argument("--state", default="NJ", choices=sorted(STATE_TAX_RATES.keys()),
                   help="State or DC code (default: NJ)")
    p.add_argument("--doc", type=float, default=499, help="Doc fee (default 499)")
    p.add_argument("--local", type=float, default=0,
                   help="Local sales tax additional pct (e.g. 1 for 1 pct extra)")
    p.add_argument("--title", type=float, default=None, help="Title fee (state default if None)")
    p.add_argument("--reg", type=float, default=None, help="Registration fee (state default if None)")
    p.add_argument("--addons", type=float, default=0, help="Add-on charges")
    p.add_argument("--forward", action="store_true", help="Compute OTD from sales (default: reverse)")
    p.add_argument("--list-states", action="store_true", help="List all supported states and exit")
    args = p.parse_args()

    if args.list_states:
        print("Supported states (state-level base tax rates):")
        for s in sorted(STATE_TAX_RATES.keys()):
            cap = STATE_DOC_FEE_CAP.get(s)
            cap_str = f"${cap}" if cap else "no cap"
            print(f"  {s}: tax {STATE_TAX_RATES[s]*100:.4f}% | doc cap {cap_str}")
        return

    tax_rate = STATE_TAX_RATES[args.state] + args.local / 100.0
    title = args.title if args.title is not None else STATE_DEFAULT_TITLE[args.state]
    reg = args.reg if args.reg is not None else STATE_DEFAULT_REG[args.state]
    doc_cap = STATE_DOC_FEE_CAP[args.state]

    if doc_cap is not None and args.doc > doc_cap:
        print(f"WARNING: {args.state} caps doc fee at ${doc_cap}; your ${args.doc} exceeds cap")

    if args.forward:
        if args.sales is None:
            p.error("--sales required in forward mode")
        result = compute_otd(args.sales, args.doc, tax_rate, title, reg, args.addons)
    else:
        if args.target is None:
            p.error("--target required in reverse mode")
        result = reverse_otd(args.target, args.doc, tax_rate, title, reg, args.addons)

    print(f"State: {args.state} (combined tax {tax_rate*100:.4f}%)")
    print(f"Sales price:      ${result['sales']:>10,.2f}")
    print(f"Doc fee:          ${result['doc']:>10,.2f}")
    print(f"Sales tax:        ${result['tax']:>10,.2f}")
    print(f"Title fee:        ${result['title']:>10,.2f}")
    print(f"Registration:     ${result['reg']:>10,.2f}")
    print(f"Add-ons:          ${result['addons']:>10,.2f}")
    print(f"-" * 32)
    print(f"OTD total:        ${result['otd']:>10,.2f}")

    if doc_cap is not None:
        print(f"\nNote: {args.state} doc fee statutory cap = ${doc_cap}")


if __name__ == "__main__":
    main()
