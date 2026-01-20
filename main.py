#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
  - single_scenario_shuttle_cbm: Shuttle size in m3
  - single_scenario_pump_m3ph: Pump flow rate in m3/h

For annual_simulation mode:
  - single_scenario_shuttle_cbm: Shuttle size in m3
  - single_scenario_pump_m3ph: Pump flow rate in m3/h
  - simulation_year: Year to simulate (e.g., 2030, 2050)

NOTE: Core execution logic is in src/runner.py.
      This file is a thin wrapper that calls those functions.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import (
    load_config,
    list_available_cases,
    # Runner functions from src/runner.py
    run_single_scenario,
    run_annual_simulation,
    run_yearly_simulation,
    run_single_case,
)


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
                print("  - single_scenario_shuttle_cbm: Shuttle size in m3", file=sys.stderr)
                print("  - single_scenario_pump_m3ph: Pump flow rate in m3/h", file=sys.stderr)
                return 1

            print(f"Running single scenario: {single_case}")
            print(f"  Shuttle: {shuttle_size}m3")
            print(f"  Pump: {pump_size}m3/h")

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
                print("  - single_scenario_shuttle_cbm: Shuttle size in m3", file=sys.stderr)
                print("  - single_scenario_pump_m3ph: Pump flow rate in m3/h", file=sys.stderr)
                print("  - simulation_year: Year to simulate (e.g., 2030, 2050)", file=sys.stderr)
                return 1

            print(f"Running annual simulation: {single_case}")
            print(f"  Shuttle: {shuttle_size}m3")
            print(f"  Pump: {pump_size}m3/h")
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
                print("  - single_scenario_shuttle_cbm: Shuttle size in m3", file=sys.stderr)
                print("  - single_scenario_pump_m3ph: Pump flow rate in m3/h", file=sys.stderr)
                return 1

            print(f"Running yearly simulation: {single_case}")
            print(f"  Shuttle: {shuttle_size}m3")
            print(f"  Pump: {pump_size}m3/h")

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
