# 2. Input Parameters

All parameters are sourced from YAML configuration files in `config/`.

## 2.1 Economic Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Discount Rate | r_disc | 0.0 | - | `economy.discount_rate` |
| Annualization Interest Rate | r | 0.07 | - | `economy.annualization_interest_rate` |
| Fuel Price | P_fuel | 600.0 | USD/ton | `economy.fuel_price_usd_per_ton` |
| Project Period | n | 21 | years | 2030-2050 inclusive |

## 2.2 Shipping Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Start Vessels (2030) | V_start | 50 | ships | `shipping.start_vessels` |
| End Vessels (2050) | V_end | 500 | ships | `shipping.end_vessels` |
| Voyages per Year | k_voy | 12 | - | `shipping.voyages_per_year` |
| Fuel per Voyage | m_voy | 2,158,995 | kg | `shipping.kg_per_voyage` |

## 2.3 Operational Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Max Annual Hours | H_max | 8,000 | h/yr | `operations.max_annual_hours_per_vessel` |
| **Setup Time (per endpoint)** | **t_setup** | **2.0** | **h** | **`operations.setup_time_hours`** |
| Tank Safety Factor | beta | 2.0 | - | `operations.tank_safety_factor` |

**v6.0 Change**: Setup time increased from 1.0h to 2.0h per endpoint. The code multiplier
(`2.0 * config_value`) was removed; the config now stores the direct per-endpoint value.

## 2.4 Shore Supply Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| **Shore Pump Rate** | **Q_shore** | **700.0** | **m3/h** | **`shore_supply.pump_rate_m3ph`** |
| **Fixed Loading Time** | **t_fixed** | **4.0** | **h** | **`shore_supply.loading_time_fixed_hours`** |
| Cost Enabled | - | false | - | `shore_supply.enabled` |

**v6.0 Changes**: Shore pump rate reduced from 1,500 to 700 m3/h. Fixed loading time increased
from 2.0 to 4.0 hours (represents 2.0h inbound setup + 2.0h outbound setup at shore terminal).

## 2.5 Shuttle CAPEX Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Reference CAPEX | C_ref | 61,500,000 | USD | `shuttle.ref_capex_usd` |
| Reference Size | S_ref | 40,000 | m3 | `shuttle.ref_size_cbm` |
| Scaling Exponent | alpha | 0.75 | - | `shuttle.capex_scaling_exponent` |
| Fixed OPEX Ratio | r_fopex | 0.05 | - | `shuttle.fixed_opex_ratio` |
| Equipment Ratio | r_equip | 0.03 | - | `shuttle.equipment_ratio` |

## 2.6 Pump Parameters (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Pump Pressure Drop | delta_P | 4.0 | bar | `propulsion.pump_delta_pressure_bar` |
| Pump Efficiency | eta | 0.7 | - | `propulsion.pump_efficiency` |
| Pump Power Cost | C_kw | 2,000 | USD/kW | `propulsion.pump_power_cost_usd_per_kw` |
| Default SFOC | SFOC_def | 379 | g/kWh | `propulsion.sfoc_g_per_kwh` |

## 2.7 Ammonia Properties (base.yaml)

| Parameter | Symbol | Value | Unit | Source |
|-----------|--------|-------|------|--------|
| Storage Density | rho_s | 0.680 | ton/m3 | `ammonia.density_storage_ton_m3` |
| Bunkering Density | rho_b | 0.681 | ton/m3 | `ammonia.density_bunkering_ton_m3` |

## 2.8 Case-Specific Parameters

### Case 1: Busan Port (case_1.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Travel Time (one-way) | 1.0 | h |
| Has Storage at Busan | true | - |
| Shuttle Sizes | 500-10,000 | m3 |
| Bunker Volume per Call | 5,000 | m3 |
| Tank Storage | 35,000 tons | - |

### Case 2-1: Yeosu (case_2_yeosu.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Distance | 86 | nm |
| Ship Speed | 15 | knots |
| Travel Time (one-way) | 5.73 | h |
| Has Storage at Busan | false | - |
| Shuttle Sizes | 2,500-50,000 | m3 |
| Bunker Volume per Call | 5,000 | m3 |

### Case 2-2: Ulsan (case_2_ulsan.yaml)

| Parameter | Value | Unit |
|-----------|-------|------|
| Distance | 59 | nm |
| Ship Speed | 15 | knots |
| Travel Time (one-way) | 3.93 | h |
| Has Storage at Busan | false | - |
| Shuttle Sizes | 2,500-50,000 | m3 |
| Bunker Volume per Call | 5,000 | m3 |

## 2.9 SFOC Map (base.yaml: sfoc_map_g_per_kwh)

| DWT Range | Engine Type | SFOC (g/kWh) | Shuttle Sizes |
|-----------|-------------|-------------|---------------|
| < 3,000 | 4-stroke high-speed | 505 | 500-3,500 m3 |
| 3,000-8,000 | 4-stroke medium-speed | 436 | 4,000-7,500 m3 |
| 8,000-15,000 | 4-stroke medium / 2-stroke | 413 | 10,000-15,000 m3 |
| 15,000-30,000 | 2-stroke | 390 | 20,000-35,000 m3 |
| > 30,000 | 2-stroke large | 379 | 40,000-50,000 m3 |

## 2.10 MCR Map (case-specific yaml)

### Case 1 MCR (Power Law: 17.17 x DWT^0.566)

| Size (m3) | DWT | MCR (kW) |
|-----------|-----|----------|
| 500 | 425 | 520 |
| 1,000 | 850 | 770 |
| 1,500 | 1,275 | 980 |
| 2,000 | 1,700 | 1,160 |
| **2,500** | **2,125** | **1,310** |
| 3,000 | 2,550 | 1,450 |
| 3,500 | 2,975 | 1,580 |
| 4,000 | 3,400 | 1,700 |
| 4,500 | 3,825 | 1,820 |
| 5,000 | 4,250 | 1,930 |
| 7,500 | 6,375 | 2,490 |
| 10,000 | 8,500 | 2,990 |

### Case 2 MCR (Same Power Law, larger sizes)

| Size (m3) | DWT | MCR (kW) |
|-----------|-----|----------|
| 2,500 | 2,125 | 1,310 |
| **5,000** | **4,250** | **1,930** |
| 10,000 | 8,500 | 2,990 |
| 15,000 | 12,750 | 3,850 |
| 20,000 | 17,000 | 4,610 |
| 25,000 | 21,250 | 5,300 |
| 30,000 | 25,500 | 5,940 |
| 35,000 | 29,750 | 6,540 |
| 40,000 | 34,000 | 7,100 |
| 45,000 | 38,250 | 7,640 |
| 50,000 | 42,500 | 8,150 |

## 2.11 Derived Constants

| Constant | Formula | Value |
|----------|---------|-------|
| Annuity Factor | [1-(1.07)^(-21)]/0.07 | 10.8355 |
| Pump Power (1000 m3/h) | (4bar x 1000m3h) / 0.7 | 158.73 kW |
| Pump CAPEX (1000 m3/h) | 158.73 x 2000 | $317,460 |
| Bunker Volume | 5,000 | m3/call |
| Total Supply (21yr) | 346.5M m3 x 0.680 | 235,620,000 tons |
