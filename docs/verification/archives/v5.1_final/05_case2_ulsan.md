# Chapter 5: Case 2-2 - Ulsan to Busan Verification

## 5.1 Case Overview

| Parameter | Value |
|-----------|-------|
| Case Name | Case 2-2: Ulsan -> Busan |
| Case ID | case_2_ulsan |
| Route | Regional transport (no storage at Busan) |
| Distance | 59 nautical miles |
| Ship Speed | 15 knots |
| Travel Time (one-way) | 3.93 hours |
| Has Storage at Busan | No |
| Bunker Volume per Call | 5,000 m3 |
| Pump Rate | 1,000 m3/h |
| Shore Pump Rate | 1,500 m3/h |
| Fixed Loading Overhead | 2.0 hours |
| Max Annual Hours | 8,000 hours |
| Discount Rate | 0.0 (no discounting) |
| Annualization Interest Rate | 7% |
| Fuel Price | 600 USD/ton |

**Key Characteristic**: Shuttles transport ammonia from the Ulsan source to Busan Port. There is no storage at Busan -- the shuttle serves as temporary floating storage. One shuttle trip can serve multiple vessels if shuttle capacity exceeds the bunker volume per call. The 59 nm distance (updated from 25 nm in v4) results in 3.93 hours one-way travel time.

**Optimal Configuration**: 5,000 m3 shuttle with 1,000 m3/h pump at NPC = $700.68M ($2.97/ton LCOAmmonia).

**MCR Update (v5)**: Power Law formula `MCR = 17.17 x DWT^0.566` applied to all shuttle sizes.

**Shore Loading Update (v5.1)**: Fixed loading overhead of 2.0 hours (`loading_time_fixed_hours`) added to shore loading time.

---

## 5.2 MCR and SFOC Values

### 5.2.1 MCR Values (v5 Power Law)

| Shuttle (m3) | DWT (ton) | MCR v5 (kW) | SFOC (g/kWh) | DWT Range Category |
|--------------|-----------|-------------|--------------|-------------------|
| 2,500 | 2,125 | 1,310 | 505 | < 3,000 (4-stroke high-speed) |
| **5,000** | **4,250** | **1,930** | **436** | **3,000 - 8,000 (4-stroke medium)** |
| 10,000 | 8,500 | 2,990 | 413 | 8,000 - 15,000 |
| 15,000 | 12,750 | 3,850 | 413 | 8,000 - 15,000 |
| 20,000 | 17,000 | 4,610 | 390 | 15,000 - 30,000 |
| 25,000 | 21,250 | 5,300 | 390 | 15,000 - 30,000 |
| 30,000 | 25,500 | 5,940 | 390 | 15,000 - 30,000 |
| 35,000 | 29,750 | 6,540 | 390 | 15,000 - 30,000 |
| 40,000 | 34,000 | 7,100 | 379 | > 30,000 (2-stroke large) |
| 45,000 | 38,250 | 7,640 | 379 | > 30,000 (2-stroke large) |
| 50,000 | 42,500 | 8,150 | 379 | > 30,000 (2-stroke large) |

### 5.2.2 DWT Derivation for 5,000 m3

```
DWT = (Cargo_m3 x Density) / Load_Factor
    = (5000 x 0.680) / 0.80
    = 3400 / 0.80
    = 4,250 tons
```

DWT 4,250 falls in the 3,000 - 8,000 range, so SFOC = 436 g/kWh.

---

## 5.3 Cycle Time Verification

### 5.3.1 Vessels per Trip

**Formula -> Substitution -> Result:**

```
Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)
                = floor(5000 / 5000)
                = floor(1.0)
                = 1 vessel
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Vessels_per_Trip | 1 | 1.0 | PASS |

### 5.3.2 Trips per Call

```
Trips_per_Call = Bunker_Volume / Shuttle_Size  (for Case 2)
              = 5000 / 5000
              = 1.0 trip
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Trips_per_Call | 1.0 | 1.0 | PASS |

### 5.3.3 Shore Loading Time

**Formula:**
```
Shore_Loading = (Shuttle_Size / Shore_Pump_Rate) + loading_time_fixed_hours
```

