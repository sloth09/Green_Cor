# Chapter 6: Cross-Case Comparison

## 6.1 Overview

This chapter compares the three optimization cases to identify the most cost-effective ammonia bunkering configuration for the Green Corridor project.

**v5.1 Update**: All results reflect Power Law MCR values (MCR = 17.17 x DWT^0.566) with corrected shore loading fixed time (+2h).

---

## 6.2 Optimal Configurations Summary (v5.1 Results)

| Case | Route | Distance | Optimal Shuttle | NPC (20yr) | LCOAmmonia |
|------|-------|----------|-----------------|------------|------------|
| Case 1 | Busan Storage | - | 2,500 m3 | $290.81M | $1.23/ton |
| Case 2-1 | Yeosu -> Busan | 86 nm | 10,000 m3 | $879.88M | $3.73/ton |
| Case 2-2 | Ulsan -> Busan | 59 nm | 5,000 m3 | $700.68M | $2.97/ton |

**Winner**: Case 1 (Busan Storage) with $290.81M NPC and $1.23/ton LCOAmmonia

### v5 to v5.1 Changes

| Case | v5 Shuttle | v5.1 Shuttle | v5 NPC | v5.1 NPC | Change |
|------|------------|--------------|--------|----------|--------|
| Case 1 | 2,500 m3 | 2,500 m3 | $249.80M | $290.81M | +16.4% |
| Case 2-1 | 10,000 m3 | 10,000 m3 | $847.56M | $879.88M | +3.8% |
| Case 2-2 | 5,000 m3 | 5,000 m3 | $667.70M | $700.68M | +4.9% |

**Key Change**: Shore loading fixed time increased by +2h. Case 1 affected most (+16.4%) because its short base cycle time is more sensitive to the fixed 2h addition. Case 2 less affected (3.8-4.9%) because longer base cycles dilute the fixed 2h addition.

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

1. **Case 1 has clear cost advantage** - roughly 2.4-3.0x cheaper than Case 2 alternatives
2. **Optimal shuttle sizes differ** - driven by distance and operational characteristics:
   - Case 1: Medium-small shuttles (2500 m3) optimal for short port distances
   - Case 2-1: Large shuttles (10000 m3) optimal for long Yeosu route
   - Case 2-2: Medium shuttles (5000 m3) optimal for moderate Ulsan route
3. **Diminishing returns at larger sizes** - beyond optimal point, bigger is not better

---

## 6.4 Cost Structure Comparison

![D6: Cost Breakdown](../../results/paper_figures/D6_cost_breakdown.png)

### Cost Component Breakdown (v5.1 Results)

| Component | Case 1 | Case 2-1 | Case 2-2 | Unit |
|-----------|--------|----------|----------|------|
| **CAPEX** | 142.13 | 371.02 | 266.76 | USDm |
| - Shuttle | 132.67 | 355.18 | 252.96 | USDm |
| - Bunkering | 9.46 | 15.84 | 13.80 | USDm |
| **Fixed OPEX** | 77.00 | 201.01 | 144.53 | USDm |
| - Shuttle | 71.88 | 192.43 | 137.05 | USDm |
| - Bunkering | 5.12 | 8.58 | 7.48 | USDm |
| **Variable OPEX** | 71.68 | 307.84 | 289.40 | USDm |
| - Shuttle Fuel | 55.01 | 294.21 | 275.01 | USDm |
| - Bunkering | 16.67 | 13.63 | 14.39 | USDm |
| **TOTAL** | **290.81** | **879.88** | **700.68** | USDm |

### Cost Shares (v5.1)

| Share | Case 1 | Case 2-1 | Case 2-2 |
|-------|--------|----------|----------|
| CAPEX | 48.9% | 42.2% | 38.1% |
| Fixed OPEX | 26.5% | 22.8% | 20.6% |
| Variable OPEX | 24.6% | 35.0% | 41.3% |

