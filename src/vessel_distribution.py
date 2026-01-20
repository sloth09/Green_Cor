#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vessel Distribution Module - Models heterogeneous vessel sizes for stochastic analysis.

This module provides:
- VesselType: Defines a vessel category (small, medium, large)
- DistributionScenario: A mix of vessel types with specified shares
- VesselDistribution: Main class for managing distributions and generating scenarios

Key Feature: Enables stochastic optimization with heterogeneous bunkering demand.

Usage:
    from src.vessel_distribution import VesselDistribution
    dist = VesselDistribution(stochastic_config)
    scenarios = dist.generate_monte_carlo_scenarios(n=100)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
from pathlib import Path
import yaml


@dataclass
class VesselType:
    """
    Defines a vessel category with volume characteristics.

    Attributes:
        name: Type identifier (e.g., "small", "medium", "large")
        min_volume: Minimum bunkering volume (m3)
        max_volume: Maximum bunkering volume (m3)
        mean_volume: Average bunkering volume (m3)
        std_volume: Standard deviation for sampling
    """
    name: str
    min_volume: float
    max_volume: float
    mean_volume: float
    std_volume: float = 0.0

    def sample(self, n: int = 1, method: str = "truncated_normal", rng: np.random.Generator = None) -> np.ndarray:
        """
        Sample bunkering volumes from this vessel type.

        Args:
            n: Number of samples
            method: Sampling method ("truncated_normal", "uniform", "fixed")
            rng: NumPy random generator for reproducibility

        Returns:
            Array of sampled volumes
        """
        if rng is None:
            rng = np.random.default_rng()

        if method == "fixed":
            return np.full(n, self.mean_volume)

        elif method == "uniform":
            return rng.uniform(self.min_volume, self.max_volume, n)

        elif method == "truncated_normal":
            # Sample from truncated normal distribution
            samples = []
            while len(samples) < n:
                raw = rng.normal(self.mean_volume, self.std_volume, n * 2)
                valid = raw[(raw >= self.min_volume) & (raw <= self.max_volume)]
                samples.extend(valid.tolist())
            return np.array(samples[:n])

        else:
            raise ValueError(f"Unknown sampling method: {method}")


