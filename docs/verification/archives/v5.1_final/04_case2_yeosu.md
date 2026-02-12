# Chapter 4: Case 2-1 -- Yeosu to Busan Full Verification

## 4.1 Case Overview

| Parameter | Value |
|-----------|-------|
| Case Name | Case 2-1: Yeosu -> Busan |
| Route | Long-distance transport (Yeosu source to Busan port) |
| Distance | 86 nautical miles |
| Ship Speed | 15 knots |
| Travel Time (one-way) | 5.73 hours |
| Has Storage at Busan | No |
| Bunker Volume per Call | 5,000 m3 |
| Pump Rate | 1,000 m3/h |
| Shore Pump Rate | 1,500 m3/h |
| Shore Loading Fixed Time | 2.0 hours |
| Optimal Shuttle Size | 10,000 m3 |
| Optimal NPC | $879.88M |

**Key Characteristic**: Shuttles transport ammonia directly from the Yeosu production facility to Busan Port. There is no storage at Busan -- the shuttle vessel itself acts as temporary floating storage. One shuttle trip can serve multiple vessels if the shuttle capacity exceeds the per-vessel bunker volume.

**MCR Model (v5)**: Power Law formula `MCR = 17.17 x DWT^0.566` (MAN data regression, R2=0.998).

**SFOC Model (v4.1)**: DWT-based engine type matching. For 10,000 m3 shuttle (DWT=8,500), SFOC = 413 g/kWh (4-stroke medium / small 2-stroke range: DWT 8,000--15,000).

---

## 4.2 Input Parameters for Optimal Scenario (10,000 m3 Shuttle)

### 4.2.1 Vessel and Route Parameters

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Shuttle Size | S | 10,000 m3 | case_2_yeosu.yaml |
| Bunker Volume per Call | V_b | 5,000 m3 | case_2_yeosu.yaml |
| Pump Flow Rate | Q_pump | 1,000 m3/h | base.yaml |
| Distance (one-way) | D | 86 nm | case_2_yeosu.yaml |
| Ship Speed | v | 15 knots | case_2_yeosu.yaml |
| Travel Time (one-way) | t_travel | 5.73 h | 86/15 |
| Setup Time (per operation) | t_setup | 0.5 h | base.yaml |
| Max Annual Hours | H_max | 8,000 h/yr | base.yaml |
| Shore Pump Rate | Q_shore | 1,500 m3/h | base.yaml |
| Shore Loading Fixed Time | t_fixed | 2.0 h | base.yaml |

### 4.2.2 Cost Parameters

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Reference CAPEX | C_ref | $61,500,000 | base.yaml |
| Reference Size | S_ref | 40,000 m3 | base.yaml |
| Scaling Exponent | alpha | 0.75 | base.yaml |
| Equipment Ratio | r_equip | 3% | base.yaml |
| Fixed OPEX Ratio (Shuttle) | r_fopex_s | 5% | base.yaml |
| Fixed OPEX Ratio (Bunkering) | r_fopex_b | 5% | base.yaml |
| MCR (10,000 m3) | MCR | 2,990 kW | case_2_yeosu.yaml |
| SFOC (DWT 8,500) | SFOC | 413 g/kWh | base.yaml sfoc_map |
| Fuel Price | P_fuel | 600 USD/ton | base.yaml |
| Pump Delta Pressure | dP | 4.0 bar | base.yaml |
| Pump Efficiency | eta | 0.7 | base.yaml |
| Pump Power Cost | C_pump_kw | 2,000 USD/kW | base.yaml |
| Travel Factor (Case 2) | f_travel | 2.0 | Round trip fuel |
| Annualization Interest Rate | r_ann | 7% (0.07) | base.yaml |
| Discount Rate | r_disc | 0% (0.0) | base.yaml |
| Project Period | n | 21 years (2030--2050) | base.yaml |
| Ammonia Density (storage) | rho | 0.680 ton/m3 | base.yaml |

---

## 4.3 Cycle Time Verification

### 4.3.1 Vessels per Trip

**Formula**: Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)

**Substitution**: floor(10,000 / 5,000)

**Result**: 2 vessels

**CSV Value**: Vessels_per_Trip = 2.0

**Status**: **PASS**

### 4.3.2 Shore Loading Time

**Formula**: Shore_Loading = (Shuttle_Size / Shore_Pump_Rate) + loading_time_fixed_hours

**Substitution**: (10,000 / 1,500) + 2.0 = 6.6667 + 2.0

**Result**: 8.6667 hours

**CSV Value**: Shore_Loading_hr = 8.6667

**Status**: **PASS**

### 4.3.3 Per-Vessel Operations at Destination (Case 2)

In Case 2, each vessel at the destination port requires the following sequential operations:

| Component | Formula | Substitution | Result (hr) |
|-----------|---------|--------------|-------------|
| Movement (docking) | Fixed per vessel | -- | 1.0 |
| Setup Inbound | 2 x setup_time | 2 x 0.5 | 1.0 |
| Pumping per Vessel | V_b / Q_pump | 5,000 / 1,000 | 5.0 |
| Setup Outbound | 2 x setup_time | 2 x 0.5 | 1.0 |
| **Per-Vessel Total** | **Sum** | **1.0 + 1.0 + 5.0 + 1.0** | **8.0** |

