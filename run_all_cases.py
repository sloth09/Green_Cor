#!/usr/bin/env python3
"""
Multi-case parallel execution helper.

Configuration is read from config/base.yaml execution settings:
  - run_mode: "multiple" or "all"
  - multi_cases: list of cases (for "multiple" mode)
  - num_jobs: number of parallel workers
  - output_directory: output location

Usage:
    python run_all_cases.py

This script is optional - main.py can handle all modes.
Use this for better parallel execution of multiple cases.
"""

import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from src import load_config, list_available_cases, BunkeringOptimizer


def run_single_case(case_name: str, config: dict, output_dir: str) -> dict:
    """
    Run optimization for a single case.

    Args:
        case_name: Case identifier
        config: Configuration dictionary
        output_dir: Output directory

    Returns:
        Dictionary with results and status
    """
    try:
        print(f"[{case_name}] Starting optimization...")
        optimizer = BunkeringOptimizer(config)
        scenario_df, yearly_df = optimizer.solve()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if not scenario_df.empty:
            scenario_file = output_path / f"MILP_scenario_summary_{case_name}.csv"
            scenario_df.to_csv(scenario_file, index=False, encoding="utf-8-sig")

            yearly_file = output_path / f"MILP_per_year_results_{case_name}.csv"
            yearly_df.to_csv(yearly_file, index=False, encoding="utf-8-sig")

            best = scenario_df.nsmallest(1, "NPC_Total_USDm").iloc[0]

            return {
                "case_name": case_name,
                "status": "[OK] Success",
                "scenarios_found": len(scenario_df),
                "best_npc_usdm": round(best["NPC_Total_USDm"], 2),
                "best_shuttle_cbm": int(best["Shuttle_Size_cbm"]),
                "best_pump_m3ph": int(best["Pump_Size_m3ph"]),
            }
        else:
            return {
                "case_name": case_name,
                "status": "[WARN] No solutions",
                "scenarios_found": 0,
            }

    except Exception as e:
        return {
            "case_name": case_name,
            "status": f"[ERROR] {str(e)[:40]}",
            "scenarios_found": 0,
        }


def main():
    """Main entry point - read config and execute multiple cases."""
    try:
        print("="*60)
        print("Green Corridor Multi-Case Optimizer")
        print("="*60)

        # Load base config to get execution settings
        base_config = load_config("case_1")
        execution_config = base_config.get("execution", {})

        run_mode = execution_config.get("run_mode", "single").lower()
        output_dir = execution_config.get("output_directory", "results")
        num_jobs = execution_config.get("num_jobs", 1)

        print(f"\nExecution Mode: {run_mode}")
        print(f"Output Directory: {output_dir}")
        print(f"Parallel Jobs: {num_jobs}")

        # Determine which cases to run
        if run_mode == "all":
            cases_to_run = list_available_cases()
        elif run_mode == "multiple":
            cases_to_run = execution_config.get("multi_cases", ["case_1"])
        else:
            print(f"Invalid run_mode: {run_mode}")
            print("Use 'all' or 'multiple' in config/base.yaml")
            return 1

        print(f"\nCases to run ({len(cases_to_run)}):")
        for case in cases_to_run:
            print(f"  - {case}")

        print("\n" + "="*60)

        # Run cases
        results = []

        if num_jobs == 1:
            # Sequential execution
            print("Running cases sequentially...\n")
            for case in cases_to_run:
                config = load_config(case)
                result = run_single_case(case, config, output_dir)
                results.append(result)
                if "[OK]" in result["status"]:
                    print(f"[{case}] {result['status']} - {result.get('scenarios_found', 0)} scenarios")
                else:
                    print(f"[{case}] {result['status']}")

        else:
            # Parallel execution
            print(f"Running cases in parallel ({num_jobs} jobs)...\n")
            with ProcessPoolExecutor(max_workers=num_jobs) as executor:
                futures = {}
                for case in cases_to_run:
                    config = load_config(case)
                    future = executor.submit(run_single_case, case, config, output_dir)
                    futures[future] = case

                for future in as_completed(futures):
                    result = future.result()
                    results.append(result)
                    case = futures[future]
                    if "[OK]" in result["status"]:
                        print(f"[{case}] {result['status']} - {result.get('scenarios_found', 0)} scenarios")
                    else:
                        print(f"[{case}] {result['status']}")

        # Print summary
        print("\n" + "="*60)
        print("RESULTS SUMMARY")
        print("="*60)

        summary_df = pd.DataFrame(results)
        print("\n" + summary_df.to_string(index=False))

        # Save summary
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        summary_file = Path(output_dir) / "MILP_cases_summary.csv"
        summary_df.to_csv(summary_file, index=False, encoding="utf-8-sig")
        print(f"\nSummary saved: {summary_file}")

        # Statistics
        successful = len([r for r in results if "[OK]" in r["status"]])
        print(f"\nSuccessful cases: {successful}/{len(cases_to_run)}")

        print("="*60)
        return 0 if successful == len(cases_to_run) else 1

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
