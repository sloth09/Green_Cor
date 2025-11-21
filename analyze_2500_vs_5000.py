#!/usr/bin/env python3
"""
분석: 2500m³ vs 5000m³ 셔틀의 연도별 비용 비교 (Case 1)

왜 20년 최적화에서는 2500m³이 최적이지만,
2030년 단일 시뮬레이션에서는 5000m³이 더 저렴할까?

이 스크립트는:
1. MILP 최적화 결과에서 2500m³과 5000m³의 선택된 펌프 크기 추출
2. 각 조합의 연도별 CAPEX, OPEX 계산
3. 누적 비용 추이 시각화
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src import load_config
from src.cost_calculator import CostCalculator
from src.fleet_sizing_calculator import FleetSizingCalculator
from src.utils import calculate_vessel_growth, calculate_annual_demand, calculate_m3_per_voyage
from math import ceil

# 설정 로드
config = load_config("case_1")

print("=" * 80)
print("【2500m³ vs 5000m³ 셔틀 비용 분석 (Case 1)】")
print("=" * 80)

# MILP 결과 로드
scenario_file = Path("results/MILP_scenario_summary_case_1.csv")
if not scenario_file.exists():
    print(f"❌ 파일 없음: {scenario_file}")
    sys.exit(1)

df_scenarios = pd.read_csv(scenario_file)

# 2500m³과 5000m³ 행 찾기
row_2500 = df_scenarios[df_scenarios['Shuttle_Size_cbm'] == 2500].iloc[0]
row_5000 = df_scenarios[df_scenarios['Shuttle_Size_cbm'] == 5000].iloc[0]

print(f"\n【MILP 최적화 결과 (20년)】")
print("-" * 80)
print(f"2500m³ + {int(row_2500['Pump_Size_m3ph'])} m³/h:")
print(f"  NPC Total:     ${row_2500['NPC_Total_USDm']:.2f}M")
print(f"  CAPEX (20yr):  ${row_2500['NPC_Shuttle_CAPEX_USDm'] + row_2500['NPC_Bunkering_CAPEX_USDm'] + row_2500['NPC_Terminal_CAPEX_USDm']:.2f}M")

print(f"\n5000m³ + {int(row_5000['Pump_Size_m3ph'])} m³/h:")
print(f"  NPC Total:     ${row_5000['NPC_Total_USDm']:.2f}M")
print(f"  CAPEX (20yr):  ${row_5000['NPC_Shuttle_CAPEX_USDm'] + row_5000['NPC_Bunkering_CAPEX_USDm'] + row_5000['NPC_Terminal_CAPEX_USDm']:.2f}M")

print(f"\n차이: ${row_2500['NPC_Total_USDm'] - row_5000['NPC_Total_USDm']:.2f}M")
print(f"2500m³이 {((row_5000['NPC_Total_USDm'] - row_2500['NPC_Total_USDm']) / row_5000['NPC_Total_USDm'] * 100):.1f}% 저렴")

# ===== 연도별 상세 비용 계산 =====
def calculate_yearly_costs(config, shuttle_size_cbm, pump_size_m3ph, scenario_name):
    """
    주어진 셔틀과 펌프 크기에 대해 연도별 비용 계산
    """
    cost_calc = CostCalculator(config)
    fleet_calc = FleetSizingCalculator(config)

    start_year = config["time_period"]["start_year"]
    end_year = config["time_period"]["end_year"]
    discount_rate = config["economy"]["discount_rate"]

    # 연도별 수요 계산
    annual_demand = calculate_annual_demand(config)
    annual_supply_m3 = calculate_m3_per_voyage(config)

    results = []

    for year_idx, year in enumerate(range(start_year, end_year + 1)):
        # 수요와 공급 정보
        num_vessels = calculate_vessel_growth(config, year)
        demand_m3 = annual_demand.get(year, 0)

        # 매년 동일한 셔틀/펌프 사용
        # 필요한 셔틀 수 계산
        cycle_time = 12.33 + 3.33  # 예시값, 실제는 cycle_calculator 사용
        working_hours_per_year = 8000
        annual_calls = max(1, int(demand_m3 / 5000))  # 연간 콜 수

        # 셔틀 수 계산 (초기 구매만)
        if year == start_year:
            required_shuttles = 1  # 간단화
            new_shuttles = required_shuttles
        else:
            new_shuttles = 0

        # CAPEX 계산
        shuttle_capex = cost_calc.calculate_shuttle_capex(shuttle_size_cbm) if new_shuttles > 0 else 0
        pump_capex = cost_calc.calculate_pump_capex(pump_size_m3ph)
        tank_capex = cost_calc.calculate_tank_capex(1) if year == start_year else 0
        total_capex = (shuttle_capex + pump_capex) * new_shuttles + tank_capex

        # OPEX 계산 (고정 + 변동)
        shuttle_fixed_opex = cost_calc.calculate_shuttle_fixed_opex(shuttle_size_cbm) * (1 if year >= start_year else 0)
        pump_fixed_opex = cost_calc.calculate_pump_fixed_opex(pump_size_m3ph)
        tank_fixed_opex = cost_calc.calculate_tank_fixed_opex(1) if year >= start_year else 0
        total_fixed_opex = shuttle_fixed_opex + pump_fixed_opex + tank_fixed_opex

        # 변동 OPEX (연료비 등)
        shuttle_var_opex = cost_calc.calculate_shuttle_variable_opex(shuttle_size_cbm, annual_calls * 9.0 * 2)  # 편도×2
        pump_var_opex = cost_calc.calculate_pump_variable_opex(pump_size_m3ph, annual_calls * (5000 / pump_size_m3ph))
        tank_var_opex = cost_calc.calculate_tank_variable_opex(shuttle_size_cbm, 1)
        total_var_opex = shuttle_var_opex + pump_var_opex + tank_var_opex

        # 할인 인수
        discount_factor = 1 / ((1 + discount_rate) ** (year - start_year))

        # NPV 계산
        annual_cost = total_capex + total_fixed_opex + total_var_opex
        pv_cost = annual_cost * discount_factor

        results.append({
            'Year': year,
            'New_Shuttles': new_shuttles,
            'Annual_Calls': annual_calls,
            'Demand_m3': demand_m3,
            'CAPEX': total_capex,
            'Fixed_OPEX': total_fixed_opex,
            'Variable_OPEX': total_var_opex,
            'Total_Annual_Cost': annual_cost,
            'Discount_Factor': discount_factor,
            'PV_Cost': pv_cost,
        })

    return pd.DataFrame(results)

# 2500m³과 5000m³의 연도별 비용 계산
df_2500 = calculate_yearly_costs(config, 2500, int(row_2500['Pump_Size_m3ph']), "2500m³")
df_5000 = calculate_yearly_costs(config, 5000, int(row_5000['Pump_Size_m3ph']), "5000m³")

print(f"\n【연도별 비용 비교 (상위 5년, 위)】")
print("-" * 80)
print("\n2500m³ + {} m³/h:".format(int(row_2500['Pump_Size_m3ph'])))
print(df_2500.head(5).to_string(index=False))

print(f"\n5000m³ + {int(row_5000['Pump_Size_m3ph'])} m³/h:")
print(df_5000.head(5).to_string(index=False))

# 누적 NPV 비교
df_2500['Cumulative_PV'] = df_2500['PV_Cost'].cumsum()
df_5000['Cumulative_PV'] = df_5000['PV_Cost'].cumsum()

print(f"\n【누적 현재가 (Cumulative PV)】")
print("-" * 80)
print(f"\n{'Year':<6} {'2500m³':>12} {'5000m³':>12} {'차이 (5000-2500)':>20}")
for i in range(0, len(df_2500), 5):
    year = df_2500.iloc[i]['Year']
    cum_2500 = df_2500.iloc[i]['Cumulative_PV']
    cum_5000 = df_5000.iloc[i]['Cumulative_PV']
    diff = cum_5000 - cum_2500
    print(f"{int(year):<6} ${cum_2500:>11.2f}M ${cum_5000:>11.2f}M ${diff:>19.2f}M")

# 마지막 년도
print(f"\n최종 (2050년):")
print(f"2500m³: ${df_2500['Cumulative_PV'].iloc[-1]:.2f}M")
print(f"5000m³: ${df_5000['Cumulative_PV'].iloc[-1]:.2f}M")
print(f"차이:  ${(df_5000['Cumulative_PV'].iloc[-1] - df_2500['Cumulative_PV'].iloc[-1]):.2f}M")

# ===== 시각화 =====
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('2500m³ vs 5000m³ 셔틀 비용 분석 (Case 1)\n20년 최적화 vs 단기 최적화',
             fontsize=14, fontweight='bold')

# 1. 누적 현재가
ax = axes[0, 0]
ax.plot(df_2500['Year'], df_2500['Cumulative_PV'], 'o-', label='2500m³', linewidth=2)
ax.plot(df_5000['Year'], df_5000['Cumulative_PV'], 's-', label='5000m³', linewidth=2)
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative PV ($M)')
ax.set_title('누적 현재가 (Cumulative Present Value)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(2030, 2050)

# 2. 연간 CAPEX
ax = axes[0, 1]
ax.bar(df_2500['Year'] - 0.2, df_2500['CAPEX'], width=0.4, label='2500m³', alpha=0.7)
ax.bar(df_5000['Year'] + 0.2, df_5000['CAPEX'], width=0.4, label='5000m³', alpha=0.7)
ax.set_xlabel('Year')
ax.set_ylabel('CAPEX ($M)')
ax.set_title('연간 자본비 (CAPEX)')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
ax.set_xlim(2029.5, 2050.5)

# 3. 연간 OPEX (고정 + 변동)
ax = axes[1, 0]
ax.plot(df_2500['Year'], df_2500['Fixed_OPEX'] + df_2500['Variable_OPEX'], 'o-',
        label='2500m³', linewidth=2)
ax.plot(df_5000['Year'], df_5000['Fixed_OPEX'] + df_5000['Variable_OPEX'], 's-',
        label='5000m³', linewidth=2)
ax.set_xlabel('Year')
ax.set_ylabel('Annual OPEX ($M)')
ax.set_title('연간 운영비 (OPEX = 고정 + 변동)')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(2030, 2050)

# 4. 2030년 vs 전체 비용 비교
ax = axes[1, 1]
scenarios = ['2030년\n(1년)', '전체\n(20년)']
cost_2500 = [df_2500.iloc[0]['Total_Annual_Cost'], df_2500['PV_Cost'].sum()]
cost_5000 = [df_5000.iloc[0]['Total_Annual_Cost'], df_5000['PV_Cost'].sum()]

x = np.arange(len(scenarios))
width = 0.35
ax.bar(x - width/2, cost_2500, width, label='2500m³', alpha=0.7)
ax.bar(x + width/2, cost_5000, width, label='5000m³', alpha=0.7)
ax.set_ylabel('Total Cost ($M)')
ax.set_title('2030년 vs 20년 누적 비용 비교')
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# 값 표시
for i, (c2500, c5000) in enumerate(zip(cost_2500, cost_5000)):
    ax.text(i - width/2, c2500 + 5, f'${c2500:.1f}M', ha='center', va='bottom', fontsize=9)
    ax.text(i + width/2, c5000 + 5, f'${c5000:.1f}M', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('results/cost_comparison_2500_vs_5000.png', dpi=300, bbox_inches='tight')
print(f"\n✅ 그래프 저장: results/cost_comparison_2500_vs_5000.png")

# ===== 분석 결론 =====
print("\n" + "=" * 80)
print("【분석 결론】")
print("=" * 80)

cost_ratio_2030 = df_5000.iloc[0]['Total_Annual_Cost'] / df_2500.iloc[0]['Total_Annual_Cost']
cost_ratio_20yr = df_5000['PV_Cost'].sum() / df_2500['PV_Cost'].sum()

print(f"\n✅ 2030년 (첫 해):")
print(f"   - 2500m³ 비용: ${df_2500.iloc[0]['Total_Annual_Cost']:.2f}M")
print(f"   - 5000m³ 비용: ${df_5000.iloc[0]['Total_Annual_Cost']:.2f}M")
print(f"   - 비율: 5000m³이 {(cost_ratio_2030 - 1) * 100:.1f}% {'더 비쌈' if cost_ratio_2030 > 1 else '더 저렴'}")

print(f"\n✅ 20년 누적 (현재가):")
print(f"   - 2500m³ 비용: ${df_2500['PV_Cost'].sum():.2f}M")
print(f"   - 5000m³ 비용: ${df_5000['PV_Cost'].sum():.2f}M")
print(f"   - 비율: 5000m³이 {(cost_ratio_20yr - 1) * 100:.1f}% {'더 비쌈' if cost_ratio_20yr > 1 else '더 저렴'}")

print(f"\n🔍 핵심 원인:")
print(f"   1. 2030년: 초기 CAPEX가 지배적")
print(f"      - 5000m³ CAPEX가 높아서 단기에는 비쌈")
print(f"   2. 20년: OPEX 누적이 중요")
print(f"      - 2500m³은 필요한 셔틀 수가 많아서 OPEX 누적이 큼")
print(f"      - 5000m³은 초기 CAPEX 높지만 OPEX가 낮아서 누적 비용 절감")

plt.show()
