#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stochastic Analysis Runner - Generate paper-ready results.

This script runs:
1. Stochastic optimization with vessel size heterogeneity
2. Sensitivity analysis (tornado diagrams)
3. Break-even analysis (case comparisons)

Usage:
    python scripts/run_stochastic_analysis.py
    python scripts/run_stochastic_analysis.py --case case_1 --scenarios 100
"""

import sys
from pathlib import Path
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import (
    load_config,
    load_stochastic_config,
    VesselDistribution,
    StochasticOptimizer,
    SensitivityAnalyzer,
    BreakevenAnalyzer,
    run_stochastic_optimization,
    run_sensitivity_analysis,
    run_breakeven_analysis,
)


def run_all_analyses(
    case_id: str = "case_1",
    n_scenarios: int = 100,
    output_dir: str = "results/stochastic",
    verbose: bool = True
):
    """
    Run complete stochastic analysis suite.

    Args:
        case_id: Primary case to analyze
        n_scenarios: Number of Monte Carlo scenarios
        output_dir: Output directory for results
        verbose: Print progress
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("Stochastic Analysis Suite")
    print("="*60)
    print(f"Case: {case_id}")
    print(f"Monte Carlo scenarios: {n_scenarios}")
    print(f"Output directory: {output_dir}")
    print("="*60)

    # Load configurations
    config = load_config(case_id)
    stoch_config = load_stochastic_config()

    # Get optimal shuttle/pump from deterministic run first
    from src.optimizer import BunkeringOptimizer

    print("\n[1/4] Running deterministic optimization to find optimal config...")
    det_optimizer = BunkeringOptimizer(config)
    scenario_df, yearly_df = det_optimizer.solve()

    if scenario_df.empty:
        print("[ERROR] No feasible solutions found in deterministic run")
        return

    # Get optimal configuration
    optimal_row = scenario_df.loc[scenario_df['NPC_Total_USDm'].idxmin()]
    optimal_shuttle = optimal_row['Shuttle_Size_cbm']
    optimal_pump = optimal_row['Pump_Size_m3ph']
    det_npc = optimal_row['NPC_Total_USDm']

    print(f"  Optimal: Shuttle={optimal_shuttle}m3, Pump={optimal_pump}m3/h")
    print(f"  Deterministic NPC: ${det_npc:.2f}M")

    # Save deterministic results
    scenario_df.to_csv(output_path / f"deterministic_scenarios_{case_id}.csv", index=False)
    yearly_df.to_csv(output_path / f"deterministic_yearly_{case_id}.csv", index=False)

    # 2. Stochastic Optimization
    print("\n[2/4] Running stochastic optimization...")
    stoch_result = run_stochastic_optimization(
        case_id=case_id,
        n_scenarios=n_scenarios,
        output_dir=str(output_path),
        verbose=verbose
    )

    # 3. Sensitivity Analysis
    print("\n[3/4] Running sensitivity analysis...")
    sens_analyzer = SensitivityAnalyzer(
        config,
        shuttle_size=optimal_shuttle,
        pump_size=optimal_pump
    )

    # Define parameters for tornado
    tornado_params = [
        {"path": "economy.fuel_price_usd_per_ton", "name": "Fuel Price"},
        {"path": "operations.max_annual_hours_per_vessel", "name": "Max Annual Hours"},
        {"path": "operations.travel_time_hours", "name": "Travel Time"},
        {"path": "bunkering.bunker_volume_per_call_m3", "name": "Bunker Volume"},
    ]

    tornado_result = sens_analyzer.analyze_tornado(tornado_params, variation_pct=0.10, verbose=verbose)
    tornado_result.to_dataframe().to_csv(output_path / f"tornado_{case_id}.csv", index=False)

    # Single parameter sensitivity for fuel price
    fuel_sens = sens_analyzer.analyze_parameter(
        "economy.fuel_price_usd_per_ton",
        variations=[-0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30],
        param_name="Fuel Price",
        verbose=verbose
    )
    fuel_sens.to_dataframe().to_csv(output_path / f"sensitivity_fuel_price_{case_id}.csv", index=False)

    # 4. Break-even Analysis (if we have multiple cases)
    print("\n[4/4] Running break-even analysis...")
    try:
        be_analyzer = BreakevenAnalyzer(
            shuttle_size=optimal_shuttle,
            pump_size=optimal_pump
        )

        # Compare all cases
        comparison = be_analyzer.compare_all_cases(
            case_ids=["case_1", "case_2", "case_3"],
            shuttle_sizes=[optimal_shuttle],
            pump_sizes=[optimal_pump],
            verbose=verbose
        )

        comparison.get_optimal_comparison_df().to_csv(
            output_path / "case_comparison.csv", index=False
        )
    except Exception as e:
        print(f"  [WARN] Break-even analysis skipped: {e}")

    # Generate summary report
    print("\n" + "="*60)
    print("Analysis Summary")
    print("="*60)
    print(f"\nDeterministic Optimization:")
    print(f"  Optimal Shuttle: {optimal_shuttle} m3")
    print(f"  Optimal Pump: {optimal_pump} m3/h")
    print(f"  NPC (20-year): ${det_npc:.2f}M")

    print(f"\nStochastic Optimization:")
    print(f"  Expected NPC: ${stoch_result.expected_npc:.2f}M")
    print(f"  NPC Std Dev: ${stoch_result.npc_std:.2f}M")
    print(f"  VSS: ${stoch_result.vss:.2f}M ({stoch_result.vss_percent:.1f}%)")
    print(f"  EVPI: ${stoch_result.evpi:.2f}M ({stoch_result.evpi_percent:.1f}%)")

    print(f"\nSensitivity (Tornado) - Top impacts:")
    for i, (param, swing) in enumerate(zip(tornado_result.parameters[:3], tornado_result.swings[:3]), 1):
        pct = swing / tornado_result.base_npc * 100 if tornado_result.base_npc else 0
        print(f"  {i}. {param}: ${swing:.2f}M ({pct:.1f}%)")

    print(f"\n[OK] All results saved to {output_path}")
    print("="*60)

    return {
        "deterministic_npc": det_npc,
        "stochastic_result": stoch_result,
        "tornado_result": tornado_result,
        "optimal_shuttle": optimal_shuttle,
        "optimal_pump": optimal_pump,
    }


def main():
    parser = argparse.ArgumentParser(description="Run stochastic analysis suite")
    parser.add_argument("--case", default="case_1", help="Case ID to analyze")
    parser.add_argument("--scenarios", type=int, default=100, help="Monte Carlo scenarios")
    parser.add_argument("--output", default="results/stochastic", help="Output directory")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    args = parser.parse_args()

    run_all_analyses(
        case_id=args.case,
        n_scenarios=args.scenarios,
        output_dir=args.output,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
