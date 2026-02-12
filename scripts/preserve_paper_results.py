#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preserve Paper Results - Copy working pipeline outputs to stable preserved directories.

Copies volatile results from the working pipeline (deterministic/, sensitivity/,
paper_figures/, stochastic*/) into stable, curated directories organized by
analysis type, with a manifest mapping figures to data sources.

New structure (results/preserved/):
  deterministic/    - base optimization data + D-figures
  sensitivity/      - per-analysis subfolder (tornado/, fuel_price/, etc.)
  yang_lam/         - Yang & Lam comparison data + FIG13-14
  cross_cutting/    - figures spanning multiple analyses
  _manifest.csv     - figure-to-data mapping

Also maintains:
  results/paper1_deterministic/  - legacy paper1 layout
  results/paper2_stochastic/     - legacy paper2 layout
  results/verification_bundle/   - self-contained verification package

Usage:
    python scripts/preserve_paper_results.py           # all targets
    python scripts/preserve_paper_results.py --paper1   # paper1 only
    python scripts/preserve_paper_results.py --paper2   # paper2 only
    python scripts/preserve_paper_results.py --verify   # verification bundle only
    python scripts/preserve_paper_results.py --figures   # figures only (all targets)
"""

import argparse
import csv
import shutil
import sys
from pathlib import Path


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

# New preserved directory
PRESERVED_DIR = RESULTS_DIR / "preserved"

# Legacy directories (maintained for backward compatibility)
PAPER1_DIR = RESULTS_DIR / "paper1_deterministic"
PAPER2_DIR = RESULTS_DIR / "paper2_stochastic"
VERIFY_DIR = RESULTS_DIR / "verification_bundle"

# Source directories
DET_DIR = RESULTS_DIR / "deterministic"
SENS_DIR = RESULTS_DIR / "sensitivity"
FIGS_DIR = RESULTS_DIR / "paper_figures"
STOCH_DIRS = {
    'case_1': RESULTS_DIR / "stochastic",
    'case_2': RESULTS_DIR / "stochastic_case2",
    'case_3': RESULTS_DIR / "stochastic_case3",
}
YANG_LAM_DIR = RESULTS_DIR / "yang_lam_des_comparison" / "data"


# Manifest entries: (figure_id, figure_pattern, data_source, analysis_type, description)
MANIFEST_ENTRIES = [
    # Deterministic figures
    ("D1", "D1*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "Total Cost vs Shuttle Size"),
    ("D2", "D2*.png", "deterministic/data/MILP_per_year_results_*.csv", "deterministic", "Yearly Cost Evolution"),
    ("D3", "D3*.png", "deterministic/data/MILP_per_year_results_*.csv", "deterministic", "Yearly Fleet & Demand"),
    ("D4", "D4*.png", "deterministic/data/MILP_per_year_results_*.csv", "deterministic", "Annual Cycles"),
    ("D5", "D5*.png", "deterministic/data/MILP_per_year_results_*.csv", "deterministic", "Utilization Rate"),
    ("D6", "D6*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "Cost Breakdown"),
    ("D7", "D7*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "Cycle Time"),
    ("D8", "D8*.png", "deterministic/data/MILP_per_year_results_*.csv", "deterministic", "Fleet Evolution"),
    ("D9", "D9*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "LCO Comparison"),
    ("D10", "D10*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "Case NPC Comparison"),
    ("D11", "D11*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "Top Configurations"),
    ("D12", "D12*.png", "deterministic/data/MILP_scenario_summary_*.csv", "deterministic", "NPC Heatmaps"),
    # Sensitivity figures
    ("FIG7", "Fig7*.png", "sensitivity/tornado/tornado_det_*.csv", "sensitivity", "Tornado Diagram"),
    ("FIG8", "Fig8*.png", "sensitivity/fuel_price/fuel_price_*.csv", "sensitivity", "Fuel Price Sensitivity"),
    ("FIG9", "Fig9*.png", "sensitivity/breakeven/breakeven_distance_*.csv", "sensitivity", "Break-even Distance"),
    ("FIG10", "Fig10*.png", "sensitivity/demand_scenarios/demand_scenarios_*.csv", "sensitivity", "Demand Scenarios"),
    ("FIGS4", "FigS4*.png", "sensitivity/two_way/two_way_det_*.csv", "sensitivity", "Two-Way Sensitivity"),
    ("FIGS5", "FigS5*.png", "sensitivity/bunker_volume/bunker_volume_*.csv", "sensitivity", "Bunker Volume Sensitivity"),
    # Yang & Lam
    ("FIG13", "Fig13*.png", "yang_lam/data/*.csv", "yang_lam", "Yang & Lam Service Time"),
    ("FIG14", "Fig14*.png", "yang_lam/data/*.csv", "yang_lam", "Yang & Lam Sensitivity"),
    # Stochastic (if available)
    ("S1", "S1*.png", "stochastic data", "stochastic", "Stochastic Result 1"),
    ("S7", "S7*.png", "sensitivity/pump_sensitivity/pump_sensitivity_*.csv", "stochastic", "Pump Sensitivity"),
]


def copy_files(src_dir, dst_dir, patterns, label=""):
    """Copy files matching glob patterns from src to dst."""
    copied = 0
    if not src_dir.exists():
        if label:
            print(f"  [  0 files] {label} (source not found)")
        return 0
    for pattern in patterns:
        for src in src_dir.glob(pattern):
            if src.is_file():
                dst = dst_dir / src.name
                shutil.copy2(src, dst)
                copied += 1
    if label:
        print(f"  [{copied:3d} files] {label}")
    return copied


def copy_named_files(src_dir, dst_dir, filenames, label=""):
    """Copy specific named files from src to dst."""
    copied = 0
    for name in filenames:
        src = src_dir / name
        if src.is_file():
            shutil.copy2(src, dst_dir / src.name)
            copied += 1
    if label:
        print(f"  [{copied:3d} files] {label}")
    return copied


def preserve_new_structure(figures_only=False):
    """Preserve results in new organized structure with manifest."""
    print("\n[New Structure: preserved/]")

    # Create directory structure
    dirs = [
        PRESERVED_DIR / "deterministic" / "data",
        PRESERVED_DIR / "deterministic" / "figures",
        PRESERVED_DIR / "deterministic" / "reports",
        PRESERVED_DIR / "sensitivity" / "tornado",
        PRESERVED_DIR / "sensitivity" / "fuel_price",
        PRESERVED_DIR / "sensitivity" / "breakeven",
        PRESERVED_DIR / "sensitivity" / "demand_scenarios",
        PRESERVED_DIR / "sensitivity" / "two_way",
        PRESERVED_DIR / "sensitivity" / "bunker_volume",
        PRESERVED_DIR / "sensitivity" / "pump_sensitivity",
        PRESERVED_DIR / "yang_lam" / "data",
        PRESERVED_DIR / "yang_lam" / "figures",
        PRESERVED_DIR / "cross_cutting",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    if not figures_only:
        # Deterministic data
        copy_files(DET_DIR, PRESERVED_DIR / "deterministic" / "data",
                   ["MILP_scenario_summary_*.csv", "MILP_per_year_results_*.csv"],
                   "deterministic data")
        # Also copy from root results/ (where main.py actually writes)
        copy_files(RESULTS_DIR, PRESERVED_DIR / "deterministic" / "data",
                   ["MILP_scenario_summary_*.csv", "MILP_per_year_results_*.csv"],
                   "root MILP data")

        # Reports
        copy_files(RESULTS_DIR, PRESERVED_DIR / "deterministic" / "reports",
                   ["MILP_results_*.xlsx", "MILP_Report_*.docx"],
                   "reports")

        # Sensitivity data by analysis type
        sens_map = {
            "tornado": ["tornado_det_*.csv"],
            "fuel_price": ["fuel_price_*.csv"],
            "breakeven": ["breakeven_distance_*.csv"],
            "demand_scenarios": ["demand_scenarios_*.csv"],
            "two_way": ["two_way_det_*.csv"],
            "bunker_volume": ["bunker_volume_*.csv"],
            "pump_sensitivity": ["pump_sensitivity_*.csv"],
        }
        for analysis, patterns in sens_map.items():
            copy_files(SENS_DIR, PRESERVED_DIR / "sensitivity" / analysis,
                       patterns, f"sensitivity/{analysis}")

        # Yang & Lam data
        if YANG_LAM_DIR.exists():
            copy_files(YANG_LAM_DIR, PRESERVED_DIR / "yang_lam" / "data",
                       ["*.csv", "*.txt"], "yang_lam data")

    # Figures by analysis type
    # Deterministic figures
    copy_files(FIGS_DIR, PRESERVED_DIR / "deterministic" / "figures",
               ["D*.png", "D*.pdf"], "deterministic figures")

    # Sensitivity figures mapped to their analysis
    fig_sens_map = {
        "tornado": ["Fig7*.png", "Fig7*.pdf"],
        "fuel_price": ["Fig8*.png", "Fig8*.pdf"],
        "breakeven": ["Fig9*.png", "Fig9*.pdf"],
        "demand_scenarios": ["Fig10*.png", "Fig10*.pdf"],
        "two_way": ["FigS4*.png", "FigS4*.pdf"],
        "bunker_volume": ["FigS5*.png", "FigS5*.pdf"],
        "pump_sensitivity": ["S7*.png", "S7*.pdf"],
    }
    for analysis, patterns in fig_sens_map.items():
        copy_files(FIGS_DIR, PRESERVED_DIR / "sensitivity" / analysis,
                   patterns, f"sensitivity/{analysis} figures")

    # Yang & Lam figures
    copy_files(FIGS_DIR, PRESERVED_DIR / "yang_lam" / "figures",
               ["Fig13*.png", "Fig13*.pdf", "Fig14*.png", "Fig14*.pdf"],
               "yang_lam figures")

    # Generate manifest
    generate_manifest()

    print("[OK] New structure preserved")


def generate_manifest():
    """Generate _manifest.csv mapping figures to data sources."""
    manifest_path = PRESERVED_DIR / "_manifest.csv"
    rows = []

    for fig_id, fig_pattern, data_source, analysis_type, description in MANIFEST_ENTRIES:
        # Find actual figure files
        fig_files = list(FIGS_DIR.glob(fig_pattern)) if FIGS_DIR.exists() else []
        if fig_files:
            for f in fig_files:
                rows.append({
                    'figure_id': fig_id,
                    'figure_file': f.name,
                    'data_source': data_source,
                    'analysis_type': analysis_type,
                    'description': description,
                })
        else:
            rows.append({
                'figure_id': fig_id,
                'figure_file': '(not generated)',
                'data_source': data_source,
                'analysis_type': analysis_type,
                'description': description,
            })

    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['figure_id', 'figure_file', 'data_source', 'analysis_type', 'description'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  [OK] Manifest: {len(rows)} entries -> preserved/_manifest.csv")


def preserve_paper1(figures_only=False):
    """Preserve Paper 1 (Deterministic) results - legacy layout."""
    print("\n[Paper 1: Deterministic (legacy)]")

    for sub in ['data', 'sensitivity', 'figures', 'reports']:
        (PAPER1_DIR / sub).mkdir(parents=True, exist_ok=True)

    if not figures_only:
        copy_files(DET_DIR, PAPER1_DIR / "data",
                   ["MILP_scenario_summary_*.csv", "MILP_per_year_results_*.csv"],
                   "deterministic data -> paper1/data/")
        # Also from root
        copy_files(RESULTS_DIR, PAPER1_DIR / "data",
                   ["MILP_scenario_summary_*.csv", "MILP_per_year_results_*.csv"],
                   "root MILP data -> paper1/data/")

        sens_patterns = [
            "fuel_price_*.csv", "tornado_det_*.csv", "bunker_volume_*.csv",
            "two_way_det_*.csv", "demand_scenarios_*.csv", "breakeven_distance_*.csv",
        ]
        copy_files(SENS_DIR, PAPER1_DIR / "sensitivity",
                   sens_patterns, "sensitivity -> paper1/sensitivity/")

        copy_files(RESULTS_DIR, PAPER1_DIR / "reports",
                   ["MILP_results_*.xlsx", "MILP_Report_*.docx"],
                   "reports -> paper1/reports/")

        if YANG_LAM_DIR.exists():
            (PAPER1_DIR / "yang_lam").mkdir(parents=True, exist_ok=True)
            copy_files(YANG_LAM_DIR, PAPER1_DIR / "yang_lam",
                       ["*.csv", "*.txt"],
                       "yang_lam data -> paper1/yang_lam/")

    fig_patterns = ["D*.png", "D*.pdf", "Fig*.png", "Fig*.pdf",
                    "FigS*.png", "FigS*.pdf"]
    copy_files(FIGS_DIR, PAPER1_DIR / "figures",
               fig_patterns, "figures -> paper1/figures/")

    print("[OK] Paper 1 preserved")


def preserve_paper2(figures_only=False):
    """Preserve Paper 2 (Stochastic) results - legacy layout."""
    print("\n[Paper 2: Stochastic (legacy)]")

    for sub in ['data', 'sensitivity', 'figures', 'reports']:
        (PAPER2_DIR / sub).mkdir(parents=True, exist_ok=True)

    if not figures_only:
        total = 0
        for case_id, stoch_dir in STOCH_DIRS.items():
            if stoch_dir.exists():
                total += copy_files(stoch_dir, PAPER2_DIR / "data",
                                    ["stochastic_*.csv", "deterministic_*.csv"], "")
                cc = stoch_dir / "case_comparison.csv"
                if cc.exists():
                    dst_name = f"case_comparison_{stoch_dir.name}.csv"
                    shutil.copy2(cc, PAPER2_DIR / "data" / dst_name)
                    total += 1
        print(f"  [{total:3d} files] stochastic data -> paper2/data/")

        sens_total = 0
        for case_id, stoch_dir in STOCH_DIRS.items():
            if stoch_dir.exists():
                sens_total += copy_files(stoch_dir, PAPER2_DIR / "sensitivity",
                                         ["tornado_*.csv", "sensitivity_*.csv"], "")
        sens_total += copy_files(SENS_DIR, PAPER2_DIR / "sensitivity",
                                 ["pump_sensitivity_*.csv"], "")
        print(f"  [{sens_total:3d} files] sensitivity -> paper2/sensitivity/")

    fig_patterns = ["S*.png", "S*.pdf", "C*.png", "C*.pdf"]
    copy_files(FIGS_DIR, PAPER2_DIR / "figures",
               fig_patterns, "figures -> paper2/figures/")

    print("[OK] Paper 2 preserved")


def preserve_verification():
    """Preserve Verification Bundle."""
    print("\n[Verification Bundle]")

    for sub in ['data', 'figures', 'docs']:
        (VERIFY_DIR / sub).mkdir(parents=True, exist_ok=True)

    copy_files(DET_DIR, VERIFY_DIR / "data",
               ["MILP_*.csv"], "deterministic data -> verification/data/")
    # Also from root
    copy_files(RESULTS_DIR, VERIFY_DIR / "data",
               ["MILP_scenario_summary_*.csv", "MILP_per_year_results_*.csv"],
               "root MILP data -> verification/data/")

    verify_figs = ["D1_*.png", "D6_*.png", "D9_*.png", "D10_*.png", "D11_*.png"]
    copy_files(FIGS_DIR, VERIFY_DIR / "figures",
               verify_figs, "figures -> verification/figures/")

    ver_docs = DOCS_DIR / "verification"
    if ver_docs.exists():
        doc_total = 0
        doc_total += copy_files(ver_docs, VERIFY_DIR / "docs",
                                ["0*.md", "stochastic_*.md"], "")
        doc_total += copy_files(ver_docs, VERIFY_DIR / "docs",
                                ["Verification_Report_*.docx", "Verification_Report_*.pdf"], "")
        print(f"  [{doc_total:3d} files] docs -> verification/docs/")

    print("[OK] Verification bundle preserved")


def main():
    parser = argparse.ArgumentParser(description="Preserve paper results to stable directories")
    parser.add_argument('--paper1', action='store_true', help='Paper 1 (deterministic) only')
    parser.add_argument('--paper2', action='store_true', help='Paper 2 (stochastic) only')
    parser.add_argument('--verify', action='store_true', help='Verification bundle only')
    parser.add_argument('--figures', action='store_true', help='Figures only (all targets)')
    args = parser.parse_args()

    do_all = not (args.paper1 or args.paper2 or args.verify or args.figures)

    print("=" * 60)
    print("Preserve Paper Results")
    print("=" * 60)

    # Always run new structure
    if do_all or args.figures:
        preserve_new_structure(figures_only=args.figures)

    # Legacy preservation
    if do_all or args.paper1:
        preserve_paper1(figures_only=args.figures)
    if do_all or args.paper2:
        preserve_paper2(figures_only=args.figures)
    if args.figures and not args.paper1:
        preserve_paper1(figures_only=True)
    if args.figures and not args.paper2:
        preserve_paper2(figures_only=True)
    if do_all or args.verify:
        preserve_verification()

    print("\n" + "=" * 60)
    print("[OK] All preservation complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
