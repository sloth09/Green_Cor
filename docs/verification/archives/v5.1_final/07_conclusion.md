# Chapter 7: Conclusion & Verification Checklist

## 7.1 Verification Summary

This report has verified the MILP optimization results for the Green Corridor ammonia bunkering infrastructure project. All key calculations have been manually verified against the CSV output files.

**v5.1 Update**: All results reflect Power Law MCR values (MCR = 17.17 x DWT^0.566) with corrected shore loading fixed time (+2h).

---

## 7.2 Master Verification Checklist

### Economic Parameters

| # | Item | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 1 | Discount Rate | 0.0 | 0.0 | PASS |
| 2 | Annualization Interest Rate | 7% | 7% | PASS |
| 3 | Annuity Factor | 10.8355 | 10.8355 | PASS |
| 4 | Fuel Price | $600/ton | $600/ton | PASS |
| 5 | Total Years | 21 | 21 | PASS |

### Operational Parameters

| # | Item | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 6 | Max Annual Hours | 8000 hr | 8000 hr | PASS |
| 7 | Setup Time | 0.5 hr | 0.5 hr | PASS |
| 8 | Shore Pump Rate | 1500 m3/h | 1500 m3/h | PASS |
| 9 | Bunker Volume | 5000 m3 | 5000 m3 | PASS |
| 10 | Pump Flow Rate | 1000 m3/h | 1000 m3/h | PASS |
| 11 | Shore Loading Fixed Time | 2.0 hr | 2.0 hr | PASS |

### Case-Specific Parameters

| # | Item | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 12 | Case 1 Travel Time | 1.0 hr | 1.0 hr | PASS |
| 13 | Case 2-1 Distance | 86 nm | 86 nm | PASS |
| 14 | Case 2-1 Travel Time | 5.73 hr | 5.73 hr | PASS |
| 15 | Case 2-2 Distance | 59 nm | 59 nm | PASS |
| 16 | Case 2-2 Travel Time | 3.93 hr | 3.93 hr | PASS |

### Cycle Time Verification (v5.1)

| # | Case | Shuttle | Expected | Actual | Status |
|---|------|---------|----------|--------|--------|
| 17 | Case 1 | 2500 m3 | 10.17 hr | 10.17 hr | PASS |
| 18 | Case 2-1 | 10000 m3 | 38.13 hr | 38.13 hr | PASS |
| 19 | Case 2-2 | 5000 m3 | 23.19 hr | 23.19 hr | PASS |

### CAPEX Verification

| # | Item | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 20 | Shuttle CAPEX (2500 m3) | $7.69M | $7.69M | PASS |
| 21 | Shuttle CAPEX (5000 m3) | $12.93M | $12.93M | PASS |
| 22 | Shuttle CAPEX (10000 m3) | $21.74M | $21.74M | PASS |
| 23 | Pump CAPEX (1000 m3/h) | $0.32M | $0.32M | PASS |

### OPEX Verification

| # | Item | Expected | Actual | Status |
|---|------|----------|--------|--------|
| 24 | Case 1 Shuttle fOPEX | 5% of CAPEX | 5% of CAPEX | PASS |
| 25 | Case 1 Shuttle vOPEX | MCR-based | CSV matches | PASS |
| 26 | Case 2-1 Shuttle vOPEX | MCR-based | CSV matches | PASS |
| 27 | Case 2-2 Shuttle vOPEX | MCR-based | CSV matches | PASS |

### NPC Verification (v5.1)

| # | Case | Optimal | NPC | LCO | Status |
|---|------|---------|-----|-----|--------|
| 28 | Case 1 | 2500 m3 | $290.81M | $1.23/ton | PASS |
| 29 | Case 2-1 | 10000 m3 | $879.88M | $3.73/ton | PASS |
| 30 | Case 2-2 | 5000 m3 | $700.68M | $2.97/ton | PASS |

### MCR/SFOC Verification (v5 Power Law)

| # | Shuttle | MCR v5 (kW) | SFOC (g/kWh) | Status |
|---|---------|-------------|--------------|--------|
| 31 | 2500 m3 | 1310 | 505 | PASS |
| 32 | 5000 m3 | 1930 | 436 | PASS |
| 33 | 10000 m3 | 2990 | 413 | PASS |

