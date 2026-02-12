# Data Inventory for Paper Writing

This document maps all available data sources, their file paths, key columns, and extraction patterns for the paper-writer skill.

---

## 1. Deterministic Optimization Results

### 1.1 Scenario Summary Files (One row per shuttle/pump combination)

| Case | File Path |
|------|-----------|
| Case 1 (Busan) | `results/deterministic/MILP_scenario_summary_case_1.csv` |
| Case 2 (Ulsan) | `results/deterministic/MILP_scenario_summary_case_2.csv` |
| Case 3 (Yeosu) | `results/deterministic/MILP_scenario_summary_case_3.csv` |

**Key Columns:**
| Column | Unit | Description | Paper Use |
|--------|------|-------------|-----------|
| `Shuttle_Size_cbm` | m3 | Shuttle capacity | Independent variable |
| `Pump_Size_m3ph` | m3/h | Pump flow rate | Independent variable |
| `NPC_Total_USDm` | USD million | 20-year Net Present Cost | Primary objective |
| `LCOAmmonia_USD_per_ton` | USD/ton | Levelized Cost of Ammonia | Key metric for comparison |
| `Cycle_Duration_hr` | hours | Full cycle time | Operational analysis |
| `Annual_Cycles_Max` | count | Max cycles per year | Capacity analysis |
| `Vessels_per_Trip` | count | Ships served per shuttle trip | Case 2 efficiency |
| `Time_Utilization_Ratio_percent` | % | Fleet utilization | Efficiency metric |
| `Trips_per_Call` | count | Trips needed per bunkering call | Case 1 logistics |
| `NPC_Annualized_Shuttle_CAPEX_USDm` | USD million | Shuttle capital cost (annualized) | Cost breakdown |
| `NPC_Annualized_Bunkering_CAPEX_USDm` | USD million | Pump/bunkering capital cost | Cost breakdown |
| `NPC_Shuttle_fOPEX_USDm` | USD million | Shuttle fixed operating cost | Cost breakdown |
| `NPC_Shuttle_vOPEX_USDm` | USD million | Shuttle variable operating cost | Cost breakdown |
| `Annuity_Factor` | dimensionless | AF = [1-(1+r)^-n]/r | Methodology |
| `Annualized_Cost_USDm_per_year` | USD million/yr | NPC / 21 years | Annual comparison |
| `Total_Supply_20yr_ton` | tons | Total ammonia delivered | Demand verification |

### 1.2 Per-Year Results Files (One row per shuttle/pump/year)

| Case | File Path |
|------|-----------|
| Case 1 (Busan) | `results/deterministic/MILP_per_year_results_case_1.csv` |
| Case 2 (Ulsan) | `results/deterministic/MILP_per_year_results_case_2.csv` |
| Case 3 (Yeosu) | `results/deterministic/MILP_per_year_results_case_3.csv` |

**Key Columns (in addition to scenario summary columns):**
| Column | Unit | Description | Paper Use |
|--------|------|-------------|-----------|
| `Year` | year | 2030-2050 | Time axis |
| `New_Shuttles` | count | Shuttles added this year | Fleet expansion |
| `Total_Shuttles` | count | Cumulative fleet size | Fleet evolution |
| `Annual_Calls` | count | Bunkering calls this year | Demand growth |
| `Annual_Cycles` | count | Total cycles this year | Operational volume |
| `Supply_m3` | m3 | Ammonia supplied this year | Supply adequacy |
| `Demand_m3` | m3 | Ammonia demanded this year | Demand growth |
| `Utilization_Rate` | ratio | Actual/available capacity | Efficiency |
| `Actual_CAPEX_Shuttle_USDm` | USD million | Actual shuttle purchase cost | Investment timing |
| `Annualized_CAPEX_Total_USDm` | USD million | Year's annualized CAPEX | Cost trajectory |
| `Total_Year_Cost_USDm` | USD million | Total cost this year | Cost evolution |

---

## 2. Sensitivity Analysis Results

### 2.1 Pump Rate Sensitivity (3 files)

