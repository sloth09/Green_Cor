# 7. Conclusion and Verification Checklist

## 7.1 Overall Verification Result

**All 72 hand-calculated values match CSV output across all 3 cases.**

| Case | Items | PASS | FAIL | Result |
|------|-------|------|------|--------|
| Case 1: Busan Port | 24 | 24 | 0 | ALL PASS |
| Case 2-1: Yeosu | 24 | 24 | 0 | ALL PASS |
| Case 2-2: Ulsan | 24 | 24 | 0 | ALL PASS |
| **Total** | **72** | **72** | **0** | **ALL PASS** |

## 7.2 Master Verification Checklist

### Economic Parameters

| # | Item | Formula | Expected | Case 1 | Case 2-1 | Case 2-2 | Status |
|---|------|---------|----------|--------|----------|----------|--------|
| 1 | Annuity Factor | [1-(1.07)^(-21)]/0.07 | 10.8355 | 10.8355 | 10.8355 | 10.8355 | PASS |

### Cycle Time (Optimal Shuttle)

| # | Item | Case 1 (2500) | Case 2-1 (5000) | Case 2-2 (5000) | Status |
|---|------|--------------|-----------------|-----------------|--------|
| 2 | Shore Loading | 7.5714 h | 11.1429 h | 11.1429 h | PASS |
| 3 | Basic Cycle | 8.5000 h | 23.4600 h | 19.8600 h | PASS |
| 4 | Total Cycle | 16.0714 h | 34.6029 h | 31.0029 h | PASS |
| 5 | Annual Cycles Max | 497.78 | 231.19 | 258.04 | PASS |
| 6 | Trips per Call | 2.0 | 1.0 | 1.0 | PASS |
| 7 | Call Duration | 32.1429 h | 34.6029 h | 31.0029 h | PASS |

### CAPEX (Per Unit)

| # | Item | Case 1 (2500) | Case 2 (5000) | Status |
|---|------|--------------|---------------|--------|
| 8 | Shuttle CAPEX | $7,687,500 | $12,928,776 | PASS |
| 9 | Pump Power | 158.73 kW | 158.73 kW | PASS |
| 10 | Pump CAPEX | $317,460 | $317,460 | PASS |
| 11 | Bunkering CAPEX | $548,085 | $705,323 | PASS |

### OPEX (Per Unit/Year)

| # | Item | Case 1 (2500) | Case 2 (5000) | Status |
|---|------|--------------|---------------|--------|
| 12 | Shuttle fOPEX | $384,375/yr | $646,439/yr | PASS |
| 13 | Bunkering fOPEX | $27,404/yr | $35,266/yr | PASS |

### Variable OPEX (Per Cycle/Call)

| # | Item | Case 1 | Case 2-1 | Case 2-2 | Status |
|---|------|--------|----------|----------|--------|
| 14 | Shuttle fuel/cycle | $396.93 | $5,786.00 | $3,968.50 | PASS |
| 15 | Pump fuel/call | $240.48 | $207.67 | $207.67 | PASS |

### NPC Components (21-year totals, USDm)

| # | Item | Case 1 | Case 2-1 | Case 2-2 | Status |
|---|------|--------|----------|----------|--------|
| 16 | NPC Ann. Shuttle CAPEX | 205.04 | 368.69 | 332.90 | PASS |
| 17 | NPC Ann. Bunkering CAPEX | 14.62 | 20.11 | 18.16 | PASS |
| 18 | NPC Shuttle fOPEX | 111.08 | 199.75 | 180.36 | PASS |
| 19 | NPC Bunkering fOPEX | 7.92 | 10.90 | 9.84 | PASS |
| 20 | NPC Shuttle vOPEX | 55.01 | 400.97 | 275.01 | PASS |
| 21 | NPC Bunkering vOPEX | 16.67 | 14.39 | 14.39 | PASS |

### Final Results

| # | Item | Case 1 | Case 2-1 | Case 2-2 | Status |
|---|------|--------|----------|----------|--------|
| 22 | NPC Total | $410.34M | $1,014.81M | $830.65M | PASS |
| 23 | Total Supply | 235,620,000 t | 235,620,000 t | 235,620,000 t | PASS |
| 24 | LCOAmmonia | $1.74/ton | $4.31/ton | $3.53/ton | PASS |

