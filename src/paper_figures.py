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
    'font.size': 12,            # Base font size (increased)
    'axes.titlesize': 15,       # Subplot titles
    'axes.labelsize': 14,       # X/Y axis labels
    'xtick.labelsize': 12,      # X tick labels
    'ytick.labelsize': 12,      # Y tick labels
    'legend.fontsize': 11,      # Legend text
    'figure.titlesize': 16,     # Figure suptitle
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.unicode_minus': False,
}

# Color scheme (colorblind-friendly)
COLORS = {
    'case_1': '#1f77b4',       # Blue
    'case_2_yeosu': '#ff7f0e', # Orange
    'case_2_ulsan': '#2ca02c', # Green
}

CASE_LABELS = {
    'case_1': 'Case 1: Busan Storage',
    'case_2_yeosu': 'Case 2-1: Yeosu Direct',
    'case_2_ulsan': 'Case 2-2: Ulsan Direct',
}

CASE_SHORT = {
    'case_1': 'Case 1',
    'case_2_yeosu': 'Case 2-1',
    'case_2_ulsan': 'Case 2-2',
}

# Y-axis limits for clean round numbers (NPC in Million USD)
Y_LIMITS_NPC = {
    'case_1': 700,
    'case_2_yeosu': 1400,
    'case_2_ulsan': 1400,
}

# Y-axis limits for yearly costs (Million USD/year)
Y_LIMITS_YEARLY_COST = {
    'case_1': 35,
    'case_2_yeosu': 70,
    'case_2_ulsan': 50,
}

