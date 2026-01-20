#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sensitivity Analysis Module - Systematic parameter sensitivity analysis.

This module provides:
- Single parameter sensitivity analysis
- Multi-parameter tornado diagrams
- Two-way sensitivity analysis
- Automatic parameter variation and result collection

Key outputs for SCI papers:
- Tornado diagrams showing relative importance of parameters
- Sensitivity tables with NPC/LCO variations
- Two-way heatmaps for critical parameter interactions

Usage:
    from src.sensitivity_analyzer import SensitivityAnalyzer
    analyzer = SensitivityAnalyzer(config, optimizer)
    result = analyzer.analyze_parameter("economy.fuel_price_usd_per_ton", [-0.2, -0.1, 0, 0.1, 0.2])
"""

import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
import pandas as pd
import numpy as np
from pathlib import Path

from .optimizer import BunkeringOptimizer
from .config_loader import load_config


@dataclass
class ParameterSensitivityResult:
    """
    Result from single parameter sensitivity analysis.

    Attributes:
        parameter_path: Config path (e.g., "economy.fuel_price_usd_per_ton")
        parameter_name: Human-readable name
        base_value: Original parameter value
        variations: List of variations applied
        values: Actual parameter values tested
        npcs: Corresponding NPC values (USD millions)
        lcos: Corresponding LCO values (USD/ton)
        elasticity: Price elasticity at base (% NPC change / % param change)
    """
    parameter_path: str
    parameter_name: str
    base_value: float
    variations: List[float] = field(default_factory=list)
    values: List[float] = field(default_factory=list)
    npcs: List[float] = field(default_factory=list)
    lcos: List[float] = field(default_factory=list)
    elasticity: float = 0.0
    base_npc: float = 0.0
    base_lco: float = 0.0

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame for export."""
        return pd.DataFrame({
            "Variation": self.variations,
            "Parameter_Value": self.values,
            "NPC_USDm": self.npcs,
            "LCO_USD_per_ton": self.lcos,
            "NPC_Change_Pct": [(npc - self.base_npc) / self.base_npc * 100 if self.base_npc else 0 for npc in self.npcs],
        })


@dataclass
class TornadoResult:
    """
    Result from tornado diagram analysis.

    Attributes:
        parameters: List of parameter names
        low_npcs: NPC values at -variation (sorted)
        high_npcs: NPC values at +variation (sorted)
        base_npc: Base case NPC
        swings: NPC swing (high - low) for each parameter
    """
    parameters: List[str] = field(default_factory=list)
    low_npcs: List[float] = field(default_factory=list)
    high_npcs: List[float] = field(default_factory=list)
    base_npc: float = 0.0
    swings: List[float] = field(default_factory=list)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame for export."""
        return pd.DataFrame({
            "Parameter": self.parameters,
            "Low_NPC_USDm": self.low_npcs,
            "High_NPC_USDm": self.high_npcs,
            "Swing_USDm": self.swings,
            "Swing_Pct": [s / self.base_npc * 100 if self.base_npc else 0 for s in self.swings],
        })


@dataclass
class TwoWaySensitivityResult:
    """
    Result from two-way sensitivity analysis.

    Attributes:
        param1_path: First parameter path
        param2_path: Second parameter path
        param1_values: Values tested for first parameter
        param2_values: Values tested for second parameter
        npc_matrix: 2D matrix of NPC values [param1 x param2]
    """
    param1_path: str
    param2_path: str
    param1_name: str
    param2_name: str
    param1_values: List[float] = field(default_factory=list)
    param2_values: List[float] = field(default_factory=list)
    npc_matrix: List[List[float]] = field(default_factory=list)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to DataFrame (pivoted table format)."""
        df = pd.DataFrame(
            self.npc_matrix,
            index=[f"{self.param1_name}={v:.2f}" for v in self.param1_values],
            columns=[f"{self.param2_name}={v:.2f}" for v in self.param2_values]
        )
        return df


