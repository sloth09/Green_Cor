# Chapter 3: Case 1 - Busan Port with Storage

## 3.1 Overview

| Parameter | Value |
|-----------|-------|
| Case ID | case_1 |
| Storage at Busan | **Yes** |
| Travel Time (one-way) | 1.0 hour |
| Bunker Volume per Call | 5,000 m3 |
| Optimal Shuttle Size | **2,500 m3** |

---

## 3.2 Cycle Time Calculation

### 3.2.1 Formula (Case 1)

For Case 1, the shuttle makes **multiple trips** from storage tank to vessel:

```
Trips_per_Call = ceil(Bunker_Volume / Shuttle_Size)

Cycle_Duration = Shore_Loading + Travel_Out + Travel_Return + Setup + Pumping

where:
  Shore_Loading = Shuttle_Size / Shore_Pump_Rate = Shuttle_Size / 1500
  Travel_Out = 1.0 hour
  Travel_Return = 1.0 hour
  Setup = 2.0 hours (1.0 inbound + 1.0 outbound)
  Pumping = Shuttle_Size / Pump_Rate
```

### 3.2.2 Example: 2,500 m3 Shuttle (Optimal)

**Step 1: Trips per Call**
```
Trips_per_Call = ceil(5000 / 2500) = 2 trips
```

**Step 2: Cycle Duration**
```
Shore_Loading = 2500 / 1500 = 1.6667 hours
Travel_Out = 1.0 hour
Travel_Return = 1.0 hour
Setup = 2.0 hours
Pumping = 2500 / 1000 = 2.5 hours

Cycle_Duration = 1.6667 + 1.0 + 1.0 + 2.0 + 2.5 = 8.1667 hours
```

**CSV Verification**: `Cycle_Duration_hr = 8.1667` [PASS]

### 3.2.3 Example: 5,000 m3 Shuttle

**Step 1: Trips per Call**
```
Trips_per_Call = ceil(5000 / 5000) = 1 trip
```

**Step 2: Cycle Duration**
```
Shore_Loading = 5000 / 1500 = 3.3333 hours
Travel_Out = 1.0 hour
Travel_Return = 1.0 hour
Setup = 2.0 hours
Pumping = 5000 / 1000 = 5.0 hours

Cycle_Duration = 3.3333 + 1.0 + 1.0 + 2.0 + 5.0 = 12.3333 hours
```

**CSV Verification**: `Cycle_Duration_hr = 12.3333` [PASS]

---

## 3.3 Annual Capacity Calculation

### 3.3.1 Formula

```
Annual_Cycles_Max = Max_Annual_Hours / Cycle_Duration
                  = 8000 / Cycle_Duration

Annual_Supply_m3 = Annual_Cycles_Max × Shuttle_Size
```

### 3.3.2 Verification Table

| Shuttle (m3) | Cycle (hr) | Annual Cycles | Annual Supply (m3) | CSV Match |
|-------------|------------|---------------|-------------------|-----------|
| 2,500 | 8.1667 | 979.59 | 2,448,980 | [PASS] |
| 5,000 | 12.3333 | 648.65 | 3,243,243 | [PASS] |

---

## 3.4 Cost Verification

### 3.4.1 Shuttle CAPEX

**Formula:**
```
Shuttle_CAPEX = 61,500,000 × (Size / 40,000)^0.75
```

**2,500 m3 Shuttle:**
```
CAPEX = 61,500,000 × (2500 / 40000)^0.75
      = 61,500,000 × (0.0625)^0.75
      = 61,500,000 × 0.1263
      = $7,761,316
```

**5,000 m3 Shuttle:**
```
CAPEX = 61,500,000 × (5000 / 40000)^0.75
      = 61,500,000 × (0.125)^0.75
      = 61,500,000 × 0.2122
      = $13,051,896
```

### 3.4.2 Annualized CAPEX

**Formula:**
```
Annualized_CAPEX = CAPEX / Annuity_Factor = CAPEX / 10.8355
```

**Per Shuttle:**
| Shuttle (m3) | CAPEX | Annualized CAPEX/yr |
|-------------|-------|---------------------|
| 2,500 | $7,761,316 | $716,345 |
| 5,000 | $13,051,896 | $1,204,496 |

