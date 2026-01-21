# Verification Report Skill

## Overview

This skill guides the creation and maintenance of MILP optimization verification reports for the Green Corridor Ammonia Bunkering project.

## Target Report Structure

```
docs/verification/
├── 00_index.md              # Table of contents, auto-updated links
├── 01_executive_summary.md  # Decision-maker summary
├── 02_parameters.md         # All input parameters with units
├── 03_case1_busan.md        # Case 1 detailed analysis
├── 04_case2_yeosu.md        # Case 2-1 detailed analysis
├── 05_case2_ulsan.md        # Case 2-2 detailed analysis
├── 06_comparison.md         # Cross-case comparison with figures
└── 07_conclusion.md         # Verification checklist
```

## Chapter-by-Chapter Guidelines

### 01_executive_summary.md
**Audience**: Decision makers, non-technical readers
**Style**: Conclusion-first, 3-line summary, one summary table
**Content**:
- Optimal configuration per case (shuttle size, pump rate)
- Key metrics: NPC, LCOAmmonia, fleet size
- One-paragraph recommendation

### 02_parameters.md
**Audience**: Technical reviewers, auditors
**Style**: Table-centric, all units explicit, source file references
**Content**:
- Economic parameters (discount_rate, annualization_interest_rate)
- Operational parameters (max_annual_hours, setup_time)
- Case-specific parameters (travel_time, shuttle sizes)

### 03-05_case_analysis.md
**Audience**: Analysts, engineers
**Style**: Formula → Example → Verification
**Content per section**:

1. **Cycle Time Calculation**
   - Full formula with variable definitions
   - Numerical example with actual values
   - Comparison with CSV output

2. **Cost Verification**
   - CAPEX formula + example
   - OPEX formula + example
   - Annualization calculation

3. **Shuttle Comparison Table**
   - Multiple shuttle sizes side-by-side
   - Key metrics: NPC, LCO, Cycle Time, Annual Cycles

### 06_comparison.md
**Audience**: Managers, researchers
**Style**: Visual-first (figures), minimal text
**Content**:
- D1: NPC vs Shuttle Size (all cases)
- D2: Annual Cost Evolution
- D3: Fleet Size & Supply
- D4: Annual Cycles
- D5: Utilization Rate
- Optional: D6, D7, D9

### 07_conclusion.md
**Audience**: All stakeholders
**Style**: Checklist format
**Content**:
- Verification checklist (PASS/FAIL per item)
- Discrepancy notes (if any)
- Final recommendation

## Editing Individual Chapters

To modify a specific chapter without regenerating others:

1. Read the target chapter file
2. Identify the section to modify
3. Make targeted edits
4. Update 00_index.md if chapter title changed

## Formula Templates

### Cycle Time (Case 1)
```
Cycle = Shore_Loading + Travel_Out + Travel_Return + Setup + Pumping
      = (Shuttle_Size / 1500) + T_travel + T_travel + 2.0 + (Shuttle_Size / Pump_Rate)
```

