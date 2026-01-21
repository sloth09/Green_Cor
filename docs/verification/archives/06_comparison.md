# Chapter 6: Cross-Case Comparison

## 6.1 Overview

This chapter compares the three supply scenarios using visualizations from the D-series figures.

---

## 6.2 Optimal Configuration Summary

| Case | Shuttle Size | NPC (20yr) | LCOAmmonia | Travel Time | Vessels/Trip |
|------|-------------|------------|------------|-------------|--------------|
| **Case 1** | 2,500 m3 | **$237.05M** | **$1.01/ton** | 1.0 hr | N/A (multi-trip) |
| Case 2-1 | 10,000 m3 | $747.18M | $3.17/ton | 5.73 hr | 2 |
| Case 2-2 | 5,000 m3 | $402.37M | $1.71/ton | 1.67 hr | 1 |

---

## 6.3 D-Series Figures

### Figure D1: NPC vs Shuttle Size

![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)

**Key Observations:**
- Case 1 shows clear minimum at 2,500 m3
- Case 2-1 (Yeosu) minimum at 10,000 m3
- Case 2-2 (Ulsan) minimum at 5,000 m3
- All cases show U-shaped cost curves

### Figure D2: Annual Cost Evolution

![D2: Yearly Cost Evolution](../../results/paper_figures/D2_yearly_cost_evolution.png)

**Key Observations:**
- Costs scale linearly with demand growth (50 to 500 vessels)
- Case 1 consistently lowest cost across all years
- Case 2-1 consistently highest cost

### Figure D3: Fleet Size & Annual Supply

![D3: Fleet & Demand](../../results/paper_figures/D3_yearly_fleet_demand.png)

**Key Observations:**
- Fleet size grows proportionally with demand
- Case 1 requires more shuttles (smaller size) but lower total cost
- Case 2 cases require fewer but larger shuttles

### Figure D4: Annual Cycles

![D4: Yearly Cycles](../../results/paper_figures/D4_yearly_cycles.png)

**Key Observations:**
- Case 1 has highest cycle frequency (shorter cycles)
- Case 2-1 has lowest frequency (longest cycles)
- Higher frequency = better asset utilization

### Figure D5: Utilization Rate

![D5: Yearly Utilization](../../results/paper_figures/D5_yearly_utilization.png)

**Key Observations:**
- All optimal configurations achieve 100% utilization
- No wasted capacity in optimal scenarios

---

## 6.4 Additional Figures (Optional)

### Figure D6: Cost Breakdown

![D6: Cost Breakdown](../../results/paper_figures/D6_cost_breakdown.png)

| Cost Component | Case 1 | Case 2-1 | Case 2-2 |
|---------------|--------|----------|----------|
| Shuttle CAPEX | 45.5% | 44.9% | 45.9% |
| Bunkering CAPEX | 3.2% | 2.0% | 2.5% |
| Shuttle Fixed OPEX | 24.6% | 24.3% | 24.9% |
| Bunkering Fixed OPEX | 1.8% | 1.1% | 1.4% |
| Shuttle Variable OPEX | 19.6% | 26.1% | 22.2% |
| Bunkering Variable OPEX | 5.3% | 1.7% | 3.1% |

### Figure D7: Cycle Time Comparison

![D7: Cycle Time](../../results/paper_figures/D7_cycle_time.png)

| Case | Optimal Shuttle | Cycle Time | Components |
|------|----------------|------------|------------|
| Case 1 | 2,500 m3 | 8.17 hr | Shore 1.67 + Travel 2.0 + Setup 2.0 + Pump 2.5 |
| Case 2-1 | 10,000 m3 | 36.13 hr | Shore 6.67 + Travel 11.46 + Port 2.0 + 2x8.0 |
| Case 2-2 | 5,000 m3 | 16.67 hr | Shore 3.33 + Travel 3.34 + Port 2.0 + 8.0 |

### Figure D9: LCO Comparison

![D9: LCO Comparison](../../results/paper_figures/D9_lco_comparison.png)

**Levelized Cost of Ammonia (LCOAmmonia):**
- Case 1: $1.01/ton (baseline)
- Case 2-2: $1.71/ton (+69% premium)
- Case 2-1: $3.17/ton (+214% premium)

### Figure D10: NPC Case Comparison

![D10: NPC Comparison](../../results/paper_figures/D10_case_npc_comparison.png)

---

## 6.5 Case-by-Case Analysis

### 6.5.1 Case 1 vs Case 2-2 (Near Alternative)

| Metric | Case 1 | Case 2-2 | Delta |
|--------|--------|----------|-------|
| NPC | $237.05M | $402.37M | **+$165.32M** |
| LCO | $1.01/ton | $1.71/ton | **+$0.70/ton** |
| Premium | - | +70% | - |
| Travel Time | 2.0 hr RT | 3.34 hr RT | +67% |

**Conclusion**: Case 2-2 (Ulsan) is the best alternative if local storage is infeasible.

### 6.5.2 Case 1 vs Case 2-1 (Far Alternative)

| Metric | Case 1 | Case 2-1 | Delta |
|--------|--------|----------|-------|
| NPC | $237.05M | $747.18M | **+$510.13M** |
| LCO | $1.01/ton | $3.17/ton | **+$2.16/ton** |
| Premium | - | +215% | - |
| Travel Time | 2.0 hr RT | 11.46 hr RT | +473% |

**Conclusion**: Case 2-1 (Yeosu) should be avoided if possible due to high travel time.

### 6.5.3 Case 2-1 vs Case 2-2 (Direct Supply Options)

| Metric | Case 2-1 | Case 2-2 | Delta |
|--------|----------|----------|-------|
| NPC | $747.18M | $402.37M | **-$344.81M** |
| LCO | $3.17/ton | $1.71/ton | **-$1.46/ton** |
| Savings | - | 46% | - |
| Distance | 86 nm | 25 nm | -71% |

**Conclusion**: Ulsan is significantly better than Yeosu for direct supply scenarios.

---

## 6.6 Shuttle Size Selection Guide

| Case | Under-sized | Optimal | Over-sized |
|------|-------------|---------|------------|
| Case 1 | 500-2000 m3 (high OPEX) | **2500 m3** | 3000+ m3 (high CAPEX) |
| Case 2-1 | 2500-5000 m3 (high trips) | **10000 m3** | 15000+ m3 (long cycles) |
| Case 2-2 | 2500 m3 (2 trips needed) | **5000 m3** | 10000+ m3 (diminishing returns) |

---

## 6.7 Economic Impact of Distance

| Source | Distance | Travel Time | NPC vs Case 1 |
|--------|----------|-------------|---------------|
| Busan Storage | 0 nm | 1.0 hr* | Baseline |
| Ulsan | 25 nm | 1.67 hr | +70% |
| Yeosu | 86 nm | 5.73 hr | +215% |

*Case 1 travel time is port internal movement, not open sea transit.

**Rule of Thumb**: Each additional 10 nm adds approximately 25% to NPC for this demand profile.

---

## 6.8 Decision Matrix

| Scenario | Recommended Case | Key Reason |
|----------|-----------------|------------|
| Local storage feasible | **Case 1** | Lowest NPC |
| No local storage, proximity to Ulsan | **Case 2-2** | 46% cheaper than Yeosu |
| No local storage, only Yeosu available | Case 2-1 | Only option |
| Future demand uncertainty | Case 1 or 2-2 | Smaller shuttles = flexibility |
