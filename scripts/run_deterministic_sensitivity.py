#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Sensitivity Analysis - Fuel price, tornado, bunker volume, two-way.

Runs systematic parameter sensitivity analysis for all 3 cases:
  A. Fuel price sensitivity ($300-$1200/ton, 9 points)
  B. Tornado diagram (6 parameters, +/-20%)
  C. Bunker volume sensitivity (2500-10000 m3, 7 points)
  D. Two-way sensitivity: fuel price x bunker volume (Case 1 only, 5x5)

Outputs:
  results/sensitivity/fuel_price_{case_id}.csv
  results/sensitivity/tornado_det_{case_id}.csv
  results/sensitivity/bunker_volume_{case_id}.csv
  results/sensitivity/two_way_det_{case_id}.csv

Usage:
    python scripts/run_deterministic_sensitivity.py
    python scripts/run_deterministic_sensitivity.py --analyses fuel tornado
    python scripts/run_deterministic_sensitivity.py --cases case_1 case_2
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import load_config
from src.sensitivity_analyzer import SensitivityAnalyzer

# Optimal shuttle sizes per case (from deterministic results)
OPTIMAL_SHUTTLES = {
    'case_1': 1000,
    'case_2': 5000,
    'case_3': 5000,
}

ALL_CASES = ['case_1', 'case_2', 'case_3']
PUMP_SIZE = 500  # Fixed pump rate for all analyses


def run_fuel_price_sensitivity(case_ids, output_dir, verbose=True):
    """A. Fuel price sensitivity: $300 - $1200/ton."""
    print("\n" + "=" * 70)
    print("[A] Fuel Price Sensitivity Analysis")
    print("=" * 70)

    fuel_prices = [300, 400, 500, 600, 700, 800, 900, 1000, 1200]

    for case_id in case_ids:
        config = load_config(case_id)
        shuttle = OPTIMAL_SHUTTLES.get(case_id, config["shuttle"]["available_sizes_cbm"][0])

        analyzer = SensitivityAnalyzer(config, shuttle_size=shuttle, pump_size=PUMP_SIZE)

        result = analyzer.analyze_parameter(
            param_path="economy.fuel_price_usd_per_ton",
            variations=fuel_prices,
            param_name="Fuel_Price_USD_per_ton",
            variation_type="absolute",
            verbose=verbose,
        )

        # Save CSV
        df = result.to_dataframe()
        csv_path = output_dir / f"fuel_price_{case_id}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  [OK] Saved: {csv_path}")


def run_tornado_analysis(case_ids, output_dir, verbose=True):
    """B. Tornado diagram: 6 parameters +/-20%."""
    print("\n" + "=" * 70)
    print("[B] Tornado Diagram Analysis (+/-20%)")
    print("=" * 70)

    tornado_params = [
        {"path": "economy.fuel_price_usd_per_ton", "name": "Fuel Price"},
        {"path": "operations.max_annual_hours_per_vessel", "name": "Max Annual Hours"},
        {"path": "operations.travel_time_hours", "name": "Travel Time"},
        {"path": "bunkering.bunker_volume_per_call_m3", "name": "Bunker Volume"},
        {"path": "propulsion.sfoc_g_per_kwh", "name": "SFOC"},
        {"path": "shuttle.capex_scaling_exponent", "name": "CAPEX Scaling"},
    ]

    for case_id in case_ids:
        config = load_config(case_id)
        shuttle = OPTIMAL_SHUTTLES.get(case_id, config["shuttle"]["available_sizes_cbm"][0])

        analyzer = SensitivityAnalyzer(config, shuttle_size=shuttle, pump_size=PUMP_SIZE)

        result = analyzer.analyze_tornado(
            params=tornado_params,
            variation_pct=0.20,
            verbose=verbose,
        )

        # Save CSV
        df = result.to_dataframe()
        csv_path = output_dir / f"tornado_det_{case_id}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  [OK] Saved: {csv_path}")


