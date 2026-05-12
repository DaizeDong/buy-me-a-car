#!/usr/bin/env python3
"""
OTD Calculator — reverse-engineer sales price from target OTD given state tax and fees.

Supports all 50 US states + DC.

Usage:
  python otd_calculator.py --target 30000 --state NJ --doc 499
  python otd_calculator.py --target 30000 --state CA --doc 85 --local 1
  python otd_calculator.py --sales 25000 --state TX --doc 150 --forward
  python otd_calculator.py --list-states

Note: Tax rates are state-level base rates. For accurate combined rates including
local sales tax, pass --local <pct> for buyer's county/city additional tax.
"""
import argparse
import sys

# State sales tax rates (state-level base, as of 2026 knowledge cutoff)
# Verify with state DMV for current rates before any transaction
STATE_TAX_RATES = {
    "AL": 0.02, "AK": 0.00, "AZ": 0.056, "AR": 0.065, "CA": 0.0725,
    "CO": 0.029, "CT": 0.0635, "DE": 0.0425, "DC": 0.07, "FL": 0.06,
    "GA": 0.04, "HI": 0.04, "ID": 0.06, "IL": 0.0625, "IN": 0.07,
    "IA": 0.06, "KS": 0.065, "KY": 0.06, "LA": 0.0445, "ME": 0.055,
    "MD": 0.06, "MA": 0.0625, "MI": 0.06, "MN": 0.065, "MS": 0.07,
    "MO": 0.04225, "MT": 0.00, "NE": 0.055, "NV": 0.0685, "NH": 0.00,
    "NJ": 0.06625, "NM": 0.04, "NY": 0.04, "NC": 0.03, "ND": 0.05,
    "OH": 0.0575, "OK": 0.045, "OR": 0.00, "PA": 0.06, "RI": 0.07,
    "SC": 0.05, "SD": 0.045, "TN": 0.07, "TX": 0.0625, "UT": 0.0485,
    "VT": 0.06, "VA": 0.0415, "WA": 0.065, "WV": 0.06, "WI": 0.05,
    "WY": 0.04,
}

# State default registration fee (typical for sedan/SUV; varies by weight)
STATE_DEFAULT_REG = {
    "AL": 30, "AK": 100, "AZ": 50, "AR": 25, "CA": 250, "CO": 90, "CT": 80,
    "DE": 50, "DC": 70, "FL": 225, "GA": 20, "HI": 45, "ID": 70, "IL": 151,
    "IN": 40, "IA": 100, "KS": 40, "KY": 65, "LA": 50, "ME": 35, "MD": 135,
    "MA": 70, "MI": 100, "MN": 100, "MS": 25, "MO": 50, "MT": 90, "NE": 30,
    "NV": 33, "NH": 90, "NJ": 70, "NM": 35, "NY": 100, "NC": 36, "ND": 90,
    "OH": 31, "OK": 96, "OR": 100, "PA": 39, "RI": 30, "SC": 40, "SD": 75,
    "TN": 24, "TX": 51, "UT": 44, "VT": 70, "VA": 41, "WA": 80, "WV": 30,
    "WI": 75, "WY": 30,
}

# State default title fee
STATE_DEFAULT_TITLE = {
    "AL": 20, "AK": 15, "AZ": 4, "AR": 10, "CA": 25, "CO": 7, "CT": 25,
    "DE": 35, "DC": 26, "FL": 77, "GA": 18, "HI": 5, "ID": 14, "IL": 155,
    "IN": 15, "IA": 25, "KS": 10, "KY": 9, "LA": 69, "ME": 33, "MD": 100,
    "MA": 75, "MI": 15, "MN": 11, "MS": 9, "MO": 11, "MT": 10, "NE": 10,
    "NV": 29, "NH": 25, "NJ": 85, "NM": 5, "NY": 50, "NC": 56, "ND": 5,
    "OH": 15, "OK": 11, "OR": 122, "PA": 58, "RI": 52, "SC": 15, "SD": 10,
    "TN": 11, "TX": 33, "UT": 6, "VT": 35, "VA": 15, "WA": 15, "WV": 15,
    "WI": 165, "WY": 15,
}

# State doc fee cap (None = no statutory cap)
STATE_DOC_FEE_CAP = {
    "AL": None, "AK": None, "AZ": None, "AR": None,
    "CA": 85,
    "CO": None, "CT": None, "DE": None, "DC": None, "FL": None,
    "GA": None, "HI": None, "ID": None,
    "IL": 347.26,
    "IN": None, "IA": None, "KS": None, "KY": None,
    "LA": 200, "ME": None,
    "MD": 499,
    "MA": None,
    "MI": 230, "MN": 125,
    "MS": None, "MO": 599, "MT": None, "NE": None, "NV": None, "NH": None,
    "NJ": 799,
    "NM": None,
    "NY": 175,
    "NC": None, "ND": None,
    "OH": 250,
    "OK": None, "OR": None, "PA": None,
    "RI": 250,
    "SC": None, "SD": None, "TN": None,
    "TX": 150,
    "UT": None, "VT": None, "VA": None,
    "WA": 200, "WV": 199,
    "WI": None, "WY": None,
}


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
