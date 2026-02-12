# 05. Case 3: Yeosu to Busan Verification

## 5.1 Overview

Case 3 models long-distance ammonia shuttle transport from **Yeosu** (ammonia production facility) to **Busan Port**. This is the longest route among the three cases at **86 nautical miles**, resulting in a one-way travel time of **5.73 hours** -- significantly longer than Case 2's 3.93 hours. The additional 1.80 hours per leg (3.60 hours round trip) is the primary cost driver that makes Case 3 the most expensive option.

Like Case 2, Case 3 has **no storage at Busan** (`has_storage_at_busan: false`), meaning the shuttle delivers ammonia directly to vessels at anchorage. The optimal configuration is a **5,000 m3 shuttle** at **500 m3/h pump rate**, yielding an NPC of **$1,094.12M** and an LCOA of **$4.64/ton**.

---

## 5.2 Case 3 Configuration

### Route Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Origin | Yeosu | case_3_yeosu.yaml |
| Destination | Busan Port | case_3_yeosu.yaml |
| Distance | 86 nm | case_3_yeosu.yaml |
| Speed | 15 knots | case_3_yeosu.yaml |
| Travel time (one-way) | 5.73 h (= 86 / 15) | Calculated |
| Has storage at Busan | false | case_3_yeosu.yaml |

### Operational Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Bunker volume per call | 5,000 m3 | case_3_yeosu.yaml |
| Optimal shuttle size | 5,000 m3 | MILP result |
| STS pump rate | 500 m3/h | base.yaml |
| Shore pump rate | 700 m3/h | base.yaml |
| Shore loading fixed time | 4.0 h | base.yaml |
| Setup time | 2.0 h per endpoint | base.yaml |
| Max annual hours (H_max) | 8,000 h/year | base.yaml |
| Port entry time | 1.0 h | base.yaml |
| Port exit time | 1.0 h | base.yaml |
| Movement per vessel | 1.0 h | base.yaml |

### MCR Map (Case 3)

| Shuttle Size (m3) | MCR (kW) |
|-------------------|----------|
| 2,500 | 1,310 |
| 5,000 | 1,930 |
| 10,000 | 2,990 |
| 15,000 | 3,850 |
| 20,000 | 4,610 |
| 25,000 | 5,300 |
| 30,000 | 5,940 |
| 35,000 | 6,540 |
| 40,000 | 7,100 |
| 45,000 | 7,640 |
| 50,000 | 8,150 |

### Key Difference vs Case 2

| Parameter | Case 2 (Ulsan) | Case 3 (Yeosu) | Difference |
|-----------|---------------|----------------|------------|
| Distance | 59 nm | 86 nm | +27 nm |
| Travel time (one-way) | 3.93 h | 5.73 h | +1.80 h |
| Round trip travel | 7.87 h | 11.47 h | +3.60 h |

The additional 3.60 hours of round-trip travel time per cycle reduces annual capacity and increases fuel consumption, making Case 3 approximately **$187M more expensive** than Case 2 over 20 years.

---

## 5.3 Cycle Time Verification

### 5.3.1 Vessels per Trip (VpT)

For Case 2/3 (`has_storage_at_busan = false`), VpT determines how many vessels can be served per shuttle trip:

```
VpT = floor(Shuttle_Size / Bunker_Volume)
    = floor(5,000 / 5,000)
    = 1 vessel per trip
```

**CSV value**: 1.0 -- [PASS]

### 5.3.2 Pumping Time per Vessel

For Case 2/3, pumping time is based on **bunker volume** (vessel demand), not shuttle size:

```
Pumping_Per_Vessel = Bunker_Volume / Pump_Rate
                   = 5,000 / 500
                   = 10.0 h
```

**CSV value**: 10.0 h -- [PASS]

### 5.3.3 Shore Loading Time

```
Shore_Loading = Shuttle_Size / Shore_Pump_Rate + Fixed_Time
             = 5,000 / 700 + 4.0
             = 7.1429 + 4.0
             = 11.1429 h
```

