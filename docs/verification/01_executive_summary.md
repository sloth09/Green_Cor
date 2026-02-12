# 1. Executive Summary

## 1.1 Purpose

This report verifies the MILP optimization model (v3.1.0) for ammonia bunkering infrastructure at Busan Port. All calculations are independently reproduced from config parameters and compared against CSV output from the optimization solver.

## 1.2 Model Overview

The model determines the optimal shuttle vessel size and fleet composition to minimize the 20-year Net Present Cost (NPC) of ammonia fuel supply for the Green Corridor initiative (2030-2050).

**Key assumptions:**
- Time horizon: 21 years (2030-2050 inclusive)
- Fleet growth: 50 vessels (2030) to 500 vessels (2050), linear interpolation
- Bunker volume per call: 5,000 m3
- STS pump rate: 500 m3/h (fixed)
- Discount rate: 0% (no time-value discounting)
- Annualization interest rate: 7% (for asset cost annualization only)

## 1.3 Key Results

### Optimal Configurations

| Case | Description | Shuttle | NPC (USD M) | LCOA (USD/ton) |
|------|-------------|---------|-------------|-----------------|
| Case 1 | Busan Port with Storage | 1,000 m3 | 447.53 | 1.90 |
| Case 2 | Ulsan -> Busan (59 nm) | 5,000 m3 | 906.80 | 3.85 |
| Case 3 | Yeosu -> Busan (86 nm) | 5,000 m3 | 1,094.12 | 4.64 |

### Cost Structure (Optimal Scenarios)

| Component | Case 1 (USD M) | Case 2 (USD M) | Case 3 (USD M) |
|-----------|----------------|----------------|----------------|
| Shuttle CAPEX (annualized) | 211.97 | 384.21 | 422.39 |
| Bunkering CAPEX (annualized) | 15.06 | 16.24 | 17.86 |
| Shuttle Fixed OPEX | 114.84 | 208.15 | 228.84 |
| Bunkering Fixed OPEX | 8.16 | 8.80 | 9.67 |
| Shuttle Variable OPEX | 80.84 | 275.01 | 400.97 |
| Bunkering Variable OPEX | 16.67 | 14.39 | 14.39 |
| **NPC Total** | **447.53** | **906.80** | **1,094.12** |

### NPC Component Verification

| Case | Sum of Components | CSV NPC Total | Diff | Status |
|------|-------------------|---------------|------|--------|
| Case 1 | 211.97+15.06+0+114.84+8.16+0+80.84+16.67+0 = 447.54 | 447.53 | 0.00% | PASS |
| Case 2 | 384.21+16.24+0+208.15+8.80+0+275.01+14.39+0 = 906.80 | 906.80 | 0.00% | PASS |
| Case 3 | 422.39+17.86+0+228.84+9.67+0+400.97+14.39+0 = 1,094.12 | 1,094.12 | 0.00% | PASS |

## 1.4 Verification Scope

This report verifies:

1. **Input parameters** - All config values used in calculations (Chapter 2)
2. **Cycle time calculations** - Time components for each case's optimal shuttle (Chapters 3-5)
3. **Cost calculations** - CAPEX, OPEX, and NPC for each case (Chapters 3-5)
4. **Cross-case comparison** - Relative cost structures and LCOA differences (Chapter 6)
5. **Final checklist** - All verification items with PASS/FAIL status (Chapter 7)

## 1.5 Verification Result

All 13 verification items across 3 cases passed with differences below 1%. The MILP optimization model produces results consistent with independent manual calculations from config parameters.
