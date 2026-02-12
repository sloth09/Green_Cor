# Verification Report Reference Guide

Detailed guidelines and **exact formulas** for verification calculations.

**WARNING: This file contains FORMULAS and CALCULATION PATTERNS only.**
**All parameter values and calculated results MUST be read from config files and CSV data.**
**Worked examples below are ILLUSTRATIVE -- always recalculate from current config.**

## Data Paths

**Primary data source (always read from here):**
- `results/deterministic/MILP_scenario_summary_{case_id}.csv`
- `results/deterministic/MILP_per_year_results_{case_id}.csv`

**Config files (always read for parameter verification):**
- `config/base.yaml` - common parameters
- `config/case_1.yaml` - Case 1 (Busan)
- `config/case_2_ulsan.yaml` - Case 2 (Ulsan)
- `config/case_3_yeosu.yaml` - Case 3 (Yeosu)

**Verification Bundle** (`results/verification_bundle/`): Self-contained package with copies of all verification-relevant data, figures, and reports.

---

## IMPORTANT: Always Read Config First

**NEVER hardcode parameter values from this reference.** Always read config files first
and use the values found there. This reference provides formulas and example calculations
for guidance only. If config values differ from this reference, **config is authoritative**.

---

## PART 1: EXACT CALCULATION FORMULAS

### 1.1 Base Parameters (from config files)

```yaml
# base.yaml (v7.0 current values)
annualization_interest_rate: 0.07    # r = 7%
years: 21                            # n = 2050 - 2030 + 1
fuel_price_usd_per_ton: 600.0        # P_fuel
pump_delta_pressure_bar: 4.0         # delta_P
pump_efficiency: 0.7                 # eta
pump_power_cost_usd_per_kw: 2000.0   # C_pump_kw
sfoc_g_per_kwh: 379.0                # SFOC_default (pump engine)

# Shore supply
shore_pump_rate_m3ph: 700.0          # Q_shore (v3.0: 1500 -> 700)
loading_time_fixed_hours: 4.0        # t_fixed (inbound 2h + outbound 2h)

# Operations
max_annual_hours: 8000               # H_max
setup_time_hours: 2.0                # t_setup per endpoint (v3.0: 0.5 -> 2.0, direct value)

# STS Pump
available_flow_rates: [500]          # Q_pump (v7.0: 1000 -> 500)

# Shuttle CAPEX parameters
ref_capex_usd: 61500000              # C_ref = $61.5M
ref_size_cbm: 40000                  # S_ref = 40,000 m3
capex_scaling_exponent: 0.75         # alpha

# OPEX ratios
shuttle_fixed_opex_ratio: 0.05       # 5% of CAPEX
shuttle_equipment_ratio: 0.03        # 3% of CAPEX
bunkering_fixed_opex_ratio: 0.05     # 5% of bunkering CAPEX
```

---

### 1.2 Annuity Factor

**Formula:**
```
AF = [1 - (1 + r)^(-n)] / r
```

**Calculation:**
```
AF = [1 - (1 + 0.07)^(-21)] / 0.07
   = [1 - (1.07)^(-21)] / 0.07
   = [1 - 0.241513] / 0.07
   = 0.758487 / 0.07
   = 10.8355
```

**Expected Value:** 10.8355

---

### 1.3 Shuttle CAPEX

**Formula:**
```
CAPEX_shuttle = C_ref x (S / S_ref)^alpha
              = 61,500,000 x (Shuttle_Size / 40,000)^0.75
```

**Calculation Examples:**

| Shuttle Size (m3) | Ratio | Ratio^0.75 | CAPEX (USD) |
|-------------------|-------|------------|-------------|
| 500 | 0.0125 | 0.03739 | 2,299,485 |
| 1000 | 0.025 | 0.06287 | 3,866,505 |
| 2500 | 0.0625 | 0.11180 | 6,875,700 |
| 5000 | 0.125 | 0.18803 | 11,563,845 |
| 10000 | 0.25 | 0.31623 | 19,448,145 |
| 50000 | 1.25 | 1.18034 | 72,590,910 |

**Exact calculation for 1000 m3:**
```
CAPEX = 61,500,000 x (1000/40000)^0.75
      = 61,500,000 x (0.025)^0.75
      = 61,500,000 x 0.062871577
      = 3,866,602 USD
```

---

### 1.4 Pump Power & CAPEX

