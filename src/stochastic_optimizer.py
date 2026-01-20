#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stochastic Optimizer Module - Two-Stage Stochastic Programming for Bunkering.

This module extends the deterministic optimizer to handle:
- Heterogeneous vessel sizes (different bunkering volumes)
- Demand uncertainty (Monte Carlo scenarios)
- Value of Stochastic Solution (VSS) calculation
- Expected Value of Perfect Information (EVPI) calculation

Mathematical Model:
    1st Stage (Here-and-Now): Infrastructure decisions
        - Shuttle size selection (discrete)
        - Pump size selection (discrete)
        - Initial fleet sizing

    2nd Stage (Wait-and-See): Operational decisions per scenario
        - Annual fleet additions
        - Number of bunkering calls

Objective: min E_s [ sum_t ( CAPEX + OPEX(s) ) ]

Usage:
    from src.stochastic_optimizer import StochasticOptimizer
    from src.vessel_distribution import VesselDistribution

    stoch_opt = StochasticOptimizer(config, vessel_distribution)
    result = stoch_opt.solve()
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from pathlib import Path

from .optimizer import BunkeringOptimizer
from .vessel_distribution import VesselDistribution, MonteCarloScenario
from .cost_calculator import CostCalculator
from .cycle_time_calculator import CycleTimeCalculator
from .config_loader import load_config


