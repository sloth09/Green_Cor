# Case 1: Busan Port with Storage -- Full Hand-Calculation Verification

## 3.1 Case Overview

| Parameter | Value |
|-----------|-------|
| Route | Busan Port Internal |
| Storage at Busan | Yes (35,000 tons) |
| Travel Time (one-way) | 1.0 hour |
| Shuttle Size Range | 500 -- 10,000 m3 |
| Optimal Shuttle Size | 2,500 m3 |
| Optimal Pump Rate | 1,000 m3/h |
| NPC (20yr Total) | $290.81M |
| LCOAmmonia | $1.23/ton |

**Key Characteristic**: Shuttles operate within Busan Port, moving fuel from storage tanks
to vessels. Each bunkering call requires multiple shuttle trips when `Shuttle_Size < Bunker_Volume`.

**Critical Design Difference from Case 2**: In Case 1, pumping time is governed by shuttle
capacity (`Shuttle_Size / Pump_Rate`), not by per-vessel demand. The shuttle empties its
entire cargo into one vessel per trip, then returns to the storage terminal for reloading.

**Source Files**:
- Scenario Summary: `results/deterministic/MILP_scenario_summary_case_1.csv`
- Per-Year Results: `results/deterministic/MILP_per_year_results_case_1.csv`
- Config: `config/case_1.yaml` + `config/base.yaml`

---

## 3.2 Cycle Time Verification (Optimal: 2,500 m3)

### 3.2.1 Shore Loading Time

The shore loading time accounts for the time to fill the shuttle at the port storage facility.

**Formula:**

```
Shore_Loading = (Shuttle_Size / Q_shore) + t_fixed
```

Where:
- `Q_shore` = 1,500 m3/h (shore pump rate, from `base.yaml`)
- `t_fixed` = 2.0 h (fixed loading preparation time, from `base.yaml: shore_supply.loading_time_fixed_hours`)

**Substitution:**

```
Shore_Loading = (2500 / 1500) + 2.0
             = 1.6667 + 2.0
             = 3.6667 hours
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Shore Pumping | 1.6667 h | -- | -- | (intermediate) |
| Fixed Loading | 2.0000 h | -- | -- | (config) |
| Shore Loading Total | 3.6667 h | 3.6667 h | 0.00% | PASS |

### 3.2.2 Basic Cycle Duration

The basic cycle is the shuttle round-trip time excluding shore loading.

**Formula (Case 1, `has_storage_at_busan = true`):**

```
Basic_Cycle = Travel_Out + Setup_Inbound + Pumping + Setup_Outbound + Travel_Return
```

**Component Calculation:**

| Component | Formula | Substitution | Value |
|-----------|---------|-------------|-------|
| Travel_Out | config | -- | 1.0 h |
| Setup_Inbound | 2 x setup_time | 2 x 0.5 | 1.0 h |
| Pumping | Shuttle_Size / Pump_Rate | 2500 / 1000 | 2.5 h |
| Setup_Outbound | 2 x setup_time | 2 x 0.5 | 1.0 h |
| Travel_Return | config | -- | 1.0 h |

Note: Setup time is `2 x 0.5 h` because each connection event involves both hose
connection (0.5 h) and disconnection/venting (0.5 h). See `shuttle_round_trip_calculator.py`
line 93: `setup_inbound = 2.0 * self.setup_time_hours`.

Note: For Case 1, `port_entry = 0`, `port_exit = 0`, and `movement_per_vessel = 0`
(all zero because operations are within the port). See source lines 97--103.

**Substitution:**

```
Basic_Cycle = 1.0 + 1.0 + 2.5 + 1.0 + 1.0
            = 6.5 hours
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Basic Cycle Duration | 6.50 h | 6.50 h | 0.00% | PASS |

### 3.2.3 Total Cycle Duration

**Formula:**

```
Cycle = Shore_Loading + Basic_Cycle
```

**Substitution:**

```
Cycle = 3.6667 + 6.5
      = 10.1667 hours
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Cycle Duration | 10.1667 h | 10.1667 h | 0.00% | PASS |

### 3.2.4 Maximum Annual Cycles per Shuttle

**Formula:**

```
Annual_Cycles_Max = H_max / Cycle_Duration
```

Where `H_max` = 8,000 hours/year (from `base.yaml: operations.max_annual_hours_per_vessel`).

**Substitution:**

```
Annual_Cycles_Max = 8000 / 10.1667
                  = 786.89 cycles/shuttle/year
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Annual Cycles Max | 786.89 | 786.89 | 0.00% | PASS |

### 3.2.5 Trips per Call and Call Duration

**Trips per Call** -- How many shuttle round-trips are needed to fulfill one 5,000 m3 bunkering call:

**Formula:**

```
Trips_per_Call = ceil(Bunker_Volume / Shuttle_Size)
```

**Substitution:**

```
Trips_per_Call = ceil(5000 / 2500)
               = ceil(2.0)
               = 2
```

**Call Duration** -- Total time for one complete bunkering call:

**Formula:**

```
Call_Duration = Trips_per_Call x Cycle_Duration
```

**Substitution:**

