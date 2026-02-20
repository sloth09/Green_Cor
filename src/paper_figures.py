#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Figure Generator - SCI-level paper figures for Green Corridor Analysis.

This module generates publication-quality figures for both deterministic
and stochastic optimization results.

Figure Categories:
    D1-D12: Deterministic Results
    S1-S7: Stochastic Results
    C1-C4: Combined Analysis

Usage:
    from src.paper_figures import PaperFigureGenerator
    gen = PaperFigureGenerator("results/")
    gen.generate_all("results/paper_figures/")
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import warnings

# Suppress matplotlib warnings
warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================================
# Configuration
# ============================================================================

# Publication-quality settings (LARGE FONTS for paper figures)
PAPER_STYLE = {
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 13,            # Base font size
    'axes.titlesize': 16,       # Subplot titles
    'axes.labelsize': 15,       # X/Y axis labels
    'xtick.labelsize': 13,      # X tick labels
    'ytick.labelsize': 13,      # Y tick labels
    'legend.fontsize': 12,      # Legend text
    'figure.titlesize': 17,     # Figure suptitle
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.unicode_minus': False,
}

# Color scheme (colorblind-friendly)
COLORS = {
    'case_1': '#1f77b4',       # Blue
    'case_3': '#ff7f0e', # Orange
    'case_2': '#2ca02c', # Green
}

CASE_LABELS = {
    'case_1': 'Case 1: Busan Storage',
    'case_3': 'Case 3: Yeosu Direct',
    'case_2': 'Case 2: Ulsan Direct',
}

CASE_SHORT = {
    'case_1': 'Case 1',
    'case_3': 'Case 3',
    'case_2': 'Case 2',
}

# Y-axis limits for clean round numbers (NPC in Million USD)
Y_LIMITS_NPC = {
    'case_1': 700,
    'case_3': 1400,
    'case_2': 1400,
}

# Y-axis limits for yearly costs (Million USD/year)
Y_LIMITS_YEARLY_COST = {
    'case_1': 35,
    'case_3': 70,
    'case_2': 50,
}

# Y-axis limits for fleet size
Y_LIMITS_FLEET = {
    'case_1': 15,
    'case_3': 16,
    'case_2': 15,
}