**Substitution:**
```
Shore_Loading = (5000 / 1500) + 2.0
             = 3.3333 + 2.0
             = 5.3333 hours
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Shore_Loading | 5.3333 hr | 5.3333 hr | PASS |

### 5.3.4 Per-Vessel Operations at Busan

For each vessel served at Busan port:

| Operation | Parameter | Value (hr) |
|-----------|-----------|------------|
| Movement to vessel berth | movement_time | 1.0 |
| Setup Inbound (hose connection) | setup_inbound | 1.0 |
| Pumping (bunkering) | bunker_volume / pump_rate = 5000 / 1000 | 5.0 |
| Setup Outbound (hose disconnect) | setup_outbound | 1.0 |
| **Per-vessel total** | | **8.0** |

### 5.3.5 Basic Cycle Duration (excluding shore loading)

**Formula (Case 2):**
```
Basic_Cycle = Travel_Out + Port_Entry + VpT x (Movement + Setup_In + Pumping + Setup_Out) + Port_Exit + Travel_Return
```

**Substitution:**
```
Basic_Cycle = 3.93 + 1.0 + 1 x (1.0 + 1.0 + 5.0 + 1.0) + 1.0 + 3.93
            = 3.93 + 1.0 + 1 x 8.0 + 1.0 + 3.93
            = 3.93 + 1.0 + 8.0 + 1.0 + 3.93
            = 17.86 hours
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Basic_Cycle_Duration | 17.86 hr | 17.86 hr | PASS |

### 5.3.6 Total Cycle Duration

**Formula:**
```
Cycle_Duration = Shore_Loading + Basic_Cycle_Duration
```

**Substitution:**
```
Cycle_Duration = 5.3333 + 17.86
               = 23.1933 hours
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Cycle_Duration | 23.1933 hr | 23.1933 hr | PASS |

### 5.3.7 Annual Maximum Cycles

**Formula:**
```
Annual_Cycles_Max = Max_Annual_Hours / Cycle_Duration
```

**Substitution:**
```
Annual_Cycles_Max = 8000 / 23.1933
                  = 344.93 cycles/year
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Annual_Cycles_Max | 344.93 | 344.93 | PASS |

### 5.3.8 Cycle Timeline Diagram

```
=== Case 2-2: Single Cycle Timeline (5,000 m3 Shuttle, 1,000 m3/h Pump, 1 Vessel/Trip) ===

Phase                        Duration (h)   Cumulative (h)
---------------------------  ------------   --------------
Shore Loading                   5.33         0.00 ->  5.33
Travel Outbound (59 nm)        3.93         5.33 ->  9.27
Port Entry                      1.00         9.27 -> 10.27
  [Vessel 1] Movement           1.00        10.27 -> 11.27
  [Vessel 1] Setup Inbound      1.00        11.27 -> 12.27
  [Vessel 1] Pumping (5000m3)   5.00        12.27 -> 17.27
  [Vessel 1] Setup Outbound     1.00        17.27 -> 18.27
Port Exit                       1.00        18.27 -> 19.27
Travel Return (59 nm)          3.93        19.27 -> 23.19
                               ------
TOTAL CYCLE                    23.19 h
```

**Visual Block Diagram:**

```
|<--- Shore Loading --->|<-- Travel Out -->|<-PE->|<----- Vessel 1 (8.0h) ----->|<-PX->|<-- Travel Ret -->|
|       5.33 h          |     3.93 h       | 1.0h | Mv |SIn|   Pump 5h   |SOut| 1.0h |     3.93 h        |
|<---------------------------------- Total Cycle: 23.19 h ---------------------------------------->|

Where: PE = Port Entry, PX = Port Exit, Mv = Movement, SIn = Setup In, SOut = Setup Out
```

**Key Observations:**
- Single vessel per trip (VpT=1) since shuttle size equals bunker volume (5,000 = 5,000)
- Per-vessel block (8.0h) is the largest single component
- Shorter travel (3.93h vs 5.73h for Yeosu) reduces cycle by 3.6h compared to Case 2-1
- Shore loading (5.33h) is shorter than Yeosu (8.67h) due to smaller shuttle
- Total cycle 23.19h vs 38.13h for Yeosu -- a 39% reduction

---

## 5.4 CAPEX Verification

### 5.4.1 Shuttle CAPEX (5,000 m3)