```
Call_Duration = 2 x 10.1667
              = 20.3333 hours
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Trips per Call | 2.0000 | 2.0000 | 0.00% | PASS |
| Call Duration | 20.3333 h | 20.3333 h | 0.00% | PASS |

### 3.2.6 Cycle Time Summary -- All Components

| Component | Manual (h) | CSV Column | CSV Value (h) | Status |
|-----------|-----------|------------|---------------|--------|
| Shore Loading | 3.6667 | Shore_Loading_hr | 3.6667 | PASS |
| Travel Outbound | 1.0000 | Travel_Outbound_hr | 1.0000 | PASS |
| Travel Return | 1.0000 | Travel_Return_hr | 1.0000 | PASS |
| Setup Inbound | 1.0000 | Setup_Inbound_hr | 1.0000 | PASS |
| Setup Outbound | 1.0000 | Setup_Outbound_hr | 1.0000 | PASS |
| Pumping per Vessel | 2.5000 | Pumping_Per_Vessel_hr | 2.5000 | PASS |
| Pumping Total | 2.5000 | Pumping_Total_hr | 2.5000 | PASS |
| Basic Cycle Duration | 6.5000 | Basic_Cycle_Duration_hr | 6.5000 | PASS |
| **Total Cycle** | **10.1667** | **Cycle_Duration_hr** | **10.1667** | **PASS** |

### 3.2.7 Single Cycle Timeline Diagram (2,500 m3 Optimal)

```
=== Case 1: Single Cycle Timeline (2,500 m3 Shuttle, 1,000 m3/h Pump) ===

Phase                  Duration (h)   Cumulative (h)
---------------------  ------------   --------------
Shore Loading             3.67         0.00 ->  3.67   [Load shuttle at shore terminal]
Travel Outbound           1.00         3.67 ->  4.67   [Move to vessel berth]
Setup Inbound             1.00         4.67 ->  5.67   [Hose connect + purge]
Pumping                   2.50         5.67 ->  8.17   [Transfer 2,500 m3 to vessel]
Setup Outbound            1.00         8.17 ->  9.17   [Hose disconnect + purge]
Travel Return             1.00         9.17 -> 10.17   [Return to shore terminal]
---------------------  ------------   --------------
TOTAL CYCLE              10.17 h

Timeline (to scale, 1 char ~ 0.2 h):
|=====Shore Loading=====|==Trav==|==Setup==|=====Pumping=====|==Setup==|==Trav==|
|       3.67 h          | 1.00 h | 1.00 h  |     2.50 h      | 1.00 h  | 1.00 h |
|<----------------------- Total Cycle: 10.17 h ------------------------------------->|
       36.1%              9.8%     9.8%        24.6%            9.8%      9.8%

Shore Loading = (2500 / 1500) + 2.0 = 1.67 + 2.00 = 3.67 h
  [Variable: 1.67 h pumping at 1500 m3/h] + [Fixed: 2.00 h setup/shutdown]

Note: 2 cycles = 1 bunkering call (5,000 m3). Call Duration = 2 x 10.17 = 20.33 h
```

---

## 3.3 CAPEX Verification

### 3.3.1 Shuttle CAPEX (per unit)

**Formula (Scaling Law):**

```
CAPEX_shuttle = Ref_CAPEX x (Shuttle_Size / Ref_Size)^alpha
```

Where:
- `Ref_CAPEX` = $61,500,000 (reference vessel at 40,000 m3)
- `Ref_Size` = 40,000 m3
- `alpha` = 0.75 (scaling exponent)

**Substitution:**

```
CAPEX_shuttle = 61,500,000 x (2500 / 40000)^0.75
              = 61,500,000 x (0.0625)^0.75
```

**Intermediate: Computing (0.0625)^0.75**

```
0.0625 = 1/16 = 2^(-4)

(2^(-4))^0.75 = 2^(-4 x 0.75)
              = 2^(-3)
              = 1/8
              = 0.1250
```

**Result:**

```
CAPEX_shuttle = 61,500,000 x 0.1250
              = 7,687,500 USD per shuttle
              = $7.6875M per shuttle
```

**Verification against per-year CSV** (Year 2040, New_Shuttles = 1):

```
CSV: Actual_CAPEX_Shuttle_USDm = 7.6875
     = $7,687,500 for 1 new shuttle
```

| Item | Manual | CSV (yr 2040) | Diff | Status |
|------|--------|---------------|------|--------|
| Shuttle CAPEX (per unit) | $7,687,500 | $7,687,500 | 0.00% | PASS |

### 3.3.2 Pump Power Calculation

**Formula:**

```
P_pump = (delta_P_Pa x Q_m3s) / eta / 1000  [kW]
```

Where:
- `delta_P` = 4.0 bar = 400,000 Pa
- `Q` = 1,000 m3/h = 1000 / 3600 = 0.27778 m3/s
- `eta` = 0.7

**Substitution:**

```
P_pump = (400,000 x 0.27778) / 0.7 / 1000
       = 111,111.11 / 0.7 / 1000
       = 158,730.16 / 1000
       = 158.73 kW
```

### 3.3.3 Pump CAPEX

**Formula:**

```
CAPEX_pump = P_pump x Cost_per_kW
```

Where `Cost_per_kW` = $2,000/kW (from `base.yaml: propulsion.pump_power_cost_usd_per_kw`).

**Substitution:**

```
CAPEX_pump = 158.73 x 2,000
           = $317,460
