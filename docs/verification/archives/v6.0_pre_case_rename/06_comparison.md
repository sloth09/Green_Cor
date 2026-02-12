# 6. Cross-Case Comparison

## 6.1 Optimal Configuration Comparison

| Parameter | Case 1: Busan | Case 2-1: Yeosu | Case 2-2: Ulsan |
|-----------|--------------|-----------------|-----------------|
| **Optimal Shuttle** | **2,500 m3** | **5,000 m3** | **5,000 m3** |
| Pump Rate | 1,000 m3/h | 1,000 m3/h | 1,000 m3/h |
| Travel (one-way) | 1.0 h | 5.73 h | 3.93 h |
| Has Storage | Yes | No | No |
| VpT (optimal) | 1 | 1 | 1 |
| Trips per Call | 2 | 1 | 1 |

## 6.2 Cycle Time Comparison

### 6.2.1 Time Components (Optimal Shuttle)

| Component | Case 1 (2500) | Case 2-1 (5000) | Case 2-2 (5000) |
|-----------|--------------|-----------------|-----------------|
| Shore Loading | 7.57 h | 11.14 h | 11.14 h |
| Travel Outbound | 1.00 h | 5.73 h | 3.93 h |
| Port Entry | 0.00 h | 1.00 h | 1.00 h |
| Movement (per vessel) | 0.00 h | 1.00 h | 1.00 h |
| Setup Inbound | 2.00 h | 2.00 h | 2.00 h |
| Pumping | 2.50 h | 5.00 h | 5.00 h |
| Setup Outbound | 2.00 h | 2.00 h | 2.00 h |
| Port Exit | 0.00 h | 1.00 h | 1.00 h |
| Travel Return | 1.00 h | 5.73 h | 3.93 h |
| **Total Cycle** | **16.07 h** | **34.60 h** | **31.00 h** |

### 6.2.2 Time Distribution Analysis

| Component | Case 1 | Case 2-1 | Case 2-2 |
|-----------|--------|----------|----------|
| Shore Loading | 47.1% | 32.2% | 35.9% |
| Travel (round trip) | 12.4% | 33.1% | 25.4% |
| Port Operations | 0.0% | 5.8% | 6.5% |
| Setup (total) | 24.9% | 11.6% | 12.9% |
| Pumping | 15.6% | 14.5% | 16.1% |
| Movement | 0.0% | 2.9% | 3.2% |
| **Total** | **100%** | **100%** | **100%** |

**Key Insight**: Shore loading is the largest single time component in all cases (35-47%),
reflecting the impact of the reduced shore pump rate (700 m3/h). For Case 1, shore loading
alone accounts for nearly half the cycle time.

### 6.2.3 Annual Capacity

| Metric | Case 1 | Case 2-1 | Case 2-2 |
|--------|--------|----------|----------|
| Cycle Duration (h) | 16.07 | 34.60 | 31.00 |
| Annual Cycles/Shuttle | 497.78 | 231.19 | 258.04 |
| Supply/Cycle (m3) | 2,500 | 5,000 | 5,000 |
| Annual Supply/Shuttle (m3) | 1,244,444 | 1,155,974 | 1,290,204 |

**Notable**: Despite Case 2-2 having fewer annual cycles than Case 1, each cycle delivers
twice the volume (5,000 vs 2,500 m3), giving Case 2-2 slightly higher annual supply per shuttle.

## 6.3 Cost Comparison

### 6.3.1 Unit CAPEX

| Item | Case 1 (2500) | Case 2 (5000) |
|------|--------------|---------------|
| Shuttle CAPEX | $7,687,500 | $12,928,776 |
| Pump CAPEX | $317,460 | $317,460 |
| Bunkering CAPEX | $548,085 | $705,323 |
| Shuttle fOPEX/yr | $384,375 | $646,439 |
| Bunkering fOPEX/yr | $27,404 | $35,266 |

### 6.3.2 NPC Component Comparison