**Pump Power Formula:**
```
P_pump = (delta_P_Pa x Q_m3s) / eta / 1000  [kW]

Where:
  delta_P_Pa = delta_P_bar x 100,000
  Q_m3s = Q_m3h / 3600
  eta = pump efficiency
```

**Calculation for 500 m3/h pump (v7.0):**
```
delta_P_Pa = 4.0 x 100,000 = 400,000 Pa
Q_m3s = 500 / 3600 = 0.13889 m3/s
P_pump = (400,000 x 0.13889) / 0.7 / 1000
       = 55,556 / 0.7 / 1000
       = 79.37 kW
```

**Pump CAPEX:**
```
CAPEX_pump = P_pump x C_pump_kw
           = 79.37 x 2000
           = 158,730 USD
```

---

### 1.5 Bunkering System CAPEX

**Formula:**
```
CAPEX_bunkering = CAPEX_shuttle_equipment + CAPEX_pump
                = (CAPEX_shuttle x equipment_ratio) + CAPEX_pump
                = (CAPEX_shuttle x 0.03) + CAPEX_pump
```

**Example for 1000 m3 shuttle (pump=500 m3/h):**
```
CAPEX_bunkering = (3,866,602 x 0.03) + 158,730
                = 115,998 + 158,730
                = 274,728 USD per shuttle
```

---

### 1.6 Fixed OPEX (Annual)

**Shuttle Fixed OPEX:**
```
fOPEX_shuttle = CAPEX_shuttle x fixed_opex_ratio
              = CAPEX_shuttle x 0.05
```

**Bunkering Fixed OPEX:**
```
fOPEX_bunkering = CAPEX_bunkering x fixed_opex_ratio
                = CAPEX_bunkering x 0.05
```

**Example for 1000 m3 shuttle (1 unit):**
```
fOPEX_shuttle = 3,866,602 x 0.05 = 193,330 USD/year
fOPEX_bunkering = 274,728 x 0.05 = 13,736 USD/year
```

---

### 1.7 Variable OPEX - Shuttle Fuel

**Formula:**
```
Fuel_per_cycle = MCR x SFOC x Travel_Time x Travel_Factor / 1,000,000  [tons]
Cost_per_cycle = Fuel_per_cycle x Fuel_Price

Where:
  MCR = engine power from mcr_map_kw [kW]
  SFOC = specific fuel consumption from sfoc_map [g/kWh]
  Travel_Time = one-way travel time [hours]
  Travel_Factor = 2.0 for round trip (Case 2/3), or per code logic (Case 1)
  Fuel_Price = 600 USD/ton
```

**MCR Map (from config, Power Law: 17.17 x DWT^0.566):**

| Size (m3) | DWT | Case 1 MCR (kW) | Case 2/3 MCR (kW) |
|-----------|-----|-----------------|-------------------|
| 500 | 425 | 520 | - |
| 1000 | 850 | 770 | - |
| 2500 | 2,125 | 1,310 | 1,310 |
| 5000 | 4,250 | 1,930 | 1,930 |
| 10000 | 8,500 | 2,990 | 2,990 |
| 50000 | 42,500 | - | 8,150 |

**SFOC Map (by DWT):**

| DWT Range | SFOC (g/kWh) | Shuttle Sizes |
|-----------|-------------|---------------|
| < 3,000 | 505 | 500 - 3,500 m3 |
| 3,000 - 8,000 | 436 | 4,000 - 9,000 m3 |
| 8,000 - 15,000 | 413 | 10,000 - 15,000 m3 |
| 15,000 - 30,000 | 390 | 20,000 - 35,000 m3 |
| > 30,000 | 379 | 40,000+ m3 |

**Example - Case 1, 1000 m3 shuttle:**
```
MCR = 770 kW (from case_1.yaml mcr_map)
SFOC = 505 g/kWh (DWT 850 < 3000)
Travel_Time = 1.0 hour (one-way)
Travel_Factor = 1.0 (Case 1 code logic)

Fuel_per_cycle = 770 x 505 x 1.0 x 1.0 / 1,000,000
               = 388,850 / 1,000,000
               = 0.3889 tons

Cost_per_cycle = 0.3889 x 600 = 233.31 USD
```

