# 2. Input Parameters

All parameters are sourced from YAML configuration files. Config values are authoritative.

## 2.1 Economic Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Discount rate | r_d | 0.0 | - | `economy.discount_rate` |
| Annualization interest rate | r | 0.07 | - | `economy.annualization_interest_rate` |
| Fuel price | P_fuel | 600.0 | USD/ton | `economy.fuel_price_usd_per_ton` |
| Electricity price | P_elec | 0.0769 | USD/kWh | `economy.electricity_price_usd_per_kwh` |

## 2.2 Time Period (base.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Start year | 2030 | year |
| End year | 2050 | year |
| Total years (n) | 21 | years |

## 2.3 Shipping Parameters (base.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Start vessels (2030) | 50 | vessels |
| End vessels (2050) | 500 | vessels |
| Voyages per vessel per year | 12 | voyages/yr |
| Fuel per voyage | 2,158,995 | kg |
| Bunker volume per call | 5,000 | m3 |

## 2.4 Operations Parameters (base.yaml)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Max annual hours per vessel | H_max | 8,000 | hours/year |
| Setup time per endpoint | t_setup | 2.0 | hours |
| Tank safety factor | Beta | 2.0 | - |
| Daily peak factor | F_peak | 1.5 | - |

## 2.5 Shore Supply Parameters (base.yaml)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Shore pump rate | Q_shore | 700 | m3/h |
| Loading fixed time | t_fixed | 4.0 | hours |
| Cost enabled | - | false | - |

**Note**: Shore supply loading time is ALWAYS included in cycle time regardless of cost enabled flag.

## 2.6 Shuttle CAPEX Parameters (base.yaml)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Reference CAPEX | C_ref | 61,500,000 | USD |
| Reference size | S_ref | 40,000 | m3 |
| Scaling exponent | alpha | 0.75 | - |
| Fixed OPEX ratio | - | 0.05 | ratio |
| Equipment ratio | - | 0.03 | ratio |

## 2.7 Bunkering System Parameters (base.yaml)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Fixed OPEX ratio | - | 0.05 | ratio |
| Equipment ratio | - | 0.03 | ratio |

## 2.8 STS Pump Parameters (base.yaml)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Available flow rate | Q_pump | 500 | m3/h |
| Pressure drop | delta_P | 4.0 | bar |
| Pump efficiency | eta | 0.7 | - |
| Pump cost | C_pump_kw | 2,000 | USD/kW |

## 2.9 Ammonia Properties (base.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Storage density | 0.680 | ton/m3 |
| Bunkering density | 0.681 | ton/m3 |

## 2.10 Tank Storage Parameters (base.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Tank size | 35,000 | tons |
| Cost per kg | 1.215 | USD/kg |
| Cooling energy | 0.0378 | kWh/kg |
| Fixed OPEX ratio | 0.03 | ratio |

## 2.11 SFOC Map (base.yaml)

SFOC values are mapped by shuttle size based on DWT-class engine type.

| DWT Range | Engine Type | SFOC (g/kWh) | Shuttle Sizes (m3) |
|-----------|-------------|-------------|-------------------|
| < 3,000 | 4-stroke high-speed | 505 | 500 - 3,500 |
| 3,000 - 8,000 | 4-stroke medium-speed | 436 | 4,000 - 7,500 |
| 8,000 - 15,000 | 4-stroke medium / small 2-stroke | 413 | 10,000 - 15,000 |
| 15,000 - 30,000 | 2-stroke | 390 | 20,000 - 35,000 |
| > 30,000 | 2-stroke large | 379 | 40,000 - 50,000 |

## 2.12 Case-Specific Parameters

### Case 1: Busan Port with Storage (case_1.yaml)

| Parameter | Value |
|-----------|-------|
| Travel time (one-way) | 1.0 h |
| Has storage at Busan | true |
| Tank storage enabled | true |
| Shuttle sizes | 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 7500, 10000 m3 |

**MCR Map (case_1.yaml):**

| Shuttle (m3) | DWT (ton) | MCR (kW) |
|-------------|-----------|----------|
| 500 | 425 | 520 |
| 1000 | 850 | 770 |
| 1500 | 1,275 | 980 |
| 2000 | 1,700 | 1,160 |
| 2500 | 2,125 | 1,310 |
| 3000 | 2,550 | 1,450 |
| 3500 | 2,975 | 1,580 |
| 4000 | 3,400 | 1,700 |
| 4500 | 3,825 | 1,820 |
| 5000 | 4,250 | 1,930 |
| 7500 | 6,375 | 2,490 |
| 10000 | 8,500 | 2,990 |

### Case 2: Ulsan to Busan (case_2_ulsan.yaml)

| Parameter | Value |
|-----------|-------|
| Distance | 59.0 nm |
| Speed | 15.0 knots |
| Travel time (one-way) | 3.93 h (= 59/15) |
| Has storage at Busan | false |
| Tank storage enabled | false |
| Shuttle sizes | 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000 m3 |

**MCR Map (case_2_ulsan.yaml):**

| Shuttle (m3) | DWT (ton) | MCR (kW) |
|-------------|-----------|----------|
| 2500 | 2,125 | 1,310 |
| 5000 | 4,250 | 1,930 |
| 10000 | 8,500 | 2,990 |
| 15000 | 12,750 | 3,850 |
| 20000 | 17,000 | 4,610 |
| 25000 | 21,250 | 5,300 |
| 30000 | 25,500 | 5,940 |
| 35000 | 29,750 | 6,540 |
| 40000 | 34,000 | 7,100 |
| 45000 | 38,250 | 7,640 |
| 50000 | 42,500 | 8,150 |

### Case 3: Yeosu to Busan (case_3_yeosu.yaml)

| Parameter | Value |
|-----------|-------|
| Distance | 86.0 nm |
| Speed | 15.0 knots |
| Travel time (one-way) | 5.73 h (= 86/15) |
| Has storage at Busan | false |
| Tank storage enabled | false |
| Shuttle sizes | 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000 m3 |

**MCR Map**: Same as Case 2 (identical shuttle sizes and MCR values).

## 2.13 Derived Parameters

These values are calculated from base parameters:

### Annuity Factor

```
AF = [1 - (1 + r)^(-n)] / r
   = [1 - (1.07)^(-21)] / 0.07
   = [1 - 0.24151] / 0.07
   = 0.75849 / 0.07
   = 10.8355
```

### Pump Power (500 m3/h)

```
P_pump = (delta_P_Pa x Q_m3s) / eta / 1000
       = (400,000 x 0.13889) / 0.7 / 1000
       = 79.37 kW
```

### Pump CAPEX

```
CAPEX_pump = P_pump x C_pump_kw
           = 79.37 x 2,000
           = 158,730 USD
```

### Shore Loading Time Formula

```
T_shore = Shuttle_Size / Q_shore + t_fixed
        = Shuttle_Size / 700 + 4.0  [hours]
```

### Demand per Year

```
Demand(year) = Vessels(year) x Voyages x Bunker_Volume
             = Vessels(year) x 12 x 5,000  [m3]

Where Vessels(year) = floor(50 + 450 x (year - 2030) / 20)
```

### Total 20-Year Supply

From CSV: **235,620,000 tons** across all 21 years (2030-2050).