**CSV Values**: Setup_Inbound = 1.0, Setup_Outbound = 1.0, Pumping_Per_Vessel = 5.0

**Status**: **PASS**

### 4.3.4 Basic Cycle Duration (Excluding Shore Loading)

**Formula**:
```
Basic_Cycle = Travel_Out + Port_Entry + VpT x (Movement + Setup_In + Pumping + Setup_Out) + Port_Exit + Travel_Return
```

**Substitution**:
```
= 5.73 + 1.0 + 2 x (1.0 + 1.0 + 5.0 + 1.0) + 1.0 + 5.73
= 5.73 + 1.0 + 2 x 8.0 + 1.0 + 5.73
= 5.73 + 1.0 + 16.0 + 1.0 + 5.73
```

**Result**: 29.46 hours

**CSV Value**: Basic_Cycle_Duration_hr = 29.46

| Component | Value (hr) |
|-----------|------------|
| Travel Outbound | 5.73 |
| Port Entry | 1.00 |
| Vessel 1 operations (move+setup+pump+setup) | 8.00 |
| Vessel 2 operations (move+setup+pump+setup) | 8.00 |
| Port Exit | 1.00 |
| Travel Return | 5.73 |
| **Basic Cycle Total** | **29.46** |

**Status**: **PASS**

### 4.3.5 Total Cycle Duration

**Formula**: Cycle_Duration = Shore_Loading + Basic_Cycle_Duration

**Substitution**: 8.6667 + 29.46

**Result**: 38.1267 hours

**CSV Value**: Cycle_Duration_hr = 38.1267

**Status**: **PASS**

### 4.3.6 Trips per Call

**Formula**: Trips_per_Call = 1 / Vessels_per_Trip (when shuttle >= bunker volume)

**Substitution**: 1 / 2

**Result**: 0.5 (meaning one trip serves 2 bunkering calls)

**CSV Value**: Trips_per_Call = 0.5

**Status**: **PASS**

### 4.3.7 Call Duration

**Formula**: Call_Duration = Trips_per_Call x Cycle_Duration

**Substitution**: 0.5 x 38.1267

**Result**: 19.0633 hours

**CSV Value**: Call_Duration_hr = 19.0633

**Status**: **PASS**

### 4.3.8 Annual Cycles Maximum

**Formula**: Annual_Cycles_Max = H_max / Cycle_Duration

**Substitution**: 8,000 / 38.1267

**Result**: 209.83

**CSV Value**: Annual_Cycles_Max = 209.83

**Status**: **PASS**

### 4.3.9 Cycle Timeline Diagram

```
=== Case 2-1: Single Cycle Timeline (10,000 m3 Shuttle, 1,000 m3/h Pump, 2 Vessels/Trip) ===

Phase                        Duration (h)   Cumulative (h)
---------------------------  ------------   --------------
Shore Loading                   8.67         0.00 ->  8.67
Travel Outbound (86 nm)        5.73         8.67 -> 14.40
Port Entry                      1.00        14.40 -> 15.40
  [Vessel 1] Movement           1.00        15.40 -> 16.40
  [Vessel 1] Setup Inbound      1.00        16.40 -> 17.40
  [Vessel 1] Pumping (5000m3)   5.00        17.40 -> 22.40
  [Vessel 1] Setup Outbound     1.00        22.40 -> 23.40
  [Vessel 2] Movement           1.00        23.40 -> 24.40
  [Vessel 2] Setup Inbound      1.00        24.40 -> 25.40
  [Vessel 2] Pumping (5000m3)   5.00        25.40 -> 30.40
  [Vessel 2] Setup Outbound     1.00        30.40 -> 31.40
Port Exit                       1.00        31.40 -> 32.40
Travel Return (86 nm)          5.73        32.40 -> 38.13
                               ------
TOTAL CYCLE                    38.13 h
```

**Visual Block Diagram:**

```
|<--- Shore Loading --->|<-- Travel Out -->|<-PE->|<---- Vessel 1 (8.0h) ---->|<---- Vessel 2 (8.0h) ---->|<-PX->|<-- Travel Ret -->|
|       8.67 h          |     5.73 h       | 1.0h | Mv|SIn|  Pump 5h  |SOut| Mv|SIn|  Pump 5h  |SOut| 1.0h |     5.73 h        |
|<--------------------------------------------- Total Cycle: 38.13 h -------------------------------------------------->|

Where: PE = Port Entry, PX = Port Exit, Mv = Movement, SIn = Setup In, SOut = Setup Out
```

**Key Observations:**
- The two-vessel service block (16.0h) is the dominant component of the basic cycle
- Shore loading (8.67h) is the second largest component due to 10,000 m3 cargo volume
- Travel time is symmetric (5.73h each way, 86 nm at 15 kt)
- Port entry/exit adds 2.0h overhead (Case 2 only)

---

## 4.4 CAPEX Verification

### 4.4.1 Shuttle CAPEX

**Formula**: Shuttle_CAPEX = C_ref x (S / S_ref)^alpha

**Substitution**:
```
= 61,500,000 x (10,000 / 40,000)^0.75
= 61,500,000 x (0.25)^0.75
```

**Intermediate calculation**:
```
ln(0.25) = -1.386294
0.75 x (-1.386294) = -1.039721
e^(-1.039721) = 0.353553
```