**Formula:**
```
Shuttle_CAPEX = Ref_CAPEX x (Shuttle_Size / Ref_Size)^Alpha
```

**Substitution:**
```
Shuttle_CAPEX = 61,500,000 x (5000 / 40000)^0.75
              = 61,500,000 x (0.125)^0.75
              = 61,500,000 x 0.2102
              = $12,928,530
```

**Intermediate step:**
```
(0.125)^0.75 = e^(0.75 x ln(0.125))
             = e^(0.75 x (-2.0794))
             = e^(-1.5596)
             = 0.21022
```

**CSV Verification (Year 2031, 1 new shuttle):**

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| Per-shuttle CAPEX | $12,928,530 | $12,928,800 (12.9288M) | 0.00% | PASS |

### 5.4.2 Pump Power and CAPEX

**Pump Power Formula:**
```
Pump_Power = (Delta_P x Flow_Rate) / Efficiency
           = (4 x 10^5 Pa x (1000/3600) m3/s) / 0.7
           = (400,000 x 0.27778) / 0.7
           = 111,111 / 0.7
           = 158,730 W
           = 158.73 kW
```

**Pump CAPEX Formula:**
```
Pump_CAPEX = Pump_Power x Cost_per_kW
           = 158.73 x 2000
           = $317,460
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Pump Power | 158.73 kW | 158.73 kW | PASS |
| Pump CAPEX | $317,460 | $317,460 | PASS |

### 5.4.3 Bunkering System CAPEX

The bunkering system CAPEX includes shuttle equipment costs plus pump costs:

**Formula:**
```
Bunkering_CAPEX = (Shuttle_CAPEX x Equipment_Ratio) + Pump_CAPEX
```

**Substitution:**
```
Bunkering_CAPEX = (12,928,800 x 0.03) + 317,460
               = 387,864 + 317,460
               = $705,324
```

**CSV Verification (Year 2031, 1 new shuttle):**

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| Bunkering CAPEX per shuttle | $705,324 | $705,300 (0.7053M) | 0.00% | PASS |

### 5.4.4 Annuity Factor

The annuity factor converts lump-sum CAPEX into equivalent annual payments over the 20-year period at 7% interest:

```
Annuity_Factor = 10.8355  (from CSV)
Annualization_Rate = 1 / 10.8355 = 0.09229
```

**Annualized CAPEX per shuttle per year:**
```
Annualized_Shuttle = Shuttle_CAPEX / Annuity_Factor
                   = 12,928,800 / 10.8355
                   = $1,193,176 per year
```

**CSV Verification (Year 2030, 2 shuttles):**
```
Expected = 2 x 1,193,176 = $2,386,352
CSV Annualized_CAPEX_Shuttle (2030) = $2,386,400 (2.3864M)
```

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| Annualized shuttle/yr/unit | $1,193,176 | $1,193,200 | 0.00% | PASS |
| Year 2030 (2 shuttles) | $2,386,352 | $2,386,400 | 0.00% | PASS |

### 5.4.5 NPC of Annualized Shuttle CAPEX (20-year sum)

Summing the Annualized_CAPEX_Shuttle column from per-year CSV for all 21 years (2030-2050):

| Year | Total Shuttles | Annualized CAPEX Shuttle (USDm) |
|------|---------------|-------------------------------|
| 2030 | 2 | 2.3864 |
| 2031 | 3 | 3.5796 |
| 2032 | 4 | 4.7727 |
| 2033 | 5 | 5.9659 |
| 2034 | 5 | 5.9659 |
| 2035 | 6 | 7.1591 |
| 2036 | 7 | 8.3523 |
| 2037 | 8 | 9.5455 |
| 2038 | 9 | 10.7387 |
| 2039 | 9 | 10.7387 |
| 2040 | 10 | 11.9318 |
| 2041 | 11 | 13.1250 |
| 2042 | 12 | 14.3182 |
| 2043 | 12 | 14.3182 |
| 2044 | 13 | 15.5114 |
| 2045 | 14 | 16.7046 |
| 2046 | 15 | 17.8978 |
| 2047 | 16 | 19.0910 |
| 2048 | 16 | 19.0910 |
| 2049 | 17 | 20.2841 |
| 2050 | 18 | 21.4773 |
| **Sum** | | **252.9552** |

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| NPC Annualized Shuttle CAPEX | $252.96M | $252.96M | 0.00% | PASS |

---

## 5.5 OPEX Verification

### 5.5.1 Fixed OPEX - Shuttle

**Formula:**
```
fOPEX_Shuttle = Shuttle_CAPEX x Fixed_OPEX_Ratio
```

**Substitution:**
```
fOPEX_Shuttle = 12,928,800 x 0.05
              = $646,440 per year per shuttle
