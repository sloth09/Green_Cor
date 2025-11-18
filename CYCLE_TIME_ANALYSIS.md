# Cycle Time Calculation Structure - Detailed Analysis

## Executive Summary

The codebase implements a **3-Layer Architecture** for cycle time calculation:

1. **Layer 1 (Core Library)**: `ShuttleRoundTripCalculator` - Basic shuttle round-trip logic
2. **Layer 2 (Integration)**: `CycleTimeCalculator` - Core + Shore supply integration
3. **Layer 3 (Optimization)**: `BunkeringOptimizer` - Optimization constraints and reporting

---

## 1. WHERE CYCLE TIME IS CALCULATED

### Core Calculation Files

#### File: `/home/user/Green_Cor/src/shuttle_round_trip_calculator.py`
**Purpose**: Fundamental time calculation logic applying equally to all cases (Case 1, 2-1, 2-2)

**Key Method**: `ShuttleRoundTripCalculator.calculate()` (Lines 42-132)
- **Input Parameters**:
  - `shuttle_size_m3`: Shuttle capacity
  - `pump_size_m3ph`: Bunkering pump flow rate
  - `bunker_volume_per_call_m3`: Volume per vessel call (5000 m³)
  - `num_vessels`: Number of vessels per round-trip
  - `is_round_trip`: Boolean flag for return travel

**Calculated Components** (Returns dict):
```python
{
    'travel_outbound_h': float,           # One-way travel time
    'travel_return_h': float,             # Return travel time (0 if not round-trip)
    'setup_inbound_h': float,             # Connection/venting at destination
    'setup_outbound_h': float,            # Disconnection/venting at destination
    'pumping_per_vessel_h': float,        # Pumping time per individual vessel
    'pumping_total_h': float,             # Total pumping for all vessels
    'basic_cycle_duration_h': float,      # Complete cycle (before shore loading)
    'trips_per_call': int,                # Shuttle trips needed per demand call
    'vessels_per_trip': int,              # Vessels served per trip
}
```

#### File: `/home/user/Green_Cor/src/cycle_time_calculator.py`
**Purpose**: Integrates ShuttleRoundTripCalculator with shore supply and final metrics

**Key Method**: `CycleTimeCalculator.calculate_single_cycle()` (Lines 64-143)
- **Wrapper around ShuttleRoundTripCalculator**
- **Adds Shore Supply Module**: Calculates shore loading time
- **Returns**: Complete breakdown including shore_loading and cycle_duration

**Key Output Fields**:
```python
{
    'shore_loading': float,               # Shore supply loading time (m³/1500)
    'basic_cycle_duration': float,        # Basic shuttle round-trip
    'cycle_duration': float,              # Total with shore loading
    'call_duration': float,               # Time to fulfill one demand call
    'trips_per_call': int,
    'vessels_per_trip': int,
    'case_type': str,                     # "case_1", "case_2_ulsan", "case_2_yeosu"
    'has_storage_at_busan': bool,
}
```

#### File: `/home/user/Green_Cor/src/shore_supply.py`
**Purpose**: Manages shore facility loading/unloading operations

**Key Method**: `ShoreSupply.load_shuttle()` (Lines 53-74)
```python
# Formula: loading_time = (shuttle_size / pump_rate) + fixed_time
# Default pump rate: 1,500 m³/h (fixed)
```

#### File: `/home/user/Green_Cor/src/optimizer.py`
**Purpose**: Uses cycle time in MILP optimization

**Key Usage** (Lines 179-184):
```python
cycle_info = self.cycle_calc.calculate_single_cycle(shuttle_size, pump_size, num_vessels)
call_duration = cycle_info["call_duration"]
cycle_duration = cycle_info["cycle_duration"]
trips_per_call = cycle_info["trips_per_call"]
```

---

## 2. KEY TIME COMPONENTS

### Time Breakdown (All Cases)

