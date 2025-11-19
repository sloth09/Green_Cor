#!/usr/bin/env python3
"""
Main entry point for bunkering optimization model.

All configuration is controlled through YAML config files.
No command-line arguments needed - everything is set in config/base.yaml

Edit config/base.yaml execution section to control:
  - Run mode: "single" (full optimization), "single_scenario" (quick time calc),
             "all" (all cases), or "multiple" (selected cases)
  - Which case to run
  - Single vs multiple case execution
  - Output directory
  - Export formats
  - (For single_scenario) Specific shuttle/pump combination

For single_scenario mode, also set:
  - single_scenario_shuttle_cbm: Shuttle size in m³
  - single_scenario_pump_m3ph: Pump flow rate in m³/h
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import load_config, BunkeringOptimizer
from src.export_excel import ExcelExporter
from src.export_docx import WordExporter
from src.cycle_time_calculator import CycleTimeCalculator


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

        # Calculate cycle time
        cycle_info = calculator.calculate_single_cycle(
            shuttle_size_m3=shuttle_size_cbm,
            pump_size_m3ph=pump_size_m3ph,
            num_vessels=1
        )

        # Display time breakdown
        print("\n【1회 왕복 운항 시간 분석】")
        print("-" * 60)
        print(f"육상 적재:          {cycle_info['shore_loading']:.2f}h")
        print(f"편도 항해:          {cycle_info['travel_outbound']:.2f}h")
        print(f"호스 연결:          {cycle_info['setup_inbound']:.2f}h")
        print(f"펌핑:               {cycle_info['pumping_per_vessel']:.2f}h")
        print(f"호스 분리:          {cycle_info['setup_outbound']:.2f}h")
        print(f"복귀 항해:          {cycle_info['travel_return']:.2f}h")
        print(f"이동:               {cycle_info['movement_per_vessel']:.2f}h")
        print("-" * 60)
        print(f"기본 사이클 (육상 제외): {cycle_info['basic_cycle_duration']:.2f}h")
        print(f"총 사이클 (육상 포함):   {cycle_info['cycle_duration']:.2f}h")
        print("="*60)

        # Operating metrics
        annual_cycles = calculator.get_annual_operations_per_shuttle(cycle_info['cycle_duration'])
        annual_supply_m3 = annual_cycles * shuttle_size_cbm
        time_utilization = (annual_cycles * cycle_info['cycle_duration'] / 8000.0) * 100

        print("\n【연간 운영 지표】")
        print("-" * 60)
        print(f"연간 최대 항차:     {annual_cycles:.0f}회")
        print(f"연간 공급 용량:     {annual_supply_m3:,.0f}m³")
        print(f"시간 활용도:        {time_utilization:.1f}%")
        print(f"선박당 일정:        {365.0 / annual_cycles if annual_cycles > 0 else 0:.1f}일/회")
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
                "Movement_Per_Vessel_hr": [cycle_info['movement_per_vessel']],
                "Pumping_Per_Vessel_hr": [cycle_info['pumping_per_vessel']],
                "Pumping_Total_hr": [cycle_info['pumping_total']],
                "Basic_Cycle_Duration_hr": [cycle_info['basic_cycle_duration']],
                "Annual_Cycles_Max": [annual_cycles],
                "Annual_Supply_m3": [annual_supply_m3],
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
        print(top10[["Shuttle_Size_cbm", "Pump_Size_m3ph", "NPC_Total_USDm",
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

        else:
            print(f"Unknown run_mode: {run_mode}", file=sys.stderr)
            print("Valid modes: single, single_scenario, all, multiple")
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