**Example - Case 2, 5000 m3 shuttle (Ulsan):**
```
MCR = 1930 kW (from case_2_ulsan.yaml mcr_map)
SFOC = 436 g/kWh (DWT 4250, range 3000-8000)
Travel_Time = 3.93 hours (one-way, 59nm / 15kn)
Travel_Factor = 2.0 (round trip)

Fuel_per_cycle = 1930 x 436 x 3.93 x 2.0 / 1,000,000
               = 6,618,290 / 1,000,000
               = 6.618 tons

Cost_per_cycle = 6.618 x 600 = 3,971.00 USD
```

---

### 1.8 Variable OPEX - Bunkering (Pump Fuel)

**Formula:**
```
Pumping_Time = Bunker_Volume / Pump_Rate  [hours]
Fuel_per_call = P_pump x SFOC_default x Pumping_Time / 1,000,000  [tons]
Cost_per_call = Fuel_per_call x Fuel_Price

Where:
  Bunker_Volume = 5000 m3 (per call)
  Pump_Rate = 500 m3/h (v7.0)
  P_pump = 79.37 kW
  SFOC_default = 379 g/kWh (default for pump engine)
```

**Calculation:**
```
Pumping_Time = 5000 / 500 = 10.0 hours
Fuel_per_call = 79.37 x 379 x 10.0 / 1,000,000
              = 300,812 / 1,000,000
              = 0.3008 tons

Cost_per_call = 0.3008 x 600 = 180.49 USD
```

**Note:** Pump fuel cost per call is nearly identical to v6.0 ($180.48) because
halving pump rate halves power but doubles time (P x T = constant for same volume).

---

### 1.9 Cycle Time Formulas

**Case 1 (Has Storage at Busan):**
```
Cycle = Shore_Loading + Travel_Out + Setup_In + Pumping + Setup_Out + Travel_Return

Where:
  Shore_Loading = Shuttle_Size / Q_shore + t_fixed = Shuttle_Size / 700 + 4.0
  Travel_Out = 1.0 hour
  Travel_Return = 1.0 hour
  Setup_In = setup_time = 2.0 hours
  Setup_Out = setup_time = 2.0 hours
  Pumping = Shuttle_Size / Pump_Rate = Shuttle_Size / 500
```

**Example - Case 1, 1000 m3 (optimal in v7.0):**
```
Shore_Loading = 1000 / 700 + 4.0 = 1.4286 + 4.0 = 5.4286 hours
Travel_Out = 1.0 hour
Setup_In = 2.0 hours
Pumping = 1000 / 500 = 2.0 hours
Setup_Out = 2.0 hours
Travel_Return = 1.0 hour

Cycle = 5.4286 + 1.0 + 2.0 + 2.0 + 2.0 + 1.0 = 13.4286 hours
```

**Case 1 Call Duration (multiple trips per call):**
```
Trips_per_Call = ceil(Bunker_Volume / Shuttle_Size)
Call_Duration = Trips_per_Call x Cycle_Duration

Example (1000 m3 shuttle, 5000 m3 bunker):
  Trips = ceil(5000 / 1000) = 5
  Call = 5 x 13.4286 = 67.14 hours
```

**Case 2/3 (No Storage - Direct Supply from Ulsan/Yeosu):**
```
Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)

Cycle = Shore_Loading + Travel_Out + Setup_In
      + VpT x (Pumping_per_Vessel + Setup_Out + Movement)
      + Travel_Return

Where:
  Shore_Loading = Shuttle_Size / 700 + 4.0
  Travel_Out = Distance / Speed (one-way)
  Travel_Return = Distance / Speed (one-way)
  Setup_In = setup_time = 2.0 hours (busan port entry)
  Pumping_per_Vessel = Bunker_Volume / Pump_Rate = 5000 / 500 = 10.0 hours
  Setup_Out = setup_time = 2.0 hours (per vessel or port exit)
  Movement = inter-vessel movement time
```

**Example - Case 2, 5000 m3 shuttle (Ulsan, VpT=1):**
```
Shore_Loading = 5000 / 700 + 4.0 = 11.14 hours
Travel_Out = 59 / 15 = 3.93 hours
Setup_In = 2.0 hours
Pumping = 5000 / 500 = 10.0 hours
Setup_Out = 2.0 hours
Travel_Return = 3.93 hours

Cycle = 11.14 + 3.93 + 2.0 + 10.0 + 2.0 + 3.93 = ~36.00 hours
(Exact value from CSV: verify against MILP_scenario_summary)
```

