# Green Corridor Codebase - Non-Unified Calculations Reference

## Issue #1: Pump Fuel Cost Calculation - CRITICAL (2.0 Factor Inconsistency)

### Files Affected
| File | Line(s) | Formula | Status |
|------|---------|---------|--------|
| src/cost_calculator.py | 214 | `2.0 * (bunker_volume_m3 / pump_flow_m3ph)` | **HAS 2.0 FACTOR** |
| src/optimizer.py | 204 | `self.bunker_volume_per_call_m3 / pump_size` | **NO 2.0 FACTOR** |
| main.py | 390 | `bunker_volume / pump_size_m3ph` | **NO 2.0 FACTOR** |

### Code Comparison

**cost_calculator.py (Lines 195-226):**
```python
def calculate_bunkering_fuel_cost_per_call(
    self,
    pump_flow_m3ph: float,
    bunker_volume_m3: float
) -> float:
    # Pumping time = 2 × (load + unload)
    pumping_time_hr = 2.0 * (bunker_volume_m3 / pump_flow_m3ph)  # ← 2.0 FACTOR
    
    delta_pressure = self.config["propulsion"]["pump_delta_pressure_bar"]
    efficiency = self.config["propulsion"]["pump_efficiency"]
    sfoc = self.config["propulsion"]["sfoc_g_per_kwh"]
    fuel_price = self.config["economy"]["fuel_price_usd_per_ton"]
    
    power_kw = calculate_pump_power(pump_flow_m3ph, delta_pressure, efficiency)
    fuel_ton = (power_kw * pumping_time_hr * sfoc) / 1e6
    return fuel_ton * fuel_price
```

**optimizer.py (Lines 198-210):**
```python
# Pump fuel cost based on pumping time per bunkering call
pumping_time_hr_call = self.bunker_volume_per_call_m3 / pump_size  # ← NO 2.0

pump_fuel_per_call = (self.cost_calc.calculate_pump_power(pump_size,
                                                           self.config["propulsion"]["pump_delta_pressure_bar"],
                                                           self.config["propulsion"]["pump_efficiency"]) *
                     pumping_time_hr_call * self.sfoc) / 1e6  # ← USING CALCULATED TIME
pump_fuel_cost_per_call = pump_fuel_per_call * self.fuel_price
```

**main.py (Lines 385-399):**
```python
pump_power = cost_calculator.calculate_pump_power(pump_size_m3ph)
sfoc = config["propulsion"]["sfoc_g_per_kwh"]
fuel_price = config["economy"]["fuel_price_usd_per_ton"]

# Pumping time per bunkering call
pumping_time_hr_call = bunker_volume / pump_size_m3ph  # ← NO 2.0

# Annual pump events = number of vessel bunkering calls
annual_pump_events = annual_calls

# Fuel per pump event (in tons)
pump_fuel_per_event = (pump_power * pumping_time_hr_call * sfoc) / 1e6  # ← USING CALCULATED TIME
pump_fuel_cost_per_event = pump_fuel_per_event * fuel_price
pump_fuel_annual = pump_fuel_cost_per_event * annual_pump_events
```

### Impact Analysis
- **Numeric Example**: bunker_volume=5000 m³, pump=1000 m³/h
  - CostCalculator: 2.0 × (5000/1000) = 10 hours
  - Optimizer/Main: 5000/1000 = 5 hours
  - **Pump fuel cost difference: 2x overestimation in CostCalculator**

### CLAUDE.md Reference
- Version 2.3.1 claims fix: "remove erroneous 2.0 coefficient"
- But the coefficient still exists in cost_calculator.py line 214
- Appears to be partially fixed (optimizer/main) but not fully (cost_calculator)

---

## Issue #2: Total Supply Calculation (20-Year) - Case 1 vs Case 2 Inconsistency

### Location
**src/optimizer.py, Lines 376-383** (in `_extract_results` method)

### Code
```python
# Calculate total supply over 20 years for LCOAmmonia
total_supply_m3 = 0.0
for t in self.years:
    y_val = y[t].varValue
    if self.has_storage_at_busan:
        total_supply_m3 += y_val * self.bunker_volume_per_call_m3  # ← CORRECT
    else:
        total_supply_m3 += y_val * shuttle_size                     # ← QUESTIONABLE
```

### Analysis

**Case 1 Logic (Correct):**
- y[t] = annual bunkering calls (number of vessel calls)
- Each call delivers bunker_volume_per_call_m3 = 5000 m³
- Total = y[t] × 5000 ✓

