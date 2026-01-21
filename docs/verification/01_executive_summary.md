# Executive Summary

## Overview

This report verifies the MILP optimization results for the Green Corridor ammonia bunkering infrastructure project (2030-2050). The optimization determines the minimum-cost configuration of shuttle vessels and bunkering equipment to meet ammonia fuel demand for vessels operating in the Korea-Japan green shipping corridor.

**Project Period**: 2030-2050 (21 years)
**Demand Growth**: 50 vessels (2030) to 500 vessels (2050), linear growth
**Bunker Volume per Call**: 5,000 m3

## Optimal Configurations

| Case | Route | Optimal Shuttle | NPC (20yr) | LCOAmmonia |
|------|-------|-----------------|------------|------------|
| **Case 1** | Busan Storage | 1,000 m3 | $238.39M | $1.01/ton |
| **Case 2-1** | Yeosu -> Busan (86nm) | 10,000 m3 | $791.47M | $3.36/ton |
| **Case 2-2** | Ulsan -> Busan (59nm) | 5,000 m3 | $650.60M | $2.76/ton |

## Key Findings

### 1. Case 1 is Most Cost-Effective
- **$1.01/ton LCOAmmonia** - lowest among all cases
- Local storage at Busan Port minimizes shuttle travel time
- Smaller shuttles (1,000 m3) are optimal due to short port-internal distances

### 2. Case 2-2 (Ulsan) Outperforms Case 2-1 (Yeosu)
- **$2.76/ton** vs **$3.36/ton**
- Shorter distance (59nm vs 86nm) reduces fuel and time costs
- Medium-sized shuttles (5,000 m3) balance capacity and cycle efficiency

### 3. Distance Impact on Case 2-2
- v4.1 update: Ulsan distance corrected from 25nm to 59nm
- This increased travel time from 1.67 hr to 3.93 hr per leg
- NPC increased compared to previous estimates with shorter distance

## Cost Structure Overview

| Case | CAPEX Share | Fixed OPEX Share | Variable OPEX Share |
|------|-------------|------------------|---------------------|
| Case 1 | 42.5% | 23.0% | 34.5% |
| Case 2-1 | 44.2% | 24.0% | 31.8% |
| Case 2-2 | 37.7% | 20.4% | 41.9% |

**Observation**: Variable OPEX (fuel costs) is the largest cost component in Case 2-2 due to longer travel distances.

## Recommendation

Based on the verification results:

1. **Primary Recommendation**: Case 1 (Busan Storage)
   - Lowest LCOAmmonia at $1.01/ton
   - Requires investment in local storage infrastructure

2. **Alternative**: Case 2-2 (Ulsan Direct Supply)
   - No local storage required
   - Competitive at $2.76/ton if storage infrastructure is not feasible

3. **Not Recommended**: Case 2-1 (Yeosu Direct Supply)
   - Highest cost at $3.36/ton
   - Only viable if Ulsan supply is unavailable
