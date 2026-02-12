#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate paper.pdf directly from paper_final.md via pandoc + xelatex.

This avoids the docx intermediate step, preserving LaTeX math rendering.
Figures are inserted inline at their first reference point.
"""

import re
import os
import sys
import subprocess
import tempfile

PAPER_MD = r"D:\code\Green_Cor\docs\paper\v4\paper_final.md"
OUTPUT_PDF = r"D:\code\Green_Cor\docs\paper\v4\paper.pdf"
FIGURES_DIR = r"D:\code\Green_Cor\results\paper_figures"
PANDOC = r"C:\Users\user\AppData\Local\Pandoc\pandoc.exe"

# Figure label -> (filename, caption)
FIGURE_MAP = {
    "Fig. 1": ("D7_cycle_time.png", "Cycle time components for three supply chain configurations"),
    "Fig. 2": ("D1_npc_vs_shuttle.png", "Net present cost vs shuttle size for all cases"),
    "Fig. 3": ("D10_case_npc_comparison.png", "NPC comparison across cases at optimal configurations"),
    "Fig. 4": ("D6_cost_breakdown.png", "Cost component breakdown (CAPEX/OPEX)"),
    "Fig. 5": ("D9_lco_comparison.png", "Levelized cost of ammonia bunkering by case"),
    "Fig. 6": ("D2_yearly_cost_evolution.png", "Annual cost evolution (2030-2050)"),
    "Fig. 7": ("D8_fleet_evolution.png", "Fleet size evolution over planning horizon"),
    "Fig. 8": ("D3_yearly_fleet_demand.png", "Annual bunkering demand and fleet response"),
    "Fig. 9": ("D5_yearly_utilization.png", "Fleet utilization rates over time"),
    "Fig. 10": ("Fig7_tornado_deterministic.png", "Tornado diagram: parametric sensitivity of NPC"),
    "Fig. 11": ("Fig8_fuel_price_sensitivity.png", "Fuel price sensitivity: NPC and LCO response"),
    "Fig. 12": ("Fig9_breakeven_distance.png", "Break-even distance analysis: Case 1 vs Case 2"),
    "Fig. 13": ("Fig10_demand_scenarios.png", "Demand scenario analysis: NPC and LCO"),
    "Fig. 14": ("S7_pump_sensitivity.png", "Pump rate sensitivity analysis"),
    "Fig. 15": ("Fig11_discount_rate_sensitivity.png", "Discount rate sensitivity: NPC and LCOA across three cases"),
    "Fig. 16": ("Fig12_discount_rate_fleet.png", "Fleet evolution under different discount rates"),
    "Fig. 17": ("Fig13_yang_lam_service_time.png", "Service time comparison: MILP model vs Yang and Lam DES model"),
    "Fig. 18": ("Fig14_yang_lam_sensitivity.png", "Flow rate sensitivity comparison: MILP vs DES model"),
    "Fig. S1": ("D12_npc_heatmaps.png", "NPC sensitivity heatmap (shuttle size x pump rate)"),
    "Fig. S2": ("D11_top_configurations.png", "Top configurations ranked by NPC"),
    "Fig. S3": ("D4_yearly_cycles.png", "Annual cycle count evolution"),
    "Fig. S4": ("FigS4_twoway_deterministic.png", "Two-way sensitivity: fuel price x bunker volume"),
    "Fig. S5": ("FigS5_bunker_volume_sensitivity.png", "Bunker volume sensitivity: NPC and LCO response"),
}


def build_markdown_with_figures(md_path):
    """Read paper_final.md and insert figure images at first reference points."""
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    inserted = set()
    output = []
    in_table = False

    for line in lines:
        output.append(line)

        # Don't insert figures inside tables
        stripped = line.strip()
        if stripped.startswith("|"):
            in_table = True
            continue
        elif in_table and not stripped.startswith("|"):
            in_table = False

        # Check for figure references in non-table lines
        refs = re.findall(r"Fig\. (S?\d+)", line)
        for ref_num in refs:
            fig_key = f"Fig. {ref_num}"
            if fig_key in FIGURE_MAP and fig_key not in inserted:
                filename, caption = FIGURE_MAP[fig_key]
                img_path = os.path.join(FIGURES_DIR, filename).replace("\\", "/")
                if os.path.exists(img_path):
                    output.append("\n")
                    output.append(f"![*{fig_key}. {caption}*]({img_path}){{ width=95% }}\n")
                    output.append("\n")
                    inserted.add(fig_key)

    # Append supplementary figures not referenced in body
    remaining = [k for k in FIGURE_MAP if k not in inserted]
    if remaining:
        output.append("\n## Supplementary Figures\n\n")
        for fig_key in remaining:
            filename, caption = FIGURE_MAP[fig_key]
            img_path = os.path.join(FIGURES_DIR, filename).replace("\\", "/")
            if os.path.exists(img_path):
                output.append(f"![*{fig_key}. {caption}*]({img_path}){{ width=95% }}\n\n")
                inserted.add(fig_key)

    print(f"[OK] {len(inserted)} figures inserted into markdown")
    return "".join(output)


def convert_to_pdf(md_content, output_path):
    """Convert markdown string to PDF via pandoc + xelatex."""
    # Write temp markdown file
    tmp_dir = os.path.dirname(output_path)
    tmp_md = os.path.join(tmp_dir, "_paper_with_figures.md")
    with open(tmp_md, "w", encoding="utf-8") as f:
        f.write(md_content)

    cmd = [
        PANDOC, tmp_md,
        "-o", output_path,
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=1in",
        "-V", "mainfont=Times New Roman",
        "-V", "fontsize=11pt",
        "-V", "linestretch=1.15",
        "-V", "documentclass=article",
        "--number-sections",
        "--highlight-style=tango",
        "-V", "header-includes=\\usepackage{float}\\floatplacement{figure}{H}",
    ]

    print(f"[INFO] Running pandoc...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    # Clean up temp file
    if os.path.exists(tmp_md):
        os.remove(tmp_md)

    if result.returncode != 0:
        print(f"[ERROR] pandoc failed:\n{result.stderr[:2000]}")
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[OK] {output_path} saved ({size_mb:.1f} MB)")


def main():
    if not os.path.exists(PAPER_MD):
        print(f"[ERROR] {PAPER_MD} not found")
        sys.exit(1)

    if not os.path.exists(PANDOC):
        print(f"[ERROR] pandoc not found at {PANDOC}")
        sys.exit(1)

    md_content = build_markdown_with_figures(PAPER_MD)
    convert_to_pdf(md_content, OUTPUT_PDF)


if __name__ == "__main__":
    main()