**Result**:
```
= 61,500,000 x 0.353553
= $21,743,509
```

**CSV Verification** (Year 2030, x=2 new shuttles):
```
Actual_CAPEX_Shuttle_USDm = 43.4871
Per shuttle = 43.4871 / 2 = $21.7436M = $21,743,600
```

**Difference**: |21,743,509 - 21,743,600| = $91 (0.0004%)

**Status**: **PASS**

### 4.4.2 Pump Power

**Formula**: P_pump = (dP x Q) / eta

**Substitution**:
```
dP = 4.0 bar = 4.0 x 10^5 Pa = 400,000 Pa
Q = 1,000 m3/h = 1,000 / 3,600 m3/s = 0.27778 m3/s
eta = 0.7

P_pump = (400,000 x 0.27778) / 0.7
       = 111,111.11 / 0.7
       = 158,730.16 W
```

**Result**: 158.73 kW

**Status**: **PASS**

### 4.4.3 Pump CAPEX

**Formula**: Pump_CAPEX = P_pump x C_pump_kw

**Substitution**: 158.73 x 2,000

**Result**: $317,460

**Status**: **PASS**

### 4.4.4 Bunkering System CAPEX

**Formula**: Bunkering_CAPEX = (Shuttle_CAPEX x r_equip) + Pump_CAPEX

**Substitution**:
```
= (21,743,509 x 0.03) + 317,460
= 652,305 + 317,460
```

**Result**: $969,765 per shuttle

**CSV Verification** (Year 2030, x=2 new shuttles):
```
Actual_CAPEX_Pump_USDm = 1.9395
Per shuttle = 1.9395 / 2 = $0.96975M = $969,750
```

**Difference**: |969,765 - 969,750| = $15 (0.002%)

**Status**: **PASS**

### 4.4.5 Annuity Factor

**Formula**: AF = [1 - (1 + r)^(-n)] / r

**Substitution**:
```
r = 0.07, n = 21

(1.07)^21 = 4.14056
(1.07)^(-21) = 1 / 4.14056 = 0.24151

AF = (1 - 0.24151) / 0.07
   = 0.75849 / 0.07
```

**Result**: 10.8356

**CSV Value**: Annuity_Factor = 10.8355

**Difference**: |10.8356 - 10.8355| = 0.0001 (0.001%)

**Status**: **PASS**

### 4.4.6 Annualized CAPEX per Year (Year 2030 Verification)

**Annualized Shuttle CAPEX** (N=2 shuttles in 2030):

**Formula**: Ann_Shuttle_CAPEX = (N x Shuttle_CAPEX) / AF

**Substitution**: (2 x 21,743,509) / 10.8355 = 43,487,018 / 10.8355

**Result**: $4,013,446

**CSV Value**: Annualized_CAPEX_Shuttle_USDm = 4.0134M = $4,013,400

**Difference**: $46 (0.001%)

**Status**: **PASS**

**Annualized Bunkering CAPEX** (N=2 shuttles in 2030):

**Formula**: Ann_Bunk_CAPEX = (N x Bunkering_CAPEX) / AF

**Substitution**: (2 x 969,765) / 10.8355 = 1,939,530 / 10.8355

**Result**: $179,003

**CSV Value**: Annualized_CAPEX_Pump_USDm = 0.179M = $179,000

**Difference**: $3 (0.002%)

**Status**: **PASS**

---

## 4.5 OPEX Verification

### 4.5.1 Fixed OPEX -- Shuttle

**Formula**: Shuttle_fOPEX = Shuttle_CAPEX x r_fopex_s (per shuttle per year)

**Substitution**: 21,743,509 x 0.05

**Result**: $1,087,175 per shuttle per year

**CSV Verification** (Year 2030, N=2 shuttles):
```
FixedOPEX_Shuttle_USDm = 2.1744
Per shuttle = 2.1744 / 2 = $1.0872M = $1,087,200
```

**Difference**: |1,087,175 - 1,087,200| = $25 (0.002%)

**Status**: **PASS**

### 4.5.2 Fixed OPEX -- Bunkering

**Formula**: Bunk_fOPEX = Bunkering_CAPEX x r_fopex_b (per shuttle per year)

**Substitution**: 969,765 x 0.05

**Result**: $48,488 per shuttle per year

**CSV Verification** (Year 2030, N=2 shuttles):
```
FixedOPEX_Pump_USDm = 0.097
Per shuttle = 0.097 / 2 = $0.0485M = $48,500
```

**Difference**: |48,488 - 48,500| = $12 (0.025%)

**Status**: **PASS**

### 4.5.3 Variable OPEX -- Shuttle Fuel (per cycle)

**Formula**: Fuel_cost_per_cycle = MCR x SFOC x t_travel x f_travel / 1e6 x P_fuel

**Substitution**:
```
Step 1: Fuel mass per cycle (tons)
= 2,990 x 413 x 5.73 x 2.0 / 1,000,000
= (2,990 x 413) x 5.73 x 2.0 / 1,000,000
= 1,234,870 x 5.73 x 2.0 / 1,000,000
= 7,075,805 x 2.0 / 1,000,000
= 14,151,610 / 1,000,000
= 14.1516 tons per cycle

Step 2: Cost per cycle
= 14.1516 x 600
= $8,490.97 per cycle
```

