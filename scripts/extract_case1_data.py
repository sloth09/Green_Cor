"""
Extract key data from Case 1 optimization results for report generation.
"""
import pandas as pd
import sys

# Load scenario summary
df_scenario = pd.read_csv('results/MILP_scenario_summary_case_1.csv')
df_scenario_sorted = df_scenario.sort_values('LCOAmmonia_USD_per_ton')

# Get optimal scenario
opt = df_scenario_sorted.iloc[0]

print("="*60)
print("CASE 1 OPTIMIZATION RESULTS")
print("="*60)
print(f"\nOptimal Scenario:")
print(f"  Shuttle Size: {int(opt['Shuttle_Size_cbm'])} m³")
print(f"  Pump Rate: {int(opt['Pump_Size_m3ph'])} m³/h")
print(f"  LCOAmmonia: ${opt['LCOAmmonia_USD_per_ton']:.2f}/ton")
print(f"  20-Year NPC: ${opt['NPC_Total_USDm']:.1f} billion")
print(f"  Cycle Time: {opt['Cycle_Duration_hr']:.2f} hours")
print(f"  Trips per Call: {opt['Trips_per_Call']:.1f}")

print(f"\n\nTop 5 Scenarios:")
print("-"*80)
for i, row in df_scenario_sorted.head(5).iterrows():
    print(f"{df_scenario_sorted.index.get_loc(i)+1}. {int(row['Shuttle_Size_cbm'])}m³ × {int(row['Pump_Size_m3ph'])}m³/h: "
          f"${row['LCOAmmonia_USD_per_ton']:.2f}/ton, NPC=${row['NPC_Total_USDm']:.1f}B")

print(f"\n\nWorst 3 Scenarios:")
print("-"*80)
for i, row in df_scenario_sorted.tail(3).iterrows():
    print(f"{int(row['Shuttle_Size_cbm'])}m³ × {int(row['Pump_Size_m3ph'])}m³/h: "
          f"${row['LCOAmmonia_USD_per_ton']:.2f}/ton (Trips={row['Trips_per_Call']:.0f})")

# Load yearly results for optimal scenario
df_yearly = pd.read_csv('results/MILP_per_year_results_case_1.csv')
df_yearly_opt = df_yearly[(df_yearly['Shuttle_Size_cbm'] == int(opt['Shuttle_Size_cbm'])) & 
                          (df_yearly['Pump_Size_m3ph'] == int(opt['Pump_Size_m3ph']))]

print(f"\n\nFleet Growth (Optimal Scenario):")
print("-"*80)
for _, row in df_yearly_opt[df_yearly_opt['Year'].isin([2030, 2035, 2040, 2045, 2050])].iterrows():
    print(f"{int(row['Year'])}: {int(row['Total_Shuttles'])} shuttles "
          f"({int(row['New_Shuttles'])} new), "
          f"Util={row['Utilization_Rate']*100:.1f}%")

print("="*60)