---

## 7.3 Verification Results Summary

| Category | Total Items | Passed | Failed | Pass Rate |
|----------|-------------|--------|--------|-----------|
| Economic Parameters | 5 | 5 | 0 | 100% |
| Operational Parameters | 6 | 6 | 0 | 100% |
| Case-Specific Parameters | 5 | 5 | 0 | 100% |
| Cycle Time | 3 | 3 | 0 | 100% |
| CAPEX | 4 | 4 | 0 | 100% |
| OPEX | 4 | 4 | 0 | 100% |
| NPC | 3 | 3 | 0 | 100% |
| MCR/SFOC | 3 | 3 | 0 | 100% |
| **TOTAL** | **33** | **33** | **0** | **100%** |

---

## 7.4 Discrepancies and Notes

### Resolved in v5.1 Verification

1. **Case 2 Cycle Time Structure**: Fully verified with code-level analysis. The basic cycle time breakdown is:
   - Travel_Out + Port_Entry(1.0h) + VpT x (Movement(1.0h) + Setup_In(1.0h) + Pumping(5.0h) + Setup_Out(1.0h)) + Port_Exit(1.0h) + Travel_Return
   - Per-vessel operational block = 8.0 hours (movement + setup + pumping)
   - All values match CSV output exactly (0.00% difference)

2. **Bunkering vOPEX (Pump Fuel)**: Resolved - the pump uses the **shuttle's SFOC** (based on DWT range), not the default SFOC of 379 g/kWh.
   - Case 1 (2500 m3): SFOC = 505 g/kWh (DWT 2125 < 3000)
   - Case 2-1 (10000 m3): SFOC = 413 g/kWh (DWT 8500, range 8000-15000)
   - Case 2-2 (5000 m3): SFOC = 436 g/kWh (DWT 4250, range 3000-8000)
   - With correct SFOC, all bunkering vOPEX values match CSV within 0.01%

3. **Shuttle Fuel Travel Factor**:
   - Case 1: Travel_Factor = 1.0 (one-way fuel calculation for port internal movement)
   - Case 2: Travel_Factor = 2.0 (round-trip fuel for long-distance routes)
   - Verified against per-year CSV data for all three cases

### All discrepancies from previous versions have been fully resolved. No FAIL items remain.

---

## 7.5 Key Findings

### Optimal Configurations (v5.1)

| Rank | Case | Shuttle | NPC | LCOAmmonia |
|------|------|---------|-----|------------|
| 1 | Case 1 | 2,500 m3 | $290.81M | $1.23/ton |
| 2 | Case 2-2 | 5,000 m3 | $700.68M | $2.97/ton |
| 3 | Case 2-1 | 10,000 m3 | $879.88M | $3.73/ton |

### v5 to v5.1 Update Impacts

| Case | v5 Shuttle | v5.1 Shuttle | v5 NPC | v5.1 NPC | Change |
|------|------------|--------------|--------|----------|--------|
| Case 1 | 2,500 m3 | 2,500 m3 | $249.80M | $290.81M | +16.4% |
| Case 2-1 | 10,000 m3 | 10,000 m3 | $847.56M | $879.88M | +3.8% |
| Case 2-2 | 5,000 m3 | 5,000 m3 | $667.70M | $700.68M | +4.9% |

### v4 to v5 Update Impacts

| Case | v4 Shuttle | v5 Shuttle | v4 NPC | v5 NPC | Change |
|------|------------|------------|--------|--------|--------|
| Case 1 | 1,000 m3 | **2,500 m3** | $238.39M | $249.80M | +4.8% |
| Case 2-1 | 10,000 m3 | 10,000 m3 | $791.47M | $847.56M | +7.1% |
| Case 2-2 | 5,000 m3 | 5,000 m3 | $650.60M | $667.70M | +2.6% |

### Key Changes in v5.1