---

### 1.9.1 Cycle Timeline Diagram (REQUIRED per case chapter)

Each case chapter MUST include a visual timeline diagram for the optimal shuttle size.
This shows the reader exactly what happens during one complete cycle.

**Template - Case 1 (1000 m3 optimal, pump=500):**

```
=== Case 1: Single Cycle Timeline (1,000 m3 Shuttle, 500 m3/h Pump) ===

Phase                  Duration    Cumulative
---------------------  ----------  ----------
Shore Loading          5.43 h      0 -> 5.43
Travel Outbound        1.00 h      5.43 -> 6.43
Setup Inbound          2.00 h      6.43 -> 8.43
Pumping                2.00 h      8.43 -> 10.43
Setup Outbound         2.00 h      10.43 -> 12.43
Travel Return          1.00 h      12.43 -> 13.43
---------------------  ----------  ----------
TOTAL CYCLE            13.43 h

Timeline:
|===Shore Loading===|==Travel==|==Setup In==|==Pumping==|==Setup Out==|==Travel==|
|      5.43 h       |  1.00 h  |   2.00 h   |  2.00 h   |   2.00 h    |  1.00 h  |
|<----------------------- Total Cycle: 13.43 h ---------------------------------->|
```

**Template - Case 2 (5000 m3 optimal, VpT=1, pump=500):**

```
=== Case 2: Single Cycle Timeline (5,000 m3 Shuttle, 500 m3/h Pump) ===

Phase                        Duration    Cumulative
---------------------------  ----------  ----------
Shore Loading                11.14 h     0 -> 11.14
Travel Outbound               3.93 h     11.14 -> 15.07
Setup Inbound                 2.00 h     15.07 -> 17.07
  Vessel 1: Pumping          10.00 h     17.07 -> 27.07
Setup Outbound                2.00 h     27.07 -> 29.07
Travel Return                 3.93 h     29.07 -> 33.00
---------------------------  ----------  ----------
TOTAL CYCLE                  ~36.00 h    (verify exact from CSV)
```

Key requirements:
- Show EVERY time component with actual values (not formulas)
- Show cumulative time progression
- Include the ASCII box timeline at the bottom
- For Case 2/3 with VpT>1, indent per-vessel operations
- **Always verify timeline total matches CSV Cycle_Duration_hr**

---

### 1.10 Annual Calculations

**Annual Cycles Maximum:**
```
Annual_Cycles_Max = floor(H_max / Cycle_Duration)
                  = floor(8000 / Cycle_Duration)
```

**Trips per Call:**
```
Case 1: Trips_per_Call = ceil(Bunker_Volume / Shuttle_Size)
Case 2/3: Trips_per_Call = 1 (when VpT >= 1)
```

**Annual Supply:**
```
Annual_Supply_m3 = Annual_Cycles x Shuttle_Size (Case 1)
                 = Annual_Cycles x Vessels_per_Trip x Bunker_Volume (Case 2/3)
```

---

### 1.11 NPC Calculation

**Total NPC over 21 years:**
```
NPC_Total = NPC_Shuttle_CAPEX + NPC_Bunkering_CAPEX + NPC_Terminal_CAPEX
          + NPC_Shuttle_fOPEX + NPC_Bunkering_fOPEX + NPC_Terminal_fOPEX
          + NPC_Shuttle_vOPEX + NPC_Bunkering_vOPEX + NPC_Terminal_vOPEX

Where each NPC component = sum of yearly costs (no discounting when discount_rate = 0)
```

**Annualized CAPEX (in CSV):**
```
NPC_Annualized_CAPEX = sum over all years of (Yearly_Asset_Value / AF)
```

**LCOA (Levelized Cost of Ammonia):**
```
LCOA = NPC_Total / Total_Supply_20yr_ton
```

---

## PART 2: VERIFICATION PROCESS

### Step 1: Read CSV Values

Read the following from CSV:
- `MILP_scenario_summary_case_*.csv` for NPC totals
- `MILP_per_year_results_case_*.csv` for yearly breakdowns

### Step 2: Manual Calculation

For EACH verified item:
1. Write the formula
2. Substitute values from config
3. Show step-by-step calculation
4. Get final result

### Step 3: Compare

Create comparison table:
```
| Item | Manual Calc | CSV Value | Diff (%) | Status |
|------|-------------|-----------|----------|--------|
| ... | ... | ... | ... | PASS/FAIL |
```