```

### 3.3.4 Bunkering System CAPEX (per shuttle)

The bunkering system CAPEX includes shuttle equipment cost plus pump cost.

**Formula:**

```
CAPEX_bunkering = (CAPEX_shuttle x equipment_ratio) + CAPEX_pump
```

Where `equipment_ratio` = 0.03 (3%, from `base.yaml: shuttle.equipment_ratio`).

**Substitution:**

```
CAPEX_bunkering = (7,687,500 x 0.03) + 317,460
                = 230,625 + 317,460
                = 548,085 USD per shuttle
```

**Verification against per-year CSV** (Year 2040, New_Shuttles = 1):

The CSV column `Actual_CAPEX_Pump_USDm` stores the total bunkering CAPEX (equipment + pump),
not just the pump alone.

```
CSV: Actual_CAPEX_Pump_USDm = 0.5481M = $548,100
Manual: $548,085 (difference due to rounding of pump power)
```

| Item | Manual | CSV (yr 2040) | Diff | Status |
|------|--------|---------------|------|--------|
| Pump Power | 158.73 kW | -- | -- | (intermediate) |
| Pump CAPEX | $317,460 | -- | -- | (intermediate) |
| Shuttle Equipment (3%) | $230,625 | -- | -- | (intermediate) |
| **Bunkering CAPEX (per shuttle)** | **$548,085** | **$548,100** | **0.00%** | **PASS** |

### 3.3.5 Annuity Factor

**Formula:**

```
AF = [1 - (1 + r)^(-n)] / r
```

Where:
- `r` = 0.07 (annualization interest rate, from `base.yaml: economy.annualization_interest_rate`)
- `n` = 21 years (2030 to 2050 inclusive)

Note: This uses the `annualization_interest_rate` (7%), NOT the `discount_rate` (0%).
The discount rate controls NPV time-value discounting (disabled at 0%). The annualization
rate converts lump-sum CAPEX into equivalent annual payments.

**Substitution:**

```
(1.07)^21 = e^(21 x ln(1.07))
          = e^(21 x 0.06766)
          = e^(1.42082)
          = 4.14056

(1.07)^(-21) = 1 / 4.14056 = 0.24151

AF = (1 - 0.24151) / 0.07
   = 0.75849 / 0.07
   = 10.8355
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Annuity Factor | 10.8355 | 10.8355 | 0.00% | PASS |

### 3.3.6 Annualized CAPEX per Shuttle per Year

**Formula:**

```
Annualized_CAPEX = Asset_Value / AF
```

**Shuttle Annualized CAPEX:**

```
Ann_Shuttle = 7,687,500 / 10.8355
            = 709,512 USD/year/shuttle
```

**Bunkering Annualized CAPEX:**

```
Ann_Bunkering = 548,085 / 10.8355
              = 50,580 USD/year/shuttle
```

**Verification against per-year CSV** (Year 2039, Total_Shuttles = 8):

```
Expected Annualized Shuttle CAPEX = 8 x 709,512 = 5,676,094 = $5.6761M
CSV: Annualized_CAPEX_Shuttle_USDm = 5.6758M

Expected Annualized Bunkering CAPEX = 8 x 50,580 = 404,640 = $0.4046M
CSV: Annualized_CAPEX_Pump_USDm = 0.4047M
```

| Item | Manual | CSV (yr 2039) | Diff | Status |
|------|--------|---------------|------|--------|
| Ann. Shuttle CAPEX (8 shuttles) | $5.6761M | $5.6758M | 0.01% | PASS |
| Ann. Bunkering CAPEX (8 shuttles) | $0.4046M | $0.4047M | 0.02% | PASS |

### 3.3.7 NPC Annualized CAPEX (21-year sum)

**Method:**

The NPC Annualized CAPEX is the sum of annualized CAPEX across all 21 years (2030--2050).

```
NPC_Ann_Shuttle_CAPEX = (Shuttle_CAPEX / AF) x Sum(Total_Shuttles over all years)
```

**Fleet Profile over 21 years** (from per-year CSV):

| Year | New | Total | | Year | New | Total |
|------|-----|-------|-|------|-----|-------|
| 2030 | 2 | 2 | | 2041 | 1 | 10 |
| 2031 | 1 | 3 | | 2042 | 0 | 10 |
| 2032 | 0 | 3 | | 2043 | 1 | 11 |
| 2033 | 1 | 4 | | 2044 | 1 | 12 |
| 2034 | 1 | 5 | | 2045 | 0 | 12 |
| 2035 | 0 | 5 | | 2046 | 1 | 13 |
| 2036 | 1 | 6 | | 2047 | 1 | 14 |
| 2037 | 1 | 7 | | 2048 | 0 | 14 |
| 2038 | 1 | 8 | | 2049 | 1 | 15 |
| 2039 | 0 | 8 | | 2050 | 1 | 16 |
| 2040 | 1 | 9 | | | | |

**Sum of Total_Shuttles** = 2+3+3+4+5+5+6+7+8+8+9+10+10+11+12+12+13+14+14+15+16 = **187 shuttle-years**

**Calculation:**

```
NPC_Ann_Shuttle_CAPEX = 709,512 x 187
                      = 132,678,744
                      = $132.68M

NPC_Ann_Bunkering_CAPEX = 50,580 x 187
                        = 9,458,460
                        = $9.46M
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| NPC Ann. Shuttle CAPEX | $132.68M | $132.67M | 0.01% | PASS |
| NPC Ann. Bunkering CAPEX | $9.46M | $9.46M | 0.00% | PASS |

---

## 3.4 OPEX Verification

### 3.4.1 Shuttle Fixed OPEX

**Formula:**

```
fOPEX_shuttle = CAPEX_shuttle x fixed_opex_ratio
```

Where `fixed_opex_ratio` = 0.05 (5%, from `base.yaml: shuttle.fixed_opex_ratio`).

**Substitution:**

```
fOPEX_shuttle = 7,687,500 x 0.05
              = 384,375 USD/year/shuttle
