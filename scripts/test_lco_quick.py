#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test of LCOAmmonia calculation consistency.

Tests the optimal scenario from case_1 optimization with yearly_simulation
to verify LCOAmmonia values match.
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from src import load_config
from src.optimizer import BunkeringOptimizer
from main import run_yearly_simulation


def test_case_1():
    """Test case_1 optimization and yearly_simulation consistency."""
    print("\n" + "="*80)
    print("Testing Case 1: LCOAmmonia Consistency")
    print("="*80)

    output_path = Path("results")
    output_path.mkdir(parents=True, exist_ok=True)

    # Run optimization for case_1
    print("\n[1/3] Running case_1 optimization...")
    config = load_config("case_1")
    optimizer = BunkeringOptimizer(config)
    scenario_df, yearly_df = optimizer.solve()

    if scenario_df.empty:
        print("[ERROR] Optimization failed")
        return False

    # Get optimal scenario
    optimal_idx = scenario_df["NPC_Total_USDm"].idxmin()
    optimal = scenario_df.loc[optimal_idx]

    shuttle_size = int(optimal["Shuttle_Size_cbm"])
    pump_size = int(optimal["Pump_Size_m3ph"])
    lco_single = optimal["LCOAmmonia_USD_per_ton"]
    npc_single = optimal["NPC_Total_USDm"]
    supply_single = optimal["Total_Supply_20yr_ton"]

    print(f"\n[OK] Optimal Scenario Found:")
    print(f"  Shuttle: {shuttle_size} m³, Pump: {pump_size} m³/h")
    print(f"  NPC (Single Mode): ${npc_single:.2f}M")
    print(f"  LCOAmmonia (Single Mode): ${lco_single:.2f}/ton")
    print(f"  Total Supply (20yr): {supply_single:.0f} tons")

    # Run yearly_simulation with same parameters
    print("\n[2/3] Running yearly_simulation with same parameters...")
    config = load_config("case_1")
    yearly_sim_df = run_yearly_simulation(config, shuttle_size, pump_size, output_path)

    if yearly_sim_df is None or yearly_sim_df.empty:
        print("[ERROR] Yearly simulation failed")
        return False

    # Get final year values
    final_row = yearly_sim_df.iloc[-1]
    lco_yearly = final_row["LCOAmmonia_USD_per_ton"]
    supply_yearly = final_row["Cumulative_Supply_ton"]
    cost_yearly = final_row["Cumulative_Cost_USDm"]

    print(f"\n[OK] Yearly Simulation Complete (Year 2050):")
    print(f"  LCOAmmonia (Yearly Sim): ${lco_yearly:.2f}/ton")
    print(f"  Cumulative Supply: {supply_yearly:.0f} tons")
    print(f"  Cumulative Cost: ${cost_yearly:.2f}M")

    # Verification
    print("\n" + "="*80)
    print("VERIFICATION RESULTS")
    print("="*80)

    diff = abs(lco_single - lco_yearly)
    tolerance = 0.5

    print(f"\nLCOAmmonia Comparison:")
    print(f"  Single Mode:       ${lco_single:.2f}/ton")
    print(f"  Yearly Simulation: ${lco_yearly:.2f}/ton")
    print(f"  Difference:        ${diff:.2f}/ton")
    print(f"  Tolerance:         ${tolerance:.2f}/ton")

    match = diff <= tolerance
    result_status = "[PASS] - Values Match!" if match else "[FAIL] - Values Differ"
    print(f"\nResult: {result_status}")

    # Supply and cost comparison
    print(f"\nSupply Comparison:")
    print(f"  Single Mode: {supply_single:.0f} tons")
    print(f"  Yearly Sim:  {supply_yearly:.0f} tons")
    supply_match = "[OK]" if abs(supply_single - supply_yearly) < 1 else "[FAIL]"
    print(f"  Match: {supply_match}")

    # Year-by-year trend
    print(f"\nYear-by-Year LCOAmmonia Trend:")
    trend_df = yearly_sim_df[["Year", "LCOAmmonia_USD_per_ton"]].copy()
    print(trend_df.to_string(index=False))

    return match


if __name__ == "__main__":
    try:
        success = test_case_1()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
