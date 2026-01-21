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

**Report Version**: v4.1 (MCR/SFOC Update + Ulsan Distance Change)

**Generated**: 2026-01-21

**Data Source**: `results/MILP_scenario_summary_case_*.csv`

---

## Version Changes (v4.1)

This report reflects the following parameter updates from the previous version:

| Parameter | Old Value | New Value | Notes |
|-----------|-----------|-----------|-------|
| **Case 2-2 Distance** | 25 nm | 59 nm | Corrected Ulsan-Busan sea route |
| **MCR Map** | Previous estimates | MAN Energy Solutions official data | Updated for all shuttle sizes |
| **SFOC Map** | Uniform value | DWT-based engine type matching | Different SFOC per vessel size |

### Key Impacts

1. **Case 2-2 (Ulsan)**: Travel time increased from 1.67 hr to 3.93 hr per leg
2. **OPEX Calculations**: More accurate fuel cost estimation with size-specific SFOC
3. **Optimal Configurations**: May differ from previous versions due to corrected parameters

---

## Document Conventions

- **PASS**: Calculated value matches CSV within 1% tolerance
- **FAIL**: Calculated value differs from CSV by more than 1%
- All costs in USD millions (USDm) unless otherwise noted
- Time periods: 2030-2050 (21 years)
- Discount rate: 0% (no time value discounting)
- Annualization interest rate: 7% (for asset annualization)