**Key Insight**: Case 2 scenarios have higher variable OPEX shares due to longer travel distances and increased fuel consumption from higher MCR values. The v5.1 shore loading correction increased CAPEX and fixed OPEX shares slightly across all cases due to additional fleet requirements.

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
   - 2500-4999 m3: 2 trips (MCR increases but trips constant -> vOPEX rises)
   - 5000+ m3: 1 trip (step drop in vOPEX)

2. **SFOC Engine-Type Boundaries**
   | DWT Range | SFOC (g/kWh) |
   |-----------|--------------|
   | < 3,000 | 505 (4-stroke high-speed) |
   | 3,000 - 8,000 | 436 (4-stroke medium) |

   - Shuttle 4000 m3 (DWT 3,400) crosses boundary -> 14% SFOC drop
   - Despite +8% MCR, net fuel consumption drops 7%

See Chapter 3, Section 3.12 for detailed analysis.

---

## 6.5 Cycle Time Comparison

![D7: Cycle Time](../../results/paper_figures/D7_cycle_time.png)

### Optimal Configuration Cycle Times (v5.1)

| Case | Shuttle | Cycle Time | Annual Max Cycles |
|------|---------|------------|-------------------|
| Case 1 | 2,500 m3 | 10.17 hr | 787 |
| Case 2-1 | 10,000 m3 | 38.13 hr | 210 |
| Case 2-2 | 5,000 m3 | 23.19 hr | 345 |

**Insight**: Case 1's shorter cycle time allows higher annual throughput per shuttle despite the shift to larger (2500 m3) shuttles. The v5.1 shore loading correction added approximately 2h to each cycle.

---

## 6.6 Fleet Evolution

![D8: Fleet Evolution](../../results/paper_figures/D8_fleet_evolution.png)

### Fleet Size at 2050 (Optimal Configurations, v5.1)

| Case | Shuttle Size | Fleet Size | Total Capacity |
|------|--------------|------------|----------------|
| Case 1 | 2,500 m3 | ~16 shuttles | 40,000 m3 |
| Case 2-1 | 10,000 m3 | ~16 shuttles | 160,000 m3 |
| Case 2-2 | 5,000 m3 | ~18 shuttles | 90,000 m3 |

**Note**: Case 2 requires larger total fleet capacity due to longer cycle times.

---

## 6.7 LCO Comparison

![D9: LCO Comparison](../../results/paper_figures/D9_lco_comparison.png)

### LCOAmmonia by Shuttle Size (v5.1)

| Shuttle (m3) | Case 1 | Case 2-1 | Case 2-2 |
|--------------|--------|----------|----------|
| 500 | $1.51 | - | - |
| 1,000 | $1.30 | - | - |
| 2,500 | **$1.23** | $4.96 | $3.82 |
| 5,000 | $1.31 | $3.76 | **$2.97** |
| 10,000 | $3.12 | **$3.73** | $3.11 |
| 20,000 | - | $4.22 | $3.75 |
| 50,000 | - | $6.22 | $5.89 |

Bold = Optimal for each case

---

## 6.8 Distance Impact Analysis

### Travel Time vs NPC (v5.1)

| Case | Distance (nm) | Travel Time (hr) | Optimal NPC ($M) | LCO ($/ton) |
|------|---------------|------------------|------------------|-------------|
| Case 1 | ~0 (internal) | 1.0 | 290.81 | 1.23 |
| Case 2-2 | 59 | 3.93 | 700.68 | 2.97 |
| Case 2-1 | 86 | 5.73 | 879.88 | 3.73 |

**Regression Analysis:**
- Each additional 27 nm increases NPC by ~$180M
- Each additional 27 nm increases LCO by ~$0.76/ton

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
| **Cost (LCO)** | Best | Worst | Middle | Case 1 is 2.4-3.0x cheaper |
| **Infrastructure** | Requires storage | No storage | No storage | Trade-off |
| **Flexibility** | Low | High | High | Case 2 can adapt routes |
| **Supply Security** | Single source | Diversified | Diversified | Case 2 has options |
| **Scalability** | Limited by storage | Good | Good | Case 2 can add shuttles |

