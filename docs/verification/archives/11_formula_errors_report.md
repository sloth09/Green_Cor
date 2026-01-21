# Chapter 11: Formula Errors and Inconsistencies Report

## 11.1 Overview

This document identifies formula errors and inconsistencies found in the existing verification documents. Each error is categorized by severity and location.

| Severity | Description |
|----------|-------------|
| **HIGH** | Calculation produces incorrect result |
| **MEDIUM** | Intermediate value differs from expected |
| **LOW** | Rounding or minor discrepancy |
| **INCONSISTENCY** | Same calculation produces different results in different documents |

---

## 11.2 Error Summary

| Document | Error Count | Severity |
|----------|-------------|----------|
| 02_parameters.md | 6 | HIGH, MEDIUM |
| 03_case1_busan.md | 2 | MEDIUM |
| 04_case2_yeosu.md | 1 | MEDIUM |
| 05_case2_ulsan.md | 2 | HIGH, INCONSISTENCY |

---

## 11.3 Errors in 02_parameters.md

### 11.3.1 Shuttle CAPEX Table (Lines 116-124)

**Severity: HIGH**

The example CAPEX calculations in section 2.7 show values that differ from the correct formula result.

**Formula:**
```
Shuttle_CAPEX = 61,500,000 × (Shuttle_Size / 40,000)^0.75
```

| Shuttle Size | Document Value | Correct Value | Difference | Error % |
|-------------|---------------|---------------|------------|---------|
| 500 m3 | $2,450,715 | $2,297,640 | +$153,075 | +6.7% |
| 1,000 m3 | $4,121,543 | $3,872,655 | +$248,888 | +6.4% |
| 2,500 m3 | $7,761,316 | $7,687,500 | +$73,816 | +1.0% |
| 5,000 m3 | $13,051,896 | $12,927,300 | +$124,596 | +1.0% |
| 10,000 m3 | $21,951,652 | $21,746,400 | +$205,252 | +0.9% |
| 15,000 m3 | $29,631,149 | $29,624,550 | +$6,599 | +0.02% |

**Verification Calculation (500 m3):**
```
(500 / 40000)^0.75 = (0.0125)^0.75
                   = exp(0.75 × ln(0.0125))
                   = exp(0.75 × (-4.382))
                   = exp(-3.287)
                   = 0.03736

CAPEX = 61,500,000 × 0.03736 = $2,297,640
```

**Verification Calculation (2,500 m3):**
```
(2500 / 40000)^0.75 = (0.0625)^0.75
                    = (1/16)^(3/4)
                    = 1/8
                    = 0.125

CAPEX = 61,500,000 × 0.125 = $7,687,500
```

**Possible Cause:**
- The document values appear to use a different scaling factor or intermediate calculation
- May be using CSV output values that differ from formula (rounding in code)

---

### 11.3.2 Annuity Factor Intermediate Calculation (Lines 197-200)

**Severity: LOW**

**Document shows:**
```
AF = [1 - (1.07)^(-21)] / 0.07
   = [1 - 0.2415] / 0.07
   = 0.7585 / 0.07
   = 10.8355
```

**Verification:**
```
(1.07)^(-21) = 1 / (1.07)^21
             = 1 / 4.1406
             = 0.2415 [CORRECT]

AF = (1 - 0.2415) / 0.07
   = 0.7585 / 0.07
   = 10.8357 (rounded to 10.8355) [CORRECT with rounding]
```

**Status: PASS** - The calculation is correct with minor rounding.

---

## 11.4 Errors in 03_case1_busan.md

### 11.4.1 Intermediate Scaling Factor (2,500 m3) - Lines 108-110

**Severity: MEDIUM**

**Document shows:**
```
CAPEX = 61,500,000 × (2500 / 40000)^0.75
      = 61,500,000 × (0.0625)^0.75
      = 61,500,000 × 0.1263        <-- ERROR
      = $7,761,316
```

**Correct calculation:**
```
(0.0625)^0.75 = 0.125              <-- CORRECT
61,500,000 × 0.125 = $7,687,500    <-- CORRECT
```

**Error:** The intermediate value `0.1263` should be `0.125`

---

### 11.4.2 Intermediate Scaling Factor (5,000 m3) - Lines 115-118

**Severity: MEDIUM**

**Document shows:**
```
CAPEX = 61,500,000 × (5000 / 40000)^0.75
      = 61,500,000 × (0.125)^0.75
      = 61,500,000 × 0.2122        <-- ERROR
      = $13,051,896
```

**Correct calculation:**
```
(0.125)^0.75 = (1/8)^0.75
             = 1 / 8^0.75
             = 1 / 4.757
             = 0.2102              <-- CORRECT

61,500,000 × 0.2102 = $12,927,300  <-- CORRECT
```

**Error:** The intermediate value `0.2122` should be `0.2102`

---

## 11.5 Errors in 04_case2_yeosu.md

### 11.5.1 5,000 m3 CAPEX Calculation (Lines 169-174)

**Severity: MEDIUM**

**Document shows:**
```
CAPEX = 61,500,000 × (5000 / 40000)^0.75
      = 61,500,000 × (0.125)^0.75
      = 61,500,000 × 0.2102
      = $12,927,300
```

**Status: CORRECT** - This matches the expected calculation.

However, there is an inconsistency with 02_parameters.md which shows $13,051,896 for the same shuttle size.

---

## 11.6 Errors in 05_case2_ulsan.md

