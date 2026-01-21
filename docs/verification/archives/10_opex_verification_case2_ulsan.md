# Chapter 10: OPEX Verification - Case 2-2 (Ulsan to Busan)

## 10.1 Overview

This document verifies all Operating Expenditure (OPEX) calculations for Case 2-2 (Ulsan).

| Component | Type | Formula Source |
|-----------|------|----------------|
| Shuttle Fixed OPEX | Annual | cost_calculator.py |
| Shuttle Variable OPEX | Per Cycle | cost_calculator.py |
| Bunkering Fixed OPEX | Annual | cost_calculator.py |
| Bunkering Variable OPEX | Per Call | cost_calculator.py |

**Note**: Case 2-2 has **NO** tank storage at Busan (direct supply from Ulsan).

---

## 10.2 Input Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Fuel Price | 600.0 | USD/ton | base.yaml |
| SFOC | 379.0 | g/kWh | base.yaml |
| Pump Delta Pressure | 4.0 | bar | base.yaml |
| Pump Efficiency | 0.7 | - | base.yaml |
| Shuttle Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Bunkering Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Shuttle Equipment Ratio | 0.03 | % of CAPEX | base.yaml |
| Distance | 25 | nautical miles | case_2_ulsan.yaml |
| Speed | 15 | knots | case_2_ulsan.yaml |
| Travel Time (one-way) | 1.67 | hours | Calculated (25/15) |
| Shore Pump Rate | 1500 | m3/h | base.yaml |
| Bunker Volume per Call | 5,000 | m3 | case_2_ulsan.yaml |

---

## 10.3 Comparison with Case 2-1 (Yeosu)

| Parameter | Case 2-1 (Yeosu) | Case 2-2 (Ulsan) | Difference |
|-----------|-----------------|------------------|------------|
| Distance | 86 nm | 25 nm | -71% |
| Travel Time (one-way) | 5.73 hr | 1.67 hr | -71% |
| Optimal Shuttle | 10,000 m3 | 5,000 m3 | -50% |
| Round Trip Time | 11.46 hr | 3.34 hr | -71% |

**Key Insight**: Ulsan's shorter distance enables smaller, more efficient shuttles.

---

## 10.4 Shuttle Fixed OPEX

### 10.4.1 Formula

```
Shuttle_Fixed_OPEX_Annual = Shuttle_CAPEX × Fixed_OPEX_Ratio
                         = Shuttle_CAPEX × 0.05
```

### 10.4.2 Verification (5,000 m3 Optimal Shuttle)

**Step 1: Shuttle CAPEX**
```
Shuttle_CAPEX = 61,500,000 × (5000 / 40000)^0.75
             = 61,500,000 × (0.125)^0.75
             = 61,500,000 × 0.2102
             = $12,927,300
```

**Step 2: Annual Fixed OPEX per Shuttle**
```
Fixed_OPEX = $12,927,300 × 0.05
           = $646,365/year per shuttle
```

### 10.4.3 Verification Table (Case 2 Shuttle Sizes)

| Shuttle (m3) | CAPEX (USD) | Fixed OPEX/yr (USD) |
|-------------|-------------|---------------------|
| 2,500 | $7,687,500 | $384,375 |
| **5,000** | **$12,927,300** | **$646,365** |
| 10,000 | $21,746,400 | $1,087,320 |
| 15,000 | $29,631,600 | $1,481,580 |
| 20,000 | $36,567,000 | $1,828,350 |
| 25,000 | $43,032,450 | $2,151,623 |
| 30,000 | $49,163,100 | $2,458,155 |
| 35,000 | $55,032,300 | $2,751,615 |
| 40,000 | $61,500,000 | $3,075,000 |
| 45,000 | $67,000,650 | $3,350,033 |
| 50,000 | $72,504,450 | $3,625,223 |

---

## 10.5 Shuttle Variable OPEX (Fuel Cost)

### 10.5.1 Formula

For Case 2, the shuttle makes a **round trip**:

```
Fuel_per_Cycle_ton = MCR_kW × SFOC_g_kWh × Travel_Time_hr × Travel_Factor / 1e6

where:
  Travel_Time = 1.67 hours (one-way)
  Travel_Factor = 2.0 (round trip: outbound + return)

Fuel_Cost_per_Cycle = Fuel_per_Cycle_ton × Fuel_Price_USD_per_ton
```

### 10.5.2 Verification (5,000 m3 Shuttle)

**Step 1: Get MCR**
```
MCR(5000 m3) = 1694 kW  (from mcr_map_kw)
```

