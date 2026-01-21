#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Paper Figures - SCI-level publication figures.

This script generates all figures needed for the Green Corridor paper:
  - D1-D7: Deterministic optimization results
  - S1-S6: Stochastic optimization results
  - C1-C4: Combined analysis figures

Usage:
    python scripts/generate_paper_figures.py
    python scripts/generate_paper_figures.py --output results/paper_figures
    python scripts/generate_paper_figures.py --figures D1 D2 S1  # specific figures only
"""

import sys
from pathlib import Path
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.paper_figures import PaperFigureGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate paper-quality figures for Green Corridor analysis"
    )
    parser.add_argument(
        "--results", "-r",
        default="results",
        help="Directory containing result CSV files (default: results)"
    )
    parser.add_argument(
        "--output", "-o",
        default="results/paper_figures",
        help="Output directory for figures (default: results/paper_figures)"
    )
    parser.add_argument(
        "--figures", "-f",
        nargs="+",
        help="Specific figures to generate (e.g., D1 D2 S1). If not specified, all figures are generated."
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("Green Corridor Paper Figure Generator")
    print("=" * 60)
    print(f"Results directory: {args.results}")
    print(f"Output directory: {args.output}")
    print("=" * 60)

    # Initialize generator
    generator = PaperFigureGenerator(args.results)

    # Create output directory
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    if args.figures:
        # Generate specific figures
        print(f"\nGenerating specific figures: {args.figures}")

        figure_map = {
            'D1': generator.fig_d1_npc_vs_shuttle,
            'D2': generator.fig_d2_yearly_cost_evolution,
            'D3': generator.fig_d3_yearly_fleet_demand,
            'D4': generator.fig_d4_yearly_cycles,
            'D5': generator.fig_d5_yearly_utilization,
            'D6': generator.fig_d6_cost_breakdown,
            'D7': generator.fig_d7_cycle_time,
            'D8': generator.fig_d8_fleet_evolution,
            'D9': generator.fig_d9_lco_comparison,
            'D10': generator.fig_d10_case_npc_comparison,
            'D11': generator.fig_d11_top_configurations,
            'D12': generator.fig_d12_npc_heatmap,
            'S1': generator.fig_s1_npc_boxplot,
            'S2': generator.fig_s2_vss_evpi,
            'S3': generator.fig_s3_mc_distribution,
            'S4': generator.fig_s4_vessel_distribution,
            'S5': generator.fig_s5_tornado,
            'S6': generator.fig_s6_twoway_sensitivity,
            'C1': generator.fig_c1_det_vs_stoch,
            'C2': generator.fig_c2_breakeven_distance,
            'C3': generator.fig_c3_breakeven_demand,
            'C4': generator.fig_c4_summary_dashboard,
        }

        for fig_id in args.figures:
            fig_id_upper = fig_id.upper()
            if fig_id_upper in figure_map:
                try:
                    figure_map[fig_id_upper](output_path)
                except Exception as e:
                    print(f"  [ERROR] {fig_id_upper}: {e}")
            else:
                print(f"  [WARN] Unknown figure ID: {fig_id}")
                print(f"         Available: {list(figure_map.keys())}")
    else:
        # Generate all figures
        generator.generate_all(args.output)

    print("\n[OK] Done!")


if __name__ == "__main__":
    main()