| Case | File Path |
|------|-----------|
| Case 1 | `results/sensitivity/pump_sensitivity_case_1.csv` |
| Case 2 | `results/sensitivity/pump_sensitivity_case_2.csv` |
| Case 3 | `results/sensitivity/pump_sensitivity_case_3.csv` |

**Columns:** `Pump_Rate_m3ph`, `Min_NPC_USDm`, `Optimal_Shuttle_cbm`, `LCO_USD_per_ton`

### 2.2 Fuel Price Sensitivity (3 files)

| Case | File Path |
|------|-----------|
| Case 1 | `results/sensitivity/fuel_price_case_1.csv` |
| Case 2 | `results/sensitivity/fuel_price_case_2.csv` |
| Case 3 | `results/sensitivity/fuel_price_case_3.csv` |

**Columns:** `Variation`, `Parameter_Value`, `NPC_USDm`, `LCO_USD_per_ton`, `NPC_Change_Pct`
**Range:** $300~$1,200/ton, 9 points

### 2.3 Tornado Diagram Data (3 files)

| Case | File Path |
|------|-----------|
| Case 1 | `results/sensitivity/tornado_det_case_1.csv` |
| Case 2 | `results/sensitivity/tornado_det_case_2.csv` |
| Case 3 | `results/sensitivity/tornado_det_case_3.csv` |

**Columns:** `Parameter`, `Low_NPC_USDm`, `High_NPC_USDm`, `Swing_USDm`, `Swing_Pct`
**Parameters:** CAPEX Scaling, Bunker Volume, Max Annual Hours, Travel Time, Fuel Price, SFOC
(6 parameters, each +/-20% from baseline)

### 2.4 Bunker Volume Sensitivity (3 files)

| Case | File Path |
|------|-----------|
| Case 1 | `results/sensitivity/bunker_volume_case_1.csv` |
| Case 2 | `results/sensitivity/bunker_volume_case_2.csv` |
| Case 3 | `results/sensitivity/bunker_volume_case_3.csv` |

**Columns:** `Variation`, `Parameter_Value`, `NPC_USDm`, `LCO_USD_per_ton`, `NPC_Change_Pct`
**Range:** 2,500~10,000 m3, 7 points

### 2.5 Two-way Sensitivity (1 file, Case 1 only)

| File Path |
|-----------|
| `results/sensitivity/two_way_det_case_1.csv` |

**Format:** Matrix (pivot table). Rows = Fuel_Price ($420~$780, 5 levels), Columns = Bunker_Volume (3500~6500 m3, 5 levels). Values = NPC_USDm.

### 2.6 Demand Scenarios (3 case files + 1 summary)

| File | Path |
|------|------|
| Case 1 | `results/sensitivity/demand_scenarios_case_1.csv` |
| Case 2 | `results/sensitivity/demand_scenarios_case_2.csv` |
| Case 3 | `results/sensitivity/demand_scenarios_case_3.csv` |
| Summary | `results/sensitivity/demand_scenarios_summary.csv` |

**Columns:** `Case`, `Scenario`, `Start_Vessels`, `End_Vessels`, `Optimal_Shuttle_cbm`, `Optimal_Pump_m3ph`, `NPC_Total_USDm`, `LCO_USD_per_ton`, plus cost component columns.
**Scenarios:** Low (250), Base (500), High (750), VeryHigh (1000) end_vessels.

### 2.7 Break-even Distance Analysis (3 files)

| File | Path |
|------|------|
| Ulsan | `results/sensitivity/breakeven_distance_ulsan.csv` |
| Yeosu | `results/sensitivity/breakeven_distance_yeosu.csv` |
| Combined | `results/sensitivity/breakeven_distance_combined.csv` |

**Columns:** `Distance_nm`, `{Case1}_NPC_USDm`, `{Case2}_NPC_USDm`, `Difference_USDm`, `Preferred_Case`, `Comparison`
**Range:** 10~200 nm, 20 points. Ulsan uses shuttle=5,000 m3, Yeosu uses shuttle=10,000 m3.

### 2.8 Discount Rate Sensitivity (v2 NEW, 4 files)