**CSV Verification** (Year 2030: Annual_Cycles=300):
```
VariableOPEX_Shuttle_USDm = 2.5473
Cost per cycle = 2,547,300 / 300 = $8,491.00
```

**Difference**: |8,490.97 - 8,491.00| = $0.03 (0.0004%)

**Status**: **PASS**

### 4.5.4 Variable OPEX -- Bunkering Pump Fuel (per call)

**Important**: The optimizer uses the shuttle's SFOC (413 g/kWh for 10,000 m3) for pump fuel calculation, not the default SFOC (379 g/kWh).

**Formula**: Pump_fuel_cost_per_call = P_pump x (V_b / Q_pump) x SFOC / 1e6 x P_fuel

**Substitution**:
```
Step 1: Pumping time per call
= 5,000 / 1,000 = 5.0 hours

Step 2: Fuel mass per call (tons)
= 158.73 x 5.0 x 413 / 1,000,000
= (158.73 x 5.0) x 413 / 1,000,000
= 793.65 x 413 / 1,000,000
= 327,777.45 / 1,000,000
= 0.32778 tons per call

Step 3: Cost per call
= 0.32778 x 600
= $196.67 per call
```

**CSV Verification** (Year 2030: Annual_Calls=600):
```
VariableOPEX_Pump_USDm = 0.118
Cost per call = 118,000 / 600 = $196.67
```

**Difference**: $0.00 (0.000%)

**Status**: **PASS**

---

## 4.6 Per-Year Results Verification

### 4.6.1 Demand Growth and Fleet Sizing

Vessel growth is linear from 50 (2030) to 500 (2050). Annual demand = Vessels x 5,000 m3 x 12 voyages.

| Year | Vessels | Demand (m3) | Annual Calls | Cycles (Calls x 0.5) | N (Shuttles) | New | Hours Needed | Hours Available | Utilization |
|------|---------|-------------|--------------|----------------------|--------------|-----|--------------|-----------------|-------------|
| 2030 | 50 | 3,000,000 | 600 | 300 | 2 | 2 | 11,438 | 16,000 | 0.7149 |
| 2031 | 73 | 4,320,000 | 864 | 432 | 3 | 1 | 16,471 | 24,000 | 0.6863 |
| 2032 | 95 | 5,700,000 | 1,140 | 570 | 3 | 0 | 21,732 | 24,000 | 0.9055 |
| 2033 | 118 | 7,080,000 | 1,416 | 708 | 4 | 1 | 26,994 | 32,000 | 0.8436 |
| 2034 | 140 | 8,400,000 | 1,680 | 840 | 5 | 1 | 32,026 | 40,000 | 0.8007 |
| 2035 | 163 | 9,720,000 | 1,944 | 972 | 5 | 0 | 37,059 | 40,000 | 0.9265 |
| 2036 | 185 | 11,100,000 | 2,220 | 1,110 | 6 | 1 | 42,321 | 48,000 | 0.8817 |
| 2037 | 208 | 12,480,000 | 2,496 | 1,248 | 6 | 0 | 47,582 | 48,000 | 0.9913 |
| 2038 | 230 | 13,800,000 | 2,760 | 1,380 | 7 | 1 | 52,615 | 56,000 | 0.9395 |
| 2039 | 253 | 15,120,000 | 3,024 | 1,512 | 8 | 1 | 57,648 | 64,000 | 0.9007 |
| 2040 | 275 | 16,500,000 | 3,300 | 1,650 | 8 | 0 | 62,909 | 64,000 | 0.9830 |
| 2041 | 298 | 17,880,000 | 3,576 | 1,788 | 9 | 1 | 68,170 | 72,000 | 0.9468 |
| 2042 | 320 | 19,200,000 | 3,840 | 1,920 | 10 | 1 | 73,203 | 80,000 | 0.9150 |
| 2043 | 343 | 20,520,000 | 4,104 | 2,052 | 10 | 0 | 78,236 | 80,000 | 0.9779 |
| 2044 | 365 | 21,900,000 | 4,380 | 2,190 | 11 | 1 | 83,497 | 88,000 | 0.9488 |
| 2045 | 388 | 23,280,000 | 4,656 | 2,328 | 12 | 1 | 88,759 | 96,000 | 0.9246 |
| 2046 | 410 | 24,600,000 | 4,920 | 2,460 | 12 | 0 | 93,792 | 96,000 | 0.9770 |
| 2047 | 433 | 25,920,000 | 5,184 | 2,592 | 13 | 1 | 98,824 | 104,000 | 0.9502 |
| 2048 | 455 | 27,300,000 | 5,460 | 2,730 | 14 | 1 | 104,086 | 112,000 | 0.9293 |
| 2049 | 478 | 28,680,000 | 5,736 | 2,868 | 14 | 0 | 109,347 | 112,000 | 0.9763 |
| 2050 | 500 | 30,000,000 | 6,000 | 3,000 | 15 | 1 | 114,380 | 120,000 | 0.9532 |

All values match per-year CSV output.

### 4.6.2 Hours Needed Verification (Year 2030)

**Formula**: Hours_Needed = Annual_Cycles x Cycle_Duration