---

## 6.11 Recommendations

### Primary Recommendation: Case 1

**If feasible to build storage at Busan Port:**
- Lowest cost: $1.23/ton LCOAmmonia
- Optimal shuttle: 2,500 m3 (unchanged from v5)
- Simplest operations: Short shuttle trips within port
- Lowest risk: Less exposure to fuel price fluctuations

### Secondary Recommendation: Case 2-2 (Ulsan)

**If no storage at Busan:**
- Second lowest cost: $2.97/ton LCOAmmonia
- Shorter distance than Yeosu (59 nm vs 86 nm)
- Medium shuttle size (5,000 m3) is operationally practical

### Avoid: Case 2-1 (Yeosu)

**Unless Ulsan supply is unavailable:**
- Highest cost: $3.73/ton LCOAmmonia
- Long distance increases fuel costs and cycle times
- Only viable for supply diversification purposes

---

## 6.12 Key Figures

### Figure D10: Case NPC Comparison
![D10: Case NPC Comparison](../../results/paper_figures/D10_case_npc_comparison.png)

### Figure D11: Top Configurations
![D11: Top Configurations](../../results/paper_figures/D11_top_configurations.png)

---

## 6.13 Summary Table (v5.1 Final Results)

| Metric | Case 1 | Case 2-1 | Case 2-2 |
|--------|--------|----------|----------|
| Optimal Shuttle | 2,500 m3 | 10,000 m3 | 5,000 m3 |
| NPC | $290.81M | $879.88M | $700.68M |
| LCOAmmonia | $1.23/ton | $3.73/ton | $2.97/ton |
| Rank | 1st | 3rd | 2nd |
| Relative Cost | 100% | 303% | 241% |

**Bottom Line**: Case 1 provides the lowest cost solution by a significant margin. The v5.1 shore loading correction increased all NPC values, with Case 1 most affected (+16.4%) due to its shorter base cycle time being more sensitive to the fixed 2h addition. However, Case 1 remains the preferred option if port storage is feasible.

---

## 6.14 Cross-Case Verification Summary

All three cases were independently verified with full hand calculations (see Chapters 3-5).

| Verification Item | Case 1 (Ch.3) | Case 2-1 (Ch.4) | Case 2-2 (Ch.5) |
|-------------------|---------------|------------------|------------------|
| Shore Loading Time | PASS (3.6667h) | PASS (8.6667h) | PASS (5.3333h) |
| Basic Cycle Duration | PASS (6.50h) | PASS (29.46h) | PASS (17.86h) |
| Total Cycle Duration | PASS (10.1667h) | PASS (38.1267h) | PASS (23.1933h) |
| Annual Cycles Max | PASS (786.89) | PASS (209.83) | PASS (344.93) |
| Shuttle CAPEX/unit | PASS ($7.69M) | PASS ($21.74M) | PASS ($12.93M) |
| Bunkering CAPEX/unit | PASS ($548K) | PASS ($970K) | PASS ($705K) |
| Shuttle fOPEX/yr/unit | PASS ($384K) | PASS ($1.09M) | PASS ($646K) |
| Shuttle Fuel/cycle | PASS ($397) | PASS ($8,491) | PASS ($3,968) |
| Pump Fuel/call | PASS ($240) | PASS ($197) | PASS ($208) |
| NPC Total | PASS ($290.81M) | PASS ($879.88M) | PASS ($700.68M) |
| LCOAmmonia | PASS ($1.23) | PASS ($3.73) | PASS ($2.97) |

**All verification items PASSED across all three cases.** Maximum difference from CSV: < 0.01% (rounding only).
