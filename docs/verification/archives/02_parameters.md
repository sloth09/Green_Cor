# Chapter 2: Parameters

## 2.1 Economic Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Discount Rate | **0.0** | - | base.yaml |
| Annualization Interest Rate | **0.07** | - | base.yaml |
| Fuel Price | 600.0 | USD/ton | base.yaml |
| Electricity Price | 0.0769 | USD/kWh | base.yaml |

> **Note**: With discount_rate = 0.0, all years are weighted equally (no time value of money).

---

## 2.2 Time Period

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Start Year | 2030 | year | base.yaml |
| End Year | 2050 | year | base.yaml |
| Analysis Period | **21** | years | Calculated |

---

## 2.3 Shipping Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Fuel per Voyage | 2,158,995 | kg | base.yaml |
| Voyages per Year | 12 | voyages/vessel/year | base.yaml |
| Start Vessels (2030) | 50 | vessels | base.yaml |
| End Vessels (2050) | 500 | vessels | base.yaml |

### Vessel Growth Calculation

```
Vessels(year) = 50 + (500 - 50) × (year - 2030) / (2050 - 2030)
             = 50 + 22.5 × (year - 2030)
```

| Year | Vessels |
|------|---------|
| 2030 | 50 |
| 2035 | 163 |
| 2040 | 275 |
| 2045 | 388 |
| 2050 | 500 |

---

## 2.4 Ammonia Properties

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Density (Storage) | 0.680 | ton/m3 | base.yaml |
| Density (Bunkering) | 0.681 | ton/m3 | base.yaml |

---

## 2.5 Operational Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Max Annual Hours | **8000** | hours/vessel/year | base.yaml |
| Setup Time (Hose) | 0.5 | hours | base.yaml |
| Tank Safety Factor | 2.0 | - | base.yaml |
| Daily Peak Factor | 1.5 | - | base.yaml |

---

## 2.6 Pump Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Main Analysis Rate | **1000** | m3/h | base.yaml (available_flow_rates) |
| Shore Pump Rate | **1500** | m3/h | base.yaml (shore_supply.pump_rate_m3ph) |
| Pump Pressure Drop | 4.0 | bar | base.yaml |
| Pump Efficiency | 0.7 | - | base.yaml |
| Pump Power Cost | 2000 | USD/kW | base.yaml |

### Sensitivity Analysis Range

| Rate (m3/h) | Analysis Type |
|-------------|---------------|
| 400 | Sensitivity (S7) |
| 600 | Sensitivity (S7) |
| 800 | Sensitivity (S7) |
| **1000** | **Main Analysis** |
| 1200 | Sensitivity (S7) |
| 1400 | Sensitivity (S7) |
| 1600 | Sensitivity (S7) |
| 1800 | Sensitivity (S7) |
| 2000 | Sensitivity (S7) |

---

## 2.7 Shuttle CAPEX Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Reference CAPEX | 61,500,000 | USD | base.yaml |
| Reference Size | 40,000 | m3 | base.yaml |
| Scaling Exponent | 0.75 | - | base.yaml |
| Fixed OPEX Ratio | 0.05 | % of CAPEX | base.yaml |
| Equipment Ratio | 0.03 | % of CAPEX | base.yaml |

### CAPEX Formula

```
Shuttle_CAPEX = 61,500,000 × (Shuttle_Size / 40,000)^0.75
```

### Example Calculations

| Shuttle Size (m3) | CAPEX (USD) |
|-------------------|-------------|
| 500 | $2,450,715 |
| 1,000 | $4,121,543 |
| 2,500 | $7,761,316 |
| 5,000 | $13,051,896 |
| 10,000 | $21,951,652 |
| 15,000 | $29,631,149 |

---

## 2.8 Tank Storage Parameters (Case 1 Only)

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Tank Size | 35,000 | tons | case_1.yaml |
| Cost per kg | 1.215 | USD/kg | base.yaml |
| Cooling Energy | 0.0378 | kWh/kg | base.yaml |
| Fixed OPEX Ratio | 0.03 | % of CAPEX | base.yaml |

### Tank CAPEX Calculation

```
Tank_CAPEX = 35,000 × 1000 × $1.215 = $42,525,000
```

---

## 2.9 Case-Specific Parameters

### Case 1: Busan Port with Storage

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Travel Time (one-way) | 1.0 | hours | case_1.yaml |
| Has Storage at Busan | **true** | - | case_1.yaml |
| Port Pump Rate | 1500 | m3/h | case_1.yaml |
| Bunker Volume per Call | 5000 | m3 | case_1.yaml |

**Available Shuttle Sizes**: 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 7500, 10000 m3

### Case 2-1: Yeosu to Busan

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Distance | 86 | nautical miles | case_2_yeosu.yaml |
| Speed | 15 | knots | case_2_yeosu.yaml |
| Travel Time (one-way) | **5.73** | hours | Calculated (86/15) |
| Has Storage at Busan | **false** | - | case_2_yeosu.yaml |
| Bunker Volume per Call | 5000 | m3 | case_2_yeosu.yaml |

**Available Shuttle Sizes**: 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000 m3

### Case 2-2: Ulsan to Busan

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Distance | 25 | nautical miles | case_2_ulsan.yaml |
| Speed | 15 | knots | case_2_ulsan.yaml |
| Travel Time (one-way) | **1.67** | hours | Calculated (25/15) |
| Has Storage at Busan | **false** | - | case_2_ulsan.yaml |
| Bunker Volume per Call | 5000 | m3 | case_2_ulsan.yaml |

**Available Shuttle Sizes**: 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000 m3

---

## 2.10 Annualization Calculation

### Annuity Factor Formula

```
AF = [1 - (1 + r)^(-n)] / r
where:
  r = 0.07 (annualization interest rate)
  n = 21 years (2030-2050 inclusive)
```

### Verification

```
AF = [1 - (1.07)^(-21)] / 0.07
   = [1 - 0.2415] / 0.07
   = 0.7585 / 0.07
   = 10.8355
```

**CSV Verification**: All scenario files show `Annuity_Factor = 10.8355` [PASS]

---

## 2.11 MCR (Maximum Continuous Rating) Values

### Case 1 MCR Map (kW)

| Size (m3) | MCR (kW) |
|-----------|----------|
| 500 | 1296 |
| 1000 | 1341 |
| 1500 | 1385 |
| 2000 | 1429 |
| 2500 | 1473 |
| 3000 | 1517 |
| 3500 | 1562 |
| 4000 | 1606 |
| 4500 | 1650 |
| 5000 | 1694 |
| 7500 | 1927 |
| 10000 | 2159 |

### Case 2 MCR Map (kW)

| Size (m3) | MCR (kW) |
|-----------|----------|
| 2500 | 1473 |
| 5000 | 1694 |
| 10000 | 2159 |
| 15000 | 2485 |
| 20000 | 2751 |
| 25000 | 2981 |
| 30000 | 3185 |
| 35000 | 3372 |
| 40000 | 3546 |
| 45000 | 3710 |
| 50000 | 3867 |
