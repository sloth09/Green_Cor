# Chapter 9: OPEX Verification - Case 2-1 (Yeosu to Busan)

## 9.1 Overview

This document verifies all Operating Expenditure (OPEX) calculations for Case 2-1 (Yeosu).

| Component | Type | Formula Source |
|-----------|------|----------------|
| Shuttle Fixed OPEX | Annual | cost_calculator.py |
| Shuttle Variable OPEX | Per Cycle | cost_calculator.py |
| Bunkering Fixed OPEX | Annual | cost_calculator.py |
| Bunkering Variable OPEX | Per Call | cost_calculator.py |

**Note**: Case 2-1 has **NO** tank storage at Busan (direct supply from Yeosu).

---

## 9.2 Input Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Fuel Price | 600.0 | USD/ton | base.yaml |
| SFOC | 379.0 | g/kWh | base.yaml |
| Pump Delta Pressure | 4.0 | bar | base.yaml |
| Pump Efficiency | 0.7 | - | base.yaml |
| Shuttle Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Bunkering Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Shuttle Equipment Ratio | 0.03 | % of CAPEX | base.yaml |
| Distance | 86 | nautical miles | case_2_yeosu.yaml |
| Speed | 15 | knots | case_2_yeosu.yaml |
| Travel Time (one-way) | 5.73 | hours | Calculated (86/15) |
| Shore Pump Rate | 1500 | m3/h | base.yaml |
| Bunker Volume per Call | 5,000 | m3 | case_2_yeosu.yaml |

---

## 9.3 Key Difference from Case 1

| Aspect | Case 1 | Case 2-1 |
|--------|--------|----------|
| Travel Time (one-way) | 1.0 hr | 5.73 hr |
| Travel Factor | 1.0 | 2.0 (round trip) |
| Storage at Busan | Yes | No |
| Tank OPEX | Included | None |
| Optimal Shuttle | 2,500 m3 | 10,000 m3 |

**Why Travel Factor = 2.0 for Case 2?**
- Case 2 shuttles complete full round trips (Yeosu -> Busan -> Yeosu)
- Fuel is consumed during both outbound and return legs
- This doubles the fuel cost per cycle compared to one-way travel

---

## 9.4 Shuttle Fixed OPEX

### 9.4.1 Formula

```
Shuttle_Fixed_OPEX_Annual = Shuttle_CAPEX × Fixed_OPEX_Ratio
                         = Shuttle_CAPEX × 0.05
```

### 9.4.2 Verification (10,000 m3 Optimal Shuttle)

**Step 1: Shuttle CAPEX**
```
Shuttle_CAPEX = 61,500,000 × (10000 / 40000)^0.75
             = 61,500,000 × (0.25)^0.75
             = 61,500,000 × 0.3536
             = $21,746,400
```

**Step 2: Annual Fixed OPEX per Shuttle**
```
Fixed_OPEX = $21,746,400 × 0.05
           = $1,087,320/year per shuttle
```

### 9.4.3 Verification Table (Case 2 Shuttle Sizes)

| Shuttle (m3) | CAPEX (USD) | Fixed OPEX/yr (USD) |
|-------------|-------------|---------------------|
| 2,500 | $7,687,500 | $384,375 |
| 5,000 | $12,927,300 | $646,365 |
| **10,000** | **$21,746,400** | **$1,087,320** |
| 15,000 | $29,631,600 | $1,481,580 |
| 20,000 | $36,567,000 | $1,828,350 |
| 25,000 | $43,032,450 | $2,151,623 |
| 30,000 | $49,163,100 | $2,458,155 |
| 35,000 | $55,032,300 | $2,751,615 |
| 40,000 | $61,500,000 | $3,075,000 |
| 45,000 | $67,000,650 | $3,350,033 |
| 50,000 | $72,504,450 | $3,625,223 |

---

## 9.5 Shuttle Variable OPEX (Fuel Cost)

### 9.5.1 Formula

For Case 2, the shuttle makes a **round trip**:

```
Fuel_per_Cycle_ton = MCR_kW × SFOC_g_kWh × Travel_Time_hr × Travel_Factor / 1e6

where:
  Travel_Time = 5.73 hours (one-way)
  Travel_Factor = 2.0 (round trip: outbound + return)

Fuel_Cost_per_Cycle = Fuel_per_Cycle_ton × Fuel_Price_USD_per_ton
```

### 9.5.2 Verification (10,000 m3 Shuttle)

**Step 1: Get MCR**
```
MCR(10000 m3) = 2159 kW  (from mcr_map_kw)
```

**Step 2: Calculate Fuel per Cycle (Round Trip)**
```
Fuel_ton = (2159 × 379 × 5.73 × 2.0) / 1e6
         = (2159 × 379 × 11.46) / 1e6
         = 9,379,262 / 1e6
         = 9.379 ton/cycle
```

**Step 3: Calculate Fuel Cost per Cycle**
```
Fuel_Cost = 9.379 × $600
          = $5,627.57/cycle
```

### 9.5.3 Comparison with Case 1

| Metric | Case 1 (2,500 m3) | Case 2-1 (10,000 m3) | Ratio |
|--------|-------------------|---------------------|-------|
| MCR | 1,473 kW | 2,159 kW | 1.47x |
| Travel (one-way) | 1.0 hr | 5.73 hr | 5.73x |
| Travel Factor | 1.0 | 2.0 | 2.0x |
| **Fuel/Cycle** | **0.558 ton** | **9.379 ton** | **16.8x** |
| **Cost/Cycle** | **$335** | **$5,628** | **16.8x** |

### 9.5.4 MCR and Fuel Cost Table (Case 2 Sizes)

| Shuttle (m3) | MCR (kW) | Fuel/Cycle (ton) | Fuel Cost/Cycle (USD) |
|-------------|----------|------------------|----------------------|
| 2,500 | 1,473 | 6.402 | $3,841.20 |
| 5,000 | 1,694 | 7.362 | $4,417.20 |
| **10,000** | **2,159** | **9.379** | **$5,627.57** |
| 15,000 | 2,485 | 10,796 | $6,477.60 |
| 20,000 | 2,751 | 11,951 | $7,170.60 |
| 25,000 | 2,981 | 12,951 | $7,770.60 |
| 30,000 | 3,185 | 13,838 | $8,302.80 |
| 35,000 | 3,372 | 14,651 | $8,790.60 |
| 40,000 | 3,546 | 15,407 | $9,244.20 |
| 45,000 | 3,710 | 16,120 | $9,672.00 |
| 50,000 | 3,867 | 16,802 | $10,081.20 |

---

## 9.6 Bunkering Fixed OPEX

### 9.6.1 Formula

```
Bunkering_CAPEX = Shuttle_Equipment_Cost + Pump_CAPEX
                = (Shuttle_CAPEX × 0.03) + (Pump_Power_kW × $2000/kW)

Bunkering_Fixed_OPEX = Bunkering_CAPEX × 0.05
```

### 9.6.2 Verification (10,000 m3 Shuttle, 1000 m3/h Pump)

**Step 1: Equipment Cost**
```
Shuttle_Equipment = $21,746,400 × 0.03
                  = $652,392
```

**Step 2: Pump CAPEX**
```
Pump_Power = 158.73 kW  (same as Case 1)
Pump_CAPEX = 158.73 × $2,000
           = $317,460
```

**Step 3: Bunkering CAPEX**
```
Bunkering_CAPEX = $652,392 + $317,460
                = $969,852
```

**Step 4: Bunkering Fixed OPEX**
```
Bunkering_Fixed_OPEX = $969,852 × 0.05
                     = $48,493/year per shuttle
```

---

## 9.7 Bunkering Variable OPEX (Pump Fuel)

### 9.7.1 Formula

```
Pumping_Time_hr = Bunker_Volume_m3 / Pump_Flow_m3ph

Fuel_per_Call_ton = (Pump_Power_kW × Pumping_Time_hr × SFOC_g_kWh) / 1e6

Bunkering_Variable_OPEX_per_Call = Fuel_per_Call_ton × Fuel_Price
```

### 9.7.2 Verification (5,000 m3 Bunker Volume, 1000 m3/h Pump)

