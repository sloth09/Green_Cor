# Tank Constraint Issue: Source of Annual_Simulation vs MLIP Discrepancy

## The Constraint (optimizer.py, Line 285)

```python
prob += N[t] * shuttle_size * self.tank_safety_factor <= tank_capacity
```

Where:
- `N[t]` = number of shuttles in year t
- `shuttle_size` = capacity of each shuttle (m³)
- `self.tank_safety_factor` = β = 2.0
- `tank_capacity` = Z[t] × tank_volume = Z[t] × 35,000 tons

## The Problem

This constraint forces tank requirements to scale with fleet size, creating an artificial penalty for smaller shuttles over 20 years.

### Example: 2500m³ vs 5000m³

**2030 (50 vessels)**:
```
2500m³ scenario:
  - Fleet: 2 shuttles
  - Tank need: 2 × 2500m³ × 2.0 = 10,000 tons → 1 tank
  - But MLIP shows: 2 tanks purchased
  
5000m³ scenario:
  - Fleet: 1 shuttle  
  - Tank need: 1 × 5000m³ × 2.0 = 10,000 tons → 1 tank
  - MLIP shows: 1 tank purchased ✓
```

**2050 (500 vessels)**:
```
2500m³ scenario:
  - Fleet: 8+ shuttles
  - Tank need: 8+ × 2500m³ × 2.0 = 40,000+ tons → 2 tanks minimum
  - MLIP shows: 8+ tanks

5000m³ scenario:
  - Fleet: 6 shuttles
  - Tank need: 6 × 5000m³ × 2.0 = 60,000 tons → 2 tanks
  - MLIP shows: 6 tanks
```

### The Cost Impact Over 20 Years

- **2500m³**: Total Tank CAPEX = $53.51M (for 8 tanks total)
- **5000m³**: Total Tank CAPEX = $60.17M (for 6 tanks total)

**Why the discrepancy?**
- Both need ~2-3 tanks in 2030 to meet 50-vessel demand  
- But smaller shuttles require more units → need more tanks across the timeline
- Larger shuttles require fewer units → need fewer total tanks
- Result: Larger shuttles get $6.66M advantage in tank costs

## Is This Realistic?

**Current Model Assumption**:
- Tank capacity must match peak fleet capacity (N[t] × shuttle_size × β)
- Each shuttle adds to storage requirement
- More shuttles = more tanks needed

**Alternative Model (May be more realistic)**:
- Tank capacity based on operational need, not fleet size
- Tank sizing independent of number of shuttles (only demand level)
- Multiple shuttles share one tank facility

## Why annual_simulation vs MLIP Show Different Results

### annual_simulation (Single Year):
- Calculates optimal fleet for 2030 only
- Tank is fixed one-time CAPEX ($42.525M)
- Doesn't show long-term tank scaling penalty
- Result: 5000m³ is cheaper ($58.9M vs $62.4M)

### MLIP (20-Year Horizon):
- Optimizes fleet growth from 50→500 vessels
- Tank constraint grows with fleet size
- Cumulative tank costs favor fewer, larger shuttles
- Result: 2500m³ is cheaper ($176.74M vs $196.18M)

## Recommendation

Need to decide:

1. **Keep current constraint** (tank scales with fleet):
   - Assumption: More shuttles = more space at facility
   - Realistic for: Modular tank systems, multiple load points
   - Accept: Smaller shuttles penalized in long-term analysis

2. **Change to demand-based tank sizing**:
   - Assumption: Tank size depends on demand, not fleet size
   - Realistic for: Large fixed facility that serves any fleet size
   - Benefit: Consistent with annual_simulation logic
   - Requires: Different constraint formulation

3. **Investigate if MLIP tank decisions are correct**:
   - Current: Shows buying 8 tanks for 8 shuttles
   - Question: Is this optimal? Or should tanks be shared/sized differently?
   - Check: Does the tank constraint allow tank sharing across years?

