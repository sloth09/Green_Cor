# 6. Cross-Case Comparison

## 6.1 Optimal Configuration Summary

| Parameter | Case 1 (Busan) | Case 2 (Ulsan) | Case 3 (Yeosu) |
|-----------|----------------|----------------|----------------|
| Route | Port internal | 59 nm | 86 nm |
| Travel time (one-way) | 1.0 h | 3.93 h | 5.73 h |
| Has storage at Busan | Yes | No | No |
| Optimal shuttle | 1,000 m3 | 5,000 m3 | 5,000 m3 |
| Vessels per trip | N/A (multi-trip) | 1 | 1 |
| Trips per call | 5 | 1 | 1 |
| Cycle duration | 13.43 h | 36.00 h | 39.60 h |
| Annual cycles max | 595.74 | 222.20 | 202.01 |

## 6.2 NPC Comparison

| Component | Case 1 (USD M) | Case 2 (USD M) | Case 3 (USD M) |
|-----------|----------------|----------------|----------------|
| Shuttle CAPEX (ann.) | 211.97 | 384.21 | 422.39 |
| Bunkering CAPEX (ann.) | 15.06 | 16.24 | 17.86 |
| Terminal CAPEX (ann.) | 0.00 | 0.00 | 0.00 |
| Shuttle Fixed OPEX | 114.84 | 208.15 | 228.84 |
| Bunkering Fixed OPEX | 8.16 | 8.80 | 9.67 |
| Terminal Fixed OPEX | 0.00 | 0.00 | 0.00 |
| Shuttle Variable OPEX | 80.84 | 275.01 | 400.97 |
| Bunkering Variable OPEX | 16.67 | 14.39 | 14.39 |
| Terminal Variable OPEX | 0.00 | 0.00 | 0.00 |
| **NPC Total** | **447.53** | **906.80** | **1,094.12** |
| **LCOA (USD/ton)** | **1.90** | **3.85** | **4.64** |

## 6.3 NPC Structure Analysis

### By Cost Category

| Category | Case 1 | % | Case 2 | % | Case 3 | % |
|----------|--------|---|--------|---|--------|---|
| CAPEX (annualized) | 227.03 | 50.7% | 400.45 | 44.2% | 440.25 | 40.2% |
| Fixed OPEX | 123.00 | 27.5% | 216.95 | 23.9% | 238.51 | 21.8% |
| Variable OPEX | 97.51 | 21.8% | 289.40 | 31.9% | 415.36 | 38.0% |
| **Total** | **447.54** | 100% | **906.80** | 100% | **1,094.12** | 100% |

**Key observation**: As travel distance increases, variable OPEX (fuel) share grows from 21.8% (Case 1) to 38.0% (Case 3), while CAPEX share decreases from 50.7% to 40.2%.

### By Asset

| Asset | Case 1 | % | Case 2 | % | Case 3 | % |
|-------|--------|---|--------|---|--------|---|
| Shuttle (CAPEX+fOPEX+vOPEX) | 407.65 | 91.1% | 867.37 | 95.7% | 1,052.20 | 96.2% |
| Bunkering (CAPEX+fOPEX+vOPEX) | 39.89 | 8.9% | 39.43 | 4.3% | 41.92 | 3.8% |
| Terminal | 0.00 | 0.0% | 0.00 | 0.0% | 0.00 | 0.0% |
| **Total** | **447.54** | 100% | **906.80** | 100% | **1,094.12** | 100% |

**Key observation**: Shuttle costs dominate in all cases (91-96%), with bunkering system costs being relatively constant (~$40M) across cases.

## 6.4 Cost Driver Analysis

### Travel Distance Impact

| Metric | Case 1 | Case 2 | Case 3 |
|--------|--------|--------|--------|
| Round-trip travel (h) | 2.0 | 7.86 | 11.46 |
| Travel as % of cycle | 14.9% | 21.8% | 28.9% |
| Shuttle vOPEX (USD M) | 80.84 | 275.01 | 400.97 |
| vOPEX ratio vs Case 1 | 1.00x | 3.40x | 4.96x |

Shuttle variable OPEX scales with travel distance because:
- Fuel consumption per cycle = MCR x SFOC x Travel_Time x Travel_Factor
- Case 1: 770 kW x 505 g/kWh x 1.0 h x 1.0 = $233/cycle
- Case 2: 1930 kW x 436 g/kWh x 3.93 h x 2.0 = $3,968/cycle
- Case 3: 1930 kW x 436 g/kWh x 5.73 h x 2.0 = $5,786/cycle

Case 3/Case 2 fuel ratio = 5,786 / 3,968 = 1.458, matching travel ratio 5.73/3.93 = 1.458.

### Fleet Size Impact

