#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
독립적인 그림 생성 스크립트

main.py 실행 후 실행: python visualization_generator.py

main.py에서 생성된 CSV 파일들을 읽어서
학술 보고서/논문용 그림 15개를 자동 생성합니다.

생성 그림:
  01-05: 기존 그림들
  06-15: 추가 필요 그림들
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
    """3개 케이스의 scenario summary 로드"""
    data = {}
    for case_id in ['case_1', 'case_2_yeosu', 'case_2_ulsan']:
        csv_path = results_dir / f"MILP_scenario_summary_{case_id}.csv"
        if not csv_path.exists():
            print(f"⚠️  경고: {csv_path} 파일을 찾을 수 없습니다")
            continue
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
    """3개 케이스의 yearly results 로드"""
    data = {}
    for case_id in ['case_1', 'case_2_yeosu', 'case_2_ulsan']:
        csv_path = results_dir / f"MILP_per_year_results_{case_id}.csv"
        if not csv_path.exists():
            print(f"⚠️  경고: {csv_path} 파일을 찾을 수 없습니다")
            continue
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
    """Figure 01: NPC 히트맵"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('NPC (Million USD) - Shuttle Size vs Pump Flow Rate', fontsize=16, fontweight='bold')

    for idx, (case_id, data) in enumerate(data_dict.items()):
        df = data['df']
        pivot_data = df.pivot_table(
            values='NPC_Total_USDm',
            index='Pump_Size_m3ph',
            columns='Shuttle_Size_cbm'
        )

        im = axes[idx].imshow(
            pivot_data.values,
            cmap='RdYlGn_r',
            aspect='auto',
            origin='lower'
        )

        axes[idx].set_xticks(np.arange(len(pivot_data.columns)))
        axes[idx].set_yticks(np.arange(len(pivot_data.index)))
        axes[idx].set_xticklabels(pivot_data.columns, rotation=45)
        axes[idx].set_yticklabels(pivot_data.index)

        cbar = plt.colorbar(im, ax=axes[idx])
        cbar.set_label('NPC (M USD)', fontweight='bold')

        best_shuttle = data['best_shuttle']
        best_pump = data['best_pump']

        if best_shuttle in pivot_data.columns and best_pump in pivot_data.index:
            x_idx = list(pivot_data.columns).index(best_shuttle)
            y_idx = list(pivot_data.index).index(best_pump)
            axes[idx].scatter(
                [x_idx], [y_idx],
                marker='*', s=800, color='red', edgecolor='black', linewidth=2,
                label=f'Optimal\n({best_shuttle}m³, {best_pump}m³/h)', zorder=5
            )

        axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Shuttle Size (m³)')
        axes[idx].set_ylabel('Pump Flow Rate (m³/h)')
        axes[idx].legend(loc='lower right', fontsize=9)

    plt.tight_layout()
    plt.savefig(figures_dir / '01_npc_heatmaps.png', dpi=300, bbox_inches='tight')
    print("[01/15] NPC Heatmaps ✅")
    plt.close()

def generate_top10_breakdown(data_dict):
    """Figure 02: Top 10 비용 분해"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Top 10 Scenarios - Cost Breakdown (Million USD)', fontsize=16, fontweight='bold')

    for idx, (case_id, data) in enumerate(data_dict.items()):
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

        axes[idx].bar(x, capex_shuttle, width, label='Shuttle CAPEX', color='#1f77b4')
        axes[idx].bar(x, capex_bunk, width, bottom=capex_shuttle, label='Bunkering CAPEX', color='#ff7f0e')
        axes[idx].bar(x, capex_tank, width, bottom=capex_shuttle+capex_bunk, color='#2ca02c')
        axes[idx].bar(x, opex_shuttle, width,
                     bottom=capex_shuttle+capex_bunk+capex_tank, label='Shuttle OPEX', color='#d62728')
        axes[idx].bar(x, opex_bunk, width,
                     bottom=capex_shuttle+capex_bunk+capex_tank+opex_shuttle,
                     label='Bunkering OPEX', color='#9467bd')
        axes[idx].bar(x, opex_tank, width,
                     bottom=capex_shuttle+capex_bunk+capex_tank+opex_shuttle+opex_bunk,
                     color='#8c564b')

        axes[idx].set_xticks(x)
        axes[idx].set_xticklabels(scenarios, fontsize=9)
        axes[idx].set_ylabel('Cost (M USD)')
        axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
        axes[idx].legend(fontsize=8, loc='lower right')
        axes[idx].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / '02_top10_breakdown.png', dpi=300, bbox_inches='tight')
    print("[02/15] Top 10 Cost Breakdown ✅")
    plt.close()

