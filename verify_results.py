"""
Verification script to compare results and validate Annualized CAPEX implementation.
"""

import pandas as pd
from pathlib import Path

# Load results
results_dir = Path("results")
scenario_df = pd.read_csv(results_dir / "MILP_scenario_summary_case_1.csv")
yearly_df = pd.read_csv(results_dir / "MILP_per_year_results_case_1.csv")

print("="*80)
print("Case 1 Optimization Results Verification")
print("="*80)

# 1. Check total scenarios
print(f"\n1. Total scenarios optimized: {len(scenario_df)}")

# 2. Find optimal scenario
optimal = scenario_df.nsmallest(1, 'NPC_Total_USDm').iloc[0]
print(f"\n2. Optimal scenario:")
print(f"   Shuttle: {optimal['Shuttle_Size_cbm']:.0f} m³")
print(f"   Pump: {optimal['Pump_Size_m3ph']:.0f} m³/h")
print(f"   NPC_Total: ${optimal['NPC_Total_USDm']:.2f}M")
print(f"   NPC_Annualized_Shuttle_CAPEX: ${optimal['NPC_Annualized_Shuttle_CAPEX_USDm']:.2f}M")
print(f"   NPC_Annualized_Bunkering_CAPEX: ${optimal['NPC_Annualized_Bunkering_CAPEX_USDm']:.2f}M")

# 3. Verify consistency for optimal scenario
shuttle_size = int(optimal['Shuttle_Size_cbm'])
pump_size = int(optimal['Pump_Size_m3ph'])

yearly_optimal = yearly_df[
    (yearly_df['Shuttle_Size_cbm'] == shuttle_size) & 
    (yearly_df['Pump_Size_m3ph'] == pump_size)
]

total_year_cost_sum = yearly_optimal['Total_Year_Cost_USDm'].sum()
annualized_capex_sum = yearly_optimal['Annualized_CAPEX_Total_USDm'].sum()
total_opex_sum = yearly_optimal['Total_OPEX_USDm'].sum()

print(f"\n3. Optimal scenario yearly breakdown:")
print(f"   Total_Year_Cost 21-year sum: ${total_year_cost_sum:.2f}M")
print(f"   Annualized_CAPEX 21-year sum: ${annualized_capex_sum:.2f}M")
print(f"   Total_OPEX 21-year sum: ${total_opex_sum:.2f}M")
print(f"   Verification: Annualized_CAPEX + OPEX = ${annualized_capex_sum + total_opex_sum:.2f}M")

# 4. Check consistency
npc_from_scenario = optimal['NPC_Total_USDm']
diff = abs(total_year_cost_sum - npc_from_scenario)
diff_pct = (diff / npc_from_scenario) * 100

print(f"\n4. Consistency check:")
print(f"   NPC from scenario summary: ${npc_from_scenario:.2f}M")
print(f"   Sum from yearly results: ${total_year_cost_sum:.2f}M")
print(f"   Difference: ${diff:.4f}M ({diff_pct:.4f}%)")

if diff_pct < 0.01:
    print(f"   ✅ PASS: Difference within tolerance (< 0.01%)")
else:
    print(f"   ❌ FAIL: Difference exceeds tolerance")

# 5. Show top 10 scenarios
print(f"\n5. Top 10 scenarios by NPC:")
print("="*80)
top10 = scenario_df.nsmallest(10, 'NPC_Total_USDm')
print(top10[['Shuttle_Size_cbm', 'Pump_Size_m3ph', 'NPC_Total_USDm', 
             'NPC_Annualized_Shuttle_CAPEX_USDm', 'NPC_Annualized_Bunkering_CAPEX_USDm']].to_string(index=False))

# 6. Check for Annualized CAPEX columns
print(f"\n6. Column verification:")
required_cols = ['Actual_CAPEX_Total_USDm', 'Annualized_CAPEX_Total_USDm', 'Total_OPEX_USDm', 'Total_Year_Cost_USDm']
for col in required_cols:
    if col in yearly_df.columns:
        print(f"   ✅ {col} present")
    else:
        print(f"   ❌ {col} missing")

print("\n" + "="*80)
print("Verification Complete")
print("="*80)