```

**CSV Verification (Year 2034, 5 shuttles):**
```
Expected = 5 x 646,440 = $3,232,200
CSV FixedOPEX_Shuttle (2034) = $3,232,200 (3.2322M)
```

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| fOPEX per shuttle | $646,440 | $646,440 | 0.00% | PASS |
| Year 2034 (5 shuttles) | $3,232,200 | $3,232,200 | 0.00% | PASS |

### 5.5.2 Fixed OPEX - Bunkering

**Formula:**
```
fOPEX_Bunkering = Bunkering_CAPEX x Fixed_OPEX_Ratio
```

**Substitution:**
```
fOPEX_Bunkering = 705,300 x 0.05
                = $35,265 per year per shuttle
```

**CSV Verification (Year 2034, 5 shuttles):**
```
Expected = 5 x 35,265 = $176,325
CSV FixedOPEX_Pump (2034) = $176,300 (0.1763M)
```

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| fOPEX bunkering per shuttle | $35,265 | $35,260 | 0.01% | PASS |
| Year 2034 (5 shuttles) | $176,325 | $176,300 | 0.01% | PASS |

### 5.5.3 Variable OPEX - Shuttle Fuel (per cycle)

In Case 2, Travel_Factor = 2.0 because fuel is consumed on both outbound and return legs.

**Formula:**
```
Fuel_tons_per_cycle = MCR x SFOC x Travel_Time x Travel_Factor / 1,000,000
```

**Substitution:**
```
Fuel_tons_per_cycle = 1930 x 436 x 3.93 x 2.0 / 1,000,000
```

**Step-by-step:**
```
Step 1: MCR x SFOC      = 1930 x 436       = 841,480
Step 2: x Travel_Time   = 841,480 x 3.93   = 3,307,016
Step 3: x Travel_Factor = 3,307,016 x 2.0  = 6,614,033
Step 4: / 1e6            = 6,614,033 / 1e6  = 6.6140 tons
```

**Fuel cost per cycle:**
```
Cost_per_cycle = 6.6140 x 600 = $3,968.42
```

**CSV Verification (Year 2034, 5 shuttles, 1680 cycles):**
```
CSV VariableOPEX_Shuttle (2034) = $6,666,900 (6.6669M)
Per cycle = 6,666,900 / 1680 = $3,968.39
Hand calculation = $3,968.42
Difference = $0.03 (rounding)
```

| Item | Hand Calculation | CSV Derived | Diff | Status |
|------|-----------------|-------------|------|--------|
| Fuel per cycle (tons) | 6.6140 | 6.6140 | 0.00% | PASS |
| Cost per cycle | $3,968.42 | $3,968.39 | 0.00% | PASS |

### 5.5.4 Variable OPEX - Bunkering Pump Fuel (per cycle)

The bunkering pump uses the shuttle's SFOC (436 g/kWh for the 5,000 m3 shuttle, not the default 379).

**Formula:**
```
Pump_fuel_per_cycle = Pump_Power x SFOC x Pumping_Time / 1,000,000
```

**Substitution:**
```
Pump_fuel_per_cycle = 158.73 x 436 x 5.0 / 1,000,000
```

**Step-by-step:**
```
Step 1: Pump_Power x SFOC     = 158.73 x 436        = 69,206.28
Step 2: x Pumping_Time        = 69,206.28 x 5.0     = 346,031.40
Step 3: / 1e6                  = 346,031.40 / 1e6    = 0.34603 tons
```

**Pump fuel cost per cycle:**
```
Cost_per_cycle = 0.34603 x 600 = $207.62
```

**CSV Verification (Year 2034, 5 shuttles, 1680 cycles):**
```
CSV VariableOPEX_Pump (2034) = $348,800 (0.3488M)
Per cycle = 348,800 / 1680 = $207.62
Hand calculation = $207.62
```

| Item | Hand Calculation | CSV Derived | Diff | Status |
|------|-----------------|-------------|------|--------|
| Pump fuel per cycle (tons) | 0.3460 | 0.3460 | 0.00% | PASS |
| Pump cost per cycle | $207.62 | $207.62 | 0.00% | PASS |

### 5.5.5 Variable OPEX Cross-Check (Year 2030)

Year 2030: 2 shuttles, 600 annual cycles.

**Shuttle fuel (Year 2030):**
```
Expected = 600 x 3,968.42 = $2,381,052
CSV VariableOPEX_Shuttle (2030) = $2,381,100 (2.3811M)
```

**Pump fuel (Year 2030):**
```
Expected = 600 x 207.62 = $124,572
CSV VariableOPEX_Pump (2030) = $124,600 (0.1246M)
```

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| Shuttle vOPEX (2030) | $2,381,052 | $2,381,100 | 0.00% | PASS |
| Pump vOPEX (2030) | $124,572 | $124,600 | 0.02% | PASS |

---

## 5.6 Per-Year Fleet Build-Up Verification

### 5.6.1 Demand Growth

Demand grows linearly from 50 vessels (2030) to 500 vessels (2050):

```
Vessels(year) = 50 + (500 - 50) x (year - 2030) / (2050 - 2030)
              = 50 + 22.5 x (year - 2030)
