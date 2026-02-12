#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discount Rate Sensitivity Analysis - Impact of discounting on optimal infrastructure.

Addresses paper reviewer criticism (Section 3.3) by demonstrating that
optimal shuttle specifications are invariant across discount rates.

Runs optimization with discount_rate = [0%, 5%, 8%] for all 3 cases:
  - case_1:        Busan port storage
  - case_2:  Ulsan direct supply
  - case_3:  Yeosu direct supply

Outputs:
  results/discount_rate_analysis/data/discount_rate_comparison.csv
  results/discount_rate_analysis/data/discount_rate_yearly_{case_id}.csv
  results/discount_rate_analysis/figures/Fig11_discount_rate_sensitivity.png
  results/discount_rate_analysis/figures/Fig12_discount_rate_fleet.png

Usage:
    python scripts/run_discount_rate_analysis.py
    python scripts/run_discount_rate_analysis.py --cases case_1 case_2
    python scripts/run_discount_rate_analysis.py --rates 0.0 0.03 0.05 0.08 0.10
"""

import sys
import argparse
from pathlib import Path
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config_loader import load_config
from src.optimizer import BunkeringOptimizer

ALL_CASES = ['case_1', 'case_2', 'case_3']
DEFAULT_RATES = [0.0, 0.05, 0.08]

CASE_LABELS = {
    'case_1': 'Case 1: Busan Storage',
    'case_2': 'Case 2: Ulsan Direct',
    'case_3': 'Case 3: Yeosu Direct',
}

CASE_SHORT = {
    'case_1': 'Case 1',
    'case_2': 'Case 2',
    'case_3': 'Case 3',
}


def run_single(case_id, discount_rate, verbose=True):
    """Run optimization for a single case/rate combination."""
    config = load_config(case_id)
    config["economy"]["discount_rate"] = discount_rate

    if verbose:
        print(f"  r={discount_rate:.0%}: ", end="", flush=True)

    optimizer = BunkeringOptimizer(config)
    scenario_df, yearly_df = optimizer.solve()

    if scenario_df.empty:
        if verbose:
            print("[WARN] No feasible solution")
        return None, None

    # Find optimal configuration
    best_idx = scenario_df['NPC_Total_USDm'].idxmin()
    best = scenario_df.loc[best_idx]

    result = {
        'Case': case_id,
        'Case_Label': CASE_SHORT.get(case_id, case_id),
        'Discount_Rate': discount_rate,
        'Discount_Rate_Pct': f"{discount_rate:.0%}",
        'Optimal_Shuttle_cbm': int(best['Shuttle_Size_cbm']),
        'Optimal_Pump_m3ph': int(best['Pump_Size_m3ph']),
        'NPC_Total_USDm': best['NPC_Total_USDm'],
        'LCO_USD_per_ton': best.get('LCOAmmonia_USD_per_ton', 0),
    }

    # Add cost breakdown
    for col in ['NPC_Annualized_Shuttle_CAPEX_USDm', 'NPC_Annualized_Bunkering_CAPEX_USDm',
                'NPC_Shuttle_fOPEX_USDm', 'NPC_Bunkering_fOPEX_USDm',
                'NPC_Shuttle_vOPEX_USDm', 'NPC_Bunkering_vOPEX_USDm',
                'Annualized_Cost_USDm_per_year']:
        if col in best.index:
            result[col] = best[col]

    if verbose:
        print(f"NPC=${result['NPC_Total_USDm']:.2f}M, "
              f"Shuttle={result['Optimal_Shuttle_cbm']}m3, "
              f"LCO=${result['LCO_USD_per_ton']:.2f}/ton")

    # Filter yearly data for optimal configuration
    opt_shuttle = int(best['Shuttle_Size_cbm'])
    opt_pump = int(best['Pump_Size_m3ph'])
    yearly_opt = yearly_df[
        (yearly_df['Shuttle_Size_cbm'] == opt_shuttle) &
        (yearly_df['Pump_Size_m3ph'] == opt_pump)
    ].copy()
    yearly_opt['Discount_Rate'] = discount_rate

    return result, yearly_opt


def generate_figures(output_dir, verbose=True):
    """Generate Fig11 and Fig12 using src/paper_figures.py (single source of truth)."""
    fig_dir = Path(output_dir) / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    if verbose:
        print("\n  Generating figures via src/paper_figures.py...")

    from src.paper_figures import PaperFigureGenerator
    generator = PaperFigureGenerator("results")
    generator.fig_11_discount_rate_sensitivity(fig_dir)
    generator.fig_12_discount_rate_fleet(fig_dir)


def print_findings(comparison_df):
    """Print key findings from the analysis."""
    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)

    cases = comparison_df['Case'].unique()

    # Check specification invariance
    print("\n1. OPTIMAL SHUTTLE SPECIFICATION INVARIANCE:")
    all_invariant = True
    for case_id in cases:
        cdf = comparison_df[comparison_df['Case'] == case_id]
        shuttles = cdf['Optimal_Shuttle_cbm'].unique()
        pumps = cdf['Optimal_Pump_m3ph'].unique()
        label = CASE_SHORT.get(case_id, case_id)

        if len(shuttles) == 1 and len(pumps) == 1:
            print(f"   {label}: INVARIANT - {shuttles[0]} m3 shuttle, {pumps[0]} m3/h pump")
        else:
            all_invariant = False
            print(f"   {label}: VARIES - Shuttles: {list(shuttles)}, Pumps: {list(pumps)}")

    if all_invariant:
        print("   => Optimal specifications are INVARIANT across all discount rates")
    else:
        print("   => Some specifications vary with discount rate")

    # NPC ranges
    print("\n2. NPC SENSITIVITY TO DISCOUNT RATE:")
    for case_id in cases:
        cdf = comparison_df[comparison_df['Case'] == case_id].sort_values('Discount_Rate')
        label = CASE_SHORT.get(case_id, case_id)
        npc_0 = cdf[cdf['Discount_Rate'] == 0.0]['NPC_Total_USDm'].values
        npc_max = cdf['NPC_Total_USDm'].max()
        npc_min = cdf['NPC_Total_USDm'].min()

        base_val = npc_0[0] if len(npc_0) > 0 else npc_max
        pct_change = ((npc_min - base_val) / base_val) * 100 if base_val > 0 else 0

        print(f"   {label}: ${npc_min:.2f}M - ${npc_max:.2f}M "
              f"({pct_change:+.1f}% from r=0%)")

    # LCO ranges
    print("\n3. LCO SENSITIVITY TO DISCOUNT RATE:")
    for case_id in cases:
        cdf = comparison_df[comparison_df['Case'] == case_id].sort_values('Discount_Rate')
        label = CASE_SHORT.get(case_id, case_id)
        lco_vals = cdf['LCO_USD_per_ton'].values
        print(f"   {label}: ${min(lco_vals):.2f} - ${max(lco_vals):.2f}/ton")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Discount rate sensitivity analysis for SCI paper"
    )
    parser.add_argument(
        "--cases", nargs="+", default=ALL_CASES,
        help="Cases to analyze (default: all 3)"
    )
    parser.add_argument(
        "--rates", nargs="+", type=float, default=DEFAULT_RATES,
        help="Discount rates to test (default: 0.0 0.05 0.08)"
    )
    parser.add_argument(
        "--output", default="results/discount_rate_analysis",
        help="Output directory (default: results/discount_rate_analysis)"
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress detailed output"
    )
    parser.add_argument(
        "--no-figures", action="store_true",
        help="Skip figure generation"
    )

    args = parser.parse_args()
    verbose = not args.quiet

    output_dir = Path(args.output)
    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("Discount Rate Sensitivity Analysis")
    print("=" * 70)
    print(f"Cases: {args.cases}")
    print(f"Discount rates: {[f'{r:.0%}' for r in args.rates]}")
    print(f"Output: {output_dir}")
    print("=" * 70)

    all_results = []
    yearly_data = {}  # {case_id: {rate: DataFrame}}

    for case_id in args.cases:
        print(f"\n--- {CASE_LABELS.get(case_id, case_id)} ---")
        yearly_data[case_id] = {}

        case_yearly_frames = []

        for rate in args.rates:
            result, yearly_opt = run_single(case_id, rate, verbose)
            if result:
                all_results.append(result)

            if yearly_opt is not None and not yearly_opt.empty:
                yearly_data[case_id][rate] = yearly_opt
                case_yearly_frames.append(yearly_opt)

        # Save per-case yearly CSV
        if case_yearly_frames:
            yearly_combined = pd.concat(case_yearly_frames, ignore_index=True)
            yearly_path = data_dir / f"discount_rate_yearly_{case_id}.csv"
            yearly_combined.to_csv(yearly_path, index=False)
            if verbose:
                print(f"  [OK] Saved: {yearly_path}")

    # Save comparison summary
    if all_results:
        comparison_df = pd.DataFrame(all_results)
        comparison_path = data_dir / "discount_rate_comparison.csv"
        comparison_df.to_csv(comparison_path, index=False)
        print(f"\n[OK] Comparison saved: {comparison_path}")

        # Print key findings
        print_findings(comparison_df)

        # Generate figures (reads CSVs just saved above via paper_figures.py)
        if not args.no_figures:
            generate_figures(output_dir, verbose)
    else:
        print("\n[WARN] No results to save")

    print("\n" + "=" * 70)
    print("[OK] Discount rate analysis complete!")
    print(f"Results saved to: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
