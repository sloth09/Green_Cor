# Chapter 5: Case 2-2 - Ulsan to Busan

## 5.1 Overview

| Parameter | Value |
|-----------|-------|
| Case ID | case_2_ulsan |
| Storage at Busan | **No** |
| Route | Ulsan to Busan |
| Distance | 25 nautical miles |
| Travel Time (one-way) | 1.67 hours (25 nm / 15 knots) |
| Bunker Volume per Call | 5,000 m3 |
| Optimal Shuttle Size | **5,000 m3** |

---

## 5.2 Cycle Time Calculation

### 5.2.1 Formula (Case 2 - Direct Supply)

Same formula as Case 2-1, but with shorter travel time:

```
Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)

Cycle_Duration = Shore_Loading + Travel_Out + Travel_Return + Port_Entry_Exit
               + (Vessels_per_Trip × (Movement + Setup + Pumping))

where:
  Shore_Loading = Shuttle_Size / 1500
  Travel_Out = 1.67 hours (25 nm / 15 knots)
  Travel_Return = 1.67 hours
  Port_Entry_Exit = 2.0 hours
  Per_Vessel = 1.0 + 2.0 + 5.0 = 8.0 hours
```

### 5.2.2 Example: 5,000 m3 Shuttle (Optimal)

**Step 1: Vessels per Trip**
```
Vessels_per_Trip = floor(5000 / 5000) = 1 vessel
```

**Step 2: Fixed Components**
```
Shore_Loading = 5000 / 1500 = 3.3333 hours
Travel_Out = 1.67 hours
Travel_Return = 1.67 hours
Port_Entry_Exit = 2.0 hours

Fixed_Time = 3.3333 + 1.67 + 1.67 + 2.0 = 8.6733 hours
```

**Step 3: Per-Vessel Components**
```
Total_Vessel_Time = 1 vessel × 8.0 hours = 8.0 hours
```

**Step 4: Total Cycle Duration**
```
Cycle_Duration = 8.6733 + 8.0 = 16.6733 hours
```

**CSV Verification**: `Cycle_Duration_hr = 16.6733` [PASS]

### 5.2.3 Example: 2,500 m3 Shuttle

**Step 1: Vessels per Trip**
```
Vessels_per_Trip = floor(2500 / 5000) = 0 vessels
→ Treated as 1 vessel (partial delivery)
Note: Trips_per_Call = 2 (two trips to complete one bunkering call)
```

**Step 2: Fixed Components**
```
Shore_Loading = 2500 / 1500 = 1.6667 hours
Travel_Out = 1.67 hours
Travel_Return = 1.67 hours
Port_Entry_Exit = 2.0 hours

Fixed_Time = 1.6667 + 1.67 + 1.67 + 2.0 = 7.0067 hours
```

**Step 3: Per-Vessel Components**
```
Total_Vessel_Time = 1 × 8.0 hours = 8.0 hours
```

**Step 4: Total Cycle Duration**
```
Cycle_Duration = 7.0067 + 8.0 = 15.0067 hours
```

**CSV Verification**: `Cycle_Duration_hr = 15.0067` [PASS]

### 5.2.4 Example: 10,000 m3 Shuttle

**Step 1: Vessels per Trip**
```
Vessels_per_Trip = floor(10000 / 5000) = 2 vessels
```

**Step 2: Fixed Components**
```
Shore_Loading = 10000 / 1500 = 6.6667 hours
Travel_Out = 1.67 hours
Travel_Return = 1.67 hours
Port_Entry_Exit = 2.0 hours

Fixed_Time = 6.6667 + 1.67 + 1.67 + 2.0 = 12.0067 hours
```

**Step 3: Per-Vessel Components**
```
Total_Vessel_Time = 2 vessels × 8.0 hours = 16.0 hours
```

**Step 4: Total Cycle Duration**
```
Cycle_Duration = 12.0067 + 16.0 = 28.0067 hours
```

**CSV Verification**: `Cycle_Duration_hr = 28.0067` [PASS]

---

## 5.3 Annual Capacity Calculation

### 5.3.1 Verification Table

| Shuttle (m3) | Vessels/Trip | Cycle (hr) | Annual Cycles | Ships/Year | CSV Match |
|-------------|--------------|------------|---------------|------------|-----------|
| 2,500 | 1 | 15.01 | 533.10 | 266.55 | [PASS] |
| 5,000 | 1 | 16.67 | 479.81 | 479.81 | [PASS] |
| 10,000 | 2 | 28.01 | 285.65 | 571.29 | [PASS] |

---

## 5.4 Cost Verification

### 5.4.1 Shuttle CAPEX

| Shuttle (m3) | CAPEX | Annualized CAPEX/yr |
|-------------|-------|---------------------|
| 2,500 | $7,761,316 | $716,345 |
| 5,000 | $13,051,896 | $1,204,496 |
| 10,000 | $21,951,652 | $2,026,087 |