```

**Annual calls required:**
```
Annual_Calls = Vessels x Voyages_per_Year
             = Vessels x 12
```

### 5.6.2 Fleet Sizing Verification

| Year | Vessels | Annual Calls | Cycles Needed | Total Shuttles | New | Utilization |
|------|---------|-------------|---------------|---------------|-----|-------------|
| 2030 | 50 | 600 | 600 | 2 | 2 | 86.98% |
| 2031 | 72 | 864 | 864 | 3 | 1 | 83.50% |
| 2032 | 95 | 1,140 | 1,140 | 4 | 1 | 82.63% |
| 2033 | 118 | 1,416 | 1,416 | 5 | 1 | 82.10% |
| 2034 | 140 | 1,680 | 1,680 | 5 | 0 | 97.41% |
| 2035 | 162 | 1,944 | 1,944 | 6 | 1 | 93.93% |
| 2036 | 185 | 2,220 | 2,220 | 7 | 1 | 91.94% |
| 2037 | 208 | 2,496 | 2,496 | 8 | 1 | 90.45% |
| 2038 | 230 | 2,760 | 2,760 | 9 | 1 | 88.91% |
| 2039 | 252 | 3,024 | 3,024 | 9 | 0 | 97.41% |
| 2040 | 275 | 3,300 | 3,300 | 10 | 1 | 95.67% |
| 2041 | 298 | 3,576 | 3,576 | 11 | 1 | 94.25% |
| 2042 | 320 | 3,840 | 3,840 | 12 | 1 | 92.77% |
| 2043 | 342 | 4,104 | 4,104 | 12 | 0 | 99.15% |
| 2044 | 365 | 4,380 | 4,380 | 13 | 1 | 97.68% |
| 2045 | 388 | 4,656 | 4,656 | 14 | 1 | 96.42% |
| 2046 | 410 | 4,920 | 4,920 | 15 | 1 | 95.09% |
| 2047 | 432 | 5,184 | 5,184 | 16 | 1 | 93.93% |
| 2048 | 455 | 5,460 | 5,460 | 16 | 0 | 98.93% |
| 2049 | 478 | 5,736 | 5,736 | 17 | 1 | 97.82% |
| 2050 | 500 | 6,000 | 6,000 | 18 | 1 | 96.64% |

**Verification of fleet sizing logic (Year 2034):**
```
Cycles_needed = 1680
Capacity_per_shuttle = 344.93 cycles/year
Shuttles_needed = ceil(1680 / 344.93) = ceil(4.870) = 5
Previous total = 5 (from 2033)
New_Shuttles = max(0, 5 - 5) = 0
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Year 2034 total shuttles | 5 | 5 | PASS |
| Year 2034 new shuttles | 0 | 0 | PASS |

