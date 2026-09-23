#!/usr/bin/env python3
"""Compute an OTD estimate with verified, explicitly scoped state tax rules.

Unsupported jurisdictions fail with instructions. Title and registration costs
must be supplied; a state headline rate is never a substitute for tax rules.
The low-level compute_otd/reverse_otd helpers are generic algebra, not state law.
"""
import argparse
import datetime as dt
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import sys

from check_freshness import REQUIRED_RULE_FIELDS, assess_field, load, parse_date, require_fields, validate_dataset

DATA_PATH = Path(__file__).resolve().parents[3] / "data/state_fees.json"
CENT = Decimal("0.01")
ZERO = Decimal("0.00")
MAX_MONEY = Decimal("1000000000")
SUPPORTED_MECHANISMS = {"excise", "motor_vehicle_sales_tax", "sut", "hut", "sales_tax"}


def number(value, name, maximum=MAX_MONEY):
    """Accept decimal text or numbers; reject booleans, nonfinite and negatives."""
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{name} must be a finite nonnegative number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{name} must be a finite nonnegative number") from None
    if not result.is_finite() or result < 0 or result > maximum:
        raise ValueError(f"{name} must be between 0 and {maximum}")
    return result


def money(value, name):
    result = number(value, name)
    if result != result.quantize(CENT):
        raise ValueError(f"{name} must have at most two decimal places")
    return result.quantize(CENT)


def _state_records(path=DATA_PATH):
    data = load(path)
    errors = validate_dataset(data)
    if errors:
        raise ValueError("Invalid state dataset: " + "; ".join(errors))
    return {rec["state"]: rec for rec in data["states"]}


def _load_state_data(path=DATA_PATH):
    """Compatibility lookup dictionaries, including unverified reference values.

    These dictionaries do not authorize a calculation; use compute_state_otd.
    """
    states = _state_records(path)
    return tuple({code: rec.get(field) for code, rec in states.items()} for field in ("tax_state", "reg_1yr", "title", "doc_cap"))


STATE_TAX_RATES, STATE_DEFAULT_REG, STATE_DEFAULT_TITLE, STATE_DOC_FEE_CAP = _load_state_data()


def _components(sales, doc, rate, title, reg, addons=0, *, taxable_addons=0,
                doc_taxable=True, credited_trade=0, minimum_tax=0, local_rate=0,
                local_base_cap=None, trade=0, trade_payoff=0):
    amounts = {name: money(value, name) for name, value in {
        "sales": sales, "doc": doc, "title": title, "reg": reg,
        "addons": addons, "taxable_addons": taxable_addons,
        "trade": trade, "trade_payoff": trade_payoff,
    }.items()}
    base = amounts["sales"] + (amounts["doc"] if doc_taxable else ZERO) + amounts["taxable_addons"]
    credited = min(money(credited_trade, "credited_trade"), base)
    taxable = base - credited
    state_tax = max(taxable * number(rate, "tax_rate", Decimal(1)), money(minimum_tax, "minimum_tax"))
    local_base = taxable if local_base_cap is None else min(taxable, money(local_base_cap, "local_base_cap"))
    tax = (state_tax + local_base * number(local_rate, "local_rate", Decimal(1))).quantize(CENT, rounding=ROUND_HALF_UP)
    total = sum(amounts[k] for k in ("sales", "doc", "title", "reg", "addons", "taxable_addons")) + tax
    return {**amounts, "credited_trade": credited, "taxable": taxable, "tax": tax,
            "otd": total, "balance_due": total - amounts["trade"] + amounts["trade_payoff"]}


def compute_otd(sales, doc, tax_rate, title, reg, addons=0):
    """Generic algebra: tax sales + doc; addons are explicitly nontaxable.

    Returns Decimal amounts rounded to cents. This helper has no state rules.
    """
    return _components(sales, doc, tax_rate, title, reg, addons)


