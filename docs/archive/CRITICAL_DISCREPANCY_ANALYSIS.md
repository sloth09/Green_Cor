# CRITICAL DISCREPANCY: Annual_Simulation vs MLIP Optimization

## Problem Statement

**Annual Simulation (Year 2030)**:
- 2500m³ + 2000m³/h: **$62.37M** First Year Cost
- 5000m³ + 2000m³/h: **$58.89M** First Year Cost
- **5000m³ is $3.48M cheaper in 2030**

**MLIP Optimization (20-Year NPC)**:
- 2500m³ + 2000m³/h: **$176.74M** (OPTIMAL)
- 5000m³ + 2000m³/h: **$196.18M** 
- **2500m³ is $19.44M cheaper over 20 years**

This is a **MAJOR CONTRADICTION** that needs to be resolved.

## Root Cause Analysis

### Why Annual_Simulation Shows 5000m³ Cheaper:

**Year 2030 Only (50 vessels, 3M m³ demand)**:
```
2500m³ shuttle:
- CAPEX: $59.6M (buy 2 shuttles)
- OPEX/yr: $2.7M
- Required: 2 shuttles (1200 trips needed, 8300h ÷ 6.92h = 1157 capacity per shuttle)
- Total: $62.4M

5000m³ shuttle:
- CAPEX: $56.5M (buy 1 shuttle)
- OPEX/yr: $2.4M
- Required: 1 shuttle (600 trips needed, 8000h ÷ 13.33h = 600 capacity per shuttle)
- Total: $58.9M
```

**Conclusion**: In 2030, smaller fleet needs fewer 5000m³ shuttles.

### Why MLIP Shows 2500m³ Optimal (Over 20 Years):

**Full 20-Year Timeline (50→500 vessels, demand grows 10x)**:

The tank sizing constraint: `N[t] × shuttle_size × safety_factor ≤ Z[t] × tank_volume`
- β = 2.0 (safety factor)
- tank_volume = 35,000 tons
- tank_cost = $42.525M per tank

**2500m³ scenario**:
```
2030: 2 shuttles → need 2×2500×2.0 = 10,000 tons → 1 tank (but MLIP shows 2)
2033: 3 shuttles → need 3×2500×2.0 = 15,000 tons → 1 tank (but MLIP shows 3)
2035: 4 shuttles → need 4×2500×2.0 = 20,000 tons → 1 tank (but MLIP shows 4)
...
2050: 8+ shuttles

Total Tank CAPEX: $53.51M
```

**5000m³ scenario**:
```
2030: 1 shuttle → need 1×5000×2.0 = 10,000 tons → 1 tank ✓
2031: 2 shuttles → need 2×5000×2.0 = 20,000 tons → 1 tank ✓
2034: 3 shuttles → need 3×5000×2.0 = 30,000 tons → 1 tank ✓
2043: 6 shuttles → need 6×5000×2.0 = 60,000 tons → 2 tanks
...
2050: 6+ shuttles

Total Tank CAPEX: $60.17M
Difference: $6.66M MORE tank cost for 5000m³
```

**Conclusion**: Over 20 years, 2500m³ is better because:
1. Better initial efficiency in 2030
2. Lower tank cost growth because tank capacity is shared across more smaller shuttles

## The Core Issue: Tank Sizing Constraint

Looking at the tank constraint implementation in optimizer.py, there might be an issue with how tanks are sized and managed.

**Expected Behavior**:
- With safety factor β=2.0, a 35,000-ton tank can support:
  - 2500m³ × 2.0 = 5,000m³ per shuttle → 7 shuttles per tank
  - 5000m³ × 2.0 = 10,000m³ per shuttle → 3.5 shuttles per tank

**Actual Data**:
- 2500m³ with 2 shuttles needs 2 tanks in 2030
- 5000m³ with 1 shuttle needs 1 tank in 2030

This suggests the tank constraint might be using TOTAL shuttle fleet capacity, not just the operational capacity.

## Validation Questions

1. **Is the tank sizing constraint using the correct formula?**
   - Current: `N[t] × shuttle_size × β ≤ Z[t] × tank_volume`
   - Should it consider: only operational shuttles? fleet redundancy? peak capacity?

2. **Why does 2500m³ need more tanks than 5000m³ proportionally?**
   - 2500m³: Start with 2 shuttles, end with 8+ → need 2 tanks initially, up to 8+
   - 5000m³: Start with 1 shuttle, end with 6 → need 1 tank initially, up to 2

3. **Is this economically realistic?**
   - Should fleet size determine tank capacity?
   - Or should each shuttle have its own receiving capacity?

## Recommendation

**URGENT**: Need to review the tank sizing constraint in optimizer.py to ensure:
1. Constraint is mathematically correct
2. Constraint reflects realistic operational needs
3. Constraint doesn't artificially penalize smaller shuttles over 20 years

The current implementation creates a situation where:
- Annual_simulation for single year shows 5000m³ is better
- MLIP for 20-year horizon shows 2500m³ is better
- The 20-year advantage comes primarily from tank sizing, not operational efficiency