| Component | Calculation | Where Used |
|-----------|-------------|-----------|
| **Shore Loading** | `shuttle_size / 1500` hours | `shore_supply.py:73` |
| **Travel Outbound** | Case-specific (1.0-5.73 hours) | `config/*.yaml` |
| **Setup Inbound** | `2 × setup_time` (typically 1.0h) | `shuttle_round_trip_calculator.py:86` |
| **Pumping per Vessel** | `bunker_volume_per_call / pump_rate` | `shuttle_round_trip_calculator.py:90` |
| **Pumping Total** | `pumping_per_vessel × num_vessels` | `shuttle_round_trip_calculator.py:93` |
| **Movement per Vessel** | Fixed 1.0 hour | `shuttle_round_trip_calculator.py:96` |
| **Setup Outbound** | `2 × setup_time` (typically 1.0h) | `shuttle_round_trip_calculator.py:87` |
| **Travel Return** | Case-specific (0-5.73 hours) | `config/*.yaml` |

### Formula for Complete Cycle

```
cycle_duration = shore_loading + basic_cycle_duration
basic_cycle_duration = travel_outbound + time_all_vessels_at_destination + travel_return
time_all_vessels_at_destination = (movement + setup_inbound + pumping_per_vessel + setup_outbound) × num_vessels
```

### Example: Case 1 with 5,000 m³ shuttle, 1,000 m³/h pump

```
Shore Loading:              5000 / 1500 = 3.33 hours
Travel Outbound:            2.0 hours
Movement (per vessel):      1.0 hour
Setup Inbound:              2 × 0.5 = 1.0 hour
Pumping (per vessel):       5000 / 1000 = 5.0 hours
Setup Outbound:             2 × 0.5 = 1.0 hour
Travel Return:              2.0 hours
────────────────────────────────────────
Basic Cycle:                2 + (1 + 1 + 5 + 1) + 2 = 12.0 hours
Cycle Duration:             3.33 + 12.0 = 15.33 hours
Call Duration:              trips_per_call × basic_cycle = 1 × 12 = 12.0 hours
Annual Operations/Shuttle:  8000 / 15.33 ≈ 522 cycles
```

---

## 3. CASE-SPECIFIC TIME CALCULATIONS

### Case 1: Busan Port with Storage

**Configuration File**: `/home/user/Green_Cor/config/case_1.yaml`

| Parameter | Value | Source |
|-----------|-------|--------|
| **Travel Time (one-way)** | 2.0 hours | `case_1.yaml:44` |
| **Setup Time** | 0.5 hours each | `base.yaml:38` |
| **Has Storage at Busan** | `True` | `case_1.yaml:47` |
| **Shore Pump Rate** | 1,500 m³/h | `shore_supply.py:22` (fixed) |
| **Bunker Volume per Call** | 5,000 m³ | `case_1.yaml:64` |
| **Shuttle Sizes** | 500-5,000 m³ | `case_1.yaml:15-25` |

**Key Characteristics**:
- Small shuttle sizes (need multiple trips for 5,000 m³ call)
- Short travel time within Busan port
- trips_per_call = ceil(5000 / shuttle_size)
- Example: 500 m³ shuttle → 10 trips; 5,000 m³ shuttle → 1 trip

### Case 2-2: Ulsan → Busan (Short Distance)

**Configuration File**: `/home/user/Green_Cor/config/case_2_ulsan.yaml`

| Parameter | Value | Source |
|-----------|-------|--------|
| **Travel Time (one-way)** | 1.67 hours | `case_2_ulsan.yaml:55` |
| **Calculation** | 25 nm ÷ 15 knots | `case_2_ulsan.yaml:18-19` |
| **Setup Time** | 0.5 hours each | `base.yaml:38` |
| **Has Storage at Busan** | `False` | `case_2_ulsan.yaml:58` |
| **Shore Pump Rate** | 1,500 m³/h | (fixed) |
| **Bunker Volume per Call** | 5,000 m³ | `case_2_ulsan.yaml:69` |
| **Shuttle Sizes** | 5,000-50,000 m³ | `case_2_ulsan.yaml:26-36` |

**Key Characteristics**:
- Large shuttle sizes (each serves multiple vessels)
- Short voyage distance
- num_vessels = floor(shuttle_size / 5000)
- trips_per_call = 1 (one complete delivery per trip)
- Example: 25,000 m³ shuttle → 5 vessels per trip

