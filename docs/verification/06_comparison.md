# Chapter 6: Cross-Case Comparison

## 6.1 Overview

This chapter compares the three optimization cases to identify the most cost-effective ammonia bunkering configuration for the Green Corridor project.

**v5 MCR Update**: All results reflect Power Law MCR values (MCR = 17.17 x DWT^0.566).

---

## 6.2 Optimal Configurations Summary (v5 Results)

| Case | Route | Distance | Optimal Shuttle | NPC (20yr) | LCOAmmonia |
|------|-------|----------|-----------------|------------|------------|
| Case 1 | Busan Storage | - | 2,500 m3 | $249.80M | $1.06/ton |
| Case 2-1 | Yeosu -> Busan | 86 nm | 10,000 m3 | $847.56M | $3.60/ton |
| Case 2-2 | Ulsan -> Busan | 59 nm | 5,000 m3 | $667.70M | $2.83/ton |

**Winner**: Case 1 (Busan Storage) with $249.80M NPC and $1.06/ton LCOAmmonia

### v4 to v5 Changes

| Case | v4 Shuttle | v5 Shuttle | v4 NPC | v5 NPC | Change |
|------|------------|------------|--------|--------|--------|
| Case 1 | 1,000 m3 | **2,500 m3** | $238.39M | $249.80M | +4.8% |
| Case 2-1 | 10,000 m3 | 10,000 m3 | $791.47M | $847.56M | +7.1% |
| Case 2-2 | 5,000 m3 | 5,000 m3 | $650.60M | $667.70M | +2.6% |

**Key Change**: Case 1 optimal shifted from 1000 m3 to 2500 m3 due to corrected MCR values for small vessels.

---

## 6.3 NPC Comparison

![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)

### Key Observations

1. **Case 1 has clear cost advantage** - roughly 2.5-3.4x cheaper than Case 2 alternatives
2. **Optimal shuttle sizes differ** - driven by distance and operational characteristics:
   - Case 1: Medium-small shuttles (2500 m3) optimal for short port distances
   - Case 2-1: Large shuttles (10000 m3) optimal for long Yeosu route
   - Case 2-2: Medium shuttles (5000 m3) optimal for moderate Ulsan route
3. **Diminishing returns at larger sizes** - beyond optimal point, bigger is not better

---

## 6.4 Cost Structure Comparison

![D6: Cost Breakdown](../../results/paper_figures/D6_cost_breakdown.png)

### Cost Component Breakdown (v5 Results)

| Component | Case 1 | Case 2-1 | Case 2-2 | Unit |
|-----------|--------|----------|----------|------|
| **CAPEX** | 115.53 | 350.07 | 245.36 | USDm |
| - Shuttle | 107.84 | 335.12 | 232.67 | USDm |
| - Bunkering | 7.69 | 14.95 | 12.69 | USDm |
| **Fixed OPEX** | 62.59 | 189.66 | 132.94 | USDm |
| - Shuttle | 58.42 | 181.56 | 126.06 | USDm |
| - Bunkering | 4.17 | 8.10 | 6.88 | USDm |
| **Variable OPEX** | 71.68 | 307.84 | 289.40 | USDm |
| - Shuttle Fuel | 55.01 | 294.21 | 275.01 | USDm |
| - Bunkering | 16.67 | 13.63 | 14.39 | USDm |
| **TOTAL** | **249.80** | **847.56** | **667.70** | USDm |

### Cost Shares (v5)

| Share | Case 1 | Case 2-1 | Case 2-2 |
|-------|--------|----------|----------|
| CAPEX | 46.3% | 41.3% | 36.7% |
| Fixed OPEX | 25.1% | 22.4% | 19.9% |
| Variable OPEX | 28.7% | 36.3% | 43.3% |

**Key Insight**: Case 2 scenarios have higher variable OPEX shares due to longer travel distances and increased fuel consumption from higher MCR values.

### Variable OPEX Pattern Difference

**Case 2**: Variable OPEX decreases **monotonically** with shuttle size
- Long travel distance (59-86 nm) makes fuel cost dominant
- Vessels_per_Trip increases with shuttle size (economies of scale)
- Fuel cost per m3 delivered decreases continuously

**Case 1**: Variable OPEX shows **non-monotonic** (step + zigzag) pattern due to:

1. **Trips_per_Call (Discrete Steps)**
   ```
   Trips_per_Call = ceil(5000 / Shuttle_Size)
   ```
   - 2500-4999 m3: 2 trips (MCR increases but trips constant → vOPEX rises)
   - 5000+ m3: 1 trip (step drop in vOPEX)

2. **SFOC Engine-Type Boundaries**
   | DWT Range | SFOC (g/kWh) |
   |-----------|--------------|
   | < 3,000 | 505 (4-stroke high-speed) |
   | 3,000 - 8,000 | 436 (4-stroke medium) |

   - Shuttle 4000 m3 (DWT 3,400) crosses boundary → 14% SFOC drop
   - Despite +8% MCR, net fuel consumption drops 7%

See Chapter 3, Section 3.12 for detailed analysis.

---

## 6.5 Cycle Time Comparison

![D7: Cycle Time](../../results/paper_figures/D7_cycle_time.png)

### Optimal Configuration Cycle Times (v5)

| Case | Shuttle | Cycle Time | Annual Max Cycles |
|------|---------|------------|-------------------|
| Case 1 | 2,500 m3 | 8.17 hr | 980 |
| Case 2-1 | 10,000 m3 | 36.13 hr | 221 |
| Case 2-2 | 5,000 m3 | 21.19 hr | 377 |