| Year | Case 1 Shuttles | Case 2 Shuttles | Case 3 Shuttles |
|------|-----------------|-----------------|-----------------|
| 2030 | 6 | 3 | 3 |
| 2040 | 28 | 15 | 17 |
| 2050 | 51 | 28 | 30 |

Case 1 requires more shuttles due to smaller shuttle size (1,000 m3 vs 5,000 m3) but each shuttle has much lower CAPEX ($3.87M vs $12.93M).

### Why Case 1 is Optimal Despite More Shuttles

| Factor | Case 1 | Case 2/3 |
|--------|--------|----------|
| Shuttle CAPEX each | $3.87M | $12.93M |
| Shuttles at 2050 | 51 | 28-30 |
| Total fleet CAPEX at 2050 | ~$197M | ~$362-388M |
| Fuel per cycle | $233 | $3,968-5,786 |
| Cycles per year (2050) | 30,000 | 6,000 |
| Annual fuel cost (2050) | ~$7.0M | ~$23.8-34.7M |

Case 1's advantage comes from:
1. Lower per-shuttle CAPEX (0.75 scaling exponent favors smaller vessels)
2. Negligible travel fuel (1.0 h one-way within port vs 3.93-5.73 h)
3. No port_entry/exit/movement overhead (Case 2/3 add 3.0h per cycle)

## 6.5 LCOA Comparison

| Case | NPC (USD M) | Total Supply (tons) | LCOA (USD/ton) | LCOA Ratio vs Case 1 |
|------|-------------|--------------------|-----------------|-----------------------|
| Case 1 | 447.53 | 235,620,000 | 1.90 | 1.00x |
| Case 2 | 906.80 | 235,620,000 | 3.85 | 2.03x |
| Case 3 | 1,094.12 | 235,620,000 | 4.64 | 2.44x |

**Interpretation**: Total supply is identical across all cases because the same fleet (50-500 vessels) requires the same total fuel. Only the cost of delivery differs.

### LCOA Increment Analysis

| Comparison | NPC Diff (USD M) | LCOA Diff (USD/ton) | Primary Driver |
|------------|-------------------|----------------------|---------------|
| Case 2 vs Case 1 | +459.27 | +1.95 | Travel distance (59 nm), larger shuttles |
| Case 3 vs Case 1 | +646.59 | +2.74 | Travel distance (86 nm), larger shuttles |
| Case 3 vs Case 2 | +187.32 | +0.79 | Additional 27 nm travel (+45.8%) |

## 6.6 Cycle Time Composition Comparison

```
Case 1 (1,000 m3, 13.43 h):
|===Shore(5.43)===|=Trav(1.0)=|=Setup(2.0)=|=Pump(2.0)=|=Setup(2.0)=|=Trav(1.0)=|

Case 2 (5,000 m3, 36.00 h):
|=====Shore(11.14)=====|==Trav(3.93)==|PE|=Mvmt=|=Setup=|====Pump(10.0)====|=Setup=|PX|==Trav(3.93)==|

Case 3 (5,000 m3, 39.60 h):
|=====Shore(11.14)=====|===Trav(5.73)===|PE|=Mvmt=|=Setup=|====Pump(10.0)====|=Setup=|PX|===Trav(5.73)===|

PE = Port Entry (1.0h), PX = Port Exit (1.0h), Mvmt = Movement (1.0h)
```

**Time breakdown:**

| Component | Case 1 | Case 2 | Case 3 |
|-----------|--------|--------|--------|
| Shore loading | 5.43 (40.4%) | 11.14 (30.9%) | 11.14 (28.1%) |
| Travel (round trip) | 2.00 (14.9%) | 7.86 (21.8%) | 11.46 (28.9%) |
| Port entry/exit | 0.00 (0.0%) | 2.00 (5.6%) | 2.00 (5.1%) |
| Movement | 0.00 (0.0%) | 1.00 (2.8%) | 1.00 (2.5%) |
| Setup (total) | 4.00 (29.8%) | 4.00 (11.1%) | 4.00 (10.1%) |
| Pumping | 2.00 (14.9%) | 10.00 (27.8%) | 10.00 (25.3%) |
| **Total** | **13.43** | **36.00** | **39.60** |

## 6.7 Verification Summary

All cross-case calculations are internally consistent:

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Case 1 NPC < Case 2 NPC | Yes | 447.53 < 906.80 | [PASS] |
| Case 2 NPC < Case 3 NPC | Yes | 906.80 < 1094.12 | [PASS] |
| Case 3/Case 2 fuel ratio = distance ratio | 1.458 | 5786/3968 = 1.458 | [PASS] |
| Total supply identical across cases | 235,620,000 | All match | [PASS] |
| LCOA ordering: Case 1 < Case 2 < Case 3 | Yes | 1.90 < 3.85 < 4.64 | [PASS] |
| Bunkering costs approximately equal | ~$40M | 39.89, 39.43, 41.92 | [PASS] |
