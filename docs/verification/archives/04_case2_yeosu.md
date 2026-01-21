# Chapter 4: Case 2-1 - Yeosu to Busan

## 4.1 Overview

| Parameter | Value |
|-----------|-------|
| Case ID | case_2_yeosu |
| Storage at Busan | **No** |
| Route | Yeosu to Busan |
| Distance | 86 nautical miles |
| Travel Time (one-way) | 5.73 hours (86 nm / 15 knots) |
| Bunker Volume per Call | 5,000 m3 |
| Optimal Shuttle Size | **10,000 m3** |

---

## 4.2 Cycle Time Calculation

### 4.2.1 Formula (Case 2 - Direct Supply)

For Case 2, the shuttle serves **multiple vessels per trip**:

```
Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)

Cycle_Duration = Shore_Loading + Travel_Out + Travel_Return + Port_Entry_Exit
               + (Vessels_per_Trip × (Movement + Setup + Pumping))

where:
  Shore_Loading = Shuttle_Size / Shore_Pump_Rate = Shuttle_Size / 1500
  Travel_Out = 5.73 hours (86 nm / 15 knots)
  Travel_Return = 5.73 hours
  Port_Entry_Exit = 2.0 hours (1.0 entry + 1.0 exit)
  Movement = 1.0 hour per vessel
  Setup = 2.0 hours per vessel (1.0 inbound + 1.0 outbound)
  Pumping = Bunker_Volume / Pump_Rate = 5000 / 1000 = 5.0 hours per vessel
```

### 4.2.2 Example: 10,000 m3 Shuttle (Optimal)

**Step 1: Vessels per Trip**
```
Vessels_per_Trip = floor(10000 / 5000) = 2 vessels
```

**Step 2: Fixed Components**
```
Shore_Loading = 10000 / 1500 = 6.6667 hours
Travel_Out = 5.73 hours
Travel_Return = 5.73 hours
Port_Entry_Exit = 2.0 hours

Fixed_Time = 6.6667 + 5.73 + 5.73 + 2.0 = 20.1267 hours
```

**Step 3: Per-Vessel Components**
```
Per_Vessel_Time = Movement + Setup + Pumping
               = 1.0 + 2.0 + 5.0
               = 8.0 hours/vessel

Total_Vessel_Time = 2 vessels × 8.0 hours = 16.0 hours
```

**Step 4: Total Cycle Duration**
```
Cycle_Duration = Fixed_Time + Total_Vessel_Time
               = 20.1267 + 16.0
               = 36.1267 hours
```

**CSV Verification**: `Cycle_Duration_hr = 36.1267` [PASS]

### 4.2.3 Example: 5,000 m3 Shuttle

**Step 1: Vessels per Trip**
```
Vessels_per_Trip = floor(5000 / 5000) = 1 vessel
```

**Step 2: Fixed Components**
```
Shore_Loading = 5000 / 1500 = 3.3333 hours
Travel_Out = 5.73 hours
Travel_Return = 5.73 hours
Port_Entry_Exit = 2.0 hours

Fixed_Time = 3.3333 + 5.73 + 5.73 + 2.0 = 16.7933 hours
```

**Step 3: Per-Vessel Components**
```
Per_Vessel_Time = 1.0 + 2.0 + 5.0 = 8.0 hours
Total_Vessel_Time = 1 vessel × 8.0 hours = 8.0 hours
```

**Step 4: Total Cycle Duration**
```
Cycle_Duration = 16.7933 + 8.0 = 24.7933 hours
```

**CSV Verification**: `Cycle_Duration_hr = 24.7933` [PASS]

### 4.2.4 Example: 15,000 m3 Shuttle

**Step 1: Vessels per Trip**
```
Vessels_per_Trip = floor(15000 / 5000) = 3 vessels
```

**Step 2: Fixed Components**
```
Shore_Loading = 15000 / 1500 = 10.0 hours
Travel_Out = 5.73 hours
Travel_Return = 5.73 hours
Port_Entry_Exit = 2.0 hours

Fixed_Time = 10.0 + 5.73 + 5.73 + 2.0 = 23.46 hours
```

**Step 3: Per-Vessel Components**
```
Total_Vessel_Time = 3 vessels × 8.0 hours = 24.0 hours
```

**Step 4: Total Cycle Duration**
```
Cycle_Duration = 23.46 + 24.0 = 47.46 hours
```

**CSV Verification**: `Cycle_Duration_hr = 47.46` [PASS]

---

## 4.3 Annual Capacity Calculation

### 4.3.1 Formula

```
Annual_Cycles_Max = Max_Annual_Hours / Cycle_Duration
                  = 8000 / Cycle_Duration

Annual_Supply_m3 = Annual_Cycles_Max × Shuttle_Size
Ships_Per_Year = Annual_Cycles_Max × Vessels_per_Trip
```

### 4.3.2 Verification Table

| Shuttle (m3) | Vessels/Trip | Cycle (hr) | Annual Cycles | Ships/Year | CSV Match |
|-------------|--------------|------------|---------------|------------|-----------|
| 5,000 | 1 | 24.79 | 322.67 | 322.67 | [PASS] |
| 10,000 | 2 | 36.13 | 221.44 | 442.89 | [PASS] |
| 15,000 | 3 | 47.46 | 168.56 | 505.69 | [PASS] |

---

## 4.4 Cost Verification

### 4.4.1 Shuttle CAPEX