@dataclass
class StochasticResult:
    """
    Result from stochastic optimization.

    Attributes:
        optimal_shuttle_size: Best shuttle size in m3
        optimal_pump_size: Best pump flow rate in m3/h
        expected_npc: Expected NPC across all scenarios (USD millions)
        npc_std: Standard deviation of NPC (USD millions)
        npc_by_scenario: NPC for each Monte Carlo scenario
        vss: Value of Stochastic Solution
        evpi: Expected Value of Perfect Information
        scenario_statistics: Statistics by distribution scenario
        deterministic_solution: Result from deterministic model (mean values)
    """
    optimal_shuttle_size: float
    optimal_pump_size: float
    expected_npc: float
    npc_std: float
    npc_by_scenario: List[float] = field(default_factory=list)
    confidence_interval_95: Tuple[float, float] = (0.0, 0.0)
    vss: float = 0.0
    vss_percent: float = 0.0
    evpi: float = 0.0
    evpi_percent: float = 0.0
    scenario_statistics: Dict = field(default_factory=dict)
    deterministic_npc: float = 0.0
    wait_and_see_npc: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary for export."""
        return {
            "Optimal_Shuttle_Size_m3": self.optimal_shuttle_size,
            "Optimal_Pump_Size_m3ph": self.optimal_pump_size,
            "Expected_NPC_USDm": self.expected_npc,
            "NPC_Std_USDm": self.npc_std,
            "CI_95_Lower_USDm": self.confidence_interval_95[0],
            "CI_95_Upper_USDm": self.confidence_interval_95[1],
            "VSS_USDm": self.vss,
            "VSS_Percent": self.vss_percent,
            "EVPI_USDm": self.evpi,
            "EVPI_Percent": self.evpi_percent,
            "Deterministic_NPC_USDm": self.deterministic_npc,
            "Wait_And_See_NPC_USDm": self.wait_and_see_npc,
        }


@dataclass
class ScenarioOptResult:
    """Result from optimizing a single scenario."""
    scenario_id: int
    shuttle_size: float
    pump_size: float
    npc: float
    feasible: bool
    yearly_data: List[Dict] = field(default_factory=list)


class StochasticOptimizer:
    """
    Two-Stage Stochastic MILP Optimizer for bunkering infrastructure.

    This optimizer:
    1. Generates Monte Carlo scenarios using VesselDistribution
    2. Solves deterministic sub-problems for each scenario
    3. Computes expected costs and optimal first-stage decisions
    4. Calculates VSS and EVPI metrics

    Args:
        config: Base configuration dictionary
        vessel_distribution: VesselDistribution instance for scenarios
        n_scenarios: Number of Monte Carlo scenarios (overrides config)
    """

    def __init__(
        self,
        config: Dict,
        vessel_distribution: VesselDistribution,
        n_scenarios: Optional[int] = None
    ):
        self.config = config
        self.vessel_dist = vessel_distribution
        self.n_scenarios = n_scenarios or vessel_distribution.n_monte_carlo

        self.case_id = config.get("case_id", "unknown")

        # Generate scenarios upfront
        self.mc_scenarios = vessel_distribution.generate_monte_carlo_scenarios(
            n_scenarios=self.n_scenarios
        )

        # Store results
        self.scenario_results: Dict[Tuple[float, float], List[ScenarioOptResult]] = {}
        self.best_result: Optional[StochasticResult] = None

    def solve(
        self,
        shuttle_sizes: Optional[List[float]] = None,
        pump_sizes: Optional[List[float]] = None,
        verbose: bool = True
    ) -> StochasticResult:
        """
        Solve two-stage stochastic optimization.

        Args:
            shuttle_sizes: Shuttle sizes to evaluate (default: from config)
            pump_sizes: Pump sizes to evaluate (default: from config)
            verbose: Print progress information

        Returns:
            StochasticResult with optimal solution and metrics
        """
        if shuttle_sizes is None:
            shuttle_sizes = self.config["shuttle"]["available_sizes_cbm"]
        if pump_sizes is None:
            pump_sizes = self.config["pumps"]["available_flow_rates"]

        if verbose:
            print("\n" + "="*60)
            print("Stochastic Optimization")
            print("="*60)
            print(f"Case: {self.case_id}")
            print(f"Monte Carlo scenarios: {self.n_scenarios}")
            print(f"Shuttle sizes: {len(shuttle_sizes)}")
            print(f"Pump sizes: {len(pump_sizes)}")
            print("="*60)

        # Store expected NPC for each (shuttle, pump) combination
        expected_npcs: Dict[Tuple[float, float], float] = {}
        npc_stds: Dict[Tuple[float, float], float] = {}
        npc_lists: Dict[Tuple[float, float], List[float]] = {}

        total_combinations = len(shuttle_sizes) * len(pump_sizes)
        current = 0

        for shuttle_size in shuttle_sizes:
            for pump_size in pump_sizes:
                current += 1

                # Solve all scenarios for this combination
                scenario_npcs = self._solve_all_scenarios(
                    shuttle_size, pump_size, verbose=False
                )

                if scenario_npcs:
                    expected_npc = np.mean(scenario_npcs)
                    npc_std = np.std(scenario_npcs)

                    expected_npcs[(shuttle_size, pump_size)] = expected_npc
                    npc_stds[(shuttle_size, pump_size)] = npc_std
                    npc_lists[(shuttle_size, pump_size)] = scenario_npcs

                if verbose and current % 10 == 0:
                    progress = (current / total_combinations) * 100
                    print(f"Progress: {current}/{total_combinations} ({progress:.1f}%)")

        if not expected_npcs:
            raise ValueError("No feasible solutions found")

        # Find optimal combination (minimum expected NPC)
        optimal_combo = min(expected_npcs, key=expected_npcs.get)
        optimal_shuttle, optimal_pump = optimal_combo

        # Get metrics for optimal solution
        optimal_expected_npc = expected_npcs[optimal_combo]
        optimal_npc_std = npc_stds[optimal_combo]
        optimal_npcs = npc_lists[optimal_combo]

        # Calculate confidence interval
        ci_lower = np.percentile(optimal_npcs, 2.5)
        ci_upper = np.percentile(optimal_npcs, 97.5)

        # Calculate VSS and EVPI
        deterministic_npc = self._solve_deterministic(optimal_shuttle, optimal_pump)
        wait_and_see_npc = self._calculate_wait_and_see(shuttle_sizes, pump_sizes)

        vss = deterministic_npc - optimal_expected_npc
        vss_percent = (vss / deterministic_npc * 100) if deterministic_npc > 0 else 0

        evpi = optimal_expected_npc - wait_and_see_npc
        evpi_percent = (evpi / optimal_expected_npc * 100) if optimal_expected_npc > 0 else 0

        # Get scenario statistics
        scenario_stats = self._calculate_scenario_statistics(optimal_npcs)

        result = StochasticResult(
            optimal_shuttle_size=optimal_shuttle,
            optimal_pump_size=optimal_pump,
            expected_npc=optimal_expected_npc,
            npc_std=optimal_npc_std,
            npc_by_scenario=optimal_npcs,
            confidence_interval_95=(ci_lower, ci_upper),
            vss=vss,
            vss_percent=vss_percent,
            evpi=evpi,
            evpi_percent=evpi_percent,
            scenario_statistics=scenario_stats,
            deterministic_npc=deterministic_npc,
            wait_and_see_npc=wait_and_see_npc,
        )

        self.best_result = result

        if verbose:
            self._print_result_summary(result, expected_npcs)

        return result

    def _solve_all_scenarios(
        self,
        shuttle_size: float,
        pump_size: float,
        verbose: bool = False
    ) -> List[float]:
        """
        Solve optimization for all Monte Carlo scenarios with fixed shuttle/pump.

        Args:
            shuttle_size: Shuttle size in m3
            pump_size: Pump flow rate in m3/h
            verbose: Print per-scenario progress

        Returns:
            List of NPC values for each scenario (feasible only)
        """
        npcs = []

        for mc_scenario in self.mc_scenarios:
            # Create modified config with scenario-specific demand
            scenario_config = self._create_scenario_config(mc_scenario)

            # Create optimizer for this scenario
            try:
                optimizer = BunkeringOptimizer(scenario_config)

                # Override with fixed shuttle/pump sizes
                optimizer.shuttle_sizes = [shuttle_size]
                optimizer.pump_sizes = [pump_size]

                # Solve
                scenario_df, yearly_df = optimizer.solve()

                if not scenario_df.empty:
                    npc = scenario_df['NPC_Total_USDm'].iloc[0]
                    npcs.append(npc)

                    if verbose:
                        print(f"  Scenario {mc_scenario.scenario_id}: NPC = ${npc:.2f}M")

            except Exception as e:
                if verbose:
                    print(f"  Scenario {mc_scenario.scenario_id}: Failed - {e}")

        return npcs

    def _create_scenario_config(self, mc_scenario: MonteCarloScenario) -> Dict:
        """
        Create modified config for a specific Monte Carlo scenario.

        This adjusts the demand based on the scenario's vessel call distribution.
        """
        import copy
        scenario_config = copy.deepcopy(self.config)

        # Calculate average bunker volume for this scenario
        if mc_scenario.vessel_calls:
            total_volume = sum(vol for _, vol in mc_scenario.vessel_calls)
            avg_volume = total_volume / len(mc_scenario.vessel_calls)
        else:
            avg_volume = self.config["bunkering"]["bunker_volume_per_call_m3"]

        # Update config with scenario-specific volume
        scenario_config["bunkering"]["bunker_volume_per_call_m3"] = avg_volume

        # Adjust for total annual demand variation
        # The number of calls is fixed, but volume per call varies
        # This changes total annual demand

        return scenario_config

    def _solve_deterministic(
        self,
        shuttle_size: float,
        pump_size: float
    ) -> float:
        """
        Solve deterministic problem using mean/expected values.

        This gives EV (Expected Value) solution cost.
        """
        # Use original config (with fixed bunker volume)
        optimizer = BunkeringOptimizer(self.config)
        optimizer.shuttle_sizes = [shuttle_size]
        optimizer.pump_sizes = [pump_size]

        scenario_df, _ = optimizer.solve()

        if scenario_df.empty:
            return float('inf')

        return scenario_df['NPC_Total_USDm'].iloc[0]

    def _calculate_wait_and_see(
        self,
        shuttle_sizes: List[float],
        pump_sizes: List[float]
    ) -> float:
        """
        Calculate Wait-and-See (WS) solution cost.

        WS = E[ min_{x} c(x, s) ] - optimize AFTER knowing the scenario
        This is the best we could do with perfect information.
        """
        ws_costs = []

        for mc_scenario in self.mc_scenarios:
            scenario_config = self._create_scenario_config(mc_scenario)

            # Find best (shuttle, pump) for THIS scenario
            best_npc = float('inf')

            for shuttle_size in shuttle_sizes:
                for pump_size in pump_sizes:
                    try:
                        optimizer = BunkeringOptimizer(scenario_config)
                        optimizer.shuttle_sizes = [shuttle_size]
                        optimizer.pump_sizes = [pump_size]

                        scenario_df, _ = optimizer.solve()

                        if not scenario_df.empty:
                            npc = scenario_df['NPC_Total_USDm'].iloc[0]
                            best_npc = min(best_npc, npc)
                    except Exception:
                        pass

            if best_npc < float('inf'):
                ws_costs.append(best_npc)

        return np.mean(ws_costs) if ws_costs else float('inf')

    def _calculate_scenario_statistics(self, npcs: List[float]) -> Dict:
        """Calculate statistics for the NPC distribution."""
        if not npcs:
            return {}

        npcs_arr = np.array(npcs)

        return {
            "mean": float(np.mean(npcs_arr)),
            "std": float(np.std(npcs_arr)),
            "min": float(np.min(npcs_arr)),
            "max": float(np.max(npcs_arr)),
            "p5": float(np.percentile(npcs_arr, 5)),
            "p25": float(np.percentile(npcs_arr, 25)),
            "p50": float(np.percentile(npcs_arr, 50)),
            "p75": float(np.percentile(npcs_arr, 75)),
            "p95": float(np.percentile(npcs_arr, 95)),
            "cv": float(np.std(npcs_arr) / np.mean(npcs_arr)) if np.mean(npcs_arr) > 0 else 0,
        }

    def _print_result_summary(
        self,
        result: StochasticResult,
        all_expected_npcs: Dict[Tuple[float, float], float]
    ) -> None:
        """Print summary of stochastic optimization results."""
        print("\n" + "="*60)
        print("Stochastic Optimization Results")
        print("="*60)

        print(f"\nOptimal Solution:")
        print(f"  Shuttle Size: {result.optimal_shuttle_size:,.0f} m3")
        print(f"  Pump Size: {result.optimal_pump_size:,.0f} m3/h")

        print(f"\nExpected NPC (20-year):")
        print(f"  Mean: ${result.expected_npc:.2f}M")
        print(f"  Std Dev: ${result.npc_std:.2f}M")
        print(f"  95% CI: [${result.confidence_interval_95[0]:.2f}M, ${result.confidence_interval_95[1]:.2f}M]")

        print(f"\nValue of Stochastic Solution (VSS):")
        print(f"  Deterministic NPC: ${result.deterministic_npc:.2f}M")
        print(f"  Stochastic NPC: ${result.expected_npc:.2f}M")
        print(f"  VSS: ${result.vss:.2f}M ({result.vss_percent:.1f}%)")

        print(f"\nExpected Value of Perfect Information (EVPI):")
        print(f"  Wait-and-See NPC: ${result.wait_and_see_npc:.2f}M")
        print(f"  EVPI: ${result.evpi:.2f}M ({result.evpi_percent:.1f}%)")

        # Top 5 combinations
        print(f"\nTop 5 Shuttle/Pump Combinations:")
        sorted_combos = sorted(all_expected_npcs.items(), key=lambda x: x[1])[:5]
        for i, ((shuttle, pump), npc) in enumerate(sorted_combos, 1):
            print(f"  {i}. Shuttle={shuttle:,.0f}m3, Pump={pump:,.0f}m3/h: ${npc:.2f}M")

        print("="*60)

    def get_detailed_results(self) -> pd.DataFrame:
        """
        Get detailed results as DataFrame for export.

        Returns:
            DataFrame with per-scenario results
        """
        if not self.mc_scenarios or self.best_result is None:
            return pd.DataFrame()

        rows = []
        for i, npc in enumerate(self.best_result.npc_by_scenario):
            mc = self.mc_scenarios[i]
            rows.append({
                "Scenario_ID": mc.scenario_id,
                "Distribution_Scenario": mc.distribution_scenario,
                "Total_Demand_m3": mc.total_demand,
                "Call_Count": mc.call_count,
                "NPC_USDm": npc,
            })

        return pd.DataFrame(rows)

    def compare_distribution_scenarios(
        self,
        shuttle_size: float,
        pump_size: float,
        verbose: bool = True
    ) -> Dict[str, Dict]:
        """
        Compare results across different distribution scenarios.

        Args:
            shuttle_size: Fixed shuttle size for comparison
            pump_size: Fixed pump size for comparison
            verbose: Print comparison summary

        Returns:
            Dict mapping scenario name to statistics
        """
        results_by_dist = {}

        for scenario_name in self.vessel_dist.distribution_scenarios.keys():
            # Generate scenarios for this distribution only
            mc_scenarios = self.vessel_dist.generate_monte_carlo_scenarios(
                n_scenarios=self.n_scenarios,
                scenario_name=scenario_name
            )

            npcs = []
            for mc in mc_scenarios:
                scenario_config = self._create_scenario_config(mc)

                try:
                    optimizer = BunkeringOptimizer(scenario_config)
                    optimizer.shuttle_sizes = [shuttle_size]
                    optimizer.pump_sizes = [pump_size]

                    scenario_df, _ = optimizer.solve()

                    if not scenario_df.empty:
                        npcs.append(scenario_df['NPC_Total_USDm'].iloc[0])
                except Exception:
                    pass

            if npcs:
                results_by_dist[scenario_name] = {
                    "mean_npc": float(np.mean(npcs)),
                    "std_npc": float(np.std(npcs)),
                    "min_npc": float(np.min(npcs)),
                    "max_npc": float(np.max(npcs)),
                    "n_feasible": len(npcs),
                    "weighted_avg_volume": self.vessel_dist.get_weighted_average_volume(scenario_name),
                }

        if verbose:
            print("\n" + "="*60)
            print("Distribution Scenario Comparison")
            print(f"Shuttle: {shuttle_size:,.0f} m3, Pump: {pump_size:,.0f} m3/h")
            print("="*60)

            for name, stats in results_by_dist.items():
                print(f"\n{name}:")
                print(f"  Weighted Avg Volume: {stats['weighted_avg_volume']:,.0f} m3")
                print(f"  Mean NPC: ${stats['mean_npc']:.2f}M")
                print(f"  Std Dev: ${stats['std_npc']:.2f}M")
                print(f"  Range: ${stats['min_npc']:.2f}M - ${stats['max_npc']:.2f}M")

            print("="*60)

        return results_by_dist


def run_stochastic_optimization(
    case_id: str = "case_1",
    n_scenarios: int = 100,
    output_dir: Optional[str] = None,
    verbose: bool = True
) -> StochasticResult:
    """
    Convenience function to run stochastic optimization.

    Args:
        case_id: Case identifier
        n_scenarios: Number of Monte Carlo scenarios
        output_dir: Optional output directory for results
        verbose: Print progress

    Returns:
        StochasticResult with optimal solution
    """
    from .vessel_distribution import load_stochastic_config

    # Load configs
    config = load_config(case_id)
    stoch_config = load_stochastic_config()

    # Create vessel distribution
    base_calls = config["shipping"]["voyages_per_year"] * config["shipping"]["start_vessels"]
    vessel_dist = VesselDistribution(stoch_config, base_annual_calls=base_calls)

    if verbose:
        vessel_dist.print_summary()

    # Create and run optimizer
    optimizer = StochasticOptimizer(config, vessel_dist, n_scenarios=n_scenarios)
    result = optimizer.solve(verbose=verbose)

    # Export if output_dir specified
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save detailed results
        detailed_df = optimizer.get_detailed_results()
        detailed_df.to_csv(output_path / f"stochastic_scenarios_{case_id}.csv", index=False)

        # Save summary
        summary_df = pd.DataFrame([result.to_dict()])
        summary_df.to_csv(output_path / f"stochastic_summary_{case_id}.csv", index=False)

        if verbose:
            print(f"\n[OK] Results saved to {output_path}")

    return result
