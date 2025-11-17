#!/usr/bin/env python3
"""
분석 및 시각화 스크립트
최적화 결과를 분석하고 보고서/발표 자료용 그래프 생성
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap

# 한글 폰트 설정
rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# 결과 파일 경로
results_dir = Path("results")
figures_dir = Path("results/figures")
figures_dir.mkdir(exist_ok=True)

# 케이스별 데이터 로드
cases = {
    'case_1': '부산항 저장소 기반',
    'case_2_yeosu': '여수 → 부산',
    'case_2_ulsan': '울산 → 부산'
}

# 데이터 로드 및 최적해 추출
results_summary = {}
for case_id, case_name in cases.items():
    df = pd.read_csv(results_dir / f"MILP_scenario_summary_{case_id}.csv")
    best_idx = df['NPC_Total_USDm'].idxmin()
    best = df.loc[best_idx]
    results_summary[case_id] = {
        'name': case_name,
        'df': df,
        'best_shuttle': int(best['Shuttle_Size_cbm']),
        'best_pump': int(best['Pump_Size_m3ph']),
        'best_npc': best['NPC_Total_USDm'],
        'best_row': best
    }

print("=" * 80)
print("최적화 결과 분석")
print("=" * 80)

for case_id, data in results_summary.items():
    print(f"\n{data['name']}:")
    print(f"  최적 셔틀 크기: {data['best_shuttle']} m³")
    print(f"  최적 펌프 유량: {data['best_pump']} m³/h")
    print(f"  최소 NPC: ${data['best_npc']:.2f}M USD")

# ============================================================================
# Figure 1: 각 케이스별 NPC 히트맵
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('NPC (Million USD) - Shuttle Size vs Pump Flow Rate', fontsize=16, fontweight='bold')

for idx, (case_id, data) in enumerate(results_summary.items()):
    df = data['df']

    # 피벗 테이블 생성
    pivot_data = df.pivot_table(
        values='NPC_Total_USDm',
        index='Pump_Size_m3ph',
        columns='Shuttle_Size_cbm'
    )

    # 히트맵
    im = axes[idx].imshow(
        pivot_data.values,
        cmap='RdYlGn_r',
        aspect='auto',
        origin='lower'
    )

    # 축 설정
    axes[idx].set_xticks(np.arange(len(pivot_data.columns)))
    axes[idx].set_yticks(np.arange(len(pivot_data.index)))
    axes[idx].set_xticklabels(pivot_data.columns, rotation=45)
    axes[idx].set_yticklabels(pivot_data.index)

    # 컬러바
    cbar = plt.colorbar(im, ax=axes[idx])
    cbar.set_label('NPC (M USD)', fontweight='bold')

    # 최적점 표시
    best_shuttle = data['best_shuttle']
    best_pump = data['best_pump']

    # 최적점의 인덱스 찾기
    if best_shuttle in pivot_data.columns and best_pump in pivot_data.index:
        x_idx = list(pivot_data.columns).index(best_shuttle)
        y_idx = list(pivot_data.index).index(best_pump)
        axes[idx].scatter(
            [x_idx],
            [y_idx],
            marker='*',
            s=800,
            color='red',
            edgecolor='black',
            linewidth=2,
            label=f'Optimal\n({best_shuttle}m³, {best_pump}m³/h)',
            zorder=5
        )

    axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('Shuttle Size (m³)')
    axes[idx].set_ylabel('Pump Flow Rate (m³/h)')
    axes[idx].legend(loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig(figures_dir / '01_npc_heatmaps.png', dpi=300, bbox_inches='tight')
print("\n[Figure 1] NPC Heatmaps saved")
plt.close()

# ============================================================================
# Figure 2: Top 10 시나리오 비용 Breakdown (각 케이스)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Top 10 Scenarios - Cost Breakdown (Million USD)', fontsize=16, fontweight='bold')

for idx, (case_id, data) in enumerate(results_summary.items()):
    df = data['df'].nsmallest(10, 'NPC_Total_USDm')

    # 시나리오 이름
    scenarios = [f"S{i+1}" for i in range(len(df))]

    # 비용 요소
    capex_shuttle = df['NPC_Shuttle_CAPEX_USDm'].values
    capex_bunk = df['NPC_Bunkering_CAPEX_USDm'].values
    capex_tank = df['NPC_Terminal_CAPEX_USDm'].values
    opex_shuttle = df['NPC_Shuttle_fOPEX_USDm'].values + df['NPC_Shuttle_vOPEX_USDm'].values
    opex_bunk = df['NPC_Bunkering_fOPEX_USDm'].values + df['NPC_Bunkering_vOPEX_USDm'].values
    opex_tank = df['NPC_Terminal_fOPEX_USDm'].values + df['NPC_Terminal_vOPEX_USDm'].values

    x = np.arange(len(scenarios))
    width = 0.6

    axes[idx].bar(x, capex_shuttle, width, label='Shuttle CAPEX', color='#1f77b4')
    axes[idx].bar(x, capex_bunk, width, bottom=capex_shuttle, label='Bunkering CAPEX', color='#ff7f0e')
    axes[idx].bar(x, capex_tank, width, bottom=capex_shuttle+capex_bunk, label='Tank CAPEX', color='#2ca02c')
    axes[idx].bar(x, opex_shuttle, width,
                 bottom=capex_shuttle+capex_bunk+capex_tank, label='Shuttle OPEX', color='#d62728')
    axes[idx].bar(x, opex_bunk, width,
                 bottom=capex_shuttle+capex_bunk+capex_tank+opex_shuttle,
                 label='Bunkering OPEX', color='#9467bd')
    axes[idx].bar(x, opex_tank, width,
                 bottom=capex_shuttle+capex_bunk+capex_tank+opex_shuttle+opex_bunk,
                 label='Tank OPEX', color='#8c564b')

    axes[idx].set_xticks(x)
    axes[idx].set_xticklabels(scenarios, fontsize=9)
    axes[idx].set_ylabel('Cost (M USD)')
    axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
    axes[idx].legend(fontsize=8, loc='upper left')
    axes[idx].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / '02_top10_breakdown.png', dpi=300, bbox_inches='tight')
print("[Figure 2] Top 10 Cost Breakdown saved")
plt.close()

# ============================================================================
# Figure 3: 3개 케이스 최적해 비교
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Optimal Solutions - Case Comparison', fontsize=16, fontweight='bold')

# 3-1: 최적 NPC 비교
cases_list = list(results_summary.keys())
optimal_npcs = [results_summary[c]['best_npc'] for c in cases_list]
case_names = [results_summary[c]['name'] for c in cases_list]

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
axes[0, 0].bar(case_names, optimal_npcs, color=colors, edgecolor='black', linewidth=1.5)
axes[0, 0].set_ylabel('NPC (M USD)', fontweight='bold')
axes[0, 0].set_title('Minimum NPC per Case', fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)
for i, v in enumerate(optimal_npcs):
    axes[0, 0].text(i, v + 3, f'${v:.1f}M', ha='center', fontweight='bold')

# 3-2: 최적 셔틀 크기 비교
optimal_shuttles = [results_summary[c]['best_shuttle'] for c in cases_list]
axes[0, 1].bar(case_names, optimal_shuttles, color=colors, edgecolor='black', linewidth=1.5)
axes[0, 1].set_ylabel('Shuttle Size (m³)', fontweight='bold')
axes[0, 1].set_title('Optimal Shuttle Size per Case', fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)
for i, v in enumerate(optimal_shuttles):
    axes[0, 1].text(i, v + 100, f'{v}m³', ha='center', fontweight='bold')

# 3-3: 최적 펌프 유량 비교
optimal_pumps = [results_summary[c]['best_pump'] for c in cases_list]
axes[1, 0].bar(case_names, optimal_pumps, color=colors, edgecolor='black', linewidth=1.5)
axes[1, 0].set_ylabel('Pump Flow Rate (m³/h)', fontweight='bold')
axes[1, 0].set_title('Optimal Pump Flow Rate per Case', fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)
for i, v in enumerate(optimal_pumps):
    axes[1, 0].text(i, v + 50, f'{v}', ha='center', fontweight='bold')

# 3-4: 비용 구조 비교 (최적해 기준)
cost_components = {
    'Shuttle\nCAPEX': [],
    'Bunkering\nCAPEX': [],
    'Tank\nCAPEX': [],
    'Total\nOPEX': []
}

for case_id in cases_list:
    best = results_summary[case_id]['best_row']
    cost_components['Shuttle\nCAPEX'].append(best['NPC_Shuttle_CAPEX_USDm'])
    cost_components['Bunkering\nCAPEX'].append(best['NPC_Bunkering_CAPEX_USDm'])
    cost_components['Tank\nCAPEX'].append(best['NPC_Terminal_CAPEX_USDm'])
    total_opex = (best['NPC_Shuttle_fOPEX_USDm'] + best['NPC_Shuttle_vOPEX_USDm'] +
                  best['NPC_Bunkering_fOPEX_USDm'] + best['NPC_Bunkering_vOPEX_USDm'] +
                  best['NPC_Terminal_fOPEX_USDm'] + best['NPC_Terminal_vOPEX_USDm'])
    cost_components['Total\nOPEX'].append(total_opex)

x = np.arange(len(case_names))
width = 0.2
for i, (comp, values) in enumerate(cost_components.items()):
    axes[1, 1].bar(x + i*width, values, width, label=comp, edgecolor='black', linewidth=0.5)

axes[1, 1].set_ylabel('Cost (M USD)', fontweight='bold')
axes[1, 1].set_title('Cost Structure - Optimal Solutions', fontweight='bold')
axes[1, 1].set_xticks(x + 1.5*width)
axes[1, 1].set_xticklabels(['Case 1', 'Case 2-1', 'Case 2-2'], fontsize=10)
axes[1, 1].legend(fontsize=9, loc='upper left')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / '03_case_comparison.png', dpi=300, bbox_inches='tight')
print("[Figure 3] Case Comparison saved")
plt.close()

# ============================================================================
# Figure 4: 비용 분포 (각 케이스별)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('NPC Distribution by Shuttle/Pump Configuration', fontsize=16, fontweight='bold')

for idx, (case_id, data) in enumerate(results_summary.items()):
    df = data['df']

    axes[idx].hist(df['NPC_Total_USDm'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    axes[idx].axvline(data['best_npc'], color='red', linestyle='--', linewidth=2, label=f'Optimal: ${data["best_npc"]:.1f}M')
    axes[idx].axvline(df['NPC_Total_USDm'].mean(), color='green', linestyle='--', linewidth=2, label=f'Mean: ${df["NPC_Total_USDm"].mean():.1f}M')

    axes[idx].set_xlabel('NPC (M USD)')
    axes[idx].set_ylabel('Frequency')
    axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
    axes[idx].legend()
    axes[idx].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / '04_npc_distribution.png', dpi=300, bbox_inches='tight')
print("[Figure 4] NPC Distribution saved")
plt.close()

# ============================================================================
# Figure 5: 민감도 분석 - 셔틀 크기의 영향
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Sensitivity Analysis - Impact of Shuttle Size (Best Pump per Shuttle)', fontsize=14, fontweight='bold')

for idx, (case_id, data) in enumerate(results_summary.items()):
    df = data['df']

    # 셔틀 크기별 최적 펌프의 NPC
    grouped = df.groupby('Shuttle_Size_cbm')['NPC_Total_USDm'].min()

    axes[idx].plot(grouped.index, grouped.values, marker='o', linewidth=2, markersize=8, color='#1f77b4')
    axes[idx].scatter([data['best_shuttle']], [data['best_npc']],
                     marker='*', s=500, color='red', edgecolor='black', linewidth=2, label='Optimal')

    axes[idx].set_xlabel('Shuttle Size (m³)', fontweight='bold')
    axes[idx].set_ylabel('Min NPC (M USD)', fontweight='bold')
    axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].legend()

plt.tight_layout()
plt.savefig(figures_dir / '05_shuttle_sensitivity.png', dpi=300, bbox_inches='tight')
print("[Figure 5] Sensitivity Analysis - Shuttle Size saved")
plt.close()

# ============================================================================
# 통계 정보 출력
# ============================================================================
print("\n" + "=" * 80)
print("상세 통계 정보")
print("=" * 80)

for case_id, data in results_summary.items():
    df = data['df']
    print(f"\n{data['name']}:")
    print(f"  총 타당한 솔루션: {len(df)}")
    print(f"  NPC 범위: ${df['NPC_Total_USDm'].min():.2f}M ~ ${df['NPC_Total_USDm'].max():.2f}M")
    print(f"  평균 NPC: ${df['NPC_Total_USDm'].mean():.2f}M")
    print(f"  표준편차: ${df['NPC_Total_USDm'].std():.2f}M")

print("\n" + "=" * 80)
print("모든 그래프 생성 완료!")
print("=" * 80)