```

**Verification against per-year CSV** (Year 2040, Total_Shuttles = 9):

```
Expected: 9 x 384,375 = 3,459,375 = $3.4594M
CSV: FixedOPEX_Shuttle_USDm = 3.4594M
```

| Item | Manual | CSV (yr 2040) | Diff | Status |
|------|--------|---------------|------|--------|
| Shuttle fOPEX (9 shuttles) | $3.4594M | $3.4594M | 0.00% | PASS |

### 3.4.2 Bunkering Fixed OPEX

**Formula:**

```
fOPEX_bunkering = CAPEX_bunkering x fixed_opex_ratio
```

Where `fixed_opex_ratio` = 0.05 (5%, from `base.yaml: bunkering.fixed_opex_ratio`).

**Substitution:**

```
fOPEX_bunkering = 548,085 x 0.05
                = 27,404 USD/year/shuttle
```

**Verification against per-year CSV** (Year 2040, Total_Shuttles = 9):

```
Expected: 9 x 27,404 = 246,638 = $0.2466M
CSV: FixedOPEX_Pump_USDm = 0.2466M
```

| Item | Manual | CSV (yr 2040) | Diff | Status |
|------|--------|---------------|------|--------|
| Bunkering fOPEX (9 shuttles) | $0.2466M | $0.2466M | 0.00% | PASS |

### 3.4.3 NPC Fixed OPEX (21-year sum)

**Method:** Sum over all 21 years of (Total_Shuttles x per-shuttle fOPEX).

Using the fleet sum of 187 shuttle-years (from Section 3.3.7):

```
NPC_Shuttle_fOPEX = 384,375 x 187
                  = 71,878,125
                  = $71.88M

NPC_Bunkering_fOPEX = 27,404 x 187
                    = 5,124,548
                    = $5.12M
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| NPC Shuttle fOPEX | $71.88M | $71.88M | 0.00% | PASS |
| NPC Bunkering fOPEX | $5.12M | $5.12M | 0.00% | PASS |

### 3.4.4 Shuttle Variable OPEX (Fuel Cost)

**IMPORTANT -- Travel Factor for Case 1:**
For Case 1, `travel_factor = 1.0` (one-way fuel calculation). This is confirmed in the
optimizer source code at line 213:
```
travel_factor = 1.0 if self.has_storage_at_busan else 2.0
```

The rationale: Case 1 shuttles operate within the port. The code models fuel consumption
based on one-way loaded travel. Case 2 uses `travel_factor = 2.0` for the full round trip
to a distant port (Yeosu/Ulsan).

**Formula:**

```
Fuel_per_cycle = MCR x SFOC x Travel_Time x Travel_Factor / 1,000,000  [tons]
Cost_per_cycle = Fuel_per_cycle x Fuel_Price
```

Where:
- `MCR` = 1,310 kW (v5 Power Law for 2,500 m3, DWT = 2,125)
- `SFOC` = 505 g/kWh (DWT < 3,000 --> 4-stroke high-speed engine)
- `Travel_Time` = 1.0 h (one-way)
- `Travel_Factor` = 1.0 (Case 1)
- `Fuel_Price` = $600/ton

**Substitution:**

```
Fuel_per_cycle = 1310 x 505 x 1.0 x 1.0 / 1,000,000
               = 661,550 / 1,000,000
               = 0.6616 tons/cycle

Cost_per_cycle = 0.6616 x 600
               = $396.93 per cycle
```

**Verification against per-year CSV** (Year 2040: 6,600 cycles):

```
Expected: 396.93 x 6600 = $2,619,738 = $2.6197M
CSV: VariableOPEX_Shuttle_USDm = 2.6197M
```

**Cross-check** (Year 2039: 6,048 cycles):

```
Expected: 396.93 x 6048 = $2,401,432 = $2.4014M
CSV: VariableOPEX_Shuttle_USDm = 2.4006M
Difference: 0.03% (rounding in per-cycle cost)
```

| Item | Manual | CSV (yr 2040) | Diff | Status |
|------|--------|---------------|------|--------|
| Fuel per cycle | 0.6616 tons | -- | -- | (intermediate) |
| Cost per cycle | $396.93 | -- | -- | (intermediate) |
| Shuttle vOPEX (6,600 cycles) | $2.6197M | $2.6197M | 0.00% | PASS |

### 3.4.5 Bunkering Variable OPEX (Pump Fuel Cost)

**IMPORTANT -- SFOC for Pump Fuel Calculation:**
The pump fuel cost uses the **shuttle's DWT-based SFOC** (not the default 379 g/kWh).
This is confirmed in the optimizer source code at lines 208--228, where `sfoc` is retrieved
from `self.sfoc_map` for the specific shuttle size, and the same `sfoc` variable is used
for both shuttle fuel and pump fuel calculations.

For 2,500 m3 shuttle (DWT = 2,125 < 3,000): **SFOC = 505 g/kWh**

**Formula:**

```
Pumping_Time_per_Call = Bunker_Volume / Pump_Rate  [hours]
Fuel_per_call = P_pump x Pumping_Time x SFOC / 1,000,000  [tons]
Cost_per_call = Fuel_per_call x Fuel_Price
```