**CSV value**: 11.1429 h -- [PASS]

### 5.3.4 Basic Cycle Duration

The basic cycle covers the sea voyage and bunkering operations (excluding shore loading):

```
Basic_Cycle = Travel_Out + Port_Entry
            + [Movement + Setup_In + Pumping + Setup_Out] x VpT
            + Port_Exit + Travel_Return

            = 5.73 + 1.0
            + [1.0 + 2.0 + 10.0 + 2.0] x 1
            + 1.0 + 5.73

            = 5.73 + 1.0 + 15.0 + 1.0 + 5.73
            = 28.46 h
```

**CSV value**: 28.46 h -- [PASS]

### 5.3.5 Total Cycle Duration

```
Total_Cycle = Shore_Loading + Basic_Cycle
            = 11.1429 + 28.46
            = 39.6029 h
```

**CSV value**: 39.6029 h -- [PASS]

### 5.3.6 Comparison with Case 2

```
Case 2 Total Cycle = 11.1429 + 24.86 = 36.0029 h
Case 3 Total Cycle = 11.1429 + 28.46 = 39.6029 h
Difference         = 39.6029 - 36.0029 = 3.60 h (round-trip travel difference)
```

The 3.60 h difference is exactly `2 x (5.73 - 3.93) = 2 x 1.80 = 3.60 h`, confirming the travel time is the sole differentiator between Case 2 and Case 3.

### 5.3.7 Annual Cycles

```
Annual_Cycles_Max = H_max / Total_Cycle
                  = 8,000 / 39.6029
                  = 202.01 cycles/year
```

**CSV value**: 202.01 -- [PASS]

### 5.3.8 Timeline Diagram (One Full Cycle, 5,000 m3 Shuttle)

```
Time(h) 0        5       10      15      20      25      30      35   39.60
        |--------|--------|--------|--------|--------|--------|--------|--|
        [== Shore Loading (11.14h) ==]
                                    [= Travel Out (5.73h) =]
                                                            [PE(1h)]
                                                              [Mv(1h)]
                                                               [Setup_In(2h)]
                                                                 [== Pumping (10h) ==]
                                                                              [Setup_Out(2h)]
                                                                                [PX(1h)]
                                                                                 [= Travel Ret (5.73h) =]

Phase breakdown:
  Shore Loading  :  0.00 -- 11.14 h  (11.14 h)
  Travel Out     : 11.14 -- 16.87 h  ( 5.73 h)
  Port Entry     : 16.87 -- 17.87 h  ( 1.00 h)
  Movement       : 17.87 -- 18.87 h  ( 1.00 h)
  Setup In       : 18.87 -- 20.87 h  ( 2.00 h)
  Pumping        : 20.87 -- 30.87 h  (10.00 h)
  Setup Out      : 30.87 -- 32.87 h  ( 2.00 h)
  Port Exit      : 32.87 -- 33.87 h  ( 1.00 h)
  Travel Return  : 33.87 -- 39.60 h  ( 5.73 h)
  -------------------------------------------------
  TOTAL          :  0.00 -- 39.60 h  (39.60 h)

  Shore Loading  : 28.1% of cycle  (11.14 / 39.60)
  Travel (R/T)   : 28.9% of cycle  (11.47 / 39.60)
  Pumping        : 25.3% of cycle  (10.00 / 39.60)
  Overhead       : 17.7% of cycle  ( 7.00 / 39.60)
```

Note: Travel accounts for 28.9% of the cycle in Case 3 versus 21.8% in Case 2, reflecting the longer route distance.

---

## 5.4 CAPEX Verification

### 5.4.1 Shuttle CAPEX (per unit)

Using the power-law scaling formula:

```
CAPEX_shuttle = Ref_CAPEX x (Size / Ref_Size) ^ Exponent
              = $61,500,000 x (5,000 / 40,000) ^ 0.75
              = $61,500,000 x (0.125) ^ 0.75
              = $61,500,000 x 0.2102
              = $12,928,530 per shuttle
```

