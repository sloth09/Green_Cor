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
├── 04_case2_ulsan.md        # Case 2 analysis
├── 05_case3_yeosu.md        # Case 3 analysis
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

### 0. Update reference.md First (CRITICAL)
Before generating any chapter, **always verify** that reference.md has correct parameter values
by comparing against config files. If config values differ from reference.md, **update reference.md first**.
Key parameters to check: STS pump rate, shore pump rate, setup time, MCR values.

### 1. Read Config Files (Authoritative Source)
Always read config FIRST to get current parameters:
```
config/base.yaml           # pump rate, shore pump, setup time, costs
config/case_1.yaml         # Case 1 shuttle sizes, MCR map
config/case_2_ulsan.yaml   # Case 2 shuttle sizes, MCR map
config/case_3_yeosu.yaml   # Case 3 shuttle sizes, MCR map
```

### 2. Read Latest Deterministic Results
Then read optimization results:
```
results/deterministic/MILP_scenario_summary_case_*.csv
results/deterministic/MILP_per_year_results_case_*.csv
```

### 3. Generate Chapters
Follow the chapter-specific guidelines in [reference.md](reference.md).
**Config values override reference.md if they differ.**

### 4. Verify Calculations
For each formula, follow this pattern:
1. Show formula with variable definitions
2. Substitute actual values from config
3. Calculate expected result
4. Compare with CSV output
5. Record PASS (diff < 1%) or FAIL (diff > 1%)

### 5. Include Cycle Timeline Diagrams
Each case chapter (03-05) MUST include a visual timeline diagram showing the time structure
of a single cycle for the optimal shuttle size. Use ASCII box diagrams:

```
|<-- Shore Loading -->|<-- Travel Out -->|<-- Setup In -->|<-- Pumping -->|<-- Setup Out -->|<-- Travel Return -->|
|      3.67 h         |      1.0 h       |     1.0 h      |    2.5 h      |     1.0 h       |      1.0 h          |
|<-------------------------- Total Cycle: 10.17 h ------------------------------------------------->|
```

For Case 2, show per-vessel blocks:
```
|<-- Shore Loading -->|<-- Travel -->|<-- Port Entry -->|<-- Vessel 1 (8.0h) -->|<-- Vessel 2 (8.0h) -->|<-- Port Exit -->|<-- Travel -->|
```

### 6. Generate DOCX/PDF
After markdown generation, ALWAYS generate combined DOCX and PDF files.

## Key Formulas

### Cycle Time (Case 1)
```
Cycle = Shore_Loading + Travel_Out + Setup_In + Pumping + Setup_Out + Travel_Return
      = (Shuttle_Size / 700 + 4.0) + 1.0 + 2.0 + (Shuttle_Size / 500) + 2.0 + 1.0
```

### Cycle Time (Case 2/3)
```
Cycle = Shore_Loading + Travel_Out + Setup_In + VpT × Pumping + Setup_Out + Travel_Return

where:
  Shore_Loading = Shuttle_Size / 700 + 4.0
  Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)
  Pumping = Bunker_Volume / Pump_Rate = 5000 / 500 = 10.0h (per vessel)
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

All figures are in `results/paper_figures/` (working, volatile). Embed with:
```markdown
![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)
```

## Verification Bundle

A self-contained copy of all verification-relevant data, figures, and reports is maintained at `results/verification_bundle/`:
- `data/` - MILP CSVs (copy from `results/deterministic/`)
- `figures/` - Verification-referenced figures (D1, D6, D9, D10, D11)
- `docs/` - All verification markdown, DOCX, and PDF files

Run `python scripts/preserve_paper_results.py --verify` to update the bundle after changes.

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
