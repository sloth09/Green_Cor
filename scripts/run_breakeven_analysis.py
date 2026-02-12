#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Break-even Distance Analysis - Case 1 (Storage) vs Case 2 (Direct Supply).

Finds the break-even distance where storage-based (Case 1) and
direct supply (Case 2) strategies have equal NPC.

Analyses:
  1. Case 1 vs Case 2 (Ulsan): distance 10-200 nm, 20 points
  2. Case 1 vs Case 3 (Yeosu): distance 10-200 nm, 20 points

For each distance point, Case 2 travel_time_hours is recalculated
while Case 1 NPC remains fixed (distance-independent).

Outputs:
  results/sensitivity/breakeven_distance_ulsan.csv
  results/sensitivity/breakeven_distance_yeosu.csv
  results/sensitivity/breakeven_distance_combined.csv

Usage:
    python scripts/run_breakeven_analysis.py
    python scripts/run_breakeven_analysis.py --n-points 30
"""

import sys
import argparse
from pathlib import Path
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import load_config
from src.breakeven_analyzer import BreakevenAnalyzer

# Optimal shuttle sizes per case (from deterministic results)
OPTIMAL_SHUTTLES = {
    'case_1': 1000,
    'case_2': 5000,
    'case_3': 5000,
}

PUMP_SIZE = 500


def main():
    parser = argparse.ArgumentParser(
        description="Run break-even distance analysis for SCI paper"
    )
    parser.add_argument(
        "--n-points", type=int, default=20,
        help="Number of distance points to evaluate (default: 20)"
    )
    parser.add_argument(
        "--min-distance", type=float, default=10,
        help="Minimum distance in nm (default: 10)"
    )
    parser.add_argument(
        "--max-distance", type=float, default=200,
        help="Maximum distance in nm (default: 200)"
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
    print("Break-even Distance Analysis")
    print("=" * 70)
    print(f"Distance range: {args.min_distance} - {args.max_distance} nm")
    print(f"Points: {args.n_points}")
    print(f"Output: {output_dir}")
    print("=" * 70)

    # Load configs
    case1_config = load_config("case_1")
    case2_ulsan_config = load_config("case_2")
    case2_yeosu_config = load_config("case_3")

    all_results = []

    # Analysis 1: Case 1 vs Case 2 (Ulsan)
    print("\n--- Case 1 vs Case 2 (Ulsan) ---")
    analyzer_ulsan = BreakevenAnalyzer(
        shuttle_size=OPTIMAL_SHUTTLES['case_2'],
        pump_size=PUMP_SIZE
    )

    result_ulsan = analyzer_ulsan.find_breakeven_distance(
        case1_config=case1_config,
        case2_config=case2_ulsan_config,
        distance_range=(args.min_distance, args.max_distance),
        n_points=args.n_points,
        verbose=verbose,
    )

    df_ulsan = result_ulsan.to_dataframe()
    df_ulsan['Comparison'] = 'Case1_vs_Ulsan'
    csv_path = output_dir / "breakeven_distance_ulsan.csv"
    df_ulsan.to_csv(csv_path, index=False)
    print(f"  [OK] Saved: {csv_path}")

    if result_ulsan.breakeven_value:
        print(f"  Break-even distance (Ulsan): {result_ulsan.breakeven_value:.1f} nm")
    else:
        print(f"  No break-even found in range")

    # Analysis 2: Case 1 vs Case 3 (Yeosu)
    print("\n--- Case 1 vs Case 3 (Yeosu) ---")
    analyzer_yeosu = BreakevenAnalyzer(
        shuttle_size=OPTIMAL_SHUTTLES['case_3'],
        pump_size=PUMP_SIZE
    )

    result_yeosu = analyzer_yeosu.find_breakeven_distance(
        case1_config=case1_config,
        case2_config=case2_yeosu_config,
        distance_range=(args.min_distance, args.max_distance),
        n_points=args.n_points,
        verbose=verbose,
    )

    df_yeosu = result_yeosu.to_dataframe()
    df_yeosu['Comparison'] = 'Case1_vs_Yeosu'
    csv_path = output_dir / "breakeven_distance_yeosu.csv"
    df_yeosu.to_csv(csv_path, index=False)
    print(f"  [OK] Saved: {csv_path}")

    if result_yeosu.breakeven_value:
        print(f"  Break-even distance (Yeosu): {result_yeosu.breakeven_value:.1f} nm")
    else:
        print(f"  No break-even found in range")

    # Combined CSV
    df_combined = pd.concat([df_ulsan, df_yeosu], ignore_index=True)
    combined_path = output_dir / "breakeven_distance_combined.csv"
    df_combined.to_csv(combined_path, index=False)
    print(f"\n[OK] Combined results: {combined_path}")

    # ---------------------------------------------------------------
    # Optimal-vs-Optimal Analysis (heterogeneous shuttle sizes)
    # Case 1 at its optimal 2500 m3 vs Case 2 at their optimal sizes
    # ---------------------------------------------------------------
    print("\n" + "=" * 70)
    print("Optimal-vs-Optimal Break-even Analysis")
    print("=" * 70)

    # Ulsan optimal-vs-optimal: Case 1 @ 1000 vs Case 2 @ 5000
    print("\n--- Optimal: Case 1 (1000 m3) vs Case 2 Ulsan (5000 m3) ---")
    analyzer_opt_ulsan = BreakevenAnalyzer(pump_size=PUMP_SIZE)
    result_opt_ulsan = analyzer_opt_ulsan.find_breakeven_distance_heterogeneous(
        case1_config=case1_config,
        case2_config=case2_ulsan_config,
        case1_shuttle_size=OPTIMAL_SHUTTLES['case_1'],
        case2_shuttle_size=OPTIMAL_SHUTTLES['case_2'],
        distance_range=(args.min_distance, args.max_distance),
        n_points=args.n_points,
        verbose=verbose,
    )

    df_opt_ulsan = result_opt_ulsan.to_dataframe()
    df_opt_ulsan['Comparison'] = 'Optimal_Case1_vs_Ulsan'
    csv_path = output_dir / "breakeven_distance_optimal_ulsan.csv"
    df_opt_ulsan.to_csv(csv_path, index=False)
    print(f"  [OK] Saved: {csv_path}")

    # Yeosu optimal-vs-optimal: Case 1 @ 1000 vs Case 3 @ 5000
    print("\n--- Optimal: Case 1 (1000 m3) vs Case 3 Yeosu (5000 m3) ---")
    analyzer_opt_yeosu = BreakevenAnalyzer(pump_size=PUMP_SIZE)
    result_opt_yeosu = analyzer_opt_yeosu.find_breakeven_distance_heterogeneous(
        case1_config=case1_config,
        case2_config=case2_yeosu_config,
        case1_shuttle_size=OPTIMAL_SHUTTLES['case_1'],
        case2_shuttle_size=OPTIMAL_SHUTTLES['case_3'],
        distance_range=(args.min_distance, args.max_distance),
        n_points=args.n_points,
        verbose=verbose,
    )

    df_opt_yeosu = result_opt_yeosu.to_dataframe()
    df_opt_yeosu['Comparison'] = 'Optimal_Case1_vs_Yeosu'
    csv_path = output_dir / "breakeven_distance_optimal_yeosu.csv"
    df_opt_yeosu.to_csv(csv_path, index=False)
    print(f"  [OK] Saved: {csv_path}")

    # Optimal combined CSV
    df_opt_combined = pd.concat([df_opt_ulsan, df_opt_yeosu], ignore_index=True)
    opt_combined_path = output_dir / "breakeven_distance_optimal_combined.csv"
    df_opt_combined.to_csv(opt_combined_path, index=False)
    print(f"\n[OK] Optimal combined results: {opt_combined_path}")

    # Summary
    print("\n" + "=" * 70)
    print("Break-even Summary")
    print("=" * 70)
    print("  Same-shuttle comparison:")
    print(f"    Case 1 vs Ulsan (5000 m3): ", end="")
    if result_ulsan.breakeven_value:
        print(f"{result_ulsan.breakeven_value:.1f} nm")
    else:
        print("No crossover")
    print(f"    Case 1 vs Yeosu (10000 m3): ", end="")
    if result_yeosu.breakeven_value:
        print(f"{result_yeosu.breakeven_value:.1f} nm")
    else:
        print("No crossover")
    print("  Optimal-vs-optimal comparison:")
    print(f"    Case 1 (2500 m3) vs Ulsan (5000 m3): ", end="")
    if result_opt_ulsan.breakeven_value:
        print(f"{result_opt_ulsan.breakeven_value:.1f} nm")
    else:
        print("No crossover")
    print(f"    Case 1 (2500 m3) vs Yeosu (10000 m3): ", end="")
    if result_opt_yeosu.breakeven_value:
        print(f"{result_opt_yeosu.breakeven_value:.1f} nm")
    else:
        print("No crossover")
    print("=" * 70)
    print("[OK] Break-even analysis complete!")


if __name__ == "__main__":
    main()
