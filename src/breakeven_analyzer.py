#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Break-even Analysis Module - Case comparison and break-even point identification.

This module provides:
- Distance-based break-even analysis (Case 1 vs Case 2)
- Demand-based break-even analysis
- Vessel mix-based break-even analysis
- Cross-case NPC comparison

Key outputs for SCI papers:
- Break-even distance curves
- Case comparison tables
- Decision boundary charts

Usage:
    from src.breakeven_analyzer import BreakevenAnalyzer
    analyzer = BreakevenAnalyzer()
    result = analyzer.find_breakeven_distance(case1_config, case2_config)
"""

import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from pathlib import Path

from .optimizer import BunkeringOptimizer
from .config_loader import load_config


@dataclass
class BreakevenResult:
    """
    Result from break-even analysis.

    Attributes:
        parameter_name: Name of the varied parameter
        breakeven_value: Value where costs are equal (None if no crossover)
        case1_name: Name of first case
        case2_name: Name of second case
        param_values: Parameter values tested
        case1_npcs: NPC values for case 1
        case2_npcs: NPC values for case 2
        case1_better_below: True if case1 is better below breakeven
    """
    parameter_name: str
    breakeven_value: Optional[float]
    case1_name: str
    case2_name: str
    param_values: List[float] = field(default_factory=list)
    case1_npcs: List[float] = field(default_factory=list)
    case2_npcs: List[float] = field(default_factory=list)
    case1_better_below: bool = True

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame for export."""
        return pd.DataFrame({
            self.parameter_name: self.param_values,
            f"{self.case1_name}_NPC_USDm": self.case1_npcs,
            f"{self.case2_name}_NPC_USDm": self.case2_npcs,
            "Difference_USDm": [c1 - c2 for c1, c2 in zip(self.case1_npcs, self.case2_npcs)],
            "Preferred_Case": [self.case1_name if c1 < c2 else self.case2_name
                             for c1, c2 in zip(self.case1_npcs, self.case2_npcs)],
        })


@dataclass
class CaseComparisonResult:
    """
    Result from multi-case comparison.

    Attributes:
        cases: List of case names
        shuttle_sizes: Shuttle sizes tested
        pump_sizes: Pump sizes tested
        npc_matrix: Dict mapping (case, shuttle, pump) to NPC
        optimal_by_case: Dict mapping case to its optimal configuration
    """
    cases: List[str] = field(default_factory=list)
    shuttle_sizes: List[float] = field(default_factory=list)
    pump_sizes: List[float] = field(default_factory=list)
    npc_matrix: Dict[Tuple[str, float, float], float] = field(default_factory=dict)
    optimal_by_case: Dict[str, Dict] = field(default_factory=dict)

    def get_optimal_comparison_df(self) -> pd.DataFrame:
        """Get DataFrame comparing optimal solutions across cases."""
        rows = []
        for case_name, optimal in self.optimal_by_case.items():
            rows.append({
                "Case": case_name,
                "Optimal_Shuttle_m3": optimal.get("shuttle_size", 0),
                "Optimal_Pump_m3ph": optimal.get("pump_size", 0),
                "NPC_USDm": optimal.get("npc", 0),
                "LCO_USD_per_ton": optimal.get("lco", 0),
            })
        return pd.DataFrame(rows)


