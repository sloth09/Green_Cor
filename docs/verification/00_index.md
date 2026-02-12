# Green Corridor MILP Optimization - Verification Report v8.0

**Project**: Ammonia Bunkering Infrastructure Optimization for Busan Port
**Model Version**: v3.1.0 (STS Pump Rate 500 m3/h)
**Report Version**: v8.0
**Date**: 2026-02-12

---

## Table of Contents

| Chapter | Title | Description |
|---------|-------|-------------|
| [01](01_executive_summary.md) | Executive Summary | Key results and decision-maker overview |
| [02](02_parameters.md) | Input Parameters | All model parameters with sources and units |
| [03](03_case1_busan.md) | Case 1: Busan Port | Cycle time, cost, and NPC verification for Case 1 |
| [04](04_case2_ulsan.md) | Case 2: Ulsan to Busan | Cycle time, cost, and NPC verification for Case 2 |
| [05](05_case3_yeosu.md) | Case 3: Yeosu to Busan | Cycle time, cost, and NPC verification for Case 3 |
| [06](06_comparison.md) | Cross-Case Comparison | NPC, LCOA, and cost structure comparison across all cases |
| [07](07_conclusion.md) | Conclusion | Verification checklist and final assessment |

---

## Optimal Results Summary (v3.1.0)

| Case | Route | Optimal Shuttle | Pump | NPC (USD M) | LCOA (USD/ton) |
|------|-------|----------------|------|-------------|-----------------|
| Case 1 | Busan Port (Storage) | 1,000 m3 | 500 m3/h | 447.53 | 1.90 |
| Case 2 | Ulsan -> Busan (59 nm) | 5,000 m3 | 500 m3/h | 906.80 | 3.85 |
| Case 3 | Yeosu -> Busan (86 nm) | 5,000 m3 | 500 m3/h | 1,094.12 | 4.64 |

---

## Data Sources

- **Config files**: `config/base.yaml`, `config/case_1.yaml`, `config/case_2_ulsan.yaml`, `config/case_3_yeosu.yaml`
- **Optimization results**: `results/deterministic/MILP_scenario_summary_case_*.csv`
- **Yearly results**: `results/deterministic/MILP_per_year_results_case_*.csv`
- **Source code**: `src/shuttle_round_trip_calculator.py`, `src/cost_calculator.py`, `src/optimizer.py`

## Verification Criteria

- Difference < 1%: **PASS**
- Difference 1-5%: **REVIEW** (explain)
- Difference > 5%: **FAIL** (investigate)