**CSV check (Year 2030)**: 3 shuttles purchased at total $38.7863M

```
Per shuttle = $38,786,300 / 3 = $12,928,767
Expected   = $12,928,530
Difference = $237 (rounding)
```

[PASS] -- Shuttle CAPEX matches within rounding tolerance.

### 5.4.2 Annualized Shuttle CAPEX

```
Annualized_CAPEX_shuttle = Actual_CAPEX / Annuity_Factor
                         = $38,786,300 / 10.8355
                         = $3,579,600
```

**CSV value (Year 2030)**: $3.5796M -- [PASS]

### 5.4.3 Pump CAPEX

```
CAPEX_pump = $158,730 per pump
Year 2030: New pumps = new_shuttles x pumps_per_shuttle (with bunkering equipment)
```

**CSV value (Year 2030)**: Actual_CAPEX_Pump = $1.6398M

Bunkering CAPEX per shuttle = Pump CAPEX + Equipment (3% of Shuttle CAPEX):

```
Per shuttle = $158,730 + ($12,928,530 x 0.03) = $158,730 + $387,856 = $546,586
3 shuttles  = 3 x $546,586 = $1,639,758 ≈ $1,639,800  [PASS]
```

### 5.4.4 Annualized Pump/Bunkering CAPEX

```
Annualized_CAPEX_Pump = Actual_CAPEX_Pump / Annuity_Factor
                      = $1,639,800 / 10.8355
                      = $151,300
```

**CSV value (Year 2030)**: $0.1513M -- [PASS]

### 5.4.5 20-Year NPC CAPEX Components

| Component | NPC (USD M) | Share of NPC |
|-----------|-------------|--------------|
| Annualized Shuttle CAPEX | 422.39 | 38.6% |
| Annualized Bunkering CAPEX | 17.86 | 1.6% |
| Annualized Terminal CAPEX | 0.00 | 0.0% |
| **Total CAPEX** | **440.25** | **40.2%** |

Terminal CAPEX is $0 because Case 3 has no storage facility at Busan (`has_storage_at_busan: false`).

---

## 5.5 OPEX Verification

### 5.5.1 Fixed OPEX

**Shuttle Fixed OPEX** (5% of actual CAPEX):

```
FixedOPEX_Shuttle = 0.05 x Actual_CAPEX_Shuttle
Year 2030: = 0.05 x $38,786,300 = $1,939,315
```

**CSV value (Year 2030)**: $1.9393M -- [PASS]

**Bunkering Equipment Fixed OPEX** (5% of actual CAPEX):

```
FixedOPEX_Pump = 0.05 x Actual_CAPEX_Pump
Year 2030: = 0.05 x $1,639,800 = $81,990
```

**CSV value (Year 2030)**: $0.082M -- [PASS]

### 5.5.2 20-Year NPC Fixed OPEX Components

| Component | NPC (USD M) | Share of NPC |
|-----------|-------------|--------------|
| Shuttle Fixed OPEX | 228.84 | 20.9% |
| Bunkering Fixed OPEX | 9.67 | 0.9% |
| Terminal Fixed OPEX | 0.00 | 0.0% |
| **Total Fixed OPEX** | **238.51** | **21.8%** |

### 5.5.3 Variable OPEX -- Shuttle Fuel

**Fuel consumption per cycle:**

```
Fuel_per_cycle = MCR x SFOC x Travel_Time x Travel_Factor / 1,000,000

Where:
  MCR          = 1,930 kW (for 5,000 m3 shuttle)
  SFOC         = 436 g/kWh
  Travel_Time  = 5.73 h (one-way)
  Travel_Factor = 2.0 (round trip)

  = 1,930 x 436 x 5.73 x 2.0 / 1,000,000
  = 841,480 x 5.73 / 1,000,000 x 2.0
  = 4,821,680.4 / 1,000,000 x 2.0
  = 4.8217 x 2.0
  = 9.6434 tons per cycle
```

**Fuel cost per cycle:**

```
Cost_per_cycle = 9.6434 x $600/ton = $5,786.0 per cycle
```