def _reverse(target, calculate, *, minimum_sales=ZERO, upper_bound=None):
    """Find the highest cent-denominated sales price that does not exceed OTD."""
    target = money(target, "target_otd")
    low = int(money(minimum_sales, "minimum_sales") / CENT)
    high = int((target if upper_bound is None else min(target, upper_bound)) / CENT)
    if low > high or calculate(Decimal(low) * CENT)["otd"] > target:
        raise ValueError("Target OTD cannot cover the required fees, taxes and minimum supported sales price")
    while low < high:
        mid = (low + high + 1) // 2
        if calculate(Decimal(mid) * CENT)["otd"] <= target:
            low = mid
        else:
            high = mid - 1
    result = calculate(Decimal(low) * CENT)
    result["target_otd"] = target
    result["budget_remaining"] = target - result["otd"]
    return result


def reverse_otd(target_otd, doc, tax_rate, title, reg, addons=0):
    """Generic cent-safe sales ceiling for compute_otd, preserving its signature."""
    return _reverse(target_otd, lambda sales: compute_otd(sales, doc, tax_rate, title, reg, addons))


def _transaction_date(as_of, today):
    if as_of is None:
        return today
    date = as_of if isinstance(as_of, dt.date) else parse_date(as_of)
    if date is None or date > today:
        raise ValueError("as_of must be a YYYY-MM-DD transaction date no later than today; future law requires a new review")
    return date


def trade_credit_for_state(state, trade, *, as_of=None, today=None, data_path=DATA_PATH):
    """Production trade-credit rule; does not assert other tax rules are supported."""
    today = today or dt.date.today()
    date = _transaction_date(as_of, today)
    rec = _state_records(data_path).get(state.upper())
    if rec is None:
        raise ValueError("Unknown state code")
    require_fields(rec, ["trade_credit"], today=today, as_of=date)
    amount = money(trade, "trade")
    rule = rec["trade_credit"]
    if rule["posture"] == "no":
        return ZERO
    if rule["posture"] == "yes":
        return amount
    if rule["posture"] == "partial":
        schedule = rule.get("annual_schedule")
        if schedule:
            if date.year < schedule["base_year"]:
                raise ValueError("Trade-credit schedule does not cover this year")
            cap = None if date.year >= schedule["unlimited_from_year"] else schedule["base_cap"] + schedule["yearly_increase"] * (date.year - schedule["base_year"])
        else:
            if rule.get("cap_year") != date.year:
                raise ValueError("Trade-credit cap is not verified for the transaction year")
            cap = rule.get("cap")
        return amount if cap is None else min(amount, money(cap, "trade_credit_cap"))
    raise ValueError("Trade-in treatment is not encoded; verify this transaction with the tax agency")


def _prepare_state(state, title, reg, as_of, today, data_path, transaction, vehicle, local_rate, condition=None):
    today = today or dt.date.today()
    date = _transaction_date(as_of, today)
    records = _state_records(data_path)
    state = state.upper()
    if state not in records:
        raise ValueError(f"Unknown state {state}")
    rec = records[state]
    profile = rec.get("calculator", {})
    if profile.get("status") != "supported":
        raise ValueError(f"{state} calculation unsupported: {profile.get('reason', 'no verified profile')}")
    if transaction != "dealer_purchase" or vehicle != "passenger_ice":
        raise ValueError("Only ordinary dealer purchases of passenger ICE vehicles are encoded. Obtain a transaction-specific DMV/dealer calculation for leases, private sales, EVs, commercial vehicles or exemptions.")
    require_fields(rec, REQUIRED_RULE_FIELDS, today=today, as_of=date)
    if rec["tax_mechanism"] not in SUPPORTED_MECHANISMS:
        raise ValueError(f"Unsupported tax mechanism {rec['tax_mechanism']}")
    if title is None or reg is None:
        raise ValueError("Supply --title and --reg from the itemized DMV/dealer fees; state averages are not valid defaults")
    rules = rec["tax_rules"]
    if condition not in (None, "new", "used"):
        raise ValueError("condition must be new or used")
    if "conditions" in rules and condition not in rules["conditions"]:
        raise ValueError(f"{state} requires --condition {' or '.join(rules['conditions'])}; new-vehicle surcharges are not encoded")
    if rules["local"] == "none":
        if local_rate is not None and number(local_rate, "local_rate", Decimal(1)) != 0:
            raise ValueError(f"{state} vehicle tax does not use a local sales-tax stack")
        local_rate = ZERO
    elif local_rate is None:
        raise ValueError("Supply the verified buyer/dealer jurisdiction's --local percentage, including explicit 0 if none")
    return rec, date, today, local_rate


