# Chapter 2: Input Parameters

This chapter documents all input parameters used in the MILP optimization model, organized by category.

---

## 2.1 Economic Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Discount Rate | 0.0 | - | base.yaml |
| Annualization Interest Rate | 7% | %/year | base.yaml |
| Fuel Price (Ammonia) | 600 | USD/ton | base.yaml |
| Electricity Price | 0.0769 | USD/kWh | base.yaml |
| Annuity Factor | 10.8355 | - | Calculated |

### Annuity Factor Calculation

```
Annuity Factor = [1 - (1 + r)^(-n)] / r
               = [1 - (1 + 0.07)^(-21)] / 0.07
               = [1 - 0.2415] / 0.07
               = 0.7585 / 0.07
               = 10.8355
```

Where:
- r = 0.07 (7% annualization interest rate)
- n = 21 (years from 2030 to 2050 inclusive)

---

## 2.2 Time Period

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Start Year | 2030 | year | base.yaml |
| End Year | 2050 | year | base.yaml |
| Total Years | 21 | years | Calculated |

---

## 2.3 Fleet Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Start Vessels (2030) | 50 | ships | base.yaml |
| End Vessels (2050) | 500 | ships | base.yaml |
| Voyages per Year | 12 | voyages/ship/year | base.yaml |
| Fuel per Voyage | 2,158,995 | kg | base.yaml |

### Vessel Growth (Linear)

| Year | Vessels | Annual Calls (at 12/year) |
|------|---------|---------------------------|
| 2030 | 50 | 600 |
| 2035 | 163 | 1,956 |
| 2040 | 275 | 3,300 |
| 2045 | 388 | 4,656 |
| 2050 | 500 | 6,000 |

---

## 2.4 Operational Parameters

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Max Annual Hours | 8,000 | hours/year | base.yaml |
| Setup Time (per connection) | 0.5 | hours | base.yaml |
| Shore Pump Rate | 1,500 | m3/h | base.yaml |
| Tank Safety Factor | 2.0 | - | base.yaml |
| Daily Peak Factor | 1.5 | - | base.yaml |

---

## 2.5 Ammonia Properties

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Storage Density | 0.680 | ton/m3 | base.yaml |
| Bunkering Density | 0.681 | ton/m3 | base.yaml |

---

## 2.6 Cost Parameters

### Shuttle Vessel Costs

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Reference CAPEX | 61,500,000 | USD | base.yaml |
| Reference Size | 40,000 | m3 | base.yaml |
| Scaling Exponent | 0.75 | - | base.yaml |
| Fixed OPEX Ratio | 5% | %/year of CAPEX | base.yaml |
| Equipment Ratio | 3% | % of CAPEX | base.yaml |

### Shuttle CAPEX Formula

```
CAPEX = 61.5M x (Shuttle_Size / 40,000)^0.75
```

**Example Calculations:**

| Shuttle Size (m3) | Calculation | CAPEX (USD) |
|-------------------|-------------|-------------|
| 500 | 61.5M x (500/40000)^0.75 | $2,299,077 |
| 1,000 | 61.5M x (1000/40000)^0.75 | $3,866,632 |
| 5,000 | 61.5M x (5000/40000)^0.75 | $12,928,812 |
| 10,000 | 61.5M x (10000/40000)^0.75 | $21,743,552 |
| 50,000 | 61.5M x (50000/40000)^0.75 | $72,715,556 |

### Pump Costs

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Pump Delta Pressure | 4.0 | bar | base.yaml |
| Pump Efficiency | 0.7 | - | base.yaml |
| Pump Power Cost | 2,000 | USD/kW | base.yaml |

### Pump Power Formula

```
Power (kW) = (Delta_Pressure_Pa x Flow_Rate_m3s) / Efficiency
           = (4 x 10^5 Pa x Q/3600) / 0.7
```

**For 1000 m3/h pump:**
```
Power = (4 x 10^5 x 1000/3600) / 0.7
      = (4 x 10^5 x 0.2778) / 0.7
      = 158.73 kW

CAPEX = 158.73 x 2000 = $317,460
```

### Tank Storage Costs (Case 1 only)

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Tank Size | 35,000 | tons | case_1.yaml |
| Cost per kg | 1.215 | USD/kg | base.yaml |
| Fixed OPEX Ratio | 3% | %/year of CAPEX | base.yaml |
| Cooling Energy | 0.0378 | kWh/kg | base.yaml |

**Tank CAPEX:**
```
CAPEX = 35,000 x 1000 kg x 1.215 USD/kg = $42,525,000
```

### Bunkering System Costs

