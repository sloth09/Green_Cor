# Verification Report Reference Guide

Detailed guidelines and **exact formulas** for verification calculations.

---

## PART 1: EXACT CALCULATION FORMULAS

### 1.1 Base Parameters (from config files)

```yaml
# base.yaml
annualization_interest_rate: 0.07    # r = 7%
years: 21                            # n = 2050 - 2030 + 1
fuel_price_usd_per_ton: 600.0        # P_fuel
pump_delta_pressure_bar: 4.0         # delta_P
pump_efficiency: 0.7                 # eta
pump_power_cost_usd_per_kw: 2000.0   # C_pump_kw
shore_pump_rate_m3ph: 1500.0         # Q_shore
max_annual_hours: 8000               # H_max
setup_time_hours: 0.5                # t_setup (per connection)

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
CAPEX_shuttle = C_ref × (S / S_ref)^alpha
              = 61,500,000 × (Shuttle_Size / 40,000)^0.75
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
CAPEX = 61,500,000 × (1000/40000)^0.75
      = 61,500,000 × (0.025)^0.75
      = 61,500,000 × 0.062871577
      = 3,866,602 USD
```

---

### 1.4 Pump Power & CAPEX

**Pump Power Formula:**
```
P_pump = (delta_P × Q) / (eta × 3600 × 1000)
       = (delta_P_Pa × Q_m3h / 3600) / eta / 1000  [kW]

Where:
  delta_P_Pa = delta_P_bar × 100,000
  Q_m3h = pump flow rate in m3/h
  eta = pump efficiency
```

**Calculation for 1000 m3/h pump:**
```
delta_P_Pa = 4.0 × 100,000 = 400,000 Pa
Q_m3s = 1000 / 3600 = 0.27778 m3/s
P_pump = (400,000 × 0.27778) / 0.7 / 1000
       = 111,111 / 0.7 / 1000
       = 158.73 kW
```

**Pump CAPEX:**
```
CAPEX_pump = P_pump × C_pump_kw
           = 158.73 × 2000
           = 317,460 USD
```

---

### 1.5 Bunkering System CAPEX

**Formula:**
```
CAPEX_bunkering = CAPEX_shuttle_equipment + CAPEX_pump
                = (CAPEX_shuttle × equipment_ratio) + CAPEX_pump
                = (CAPEX_shuttle × 0.03) + CAPEX_pump
```

**Example for 1000 m3 shuttle:**
```
CAPEX_bunkering = (3,866,602 × 0.03) + 317,460
                = 115,998 + 317,460
                = 433,458 USD per shuttle
```

---

### 1.6 Fixed OPEX (Annual)

**Shuttle Fixed OPEX:**
```
fOPEX_shuttle = CAPEX_shuttle × fixed_opex_ratio
              = CAPEX_shuttle × 0.05
```

**Bunkering Fixed OPEX:**
```
fOPEX_bunkering = CAPEX_bunkering × fixed_opex_ratio
                = CAPEX_bunkering × 0.05
```

**Example for 1000 m3 shuttle (1 unit):**
```
fOPEX_shuttle = 3,866,602 × 0.05 = 193,330 USD/year
fOPEX_bunkering = 433,458 × 0.05 = 21,673 USD/year
```

---

### 1.7 Variable OPEX - Shuttle Fuel

**Formula:**
```
Fuel_per_cycle = MCR × SFOC × Travel_Time × Travel_Factor / 1,000,000  [tons]
Cost_per_cycle = Fuel_per_cycle × Fuel_Price

Where:
  MCR = engine power from mcr_map_kw [kW]
  SFOC = specific fuel consumption from sfoc_map [g/kWh]
  Travel_Time = one-way travel time [hours]
  Travel_Factor = 2.0 for round trip (Case 2), or per code logic (Case 1)
  Fuel_Price = 600 USD/ton
```

**MCR Map (from config):**

| Size (m3) | Case 1 MCR | Case 2 MCR |
|-----------|------------|------------|
| 500 | 380 | - |
| 1000 | 620 | - |
| 2500 | 1160 | 1160 |
| 5000 | 1810 | 1810 |
| 10000 | 2420 | 2420 |

**SFOC Map (by DWT):**

| Shuttle Size | DWT (= Size × 0.85) | SFOC (g/kWh) |
|--------------|---------------------|--------------|
| 500 | 425 | 505 |
| 1000 | 850 | 505 |
| 2500 | 2125 | 505 |
| 3500 | 2975 | 505 |
| 4000 | 3400 | 436 |
| 5000 | 4250 | 436 |
| 10000 | 8500 | 413 |
| 20000 | 17000 | 390 |
| 40000 | 34000 | 379 |

**Example - Case 1, 1000 m3 shuttle:**
```
MCR = 620 kW
SFOC = 505 g/kWh (DWT 850 < 3000)
Travel_Time = 1.0 hour (one-way)
Travel_Factor = 1.0 (for Case 1, code uses single direction)

Fuel_per_cycle = 620 × 505 × 1.0 × 1.0 / 1,000,000
               = 313,100 / 1,000,000
               = 0.3131 tons

Cost_per_cycle = 0.3131 × 600 = 187.86 USD
```