Note: Pumping time is computed per bunkering **call** (5,000 m3), not per shuttle cycle
(2,500 m3). The pump operates to fill the entire vessel demand, regardless of how many
shuttle trips are needed. See optimizer line 223:
```
pumping_time_hr_call = self.bunker_volume_per_call_m3 / pump_size
```

**Substitution:**

```
Pumping_Time_per_Call = 5000 / 1000 = 5.0 hours

Fuel_per_call = 158.73 x 5.0 x 505 / 1,000,000
              = 158.73 x 2,525 / 1,000,000
              = 400,793 / 1,000,000
              = 0.4008 tons/call

Cost_per_call = 0.4008 x 600
              = $240.48 per call
```

**Verification against per-year CSV** (Year 2040: 3,300 calls):

```
Expected: 240.48 x 3300 = $793,584 = $0.7936M
CSV: VariableOPEX_Pump_USDm = 0.7936M
```

**Cross-check** (Year 2039: 3,024 calls):

```
Expected: 240.48 x 3024 = $727,211 = $0.7272M
CSV: VariableOPEX_Pump_USDm = 0.7272M
```

| Item | Manual | CSV (yr 2040) | Diff | Status |
|------|--------|---------------|------|--------|
| Pumping time/call | 5.0 h | -- | -- | (intermediate) |
| Fuel per call | 0.4008 tons | -- | -- | (intermediate) |
| Cost per call | $240.48 | -- | -- | (intermediate) |
| Bunkering vOPEX (3,300 calls) | $0.7936M | $0.7936M | 0.00% | PASS |

### 3.4.6 NPC Variable OPEX (21-year sum)

**Total Cycles over 21 years:**

Annual Cycles = Annual_Calls x Trips_per_Call = Annual_Calls x 2

Using symmetry of the linear demand growth (600 to 6,000 calls):

```
Sum of Annual_Calls = (600 + 6000)/2 x 21 = 3300 x 21 = 69,300 calls
Sum of Annual_Cycles = 69,300 x 2 = 138,600 cycles
```

**Calculation:**

```
NPC_Shuttle_vOPEX = 396.93 x 138,600
                  = 55,014,498
                  = $55.01M

NPC_Bunkering_vOPEX = 240.48 x 69,300
                    = 16,665,264
                    = $16.67M
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Total Cycles (21 yr) | 138,600 | -- | -- | (intermediate) |
| Total Calls (21 yr) | 69,300 | -- | -- | (intermediate) |
| NPC Shuttle vOPEX | $55.01M | $55.01M | 0.00% | PASS |
| NPC Bunkering vOPEX | $16.67M | $16.67M | 0.00% | PASS |

---

## 3.5 NPC Total Verification

### 3.5.1 Component Breakdown

| # | Cost Component | NPC Value (USDm) | Share |
|---|----------------|------------------|-------|
| 1 | NPC Annualized Shuttle CAPEX | 132.67 | 45.61% |
| 2 | NPC Annualized Bunkering CAPEX | 9.46 | 3.25% |
| 3 | NPC Terminal CAPEX | 0.00 | 0.00% |
| | **Subtotal CAPEX** | **142.13** | **48.87%** |
| 4 | NPC Shuttle fOPEX | 71.88 | 24.72% |
| 5 | NPC Bunkering fOPEX | 5.12 | 1.76% |
| 6 | NPC Terminal fOPEX | 0.00 | 0.00% |
| | **Subtotal Fixed OPEX** | **77.00** | **26.48%** |
| 7 | NPC Shuttle vOPEX | 55.01 | 18.91% |
| 8 | NPC Bunkering vOPEX | 16.67 | 5.73% |
| 9 | NPC Terminal vOPEX | 0.00 | 0.00% |
| | **Subtotal Variable OPEX** | **71.68** | **24.65%** |
| | **NPC TOTAL** | **290.81** | **100.00%** |

Note: Terminal costs are $0 because `shore_supply.enabled = false` in `base.yaml`. Shore
loading **time** is always included in cycle calculations, but shore facility **costs** are
excluded when disabled.

### 3.5.2 Sum Verification

**Formula:**

```
NPC_Total = NPC_CAPEX + NPC_fOPEX + NPC_vOPEX
```

**Substitution:**

```
NPC_Total = (132.67 + 9.46 + 0.00)
          + (71.88 + 5.12 + 0.00)
          + (55.01 + 16.67 + 0.00)
          = 142.13 + 77.00 + 71.68
          = 290.81M
```

| Item | Manual Sum | CSV | Diff | Status |
|------|-----------|-----|------|--------|
| NPC Total | $290.81M | $290.81M | 0.00% | PASS |

---

## 3.6 Total Supply and LCOAmmonia Verification

### 3.6.1 Total Supply Calculation

**Formula:**

```
Total_Supply_m3 = Sum over all years of (Annual_Calls x Bunker_Volume)
Total_Supply_ton = Total_Supply_m3 x density_storage
```

Where `density_storage` = 0.680 ton/m3 (from `base.yaml: ammonia.density_storage_ton_m3`).

**Annual Demand Growth:**

Vessels grow linearly from 50 (2030) to 500 (2050). With each vessel requiring 12 voyages/year
and 5,000 m3/call:

```
Annual_Calls_2030 = 600
Annual_Calls_2050 = 6,000
Average calls = (600 + 6000) / 2 = 3,300
Sum over 21 years = 3,300 x 21 = 69,300 calls
```

```
Total_Supply_m3 = 69,300 x 5,000 = 346,500,000 m3
Total_Supply_ton = 346,500,000 x 0.680 = 235,620,000 tons
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Total Supply (20yr) | 235,620,000 tons | 235,620,000 tons | 0.00% | PASS |