| Parameter | Value | Unit | Source |
|-----------|-------|------|--------|
| Fixed OPEX Ratio | 5% | %/year of CAPEX | base.yaml |
| Equipment Ratio | 3% | % of CAPEX | base.yaml |

Bunkering CAPEX = Shuttle Equipment Cost + Pump CAPEX
               = (Shuttle CAPEX x 3%) + Pump CAPEX

---

## 2.7 Case-Specific Parameters

| Parameter | Case 1 | Case 2-1 | Case 2-2 | Unit |
|-----------|--------|----------|----------|------|
| Route | Busan internal | Yeosu->Busan | Ulsan->Busan | - |
| Distance | - | 86 | 59 | nm |
| Ship Speed | - | 15 | 15 | knots |
| Travel Time (one-way) | 1.0 | 5.73 | 3.93 | hours |
| Has Busan Storage | Yes | No | No | - |
| Storage Tank Enabled | Yes | No | No | - |
| Bunker Volume/Call | 5,000 | 5,000 | 5,000 | m3 |

### Travel Time Calculation (Case 2)

```
Travel Time = Distance / Speed

Case 2-1: 86 nm / 15 knots = 5.733 hours
Case 2-2: 59 nm / 15 knots = 3.933 hours
```

---

## 2.8 MCR Map (kW by Shuttle Size)

v4.1 Update: Based on MAN Energy Solutions official data

| Size (m3) | Case 1 MCR | Case 2 MCR | Source |
|-----------|------------|------------|--------|
| 500 | 380 | - | MAN extrapolation |
| 1,000 | 620 | - | MAN extrapolation |
| 1,500 | 820 | - | MAN extrapolation |
| 2,000 | 1,000 | - | MAN extrapolation |
| 2,500 | 1,160 | 1,160 | MAN extrapolation |
| 3,000 | 1,310 | - | MAN extrapolation |
| 3,500 | 1,450 | - | MAN extrapolation |
| 4,000 | 1,580 | - | MAN extrapolation |
| 4,500 | 1,700 | - | MAN extrapolation |
| 5,000 | 1,810 | 1,810 | MAN interpolation |
| 7,500 | 2,180 | - | MAN interpolation |
| 10,000 | 2,420 | 2,420 | MAN interpolation |
| 15,000 | - | 3,080 | MAN interpolation |
| 20,000 | - | 3,660 | MAN interpolation |
| 25,000 | - | 4,090 | MAN interpolation |
| 30,000 | - | 4,510 | MAN interpolation |
| 35,000 | - | 5,030 | MAN interpolation |
| 40,000 | - | 5,620 | MAN interpolation |
| 45,000 | - | 6,070 | MAN interpolation |
| 50,000 | - | 6,510 | MAN approximation |

---

## 2.9 SFOC Map (g/kWh by DWT)

v4.1 Update: DWT-based engine type matching for ammonia fuel

| DWT Range | Engine Type | SFOC (g/kWh) | Diesel Equivalent |
|-----------|-------------|--------------|-------------------|
| < 3,000 | 4-stroke high-speed | 505 | 220 |
| 3,000-8,000 | 4-stroke medium | 436 | 190 |
| 8,000-15,000 | 4-stroke/small 2-stroke | 413 | 180 |
| 15,000-30,000 | 2-stroke | 390 | 170 |
| > 30,000 | 2-stroke large | 379 | 165 |

### DWT Calculation

```
DWT = Cargo_m3 x Density / Cargo_Fraction
    = Shuttle_Size x 0.680 / 0.80
    = Shuttle_Size x 0.85
```

### SFOC by Shuttle Size

| Shuttle Size (m3) | DWT (ton) | SFOC (g/kWh) |
|-------------------|-----------|--------------|
| 500 | 425 | 505 |
| 1,000 | 850 | 505 |
| 2,500 | 2,125 | 505 |
| 3,500 | 2,975 | 505 |
| 4,000 | 3,400 | 436 |
| 5,000 | 4,250 | 436 |
| 10,000 | 8,500 | 413 |
| 15,000 | 12,750 | 413 |
| 20,000 | 17,000 | 390 |
| 30,000 | 25,500 | 390 |
| 40,000 | 34,000 | 379 |
| 50,000 | 42,500 | 379 |

---

## 2.10 Available Shuttle Sizes

| Case | Available Sizes (m3) |
|------|---------------------|
| Case 1 | 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 7500, 10000 |
| Case 2-1 | 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000 |
| Case 2-2 | 2500, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000 |

---

## 2.11 Pump Flow Rates

| Configuration | Flow Rates (m3/h) |
|---------------|------------------|
| Main Optimization | 1000 |
| Sensitivity Analysis | 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000 |