**Insight**: Case 1's shorter cycle time allows higher annual throughput per shuttle despite the shift to larger (2500 m3) shuttles.

---

## 6.6 Fleet Evolution

![D8: Fleet Evolution](../../results/paper_figures/D8_fleet_evolution.png)

### Fleet Size at 2050 (Optimal Configurations, v5)

| Case | Shuttle Size | Fleet Size | Total Capacity |
|------|--------------|------------|----------------|
| Case 1 | 2,500 m3 | ~16 shuttles | 40,000 m3 |
| Case 2-1 | 10,000 m3 | ~16 shuttles | 160,000 m3 |
| Case 2-2 | 5,000 m3 | ~18 shuttles | 90,000 m3 |

**Note**: Case 2 requires larger total fleet capacity due to longer cycle times.

---

## 6.7 LCO Comparison

![D9: LCO Comparison](../../results/paper_figures/D9_lco_comparison.png)

### LCOAmmonia by Shuttle Size (v5)

| Shuttle (m3) | Case 1 | Case 2-1 | Case 2-2 |
|--------------|--------|----------|----------|
| 500 | $1.23 | - | - |
| 1,000 | $1.08 | - | - |
| 2,500 | **$1.06** | $4.79 | $3.65 |
| 5,000 | $1.16 | $3.62 | **$2.83** |
| 10,000 | $2.88 | **$3.60** | $3.00 |
| 20,000 | - | $4.22 | $3.66 |
| 50,000 | - | $6.13 | $5.75 |

Bold = Optimal for each case

---

## 6.8 Distance Impact Analysis

### Travel Time vs NPC (v5)

| Case | Distance (nm) | Travel Time (hr) | Optimal NPC ($M) | LCO ($/ton) |
|------|---------------|------------------|------------------|-------------|
| Case 1 | ~0 (internal) | 1.0 | 249.80 | 1.06 |
| Case 2-2 | 59 | 3.93 | 667.70 | 2.83 |
| Case 2-1 | 86 | 5.73 | 847.56 | 3.60 |

**Regression Analysis:**
- Each additional 27 nm increases NPC by ~$180M
- Each additional 27 nm increases LCO by ~$0.77/ton

### Break-Even Distance

Based on the data, Case 2 would need a distance of approximately **10-15 nm** to approach Case 1 costs, assuming similar operational characteristics.

---

## 6.9 MCR Update Impact Analysis

### v5 Power Law MCR Effects

| Shuttle | v4 MCR | v5 MCR | Change | Impact on Fuel Cost |
|---------|--------|--------|--------|---------------------|
| 1000 m3 | 620 kW | 770 kW | +24% | +24% per cycle |
| 2500 m3 | 1160 kW | 1310 kW | +13% | +13% per cycle |
| 5000 m3 | 1810 kW | 1930 kW | +7% | +7% per cycle |
| 10000 m3 | 2420 kW | 2990 kW | +24% | +24% per cycle |

**Key Observation**: Small shuttles (500-2000 m3) experienced the largest MCR corrections (+20-37%), which shifted the Case 1 optimal from 1000 m3 to 2500 m3.

---

## 6.10 Decision Matrix

| Factor | Case 1 | Case 2-1 | Case 2-2 | Notes |
|--------|--------|----------|----------|-------|
| **Cost (LCO)** | Best | Worst | Middle | Case 1 is 2.7-3.4x cheaper |
| **Infrastructure** | Requires storage | No storage | No storage | Trade-off |
| **Flexibility** | Low | High | High | Case 2 can adapt routes |
| **Supply Security** | Single source | Diversified | Diversified | Case 2 has options |
| **Scalability** | Limited by storage | Good | Good | Case 2 can add shuttles |

---

## 6.11 Recommendations

### Primary Recommendation: Case 1

**If feasible to build storage at Busan Port:**
- Lowest cost: $1.06/ton LCOAmmonia
- Optimal shuttle: 2,500 m3 (updated from v4's 1,000 m3)
- Simplest operations: Short shuttle trips within port
- Lowest risk: Less exposure to fuel price fluctuations

### Secondary Recommendation: Case 2-2 (Ulsan)

**If no storage at Busan:**
- Second lowest cost: $2.83/ton LCOAmmonia
- Shorter distance than Yeosu (59 nm vs 86 nm)
- Medium shuttle size (5,000 m3) is operationally practical

### Avoid: Case 2-1 (Yeosu)

**Unless Ulsan supply is unavailable:**
- Highest cost: $3.60/ton LCOAmmonia
- Long distance increases fuel costs and cycle times
- Only viable for supply diversification purposes

---

## 6.12 Key Figures

### Figure D10: Case NPC Comparison
![D10: Case NPC Comparison](../../results/paper_figures/D10_case_npc_comparison.png)

### Figure D11: Top Configurations
![D11: Top Configurations](../../results/paper_figures/D11_top_configurations.png)

---

## 6.13 Summary Table (v5 Final Results)

| Metric | Case 1 | Case 2-1 | Case 2-2 |
|--------|--------|----------|----------|
| Optimal Shuttle | 2,500 m3 | 10,000 m3 | 5,000 m3 |
| NPC | $249.80M | $847.56M | $667.70M |
| LCOAmmonia | $1.06/ton | $3.60/ton | $2.83/ton |
| Rank | 1st | 3rd | 2nd |
| Relative Cost | 100% | 339% | 267% |

**Bottom Line**: Case 1 provides the lowest cost solution by a significant margin. The v5 MCR update shifted the optimal shuttle from 1000 m3 to 2500 m3, but Case 1 remains the preferred option if port storage is feasible.