**Case 2 Logic (Questionable):**
- y[t] = annual bunkering calls (STILL number of vessel calls, not shuttle trips!)
- But formula uses shuttle_size instead of bunker_volume_per_call_m3
- Example: 10,000 m³ shuttle serving 2 vessels per trip
  - If y[t] = 1000 calls and shuttle_size = 10,000
  - Total supply = 1000 × 10,000 = 10,000,000 m³
  - But actual: 1000 calls × 5000 m³ = 5,000,000 m³
  - **Result: 2x OVERCOUNT of supply**

### Yearly Results Show Correct Calculation
**src/optimizer.py, Line 467** (in yearly results):
```python
supply = y_val * self.bunker_volume_per_call_m3  # ← CORRECT - uses bunker volume
```

This is inconsistent with scenario-level calculation.

### Impact
- **LCOAmmonia = NPC / Total_Supply_ton**
- Inflated total_supply → Understated LCOAmmonia cost
- Case 2 appears more economical than it actually is

---

## Issue #3: Annual Supply Calculation - Theoretical vs Actual

### Locations
| Location | File | Line | Calculation |
|----------|------|------|-------------|
| Theoretical max | src/cycle_time_calculator.py | 120 | `annual_cycles * shuttle_size_m3` |
| Theoretical max | src/optimizer.py | 404 | `annual_cycles_max * shuttle_size` |
| Ships per year | src/optimizer.py | 431 | `annual_supply_m3 / bunker_volume_per_call_m3` |
| Yearly actual | src/optimizer.py | 467 | `y_val * bunker_volume_per_call_m3` |

### Code Examples

**cycle_time_calculator.py (Lines 119-124):**
```python
annual_cycles = 8000.0 / cycle_duration if cycle_duration > 0 else 0
annual_supply_m3 = annual_cycles * shuttle_size_m3

# Ships per year: how many ships can be bunkered annually
ships_per_year = annual_supply_m3 / self.bunker_volume_per_call_m3
```

**optimizer.py (Lines 403-405, 431):**
```python
annual_cycles_max = 8000 / cycle_duration if cycle_duration > 0 else 0
annual_supply_m3 = annual_cycles_max * shuttle_size
# ...
"Ships_Per_Year": round(annual_supply_m3 / self.bunker_volume_per_call_m3, 2),
```

**optimizer.py (Line 467 - yearly results):**
```python
supply = y_val * self.bunker_volume_per_call_m3  # Different calculation!
```

### Issue
- Annual_Supply_M3 is MAXIMUM theoretical capacity
- Ships_Per_Year is derived from this MAX, not actual
- But yearly supply uses actual optimization results (y_val)
- **Metric inconsistency**: Scenario-level metrics assume 100% utilization

### Impact
- Ships_Per_Year overstates actual ships served
- If optimizer doesn't use full capacity, Ships_Per_Year is misleading
- Scenario metrics don't match yearly aggregate

---

## Issue #4: Demand Satisfaction Constraint - Case 1 vs Case 2

### Location
**src/optimizer.py, Lines 274-277** (in `_solve_combination` method)

### Code
```python
# Demand satisfaction
if self.has_storage_at_busan:  # CASE 1
    prob += y[t] * self.bunker_volume_per_call_m3 >= self.annual_demand[t]
else:  # CASE 2
    prob += y[t] * shuttle_size >= self.annual_demand[t]
```

### Semantic Issue

**Case 1:**
- y[t] represents annual bunkering CALLS (vessel calls)
- Constraint: calls × 5000 m³ ≥ demand ✓

**Case 2:**
- y[t] ALSO represents annual bunkering CALLS
- But constraint: calls × shuttle_size m³ ≥ demand ✗
- This assumes each "call" delivers shuttle_size, not bunker_volume

### Conflicting Constraint
**Line 280** - Working time constraint:
```python
prob += y[t] * trips_per_call * cycle_duration <= N[t] * self.max_annual_hours
```
This constraint treats y[t] as CALLS for both cases!

### Mismatch
- **Line 280**: y[t] = calls
- **Line 277 Case 2**: y[t] = trips (implied by using shuttle_size)
- **Definition inconsistency** in Case 2

### Impact
- **Optimizer constraint is inconsistent for Case 2**
- May allow solver to find infeasible or suboptimal solutions
- Working time constraint and demand constraint interpret y[t] differently in Case 2