@dataclass
class DistributionScenario:
    """
    A scenario defining a mix of vessel types.

    Attributes:
        name: Scenario identifier (e.g., "balanced", "high_large")
        description: Human-readable description
        shares: Dict mapping vessel type name to share (must sum to 1.0)
        probability: Probability of this scenario in stochastic analysis
    """
    name: str
    description: str
    shares: Dict[str, float]  # {"small": 0.3, "medium": 0.5, "large": 0.2}
    probability: float = 1.0

    def __post_init__(self):
        """Validate that shares sum to 1.0."""
        total = sum(self.shares.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Shares must sum to 1.0, got {total}")

    def get_weighted_mean_volume(self, vessel_types: Dict[str, VesselType]) -> float:
        """Calculate weighted average volume for this scenario."""
        total = 0.0
        for type_name, share in self.shares.items():
            if type_name in vessel_types:
                total += share * vessel_types[type_name].mean_volume
        return total


@dataclass
class MonteCarloScenario:
    """
    A single Monte Carlo scenario with sampled vessel calls.

    Attributes:
        scenario_id: Unique identifier
        distribution_scenario: The underlying distribution scenario name
        vessel_calls: List of (vessel_type, volume) tuples
        total_demand: Total bunkering demand for this scenario
        call_count: Number of vessel calls
    """
    scenario_id: int
    distribution_scenario: str
    vessel_calls: List[Tuple[str, float]] = field(default_factory=list)
    total_demand: float = 0.0
    call_count: int = 0

    def get_demand_by_type(self) -> Dict[str, float]:
        """Get total demand grouped by vessel type."""
        demand_by_type = {}
        for vtype, volume in self.vessel_calls:
            demand_by_type[vtype] = demand_by_type.get(vtype, 0) + volume
        return demand_by_type

    def get_call_count_by_type(self) -> Dict[str, int]:
        """Get call count grouped by vessel type."""
        count_by_type = {}
        for vtype, _ in self.vessel_calls:
            count_by_type[vtype] = count_by_type.get(vtype, 0) + 1
        return count_by_type


class VesselDistribution:
    """
    Main class for managing vessel distributions and generating scenarios.

    This class:
    - Loads vessel type definitions from config
    - Manages multiple distribution scenarios
    - Generates Monte Carlo samples for stochastic analysis

    Args:
        config: Stochastic configuration dict (from stochastic.yaml)
        base_annual_calls: Base number of annual calls (from base config)
    """

    def __init__(self, config: Dict, base_annual_calls: int = 600):
        self.config = config
        self.base_annual_calls = base_annual_calls

        # Load vessel types
        self.vessel_types = self._load_vessel_types()

        # Load distribution scenarios
        self.distribution_scenarios = self._load_distribution_scenarios()

        # Sampling parameters
        sampling_config = config.get("sampling", {})
        self.n_monte_carlo = sampling_config.get("n_monte_carlo", 100)
        self.random_seed = sampling_config.get("random_seed", 42)
        self.sampling_method = sampling_config.get("method", "discrete")
        self.continuous_distribution = sampling_config.get("continuous_distribution", "truncated_normal")

        # Random generator
        self.rng = np.random.default_rng(self.random_seed)

        # Default scenario
        self.default_scenario_name = config.get("vessel_distribution", {}).get("default_scenario", "balanced")

    def _load_vessel_types(self) -> Dict[str, VesselType]:
        """Load vessel type definitions from config."""
        types_config = self.config.get("vessel_distribution", {}).get("types", {})
        vessel_types = {}

        for type_name, type_config in types_config.items():
            vessel_types[type_name] = VesselType(
                name=type_name,
                min_volume=type_config.get("min_volume", 1000),
                max_volume=type_config.get("max_volume", 5000),
                mean_volume=type_config.get("mean_volume", 3000),
                std_volume=type_config.get("std_volume", 500)
            )

        # Default vessel types if not configured
        if not vessel_types:
            vessel_types = {
                "small": VesselType("small", 1000, 2500, 1500, 300),
                "medium": VesselType("medium", 2500, 6000, 4000, 700),
                "large": VesselType("large", 6000, 15000, 10000, 2000)
            }

        return vessel_types

    def _load_distribution_scenarios(self) -> Dict[str, DistributionScenario]:
        """Load distribution scenarios from config."""
        scenarios_config = self.config.get("vessel_distribution", {}).get("distribution_scenarios", {})
        scenarios = {}

        for scenario_name, scenario_config in scenarios_config.items():
            shares = {
                "small": scenario_config.get("small_share", 0.33),
                "medium": scenario_config.get("medium_share", 0.34),
                "large": scenario_config.get("large_share", 0.33)
            }
            scenarios[scenario_name] = DistributionScenario(
                name=scenario_name,
                description=scenario_config.get("description", ""),
                shares=shares,
                probability=scenario_config.get("probability", 1.0)
            )

        # Default scenarios if not configured
        if not scenarios:
            scenarios = {
                "balanced": DistributionScenario(
                    "balanced", "Balanced mix",
                    {"small": 0.30, "medium": 0.50, "large": 0.20},
                    probability=0.5
                ),
                "high_large": DistributionScenario(
                    "high_large", "Large vessel dominated",
                    {"small": 0.15, "medium": 0.35, "large": 0.50},
                    probability=0.25
                ),
                "high_small": DistributionScenario(
                    "high_small", "Small vessel dominated",
                    {"small": 0.50, "medium": 0.40, "large": 0.10},
                    probability=0.25
                )
            }

        return scenarios

    def get_vessel_types(self) -> List[VesselType]:
        """Return list of all vessel types."""
        return list(self.vessel_types.values())

    def get_distribution_scenarios(self) -> List[DistributionScenario]:
        """Return list of all distribution scenarios."""
        return list(self.distribution_scenarios.values())

    def get_default_scenario(self) -> DistributionScenario:
        """Return the default distribution scenario."""
        return self.distribution_scenarios.get(
            self.default_scenario_name,
            list(self.distribution_scenarios.values())[0]
        )

    def get_weighted_average_volume(self, scenario_name: str = None) -> float:
        """
        Get weighted average bunkering volume for a scenario.

        Args:
            scenario_name: Scenario to use (default: default_scenario)

        Returns:
            Weighted average volume in m3
        """
        if scenario_name is None:
            scenario_name = self.default_scenario_name

        scenario = self.distribution_scenarios.get(scenario_name)
        if scenario is None:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        return scenario.get_weighted_mean_volume(self.vessel_types)

    def generate_vessel_call_sequence(
        self,
        scenario_name: str,
        n_calls: int,
        method: str = None
    ) -> List[Tuple[str, float]]:
        """
        Generate a sequence of vessel calls for a given scenario.

        Args:
            scenario_name: Distribution scenario to use
            n_calls: Number of calls to generate
            method: Sampling method (default: from config)

        Returns:
            List of (vessel_type_name, bunkering_volume) tuples
        """
        if method is None:
            method = self.sampling_method

        scenario = self.distribution_scenarios.get(scenario_name)
        if scenario is None:
            raise ValueError(f"Unknown scenario: {scenario_name}")

        calls = []

        if method == "discrete":
            # Discrete: Assign vessel type based on share, use mean volume
            for _ in range(n_calls):
                # Select vessel type based on shares
                r = self.rng.random()
                cumulative = 0.0
                selected_type = None
                for type_name, share in scenario.shares.items():
                    cumulative += share
                    if r <= cumulative:
                        selected_type = type_name
                        break
                if selected_type is None:
                    selected_type = list(scenario.shares.keys())[-1]

                # Get volume (mean for discrete)
                vtype = self.vessel_types[selected_type]
                volume = vtype.mean_volume
                calls.append((selected_type, volume))

        else:
            # Continuous: Sample from distribution within each type
            for _ in range(n_calls):
                # Select vessel type
                r = self.rng.random()
                cumulative = 0.0
                selected_type = None
                for type_name, share in scenario.shares.items():
                    cumulative += share
                    if r <= cumulative:
                        selected_type = type_name
                        break
                if selected_type is None:
                    selected_type = list(scenario.shares.keys())[-1]

                # Sample volume
                vtype = self.vessel_types[selected_type]
                volume = vtype.sample(1, method=self.continuous_distribution, rng=self.rng)[0]
                calls.append((selected_type, volume))

        return calls

    def generate_monte_carlo_scenarios(
        self,
        n_scenarios: int = None,
        scenario_name: str = None,
        calls_per_scenario: int = None
    ) -> List[MonteCarloScenario]:
        """
        Generate Monte Carlo scenarios for stochastic analysis.

        Args:
            n_scenarios: Number of scenarios (default: from config)
            scenario_name: Distribution scenario (default: all scenarios with probability weighting)
            calls_per_scenario: Calls per scenario (default: base_annual_calls)

        Returns:
            List of MonteCarloScenario objects
        """
        if n_scenarios is None:
            n_scenarios = self.n_monte_carlo
        if calls_per_scenario is None:
            calls_per_scenario = self.base_annual_calls

        scenarios = []

        if scenario_name is not None:
            # Generate all scenarios from single distribution scenario
            for i in range(n_scenarios):
                calls = self.generate_vessel_call_sequence(
                    scenario_name, calls_per_scenario
                )
                total_demand = sum(v for _, v in calls)
                scenarios.append(MonteCarloScenario(
                    scenario_id=i,
                    distribution_scenario=scenario_name,
                    vessel_calls=calls,
                    total_demand=total_demand,
                    call_count=len(calls)
                ))
        else:
            # Mix scenarios based on probability
            scenario_list = list(self.distribution_scenarios.values())
            probabilities = [s.probability for s in scenario_list]
            prob_sum = sum(probabilities)
            probabilities = [p / prob_sum for p in probabilities]  # Normalize

            for i in range(n_scenarios):
                # Select distribution scenario based on probability
                selected_scenario = self.rng.choice(scenario_list, p=probabilities)

                calls = self.generate_vessel_call_sequence(
                    selected_scenario.name, calls_per_scenario
                )
                total_demand = sum(v for _, v in calls)
                scenarios.append(MonteCarloScenario(
                    scenario_id=i,
                    distribution_scenario=selected_scenario.name,
                    vessel_calls=calls,
                    total_demand=total_demand,
                    call_count=len(calls)
                ))

        return scenarios

    def get_scenario_statistics(
        self,
        mc_scenarios: List[MonteCarloScenario]
    ) -> Dict:
        """
        Compute statistics from Monte Carlo scenarios.

        Args:
            mc_scenarios: List of MonteCarloScenario objects

        Returns:
            Dict with demand statistics
        """
        demands = np.array([s.total_demand for s in mc_scenarios])

        # Group by distribution scenario
        by_scenario = {}
        for s in mc_scenarios:
            if s.distribution_scenario not in by_scenario:
                by_scenario[s.distribution_scenario] = []
            by_scenario[s.distribution_scenario].append(s.total_demand)

        return {
            "total": {
                "mean": float(np.mean(demands)),
                "std": float(np.std(demands)),
                "min": float(np.min(demands)),
                "max": float(np.max(demands)),
                "p5": float(np.percentile(demands, 5)),
                "p25": float(np.percentile(demands, 25)),
                "p50": float(np.percentile(demands, 50)),
                "p75": float(np.percentile(demands, 75)),
                "p95": float(np.percentile(demands, 95)),
            },
            "by_scenario": {
                name: {
                    "count": len(vals),
                    "mean": float(np.mean(vals)),
                    "std": float(np.std(vals))
                }
                for name, vals in by_scenario.items()
            },
            "n_scenarios": len(mc_scenarios)
        }

    def print_summary(self):
        """Print summary of vessel distribution configuration."""
        print("\n" + "="*60)
        print("Vessel Distribution Summary")
        print("="*60)

        print("\nVessel Types:")
        for vtype in self.vessel_types.values():
            print(f"  {vtype.name}: {vtype.min_volume}-{vtype.max_volume} m3 (mean: {vtype.mean_volume})")

        print("\nDistribution Scenarios:")
        for scenario in self.distribution_scenarios.values():
            weighted_avg = scenario.get_weighted_mean_volume(self.vessel_types)
            print(f"  {scenario.name} (prob={scenario.probability:.2f}):")
            for vtype, share in scenario.shares.items():
                print(f"    {vtype}: {share*100:.0f}%")
            print(f"    Weighted avg volume: {weighted_avg:.0f} m3")

        print("\nSampling Config:")
        print(f"  Monte Carlo scenarios: {self.n_monte_carlo}")
        print(f"  Method: {self.sampling_method}")
        print(f"  Random seed: {self.random_seed}")
        print("="*60)


def load_stochastic_config(config_path: str = None) -> Dict:
    """
    Load stochastic configuration from YAML file.

    Args:
        config_path: Path to stochastic.yaml (default: config/stochastic.yaml)

    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "stochastic.yaml"

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# Convenience function for quick testing
def create_vessel_distribution(base_annual_calls: int = 600) -> VesselDistribution:
    """
    Create a VesselDistribution with default stochastic config.

    Args:
        base_annual_calls: Base number of annual calls

    Returns:
        VesselDistribution instance
    """
    config = load_stochastic_config()
    return VesselDistribution(config, base_annual_calls)