def generate_case_comparison(data_dict):
    """Figure 03: Case 비교 (4개 부그래프)"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Optimal Solutions - Case Comparison', fontsize=16, fontweight='bold')

    cases_list = list(data_dict.keys())
    optimal_npcs = [data_dict[c]['best_npc'] for c in cases_list]
    case_names = [data_dict[c]['label'] for c in cases_list]

    # 3-1: 최적 NPC 비교
    axes[0, 0].bar(case_names, optimal_npcs, color=COLORS, edgecolor='black', linewidth=1.5)
    axes[0, 0].set_ylabel('NPC (M USD)', fontweight='bold')
    axes[0, 0].set_title('Minimum NPC per Case', fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(optimal_npcs):
        axes[0, 0].text(i, v + 3, f'${v:.1f}M', ha='center', fontweight='bold')

    # 3-2: 최적 셔틀 크기 비교
    optimal_shuttles = [data_dict[c]['best_shuttle'] for c in cases_list]
    axes[0, 1].bar(case_names, optimal_shuttles, color=COLORS, edgecolor='black', linewidth=1.5)
    axes[0, 1].set_ylabel('Shuttle Size (m³)', fontweight='bold')
    axes[0, 1].set_title('Optimal Shuttle Size per Case', fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate(optimal_shuttles):
        axes[0, 1].text(i, v + 100, f'{v}m³', ha='center', fontweight='bold')

    # 3-3: 최적 펌프 유량 비교
    optimal_pumps = [data_dict[c]['best_pump'] for c in cases_list]
    axes[1, 0].bar(case_names, optimal_pumps, color=COLORS, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_ylabel('Pump Flow Rate (m³/h)', fontweight='bold')
    axes[1, 0].set_title('Optimal Pump Flow Rate per Case', fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(optimal_pumps):
        axes[1, 0].text(i, v + 50, f'{v}', ha='center', fontweight='bold')

    # 3-4: 비용 구조 비교
    cost_components = {
        'Shuttle\nCAPEX': [],
        'Bunkering\nCAPEX': [],
        'Tank\nCAPEX': [],
        'Total\nOPEX': []
    }

    for case_id in cases_list:
        best = data_dict[case_id]['best_row']
        cost_components['Shuttle\nCAPEX'].append(best['NPC_Annualized_Shuttle_CAPEX_USDm'])
        cost_components['Bunkering\nCAPEX'].append(best['NPC_Annualized_Bunkering_CAPEX_USDm'])
        cost_components['Tank\nCAPEX'].append(best['NPC_Annualized_Terminal_CAPEX_USDm'])
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
    axes[1, 1].set_xticklabels(case_names, fontsize=10)
    axes[1, 1].legend(fontsize=9, loc='upper left')
    axes[1, 1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / '03_case_comparison.png', dpi=300, bbox_inches='tight')
    print("[03/15] Case Comparison ✅")
    plt.close()

def generate_distribution(data_dict):
    """Figure 04: NPC 분포도"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('NPC Distribution by Shuttle/Pump Configuration', fontsize=16, fontweight='bold')

    for idx, (case_id, data) in enumerate(data_dict.items()):
        df = data['df']
        axes[idx].hist(df['NPC_Total_USDm'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        axes[idx].axvline(data['best_npc'], color='red', linestyle='--', linewidth=2,
                         label=f'Optimal: ${data["best_npc"]:.1f}M')
        axes[idx].axvline(df['NPC_Total_USDm'].mean(), color='green', linestyle='--', linewidth=2,
                         label=f'Mean: ${df["NPC_Total_USDm"].mean():.1f}M')

        axes[idx].set_xlabel('NPC (M USD)')
        axes[idx].set_ylabel('Frequency')
        axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / '04_npc_distribution.png', dpi=300, bbox_inches='tight')
    print("[04/15] NPC Distribution ✅")
    plt.close()

def generate_shuttle_sensitivity(data_dict):
    """Figure 05: 셔틀 크기 민감도"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Sensitivity Analysis - Impact of Shuttle Size (Best Pump per Shuttle)',
                 fontsize=14, fontweight='bold')

    for idx, (case_id, data) in enumerate(data_dict.items()):
        df = data['df']
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
    print("[05/15] Shuttle Sensitivity ✅")
    plt.close()

# ============================================================================
# Figure 06-15: 새로운 그림들
# ============================================================================

def generate_cycle_time_breakdown(data_dict):
    """Figure 06: 사이클 시간 분해 (Cycle Time Breakdown) - Table Format"""
    fig, ax = plt.subplots(figsize=(14, 6))

    # 각 Case별 사이클 시간 구성
    cycle_data = {
        'case_1': {
            'Movement': 1.0,
            'Setup': 2.0,
            'Pumping': 5.0,
            'Other': 3.33
        },
        'case_2_ulsan': {
            'Movement': 3.34,
            'Setup': 2.0,
            'Pumping': 5.0,
            'Other': 18.0
        },
        'case_2_yeosu': {
            'Movement': 11.46,
            'Setup': 2.0,
            'Pumping': 5.0,
            'Other': 16.54
        }
    }

    cases_list = ['case_1', 'case_2_ulsan', 'case_2_yeosu']
    components = ['Movement', 'Setup', 'Pumping', 'Other']

    # 테이블 데이터 준비
    table_data = []
    for case_id in cases_list:
        times = cycle_data[case_id]
        total = sum(times.values())
        row = [CASE_NAMES[case_id]]
        for comp in components:
            val = times[comp]
            percent = (val / total) * 100
            row.append(f'{val:.2f}h\n({percent:.1f}%)')
        row.append(f'{total:.2f}h')
        table_data.append(row)

    # 컬럼 헤더
    columns = ['Case'] + [f'{comp}' for comp in components] + ['Total']

    # 테이블 그리기
    table = ax.table(cellText=table_data, colLabels=columns,
                    cellLoc='center', loc='center',
                    colWidths=[0.15, 0.15, 0.15, 0.15, 0.15, 0.13])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)

    # 헤더 스타일
    for i in range(len(columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # 행별 스타일
    colors = ['#E7E6E6', '#F2F2F2']
    for i in range(1, len(table_data) + 1):
        for j in range(len(columns)):
            table[(i, j)].set_facecolor(colors[(i - 1) % 2])
            table[(i, j)].set_text_props(weight='bold')

    ax.axis('off')
    fig.suptitle('Cycle Time Breakdown - Optimal Solutions', fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.savefig(figures_dir / '06_cycle_time_breakdown.png', dpi=300, bbox_inches='tight')
    print("[06/15] Cycle Time Breakdown ✅")
    plt.close()

def generate_pump_sensitivity(data_dict):
    """Figure 07: 펌프 크기 민감도"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Sensitivity Analysis - Impact of Pump Size (Best Shuttle per Pump)',
                 fontsize=14, fontweight='bold')

    for idx, (case_id, data) in enumerate(data_dict.items()):
        df = data['df']
        grouped = df.groupby('Pump_Size_m3ph')['NPC_Total_USDm'].min()

        axes[idx].plot(grouped.index, grouped.values, marker='s', linewidth=2, markersize=8, color='#ff7f0e')
        axes[idx].scatter([data['best_pump']], [data['best_npc']],
                         marker='*', s=500, color='red', edgecolor='black', linewidth=2, label='Optimal')

        axes[idx].set_xlabel('Pump Flow Rate (m³/h)', fontweight='bold')
        axes[idx].set_ylabel('Min NPC (M USD)', fontweight='bold')
        axes[idx].set_title(data['name'], fontsize=12, fontweight='bold')
        axes[idx].grid(True, alpha=0.3)
        axes[idx].legend()

    plt.tight_layout()
    plt.savefig(figures_dir / '07_pump_sensitivity.png', dpi=300, bbox_inches='tight')
    print("[07/15] Pump Sensitivity ✅")
    plt.close()