**Substitution**: 300 x 38.1267

**Result**: 11,438 hours

**CSV Value**: Total_Hours_Needed = 11,438

**Status**: **PASS**

### 4.6.3 Hours Needed Verification (Year 2050)

**Formula**: Hours_Needed = Annual_Cycles x Cycle_Duration

**Substitution**: 3,000 x 38.1267

**Result**: 114,380 hours

**CSV Value**: Total_Hours_Needed = 114,380

**Status**: **PASS**

### 4.6.4 Fleet Sizing Constraint Verification (Year 2050)

**Formula**: N >= Hours_Needed / H_max

**Substitution**: 114,380 / 8,000 = 14.30 -> ceil(14.30) = 15

**CSV Value**: Total_Shuttles = 15

**Status**: **PASS**

---

## 4.7 NPC Component Summation (20-Year)

### 4.7.1 NPC Annualized Shuttle CAPEX

**Formula**: NPC_Ann_Shuttle_CAPEX = Sum over t=2030..2050 of [N(t) x Shuttle_CAPEX / AF]

**Per-year breakdown**:

| Year | N | N x $21.7435M | Annualized (/ 10.8355) |
|------|---|----------------|------------------------|
| 2030 | 2 | 43.4871 | 4.0134 |
| 2031 | 3 | 65.2306 | 6.0201 |
| 2032 | 3 | 65.2306 | 6.0201 |
| 2033 | 4 | 86.9741 | 8.0268 |
| 2034 | 5 | 108.7176 | 10.0334 |
| 2035 | 5 | 108.7176 | 10.0334 |
| 2036 | 6 | 130.4612 | 12.0401 |
| 2037 | 6 | 130.4612 | 12.0401 |
| 2038 | 7 | 152.2047 | 14.0468 |
| 2039 | 8 | 173.9482 | 16.0535 |
| 2040 | 8 | 173.9482 | 16.0535 |
| 2041 | 9 | 195.6918 | 18.0602 |
| 2042 | 10 | 217.4353 | 20.0669 |
| 2043 | 10 | 217.4353 | 20.0669 |
| 2044 | 11 | 239.1788 | 22.0736 |
| 2045 | 12 | 260.9224 | 24.0803 |
| 2046 | 12 | 260.9224 | 24.0803 |
| 2047 | 13 | 282.6659 | 26.0870 |
| 2048 | 14 | 304.4094 | 28.0936 |
| 2049 | 14 | 304.4094 | 28.0936 |
| 2050 | 15 | 326.1530 | 30.1003 |

**Sum**: 355.18M

**CSV Value**: NPC_Annualized_Shuttle_CAPEX_USDm = 355.18

**Status**: **PASS**

### 4.7.2 NPC Annualized Bunkering CAPEX

**Formula**: NPC_Ann_Bunk_CAPEX = Sum over t=2030..2050 of [N(t) x Bunkering_CAPEX / AF]

**Sum of per-year values**:
```
0.179 + 0.2685 + 0.2685 + 0.358 + 0.4475 + 0.4475 + 0.537 + 0.537
+ 0.6265 + 0.716 + 0.716 + 0.8055 + 0.895 + 0.895 + 0.9845
+ 1.074 + 1.074 + 1.1635 + 1.253 + 1.253 + 1.3425
= 15.84M
```

**CSV Value**: NPC_Annualized_Bunkering_CAPEX_USDm = 15.84

**Status**: **PASS**

### 4.7.3 NPC Shuttle Fixed OPEX

**Formula**: NPC_Shuttle_fOPEX = Sum over t=2030..2050 of [N(t) x $1,087,175]

**Sum of per-year values**:
```
2.1744 + 3.2615 + 3.2615 + 4.3487 + 5.4359 + 5.4359 + 6.5231 + 6.5231
+ 7.6102 + 8.6974 + 8.6974 + 9.7846 + 10.8718 + 10.8718 + 11.9589
+ 13.0461 + 13.0461 + 14.1333 + 15.2205 + 15.2205 + 16.3077
= 192.43M
```

**CSV Value**: NPC_Shuttle_fOPEX_USDm = 192.43

**Status**: **PASS**

### 4.7.4 NPC Bunkering Fixed OPEX

**Formula**: NPC_Bunk_fOPEX = Sum over t=2030..2050 of [N(t) x $48,488]

**Sum of per-year values**:
```
0.097 + 0.1455 + 0.1455 + 0.194 + 0.2424 + 0.2424 + 0.2909 + 0.2909
+ 0.3394 + 0.3879 + 0.3879 + 0.4364 + 0.4849 + 0.4849 + 0.5334
+ 0.5819 + 0.5819 + 0.6303 + 0.6788 + 0.6788 + 0.7273
= 8.58M
```

**CSV Value**: NPC_Bunkering_fOPEX_USDm = 8.58

**Status**: **PASS**

### 4.7.5 NPC Shuttle Variable OPEX

**Formula**: NPC_Shuttle_vOPEX = Sum over t=2030..2050 of [Cycles(t) x $8,491]

**Per-year breakdown**:

| Year | Calls | Cycles | vOPEX Shuttle (USDm) |
|------|-------|--------|----------------------|
| 2030 | 600 | 300 | 2.5473 |
| 2031 | 864 | 432 | 3.6681 |
| 2032 | 1,140 | 570 | 4.8399 |
| 2033 | 1,416 | 708 | 6.0116 |
| 2034 | 1,680 | 840 | 7.1324 |
| 2035 | 1,944 | 972 | 8.2532 |
| 2036 | 2,220 | 1,110 | 9.4250 |
| 2037 | 2,496 | 1,248 | 10.5967 |
| 2038 | 2,760 | 1,380 | 11.7175 |
| 2039 | 3,024 | 1,512 | 12.8383 |
| 2040 | 3,300 | 1,650 | 14.0101 |
| 2041 | 3,576 | 1,788 | 15.1818 |
| 2042 | 3,840 | 1,920 | 16.3027 |
| 2043 | 4,104 | 2,052 | 17.4235 |
| 2044 | 4,380 | 2,190 | 18.5952 |
| 2045 | 4,656 | 2,328 | 19.7670 |
| 2046 | 4,920 | 2,460 | 20.8878 |
| 2047 | 5,184 | 2,592 | 22.0086 |
| 2048 | 5,460 | 2,730 | 23.1803 |
| 2049 | 5,736 | 2,868 | 24.3521 |
| 2050 | 6,000 | 3,000 | 25.4729 |

**Sum**: 294.21M

**CSV Value**: NPC_Shuttle_vOPEX_USDm = 294.21

**Status**: **PASS**

### 4.7.6 NPC Bunkering Variable OPEX

**Formula**: NPC_Bunk_vOPEX = Sum over t=2030..2050 of [Calls(t) x $196.67]

**Sum of per-year values**:
```
0.118 + 0.1699 + 0.2242 + 0.2785 + 0.3304 + 0.3823 + 0.4366 + 0.4909
+ 0.5428 + 0.5947 + 0.6490 + 0.7033 + 0.7552 + 0.8071 + 0.8614
+ 0.9157 + 0.9676 + 1.0195 + 1.0738 + 1.1281 + 1.1800
= 13.63M
```

**CSV Value**: NPC_Bunkering_vOPEX_USDm = 13.63

**Status**: **PASS**

---

## 4.8 NPC Total Verification

### 4.8.1 Component Summation

**Formula**:
```
NPC_Total = NPC_Ann_Shuttle_CAPEX + NPC_Ann_Bunkering_CAPEX
          + NPC_Shuttle_fOPEX + NPC_Bunkering_fOPEX
          + NPC_Shuttle_vOPEX + NPC_Bunkering_vOPEX
```

**Substitution**:
```
= 355.18 + 15.84 + 192.43 + 8.58 + 294.21 + 13.63
```

| Component | NPC (USDm) | Share |
|-----------|------------|-------|
| Shuttle CAPEX (Annualized) | 355.18 | 40.37% |
| Bunkering CAPEX (Annualized) | 15.84 | 1.80% |
| **Total CAPEX** | **371.02** | **42.17%** |
| Shuttle Fixed OPEX | 192.43 | 21.87% |
| Bunkering Fixed OPEX | 8.58 | 0.98% |
| **Total Fixed OPEX** | **201.01** | **22.85%** |
| Shuttle Variable OPEX | 294.21 | 33.44% |
| Bunkering Variable OPEX | 13.63 | 1.55% |
| **Total Variable OPEX** | **307.84** | **34.99%** |
| **TOTAL NPC** | **879.87** | **100.00%** |

**Result**: $879.87M

**CSV Value**: NPC_Total_USDm = $879.88M

**Difference**: $0.01M (rounding across 6 components, each rounded to 2 decimal places)

**Status**: **PASS**

### 4.8.2 Cross-Verification with Per-Year Total

**Sum of Total_Year_Cost_USDm** across all 21 years:
```
9.129 + 13.5336 + 14.7596 + 19.2175 + 23.6221 + 24.7948
+ 29.2527 + 30.4787 + 34.8833 + 39.2879 + 40.5139 + 44.9718
+ 49.3764 + 50.5491 + 55.007 + 59.4649 + 60.6376 + 65.0422
+ 69.5001 + 70.7261 + 75.1307
= 879.88M
```

**CSV NPC_Total**: $879.88M

**Status**: **PASS**

---

## 4.9 LCOAmmonia Verification

### 4.9.1 Total Supply Calculation

**Formula**: Total_Supply_ton = Sum(Annual_Calls x V_b) x rho

**Annual calls sum**:
```
600 + 864 + 1140 + 1416 + 1680 + 1944 + 2220 + 2496 + 2760 + 3024
+ 3300 + 3576 + 3840 + 4104 + 4380 + 4656 + 4920 + 5184 + 5460 + 5736 + 6000
= 69,300 total calls
```

**Total supply in m3**: 69,300 x 5,000 = 346,500,000 m3

**Total supply in tons**: 346,500,000 x 0.680 = 235,620,000 tons

**CSV Value**: Total_Supply_20yr_ton = 235,620,000

**Status**: **PASS**

### 4.9.2 LCOAmmonia Calculation

**Formula**: LCOAmmonia = NPC_Total / Total_Supply_20yr_ton

**Substitution**: 879,880,000 / 235,620,000

**Result**: 3.7341 -> rounded to 2 decimal places: $3.73/ton