class BreakevenAnalyzer:
    """
    Break-even analysis between different cases and configurations.

    This analyzer:
    - Compares NPC between Case 1 (storage) and Case 2 (direct supply)
    - Finds break-even points for key parameters
    - Generates decision boundary data

    Args:
        shuttle_size: Fixed shuttle size for analysis (optional)
        pump_size: Fixed pump size for analysis (optional)
    """

    def __init__(
        self,
        shuttle_size: Optional[float] = None,
        pump_size: Optional[float] = None
    ):
        self.shuttle_size = shuttle_size
        self.pump_size = pump_size

    def _run_optimization(
        self,
        config: Dict,
        shuttle_size: Optional[float] = None,
        pump_size: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Run optimization and return NPC and LCO.

        Returns:
            Tuple of (NPC in USD millions, LCO in USD/ton)
        """
        shuttle = shuttle_size or self.shuttle_size or config["shuttle"]["available_sizes_cbm"][0]
        pump = pump_size or self.pump_size or config["pumps"]["available_flow_rates"][0]

        optimizer = BunkeringOptimizer(config)
        optimizer.shuttle_sizes = [shuttle]
        optimizer.pump_sizes = [pump]

        scenario_df, yearly_df = optimizer.solve()

        if scenario_df.empty:
            return float('inf'), float('inf')

        npc = scenario_df['NPC_Total_USDm'].iloc[0]
        lco = scenario_df.get('LCOAmmonia_USD_per_ton', pd.Series([0])).iloc[0]

        return npc, lco

    def find_breakeven_distance(
        self,
        case1_config: Dict,
        case2_config: Dict,
        distance_range: Tuple[float, float] = (10, 100),
        n_points: int = 10,
        verbose: bool = True
    ) -> BreakevenResult:
        """
        Find break-even travel distance between two cases.

        Varies travel_time_hours in case2_config to find where NPCs cross.

        Args:
            case1_config: Case 1 configuration (typically with storage)
            case2_config: Case 2 configuration (direct supply)
            distance_range: Range of distances in nautical miles
            n_points: Number of points to evaluate
            verbose: Print progress

        Returns:
            BreakevenResult with break-even distance
        """
        case1_name = case1_config.get("case_name", "Case 1")
        case2_name = case2_config.get("case_name", "Case 2")

        if verbose:
            print("\n" + "="*60)
            print("Break-even Distance Analysis")
            print("="*60)
            print(f"Case 1: {case1_name}")
            print(f"Case 2: {case2_name}")
            print(f"Distance range: {distance_range[0]} - {distance_range[1]} nm")

        # Get base travel speed (assume 15 knots if not specified)
        base_travel_time = case2_config["operations"]["travel_time_hours"]
        base_distance = case2_config["operations"].get("distance_nm", 86)  # Default Yeosu
        speed_knots = base_distance / base_travel_time if base_travel_time > 0 else 15.0

        # Generate distance points
        distances = np.linspace(distance_range[0], distance_range[1], n_points)

        # Case 1 NPC (constant - doesn't depend on distance)
        case1_npc, _ = self._run_optimization(case1_config)
        case1_npcs = [case1_npc] * len(distances)

        if verbose:
            print(f"\n{case1_name} NPC (fixed): ${case1_npc:.2f}M")

        # Case 2 NPCs (vary with distance)
        case2_npcs = []

        for dist in distances:
            # Calculate travel time for this distance
            travel_time = dist / speed_knots

            # Modify config
            modified_config = copy.deepcopy(case2_config)
            modified_config["operations"]["travel_time_hours"] = travel_time

            npc, _ = self._run_optimization(modified_config)
            case2_npcs.append(npc)

            if verbose:
                print(f"  Distance={dist:.0f}nm (travel={travel_time:.2f}h): ${npc:.2f}M")

        # Find break-even point (where NPCs cross)
        breakeven_distance = self._find_crossover(distances, case1_npcs, case2_npcs)

        result = BreakevenResult(
            parameter_name="Distance_nm",
            breakeven_value=breakeven_distance,
            case1_name=case1_name,
            case2_name=case2_name,
            param_values=list(distances),
            case1_npcs=case1_npcs,
            case2_npcs=case2_npcs,
            case1_better_below=(case1_npc < case2_npcs[0]) if case2_npcs else True,
        )

        if verbose:
            print(f"\nBreak-even distance: ", end="")
            if breakeven_distance is not None:
                print(f"{breakeven_distance:.1f} nm")
                if result.case1_better_below:
                    print(f"  Below {breakeven_distance:.0f}nm: {case1_name} preferred")
                    print(f"  Above {breakeven_distance:.0f}nm: {case2_name} preferred")
                else:
                    print(f"  Below {breakeven_distance:.0f}nm: {case2_name} preferred")
                    print(f"  Above {breakeven_distance:.0f}nm: {case1_name} preferred")
            else:
                print("No crossover in range")
            print("="*60)

        return result

    def find_breakeven_demand(
        self,
        case1_config: Dict,
        case2_config: Dict,
        demand_range: Tuple[int, int] = (50, 500),
        n_points: int = 10,
        verbose: bool = True
    ) -> BreakevenResult:
        """
        Find break-even annual demand (number of vessels) between two cases.

        Args:
            case1_config: Case 1 configuration
            case2_config: Case 2 configuration
            demand_range: Range of annual vessel counts
            n_points: Number of points to evaluate
            verbose: Print progress

        Returns:
            BreakevenResult with break-even demand
        """
        case1_name = case1_config.get("case_name", "Case 1")
        case2_name = case2_config.get("case_name", "Case 2")

        if verbose:
            print("\n" + "="*60)
            print("Break-even Demand Analysis")
            print("="*60)
            print(f"Case 1: {case1_name}")
            print(f"Case 2: {case2_name}")
            print(f"Vessel range: {demand_range[0]} - {demand_range[1]} vessels/year")

        # Generate demand points (start vessels in 2030)
        demands = np.linspace(demand_range[0], demand_range[1], n_points, dtype=int)

        case1_npcs = []
        case2_npcs = []

        for demand in demands:
            # Modify configs for this demand level
            # Keep end_vessels proportional
            end_factor = case1_config["shipping"]["end_vessels"] / case1_config["shipping"]["start_vessels"]

            modified_config1 = copy.deepcopy(case1_config)
            modified_config1["shipping"]["start_vessels"] = int(demand)
            modified_config1["shipping"]["end_vessels"] = int(demand * end_factor)

            modified_config2 = copy.deepcopy(case2_config)
            modified_config2["shipping"]["start_vessels"] = int(demand)
            modified_config2["shipping"]["end_vessels"] = int(demand * end_factor)

            npc1, _ = self._run_optimization(modified_config1)
            npc2, _ = self._run_optimization(modified_config2)

            case1_npcs.append(npc1)
            case2_npcs.append(npc2)

            if verbose:
                better = case1_name if npc1 < npc2 else case2_name
                print(f"  Vessels={demand}: {case1_name}=${npc1:.2f}M, {case2_name}=${npc2:.2f}M -> {better}")

        # Find break-even point
        breakeven_demand = self._find_crossover(demands, case1_npcs, case2_npcs)

        result = BreakevenResult(
            parameter_name="Annual_Vessels",
            breakeven_value=breakeven_demand,
            case1_name=case1_name,
            case2_name=case2_name,
            param_values=list(demands),
            case1_npcs=case1_npcs,
            case2_npcs=case2_npcs,
            case1_better_below=(case1_npcs[0] < case2_npcs[0]) if case1_npcs and case2_npcs else True,
        )

        if verbose:
            print(f"\nBreak-even demand: ", end="")
            if breakeven_demand is not None:
                print(f"{breakeven_demand:.0f} vessels/year")
            else:
                print("No crossover in range")
            print("="*60)

        return result

    def find_breakeven_vessel_mix(
        self,
        case1_config: Dict,
        case2_config: Dict,
        large_share_range: Tuple[float, float] = (0.10, 0.50),
        n_points: int = 9,
        verbose: bool = True
    ) -> BreakevenResult:
        """
        Find break-even large vessel share between two cases.

        This varies the bunker_volume_per_call based on vessel mix.

        Args:
            case1_config: Case 1 configuration
            case2_config: Case 2 configuration
            large_share_range: Range of large vessel shares (0-1)
            n_points: Number of points to evaluate
            verbose: Print progress

        Returns:
            BreakevenResult with break-even vessel mix
        """
        case1_name = case1_config.get("case_name", "Case 1")
        case2_name = case2_config.get("case_name", "Case 2")

        if verbose:
            print("\n" + "="*60)
            print("Break-even Vessel Mix Analysis")
            print("="*60)
            print(f"Case 1: {case1_name}")
            print(f"Case 2: {case2_name}")
            print(f"Large vessel share range: {large_share_range[0]:.0%} - {large_share_range[1]:.0%}")

        # Vessel type volumes (from stochastic config defaults)
        small_vol = 1500    # m3
        medium_vol = 4000   # m3
        large_vol = 10000   # m3

        # Generate share points
        large_shares = np.linspace(large_share_range[0], large_share_range[1], n_points)

        case1_npcs = []
        case2_npcs = []

        for large_share in large_shares:
            # Calculate weighted average bunker volume
            # Assume: small=30%*(1-large), medium=70%*(1-large), large=large
            remaining = 1 - large_share
            small_share = 0.30 * remaining
            medium_share = 0.70 * remaining

            weighted_volume = (
                small_share * small_vol +
                medium_share * medium_vol +
                large_share * large_vol
            )

            # Modify configs
            modified_config1 = copy.deepcopy(case1_config)
            modified_config1["bunkering"]["bunker_volume_per_call_m3"] = weighted_volume

            modified_config2 = copy.deepcopy(case2_config)
            modified_config2["bunkering"]["bunker_volume_per_call_m3"] = weighted_volume

            npc1, _ = self._run_optimization(modified_config1)
            npc2, _ = self._run_optimization(modified_config2)

            case1_npcs.append(npc1)
            case2_npcs.append(npc2)

            if verbose:
                print(f"  Large={large_share:.0%} (avg vol={weighted_volume:.0f}m3): "
                      f"{case1_name}=${npc1:.2f}M, {case2_name}=${npc2:.2f}M")

        # Find break-even point
        breakeven_share = self._find_crossover(large_shares, case1_npcs, case2_npcs)

        result = BreakevenResult(
            parameter_name="Large_Vessel_Share",
            breakeven_value=breakeven_share,
            case1_name=case1_name,
            case2_name=case2_name,
            param_values=list(large_shares),
            case1_npcs=case1_npcs,
            case2_npcs=case2_npcs,
            case1_better_below=(case1_npcs[0] < case2_npcs[0]) if case1_npcs and case2_npcs else True,
        )

        if verbose:
            print(f"\nBreak-even large vessel share: ", end="")
            if breakeven_share is not None:
                print(f"{breakeven_share:.0%}")
            else:
                print("No crossover in range")
            print("="*60)

        return result

    def _find_crossover(
        self,
        x_values: np.ndarray,
        y1_values: List[float],
        y2_values: List[float]
    ) -> Optional[float]:
        """Find where two curves cross using linear interpolation."""
        x = np.array(x_values)
        y1 = np.array(y1_values)
        y2 = np.array(y2_values)

        # Calculate difference
        diff = y1 - y2

        # Look for sign change
        for i in range(len(diff) - 1):
            if diff[i] * diff[i + 1] < 0:
                # Linear interpolation to find crossover
                x0, x1 = x[i], x[i + 1]
                d0, d1 = diff[i], diff[i + 1]

                # x_cross where diff = 0
                x_cross = x0 - d0 * (x1 - x0) / (d1 - d0)
                return float(x_cross)

        return None

    def compare_all_cases(
        self,
        case_ids: List[str] = None,
        shuttle_sizes: Optional[List[float]] = None,
        pump_sizes: Optional[List[float]] = None,
        verbose: bool = True
    ) -> CaseComparisonResult:
        """
        Compare NPC across multiple cases.

        Args:
            case_ids: List of case IDs to compare (default: all 3 cases)
            shuttle_sizes: Shuttle sizes to test (default: from config)
            pump_sizes: Pump sizes to test (default: from config)
            verbose: Print progress

        Returns:
            CaseComparisonResult with comparison data
        """
        if case_ids is None:
            case_ids = ["case_1", "case_2_yeosu", "case_2_ulsan"]

        if verbose:
            print("\n" + "="*60)
            print("Multi-Case Comparison")
            print("="*60)
            print(f"Cases: {case_ids}")

        result = CaseComparisonResult(cases=case_ids)
        configs = {}

        # Load configs
        for case_id in case_ids:
            try:
                configs[case_id] = load_config(case_id)
            except Exception as e:
                if verbose:
                    print(f"  [WARN] Could not load {case_id}: {e}")

        if not configs:
            return result

        # Use first config for shuttle/pump lists
        first_config = list(configs.values())[0]

        if shuttle_sizes is None:
            shuttle_sizes = first_config["shuttle"]["available_sizes_cbm"][:3]  # Top 3
        if pump_sizes is None:
            pump_sizes = first_config["pumps"]["available_flow_rates"][:3]  # Top 3

        result.shuttle_sizes = list(shuttle_sizes)
        result.pump_sizes = list(pump_sizes)

        # Run optimizations
        for case_id, config in configs.items():
            if verbose:
                print(f"\n{case_id}:")

            best_npc = float('inf')
            best_config = {}

            for shuttle in shuttle_sizes:
                for pump in pump_sizes:
                    try:
                        npc, lco = self._run_optimization(config, shuttle, pump)
                        result.npc_matrix[(case_id, shuttle, pump)] = npc

                        if npc < best_npc:
                            best_npc = npc
                            best_config = {
                                "shuttle_size": shuttle,
                                "pump_size": pump,
                                "npc": npc,
                                "lco": lco,
                            }

                        if verbose:
                            print(f"  Shuttle={shuttle}, Pump={pump}: ${npc:.2f}M")

                    except Exception as e:
                        if verbose:
                            print(f"  Shuttle={shuttle}, Pump={pump}: Failed - {e}")

            result.optimal_by_case[case_id] = best_config

        if verbose:
            print("\n" + "="*60)
            print("Optimal Solutions by Case:")
            for case_id, opt in result.optimal_by_case.items():
                print(f"  {case_id}: Shuttle={opt.get('shuttle_size', 'N/A')}m3, "
                      f"Pump={opt.get('pump_size', 'N/A')}m3/h, NPC=${opt.get('npc', 0):.2f}M")
            print("="*60)

        return result

    def run_full_analysis(
        self,
        case1_id: str = "case_1",
        case2_id: str = "case_2_yeosu",
        output_dir: Optional[str] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run complete break-even analysis suite.

        Args:
            case1_id: First case ID
            case2_id: Second case ID
            output_dir: Optional output directory
            verbose: Print progress

        Returns:
            Dict with all analysis results
        """
        case1_config = load_config(case1_id)
        case2_config = load_config(case2_id)

        results = {}

        # 1. Distance-based break-even
        results["distance"] = self.find_breakeven_distance(
            case1_config, case2_config, verbose=verbose
        )

        # 2. Demand-based break-even
        results["demand"] = self.find_breakeven_demand(
            case1_config, case2_config, verbose=verbose
        )

        # 3. Vessel mix-based break-even
        results["vessel_mix"] = self.find_breakeven_vessel_mix(
            case1_config, case2_config, verbose=verbose
        )

        # 4. Multi-case comparison
        results["comparison"] = self.compare_all_cases(verbose=verbose)

        # Save results
        if output_dir:
            self._save_results(results, output_dir)

        return results

    def _save_results(self, results: Dict, output_dir: str) -> None:
        """Save analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for name in ["distance", "demand", "vessel_mix"]:
            if name in results and results[name] is not None:
                df = results[name].to_dataframe()
                df.to_csv(output_path / f"breakeven_{name}.csv", index=False)

        if "comparison" in results:
            df = results["comparison"].get_optimal_comparison_df()
            df.to_csv(output_path / "case_comparison.csv", index=False)

        print(f"\n[OK] Results saved to {output_path}")


def run_breakeven_analysis(
    case1_id: str = "case_1",
    case2_id: str = "case_2_yeosu",
    shuttle_size: Optional[float] = None,
    pump_size: Optional[float] = None,
    output_dir: Optional[str] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to run break-even analysis.

    Args:
        case1_id: First case ID
        case2_id: Second case ID
        shuttle_size: Fixed shuttle size (optional)
        pump_size: Fixed pump size (optional)
        output_dir: Output directory (optional)
        verbose: Print progress

    Returns:
        Dict with all analysis results
    """
    analyzer = BreakevenAnalyzer(
        shuttle_size=shuttle_size,
        pump_size=pump_size
    )

    return analyzer.run_full_analysis(
        case1_id=case1_id,
        case2_id=case2_id,
        output_dir=output_dir,
        verbose=verbose
    )