**Year 2030 verification (600 cycles):**

```
Annual_Shuttle_vOPEX = $5,786.0 x 600 = $3,471,600
```

**CSV value (Year 2030)**: $3.4716M -- [PASS]

### 5.5.4 Variable OPEX -- Pump Fuel

**Pump fuel consumption per cycle:**

```
Fuel_pump = P_pump x SFOC x Pumping_Time / 1,000,000

Where:
  P_pump       = 79.37 kW
  SFOC         = 436 g/kWh
  Pumping_Time = 10.0 h

  = 79.37 x 436 x 10.0 / 1,000,000
  = 346,053.2 / 1,000,000
  = 0.34605 tons per cycle
```

**Pump fuel cost per cycle:**

```
Cost_pump = 0.34605 x $600/ton = $207.63 per cycle
```

**Year 2030 verification (600 cycles):**

```
Annual_Pump_vOPEX = $207.63 x 600 = $124,578
```

**CSV value (Year 2030)**: $0.1246M ($124,600) -- [PASS] (within $22 rounding)

### 5.5.5 Fuel Cost Comparison with Case 2

| Metric | Case 2 (Ulsan) | Case 3 (Yeosu) | Difference |
|--------|---------------|----------------|------------|
| Travel time (one-way) | 3.93 h | 5.73 h | +1.80 h |
| Fuel per cycle | 6.618 tons | 9.643 tons | +3.025 tons |
| Fuel cost per cycle | $3,970.8 | $5,786.0 | +$1,815.2 |
| Additional cost per cycle | -- | +45.7% | -- |

The 45.7% higher fuel cost per cycle directly reflects the longer travel distance (86 nm vs 59 nm = 45.8% longer).

### 5.5.6 20-Year NPC Variable OPEX Components

| Component | NPC (USD M) | Share of NPC |
|-----------|-------------|--------------|
| Shuttle Variable OPEX | 400.97 | 36.6% |
| Bunkering Variable OPEX | 14.39 | 1.3% |
| Terminal Variable OPEX | 0.00 | 0.0% |
| **Total Variable OPEX** | **415.36** | **38.0%** |

---

## 5.6 NPC Verification

### 5.6.1 Component Sum Check

```
NPC_Total = Annualized_Shuttle_CAPEX
          + Annualized_Bunkering_CAPEX
          + Annualized_Terminal_CAPEX
          + Shuttle_fOPEX
          + Bunkering_fOPEX
          + Terminal_fOPEX
          + Shuttle_vOPEX
          + Bunkering_vOPEX
          + Terminal_vOPEX

          = 422.39
          +  17.86
          +   0.00
          + 228.84
          +   9.67
          +   0.00
          + 400.97
          +  14.39
          +   0.00

          = 1,094.12 USD M
```

**CSV value**: 1,094.12 USD M -- [PASS]

### 5.6.2 NPC Breakdown by Category

| Category | Amount (USD M) | Percentage |
|----------|---------------|------------|
| CAPEX (Annualized) | 440.25 | 40.2% |
| Fixed OPEX | 238.51 | 21.8% |
| Variable OPEX | 415.36 | 38.0% |
| **Total NPC** | **1,094.12** | **100.0%** |

### 5.6.3 NPC Breakdown by Asset

| Asset | CAPEX | Fixed OPEX | Variable OPEX | Total | Share |
|-------|-------|------------|---------------|-------|-------|
| Shuttle | 422.39 | 228.84 | 400.97 | 1,052.20 | 96.2% |
| Bunkering | 17.86 | 9.67 | 14.39 | 41.92 | 3.8% |
| Terminal | 0.00 | 0.00 | 0.00 | 0.00 | 0.0% |
| **Total** | **440.25** | **238.51** | **415.36** | **1,094.12** | **100.0%** |

Shuttle costs dominate at 96.2% of total NPC, even higher than Case 2 due to the increased fuel consumption from the longer voyage.

---

## 5.7 LCOA Verification