class SensitivityAnalyzer:
    """
    Systematic sensitivity analysis for bunkering optimization.

    This analyzer:
    - Varies parameters one-at-a-time or in combination
    - Re-runs optimization for each variation
    - Collects NPC and LCO results
    - Generates publication-ready tables and data

    Args:
        base_config: Base configuration dictionary
        shuttle_size: Fixed shuttle size for analysis (optional)
        pump_size: Fixed pump size for analysis (optional)
    """

    def __init__(
        self,
        base_config: Dict,
        shuttle_size: Optional[float] = None,
        pump_size: Optional[float] = None
    ):
        self.base_config = base_config
        self.case_id = base_config.get("case_id", "unknown")

        # If shuttle/pump not specified, use first available
        self.shuttle_size = shuttle_size or base_config["shuttle"]["available_sizes_cbm"][0]
        self.pump_size = pump_size or base_config["pumps"]["available_flow_rates"][0]

        # Cache base result
        self._base_npc = None
        self._base_lco = None

    def _get_nested_value(self, config: Dict, path: str) -> Any:
        """Get value from nested config using dot notation."""
        keys = path.split(".")
        value = config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                raise KeyError(f"Path '{path}' not found in config")
        return value

    def _set_nested_value(self, config: Dict, path: str, value: Any) -> None:
        """Set value in nested config using dot notation."""
        keys = path.split(".")
        d = config
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value

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
        shuttle = shuttle_size or self.shuttle_size
        pump = pump_size or self.pump_size

        optimizer = BunkeringOptimizer(config)
        optimizer.shuttle_sizes = [shuttle]
        optimizer.pump_sizes = [pump]

        scenario_df, yearly_df = optimizer.solve()

        if scenario_df.empty:
            return float('inf'), float('inf')

        npc = scenario_df['NPC_Total_USDm'].iloc[0]
        lco = scenario_df.get('LCOAmmonia_USD_per_ton', pd.Series([0])).iloc[0]

        return npc, lco

    def get_base_result(self) -> Tuple[float, float]:
        """Get or calculate base case NPC and LCO."""
        if self._base_npc is None:
            self._base_npc, self._base_lco = self._run_optimization(self.base_config)
        return self._base_npc, self._base_lco

    def analyze_parameter(
        self,
        param_path: str,
        variations: List[float],
        param_name: Optional[str] = None,
        variation_type: str = "relative",
        verbose: bool = True
    ) -> ParameterSensitivityResult:
        """
        Analyze sensitivity to a single parameter.

        Args:
            param_path: Config path (e.g., "economy.fuel_price_usd_per_ton")
            variations: List of variations (-0.2 = -20%, 0.1 = +10%, etc.)
            param_name: Human-readable name (default: param_path)
            variation_type: "relative" (multiply) or "absolute" (add/replace)
            verbose: Print progress

        Returns:
            ParameterSensitivityResult with all results
        """
        if param_name is None:
            param_name = param_path.split(".")[-1]

        base_value = self._get_nested_value(self.base_config, param_path)
        base_npc, base_lco = self.get_base_result()

        if verbose:
            print(f"\nAnalyzing sensitivity: {param_name}")
            print(f"  Base value: {base_value}")
            print(f"  Variations: {variations}")

        values = []
        npcs = []
        lcos = []

        for var in variations:
            # Calculate new value
            if variation_type == "relative":
                new_value = base_value * (1 + var)
            else:
                new_value = var  # absolute value

            # Create modified config
            modified_config = copy.deepcopy(self.base_config)
            self._set_nested_value(modified_config, param_path, new_value)

            # Run optimization
            npc, lco = self._run_optimization(modified_config)

            values.append(new_value)
            npcs.append(npc)
            lcos.append(lco if lco < float('inf') else 0)

            if verbose:
                pct_change = (npc - base_npc) / base_npc * 100 if base_npc else 0
                print(f"  {var:+.0%}: value={new_value:.2f}, NPC=${npc:.2f}M ({pct_change:+.1f}%)")

        # Calculate elasticity at base
        # Use central difference if 0 is in variations
        if 0 in variations:
            idx = variations.index(0)
            if idx > 0 and idx < len(variations) - 1:
                delta_var = variations[idx + 1] - variations[idx - 1]
                delta_npc = npcs[idx + 1] - npcs[idx - 1]
                elasticity = (delta_npc / base_npc) / delta_var if base_npc and delta_var else 0
            else:
                elasticity = 0
        else:
            elasticity = 0

        return ParameterSensitivityResult(
            parameter_path=param_path,
            parameter_name=param_name,
            base_value=base_value,
            variations=variations,
            values=values,
            npcs=npcs,
            lcos=lcos,
            elasticity=elasticity,
            base_npc=base_npc,
            base_lco=base_lco,
        )

    def analyze_tornado(
        self,
        params: List[Dict],
        variation_pct: float = 0.10,
        verbose: bool = True
    ) -> TornadoResult:
        """
        Generate tornado diagram data for multiple parameters.

        Args:
            params: List of dicts with "path" and optional "name" keys
            variation_pct: Symmetric variation (default: 10%)
            verbose: Print progress

        Returns:
            TornadoResult sorted by swing magnitude
        """
        base_npc, _ = self.get_base_result()

        if verbose:
            print("\n" + "="*60)
            print(f"Tornado Diagram Analysis (+/-{variation_pct:.0%})")
            print("="*60)
            print(f"Base NPC: ${base_npc:.2f}M")

        results = []

        for param_info in params:
            path = param_info["path"]
            name = param_info.get("name", path.split(".")[-1])

            try:
                # Get low and high NPCs
                sens_result = self.analyze_parameter(
                    path,
                    variations=[-variation_pct, variation_pct],
                    param_name=name,
                    verbose=False
                )

                low_npc = sens_result.npcs[0]
                high_npc = sens_result.npcs[1]
                swing = abs(high_npc - low_npc)

                results.append({
                    "name": name,
                    "low_npc": low_npc,
                    "high_npc": high_npc,
                    "swing": swing,
                })

                if verbose:
                    print(f"  {name}: ${low_npc:.2f}M to ${high_npc:.2f}M (swing: ${swing:.2f}M)")

            except Exception as e:
                if verbose:
                    print(f"  {name}: Failed - {e}")

        # Sort by swing (descending)
        results.sort(key=lambda x: x["swing"], reverse=True)

        tornado = TornadoResult(
            parameters=[r["name"] for r in results],
            low_npcs=[r["low_npc"] for r in results],
            high_npcs=[r["high_npc"] for r in results],
            base_npc=base_npc,
            swings=[r["swing"] for r in results],
        )

        if verbose:
            print("\nRanked by Impact:")
            for i, (name, swing) in enumerate(zip(tornado.parameters, tornado.swings), 1):
                pct = swing / base_npc * 100 if base_npc else 0
                print(f"  {i}. {name}: ${swing:.2f}M ({pct:.1f}%)")
            print("="*60)

        return tornado

    def analyze_two_way(
        self,
        param1_path: str,
        param2_path: str,
        variations1: List[float],
        variations2: List[float],
        param1_name: Optional[str] = None,
        param2_name: Optional[str] = None,
        verbose: bool = True
    ) -> TwoWaySensitivityResult:
        """
        Two-way sensitivity analysis.

        Args:
            param1_path: First parameter path
            param2_path: Second parameter path
            variations1: Variations for first parameter
            variations2: Variations for second parameter
            param1_name: Name for first parameter
            param2_name: Name for second parameter
            verbose: Print progress

        Returns:
            TwoWaySensitivityResult with NPC matrix
        """
        if param1_name is None:
            param1_name = param1_path.split(".")[-1]
        if param2_name is None:
            param2_name = param2_path.split(".")[-1]

        base_value1 = self._get_nested_value(self.base_config, param1_path)
        base_value2 = self._get_nested_value(self.base_config, param2_path)

        if verbose:
            print("\n" + "="*60)
            print("Two-Way Sensitivity Analysis")
            print("="*60)
            print(f"Parameter 1: {param1_name} (base={base_value1})")
            print(f"Parameter 2: {param2_name} (base={base_value2})")

        # Calculate actual values
        values1 = [base_value1 * (1 + v) for v in variations1]
        values2 = [base_value2 * (1 + v) for v in variations2]

        # Build NPC matrix
        npc_matrix = []

        for i, (var1, val1) in enumerate(zip(variations1, values1)):
            row = []
            for j, (var2, val2) in enumerate(zip(variations2, values2)):
                # Create modified config
                modified_config = copy.deepcopy(self.base_config)
                self._set_nested_value(modified_config, param1_path, val1)
                self._set_nested_value(modified_config, param2_path, val2)

                # Run optimization
                npc, _ = self._run_optimization(modified_config)
                row.append(npc)

                if verbose:
                    print(f"  [{i+1},{j+1}] {param1_name}={val1:.2f}, {param2_name}={val2:.2f}: ${npc:.2f}M")

            npc_matrix.append(row)

        result = TwoWaySensitivityResult(
            param1_path=param1_path,
            param2_path=param2_path,
            param1_name=param1_name,
            param2_name=param2_name,
            param1_values=values1,
            param2_values=values2,
            npc_matrix=npc_matrix,
        )

        if verbose:
            print("="*60)

        return result

    def run_full_analysis(
        self,
        output_dir: Optional[str] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run complete sensitivity analysis suite.

        Args:
            output_dir: Optional directory for saving results
            verbose: Print progress

        Returns:
            Dict with all analysis results
        """
        results = {}

        # 1. Single parameter analyses
        single_params = [
            {"path": "economy.fuel_price_usd_per_ton", "name": "Fuel Price"},
            {"path": "operations.max_annual_hours_per_vessel", "name": "Max Annual Hours"},
            {"path": "operations.travel_time_hours", "name": "Travel Time"},
            {"path": "bunkering.bunker_volume_per_call_m3", "name": "Bunker Volume"},
        ]

        single_results = {}
        for param in single_params:
            try:
                result = self.analyze_parameter(
                    param["path"],
                    variations=[-0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30],
                    param_name=param["name"],
                    verbose=verbose
                )
                single_results[param["name"]] = result
            except Exception as e:
                if verbose:
                    print(f"  Failed: {param['name']} - {e}")

        results["single_parameter"] = single_results

        # 2. Tornado diagram
        tornado_params = [
            {"path": "economy.fuel_price_usd_per_ton", "name": "Fuel Price"},
            {"path": "operations.max_annual_hours_per_vessel", "name": "Max Hours"},
            {"path": "operations.travel_time_hours", "name": "Travel Time"},
            {"path": "bunkering.bunker_volume_per_call_m3", "name": "Bunker Volume"},
            {"path": "propulsion.sfoc_g_per_kwh", "name": "SFOC"},
        ]

        results["tornado"] = self.analyze_tornado(tornado_params, verbose=verbose)

        # 3. Two-way analysis (fuel price vs bunker volume)
        results["two_way"] = self.analyze_two_way(
            "economy.fuel_price_usd_per_ton",
            "bunkering.bunker_volume_per_call_m3",
            variations1=[-0.20, -0.10, 0, 0.10, 0.20],
            variations2=[-0.20, -0.10, 0, 0.10, 0.20],
            param1_name="Fuel Price",
            param2_name="Bunker Volume",
            verbose=verbose
        )

        # Save results if output_dir specified
        if output_dir:
            self._save_results(results, output_dir)

        return results

    def _save_results(self, results: Dict, output_dir: str) -> None:
        """Save analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save single parameter results
        for name, result in results.get("single_parameter", {}).items():
            df = result.to_dataframe()
            safe_name = name.replace(" ", "_").lower()
            df.to_csv(output_path / f"sensitivity_{safe_name}_{self.case_id}.csv", index=False)

        # Save tornado
        if "tornado" in results:
            df = results["tornado"].to_dataframe()
            df.to_csv(output_path / f"tornado_{self.case_id}.csv", index=False)

        # Save two-way
        if "two_way" in results:
            df = results["two_way"].to_dataframe()
            df.to_csv(output_path / f"two_way_{self.case_id}.csv")

        print(f"\n[OK] Results saved to {output_path}")


def run_sensitivity_analysis(
    case_id: str = "case_1",
    shuttle_size: Optional[float] = None,
    pump_size: Optional[float] = None,
    output_dir: Optional[str] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to run sensitivity analysis.

    Args:
        case_id: Case identifier
        shuttle_size: Fixed shuttle size (optional)
        pump_size: Fixed pump size (optional)
        output_dir: Output directory (optional)
        verbose: Print progress

    Returns:
        Dict with all analysis results
    """
    config = load_config(case_id)

    analyzer = SensitivityAnalyzer(
        base_config=config,
        shuttle_size=shuttle_size,
        pump_size=pump_size
    )

    return analyzer.run_full_analysis(output_dir=output_dir, verbose=verbose)


def analyze_pump_rate_sensitivity(
    case_id: str = "case_1",
    pump_rates: Optional[List[float]] = None,
    shuttle_sizes: Optional[List[float]] = None,
    output_dir: Optional[str] = None,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Analyze NPC sensitivity to pump rate variations.

    Runs optimization for each pump rate, finding optimal shuttle at each point.
    This generates data for the S7 figure in the paper.

    Args:
        case_id: Case identifier (e.g., "case_1", "case_2_yeosu", "case_2_ulsan")
        pump_rates: List of pump rates to test (default: config sensitivity_flow_rates)
        shuttle_sizes: Shuttle sizes to test (default: from case config)
        output_dir: Output directory for CSV results (optional)
        verbose: Print progress

    Returns:
        DataFrame with columns: Pump_Rate_m3ph, Min_NPC_USDm, Optimal_Shuttle_cbm, LCO_USD_per_ton
    """
    config = load_config(case_id)

    # Get pump rates from config if not specified
    if pump_rates is None:
        pump_rates = config.get("pumps", {}).get("sensitivity_flow_rates", [1000])

    # Get shuttle sizes from config if not specified
    if shuttle_sizes is None:
        shuttle_sizes = config["shuttle"]["available_sizes_cbm"]

    if verbose:
        print("\n" + "=" * 60)
        print(f"Pump Rate Sensitivity Analysis: {case_id}")
        print("=" * 60)
        print(f"Pump rates: {pump_rates}")
        print(f"Shuttle sizes: {shuttle_sizes}")

    results = []

    for pump_rate in pump_rates:
        if verbose:
            print(f"\n[INFO] Testing pump rate: {pump_rate} m3/h")

        # Create modified config with single pump rate
        modified_config = copy.deepcopy(config)
        modified_config["pumps"]["available_flow_rates"] = [pump_rate]

        # Run optimization
        optimizer = BunkeringOptimizer(modified_config)
        scenario_df, _ = optimizer.solve()

        if scenario_df.empty:
            if verbose:
                print(f"  [WARN] No feasible solution for pump rate {pump_rate}")
            continue

        # Find minimum NPC
        best_idx = scenario_df['NPC_Total_USDm'].idxmin()
        best_row = scenario_df.loc[best_idx]

        result = {
            'Pump_Rate_m3ph': pump_rate,
            'Min_NPC_USDm': best_row['NPC_Total_USDm'],
            'Optimal_Shuttle_cbm': int(best_row['Shuttle_Size_cbm']),
            'LCO_USD_per_ton': best_row.get('LCOAmmonia_USD_per_ton', 0),
        }
        results.append(result)

        if verbose:
            print(f"  [OK] Min NPC: ${result['Min_NPC_USDm']:.2f}M "
                  f"(Shuttle: {result['Optimal_Shuttle_cbm']} m3)")

    # Create DataFrame
    df = pd.DataFrame(results)

    # Save if output_dir specified
    if output_dir and not df.empty:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        csv_path = output_path / f"pump_sensitivity_{case_id}.csv"
        df.to_csv(csv_path, index=False)
        if verbose:
            print(f"\n[OK] Saved to {csv_path}")

    if verbose:
        print("\n" + "=" * 60)
        print("Summary:")
        print(df.to_string(index=False))
        print("=" * 60)

    return df