### Case 2-1: Yeosu → Busan (Long Distance)

**Configuration File**: `/home/user/Green_Cor/config/case_2_yeosu.yaml`

| Parameter | Value | Source |
|-----------|-------|--------|
| **Travel Time (one-way)** | 5.73 hours | `case_2_yeosu.yaml:55` |
| **Calculation** | 86 nm ÷ 15 knots | `case_2_yeosu.yaml:18-19` |
| **Setup Time** | 0.5 hours each | `base.yaml:38` |
| **Has Storage at Busan** | `False` | `case_2_yeosu.yaml:58` |
| **Shore Pump Rate** | 1,500 m³/h | (fixed) |
| **Bunker Volume per Call** | 5,000 m³ | `case_2_yeosu.yaml:69` |
| **Shuttle Sizes** | 5,000-50,000 m³ | `case_2_yeosu.yaml:26-36` |

**Key Characteristics**:
- Same shuttle sizes as Case 2-2
- Long voyage distance (significantly slower)
- Same vessels_per_trip calculation
- Much longer cycle duration due to travel time

### Comparison: Case 2-2 vs Case 2-1

**Example: 25,000 m³ Shuttle, 1,000 m³/h Pump, 5 Vessels**

| Component | Case 2-2 (Ulsan) | Case 2-1 (Yeosu) | Difference |
|-----------|-----------------|-----------------|-----------|
| Shore Loading | 16.67h | 16.67h | 0h |
| Travel Outbound | 1.67h | 5.73h | 4.06h |
| Vessel Service Time | 40h (5×8h) | 40h (5×8h) | 0h |
| Travel Return | 1.67h | 5.73h | 4.06h |
| **Basic Cycle** | ~59.3h | ~68.1h | **8.8h slower** |
| **Cycle Duration** | ~76.0h | ~84.8h | **8.8h slower** |
| **Annual Trips** | 8000/76 ≈ 105 | 8000/84.8 ≈ 94 | **11 fewer trips** |

---

## 4. WHERE CYCLE TIME IS USED

### In Optimizer (`/home/user/Green_Cor/src/optimizer.py`)

#### 1. **Pre-screening Check** (Line 187)
```python
if call_duration > self.max_call_hours:
    return  # Skip infeasible combination
# Constraint: call_duration <= 72 hours (from config base.yaml:79)
```

#### 2. **Working Time Capacity Constraint** (Line 278)
```python
prob += y[t] * trips_per_call * cycle_duration <= N[t] * self.max_annual_hours
# Formula: Annual_Calls × Trips_per_Call × Cycle_Duration <= Shuttles × 8000 hours
```

#### 3. **Daily Peak Demand Constraint** (Line 292)
```python
daily_capacity = (N[t] * (self.max_annual_hours / cycle_duration) / 365.0) * shuttle_size
# Formula: Capacity = Shuttles × (8000 / cycle_duration) / 365 × shuttle_size
```

#### 4. **Fuel Cost Calculation** (Lines 193-207)
```python
# Shuttle fuel cost based on travel time and cycle count
shuttle_fuel_per_cycle = (mcr * self.sfoc * travel_factor * self.travel_time_hours) / 1e6
cycles = y[t] * trips_per_call  # Uses trips_per_call from cycle_info

# Pump fuel cost based on pumping time
if self.has_storage_at_busan:
    pumping_time_hr_call = 2.0 * (self.bunker_volume_per_call_m3 / pump_size)
else:
    pumping_time_hr_call = 2.0 * (shuttle_size / pump_size)
```

#### 5. **Annualized Metrics** (Lines 446, 492-496)
```python
cycles_avail = N_val * (self.max_annual_hours / cycle_duration) if N_val > 0 else 0
Annual_Cycles = round(cycles, 4)
Cycles_Available = round(cycles_avail, 4)
Utilization_Rate = round((cycles / cycles_avail) if cycles_avail > 0 else 0, 6)
```

---

## 5. CURRENT CYCLE TIME REPORTING

### Output Files

#### CSV: `MILP_scenario_summary_{case_id}.csv`
**File Written**: `optimizer.py:_extract_results()` Lines 403-433