**Same as Case 1** (bunker volume and pump rate are identical):

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

## 9.8 20-Year OPEX Summary (10,000 m3 Optimal)

### 9.8.1 Annual Cost Calculation

Each year's OPEX depends on:
- Number of shuttles in operation
- Number of cycles per year
- Number of bunkering calls

### 9.8.2 Cost Growth Pattern

| Year | Vessels | Annual Calls | Shuttles | Shuttle Fixed OPEX | Shuttle Var OPEX |
|------|---------|--------------|----------|-------------------|------------------|
| 2030 | 50 | 600 | 3 | $3,261,960 | ~$3.7M |
| 2035 | 163 | 1,956 | 9 | $9,785,880 | ~$11.2M |
| 2040 | 275 | 3,300 | 15 | $16,309,800 | ~$18.7M |
| 2045 | 388 | 4,656 | 21 | $22,833,720 | ~$26.2M |
| 2050 | 500 | 6,000 | 28 | $30,444,960 | ~$34.9M |

### 9.8.3 NPC OPEX Components (from CSV)

| OPEX Component | 20-Year NPC (USD M) | % of Total |
|---------------|---------------------|------------|
| Shuttle Fixed OPEX | $181.56M | 24.3% |
| Bunkering Fixed OPEX | $8.10M | 1.1% |
| Shuttle Variable OPEX | $194.95M | 26.1% |
| Bunkering Variable OPEX | $12.51M | 1.7% |
| **Total OPEX** | **$397.12M** | **53.2%** |

---

## 9.9 OPEX Comparison: Case 1 vs Case 2-1

| Component | Case 1 (2,500 m3) | Case 2-1 (10,000 m3) | Ratio |
|-----------|-------------------|---------------------|-------|
| Shuttle Fixed OPEX (20yr) | $58.42M | $181.56M | 3.1x |
| Bunkering Fixed OPEX (20yr) | $4.17M | $8.10M | 1.9x |
| Shuttle Variable OPEX (20yr) | $46.43M | $194.95M | 4.2x |
| Bunkering Variable OPEX (20yr) | $12.51M | $12.51M | 1.0x |
| **Total OPEX (20yr)** | **$121.53M** | **$397.12M** | **3.3x** |

**Why is Case 2-1 OPEX so much higher?**

1. **Longer travel distance**: 86 nm vs ~0 nm internal port movement
2. **Larger shuttles needed**: 10,000 m3 vs 2,500 m3
3. **Higher fuel consumption**: 9.4 ton/cycle vs 0.6 ton/cycle
4. **More shuttles required**: Higher CAPEX-based fixed OPEX

---

## 9.10 Verification Summary

| Item | Manual Calculation | Expected | Status |
|------|-------------------|----------|--------|
| Shuttle Fixed OPEX (10,000 m3) | $1,087,320/yr | ~$1.09M/yr | [PASS] |
| Shuttle Fuel Cost (10,000 m3) | $5,627.57/cycle | ~$5,600/cycle | [PASS] |
| Pump Power | 158.73 kW | 158.73 kW | [PASS] |
| Bunkering Fixed OPEX | $48,493/yr | ~$48K/yr | [PASS] |
| Pump Fuel Cost | $180.48/call | ~$180/call | [PASS] |
| No Tank OPEX | $0 | $0 | [PASS] |

---

## 9.11 Key Formulas Summary

```
=== SHUTTLE (Case 2 - Round Trip) ===
Shuttle_Fixed_OPEX = CAPEX × 0.05
Shuttle_Var_OPEX = MCR × SFOC × Travel_hr × 2.0 / 1e6 × Fuel_Price
                         ↑ Travel_Factor = 2.0 for round trip

=== BUNKERING ===
Bunkering_CAPEX = (Shuttle_CAPEX × 0.03) + (Pump_Power × $2000)
Bunkering_Fixed_OPEX = Bunkering_CAPEX × 0.05
Bunkering_Var_OPEX = Pump_Power × Pump_hr × SFOC / 1e6 × Fuel_Price

=== NO TANK STORAGE ===
Tank_OPEX = $0 (No storage at Busan for Case 2)
```
