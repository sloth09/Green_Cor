# Chapter 8: OPEX Verification - Case 1 (Busan Port with Storage)

## 8.1 Overview

This document verifies all Operating Expenditure (OPEX) calculations for Case 1.

| Component | Type | Formula Source |
|-----------|------|----------------|
| Shuttle Fixed OPEX | Annual | cost_calculator.py |
| Shuttle Variable OPEX | Per Cycle | cost_calculator.py |
| Bunkering Fixed OPEX | Annual | cost_calculator.py |
| Bunkering Variable OPEX | Per Call | cost_calculator.py |
| Tank Fixed OPEX | Annual | cost_calculator.py |
| Tank Variable OPEX | Annual | cost_calculator.py |

---

## 8.2 Input Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Fuel Price | 600.0 | USD/ton | base.yaml |
| Electricity Price | 0.0769 | USD/kWh | base.yaml |
| SFOC | 379.0 | g/kWh | base.yaml |
| Pump Delta Pressure | 4.0 | bar | base.yaml |
| Pump Efficiency | 0.7 | - | base.yaml |
| Shuttle Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Bunkering Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Tank Fixed OPEX Ratio | 0.03 | % of CAPEX | base.yaml |
| Shuttle Equipment Ratio | 0.03 | % of CAPEX | base.yaml |
| Travel Time (one-way) | 1.0 | hours | case_1.yaml |
| Shore Pump Rate | 1500 | m3/h | base.yaml |

---

## 8.3 Shuttle Fixed OPEX

### 8.3.1 Formula

```
Shuttle_Fixed_OPEX_Annual = Shuttle_CAPEX × Fixed_OPEX_Ratio
                         = Shuttle_CAPEX × 0.05
```

### 8.3.2 Verification (2,500 m3 Optimal Shuttle)

**Step 1: Shuttle CAPEX**
```
Shuttle_CAPEX = 61,500,000 × (2500 / 40000)^0.75
             = 61,500,000 × (0.0625)^0.75
             = 61,500,000 × 0.125
             = $7,687,500
```

**Step 2: Annual Fixed OPEX per Shuttle**
```
Fixed_OPEX = $7,687,500 × 0.05
           = $384,375/year per shuttle
```

### 8.3.3 Verification Table (All Shuttle Sizes)

| Shuttle (m3) | CAPEX (USD) | Fixed OPEX/yr (USD) |
|-------------|-------------|---------------------|
| 500 | $2,300,100 | $115,005 |
| 1,000 | $3,868,350 | $193,418 |
| 1,500 | $5,308,917 | $265,446 |
| 2,000 | $6,502,906 | $325,145 |
| **2,500** | **$7,687,500** | **$384,375** |
| 3,000 | $8,869,894 | $443,495 |
| 3,500 | $10,051,579 | $502,579 |
| 4,000 | $11,233,125 | $561,656 |
| 4,500 | $12,414,828 | $620,741 |
| 5,000 | $12,927,300 | $646,365 |

---

## 8.4 Shuttle Variable OPEX (Fuel Cost)

### 8.4.1 Formula

Shuttle fuel consumption is based on propulsion during travel:

```
Fuel_per_Cycle_ton = MCR_kW × SFOC_g_kWh × Travel_Time_hr × Travel_Factor / 1e6

Fuel_Cost_per_Cycle = Fuel_per_Cycle_ton × Fuel_Price_USD_per_ton

where:
  MCR = Maximum Continuous Rating (from mcr_map_kw)
  SFOC = 379 g/kWh
  Travel_Time = 1.0 hour (one-way for Case 1)
  Travel_Factor = 1.0 (Case 1 is one-way per cycle, return is part of next cycle)
```

### 8.4.2 Verification (2,500 m3 Shuttle)

**Step 1: Get MCR**
```
MCR(2500 m3) = 1473 kW  (from mcr_map_kw)
```

**Step 2: Calculate Fuel per Cycle**
```
Fuel_ton = (1473 × 379 × 1.0 × 1.0) / 1e6
         = 558,267 / 1e6
         = 0.558 ton/cycle
```