| File | Path |
|------|------|
| Comparison | `results/discount_rate_analysis/data/discount_rate_comparison.csv` |
| Case 1 Yearly | `results/discount_rate_analysis/data/discount_rate_yearly_case_1.csv` |
| Case 2 Yearly | `results/discount_rate_analysis/data/discount_rate_yearly_case_2.csv` |
| Case 3 Yearly | `results/discount_rate_analysis/data/discount_rate_yearly_case_3.csv` |

**Columns (comparison):** `Case`, `Case_Label`, `Discount_Rate`, `Discount_Rate_Pct`, `Optimal_Shuttle_cbm`, `Optimal_Pump_m3ph`, `NPC_Total_USDm`, `LCO_USD_per_ton`, cost component columns, `Annualized_Cost_USDm_per_year`

**Columns (yearly):** Same as per-year results (Section 1.2) with additional `Discount_Rate` column.

### 2.9 Yang & Lam DES Comparison (v2 NEW, 7 files)

| File | Path |
|------|------|
| Service Time | `results/yang_lam_des_comparison/data/service_time_comparison.csv` |
| Methodology | `results/yang_lam_des_comparison/data/methodology_comparison.csv` |
| Cost Structure | `results/yang_lam_des_comparison/data/cost_structure_comparison.csv` |
| Flow Rate Sens. | `results/yang_lam_des_comparison/data/flow_rate_sensitivity_comparison.csv` |
| Sens. Summary | `results/yang_lam_des_comparison/data/sensitivity_summary_comparison.csv` |
| Reference Data | `results/yang_lam_des_comparison/data/yang_lam_reference_data.csv` |
| Summary | `results/yang_lam_des_comparison/data/comparison_summary.txt` |

---

## 3. Stochastic Analysis Results

### 3.1 Case 1 (Busan)
| File | Path |
|------|------|
| Deterministic baseline | `results/stochastic/deterministic_scenarios_case_1.csv` |
| Deterministic yearly | `results/stochastic/deterministic_yearly_case_1.csv` |
| Stochastic scenarios | `results/stochastic/stochastic_scenarios_case_1.csv` |
| Stochastic summary | `results/stochastic/stochastic_summary_case_1.csv` |
| Tornado data | `results/stochastic/tornado_case_1.csv` |
| Fuel price sensitivity | `results/stochastic/sensitivity_fuel_price_case_1.csv` |
| Case comparison | `results/stochastic/case_comparison.csv` |

### 3.2 Case 2 (Ulsan)
Base path: `results/stochastic_case2/`
Same file naming pattern as Case 1 with `_case_2` suffix.

### 3.3 Case 3 (Yeosu)
Base path: `results/stochastic_case3/`
Same file naming pattern as Case 1 with `_case_3` suffix.

---

## 4. Configuration Files

| File | Content | Paper Use |
|------|---------|-----------|
| `config/base.yaml` | Common parameters | Methodology section |
| `config/case_1.yaml` | Case 1 specifics | Case description |
| `config/case_2_ulsan.yaml` | Case 2 specifics | Case description |
| `config/case_3_yeosu.yaml` | Case 3 specifics | Case description |
| `config/stochastic.yaml` | Uncertainty parameters | Stochastic methodology |

**Key Parameters to Extract:**
| Parameter | Path in YAML | Value | Paper Section |
|-----------|-------------|-------|---------------|
| Planning horizon | `time_period.start_year` / `end_year` | 2030-2050 | Methodology |
| Discount rate | `economy.discount_rate` | 0.0 | Methodology |
| Fuel price | `economy.fuel_price_usd_per_ton` | 600 | Methodology |
| Initial fleet | `shipping.start_vessels` | 50 | Problem definition |
| Final fleet | `shipping.end_vessels` | 500 | Problem definition |
| Voyages/year | `shipping.voyages_per_year` | 12 | Methodology |
| Max hours | `operations.max_annual_hours_per_vessel` | 8000 | Constraints |
| CAPEX scaling | `shuttle_capex.base_cost_usd_million` | 61.5 | Cost model |
| CAPEX exponent | `shuttle_capex.scaling_exponent` | 0.75 | Cost model |
| Annualization rate | `annualization.rate` | 0.07 | Cost model |
| Annualization period | `annualization.period_years` | 21 | Cost model |

