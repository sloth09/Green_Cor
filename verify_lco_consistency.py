#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify consistency between single mode and yearly_simulation LCOAmmonia values.

This script:
1. Runs single mode optimization to get the optimal scenario
2. Extracts the optimal shuttle/pump combination
3. Runs yearly_simulation with the same parameters
4. Compares LCOAmmonia values from both modes
5. Validates that they match within tolerance

The LCOAmmonia calculation should be identical:
  LCOAmmonia = (Annualized_CAPEX + OPEX over 20 years) / (Total_Supply in tons over 20 years)
"""

import sys
from pathlib import Path
import pandas as pd
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import load_config
from main import run_single_case, run_yearly_simulation


def verify_lco_consistency(case_id: str):
    """
    Verify LCOAmmonia consistency between single mode and yearly_simulation.

    Args:
        case_id: Case ID to test (e.g., "case_1", "case_2_ulsan")

    Returns:
        Dictionary with verification results
    """
    print("\n" + "="*80)
    print(f"LCOAmmonia Consistency Verification - {case_id}")
    print("="*80)

    output_path = Path("results")
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Load config and run single mode optimization
        print("\n[Step 1] Running single mode optimization...")
        config = load_config(case_id)
        scenario_df, yearly_df = run_single_case(config, output_path)

        if scenario_df is None or scenario_df.empty:
            print("[ERROR] Single mode returned no results")
            return None

        # Step 2: Extract optimal scenario
        optimal_idx = scenario_df["NPC_Total_USDm"].idxmin()
        optimal = scenario_df.loc[optimal_idx]

        shuttle_size = int(optimal["Shuttle_Size_cbm"])
        pump_size = int(optimal["Pump_Size_m3ph"])
        lco_single_mode = optimal["LCOAmmonia_USD_per_ton"]

        print(f"\n[Step 2] Optimal Scenario Found:")
        print(f"  Shuttle Size: {shuttle_size} m³")
        print(f"  Pump Size: {pump_size} m³/h")
        print(f"  NPC Total: ${optimal['NPC_Total_USDm']:.2f}M")
        print(f"  LCOAmmonia (Single Mode): ${lco_single_mode:.2f}/ton")
        print(f"  Total Supply (20 years): {optimal['Total_Supply_20yr_ton']:.0f} tons")

        # Step 3: Run yearly_simulation with same parameters
        print("\n[Step 3] Running yearly_simulation with same parameters...")
        config = load_config(case_id)
        config["execution"]["run_mode"] = "yearly_simulation"
        config["execution"]["single_scenario_shuttle_cbm"] = shuttle_size
        config["execution"]["single_scenario_pump_m3ph"] = pump_size

        yearly_sim_df = run_yearly_simulation(config, shuttle_size, pump_size, output_path)

        if yearly_sim_df is None or yearly_sim_df.empty:
            print("[ERROR] Yearly simulation returned no results")
            return None

        # Step 4: Extract final LCOAmmonia from yearly_simulation (last row = year 2050)
        final_row = yearly_sim_df.iloc[-1]
        lco_yearly_sim = final_row["LCOAmmonia_USD_per_ton"]
        cumulative_supply_ton = final_row["Cumulative_Supply_ton"]
        cumulative_cost_usdm = final_row["Cumulative_Cost_USDm"]

        print(f"\n[Step 4] Yearly Simulation Results (Final Year 2050):")
        print(f"  LCOAmmonia (Yearly Simulation): ${lco_yearly_sim:.2f}/ton")
        print(f"  Cumulative Supply: {cumulative_supply_ton:.0f} tons")
        print(f"  Cumulative Cost: ${cumulative_cost_usdm:.2f}M")

        # Step 5: Compare values
        print("\n" + "="*80)
        print("VERIFICATION RESULTS")
        print("="*80)

        difference = abs(lco_single_mode - lco_yearly_sim)
        tolerance = 0.5  # $0.50/ton tolerance
        match = difference <= tolerance

        print(f"\nLCOAmmonia Comparison:")
        print(f"  Single Mode:        ${lco_single_mode:.2f}/ton")
        print(f"  Yearly Simulation:  ${lco_yearly_sim:.2f}/ton")
        print(f"  Difference:         ${difference:.2f}/ton")
        print(f"  Tolerance:          ${tolerance:.2f}/ton")
        match_status = "[PASS]" if match else "[FAIL]"
        print(f"  Match Status:       {match_status}")

        if match:
            print("\n[OK] LCOAmmonia values are consistent!")
        else:
            print(f"\n[WARN] LCOAmmonia values differ by ${difference:.2f}/ton")
            print("This may indicate a calculation discrepancy.")

        # Step 6: Detailed year-by-year analysis
        print("\n" + "="*80)
        print("Year-by-Year LCOAmmonia Evolution")
        print("="*80)

        yearly_summary = yearly_sim_df[[
            "Year", "Supply_m3", "Cumulative_Supply_ton",
            "Total_Year_Cost_USDm", "Cumulative_Cost_USDm", "LCOAmmonia_USD_per_ton"
        ]].copy()

        print("\n" + yearly_summary.to_string(index=False))

        # Analysis of early years vs final year
        first_row = yearly_sim_df.iloc[0]
        lco_first_year = first_row.get("LCOAmmonia_USD_per_ton", 0)

        print(f"\n\nLCOAmmonia Trend Analysis:")
        print(f"  Year 2030 (First Year):  ${lco_first_year:.2f}/ton")
        print(f"  Year 2050 (Final Year):  ${lco_yearly_sim:.2f}/ton")
        print(f"  Change Over 20 Years:    ${lco_yearly_sim - lco_first_year:+.2f}/ton")

        # Summary statistics
        avg_lco = yearly_sim_df["LCOAmmonia_USD_per_ton"].mean()
        min_lco = yearly_sim_df["LCOAmmonia_USD_per_ton"].min()
        max_lco = yearly_sim_df["LCOAmmonia_USD_per_ton"].max()

        print(f"\nLCOAmmonia Statistics Across All Years:")
        print(f"  Average:  ${avg_lco:.2f}/ton")
        print(f"  Minimum:  ${min_lco:.2f}/ton")
        print(f"  Maximum:  ${max_lco:.2f}/ton")

        return {
            "case_id": case_id,
            "shuttle_size": shuttle_size,
            "pump_size": pump_size,
            "lco_single_mode": lco_single_mode,
            "lco_yearly_sim": lco_yearly_sim,
            "difference": difference,
            "tolerance": tolerance,
            "match": match,
            "cumulative_supply_ton": cumulative_supply_ton,
            "cumulative_cost_usdm": cumulative_cost_usdm,
            "yearly_df": yearly_sim_df,
        }

    except Exception as e:
        print(f"\n[ERROR] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run verification for all available cases."""
    print("\n" + "="*80)
    print("LCOAmmonia Consistency Verification Suite")
    print("="*80)

    # Test cases
    test_cases = ["case_1", "case_2_yeosu", "case_2_ulsan"]

    results = {}
    for case in test_cases:
        try:
            result = verify_lco_consistency(case)
            if result:
                results[case] = result
                print(f"\n[OK] {case} verification completed")
            else:
                print(f"\n[FAIL] {case} verification failed")
        except Exception as e:
            print(f"\n[ERROR] {case} verification error: {e}")
            results[case] = {"error": str(e)}

    # Summary report
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)

    passed = sum(1 for r in results.values() if isinstance(r, dict) and r.get("match"))
    total = len(results)

    print(f"\nTests Passed: {passed}/{total}")

    for case, result in results.items():
        if isinstance(result, dict) and "error" not in result:
            status = "[PASS]" if result.get("match") else "[FAIL]"
            diff = result.get("difference", 0)
            print(f"  {case:20} {status}  (diff: ${diff:.2f}/ton)")
        else:
            print(f"  {case:20} [ERROR]")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
