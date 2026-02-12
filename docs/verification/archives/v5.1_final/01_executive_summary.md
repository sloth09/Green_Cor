# Executive Summary

## Overview

This report verifies the MILP optimization results for the Green Corridor ammonia bunkering infrastructure project (2030-2050). The optimization determines the minimum-cost configuration of shuttle vessels and bunkering equipment to meet ammonia fuel demand for vessels operating in the Korea-Japan green shipping corridor.

**Report Version**: v5.1 (Shore Loading Fixed Time + v5 MCR Power Law)
**Project Period**: 2030-2050 (21 years)
**Demand Growth**: 50 vessels (2030) to 500 vessels (2050), linear growth
**Bunker Volume per Call**: 5,000 m3
**Discount Rate**: 0% (no time value discounting)
**Annualization Interest Rate**: 7% (for asset annualization)

### v5.1 Key Updates
1. **Shore Loading Fixed Time**: 2.0 hours added to all cycle time calculations (setup/shutdown for shore loading operations)
2. **MCR v5 Power Law**: MCR = 17.17 x DWT^0.566 (MAN Energy Solutions regression, R2 = 0.998)
3. **Data Source**: `results/deterministic/MILP_scenario_summary_case_*.csv`

## Optimal Configurations

| Case | Route | Optimal Shuttle | NPC (20yr) | LCOAmmonia | Annual Cycles (Max) |
|------|-------|-----------------|------------|------------|---------------------|
| **Case 1** | Busan Storage | 2,500 m3 | $290.81M | $1.23/ton | 786.89 |
| **Case 2-1** | Yeosu -> Busan (86nm) | 10,000 m3 | $879.88M | $3.73/ton | 209.83 |
| **Case 2-2** | Ulsan -> Busan (59nm) | 5,000 m3 | $700.68M | $2.97/ton | 344.93 |

## Verification Summary

All 13 verification items were manually calculated and compared against CSV optimizer output for each case. The verification follows this process:
1. Extract parameters from YAML config files
2. Apply formulas with actual values (hand calculation)
3. Compare calculated values with CSV output
4. Record PASS (diff < 1%), REVIEW (1-5%), or FAIL (> 5%)

### Verification Results Overview

| Category | Items | Case 1 | Case 2-1 | Case 2-2 |
|----------|-------|--------|----------|----------|
| Economic (AF) | 1 | PASS | PASS | PASS |
| CAPEX (Shuttle, Pump, Bunkering) | 3 | PASS | PASS | PASS |
| Fixed OPEX | 2 | PASS | PASS | PASS |
| Variable OPEX (Fuel) | 2 | PASS | PASS | PASS |
| Time (Cycle, Annual) | 2 | PASS | PASS | PASS |
| Final (NPC, LCO) | 2 | PASS | PASS | PASS |
| **Total** | **13** | **13/13 PASS** | **13/13 PASS** | **13/13 PASS** |

## Key Findings

### 1. Case 1 is Most Cost-Effective
- **$1.23/ton LCOAmmonia** - lowest among all cases
- Local storage at Busan Port minimizes shuttle travel time
- Medium-small shuttles (2,500 m3) optimal
- Shore loading 2h addition increased NPC by 16.4% (largest impact due to short cycle sensitivity)

### 2. Case 2-2 (Ulsan) Outperforms Case 2-1 (Yeosu)
- **$2.97/ton** vs **$3.73/ton**
- Shorter distance (59nm vs 86nm) reduces fuel and time costs
- Medium-sized shuttles (5,000 m3) balance capacity and cycle efficiency

### 3. Shore Loading Time Impact (v5.1)
- Shore loading fixed time of 2.0 hours per cycle
- Case 1 most affected (+16.4%) due to short base cycles
- Case 2 scenarios less affected (+3.8% to +4.9%) as longer travel distances dilute the fixed time impact
- Optimal shuttle sizes unchanged across all cases

### 4. MCR v5 Power Law
- MCR = 17.17 x DWT^0.566 (regression from MAN Energy Solutions data)
- DWT = Cargo_m3 x 0.680 / 0.80 = Shuttle_Size x 0.85
- Higher MCR values than v4 (especially for small vessels: +37% at 500 m3)
- Results in higher fuel costs for small shuttles, reinforcing optimal size selection

## Cost Structure Overview

| Case | CAPEX Share | Fixed OPEX Share | Variable OPEX Share |
|------|-------------|------------------|---------------------|
| Case 1 (2500 m3) | 48.9% | 26.5% | 24.6% |
| Case 2-1 (10000 m3) | 42.2% | 22.8% | 35.0% |
| Case 2-2 (5000 m3) | 38.1% | 20.6% | 41.3% |

## Recommendation

1. **Primary**: Case 1 (Busan Storage) - Lowest LCOAmmonia at $1.23/ton, optimal shuttle 2,500 m3
2. **Alternative**: Case 2-2 (Ulsan) - $2.97/ton, no local storage required
3. **Not Recommended**: Case 2-1 (Yeosu) - Highest cost at $3.73/ton