---

## Issue #5: Annuity Factor - 20 vs 21 Years

### Locations
| File | Line | Value | Issue |
|------|------|-------|-------|
| src/cost_calculator.py | 381 | `project_years = 20` | Hardcoded |
| src/optimizer.py | 52 | `self.years = range(2030, 2050+1)` | 21 elements |

### Code

**cost_calculator.py (Lines 363-382):**
```python
def get_annuity_factor(self) -> float:
    discount_rate = self.config["economy"]["discount_rate"]
    project_years = 20  # Fixed: 2030-2050
    return calculate_annuity_factor(discount_rate, project_years)
```

**optimizer.py (Lines 50-52):**
```python
self.start_year = self.config["time_period"]["start_year"]
self.end_year = self.config["time_period"]["end_year"]
self.years = list(range(self.start_year, self.end_year + 1))  # 2030-2050 = 21 years!
```

### Issue
- Years range: 2030, 2031, ..., 2050 = **21 elements**
- Annuity factor calculated for: **20 years**
- Discrepancy: using range(start, end+1) but calculating for (end-start)

### Impact
- **Small but systematic error**
- Annuity factor uses 20 years (smaller denominator)
- Annualized costs appear slightly higher than with correct 21-year basis

---

## Issue #6: Shuttle Fuel Cost - Travel Factor Missing in CostCalculator

### Locations
| File | Line | Has travel_factor | Status |
|------|------|-------------------|--------|
| src/optimizer.py | 195 | YES | Correct |
| main.py | 374 | YES | Correct |
| src/cost_calculator.py | 76-110 | NO | Missing |

### Code Comparison

**optimizer.py (Lines 192-196):**
```python
# For Case 1: One-way travel; Case 2: Round-trip travel
travel_factor = 1.0 if self.has_storage_at_busan else 2.0
shuttle_fuel_per_cycle = (mcr * self.sfoc * travel_factor * self.travel_time_hours) / 1e6
shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * self.fuel_price
```

**main.py (Lines 370-375):**
```python
# Travel factor: Case 1 = one-way, Case 2 = round-trip
travel_factor = 1.0 if has_storage_at_busan else 2.0

# Fuel per cycle (in tons): MCR × SFOC × travel_time / 1e6
shuttle_fuel_per_cycle = (mcr * sfoc * travel_factor * travel_time_hours) / 1e6
shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * fuel_price
```

**cost_calculator.py (Lines 76-110):**
```python
def calculate_shuttle_fuel_cost_per_cycle(
    self,
    shuttle_size_cbm: float,
    travel_time_hours: float
) -> float:
    # ...
    fuel_ton = (mcr * sfoc * travel_time_hours) / 1e6  # ← NO travel_factor!
    return fuel_ton * fuel_price
```

### Issue
- CostCalculator.py doesn't take has_storage_at_busan as parameter
- Cannot adjust for round-trip (Case 2) vs one-way (Case 1)
- If called directly, always calculates one-way travel fuel

### Impact
- **Case 2 shuttle fuel understated by 50%** if CostCalculator used directly
- Currently mitigated because optimizer/main calculate their own fuel
- But creates dead code/liability in CostCalculator

---

## Issue #7: Annual Cycles - Multiple Definitions

### Locations

| Source | File | Line | Definition |
|--------|------|------|-----------|
| Theoretical max | src/cycle_time_calculator.py | 119 | `8000 / cycle_duration` |
| Theoretical max | src/optimizer.py | 403 | `8000 / cycle_duration` |
| Actual trips | main.py | 330 | `total_trips` |
| Theoretical max | main.py | 464 | `max_annual_hours / cycle_duration` |

### Code Examples

**cycle_time_calculator.py (Line 119):**
```python
annual_cycles = 8000.0 / cycle_duration if cycle_duration > 0 else 0
```

**optimizer.py (Line 403):**
```python
annual_cycles_max = 8000 / cycle_duration if cycle_duration > 0 else 0
```

**main.py (Line 330 - annual_simulation):**
```python
annual_cycles = total_trips  # ACTUAL trips from fleet sizing
```

**main.py (Line 464):**
```python
annual_cycles_max = max_annual_hours / cycle_duration if cycle_duration > 0 else 0
```

### Ambiguity
- "annual_cycles" sometimes = theoretical max
- "annual_cycles" sometimes = actual trips
- Naming is confusing: should be "annual_cycles_max" vs "annual_cycles_actual"