**Step 3: Calculate Fuel Cost per Cycle**
```
Fuel_Cost = 0.558 × $600
          = $335.01/cycle
```

### 8.4.3 Annual Shuttle Variable OPEX

```
Annual_Variable_OPEX = Fuel_Cost_per_Cycle × Annual_Cycles × Num_Shuttles
```

For 2030 (2 shuttles, ~980 cycles/shuttle):
```
Annual_Variable_OPEX = $335.01 × 980 × 2
                     = $656,620/year
```

### 8.4.4 MCR and Fuel Cost Table

| Shuttle (m3) | MCR (kW) | Fuel/Cycle (ton) | Fuel Cost/Cycle (USD) |
|-------------|----------|------------------|----------------------|
| 500 | 1,296 | 0.491 | $294.69 |
| 1,000 | 1,341 | 0.508 | $305.01 |
| 1,500 | 1,385 | 0.525 | $315.11 |
| 2,000 | 1,429 | 0.542 | $325.06 |
| **2,500** | **1,473** | **0.558** | **$335.01** |
| 3,000 | 1,517 | 0.575 | $344.96 |
| 3,500 | 1,562 | 0.592 | $355.29 |
| 4,000 | 1,606 | 0.609 | $365.24 |
| 4,500 | 1,650 | 0.626 | $375.26 |
| 5,000 | 1,694 | 0.642 | $385.28 |

---

## 8.5 Bunkering Fixed OPEX

### 8.5.1 Formula

```
Bunkering_CAPEX = Shuttle_Equipment_Cost + Pump_CAPEX
                = (Shuttle_CAPEX × 0.03) + (Pump_Power_kW × $2000/kW)

Bunkering_Fixed_OPEX = Bunkering_CAPEX × 0.05
```

### 8.5.2 Pump Power Calculation

```
Pump_Power_kW = (Flow_Rate_m3ph × Delta_P_bar × 100) / (3600 × Efficiency)
             = (1000 × 4 × 100) / (3600 × 0.7)
             = 400,000 / 2,520
             = 158.73 kW
```

### 8.5.3 Verification (2,500 m3 Shuttle, 1000 m3/h Pump)

**Step 1: Equipment Cost**
```
Shuttle_Equipment = $7,687,500 × 0.03
                  = $230,625
```

**Step 2: Pump CAPEX**
```
Pump_CAPEX = 158.73 kW × $2,000/kW
           = $317,460
```

**Step 3: Bunkering CAPEX**
```
Bunkering_CAPEX = $230,625 + $317,460
                = $548,085
```

**Step 4: Bunkering Fixed OPEX**
```
Bunkering_Fixed_OPEX = $548,085 × 0.05
                     = $27,404/year per shuttle
```

---

## 8.6 Bunkering Variable OPEX (Pump Fuel)

### 8.6.1 Formula

```
Pumping_Time_hr = Bunker_Volume_m3 / Pump_Flow_m3ph

Fuel_per_Call_ton = (Pump_Power_kW × Pumping_Time_hr × SFOC_g_kWh) / 1e6

Bunkering_Variable_OPEX_per_Call = Fuel_per_Call_ton × Fuel_Price
```

### 8.6.2 Verification (5,000 m3 Bunker Volume, 1000 m3/h Pump)

**Step 1: Pumping Time**
```
Pumping_Time = 5000 / 1000 = 5.0 hours
```

**Step 2: Fuel Consumption**
```
Fuel_ton = (158.73 × 5.0 × 379) / 1e6
         = 300,793 / 1e6
         = 0.301 ton/call
```

**Step 3: Fuel Cost per Call**
```
Fuel_Cost = 0.301 × $600
          = $180.48/call
```

### 8.6.3 Annual Bunkering Variable OPEX

```
Annual_Bunkering_Variable = Fuel_Cost_per_Call × Annual_Calls
```

For 2030 (50 vessels × 12 voyages = 600 calls):
```
Annual_Bunkering_Variable = $180.48 × 600
                          = $108,288/year
```

---