---

## 5. Key Numbers Extraction Guide (Deterministic)

**WARNING: This section contains NO hardcoded values. All numbers MUST be extracted fresh from CSV/config during Phase 0. Never copy values from any reference document.**

### How to Extract Optimal Solutions

Read `results/deterministic/MILP_scenario_summary_{case_id}.csv` for each case.
Find the row with minimum `NPC_Total_USDm`. Record:

| Case | Extract from CSV |
|------|-----------------|
| Case 1 (Busan) | `Shuttle_Size_cbm`, `Pump_Size_m3ph`, `NPC_Total_USDm`, `LCOAmmonia_USD_per_ton` |
| Case 2 (Ulsan) | same columns |
| Case 3 (Yeosu) | same columns |

### How to Extract Cost Structure

From the optimal row of each case, read these NPC component columns:

| Column | Description |
|--------|-------------|
| `NPC_Annualized_Shuttle_CAPEX_USDm` | Shuttle capital cost |
| `NPC_Annualized_Bunkering_CAPEX_USDm` | Pump/bunkering capital cost |
| `NPC_Shuttle_fOPEX_USDm` | Shuttle fixed operating cost |
| `NPC_Shuttle_vOPEX_USDm` | Shuttle variable operating cost |
| `NPC_Bunkering_fOPEX_USDm` | Bunkering fixed operating cost |
| `NPC_Bunkering_vOPEX_USDm` | Bunkering variable operating cost |

### How to Extract Operational Parameters

From the optimal row, read:
- `Cycle_Duration_hr` - Full cycle time
- `Annual_Cycles_Max` - Max cycles per year
- `Vessels_per_Trip` - Ships served per shuttle trip
- `Total_Supply_20yr_ton` - Total ammonia delivered
- `Annualized_Cost_USDm_per_year` - Annual cost

### How to Extract Sensitivity Key Results

| Analysis | Source File | What to Extract |
|----------|-----------|-----------------|
| Fuel price range | `fuel_price_{case_id}.csv` | Min/max `NPC_USDm` across price range |
| Tornado top driver | `tornado_det_{case_id}.csv` | Parameter with max `Swing_Pct` |
| Tornado SFOC swing | `tornado_det_{case_id}.csv` | `Swing_USDm` for SFOC parameter |
| Break-even distance | `breakeven_distance_*.csv` | Where `Preferred_Case` changes |

### How to Extract Demand Scenario Results

From `demand_scenarios_summary.csv`:
- Read all rows for each case x scenario combination
- Key columns: `Scenario`, `End_Vessels`, `NPC_Total_USDm`, `LCO_USD_per_ton`
- Calculate LCO stability: range across scenarios for each case
- Check if `Optimal_Shuttle_cbm` changes across scenarios

### Discount Rate Sensitivity

From `discount_rate_comparison.csv` (9 rows: 3 cases x 3 rates):
- Key columns: `Discount_Rate_Pct`, `Optimal_Shuttle_cbm`, `NPC_Total_USDm`, `LCO_USD_per_ton`
- Key check: does `Optimal_Shuttle_cbm` change across discount rates?
- Calculate NPC reduction percentage from r=0% to r=8%

### Yang & Lam DES Comparison Key Metrics

From `yang_lam_des_comparison/data/`:
- `flow_rate_sensitivity_comparison.csv` → flow rate sensitivity percentages
- `service_time_comparison.csv` → service time at 3 transfer volumes
- `cost_structure_comparison.csv` → annual cost figures

**Framing notes** (from `yang_lam_evaluation.md`):
- Methodology comparison (Table 10) = strongest contribution (grade A)
- Flow rate sensitivity gap = meaningful, caused by DES TRIA smoothing (grade B+)
- Service time "agreement" = only pumping component shared (grade B-, do not overstate)
- Annual cost similarity = coincidental scope difference (grade C, mention only)