**Example - Case 2-2, 5000 m3 shuttle:**
```
MCR = 1810 kW
SFOC = 436 g/kWh (DWT 4250, range 3000-8000)
Travel_Time = 3.93 hours (one-way, Ulsan)
Travel_Factor = 2.0 (round trip)

Fuel_per_cycle = 1810 × 436 × 3.93 × 2.0 / 1,000,000
               = 6,202,834 / 1,000,000
               = 6.203 tons

Cost_per_cycle = 6.203 × 600 = 3,721.68 USD
```

---

### 1.8 Variable OPEX - Bunkering (Pump Fuel)

**Formula:**
```
Pumping_Time = Bunker_Volume / Pump_Rate  [hours]
Fuel_per_call = P_pump × SFOC_default × Pumping_Time / 1,000,000  [tons]
Cost_per_call = Fuel_per_call × Fuel_Price

Where:
  Bunker_Volume = 5000 m3 (per call)
  Pump_Rate = 1000 m3/h
  P_pump = 158.73 kW
  SFOC_default = 379 g/kWh (default for pump)
```

**Calculation:**
```
Pumping_Time = 5000 / 1000 = 5.0 hours
Fuel_per_call = 158.73 × 379 × 5.0 / 1,000,000
              = 300,794 / 1,000,000
              = 0.3008 tons

Cost_per_call = 0.3008 × 600 = 180.48 USD
```

---

### 1.9 Cycle Time Formulas

**Case 1 (Has Storage at Busan):**
```
Cycle = Shore_Loading + Travel_Out + Travel_Return + Setup_Total + Pumping_Total

Where:
  Shore_Loading = Shuttle_Size / 1500
  Travel_Out = 1.0 hour
  Travel_Return = 1.0 hour
  Setup_Total = 2 × (2 × setup_time) = 2 × 1.0 = 2.0 hours
  Pumping_Total = Shuttle_Size / Pump_Rate
```

**Example - Case 1, 1000 m3:**
```
Shore_Loading = 1000 / 1500 = 0.6667 hours
Travel_Out = 1.0 hour
Travel_Return = 1.0 hour
Setup_Total = 2.0 hours
Pumping_Total = 1000 / 1000 = 1.0 hour

Cycle = 0.6667 + 1.0 + 1.0 + 2.0 + 1.0 = 5.6667 hours
```

**Case 2 (No Storage - Direct Supply):**
```
Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)

Cycle = Shore_Loading + Travel_Out + Travel_Return + Setup_Total
      + Pumping_Total + Overhead

Where:
  Shore_Loading = Shuttle_Size / 1500
  Travel_Out = Distance / Speed (one-way)
  Travel_Return = Distance / Speed (one-way)
  Setup_Total = 2.0 hours (inbound + outbound)
  Pumping_Total = Vessels_per_Trip × (Bunker_Volume / Pump_Rate)
  Overhead = additional port operations time (varies)
```

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
Case 2: Trips_per_Call = 1 / Vessels_per_Trip
```

**Annual Supply:**
```
Annual_Supply_m3 = Annual_Cycles × Shuttle_Size (Case 1)
                 = Annual_Cycles × Vessels_per_Trip × Bunker_Volume (Case 2)
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

**LCOAmmonia:**
```
LCOAmmonia = NPC_Total / Total_Supply_20yr_ton
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
| 2 | Shuttle | CAPEX (per size) | 61.5M × (S/40000)^0.75 |
| 3 | Pump | Power (kW) | (delta_P × Q) / eta |
| 4 | Pump | CAPEX | Power × 2000 |
| 5 | Bunkering | CAPEX | Shuttle×3% + Pump |
| 6 | fOPEX | Shuttle | CAPEX × 5% |
| 7 | fOPEX | Bunkering | CAPEX × 5% |
| 8 | vOPEX | Shuttle fuel | MCR×SFOC×T×TF/1e6×600 |
| 9 | vOPEX | Pump fuel | P×SFOC×PT/1e6×600 |
| 10 | Time | Cycle duration | sum of components |
| 11 | Time | Annual cycles | 8000 / cycle |
| 12 | Final | NPC Total | sum of components |
| 13 | Final | LCOAmmonia | NPC / Supply |

### Per-Case Verification

For each case (Case 1, Case 2-1, Case 2-2):
1. Verify cycle time for optimal shuttle size
2. Verify CAPEX components for Year 2030
3. Verify OPEX components for Year 2030
4. Verify NPC total matches sum
5. Verify LCOAmmonia calculation

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

## PART 5: CHAPTER TEMPLATES

(Previous templates remain the same - see original reference.md)

---

## APPENDIX: Quick Reference

### Key Values

| Parameter | Value |
|-----------|-------|
| Annuity Factor | 10.8355 |
| Pump Power (1000 m3/h) | 158.73 kW |
| Pump CAPEX (1000 m3/h) | $317,460 |
| Shuttle CAPEX (1000 m3) | $3,866,602 |
| Shuttle CAPEX (5000 m3) | $12,928,780 |
| Shuttle CAPEX (10000 m3) | $21,743,480 |

### SFOC Quick Reference

| DWT Range | SFOC |
|-----------|------|
| < 3000 | 505 |
| 3000-8000 | 436 |
| 8000-15000 | 413 |
| 15000-30000 | 390 |
| > 30000 | 379 |
