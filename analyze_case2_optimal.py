"""
Case 2 Yeosu 최적 Shuttle 용량 분석
왜 10000m3이 최적인지, 그리고 5000m3/50000m3와의 비교 분석
"""

import pandas as pd
import numpy as np

# CSV 파일 읽기
df_summary = pd.read_csv('results/MILP_scenario_summary_case_2_yeosu.csv')
df_yearly = pd.read_csv('results/MILP_per_year_results_case_2_yeosu.csv')

# 주요 컬럼만 선택 (Summary)
columns_of_interest = [
    'Shuttle_Size_cbm', 'Pump_Size_m3ph', 
    'NPC_Total_USDm', 
    'NPC_Annualized_Shuttle_CAPEX_USDm',
    'NPC_Annualized_Bunkering_CAPEX_USDm',
    'NPC_Shuttle_vOPEX_USDm',
    'NPC_Bunkering_vOPEX_USDm',
    'Cycle_Duration_hr',
    'Trips_per_Call',
    'LCOAmmonia_USD_per_ton'
]

# 각 shuttle size별로 최적 pump를 선택 (NPC 기준)
optimal_per_size = df_summary.loc[df_summary.groupby('Shuttle_Size_cbm')['NPC_Total_USDm'].idxmin()].copy()

# 2030년과 2050년의 필요 Shuttle 수 추가
optimal_per_size['Required_Shuttles_2030'] = 0
optimal_per_size['Required_Shuttles_2050'] = 0

for idx, row in optimal_per_size.iterrows():
    shuttle_size = row['Shuttle_Size_cbm']
    pump_size = row['Pump_Size_m3ph']
    
    # Yearly data에서 해당 시나리오 찾기
    mask = (df_yearly['Shuttle_Size_cbm'] == shuttle_size) & (df_yearly['Pump_Size_m3ph'] == pump_size)
    scenario_yearly = df_yearly[mask]
    
    if not scenario_yearly.empty:
        shuttles_2030 = scenario_yearly[scenario_yearly['Year'] == 2030]['Total_Shuttles'].values[0]
        shuttles_2050 = scenario_yearly[scenario_yearly['Year'] == 2050]['Total_Shuttles'].values[0]
        
        optimal_per_size.at[idx, 'Required_Shuttles_2030'] = shuttles_2030
        optimal_per_size.at[idx, 'Required_Shuttles_2050'] = shuttles_2050

print("=" * 100)
print("Case 2 Yeosu: 각 Shuttle 용량별 최적 조합 (최적 Pump 선택)")
print("=" * 100)
# 컬럼 순서 재정렬
display_cols = columns_of_interest + ['Required_Shuttles_2030', 'Required_Shuttles_2050']
print(optimal_per_size[display_cols].to_string(index=False))

print("\n" + "=" * 100)
print("비용 구조 분석: 5000m3 vs 10000m3 (최적) vs 50000m3")
print("=" * 100)

