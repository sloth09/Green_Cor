---
name: verification-report
description: Creates and maintains MILP optimization verification reports for Green Corridor Ammonia Bunkering project. Use this skill when the user asks to generate verification documents, update verification chapters, compare calculations with optimization results, or create technical reports with formulas and CSV comparisons.
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: "[chapter|all|update]"
---

# Verification Report Skill

Generate and maintain verification reports for the Green Corridor MILP Optimization project.

## When to Use This Skill

- User asks to create/update verification documents
- User wants to verify calculation results against CSV output
- User needs to generate technical reports with formula explanations
- User asks for DOCX/PDF generation of verification chapters

## Target Report Structure

```
docs/verification/
├── 00_index.md              # Table of contents
├── 01_executive_summary.md  # Decision-maker summary
├── 02_parameters.md         # Input parameters with units
├── 03_case1_busan.md        # Case 1 analysis
├── 04_case2_yeosu.md        # Case 2-1 analysis
├── 05_case2_ulsan.md        # Case 2-2 analysis
├── 06_comparison.md         # Cross-case comparison
└── 07_conclusion.md         # Verification checklist
```

## Quick Commands

| Command | Action |
|---------|--------|
| `/verification-report all` | Generate all chapters |
| `/verification-report update` | Update existing chapters with latest results |
| `/verification-report 03` | Generate/update Case 1 chapter only |
| `/verification-report docx` | Generate DOCX files from markdown |

## Workflow

### 1. Read Latest Results
Always start by reading the latest optimization results:
```
results/MILP_scenario_summary_case_*.csv
results/MILP_per_year_results_case_*.csv
```

### 2. Read Config Files
Get current parameters from:
```
config/base.yaml
config/case_1.yaml
config/case_2_yeosu.yaml
config/case_2_ulsan.yaml
```

### 3. Generate Chapters
Follow the chapter-specific guidelines in [reference.md](reference.md).

### 4. Verify Calculations
For each formula, follow this pattern:
1. Show formula with variable definitions
2. Substitute actual values from config
3. Calculate expected result
4. Compare with CSV output
5. Record PASS (diff < 1%) or FAIL (diff > 1%)

## Key Formulas

### Cycle Time (Case 1)
```
Cycle = Shore_Loading + Travel_Out + Travel_Return + Setup + Pumping
      = (Shuttle_Size / 1500) + 1.0 + 1.0 + 2.0 + (Shuttle_Size / Pump_Rate)
```

### Cycle Time (Case 2)
```
Cycle = Shore_Loading + Travel_Out + Travel_Return + Port_Entry_Exit
      + (Vessels_per_Trip × (Movement + Setup + Pumping))

where:
  Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)
  Pumping = Bunker_Volume / Pump_Rate (per vessel)
```

### Shuttle CAPEX
```
CAPEX = 61.5M × (Shuttle_Size / 40000)^0.75
```

### Annuity Factor
```
AF = [1 - (1 + r)^(-n)] / r
where r = 0.07, n = 21 years
AF = 10.8355
```

## Figure References

All figures are in `results/paper_figures/`. Embed with:
```markdown
![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)
```

## DOCX/PDF Generation

Run from `docs/verification/` directory:
```bash
# All chapters to DOCX
for f in 0*.md; do pandoc "$f" -o "${f%.md}_v2.docx"; done

# Combined report
pandoc 0*.md -o Verification_Report_Combined_v2.docx --toc --toc-depth=2

# PDF (requires xelatex)
pandoc 0*.md -o Verification_Report_Combined_v2.pdf --pdf-engine=xelatex --toc
```

## Output Format Requirements

- Use UTF-8 encoding
- Tables: pipe-separated markdown format
- Numbers: 2 decimal places for costs, 4 for ratios
- Units: Always explicit (m³, hours, USD, etc.)
- No emojis in output files

See [reference.md](reference.md) for detailed chapter guidelines.