### Impact
- Developers may use wrong metric for calculations
- Scenario outputs "Annual_Cycles_Max" (theoretical)
- Yearly outputs calculate from actual optimization

---

## Issue #8: Fleet Sizing - Multiple Implementations

### Locations

| Implementation | File | Lines | Method |
|---|---|---|---|
| Explicit | main.py | 314-316 | FleetSizingCalculator.calculate_required_shuttles_working_time_only() |
| Implicit | src/optimizer.py | 280 | MILP constraint |
| Implicit | src/optimizer.py | 290 | Comment only |

### Code

**main.py (Lines 313-316):**
```python
fleet_calc = FleetSizingCalculator(config)
required_shuttles = fleet_calc.calculate_required_shuttles_working_time_only(
    annual_calls, trips_per_call, cycle_duration
)
```

**src/optimizer.py (Line 280):**
```python
# Working time capacity
prob += y[t] * trips_per_call * cycle_duration <= N[t] * self.max_annual_hours
```

**src/fleet_sizing_calculator.py (Lines 64-67):**
```python
def calculate_required_shuttles_working_time_only(self, ...):
    total_trips = annual_calls * trips_per_call
    total_hours_needed = total_trips * cycle_duration
    required_shuttles = ceil(total_hours_needed / self.max_annual_hours)
    return required_shuttles
```

### Relationship
- main.py explicitly uses FleetSizingCalculator
- optimizer.py implicitly enforces same constraint via MILP
- If MILP constraint is modified, main.py won't track it

### Risk
- Two separate implementations of "same" logic
- Easy to introduce inconsistency if one is modified
- Discrepancies could arise between annual_simulation and full optimization

---

## Summary Table

| # | Issue | File(s) | Lines | Type | Severity | Impact |
|---|-------|---------|-------|------|----------|--------|
| 1 | Pump fuel 2.0 factor | cost_calc, optim, main | 214, 204, 390 | Inconsistent factor | CRITICAL | 2x cost discrepancy |
| 2 | Case 2 supply calc | optimizer | 383 | Wrong variable | CRITICAL | 2x overcount supply |
| 3 | Annual supply mismatch | optim, cycle_calc, main | 404, 120, 467 | Theoretical vs actual | HIGH | Metrics misleading |
| 4 | Demand constraint Case 2 | optimizer | 274-277 | Semantic inconsistency | HIGH | Constraint incorrect |
| 5 | Annuity factor years | cost_calc, optim | 381, 52 | Hardcoded mismatch | MEDIUM | Slight cost overstate |
| 6 | Shuttle fuel no factor | cost_calc | 76-110 | Missing parameter | LOW | Not currently used |
| 7 | Annual cycles ambiguity | cycle_calc, optim, main | 119, 403, 330, 464 | Naming inconsistency | MEDIUM | Confusion |
| 8 | Fleet sizing duplication | main, optim, fleet_calc | 314, 280, 64 | Multiple implementations | MEDIUM | Risk of divergence |

---

## Recommended Fix Order

1. **FIRST - Issue #1**: Remove 2.0 factor from cost_calculator.py line 214
   - Most critical impact on accuracy
   - Referenced in CLAUDE.md as "fixed" but not actually fixed

2. **SECOND - Issue #2**: Change Case 2 supply to use bunker_volume_per_call_m3
   - Direct calculation error
   - Affects LCOAmmonia metric

3. **THIRD - Issue #4**: Fix demand constraint for Case 2
   - Semantic inconsistency could cause solver issues
   - Match constraint logic to working time constraint interpretation of y[t]

4. **FOURTH - Issue #3**: Unify annual supply calculation
   - Calculate Ships_Per_Year from actual y[t] values
   - Or clarify metrics as theoretical vs actual

5. **FIFTH - Issue #5**: Fix annuity factor to use 21 years
   - Either change hardcode or use actual year count from range

6. **SIXTH - Issue #6**: Add travel_factor to cost_calculator
   - Add has_storage_at_busan parameter
   - Make method case-aware

7. **SEVENTH - Issue #7**: Unify annual cycles terminology
   - Rename to annual_cycles_max vs annual_cycles_actual
   - Make distinction clear in code

8. **EIGHTH - Issue #8**: Consolidate fleet sizing
   - Consider creating unified FleetSizer interface
   - Document relationship between MILP and explicit calculation