**10,000 m3 Shuttle:**
```
CAPEX = 61,500,000 × (10000 / 40000)^0.75
      = 61,500,000 × (0.25)^0.75
      = 61,500,000 × 0.3536
      = $21,746,430
```

**5,000 m3 Shuttle:**
```
CAPEX = 61,500,000 × (5000 / 40000)^0.75
      = 61,500,000 × (0.125)^0.75
      = 61,500,000 × 0.2102
      = $12,927,300
```

### 4.4.2 Annualized CAPEX

| Shuttle (m3) | CAPEX | Annualized CAPEX/yr |
|-------------|-------|---------------------|
| 5,000 | $12,927,300 | $1,193,053 |
| 10,000 | $21,746,430 | $2,007,330 |
| 15,000 | $29,631,149 | $2,735,075 |

---

## 4.5 Shuttle Size Comparison

### 4.5.1 Comparison Table (1000 m3/h Pump)

| Metric | 5,000 m3 | 10,000 m3 | 15,000 m3 |
|--------|----------|-----------|-----------|
| **NPC Total** | $754.93M | **$747.18M** | $803.67M |
| **LCOAmmonia** | $3.20/ton | **$3.17/ton** | $3.41/ton |
| Cycle Duration | 24.79 hr | 36.13 hr | 47.46 hr |
| Vessels per Trip | 1 | 2 | 3 |
| Annual Cycles | 322.67 | 221.44 | 168.56 |
| Ships per Year | 322.67 | 442.89 | 505.69 |
| Time Utilization | 100% | 100% | 100% |

### 4.5.2 Cost Breakdown Comparison

| Cost Component | 5,000 m3 | 10,000 m3 | 15,000 m3 |
|---------------|----------|-----------|-----------|
| Annualized Shuttle CAPEX | $268.47M | $335.12M | $399.82M |
| Annualized Bunkering CAPEX | $14.65M | $14.95M | $16.30M |
| Shuttle Fixed OPEX | $145.45M | $181.56M | $216.61M |
| Bunkering Fixed OPEX | $7.93M | $8.10M | $8.83M |
| Shuttle Variable OPEX | $305.93M | $194.95M | $149.59M |
| Bunkering Variable OPEX | $12.51M | $12.51M | $12.51M |
| **NPC Total** | **$754.93M** | **$747.18M** | **$803.67M** |

### 4.5.3 Why 10,000 m3 is Optimal

1. **Economies of batch**: 2 vessels/trip reduces travel cost per vessel by 50%
2. **CAPEX efficiency**: Larger shuttle amortized over more vessels
3. **Sweet spot**: Balances cycle time increase vs vessels served

The 5,000 m3 shuttle has lower CAPEX but very high variable OPEX ($305.93M) due to many trips.
The 15,000 m3 shuttle serves more vessels but has diminishing returns on cycle efficiency.

---

## 4.6 Full Scenario Results

| Shuttle (m3) | NPC (M$) | LCO ($/ton) | Cycle (hr) | Vessels/Trip | Utilization |
|-------------|----------|-------------|------------|--------------|-------------|
| 2,500 | 1024.99 | 4.35 | 23.13 | 1 | 100% |
| 5,000 | 754.93 | 3.20 | 24.79 | 1 | 100% |
| **10,000** | **747.18** | **3.17** | **36.13** | **2** | 100% |
| 15,000 | 803.67 | 3.41 | 47.46 | 3 | 100% |
| 20,000 | 904.15 | 3.84 | 58.79 | 4 | 100% |
| 25,000 | 962.45 | 4.08 | 70.13 | 5 | 100% |
| 30,000 | 1043.96 | 4.43 | 81.46 | 6 | 100% |
| 35,000 | 1124.44 | 4.77 | 92.79 | 7 | 100% |
| 40,000 | 1206.75 | 5.12 | 104.13 | 8 | 100% |
| 45,000 | 1293.64 | 5.49 | 115.46 | 9 | 100% |
| 50,000 | 1366.40 | 5.80 | 126.79 | 10 | 100% |

---

## 4.7 Travel Time Impact

Case 2-1 (Yeosu) has the longest travel time among all cases:

| Case | Travel Time (one-way) | Round Trip | Impact |
|------|----------------------|------------|--------|
| Case 1 | 1.0 hr | 2.0 hr | Baseline |
| Case 2-2 | 1.67 hr | 3.34 hr | +67% |
| **Case 2-1** | **5.73 hr** | **11.46 hr** | **+473%** |

This explains why Case 2-1 has the highest NPC and LCOAmmonia among all cases.

---

## 4.8 Verification Summary

| Item | Expected | CSV Result | Status |
|------|----------|------------|--------|
| Optimal Shuttle | 10,000 m3 | 10,000 m3 (min NPC) | [PASS] |
| Cycle Time (5000) | 24.7933 hr | 24.7933 hr | [PASS] |
| Cycle Time (10000) | 36.1267 hr | 36.1267 hr | [PASS] |
| Cycle Time (15000) | 47.46 hr | 47.46 hr | [PASS] |
| Vessels/Trip (10000) | 2 | 2.0 | [PASS] |
| Annuity Factor | 10.8355 | 10.8355 | [PASS] |
| NPC (10000) | ~$747M | $747.18M | [PASS] |
| LCO (10000) | ~$3.17/ton | $3.17/ton | [PASS] |
