#!/usr/bin/env python3
"""
Main entry point for bunkering optimization model.

All configuration is controlled through YAML config files.
No command-line arguments needed - everything is set in config/base.yaml

Edit config/base.yaml execution section to control:
  - Run mode: "single" (full optimization), "single_scenario" (quick time calc),
             "annual_simulation" (1-year simulation), "all" (all cases),
             or "multiple" (selected cases)
  - Which case to run
  - Single vs multiple case execution
  - Output directory
  - Export formats
  - (For single_scenario/annual_simulation) Specific shuttle/pump combination

For single_scenario mode:
  - single_scenario_shuttle_cbm: Shuttle size in m³
  - single_scenario_pump_m3ph: Pump flow rate in m³/h

For annual_simulation mode:
  - single_scenario_shuttle_cbm: Shuttle size in m³
  - single_scenario_pump_m3ph: Pump flow rate in m³/h
  - simulation_year: Year to simulate (e.g., 2030, 2050)
"""

import sys
from pathlib import Path
import time
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import load_config, BunkeringOptimizer
from src.export_excel import ExcelExporter
from src.export_docx import WordExporter
from src.cycle_time_calculator import CycleTimeCalculator
from src.cost_calculator import CostCalculator
from src.fleet_sizing_calculator import FleetSizingCalculator
from src.utils import calculate_vessel_growth, calculate_annual_demand, calculate_m3_per_voyage
from math import ceil


def print_cycle_time_breakdown(cycle_info, config, shuttle_size_cbm, pump_size_m3ph):
    """
    Print detailed breakdown of single round-trip cycle time.

    Reusable function for both single_scenario and annual_simulation modes.

    Args:
        cycle_info: Dictionary with cycle time breakdown from CycleTimeCalculator
        config: Configuration dictionary
        shuttle_size_cbm: Shuttle size in m³
        pump_size_m3ph: Pump flow rate in m³/h
    """
    # Get land pump rate
    land_pump_rate = config["operations"].get("port_pump_rate_m3h",
                                               config["operations"].get("shore_supply_pump_rate_m3ph", 1500.0))
    ship_fuel_per_call = config["bunkering"]["bunker_volume_per_call_m3"]

    # Display time breakdown - case-specific structure
    print("\n【1회 왕복 운항 시간 분석 (Single Round-Trip Voyage Breakdown)】")
    print("-" * 60)

    # Common first steps
    print(f"육상 적재 (Shore Loading):               {cycle_info['shore_loading']:.2f}h")
    print(f"  Land Pump: {land_pump_rate:.0f} m³/h × Shuttle: {shuttle_size_cbm} m³")
    print(f"편도 항해 (Outbound Travel):             {cycle_info['travel_outbound']:.2f}h")

    # Case-specific: Port operations
    is_case_1 = cycle_info['has_storage_at_busan']

    if is_case_1:
        # CASE 1: Shuttle makes multiple trips within port
        print(f"호스 연결 (Connection & Purging):       {cycle_info['setup_inbound']:.2f}h")
        print(f"벙커링 (Bunkering):                      {cycle_info['pumping_per_vessel']:.2f}h")
        print(f"  Pump: {pump_size_m3ph} m³/h × Shuttle Capacity: {shuttle_size_cbm} m³")
        print(f"호스 분리 (Disconnection & Purging):    {cycle_info['setup_outbound']:.2f}h")
    else:
        # CASE 2: One trip serves multiple vessels at destination port
        if cycle_info['port_entry'] > 0:
            print(f"부산항 진입 (Port Entry):                {cycle_info['port_entry']:.2f}h")

        # Repeat per vessel at destination
        num_vessels_display = cycle_info['vessels_per_trip']
        if num_vessels_display > 1:
            print(f"  [아래 내용이 {num_vessels_display}척 반복]")

        print(f"  부산항 이동 (Docking/Movement):        {cycle_info['movement_per_vessel']:.2f}h")
        print(f"  호스 연결 (Connection & Purging):      {cycle_info['setup_inbound']:.2f}h")
        print(f"  벙커링 (Bunkering):                     {cycle_info['pumping_per_vessel']:.2f}h")
        print(f"    Pump: {pump_size_m3ph} m³/h × Ship Fuel: {ship_fuel_per_call:.0f} m³")
        print(f"  호스 분리 (Disconnection & Purging):   {cycle_info['setup_outbound']:.2f}h")

        if cycle_info['port_exit'] > 0:
            print(f"부산항 퇴출 (Port Exit):                 {cycle_info['port_exit']:.2f}h")

    print(f"복귀 항해 (Return Travel):               {cycle_info['travel_return']:.2f}h")
    print("-" * 60)
    print(f"★ 총 왕복 사이클 시간:                   {cycle_info['cycle_duration']:.2f}h")

    # Calculate and display annual capacity for one shuttle
    max_annual_hours = config["operations"]["max_annual_hours_per_vessel"]
    annual_cycles_max = max_annual_hours / cycle_info['cycle_duration'] if cycle_info['cycle_duration'] > 0 else 0
    print(f"★ 연간 최대 항차 (1대):                  {annual_cycles_max:.0f}회 ({max_annual_hours:.0f}h ÷ {cycle_info['cycle_duration']:.2f}h)")
    print("-" * 60)


