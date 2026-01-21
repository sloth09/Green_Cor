# Fleet Sizing Analysis: 5000m³ vs 2500m³ Shuttle Comparison

## Executive Summary

This document explains why a **2500m³ shuttle requires 38% more vessels** (11 vs 8) than a 5000m³ shuttle in 2050, despite having half the capacity. The key insight is that **smaller shuttles require more round-trips per vessel call**, leading to disproportionately higher total operating hours.

---

## 1. Correct Fleet Sizing Formula

### Working Time Constraint (Currently Used)

```python
required_shuttles = ceil(total_hours_needed / max_annual_hours)

where:
  total_hours_needed = annual_calls × trips_per_call × cycle_duration
  max_annual_hours = 8,000 hours/year
```

**This is the ONLY constraint currently active** in `yearly_simulation` mode.

### Daily Peak Constraint (Available but Not Used)

```python
required_shuttles_peak = ceil(daily_demand_with_peak / daily_capacity_per_shuttle)

where:
  daily_demand_with_peak = (annual_calls / 365) × bunker_volume × daily_peak_factor
  daily_capacity_per_shuttle = (8000 / cycle_duration / 365) × shuttle_size
  daily_peak_factor = 1.5 (from config)
```

**Note:** This constraint is implemented in `FleetSizingCalculator.calculate_required_shuttles_with_daily_peak()` but is **NOT used** in `yearly_simulation` mode. Only the optimizer uses it.

---

## 2. 2050 Detailed Comparison

### Input Parameters (Same for Both)

| Parameter | Value |
|-----------|-------|
| Vessels in operation | 500 |
| Voyages per vessel per year | 12 |
| Bunker volume per call | 5,000 m³ |
| **Annual demand** | **30,000,000 m³** |
| **Annual calls** | **6,000** |
| Pump flow rate | 2,000 m³/h |
| Max annual hours | 8,000 h |

---

### Configuration A: 5000m³ Shuttle

#### Cycle Time Breakdown
```
Shore Loading:        5000 / 1500 = 3.33 hours
Travel Outbound:                    1.00 hours
Setup (connect):                    1.00 hours
Pumping:              5000 / 2000 = 2.50 hours
Setup (disconnect):                 1.00 hours
Travel Return:                      1.00 hours
─────────────────────────────────────────────
Total Cycle:                        9.83 hours
```

#### Fleet Sizing Calculation
```
Trips_Per_Call:       ceil(5000 / 5000) = 1 trip
Annual_Cycles:        6,000 × 1 = 6,000 trips
Total_Hours_Needed:   6,000 × 9.83 = 58,980 hours
Required_Shuttles:    ceil(58,980 / 8,000) = 8 shuttles ✓
```

#### Efficiency Metrics
```
Hours_Per_Shuttle:    58,980 / 8 = 7,373 hours/year
Utilization_Rate:     58,980 / 64,000 = 92.2%
Cycles_Per_Shuttle:   6,000 / 8 = 750 trips/year
```

---

### Configuration B: 2500m³ Shuttle

#### Cycle Time Breakdown
```
Shore Loading:        2500 / 1500 = 1.67 hours
Travel Outbound:                    1.00 hours
Setup (connect):                    1.00 hours
Pumping:              2500 / 2000 = 1.25 hours
Setup (disconnect):                 1.00 hours
Travel Return:                      1.00 hours
─────────────────────────────────────────────
Total Cycle:                        6.92 hours
```

#### Fleet Sizing Calculation
```
Trips_Per_Call:       ceil(5000 / 2500) = 2 trips
Annual_Cycles:        6,000 × 2 = 12,000 trips
Total_Hours_Needed:   12,000 × 6.92 = 83,040 hours
Required_Shuttles:    ceil(83,040 / 8,000) = 11 shuttles ✓
```

#### Efficiency Metrics
```
Hours_Per_Shuttle:    83,040 / 11 = 7,549 hours/year
Utilization_Rate:     83,040 / 88,000 = 94.4%
Cycles_Per_Shuttle:   12,000 / 11 = 1,091 trips/year
```

---

## 3. Why 2500m³ Requires More Shuttles

### The Non-Linear Relationship

| Metric | 5000m³ | 2500m³ | Ratio |
|--------|--------|--------|-------|
| Shuttle Capacity | 5,000 m³ | 2,500 m³ | **0.5x** |
| Trips Per Call | 1 | 2 | **2.0x** |
| Cycle Duration | 9.83 h | 6.92 h | **0.70x** |
| Annual Cycles | 6,000 | 12,000 | **2.0x** |
| **Total Hours** | **58,980 h** | **83,040 h** | **1.41x** ⚠️ |
| **Required Shuttles** | **8** | **11** | **1.38x** ⚠️ |

### Key Insight

**The problem:** While the shuttle is 50% smaller, the cycle time is only 70% (not 50%), because:

1. **Fixed time components don't scale:**
   - Travel time: 2.0 hours (same for both)
   - Setup time: 2.0 hours (same for both)
   - **Total fixed: 4.0 hours** (41% of 5000m³ cycle, 58% of 2500m³ cycle)

2. **Variable time components scale linearly:**
   - Shore loading: 3.33h → 1.67h (50% reduction ✓)
   - Pumping: 2.50h → 1.25h (50% reduction ✓)

3. **But you need 2x more trips:**
   - Time per vessel call: 9.83h → 13.84h (41% **increase**!)

**Formula:**
```
Total_Hours = Annual_Calls × Trips_Per_Call × Cycle_Duration
            = 6,000 × 2 × 6.92
            = 83,040 hours (vs 58,980 for 5000m³)
            = 41% more hours needed!
```