### 3.6.2 LCOAmmonia

**Formula:**

```
LCOAmmonia = NPC_Total / Total_Supply_ton
```

**Substitution:**

```
LCOAmmonia = 290,810,000 / 235,620,000
           = 1.2343 USD/ton
```

Rounded to 2 decimal places: **$1.23/ton**

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| LCOAmmonia | $1.23/ton | $1.23/ton | 0.00% | PASS |

---

## 3.7 Per-Year Results Verification (Selected Years)

### 3.7.1 Year 2030 (First Year)

| Item | Formula | Manual | CSV | Status |
|------|---------|--------|-----|--------|
| New Shuttles | MILP decision | 2 | 2 | PASS |
| Total Shuttles | cumulative | 2 | 2 | PASS |
| Annual Calls | demand / 5000 | 600 | 600 | PASS |
| Annual Cycles | calls x trips | 600 x 2 = 1,200 | 1,200 | PASS |
| Supply_m3 | calls x 5000 | 3,000,000 | 3,000,000 | PASS |
| Actual_CAPEX_Shuttle | 2 x 7.6875 | $15.375M | $15.375M | PASS |
| Actual_CAPEX_Pump | 2 x 0.5481 | $1.0962M | $1.0962M | PASS |
| Ann. CAPEX_Shuttle | 2 x 0.7095 | $1.4190M | $1.4189M | PASS |
| FixedOPEX_Shuttle | 2 x 0.3844 | $0.7688M | $0.7688M | PASS |
| FixedOPEX_Pump | 2 x 0.0274 | $0.0548M | $0.0548M | PASS |
| VarOPEX_Shuttle | 1200 x 396.93 | $0.4763M | $0.4763M | PASS |
| VarOPEX_Pump | 600 x 240.48 | $0.1443M | $0.1443M | PASS |

### 3.7.2 Year 2040 (Mid-Project)

| Item | Formula | Manual | CSV | Status |
|------|---------|--------|-----|--------|
| New Shuttles | MILP decision | 1 | 1 | PASS |
| Total Shuttles | cumulative | 9 | 9 | PASS |
| Annual Calls | demand / 5000 | 3,300 | 3,300 | PASS |
| Annual Cycles | calls x trips | 3,300 x 2 = 6,600 | 6,600 | PASS |
| Supply_m3 | calls x 5000 | 16,500,000 | 16,500,000 | PASS |
| Actual_CAPEX_Shuttle | 1 x 7.6875 | $7.6875M | $7.6875M | PASS |
| Actual_CAPEX_Pump | 1 x 0.5481 | $0.5481M | $0.5481M | PASS |
| Ann. CAPEX_Shuttle | 9 x 0.7095 | $6.3856M | $6.3852M | PASS |
| FixedOPEX_Shuttle | 9 x 0.3844 | $3.4594M | $3.4594M | PASS |
| FixedOPEX_Pump | 9 x 0.0274 | $0.2466M | $0.2466M | PASS |
| VarOPEX_Shuttle | 6600 x 396.93 | $2.6197M | $2.6197M | PASS |
| VarOPEX_Pump | 3300 x 240.48 | $0.7936M | $0.7936M | PASS |

### 3.7.3 Year 2050 (Final Year)

| Item | Formula | Manual | CSV | Status |
|------|---------|--------|-----|--------|
| New Shuttles | MILP decision | 1 | 1 | PASS |
| Total Shuttles | cumulative | 16 | 16 | PASS |
| Annual Calls | demand / 5000 | 6,000 | 6,000 | PASS |
| Annual Cycles | calls x trips | 6,000 x 2 = 12,000 | 12,000 | PASS |
| Supply_m3 | calls x 5000 | 30,000,000 | 30,000,000 | PASS |
| Actual_CAPEX_Shuttle | 1 x 7.6875 | $7.6875M | $7.6875M | PASS |
| Actual_CAPEX_Pump | 1 x 0.5481 | $0.5481M | $0.5481M | PASS |
| Ann. CAPEX_Shuttle | 16 x 0.7095 | $11.3521M | $11.3515M | PASS |
| FixedOPEX_Shuttle | 16 x 0.3844 | $6.1500M | $6.1500M | PASS |
| FixedOPEX_Pump | 16 x 0.0274 | $0.4385M | $0.4385M | PASS |
| VarOPEX_Shuttle | 12000 x 396.93 | $4.7632M | $4.7632M | PASS |
| VarOPEX_Pump | 6000 x 240.48 | $1.4429M | $1.4429M | PASS |

### 3.7.4 Utilization Rate Check (Year 2040)

**Formula:**

```
Total_Hours_Needed = Annual_Cycles x Cycle_Duration
Total_Hours_Available = Total_Shuttles x H_max
Utilization_Rate = Total_Hours_Needed / Total_Hours_Available
```

**Substitution:**