**Step 2: Calculate Fuel per Cycle (Round Trip)**
```
Fuel_ton = (1694 × 379 × 1.67 × 2.0) / 1e6
         = (1694 × 379 × 3.34) / 1e6
         = 2,144,287 / 1e6
         = 2.144 ton/cycle
```

**Step 3: Calculate Fuel Cost per Cycle**
```
Fuel_Cost = 2.144 × $600
          = $1,286.57/cycle
```

### 10.5.3 Comparison: Case 2-1 vs Case 2-2

| Metric | Case 2-1 (10,000 m3) | Case 2-2 (5,000 m3) | Ratio |
|--------|---------------------|---------------------|-------|
| MCR | 2,159 kW | 1,694 kW | 0.78x |
| Travel (one-way) | 5.73 hr | 1.67 hr | 0.29x |
| Travel Factor | 2.0 | 2.0 | 1.0x |
| **Fuel/Cycle** | **9.379 ton** | **2.144 ton** | **0.23x** |
| **Cost/Cycle** | **$5,628** | **$1,287** | **0.23x** |

**Why Case 2-2 has lower fuel cost:**
- 71% shorter distance -> 71% less travel time
- Smaller optimal shuttle -> lower MCR
- Combined effect: 77% lower fuel cost per cycle

### 10.5.4 MCR and Fuel Cost Table (Case 2-2 Sizes)

| Shuttle (m3) | MCR (kW) | Fuel/Cycle (ton) | Fuel Cost/Cycle (USD) |
|-------------|----------|------------------|----------------------|
| 2,500 | 1,473 | 1.866 | $1,119.60 |
| **5,000** | **1,694** | **2.144** | **$1,286.57** |
| 10,000 | 2,159 | 2.733 | $1,639.80 |
| 15,000 | 2,485 | 3.146 | $1,887.60 |
| 20,000 | 2,751 | 3.483 | $2,089.80 |
| 25,000 | 2,981 | 3.774 | $2,264.40 |
| 30,000 | 3,185 | 4.032 | $2,419.20 |
| 35,000 | 3,372 | 4.269 | $2,561.40 |
| 40,000 | 3,546 | 4.489 | $2,693.40 |
| 45,000 | 3,710 | 4.697 | $2,818.20 |
| 50,000 | 3,867 | 4.896 | $2,937.60 |

---

## 10.6 Bunkering Fixed OPEX

### 10.6.1 Formula

```
Bunkering_CAPEX = Shuttle_Equipment_Cost + Pump_CAPEX
                = (Shuttle_CAPEX × 0.03) + (Pump_Power_kW × $2000/kW)

Bunkering_Fixed_OPEX = Bunkering_CAPEX × 0.05
```

### 10.6.2 Verification (5,000 m3 Shuttle, 1000 m3/h Pump)

**Step 1: Equipment Cost**
```
Shuttle_Equipment = $12,927,300 × 0.03
                  = $387,819
```

**Step 2: Pump CAPEX**
```
Pump_Power = 158.73 kW  (same as other cases)
Pump_CAPEX = 158.73 × $2,000
           = $317,460
```

**Step 3: Bunkering CAPEX**
```
Bunkering_CAPEX = $387,819 + $317,460
                = $705,279
```

**Step 4: Bunkering Fixed OPEX**
```
Bunkering_Fixed_OPEX = $705,279 × 0.05
                     = $35,264/year per shuttle
```

---

## 10.7 Bunkering Variable OPEX (Pump Fuel)

### 10.7.1 Formula

```
Pumping_Time_hr = Bunker_Volume_m3 / Pump_Flow_m3ph

Fuel_per_Call_ton = (Pump_Power_kW × Pumping_Time_hr × SFOC_g_kWh) / 1e6

Bunkering_Variable_OPEX_per_Call = Fuel_per_Call_ton × Fuel_Price
```

### 10.7.2 Verification (5,000 m3 Bunker Volume, 1000 m3/h Pump)

**Same as Case 1 and Case 2-1** (bunker volume and pump rate are identical):

**Step 1: Pumping Time**
```
Pumping_Time = 5000 / 1000 = 5.0 hours
```

**Step 2: Fuel Consumption**
```
Fuel_ton = (158.73 × 5.0 × 379) / 1e6
         = 0.301 ton/call
```

**Step 3: Fuel Cost per Call**
```
Fuel_Cost = 0.301 × $600
          = $180.48/call
```

---

## 10.8 20-Year OPEX Summary (5,000 m3 Optimal)

### 10.8.1 Cost Growth Pattern

