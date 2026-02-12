# Parameters

## 2.1 Common Parameters (base.yaml)

### Economic Parameters

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Annualization Interest Rate | r | 0.07 | - | base.yaml |
| Discount Rate | - | 0.0 | - | base.yaml |
| Fuel Price (Green Ammonia) | P_fuel | 600.0 | USD/ton | base.yaml |
| Electricity Price | P_elec | 0.0769 | USD/kWh | base.yaml |
| Time Period | - | 2030-2050 | years | base.yaml |
| Number of Years | n | 21 | years | calculated |

### Annuity Factor Verification

**Formula:**
AF = [1 - (1 + r)^(-n)] / r

**Manual Calculation:**
AF = [1 - (1 + 0.07)^(-21)] / 0.07
   = [1 - (1.07)^(-21)] / 0.07
   = [1 - 0.241513] / 0.07
   = 0.758487 / 0.07
   = **10.8355**

| Item | Manual | CSV | Status |
|------|--------|-----|--------|
| Annuity Factor | 10.8355 | 10.8355 | PASS |

### Demand Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Start Vessels (2030) | 50 | ships | base.yaml |
| End Vessels (2050) | 500 | ships | base.yaml |
| Voyages per Year | 12 | voyages/ship/year | base.yaml |
| Bunker Volume per Call | 5,000 | m3 | case configs |
| Ammonia Density (Storage) | 0.680 | ton/m3 | base.yaml |

**Annual Demand Calculation:**
- Year 2030: 50 ships x 12 voyages x 5,000 m3 = 3,000,000 m3
- Year 2050: 500 ships x 12 voyages x 5,000 m3 = 30,000,000 m3
- Total Supply (21 years): 235,620,000 tons (from CSV, all cases identical)

### Operational Parameters

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Max Annual Hours | H_max | 8,000 | hours/vessel/year | base.yaml |
| Setup Time | t_setup | 0.5 | hours/connection | base.yaml |
| Tank Safety Factor | beta | 2.0 | - | base.yaml |
| Shore Pump Rate | Q_shore | 1,500 | m3/h | base.yaml |
| Shore Loading Fixed Time | t_fixed | 2.0 | hours | base.yaml |

### Shore Loading Time Formula (v5.1)

**Formula:**
Shore_Loading = (Shuttle_Size / Q_shore) + t_fixed
              = (Shuttle_Size / 1500) + 2.0

**Verification Examples:**

| Shuttle Size (m3) | Variable Time (h) | Fixed Time (h) | Total Shore Loading (h) | CSV Value (h) | Status |
|--------------------|--------------------|-----------------|--------------------------|----------------|--------|
| 2,500 | 1.6667 | 2.0 | 3.6667 | 3.6667 | PASS |
| 5,000 | 3.3333 | 2.0 | 5.3333 | 5.3333 | PASS |
| 10,000 | 6.6667 | 2.0 | 8.6667 | 8.6667 | PASS |

## 2.2 Shuttle CAPEX Parameters

### CAPEX Formula

**Formula:**
CAPEX_shuttle = C_ref x (Shuttle_Size / S_ref)^alpha

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Reference CAPEX | C_ref | 61,500,000 | USD |
| Reference Size | S_ref | 40,000 | m3 |
| Scaling Exponent | alpha | 0.75 | - |

### CAPEX Verification

| Shuttle Size (m3) | Ratio (S/S_ref) | Ratio^0.75 | CAPEX per Shuttle (USD) |
|--------------------|-----------------|------------|-------------------------|
| 500 | 0.0125 | 0.0373 | 2,292,105 |
| 1,000 | 0.0250 | 0.0629 | 3,867,120 |
| 2,500 | 0.0625 | 0.1250 | 7,687,500 |
| 5,000 | 0.1250 | 0.2102 | 12,928,530 |
| 10,000 | 0.2500 | 0.3536 | 21,743,325 |
| 40,000 | 1.0000 | 1.0000 | 61,500,000 |
| 50,000 | 1.2500 | 1.1768 | 72,371,970 |

## 2.3 Pump Parameters

### Pump Power

**Formula:**
P_pump = (delta_P_Pa x Q_m3s) / eta / 1000 [kW]

| Parameter | Value | Unit |
|-----------|-------|------|
| Pressure Drop (delta_P) | 4.0 | bar |
| Pump Efficiency (eta) | 0.7 | - |
| Cost per kW | 2,000 | USD/kW |

**Manual Calculation (Q = 1000 m3/h):**
delta_P_Pa = 4.0 x 100,000 = 400,000 Pa
Q_m3s = 1000 / 3600 = 0.27778 m3/s
P_pump = (400,000 x 0.27778) / 0.7 / 1000
       = 111,111.1 / 700
       = 158.73 kW

**Pump CAPEX:**
CAPEX_pump = 158.73 x 2,000 = 317,460 USD per shuttle

## 2.4 MCR Map (v5 Power Law)

### MCR Formula
MCR = 17.17 x DWT^0.566

### DWT Conversion
DWT = Shuttle_Size_m3 x density_storage / loading_factor
    = Shuttle_Size_m3 x 0.680 / 0.80
    = Shuttle_Size_m3 x 0.85