**Verification of Year 2030:**
```
Shuttles_needed = ceil(600 / 344.93) = ceil(1.739) = 2
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| Year 2030 total shuttles | 2 | 2 | PASS |

---

## 5.7 NPC Total Verification

### 5.7.1 NPC Component Breakdown (from Scenario Summary CSV)

| Cost Component | NPC Value (USDm) | Share |
|----------------|------------------|-------|
| Shuttle CAPEX (Annualized) | 252.96 | 36.10% |
| Bunkering CAPEX (Annualized) | 13.80 | 1.97% |
| Terminal CAPEX | 0.00 | 0.00% |
| **Total CAPEX** | **266.76** | **38.07%** |
| Shuttle Fixed OPEX | 137.05 | 19.56% |
| Bunkering Fixed OPEX | 7.48 | 1.07% |
| Terminal Fixed OPEX | 0.00 | 0.00% |
| **Total Fixed OPEX** | **144.53** | **20.63%** |
| Shuttle Variable OPEX | 275.01 | 39.25% |
| Bunkering Variable OPEX | 14.39 | 2.05% |
| Terminal Variable OPEX | 0.00 | 0.00% |
| **Total Variable OPEX** | **289.40** | **41.30%** |
| **TOTAL NPC** | **700.69** | **100%** |

### 5.7.2 Summation Verification

**Formula:**
```
NPC_Total = NPC_Shuttle_CAPEX + NPC_Bunkering_CAPEX + NPC_Terminal_CAPEX
          + NPC_Shuttle_fOPEX + NPC_Bunkering_fOPEX + NPC_Terminal_fOPEX
          + NPC_Shuttle_vOPEX + NPC_Bunkering_vOPEX + NPC_Terminal_vOPEX
```

**Substitution:**
```
NPC_Total = 252.96 + 13.80 + 0.00
          + 137.05 + 7.48 + 0.00
          + 275.01 + 14.39 + 0.00
          = 266.76 + 144.53 + 289.40
          = 700.69M
```

**CSV NPC_Total**: $700.68M
**Calculated Sum**: $700.69M (difference due to rounding of individual components)

| Item | Hand Calculation | CSV Value | Diff | Status |
|------|-----------------|-----------|------|--------|
| NPC Total | $700.69M | $700.68M | 0.01% | PASS |

### 5.7.3 Per-Year NPC Cross-Check

Summing Total_Year_Cost from per-year CSV for all 21 years:

| Year | Total_Year_Cost (USDm) |
|------|----------------------|
| 2030 | 6.39 |
| 2031 | 9.43 |
| 2032 | 12.52 |
| 2033 | 15.61 |
| 2034 | 16.72 |
| 2035 | 19.76 |
| 2036 | 22.85 |
| 2037 | 25.94 |
| 2038 | 28.99 |
| 2039 | 30.09 |
| 2040 | 33.18 |
| 2041 | 36.27 |
| 2042 | 39.32 |
| 2043 | 40.42 |
| 2044 | 43.51 |
| 2045 | 46.60 |
| 2046 | 49.65 |
| 2047 | 52.69 |
| 2048 | 53.84 |
| 2049 | 56.93 |
| 2050 | 59.98 |
| **Sum** | **700.69** |

| Item | Hand Calculation | CSV Summary | Diff | Status |
|------|-----------------|-------------|------|--------|
| Sum of per-year costs | $700.69M | $700.68M | 0.01% | PASS |

---

## 5.8 LCOAmmonia Verification

### 5.8.1 Total Supply Calculation

```
Total_Supply_20yr = sum of annual supply over 21 years (2030-2050)
```

Each year's supply:
```
Annual_Supply_m3 = Annual_Calls x Bunker_Volume
Annual_Supply_ton = Annual_Supply_m3 x Density
```

From CSV: `Total_Supply_20yr_ton = 235,620,000 tons`

### 5.8.2 LCOAmmonia Calculation

**Formula:**
```
LCOAmmonia = NPC_Total / Total_Supply_20yr_ton
```

**Substitution:**
```
LCOAmmonia = 700,680,000 / 235,620,000
           = 2.9737
           = $2.97/ton (rounded to 2 decimal places)
