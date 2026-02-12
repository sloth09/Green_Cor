# Green Corridor MILP Verification Report

## Table of Contents

1. [Executive Summary](01_executive_summary.md)
2. [Parameters](02_parameters.md)
3. [Case 1: Busan Port](03_case1_busan.md)
4. [Case 2-1: Yeosu to Busan](04_case2_yeosu.md)
5. [Case 2-2: Ulsan to Busan](05_case2_ulsan.md)
6. [Cross-Case Comparison](06_comparison.md)
7. [Conclusion & Checklist](07_conclusion.md)

---

**Report Version**: v5.1 (Shore Loading Fixed Time + v5 MCR Power Law)

**Generated**: 2026-02-02

**Data Source**: `results/deterministic/MILP_scenario_summary_case_*.csv`

---

## Version Changes (v5.1)

This report reflects the following parameter updates from the previous version (v5):

| Parameter | v5 Value | v5.1 Value | Notes |
|-----------|----------|------------|-------|
| **Shore Loading Fixed Time** | 0.0 hours | 2.0 hours | Added fixed setup/shutdown time for shore loading |
| **MCR Map** | v5 Power Law | v5 Power Law (same) | No change - already using Power Law |
| **Data Source** | `results/MILP_*.csv` | `results/deterministic/MILP_*.csv` | Reorganized file structure |

### Key Impacts

1. **All Cases**: Shore loading time increased by 2.0 hours per cycle
2. **Case 1**: Cycle time +2.0h (8.17 -> 10.17 hr for 2500 m3), NPC +16.4%
3. **Case 2**: Cycle time +2.0h, proportionally smaller impact due to longer base cycles
4. **Optimal shuttles unchanged**: Same shuttle sizes remain optimal for all cases

---

## Verification Method

Each chapter (03-05) performs full hand calculations:
1. Extract parameters from YAML config files
2. Apply formulas with actual values (step-by-step calculation)
3. Compare calculated values against CSV optimizer output
4. Record PASS/FAIL status

**All 13 verification items PASSED for all 3 cases** (39/39 total checks).

---

## Document Conventions

- **PASS**: Calculated value matches CSV within 1% tolerance
- **FAIL**: Calculated value differs from CSV by more than 1%
- All costs in USD millions (USDm) unless otherwise noted
- Time periods: 2030-2050 (21 years)
- Discount rate: 0% (no time value discounting)
- Annualization interest rate: 7% (for asset annualization)