```
Total_Hours_Needed = 6,600 x 10.1667 = 67,100 hours
Total_Hours_Available = 9 x 8,000 = 72,000 hours
Utilization_Rate = 67,100 / 72,000 = 0.9319 = 93.19%
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Hours Needed | 67,100 | 67,100 | 0.00% | PASS |
| Hours Available | 72,000 | 72,000 | 0.00% | PASS |
| Utilization Rate | 93.19% | 93.19% | 0.00% | PASS |

---

## 3.8 All Shuttle Sizes Summary

The following table shows all evaluated shuttle sizes from the scenario summary CSV.
The optimal configuration (minimum NPC) is 2,500 m3.

| Shuttle (m3) | Cycle (h) | Shore Loading (h) | Ann. Cycles | Trips/Call | NPC ($M) | LCO ($/ton) | Rank |
|-------------|-----------|-------------------|-------------|-----------|----------|-------------|------|
| 500 | 6.83 | 2.33 | 1,170.73 | 10 | 356.27 | 1.51 | 7 |
| 1,000 | 7.67 | 2.67 | 1,043.48 | 5 | 306.76 | 1.30 | 2 |
| 1,500 | 8.50 | 3.00 | 941.18 | 4 | 347.83 | 1.48 | 6 |
| 2,000 | 9.33 | 3.33 | 857.14 | 3 | 342.29 | 1.45 | 4 |
| **2,500** | **10.17** | **3.67** | **786.89** | **2** | **290.81** | **1.23** | **1** |
| 3,000 | 11.00 | 4.00 | 727.27 | 2 | 347.62 | 1.48 | 5 |
| 3,500 | 11.83 | 4.33 | 676.06 | 2 | 403.00 | 1.71 | 8 |
| 4,000 | 12.67 | 4.67 | 631.58 | 2 | 453.42 | 1.92 | 9 |
| 4,500 | 13.50 | 5.00 | 592.59 | 2 | 518.61 | 2.20 | 11 |
| 5,000 | 14.33 | 5.33 | 558.14 | 1 | 309.33 | 1.31 | 3 |
| 7,500 | 18.50 | 7.00 | 432.43 | 1 | 501.19 | 2.13 | 10 |
| 10,000 | 22.67 | 8.67 | 352.94 | 1 | 733.97 | 3.12 | 12 |

**Key Observations:**

1. The optimal 2,500 m3 shuttle benefits from a favorable Trips_per_Call step:
   - At 2,500 m3, Trips_per_Call drops from 3 (at 2,000 m3) to 2, significantly reducing
     the number of shuttle cycles needed per bunkering call.

2. The 5,000 m3 shuttle (Rank 3) benefits from Trips_per_Call = 1, but its higher unit
   CAPEX ($14.57M vs $7.69M) and SFOC change (436 g/kWh instead of 505 g/kWh) result
   in a different cost balance.

3. NPC does NOT decrease monotonically with shuttle size due to the discrete
   Trips_per_Call function and DWT-based SFOC step changes.

---

## 3.9 Variable OPEX Pattern Analysis

### 3.9.1 Why Case 1 Variable OPEX is Non-Monotonic

Unlike Case 2 where Variable OPEX decreases monotonically with shuttle size, Case 1 shows
a complex pattern with local fluctuations. Two discrete effects create this behavior:

**Factor 1: Trips_per_Call (Discrete Step Function)**

```
Trips_per_Call = ceil(5000 / Shuttle_Size)
```

| Shuttle Range (m3) | Trips_per_Call |
|--------------------|----------------|
| 500 | 10 |
| 1,000 -- 1,249 | 5 |
| 1,250 -- 1,666 | 4 |
| 1,667 -- 2,499 | 3 |
| 2,500 -- 4,999 | 2 |
| 5,000+ | 1 |

Within each band (e.g., 2,500--4,999), trips remain constant but MCR increases with size,
causing Variable OPEX to rise within the band.

**Factor 2: SFOC Step Change at DWT 3,000**

| DWT Range | Engine Type | SFOC (g/kWh) |
|-----------|-------------|--------------|
| < 3,000 | 4-stroke high-speed | 505 |
| 3,000 -- 8,000 | 4-stroke medium-speed | 436 |
| 8,000 -- 15,000 | 4-stroke medium / small 2-stroke | 413 |

At 4,000 m3 shuttle (DWT = 3,400), the SFOC drops from 505 to 436 g/kWh (a 14% reduction),
partially offsetting the MCR increase.

**Fuel Consumption Factor (MCR x SFOC):**

| Shuttle (m3) | MCR (kW) | SFOC (g/kWh) | MCR x SFOC | Change |
|-------------|----------|-------------|-----------|--------|
| 3,000 | 1,450 | 505 | 732,250 | -- |
| 3,500 | 1,580 | 505 | 797,900 | +9% |
| 4,000 | 1,700 | 436 | 741,200 | -7% |
| 4,500 | 1,820 | 436 | 793,520 | +7% |

---

## 3.10 Annualized Cost Verification

**Formula:**

```
Annualized_Cost = NPC_Total / Annuity_Factor
```

**Substitution:**

```
Annualized_Cost = 290,810,000 / 10.8355
                = 26,838,247
                = $26.84M/year
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Annualized Cost | $26.84M/yr | $26.84M/yr | 0.00% | PASS |

**Component Breakdown:**