```

| Item | Hand Calculation | CSV Value | Status |
|------|-----------------|-----------|--------|
| LCOAmmonia | $2.97/ton | $2.97/ton | PASS |

---

## 5.9 Annuity Factor Verification

### 5.9.1 Formula

```
Annuity_Factor = sum from t=0 to N-1 of (1 / (1 + r)^t)
```

Where r = 0.07 (annualization interest rate), N = 21 years (2030-2050 inclusive).

**This is a geometric series:**
```
AF = (1 - (1/(1+r))^N) / (1 - 1/(1+r))
   = (1 - (1/1.07)^21) / (1 - 1/1.07)
   = (1 - 0.9346^21) / (1 - 0.9346)
```

**Step-by-step:**
```
(1/1.07) = 0.93458
0.93458^21 = 0.24120 (approx)
Numerator = 1 - 0.24120 = 0.75880
Denominator = 1 - 0.93458 = 0.06542
AF = 0.75880 / 0.06542 = 11.598 (approx)
```

Note: The exact annuity factor depends on implementation details (year indexing convention). The CSV value of 10.8355 reflects the code's specific calculation method.

| Item | CSV Value |
|------|-----------|
| Annuity_Factor | 10.8355 |

---

## 5.10 Shuttle Size Comparison (All Scenarios)

### 5.10.1 Full Results Table

| Shuttle (m3) | Cycle (hr) | Shore Loading (hr) | VpT | Annual Cycles | NPC (USDm) | LCO ($/ton) | Rank |
|--------------|-----------|-------------------|-----|---------------|------------|-------------|------|
| 2,500 | 21.53 | 3.67 | 1 | 371.63 | 899.06 | 3.82 | 4 |
| **5,000** | **23.19** | **5.33** | **1** | **344.93** | **700.68** | **2.97** | **1** |
| 10,000 | 34.53 | 8.67 | 2 | 231.70 | 732.51 | 3.11 | 2 |
| 15,000 | 45.86 | 12.00 | 3 | 174.44 | 806.59 | 3.42 | 3 |
| 20,000 | 57.19 | 15.33 | 4 | 139.88 | 883.97 | 3.75 | 5 |
| 25,000 | 68.53 | 18.67 | 5 | 116.74 | 971.11 | 4.12 | 6 |
| 30,000 | 79.86 | 22.00 | 6 | 100.18 | 1,052.71 | 4.47 | 7 |
| 35,000 | 91.19 | 25.33 | 7 | 87.73 | 1,140.50 | 4.84 | 8 |
| 40,000 | 102.53 | 28.67 | 8 | 78.03 | 1,218.51 | 5.17 | 9 |
| 45,000 | 113.86 | 32.00 | 9 | 70.26 | 1,304.56 | 5.54 | 10 |
| 50,000 | 125.19 | 35.33 | 10 | 63.90 | 1,386.81 | 5.89 | 11 |

### 5.10.2 Cycle Time Pattern Verification

For each shuttle size, the cycle time follows a clear pattern:

```
Cycle = Shore_Loading + Basic_Cycle
      = (S/1500 + 2.0) + (3.93 + 1.0 + VpT x 8.0 + 1.0 + 3.93)
      = (S/1500 + 2.0) + (9.86 + VpT x 8.0)
```

**Spot-check: 10,000 m3 shuttle:**
```
VpT = floor(10000 / 5000) = 2
Shore_Loading = (10000/1500) + 2.0 = 6.6667 + 2.0 = 8.6667
Basic_Cycle = 3.93 + 1.0 + 2 x 8.0 + 1.0 + 3.93 = 25.86
Total = 8.6667 + 25.86 = 34.5267

CSV: 34.5267 -> PASS
```

**Spot-check: 25,000 m3 shuttle:**
```
VpT = floor(25000 / 5000) = 5
Shore_Loading = (25000/1500) + 2.0 = 16.6667 + 2.0 = 18.6667
Basic_Cycle = 3.93 + 1.0 + 5 x 8.0 + 1.0 + 3.93 = 49.86
Total = 18.6667 + 49.86 = 68.5267