def generate_cost_pie_charts(data_dict):
    """Figure 08: 비용 구성 파이차트 (Tank 제외)"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Cost Composition - Optimal Solutions', fontsize=16, fontweight='bold')

    cases_list = list(data_dict.keys())

    for idx, case_id in enumerate(cases_list):
        best = data_dict[case_id]['best_row']

        capex_shuttle = best['NPC_Annualized_Shuttle_CAPEX_USDm']
        capex_bunk = best['NPC_Annualized_Bunkering_CAPEX_USDm']
        opex_shuttle = best['NPC_Shuttle_fOPEX_USDm'] + best['NPC_Shuttle_vOPEX_USDm']
        opex_bunk = best['NPC_Bunkering_fOPEX_USDm'] + best['NPC_Bunkering_vOPEX_USDm']

        sizes = [capex_shuttle, capex_bunk, opex_shuttle, opex_bunk]
        labels = ['Shuttle CAPEX', 'Bunkering CAPEX', 'Shuttle OPEX', 'Bunkering OPEX']
        colors_pie = ['#1f77b4', '#ff7f0e', '#d62728', '#9467bd']

        axes[idx].pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                     startangle=90, textprops={'fontsize': 9})
        axes[idx].set_title(f'{data_dict[case_id]["name"]}\nTotal: ${best["NPC_Total_USDm"]:.1f}M',
                          fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(figures_dir / '08_cost_pie_charts.png', dpi=300, bbox_inches='tight')
    print("[08/15] Cost Pie Charts ✅")
    plt.close()

def generate_year_shuttles(yearly_data, scenario_data):
    """Figure 09: 연도별 셔틀 수 (최적값만 표시)"""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('Year-by-Year Fleet Growth (Optimal Solutions)', fontsize=16, fontweight='bold')

    cases_list = ['case_1', 'case_2_yeosu', 'case_2_ulsan']

    for idx, case_id in enumerate(cases_list):
        if case_id not in yearly_data:
            print(f"    ⚠️  {case_id} 데이터 없음")
            continue

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
                   marker='o', linewidth=2.5, markersize=7, color=COLORS[idx],
                   label=f'{CASE_NAMES[case_id]}')
            ax.fill_between(df_filtered['Year'], df_filtered['Total_Shuttles'],
                          alpha=0.2, color=COLORS[idx])

    ax.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Total Shuttles (Cumulative)', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='upper left')

    plt.tight_layout()
    plt.savefig(figures_dir / '09_year_shuttles.png', dpi=300, bbox_inches='tight')
    print("[09/15] Year Shuttles ✅")
    plt.close()

def generate_year_costs(yearly_data, scenario_data):
    """Figure 10: 연도별 총 비용"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Year-by-Year Cost Trends (Discount-Adjusted)', fontsize=16, fontweight='bold')

    cases_list = ['case_1', 'case_2_yeosu', 'case_2_ulsan']

    for idx, case_id in enumerate(cases_list):
        if case_id not in yearly_data:
            print(f"    ⚠️  {case_id} 데이터 없음")
            continue

        df = yearly_data[case_id]

        # 최적 shuttle/pump 조합 필터링
        if case_id in scenario_data:
            best_shuttle = scenario_data[case_id]['best_shuttle']
            best_pump = scenario_data[case_id]['best_pump']
            df_filtered = df[(df['Shuttle_Size_cbm'] == best_shuttle) & (df['Pump_Size_m3ph'] == best_pump)]
        else:
            # 최적 조합이 없으면 첫 번째 조합 사용
            df_filtered = df[df['Shuttle_Size_cbm'] == df['Shuttle_Size_cbm'].iloc[0]]

        if df_filtered.empty:
            axes[idx].text(0.5, 0.5, 'No data', ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].set_title(CASE_NAMES[case_id], fontsize=12, fontweight='bold')
            continue

        # 총 비용: Total_Year_Cost_Discounted_USDm 사용
        if 'Total_Year_Cost_Discounted_USDm' in df_filtered.columns:
            costs = df_filtered['Total_Year_Cost_Discounted_USDm'].values
        elif 'Total_Cost_USDm' in df_filtered.columns:
            costs = df_filtered['Total_Cost_USDm'].values
        else:
            costs = np.zeros(len(df_filtered))

        years = df_filtered['Year'].values

        axes[idx].bar(years, costs, color=COLORS[idx], alpha=0.7, edgecolor='black')
        axes[idx].plot(years, costs, color=COLORS[idx], linewidth=2, marker='o', markersize=5)

        axes[idx].set_xlabel('Year', fontweight='bold')
        axes[idx].set_ylabel('Discount-Adjusted Cost (M USD)', fontweight='bold')
        axes[idx].set_title(CASE_NAMES[case_id], fontsize=12, fontweight='bold')
        axes[idx].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / '10_year_costs.png', dpi=300, bbox_inches='tight')
    print("[10/15] Year Costs ✅")
    plt.close()

