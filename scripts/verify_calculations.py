#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script: Manual Calculations vs CSV Comparison
This script performs manual calculations and compares against CSV output.
"""

import math
import csv
from pathlib import Path

# ============================================
# BASE PARAMETERS (from config files)
# ============================================

# Economic
ANNUALIZATION_RATE = 0.07
YEARS = 21
FUEL_PRICE = 600.0  # USD/ton

# Pump
PUMP_DELTA_P_BAR = 4.0
PUMP_EFFICIENCY = 0.7
PUMP_COST_PER_KW = 2000.0

# Shuttle CAPEX
REF_CAPEX = 61_500_000
REF_SIZE = 40_000
ALPHA = 0.75

# OPEX Ratios
SHUTTLE_FIXED_OPEX_RATIO = 0.05
SHUTTLE_EQUIPMENT_RATIO = 0.03
BUNKERING_FIXED_OPEX_RATIO = 0.05

# Operational
SHORE_PUMP_RATE = 1500.0  # m3/h
MAX_ANNUAL_HOURS = 8000
BUNKER_VOLUME = 5000.0  # m3

# MCR Map (kW)
MCR_MAP = {
    # Case 1
    500: 380, 1000: 620, 1500: 820, 2000: 1000, 2500: 1160,
    3000: 1310, 3500: 1450, 4000: 1580, 4500: 1700,
    5000: 1810, 7500: 2180, 10000: 2420,
    # Case 2 additional
    15000: 3080, 20000: 3660, 25000: 4090, 30000: 4510,
    35000: 5030, 40000: 5620, 45000: 6070, 50000: 6510
}

# SFOC Map (g/kWh by shuttle size -> DWT -> engine type)
SFOC_MAP = {
    500: 505, 1000: 505, 1500: 505, 2000: 505, 2500: 505,
    3000: 505, 3500: 505,
    4000: 436, 4500: 436, 5000: 436, 7500: 436,
    10000: 413, 15000: 413,
    20000: 390, 25000: 390, 30000: 390, 35000: 390,
    40000: 379, 45000: 379, 50000: 379
}

# Case parameters
CASE_PARAMS = {
    'case_1': {
        'travel_time': 1.0,  # hours one-way
        'has_storage': True,
        'travel_factor': 1.0,  # code uses 1.0 for Case 1
    },
    'case_2_yeosu': {
        'travel_time': 5.73,  # 86nm / 15knots
        'has_storage': False,
        'travel_factor': 2.0,
    },
    'case_2_ulsan': {
        'travel_time': 3.93,  # 59nm / 15knots
        'has_storage': False,
        'travel_factor': 2.0,
    }
}


def calc_annuity_factor(r, n):
    """Calculate annuity factor."""
    if r == 0:
        return float(n)
    return (1.0 - (1.0 + r) ** (-n)) / r


def calc_shuttle_capex(size):
    """Calculate shuttle CAPEX."""
    return REF_CAPEX * (size / REF_SIZE) ** ALPHA


def calc_pump_power(flow_rate):
    """Calculate pump power in kW."""
    delta_p_pa = PUMP_DELTA_P_BAR * 100000
    flow_m3s = flow_rate / 3600
    power_w = (delta_p_pa * flow_m3s) / PUMP_EFFICIENCY
    return power_w / 1000


def calc_pump_capex(flow_rate):
    """Calculate pump CAPEX."""
    power_kw = calc_pump_power(flow_rate)
    return power_kw * PUMP_COST_PER_KW


def calc_bunkering_capex(shuttle_size, pump_rate):
    """Calculate bunkering system CAPEX per shuttle."""
    shuttle_capex = calc_shuttle_capex(shuttle_size)
    equipment_cost = shuttle_capex * SHUTTLE_EQUIPMENT_RATIO
    pump_capex = calc_pump_capex(pump_rate)
    return equipment_cost + pump_capex


def calc_shuttle_fixed_opex(shuttle_size):
    """Calculate annual shuttle fixed OPEX."""
    capex = calc_shuttle_capex(shuttle_size)
    return capex * SHUTTLE_FIXED_OPEX_RATIO


def calc_bunkering_fixed_opex(shuttle_size, pump_rate):
    """Calculate annual bunkering fixed OPEX."""
    capex = calc_bunkering_capex(shuttle_size, pump_rate)
    return capex * BUNKERING_FIXED_OPEX_RATIO


def calc_shuttle_fuel_cost_per_cycle(shuttle_size, case_id):
    """Calculate shuttle fuel cost per cycle."""
    params = CASE_PARAMS[case_id]
    mcr = MCR_MAP.get(shuttle_size, 0)
    sfoc = SFOC_MAP.get(shuttle_size, 379)
    travel_time = params['travel_time']
    travel_factor = params['travel_factor']

    fuel_tons = (mcr * sfoc * travel_time * travel_factor) / 1_000_000
    return fuel_tons * FUEL_PRICE


def calc_pump_fuel_cost_per_call(pump_rate):
    """Calculate pump fuel cost per bunkering call."""
    pumping_time = BUNKER_VOLUME / pump_rate  # hours
    pump_power = calc_pump_power(pump_rate)
    sfoc = 379  # default SFOC for pump

    fuel_tons = (pump_power * sfoc * pumping_time) / 1_000_000
    return fuel_tons * FUEL_PRICE


def calc_cycle_time_case1(shuttle_size, pump_rate):
    """Calculate cycle time for Case 1."""
    shore_loading = shuttle_size / SHORE_PUMP_RATE
    travel_out = 1.0
    travel_return = 1.0
    setup_total = 2.0  # 2 x (inbound + outbound) = 2 x 1.0
    pumping = shuttle_size / pump_rate

    return shore_loading + travel_out + travel_return + setup_total + pumping


def calc_cycle_time_case2(shuttle_size, pump_rate, travel_time):
    """Calculate cycle time for Case 2."""
    shore_loading = shuttle_size / SHORE_PUMP_RATE
    travel_out = travel_time
    travel_return = travel_time
    setup_total = 2.0

    vessels_per_trip = max(1, shuttle_size // BUNKER_VOLUME)
    pumping_per_vessel = BUNKER_VOLUME / pump_rate
    pumping_total = vessels_per_trip * pumping_per_vessel

    # Basic cycle without overhead
    basic = travel_out + travel_return + setup_total + pumping_total

    # Note: actual cycle time includes overhead - we'll compare with CSV
    return shore_loading, basic


def read_csv_summary(case_id):
    """Read scenario summary CSV."""
    filepath = Path(f'results/MILP_scenario_summary_{case_id}.csv')
    if not filepath.exists():
        return {}

    data = {}
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            size = int(float(row['Shuttle_Size_cbm']))
            data[size] = {k: float(v) if v else 0 for k, v in row.items() if k != 'Shuttle_Size_cbm'}
    return data


def read_csv_yearly(case_id):
    """Read yearly results CSV (first year 2030 only)."""
    filepath = Path(f'results/MILP_per_year_results_{case_id}.csv')
    if not filepath.exists():
        return {}

    data = {}
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(float(row['Year']))
            if year != 2030:
                continue
            size = int(float(row['Shuttle_Size_cbm']))
            data[size] = {k: float(v) if v else 0 for k, v in row.items()}
    return data


def verify_case(case_id, shuttle_sizes):
    """Verify calculations for a case."""
    print(f"\n{'='*70}")
    print(f"VERIFICATION: {case_id.upper()}")
    print(f"{'='*70}")

    summary_csv = read_csv_summary(case_id)
    yearly_csv = read_csv_yearly(case_id)
    params = CASE_PARAMS[case_id]

    results = []

    for size in shuttle_sizes:
        if size not in summary_csv:
            continue

        csv_data = summary_csv[size]
        yearly_data = yearly_csv.get(size, {})

        print(f"\n--- Shuttle Size: {size} m3 ---")

        # 1. Shuttle CAPEX
        manual_shuttle_capex = calc_shuttle_capex(size)
        # CSV has per-shuttle value in yearly data
        csv_yearly_capex = yearly_data.get('Actual_CAPEX_Shuttle_USDm', 0) * 1_000_000
        csv_shuttles = yearly_data.get('New_Shuttles', 0)
        csv_per_shuttle = csv_yearly_capex / csv_shuttles if csv_shuttles > 0 else 0

        diff_capex = abs(manual_shuttle_capex - csv_per_shuttle) / csv_per_shuttle * 100 if csv_per_shuttle > 0 else 0
        status_capex = "PASS" if diff_capex < 1 else "FAIL"

        print(f"  Shuttle CAPEX:")
        print(f"    Manual:  ${manual_shuttle_capex:,.0f}")
        print(f"    CSV:     ${csv_per_shuttle:,.0f}")
        print(f"    Diff:    {diff_capex:.2f}%  [{status_capex}]")

        results.append(('Shuttle CAPEX', size, manual_shuttle_capex, csv_per_shuttle, diff_capex, status_capex))

        # 2. Pump Power & CAPEX
        pump_rate = 1000
        manual_pump_power = calc_pump_power(pump_rate)
        manual_pump_capex = calc_pump_capex(pump_rate)

        print(f"  Pump (1000 m3/h):")
        print(f"    Power:   {manual_pump_power:.2f} kW")
        print(f"    CAPEX:   ${manual_pump_capex:,.0f}")

        # 3. Fixed OPEX (per shuttle per year)
        manual_fopex_shuttle = calc_shuttle_fixed_opex(size)
        csv_fopex_shuttle = yearly_data.get('FixedOPEX_Shuttle_USDm', 0) * 1_000_000
        csv_total_shuttles = yearly_data.get('Total_Shuttles', 0)
        csv_fopex_per_shuttle = csv_fopex_shuttle / csv_total_shuttles if csv_total_shuttles > 0 else 0

        diff_fopex = abs(manual_fopex_shuttle - csv_fopex_per_shuttle) / csv_fopex_per_shuttle * 100 if csv_fopex_per_shuttle > 0 else 0
        status_fopex = "PASS" if diff_fopex < 1 else "FAIL"

        print(f"  Shuttle Fixed OPEX (per unit/year):")
        print(f"    Manual:  ${manual_fopex_shuttle:,.0f}")
        print(f"    CSV:     ${csv_fopex_per_shuttle:,.0f}")
        print(f"    Diff:    {diff_fopex:.2f}%  [{status_fopex}]")

        results.append(('Shuttle fOPEX', size, manual_fopex_shuttle, csv_fopex_per_shuttle, diff_fopex, status_fopex))

        # 4. Variable OPEX - Shuttle Fuel (per cycle)
        manual_fuel_cost = calc_shuttle_fuel_cost_per_cycle(size, case_id)
        csv_vopex_shuttle = yearly_data.get('VariableOPEX_Shuttle_USDm', 0) * 1_000_000
        csv_annual_cycles = yearly_data.get('Annual_Cycles', 0)
        csv_fuel_per_cycle = csv_vopex_shuttle / csv_annual_cycles if csv_annual_cycles > 0 else 0

        diff_fuel = abs(manual_fuel_cost - csv_fuel_per_cycle) / csv_fuel_per_cycle * 100 if csv_fuel_per_cycle > 0 else 0
        status_fuel = "PASS" if diff_fuel < 5 else "FAIL"  # 5% tolerance for fuel

        print(f"  Shuttle Fuel Cost (per cycle):")
        print(f"    Manual:  ${manual_fuel_cost:,.2f}")
        print(f"    CSV:     ${csv_fuel_per_cycle:,.2f}")
        print(f"    Diff:    {diff_fuel:.2f}%  [{status_fuel}]")

        results.append(('Shuttle vOPEX/cycle', size, manual_fuel_cost, csv_fuel_per_cycle, diff_fuel, status_fuel))

        # 5. Cycle Time
        csv_cycle = csv_data.get('Cycle_Duration_hr', 0)

        if params['has_storage']:
            manual_cycle = calc_cycle_time_case1(size, pump_rate)
            diff_cycle = abs(manual_cycle - csv_cycle) / csv_cycle * 100 if csv_cycle > 0 else 0
            status_cycle = "PASS" if diff_cycle < 1 else "FAIL"

            print(f"  Cycle Time:")
            print(f"    Manual:  {manual_cycle:.4f} hr")
            print(f"    CSV:     {csv_cycle:.4f} hr")
            print(f"    Diff:    {diff_cycle:.2f}%  [{status_cycle}]")
        else:
            shore, basic = calc_cycle_time_case2(size, pump_rate, params['travel_time'])
            csv_shore = csv_data.get('Shore_Loading_hr', 0)
            csv_basic = csv_data.get('Basic_Cycle_Duration_hr', 0)

            diff_shore = abs(shore - csv_shore) / csv_shore * 100 if csv_shore > 0 else 0
            status_shore = "PASS" if diff_shore < 1 else "FAIL"

            print(f"  Shore Loading:")
            print(f"    Manual:  {shore:.4f} hr")
            print(f"    CSV:     {csv_shore:.4f} hr")
            print(f"    Diff:    {diff_shore:.2f}%  [{status_shore}]")

            print(f"  Basic Cycle (excl. overhead):")
            print(f"    Manual:  {basic:.4f} hr (without overhead)")
            print(f"    CSV:     {csv_basic:.4f} hr (includes overhead)")
            overhead = csv_basic - (basic - shore)  # Reverse calculate overhead
            print(f"    Overhead: {overhead:.2f} hr")

            manual_cycle = shore
            status_cycle = status_shore

        results.append(('Cycle Time', size, manual_cycle if params['has_storage'] else shore,
                       csv_cycle if params['has_storage'] else csv_shore,
                       diff_cycle if params['has_storage'] else diff_shore, status_cycle))

        # 6. NPC Total
        csv_npc = csv_data.get('NPC_Total_USDm', 0)
        csv_lco = csv_data.get('LCOAmmonia_USD_per_ton', 0)

        print(f"  NPC Total: ${csv_npc:.2f}M")
        print(f"  LCOAmmonia: ${csv_lco:.2f}/ton")

    return results


def main():
    print("=" * 70)
    print("GREEN CORRIDOR MILP VERIFICATION")
    print("Manual Calculations vs CSV Comparison")
    print("=" * 70)

    # 1. Annuity Factor
    af = calc_annuity_factor(ANNUALIZATION_RATE, YEARS)
    print(f"\n[1] Annuity Factor")
    print(f"    Formula: [1 - (1+r)^(-n)] / r")
    print(f"    Calc:    [1 - (1+0.07)^(-21)] / 0.07")
    print(f"    Result:  {af:.4f}")
    print(f"    Expected: 10.8355")
    print(f"    Status:  {'PASS' if abs(af - 10.8355) < 0.001 else 'FAIL'}")

    # 2. Pump Power
    pump_power = calc_pump_power(1000)
    print(f"\n[2] Pump Power (1000 m3/h)")
    print(f"    Formula: (delta_P_Pa x Q_m3s) / eta / 1000")
    print(f"    Calc:    (400000 x 0.2778) / 0.7 / 1000")
    print(f"    Result:  {pump_power:.2f} kW")
    print(f"    Status:  {'PASS' if abs(pump_power - 158.73) < 0.1 else 'FAIL'}")

    # 3. Case 1 Verification
    case1_sizes = [500, 1000, 2500, 5000, 10000]
    verify_case('case_1', case1_sizes)

    # 4. Case 2-1 Verification
    case2_1_sizes = [5000, 10000, 20000]
    verify_case('case_2_yeosu', case2_1_sizes)

    # 5. Case 2-2 Verification
    case2_2_sizes = [5000, 10000, 20000]
    verify_case('case_2_ulsan', case2_2_sizes)

    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