```
LCOA = NPC_Total / Total_Supply_20yr

Where:
  NPC_Total        = $1,094,120,000
  Total_Supply_ton = 235,620,000 tons (20-year cumulative)

LCOA = $1,094,120,000 / 235,620,000
     = $4.6434/ton
     ~ $4.64/ton
```

**CSV value**: 4.64 -- [PASS]

### LCOA Comparison Across Cases

| Case | NPC (USD M) | Total Supply (tons) | LCOA (USD/ton) |
|------|-------------|---------------------|-----------------|
| Case 1 (Busan) | 447.53 | 235,620,000 | 1.90 |
| Case 2 (Ulsan) | 906.80 | 235,620,000 | 3.85 |
| Case 3 (Yeosu) | 1,094.12 | 235,620,000 | 4.64 |

Case 3 LCOA is **$0.79/ton higher** than Case 2 and **$2.74/ton higher** than Case 1, driven entirely by the longer travel distance.

---

## 5.8 Year 2030 Detailed Verification

Year 2030 is the first year of operation with the lowest demand level.

### 5.8.1 Fleet and Demand

| Parameter | Value | Verification |
|-----------|-------|-------------|
| New Shuttles | 3 | From MILP optimization |
| Total Shuttles | 3 | Cumulative (first year) |
| Annual Cycles | 600 | Demand-driven |
| Annual Calls | 600 | = Annual_Cycles (VpT=1) |
| Supply (m3) | 3,000,000 | = 600 x 5,000 |
| Demand (m3) | 3,000,000 | Supply = Demand |

### 5.8.2 Fleet Capacity Check

```
Capacity per shuttle = Annual_Cycles_Max = 202.01 cycles/year
Fleet capacity       = 3 x 202.01 = 606.03 cycles/year
Required cycles      = 600
Utilization          = 600 / 606.03 = 99.0%
```

The fleet of 3 shuttles can just barely serve 600 annual cycles (606 capacity vs 600 required), operating at 99.0% utilization.

### 5.8.3 CAPEX Verification (Year 2030)

| Item | Formula | Value (USD M) | CSV (USD M) | Status |
|------|---------|---------------|-------------|--------|
| Shuttle CAPEX | 3 x $12.929M | 38.786 | 38.7863 | [PASS] |
| Pump CAPEX | (equipment package) | 1.640 | 1.6398 | [PASS] |
| Annualized Shuttle | 38.786 / 10.8355 | 3.580 | 3.5796 | [PASS] |
| Annualized Pump | 1.640 / 10.8355 | 0.151 | 0.1513 | [PASS] |

### 5.8.4 Fixed OPEX Verification (Year 2030)

| Item | Formula | Value (USD M) | CSV (USD M) | Status |
|------|---------|---------------|-------------|--------|
| Shuttle fOPEX | 0.05 x 38.786 | 1.939 | 1.9393 | [PASS] |
| Pump fOPEX | 0.05 x 1.640 | 0.082 | 0.082 | [PASS] |

### 5.8.5 Variable OPEX Verification (Year 2030)

| Item | Formula | Value (USD M) | CSV (USD M) | Status |
|------|---------|---------------|-------------|--------|
| Shuttle vOPEX | $5,786.0 x 600 | 3.4716 | 3.4716 | [PASS] |
| Pump vOPEX | $207.63 x 600 | 0.1246 | 0.1246 | [PASS] |

### 5.8.6 Year 2030 Total Cost

```
Total_2030 = Annualized_CAPEX + Fixed_OPEX + Variable_OPEX
           = (3.5796 + 0.1513) + (1.9393 + 0.082) + (3.4716 + 0.1246)
           = 3.7309 + 2.0213 + 3.5962
           = 9.3484 USD M
```

---

## 5.9 All Scenarios Overview

The following table shows MILP results for all evaluated shuttle sizes in Case 3 (pump rate fixed at 500 m3/h):