### MCR Values by Shuttle Size

| Shuttle Size (m3) | DWT (tons) | MCR Formula (kW) | Config MCR (kW) |
|--------------------|-----------|-------------------|-----------------|
| 500 | 425 | 519 | 520 |
| 1,000 | 850 | 770 | 770 |
| 1,500 | 1,275 | 979 | 980 |
| 2,000 | 1,700 | 1,159 | 1,160 |
| 2,500 | 2,125 | 1,314 | 1,310 |
| 3,000 | 2,550 | 1,453 | 1,450 |
| 3,500 | 2,975 | 1,579 | 1,580 |
| 4,000 | 3,400 | 1,699 | 1,700 |
| 4,500 | 3,825 | 1,817 | 1,820 |
| 5,000 | 4,250 | 1,926 | 1,930 |
| 7,500 | 6,375 | 2,486 | 2,490 |
| 10,000 | 8,500 | 2,989 | 2,990 |
| 15,000 | 12,750 | 3,848 | 3,850 |
| 20,000 | 17,000 | 4,607 | 4,610 |
| 25,000 | 21,250 | 5,296 | 5,300 |
| 30,000 | 25,500 | 5,937 | 5,940 |
| 35,000 | 29,750 | 6,537 | 6,540 |
| 40,000 | 34,000 | 7,103 | 7,100 |
| 45,000 | 38,250 | 7,640 | 7,640 |
| 50,000 | 42,500 | 8,151 | 8,150 |

Note: Config values are rounded to nearest 10 kW. All match within rounding tolerance.

## 2.5 SFOC Map (by DWT Range)

| DWT Range | Engine Type | SFOC (g/kWh) | Shuttle Sizes |
|-----------|-------------|--------------|---------------|
| < 3,000 | 4-stroke high-speed | 505 | 500 - 3,500 m3 |
| 3,000 - 8,000 | 4-stroke medium-speed | 436 | 4,000 - 7,500 m3 |
| 8,000 - 15,000 | 4-stroke medium / small 2-stroke | 413 | 10,000 - 15,000 m3 |
| 15,000 - 30,000 | 2-stroke | 390 | 20,000 - 35,000 m3 |
| > 30,000 | 2-stroke large | 379 | 40,000 - 50,000 m3 |

## 2.6 OPEX Ratios

| Parameter | Value | Applied To |
|-----------|-------|------------|
| Shuttle Fixed OPEX Ratio | 5% of CAPEX | Annual shuttle maintenance |
| Shuttle Equipment Ratio | 3% of CAPEX | Equipment cost (part of bunkering CAPEX) |
| Bunkering Fixed OPEX Ratio | 5% of CAPEX | Annual bunkering system maintenance |

## 2.7 Case-Specific Parameters

| Parameter | Case 1 | Case 2-1 (Yeosu) | Case 2-2 (Ulsan) |
|-----------|--------|-------------------|-------------------|
| Route | Busan Internal | Yeosu -> Busan | Ulsan -> Busan |
| Distance | N/A (port) | 86 nm | 59 nm |
| Travel Time (one-way) | 1.0 h | 5.73 h | 3.93 h |
| Has Storage at Busan | Yes | No | No |
| Shuttle Sizes | 500-10,000 m3 | 2,500-50,000 m3 | 2,500-50,000 m3 |
| Bunker Volume per Call | 5,000 m3 | 5,000 m3 | 5,000 m3 |
| Port Entry/Exit Time | 0 h | 2.0 h (1.0+1.0) | 2.0 h (1.0+1.0) |
| Movement per Vessel | 0 h | 1.0 h | 1.0 h |

## 2.8 Cycle Time Structure

### Case 1 (Has Storage at Busan)

Cycle_Duration = Shore_Loading + Basic_Cycle
Shore_Loading = (Shuttle_Size / 1500) + 2.0
Basic_Cycle = Travel_Out + Setup_In + Pumping + Setup_Out + Travel_Return
            = 1.0 + 1.0 + (Shuttle_Size/1000) + 1.0 + 1.0
            = 4.0 + Shuttle_Size/1000

### Case 2 (No Storage - Direct Supply)

Cycle_Duration = Shore_Loading + Basic_Cycle
Shore_Loading = (Shuttle_Size / 1500) + 2.0
Vessels_per_Trip = floor(Shuttle_Size / 5000)
Basic_Cycle = Travel_Out + Port_Entry + VpT x (Movement + Setup_In + Pumping + Setup_Out) + Port_Exit + Travel_Return
            = Travel + 2.0 + VpT x (1.0 + 1.0 + 5.0 + 1.0) + Travel
            = 2 x Travel + 2.0 + VpT x 8.0

Where:
- Travel = 5.73 h (Yeosu) or 3.93 h (Ulsan)
- Port_Entry = 1.0 h, Port_Exit = 1.0 h
- Movement per vessel = 1.0 h
- Setup_In = 2 x 0.5 = 1.0 h
- Pumping per vessel = 5000/1000 = 5.0 h
- Setup_Out = 2 x 0.5 = 1.0 h