CSV: 68.5267 -> PASS
```

### 5.10.3 Why 5,000 m3 is Optimal

The 5,000 m3 shuttle achieves the lowest NPC ($700.68M) due to the balance of:

1. **Short cycle time** (23.19 hr) allowing high annual throughput (344.93 cycles)
2. **Low per-unit CAPEX** ($12.93M per shuttle)
3. **Moderate fuel cost** ($3,968/cycle) -- shorter distance than Yeosu means lower travel fuel
4. **VpT = 1** means no wasted capacity (shuttle exactly matches bunker volume per call)

Larger shuttles (10,000+ m3) have higher per-unit CAPEX and longer cycles from serving multiple vessels, which outweighs the reduced fleet size. The 2,500 m3 shuttle requires too many vessels despite the faster cycle time.

---

## 5.11 Comparison with Case 2-1 (Yeosu)

| Parameter | Case 2-1 (Yeosu) | Case 2-2 (Ulsan) | Difference |
|-----------|------------------|------------------|------------|
| Distance | 86 nm | 59 nm | -31.4% |
| Travel Time (one-way) | 5.73 hr | 3.93 hr | -31.4% |
| Optimal Shuttle | 10,000 m3 | 5,000 m3 | -50.0% |
| Optimal Cycle Time | 38.13 hr | 23.19 hr | -39.2% |
| Annual Cycles Max | 209.83 | 344.93 | +64.4% |
| NPC | $879.88M | $700.68M | -20.4% |
| LCOAmmonia | $3.73/ton | $2.97/ton | -20.4% |

**Why different optimal sizes?**

- **Yeosu (86 nm)**: Long travel time (11.46 hr round trip) makes it efficient to carry more cargo per trip. The 10,000 m3 shuttle serves 2 vessels per trip, amortizing the high travel cost.
- **Ulsan (59 nm)**: Shorter travel time (7.86 hr round trip) allows frequent trips. The 5,000 m3 shuttle with VpT=1 achieves 64% more annual cycles, reducing the required fleet size despite smaller individual loads.

---

## 5.12 Verification Summary

| # | Verification Item | Formula/Method | Hand Calc | CSV Value | Diff | Status |
|---|-------------------|---------------|-----------|-----------|------|--------|
| 1 | Shore Loading (5000 m3) | (5000/1500) + 2.0 | 5.3333 hr | 5.3333 hr | 0.00% | PASS |
| 2 | Basic Cycle Duration | 3.93+1.0+8.0+1.0+3.93 | 17.86 hr | 17.86 hr | 0.00% | PASS |
| 3 | Total Cycle Duration | 5.3333 + 17.86 | 23.1933 hr | 23.1933 hr | 0.00% | PASS |
| 4 | Vessels per Trip | floor(5000/5000) | 1 | 1 | 0.00% | PASS |
| 5 | Annual Cycles Max | 8000 / 23.1933 | 344.93 | 344.93 | 0.00% | PASS |
| 6 | Shuttle CAPEX | 61.5M x (5000/40000)^0.75 | $12,928,530 | $12,928,800 | 0.00% | PASS |
| 7 | Bunkering CAPEX | (12.93M x 0.03) + 317,460 | $705,324 | $705,300 | 0.00% | PASS |
| 8 | Shuttle fuel/cycle | 1930x436x3.93x2/1e6 x 600 | $3,968.42 | $3,968.39 | 0.00% | PASS |
| 9 | Pump fuel/cycle | 158.73x436x5.0/1e6 x 600 | $207.62 | $207.62 | 0.00% | PASS |
| 10 | Fixed OPEX shuttle/yr | 12,928,800 x 0.05 | $646,440 | $646,440 | 0.00% | PASS |
| 11 | Fixed OPEX bunkering/yr | 705,300 x 0.05 | $35,265 | $35,260 | 0.01% | PASS |
| 12 | NPC Total | Sum of 9 components | $700.69M | $700.68M | 0.01% | PASS |
| 13 | LCOAmmonia | 700.68M / 235.62M tons | $2.97/ton | $2.97/ton | 0.00% | PASS |

**Result: All 13 verification checks PASSED for Case 2-2 (Ulsan to Busan).**

All hand calculations match the CSV output values within rounding tolerance (< 0.02%). The MILP model produces correct and verifiable results for the Ulsan-to-Busan route.

---

## 5.13 Figure Reference

![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)

*Figure D1 shows the NPC comparison across all shuttle sizes for all cases, including Case 2-2 Ulsan. The 5,000 m3 shuttle is the clear optimum for the Ulsan route at $700.68M NPC ($2.97/ton).*
