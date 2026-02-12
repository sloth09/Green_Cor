# 1. Executive Summary

## 1.1 Purpose

This report verifies the Green Corridor MILP optimization model outputs by performing
independent hand calculations and comparing them against the CSV results produced by the
optimizer. The verification covers all three cases across 13 verification categories.

## 1.2 Key Results (v6.0)

| Case | Optimal Shuttle | Pump | NPC (20yr) | LCO ($/ton) | Annual Cycles |
|------|----------------|------|-----------|-------------|---------------|
| **Case 1: Busan** | 2,500 m3 | 1,000 m3/h | **$410.34M** | **$1.74** | 497.78 |
| **Case 2-1: Yeosu** | 5,000 m3 | 1,000 m3/h | **$1,014.81M** | **$4.31** | 231.19 |
| **Case 2-2: Ulsan** | 5,000 m3 | 1,000 m3/h | **$830.65M** | **$3.53** | 258.04 |

## 1.3 Parameter Changes from v5.1

| Parameter | v5.1 | v6.0 | Effect |
|-----------|------|------|--------|
| Shore Pump Rate | 1,500 m3/h | **700 m3/h** | Shore loading pumping time x2.14 |
| Setup Time (per endpoint) | 1.0h | **2.0h** | Setup phase doubled |
| Shore Loading Fixed Time | 2.0h | **4.0h** | Fixed overhead doubled |
| Pump Sensitivity Range | 400-2000 m3/h | **100-1500 m3/h** | 15 points, finer resolution |

### Cycle Time Impact (Optimal Shuttles)

| Case | v5.1 Cycle | v6.0 Cycle | Increase | Cause Breakdown |
|------|-----------|-----------|----------|-----------------|
| Case 1 (2500 m3) | 10.17h | **16.07h** | +5.90h | Shore pump: +1.90h, Setup: +2.0h, Fixed: +2.0h |
| Case 2-1 (5000 m3) | 26.13h | **34.60h** | +8.47h | Shore pump: +5.00h, Setup: +2.0h, Fixed: +2.0h (Note 1) |
| Case 2-2 (5000 m3) | 22.53h | **31.00h** | +8.47h | Shore pump: +5.00h, Setup: +2.0h, Fixed: +2.0h (Note 1) |

Note 1: For Case 2, the "setup" increase only affects the shore-side endpoint setup. The vessel-side
setup per vessel also increases, but the optimal shuttle at 5000 m3 serves only 1 vessel per trip,
so the per-vessel setup increase is the same 2.0h total (inbound + outbound).

### NPC Impact

| Case | v5.1 NPC | v6.0 NPC | Increase |
|------|---------|---------|----------|
| Case 1 | $290.81M | **$410.34M** | +41.1% |
| Case 2-1 | $879.88M | **$1,014.81M** | +15.3% |
| Case 2-2 | $700.68M | **$830.65M** | +18.6% |

Case 1 is most impacted because its shorter base cycle means the added time has proportionally
greater effect. Case 2 Yeosu has the smallest relative increase because its long travel time
(5.73h each way) dilutes the impact of the parameter changes.

## 1.4 Notable Change: 500 m3 Shuttle Eliminated

With the new parameters, the 500 m3 shuttle in Case 1 exceeds the maximum call duration
constraint (80 hours):

```
v5.1: Call_Duration = 10 x 6.83h = 68.3h < 80h  -> Feasible
v6.0: Call_Duration = 10 x 11.21h = 112.1h > 80h -> INFEASIBLE
```

This is expected: longer cycle times combined with 10 trips per call push the total beyond
the operational limit. The optimizer correctly excludes this configuration.

## 1.5 Verification Verdict

**All 72 hand-calculated values match CSV output across all 3 cases.**

| Case | Items Verified | Result |
|------|---------------|--------|
| Case 1: Busan | 24/24 | ALL PASS |
| Case 2-1: Yeosu | 24/24 | ALL PASS |
| Case 2-2: Ulsan | 24/24 | ALL PASS |
| **Total** | **72/72** | **ALL PASS** |