| Shuttle (m3) | Cycle (h) | VpT | NPC (USD M) | LCOA (USD/ton) | Rank |
|-------------|-----------|-----|-------------|-----------------|------|
| 2,500 | 36.03 | 1 | 1,375.75 | 5.84 | 7 |
| **5,000** | **39.60** | **1** | **1,094.12** | **4.64** | **1** |
| 10,000 | 61.75 | 2 | 1,196.81 | 5.08 | 2 |
| 15,000 | 83.89 | 3 | 1,364.67 | 5.79 | 6 |
| 20,000 | 106.03 | 4 | 1,518.71 | 6.45 | 8 |
| 25,000 | 128.17 | 5 | 1,684.98 | 7.15 | 9 |
| 30,000 | 150.32 | 6 | 1,850.92 | 7.86 | 10 |
| 35,000 | 172.46 | 7 | 2,009.95 | 8.53 | 11 |
| 40,000 | 194.60 | 8 | 2,169.72 | 9.21 | 12 |
| 45,000 | 216.75 | 9 | 2,336.84 | 9.92 | 13 |
| 50,000 | 238.89 | 10 | 2,487.47 | 10.56 | 14 |

### Key Observations

1. **Optimal at 5,000 m3**: The smallest practical shuttle (VpT=1) minimizes NPC because it avoids excess cycle time from serving multiple vessels per trip.

2. **Same optimal as Case 2**: Both Cases 2 and 3 share the optimal shuttle size of 5,000 m3, confirming that the VpT=1 configuration is universally optimal for direct delivery (no-storage) cases at this pump rate.

3. **NPC grows monotonically above 10,000 m3**: Larger shuttles serve more vessels per trip (VpT increases), but the idle/setup time per additional vessel outweighs any CAPEX scale economies.

4. **2,500 m3 is worse than 5,000 m3**: Although VpT=1 for both, the 2,500 m3 shuttle requires twice as many trips to deliver the same volume, resulting in a higher fleet count and thus higher total NPC despite lower per-unit CAPEX.

5. **Cycle time scales linearly with VpT**: Each additional vessel adds approximately 22.14 h to the cycle (movement + setup_in + pumping + setup_out = 1.0 + 2.0 + 10.0 + 2.0 + overhead adjustments).

---

## 5.10 Summary Verification Table

| Verification Item | Expected | CSV/Calculated | Status |
|-------------------|----------|----------------|--------|
| **Cycle Time** | | | |
| Vessels per Trip (VpT) | 1 | 1.0 | [PASS] |
| Pumping per Vessel | 10.0 h | 10.0 h | [PASS] |
| Shore Loading | 11.1429 h | 11.1429 h | [PASS] |
| Basic Cycle Duration | 28.46 h | 28.46 h | [PASS] |
| Total Cycle Duration | 39.6029 h | 39.6029 h | [PASS] |
| Annual Cycles Max | 202.01 | 202.01 | [PASS] |
| **CAPEX** | | | |
| Shuttle CAPEX (per unit) | $12.929M | $12.929M | [PASS] |
| Annualized Shuttle CAPEX (2030) | $3.580M | $3.5796M | [PASS] |
| Annualized Pump CAPEX (2030) | $0.151M | $0.1513M | [PASS] |
| **Fixed OPEX** | | | |
| Shuttle fOPEX (2030) | $1.939M | $1.9393M | [PASS] |
| Pump fOPEX (2030) | $0.082M | $0.082M | [PASS] |
| **Variable OPEX** | | | |
| Shuttle fuel/cycle | $5,786.0 | $5,786.0 | [PASS] |
| Pump fuel/cycle | $207.63 | $207.67 | [PASS] |
| Shuttle vOPEX (2030) | $3.4716M | $3.4716M | [PASS] |
| Pump vOPEX (2030) | $0.1246M | $0.1246M | [PASS] |
| **NPC** | | | |
| Component sum | 1,094.12 | 1,094.12 | [PASS] |
| NPC Total | $1,094.12M | $1,094.12M | [PASS] |
| **LCOA** | | | |
| LCOA | $4.64/ton | $4.64/ton | [PASS] |

**Result: 17/17 checks passed. All Case 3 calculations verified.**
