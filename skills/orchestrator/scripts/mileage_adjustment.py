#!/usr/bin/env python3
"""
Mileage Adjustment Calculator — compute fair price adjustment between two used vehicles
based on mileage delta.

Usage:
  python mileage_adjustment.py --miles-a 50000 --miles-b 73000 --segment suv
  python mileage_adjustment.py --miles-a 50000 --miles-b 73000 --rate 0.12
"""
import argparse

SEGMENT_RATES = {
    "sedan-compact": (0.07, 0.10),       # Civic, Corolla
    "sedan-midsize": (0.08, 0.11),       # Accord, Camry
    "suv": (0.10, 0.15),                  # Forester, Outback, CR-V, RAV4
    "suv-midsize": (0.10, 0.15),
    "suv-luxury": (0.15, 0.25),           # MDX, X5, GLE
    "truck": (0.10, 0.15),                # Tacoma, F-150
    "performance": (0.15, 0.25),          # WRX, Camaro
    "luxury": (0.15, 0.25),               # 3-series, Lexus
}


def compute_mileage_adjustment(miles_a, miles_b, rate):
    """Compute dollar adjustment for higher-mileage vehicle (b > a)."""
    delta_miles = abs(miles_b - miles_a)
    delta_dollars = delta_miles * rate
    return delta_dollars


def main():
    p = argparse.ArgumentParser(description="Mileage adjustment between two vehicles")
    p.add_argument("--miles-a", type=int, required=True, help="Lower-mileage comp")
    p.add_argument("--miles-b", type=int, required=True, help="Higher-mileage target")
    p.add_argument("--segment", choices=SEGMENT_RATES.keys(), help="Vehicle segment")
    p.add_argument("--rate", type=float, help="Custom $/mile rate (overrides segment)")
    args = p.parse_args()

    if args.rate:
        rate_low = args.rate
        rate_high = args.rate
    elif args.segment:
        rate_low, rate_high = SEGMENT_RATES[args.segment]
    else:
        # Default to SUV rates
        rate_low, rate_high = SEGMENT_RATES["suv"]
        print("(No segment specified, using SUV default)")

    delta_miles = abs(args.miles_b - args.miles_a)
    adj_low = delta_miles * rate_low
    adj_high = delta_miles * rate_high

    print(f"Mileage A: {args.miles_a:,} mi")
    print(f"Mileage B: {args.miles_b:,} mi")
    print(f"Delta:     {delta_miles:,} mi")
    print(f"Rate:      ${rate_low:.2f} - ${rate_high:.2f} per mile")
    print(f"Adjustment: ${adj_low:,.0f} - ${adj_high:,.0f}")
    print()

    if args.miles_b > args.miles_a:
        print(f"=> Higher-mileage car (B) should be ${adj_low:,.0f}-{adj_high:,.0f} CHEAPER than A")
    else:
        print(f"=> Higher-mileage car (A) should be ${adj_low:,.0f}-{adj_high:,.0f} CHEAPER than B")


if __name__ == "__main__":
    main()