---

## 6. Extraction Patterns

### Pattern: Find optimal scenario
```python
# Read CSV, find row with minimum NPC_Total_USDm
import pandas as pd
df = pd.read_csv('results/deterministic/MILP_scenario_summary_case_1.csv')
optimal = df.loc[df['NPC_Total_USDm'].idxmin()]
optimal_shuttle = optimal['Shuttle_Size_cbm']
optimal_pump = optimal['Pump_Size_m3ph']
```

### Pattern: Extract yearly data for optimal scenario
```python
yearly = pd.read_csv('results/deterministic/MILP_per_year_results_case_1.csv')
# Use values extracted from optimal scenario above -- NEVER hardcode
optimal_yearly = yearly[
    (yearly['Shuttle_Size_cbm'] == optimal_shuttle) &
    (yearly['Pump_Size_m3ph'] == optimal_pump)
]
```

### Pattern: Cost component ratios
```
CAPEX_ratio = (Shuttle_CAPEX + Bunkering_CAPEX) / NPC_Total
OPEX_ratio = 1 - CAPEX_ratio
vOPEX_share = (Shuttle_vOPEX + Bunkering_vOPEX) / Total_OPEX
```

---

## 7. Figure Files

All figures available in both PNG and PDF format.

**Working (volatile):** `results/paper_figures/` - regenerated by Python scripts
**Preserved (stable):**
- Paper 1: `results/paper1_deterministic/figures/` (D*, Fig*, FigS*)
- Paper 2: `results/paper2_stochastic/figures/` (S*, C*)

| Series | Count | Purpose | Paper |
|--------|-------|---------|-------|
| D1-D12 | 12 figures (+ sub-figures) | Deterministic base analysis | Paper 1 |
| Fig7-Fig10 | 4 figures | SCI paper deterministic sensitivity | Paper 1 |
| Fig11-Fig12 | 2 figures | Discount rate sensitivity (v2 NEW) | Paper 1 |
| Fig13-Fig14 | 2 figures | Yang & Lam DES comparison (v2 NEW) | Paper 1 |
| FigS4-FigS5 | 2 figures | SCI paper supplementary sensitivity | Paper 1 |
| S1-S7 | 7 figures | Stochastic analysis | Paper 2 |
| C1-C4 | 4 figures | Comparison analysis | Paper 2 |

### SCI Paper Figures (New)
| ID | File | Data Source |
|----|------|-------------|
| Fig7 | `Fig7_tornado_deterministic.png` | `tornado_det_*.csv` |
| Fig8 | `Fig8_fuel_price_sensitivity.png` | `fuel_price_*.csv` |
| Fig9 | `Fig9_breakeven_distance.png` | `breakeven_distance_*.csv` |
| Fig10 | `Fig10_demand_scenarios.png` | `demand_scenarios_*.csv` |
| FigS4 | `FigS4_twoway_deterministic.png` | `two_way_det_case_1.csv` |
| FigS5 | `FigS5_bunker_volume_sensitivity.png` | `bunker_volume_*.csv` |

See `figure-map.md` for detailed section-to-figure mapping.

---

## 8. Stable Data Locations

Working pipeline paths (`results/deterministic/`, `results/sensitivity/`) remain unchanged for script compatibility. Preserved copies provide stable snapshots for paper submission.

| Paper | Working Data | Preserved Data | Preserved Figures |
|-------|-------------|----------------|-------------------|
| Paper 1 (Deterministic) | `results/deterministic/` + `results/sensitivity/` | `results/paper1_deterministic/data/` + `sensitivity/` | `results/paper1_deterministic/figures/` |
| Paper 2 (Stochastic) | `results/stochastic*/` | `results/paper2_stochastic/data/` + `sensitivity/` | `results/paper2_stochastic/figures/` |
| Verification | `results/deterministic/` | `results/verification_bundle/data/` | `results/verification_bundle/figures/` |

Run `python scripts/preserve_paper_results.py` after any figure regeneration to update preserved copies.
