#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shuttle Size Comparison Analysis Script.

Generates detailed shuttle size comparison table for any case.

Usage:
    python scripts/analyze_shuttle_comparison.py --case case_2_yeosu --pump 2000
    python scripts/analyze_shuttle_comparison.py --case case_1 --pump 1000
    python scripts/analyze_shuttle_comparison.py --case case_2_ulsan --year 2040
"""

import pandas as pd
import argparse
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def analyze_shuttle_comparison(case_id: str, pump_rate: int = 2000, year: int = 2050):
    """Generate shuttle size comparison table."""

    results_dir = Path("results/deterministic")

    # Load data
    yearly_path = results_dir / f"yearly_{case_id}.csv"
    scenario_path = results_dir / f"scenarios_{case_id}.csv"

    if not yearly_path.exists():
        print(f"[ERROR] File not found: {yearly_path}")
        return

    df_yearly = pd.read_csv(yearly_path)
    df_scenario = pd.read_csv(scenario_path)

    # Filter for year and pump rate
    df_year = df_yearly[(df_yearly['Year'] == year) & (df_yearly['Pump_Size_m3ph'] == pump_rate)].copy()
    df_year = df_year.sort_values('Shuttle_Size_cbm')

    if df_year.empty:
        print(f"[ERROR] No data for Year={year}, Pump={pump_rate}")
        return

    # Get scenario data for costs
    scenario_pump = df_scenario[df_scenario['Pump_Size_m3ph'] == pump_rate].set_index('Shuttle_Size_cbm')

    # Find optimal
    optimal_shuttle = scenario_pump['NPC_Total_USDm'].idxmin()

    # Print header
    print(f"\n{'='*100}")
    print(f"Shuttle Size Comparison: {case_id}")
    print(f"Year: {year} | Pump Rate: {pump_rate} m3/h")
    print(f"{'='*100}\n")

    # Print table header
    print(f"| {'Shuttle':>8} | {'Shuttles':>8} | {'Vessels':>7} | {'Annual':>7} | {'Annual':>7} | {'Total Supply':>14} | {'CAPEX':>8} | {'Fixed':>8} | {'Variable':>8} | {'Total':>8} | {'LCO':>7} | {'Opt':>3} |")
    print(f"| {'(m3)':>8} | {'('+str(year)+')':>8} | {'/Trip':>7} | {'Cycles':>7} | {'Calls':>7} | {'(m3)':>14} | {'(M$)':>8} | {'OPEX':>8} | {'OPEX':>8} | {'NPC':>8} | {'($/ton)':>7} | {'':>3} |")
    print(f"|{'-'*10}|{'-'*10}|{'-'*9}|{'-'*9}|{'-'*9}|{'-'*16}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*9}|{'-'*5}|")

    for _, row in df_year.iterrows():
        shuttle = int(row['Shuttle_Size_cbm'])
        shuttles = int(row['Total_Shuttles'])
        vessels_per_trip = int(row['Vessels_Per_Trip'])
        annual_cycles = int(row['Annual_Cycles'])
        annual_calls = int(row['Annual_Calls'])
        total_supply = int(row['Supply_m3'])

        if shuttle in scenario_pump.index:
            scen = scenario_pump.loc[shuttle]
            capex = scen['NPC_Annualized_Shuttle_CAPEX_USDm'] + scen['NPC_Annualized_Bunkering_CAPEX_USDm']
            fixed_opex = scen['NPC_Shuttle_fOPEX_USDm'] + scen['NPC_Bunkering_fOPEX_USDm']
            var_opex = scen['NPC_Shuttle_vOPEX_USDm'] + scen['NPC_Bunkering_vOPEX_USDm']
            npc = scen['NPC_Total_USDm']
            lco = scen['LCOAmmonia_USD_per_ton']
        else:
            capex = fixed_opex = var_opex = npc = lco = 0

        opt = 'YES' if shuttle == optimal_shuttle else ''

        print(f"| {shuttle:>8,} | {shuttles:>8} | {vessels_per_trip:>7} | {annual_cycles:>7,} | {annual_calls:>7,} | {total_supply:>14,} | {capex:>8.1f} | {fixed_opex:>8.1f} | {var_opex:>8.1f} | {npc:>8.2f} | {lco:>7.2f} | {opt:>3} |")

    print(f"\n{'='*100}")
    print(f"Optimal: Shuttle {optimal_shuttle:,} m3 with NPC ${scenario_pump.loc[optimal_shuttle, 'NPC_Total_USDm']:.2f}M")
    print(f"{'='*100}\n")


def main():
    parser = argparse.ArgumentParser(description="Shuttle size comparison analysis")
    parser.add_argument("--case", "-c", default="case_2_yeosu",
                        help="Case ID (case_1, case_2_yeosu, case_2_ulsan)")
    parser.add_argument("--pump", "-p", type=int, default=1000,
                        help="Pump rate in m3/h (default: 1000)")
    parser.add_argument("--year", "-y", type=int, default=2050,
                        help="Year for analysis (default: 2050)")

    args = parser.parse_args()
    analyze_shuttle_comparison(args.case, args.pump, args.year)


if __name__ == "__main__":
    main()