**Cycle Time Columns**:
```
"Shuttle_Size_cbm"        - Shuttle capacity
"Pump_Size_m3ph"          - Pump flow rate
"Call_Duration_hr"        - Time to fulfill one complete 5,000 m³ call
"Cycle_Duration_hr"       - Time for one complete shuttle round-trip cycle
"Trips_per_Call"          - Number of shuttle trips per demand call
```

#### CSV: `MILP_per_year_results_{case_id}.csv`
**File Written**: `optimizer.py:_extract_results()` Lines 436-517

**Cycle Time-Related Columns**:
```
"Annual_Calls"            - Number of annual demand calls (y[t])
"Annual_Cycles"           - cycles = Annual_Calls × Trips_per_Call
"Cycles_Available"        - Capacity cycles per shuttle per year (8000 / cycle_duration)
"Utilization_Rate"        - Actual_Cycles / Available_Cycles
```

### Example Output (Case 1, 5000m³ shuttle, 1000 m³/h pump)

```
Shuttle_Size_cbm: 5000
Pump_Size_m3ph: 1000
Call_Duration_hr: 12.0000
Cycle_Duration_hr: 15.3333
Trips_per_Call: 1
```

Per-year example:
```
Year: 2030
Annual_Calls: 382
Annual_Cycles: 382
Cycles_Available: 522
Utilization_Rate: 0.732
```

---

## 6. CONFIGURATION PARAMETERS (Time-Related)

### Base Configuration (`/home/user/Green_Cor/config/base.yaml`)

```yaml
operations:
  max_annual_hours_per_vessel: 8000.0  # Line 37 - Annual operational availability
  setup_time_hours: 0.5                # Line 38 - Hose connection/disconnection
  tank_safety_factor: 2.0              # Line 39 - Not time-related
  daily_peak_factor: 1.5               # Line 40 - Not time-related

shore_supply:  # Implicit, defined in shore_supply.py
  pump_rate_m3ph: 1500.0               # shore_supply.py:22
  enabled: true                        # Default

constraints:
  max_call_duration_hours: 72.0        # Line 79 - Maximum bunkering call duration
```

### Case-Specific (`config/case_X.yaml`)

**Case 1**:
```yaml
operations:
  travel_time_hours: 2.0               # One-way port travel
  has_storage_at_busan: true
```

**Case 2-2 (Ulsan)**:
```yaml
operations:
  travel_time_hours: 1.67              # 25 nm ÷ 15 knots
  has_storage_at_busan: false
```

**Case 2-1 (Yeosu)**:
```yaml
operations:
  travel_time_hours: 5.73              # 86 nm ÷ 15 knots
  has_storage_at_busan: false
```

---

## 7. KEY CALCULATIONS SUMMARY

### Cycle Time Formula by Case

**Case 1** (Small shuttles, multiple trips):
```
basic_cycle = 2×travel_time + movement + 2×setup + pumping_per_vessel
call_duration = trips_per_call × basic_cycle
cycle_duration = (shuttle_size / 1500) + basic_cycle
```

**Case 2** (Large shuttles, multiple vessels):
```
basic_cycle = 2×travel_time + (movement + 2×setup + pumping_per_vessel) × num_vessels
call_duration = 1 × basic_cycle  (always 1 trip)
cycle_duration = (shuttle_size / 1500) + basic_cycle
```

### Constraint Use

| Constraint | Equation | File:Line |
|-----------|----------|-----------|
| **Call Duration Feasibility** | call_duration ≤ 72h | `optimizer.py:187` |
| **Working Capacity** | y[t] × trips × cycle_duration ≤ N[t] × 8000 | `optimizer.py:278` |
| **Daily Peak** | daily_demand × F_peak ≤ daily_capacity | `optimizer.py:293` |

---

## 8. CODE FLOW DIAGRAM

