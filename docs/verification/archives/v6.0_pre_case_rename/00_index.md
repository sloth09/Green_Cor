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

**Report Version**: v6.0 (Shore Pump 700 m3/h + Setup 2.0h + Fixed Time 4.0h)

**Generated**: 2026-02-11

**Data Source**: `results/deterministic/MILP_scenario_summary_case_*.csv`

---

## Version Changes (v6.0)

This report reflects major parameter updates from the previous version (v5.1):

| Parameter | v5.1 Value | v6.0 Value | Impact |
|-----------|-----------|-----------|--------|
| **Shore Pump Rate** | 1,500 m3/h | **700 m3/h** | Shore loading time more than doubled |
| **Setup Time (per endpoint)** | 0.5h (x2 multiplier in code) = 1.0h | **2.0h (direct, no multiplier)** | Setup time doubled |
| **Shore Loading Fixed Time** | 2.0 hours | **4.0 hours** | Fixed overhead doubled |
| **Pump Sensitivity Range** | 400-2000 (9 pts) | **100-1500 (15 pts)** | Wider low-end exploration |

### Code Change: Setup Time Multiplier Removal

Previous code applied a hidden `2.0x` multiplier to the config value:
```
v5.1: config=0.5 -> code: 2.0 * 0.5 = 1.0h per endpoint
v6.0: config=2.0 -> code: 2.0h per endpoint (direct, no multiplier)
```

This change improves code clarity without changing the setup time model -- it is purely a
config/code refactoring that coincides with the actual parameter value increase from 1.0h to 2.0h.

### Key Impacts

1. **Case 1**: Cycle time 10.17h -> 16.07h (+58%), NPC $290.81M -> $410.34M (+41%)
2. **Case 2-1 (Yeosu)**: Cycle time 26.13h -> 34.60h (+32%), NPC $879.88M -> $1,014.81M (+15%)
3. **Case 2-2 (Ulsan)**: Cycle time 22.53h -> 31.00h (+38%), NPC $700.68M -> $830.65M (+19%)
4. **Optimal shuttles unchanged**: Case 1 = 2,500 m3, Case 2 = 5,000 m3
5. **500 m3 shuttle eliminated**: Call duration exceeds 80h constraint with new parameters

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