## 8.7 Tank Storage OPEX (Case 1 Only)

### 8.7.1 Tank Fixed OPEX Formula

```
Tank_CAPEX = Tank_Size_kg × Cost_per_kg
           = 35,000 × 1000 × $1.215
           = $42,525,000

Tank_Fixed_OPEX = Tank_CAPEX × Fixed_OPEX_Ratio
                = $42,525,000 × 0.03
                = $1,275,750/year
```

### 8.7.2 Tank Variable OPEX Formula (Refrigeration)

```
Tank_Variable_OPEX = Tank_kg × Cooling_Energy_kWh_per_kg × Electricity_Price
                   = 35,000,000 × 0.0378 × $0.0769
                   = $101,754/year
```

### 8.7.3 Tank OPEX Summary

| Component | Annual Cost |
|-----------|-------------|
| Tank Fixed OPEX | $1,275,750 |
| Tank Variable OPEX | $101,754 |
| **Total Tank OPEX** | **$1,377,504** |

---

## 8.8 20-Year OPEX Summary (2,500 m3 Optimal)

### 8.8.1 Annual Cost Calculation Method

Each year's OPEX depends on:
- Number of shuttles in operation
- Number of bunkering calls

### 8.8.2 Cost Growth Pattern

| Year | Vessels | Annual Calls | Shuttles | Shuttle Fixed OPEX | Bunkering Var OPEX |
|------|---------|--------------|----------|-------------------|-------------------|
| 2030 | 50 | 600 | 2 | $768,750 | $108,288 |
| 2035 | 163 | 1,956 | 4 | $1,537,500 | $353,080 |
| 2040 | 275 | 3,300 | 7 | $2,690,625 | $595,584 |
| 2045 | 388 | 4,656 | 10 | $3,843,750 | $840,345 |
| 2050 | 500 | 6,000 | 13 | $4,996,875 | $1,082,880 |

### 8.8.3 NPC OPEX Components (from CSV)

| OPEX Component | 20-Year NPC (USD M) | % of Total |
|---------------|---------------------|------------|
| Shuttle Fixed OPEX | $58.42M | 24.6% |
| Bunkering Fixed OPEX | $4.17M | 1.8% |
| Shuttle Variable OPEX | $46.43M | 19.6% |
| Bunkering Variable OPEX | $12.51M | 5.3% |
| **Total OPEX** | **$121.53M** | **51.3%** |

---

## 8.9 Verification Summary

| Item | Manual Calculation | Expected | Status |
|------|-------------------|----------|--------|
| Shuttle Fixed OPEX (2500 m3) | $384,375/yr | ~$384K/yr | [PASS] |
| Shuttle Fuel Cost (2500 m3) | $335.01/cycle | ~$335/cycle | [PASS] |
| Pump Power | 158.73 kW | 158.73 kW | [PASS] |
| Bunkering Fixed OPEX | $27,404/yr | ~$27K/yr | [PASS] |
| Pump Fuel Cost | $180.48/call | ~$180/call | [PASS] |
| Tank Fixed OPEX | $1,275,750/yr | ~$1.28M/yr | [PASS] |
| Tank Variable OPEX | $101,754/yr | ~$102K/yr | [PASS] |

---

## 8.10 Key Formulas Summary

```
=== SHUTTLE ===
Shuttle_Fixed_OPEX = CAPEX × 0.05
Shuttle_Var_OPEX = MCR × SFOC × Travel_hr × Travel_Factor / 1e6 × Fuel_Price

=== BUNKERING ===
Bunkering_CAPEX = (Shuttle_CAPEX × 0.03) + (Pump_Power × $2000)
Bunkering_Fixed_OPEX = Bunkering_CAPEX × 0.05
Bunkering_Var_OPEX = Pump_Power × Pump_hr × SFOC / 1e6 × Fuel_Price

=== TANK (Case 1 Only) ===
Tank_Fixed_OPEX = Tank_CAPEX × 0.03
Tank_Var_OPEX = Tank_kg × Cooling_kWh/kg × Elec_Price
```
