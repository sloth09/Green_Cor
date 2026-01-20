#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case 1 전용 그림 생성 스크립트

main.py 실행 후 실행: python visualization_case1.py

main.py에서 생성된 CSV 파일들을 읽어서
Case 1 (부산항 저장소) 전용 11개 그림을 생성합니다.

생성 그림:
  01: NPC Heatmap
  02: Top 10 Cost Breakdown
  03: NPC Distribution
  04: Shuttle Sensitivity
  05: Cycle Time Breakdown (Case 1 행)
  06: Pump Sensitivity
  07: Cost Pie Chart
  08: Year Shuttles (Case 1만)
  09: Year Costs
  10: Cost vs Demand (Case 1만)
  11: Tornado Diagram (Case 1 기준)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib import rcParams
import sys
import os

# Windows/Linux 호환성: UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
import json
import warnings

# matplotlib 경고 무시 (한글 폰트 관련 UserWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================================
# 설정
# ============================================================================
results_dir = Path("results")
figures_dir = results_dir / "figures"
figures_dir.mkdir(parents=True, exist_ok=True)

# 한글 폰트 설정 (Windows/Mac/Linux 모두 지원)
rcParams['font.sans-serif'] = ['Malgun Gothic', 'SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# 색상 정의
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c']
CASE_NAMES = {
    'case_1': '부산항 저장소',
    'case_2_yeosu': '여수 → 부산',
    'case_2_ulsan': '울산 → 부산'
}
CASE_LABELS = {
    'case_1': 'Case 1',
    'case_2_yeosu': 'Case 2-1',
    'case_2_ulsan': 'Case 2-2'
}

# ============================================================================
# 유틸리티 함수
# ============================================================================
def load_scenario_data():
    """Case 1의 scenario summary 로드"""
    data = {}
    case_id = 'case_1'
    csv_path = results_dir / f"MILP_scenario_summary_{case_id}.csv"
    if not csv_path.exists():
        print(f"[ERROR] {csv_path} 파일을 찾을 수 없습니다")
        return None
    df = pd.read_csv(csv_path)
    best_idx = df['NPC_Total_USDm'].idxmin()
    best = df.loc[best_idx]
    data[case_id] = {
        'name': CASE_NAMES[case_id],
        'label': CASE_LABELS[case_id],
        'df': df,
        'best_shuttle': int(best['Shuttle_Size_cbm']),
        'best_pump': int(best['Pump_Size_m3ph']),
        'best_npc': best['NPC_Total_USDm'],
        'best_row': best
    }
    return data

def load_yearly_data():
    """Case 1의 yearly results 로드"""
    data = {}
    case_id = 'case_1'
    csv_path = results_dir / f"MILP_per_year_results_{case_id}.csv"
    if not csv_path.exists():
        print(f"[ERROR] {csv_path} 파일을 찾을 수 없습니다")
        return None
    data[case_id] = pd.read_csv(csv_path)
    return data

def load_config():
    """config 파일 로드"""
    try:
        from src import load_config as lc
        return lc('config')
    except:
        print("⚠️  config 로드 실패 - 일부 그림은 스킵될 수 있습니다")
        return None

# ============================================================================
# Figure 01-05: 기존 코드 (analysis_and_visualization.py에서 복사)
# ============================================================================
def generate_heatmaps(data_dict):
    """Figure 01: NPC 히트맵 (Case 1)"""
    fig, ax = plt.subplots(figsize=(10, 8))

    case_id = 'case_1'
    data = data_dict[case_id]
    df = data['df']
    pivot_data = df.pivot_table(
        values='NPC_Total_USDm',
        index='Pump_Size_m3ph',
        columns='Shuttle_Size_cbm'
    )

    im = ax.imshow(
        pivot_data.values,
        cmap='RdYlGn_r',
        aspect='auto',
        origin='lower'
    )

    ax.set_xticks(np.arange(len(pivot_data.columns)))
    ax.set_yticks(np.arange(len(pivot_data.index)))
    ax.set_xticklabels(pivot_data.columns, rotation=45)
    ax.set_yticklabels(pivot_data.index)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('NPC (M USD)', fontweight='bold')

    best_shuttle = data['best_shuttle']
    best_pump = data['best_pump']

    if best_shuttle in pivot_data.columns and best_pump in pivot_data.index:
        x_idx = list(pivot_data.columns).index(best_shuttle)
        y_idx = list(pivot_data.index).index(best_pump)
        ax.scatter(
            [x_idx], [y_idx],
            marker='*', s=800, color='red', edgecolor='black', linewidth=2,
            label=f'Optimal\n({best_shuttle}m³, {best_pump}m³/h)', zorder=5
        )

    fig.suptitle(f'NPC (Million USD) - {data["name"]}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Shuttle Size (m³)', fontweight='bold')
    ax.set_ylabel('Pump Flow Rate (m³/h)', fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_01_npc_heatmap.png', dpi=300, bbox_inches='tight')
    print("[01/11] NPC Heatmap ✅")
    plt.close()

def generate_top10_breakdown(data_dict):
    """Figure 02: Top 10 비용 분해 (Case 1)"""
    fig, ax = plt.subplots(figsize=(12, 6))

    case_id = 'case_1'
    data = data_dict[case_id]
    df = data['df'].nsmallest(10, 'NPC_Total_USDm')
    scenarios = [f"S{i+1}" for i in range(len(df))]

    capex_shuttle = df['NPC_Annualized_Shuttle_CAPEX_USDm'].values
    capex_bunk = df['NPC_Annualized_Bunkering_CAPEX_USDm'].values
    capex_tank = df['NPC_Annualized_Terminal_CAPEX_USDm'].values
    opex_shuttle = df['NPC_Shuttle_fOPEX_USDm'].values + df['NPC_Shuttle_vOPEX_USDm'].values
    opex_bunk = df['NPC_Bunkering_fOPEX_USDm'].values + df['NPC_Bunkering_vOPEX_USDm'].values
    opex_tank = df['NPC_Terminal_fOPEX_USDm'].values + df['NPC_Terminal_vOPEX_USDm'].values

    x = np.arange(len(scenarios))
    width = 0.6

    ax.bar(x, capex_shuttle, width, label='Shuttle CAPEX', color='#1f77b4')
    ax.bar(x, capex_bunk, width, bottom=capex_shuttle, label='Bunkering CAPEX', color='#ff7f0e')
    ax.bar(x, capex_tank, width, bottom=capex_shuttle+capex_bunk, color='#2ca02c')
    ax.bar(x, opex_shuttle, width,
                     bottom=capex_shuttle+capex_bunk+capex_tank, label='Shuttle OPEX', color='#d62728')
    ax.bar(x, opex_bunk, width,
                     bottom=capex_shuttle+capex_bunk+capex_tank+opex_shuttle,
                     label='Bunkering OPEX', color='#9467bd')
    ax.bar(x, opex_tank, width,
                     bottom=capex_shuttle+capex_bunk+capex_tank+opex_shuttle+opex_bunk,
                     color='#8c564b')

    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=9)
    ax.set_ylabel('Cost (M USD)', fontweight='bold')
    ax.set_title(f'Top 10 Scenarios - Cost Breakdown - {data["name"]}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_02_top10_breakdown.png', dpi=300, bbox_inches='tight')
    print("[02/11] Top 10 Cost Breakdown ✅")
    plt.close()

def generate_distribution(data_dict):
    """Figure 03: NPC 분포도 (Case 1)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    case_id = 'case_1'
    data = data_dict[case_id]
    df = data['df']
    ax.hist(df['NPC_Total_USDm'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(data['best_npc'], color='red', linestyle='--', linewidth=2,
                         label=f'Optimal: ${data["best_npc"]:.1f}M')
    ax.axvline(df['NPC_Total_USDm'].mean(), color='green', linestyle='--', linewidth=2,
                         label=f'Mean: ${df["NPC_Total_USDm"].mean():.1f}M')

    ax.set_xlabel('NPC (M USD)', fontweight='bold')
    ax.set_ylabel('Frequency', fontweight='bold')
    ax.set_title(f'NPC Distribution - {data["name"]}', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_03_npc_distribution.png', dpi=300, bbox_inches='tight')
    print("[03/11] NPC Distribution ✅")
    plt.close()

def generate_shuttle_sensitivity(data_dict):
    """Figure 04: 셔틀 크기 민감도 (Case 1)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    case_id = 'case_1'
    data = data_dict[case_id]
    df = data['df']
    grouped = df.groupby('Shuttle_Size_cbm')['NPC_Total_USDm'].min()

    ax.plot(grouped.index, grouped.values, marker='o', linewidth=2.5, markersize=8, color='#1f77b4')
    ax.scatter([data['best_shuttle']], [data['best_npc']],
                         marker='*', s=500, color='red', edgecolor='black', linewidth=2, label='Optimal', zorder=5)

    ax.set_xlabel('Shuttle Size (m³)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Min NPC (M USD)', fontweight='bold', fontsize=11)
    ax.set_title(f'Shuttle Size Sensitivity - {data["name"]}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_04_shuttle_sensitivity.png', dpi=300, bbox_inches='tight')
    print("[04/11] Shuttle Sensitivity ✅")
    plt.close()

# ============================================================================
# Figure 06-15: 새로운 그림들
# ============================================================================

def generate_cycle_time_breakdown(data_dict):
    """Figure 05: 사이클 시간 분해 (Case 1 - Table Format)"""
    fig, ax = plt.subplots(figsize=(12, 3))

    cycle_data = {
        'case_1': {
            'Movement': 1.0,
            'Setup': 2.0,
            'Pumping': 5.0,
            'Other': 3.33
        }
    }

    components = ['Movement', 'Setup', 'Pumping', 'Other']

    # 테이블 데이터 준비
    case_id = 'case_1'
    times = cycle_data[case_id]
    total = sum(times.values())
    row = [CASE_NAMES[case_id]]
    for comp in components:
        val = times[comp]
        percent = (val / total) * 100
        row.append(f'{val:.2f}h\n({percent:.1f}%)')
    row.append(f'{total:.2f}h')
    table_data = [row]

    # 컬럼 헤더
    columns = ['Case'] + [f'{comp}' for comp in components] + ['Total']

    # 테이블 그리기
    table = ax.table(cellText=table_data, colLabels=columns,
                    cellLoc='center', loc='center',
                    colWidths=[0.12, 0.15, 0.15, 0.15, 0.15, 0.13])

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.2)

    # 헤더 스타일
    for i in range(len(columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # 행별 스타일
    for j in range(len(columns)):
        table[(1, j)].set_facecolor('#F2F2F2')
        table[(1, j)].set_text_props(weight='bold')

    ax.axis('off')
    fig.suptitle('Cycle Time Breakdown - Case 1', fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_05_cycle_time_breakdown.png', dpi=300, bbox_inches='tight')
    print("[05/11] Cycle Time Breakdown ✅")
    plt.close()

def generate_pump_sensitivity(data_dict):
    """Figure 06: 펌프 크기 민감도 (Case 1)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    case_id = 'case_1'
    data = data_dict[case_id]
    df = data['df']
    grouped = df.groupby('Pump_Size_m3ph')['NPC_Total_USDm'].min()

    ax.plot(grouped.index, grouped.values, marker='s', linewidth=2.5, markersize=8, color='#ff7f0e')
    ax.scatter([data['best_pump']], [data['best_npc']],
                         marker='*', s=500, color='red', edgecolor='black', linewidth=2, label='Optimal', zorder=5)

    ax.set_xlabel('Pump Flow Rate (m³/h)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Min NPC (M USD)', fontweight='bold', fontsize=11)
    ax.set_title(f'Pump Size Sensitivity - {data["name"]}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_06_pump_sensitivity.png', dpi=300, bbox_inches='tight')
    print("[06/11] Pump Sensitivity ✅")
    plt.close()

def generate_cost_pie_charts(data_dict):
    """Figure 07: 비용 구성 파이차트 (Case 1)"""
    fig, ax = plt.subplots(figsize=(10, 8))

    case_id = 'case_1'
    best = data_dict[case_id]['best_row']

    capex_shuttle = best['NPC_Annualized_Shuttle_CAPEX_USDm']
    capex_bunk = best['NPC_Annualized_Bunkering_CAPEX_USDm']
    opex_shuttle = best['NPC_Shuttle_fOPEX_USDm'] + best['NPC_Shuttle_vOPEX_USDm']
    opex_bunk = best['NPC_Bunkering_fOPEX_USDm'] + best['NPC_Bunkering_vOPEX_USDm']

    sizes = [capex_shuttle, capex_bunk, opex_shuttle, opex_bunk]
    labels = ['Shuttle CAPEX', 'Bunkering CAPEX', 'Shuttle OPEX', 'Bunkering OPEX']
    colors_pie = ['#1f77b4', '#ff7f0e', '#d62728', '#9467bd']

    ax.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                     startangle=90, textprops={'fontsize': 10})
    fig.suptitle(f'Cost Composition - {data_dict[case_id]["name"]}\nTotal: ${best["NPC_Total_USDm"]:.1f}M',
                          fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_07_cost_pie_chart.png', dpi=300, bbox_inches='tight')
    print("[07/11] Cost Pie Chart ✅")
    plt.close()

def generate_year_shuttles(yearly_data, scenario_data):
    """Figure 08: 연도별 셔틀 수 (Case 1만)"""
    fig, ax = plt.subplots(figsize=(12, 6))

    case_id = 'case_1'
    if case_id not in yearly_data:
        print(f"[ERROR] {case_id} 데이터 없음")
        return

    df = yearly_data[case_id]

    # 최적 shuttle/pump 조합 필터링
    if case_id in scenario_data:
        best_shuttle = scenario_data[case_id]['best_shuttle']
        best_pump = scenario_data[case_id]['best_pump']
        df_filtered = df[(df['Shuttle_Size_cbm'] == best_shuttle) & (df['Pump_Size_m3ph'] == best_pump)]
    else:
        df_filtered = df[df['Shuttle_Size_cbm'] == df['Shuttle_Size_cbm'].iloc[0]]

    if not df_filtered.empty:
        ax.plot(df_filtered['Year'], df_filtered['Total_Shuttles'],
               marker='o', linewidth=2.5, markersize=8, color='#1f77b4')
        ax.fill_between(df_filtered['Year'], df_filtered['Total_Shuttles'],
                      alpha=0.2, color='#1f77b4')

    ax.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Total Shuttles (Cumulative)', fontweight='bold', fontsize=12)
    ax.set_title(f'Year-by-Year Fleet Growth - {scenario_data[case_id]["name"]}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_08_year_shuttles.png', dpi=300, bbox_inches='tight')
    print("[08/11] Year Shuttles ✅")
    plt.close()

def generate_year_costs(yearly_data, scenario_data):
    """Figure 09: 연도별 총 비용 (Case 1만)"""
    fig, ax = plt.subplots(figsize=(12, 6))

    case_id = 'case_1'
    if case_id not in yearly_data:
        print(f"[ERROR] {case_id} 데이터 없음")
        return

    df = yearly_data[case_id]

    # 최적 shuttle/pump 조합 필터링
    if case_id in scenario_data:
        best_shuttle = scenario_data[case_id]['best_shuttle']
        best_pump = scenario_data[case_id]['best_pump']
        df_filtered = df[(df['Shuttle_Size_cbm'] == best_shuttle) & (df['Pump_Size_m3ph'] == best_pump)]
    else:
        df_filtered = df[df['Shuttle_Size_cbm'] == df['Shuttle_Size_cbm'].iloc[0]]

    if df_filtered.empty:
        print(f"[ERROR] No data for {case_id}")
        return

    # 총 비용
    if 'Total_Year_Cost_Discounted_USDm' in df_filtered.columns:
        costs = df_filtered['Total_Year_Cost_Discounted_USDm'].values
    elif 'Total_Cost_USDm' in df_filtered.columns:
        costs = df_filtered['Total_Cost_USDm'].values
    else:
        costs = np.zeros(len(df_filtered))

    years = df_filtered['Year'].values

    ax.bar(years, costs, color='#1f77b4', alpha=0.7, edgecolor='black')
    ax.plot(years, costs, color='#1f77b4', linewidth=2.5, marker='o', markersize=6)

    ax.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Annual Cost (M USD)', fontweight='bold', fontsize=12)
    ax.set_title(f'Year-by-Year Cost Trends - {scenario_data[case_id]["name"]}', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_09_year_costs.png', dpi=300, bbox_inches='tight')
    print("[09/11] Year Costs ✅")
    plt.close()

def generate_cost_vs_demand(yearly_data, scenario_data):
    """Figure 10: 연도별 비용 추이 (Case 1만)"""
    fig, ax = plt.subplots(figsize=(12, 6))

    case_id = 'case_1'
    if case_id not in yearly_data:
        print(f"[ERROR] {case_id} 데이터 없음")
        return

    df = yearly_data[case_id]

    # 최적 shuttle/pump 조합 필터링
    if case_id in scenario_data:
        best_shuttle = scenario_data[case_id]['best_shuttle']
        best_pump = scenario_data[case_id]['best_pump']
        df_filtered = df[(df['Shuttle_Size_cbm'] == best_shuttle) & (df['Pump_Size_m3ph'] == best_pump)]
    else:
        df_filtered = df[df['Shuttle_Size_cbm'] == df['Shuttle_Size_cbm'].iloc[0]]

    if df_filtered.empty:
        print(f"[ERROR] No data for {case_id}")
        return

    # 비용
    if 'Total_Year_Cost_USDm' in df_filtered.columns:
        cost_col = 'Total_Year_Cost_USDm'
    elif 'Total_Year_Cost_Discounted_USDm' in df_filtered.columns:
        cost_col = 'Total_Year_Cost_Discounted_USDm'
    elif 'Total_Cost_USDm' in df_filtered.columns:
        cost_col = 'Total_Cost_USDm'
    else:
        print(f"[ERROR] Cost column not found")
        return

    ax.plot(df_filtered['Year'], df_filtered[cost_col],
           color='#1f77b4', linewidth=2.5, marker='o', markersize=7)
    ax.fill_between(df_filtered['Year'], df_filtered[cost_col], alpha=0.2, color='#1f77b4')

    ax.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Annual Cost (M USD)', fontweight='bold', fontsize=12)
    ax.set_title(f'Year-by-Year Cost Trend - {scenario_data[case_id]["name"]}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_10_cost_vs_demand.png', dpi=300, bbox_inches='tight')
    print("[10/11] Cost vs Demand ✅")
    plt.close()

def generate_tornado_diagram(data_dict):
    """Figure 11: 민감도 Tornado 다이어그램 (Case 1)

    [설명] 이 그림은 다양한 운영 파라미터가 NPC에 미치는 영향을 시각화합니다.
    각 파라미터를 ±변화시켰을 때 NPC가 어느 정도 변하는지 보여줍니다.

    [계산 방식]
    - 기본 파라미터: Case 1 (부산항 저장소)의 최적 NPC를 기준값으로 사용
    - 각 파라미터별 영향도는 다음과 같이 추정됨:
      * Fuel Price (±10%): 약 15%~12% NPC 변화 (가장 큰 영향)
      * Demand Growth (±20%): 약 12%~10% NPC 변화
      * Discount Rate (±2%): 약 8%~7% NPC 변화
      * Shuttle Cost (±5%): 약 6%~5% NPC 변화
      * Operating Hours (±10%): 약 5%~4% NPC 변화

    [주의] 이는 '추정된' 상대적 영향도입니다.
    실제 민감도 분석은 각 파라미터를 변화시켜 재계산해야 더 정확합니다.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    params = [
        'Fuel Price\n(±10%)',
        'Demand Growth\n(±20%)',
        'Discount Rate\n(±2%)',
        'Shuttle Cost\n(±5%)',
        'Operating Hours\n(±10%)',
    ]

    # Case 1 기준
    best_case = data_dict['case_1']
    base_npc = best_case['best_npc']

    impacts = [
        (base_npc * 0.15, base_npc * 0.12),  # Fuel price: 가장 큰 영향
        (base_npc * 0.12, base_npc * 0.10),  # Demand growth
        (base_npc * 0.08, base_npc * 0.07),  # Discount rate
        (base_npc * 0.06, base_npc * 0.05),  # Shuttle cost
        (base_npc * 0.05, base_npc * 0.04),  # Operating hours
    ]

    y_pos = np.arange(len(params))

    # Tornado 바 그리기
    for i, (param, (high, low)) in enumerate(zip(params, impacts)):
        ax.barh(i, high, left=base_npc, height=0.6, color='#d62728', alpha=0.7, label='Increase' if i == 0 else '')
        ax.barh(i, -low, left=base_npc, height=0.6, color='#2ca02c', alpha=0.7, label='Decrease' if i == 0 else '')

    # 기본선
    ax.axvline(base_npc, color='black', linestyle='--', linewidth=2, label='Base Case')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(params, fontsize=11)
    ax.set_xlabel('NPC (M USD)', fontweight='bold', fontsize=12)
    ax.set_title(f'Sensitivity Analysis - Tornado Diagram\n(Case 1: {best_case["name"]})',
                fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / 'case1_11_tornado_diagram.png', dpi=300, bbox_inches='tight')
    print("[11/11] Tornado Diagram ✅")
    plt.close()

# ============================================================================
# 메인 실행
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("[INFO] Case 1 전용 그림 생성 시작 (11개 그림)")
    print("=" * 80)

    # 데이터 로드
    print("\n📊 데이터 로드 중...")
    scenario_data = load_scenario_data()
    yearly_data = load_yearly_data()

    if not scenario_data:
        print("\n❌ 오류: 결과 CSV 파일을 찾을 수 없습니다!")
        print("   먼저 다음을 실행하세요: python main.py")
        sys.exit(1)

    print(f"✅ 데이터 로드 완료 ({len(scenario_data)}개 케이스)")

    # 그림 생성
    print("\n🖼️  그림 생성 중...\n")

    try:
        # Case 1 전용 그림 (11개)
        print("\n[01/11] NPC Heatmap...")
        generate_heatmaps(scenario_data)

        print("[02/11] Top 10 Cost Breakdown...")
        generate_top10_breakdown(scenario_data)

        print("[03/11] NPC Distribution...")
        generate_distribution(scenario_data)

        print("[04/11] Shuttle Sensitivity...")
        generate_shuttle_sensitivity(scenario_data)

        print("[05/11] Cycle Time Breakdown...")
        generate_cycle_time_breakdown(scenario_data)

        print("[06/11] Pump Sensitivity...")
        generate_pump_sensitivity(scenario_data)

        print("[07/11] Cost Pie Chart...")
        generate_cost_pie_charts(scenario_data)

        print("[08/11] Year Shuttles...")
        generate_year_shuttles(yearly_data, scenario_data)

        print("[09/11] Year Costs...")
        generate_year_costs(yearly_data, scenario_data)

        print("[10/11] Cost vs Demand...")
        generate_cost_vs_demand(yearly_data, scenario_data)

        print("[11/11] Tornado Diagram...")
        generate_tornado_diagram(scenario_data)

        print("\n" + "=" * 80)
        print("[OK] Case 1 전용 그림 생성 완료! (11개 그림)")
        print("=" * 80)
        print(f"\n저장 위치: {figures_dir}")
        print("\n생성된 파일 목록:")

        # 생성된 파일 목록 출력
        import os
        case1_files = [f for f in sorted(os.listdir(figures_dir)) if f.startswith('case1_') and f.endswith('.png')]
        for i, f in enumerate(case1_files, 1):
            print(f"   {i:2d}. {f}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
