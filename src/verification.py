#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification module - Tools for validating calculations and results.

This module provides utilities for verifying:
- Cycle time calculations
- Cost calculations (NPC breakdown)
- Constraint satisfaction
- LCO consistency between modes
- Cross-scenario consistency

Usage:
    from src.verification import CalculationVerifier
    verifier = CalculationVerifier(config)
    result = verifier.verify_cycle_time(shuttle_size=2500, pump_size=2000)
"""

import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

from .cycle_time_calculator import CycleTimeCalculator
from .cost_calculator import CostCalculator
from .fleet_sizing_calculator import FleetSizingCalculator
from .config_loader import load_config


@dataclass
class VerificationResult:
    """Result of a verification check."""
    passed: bool
    name: str
    expected: Any
    actual: Any
    tolerance: float
    difference: float
    message: str

    def __str__(self):
        status = "[PASS]" if self.passed else "[FAIL]"
        return f"{status} {self.name}: expected={self.expected}, actual={self.actual}, diff={self.difference:.4f}"


class CalculationVerifier:
    """
    Utility class for verifying calculations.

    Provides methods to validate:
    - Cycle time breakdown
    - NPC cost breakdown
    - Constraint satisfaction
    - LCO consistency

    Args:
        config: Configuration dictionary
    """

    # Standard tolerances
    TOLERANCE_TIME = 0.01       # 1% for time calculations
    TOLERANCE_COST = 0.005      # 0.5% for cost calculations
    TOLERANCE_LCO = 0.02        # 2% for LCO (more variable)

    def __init__(self, config: Dict):
        self.config = config
        self.case_id = config.get("case_id", "unknown")

    def verify_cycle_time(
        self,
        shuttle_size: float,
        pump_size: float,
        expected_results: Optional[Dict] = None,
        tolerance: float = None
    ) -> VerificationResult:
        """
        Verify cycle time calculation against expected values or manual calculation.

        Args:
            shuttle_size: Shuttle size in m3
            pump_size: Pump flow rate in m3/h
            expected_results: Optional dict with expected values
            tolerance: Optional custom tolerance (default: 1%)

        Returns:
            VerificationResult with pass/fail status
        """
        if tolerance is None:
            tolerance = self.TOLERANCE_TIME

        calculator = CycleTimeCalculator(self.case_id, self.config)

        # Get bunker volume for num_vessels calculation
        bunker_volume = self.config["bunkering"]["bunker_volume_per_call_m3"]
        has_storage = self.config["operations"].get("has_storage_at_busan", True)

        if has_storage:
            num_vessels = 1
        else:
            num_vessels = max(1, int(shuttle_size // bunker_volume))

        actual = calculator.calculate_single_cycle(
            shuttle_size_m3=shuttle_size,
            pump_size_m3ph=pump_size,
            num_vessels=num_vessels
        )

        # If no expected values provided, calculate manually
        if expected_results is None:
            expected_results = self._calculate_expected_cycle_time(
                shuttle_size, pump_size, bunker_volume, has_storage
            )

        # Compare cycle duration
        expected_duration = expected_results.get('cycle_duration', 0)
        actual_duration = actual['cycle_duration']
        diff = abs(expected_duration - actual_duration)
        rel_diff = diff / expected_duration if expected_duration > 0 else 0

        passed = rel_diff <= tolerance

        return VerificationResult(
            passed=passed,
            name=f"Cycle Time (Shuttle={shuttle_size}, Pump={pump_size})",
            expected=expected_duration,
            actual=actual_duration,
            tolerance=tolerance,
            difference=rel_diff,
            message=f"Cycle time {'matches' if passed else 'differs from'} expected"
        )

    def _calculate_expected_cycle_time(
        self,
        shuttle_size: float,
        pump_size: float,
        bunker_volume: float,
        has_storage: bool
    ) -> Dict:
        """Calculate expected cycle time manually for verification."""
        # Get config values
        travel_time = self.config["operations"]["travel_time_hours"]
        setup_time = self.config["operations"]["setup_time_hours"]
        shore_pump_rate = self.config.get("shore_supply", {}).get("pump_rate_m3ph", 700.0)

        # Shore loading time
        shore_loading = shuttle_size / shore_pump_rate

        # Setup times: direct per-endpoint value, no multiplier
        setup_inbound = setup_time   # Direct per-endpoint setup time
        setup_outbound = setup_time  # Direct per-endpoint setup time

        if has_storage:
            # Case 1: pumping based on shuttle size
            pumping_per_vessel = shuttle_size / pump_size
            # travel_outbound + setup_inbound + pumping + setup_outbound + travel_return
            basic_cycle = (travel_time + setup_inbound + pumping_per_vessel + setup_outbound + travel_time)
        else:
            # Case 2: pumping based on bunker volume
            pumping_per_vessel = bunker_volume / pump_size
            num_vessels = max(1, int(shuttle_size // bunker_volume))
            # travel_outbound + (per vessel: setup + pumping + setup) + travel_return
            basic_cycle = (travel_time * 2 + num_vessels * (setup_inbound + pumping_per_vessel + setup_outbound))

        cycle_duration = shore_loading + basic_cycle

        return {
            'cycle_duration': cycle_duration,
            'shore_loading': shore_loading,
            'basic_cycle_duration': basic_cycle
        }

    def verify_npc_breakdown(
        self,
        result_row: Dict,
        tolerance: float = None
    ) -> VerificationResult:
        """
        Verify NPC = CAPEX + OPEX breakdown.

        Args:
            result_row: Dictionary with NPC components
            tolerance: Optional custom tolerance (default: 0.5%)

        Returns:
            VerificationResult with pass/fail status
        """
        if tolerance is None:
            tolerance = self.TOLERANCE_COST

        # Extract components
        capex_total = result_row.get('NPC_Annualized_CAPEX_Total_USDm', 0)
        opex_total = result_row.get('NPC_Total_OPEX_USDm', 0)
        npc_total = result_row.get('NPC_Total_USDm', 0)

        expected = capex_total + opex_total
        diff = abs(npc_total - expected)
        rel_diff = diff / npc_total if npc_total > 0 else 0

        passed = rel_diff <= tolerance

        return VerificationResult(
            passed=passed,
            name="NPC Breakdown",
            expected=expected,
            actual=npc_total,
            tolerance=tolerance,
            difference=rel_diff,
            message=f"NPC total {'matches' if passed else 'differs from'} sum of components"
        )

    def verify_constraint_satisfaction(
        self,
        yearly_df: pd.DataFrame,
        shuttle_size: float,
        pump_size: float
    ) -> List[VerificationResult]:
        """
        Verify all constraints are satisfied in optimization result.

        Constraints checked:
        - Demand satisfaction (supply >= demand)
        - Working hours (hours_used <= max_hours)
        - Utilization (0 < utilization <= 1)

        Args:
            yearly_df: DataFrame with yearly results
            shuttle_size: Shuttle size to filter
            pump_size: Pump size to filter

        Returns:
            List of VerificationResults
        """
        results = []
        max_hours = self.config["operations"]["max_annual_hours_per_vessel"]

        # Filter to specific scenario
        mask = (yearly_df['Shuttle_Size_cbm'] == shuttle_size) & \
               (yearly_df['Pump_Size_m3ph'] == pump_size)
        scenario_df = yearly_df[mask]

        if scenario_df.empty:
            return [VerificationResult(
                passed=False,
                name="Scenario exists",
                expected="Found",
                actual="Not found",
                tolerance=0,
                difference=1,
                message=f"No data for Shuttle={shuttle_size}, Pump={pump_size}"
            )]

        # Check 1: Demand satisfaction
        supply_shortage = scenario_df[scenario_df['Supply_m3'] < scenario_df['Demand_m3']]
        passed_demand = supply_shortage.empty

        results.append(VerificationResult(
            passed=passed_demand,
            name="Demand Satisfaction",
            expected="Supply >= Demand all years",
            actual=f"{len(supply_shortage)} years with shortage" if not passed_demand else "All satisfied",
            tolerance=0,
            difference=len(supply_shortage) / len(scenario_df) if not passed_demand else 0,
            message="Demand constraint satisfied" if passed_demand else f"Shortage in years: {supply_shortage['Year'].tolist()}"
        ))

        # Check 2: Working hours
        if 'Total_Hours_Needed' in scenario_df.columns and 'Total_Shuttles' in scenario_df.columns:
            scenario_df = scenario_df.copy()
            scenario_df['Max_Available_Hours'] = scenario_df['Total_Shuttles'] * max_hours
            hours_violation = scenario_df[scenario_df['Total_Hours_Needed'] > scenario_df['Max_Available_Hours']]
            passed_hours = hours_violation.empty

            results.append(VerificationResult(
                passed=passed_hours,
                name="Working Hours Constraint",
                expected=f"Hours <= {max_hours} * shuttles",
                actual=f"{len(hours_violation)} violations" if not passed_hours else "All within limits",
                tolerance=0,
                difference=len(hours_violation) / len(scenario_df) if not passed_hours else 0,
                message="Hours constraint satisfied" if passed_hours else f"Violation in years: {hours_violation['Year'].tolist()}"
            ))

        # Check 3: Utilization range
        if 'Utilization_Rate' in scenario_df.columns:
            invalid_util = scenario_df[(scenario_df['Utilization_Rate'] <= 0) |
                                       (scenario_df['Utilization_Rate'] > 1.0)]
            passed_util = invalid_util.empty

            results.append(VerificationResult(
                passed=passed_util,
                name="Utilization Range",
                expected="0 < utilization <= 1",
                actual=f"{len(invalid_util)} invalid" if not passed_util else "All valid",
                tolerance=0,
                difference=len(invalid_util) / len(scenario_df) if not passed_util else 0,
                message="Utilization in valid range" if passed_util else f"Invalid in years: {invalid_util['Year'].tolist()}"
            ))

        return results

    def verify_lco_consistency(
        self,
        single_mode_lco: float,
        yearly_sim_lco: float,
        tolerance: float = None
    ) -> VerificationResult:
        """
        Verify LCO consistency between single mode and yearly simulation.

        Args:
            single_mode_lco: LCO from optimization (single mode)
            yearly_sim_lco: LCO from yearly simulation
            tolerance: Optional custom tolerance (default: 2%)

        Returns:
            VerificationResult with pass/fail status
        """
        if tolerance is None:
            tolerance = self.TOLERANCE_LCO

        diff = abs(single_mode_lco - yearly_sim_lco)
        rel_diff = diff / single_mode_lco if single_mode_lco > 0 else 0

        passed = rel_diff <= tolerance

        return VerificationResult(
            passed=passed,
            name="LCO Consistency",
            expected=single_mode_lco,
            actual=yearly_sim_lco,
            tolerance=tolerance,
            difference=rel_diff,
            message=f"LCO {'consistent' if passed else 'inconsistent'} between modes"
        )

    def run_all_verifications(
        self,
        shuttle_size: float,
        pump_size: float,
        scenario_df: Optional[pd.DataFrame] = None,
        yearly_df: Optional[pd.DataFrame] = None,
        verbose: bool = True
    ) -> Tuple[bool, List[VerificationResult]]:
        """
        Run all verification checks for a given scenario.

        Args:
            shuttle_size: Shuttle size in m3
            pump_size: Pump flow rate in m3/h
            scenario_df: Optional scenario summary DataFrame
            yearly_df: Optional yearly results DataFrame
            verbose: Print results to console

        Returns:
            Tuple of (all_passed, list of VerificationResults)
        """
        all_results = []

        # 1. Cycle time verification
        cycle_result = self.verify_cycle_time(shuttle_size, pump_size)
        all_results.append(cycle_result)

        # 2. Constraint verification (if yearly_df provided)
        if yearly_df is not None:
            constraint_results = self.verify_constraint_satisfaction(
                yearly_df, shuttle_size, pump_size
            )
            all_results.extend(constraint_results)

        # 3. NPC breakdown (if scenario_df provided)
        if scenario_df is not None:
            mask = (scenario_df['Shuttle_Size_cbm'] == shuttle_size) & \
                   (scenario_df['Pump_Size_m3ph'] == pump_size)
            if mask.any():
                row = scenario_df[mask].iloc[0].to_dict()
                npc_result = self.verify_npc_breakdown(row)
                all_results.append(npc_result)

        # Print results
        if verbose:
            print("\n" + "="*60)
            print(f"Verification Results: Shuttle={shuttle_size}m3, Pump={pump_size}m3/h")
            print("="*60)
            for result in all_results:
                print(result)
            print("="*60)

        all_passed = all(r.passed for r in all_results)
        summary = "[PASS] All verifications passed" if all_passed else "[FAIL] Some verifications failed"
        if verbose:
            print(summary)

        return all_passed, all_results


def verify_case(
    case_id: str,
    shuttle_size: float,
    pump_size: float,
    verbose: bool = True
) -> bool:
    """
    Convenience function to verify a specific case/scenario.

    Args:
        case_id: Case ID (e.g., "case_1", "case_2")
        shuttle_size: Shuttle size in m3
        pump_size: Pump flow rate in m3/h
        verbose: Print results

    Returns:
        True if all verifications passed
    """
    config = load_config(case_id)
    verifier = CalculationVerifier(config)
    passed, _ = verifier.run_all_verifications(shuttle_size, pump_size, verbose=verbose)
    return passed


def verify_optimization_result(
    case_id: str,
    scenario_df: pd.DataFrame,
    yearly_df: pd.DataFrame,
    top_n: int = 5,
    verbose: bool = True
) -> Tuple[bool, Dict]:
    """
    Verify top N scenarios from optimization results.

    Args:
        case_id: Case ID
        scenario_df: Scenario summary DataFrame
        yearly_df: Yearly results DataFrame
        top_n: Number of top scenarios to verify
        verbose: Print results

    Returns:
        Tuple of (all_passed, dict with details)
    """
    config = load_config(case_id)
    verifier = CalculationVerifier(config)

    # Get top N scenarios by NPC
    top_scenarios = scenario_df.nsmallest(top_n, "NPC_Total_USDm")

    all_passed = True
    results_summary = {}

    if verbose:
        print("\n" + "="*60)
        print(f"Verifying Top {top_n} Scenarios for {case_id}")
        print("="*60)

    for _, row in top_scenarios.iterrows():
        shuttle_size = row['Shuttle_Size_cbm']
        pump_size = row['Pump_Size_m3ph']

        passed, results = verifier.run_all_verifications(
            shuttle_size=shuttle_size,
            pump_size=pump_size,
            scenario_df=scenario_df,
            yearly_df=yearly_df,
            verbose=verbose
        )

        results_summary[(shuttle_size, pump_size)] = {
            'passed': passed,
            'results': results,
            'npc': row['NPC_Total_USDm']
        }

        if not passed:
            all_passed = False

    return all_passed, results_summary