```
ConfigLoader (load_config)
    ↓
BunkeringOptimizer.__init__()
    ├── CycleTimeCalculator.__init__()
    │   └── ShuttleRoundTripCalculator.__init__()
    └── ShoreSupply.__init__()
    ↓
BunkeringOptimizer.solve()
    ├── For each shuttle_size, pump_size:
    │   ├── _solve_combination()
    │   │   ├── cycle_calc.calculate_single_cycle()
    │   │   │   ├── shuttle_calc.calculate()  [Core logic]
    │   │   │   ├── shore_supply.load_shuttle()
    │   │   │   └── Return: cycle_info dict
    │   │   ├── Check call_duration ≤ 72h
    │   │   ├── Build MILP with constraints using cycle_duration
    │   │   ├── Solve and extract results
    │   │   └── _extract_results()
    │   │       └── Append to scenario_results, yearly_results
    │   └── Print progress
    ├── Convert to DataFrames
    └── Return (scenario_df, yearly_df)
    ↓
main.run_single_case()
    ├── Export to CSV
    ├── Export to Excel (if enabled)
    └── Export to Word (if enabled)
```

---

## 9. TEST COVERAGE

### Test File: `tests/test_shuttle_round_trip_calculator.py`
- Tests core library logic (same for all cases)
- Validates time component calculations
- Verifies trips_per_call and vessels_per_trip

### Test File: `tests/test_cycle_time_calculator.py`
- Tests integration with shore supply
- Case-specific validation (Case 1, 2-1, 2-2)
- Validates complete cycle_duration calculation
- Example: `test_single_cycle_5000m3_1000m3ph()` Line 83

---

## 10. QUICK REFERENCE

### To Change Cycle Time Calculation
1. **Travel Time**: Modify `config/case_X.yaml` → `operations.travel_time_hours`
2. **Setup Time**: Modify `config/base.yaml` → `operations.setup_time_hours`
3. **Shore Pump Rate**: Modify `src/shore_supply.py` → `STANDARD_PUMP_RATE_M3PH` (currently 1500)
4. **Bunker Volume**: Modify `config/case_X.yaml` → `bunkering.bunker_volume_per_call_m3`
5. **Call Duration Limit**: Modify `config/base.yaml` → `constraints.max_call_duration_hours`

### To Use Cycle Time Results
- **CSV Results**: Read `Cycle_Duration_hr` and `Call_Duration_hr` columns
- **Annual Operations**: Divide 8,000 hours by `Cycle_Duration_hr`
- **Utilization**: `Annual_Cycles / Cycles_Available` (already calculated in yearly_results)

---

## Attachment A: Complete Time Calculation Example

**Input**:
- Case: Case 2-2 (Ulsan)
- Shuttle Size: 25,000 m³
- Pump Rate: 1,000 m³/h
- Number of Vessels: 5 (calculated as 25000 / 5000)

**Step-by-Step Calculation**:

1. **ShuttleRoundTripCalculator.calculate()**:
   ```
   travel_outbound = 1.67h
   travel_return = 1.67h
   setup_inbound = 2 × 0.5 = 1.0h
   setup_outbound = 2 × 0.5 = 1.0h
   pumping_per_vessel = 5000 / 1000 = 5.0h
   pumping_total = 5.0 × 5 = 25.0h
   movement_per_vessel = 1.0h
   
   time_per_vessel = 1.0 + 1.0 + 5.0 + 1.0 = 8.0h
   time_all_vessels = 8.0 × 5 = 40.0h
   
   basic_cycle_duration = 1.67 + 40.0 + 1.67 = 43.34h
   trips_per_call = 1
   ```

2. **CycleTimeCalculator.calculate_single_cycle()**:
   ```
   shore_loading = 25000 / 1500 = 16.67h
   cycle_duration = 16.67 + 43.34 = 60.01h
   call_duration = 1 × 43.34 = 43.34h
   ```

3. **BunkeringOptimizer Usage**:
   ```
   Check: call_duration (43.34h) ≤ max_call_hours (72h) ✓ PASS
   Working capacity: y[t] × 1 × 60.01 ≤ N[t] × 8000
   Annual cycles per shuttle: 8000 / 60.01 ≈ 133 cycles
   ```

4. **Output**:
   ```
   CSV: Call_Duration_hr = 43.3400
        Cycle_Duration_hr = 60.0100
        Trips_per_Call = 1
   ```