| Year | Vessels | Annual Calls | Shuttles | Shuttle Fixed OPEX | Shuttle Var OPEX |
|------|---------|--------------|----------|-------------------|------------------|
| 2030 | 50 | 600 | 3 | $1,939,095 | ~$1.9M |
| 2035 | 163 | 1,956 | 8 | $5,170,920 | ~$5.0M |
| 2040 | 275 | 3,300 | 14 | $9,049,110 | ~$8.7M |
| 2045 | 388 | 4,656 | 20 | $12,927,300 | ~$12.5M |
| 2050 | 500 | 6,000 | 26 | $16,805,490 | ~$16.2M |

### 10.8.2 NPC OPEX Components (from CSV)

| OPEX Component | 20-Year NPC (USD M) | % of Total |
|---------------|---------------------|------------|
| Shuttle Fixed OPEX | $100.20M | 24.9% |
| Bunkering Fixed OPEX | $5.47M | 1.4% |
| Shuttle Variable OPEX | $89.16M | 22.2% |
| Bunkering Variable OPEX | $12.51M | 3.1% |
| **Total OPEX** | **$207.34M** | **51.5%** |

---

## 10.9 Three-Case OPEX Comparison

| Component | Case 1 | Case 2-1 | Case 2-2 | Best |
|-----------|--------|----------|----------|------|
| Shuttle Fixed OPEX (20yr) | $58.42M | $181.56M | $100.20M | Case 1 |
| Bunkering Fixed OPEX (20yr) | $4.17M | $8.10M | $5.47M | Case 1 |
| Shuttle Variable OPEX (20yr) | $46.43M | $194.95M | $89.16M | Case 1 |
| Bunkering Variable OPEX (20yr) | $12.51M | $12.51M | $12.51M | Tie |
| **Total OPEX (20yr)** | **$121.53M** | **$397.12M** | **$207.34M** | **Case 1** |

### Key Observations

1. **Case 1 has lowest OPEX**: Shortest travel distance, smallest shuttles
2. **Case 2-2 is 70% more expensive than Case 1**: But 48% cheaper than Case 2-1
3. **Bunkering Variable OPEX is constant**: Same pump rate and bunker volume across all cases
4. **Shuttle Variable OPEX varies most**: Directly proportional to travel distance

---

## 10.10 OPEX Cost Drivers Analysis

### Distance Impact on Shuttle Variable OPEX

| Case | Distance (nm) | Fuel/Cycle (ton) | 20yr Shuttle Var OPEX |
|------|---------------|------------------|----------------------|
| Case 1 | ~0 (port) | 0.558 | $46.43M |
| Case 2-2 | 25 | 2.144 | $89.16M |
| Case 2-1 | 86 | 9.379 | $194.95M |

**Rule**: ~$1.7M/nm of distance over 20 years (approximate)

### Shuttle Size Impact on Fixed OPEX

| Optimal Shuttle | CAPEX | Fixed OPEX/yr | 20yr Fixed OPEX |
|----------------|-------|---------------|-----------------|
| 2,500 m3 | $7.69M | $384K | $58.42M (Case 1) |
| 5,000 m3 | $12.93M | $646K | $100.20M (Case 2-2) |
| 10,000 m3 | $21.75M | $1.09M | $181.56M (Case 2-1) |

---

## 10.11 Verification Summary

| Item | Manual Calculation | Expected | Status |
|------|-------------------|----------|--------|
| Shuttle Fixed OPEX (5,000 m3) | $646,365/yr | ~$646K/yr | [PASS] |
| Shuttle Fuel Cost (5,000 m3) | $1,286.57/cycle | ~$1,287/cycle | [PASS] |
| Pump Power | 158.73 kW | 158.73 kW | [PASS] |
| Bunkering Fixed OPEX | $35,264/yr | ~$35K/yr | [PASS] |
| Pump Fuel Cost | $180.48/call | ~$180/call | [PASS] |
| No Tank OPEX | $0 | $0 | [PASS] |

---

## 10.12 Key Formulas Summary

```
=== SHUTTLE (Case 2-2 - Round Trip) ===
Shuttle_Fixed_OPEX = CAPEX × 0.05
Shuttle_Var_OPEX = MCR × SFOC × 1.67 hr × 2.0 / 1e6 × $600
                 = MCR × 379 × 3.34 / 1e6 × $600

=== BUNKERING ===
Bunkering_CAPEX = (Shuttle_CAPEX × 0.03) + (158.73 kW × $2000)
Bunkering_Fixed_OPEX = Bunkering_CAPEX × 0.05
Bunkering_Var_OPEX = 158.73 kW × 5.0 hr × 379 / 1e6 × $600 = $180.48/call

=== NO TANK STORAGE ===
Tank_OPEX = $0 (No storage at Busan for Case 2-2)
```