def run_single_scenario(config, shuttle_size_cbm, pump_size_m3ph, output_path):
    """
    Run a single scenario calculation (no optimization).

    Calculates cycle time for a specific shuttle/pump combination without
    running the full optimization. Useful for quick time calculations.

    Args:
        config: Configuration dictionary
        shuttle_size_cbm: Shuttle size in m³
        pump_size_m3ph: Pump flow rate in m³/h
        output_path: Output directory path

    Returns:
        Dictionary with time breakdown information
    """
    try:
        print("\n" + "="*60)
        print(f"Case: {config.get('case_name', 'Unknown')}")
        print(f"Case ID: {config.get('case_id', 'unknown')}")
        print(f"Scenario: Shuttle {shuttle_size_cbm}m³ + Pump {pump_size_m3ph}m³/h")
        print("="*60)

        # Initialize calculator
        case_id = config.get("case_id", "unknown")
        calculator = CycleTimeCalculator(case_id, config)

        # Get shuttle configuration details (before calculating num_vessels)
        ship_fuel_per_call = config["bunkering"]["bunker_volume_per_call_m3"]
        has_storage_at_busan = config["operations"].get("has_storage_at_busan", True)

        # Calculate num_vessels based on case type
        # Case 1: Always 1 vessel (shuttle makes multiple trips if needed)
        # Case 2: Multiple vessels per trip (shuttle_size / bunker_volume)
        if has_storage_at_busan:
            num_vessels = 1
        else:
            # Case 2: Calculate how many vessels can be served per trip
            num_vessels = max(1, int(shuttle_size_cbm // ship_fuel_per_call))

        # Calculate cycle time
        cycle_info = calculator.calculate_single_cycle(
            shuttle_size_m3=shuttle_size_cbm,
            pump_size_m3ph=pump_size_m3ph,
            num_vessels=num_vessels
        )

        # Display single round-trip cycle time breakdown
        print_cycle_time_breakdown(cycle_info, config, shuttle_size_cbm, pump_size_m3ph)
        print("="*60)

        # Operating metrics - use values from cycle_info for consistency
        annual_cycles = cycle_info['annual_cycles']
        annual_supply_m3 = cycle_info['annual_supply_m3']
        ships_per_year = cycle_info['ships_per_year']
        time_utilization = (annual_cycles * cycle_info['cycle_duration'] / 8000.0) * 100

        print("\n【연간 운영 지표 (Annual Operations Metrics)】")
        print("-" * 60)
        print(f"연간 운항 한도:     8,000 시간")
        print(f"1회 운항 시간:      {cycle_info['cycle_duration']:.2f}시간")
        print(f"연간 최대 항차:     {annual_cycles:.0f}회 ({annual_cycles * cycle_info['cycle_duration']:.0f}시간)")
        print(f"연간 공급 용량:     {annual_supply_m3:,.0f}m³")
        print(f"★ 벙커링 가능선박:   {ships_per_year:.0f}척/년 (1척 = {ship_fuel_per_call:.0f}m³)")
        print(f"시간 활용도:        {time_utilization:.1f}%")
        print(f"선박당 왕복 일정:   {cycle_info['cycle_duration'] / 24 if cycle_info['cycle_duration'] > 0 else 0:.3f}일/회")
        print("="*60)

        # Export to CSV for single scenario
        export_config = config.get("execution", {}).get("export", {})
        if export_config.get("csv", True):
            # Create a minimal scenario dataframe for this single scenario
            scenario_data = {
                "Shuttle_Size_cbm": [shuttle_size_cbm],
                "Pump_Size_m3ph": [pump_size_m3ph],
                "Cycle_Duration_hr": [cycle_info['cycle_duration']],
                "Shore_Loading_hr": [cycle_info['shore_loading']],
                "Travel_Outbound_hr": [cycle_info['travel_outbound']],
                "Travel_Return_hr": [cycle_info['travel_return']],
                "Setup_Inbound_hr": [cycle_info['setup_inbound']],
                "Setup_Outbound_hr": [cycle_info['setup_outbound']],
                "Pumping_Per_Vessel_hr": [cycle_info['pumping_per_vessel']],
                "Pumping_Total_hr": [cycle_info['pumping_total']],
                "Basic_Cycle_Duration_hr": [cycle_info['basic_cycle_duration']],
                "Annual_Cycles_Max": [annual_cycles],
                "Annual_Supply_m3": [annual_supply_m3],
                "Ships_Per_Year": [ships_per_year],
                "Time_Utilization_Ratio_percent": [time_utilization],
            }
            scenario_df = pd.DataFrame(scenario_data)

            scenario_file = output_path / f"MILP_scenario_single_{case_id}_{shuttle_size_cbm}_{pump_size_m3ph}.csv"
            scenario_df.to_csv(scenario_file, index=False, encoding="utf-8-sig")
            print(f"\n[OK] CSV single scenario: {scenario_file}")

        return cycle_info

    except Exception as e:
        print(f"Error during single scenario calculation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def run_annual_simulation(config, shuttle_size_cbm, pump_size_m3ph, simulation_year, output_path):
    """
    Run a single-year simulation for a specific shuttle/pump combination.

    Calculates required shuttles, annual operations, utilization, and costs
    for one specific year without optimization.

    Args:
        config: Configuration dictionary
        shuttle_size_cbm: Shuttle size in m³
        pump_size_m3ph: Pump flow rate in m³/h
        simulation_year: Year to simulate (e.g., 2030, 2050)
        output_path: Output directory path

    Returns:
        Dictionary with simulation results
    """
    try:
        print("\n" + "="*60)
        print("Annual Simulation Mode (Single Year)")
        print("="*60)
        print(f"Case: {config.get('case_name', 'Unknown')}")
        print(f"Case ID: {config.get('case_id', 'unknown')}")
        print(f"Year: {simulation_year}")
        print(f"Shuttle: {shuttle_size_cbm} m³")
        print(f"Pump: {pump_size_m3ph} m³/h")
        print("="*60)

        # Initialize calculators
        case_id = config.get("case_id", "unknown")
        cycle_calculator = CycleTimeCalculator(case_id, config)
        cost_calculator = CostCalculator(config)

        # Get configuration parameters
        start_year = config["time_period"]["start_year"]
        end_year = config["time_period"]["end_year"]
        start_vessels = config["shipping"]["start_vessels"]
        end_vessels = config["shipping"]["end_vessels"]
        kg_per_voyage = config["shipping"]["kg_per_voyage"]
        voyages_per_year = config["shipping"]["voyages_per_year"]
        density_storage = config["ammonia"]["density_storage_ton_m3"]
        bunker_volume = config["bunkering"]["bunker_volume_per_call_m3"]
        max_annual_hours = config["operations"]["max_annual_hours_per_vessel"]
        has_storage_at_busan = config["operations"].get("has_storage_at_busan", True)

        # Validate simulation year
        if simulation_year < start_year or simulation_year > end_year:
            print(f"[ERROR] Simulation year {simulation_year} out of range [{start_year}, {end_year}]",
                  file=sys.stderr)
            return None

        # Calculate vessel growth and demand for the specific year
        vessel_growth = calculate_vessel_growth(start_year, end_year, start_vessels, end_vessels)
        vessels_in_year = vessel_growth[simulation_year]

        # Use bunker_volume_per_call_m3 directly for demand calculation
        # (This overrides the kg_per_voyage conversion as intended by config)
        m3_per_voyage = bunker_volume
        annual_demand_dict = calculate_annual_demand(vessel_growth, m3_per_voyage, voyages_per_year)
        demand_m3 = annual_demand_dict[simulation_year]

        # Calculate number of vessels per trip for Case 2
        if has_storage_at_busan:
            num_vessels = 1
        else:
            num_vessels = max(1, int(shuttle_size_cbm // bunker_volume))

        # Calculate cycle time
        cycle_info = cycle_calculator.calculate_single_cycle(
            shuttle_size_m3=shuttle_size_cbm,
            pump_size_m3ph=pump_size_m3ph,
            num_vessels=num_vessels
        )

        # Display single round-trip cycle time breakdown
        print_cycle_time_breakdown(cycle_info, config, shuttle_size_cbm, pump_size_m3ph)

        cycle_duration = cycle_info['cycle_duration']

        # Calculate annual operations
        annual_calls = demand_m3 / bunker_volume  # Number of vessel bunkering calls needed

        # Extract trips_per_call from cycle_info
        # This is the key difference between bunkering calls and actual shuttle trips
        trips_per_call = cycle_info.get('trips_per_call', 1)

        # Calculate actual shuttle trips needed (Case 1 vs Case 2 difference)
        if has_storage_at_busan:
            # Case 1: Each vessel call requires multiple shuttle trips
            # Example: 1,000 m³ shuttle serving 5,000 m³ vessel = 5 trips per call
            total_trips = annual_calls * trips_per_call
        else:
            # Case 2: Each shuttle trip serves multiple vessels
            # Example: 10,000 m³ shuttle serving 2 vessels (5,000 m³ each) = 600 calls / 2 = 300 trips
            vessels_per_trip = num_vessels if num_vessels > 0 else 1
            total_trips = ceil(annual_calls / vessels_per_trip)

        # Calculate required shuttles using shared library (working time constraint only)
        # This ensures consistency with annual_simulation baseline
        fleet_calc = FleetSizingCalculator(config)
        required_shuttles = fleet_calc.calculate_required_shuttles_working_time_only(
            annual_calls, trips_per_call, cycle_duration
        )

        # Get detailed constraint info for debugging
        constraint_details = fleet_calc.get_constraint_details(
            annual_calls, trips_per_call, cycle_duration, shuttle_size_cbm
        )
        total_hours_needed = constraint_details['total_hours_needed']

        # Calculate utilization
        actual_hours = total_hours_needed
        available_hours = required_shuttles * max_annual_hours
        utilization = actual_hours / available_hours if available_hours > 0 else 0

        # Calculate annual cycles (actual shuttle trips, not bunkering calls)
        annual_cycles = total_trips  # Correct: shuttle trips, not calls
        cycles_per_shuttle = annual_cycles / required_shuttles if required_shuttles > 0 else 0

        # Calculate costs
        shuttle_capex = cost_calculator.calculate_shuttle_capex(shuttle_size_cbm)
        pump_capex = cost_calculator.calculate_pump_capex(pump_size_m3ph)
        bunkering_capex = cost_calculator.calculate_bunkering_capex(shuttle_size_cbm, pump_size_m3ph)

        # Fixed OPEX
        shuttle_fixed_opex = cost_calculator.calculate_shuttle_fixed_opex(shuttle_size_cbm)
        bunkering_fixed_opex = cost_calculator.calculate_bunkering_fixed_opex(shuttle_size_cbm, pump_size_m3ph)

        # Total CAPEX
        total_shuttle_capex = shuttle_capex * required_shuttles
        total_bunkering_capex = bunkering_capex * required_shuttles
        total_capex = total_shuttle_capex + total_bunkering_capex

        # Shore supply costs (Tank + Pump): controlled by shore_supply.enabled
        tank_capex = 0
        tank_fixed_opex = 0
        shore_pump_capex = 0
        shore_pump_fixed_opex = 0

        shore_supply_enabled = config.get("shore_supply", {}).get("enabled", False)
        if shore_supply_enabled:
            # Tank CAPEX and OPEX (Case 1 only)
            if config.get("tank_storage", {}).get("enabled", False):
                tank_capex = cost_calculator.calculate_tank_capex()
                tank_fixed_opex = cost_calculator.calculate_tank_fixed_opex()
                total_capex += tank_capex

            # Shore pump CAPEX (one-time, 1500 m³/h fixed)
            shore_pump_capex = cost_calculator.calculate_shore_pump_capex()
            shore_pump_fixed_opex = cost_calculator.calculate_shore_pump_fixed_opex()
            total_capex += shore_pump_capex

        # Annual OPEX
        total_fixed_opex = ((shuttle_fixed_opex + bunkering_fixed_opex) * required_shuttles +
                           tank_fixed_opex + shore_pump_fixed_opex)

        # Variable OPEX (fuel and energy costs)
        # Uses same logic as optimizer.py for consistency

        # 1. Shuttle fuel cost (travel time only, not total cycle)
        mcr = config["shuttle"]["mcr_map_kw"].get(int(shuttle_size_cbm), 0)
        if mcr == 0:
            shuttle_fuel_annual = 0
        else:
            sfoc = config["propulsion"]["sfoc_g_per_kwh"]
            fuel_price = config["economy"]["fuel_price_usd_per_ton"]
            travel_time_hours = config["operations"]["travel_time_hours"]

            # Travel factor: Case 1 = one-way, Case 2 = round-trip
            travel_factor = 1.0 if has_storage_at_busan else 2.0

            # Fuel per cycle (in tons): MCR × SFOC × travel_time / 1e6
            shuttle_fuel_per_cycle = (mcr * sfoc * travel_factor * travel_time_hours) / 1e6
            shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * fuel_price

            # Annual cost: per-cycle cost × annual cycles
            shuttle_fuel_annual = shuttle_fuel_cost_per_cycle * annual_cycles

        # 2. Pump energy cost
        # Both Case 1 and Case 2: One bunkering call = one pumping event = 5000 m³
        # - Case 1: Shuttle makes multiple trips for one call (shuttle < bunker_volume)
        # - Case 2: One shuttle trip serves multiple calls (shuttle > bunker_volume)
        # But pump is activated PER CALL, not per trip
        pump_power = cost_calculator.calculate_pump_power(pump_size_m3ph)
        sfoc = config["propulsion"]["sfoc_g_per_kwh"]
        fuel_price = config["economy"]["fuel_price_usd_per_ton"]

        # Pumping time per bunkering call
        pumping_time_hr_call = bunker_volume / pump_size_m3ph

        # Annual pump events = number of vessel bunkering calls
        # This is the same for both Case 1 and Case 2
        annual_pump_events = annual_calls

        # Fuel per pump event (in tons): pump_power × pumping_time × SFOC / 1e6
        pump_fuel_per_event = (pump_power * pumping_time_hr_call * sfoc) / 1e6
        pump_fuel_cost_per_event = pump_fuel_per_event * fuel_price
        pump_fuel_annual = pump_fuel_cost_per_event * annual_pump_events

        # 3. Tank cooling cost (Case 1 only, if shore_supply enabled)
        tank_variable_opex = 0
        if shore_supply_enabled and config.get("tank_storage", {}).get("enabled", False):
            tank_variable_opex = cost_calculator.calculate_tank_variable_opex()

        # Total variable OPEX
        total_variable_opex = shuttle_fuel_annual + pump_fuel_annual + tank_variable_opex

        total_opex = total_fixed_opex + total_variable_opex

        # First year total cost
        first_year_cost = total_capex + total_opex

        # Display annual operation parameters
        print("\n【연간 운영 파라미터 (Annual Operation Parameters)】")
        print("-" * 60)
        print(f"Vessels in Year {simulation_year}:        {vessels_in_year:>8} vessels")
        print(f"Annual Demand:                           {demand_m3:>8,.0f} m³")
        print(f"Bunker Volume per Call:                  {bunker_volume:>8,.0f} m³")
        print(f"Required Annual Calls:                   {annual_calls:>8,.0f} calls")
        print("-" * 60)

        print("\n【함대 요구사항 (Fleet Requirements)】")
        print("-" * 60)
        if has_storage_at_busan:
            # Case 1: Display trips_per_call conversion
            print(f"Total Hours Needed:                      {total_hours_needed:>8,.0f} hours ({total_trips:.0f} trips × {cycle_duration:.2f}h)")
            print(f"  Breakdown: {annual_calls:.0f} calls × {trips_per_call} trips/call = {total_trips:.0f} trips")
        else:
            # Case 2: Display vessels_per_trip conversion
            print(f"Total Hours Needed:                      {total_hours_needed:>8,.0f} hours ({total_trips:.0f} trips × {cycle_duration:.2f}h)")
            print(f"  Breakdown: {annual_calls:.0f} calls ÷ {num_vessels} vessels/trip = {total_trips:.0f} trips")
        print(f"Required Shuttles:                       {required_shuttles:>8} vessels (ceil({total_hours_needed:.0f}h ÷ {max_annual_hours:.0f}h))")
        print(f"Utilization Rate:                        {utilization*100:>8.1f}% ({total_hours_needed:.0f}h ÷ {available_hours:.0f}h)")
        print(f"Annual Cycles per Shuttle:               {cycles_per_shuttle:>8,.0f} trips")
        print("-" * 60)

        print(f"\n【Cost Breakdown (Year {simulation_year})】")
        print("-" * 60)
        print("CAPEX:")
        print(f"  - Shuttle:                             ${total_shuttle_capex/1e6:>8.1f}M")
        print(f"  - Bunkering Equipment:                 ${total_bunkering_capex/1e6:>8.1f}M")
        if tank_capex > 0:
            print(f"  - Storage Tank:                        ${tank_capex/1e6:>8.1f}M")
        if shore_pump_capex > 0:
            print(f"  - Shore Supply Pump:                   ${shore_pump_capex/1e6:>8.3f}M")
        print(f"  Total CAPEX:                           ${total_capex/1e6:>8.1f}M")
        print()
        print("OPEX (Annual):")
        print(f"  - Fixed (Maintenance):                 ${total_fixed_opex/1e6:>8.1f}M/year")
        print(f"  - Variable (Fuel + Energy):            ${total_variable_opex/1e6:>8.1f}M/year")
        if shuttle_fuel_annual > 0 or pump_fuel_annual > 0 or tank_variable_opex > 0:
            print(f"      * Shuttle Fuel Cost:              ${shuttle_fuel_annual/1e6:>8.3f}M/year")
            print(f"      * Pump Energy Cost:               ${pump_fuel_annual/1e6:>8.3f}M/year")
            if tank_variable_opex > 0:
                print(f"      * Tank Cooling Cost:              ${tank_variable_opex/1e6:>8.3f}M/year")
        print(f"  Total OPEX:                            ${total_opex/1e6:>8.1f}M/year")
        print()
        print(f"First Year Total:                        ${first_year_cost/1e6:>8.1f}M")
        print("-" * 60)

        # Export to CSV
        export_config = config.get("execution", {}).get("export", {})
        if export_config.get("csv", True):
            # Calculate max annual cycles for one shuttle
            annual_cycles_max = max_annual_hours / cycle_duration if cycle_duration > 0 else 0

            result_data = {
                "Parameter": [
                    "Case", "Case_ID", "Simulation_Year", "Shuttle_Size_cbm", "Pump_Size_m3ph",
                    "",
                    "=== SINGLE ROUND-TRIP BREAKDOWN ===",
                    "Shore_Loading_Hours",
                    "Travel_Outbound_Hours",
                    "Port_Entry_Hours",
                    "Setup_Inbound_Hours",
                    "Pumping_Per_Vessel_Hours",
                    "Setup_Outbound_Hours",
                    "Travel_Return_Hours",
                    "Port_Exit_Hours",
                    "Total_Cycle_Duration_Hours",
                    "Annual_Cycles_Max_Per_Shuttle",
                    "",
                    "=== ANNUAL OPERATION PARAMETERS ===",
                    "Vessels_in_Year",
                    "Annual_Demand_m3",
                    "Bunker_per_Call_m3",
                    "Required_Annual_Calls",
                    "",
                    "=== FLEET REQUIREMENTS ===",
                    "Annual_Bunkering_Calls",
                    "Trips_Per_Call_or_Vessels_Per_Trip",
                    "Total_Shuttle_Trips",
                    "Total_Hours_Needed",
                    "Annual_Hours_Max_Per_Shuttle",
                    "Required_Shuttles",
                    "Available_Hours_Total",
                    "Utilization_Rate",
                    "Annual_Cycles_Per_Shuttle",
                    "",
                    "=== COST BREAKDOWN ===",
                    "CAPEX_Shuttle_USDm",
                    "CAPEX_Bunkering_USDm",
                    "CAPEX_Tank_USDm",
                    "CAPEX_Total_USDm",
                    "",
                    "OPEX_Fixed_USDm",
                    "OPEX_Variable_USDm",
                    "OPEX_Total_USDm",
                    "",
                    "First_Year_Cost_USDm"
                ],
                "Value": [
                    config.get('case_name', 'Unknown'), case_id, simulation_year, shuttle_size_cbm, pump_size_m3ph,
                    "",
                    "",
                    cycle_info['shore_loading'],
                    cycle_info['travel_outbound'],
                    cycle_info.get('port_entry', 0),
                    cycle_info['setup_inbound'],
                    cycle_info['pumping_per_vessel'],
                    cycle_info['setup_outbound'],
                    cycle_info['travel_return'],
                    cycle_info.get('port_exit', 0),
                    cycle_duration,
                    annual_cycles_max,
                    "",
                    "",
                    vessels_in_year,
                    demand_m3,
                    bunker_volume,
                    annual_calls,
                    "",
                    "",
                    annual_calls,
                    trips_per_call if has_storage_at_busan else num_vessels,
                    total_trips,
                    total_hours_needed,
                    max_annual_hours,
                    required_shuttles,
                    available_hours,
                    utilization,
                    cycles_per_shuttle,
                    "",
                    "",
                    total_shuttle_capex/1e6,
                    total_bunkering_capex/1e6,
                    tank_capex/1e6,
                    total_capex/1e6,
                    "",
                    total_fixed_opex/1e6,
                    total_variable_opex/1e6,
                    total_opex/1e6,
                    "",
                    first_year_cost/1e6
                ],
                "Unit": [
                    "", "", "", "m³", "m³/h",
                    "",
                    "",
                    "hours",
                    "hours",
                    "hours",
                    "hours",
                    "hours",
                    "hours",
                    "hours",
                    "hours",
                    "hours",
                    "cycles",
                    "",
                    "",
                    "vessels",
                    "m³",
                    "m³",
                    "calls",
                    "",
                    "",
                    "calls",
                    "trips/call or vessels/trip",
                    "trips",
                    "hours",
                    "hours/vessel",
                    "vessels",
                    "hours",
                    "%",
                    "trips",
                    "",
                    "",
                    "$M",
                    "$M",
                    "$M",
                    "$M",
                    "",
                    "$M/year",
                    "$M/year",
                    "$M/year",
                    "",
                    "$M"
                ]
            }

            result_df = pd.DataFrame(result_data)
            result_file = output_path / f"annual_simulation_{case_id}_{simulation_year}_{shuttle_size_cbm}_{pump_size_m3ph}.csv"
            result_df.to_csv(result_file, index=False, encoding="utf-8-sig")
            print(f"\n[OK] Results saved to: {result_file}")

        return {
            'year': simulation_year,
            'shuttle_size': shuttle_size_cbm,
            'pump_size': pump_size_m3ph,
            'demand_m3': demand_m3,
            'annual_calls': annual_calls,
            'required_shuttles': required_shuttles,
            'utilization': utilization,
            'cycle_time': cycle_duration,
            'total_capex': total_capex,
            'total_opex': total_opex,
            'first_year_cost': first_year_cost
        }

    except Exception as e:
        print(f"Error during annual simulation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def run_yearly_simulation(config, shuttle_size_cbm, pump_size_m3ph, output_path):
    """
    Run a 20-year simulation for a specific shuttle/pump combination.
    """
    try:
        print("\n" + "="*60)
        print("Yearly Simulation Mode (20-year period)")
        print("="*60)
        case_id = config.get("case_id", "unknown")
        print(f"Case: {config.get('case_name', 'Unknown')}")
        print(f"Case ID: {case_id}")
        print(f"Shuttle: {shuttle_size_cbm} m³")
        print(f"Pump: {pump_size_m3ph} m³/h")
        print("="*60)

        # Initialize calculators
        cycle_calculator = CycleTimeCalculator(case_id, config)
        cost_calculator = CostCalculator(config)
        fleet_calc = FleetSizingCalculator(config)

        # Get config parameters
        start_year = config["time_period"]["start_year"]
        end_year = config["time_period"]["end_year"]
        years = range(start_year, end_year + 1)
        discount_rate = config["economy"]["discount_rate"]
        max_annual_hours = config["operations"]["max_annual_hours_per_vessel"]

        start_vessels = config["shipping"]["start_vessels"]
        end_vessels = config["shipping"]["end_vessels"]
        voyages_per_year = config["shipping"]["voyages_per_year"]
        bunker_volume = config["bunkering"]["bunker_volume_per_call_m3"]
        has_storage_at_busan = config["operations"].get("has_storage_at_busan", True)
        shore_supply_enabled = config.get("shore_supply", {}).get("enabled", False)

        # Calculate demand for all years
        vessel_growth = calculate_vessel_growth(start_year, end_year, start_vessels, end_vessels)
        annual_demand_dict = calculate_annual_demand(vessel_growth, bunker_volume, voyages_per_year)

        # Calculate cycle time once
        if has_storage_at_busan:
            num_vessels_per_trip = 1
        else:
            num_vessels_per_trip = max(1, int(shuttle_size_cbm // bunker_volume))
        
        cycle_info = cycle_calculator.calculate_single_cycle(
            shuttle_size_m3=shuttle_size_cbm,
            pump_size_m3ph=pump_size_m3ph,
            num_vessels=num_vessels_per_trip
        )
        cycle_duration = cycle_info['cycle_duration']
        trips_per_call = cycle_info.get('trips_per_call', 1)

        # Pre-calculate cost components
        shuttle_capex = cost_calculator.calculate_shuttle_capex(shuttle_size_cbm)
        bunk_capex = cost_calculator.calculate_bunkering_capex(shuttle_size_cbm, pump_size_m3ph) # pump is part of bunkering equipment
        shuttle_fixed_opex = cost_calculator.calculate_shuttle_fixed_opex(shuttle_size_cbm)
        bunk_fixed_opex = cost_calculator.calculate_bunkering_fixed_opex(shuttle_size_cbm, pump_size_m3ph)

        tank_capex = cost_calculator.calculate_tank_capex() if config["tank_storage"]["enabled"] and shore_supply_enabled else 0
        tank_fixed_opex = cost_calculator.calculate_tank_fixed_opex() if config["tank_storage"]["enabled"] and shore_supply_enabled else 0
        tank_variable_opex = cost_calculator.calculate_tank_variable_opex() if config["tank_storage"]["enabled"] and shore_supply_enabled else 0

        mcr = config["shuttle"]["mcr_map_kw"].get(int(shuttle_size_cbm), 0)
        sfoc = config["propulsion"]["sfoc_g_per_kwh"]
        fuel_price = config["economy"]["fuel_price_usd_per_ton"]
        travel_time_hours = config["operations"]["travel_time_hours"]
        travel_factor = 1.0 if has_storage_at_busan else 2.0
        shuttle_fuel_per_cycle = (mcr * sfoc * travel_factor * travel_time_hours) / 1e6
        shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * fuel_price

        pump_power = cost_calculator.calculate_pump_power(pump_size_m3ph)
        pumping_time_hr_call = bunker_volume / pump_size_m3ph
        pump_fuel_per_event = (pump_power * pumping_time_hr_call * sfoc) / 1e6
        pump_fuel_cost_per_event = pump_fuel_per_event * fuel_price

        yearly_results = []
        total_shuttles = 0
        
        tank_purchased = False

        for year in years:
            demand_m3 = annual_demand_dict[year]
            annual_calls = demand_m3 / bunker_volume if bunker_volume > 0 else 0

            required_shuttles = fleet_calc.calculate_required_shuttles_working_time_only(
                annual_calls, trips_per_call, cycle_duration
            )
            
            new_shuttles = max(0, required_shuttles - total_shuttles)
            total_shuttles = required_shuttles

            new_tank = 0
            if config["tank_storage"]["enabled"] and shore_supply_enabled and not tank_purchased and new_shuttles > 0:
                new_tank = 1
                tank_purchased = True
            
            disc_factor = 1.0 / ((1.0 + discount_rate) ** (year - start_year))

            capex_shuttle_usd = disc_factor * shuttle_capex * new_shuttles
            capex_pump_usd = disc_factor * bunk_capex * new_shuttles
            capex_tank_usd = disc_factor * tank_capex * new_tank
            capex_total_usd = capex_shuttle_usd + capex_pump_usd + capex_tank_usd
            
            fopex_shuttle_usd = disc_factor * shuttle_fixed_opex * total_shuttles
            fopex_pump_usd = disc_factor * bunk_fixed_opex * total_shuttles
            fopex_tank_usd = disc_factor * tank_fixed_opex if tank_purchased else 0
            fopex_total_usd = fopex_shuttle_usd + fopex_pump_usd + fopex_tank_usd

            if has_storage_at_busan:
                total_trips = annual_calls * trips_per_call
            else:
                vessels_per_trip = num_vessels_per_trip if num_vessels_per_trip > 0 else 1
                total_trips = ceil(annual_calls / vessels_per_trip)

            vopex_shuttle_usd = disc_factor * shuttle_fuel_cost_per_cycle * total_trips
            vopex_pump_usd = disc_factor * pump_fuel_cost_per_event * annual_calls
            vopex_tank_usd = disc_factor * tank_variable_opex if tank_purchased else 0
            vopex_total_usd = vopex_shuttle_usd + vopex_pump_usd + vopex_tank_usd

            total_year_cost_usd = capex_total_usd + fopex_total_usd + vopex_total_usd
            
            total_shuttle_asset_usd = total_shuttles * shuttle_capex
            total_pump_asset_usd = total_shuttles * bunk_capex
            total_tank_asset_usd = tank_capex if tank_purchased else 0
            
            annualized_shuttle_capex_usd = cost_calculator.calculate_annualized_capex_yearly(total_shuttle_asset_usd)
            annualized_pump_capex_usd = cost_calculator.calculate_annualized_capex_yearly(total_pump_asset_usd)
            annualized_tank_capex_usd = cost_calculator.calculate_annualized_capex_yearly(total_tank_asset_usd)
            annualized_total_capex_usd = annualized_shuttle_capex_usd + annualized_pump_capex_usd + annualized_tank_capex_usd

            supply_m3 = annual_calls * bunker_volume
            cycles_available = total_shuttles * (max_annual_hours / cycle_duration) if cycle_duration > 0 else 0
            utilization_rate = (total_trips / cycles_available) if cycles_available > 0 else 0

            yearly_results.append({
                # Identification
                "Shuttle_Size_cbm": int(shuttle_size_cbm), "Pump_Size_m3ph": int(pump_size_m3ph), "Year": year,
                # Assets
                "New_Shuttles": new_shuttles, "Total_Shuttles": total_shuttles,
                # Operations
                "Annual_Calls": annual_calls, "Annual_Cycles": total_trips, "Supply_m3": supply_m3, "Demand_m3": demand_m3,
                "Cycles_Available": cycles_available, "Utilization_Rate": utilization_rate,
                # ===== COSTS (MILLIONS USD, DISCOUNTED) =====
                "CAPEX_Shuttle_USDm": capex_shuttle_usd / 1e6, "CAPEX_Pump_USDm": capex_pump_usd / 1e6,
                "CAPEX_Tank_USDm": capex_tank_usd / 1e6, "CAPEX_Total_USDm": capex_total_usd / 1e6,
                "FixedOPEX_Shuttle_USDm": fopex_shuttle_usd / 1e6, "FixedOPEX_Pump_USDm": fopex_pump_usd / 1e6,
                "FixedOPEX_Tank_USDm": fopex_tank_usd / 1e6, "FixedOPEX_Total_USDm": fopex_total_usd / 1e6,
                "VariableOPEX_Shuttle_USDm": vopex_shuttle_usd / 1e6, "VariableOPEX_Pump_USDm": vopex_pump_usd / 1e6,
                "VariableOPEX_Tank_USDm": vopex_tank_usd / 1e6, "VariableOPEX_Total_USDm": vopex_total_usd / 1e6,
                "Total_Year_Cost_Discounted_USDm": total_year_cost_usd / 1e6, "Discount_Factor": disc_factor,
                # ===== ANNUALIZED CAPEX (for year-by-year comparison) =====
                "Annualized_CAPEX_Shuttle_USDm": annualized_shuttle_capex_usd / 1e6,
                "Annualized_CAPEX_Pump_USDm": annualized_pump_capex_usd / 1e6,
                "Annualized_CAPEX_Tank_USDm": annualized_tank_capex_usd / 1e6,
                "Annualized_CAPEX_Total_USDm": annualized_total_capex_usd / 1e6,
            })

        result_df = pd.DataFrame(yearly_results)
        
        timestamp = int(time.time())
        output_filename = f"yearly_simulation_{case_id}_{int(shuttle_size_cbm)}_{int(pump_size_m3ph)}_{timestamp}.csv"
        output_file = output_path / output_filename
        result_df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"\n[OK] Yearly simulation results saved to: {output_file}")
        
        # Print a summary to the console
        print("\n" + "="*80)
        print("Yearly Simulation Summary")
        print("="*80)
        print(result_df[[ "Year", "New_Shuttles", "Total_Shuttles", "Demand_m3", 
                    "CAPEX_Total_USDm", "FixedOPEX_Total_USDm", "VariableOPEX_Total_USDm"
        ]].to_string(index=False))
        print("="*80)

        return result_df

    except Exception as e:
        print(f"Error during yearly simulation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def run_single_case(config, output_path):
    """
    Run optimization for a single case.

    Args:
        config: Configuration dictionary
        output_path: Output directory path

    Returns:
        Tuple of (scenario_df, yearly_df) or (None, None) if failed
    """
    try:
        print("\n" + "="*60)
        print(f"Case: {config.get('case_name', 'Unknown')}")
        print(f"Case ID: {config.get('case_id', 'unknown')}")
        print("="*60)

        # Run optimization
        optimizer = BunkeringOptimizer(config)
        scenario_df, yearly_df = optimizer.solve()

        if scenario_df.empty:
            print("No feasible solutions found for this case.")
            return None, None

        # Determine export formats
        export_config = config.get("execution", {}).get("export", {})
        case_id = config.get("case_id", "unknown")

        # CSV export (default)
        if export_config.get("csv", True):
            scenario_file = output_path / f"MILP_scenario_summary_{case_id}.csv"
            scenario_df.to_csv(scenario_file, index=False, encoding="utf-8-sig")
            print(f"[OK] CSV scenario summary: {scenario_file}")

            yearly_file = output_path / f"MILP_per_year_results_{case_id}.csv"
            yearly_df.to_csv(yearly_file, index=False, encoding="utf-8-sig")
            print(f"[OK] CSV yearly results: {yearly_file}")

        # Excel export
        if export_config.get("excel", False):
            try:
                exporter = ExcelExporter(config)
                excel_file = exporter.export_results(scenario_df, yearly_df, output_path)
                print(f"[OK] Excel export: {excel_file}")
            except ImportError:
                print("[WARN] Excel export requested but openpyxl not installed (pip install openpyxl)")

        # Word export
        if export_config.get("docx", False):
            try:
                exporter = WordExporter(config)
                docx_file = exporter.export_report(scenario_df, yearly_df, output_path)
                print(f"[OK] Word export: {docx_file}")
            except ImportError:
                print("[WARN] Word export requested but python-docx not installed (pip install python-docx)")

        # Print top 10 scenarios
        print("\n" + "="*60)
        print("Top 10 Scenarios (by NPC)")
        print("="*60)
        top10 = scenario_df.nsmallest(10, "NPC_Total_USDm")
        print(top10[[ "Shuttle_Size_cbm", "Pump_Size_m3ph", "NPC_Total_USDm",
                    "NPC_Shuttle_CAPEX_USDm", "NPC_Bunkering_CAPEX_USDm"]].to_string(index=False))

        return scenario_df, yearly_df

    except Exception as e:
        print(f"Error during optimization: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None, None


def main():
    """Main entry point - read config and execute."""
    try:
        # Load base configuration (which includes execution settings)
        config = load_config("case_1")  # Load case_1 first to get base settings

        # Get execution settings
        execution_config = config.get("execution", {})
        run_mode = execution_config.get("run_mode", "single").lower()
        single_case = execution_config.get("single_case", "case_1")
        output_dir = execution_config.get("output_directory", "results")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print("="*60)
        print("Green Corridor MILP Optimization")
        print("="*60)
        print(f"Run Mode: {run_mode}")
        print(f"Output Directory: {output_dir}")

        if run_mode == "single":
            # Single case mode - run ONE case specified in 'single_case'
            print(f"Running single case: {single_case}")
            config = load_config(single_case)
            run_single_case(config, output_path)

        elif run_mode == "all":
            # All cases mode - run ALL available cases automatically
            from src import list_available_cases
            available_cases = list_available_cases()
            print(f"Running all {len(available_cases)} cases...")
            for case in available_cases:
                config = load_config(case)
                run_single_case(config, output_path)

        elif run_mode == "multiple":
            # Multiple specific cases - run cases listed in 'multi_cases'
            multi_cases = execution_config.get("multi_cases", [single_case])
            print(f"Running {len(multi_cases)} specific cases...")
            for case in multi_cases:
                try:
                    config = load_config(case)
                    run_single_case(config, output_path)
                except Exception as e:
                    print(f"Failed to run case {case}: {e}", file=sys.stderr)

        elif run_mode == "single_scenario":
            # Single scenario mode - calculate time for ONE specific shuttle/pump combination
            # NO optimization, just quick time calculation
            shuttle_size = execution_config.get("single_scenario_shuttle_cbm")
            pump_size = execution_config.get("single_scenario_pump_m3ph")

            if shuttle_size is None or pump_size is None:
                print("[ERROR] single_scenario mode requires both:", file=sys.stderr)
                print("  - single_scenario_shuttle_cbm: Shuttle size in m³", file=sys.stderr)
                print("  - single_scenario_pump_m3ph: Pump flow rate in m³/h", file=sys.stderr)
                return 1

            print(f"Running single scenario: {single_case}")
            print(f"  Shuttle: {shuttle_size}m³")
            print(f"  Pump: {pump_size}m³/h")

            try:
                config = load_config(single_case)
                run_single_scenario(config, shuttle_size, pump_size, output_path)
            except Exception as e:
                print(f"Failed to run single scenario: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                return 1

        elif run_mode == "annual_simulation":
            # Annual simulation mode - simulate ONE specific year with ONE shuttle/pump combination
            # NO optimization, calculates required shuttles, operations, and costs for one year
            shuttle_size = execution_config.get("single_scenario_shuttle_cbm")
            pump_size = execution_config.get("single_scenario_pump_m3ph")
            simulation_year = execution_config.get("simulation_year", 2030)

            if shuttle_size is None or pump_size is None:
                print("[ERROR] annual_simulation mode requires:", file=sys.stderr)
                print("  - single_scenario_shuttle_cbm: Shuttle size in m³", file=sys.stderr)
                print("  - single_scenario_pump_m3ph: Pump flow rate in m³/h", file=sys.stderr)
                print("  - simulation_year: Year to simulate (e.g., 2030, 2050)", file=sys.stderr)
                return 1

            print(f"Running annual simulation: {single_case}")
            print(f"  Shuttle: {shuttle_size}m³")
            print(f"  Pump: {pump_size}m³/h")
            print(f"  Year: {simulation_year}")

            try:
                config = load_config(single_case)
                run_annual_simulation(config, shuttle_size, pump_size, simulation_year, output_path)
            except Exception as e:
                print(f"Failed to run annual simulation: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                return 1

        elif run_mode == "yearly_simulation":
            # Yearly simulation mode - simulate 20 years for ONE specific shuttle/pump combination
            shuttle_size = execution_config.get("single_scenario_shuttle_cbm")
            pump_size = execution_config.get("single_scenario_pump_m3ph")

            if shuttle_size is None or pump_size is None:
                print("[ERROR] yearly_simulation mode requires:", file=sys.stderr)
                print("  - single_scenario_shuttle_cbm: Shuttle size in m³", file=sys.stderr)
                print("  - single_scenario_pump_m3ph: Pump flow rate in m³/h", file=sys.stderr)
                return 1
            
            print(f"Running yearly simulation: {single_case}")
            print(f"  Shuttle: {shuttle_size}m³")
            print(f"  Pump: {pump_size}m³/h")

            try:
                config = load_config(single_case)
                run_yearly_simulation(config, shuttle_size, pump_size, output_path)
            except Exception as e:
                print(f"Failed to run yearly simulation: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                return 1

        else:
            print(f"Unknown run_mode: {run_mode}", file=sys.stderr)
            print("Valid modes: single, single_scenario, annual_simulation, yearly_simulation, all, multiple")
            return 1

        print("\n" + "="*60)
        print("Optimization Complete")
        print("="*60)
        return 0

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