1. **Shore Loading Fixed Time**: Added +2h fixed shore loading time to all cycle time calculations
2. **Case 1 Most Affected**: +16.4% NPC increase because short base cycle is more sensitive to the fixed 2h addition
3. **Case 2 Less Affected**: +3.8% to +4.9% NPC increase because longer base cycles dilute the fixed 2h addition
4. **Optimal Sizes Unchanged**: All three cases retain the same optimal shuttle sizes as v5

### Key Changes in v5

1. **MCR Update**: Power Law formula `MCR = 17.17 x DWT^0.566` applied to all shuttle sizes
2. **Small Shuttle Impact**: Small shuttles (500-2000 m3) experienced largest MCR corrections (+20-37%)
3. **Case 1 Optimal Shift**: Changed from 1000 m3 to 2500 m3 due to corrected MCR values
4. **Case 2 Unchanged**: Optimal shuttle sizes remain at 10000 m3 (Yeosu) and 5000 m3 (Ulsan)

---

## 7.6 Final Recommendations

### Primary: Case 1 (Busan Storage)

**Recommended Configuration:**
- Shuttle Size: 2,500 m3
- Pump Rate: 1,000 m3/h
- 20-year NPC: $290.81M
- LCOAmmonia: $1.23/ton

**Rationale:**
- Lowest cost option by a significant margin (2.4-3.0x cheaper than Case 2)
- Simple operational model with short cycle times
- Requires investment in local storage infrastructure
- v5 MCR update shifted optimal from 1000 m3 to 2500 m3 (unchanged in v5.1)

### Alternative: Case 2-2 (Ulsan Direct)

**Recommended Configuration:**
- Shuttle Size: 5,000 m3
- Pump Rate: 1,000 m3/h
- 20-year NPC: $700.68M
- LCOAmmonia: $2.97/ton

**Rationale:**
- No local storage required
- Shorter distance than Yeosu route
- Suitable if Busan port storage is not feasible

---

## 7.7 Report Sign-off

### Verification Completed

- [x] All input parameters verified
- [x] All cycle time calculations verified (including shore loading fixed time)
- [x] All CAPEX calculations verified
- [x] All OPEX calculations verified
- [x] All NPC totals verified
- [x] All LCOAmmonia values verified
- [x] MCR/SFOC updates (v5 Power Law) verified
- [x] Shore loading fixed time (+2h) verified (v5.1)
- [x] Cross-case comparison completed
- [x] Variable OPEX pattern analysis completed

### Verification Report Status

**Status**: COMPLETE

**Version**: v5.1 (Shore Loading Fixed Time Correction)

**Date**: 2026-02-02

---

## 7.8 Appendix: Formula Reference

### Cycle Time (Case 1)
```
Shore_Loading = (Shuttle_Size / 1500) + 2.0
Basic_Cycle = Travel_Out(1.0) + Setup_In(1.0) + Pumping(Shuttle/1000) + Setup_Out(1.0) + Travel_Return(1.0)
Cycle = Shore_Loading + Basic_Cycle
```

### Cycle Time (Case 2)
```
Shore_Loading = (Shuttle_Size / 1500) + 2.0
VpT = floor(Shuttle_Size / 5000)
Basic_Cycle = Travel_Out + Port_Entry(1.0) + VpT x (Movement(1.0) + Setup_In(1.0) + Pumping(5.0) + Setup_Out(1.0)) + Port_Exit(1.0) + Travel_Return
Cycle = Shore_Loading + Basic_Cycle
```

### Shuttle CAPEX
```
CAPEX = 61.5M x (Shuttle_Size / 40000)^0.75
```

### Annuity Factor
```
AF = [1 - (1 + r)^(-n)] / r
   = [1 - (1.07)^(-21)] / 0.07
   = 10.8355
```

### Annualized CAPEX
```
Annualized = Actual_CAPEX / Annuity_Factor
```

### Fuel Cost per Cycle
```
Fuel_cost = MCR x SFOC x Travel_Time x Travel_Factor / 1e6 x Fuel_Price
```

### MCR Power Law (v5)
```
MCR = 17.17 x DWT^0.566
DWT = Cargo_m3 x 0.680 / 0.80
```

### LCOAmmonia
```
LCO = NPC_Total / Total_Supply_20yr_ton
```
