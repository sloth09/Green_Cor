#!/usr/bin/env python3
"""
분석: 2500m³ vs 5000m³ 셔틀의 연도별 비용 비교 (Case 1)

실제 MILP 결과 데이터를 사용하여:
1. 2500m³과 5000m³의 최적 펌프 크기 추출
2. 연도별 CAPEX, OPEX, 누적 현재가 계산
3. 왜 20년 최적화와 2030년 최적값이 다른지 시각화
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# 결과 파일 로드
per_year_file = Path("results/MILP_per_year_results_case_1.csv")
summary_file = Path("results/MILP_scenario_summary_case_1.csv")

if not per_year_file.exists() or not summary_file.exists():
    print("❌ 결과 파일이 없습니다.")
    print(f"   - {per_year_file}")
    print(f"   - {summary_file}")
    sys.exit(1)

# 데이터 로드
df_summary = pd.read_csv(summary_file)
df_per_year = pd.read_csv(per_year_file)

print("=" * 90)
print("【2500m³ vs 5000m³ 셔틀 비용 분석 (Case 1)】")
print("="* 90)

# 각 크기별 최적 펌프 크기 찾기 (최소 NPC)
row_2500 = df_summary[df_summary['Shuttle_Size_cbm'] == 2500].nsmallest(1, 'NPC_Total_USDm').iloc[0]
row_5000 = df_summary[df_summary['Shuttle_Size_cbm'] == 5000].nsmallest(1, 'NPC_Total_USDm').iloc[0]

pump_2500 = int(row_2500['Pump_Size_m3ph'])
pump_5000 = int(row_5000['Pump_Size_m3ph'])

print(f"\n【MILP 최적화 결과 (20년 NPV)】")
print("-" * 90)
print(f"\n2500m³ + {pump_2500} m³/h:")
print(f"  NPC Total:     ${row_2500['NPC_Total_USDm']:.2f}M")
print(f"  Shuttle CAPEX: ${row_2500['NPC_Shuttle_CAPEX_USDm']:.2f}M")
print(f"  Pump CAPEX:    ${row_2500['NPC_Bunkering_CAPEX_USDm']:.2f}M")
print(f"  Tank CAPEX:    ${row_2500['NPC_Terminal_CAPEX_USDm']:.2f}M")
print(f"  Total CAPEX:   ${row_2500['NPC_Shuttle_CAPEX_USDm'] + row_2500['NPC_Bunkering_CAPEX_USDm'] + row_2500['NPC_Terminal_CAPEX_USDm']:.2f}M")

print(f"\n5000m³ + {pump_5000} m³/h:")
print(f"  NPC Total:     ${row_5000['NPC_Total_USDm']:.2f}M")
print(f"  Shuttle CAPEX: ${row_5000['NPC_Shuttle_CAPEX_USDm']:.2f}M")
print(f"  Pump CAPEX:    ${row_5000['NPC_Bunkering_CAPEX_USDm']:.2f}M")
print(f"  Tank CAPEX:    ${row_5000['NPC_Terminal_CAPEX_USDm']:.2f}M")
print(f"  Total CAPEX:   ${row_5000['NPC_Shuttle_CAPEX_USDm'] + row_5000['NPC_Bunkering_CAPEX_USDm'] + row_5000['NPC_Terminal_CAPEX_USDm']:.2f}M")

npc_diff = row_2500['NPC_Total_USDm'] - row_5000['NPC_Total_USDm']
percent_diff = (row_5000['NPC_Total_USDm'] - row_2500['NPC_Total_USDm']) / row_5000['NPC_Total_USDm'] * 100

print(f"\n차이: ${abs(npc_diff):.2f}M ({percent_diff:+.1f}%)")
if npc_diff < 0:
    print(f"✅ 2500m³이 {abs(npc_diff):.2f}M ({abs(percent_diff):.1f}%) 더 저렴")
else:
    print(f"✅ 5000m³이 {abs(npc_diff):.2f}M ({abs(percent_diff):.1f}%) 더 저렴")

# ===== 연도별 데이터 필터링 =====
df_2500 = df_per_year[(df_per_year['Shuttle_Size_cbm'] == 2500) &
                       (df_per_year['Pump_Size_m3ph'] == pump_2500)].copy()
df_5000 = df_per_year[(df_per_year['Shuttle_Size_cbm'] == 5000) &
                       (df_per_year['Pump_Size_m3ph'] == pump_5000)].copy()

if len(df_2500) == 0 or len(df_5000) == 0:
    print("\n❌ 연도별 데이터를 찾을 수 없습니다.")
    print(f"   2500m³ 행 수: {len(df_2500)}")
    print(f"   5000m³ 행 수: {len(df_5000)}")
    sys.exit(1)

# 누적 현재가 계산
df_2500['Cumulative_PV'] = df_2500['Total_Year_Cost_Discounted_USDm'].cumsum()
df_5000['Cumulative_PV'] = df_5000['Total_Year_Cost_Discounted_USDm'].cumsum()

# 합계 OPEX
df_2500['Total_OPEX'] = df_2500['FixedOPEX_Total_USDm'] + df_2500['VariableOPEX_Total_USDm']
df_5000['Total_OPEX'] = df_5000['FixedOPEX_Total_USDm'] + df_5000['VariableOPEX_Total_USDm']

print(f"\n【연도별 비용 데이터 (첫 5년)】")
print("-" * 90)
print(f"\n2500m³ + {pump_2500} m³/h:")
print(df_2500[['Year', 'New_Shuttles', 'Total_Shuttles', 'Annual_Calls',
               'CAPEX_Total_USDm', 'Total_OPEX', 'Total_Year_Cost_Discounted_USDm',
               'Cumulative_PV']].head(5).to_string(index=False))

print(f"\n5000m³ + {pump_5000} m³/h:")
print(df_5000[['Year', 'New_Shuttles', 'Total_Shuttles', 'Annual_Calls',
               'CAPEX_Total_USDm', 'Total_OPEX', 'Total_Year_Cost_Discounted_USDm',
               'Cumulative_PV']].head(5).to_string(index=False))

# ===== 시각화 =====
fig, axes = plt.subplots(2, 2, figsize=(15, 11))
fig.suptitle('2500m³ vs 5000m³ 셔틀 비용 분석 (Case 1)\n20년 최적화 vs 2030년 단기 최적화',
             fontsize=14, fontweight='bold')

# 1. 누적 현재가 (가장 중요한 지표)
ax = axes[0, 0]
ax.plot(df_2500['Year'], df_2500['Cumulative_PV'], 'o-', label='2500m³',
        linewidth=2.5, markersize=6, color='#1f77b4')
ax.plot(df_5000['Year'], df_5000['Cumulative_PV'], 's-', label='5000m³',
        linewidth=2.5, markersize=6, color='#ff7f0e')
ax.axhline(y=df_2500['Cumulative_PV'].iloc[0], color='#1f77b4', linestyle=':',
           alpha=0.5, label='2500m³ (2030년)')
ax.axhline(y=df_5000['Cumulative_PV'].iloc[0], color='#ff7f0e', linestyle=':',
           alpha=0.5, label='5000m³ (2030년)')
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Cumulative PV ($M)', fontsize=11)
ax.set_title('누적 현재가 (Cumulative Present Value)\n↓ 낮을수록 좋음',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(2029.5, 2050.5)

# 2. 연간 CAPEX 비교
ax = axes[0, 1]
years = df_2500['Year'].values
x = np.arange(len(years))
width = 0.35
ax.bar(x - width/2, df_2500['CAPEX_Total_USDm'], width, label='2500m³',
       alpha=0.8, color='#1f77b4')
ax.bar(x + width/2, df_5000['CAPEX_Total_USDm'], width, label='5000m³',
       alpha=0.8, color='#ff7f0e')
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Annual CAPEX ($M)', fontsize=11)
ax.set_title('연간 자본비 (CAPEX)\n초기에 5000m³이 더 높음',
             fontsize=12, fontweight='bold')
ax.set_xticks(x[::3])
ax.set_xticklabels(years[::3].astype(int))
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

# 3. 누적 셔틀 수 (핵심 차이점)
ax = axes[1, 0]
ax.plot(df_2500['Year'], df_2500['Total_Shuttles'], 'o-', label='2500m³',
        linewidth=2.5, markersize=6, color='#1f77b4')
ax.plot(df_5000['Year'], df_5000['Total_Shuttles'], 's-', label='5000m³',
        linewidth=2.5, markersize=6, color='#ff7f0e')
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Total Shuttles (count)', fontsize=11)
ax.set_title('누적 셔틀 수\n2500m³은 더 많은 셔틀 필요 (장기 OPEX 증가)',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(2029.5, 2050.5)

# 4. 2030년 vs 2050년 누적 비용
ax = axes[1, 1]
cost_2030_2500 = df_2500['Total_Year_Cost_Discounted_USDm'].iloc[0]
cost_2050_2500 = df_2500['Cumulative_PV'].iloc[-1]
cost_2030_5000 = df_5000['Total_Year_Cost_Discounted_USDm'].iloc[0]
cost_2050_5000 = df_5000['Cumulative_PV'].iloc[-1]

scenarios = ['2030년\n(첫 해)', '2050년까지\n누적']
cost_2500_vals = [cost_2030_2500, cost_2050_2500]
cost_5000_vals = [cost_2030_5000, cost_2050_5000]

x = np.arange(len(scenarios))
width = 0.35
bars1 = ax.bar(x - width/2, cost_2500_vals, width, label='2500m³',
               alpha=0.8, color='#1f77b4')
bars2 = ax.bar(x + width/2, cost_5000_vals, width, label='5000m³',
               alpha=0.8, color='#ff7f0e')

ax.set_ylabel('Cost ($M)', fontsize=11)
ax.set_title('2030년 vs 누적 (2050년)\n시간 관점에 따른 최적해 변화',
             fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

# 값 표시
for i, (c1, c2) in enumerate(zip(cost_2500_vals, cost_5000_vals)):
    ax.text(i - width/2, c1 + 5, f'${c1:.1f}M', ha='center', va='bottom',
            fontsize=9, fontweight='bold')
    ax.text(i + width/2, c2 + 5, f'${c2:.1f}M', ha='center', va='bottom',
            fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('results/cost_comparison_2500_vs_5000.png', dpi=300, bbox_inches='tight')
print(f"\n✅ 그래프 저장: results/cost_comparison_2500_vs_5000.png")

# ===== 자세한 분석 =====
print(f"\n" + "=" * 90)
print("【상세 비용 비교 분석】")
print("=" * 90)

print(f"\n【1단계: 2030년 (첫 해 관점)】")
print("-" * 90)
cost_2030_2500 = df_2500['Total_Year_Cost_Discounted_USDm'].iloc[0]
cost_2030_5000 = df_5000['Total_Year_Cost_Discounted_USDm'].iloc[0]
capex_2030_2500 = df_2500['CAPEX_Total_USDm'].iloc[0]
capex_2030_5000 = df_5000['CAPEX_Total_USDm'].iloc[0]

print(f"2500m³ 비용: ${cost_2030_2500:.2f}M")
print(f"  - CAPEX: ${capex_2030_2500:.2f}M (초기 셔틀 구매)")
print(f"  - OPEX: ${cost_2030_2500 - capex_2030_2500:.2f}M")

print(f"\n5000m³ 비용: ${cost_2030_5000:.2f}M")
print(f"  - CAPEX: ${capex_2030_5000:.2f}M (초기 셔틀 구매, 더 비쌈)")
print(f"  - OPEX: ${cost_2030_5000 - capex_2030_5000:.2f}M")

print(f"\n→ 2030년만 보면: 2500m³이 ${cost_2030_2500 - cost_2030_5000:+.2f}M 더 {'저렴' if cost_2030_2500 < cost_2030_5000 else '비쌈'}")
print(f"  (5000m³의 초기 CAPEX가 높아서 단기에는 비효율적으로 보임)")

print(f"\n【2단계: 누적 효과 (20년 관점)】")
print("-" * 90)
cum_2500_final = df_2500['Cumulative_PV'].iloc[-1]
cum_5000_final = df_5000['Cumulative_PV'].iloc[-1]
shuttles_2500_final = df_2500['Total_Shuttles'].iloc[-1]
shuttles_5000_final = df_5000['Total_Shuttles'].iloc[-1]

print(f"누적 비용 (2030-2050):")
print(f"  2500m³: ${cum_2500_final:.2f}M")
print(f"  5000m³: ${cum_5000_final:.2f}M")
print(f"  차이: ${cum_2500_final - cum_5000_final:+.2f}M")

print(f"\n필요한 셔틀 수:")
print(f"  2500m³: {shuttles_2500_final:.0f}척")
print(f"  5000m³: {shuttles_5000_final:.0f}척")

print(f"\n→ 20년 누적: 2500m³이 {'더 저렴' if cum_2500_final < cum_5000_final else '더 비쌈'}")
print(f"  원인:")
print(f"    1. 2500m³은 더 많은 셔틀 필요 (총 {shuttles_2500_final:.0f}척)")
print(f"    2. 추가 셔틀의 CAPEX와 OPEX가 누적됨")
print(f"    3. 5000m³은 초기 비용 높지만, 필요한 셔틀이 적어서 누적 효과가 작음")

print(f"\n【3단계: 전환점 분석】")
print("-" * 90)
# 누적 비용이 같아지는 해 찾기
cum_diff = df_2500['Cumulative_PV'] - df_5000['Cumulative_PV']
if (cum_diff > 0).any() and (cum_diff < 0).any():
    crossover_idx = np.where(cum_diff >= 0)[0][0] if np.any(cum_diff >= 0) else -1
    if crossover_idx > 0:
        crossover_year = df_2500['Year'].iloc[crossover_idx]
        print(f"전환점: {crossover_year:.0f}년 경")
        print(f"  - 이전: 5000m³이 누적 비용이 낮음 (초기 구매 효율)")
        print(f"  - 이후: 2500m³이 누적 비용이 낮음 (추가 셔틀 누적 효과)")
else:
    print(f"전환점: 없음 (5000m³이 전 기간 더 저렴 또는 2500m³이 전 기간 더 저렴)")

print(f"\n【결론: 왜 최적해가 다른가?】")
print("=" * 90)
print(f"""
✅ 2030년 단기 최적화:
   - 초기 CAPEX가 지배적
   - 5000m³의 높은 초기 구매가 비효율적으로 보임
   - 결과: 5000m³이 조금 더 저렴해 보일 수 있음 (초기 해석)

✅ 20년 장기 최적화:
   - 누적 CAPEX + OPEX가 중요
   - 2500m³ × 많은 수량 → 누적 CAPEX 증가
   - 더 많은 셔틀 운영 → 누적 OPEX 증가
   - 결과: 2500m³이 최종적으로 약간 더 효율적 (${cum_2500_final:.2f}M vs ${cum_5000_final:.2f}M)

🔑 핵심 차이점:
   1. 시간 관점의 차이
      - 단기: 초기 투자 효율 중시
      - 장기: 누적 효과와 규모의 경제 고려

   2. 선택 효과
      - 2500m³: 작은 셔틀 많이 필요 (운영 복잡도↑, OPEX↑)
      - 5000m³: 큰 셔틀 적게 필요 (운영 단순↑, OPEX↓)

⚠️ 주의:
   - 두 방식의 차이는 {abs(cum_2500_final - cum_5000_final):.2f}M로 매우 작음
   - 실무에서는 다른 요소 (운영 인력, 기술 성숙도, 위험도) 고려 필요
""")

plt.show()