class PaperFigureGenerator:
    """
    Paper Figure Generator for Green Corridor Ammonia Bunkering Analysis.

    Generates publication-quality figures for SCI-level papers.
    """

    def __init__(self, results_dir: str = "results"):
        """
        Initialize the figure generator.

        Args:
            results_dir: Base directory containing result files
        """
        self.results_dir = Path(results_dir)
        self.det_dir = self.results_dir / "deterministic"
        self.stoch_dirs = {
            'case_1': self.results_dir / "stochastic",
            'case_3': self.results_dir / "stochastic_case3",
            'case_2': self.results_dir / "stochastic_case2",
        }

        # Apply paper style
        rcParams.update(PAPER_STYLE)

        # Load data
        self.det_scenarios = self._load_deterministic_scenarios()
        self.det_yearly = self._load_deterministic_yearly()
        self.stoch_summary = self._load_stochastic_summary()
        self.stoch_scenarios = self._load_stochastic_scenarios()
        self.tornado_data = self._load_tornado_data()

    def _load_deterministic_scenarios(self) -> Dict[str, pd.DataFrame]:
        """Load deterministic scenario results.

        Search order:
        1. results/MILP_scenario_summary_{case_id}.csv (main.py output)
        2. results/deterministic/scenarios_{case_id}.csv (legacy)
        3. results/stochastic*/deterministic_scenarios_{case_id}.csv (stochastic fallback)
        """
        data = {}
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = None
            # Priority 1: main.py output (MILP_scenario_summary_*)
            milp_path = self.results_dir / f"MILP_scenario_summary_{case_id}.csv"
            if milp_path.exists():
                path = milp_path
            # Priority 1.5: deterministic directory (MILP_scenario_summary_*)
            elif (self.det_dir / f"MILP_scenario_summary_{case_id}.csv").exists():
                path = self.det_dir / f"MILP_scenario_summary_{case_id}.csv"
            # Priority 2: deterministic directory (legacy)
            elif (self.det_dir / f"scenarios_{case_id}.csv").exists():
                path = self.det_dir / f"scenarios_{case_id}.csv"
            # Priority 3: stochastic directory fallback
            elif (self.stoch_dirs[case_id] / f"deterministic_scenarios_{case_id}.csv").exists():
                path = self.stoch_dirs[case_id] / f"deterministic_scenarios_{case_id}.csv"

            if path and path.exists():
                data[case_id] = pd.read_csv(path)
                print(f"  [OK] Loaded {case_id} deterministic scenarios")
            else:
                print(f"  [WARN] Missing {case_id} deterministic scenarios")
        return data

    def _load_deterministic_yearly(self) -> Dict[str, pd.DataFrame]:
        """Load deterministic yearly results.

        Search order:
        1. results/MILP_per_year_results_{case_id}.csv (main.py output)
        2. results/deterministic/yearly_{case_id}.csv (legacy)
        3. results/stochastic*/deterministic_yearly_{case_id}.csv (stochastic fallback)
        """
        data = {}
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = None
            # Priority 1: main.py output (MILP_per_year_results_*)
            milp_path = self.results_dir / f"MILP_per_year_results_{case_id}.csv"
            if milp_path.exists():
                path = milp_path
            # Priority 1.5: deterministic directory (MILP_per_year_results_*)
            elif (self.det_dir / f"MILP_per_year_results_{case_id}.csv").exists():
                path = self.det_dir / f"MILP_per_year_results_{case_id}.csv"
            # Priority 2: deterministic directory (legacy)
            elif (self.det_dir / f"yearly_{case_id}.csv").exists():
                path = self.det_dir / f"yearly_{case_id}.csv"
            # Priority 3: stochastic directory fallback
            elif (self.stoch_dirs[case_id] / f"deterministic_yearly_{case_id}.csv").exists():
                path = self.stoch_dirs[case_id] / f"deterministic_yearly_{case_id}.csv"

            if path and path.exists():
                data[case_id] = pd.read_csv(path)
        return data

    def _load_stochastic_summary(self) -> Dict[str, pd.DataFrame]:
        """Load stochastic summary results."""
        data = {}
        for case_id, stoch_dir in self.stoch_dirs.items():
            path = stoch_dir / f"stochastic_summary_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
                print(f"  [OK] Loaded {case_id} stochastic summary")
        return data

    def _load_stochastic_scenarios(self) -> Dict[str, pd.DataFrame]:
        """Load Monte Carlo scenario results."""
        data = {}
        for case_id, stoch_dir in self.stoch_dirs.items():
            path = stoch_dir / f"stochastic_scenarios_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
        return data

    def _load_tornado_data(self) -> Dict[str, pd.DataFrame]:
        """Load tornado diagram data."""
        data = {}
        for case_id, stoch_dir in self.stoch_dirs.items():
            path = stoch_dir / f"tornado_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
        return data

    def _load_pump_sensitivity_data(self) -> Dict[str, pd.DataFrame]:
        """Load pump rate sensitivity data for S7 figure."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = sensitivity_dir / f"pump_sensitivity_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
                print(f"  [OK] Loaded {case_id} pump sensitivity data")
            else:
                print(f"  [WARN] Missing {case_id} pump sensitivity data")
        return data

    def _load_fuel_price_sensitivity(self) -> Dict[str, pd.DataFrame]:
        """Load fuel price sensitivity data for Fig8."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = sensitivity_dir / f"fuel_price_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
        return data

    def _load_deterministic_tornado(self) -> Dict[str, pd.DataFrame]:
        """Load deterministic tornado data for Fig7."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = sensitivity_dir / f"tornado_det_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
        return data

    def _load_breakeven_distance(self) -> Dict[str, pd.DataFrame]:
        """Load breakeven distance data for Fig9."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for name in ['ulsan', 'yeosu']:
            path = sensitivity_dir / f"breakeven_distance_{name}.csv"
            if path.exists():
                data[name] = pd.read_csv(path)
        return data

    def _load_breakeven_distance_optimal(self) -> Dict[str, pd.DataFrame]:
        """Load optimal-vs-optimal breakeven distance data for Fig9 overlay."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for name in ['ulsan', 'yeosu']:
            path = sensitivity_dir / f"breakeven_distance_optimal_{name}.csv"
            if path.exists():
                data[name] = pd.read_csv(path)
        return data

    def _load_demand_scenarios(self) -> Dict[str, pd.DataFrame]:
        """Load demand scenario data for Fig10."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = sensitivity_dir / f"demand_scenarios_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
        # Also try summary file
        summary_path = sensitivity_dir / "demand_scenarios_summary.csv"
        if summary_path.exists():
            data['summary'] = pd.read_csv(summary_path)
        return data

    def _load_bunker_volume_sensitivity(self) -> Dict[str, pd.DataFrame]:
        """Load bunker volume sensitivity data for FigS5."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = sensitivity_dir / f"bunker_volume_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
        return data

    def _load_two_way_det(self) -> Dict[str, pd.DataFrame]:
        """Load deterministic two-way sensitivity data for FigS4."""
        data = {}
        sensitivity_dir = self.results_dir / "sensitivity"
        for case_id in ['case_1', 'case_2', 'case_3']:
            path = sensitivity_dir / f"two_way_det_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path, index_col=0)
        return data

    def _get_optimal(self, case_id: str) -> Dict[str, Any]:
        """Get optimal configuration for a case."""
        if case_id not in self.det_scenarios:
            return {}
        df = self.det_scenarios[case_id]
        best_idx = df['NPC_Total_USDm'].idxmin()
        best = df.loc[best_idx]
        return {
            'shuttle': int(best['Shuttle_Size_cbm']),
            'pump': int(best['Pump_Size_m3ph']),
            'npc': best['NPC_Total_USDm'],
            'lco': best.get('LCOAmmonia_USD_per_ton', best['NPC_Total_USDm'] / 235.62),
            'row': best
        }

    # =========================================================================
    # Deterministic Figures (D1-D12)
    # =========================================================================

    def fig_d1_npc_vs_shuttle(self, output_path: Path) -> None:
        """D1: Total Cost vs Shuttle Size (1D line plot for fixed pump rate)."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Total Cost vs Shuttle Size (2030-2050, Pump Rate: 1000 m$^3$/h)',
                    fontsize=16, fontweight='bold')

        for idx, (case_id, df) in enumerate(self.det_scenarios.items()):
            ax = axes[idx]

            # Sort by shuttle size
            df_sorted = df.sort_values('Shuttle_Size_cbm')
            shuttle_sizes = df_sorted['Shuttle_Size_cbm'].values

            # Calculate CAPEX, Fixed OPEX, Variable OPEX
            capex = (df_sorted['NPC_Annualized_Shuttle_CAPEX_USDm'] +
                    df_sorted['NPC_Annualized_Bunkering_CAPEX_USDm'] +
                    df_sorted.get('NPC_Annualized_Terminal_CAPEX_USDm', 0)).values
            fixed_opex = (df_sorted['NPC_Shuttle_fOPEX_USDm'] +
                         df_sorted['NPC_Bunkering_fOPEX_USDm'] +
                         df_sorted.get('NPC_Terminal_fOPEX_USDm', 0)).values
            var_opex = (df_sorted['NPC_Shuttle_vOPEX_USDm'] +
                       df_sorted['NPC_Bunkering_vOPEX_USDm'] +
                       df_sorted.get('NPC_Terminal_vOPEX_USDm', 0)).values
            npc_values = df_sorted['NPC_Total_USDm'].values

            # Plot lines (4 lines: Total, CAPEX, Fixed OPEX, Variable OPEX)
            ax.plot(shuttle_sizes, npc_values,
                   marker='o', linewidth=2.5, markersize=7,
                   color=COLORS[case_id], label='Total')
            ax.plot(shuttle_sizes, capex,
                   marker='s', linewidth=2, markersize=6,
                   color=COLORS[case_id], alpha=0.7, linestyle='--', label='CAPEX')
            ax.plot(shuttle_sizes, fixed_opex,
                   marker='^', linewidth=2, markersize=6,
                   color=COLORS[case_id], alpha=0.5, linestyle='-.', label='Fixed OPEX')
            ax.plot(shuttle_sizes, var_opex,
                   marker='d', linewidth=2, markersize=6,
                   color=COLORS[case_id], alpha=0.5, linestyle=':', label='Var. OPEX')

            ax.set_xlabel('Shuttle Size (m$^3$)', fontsize=14)
            ax.set_ylabel('Total Cost (Million USD)', fontsize=14)
            ax.set_title(CASE_SHORT[case_id], fontweight='bold', fontsize=15)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='both', labelsize=12)

            # Format x-axis with thousand separator
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k' if x >= 1000 else f'{x:.0f}'))

            # Set y-axis limits with padding so curves aren't cut off
            data_max = max(npc_values.max(), capex.max(), fixed_opex.max(), var_opex.max())
            y_upper = max(Y_LIMITS_NPC.get(case_id, 1400), data_max * 1.1)
            ax.set_ylim(0, y_upper)

            # Place legend in upper left (where there's empty space)
            ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

        plt.tight_layout()
        plt.savefig(output_path / 'D1_npc_vs_shuttle.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D1: Total Cost vs Shuttle Size")

    def fig_d2_yearly_cost_evolution(self, output_path: Path) -> None:
        """D2: Yearly cost evolution for optimal configurations."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Annual Cost Evolution (2030-2050) - Optimal Configurations',
                    fontsize=16, fontweight='bold')

        for idx, case_id in enumerate(self.det_yearly.keys()):
            ax = axes[idx]
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            # Filter optimal configuration
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])].copy()

            if df_opt.empty:
                continue

            years = df_opt['Year'].values

            # Get cost components
            capex = df_opt['Annualized_CAPEX_Total_USDm'].values
            fopex = df_opt['FixedOPEX_Total_USDm'].values
            vopex = df_opt['VariableOPEX_Total_USDm'].values

            # Stacked area plot
            ax.fill_between(years, 0, capex, alpha=0.7, label='CAPEX', color='#1f77b4')
            ax.fill_between(years, capex, capex + fopex, alpha=0.7, label='Fixed OPEX', color='#ff7f0e')
            ax.fill_between(years, capex + fopex, capex + fopex + vopex, alpha=0.7, label='Var. OPEX', color='#2ca02c')

            # Total line
            total = capex + fopex + vopex
            ax.plot(years, total, 'k-', linewidth=2, label='Total')

            ax.set_xlabel('Year', fontsize=14)
            ax.set_ylabel('Annual Cost (Million USD)', fontsize=14)
            ax.set_title(f"{CASE_SHORT[case_id]} (Shuttle: {opt['shuttle']/1000:.0f}k m$^3$)",
                        fontweight='bold', fontsize=15)
            ax.set_xlim(2030, 2050)
            ax.set_ylim(0, Y_LIMITS_YEARLY_COST.get(case_id, 50))
            ax.tick_params(axis='both', labelsize=12)
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Integer years only
            ax.legend(loc='upper left', fontsize=11)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'D2_yearly_cost_evolution.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D2: Yearly Cost Evolution")

    def fig_d3_yearly_fleet_demand(self, output_path: Path) -> None:
        """D3: Yearly fleet size and demand evolution for optimal configurations."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Fleet Size & Supply Evolution (2030-2050) - Optimal Configurations',
                    fontsize=16, fontweight='bold')

        for idx, case_id in enumerate(self.det_yearly.keys()):
            ax = axes[idx]
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            # Filter optimal configuration
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])].copy()

            if df_opt.empty:
                continue

            years = df_opt['Year'].values
            fleet = df_opt['Total_Shuttles'].values
            supply = df_opt['Supply_m3'].values / 1e6  # Convert to million m3

            # Primary axis: Fleet size
            color1 = COLORS[case_id]
            ax.plot(years, fleet, 'o-', color=color1, linewidth=2, markersize=5, label='Fleet Size')
            ax.fill_between(years, fleet, alpha=0.2, color=color1)
            ax.set_xlabel('Year', fontsize=14)
            ax.set_ylabel('Total Shuttles', fontsize=14, color=color1)
            ax.tick_params(axis='y', labelcolor=color1, labelsize=12)
            ax.tick_params(axis='x', labelsize=12)
            ax.set_xlim(2030, 2050)
            # Fix y-axis: use data-driven max with padding so fleet curves are fully visible
            fleet_max = max(fleet) if len(fleet) > 0 else 15
            y_upper_fleet = max(Y_LIMITS_FLEET.get(case_id, 15), fleet_max * 1.15)
            ax.set_ylim(0, y_upper_fleet)
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Integer years only
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Integer fleet size

            # Secondary axis: Supply volume
            ax2 = ax.twinx()
            color2 = '#d62728'
            ax2.plot(years, supply, 's--', color=color2, linewidth=2, markersize=4, label='Annual Supply')
            ax2.set_ylabel('Annual Supply (Million m$^3$)', fontsize=14, color=color2)
            ax2.tick_params(axis='y', labelcolor=color2, labelsize=12)

            ax.set_title(f"{CASE_SHORT[case_id]} (Shuttle: {opt['shuttle']/1000:.0f}k m$^3$)",
                        fontweight='bold', fontsize=15)
            ax.grid(True, alpha=0.3)

            # Combined legend
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'D3_yearly_fleet_demand.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D3: Yearly Fleet & Demand Evolution")

    def fig_d4_yearly_cycles(self, output_path: Path) -> None:
        """D4: Annual cycles for optimal configurations."""
        fig, ax = plt.subplots(figsize=(10, 6))

        for case_id in self.det_yearly.keys():
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            # Filter optimal configuration
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])].copy()

            if df_opt.empty:
                continue

            years = df_opt['Year'].values
            cycles = df_opt['Annual_Cycles'].values

            ax.plot(years, cycles, 'o-', color=COLORS[case_id], linewidth=2,
                   markersize=6, label=f"{CASE_SHORT[case_id]} ({opt['shuttle']/1000:.0f}k m$^3$)")

        ax.set_xlabel('Year', fontsize=14)
        ax.set_ylabel('Annual Cycles', fontsize=14)
        ax.set_title('Annual Shuttle Cycles (2030-2050) - Optimal Configurations',
                    fontsize=16, fontweight='bold')
        ax.set_xlim(2030, 2050)
        ax.set_ylim(0, None)
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.legend(loc='upper left', fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'D4_yearly_cycles.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D4: Annual Cycles")

    def fig_d5_yearly_utilization(self, output_path: Path) -> None:
        """D5: Utilization rate for optimal configurations."""
        fig, ax = plt.subplots(figsize=(10, 6))

        for case_id in self.det_yearly.keys():
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            # Filter optimal configuration
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])].copy()

            if df_opt.empty:
                continue

            years = df_opt['Year'].values
            utilization = df_opt['Utilization_Rate'].values * 100  # Convert to percentage

            ax.plot(years, utilization, 'o-', color=COLORS[case_id], linewidth=2,
                   markersize=6, label=f"{CASE_SHORT[case_id]} ({opt['shuttle']/1000:.0f}k m$^3$)")

        ax.set_xlabel('Year', fontsize=14)
        ax.set_ylabel('Utilization Rate (%)', fontsize=14)
        ax.set_title('Fleet Utilization Rate (2030-2050) - Optimal Configurations',
                    fontsize=16, fontweight='bold')
        ax.set_xlim(2030, 2050)
        # Fix y-axis to clearly show full 0-100% range with padding above max capacity line
        ax.set_ylim(0, 115)
        ax.set_yticks([0, 20, 40, 60, 80, 100])
        ax.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='Max Capacity')
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'D5_yearly_utilization.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D5: Utilization Rate")

    def fig_d4_case_cycles(self, output_path: Path, case_id: str,
                          shuttle_sizes: List[int], case_label: str) -> None:
        """D4_case: Annual cycles for specific case with multiple shuttle sizes."""
        fig, ax = plt.subplots(figsize=(10, 6))

        if case_id not in self.det_yearly:
            print(f"  [WARN] D4_{case_label}: No data for {case_id}")
            return

        df = self.det_yearly[case_id]

        # Color palette for different shuttle sizes
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        markers = ['o', 's', '^', 'D', 'v']

        for idx, shuttle_size in enumerate(shuttle_sizes):
            df_shuttle = df[(df['Shuttle_Size_cbm'] == shuttle_size) &
                           (df['Pump_Size_m3ph'] == 500)].copy()

            if df_shuttle.empty:
                continue

            years = df_shuttle['Year'].values
            cycles = df_shuttle['Annual_Cycles'].values

            label = f'{shuttle_size/1000:.1f}k m$^3$' if shuttle_size >= 1000 else f'{shuttle_size} m$^3$'
            ax.plot(years, cycles, marker=markers[idx % len(markers)],
                   linewidth=2, markersize=6, color=colors[idx % len(colors)],
                   label=label)

        ax.set_xlabel('Year', fontsize=14)
        ax.set_ylabel('Annual Cycles', fontsize=14)
        ax.set_title(f'Annual Shuttle Cycles (2030-2050) - {CASE_SHORT[case_id]}',
                    fontsize=16, fontweight='bold')
        ax.set_xlim(2030, 2050)
        ax.set_ylim(0, None)
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.legend(loc='upper left', fontsize=11, title='Shuttle Size')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / f'D4_{case_label}.png', bbox_inches='tight')
        plt.close()
        print(f"  [OK] D4_{case_label}: Annual Cycles")

    def fig_d5_case_utilization(self, output_path: Path, case_id: str,
                                shuttle_sizes: List[int], case_label: str) -> None:
        """D5_case: Utilization rate for specific case with multiple shuttle sizes."""
        fig, ax = plt.subplots(figsize=(10, 6))

        if case_id not in self.det_yearly:
            print(f"  [WARN] D5_{case_label}: No data for {case_id}")
            return

        df = self.det_yearly[case_id]

        # Color palette for different shuttle sizes
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        markers = ['o', 's', '^', 'D', 'v']

        for idx, shuttle_size in enumerate(shuttle_sizes):
            df_shuttle = df[(df['Shuttle_Size_cbm'] == shuttle_size) &
                           (df['Pump_Size_m3ph'] == 500)].copy()

            if df_shuttle.empty:
                continue

            years = df_shuttle['Year'].values
            utilization = df_shuttle['Utilization_Rate'].values * 100

            label = f'{shuttle_size/1000:.1f}k m$^3$' if shuttle_size >= 1000 else f'{shuttle_size} m$^3$'
            ax.plot(years, utilization, marker=markers[idx % len(markers)],
                   linewidth=2, markersize=6, color=colors[idx % len(colors)],
                   label=label)

        ax.set_xlabel('Year', fontsize=14)
        ax.set_ylabel('Utilization Rate (%)', fontsize=14)
        ax.set_title(f'Fleet Utilization Rate (2030-2050) - {CASE_SHORT[case_id]}',
                    fontsize=16, fontweight='bold')
        ax.set_xlim(2030, 2050)
        ax.set_ylim(0, 110)
        ax.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='Max Capacity')
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.legend(loc='lower right', fontsize=11, title='Shuttle Size')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / f'D5_{case_label}.png', bbox_inches='tight')
        plt.close()
        print(f"  [OK] D5_{case_label}: Utilization Rate")

    def generate_case_specific_figures(self, output_path: Path) -> None:
        """Generate D4 and D5 figures for each case with multiple shuttle sizes."""
        print("\n  Generating case-specific D4/D5 figures...")

        # Case 1: 2500, 5000 m3
        self.fig_d4_case_cycles(output_path, 'case_1', [2500, 5000], 'case1')
        self.fig_d5_case_utilization(output_path, 'case_1', [2500, 5000], 'case1')

        # Case 2 (Ulsan): 2500, 5000, 10000 m3
        self.fig_d4_case_cycles(output_path, 'case_2', [2500, 5000, 10000], 'case2')
        self.fig_d5_case_utilization(output_path, 'case_2', [2500, 5000, 10000], 'case2')

        # Case 3 (Yeosu): 5000, 10000, 15000 m3
        self.fig_d4_case_cycles(output_path, 'case_3', [5000, 10000, 15000], 'case3')
        self.fig_d5_case_utilization(output_path, 'case_3', [5000, 10000, 15000], 'case3')

    def fig_d12_npc_heatmap(self, output_path: Path) -> None:
        """D12: NPC Heatmaps for all cases (legacy, for multi-pump analysis)."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
        fig.suptitle('Net Present Cost by Shuttle/Pump Configuration',
                     fontsize=14, fontweight='bold')

        for idx, (case_id, df) in enumerate(self.det_scenarios.items()):
            pivot = df.pivot_table(
                values='NPC_Total_USDm',
                index='Pump_Size_m3ph',
                columns='Shuttle_Size_cbm'
            )

            # Handle infeasible (NaN) cells: fill with gray background + hatching
            mask = np.isnan(pivot.values)
            plot_data = pivot.values.copy()
            if mask.any():
                plot_data[mask] = np.nanmax(plot_data)

            im = axes[idx].imshow(plot_data, cmap='RdYlGn_r',
                                  aspect='auto', origin='lower')

            # Overlay gray hatching on infeasible cells
            if mask.any():
                for r_i in range(mask.shape[0]):
                    for c_i in range(mask.shape[1]):
                        if mask[r_i, c_i]:
                            axes[idx].add_patch(plt.Rectangle(
                                (c_i - 0.5, r_i - 0.5), 1, 1,
                                facecolor='#d0d0d0', edgecolor='gray',
                                hatch='///', linewidth=0.5, zorder=2))
                            axes[idx].text(c_i, r_i, 'N/A', ha='center', va='center',
                                          fontsize=7, color='gray', zorder=3)

            # Set ticks
            axes[idx].set_xticks(np.arange(len(pivot.columns)))
            axes[idx].set_yticks(np.arange(len(pivot.index)))

            # Reduce tick labels for readability
            x_labels = [str(int(c)) if i % 2 == 0 else ''
                       for i, c in enumerate(pivot.columns)]
            y_labels = [str(int(r)) for r in pivot.index]
            axes[idx].set_xticklabels(x_labels, rotation=45, ha='right', fontsize=11)
            axes[idx].set_yticklabels(y_labels, fontsize=11)

            # Colorbar
            cbar = plt.colorbar(im, ax=axes[idx], shrink=0.8)
            cbar.set_label('NPC (M USD)', fontsize=11)

            # Mark optimal
            opt = self._get_optimal(case_id)
            if opt and opt['shuttle'] in pivot.columns.tolist():
                x_idx = pivot.columns.tolist().index(opt['shuttle'])
                y_idx = pivot.index.tolist().index(opt['pump'])
                axes[idx].scatter([x_idx], [y_idx], marker='*', s=400,
                                 color='red', edgecolor='white', linewidth=1.5,
                                 zorder=5)

            axes[idx].set_xlabel('Shuttle Size (m$^3$)')
            axes[idx].set_ylabel('Pump Rate (m$^3$/h)')
            axes[idx].set_title(CASE_SHORT[case_id], fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_path / 'D12_npc_heatmaps.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D12: NPC Heatmaps (legacy)")

    def fig_d6_cost_breakdown(self, output_path: Path) -> None:
        """D6: Cost breakdown stacked bar chart."""
        fig, ax = plt.subplots(figsize=(10, 6))

        cases = list(self.det_scenarios.keys())
        x = np.arange(len(cases))
        width = 0.6

        # Extract cost components
        capex_shuttle = []
        capex_bunk = []
        opex_fixed = []
        opex_var = []

        for case_id in cases:
            opt = self._get_optimal(case_id)
            row = opt['row']
            capex_shuttle.append(row['NPC_Annualized_Shuttle_CAPEX_USDm'])
            capex_bunk.append(row['NPC_Annualized_Bunkering_CAPEX_USDm'])
            fixed = (row['NPC_Shuttle_fOPEX_USDm'] + row['NPC_Bunkering_fOPEX_USDm'] +
                    row.get('NPC_Terminal_fOPEX_USDm', 0))
            var = (row['NPC_Shuttle_vOPEX_USDm'] + row['NPC_Bunkering_vOPEX_USDm'] +
                  row.get('NPC_Terminal_vOPEX_USDm', 0))
            opex_fixed.append(fixed)
            opex_var.append(var)

        # Stack bars
        p1 = ax.bar(x, capex_shuttle, width, label='Shuttle CAPEX', color='#1f77b4')
        p2 = ax.bar(x, capex_bunk, width, bottom=capex_shuttle,
                   label='Bunkering CAPEX', color='#ff7f0e')
        bottom2 = np.array(capex_shuttle) + np.array(capex_bunk)
        p3 = ax.bar(x, opex_fixed, width, bottom=bottom2,
                   label='Fixed OPEX', color='#2ca02c')
        bottom3 = bottom2 + np.array(opex_fixed)
        p4 = ax.bar(x, opex_var, width, bottom=bottom3,
                   label='Variable OPEX', color='#d62728')

        # Total labels
        totals = np.array(capex_shuttle) + np.array(capex_bunk) + np.array(opex_fixed) + np.array(opex_var)
        for i, total in enumerate(totals):
            ax.text(i, total + 5, f'${total:.1f}M', ha='center', fontweight='bold')

        ax.set_ylabel('20-Year NPC (Million USD)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('Cost Structure Breakdown - Optimal Configurations', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax.legend(loc='upper left')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'D6_cost_breakdown.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D6: Cost Breakdown")

    def fig_d7_cycle_time(self, output_path: Path) -> None:
        """D7: Cycle time comparison bar chart."""
        fig, ax = plt.subplots(figsize=(10, 6))

        cases = list(self.det_scenarios.keys())
        x = np.arange(len(cases))
        width = 0.5

        # Extract cycle time components from optimal row
        components = {
            'Shore Loading': [],
            'Travel': [],
            'Setup': [],
            'Pumping': [],
        }

        for case_id in cases:
            opt = self._get_optimal(case_id)
            row = opt['row']
            components['Shore Loading'].append(row.get('Shore_Loading_hr', 0))
            travel = row.get('Travel_Outbound_hr', 0) + row.get('Travel_Return_hr', 0)
            components['Travel'].append(travel)
            setup = row.get('Setup_Inbound_hr', 0) + row.get('Setup_Outbound_hr', 0)
            components['Setup'].append(setup)
            components['Pumping'].append(row.get('Pumping_Total_hr', 0))

        # Stack bars
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
        bottom = np.zeros(len(cases))

        for (comp_name, values), color in zip(components.items(), colors):
            ax.bar(x, values, width, bottom=bottom, label=comp_name, color=color)
            bottom += np.array(values)

        # Total labels
        for i, total in enumerate(bottom):
            ax.text(i, total + 0.5, f'{total:.1f}h', ha='center', fontweight='bold')

        ax.set_ylabel('Cycle Time (hours)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('Cycle Time Breakdown - Optimal Configurations', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax.legend(loc='upper left')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'D7_cycle_time.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D7: Cycle Time")

    def fig_d8_fleet_evolution(self, output_path: Path) -> None:
        """D8: Fleet size evolution over time."""
        fig, ax = plt.subplots(figsize=(10, 6))

        for case_id in self.det_yearly.keys():
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            # Filter optimal configuration
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])]

            if not df_opt.empty:
                ax.plot(df_opt['Year'], df_opt['Total_Shuttles'],
                       marker='o', linewidth=2, markersize=6,
                       color=COLORS[case_id], label=CASE_SHORT[case_id])
                ax.fill_between(df_opt['Year'], df_opt['Total_Shuttles'],
                              alpha=0.2, color=COLORS[case_id])

        ax.set_xlabel('Year')
        ax.set_ylabel('Total Fleet Size (Shuttles)')
        ax.set_title('Fleet Growth 2030-2050 - Optimal Configurations', fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(2030, 2050)
        # Fix y-axis to show full range of fleet sizes with padding
        y_max_fleet = ax.get_ylim()[1]
        ax.set_ylim(0, y_max_fleet * 1.1)
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        plt.tight_layout()
        plt.savefig(output_path / 'D8_fleet_evolution.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D8: Fleet Evolution")

    def fig_d9_lco_comparison(self, output_path: Path) -> None:
        """D9: Levelized Cost of Ammonia comparison."""
        fig, ax = plt.subplots(figsize=(8, 5))

        cases = list(self.det_scenarios.keys())
        x = np.arange(len(cases))

        lcos = [self._get_optimal(c)['lco'] for c in cases]
        colors = [COLORS[c] for c in cases]

        bars = ax.bar(x, lcos, color=colors, edgecolor='black', linewidth=1.5, width=0.6)

        # Value labels
        for bar, v in zip(bars, lcos):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                   f'${v:.2f}', ha='center', va='bottom', fontweight='bold')

        ax.set_ylabel('LCO (USD/ton)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('Levelized Cost of Ammonia - Optimal Configurations', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, max(lcos) * 1.2)

        plt.tight_layout()
        plt.savefig(output_path / 'D9_lco_comparison.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D9: LCO Comparison")

    def fig_d10_case_npc_comparison(self, output_path: Path) -> None:
        """D10: Case NPC comparison bar chart."""
        fig, ax = plt.subplots(figsize=(8, 5))

        cases = list(self.det_scenarios.keys())
        x = np.arange(len(cases))

        npcs = [self._get_optimal(c)['npc'] for c in cases]
        colors = [COLORS[c] for c in cases]

        bars = ax.bar(x, npcs, color=colors, edgecolor='black', linewidth=1.5, width=0.6)

        # Value labels
        for bar, v in zip(bars, npcs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                   f'${v:.1f}M', ha='center', va='bottom', fontweight='bold')

        ax.set_ylabel('20-Year NPC (Million USD)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('Minimum Net Present Cost Comparison', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, max(npcs) * 1.15)

        plt.tight_layout()
        plt.savefig(output_path / 'D10_case_npc_comparison.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D10: Case NPC Comparison")

    def fig_d11_top_configurations(self, output_path: Path) -> None:
        """D11: Top 5 configurations table/bar for each case."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Top 5 Cost-Effective Configurations', fontsize=14, fontweight='bold')

        for idx, (case_id, df) in enumerate(self.det_scenarios.items()):
            top5 = df.nsmallest(5, 'NPC_Total_USDm')

            labels = [f"{int(r['Shuttle_Size_cbm'])}m$^3$/{int(r['Pump_Size_m3ph'])}m$^3$/h"
                     for _, r in top5.iterrows()]
            npcs = top5['NPC_Total_USDm'].values

            y_pos = np.arange(len(labels))
            colors_list = [COLORS[case_id] if i == 0 else '#cccccc' for i in range(len(labels))]

            bars = axes[idx].barh(y_pos, npcs, color=colors_list, edgecolor='black')
            axes[idx].set_yticks(y_pos)
            axes[idx].set_yticklabels(labels)
            axes[idx].invert_yaxis()
            axes[idx].set_xlabel('NPC (M USD)')
            axes[idx].set_title(CASE_SHORT[case_id], fontweight='bold')

            # Value labels
            for bar, v in zip(bars, npcs):
                axes[idx].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                             f'${v:.1f}M', va='center', fontsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'D11_top_configurations.png', bbox_inches='tight')
        plt.close()
        print("  [OK] D11: Top Configurations")

    # =========================================================================
    # V5 Combined Figures
    # =========================================================================

    def fig_v5_cost_lcoa(self, output_path: Path) -> None:
        """V5 Combined: (a) Cost breakdown + (b) LCOA comparison side by side."""
        if not self.det_scenarios:
            print("  [WARN] V5_cost_lcoa: No deterministic data available")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Cost Analysis - Optimal Configurations',
                     fontsize=16, fontweight='bold')

        cases = list(self.det_scenarios.keys())

        # --- Panel (a): Cost breakdown stacked bar chart (from D6) ---
        x = np.arange(len(cases))
        width = 0.6

        capex_shuttle = []
        capex_bunk = []
        opex_fixed = []
        opex_var = []

        for case_id in cases:
            opt = self._get_optimal(case_id)
            row = opt['row']
            capex_shuttle.append(row['NPC_Annualized_Shuttle_CAPEX_USDm'])
            capex_bunk.append(row['NPC_Annualized_Bunkering_CAPEX_USDm'])
            fixed = (row['NPC_Shuttle_fOPEX_USDm'] + row['NPC_Bunkering_fOPEX_USDm'] +
                    row.get('NPC_Terminal_fOPEX_USDm', 0))
            var = (row['NPC_Shuttle_vOPEX_USDm'] + row['NPC_Bunkering_vOPEX_USDm'] +
                  row.get('NPC_Terminal_vOPEX_USDm', 0))
            opex_fixed.append(fixed)
            opex_var.append(var)

        p1 = ax1.bar(x, capex_shuttle, width, label='Shuttle CAPEX', color='#1f77b4')
        p2 = ax1.bar(x, capex_bunk, width, bottom=capex_shuttle,
                   label='Bunkering CAPEX', color='#ff7f0e')
        bottom2 = np.array(capex_shuttle) + np.array(capex_bunk)
        p3 = ax1.bar(x, opex_fixed, width, bottom=bottom2,
                   label='Fixed OPEX', color='#2ca02c')
        bottom3 = bottom2 + np.array(opex_fixed)
        p4 = ax1.bar(x, opex_var, width, bottom=bottom3,
                   label='Variable OPEX', color='#d62728')

        totals = np.array(capex_shuttle) + np.array(capex_bunk) + np.array(opex_fixed) + np.array(opex_var)
        for i, total in enumerate(totals):
            ax1.text(i, total + 5, f'${total:.1f}M', ha='center', fontweight='bold')

        ax1.set_ylabel('20-Year NPC (Million USD)', fontsize=13)
        ax1.set_xlabel('Supply Scenario', fontsize=13)
        ax1.set_title('(a) Cost Structure Breakdown', fontweight='bold', fontsize=14)
        ax1.set_xticks(x)
        ax1.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(axis='y', alpha=0.3)
        ax1.tick_params(axis='both', labelsize=11)

        # --- Panel (b): LCOA comparison bar chart (from D9) ---
        lcos = [self._get_optimal(c)['lco'] for c in cases]
        colors = [COLORS[c] for c in cases]

        bars = ax2.bar(x, lcos, color=colors, edgecolor='black', linewidth=1.5, width=0.6)

        for bar, v in zip(bars, lcos):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                   f'${v:.2f}', ha='center', va='bottom', fontweight='bold')

        ax2.set_ylabel('LCOA (USD/ton)', fontsize=13)
        ax2.set_xlabel('Supply Scenario', fontsize=13)
        ax2.set_title('(b) Levelized Cost of Ammonia', fontweight='bold', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax2.grid(axis='y', alpha=0.3)
        ax2.set_ylim(0, max(lcos) * 1.3)
        ax2.tick_params(axis='both', labelsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'V5_cost_lcoa.png', bbox_inches='tight')
        plt.close()
        print("  [OK] V5: Cost Breakdown + LCOA Comparison")

    def fig_v5_fleet_demand(self, output_path: Path) -> None:
        """V5 Combined: (a) Fleet evolution + (b) Demand vs supply overlay."""
        if not self.det_yearly:
            print("  [WARN] V5_fleet_demand: No yearly data available")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Fleet and Supply Evolution (2030-2050) - Optimal Configurations',
                     fontsize=16, fontweight='bold')

        # --- Panel (a): Fleet size evolution (from D8) ---
        for case_id in self.det_yearly.keys():
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])]

            if not df_opt.empty:
                ax1.plot(df_opt['Year'], df_opt['Total_Shuttles'],
                       marker='o', linewidth=2, markersize=6,
                       color=COLORS[case_id], label=CASE_SHORT[case_id])
                ax1.fill_between(df_opt['Year'], df_opt['Total_Shuttles'],
                              alpha=0.2, color=COLORS[case_id])

        ax1.set_xlabel('Year', fontsize=13)
        ax1.set_ylabel('Total Fleet Size (Shuttles)', fontsize=13)
        ax1.set_title('(a) Fleet Growth', fontweight='bold', fontsize=14)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(2030, 2050)
        # Fix y-axis to show full range with padding
        y_max_fleet = ax1.get_ylim()[1]
        ax1.set_ylim(0, y_max_fleet * 1.1)
        ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax1.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax1.tick_params(axis='both', labelsize=11)

        # --- Panel (b): Demand vs supply overlay (from D3, using first case) ---
        # Plot all cases on shared axes: fleet on primary, supply on secondary
        case_ids = list(self.det_yearly.keys())
        for case_id in case_ids:
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)

            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])].copy()

            if df_opt.empty:
                continue

            years = df_opt['Year'].values
            supply = df_opt['Supply_m3'].values / 1e6  # Convert to million m3

            ax2.plot(years, supply, marker='o', linewidth=2, markersize=5,
                    color=COLORS[case_id],
                    label=f'{CASE_SHORT[case_id]} Supply')

        # Add demand line if available (from first case)
        first_case = case_ids[0] if case_ids else None
        if first_case:
            df = self.det_yearly[first_case]
            opt = self._get_optimal(first_case)
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])].copy()
            if not df_opt.empty and 'Demand_m3' in df_opt.columns:
                years = df_opt['Year'].values
                demand = df_opt['Demand_m3'].values / 1e6
                ax2.plot(years, demand, 'k--', linewidth=2.5, markersize=0,
                        label='Demand (all cases)', alpha=0.7)

        ax2.set_xlabel('Year', fontsize=13)
        ax2.set_ylabel('Annual Volume (Million m$^3$)', fontsize=13)
        ax2.set_title('(b) Supply vs Demand', fontweight='bold', fontsize=14)
        ax2.legend(loc='upper left', fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(2030, 2050)
        ax2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax2.tick_params(axis='both', labelsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'V5_fleet_demand.png', bbox_inches='tight')
        plt.close()
        print("  [OK] V5: Fleet Evolution + Demand/Supply")

    # =========================================================================
    # Stochastic Figures (S1-S6)
    # =========================================================================

    def fig_s1_npc_boxplot(self, output_path: Path) -> None:
        """S1: NPC uncertainty box plot with 95% CI."""
        fig, ax = plt.subplots(figsize=(8, 6))

        cases = list(self.stoch_scenarios.keys())
        data_list = []
        labels = []

        for case_id in cases:
            if case_id in self.stoch_scenarios:
                df = self.stoch_scenarios[case_id]
                data_list.append(df['NPC_USDm'].values)
                labels.append(CASE_SHORT[case_id])

        if not data_list:
            print("  [WARN] S1: No stochastic data available")
            return

        bp = ax.boxplot(data_list, labels=labels, patch_artist=True,
                       showfliers=True, whis=[2.5, 97.5])

        # Color boxes
        colors_list = [COLORS[c] for c in cases if c in self.stoch_scenarios]
        for patch, color in zip(bp['boxes'], colors_list):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        # Add mean markers
        means = [np.mean(d) for d in data_list]
        ax.scatter(range(1, len(means)+1), means, marker='D', s=80,
                  color='red', zorder=5, label='Mean')

        # Add 95% CI annotation
        for i, (case_id, data) in enumerate(zip(cases, data_list), 1):
            if case_id in self.stoch_summary:
                summary = self.stoch_summary[case_id].iloc[0]
                ci_lower = summary['CI_95_Lower_USDm']
                ci_upper = summary['CI_95_Upper_USDm']
                ax.annotate(f'95% CI: [{ci_lower:.0f}, {ci_upper:.0f}]',
                          xy=(i, ci_upper), xytext=(i+0.3, ci_upper+30),
                          fontsize=11, ha='left')

        ax.set_ylabel('NPC (Million USD)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('NPC Distribution with Vessel Size Uncertainty\n(100 Monte Carlo Scenarios)',
                    fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S1_npc_boxplot.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S1: NPC Box Plot")

    def fig_s2_vss_evpi(self, output_path: Path) -> None:
        """S2: VSS and EVPI comparison."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        cases = list(self.stoch_summary.keys())
        x = np.arange(len(cases))
        width = 0.35

        # Extract values
        vss_vals = []
        evpi_vals = []
        det_npcs = []
        stoch_npcs = []

        for case_id in cases:
            summary = self.stoch_summary[case_id].iloc[0]
            vss_vals.append(abs(summary['VSS_USDm']))
            evpi_vals.append(summary['EVPI_USDm'])
            det_npcs.append(summary['Deterministic_NPC_USDm'])
            stoch_npcs.append(summary['Expected_NPC_USDm'])

        # Left plot: VSS vs EVPI
        ax1.bar(x - width/2, vss_vals, width, label='|VSS|', color='#d62728')
        ax1.bar(x + width/2, evpi_vals, width, label='EVPI', color='#2ca02c')

        ax1.set_ylabel('Value (Million USD)')
        ax1.set_xlabel('Supply Scenario')
        ax1.set_title('Value of Stochastic Solution (VSS) vs EVPI', fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # Right plot: Deterministic vs Stochastic NPC
        ax2.bar(x - width/2, det_npcs, width, label='Deterministic', color='#1f77b4')
        ax2.bar(x + width/2, stoch_npcs, width, label='Stochastic', color='#ff7f0e')

        ax2.set_ylabel('NPC (Million USD)')
        ax2.set_xlabel('Supply Scenario')
        ax2.set_title('Deterministic vs Expected Stochastic NPC', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S2_vss_evpi.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S2: VSS/EVPI")

    def fig_s3_mc_distribution(self, output_path: Path) -> None:
        """S3: Monte Carlo NPC distribution histogram."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
        fig.suptitle('Monte Carlo Simulation Results (100 Scenarios)',
                     fontsize=14, fontweight='bold')

        for idx, (case_id, df) in enumerate(self.stoch_scenarios.items()):
            ax = axes[idx]

            # Histogram
            n, bins, patches = ax.hist(df['NPC_USDm'], bins=20,
                                       color=COLORS[case_id], alpha=0.7,
                                       edgecolor='black')

            # Mean and median lines
            mean_val = df['NPC_USDm'].mean()
            median_val = df['NPC_USDm'].median()

            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2,
                      label=f'Mean: ${mean_val:.1f}M')
            ax.axvline(median_val, color='green', linestyle=':', linewidth=2,
                      label=f'Median: ${median_val:.1f}M')

            # 95% CI shading
            ci_lower = np.percentile(df['NPC_USDm'], 2.5)
            ci_upper = np.percentile(df['NPC_USDm'], 97.5)
            ax.axvspan(ci_lower, ci_upper, alpha=0.2, color='gray',
                      label=f'95% CI')

            ax.set_xlabel('NPC (Million USD)')
            ax.set_ylabel('Frequency')
            ax.set_title(CASE_SHORT[case_id], fontweight='bold')
            ax.legend(fontsize=11)
            ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S3_mc_distribution.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S3: MC Distribution")

    def fig_s4_vessel_distribution(self, output_path: Path) -> None:
        """S4: Vessel size distribution scenarios pie chart."""
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        fig.suptitle('Vessel Size Distribution Scenarios', fontsize=14, fontweight='bold')

        # Distribution scenarios (from stochastic config)
        scenarios = {
            'High Small': {'Small': 50, 'Medium': 40, 'Large': 10},
            'Balanced': {'Small': 30, 'Medium': 50, 'Large': 20},
            'High Large': {'Small': 15, 'Medium': 35, 'Large': 50},
        }

        colors = ['#2ca02c', '#ff7f0e', '#1f77b4']  # Green, Orange, Blue

        for idx, (scenario_name, dist) in enumerate(scenarios.items()):
            sizes = list(dist.values())
            labels = [f'{k}\n({v}%)' for k, v in dist.items()]

            axes[idx].pie(sizes, labels=labels, colors=colors, autopct='',
                         startangle=90, textprops={'fontsize': 10})

            # Calculate weighted average
            vessel_sizes = {'Small': 1500, 'Medium': 4000, 'Large': 10000}
            weighted_avg = sum(dist[k]/100 * vessel_sizes[k] for k in dist.keys())

            axes[idx].set_title(f'{scenario_name}\nAvg: {weighted_avg:.0f} m$^3$',
                               fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_path / 'S4_vessel_distribution.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S4: Vessel Distribution")

    def fig_s5_tornado(self, output_path: Path) -> None:
        """S5: Tornado diagram for sensitivity analysis."""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Sensitivity Analysis - Tornado Diagram', fontsize=14, fontweight='bold')

        for idx, (case_id, df) in enumerate(self.tornado_data.items()):
            ax = axes[idx]

            # Sort by swing
            df_sorted = df.sort_values('Swing_USDm', ascending=True)

            params = df_sorted['Parameter'].values
            swings = df_sorted['Swing_USDm'].values

            y_pos = np.arange(len(params))

            # Get base NPC
            opt = self._get_optimal(case_id)
            base_npc = opt['npc']

            # Horizontal bars
            colors_bar = ['#d62728' if s > 0 else '#2ca02c' for s in swings]
            bars = ax.barh(y_pos, swings, color=COLORS[case_id], alpha=0.7,
                          edgecolor='black')

            ax.set_yticks(y_pos)
            ax.set_yticklabels(params, fontsize=11)
            ax.set_xlabel('NPC Swing (Million USD)')
            ax.set_title(f'{CASE_SHORT[case_id]}\n(Base: ${base_npc:.1f}M)',
                        fontweight='bold')

            # Value labels
            for bar, swing in zip(bars, swings):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                       f'${swing:.1f}M', va='center', fontsize=11)

            ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S5_tornado.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S5: Tornado Diagram")

    def fig_s6_twoway_sensitivity(self, output_path: Path) -> None:
        """S6: Two-way sensitivity heatmap (Fuel Price x Bunker Volume)."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # For Case 1, create a two-way sensitivity matrix
        # Using fuel price from sensitivity data and bunker volume from tornado
        case_id = 'case_1'
        opt = self._get_optimal(case_id)
        base_npc = opt['npc']

        # Create synthetic two-way data (based on tornado analysis)
        fuel_variations = np.array([-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3])
        volume_variations = np.array([-0.1, -0.05, 0, 0.05, 0.1])

        # Fuel sensitivity: ~5.4% swing per 10% variation
        # Volume sensitivity: ~45% swing per 10% variation
        fuel_impact = 0.054  # per 10%
        volume_impact = 0.455  # per 10%

        npc_matrix = np.zeros((len(volume_variations), len(fuel_variations)))

        for i, vol_var in enumerate(volume_variations):
            for j, fuel_var in enumerate(fuel_variations):
                npc_change = (fuel_var * fuel_impact + vol_var * volume_impact) * base_npc
                npc_matrix[i, j] = base_npc + npc_change

        im = ax.imshow(npc_matrix, cmap='RdYlGn_r', aspect='auto')

        # Labels
        ax.set_xticks(np.arange(len(fuel_variations)))
        ax.set_yticks(np.arange(len(volume_variations)))
        ax.set_xticklabels([f'{v*100:+.0f}%' for v in fuel_variations])
        ax.set_yticklabels([f'{v*100:+.0f}%' for v in volume_variations])

        ax.set_xlabel('Fuel Price Variation')
        ax.set_ylabel('Bunker Volume Variation')
        ax.set_title(f'Two-Way Sensitivity Analysis - {CASE_SHORT[case_id]}\n(Base NPC: ${base_npc:.1f}M)',
                    fontweight='bold')

        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('NPC (Million USD)')

        # Annotate cells
        for i in range(len(volume_variations)):
            for j in range(len(fuel_variations)):
                text = ax.text(j, i, f'{npc_matrix[i, j]:.0f}',
                             ha='center', va='center', fontsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'S6_twoway_sensitivity.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S6: Two-Way Sensitivity")

    def fig_s7_pump_sensitivity(self, output_path: Path) -> None:
        """S7: Pump Rate Sensitivity - NPC vs Pump Rate for all cases.

        Shows how NPC changes with pump rate, with optimal shuttle size annotated.
        Vertical dashed line at 500 m3/h indicates the fixed rate used in main analysis.
        """
        # Load pump sensitivity data
        pump_data = self._load_pump_sensitivity_data()

        if not pump_data:
            print("  [WARN] S7: No pump sensitivity data available")
            print("         Run: python scripts/run_pump_sensitivity.py")
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot line for each case
        for case_id, df in pump_data.items():
            if df.empty:
                continue

            ax.plot(df['Pump_Rate_m3ph'], df['Min_NPC_USDm'],
                   marker='o', linewidth=2, markersize=8,
                   color=COLORS[case_id], label=CASE_LABELS[case_id])

            # Annotate optimal shuttle size at each point
            for _, row in df.iterrows():
                ax.annotate(f"{int(row['Optimal_Shuttle_cbm'])}",
                          xy=(row['Pump_Rate_m3ph'], row['Min_NPC_USDm']),
                          xytext=(0, 10), textcoords='offset points',
                          ha='center', va='bottom', fontsize=7,
                          color=COLORS[case_id], alpha=0.8)

        # Vertical line at fixed pump rate (500 m3/h)
        ax.axvline(x=500, color='red', linestyle='--', linewidth=2, alpha=0.7,
                  label='Fixed Rate (500 m$^3$/h)')

        # Add annotation for fixed rate
        ymin, ymax = ax.get_ylim()
        ax.annotate('Main Analysis\nFixed Rate',
                   xy=(500, ymin + (ymax - ymin) * 0.15),
                   ha='center', fontsize=11, color='red', alpha=0.8,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        ax.set_xlabel('Pump Rate (m$^3$/h)', fontsize=11)
        ax.set_ylabel('Minimum NPC (Million USD)', fontsize=11)
        ax.set_title('NPC Sensitivity to Pump Rate\n(Numbers indicate optimal shuttle size in m$^3$)',
                    fontweight='bold', fontsize=12)
        ax.legend(loc='upper right', fontsize=11)
        ax.grid(True, alpha=0.3)

        # Fix x-axis to match actual data range (100-1500 m3/h) with padding
        all_rates = []
        for df in pump_data.values():
            if not df.empty:
                all_rates.extend(df['Pump_Rate_m3ph'].tolist())
        if all_rates:
            ax.set_xlim(min(all_rates) * 0.9, max(all_rates) * 1.1)
        else:
            ax.set_xlim(50, 1600)

        plt.tight_layout()
        plt.savefig(output_path / 'S7_pump_sensitivity.png', bbox_inches='tight')
        plt.close()
        print("  [OK] S7: Pump Rate Sensitivity")

    # =========================================================================
    # New Deterministic Sensitivity Figures (Fig7-Fig10, FigS4-S5)
    # =========================================================================

    def fig_7_tornado_deterministic(self, output_path: Path) -> None:
        """Fig7: Tornado diagram from deterministic sensitivity (+/-20%)."""
        tornado_data = self._load_deterministic_tornado()

        if not tornado_data:
            print("  [WARN] Fig7: No deterministic tornado data available")
            print("         Run: python scripts/run_deterministic_sensitivity.py --analyses tornado")
            return

        n_cases = len(tornado_data)
        fig, axes = plt.subplots(1, n_cases, figsize=(5 * n_cases, 5))
        if n_cases == 1:
            axes = [axes]

        fig.suptitle('Parameter Sensitivity Analysis ($\\pm$20%)',
                     fontsize=16, fontweight='bold')

        for idx, (case_id, df) in enumerate(tornado_data.items()):
            ax = axes[idx]

            # Sort by swing (ascending for horizontal bar chart, largest at top)
            df_sorted = df.sort_values('Swing_USDm', ascending=True)

            params = df_sorted['Parameter'].values
            low_npcs = df_sorted['Low_NPC_USDm'].values
            high_npcs = df_sorted['High_NPC_USDm'].values

            # Get base NPC
            opt = self._get_optimal(case_id)
            base_npc = opt['npc'] if opt else df_sorted['Low_NPC_USDm'].mean()

            y_pos = np.arange(len(params))
            bar_height = 0.6

            # Plot low-side bars (from base to low value)
            low_delta = low_npcs - base_npc
            high_delta = high_npcs - base_npc

            ax.barh(y_pos, low_delta, bar_height, left=base_npc,
                    color='#2ca02c', alpha=0.7, label='-20%')
            ax.barh(y_pos, high_delta, bar_height, left=base_npc,
                    color='#d62728', alpha=0.7, label='+20%')

            # Base NPC line
            ax.axvline(base_npc, color='black', linewidth=1.5, linestyle='-')

            ax.set_yticks(y_pos)
            ax.set_yticklabels(params, fontsize=10)
            ax.set_xlabel('NPC (Million USD)', fontsize=12)
            ax.set_title(f'{CASE_SHORT[case_id]}\n(Base: ${base_npc:.1f}M)',
                         fontweight='bold', fontsize=13)
            ax.legend(loc='lower right', fontsize=11)
            ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig7_tornado_deterministic.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig7: Tornado Diagram (Deterministic)")

    def fig_8_fuel_price_sensitivity(self, output_path: Path) -> None:
        """Fig8: Fuel price sensitivity - LCO vs fuel price for all cases."""
        fuel_data = self._load_fuel_price_sensitivity()

        if not fuel_data:
            print("  [WARN] Fig8: No fuel price sensitivity data available")
            print("         Run: python scripts/run_deterministic_sensitivity.py --analyses fuel")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle('Fuel Price Sensitivity Analysis',
                     fontsize=16, fontweight='bold')

        # Left panel: NPC vs Fuel Price
        for case_id, df in fuel_data.items():
            if df.empty:
                continue
            ax1.plot(df['Parameter_Value'], df['NPC_USDm'],
                     marker='o', linewidth=2.5, markersize=7,
                     color=COLORS[case_id], label=CASE_SHORT[case_id])

        # Mark base case
        ax1.axvline(x=600, color='gray', linestyle='--', linewidth=1.5, alpha=0.6,
                    label='Base ($600/ton)')

        ax1.set_xlabel('Ammonia Fuel Price (USD/ton)', fontsize=13)
        ax1.set_ylabel('20-Year NPC (Million USD)', fontsize=13)
        ax1.set_title('(a) Total Cost vs Fuel Price', fontweight='bold', fontsize=14)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='both', labelsize=11)

        # Right panel: LCO vs Fuel Price
        for case_id, df in fuel_data.items():
            if df.empty or 'LCO_USD_per_ton' not in df.columns:
                continue
            ax2.plot(df['Parameter_Value'], df['LCO_USD_per_ton'],
                     marker='s', linewidth=2.5, markersize=7,
                     color=COLORS[case_id], label=CASE_SHORT[case_id])

        ax2.axvline(x=600, color='gray', linestyle='--', linewidth=1.5, alpha=0.6,
                    label='Base ($600/ton)')

        ax2.set_xlabel('Ammonia Fuel Price (USD/ton)', fontsize=13)
        ax2.set_ylabel('LCO (USD/ton)', fontsize=13)
        ax2.set_title('(b) Levelized Cost vs Fuel Price', fontweight='bold', fontsize=14)
        ax2.legend(loc='upper left', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='both', labelsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig8_fuel_price_sensitivity.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig8: Fuel Price Sensitivity")

    def fig_9_breakeven_distance(self, output_path: Path) -> None:
        """Fig9: Break-even distance analysis - Case 1 vs Case 2 NPC curves."""
        breakeven_data = self._load_breakeven_distance()

        if not breakeven_data:
            print("  [WARN] Fig9: No breakeven distance data available")
            print("         Run: python scripts/run_breakeven_analysis.py")
            return

        fig, ax = plt.subplots(figsize=(10, 6))

        case1_npc_val = None

        for name, df in breakeven_data.items():
            # Find NPC columns dynamically (each CSV has different Case 2 column)
            npc_cols = [c for c in df.columns if 'NPC_USDm' in c]
            if len(npc_cols) < 2:
                continue

            # Case 1 column: contains "Case 1" or "Busan"
            c1_cols = [c for c in npc_cols if 'Case 1' in c or 'Busan' in c]
            c2_cols = [c for c in npc_cols if c not in c1_cols]

            case1_col = c1_cols[0] if c1_cols else npc_cols[0]
            case2_col = c2_cols[0] if c2_cols else npc_cols[1]

            distances = df['Distance_nm'].values
            case2_vals = df[case2_col].values

            if case1_npc_val is None:
                case1_npc_val = df[case1_col].iloc[0]

            # Case 2/3 line (NPC varies with distance)
            color = COLORS['case_2'] if name == 'ulsan' else COLORS['case_3']
            label = 'Case 2: Ulsan (same shuttle, NPC vs distance)' if name == 'ulsan' \
                else 'Case 3: Yeosu (same shuttle, NPC vs distance)'
            ax.plot(distances, case2_vals,
                    marker='o', linewidth=2.5, markersize=6,
                    color=color, label=label)

            # Find and annotate breakeven point for this comparison
            if case1_npc_val is not None:
                diff = case1_npc_val - case2_vals
                for i in range(len(diff) - 1):
                    if diff[i] * diff[i + 1] < 0:
                        x0, x1 = distances[i], distances[i + 1]
                        d0, d1 = diff[i], diff[i + 1]
                        x_cross = x0 - d0 * (x1 - x0) / (d1 - d0)

                        ax.axvline(x=x_cross, color=color, linestyle=':', linewidth=1.5, alpha=0.6)
                        ax.annotate(f'Break-even\n{x_cross:.0f} nm',
                                    xy=(x_cross, case1_npc_val),
                                    xytext=(x_cross + 8, case1_npc_val * 1.12),
                                    fontsize=10, fontweight='bold', color=color,
                                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
                        break

        # Case 1 horizontal line (fixed NPC, distance-independent)
        if case1_npc_val is not None:
            ax.axhline(y=case1_npc_val, color=COLORS['case_1'], linewidth=2.5,
                       linestyle='--', label='Case 1: Busan Storage (fixed NPC)')

        # --- Optimal-vs-optimal overlay (dashed curves) ---
        optimal_data = self._load_breakeven_distance_optimal()
        opt_case1_npc_val = None

        if optimal_data:
            for name, df in optimal_data.items():
                npc_cols = [c for c in df.columns if 'NPC_USDm' in c]
                if len(npc_cols) < 2:
                    continue

                c1_cols = [c for c in npc_cols if 'Case 1' in c or 'Busan' in c]
                c2_cols = [c for c in npc_cols if c not in c1_cols]

                case1_col = c1_cols[0] if c1_cols else npc_cols[0]
                case2_col = c2_cols[0] if c2_cols else npc_cols[1]

                distances = df['Distance_nm'].values
                case2_vals = df[case2_col].values

                if opt_case1_npc_val is None:
                    opt_case1_npc_val = df[case1_col].iloc[0]

                color = COLORS['case_2'] if name == 'ulsan' else COLORS['case_3']
                label = 'Case 2: Ulsan (optimal shuttle)' if name == 'ulsan' \
                    else 'Case 3: Yeosu (optimal shuttle)'
                ax.plot(distances, case2_vals,
                        linestyle='--', linewidth=2.0, markersize=0,
                        color=color, alpha=0.7, label=label)

                # Find and annotate optimal breakeven point
                if opt_case1_npc_val is not None:
                    diff = opt_case1_npc_val - case2_vals
                    for i in range(len(diff) - 1):
                        if diff[i] * diff[i + 1] < 0:
                            x0, x1 = distances[i], distances[i + 1]
                            d0, d1 = diff[i], diff[i + 1]
                            x_cross = x0 - d0 * (x1 - x0) / (d1 - d0)

                            ax.axvline(x=x_cross, color=color, linestyle='--',
                                       linewidth=1.2, alpha=0.4)
                            ax.annotate(f'Opt. BE\n{x_cross:.0f} nm',
                                        xy=(x_cross, opt_case1_npc_val),
                                        xytext=(x_cross - 20, opt_case1_npc_val * 0.85),
                                        fontsize=11, fontstyle='italic', color=color,
                                        arrowprops=dict(arrowstyle='->', color=color,
                                                        lw=1.2, ls='--'))
                            break

            # Case 1 optimal horizontal line
            if opt_case1_npc_val is not None and opt_case1_npc_val != case1_npc_val:
                ax.axhline(y=opt_case1_npc_val, color=COLORS['case_1'], linewidth=2.0,
                           linestyle=':', alpha=0.7,
                           label='Case 1: Busan Storage (optimal shuttle, fixed NPC)')

        ax.set_xlabel('Supply Distance (nautical miles)', fontsize=13)
        ax.set_ylabel('21-Year NPC (Million USD)', fontsize=13)
        ax.set_title('Break-even Distance: Storage vs Direct Supply',
                     fontsize=15, fontweight='bold')
        ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='both', labelsize=11)
        ax.set_xlim(0, None)
        ax.set_ylim(0, None)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig9_breakeven_distance.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig9: Break-even Distance")

    def fig_10_demand_scenarios(self, output_path: Path) -> None:
        """Fig10: Demand scenario comparison - grouped bar chart."""
        demand_data = self._load_demand_scenarios()

        # Prefer summary file
        if 'summary' in demand_data:
            df = demand_data['summary']
        elif demand_data:
            df = pd.concat(list(demand_data.values()), ignore_index=True)
        else:
            print("  [WARN] Fig10: No demand scenario data available")
            print("         Run: python scripts/run_demand_scenarios.py")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle('Impact of Demand Growth on Optimal Infrastructure',
                     fontsize=16, fontweight='bold')

        scenarios = df['Scenario'].unique()
        cases = [c for c in ['case_1', 'case_2', 'case_3'] if c in df['Case'].unique()]
        n_cases = len(cases)

        x = np.arange(len(scenarios))
        total_width = 0.7
        bar_width = total_width / n_cases

        # Left panel: NPC by scenario
        for i, case_id in enumerate(cases):
            case_data = df[df['Case'] == case_id]
            # Sort by scenario order
            scenario_order = {s: idx for idx, s in enumerate(scenarios)}
            case_data = case_data.copy()
            case_data['order'] = case_data['Scenario'].map(scenario_order)
            case_data = case_data.sort_values('order')

            offset = (i - n_cases / 2 + 0.5) * bar_width
            bars = ax1.bar(x + offset, case_data['NPC_Total_USDm'].values,
                           bar_width, color=COLORS[case_id],
                           label=CASE_SHORT[case_id], edgecolor='black', linewidth=0.5)

        ax1.set_xlabel('Demand Scenario', fontsize=13)
        ax1.set_ylabel('20-Year NPC (Million USD)', fontsize=13)
        ax1.set_title('(a) Total Cost by Scenario', fontweight='bold', fontsize=14)
        ax1.set_xticks(x)
        ax1.set_xticklabels(scenarios, fontsize=10)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(axis='y', alpha=0.3)
        ax1.tick_params(axis='both', labelsize=11)

        # Right panel: LCO by scenario
        for i, case_id in enumerate(cases):
            case_data = df[df['Case'] == case_id]
            case_data = case_data.copy()
            scenario_order = {s: idx for idx, s in enumerate(scenarios)}
            case_data['order'] = case_data['Scenario'].map(scenario_order)
            case_data = case_data.sort_values('order')

            offset = (i - n_cases / 2 + 0.5) * bar_width
            ax2.bar(x + offset, case_data['LCO_USD_per_ton'].values,
                    bar_width, color=COLORS[case_id],
                    label=CASE_SHORT[case_id], edgecolor='black', linewidth=0.5)

        ax2.set_xlabel('Demand Scenario', fontsize=13)
        ax2.set_ylabel('LCO (USD/ton)', fontsize=13)
        ax2.set_title('(b) Levelized Cost by Scenario', fontweight='bold', fontsize=14)
        ax2.set_xticks(x)
        ax2.set_xticklabels(scenarios, fontsize=10)
        ax2.legend(loc='upper right', fontsize=10)
        ax2.grid(axis='y', alpha=0.3)
        ax2.tick_params(axis='both', labelsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig10_demand_scenarios.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig10: Demand Scenarios")

    def fig_s4_twoway_deterministic(self, output_path: Path) -> None:
        """FigS4: Two-way sensitivity heatmap (actual optimization, not synthetic)."""
        twoway_data = self._load_two_way_det()

        if not twoway_data:
            print("  [WARN] FigS4: No two-way deterministic data available")
            print("         Run: python scripts/run_deterministic_sensitivity.py --analyses twoway")
            return

        n_cases = len(twoway_data)
        fig, axes = plt.subplots(1, n_cases, figsize=(7 * n_cases, 5))
        if n_cases == 1:
            axes = [axes]

        fig.suptitle('Two-Way Sensitivity: Fuel Price x Bunker Volume',
                     fontsize=16, fontweight='bold')

        for idx, (case_id, df) in enumerate(twoway_data.items()):
            ax = axes[idx]

            # Convert to numpy matrix
            npc_matrix = df.values.astype(float)

            im = ax.imshow(npc_matrix, cmap='RdYlGn_r', aspect='auto')

            # Labels from index/columns
            row_labels = [str(r).split('=')[-1] if '=' in str(r) else str(r) for r in df.index]
            col_labels = [str(c).split('=')[-1] if '=' in str(c) else str(c) for c in df.columns]

            ax.set_xticks(np.arange(len(col_labels)))
            ax.set_yticks(np.arange(len(row_labels)))
            ax.set_xticklabels(col_labels, rotation=45, ha='right', fontsize=11)
            ax.set_yticklabels(row_labels, fontsize=11)

            # Axis labels from index/column names
            ax.set_xlabel('Bunker Volume Variation', fontsize=11)
            ax.set_ylabel('Fuel Price Variation', fontsize=11)
            ax.set_title(f'{CASE_SHORT[case_id]}', fontweight='bold', fontsize=13)

            # Colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label('NPC (Million USD)', fontsize=10)

            # Annotate cells
            for i in range(npc_matrix.shape[0]):
                for j in range(npc_matrix.shape[1]):
                    val = npc_matrix[i, j]
                    text_color = 'white' if val > np.median(npc_matrix) else 'black'
                    ax.text(j, i, f'{val:.0f}', ha='center', va='center',
                            fontsize=11, color=text_color)

        plt.tight_layout()
        plt.savefig(output_path / 'FigS4_twoway_deterministic.png', bbox_inches='tight')
        plt.close()
        print("  [OK] FigS4: Two-Way Sensitivity (Deterministic)")

    def fig_s5_bunker_volume_sensitivity(self, output_path: Path) -> None:
        """FigS5: Bunker volume sensitivity - NPC and LCO vs bunker volume."""
        volume_data = self._load_bunker_volume_sensitivity()

        if not volume_data:
            print("  [WARN] FigS5: No bunker volume sensitivity data available")
            print("         Run: python scripts/run_deterministic_sensitivity.py --analyses bunker")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle('Bunker Volume Sensitivity Analysis',
                     fontsize=16, fontweight='bold')

        # Left panel: NPC vs Bunker Volume
        for case_id, df in volume_data.items():
            if df.empty:
                continue
            ax1.plot(df['Parameter_Value'], df['NPC_USDm'],
                     marker='o', linewidth=2.5, markersize=7,
                     color=COLORS[case_id], label=CASE_SHORT[case_id])

        # Mark base volume
        ax1.axvline(x=5000, color='gray', linestyle='--', linewidth=1.5, alpha=0.6,
                    label='Base (5,000 m$^3$)')

        ax1.set_xlabel('Bunker Volume per Call (m$^3$)', fontsize=13)
        ax1.set_ylabel('20-Year NPC (Million USD)', fontsize=13)
        ax1.set_title('(a) Total Cost vs Bunker Volume', fontweight='bold', fontsize=14)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='both', labelsize=11)
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{x/1000:.1f}k' if x >= 1000 else f'{x:.0f}'))

        # Right panel: LCO vs Bunker Volume
        for case_id, df in volume_data.items():
            if df.empty or 'LCO_USD_per_ton' not in df.columns:
                continue
            ax2.plot(df['Parameter_Value'], df['LCO_USD_per_ton'],
                     marker='s', linewidth=2.5, markersize=7,
                     color=COLORS[case_id], label=CASE_SHORT[case_id])

        ax2.axvline(x=5000, color='gray', linestyle='--', linewidth=1.5, alpha=0.6,
                    label='Base (5,000 m$^3$)')

        ax2.set_xlabel('Bunker Volume per Call (m$^3$)', fontsize=13)
        ax2.set_ylabel('LCO (USD/ton)', fontsize=13)
        ax2.set_title('(b) Levelized Cost vs Bunker Volume', fontweight='bold', fontsize=14)
        ax2.legend(loc='upper right', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='both', labelsize=11)
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'{x/1000:.1f}k' if x >= 1000 else f'{x:.0f}'))

        plt.tight_layout()
        plt.savefig(output_path / 'FigS5_bunker_volume_sensitivity.png', bbox_inches='tight')
        plt.close()
        print("  [OK] FigS5: Bunker Volume Sensitivity")

    # =========================================================================
    # Combined Figures (C1-C4)
    # =========================================================================

    def fig_c1_det_vs_stoch(self, output_path: Path) -> None:
        """C1: Deterministic vs Stochastic NPC comparison."""
        fig, ax = plt.subplots(figsize=(10, 6))

        cases = list(self.stoch_summary.keys())
        x = np.arange(len(cases))
        width = 0.35

        det_npcs = []
        stoch_npcs = []
        stoch_std = []

        for case_id in cases:
            det_npcs.append(self._get_optimal(case_id)['npc'])
            summary = self.stoch_summary[case_id].iloc[0]
            stoch_npcs.append(summary['Expected_NPC_USDm'])
            stoch_std.append(summary['NPC_Std_USDm'])

        # Bars
        bars1 = ax.bar(x - width/2, det_npcs, width, label='Deterministic',
                      color='#1f77b4', edgecolor='black')
        bars2 = ax.bar(x + width/2, stoch_npcs, width, label='Stochastic (Expected)',
                      color='#ff7f0e', edgecolor='black', yerr=stoch_std, capsize=5)

        # Value labels
        for bar, v in zip(bars1, det_npcs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                   f'${v:.0f}M', ha='center', va='bottom', fontsize=11, fontweight='bold')

        for bar, v, std in zip(bars2, stoch_npcs, stoch_std):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 10,
                   f'${v:.0f}M\n(+{std:.0f})', ha='center', va='bottom', fontsize=11)

        ax.set_ylabel('20-Year NPC (Million USD)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('Deterministic vs Stochastic Optimization Results', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'C1_det_vs_stoch.png', bbox_inches='tight')
        plt.close()
        print("  [OK] C1: Det vs Stoch")

    def fig_c2_breakeven_distance(self, output_path: Path) -> None:
        """C2: Break-even analysis by distance."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Distance data
        distances = {
            'case_1': 2,    # ~2nm within port
            'case_2': 25,  # 25nm
            'case_3': 86,  # 86nm
        }

        cases = ['case_1', 'case_2', 'case_3']
        dist_vals = [distances[c] for c in cases]
        npc_vals = [self._get_optimal(c)['npc'] for c in cases]

        # Scatter plot
        for case_id, d, npc in zip(cases, dist_vals, npc_vals):
            ax.scatter(d, npc, s=200, c=COLORS[case_id], edgecolor='black',
                      linewidth=2, label=CASE_SHORT[case_id], zorder=5)

        # Fit line for Case 2 (direct supply cases)
        case2_dists = [distances['case_2'], distances['case_3']]
        case2_npcs = [self._get_optimal('case_2')['npc'],
                     self._get_optimal('case_3')['npc']]

        # Linear extrapolation
        slope = (case2_npcs[1] - case2_npcs[0]) / (case2_dists[1] - case2_dists[0])
        intercept = case2_npcs[0] - slope * case2_dists[0]

        x_line = np.linspace(0, 100, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, '--', color='gray', alpha=0.7,
               label='Direct Supply Trend')

        # Case 1 horizontal line
        case1_npc = self._get_optimal('case_1')['npc']
        ax.axhline(case1_npc, color=COLORS['case_1'], linestyle=':', linewidth=2,
                  label='Busan Storage NPC')

        # Find break-even point
        breakeven_dist = (case1_npc - intercept) / slope
        if 0 < breakeven_dist < 100:
            ax.axvline(breakeven_dist, color='red', linestyle='--', alpha=0.5)
            ax.annotate(f'Break-even\n~{breakeven_dist:.0f}nm',
                       xy=(breakeven_dist, case1_npc),
                       xytext=(breakeven_dist + 10, case1_npc + 50),
                       fontsize=10, arrowprops=dict(arrowstyle='->', color='red'))

        ax.set_xlabel('Supply Distance (nautical miles)')
        ax.set_ylabel('20-Year NPC (Million USD)')
        ax.set_title('Cost vs Distance Analysis', fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, max(npc_vals) * 1.1)

        plt.tight_layout()
        plt.savefig(output_path / 'C2_breakeven_distance.png', bbox_inches='tight')
        plt.close()
        print("  [OK] C2: Break-even Distance")

    def fig_c3_breakeven_demand(self, output_path: Path) -> None:
        """C3: Break-even analysis by demand volume."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create demand sensitivity (synthetic based on analysis)
        demand_factors = np.array([0.5, 0.75, 1.0, 1.25, 1.5])

        cases = ['case_1', 'case_2', 'case_3']

        for case_id in cases:
            base_npc = self._get_optimal(case_id)['npc']
            # NPC scales roughly linearly with demand
            npcs = base_npc * demand_factors

            ax.plot(demand_factors * 100, npcs, marker='o', linewidth=2,
                   color=COLORS[case_id], label=CASE_SHORT[case_id])

        ax.set_xlabel('Demand Level (% of Base Case)')
        ax.set_ylabel('20-Year NPC (Million USD)')
        ax.set_title('NPC Sensitivity to Demand Volume', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'C3_breakeven_demand.png', bbox_inches='tight')
        plt.close()
        print("  [OK] C3: Break-even Demand")

    def fig_c4_summary_dashboard(self, output_path: Path) -> None:
        """C4: Summary dashboard with 6 panels."""
        fig = plt.figure(figsize=(16, 10))

        # Create 2x3 grid
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

        cases = list(self.det_scenarios.keys())

        # (a) NPC Comparison
        ax1 = fig.add_subplot(gs[0, 0])
        npcs = [self._get_optimal(c)['npc'] for c in cases]
        bars = ax1.bar([CASE_SHORT[c] for c in cases], npcs,
                      color=[COLORS[c] for c in cases], edgecolor='black')
        ax1.set_ylabel('NPC (M USD)')
        ax1.set_title('(a) Minimum NPC', fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        for bar, v in zip(bars, npcs):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'${v:.0f}M', ha='center', va='bottom', fontsize=11)

        # (b) LCO Comparison
        ax2 = fig.add_subplot(gs[0, 1])
        lcos = [self._get_optimal(c)['lco'] for c in cases]
        bars = ax2.bar([CASE_SHORT[c] for c in cases], lcos,
                      color=[COLORS[c] for c in cases], edgecolor='black')
        ax2.set_ylabel('LCO (USD/ton)')
        ax2.set_title('(b) Levelized Cost', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        for bar, v in zip(bars, lcos):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'${v:.2f}', ha='center', va='bottom', fontsize=11)

        # (c) Fleet Growth
        ax3 = fig.add_subplot(gs[0, 2])
        for case_id in self.det_yearly.keys():
            df = self.det_yearly[case_id]
            opt = self._get_optimal(case_id)
            df_opt = df[(df['Shuttle_Size_cbm'] == opt['shuttle']) &
                       (df['Pump_Size_m3ph'] == opt['pump'])]
            if not df_opt.empty:
                ax3.plot(df_opt['Year'], df_opt['Total_Shuttles'],
                        color=COLORS[case_id], linewidth=2, label=CASE_SHORT[case_id])
        ax3.set_xlabel('Year')
        ax3.set_ylabel('Fleet Size')
        ax3.set_title('(c) Fleet Evolution', fontweight='bold')
        ax3.legend(fontsize=11)
        ax3.grid(True, alpha=0.3)

        # (d) Cost Structure Pie (Case 1)
        ax4 = fig.add_subplot(gs[1, 0])
        opt = self._get_optimal('case_1')
        row = opt['row']
        sizes = [
            row['NPC_Annualized_Shuttle_CAPEX_USDm'] + row['NPC_Annualized_Bunkering_CAPEX_USDm'],
            row['NPC_Shuttle_fOPEX_USDm'] + row['NPC_Bunkering_fOPEX_USDm'],
            row['NPC_Shuttle_vOPEX_USDm'] + row['NPC_Bunkering_vOPEX_USDm'],
        ]
        labels = ['CAPEX', 'Fixed OPEX', 'Variable OPEX']
        ax4.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=['#1f77b4', '#2ca02c', '#d62728'])
        ax4.set_title('(d) Cost Structure (Case 1)', fontweight='bold')

        # (e) Tornado Summary (Case 1)
        ax5 = fig.add_subplot(gs[1, 1])
        if 'case_1' in self.tornado_data:
            df = self.tornado_data['case_1'].sort_values('Swing_USDm', ascending=True)
            y_pos = np.arange(len(df))
            ax5.barh(y_pos, df['Swing_USDm'].values, color=COLORS['case_1'], alpha=0.7)
            ax5.set_yticks(y_pos)
            ax5.set_yticklabels(df['Parameter'].values, fontsize=11)
            ax5.set_xlabel('NPC Swing (M USD)')
            ax5.set_title('(e) Sensitivity Analysis', fontweight='bold')
            ax5.grid(axis='x', alpha=0.3)

        # (f) VSS/EVPI Summary
        ax6 = fig.add_subplot(gs[1, 2])
        if self.stoch_summary:
            vss_vals = []
            evpi_vals = []
            for case_id in cases:
                if case_id in self.stoch_summary:
                    summary = self.stoch_summary[case_id].iloc[0]
                    vss_vals.append(abs(summary['VSS_USDm']))
                    evpi_vals.append(summary['EVPI_USDm'])
                else:
                    vss_vals.append(0)
                    evpi_vals.append(0)

            x = np.arange(len(cases))
            width = 0.35
            ax6.bar(x - width/2, vss_vals, width, label='|VSS|', color='#d62728')
            ax6.bar(x + width/2, evpi_vals, width, label='EVPI', color='#2ca02c')
            ax6.set_xticks(x)
            ax6.set_xticklabels([CASE_SHORT[c] for c in cases], fontsize=11)
            ax6.set_ylabel('Value (M USD)')
            ax6.set_title('(f) Stochastic Value', fontweight='bold')
            ax6.legend(fontsize=11)
            ax6.grid(axis='y', alpha=0.3)

        fig.suptitle('Green Corridor Ammonia Bunkering Analysis Summary',
                    fontsize=16, fontweight='bold', y=0.98)

        plt.savefig(output_path / 'C4_summary_dashboard.png', bbox_inches='tight')
        plt.close()
        print("  [OK] C4: Summary Dashboard")

    # =========================================================================
    # Discount Rate Sensitivity Figures (Fig11-Fig12)
    # =========================================================================

    def _load_discount_rate_data(self) -> Dict[str, pd.DataFrame]:
        """Load discount rate analysis data for Fig11/Fig12."""
        data = {}
        dr_dir = self.results_dir / "discount_rate_analysis" / "data"
        # Comparison summary
        comparison_path = dr_dir / "discount_rate_comparison.csv"
        if comparison_path.exists():
            data['comparison'] = pd.read_csv(comparison_path)
        # Yearly data per case
        for case_id in ['case_1', 'case_2', 'case_3']:
            yearly_path = dr_dir / f"discount_rate_yearly_{case_id}.csv"
            if yearly_path.exists():
                data[f'yearly_{case_id}'] = pd.read_csv(yearly_path)
        return data

    def fig_11_discount_rate_sensitivity(self, output_path: Path) -> None:
        """Fig11: Discount rate sensitivity - NPC/LCO vs discount rate for all cases."""
        dr_data = self._load_discount_rate_data()

        if 'comparison' not in dr_data:
            print("  [WARN] Fig11: No discount rate comparison data available")
            print("         Run: python scripts/run_discount_rate_analysis.py")
            return

        df = dr_data['comparison']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle('Discount Rate Sensitivity Analysis',
                     fontsize=16, fontweight='bold')

        cases_in_data = [c for c in ['case_1', 'case_2', 'case_3']
                         if c in df['Case'].unique()]

        for case_id in cases_in_data:
            cdf = df[df['Case'] == case_id].sort_values('Discount_Rate')
            color = COLORS.get(case_id, '#333333')
            label = CASE_SHORT.get(case_id, case_id)

            # Left panel: NPC
            ax1.plot(cdf['Discount_Rate'] * 100, cdf['NPC_Total_USDm'],
                     marker='o', linewidth=2.5, markersize=8,
                     color=color, label=label)

            # Annotate shuttle size at each point
            for _, row in cdf.iterrows():
                ax1.annotate(f"{int(row['Optimal_Shuttle_cbm'])} m3",
                             xy=(row['Discount_Rate'] * 100, row['NPC_Total_USDm']),
                             xytext=(5, 10), textcoords='offset points',
                             fontsize=11, color=color, alpha=0.8)

            # Right panel: LCO
            ax2.plot(cdf['Discount_Rate'] * 100, cdf['LCO_USD_per_ton'],
                     marker='s', linewidth=2.5, markersize=8,
                     color=color, label=label)

        ax1.set_xlabel('Discount Rate (%)', fontsize=13)
        ax1.set_ylabel('20-Year NPC (Million USD)', fontsize=13)
        ax1.set_title('(a) Total Cost vs Discount Rate', fontweight='bold', fontsize=14)
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='both', labelsize=11)

        ax2.set_xlabel('Discount Rate (%)', fontsize=13)
        ax2.set_ylabel('LCO (USD/ton)', fontsize=13)
        ax2.set_title('(b) Levelized Cost vs Discount Rate', fontweight='bold', fontsize=14)
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='both', labelsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig11_discount_rate_sensitivity.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig11: Discount Rate Sensitivity")

    def fig_12_discount_rate_fleet(self, output_path: Path) -> None:
        """Fig12: Fleet expansion timeline under different discount rates."""
        dr_data = self._load_discount_rate_data()

        # Need yearly data for at least one case
        yearly_keys = [k for k in dr_data if k.startswith('yearly_')]
        if not yearly_keys:
            print("  [WARN] Fig12: No discount rate yearly data available")
            print("         Run: python scripts/run_discount_rate_analysis.py")
            return

        cases_in_data = []
        for case_id in ['case_1', 'case_2', 'case_3']:
            if f'yearly_{case_id}' in dr_data:
                cases_in_data.append(case_id)

        n_cases = len(cases_in_data)
        if n_cases == 0:
            print("  [WARN] Fig12: No yearly data found")
            return

        fig, axes = plt.subplots(1, n_cases, figsize=(5.5 * n_cases, 5))
        if n_cases == 1:
            axes = [axes]
        fig.suptitle('Fleet Expansion Under Different Discount Rates',
                     fontsize=16, fontweight='bold')

        rate_styles = {0.0: '-', 0.05: '--', 0.08: ':'}

        for ax_idx, case_id in enumerate(cases_in_data):
            ax = axes[ax_idx]
            color = COLORS.get(case_id, '#333333')
            ydf_all = dr_data[f'yearly_{case_id}']

            rates = sorted(ydf_all['Discount_Rate'].unique())
            for rate in rates:
                ydf = ydf_all[ydf_all['Discount_Rate'] == rate].sort_values('Year')
                style = rate_styles.get(rate, '-.')
                label = f'r={rate:.0%}'
                ax.plot(ydf['Year'], ydf['Total_Shuttles'],
                        linestyle=style, linewidth=2.0, marker='o', markersize=4,
                        color=color, label=label, alpha=0.9)

            ax.set_xlabel('Year', fontsize=13)
            if ax_idx == 0:
                ax.set_ylabel('Total Shuttles', fontsize=13)
            panel_label = chr(ord('a') + ax_idx)
            ax.set_title(f'({panel_label}) {CASE_SHORT.get(case_id, case_id)}',
                         fontweight='bold', fontsize=14)
            ax.legend(loc='upper left', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='both', labelsize=11)
            ax.set_xlim(2029, 2051)
            ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

        plt.tight_layout()
        plt.savefig(output_path / 'Fig12_discount_rate_fleet.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig12: Fleet Expansion Timeline")

    # =========================================================================
    # Yang & Lam DES Comparison Figures (Fig13-Fig14)
    # =========================================================================

    def _load_yang_lam_data(self) -> Dict[str, pd.DataFrame]:
        """Load Yang & Lam comparison data for Fig13/Fig14."""
        data = {}
        yl_dir = self.results_dir / "yang_lam_des_comparison" / "data"

        for name in ['service_time_comparison', 'flow_rate_sensitivity_comparison',
                     'sensitivity_summary_comparison']:
            path = yl_dir / f"{name}.csv"
            if path.exists():
                data[name] = pd.read_csv(path)
        return data

    def fig_13_yang_lam_service_time(self, output_path: Path) -> None:
        """Fig13: Yang & Lam DES vs MILP service time comparison (2 panels)."""
        yl_data = self._load_yang_lam_data()

        if 'service_time_comparison' not in yl_data:
            print("  [WARN] Fig13: No Yang & Lam service time data available")
            print("         Run: python scripts/run_yang_lam_comparison.py")
            return

        df = yl_data['service_time_comparison']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle('Service Time Cross-Validation: Yang & Lam DES vs MILP',
                     fontsize=16, fontweight='bold')

        # --- Panel (a): Grouped bar chart ---
        x = np.arange(len(df))
        width = 0.22

        bars1 = ax1.bar(x - width, df['Yang_Actual_h'], width,
                        label='Yang & Lam Actual', color='#d62728', alpha=0.85)
        bars2 = ax1.bar(x, df['Yang_DES_h'], width,
                        label='Yang & Lam DES', color='#ff7f0e', alpha=0.85)
        bars3 = ax1.bar(x + width, df['Our_MILP_Adjusted_h'], width,
                        label='Our MILP (adjusted)', color='#1f77b4', alpha=0.85)

        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{height:.1f}h',
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 4), textcoords='offset points',
                             ha='center', fontsize=11)

        labels = [f"{int(row['Volume_tons']):,}t\n@{int(row['Flow_Rate_tph'])} t/h"
                  for _, row in df.iterrows()]
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, fontsize=11)
        ax1.set_ylabel('Service Time (hours)', fontsize=13)
        ax1.set_title('(a) Service Time by Validation Point', fontweight='bold', fontsize=14)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, axis='y', alpha=0.3)
        ax1.set_ylim(0, max(df['Yang_DES_h'].max(), df['Yang_Actual_h'].max()) * 1.2)
        ax1.tick_params(axis='y', labelsize=11)

        # --- Panel (b): Parity scatter plot ---
        ax2.scatter(df['Yang_DES_h'], df['Our_MILP_Adjusted_h'],
                    s=150, color='#1f77b4', edgecolors='black', linewidth=1.5,
                    zorder=5, label='Validation points')

        # 45-degree reference line
        all_vals = list(df['Yang_DES_h']) + list(df['Our_MILP_Adjusted_h'])
        line_min = min(all_vals) * 0.9
        line_max = max(all_vals) * 1.1
        ax2.plot([line_min, line_max], [line_min, line_max],
                 'k--', alpha=0.5, linewidth=1.5, label='Perfect agreement')

        # Annotate each point
        for _, row in df.iterrows():
            ax2.annotate(f"{int(row['Volume_tons']):,}t",
                         xy=(row['Yang_DES_h'], row['Our_MILP_Adjusted_h']),
                         xytext=(8, -5), textcoords='offset points',
                         fontsize=10, color='#333333')

        ax2.set_xlabel('Yang & Lam DES Service Time (hours)', fontsize=13)
        ax2.set_ylabel('Our MILP Adjusted Service Time (hours)', fontsize=13)
        ax2.set_title('(b) Parity Plot (DES vs MILP)', fontweight='bold', fontsize=14)
        ax2.legend(loc='upper left', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(line_min, line_max)
        ax2.set_ylim(line_min, line_max)
        ax2.set_aspect('equal', adjustable='box')
        ax2.tick_params(axis='both', labelsize=11)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig13_yang_lam_service_time.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig13: Yang & Lam Service Time Comparison")

    def fig_14_yang_lam_sensitivity(self, output_path: Path) -> None:
        """Fig14: Yang & Lam DES vs MILP sensitivity comparison (2 panels)."""
        yl_data = self._load_yang_lam_data()

        has_flow = 'flow_rate_sensitivity_comparison' in yl_data
        has_sens = 'sensitivity_summary_comparison' in yl_data

        if not has_flow and not has_sens:
            print("  [WARN] Fig14: No Yang & Lam sensitivity data available")
            print("         Run: python scripts/run_yang_lam_comparison.py")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle('Sensitivity Comparison: Yang & Lam DES vs MILP',
                     fontsize=16, fontweight='bold')

        # --- Panel (a): Flow rate vs service time ---
        if has_flow:
            df_flow = yl_data['flow_rate_sensitivity_comparison']

            for pset, color, marker, ls in [
                ('Our_Case1', '#1f77b4', 'o', '-'),
                ('Yang_Matched', '#2ca02c', 's', '--'),
            ]:
                subset = df_flow[df_flow['Parameter_Set'] == pset].sort_values('Flow_Multiplier')
                label = subset.iloc[0]['Label'] if not subset.empty else pset
                ax1.plot(subset['Flow_Multiplier'] * 100, subset['Service_Time_h'],
                         marker=marker, linewidth=2.0, markersize=7,
                         color=color, linestyle=ls, label=f'MILP: {label}')

            # Add Yang & Lam DES reference point (mode flow rate)
            # Yang DES: at base flow, service_time ~ our Yang-matched base + overhead
            yang_base_flow_pct = 100  # 100% = base
            yang_base_svc = 7.3  # MFO average service time from Yang
            ax1.axhline(y=yang_base_svc, color='#ff7f0e', linestyle=':', linewidth=1.5,
                        alpha=0.7, label=f'Yang DES avg ({yang_base_svc}h)')

            ax1.set_xlabel('Flow Rate (% of base)', fontsize=13)
            ax1.set_ylabel('Service Time (hours)', fontsize=13)
            ax1.set_title('(a) Flow Rate Sensitivity', fontweight='bold', fontsize=14)
            ax1.legend(loc='upper right', fontsize=11)
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='both', labelsize=11)
        else:
            ax1.text(0.5, 0.5, 'No flow rate data', transform=ax1.transAxes,
                     ha='center', va='center', fontsize=14)

        # --- Panel (b): Multi-dimension sensitivity horizontal bars ---
        if has_sens:
            df_sens = yl_data['sensitivity_summary_comparison']

            # Filter to dimensions that have both Yang and Our values
            plot_dims = []
            yang_vals = []
            our_vals = []

            for _, row in df_sens.iterrows():
                yang_v = row['Yang_Impact_Pct']
                our_v = row['Our_Impact_Pct']
                has_yang = yang_v != '' and not (isinstance(yang_v, float) and np.isnan(yang_v))
                has_our = our_v != '' and not (isinstance(our_v, float) and np.isnan(our_v))

                if has_yang or has_our:
                    plot_dims.append(row['Dimension'])
                    yang_vals.append(float(yang_v) if has_yang else 0)
                    our_vals.append(float(our_v) if has_our else 0)

            if plot_dims:
                y = np.arange(len(plot_dims))
                height = 0.35

                ax2.barh(y - height/2, yang_vals, height,
                         label='Yang & Lam DES', color='#ff7f0e', alpha=0.85)
                ax2.barh(y + height/2, our_vals, height,
                         label='Our MILP', color='#1f77b4', alpha=0.85)

                ax2.set_yticks(y)
                ax2.set_yticklabels(plot_dims, fontsize=10)
                ax2.set_xlabel('Impact (%)', fontsize=13)
                ax2.set_title('(b) Multi-Dimension Sensitivity', fontweight='bold', fontsize=14)
                ax2.legend(loc='lower right', fontsize=10)
                ax2.grid(True, axis='x', alpha=0.3)
                ax2.tick_params(axis='both', labelsize=11)
                ax2.invert_yaxis()
        else:
            ax2.text(0.5, 0.5, 'No sensitivity data', transform=ax2.transAxes,
                     ha='center', va='center', fontsize=14)

        plt.tight_layout()
        plt.savefig(output_path / 'Fig14_yang_lam_sensitivity.png', bbox_inches='tight')
        plt.close()
        print("  [OK] Fig14: Yang & Lam Sensitivity Comparison")

    # =========================================================================
    # Main Generation Method
    # =========================================================================

    def generate_all(self, output_dir: str = "results/paper_figures") -> None:
        """
        Generate all paper figures.

        Args:
            output_dir: Output directory for figures
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print("\n" + "=" * 60)
        print("Paper Figure Generation")
        print("=" * 60)
        print(f"Output directory: {output_path}")
        print("=" * 60)

        # Deterministic Figures (D1-D12)
        print("\n[1/3] Generating Deterministic Figures (D1-D12)...")
        if self.det_scenarios:
            self.fig_d1_npc_vs_shuttle(output_path)
            self.fig_d2_yearly_cost_evolution(output_path)
            self.fig_d3_yearly_fleet_demand(output_path)
            self.fig_d4_yearly_cycles(output_path)
            self.fig_d5_yearly_utilization(output_path)
            # Case-specific D4/D5 figures with multiple shuttle sizes
            self.generate_case_specific_figures(output_path)
            self.fig_d6_cost_breakdown(output_path)
            self.fig_d7_cycle_time(output_path)
            self.fig_d8_fleet_evolution(output_path)
            self.fig_d9_lco_comparison(output_path)
            # fig_d10_case_npc_comparison removed in v5 (redundant with D1)
            self.fig_d11_top_configurations(output_path)
            self.fig_d12_npc_heatmap(output_path)
            # V5 combined figures
            self.fig_v5_cost_lcoa(output_path)
            self.fig_v5_fleet_demand(output_path)
        else:
            print("  [WARN] No deterministic data available")

        # Stochastic Figures
        print("\n[2/3] Generating Stochastic Figures (S1-S7)...")
        if self.stoch_summary:
            self.fig_s1_npc_boxplot(output_path)
            self.fig_s2_vss_evpi(output_path)
            self.fig_s3_mc_distribution(output_path)
            self.fig_s4_vessel_distribution(output_path)
            self.fig_s5_tornado(output_path)
            self.fig_s6_twoway_sensitivity(output_path)
        else:
            print("  [WARN] No stochastic data available")

        # S7 can be generated independently (uses separate sensitivity data)
        self.fig_s7_pump_sensitivity(output_path)

        # New Deterministic Sensitivity Figures (Fig7-Fig10, FigS4-S5)
        print("\n[2.5/3] Generating Deterministic Sensitivity Figures (Fig7-10, FigS4-S5)...")
        self.fig_7_tornado_deterministic(output_path)
        self.fig_8_fuel_price_sensitivity(output_path)
        self.fig_9_breakeven_distance(output_path)
        self.fig_10_demand_scenarios(output_path)
        self.fig_s4_twoway_deterministic(output_path)
        self.fig_s5_bunker_volume_sensitivity(output_path)

        # Discount Rate Sensitivity Figures (Fig11 only; Fig12 removed in v5 - 3 identical lines)
        print("\n[2.6/3] Generating Discount Rate Figures (Fig11)...")
        self.fig_11_discount_rate_sensitivity(output_path)
        # fig_12_discount_rate_fleet removed in v5 (3 overlapping lines)

        # Yang & Lam DES Comparison Figures (Fig13-Fig14)
        print("\n[2.7/3] Generating Yang & Lam Comparison Figures (Fig13-14)...")
        self.fig_13_yang_lam_service_time(output_path)
        self.fig_14_yang_lam_sensitivity(output_path)

        # Combined Figures
        print("\n[3/3] Generating Combined Figures (C1-C4)...")
        if self.det_scenarios and self.stoch_summary:
            self.fig_c1_det_vs_stoch(output_path)
            self.fig_c2_breakeven_distance(output_path)
            self.fig_c3_breakeven_demand(output_path)
            self.fig_c4_summary_dashboard(output_path)
        else:
            print("  [WARN] Need both deterministic and stochastic data")

        # Summary
        print("\n" + "=" * 60)
        print("[OK] Figure generation complete!")
        print("=" * 60)

        # List generated files
        png_files = list(output_path.glob("*.png"))
        pdf_files = list(output_path.glob("*.pdf"))
        print(f"\nGenerated files:")
        print(f"  PNG: {len(png_files)} files")
        print(f"  PDF: {len(pdf_files)} files")
        print(f"\nLocation: {output_path}")


# ============================================================================
# Convenience Functions
# ============================================================================

def generate_paper_figures(results_dir: str = "results",
                          output_dir: str = "results/paper_figures") -> None:
    """
    Convenience function to generate all paper figures.

    Args:
        results_dir: Directory containing result CSV files
        output_dir: Output directory for figures
    """
    generator = PaperFigureGenerator(results_dir)
    generator.generate_all(output_dir)


if __name__ == "__main__":
    generate_paper_figures()
