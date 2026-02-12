#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demand Scenario Analysis - Impact of fleet growth rate on optimal infrastructure.

Runs 4 demand scenarios for all 3 cases:
  - Low:       50 -> 250 vessels (conservative decarbonization)
  - Base:      50 -> 500 vessels (current assumption)
  - High:      50 -> 750 vessels (aggressive adoption)
  - VeryHigh:  50 -> 1000 vessels (maximum scenario)

Each scenario runs full optimization to find optimal shuttle/pump configuration.

Outputs:
  results/sensitivity/demand_scenarios_{case_id}.csv
  results/sensitivity/demand_scenarios_summary.csv

Usage:
    python scripts/run_demand_scenarios.py
    python scripts/run_demand_scenarios.py --cases case_1 case_2
"""

import sys
import copy
import argparse
from pathlib import Path
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import load_config
from src.optimizer import BunkeringOptimizer

ALL_CASES = ['case_1', 'case_2', 'case_3']

DEMAND_SCENARIOS = {
    'Low': {'start_vessels': 50, 'end_vessels': 250},
    'Base': {'start_vessels': 50, 'end_vessels': 500},
    'High': {'start_vessels': 50, 'end_vessels': 750},
    'VeryHigh': {'start_vessels': 50, 'end_vessels': 1000},
}


def run_demand_scenario(case_id, scenario_name, scenario_params, verbose=True):
    """Run a single demand scenario and return optimal result."""
    config = load_config(case_id)

    # Modify demand parameters
    config["shipping"]["start_vessels"] = scenario_params["start_vessels"]
    config["shipping"]["end_vessels"] = scenario_params["end_vessels"]

    if verbose:
        print(f"  {scenario_name}: {scenario_params['start_vessels']} -> "
              f"{scenario_params['end_vessels']} vessels")

    # Run full optimization
    optimizer = BunkeringOptimizer(config)
    scenario_df, yearly_df = optimizer.solve()

    if scenario_df.empty:
        if verbose:
            print(f"    [WARN] No feasible solution")
        return None

    # Find optimal configuration
    best_idx = scenario_df['NPC_Total_USDm'].idxmin()
    best = scenario_df.loc[best_idx]

    result = {
        'Case': case_id,
        'Scenario': scenario_name,
        'Start_Vessels': scenario_params['start_vessels'],
        'End_Vessels': scenario_params['end_vessels'],
        'Optimal_Shuttle_cbm': int(best['Shuttle_Size_cbm']),
        'Optimal_Pump_m3ph': int(best['Pump_Size_m3ph']),
        'NPC_Total_USDm': best['NPC_Total_USDm'],
        'LCO_USD_per_ton': best.get('LCOAmmonia_USD_per_ton', 0),
    }

    # Add cost breakdown if available
    for col in ['NPC_Annualized_Shuttle_CAPEX_USDm', 'NPC_Annualized_Bunkering_CAPEX_USDm',
                'NPC_Shuttle_fOPEX_USDm', 'NPC_Bunkering_fOPEX_USDm',
                'NPC_Shuttle_vOPEX_USDm', 'NPC_Bunkering_vOPEX_USDm']:
        if col in best.index:
            result[col] = best[col]

    if verbose:
        print(f"    [OK] NPC=${result['NPC_Total_USDm']:.2f}M, "
              f"Shuttle={result['Optimal_Shuttle_cbm']}m3, "
              f"LCO=${result['LCO_USD_per_ton']:.2f}/ton")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run demand scenario analysis for SCI paper"
    )
    parser.add_argument(
        "--cases", nargs="+", default=ALL_CASES,
        help="Cases to analyze (default: all 3)"
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
    print("Demand Scenario Analysis")
    print("=" * 70)
    print(f"Cases: {args.cases}")
    print(f"Scenarios: {list(DEMAND_SCENARIOS.keys())}")
    print(f"Output: {output_dir}")
    print("=" * 70)

    all_results = []

    for case_id in args.cases:
        print(f"\n--- {case_id} ---")

        case_results = []
        for scenario_name, scenario_params in DEMAND_SCENARIOS.items():
            result = run_demand_scenario(case_id, scenario_name, scenario_params, verbose)
            if result:
                case_results.append(result)
                all_results.append(result)

        # Save per-case CSV
        if case_results:
            df = pd.DataFrame(case_results)
            csv_path = output_dir / f"demand_scenarios_{case_id}.csv"
            df.to_csv(csv_path, index=False)
            if verbose:
                print(f"  [OK] Saved: {csv_path}")

    # Save summary CSV (all cases combined)
    if all_results:
        df_all = pd.DataFrame(all_results)
        summary_path = output_dir / "demand_scenarios_summary.csv"
        df_all.to_csv(summary_path, index=False)
        print(f"\n[OK] Summary saved: {summary_path}")

    print("\n" + "=" * 70)
    print("[OK] Demand scenario analysis complete!")
    print(f"Results saved to: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