def compute_state_otd(sales, doc, state, title=None, reg=None, addons=0, *,
                      taxable_addons=0, trade=0, trade_payoff=0, local_rate=None,
                      as_of=None, today=None, data_path=DATA_PATH,
                      transaction="dealer_purchase", vehicle="passenger_ice",
                      condition=None, warranty=0):
    """Scoped state-tax estimate; gross OTD and net trade settlement stay separate.

    sales includes all taxable vehicle charges before any unencoded rebates.
    addons are explicitly nontaxable; taxable_addons is a separate amount.
    CT service/extended warranties must use warranty, never taxable_addons or
    sales. NY doc is only a separately stated qualifying title/registration fee.
    The caller must confirm fees and applicability; output is never a quote.
    """
    rec, date, today, local_rate = _prepare_state(state, title, reg, as_of, today, data_path, transaction, vehicle, local_rate, condition)
    doc = money(doc, "doc")
    rules = rec["tax_rules"]
    warnings = []
    if "doc_exemption_limit" in rules and doc > money(rules["doc_exemption_limit"], "doc_exemption_limit"):
        raise ValueError(f"{state} documentation fee exceeds the verified exemption/cap scope; obtain an itemized tax review")
    cap_status, _ = assess_field(rec, "doc_cap", today, as_of=date)
    if cap_status == "fresh" and rec["doc_cap"] is not None:
        if doc > money(rec["doc_cap"], "doc_cap"):
            raise ValueError(f"{state} doc fee exceeds verified statutory cap of ${rec['doc_cap']}; correct the quote before calculating")
    else:
        warnings.append("Documentary-fee legality/cap is not verified; supplied fee is used only as an arithmetic input.")
    warranty = money(warranty, "warranty")
    if warranty and "warranty_rate" not in rules:
        raise ValueError(f"{state} separate warranty treatment is not encoded; obtain a verified itemized tax classification")
    rate = number(rec["tax_state"], "tax_rate", Decimal(1))
    if "luxury_threshold" in rules:
        vehicle_price = money(sales, "sales") + doc + money(taxable_addons, "taxable_addons")
        threshold = money(rules["luxury_threshold"], "luxury_threshold")
        if warranty and vehicle_price <= threshold < vehicle_price + warranty:
            raise ValueError(f"{state} warranty-only threshold crossing requires an itemized tax review; warranty rate is verified but this classification is not")
        if vehicle_price > threshold:
            rate = number(rules["luxury_rate"], "luxury_rate", Decimal(1))
    credited = trade_credit_for_state(state, trade, as_of=date, today=today, data_path=data_path)
    result = _components(sales, doc, rate, title, reg, addons,
                         taxable_addons=taxable_addons, doc_taxable=rules["doc_taxable"],
                         credited_trade=credited, minimum_tax=rules["minimum_tax"],
                         local_rate=local_rate, local_base_cap=rules.get("local_base_cap"),
                         trade=trade, trade_payoff=trade_payoff)
    warranty_tax = (warranty * number(rules.get("warranty_rate", 0), "warranty_rate", Decimal(1))).quantize(CENT, rounding=ROUND_HALF_UP)
    result.update(warranty=warranty, vehicle_tax=result["tax"], warranty_tax=warranty_tax)
    result["tax"] += warranty_tax
    result["otd"] += warranty + warranty_tax
    result["balance_due"] += warranty + warranty_tax
    minimum = money(rules["minimum_supported_base"], "minimum_supported_base")
    if result["taxable"] < minimum:
        raise ValueError(f"{state}: taxable base below ${minimum} requires a separate valuation/minimum-tax review")
    if result["trade"] == 0 and result["trade_payoff"] != 0:
        raise ValueError("trade_payoff requires a trade-in allowance")
    sources = {rec["field_provenance"][field]["source_url"] for field in REQUIRED_RULE_FIELDS}
    sources.update(source["source_url"] for field in REQUIRED_RULE_FIELDS for source in rec["field_provenance"][field].get("supporting_sources", []))
    return {**result, "state": rec["state"], "tax_rate": rate, "condition": condition,
            "local_rate": number(local_rate, "local_rate", Decimal(1)),
            "as_of": date.isoformat(), "status": "estimate", "tax_rule_evidence": "verified",
            "scope": rec["calculator"]["scope"], "warnings": warnings,
            "local_rate_source": "user_supplied" if rules["local"] != "none" else "not_applicable",
            "fee_source": "user_supplied", "sources": sorted(sources)}