---

## 4. Cost Implications

### CAPEX Impact (2050)

| Cost Component | 5000m³ (8 shuttles) | 2500m³ (11 shuttles) | Difference |
|----------------|---------------------|----------------------|------------|
| Shuttle CAPEX | 8 × $12.9M = $103.4M | 11 × $8.1M = $89.1M | -14% |
| Pump CAPEX | 8 × $1.0M = $8.2M | 11 × $1.0M = $11.2M | +37% |
| **Total CAPEX** | **$111.6M** | **$100.3M** | **-10%** ✓ |

**Note:** 2500m³ shuttle has lower unit CAPEX due to scaling exponent (0.75), so despite needing more vessels, total CAPEX is actually **lower**.

### OPEX Impact (Annual, 2050)

| Cost Component | 5000m³ | 2500m³ | Difference |
|----------------|--------|--------|------------|
| Fixed OPEX | 8 × $0.70M = $5.6M | 11 × $0.44M = $4.8M | -14% |
| Shuttle Fuel | 6,000 cycles × cost | 12,000 cycles × cost | **+100%** ⚠️ |
| Pump Energy | 6,000 calls × cost | 6,000 calls × cost | Same |
| **Total OPEX** | **Higher fixed, lower fuel** | **Lower fixed, higher fuel** | **Depends on fuel price** |

**Critical:** Variable OPEX (fuel) is proportional to `Annual_Cycles`, so 2500m³ has **double the shuttle fuel cost**.

---

## 5. Verification Checklist

### Excel Formulas for CSV Validation

Open `yearly_simulation_case_1_XXXX_2000_*.csv` and verify 2050 row:

```excel
# Column calculations (assuming row 21 is 2050)
=Q21 * R21                    # Annual_Cycles = Annual_Calls × Trips_Per_Call
=S21 * G21                    # Total_Hours_Needed = Annual_Cycles × Cycle_Duration
=CEILING(V21/8000, 1)         # Total_Shuttles = ceil(Total_Hours_Needed / 8000)
=V21 / W21                    # Utilization_Rate = Total_Hours_Needed / Total_Hours_Available
=S21 / F21                    # Cycles_Per_Shuttle = Annual_Cycles / Total_Shuttles
```

### Expected Values (2050)

#### 5000m³ Shuttle + 2000m³/h Pump

| Column | Expected Value | Verification |
|--------|----------------|--------------|
| Annual_Calls | 6000.0 | 30M / 5000 |
| Trips_Per_Call | 1.0 | ceil(5000/5000) |
| Annual_Cycles | 6000 | 6000 × 1 |
| Cycle_Duration_Hours | 9.83 | Sum of components |
| Total_Hours_Needed | 58980 | 6000 × 9.83 |
| Total_Shuttles | 8 | ceil(58980/8000) |
| Utilization_Rate | 0.9222 | 58980/64000 |

#### 2500m³ Shuttle + 2000m³/h Pump

| Column | Expected Value | Verification |
|--------|----------------|--------------|
| Annual_Calls | 6000.0 | 30M / 5000 |
| Trips_Per_Call | 2.0 | ceil(5000/2500) |
| Annual_Cycles | 12000 | 6000 × 2 |
| Cycle_Duration_Hours | 6.92 | Sum of components |
| Total_Hours_Needed | 83040 | 12000 × 6.92 |
| Total_Shuttles | 11 | ceil(83040/8000) |
| Utilization_Rate | 0.9441 | 83040/88000 |

---

## 6. Column Formatting Verification

### Data Type Check

All columns should be **float64** in pandas, displayed with decimal places in CSV:

```python
import pandas as pd
df = pd.read_csv('results/yearly_simulation_case_1_5000_2000_*.csv')

# Check data types
assert df['Trips_Per_Call'].dtype == 'float64', "Should be float"
assert df['Vessels_Per_Trip'].dtype == 'float64', "Should be float"
assert df['Setup_Total_Hours'].dtype == 'float64', "Should be float"
assert df['Time_Per_Vessel_Call_Hours'].dtype == 'float64', "Should be float"

# Check 2050 values
row_2050 = df[df['Year'] == 2050].iloc[0]
print(f"Trips_Per_Call: {row_2050['Trips_Per_Call']}")  # Should show 1.0 or 2.0, not 1 or 2
```

### CSV Display

In the CSV file, these columns should appear as:
```
Trips_Per_Call,Vessels_Per_Trip,Setup_Total_Hours,Time_Per_Vessel_Call_Hours
1.0,1.0,2.0,9.83
```

**Not as:**
```
Trips_Per_Call,Vessels_Per_Trip,Setup_Total_Hours,Time_Per_Vessel_Call_Hours
1,1,2,9.83
```

---

## 7. Conclusion

### Summary

- **5000m³ shuttle** is more efficient for high-demand scenarios (2050)
  - Fewer total operating hours (58,980 vs 83,040)
  - Fewer vessels needed (8 vs 11)
  - Lower variable OPEX (fuel costs)
  - Higher utilization per vessel (92.2% vs 94.4%)

- **2500m³ shuttle** has advantages in:
  - Lower total CAPEX (smaller unit cost × more vessels = still cheaper)
  - Lower fixed OPEX per vessel
  - Better for early years (2030-2035) when demand is low

### Recommendation

For **Case 1 (Busan Port Storage)**, the optimal shuttle size depends on:
1. **Fuel price sensitivity:** High fuel costs favor larger shuttles
2. **Demand profile:** Low initial demand favors smaller shuttles
3. **Fleet flexibility:** Smaller shuttles provide better scalability

The optimizer should evaluate both options across all years to find the true minimum NPC.