### 11.6.1 10,000 m3 Shuttle CAPEX (Line 148)

**Severity: INCONSISTENCY (HIGH)**

| Document | 10,000 m3 CAPEX |
|----------|-----------------|
| 02_parameters.md | $21,951,652 |
| 04_case2_yeosu.md | $21,746,430 |
| **05_case2_ulsan.md** | **$21,951,652** |
| Correct Value | $21,746,400 |

**Problem:** The CAPEX for the same shuttle size differs between documents.

- 04_case2_yeosu.md: $21,746,430 (close to correct)
- 05_case2_ulsan.md: $21,951,652 (differs by $205,222)

**Expected:** All documents should show the same CAPEX value for the same shuttle size, as CAPEX only depends on shuttle size, not on the route.

---

### 11.6.2 2,500 m3 Shuttle Annualized CAPEX (Line 146)

**Severity: LOW**

**Document shows:** $716,345

**Calculation:**
```
CAPEX = $7,687,500 (correct) or $7,761,316 (from doc)
Annualized = CAPEX / 10.8355

If CAPEX = $7,761,316:
  $7,761,316 / 10.8355 = $716,534

If CAPEX = $7,687,500 (correct):
  $7,687,500 / 10.8355 = $709,715
```

The document value $716,345 doesn't match either calculation exactly.

---

## 11.7 Cross-Document Inconsistencies

### 11.7.1 Shuttle CAPEX Values

| Shuttle Size | 02_parameters.md | 04_case2_yeosu.md | 05_case2_ulsan.md | Correct |
|-------------|-----------------|-------------------|-------------------|---------|
| 5,000 m3 | $13,051,896 | $12,927,300 | - | $12,927,300 |
| 10,000 m3 | $21,951,652 | $21,746,430 | $21,951,652 | $21,746,400 |

**Problem:** Same shuttle size shows different CAPEX values in different documents.

### 11.7.2 Consistent vs Inconsistent Documents

| Document | Uses Consistent Values |
|----------|----------------------|
| 02_parameters.md | Uses inflated values |
| 03_case1_busan.md | Follows 02_parameters.md |
| 04_case2_yeosu.md | **Uses correct values** |
| 05_case2_ulsan.md | Mixes both |

---

## 11.8 Root Cause Analysis

### Possible Causes

1. **Different calculation methods**: Some values may come from code output (with rounding) while others are manual calculations

2. **Intermediate rounding**: Rounding at intermediate steps can cause propagation errors

3. **Copy-paste errors**: Values may have been copied from different sources

4. **Parameter drift**: Different versions of the model may have used slightly different parameters

### Recommended Fix

1. **Standardize calculations**: Use consistent precision (e.g., 6 decimal places for intermediate values)

2. **Reference single source**: All documents should reference the same CAPEX calculation method

3. **Update 02_parameters.md**: Correct the CAPEX table to use formula-derived values

4. **Update 05_case2_ulsan.md**: Use consistent 10,000 m3 CAPEX value of $21,746,400

---

## 11.9 Verification Checklist

### Formula Correctness Check

| Formula | Expected | Documents | Status |
|---------|----------|-----------|--------|
| Shuttle CAPEX = 61.5M × (S/40000)^0.75 | See table | Various | INCONSISTENT |
| Pump Power = (Q×dP×100)/(3600×eta) | 158.73 kW | All | PASS |
| Annuity Factor = [1-(1+r)^-n]/r | 10.8355 | All | PASS |
| Cycle Duration formulas | Various | All | PASS |

### Numerical Accuracy Check

| Calculation Type | Status |
|-----------------|--------|
| Pump Power | PASS |
| Cycle Time (Case 1) | PASS |
| Cycle Time (Case 2-1) | PASS |
| Cycle Time (Case 2-2) | PASS |
| Shuttle CAPEX | FAIL (inconsistent) |
| Annuity Factor | PASS |

---

## 11.10 Recommended Corrections

### 11.10.1 Update 02_parameters.md Line 116-124

Replace the CAPEX table with correct values:

```markdown
| Shuttle Size (m3) | CAPEX (USD) |
|-------------------|-------------|
| 500 | $2,297,640 |
| 1,000 | $3,872,655 |
| 2,500 | $7,687,500 |
| 5,000 | $12,927,300 |
| 10,000 | $21,746,400 |
| 15,000 | $29,624,550 |
```

### 11.10.2 Update 03_case1_busan.md Lines 108-110

Replace:
```
= 61,500,000 × 0.1263
```

With:
```
= 61,500,000 × 0.125
```

### 11.10.3 Update 03_case1_busan.md Lines 116-118

Replace:
```
= 61,500,000 × 0.2122
= $13,051,896
```

With:
```
= 61,500,000 × 0.2102
= $12,927,300
```

### 11.10.4 Update 05_case2_ulsan.md Line 148

Replace:
```
| 10,000 | $21,951,652 | $2,026,087 |
```

With:
```
| 10,000 | $21,746,400 | $2,007,350 |
```

---

## 11.11 Summary

| Error Type | Count | Documents Affected |
|------------|-------|-------------------|
| Incorrect CAPEX values | 6 | 02_parameters, 05_case2_ulsan |
| Incorrect intermediate values | 2 | 03_case1_busan |
| Cross-document inconsistencies | 2 | All |
| **Total Errors** | **10** | - |

**Severity Distribution:**
- HIGH: 3
- MEDIUM: 4
- LOW: 1
- INCONSISTENCY: 2