**Pass Criteria:**
- Diff < 1%: PASS
- Diff 1-5%: REVIEW (explain difference)
- Diff > 5%: FAIL (investigate)

### Step 4: Investigate Discrepancies

If FAIL:
1. Check formula interpretation
2. Check parameter source
3. Check rounding differences
4. Document root cause
5. Re-calculate if needed

---

## PART 3: REQUIRED VERIFICATION ITEMS

### Essential Items (Must Verify)

| # | Category | Item | Formula |
|---|----------|------|---------|
| 1 | Economic | Annuity Factor | [1-(1+r)^(-n)]/r |
| 2 | Shuttle | CAPEX (per size) | 61.5M x (S/40000)^0.75 |
| 3 | Pump | Power (kW) | (delta_P x Q) / eta |
| 4 | Pump | CAPEX | Power x 2000 |
| 5 | Bunkering | CAPEX | Shuttle x 3% + Pump |
| 6 | fOPEX | Shuttle | CAPEX x 5% |
| 7 | fOPEX | Bunkering | CAPEX x 5% |
| 8 | vOPEX | Shuttle fuel | MCR x SFOC x T x TF / 1e6 x 600 |
| 9 | vOPEX | Pump fuel | P x SFOC x PT / 1e6 x 600 |
| 10 | Time | Cycle duration | sum of components |
| 11 | Time | Annual cycles | 8000 / cycle |
| 12 | Final | NPC Total | sum of components |
| 13 | Final | LCOA | NPC / Supply |

### Per-Case Verification

For each case (Case 1, Case 2, Case 3):
1. Verify cycle time for optimal shuttle size
2. Verify CAPEX components for Year 2030
3. Verify OPEX components for Year 2030
4. Verify NPC total matches sum
5. Verify LCOA calculation

---

## PART 4: OUTPUT FORMAT

### Verification Table Format

```markdown
## X.Y Item Verification

### Formula
[Write exact formula]

### Manual Calculation
[Show step-by-step calculation]

### Comparison

| Item | Manual | CSV | Diff | Status |
|------|--------|-----|------|--------|
| [item] | [value] | [value] | [%] | [PASS/FAIL] |

### Notes
[Any observations or discrepancies]
```

---

## PART 5: TERMINOLOGY AND CONVENTIONS

- **LCOA**: Always use "LCOA" (Levelized Cost of Ammonia). Never "LCO" or "LCOAmmonia".
- **Case order**: Always Case 1 (Busan) -> Case 2 (Ulsan) -> Case 3 (Yeosu)
- **Costs**: USD millions (USDm) unless otherwise noted
- **Time**: hours (h), with 2-4 decimal places
- **No emojis**: Use [PASS], [FAIL], [OK] patterns only
- **Discount rate**: 0% (no time value discounting)
- **Annualization rate**: 7% (for asset annualization only)

---

## APPENDIX: Notes

### SFOC Quick Reference (from config sfoc_map)

| DWT Range | SFOC (g/kWh) |
|-----------|-------------|
| < 3000 | 505 |
| 3000-8000 | 436 |
| 8000-15000 | 413 |
| 15000-30000 | 390 |
| > 30000 | 379 |

### How to Extract Key Values

All calculated values (annuity factor, pump power, shuttle CAPEX, optimal configurations)
must be computed fresh from config parameters. Never copy values from this reference.

1. **Annuity Factor**: Calculate from `annualization.rate` and `annualization.period_years` in config
2. **Pump Power/CAPEX**: Calculate from `pump_delta_pressure_bar`, `pump_efficiency`, and `pump_power_cost_usd_per_kw`
3. **Shuttle CAPEX**: Calculate from `shuttle_capex` section in config for each shuttle size
4. **Optimal Configurations**: Read from `MILP_scenario_summary_{case_id}.csv`, find min `NPC_Total_USDm` row

### Version History

| Version | Pump Rate | Shore Pump | Setup Time | Key Change |
|---------|-----------|------------|------------|------------|
| v5.1 | 1000 m3/h | 1500 m3/h | 0.5 h | Original |
| v6.0 | 1000 m3/h | 700 m3/h | 2.0 h | Shore pump + setup corrected |
| v7.0 | 500 m3/h | 700 m3/h | 2.0 h | STS pump halved |