# 비교 대상 선택
try:
    size_5000 = optimal_per_size[optimal_per_size['Shuttle_Size_cbm'] == 5000].iloc[0]
    size_10000 = optimal_per_size[optimal_per_size['Shuttle_Size_cbm'] == 10000].iloc[0]
    size_50000 = optimal_per_size[optimal_per_size['Shuttle_Size_cbm'] == 50000].iloc[0]

    print(f"\n{'항목':<40} {'5000m3':>15} {'10000m3 (최적)':>15} {'50000m3':>15}")
    print("-" * 100)
    print(f"{'총 NPC (USDm)':<40} {size_5000['NPC_Total_USDm']:>15.2f} {size_10000['NPC_Total_USDm']:>15.2f} {size_50000['NPC_Total_USDm']:>15.2f}")
    print(f"{'Shuttle CAPEX (USDm)':<40} {size_5000['NPC_Annualized_Shuttle_CAPEX_USDm']:>15.2f} {size_10000['NPC_Annualized_Shuttle_CAPEX_USDm']:>15.2f} {size_50000['NPC_Annualized_Shuttle_CAPEX_USDm']:>15.2f}")
    print(f"{'Bunkering CAPEX (USDm)':<40} {size_5000['NPC_Annualized_Bunkering_CAPEX_USDm']:>15.2f} {size_10000['NPC_Annualized_Bunkering_CAPEX_USDm']:>15.2f} {size_50000['NPC_Annualized_Bunkering_CAPEX_USDm']:>15.2f}")
    print(f"{'Shuttle Fuel Cost (vOPEX) (USDm)':<40} {size_5000['NPC_Shuttle_vOPEX_USDm']:>15.2f} {size_10000['NPC_Shuttle_vOPEX_USDm']:>15.2f} {size_50000['NPC_Shuttle_vOPEX_USDm']:>15.2f}")
    print(f"{'Cycle Duration (hours)':<40} {size_5000['Cycle_Duration_hr']:>15.2f} {size_10000['Cycle_Duration_hr']:>15.2f} {size_50000['Cycle_Duration_hr']:>15.2f}")
    print(f"{'Trips per Call':<40} {size_5000['Trips_per_Call']:>15.2f} {size_10000['Trips_per_Call']:>15.2f} {size_50000['Trips_per_Call']:>15.2f}")
    print(f"{'Required Shuttles (2030)':<40} {size_5000['Required_Shuttles_2030']:>15.0f} {size_10000['Required_Shuttles_2030']:>15.0f} {size_50000['Required_Shuttles_2030']:>15.0f}")
    print(f"{'Required Shuttles (2050)':<40} {size_5000['Required_Shuttles_2050']:>15.0f} {size_10000['Required_Shuttles_2050']:>15.0f} {size_50000['Required_Shuttles_2050']:>15.0f}")
    print(f"{'LCO (USD/ton)':<40} {size_5000['LCOAmmonia_USD_per_ton']:>15.2f} {size_10000['LCOAmmonia_USD_per_ton']:>15.2f} {size_50000['LCOAmmonia_USD_per_ton']:>15.2f}")

    print("\n" + "=" * 100)
    print("핵심 인사이트")
    print("=" * 100)

    print(f"""
    1. 최적 용량의 이동 (5000m3 -> 10000m3):
       - 여수(86nm)는 울산(25nm)보다 거리가 3.4배 멉니다.
       - 이동 시간(Travel Time)이 증가함에 따라, 한번 출항해서 더 많은 선박을 벙커링하는 것이 유리해졌습니다.
       - 5000m3: 1회 출항 시 1척 벙커링 (이동 시간 비중 높음)
       - 10000m3: 1회 출항 시 2척 벙커링 (이동 시간 절약)
       
    2. 10000m3가 5000m3보다 유리한 이유:
       - 총 NPC 절감: {size_5000['NPC_Total_USDm'] - size_10000['NPC_Total_USDm']:.2f} USDm
       - Shuttle Fuel Cost 절감: {size_5000['NPC_Shuttle_vOPEX_USDm'] - size_10000['NPC_Shuttle_vOPEX_USDm']:.2f} USDm (이동 횟수 감소 효과)
       - CAPEX는 증가했지만({size_10000['NPC_Annualized_Shuttle_CAPEX_USDm'] - size_5000['NPC_Annualized_Shuttle_CAPEX_USDm']:.2f} USDm), 연료비 절감과 운영 효율성이 이를 상쇄했습니다.
       
    3. 50000m3가 여전히 비싼 이유:
       - CAPEX가 너무 높음 ({size_50000['NPC_Annualized_Shuttle_CAPEX_USDm']:.2f} USDm)
       - 10척을 한번에 벙커링하더라도, Cycle Time이 너무 길어져서({size_50000['Cycle_Duration_hr']:.2f}h) 유연성이 떨어짐
    """)

except Exception as e:
    print(f"Error calculating comparison: {e}")
    print("Available columns:", df_summary.columns.tolist())