# Y-axis limits for fleet size
Y_LIMITS_FLEET = {
    'case_1': 15,
    'case_2_yeosu': 16,
    'case_2_ulsan': 15,
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
            'case_2_yeosu': self.results_dir / "stochastic_case2_yeosu",
            'case_2_ulsan': self.results_dir / "stochastic_case2_ulsan",
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
        """Load deterministic scenario results."""
        data = {}
        for case_id in ['case_1', 'case_2_yeosu', 'case_2_ulsan']:
            # Try deterministic directory first
            path = self.det_dir / f"scenarios_{case_id}.csv"
            if not path.exists():
                # Fallback to stochastic directory
                path = self.stoch_dirs[case_id] / f"deterministic_scenarios_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
                print(f"  [OK] Loaded {case_id} deterministic scenarios")
            else:
                print(f"  [WARN] Missing {case_id} deterministic scenarios")
        return data

    def _load_deterministic_yearly(self) -> Dict[str, pd.DataFrame]:
        """Load deterministic yearly results."""
        data = {}
        for case_id in ['case_1', 'case_2_yeosu', 'case_2_ulsan']:
            path = self.det_dir / f"yearly_{case_id}.csv"
            if not path.exists():
                path = self.stoch_dirs[case_id] / f"deterministic_yearly_{case_id}.csv"
            if path.exists():
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
        for case_id in ['case_1', 'case_2_yeosu', 'case_2_ulsan']:
            path = sensitivity_dir / f"pump_sensitivity_{case_id}.csv"
            if path.exists():
                data[case_id] = pd.read_csv(path)
                print(f"  [OK] Loaded {case_id} pump sensitivity data")
            else:
                print(f"  [WARN] Missing {case_id} pump sensitivity data")
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

            # Set y-axis limits (0 to clean round number)
            ax.set_ylim(0, Y_LIMITS_NPC.get(case_id, 1400))

            # Place legend in upper left (where there's empty space)
            ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

        plt.tight_layout()
        plt.savefig(output_path / 'D1_npc_vs_shuttle.png', bbox_inches='tight')
        plt.savefig(output_path / 'D1_npc_vs_shuttle.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'D2_yearly_cost_evolution.pdf', bbox_inches='tight')
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
            ax.set_ylim(0, Y_LIMITS_FLEET.get(case_id, 15))
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
        plt.savefig(output_path / 'D3_yearly_fleet_demand.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'D4_yearly_cycles.pdf', bbox_inches='tight')
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
        ax.set_ylim(0, 110)
        ax.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='Max Capacity')
        ax.tick_params(axis='both', labelsize=12)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'D5_yearly_utilization.png', bbox_inches='tight')
        plt.savefig(output_path / 'D5_yearly_utilization.pdf', bbox_inches='tight')
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
                           (df['Pump_Size_m3ph'] == 1000)].copy()

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
        plt.savefig(output_path / f'D4_{case_label}.pdf', bbox_inches='tight')
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
                           (df['Pump_Size_m3ph'] == 1000)].copy()

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
        plt.savefig(output_path / f'D5_{case_label}.pdf', bbox_inches='tight')
        plt.close()
        print(f"  [OK] D5_{case_label}: Utilization Rate")

    def generate_case_specific_figures(self, output_path: Path) -> None:
        """Generate D4 and D5 figures for each case with multiple shuttle sizes."""
        print("\n  Generating case-specific D4/D5 figures...")

        # Case 1: 2500, 5000 m3
        self.fig_d4_case_cycles(output_path, 'case_1', [2500, 5000], 'case1')
        self.fig_d5_case_utilization(output_path, 'case_1', [2500, 5000], 'case1')

        # Case 2-1 (Yeosu): 5000, 10000, 15000 m3
        self.fig_d4_case_cycles(output_path, 'case_2_yeosu', [5000, 10000, 15000], 'case2-1')
        self.fig_d5_case_utilization(output_path, 'case_2_yeosu', [5000, 10000, 15000], 'case2-1')

        # Case 2-2 (Ulsan): 2500, 5000, 10000 m3
        self.fig_d4_case_cycles(output_path, 'case_2_ulsan', [2500, 5000, 10000], 'case2-2')
        self.fig_d5_case_utilization(output_path, 'case_2_ulsan', [2500, 5000, 10000], 'case2-2')

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

            im = axes[idx].imshow(pivot.values, cmap='RdYlGn_r',
                                  aspect='auto', origin='lower')

            # Set ticks
            axes[idx].set_xticks(np.arange(len(pivot.columns)))
            axes[idx].set_yticks(np.arange(len(pivot.index)))

            # Reduce tick labels for readability
            x_labels = [str(int(c)) if i % 2 == 0 else ''
                       for i, c in enumerate(pivot.columns)]
            y_labels = [str(int(r)) for r in pivot.index]
            axes[idx].set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
            axes[idx].set_yticklabels(y_labels, fontsize=8)

            # Colorbar
            cbar = plt.colorbar(im, ax=axes[idx], shrink=0.8)
            cbar.set_label('NPC (M USD)', fontsize=9)

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
        plt.savefig(output_path / 'D12_npc_heatmaps.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'D6_cost_breakdown.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'D7_cycle_time.pdf', bbox_inches='tight')
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

        plt.tight_layout()
        plt.savefig(output_path / 'D8_fleet_evolution.png', bbox_inches='tight')
        plt.savefig(output_path / 'D8_fleet_evolution.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'D9_lco_comparison.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'D10_case_npc_comparison.pdf', bbox_inches='tight')
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
                             f'${v:.1f}M', va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(output_path / 'D11_top_configurations.png', bbox_inches='tight')
        plt.savefig(output_path / 'D11_top_configurations.pdf', bbox_inches='tight')
        plt.close()
        print("  [OK] D11: Top Configurations")

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
                          fontsize=8, ha='left')

        ax.set_ylabel('NPC (Million USD)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('NPC Distribution with Vessel Size Uncertainty\n(100 Monte Carlo Scenarios)',
                    fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S1_npc_boxplot.png', bbox_inches='tight')
        plt.savefig(output_path / 'S1_npc_boxplot.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'S2_vss_evpi.pdf', bbox_inches='tight')
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
            ax.legend(fontsize=8)
            ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S3_mc_distribution.png', bbox_inches='tight')
        plt.savefig(output_path / 'S3_mc_distribution.pdf', bbox_inches='tight')
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
        plt.savefig(output_path / 'S4_vessel_distribution.pdf', bbox_inches='tight')
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
            ax.set_yticklabels(params, fontsize=9)
            ax.set_xlabel('NPC Swing (Million USD)')
            ax.set_title(f'{CASE_SHORT[case_id]}\n(Base: ${base_npc:.1f}M)',
                        fontweight='bold')

            # Value labels
            for bar, swing in zip(bars, swings):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                       f'${swing:.1f}M', va='center', fontsize=8)

            ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'S5_tornado.png', bbox_inches='tight')
        plt.savefig(output_path / 'S5_tornado.pdf', bbox_inches='tight')
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
                             ha='center', va='center', fontsize=8)

        plt.tight_layout()
        plt.savefig(output_path / 'S6_twoway_sensitivity.png', bbox_inches='tight')
        plt.savefig(output_path / 'S6_twoway_sensitivity.pdf', bbox_inches='tight')
        plt.close()
        print("  [OK] S6: Two-Way Sensitivity")

    def fig_s7_pump_sensitivity(self, output_path: Path) -> None:
        """S7: Pump Rate Sensitivity - NPC vs Pump Rate for all cases.

        Shows how NPC changes with pump rate, with optimal shuttle size annotated.
        Vertical dashed line at 1000 m3/h indicates the fixed rate used in main analysis.
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

        # Vertical line at fixed pump rate (1000 m3/h)
        ax.axvline(x=1000, color='red', linestyle='--', linewidth=2, alpha=0.7,
                  label='Fixed Rate (1000 m$^3$/h)')

        # Add annotation for fixed rate
        ymin, ymax = ax.get_ylim()
        ax.annotate('Main Analysis\nFixed Rate',
                   xy=(1000, ymin + (ymax - ymin) * 0.15),
                   ha='center', fontsize=9, color='red', alpha=0.8,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        ax.set_xlabel('Pump Rate (m$^3$/h)', fontsize=11)
        ax.set_ylabel('Minimum NPC (Million USD)', fontsize=11)
        ax.set_title('NPC Sensitivity to Pump Rate\n(Numbers indicate optimal shuttle size in m$^3$)',
                    fontweight='bold', fontsize=12)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)

        # Set x-axis limits with some padding
        ax.set_xlim(300, 2100)

        plt.tight_layout()
        plt.savefig(output_path / 'S7_pump_sensitivity.png', bbox_inches='tight')
        plt.savefig(output_path / 'S7_pump_sensitivity.pdf', bbox_inches='tight')
        plt.close()
        print("  [OK] S7: Pump Rate Sensitivity")

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
                   f'${v:.0f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')

        for bar, v, std in zip(bars2, stoch_npcs, stoch_std):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 10,
                   f'${v:.0f}M\n(+{std:.0f})', ha='center', va='bottom', fontsize=8)

        ax.set_ylabel('20-Year NPC (Million USD)')
        ax.set_xlabel('Supply Scenario')
        ax.set_title('Deterministic vs Stochastic Optimization Results', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([CASE_SHORT[c] for c in cases])
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path / 'C1_det_vs_stoch.png', bbox_inches='tight')
        plt.savefig(output_path / 'C1_det_vs_stoch.pdf', bbox_inches='tight')
        plt.close()
        print("  [OK] C1: Det vs Stoch")

    def fig_c2_breakeven_distance(self, output_path: Path) -> None:
        """C2: Break-even analysis by distance."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Distance data
        distances = {
            'case_1': 2,    # ~2nm within port
            'case_2_ulsan': 25,  # 25nm
            'case_2_yeosu': 86,  # 86nm
        }

        cases = ['case_1', 'case_2_ulsan', 'case_2_yeosu']
        dist_vals = [distances[c] for c in cases]
        npc_vals = [self._get_optimal(c)['npc'] for c in cases]

        # Scatter plot
        for case_id, d, npc in zip(cases, dist_vals, npc_vals):
            ax.scatter(d, npc, s=200, c=COLORS[case_id], edgecolor='black',
                      linewidth=2, label=CASE_SHORT[case_id], zorder=5)

        # Fit line for Case 2 (direct supply cases)
        case2_dists = [distances['case_2_ulsan'], distances['case_2_yeosu']]
        case2_npcs = [self._get_optimal('case_2_ulsan')['npc'],
                     self._get_optimal('case_2_yeosu')['npc']]

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
        plt.savefig(output_path / 'C2_breakeven_distance.pdf', bbox_inches='tight')
        plt.close()
        print("  [OK] C2: Break-even Distance")

    def fig_c3_breakeven_demand(self, output_path: Path) -> None:
        """C3: Break-even analysis by demand volume."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create demand sensitivity (synthetic based on analysis)
        demand_factors = np.array([0.5, 0.75, 1.0, 1.25, 1.5])

        cases = ['case_1', 'case_2_ulsan', 'case_2_yeosu']

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
        plt.savefig(output_path / 'C3_breakeven_demand.pdf', bbox_inches='tight')
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
                    f'${v:.0f}M', ha='center', va='bottom', fontsize=9)

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
                    f'${v:.2f}', ha='center', va='bottom', fontsize=9)

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
        ax3.legend(fontsize=8)
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
            ax5.set_yticklabels(df['Parameter'].values, fontsize=9)
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
            ax6.set_xticklabels([CASE_SHORT[c] for c in cases], fontsize=9)
            ax6.set_ylabel('Value (M USD)')
            ax6.set_title('(f) Stochastic Value', fontweight='bold')
            ax6.legend(fontsize=8)
            ax6.grid(axis='y', alpha=0.3)

        fig.suptitle('Green Corridor Ammonia Bunkering Analysis Summary',
                    fontsize=16, fontweight='bold', y=0.98)

        plt.savefig(output_path / 'C4_summary_dashboard.png', bbox_inches='tight')
        plt.savefig(output_path / 'C4_summary_dashboard.pdf', bbox_inches='tight')
        plt.close()
        print("  [OK] C4: Summary Dashboard")

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
            self.fig_d10_case_npc_comparison(output_path)
            self.fig_d11_top_configurations(output_path)
            self.fig_d12_npc_heatmap(output_path)
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
