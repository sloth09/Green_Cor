#!/usr/bin/env python3
"""
Main entry point for bunkering optimization model.

All configuration is controlled through YAML config files.
No command-line arguments needed - everything is set in config/base.yaml

Edit config/base.yaml execution section to control:
  - Which case to run
  - Single vs multiple case execution
  - Output directory
  - Export formats
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import load_config, BunkeringOptimizer
from src.export_excel import ExcelExporter
from src.export_docx import WordExporter


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

        else:
            print(f"Unknown run_mode: {run_mode}", file=sys.stderr)
            print("Valid modes: single, all, multiple")
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