def reverse_state_otd(target_otd, doc, state, title=None, reg=None, addons=0, **kwargs):
    """Return the highest supported sales-price cent within a gross OTD target."""
    rec, date, today, _ = _prepare_state(state, title, reg, kwargs.get("as_of"), kwargs.get("today"), kwargs.get("data_path", DATA_PATH), kwargs.get("transaction", "dealer_purchase"), kwargs.get("vehicle", "passenger_ice"), kwargs.get("local_rate"), kwargs.get("condition"))
    minimum = money(rec["tax_rules"]["minimum_supported_base"], "minimum_supported_base")
    if minimum:
        credit = trade_credit_for_state(state, kwargs.get("trade", 0), as_of=date, today=today, data_path=kwargs.get("data_path", DATA_PATH))
        minimum = max(ZERO, minimum + credit - (money(doc, "doc") if rec["tax_rules"]["doc_taxable"] else ZERO) - money(kwargs.get("taxable_addons", 0), "taxable_addons"))
    calculate = lambda sales: compute_state_otd(sales, doc, state, title, reg, addons, **kwargs)
    rules = rec["tax_rules"]
    warranty = money(kwargs.get("warranty", 0), "warranty")
    if "luxury_threshold" in rules and warranty:
        target = money(target_otd, "target_otd")
        threshold = money(rules["luxury_threshold"], "luxury_threshold")
        charges = money(doc, "doc") + money(kwargs.get("taxable_addons", 0), "taxable_addons")
        upper_floor = max(minimum, threshold + CENT - charges)
        if upper_floor <= target and calculate(upper_floor)["otd"] <= target:
            return _reverse(target, calculate, minimum_sales=upper_floor)
        lower_ceiling = threshold - warranty - charges
        if lower_ceiling < minimum:
            raise ValueError("Target OTD cannot cover a supported price outside the warranty threshold review interval")
        result = _reverse(target, calculate, minimum_sales=minimum, upper_bound=lower_ceiling)
        if result["sales"] == lower_ceiling and result["budget_remaining"]:
            result["warnings"].append("Higher prices in the warranty threshold review interval were not evaluated; obtain an itemized tax review before raising this ceiling.")
        return result
    return _reverse(target_otd, calculate, minimum_sales=minimum)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", help="Gross OTD ceiling before trade settlement")
    parser.add_argument("--sales", "--sale-price", help="Sales price, dollars")
    parser.add_argument("--state", choices=sorted(STATE_TAX_RATES))
    parser.add_argument("--doc", default="0")
    parser.add_argument("--local", help="Verified local percentage (1 means 1%%)")
    parser.add_argument("--title")
    parser.add_argument("--reg")
    parser.add_argument("--addons", default="0", help="Separately identified nontaxable charges")
    parser.add_argument("--taxable-addons", default="0")
    parser.add_argument("--warranty", default="0", help="CT only: separately stated service/extended warranties, taxed at 6.35%%")
    parser.add_argument("--condition", choices=("new", "used"), help="NJ requires explicit used; new NJ vehicle surcharges are not encoded")
    parser.add_argument("--trade", default="0", help="Same-transaction buyer-owned vehicle allowance, not equity")
    parser.add_argument("--trade-payoff", default="0")
    parser.add_argument("--as-of", help="Transaction date YYYY-MM-DD (default today)")
    parser.add_argument("--transaction", default="dealer_purchase")
    parser.add_argument("--vehicle", default="passenger_ice")
    parser.add_argument("--forward", action="store_true")
    parser.add_argument("--list-states", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--estimate", action="store_true", help="Explicit generic algebra; requires --tax-rate and --doc-taxable, no automatic state lookup")
    parser.add_argument("--tax-rate", help="User-supplied combined percentage for generic estimate")
    parser.add_argument("--doc-taxable", choices=("yes", "no"))
    args = parser.parse_args()
    if args.list_states:
        for state, rec in sorted(_state_records().items()):
            print(f"{state}: {rec['calculator']['status']} | {rec['calculator'].get('scope', rec['calculator'].get('reason'))}")
        return 0
    if args.forward and args.target is not None or not args.forward and args.sales is not None:
        parser.error("Use --sales with --forward, or --target for reverse mode")
    value = args.sales if args.forward else args.target
    if value is None:
        parser.error("--sales required with --forward; otherwise --target is required")
    try:
        if args.estimate:
            if args.tax_rate is None or args.doc_taxable is None or args.title is None or args.reg is None:
                raise ValueError("Generic estimate requires --tax-rate, --doc-taxable, --title and --reg")
            if money(args.trade, "trade") or money(args.trade_payoff, "trade_payoff"):
                raise ValueError("Generic estimate does not infer trade-in credits; use a supported state profile or obtain a dealer calculation")
            if args.local is not None or args.as_of is not None:
                raise ValueError("Generic estimate uses only the supplied combined tax rate, with no local/date lookup")
            if args.condition is not None or money(args.warranty, "warranty"):
                raise ValueError("Generic estimate does not interpret condition or separate warranty treatment")
            rate = number(args.tax_rate, "tax_rate percentage", Decimal(100)) / 100
            calculate = lambda sales: _components(sales, args.doc, rate, args.title, args.reg, args.addons, taxable_addons=args.taxable_addons, doc_taxable=args.doc_taxable == "yes")
            result = calculate(value) if args.forward else _reverse(value, calculate)
            result.update(status="unverified_custom_estimate", warnings=["Generic arithmetic only; no state rule or fee has been verified."])
        else:
            if not args.state:
                raise ValueError("--state is required for a state-rule estimate")
            if args.tax_rate is not None or args.doc_taxable is not None:
                raise ValueError("--tax-rate and --doc-taxable require explicit --estimate")
            calculate = compute_state_otd if args.forward else reverse_state_otd
            result = calculate(value, args.doc, args.state, args.title, args.reg, args.addons,
                               taxable_addons=args.taxable_addons, trade=args.trade, trade_payoff=args.trade_payoff,
                               local_rate=None if args.local is None else number(args.local, "local percentage", Decimal(100)) / 100,
                               as_of=args.as_of, transaction=args.transaction, vehicle=args.vehicle,
                               condition=args.condition, warranty=args.warranty)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"OTD ESTIMATE | {result['status']}")
        for key in ("sales", "doc", "taxable_addons", "taxable", "credited_trade", "tax", "title", "reg", "addons", "otd", "trade", "trade_payoff", "balance_due"):
            print(f"{key:>18}: ${result[key]:,.2f}")
        if result.get("warranty"):
            print(f"{'warranty':>18}: ${result['warranty']:,.2f} (tax ${result['warranty_tax']:,.2f}, included above)")
        print("Gross OTD is before trade allowance/payoff settlement; balance_due includes them.")
        for warning in result["warnings"]:
            print("WARNING: " + warning)
    return 0


if __name__ == "__main__":
    sys.exit(main())