---

## 5.5 Shuttle Size Comparison

### 5.5.1 Comparison Table (1000 m3/h Pump)

| Metric | 2,500 m3 | 5,000 m3 | 10,000 m3 |
|--------|----------|----------|-----------|
| **NPC Total** | $487.48M | **$402.37M** | $495.93M |
| **LCOAmmonia** | $2.07/ton | **$1.71/ton** | $2.10/ton |
| Cycle Duration | 15.01 hr | 16.67 hr | 28.01 hr |
| Vessels per Trip | 1 | 1 | 2 |
| Annual Cycles | 533.10 | 479.81 | 285.65 |
| Ships per Year | 266.55 | 479.81 | 571.29 |
| Time Utilization | 100% | 100% | 100% |

### 5.5.2 Cost Breakdown Comparison

| Cost Component | 2,500 m3 | 5,000 m3 | 10,000 m3 |
|---------------|----------|----------|-----------|
| Annualized Shuttle CAPEX | $193.69M | $184.94M | $264.88M |
| Annualized Bunkering CAPEX | $13.81M | $10.09M | $11.81M |
| Shuttle Fixed OPEX | $104.93M | $100.20M | $143.51M |
| Bunkering Fixed OPEX | $7.48M | $5.47M | $6.40M |
| Shuttle Variable OPEX | $155.06M | $89.16M | $56.82M |
| Bunkering Variable OPEX | $12.51M | $12.51M | $12.51M |
| **NPC Total** | **$487.48M** | **$402.37M** | **$495.93M** |

### 5.5.3 Why 5,000 m3 is Optimal

1. **Perfect match**: 5,000 m3 shuttle = 5,000 m3 bunker demand per call
2. **Single trip efficiency**: No wasted capacity, no multiple trips
3. **Short distance advantage**: 1.67 hr travel offsets smaller shuttle CAPEX benefit
4. **Lower variable OPEX**: $89.16M vs $155.06M (2,500) or $56.82M (10,000)

The 2,500 m3 shuttle requires 2 trips per call, doubling travel time impact.
The 10,000 m3 shuttle has higher CAPEX and longer cycle time (28 hr) with diminishing returns.

---

## 5.6 Full Scenario Results

| Shuttle (m3) | NPC (M$) | LCO ($/ton) | Cycle (hr) | Vessels/Trip | Utilization |
|-------------|----------|-------------|------------|--------------|-------------|
| 2,500 | 487.48 | 2.07 | 15.01 | 1 | 100% |
| **5,000** | **402.37** | **1.71** | **16.67** | **1** | 100% |
| 10,000 | 495.93 | 2.10 | 28.01 | 2 | 100% |
| 15,000 | 592.93 | 2.52 | 39.34 | 3 | 100% |
| 20,000 | 697.25 | 2.96 | 50.67 | 4 | 100% |
| 25,000 | 796.83 | 3.38 | 62.01 | 5 | 100% |
| 30,000 | 888.32 | 3.77 | 73.34 | 6 | 100% |
| 35,000 | 980.81 | 4.16 | 84.67 | 7 | 100% |
| 40,000 | 1068.50 | 4.53 | 96.01 | 8 | 100% |
| 45,000 | 1151.88 | 4.89 | 107.34 | 9 | 100% |
| 50,000 | 1242.02 | 5.27 | 118.67 | 10 | 100% |

---

## 5.7 Comparison with Case 2-1 (Yeosu)

| Metric | Case 2-1 (Yeosu) | Case 2-2 (Ulsan) | Difference |
|--------|-----------------|------------------|------------|
| Distance | 86 nm | 25 nm | -71% |
| Travel Time | 5.73 hr | 1.67 hr | -71% |
| Optimal Shuttle | 10,000 m3 | 5,000 m3 | -50% |
| Optimal NPC | $747.18M | $402.37M | -46% |
| Optimal LCO | $3.17/ton | $1.71/ton | -46% |

**Key Insight**: Shorter distance (Ulsan) enables smaller, more efficient shuttles and significantly lower costs.

---

## 5.8 Verification Summary

| Item | Expected | CSV Result | Status |
|------|----------|------------|--------|
| Optimal Shuttle | 5,000 m3 | 5,000 m3 (min NPC) | [PASS] |
| Cycle Time (2500) | 15.0067 hr | 15.0067 hr | [PASS] |
| Cycle Time (5000) | 16.6733 hr | 16.6733 hr | [PASS] |
| Cycle Time (10000) | 28.0067 hr | 28.0067 hr | [PASS] |
| Vessels/Trip (5000) | 1 | 1.0 | [PASS] |
| Annuity Factor | 10.8355 | 10.8355 | [PASS] |
| NPC (5000) | ~$402M | $402.37M | [PASS] |
| LCO (5000) | ~$1.71/ton | $1.71/ton | [PASS] |
