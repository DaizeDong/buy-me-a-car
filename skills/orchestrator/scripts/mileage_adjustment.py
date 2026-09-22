"""Apply an explicitly supplied mileage sensitivity; this is not a valuation model."""
from __future__ import annotations

import argparse
from decimal import Decimal, DecimalException, ROUND_HALF_UP
import sys


def compute_mileage_adjustment(miles_a, miles_b, rate):
    """Return the absolute dollar difference under the supplied per-mile assumption."""
    mileage = []
    for value in (miles_a, miles_b):
        if isinstance(value, bool):
            raise ValueError("Mileage must be a nonnegative whole number")
        number = Decimal(str(value))
        if not number.is_finite() or number < 0 or number > 10000000 or number != number.to_integral_value():
            raise ValueError("Mileage must be a nonnegative whole number")
        mileage.append(number)
    if isinstance(rate, bool):
        raise ValueError("Rate must be finite and nonnegative")
    value = Decimal(str(rate))
    if not value.is_finite() or value < 0 or value > 1000:
        raise ValueError("Rate must be finite and nonnegative")
    return (abs(mileage[1] - mileage[0]) * value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--miles-a", required=True)
    parser.add_argument("--miles-b", required=True)
    parser.add_argument("--rate", required=True, help="Explicit dollars per mile assumption, justified separately")
    args = parser.parse_args(argv)
    try:
        adjustment = compute_mileage_adjustment(args.miles_a, args.miles_b, args.rate)
    except (DecimalException, ValueError) as exc:
        print(f"Invalid sensitivity input: {exc}", file=sys.stderr)
        return 2
    print(f"Assumed absolute mileage adjustment: ${adjustment:,.2f}")
    print("Sensitivity only. No market value, dealer acceptance, or causality is established.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
