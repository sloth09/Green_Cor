# Executive Summary

## Overview

This report verifies the MILP optimization results for the Green Corridor ammonia bunkering infrastructure project (2030-2050). The optimization determines the minimum-cost configuration of shuttle vessels and bunkering equipment to meet ammonia fuel demand for vessels operating in the Korea-Japan green shipping corridor.

**Project Period**: 2030-2050 (21 years)
**Demand Growth**: 50 vessels (2030) to 500 vessels (2050), linear growth
**Bunker Volume per Call**: 5,000 m3

**v5 MCR Update**: All results reflect Power Law MCR values (MCR = 17.17 x DWT^0.566).

## Optimal Configurations (v5 Results)

| Case | Route | Optimal Shuttle | NPC (20yr) | LCOAmmonia |
|------|-------|-----------------|------------|------------|
| **Case 1** | Busan Storage | 2,500 m3 | $249.80M | $1.06/ton |
| **Case 2-1** | Yeosu -> Busan (86nm) | 10,000 m3 | $847.56M | $3.60/ton |
| **Case 2-2** | Ulsan -> Busan (59nm) | 5,000 m3 | $667.70M | $2.83/ton |

### v4 to v5 Changes

| Case | v4 Shuttle | v5 Shuttle | v4 NPC | v5 NPC | Change |
|------|------------|------------|--------|--------|--------|
| Case 1 | 1,000 m3 | **2,500 m3** | $238.39M | $249.80M | +4.8% |
| Case 2-1 | 10,000 m3 | 10,000 m3 | $791.47M | $847.56M | +7.1% |
| Case 2-2 | 5,000 m3 | 5,000 m3 | $650.60M | $667.70M | +2.6% |

**Key Change**: Case 1 optimal shifted from 1000 m3 to 2500 m3 due to corrected MCR values for small vessels.

## Key Findings

### 1. Case 1 is Most Cost-Effective
- **$1.06/ton LCOAmmonia** - lowest among all cases
- Local storage at Busan Port minimizes shuttle travel time
- Medium-small shuttles (2,500 m3) are optimal due to MCR correction for small vessels
- v5 MCR update increased small shuttle fuel costs, shifting optimal from 1000 m3 to 2500 m3

### 2. Case 2-2 (Ulsan) Outperforms Case 2-1 (Yeosu)
- **$2.83/ton** vs **$3.60/ton**
- Shorter distance (59nm vs 86nm) reduces fuel and time costs
- Medium-sized shuttles (5,000 m3) balance capacity and cycle efficiency

### 3. MCR Update Impact
- Power Law formula `MCR = 17.17 x DWT^0.566` applied to all shuttle sizes
- Small shuttles (500-2000 m3) experienced largest MCR corrections (+20-37%)
- This shifted Case 1 optimal from 1000 m3 to 2500 m3

## Cost Structure Overview (v5)

| Case | CAPEX Share | Fixed OPEX Share | Variable OPEX Share |
|------|-------------|------------------|---------------------|
| Case 1 | 46.3% | 25.1% | 28.7% |
| Case 2-1 | 41.3% | 22.4% | 36.3% |
| Case 2-2 | 36.7% | 19.9% | 43.3% |

**Observation**: Variable OPEX (fuel costs) is the largest cost component in Case 2 scenarios due to longer travel distances and increased fuel consumption from higher MCR values.

## Recommendation

Based on the verification results:

1. **Primary Recommendation**: Case 1 (Busan Storage)
   - Lowest LCOAmmonia at $1.06/ton
   - Optimal shuttle: 2,500 m3 (updated from v4's 1,000 m3)
   - Requires investment in local storage infrastructure

2. **Alternative**: Case 2-2 (Ulsan Direct Supply)
   - No local storage required
   - Competitive at $2.83/ton if storage infrastructure is not feasible

3. **Not Recommended**: Case 2-1 (Yeosu Direct Supply)
   - Highest cost at $3.60/ton
   - Only viable if Ulsan supply is unavailable