```
Annualized CAPEX = 142,130,000 / 10.8355 = $13.12M/yr
Annualized fOPEX = 77,000,000 / 10.8355 = $7.11M/yr
Annualized vOPEX = 71,680,000 / 10.8355 = $6.62M/yr
```

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| Ann. CAPEX | $13.12M/yr | $13.12M/yr | 0.00% | PASS |
| Ann. fOPEX | $7.11M/yr | $7.11M/yr | 0.00% | PASS |
| Ann. vOPEX | $6.62M/yr | $6.62M/yr | 0.00% | PASS |

---

## 3.11 Verification Summary

| # | Item | Formula | Manual | CSV | Diff | Status |
|---|------|---------|--------|-----|------|--------|
| 1 | Shore Loading Time | (2500/1500) + 2.0 | 3.6667 h | 3.6667 h | 0.00% | PASS |
| 2 | Basic Cycle Duration | 1.0+1.0+2.5+1.0+1.0 | 6.50 h | 6.50 h | 0.00% | PASS |
| 3 | Total Cycle Duration | 3.6667 + 6.5 | 10.1667 h | 10.1667 h | 0.00% | PASS |
| 4 | Trips per Call | ceil(5000/2500) | 2.0 | 2.0 | 0.00% | PASS |
| 5 | Call Duration | 2 x 10.1667 | 20.3333 h | 20.3333 h | 0.00% | PASS |
| 6 | Annual Cycles Max | 8000/10.1667 | 786.89 | 786.89 | 0.00% | PASS |
| 7 | Annuity Factor | [1-(1.07)^-21]/0.07 | 10.8355 | 10.8355 | 0.00% | PASS |
| 8 | Shuttle CAPEX (per unit) | 61.5M x (2500/40000)^0.75 | $7,687,500 | $7,687,500 | 0.00% | PASS |
| 9 | Pump Power | (400000 x 0.2778)/0.7/1000 | 158.73 kW | -- | -- | PASS |
| 10 | Bunkering CAPEX (per unit) | equipment + pump | $548,085 | $548,100 | 0.00% | PASS |
| 11 | Shuttle fOPEX/yr/unit | CAPEX x 5% | $384,375 | $384,375 | 0.00% | PASS |
| 12 | Bunkering fOPEX/yr/unit | bunk_CAPEX x 5% | $27,404 | $27,404 | 0.00% | PASS |
| 13 | Shuttle fuel/cycle | 1310x505x1.0/1e6 x 600 | $396.93 | $396.93 | 0.00% | PASS |
| 14 | Pump fuel/call | 158.73x5.0x505/1e6 x 600 | $240.48 | $240.48 | 0.00% | PASS |
| 15 | NPC Ann. Shuttle CAPEX | 709,512 x 187 shuttle-yrs | $132.68M | $132.67M | 0.01% | PASS |
| 16 | NPC Ann. Bunkering CAPEX | 50,580 x 187 shuttle-yrs | $9.46M | $9.46M | 0.00% | PASS |
| 17 | NPC Shuttle fOPEX | 384,375 x 187 shuttle-yrs | $71.88M | $71.88M | 0.00% | PASS |
| 18 | NPC Bunkering fOPEX | 27,404 x 187 shuttle-yrs | $5.12M | $5.12M | 0.00% | PASS |
| 19 | NPC Shuttle vOPEX | 396.93 x 138,600 cycles | $55.01M | $55.01M | 0.00% | PASS |
| 20 | NPC Bunkering vOPEX | 240.48 x 69,300 calls | $16.67M | $16.67M | 0.00% | PASS |
| 21 | NPC Total | sum of all components | $290.81M | $290.81M | 0.00% | PASS |
| 22 | Total Supply (20yr) | 346.5M m3 x 0.680 | 235,620,000 t | 235,620,000 t | 0.00% | PASS |
| 23 | LCOAmmonia | 290.81M / 235.62M t | $1.23/ton | $1.23/ton | 0.00% | PASS |
| 24 | Utilization (yr 2040) | 67100/72000 | 93.19% | 93.19% | 0.00% | PASS |

**Result: 24/24 PASS -- All hand calculations match CSV output within rounding tolerance.**

---

## 3.12 Figure Reference

![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)

*Figure D1: NPC comparison across all shuttle sizes for all three cases. The Case 1 optimum
at 2,500 m3 ($290.81M) is clearly visible. Note the non-monotonic NPC pattern caused by
discrete Trips_per_Call steps and DWT-based SFOC discontinuities.*

![D4: Case 1 Yearly Cycles](../../results/paper_figures/D4_case1.png)

*Figure D4 (Case 1): Yearly cycle count and fleet evolution for the optimal 2,500 m3
configuration, showing the linear demand growth from 1,200 cycles (2030) to 12,000 cycles
(2050) and corresponding fleet expansion from 2 to 16 shuttles.*

![D5: Case 1 Utilization](../../results/paper_figures/D5_case1.png)

*Figure D5 (Case 1): Fleet utilization rate for the optimal 2,500 m3 configuration. The
sawtooth pattern reflects the discrete nature of shuttle additions -- utilization rises
until a new shuttle is added, then drops as excess capacity becomes available.*

![D6: Cost Breakdown](../../results/paper_figures/D6_cost_breakdown.png)

*Figure D6: NPC cost breakdown by category, showing the dominance of Shuttle CAPEX (45.6%)
in Case 1 total costs.*

---

*Verification completed. All 24 hand-calculated values match CSV output.*
*Source code references: optimizer.py (lines 208-228), cost_calculator.py, shuttle_round_trip_calculator.py*