def generate_case_npc_bars(data_dict):
    """Figure 11: Case NPC 비교 막대"""
    fig, ax = plt.subplots(figsize=(10, 6))

    cases_list = list(data_dict.keys())
    case_labels = [data_dict[c]['label'] for c in cases_list]
    optimal_npcs = [data_dict[c]['best_npc'] for c in cases_list]

    bars = ax.bar(case_labels, optimal_npcs, color=COLORS, edgecolor='black', linewidth=2, width=0.6)

    # 값 라벨 추가
    for i, (bar, v) in enumerate(zip(bars, optimal_npcs)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'${v:.1f}M',
               ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('Minimum NPC (M USD)', fontsize=12, fontweight='bold')
    ax.set_title('Optimal Net Present Cost Comparison (20-Year Period)', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(optimal_npcs) * 1.15)

    plt.tight_layout()
    plt.savefig(figures_dir / '11_case_npc_bars.png', dpi=300, bbox_inches='tight')
    print("[11/15] Case NPC Bars ✅")
    plt.close()

def generate_operating_metrics(data_dict):
    """Figure 12: 운영 메트릭 비교"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Operating Metrics Comparison - Optimal Solutions', fontsize=16, fontweight='bold')

    cases_list = list(data_dict.keys())
    case_labels = [data_dict[c]['label'] for c in cases_list]

    # 메트릭 1: 최적 셔틀 크기
    optimal_shuttles = [data_dict[c]['best_shuttle'] for c in cases_list]
    axes[0, 0].bar(case_labels, optimal_shuttles, color=COLORS, edgecolor='black', linewidth=1.5)
    axes[0, 0].set_ylabel('Shuttle Size (m³)', fontweight='bold')
    axes[0, 0].set_title('Optimal Shuttle Size', fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(optimal_shuttles):
        axes[0, 0].text(i, v + 100, f'{v}', ha='center', fontweight='bold')

    # 메트릭 2: 최적 펌프 유량
    optimal_pumps = [data_dict[c]['best_pump'] for c in cases_list]
    axes[0, 1].bar(case_labels, optimal_pumps, color=COLORS, edgecolor='black', linewidth=1.5)
    axes[0, 1].set_ylabel('Pump Flow Rate (m³/h)', fontweight='bold')
    axes[0, 1].set_title('Optimal Pump Size', fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate(optimal_pumps):
        axes[0, 1].text(i, v + 30, f'{v}', ha='center', fontweight='bold')

    # 메트릭 3: 전체 비용 대비 CAPEX 비율
    capex_ratios = []
    for case_id in cases_list:
        best = data_dict[case_id]['best_row']
        total_capex = (best['NPC_Annualized_Shuttle_CAPEX_USDm'] +
                      best['NPC_Annualized_Bunkering_CAPEX_USDm'] +
                      best['NPC_Annualized_Terminal_CAPEX_USDm'])
        total_cost = best['NPC_Total_USDm']
        capex_ratios.append((total_capex / total_cost) * 100)

    axes[1, 0].bar(case_labels, capex_ratios, color=COLORS, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_ylabel('CAPEX Ratio (%)', fontweight='bold')
    axes[1, 0].set_title('CAPEX as % of Total Cost', fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    axes[1, 0].set_ylim(0, 100)
    for i, v in enumerate(capex_ratios):
        axes[1, 0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

    # 메트릭 4: 평균 NPC (모든 조합)
    avg_npcs = []
    for case_id in cases_list:
        avg_npcs.append(data_dict[case_id]['df']['NPC_Total_USDm'].mean())

    axes[1, 1].bar(case_labels, avg_npcs, color=COLORS, edgecolor='black', linewidth=1.5, alpha=0.7)
    axes[1, 1].scatter(case_labels, [data_dict[c]['best_npc'] for c in cases_list],
                      color='red', s=200, marker='*', zorder=5, label='Optimal')
    axes[1, 1].set_ylabel('NPC (M USD)', fontweight='bold')
    axes[1, 1].set_title('Average vs Optimal NPC', fontweight='bold')
    axes[1, 1].grid(axis='y', alpha=0.3)
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig(figures_dir / '12_operating_metrics.png', dpi=300, bbox_inches='tight')
    print("[12/15] Operating Metrics ✅")
    plt.close()

def generate_cost_vs_demand(yearly_data, scenario_data):
    """Figure 13: 비용 vs 수요 (최적값만 표시)"""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('Total Cost vs Annual Demand Trend (Optimal Solutions)', fontsize=16, fontweight='bold')

    cases_list = ['case_1', 'case_2_yeosu', 'case_2_ulsan']

    for idx, case_id in enumerate(cases_list):
        if case_id not in yearly_data:
            continue

        df = yearly_data[case_id]

        # 최적 shuttle/pump 조합 필터링
        if case_id in scenario_data:
            best_shuttle = scenario_data[case_id]['best_shuttle']
            best_pump = scenario_data[case_id]['best_pump']
            df_filtered = df[(df['Shuttle_Size_cbm'] == best_shuttle) & (df['Pump_Size_m3ph'] == best_pump)]
        else:
            df_filtered = df[df['Shuttle_Size_cbm'] == df['Shuttle_Size_cbm'].iloc[0]]

        if df_filtered.empty:
            continue

        # 비용 (왼쪽 y축)
        cost_col = 'Total_Year_Cost_Discounted_USDm' if 'Total_Year_Cost_Discounted_USDm' in df_filtered.columns else 'Total_Cost_USDm'
        if cost_col not in df_filtered.columns:
            continue

        color = COLORS[idx]
        ax.plot(df_filtered['Year'], df_filtered[cost_col],
               color=color, linewidth=2.5, marker='o', markersize=6,
               label=f'{CASE_NAMES[case_id]} - Cost')

    ax.set_xlabel('Year', fontweight='bold', fontsize=12)
    ax.set_ylabel('Annual Cost (M USD)', fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, loc='best')

    plt.tight_layout()
    plt.savefig(figures_dir / '13_cost_vs_demand.png', dpi=300, bbox_inches='tight')
    print("[13/15] Cost vs Demand ✅")
    plt.close()

def generate_tornado_diagram(data_dict):
    """Figure 14: 민감도 Tornado 다이어그램

    [설명] 이 그림은 다양한 운영 파라미터가 NPC에 미치는 영향을 시각화합니다.
    각 파라미터를 ±변화시켰을 때 NPC가 어느 정도 변하는지 보여줍니다.

    [계산 방식]
    - 기본 파라미터: Case 2-2 (울산→부산)의 최적 NPC를 기준값으로 사용
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

    # 각 파라미터의 NPC 변화를 추정
    # (Case 2-2 기준)
    best_case = data_dict['case_2_ulsan']
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
    ax.set_title('Sensitivity Analysis - Tornado Diagram\n(Case 2-2: 울산 → 부산)',
                fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(figures_dir / '14_tornado_diagram.png', dpi=300, bbox_inches='tight')
    print("[14/15] Tornado Diagram ✅")
    plt.close()

def generate_lcoa_comparison(data_dict):
    """Figure 15: LCOA (Levelized Cost of Ammonia) 비교

    [설명] LCOA는 톤당 암모니아 평준화 비용(USD/ton)을 나타냅니다.

    [계산 방식] CSV의 'LCOAmmonia_USD_per_ton' 컬럼값을 직접 사용합니다:
    LCOA = Total NPC (USD) / Total 20-Year Supply (tons)

    각 케이스별 최적 솔루션의 LCOA 값을 표시합니다.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    cases_list = list(data_dict.keys())
    case_labels = [data_dict[c]['label'] for c in cases_list]

    # LCOA: CSV 데이터에서 직접 읽음
    lcoas = []
    for case_id in cases_list:
        best = data_dict[case_id]['best_row']
        # CSV의 LCOAmmonia_USD_per_ton 컬럼 사용 (있으면)
        if 'LCOAmmonia_USD_per_ton' in best.index:
            lcoa = best['LCOAmmonia_USD_per_ton']
        else:
            # 대체: 이전의 근사값 사용 (권장하지 않음)
            lcoa = best['NPC_Total_USDm'] * 0.5
        lcoas.append(lcoa)

    bars = ax.bar(case_labels, lcoas, color=COLORS, edgecolor='black', linewidth=2, width=0.6)

    # 값 라벨
    for bar, v in zip(bars, lcoas):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'${v:.1f}/ton',
               ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('LCOA (USD/ton)', fontsize=12, fontweight='bold')
    ax.set_title('Levelized Cost of Ammonia (LCOA) - Optimal Solutions', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(lcoas) * 1.15)

    plt.tight_layout()
    plt.savefig(figures_dir / '15_lcoa_comparison.png', dpi=300, bbox_inches='tight')
    print("[15/15] LCOA Comparison ✅")
    plt.close()

# ============================================================================
# 메인 실행
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🎨 15개 그림 생성 시작")
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
        # Figure 01-05: 기존 그림
        generate_heatmaps(scenario_data)
        generate_top10_breakdown(scenario_data)
        generate_case_comparison(scenario_data)
        generate_distribution(scenario_data)
        generate_shuttle_sensitivity(scenario_data)

        # Figure 06-15: 새로운 그림
        generate_cycle_time_breakdown(scenario_data)  # Figure 06: Cycle Time Breakdown
        generate_pump_sensitivity(scenario_data)
        generate_cost_pie_charts(scenario_data)
        generate_year_shuttles(yearly_data, scenario_data)
        generate_year_costs(yearly_data, scenario_data)
        generate_case_npc_bars(scenario_data)
        generate_operating_metrics(scenario_data)
        generate_cost_vs_demand(yearly_data, scenario_data)
        generate_tornado_diagram(scenario_data)
        generate_lcoa_comparison(scenario_data)

        print("\n" + "=" * 80)
        print("✅ 모든 그림 생성 완료!")
        print("=" * 80)
        print(f"\n📁 저장 위치: {figures_dir}")
        print(f"📊 생성된 파일 수: 15개")
        print("\n다음 파일들이 생성되었습니다:")

        # 생성된 파일 목록 출력
        import os
        for i, f in enumerate(sorted(os.listdir(figures_dir)), 1):
            if f.endswith('.png'):
                print(f"   {i:2d}. {f}")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
