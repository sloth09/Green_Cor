# Chapter 1: Executive Summary

## Key Findings

The MILP optimization identifies the most cost-effective ammonia bunkering configurations for Busan Port across three supply scenarios. **Case 1 (local storage) is the most economical**, followed by Case 2-2 (Ulsan), with Case 2-1 (Yeosu) being the most expensive due to longer transport distances.

---

## Optimal Configurations (1000 m3/h Pump)

| Case | Configuration | NPC (20yr) | LCOAmmonia | Fleet Size (2050) |
|------|--------------|------------|------------|-------------------|
| **Case 1: Busan Storage** | 2,500 m3 shuttle | **$237.05M** | **$1.01/ton** | ~20 shuttles |
| **Case 2-1: Yeosu** | 10,000 m3 shuttle | $747.18M | $3.17/ton | ~10 shuttles |
| **Case 2-2: Ulsan** | 5,000 m3 shuttle | $402.37M | $1.71/ton | ~15 shuttles |

---

## Cost Comparison

```
Case 1 (Busan)  : ████████████████████ $237M (baseline)
Case 2-2 (Ulsan): ████████████████████████████████████ $402M (+70%)
Case 2-1 (Yeosu): ████████████████████████████████████████████████████████████████ $747M (+215%)
```

---

## Why Case 1 is Optimal

1. **Short Travel Distance**: 1 hour round trip vs 3.34h (Ulsan) or 11.46h (Yeosu)
2. **Higher Utilization**: More cycles per year = better asset utilization
3. **Smaller Shuttles**: 2,500 m3 vs 5,000-10,000 m3 = lower CAPEX per unit

---

## Why 2,500 m3 Shuttle (Case 1)

| Shuttle Size | NPC | LCO | Reason |
|-------------|-----|-----|--------|
| 2,000 m3 | $281.7M | $1.20/ton | Higher OPEX (more trips) |
| **2,500 m3** | **$237.05M** | **$1.01/ton** | **Optimal balance** |
| 3,000 m3 | $282.25M | $1.20/ton | Higher CAPEX |
| 5,000 m3 | $264.24M | $1.12/ton | Overkill for demand |

The 2,500 m3 shuttle requires 2 trips per bunkering call (5000 m3 demand), achieving optimal balance between:
- Fleet size (capital cost)
- Trip frequency (operating cost)
- Asset utilization (efficiency)

---

## Recommendation

**For Busan Port ammonia bunkering infrastructure (2030-2050):**

1. **Primary Recommendation**: Build local storage tanks at Busan Port with 2,500 m3 shuttle fleet
   - 20-year NPC: $237.05M
   - Levelized cost: $1.01/ton

2. **Alternative (if local storage not feasible)**: Ulsan supply with 5,000 m3 shuttle fleet
   - 20-year NPC: $402.37M
   - Levelized cost: $1.71/ton
   - Premium: +70% over Case 1

3. **Not Recommended**: Yeosu supply
   - 20-year NPC: $747.18M
   - Levelized cost: $3.17/ton
   - Premium: +215% over Case 1

---

## Key Assumptions

- **Pump Rate**: 1000 m3/h (fixed for main analysis)
- **Discount Rate**: 0.0 (no time value of money adjustment)
- **Annualization Rate**: 7.0% (for asset cost spreading)
- **Demand Growth**: 50 vessels (2030) to 500 vessels (2050)
- **Bunker Volume**: 5,000 m3 per call