**CSV Value**: LCOAmmonia_USD_per_ton = 3.73

**Status**: **PASS**

---

## 4.10 All Shuttle Sizes Summary

| Shuttle (m3) | Cycle (hr) | Vessels/Trip | Ann Cycles | NPC (USDm) | LCO ($/ton) | Rank |
|--------------|------------|--------------|------------|------------|--------------|------|
| 2,500 | 25.13 | 1 | 318.39 | 1,168.60 | 4.96 | 7 |
| 5,000 | 26.79 | 1 | 298.58 | 886.77 | 3.76 | 2 |
| **10,000** | **38.13** | **2** | **209.83** | **879.88** | **3.73** | **1** |
| 15,000 | 49.46 | 3 | 161.75 | 938.30 | 3.98 | 3 |
| 20,000 | 60.79 | 4 | 131.59 | 994.49 | 4.22 | 4 |
| 25,000 | 72.13 | 5 | 110.92 | 1,071.27 | 4.55 | 5 |
| 30,000 | 83.46 | 6 | 95.85 | 1,154.36 | 4.90 | 6 |
| 35,000 | 94.79 | 7 | 84.39 | 1,236.04 | 5.25 | 8 |
| 40,000 | 106.13 | 8 | 75.38 | 1,305.09 | 5.54 | 9 |
| 45,000 | 117.46 | 9 | 68.11 | 1,382.39 | 5.87 | 10 |
| 50,000 | 128.79 | 10 | 62.12 | 1,465.15 | 6.22 | 11 |

### Cycle Time Verification for All Sizes

| Shuttle (m3) | Shore Load (hr) | VpT | Basic Cycle (hr) | Total Cycle (hr) | CSV Match |
|--------------|-----------------|-----|-------------------|-------------------|-----------|
| 2,500 | (2500/1500)+2.0 = 3.67 | 1 | 5.73+1.0+1x8.0+1.0+5.73 = 21.46 | 25.13 | PASS |
| 5,000 | (5000/1500)+2.0 = 5.33 | 1 | 5.73+1.0+1x8.0+1.0+5.73 = 21.46 | 26.79 | PASS |
| 10,000 | (10000/1500)+2.0 = 8.67 | 2 | 5.73+1.0+2x8.0+1.0+5.73 = 29.46 | 38.13 | PASS |
| 15,000 | (15000/1500)+2.0 = 12.00 | 3 | 5.73+1.0+3x8.0+1.0+5.73 = 37.46 | 49.46 | PASS |
| 20,000 | (20000/1500)+2.0 = 15.33 | 4 | 5.73+1.0+4x8.0+1.0+5.73 = 45.46 | 60.79 | PASS |
| 25,000 | (25000/1500)+2.0 = 18.67 | 5 | 5.73+1.0+5x8.0+1.0+5.73 = 53.46 | 72.13 | PASS |
| 30,000 | (30000/1500)+2.0 = 22.00 | 6 | 5.73+1.0+6x8.0+1.0+5.73 = 61.46 | 83.46 | PASS |
| 35,000 | (35000/1500)+2.0 = 25.33 | 7 | 5.73+1.0+7x8.0+1.0+5.73 = 69.46 | 94.79 | PASS |
| 40,000 | (40000/1500)+2.0 = 28.67 | 8 | 5.73+1.0+8x8.0+1.0+5.73 = 77.46 | 106.13 | PASS |
| 45,000 | (45000/1500)+2.0 = 32.00 | 9 | 5.73+1.0+9x8.0+1.0+5.73 = 85.46 | 117.46 | PASS |
| 50,000 | (50000/1500)+2.0 = 35.33 | 10 | 5.73+1.0+10x8.0+1.0+5.73 = 93.46 | 128.79 | PASS |

### Why 10,000 m3 is Optimal

The 10,000 m3 shuttle achieves the lowest NPC ($879.88M) and LCOAmmonia ($3.73/ton) due to the balance between:

1. **CAPEX efficiency**: Moderate vessel cost ($21.74M per shuttle) with reasonable fleet size (15 shuttles at 2050).
2. **Fuel economy**: 2 vessels per trip amortizes the long 86 nm round-trip fuel cost ($8,491/cycle) across 2 calls.
3. **Time utilization**: 38.13 hr cycle allows 209.83 cycles/yr per shuttle -- enough throughput without excessive idle time.
4. **Smaller shuttles** (2,500-5,000 m3): Too many trips needed, higher fleet counts, more fuel consumed per m3 delivered.
5. **Larger shuttles** (15,000+ m3): Higher per-vessel CAPEX grows faster than throughput gains; shore loading time becomes dominant.

---

## 4.11 SFOC and MCR Impact Analysis

### 4.11.1 SFOC Map for Case 2-1