### 3.4.3 Bunkering Equipment CAPEX

**Formula:**
```
Pump_Power_kW = (Pump_Rate × Delta_P × 100) / (3600 × Efficiency)
             = (1000 × 4 × 100) / (3600 × 0.7)
             = 400000 / 2520
             = 158.73 kW

Pump_CAPEX = Power_kW × $2000/kW
           = 158.73 × 2000
           = $317,460
```

---

## 3.5 Shuttle Size Comparison

### 3.5.1 Comparison Table (1000 m3/h Pump)

| Metric | 2,500 m3 | 5,000 m3 | Difference |
|--------|----------|----------|------------|
| **NPC Total** | **$237.05M** | $264.24M | +$27.19M (+11.5%) |
| **LCOAmmonia** | **$1.01/ton** | $1.12/ton | +$0.11/ton (+10.9%) |
| Cycle Duration | 8.17 hr | 12.33 hr | +4.16 hr |
| Trips per Call | 2 | 1 | -1 |
| Annual Cycles | 979.59 | 648.65 | -330.94 |
| Time Utilization | 100% | 100% | - |

### 3.5.2 Cost Breakdown Comparison

| Cost Component | 2,500 m3 | 5,000 m3 |
|---------------|----------|----------|
| Annualized Shuttle CAPEX | $107.84M | $138.41M |
| Annualized Bunkering CAPEX | $7.69M | $7.55M |
| Shuttle Fixed OPEX | $58.42M | $74.99M |
| Bunkering Fixed OPEX | $4.17M | $4.09M |
| Shuttle Variable OPEX | $46.43M | $26.70M |
| Bunkering Variable OPEX | $12.51M | $12.51M |
| **NPC Total** | **$237.05M** | **$264.24M** |

### 3.5.3 Why 2,500 m3 is Optimal

1. **Lower CAPEX per unit**: $7.76M vs $13.05M per shuttle
2. **Higher cycle frequency**: 979 cycles/year vs 649 cycles/year
3. **Better scalability**: Easier to add incremental capacity
4. **Fleet flexibility**: Multiple smaller shuttles provide redundancy

The higher variable OPEX from more trips ($46.43M vs $26.70M) is offset by significantly lower annualized CAPEX ($107.84M vs $138.41M).

---

## 3.6 Full Scenario Results

| Shuttle (m3) | NPC (M$) | LCO ($/ton) | Cycle (hr) | Trips/Call | Utilization |
|-------------|----------|-------------|------------|------------|-------------|
| 500 | 380.67 | 1.62 | 4.83 | 10 | 100% |
| 1,000 | 274.80 | 1.17 | 5.67 | 5 | 100% |
| 1,500 | 290.11 | 1.23 | 6.50 | 4 | 100% |
| 2,000 | 281.70 | 1.20 | 7.33 | 3 | 100% |
| **2,500** | **237.05** | **1.01** | **8.17** | **2** | 100% |
| 3,000 | 282.25 | 1.20 | 9.00 | 2 | 100% |
| 3,500 | 333.87 | 1.42 | 9.83 | 2 | 100% |
| 4,000 | 384.48 | 1.63 | 10.67 | 2 | 100% |
| 4,500 | 441.67 | 1.87 | 11.50 | 2 | 100% |
| 5,000 | 264.24 | 1.12 | 12.33 | 1 | 100% |
| 7,500 | 445.34 | 1.89 | 16.50 | 1 | 100% |
| 10,000 | 660.58 | 2.80 | 20.67 | 1 | 100% |

---

## 3.7 Verification Summary

| Item | Expected | CSV Result | Status |
|------|----------|------------|--------|
| Optimal Shuttle | 2,500 m3 | 2,500 m3 (min NPC) | [PASS] |
| Cycle Time (2500) | 8.1667 hr | 8.1667 hr | [PASS] |
| Cycle Time (5000) | 12.3333 hr | 12.3333 hr | [PASS] |
| Annuity Factor | 10.8355 | 10.8355 | [PASS] |
| NPC (2500) | ~$237M | $237.05M | [PASS] |
| LCO (2500) | ~$1.01/ton | $1.01/ton | [PASS] |