## 7.3 Parameter Change Verification (v5.1 -> v6.0)

The following checks confirm that the parameter updates were correctly propagated:

| Check | Method | Result |
|-------|--------|--------|
| Shore pump = 700 m3/h | Shore_Loading = Size/700 + 4.0; verified for all sizes | PASS |
| Setup = 2.0h per endpoint | Setup_Inbound = 2.0, Setup_Outbound = 2.0 in all CSVs | PASS |
| Fixed time = 4.0h | Shore_Loading - (Size/700) = 4.0 for all sizes | PASS |
| No code multiplier | Config value 2.0 matches CSV directly (no 2x) | PASS |
| 500 m3 excluded | Call_Duration = 10 x 11.21 = 112.1h > 80h max | PASS |

## 7.4 Key Findings (v6.0)

### 7.4.1 Optimal Configurations

| Case | Optimal | NPC | LCO | Change from v5.1 |
|------|---------|-----|-----|-------------------|
| Case 1 | 2,500 m3 | $410.34M | $1.74/ton | +41.1% |
| Case 2-1 | 5,000 m3 | $1,014.81M | $4.31/ton | +15.3% |
| Case 2-2 | 5,000 m3 | $830.65M | $3.53/ton | +18.6% |

### 7.4.2 Parameter Impact Assessment

1. **Shore pump rate reduction (1500 -> 700 m3/h)**: Largest impact on shore loading time.
   For 5000 m3 shuttle: loading time increased from 3.33h to 7.14h (+3.81h).

2. **Setup time increase (1.0h -> 2.0h per endpoint)**: Adds 2.0h per cycle
   (both inbound and outbound increased by 1.0h each).

3. **Fixed loading time increase (2.0h -> 4.0h)**: Adds 2.0h per cycle for
   shore terminal operations.

4. **Combined effect**: +5.90h to +8.47h per cycle depending on shuttle size,
   with proportionally greater impact on shorter-cycle cases (Case 1).

### 7.4.3 Notable Observations

1. **Optimal shuttles unchanged**: Despite significant parameter changes, the same shuttle
   sizes remain optimal for all cases. This indicates robust optima.

2. **500 m3 shuttle eliminated**: The smallest shuttle size in Case 1 now exceeds the
   80-hour call duration constraint and is excluded from feasible solutions.

3. **Variable OPEX dominance in Case 2**: For Case 2-1 (Yeosu), variable OPEX now
   accounts for 41% of total NPC, driven by long-distance fuel consumption.

4. **Shore loading as bottleneck**: With 700 m3/h pump rate, shore loading now represents
   35-47% of total cycle time across all cases, making it the single largest time component.

## 7.5 Recommendations

1. **Shore pump rate sensitivity**: The 700 m3/h rate significantly impacts all cases.
   A sensitivity analysis on this parameter (already included in the pump sensitivity study)
   should inform infrastructure investment decisions.

2. **Setup time reduction**: At 2.0h per endpoint, setup operations represent ~25% of
   Case 1 cycle time. Operational improvements (quick-connect fittings, automated purging)
   could yield meaningful cost reductions.

3. **Case 1 remains strongly preferred**: The 51-60% cost advantage of onshore storage
   (Case 1) over long-distance supply (Case 2) persists and even grows with the updated
   parameters.

---

## 7.6 Report Metadata

| Field | Value |
|-------|-------|
| Report Version | v6.0 |
| Generated | 2026-02-11 |
| Model Version | v2.3.3 -> v3.0.0 |
| Data Source | `results/deterministic/MILP_scenario_summary_case_*.csv` |
| Config Files | `config/base.yaml`, `config/case_*.yaml` |
| Source Code | `src/optimizer.py`, `src/shuttle_round_trip_calculator.py`, `src/cost_calculator.py` |
| Verification Items | 72 (24 per case x 3 cases) |
| Pass Rate | 72/72 (100%) |

---

*Verification report completed. All hand calculations match optimizer output.*
