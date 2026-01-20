#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate pump rate sensitivity data for S7 figure.

This script runs optimization for each pump rate (400-2000 m3/h) and finds
the optimal shuttle size at each point. Results are saved to CSV files
for use by the paper figure generator.

Usage:
    python scripts/run_pump_sensitivity.py

Output:
    results/sensitivity/pump_sensitivity_{case_id}.csv
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sensitivity_analyzer import analyze_pump_rate_sensitivity


def main():
    """Run pump rate sensitivity analysis for all cases."""
    print("\n" + "=" * 70)
    print("Pump Rate Sensitivity Analysis")
    print("=" * 70)
    print("This generates data for S7 figure in the paper.")
    print("Output: results/sensitivity/pump_sensitivity_*.csv")
    print("=" * 70)

    # Output directory
    output_dir = project_root / "results" / "sensitivity"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run for all three cases
    cases = ["case_1", "case_2_yeosu", "case_2_ulsan"]
    all_results = {}

    for case_id in cases:
        print(f"\n{'='*70}")
        print(f"Processing: {case_id}")
        print("=" * 70)

        try:
            df = analyze_pump_rate_sensitivity(
                case_id=case_id,
                output_dir=str(output_dir),
                verbose=True
            )
            all_results[case_id] = df
        except Exception as e:
            print(f"[ERROR] Failed to process {case_id}: {e}")
            continue

    # Summary
    print("\n" + "=" * 70)
    print("Summary - Pump Rate Sensitivity Analysis Complete")
    print("=" * 70)

    for case_id, df in all_results.items():
        if not df.empty:
            best_idx = df['Min_NPC_USDm'].idxmin()
            best = df.loc[best_idx]
            print(f"\n{case_id}:")
            print(f"  Best Pump Rate: {int(best['Pump_Rate_m3ph'])} m3/h")
            print(f"  Min NPC: ${best['Min_NPC_USDm']:.2f}M")
            print(f"  Optimal Shuttle: {int(best['Optimal_Shuttle_cbm'])} m3")

    print("\n" + "=" * 70)
    print(f"[OK] Results saved to: {output_dir}")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Run: python scripts/generate_paper_figures.py")
    print("  2. Check: results/paper_figures/S7_pump_sensitivity.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