| Shuttle (m3) | DWT (ton) | DWT Range | Engine Type | SFOC (g/kWh) |
|--------------|-----------|-----------|-------------|--------------|
| 2,500 | 2,125 | < 3,000 | 4-stroke high-speed | 505 |
| 5,000 | 4,250 | 3,000-8,000 | 4-stroke medium-speed | 436 |
| 10,000 | 8,500 | 8,000-15,000 | 4-stroke medium / small 2-stroke | 413 |
| 15,000 | 12,750 | 8,000-15,000 | 4-stroke medium / small 2-stroke | 413 |
| 20,000 | 17,000 | 15,000-30,000 | 2-stroke | 390 |
| 25,000 | 21,250 | 15,000-30,000 | 2-stroke | 390 |
| 30,000 | 25,500 | 15,000-30,000 | 2-stroke | 390 |
| 35,000 | 29,750 | 15,000-30,000 | 2-stroke | 390 |
| 40,000 | 34,000 | > 30,000 | 2-stroke large | 379 |
| 45,000 | 38,250 | > 30,000 | 2-stroke large | 379 |
| 50,000 | 42,500 | > 30,000 | 2-stroke large | 379 |

### 4.11.2 Fuel Cost per Cycle by Shuttle Size

| Shuttle (m3) | MCR (kW) | SFOC (g/kWh) | Fuel (ton/cycle) | Cost ($/cycle) |
|--------------|----------|--------------|------------------|----------------|
| 2,500 | 1,310 | 505 | 7.5809 | 4,548.55 |
| 5,000 | 1,930 | 436 | 9.6445 | 5,786.72 |
| 10,000 | 2,990 | 413 | 14.1516 | 8,490.97 |
| 15,000 | 3,850 | 413 | 18.2235 | 10,934.09 |
| 20,000 | 4,610 | 390 | 20.6093 | 12,365.56 |
| 25,000 | 5,300 | 390 | 23.6934 | 14,216.04 |
| 30,000 | 5,940 | 390 | 26.5525 | 15,931.48 |
| 35,000 | 6,540 | 390 | 29.2327 | 17,539.65 |
| 40,000 | 7,100 | 379 | 30.8415 | 18,504.91 |
| 45,000 | 7,640 | 379 | 33.1862 | 19,911.69 |
| 50,000 | 8,150 | 379 | 35.3996 | 21,239.78 |

**Note**: Fuel cost per cycle increases with shuttle size, but fuel cost per m3 delivered decreases for Case 2 because larger shuttles serve more vessels per trip.

---

## 4.12 Distance Impact Analysis

The 86 nm route between Yeosu and Busan significantly impacts all cost components:

| Factor | Value | Impact |
|--------|-------|--------|
| Travel Time (round trip) | 11.46 hr | 30% of basic cycle time (29.46 hr) |
| Fuel Cost per Cycle | $8,491 (10,000 m3) | Dominant variable cost driver |
| Shore Loading Time | 8.67 hr (10,000 m3) | 23% of total cycle (38.13 hr) |
| Annual Cycles | 209.83 (10,000 m3) | Limits throughput per shuttle |
| Fleet Size at 2050 | 15 shuttles | Drives CAPEX and Fixed OPEX |

### Cost Structure Comparison

| Category | NPC (USDm) | Share |
|----------|------------|-------|
| CAPEX (Annualized) | 371.02 | 42.17% |
| Fixed OPEX | 201.01 | 22.85% |
| Variable OPEX | 307.84 | 34.99% |

The long distance creates a balanced cost structure where CAPEX (42%), Fixed OPEX (23%), and Variable OPEX (35%) all contribute significantly. Variable OPEX is dominated by shuttle fuel ($294.21M, 95.6% of total variable OPEX).

---

## 4.13 Verification Summary

| # | Item | Hand Calculation | CSV Value | Difference | Status |
|---|------|------------------|-----------|------------|--------|
| 1 | Shore Loading (10,000 m3) | 8.6667 hr | 8.6667 hr | 0.00% | PASS |
| 2 | Basic Cycle Duration | 29.46 hr | 29.46 hr | 0.00% | PASS |
| 3 | Total Cycle Duration | 38.1267 hr | 38.1267 hr | 0.00% | PASS |
| 4 | Vessels per Trip | 2 | 2 | 0.00% | PASS |
| 5 | Trips per Call | 0.5 | 0.5 | 0.00% | PASS |
| 6 | Annual Cycles Max | 209.83 | 209.83 | 0.00% | PASS |
| 7 | Shuttle CAPEX | $21,743,509 | $21,743,600 | 0.0004% | PASS |
| 8 | Bunkering CAPEX | $969,765 | $969,750 | 0.002% | PASS |
| 9 | Annuity Factor | 10.8356 | 10.8355 | 0.001% | PASS |
| 10 | Shuttle Fuel Cost/Cycle | $8,490.97 | $8,491.00 | 0.0004% | PASS |
| 11 | Pump Fuel Cost/Call | $196.67 | $196.67 | 0.00% | PASS |
| 12 | NPC Total | $879.87M | $879.88M | 0.001% | PASS |
| 13 | LCOAmmonia | $3.73/ton | $3.73/ton | 0.00% | PASS |

**All 13 verification checks PASSED for Case 2-1 (Yeosu to Busan).**

Differences are within rounding tolerance (maximum 0.002%) caused by intermediate rounding in CSV output to 4 decimal places.

---

## 4.14 Figure Reference

![D1: NPC vs Shuttle Size](../../results/paper_figures/D1_npc_vs_shuttle.png)

*Figure D1 shows the NPC comparison across all shuttle sizes for all cases, including Case 2-1 Yeosu. The 10,000 m3 shuttle achieves the minimum NPC at $879.88M ($3.73/ton LCOAmmonia).*