def run_bunker_volume_sensitivity(case_ids, output_dir, verbose=True):
    """C. Bunker volume sensitivity: 2500 - 10000 m3."""
    print("\n" + "=" * 70)
    print("[C] Bunker Volume Sensitivity Analysis")
    print("=" * 70)

    volumes = [2500, 3500, 5000, 6000, 7000, 8000, 10000]

    for case_id in case_ids:
        config = load_config(case_id)
        shuttle = OPTIMAL_SHUTTLES.get(case_id, config["shuttle"]["available_sizes_cbm"][0])

        analyzer = SensitivityAnalyzer(config, shuttle_size=shuttle, pump_size=PUMP_SIZE)

        result = analyzer.analyze_parameter(
            param_path="bunkering.bunker_volume_per_call_m3",
            variations=volumes,
            param_name="Bunker_Volume_m3",
            variation_type="absolute",
            verbose=verbose,
        )

        # Save CSV
        df = result.to_dataframe()
        csv_path = output_dir / f"bunker_volume_{case_id}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  [OK] Saved: {csv_path}")


def run_two_way_sensitivity(case_ids, output_dir, verbose=True):
    """D. Two-way sensitivity: fuel price x bunker volume (Case 1 only by default)."""
    print("\n" + "=" * 70)
    print("[D] Two-Way Sensitivity Analysis (Fuel Price x Bunker Volume)")
    print("=" * 70)

    for case_id in case_ids:
        config = load_config(case_id)
        shuttle = OPTIMAL_SHUTTLES.get(case_id, config["shuttle"]["available_sizes_cbm"][0])

        analyzer = SensitivityAnalyzer(config, shuttle_size=shuttle, pump_size=PUMP_SIZE)

        result = analyzer.analyze_two_way(
            param1_path="economy.fuel_price_usd_per_ton",
            param2_path="bunkering.bunker_volume_per_call_m3",
            variations1=[-0.30, -0.15, 0, 0.15, 0.30],
            variations2=[-0.30, -0.15, 0, 0.15, 0.30],
            param1_name="Fuel_Price",
            param2_name="Bunker_Volume",
            verbose=verbose,
        )

        # Save CSV
        df = result.to_dataframe()
        csv_path = output_dir / f"two_way_det_{case_id}.csv"
        df.to_csv(csv_path)
        print(f"  [OK] Saved: {csv_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Run deterministic sensitivity analyses for SCI paper"
    )
    parser.add_argument(
        "--cases", nargs="+", default=ALL_CASES,
        help="Cases to analyze (default: all 3)"
    )
    parser.add_argument(
        "--analyses", nargs="+",
        default=["fuel", "tornado", "bunker", "twoway"],
        choices=["fuel", "tornado", "bunker", "twoway"],
        help="Which analyses to run (default: all)"
    )
    parser.add_argument(
        "--output", default="results/sensitivity",
        help="Output directory (default: results/sensitivity)"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress detailed output"
    )

    args = parser.parse_args()
    verbose = not args.quiet

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("Deterministic Sensitivity Analysis Suite")
    print("=" * 70)
    print(f"Cases: {args.cases}")
    print(f"Analyses: {args.analyses}")
    print(f"Output: {output_dir}")
    print("=" * 70)

    if "fuel" in args.analyses:
        run_fuel_price_sensitivity(args.cases, output_dir, verbose)

    if "tornado" in args.analyses:
        run_tornado_analysis(args.cases, output_dir, verbose)

    if "bunker" in args.analyses:
        run_bunker_volume_sensitivity(args.cases, output_dir, verbose)

    if "twoway" in args.analyses:
        # Two-way only for case_1 by default (expensive: 25 optimizations per case)
        twoway_cases = [c for c in args.cases if c == "case_1"]
        if not twoway_cases:
            twoway_cases = args.cases[:1]
        run_two_way_sensitivity(twoway_cases, output_dir, verbose)

    print("\n" + "=" * 70)
    print("[OK] All sensitivity analyses complete!")
    print(f"Results saved to: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