| Component | Case 1 ($M) | % | Case 2-1 ($M) | % | Case 2-2 ($M) | % |
|-----------|------------|---|--------------|---|--------------|---|
| Shuttle CAPEX | 205.04 | 49.97% | 368.69 | 36.33% | 332.90 | 40.08% |
| Bunkering CAPEX | 14.62 | 3.56% | 20.11 | 1.98% | 18.16 | 2.19% |
| Terminal CAPEX | 0.00 | 0.00% | 0.00 | 0.00% | 0.00 | 0.00% |
| **Subtotal CAPEX** | **219.66** | **53.53%** | **388.80** | **38.31%** | **351.06** | **42.26%** |
| Shuttle fOPEX | 111.08 | 27.07% | 199.75 | 19.68% | 180.36 | 21.71% |
| Bunkering fOPEX | 7.92 | 1.93% | 10.90 | 1.07% | 9.84 | 1.18% |
| Terminal fOPEX | 0.00 | 0.00% | 0.00 | 0.00% | 0.00 | 0.00% |
| **Subtotal fOPEX** | **119.00** | **29.00%** | **210.65** | **20.76%** | **190.20** | **22.90%** |
| Shuttle vOPEX | 55.01 | 13.40% | 400.97 | 39.51% | 275.01 | 33.11% |
| Bunkering vOPEX | 16.67 | 4.06% | 14.39 | 1.42% | 14.39 | 1.73% |
| Terminal vOPEX | 0.00 | 0.00% | 0.00 | 0.00% | 0.00 | 0.00% |
| **Subtotal vOPEX** | **71.68** | **17.47%** | **415.36** | **40.93%** | **289.40** | **34.84%** |
| **NPC TOTAL** | **410.34** | **100%** | **1,014.81** | **100%** | **830.65** | **100%** |

### 6.3.3 Cost Structure Insight

**Case 1**: Dominated by CAPEX (53.5%) because short travel distance means low fuel costs.
The fleet grows to 25 shuttles, driving high cumulative CAPEX.

**Case 2-1 (Yeosu)**: Dominated by Variable OPEX (40.9%) because the long round trip
(11.46h) consumes significant fuel per cycle. Shuttle vOPEX ($401M) exceeds Shuttle CAPEX ($369M).

**Case 2-2 (Ulsan)**: Balanced between CAPEX (42.3%) and vOPEX (34.8%). Shorter travel
than Yeosu reduces fuel cost, but still significant.

## 6.4 LCOAmmonia Comparison

| Case | NPC ($M) | Total Supply (ton) | LCO ($/ton) |
|------|---------|-------------------|-------------|
| Case 1 | 410.34 | 235,620,000 | **1.74** |
| Case 2-2 (Ulsan) | 830.65 | 235,620,000 | **3.53** |
| Case 2-1 (Yeosu) | 1,014.81 | 235,620,000 | **4.31** |

**Case 1 is 51% cheaper than Case 2-2** ($1.74 vs $3.53/ton) and **60% cheaper than Case 2-1**
($1.74 vs $4.31/ton) in terms of levelized cost per ton of ammonia delivered.

## 6.5 Fleet Size Comparison

| Metric | Case 1 | Case 2-1 | Case 2-2 |
|--------|--------|----------|----------|
| Shuttles in 2030 | 3 | 3 | 3 |
| Shuttles in 2050 | 25 | 26 | 24 |
| Shuttle-years (21yr) | 289 | 309 | 279 |
| Total new shuttles | 25 | 26 | 24 |
| Avg fleet size | 13.76 | 14.71 | 13.29 |

**Observation**: All cases require similar fleet sizes (~24-26 shuttles by 2050), despite
very different shuttle sizes. This is because larger shuttles have proportionally fewer
annual cycles, requiring similar numbers to meet growing demand.

## 6.6 Sensitivity to Parameter Changes (v5.1 vs v6.0)

| Case | v5.1 NPC | v6.0 NPC | Abs. Change | Rel. Change |
|------|---------|---------|-------------|-------------|
| Case 1 | $290.81M | $410.34M | +$119.53M | +41.1% |
| Case 2-1 | $879.88M | $1,014.81M | +$134.93M | +15.3% |
| Case 2-2 | $700.68M | $830.65M | +$129.97M | +18.6% |

**Absolute increase** is similar across cases (~$120-135M), but the **relative increase**
varies significantly (15-41%) because Case 1 has a lower baseline NPC.

The parameter changes add approximately the same fixed time per cycle to all cases (~5.9h
for Case 1, ~8.5h for Case 2), but Case 1's shorter base cycle amplifies the relative
impact.

## 6.7 Verification Consistency Check

| Check | Result |
|-------|--------|
| Same Annuity Factor across all cases | 10.8355 (PASS) |
| Same Pump Power across all cases | 158.73 kW (PASS) |
| Same Total Supply across all cases | 235,620,000 tons (PASS) |
| Same total calls across all cases | 69,300 (PASS) |
| Shore Loading consistent (same formula) | Size/700 + 4.0 (PASS) |
| Setup times consistent | 2.0h inbound + 2.0h outbound (PASS) |

All cross-case consistency checks PASS. The three cases differ only in travel time,
shuttle size options, and storage configuration.

---

## 6.8 Figure Reference

![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)

*Figure D1: NPC comparison across all three cases showing optimal shuttle sizes and the
cost advantage of Case 1.*

![D6: Cost Breakdown](../../results/paper_figures/D6_cost_breakdown.png)

*Figure D6: NPC cost breakdown by category showing the shift from CAPEX-dominated (Case 1)
to vOPEX-dominated (Case 2-1) cost structures.*