### Cycle Time (Case 2)
```
Cycle = Shore_Loading + Travel_Out + Travel_Return + Port_Entry_Exit
      + (Vessels_per_Trip × (Movement + Setup + Pumping))

where:
  Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)
  Pumping = Bunker_Volume / Pump_Rate
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

### NPC Calculation (No Discounting)
```
NPC = sum over years (Annualized_CAPEX + Fixed_OPEX + Variable_OPEX)
```

## Figure References

All figures are located in: `results/paper_figures/`

| Figure | Filename | Description |
|--------|----------|-------------|
| D1 | D1_npc_vs_shuttle.png | NPC vs Shuttle Size |
| D2 | D2_yearly_cost_evolution.png | Annual Cost Evolution |
| D3 | D3_yearly_fleet_demand.png | Fleet Size & Supply |
| D4 | D4_yearly_cycles.png | Annual Cycles |
| D5 | D5_yearly_utilization.png | Utilization Rate |
| D6 | D6_cost_breakdown.png | Cost Breakdown |
| D7 | D7_cycle_time.png | Cycle Time |
| D9 | D9_lco_comparison.png | LCO Comparison |
| D10 | D10_case_npc_comparison.png | NPC Comparison |

## Verification Workflow

1. Calculate expected value using formula
2. Compare with CSV result
3. Record PASS if difference < 1%
4. Record FAIL and stop if difference > 1%

## Key Validation Points

| Item | Expected | Source |
|------|----------|--------|
| Annuity Factor | 10.8355 | [1-(1.07)^(-21)]/0.07 |
| Discount Rate | 0.0 | base.yaml |
| Pump Rate | 1000 m3/h | base.yaml |
| Max Annual Hours | 8000 | base.yaml |

---

## DOCX/PDF Generation Workflow

### Prerequisites
- pandoc (version 3.x+)
- xelatex (for PDF with Unicode support)

### Directory Structure
```
docs/verification/
├── *.md                    # Source markdown files
├── *_v2.docx              # Generated Word documents
├── *_v2.pdf               # Generated PDF documents
└── Verification_Report_Combined_v2.docx/pdf  # Combined report
```

### Step 1: Generate Individual Chapter DOCX

Run from `docs/verification/` directory:

```bash
# Single chapter
pandoc 01_executive_summary.md -o 01_executive_summary_v2.docx

# All chapters (bash loop)
for f in 0*.md; do
  name="${f%.md}"
  pandoc "$f" -o "${name}_v2.docx"
done
```

**Important**: Run pandoc from `docs/verification/` so image paths (`../../results/paper_figures/`) resolve correctly.

### Step 2: Generate Combined DOCX with TOC

```bash
pandoc 00_index.md 01_executive_summary.md 02_parameters.md \
       03_case1_busan.md 04_case2_yeosu.md 05_case2_ulsan.md \
       06_comparison.md 07_conclusion.md \
       -o Verification_Report_Combined_v2.docx \
       --toc --toc-depth=2
```

### Step 3: Generate PDF (with xelatex for Unicode)

```bash
# Single chapter
pandoc 01_executive_summary.md -o 01_executive_summary_v2.pdf --pdf-engine=xelatex

# Combined with TOC
pandoc 00_index.md 01_executive_summary.md 02_parameters.md \
       03_case1_busan.md 04_case2_yeosu.md 05_case2_ulsan.md \
       06_comparison.md 07_conclusion.md \
       -o Verification_Report_Combined_v2.pdf \
       --pdf-engine=xelatex --toc --toc-depth=2
```

### Image Handling

Images in MD files use relative paths:
```markdown
![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)
```

- **DOCX**: Images are embedded automatically when pandoc runs from correct directory
- **PDF**: Same behavior with xelatex engine

### Table Formatting

Pandoc preserves markdown tables in DOCX format:
```markdown
| Case | NPC | LCO |
|------|-----|-----|
| Case 1 | $237M | $1.01/ton |
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Images not found | Run pandoc from `docs/verification/` directory |
| Unicode errors in PDF | Use `--pdf-engine=xelatex` |
| Permission denied | Close Word/PDF viewer first |
| Tables not formatted | Check markdown table syntax (pipes aligned) |

### Quick Commands (Copy-Paste)

```bash
# Full regeneration (from docs/verification/)
cd docs/verification

# Generate all DOCX
for f in 0*.md; do pandoc "$f" -o "${f%.md}_v2.docx"; done

# Generate all PDF
for f in 0*.md; do pandoc "$f" -o "${f%.md}_v2.pdf" --pdf-engine=xelatex; done

# Generate combined
pandoc 0*.md -o Verification_Report_Combined_v2.docx --toc --toc-depth=2
pandoc 0*.md -o Verification_Report_Combined_v2.pdf --pdf-engine=xelatex --toc --toc-depth=2
```
