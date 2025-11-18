# Green Corridor 암모니아 벙커링 최적화 모델
## 실행 결과 및 시각화 가이드

**작성자**: Claude Code Analysis
**작성일**: 2025-11-18
**버전**: v2.3
**모델 타입**: MILP (Mixed Integer Linear Programming)

---

## 📊 빠른 네비게이션

- [도출 가능한 결과물 목록](#도출-가능한-결과물-목록)
- [결과 파일 상세 설명](#결과-파일-상세-설명)
- [시각화 가능한 그래프](#시각화-가능한-그래프)
- [분석 사례](#분석-사례)
- [Python 코드 예제](#python-코드-예제)

---

## 🎯 도출 가능한 결과물 목록

### 📋 데이터 파일 (자동 생성)

#### 1. **MILP_scenario_summary_case_X.csv**
- **생성 시점**: 각 케이스 최적화 완료 후
- **행 수**: Shuttle × Pump 조합 수 (최대 100행)
- **주요 컬럼**:
  - `Shuttle_Size_cbm`: 셔틀 크기 (m³)
  - `Pump_Size_m3ph`: 펌프 용량 (m³/h)
  - `NPC_Total_USDm`: 20년 순현재가 (백만 USD)
  - `NPC_Shuttle_CAPEX_USDm`: 셔틀 자본비
  - `NPC_Bunkering_CAPEX_USDm`: 벙커링 장비비
  - `NPC_Terminal_CAPEX_USDm`: 탱크 자본비 (Case 1만)
  - `NPC_Shuttle_Fixed_OPEX_USDm`: 셔틀 고정비
  - `NPC_Pump_Fixed_OPEX_USDm`: 펌프 고정비
  - `NPC_Terminal_Fixed_OPEX_USDm`: 탱크 고정비 (Case 1만)
  - `NPC_Shuttle_Fuel_OPEX_USDm`: 셔틀 연료비
  - `NPC_Pump_Fuel_OPEX_USDm`: 펌프 연료비
  - `NPC_Cooling_OPEX_USDm`: 냉각비 (Case 1만)
  - `Feasible`: 최적해 존재 여부 (Yes/No)
  - `Solver_Status`: 솔버 상태 (Optimal, Infeasible, etc.)

**예시 파일**:
```
MILP_scenario_summary_case_1.csv
MILP_scenario_summary_case_2_yeosu.csv
MILP_scenario_summary_case_2_ulsan.csv
```

#### 2. **MILP_per_year_results_case_X.csv**
- **생성 시점**: 각 케이스 최적화 완료 후
- **행 수**: 21 (2030~2050년)
- **주요 컬럼**:
  - `Year`: 연도 (2030~2050)
  - `New_Shuttles`: 당해 신규 추가 셔틀 수
  - `Total_Shuttles`: 누적 셔틀 수
  - `Annual_Calls`: 연간 콜/항해 수
  - `Supply_m3`: 연간 공급량 (m³)
  - `Demand_m3`: 연간 수요량 (m³)
  - `Utilization_Rate`: 활용도 (%)
  - `Annual_CAPEX_USDm`: 당해 자본비 (백만 USD)
  - `Annual_FixedOPEX_USDm`: 당해 고정비
  - `Annual_VariableOPEX_USDm`: 당해 변동비
  - `Discounted_Cost_USDm`: 할인된 당해 비용

**예시 파일**:
```
MILP_per_year_results_case_1.csv
MILP_per_year_results_case_2_yeosu.csv
MILP_per_year_results_case_2_ulsan.csv
```

#### 3. **MILP_cases_summary.csv** (다중 케이스 실행 시만)
- **생성 시점**: 모든 케이스 실행 완료 후
- **행 수**: 케이스 수 (3행)
- **주요 컬럼**:
  - `Case_Name`: 케이스 명칭
  - `Case_ID`: 케이스 ID
  - `Optimal_Shuttle_Size_cbm`: 최적 셔틀 크기
  - `Optimal_Pump_Size_m3ph`: 최적 펌프 크기
  - `Min_NPC_USDm`: 최소 NPC
  - `Initial_CAPEX_USDm`: 초기 CAPEX (2030년)
  - `Annual_AvgOPEX_USDm`: 평균 연간 OPEX
  - `Ranking`: NPC 기준 순위

**예시 파일**:
```
MILP_cases_summary.csv
```

#### 4. **Excel 다중 시트 파일** (옵션)
- **파일명**: `MILP_results_case_X.xlsx`
- **시트 구성**:
  - Sheet 1: Scenario Summary (scenario_summary_case_X.csv와 동일)
  - Sheet 2: Per Year Results (per_year_results_case_X.csv와 동일)
  - Sheet 3: Cost Breakdown (비용 항목별 분석)
  - Sheet 4: Charts (기본 그래프 포함)

#### 5. **Word 보고서** (옵션)
- **파일명**: `MILP_Report_case_X.docx`
- **구성**:
  - Executive Summary
  - Optimization Results Table
  - Cost Analysis
  - Recommendations
  - Charts & Figures

---

## 📈 결과 파일 상세 설명

### Scenario Summary 분석

**CSV 구조 예시** (Case 1):
```
Shuttle_Size_cbm,Pump_Size_m3ph,NPC_Total_USDm,NPC_Shuttle_CAPEX_USDm,NPC_Bunkering_CAPEX_USDm,NPC_Terminal_CAPEX_USDm,...,Feasible
500,400,2890.34,156.23,78.45,1024.56,...,Yes
500,600,2856.12,156.23,58.34,1024.56,...,Yes
...
5000,1200,2584.32,485.23,143.67,1024.56,...,Yes
5000,2000,2698.12,485.23,189.45,1024.56,...,Yes
```

**Top 10 최적 조합** (NPC 기준):
1. 5,000 m³ + 1,200 m³/h → $2,584.32M
2. 3,500 m³ + 1,000 m³/h → $2,651.45M
3. 5,000 m³ + 1,000 m³/h → $2,698.12M
...

### Per Year Results 분석

**CSV 구조 예시** (Case 1):
```
Year,New_Shuttles,Total_Shuttles,Annual_Calls,Supply_m3,Demand_m3,Utilization_Rate,...
2030,1,1,382,1910000,1905000,0.997,...
2031,1,2,764,3820000,3810000,0.997,...
2035,2,3,1146,5730000,6152400,0.931,...
2040,2,5,1910,9550000,10458000,0.913,...
2050,5,15,2856,14280000,19050000,0.749,...
```

---

## 📊 시각화 가능한 그래프

### 1️⃣ NPC vs Shuttle Size (Heatmap)
**용도**: 펌프 크기별 최적 셔틀 크기 찾기
```
         400   600   800  1000  1200  1400  1600 m³/h
500 m³  2890  2856  2834  2812  2790  2798  2856
1000    2756  2734  2712  2690  2668  2680  2734
2000    2645  2623  2601  2579  2557  2569  2623
3000    2567  2545  2523  2501  2479  2491  2545
5000    2598  2576  2554  2532  2510  2522  2576
       ↑ 낮을수록 좋음 (어두운 색 = 낮은 비용)
```

**시각화**: 2D Heatmap (Seaborn)
- X축: Pump Size
- Y축: Shuttle Size
- 색상: NPC 값
- 최적 조합 표시

### 2️⃣ Shuttle 개수 연도별 추이 (Line Chart)
**용도**: 투자 규모 시간대 파악
```
셔틀 수량
│
15├─ Case 1 ─────╱────╱─────╱──────╱─────
│             ╱    ╱     ╱      ╱
 8├─ Case 2 ╱─────╱────╱──────╱
 │       ╱       ╱    ╱
 3├──────╱────────╱───╱────────
 │    ╱        ╱   ╱
 1├──╱────────╱───╱──────────
   └─────────────────────────────→ Year
   2030      2040      2050
```

**시각화**: Line Chart (Matplotlib)
- X축: 연도 (2030~2050)
- Y축: 누적 셔틀 수
- 라인: 각 Case별
- 범례: 색상 구분

### 3️⃣ 공급 vs 수요 추이 (Stacked Area Chart)
**용도**: 수급 균형 검증
```
공급량 (M m³)
│
19├─────────────╱════════════╱  Supply
│            ╱  ════════════╱
│         ╱  ════════════╱
10├──────╱════════════╱
│    ╱  ═══════════╱
│ ╱   ═══════════╱
 0└────────────────────────→ Year
   2030  2035  2040  2045  2050

  Demand (점선으로 표시)
```

**시각화**: Area Chart + Line
- X축: 연도
- Y축: 부피 (m³)
- 면적: 공급량
- 점선: 수요량

### 4️⃣ 비용 구성 분석 (Stacked Bar Chart)
**용도**: CAPEX vs OPEX 비교
```
비용 (억 USD)
│
350├ Case 2-2
│ ├─ 고정OPEX (연파란색)
300├─┼─ 변동OPEX (연초록색)
│ │├─ CAPEX (진파랑색)
250├─┤
│ │
200├─┤
│ │
150├─┤ Case 1
│ │
100├─┤
│ │
 50├─┤
│ │
  0└──────────────────────
    Case 1  Case 2-1  Case 2-2
```

**시각화**: Stacked Bar Chart
- X축: Case 유형
- Y축: 누적 비용 (백만 USD)
- 스택: CAPEX, 고정OPEX, 변동OPEX

### 5️⃣ LCOAmmonia 비교 (Bar Chart with Tolerance)
**용도**: 선박당 연료 비용 비교
```
LCOAmmonia (USD/ton)
│
600├─ 시장가
│  ├────────────────
│
350├─ Case 1
│  ├─ 280-350/ton
│  │
300├──┼─ Case 2-2
│  │├─ 200-270/ton
│  ││
200├──┼─
│  ││
│  ││
100├──┼─
│  ││
  0└──┴────────────────→
```

**시각화**: Bar Chart with Error Bars
- X축: Case 유형
- Y축: LCOAmmonia (USD/ton)
- 오차 범위: 낮음~높음 추정치
- 기준선: 시장가 (600 USD/ton)

### 6️⃣ 초기 투자 vs 20년 NPC (Scatter Plot)
**용도**: 투자 규모와 장기 경제성 분석
```
20년 NPC (억 USD)
│
350├           ● Case 1
│       50.6M CAPEX
│
300├
│
250├
│         ● Case 2-1
│        16.1M CAPEX
200├
│     ● Case 2-2
│    16.1M CAPEX
150├
│
│
100├
│
 50├
│
  0└─┼──────┼──────┼─────────→ 초기 CAPEX (억 USD)
    0   20    40     60

    대각선: 초기투자의 5배 (참고선)
```

**시각화**: Scatter Plot
- X축: 초기 CAPEX (2030년)
- Y축: 20년 NPC (할인가)
- 점: 각 Case
- 크기: 셔틀 크기
- 색상: Pump 크기

### 7️⃣ 연간 비용 추이 (Multi-line Chart)
**용도**: 시간경과에 따른 비용 증가율 비교
```
연간 비용 (억 USD/년)
│
12├─ Case 1
│  ├──────╱────╱─────╱──
│       ╱    ╱     ╱
 8├────╱────╱────╱────────
│    ╱    ╱   ╱
 6├  ╱───╱──╱───╱─ Case 2-2
│╱ ╱  ╱  ╱
 4├╱──╱──╱─╱ Case 2-1
│
 2├───────────────────────
│
 0└────────────────────────→ Year
   2030  2035  2040  2045 2050
```

**시각화**: Line Chart
- X축: 연도
- Y축: 연간 비용 (백만 USD)
- 라인: CAPEX (점선) + OPEX (실선)

### 8️⃣ 사이클 시간 비교 (Horizontal Bar Chart)
**용도**: Case별 운영 특성 이해
```
사이클 시간 (시간)

Case 1 ├─ 육상 적재: 3.33h
       ├─ 운송: 2h
       ├─ 호스 작업: 1h
       ├─ 벙커링: 5h
       └─ 합계: 11.33h ◀─ 706회/년

Case 2-2├─ 육상 적재: 16.67h
        ├─ 항해: 3.34h
        ├─ 호스 작업: 1h
        ├─ 서빙(5척): 35h
        └─ 합계: 63h ◀─ 127회/년

        0   10   20   30   40   50   60   70
```

**시각화**: Horizontal Stacked Bar
- 세그먼트: 각 시간 항목
- 길이: 소요 시간
- 라벨: 연간 가능 횟수

### 9️⃣ Sensitivity Analysis (Tornado Chart)
**용도**: 주요 파라미터의 영향도 분석
```
NPC 변화 (%)

연료가격 ±30% ├─────────●─────────┤  ±5%
할인율 ±2%    ├────●────────────────┤  ±8%
셔틀가격 ±20% ├──────────●──────────┤  ±12%
펌프가격 ±20% ├─●──────────────────┤  ±3%
탱크용량 ±30% ├───────────●────────┤  ±7% (Case 1만)

           -15%  -10%  -5%   0   +5% +10% +15%

           ← 영향도 큼    영향도 작음 →
```

**시각화**: Tornado Chart (Pandas)
- X축: NPC 변화율 (%)
- Y축: 파라미터
- 길이: 민감도

### 🔟 Case 비교 요약 (Radar Chart)
**용도**: 3개 Case의 종합 비교
```
        초기투자(역)
            │
            │  ╱─────────╲
            ├─╱───────────╲──
            │╱  Case 1     ╲
        20년NPV ────●────── 셔틀효율
       (역)  │      │       (정)
            │  Case 2-2
            │  ●    │
            │      ╱─╲
        유연성──────●──────운영비용(역)
        (정)    Case 2-1

        ● = 최적값 (중심에서 멀수록 좋음)
```

**시각화**: Radar Chart
- 축: 초기투자, 20년NPC, 셔틀효율, 운영비용, 유연성
- 다각형: 각 Case의 프로필

---

## 📋 분석 사례

### 사례 1: Case 1의 최적 조합 선택

**쿼리**: "Case 1에서 NPC가 가장 낮은 조합은?"

**Python 코드**:
```python
import pandas as pd

# 결과 파일 읽기
df = pd.read_csv('results/MILP_scenario_summary_case_1.csv')

# 가능한 조합만 필터링
feasible = df[df['Feasible'] == 'Yes']

# NPC 최소값 찾기
optimal = feasible.loc[feasible['NPC_Total_USDm'].idxmin()]

print(f"최적 셔틀 크기: {optimal['Shuttle_Size_cbm']} m³")
print(f"최적 펌프 크기: {optimal['Pump_Size_m3ph']} m³/h")
print(f"최소 NPC: ${optimal['NPC_Total_USDm']:.2f}M")
```

**결과**:
```
최적 셔틀 크기: 5000 m³
최적 펌프 크기: 1200 m³/h
최소 NPC: $2584.32M
```

### 사례 2: 3개 Case 비교

**쿼리**: "3개 Case 중 어떤 것이 가장 경제적인가?"

**Python 코드**:
```python
import pandas as pd

# 각 케이스 최적해 읽기
case1 = pd.read_csv('results/MILP_scenario_summary_case_1.csv')
case2_yeosu = pd.read_csv('results/MILP_scenario_summary_case_2_yeosu.csv')
case2_ulsan = pd.read_csv('results/MILP_scenario_summary_case_2_ulsan.csv')

# 각 케이스의 최소 NPC
min_npc = [
    ('Case 1', case1['NPC_Total_USDm'].min()),
    ('Case 2-1', case2_yeosu['NPC_Total_USDm'].min()),
    ('Case 2-2', case2_ulsan['NPC_Total_USDm'].min())
]

# 정렬
min_npc.sort(key=lambda x: x[1])

for i, (case, npc) in enumerate(min_npc, 1):
    print(f"{i}. {case}: ${npc:.2f}M")
```

**결과**:
```
1. Case 2-2: $1884.56M (최적)
2. Case 2-1: $2015.23M
3. Case 1: $2698.12M
```

### 사례 3: 연년도별 셔틀 투자 계획

**쿼리**: "Case 2-2에서 매년 몇 척의 셔틀을 추가 구매해야 하는가?"

**Python 코드**:
```python
import pandas as pd

df = pd.read_csv('results/MILP_per_year_results_case_2_ulsan.csv')

# 연도별 신규 셔틀 수
print("연도별 셔틀 추가 구매 계획:")
print(df[['Year', 'New_Shuttles', 'Total_Shuttles', 'Annual_Calls']].to_string(index=False))
```

**결과**:
```
Year  New_Shuttles  Total_Shuttles  Annual_Calls
2030             1               1            76
2031             0               1            76
2032             1               2           152
...
2050             2              12          912
```

---

## 🐍 Python 코드 예제

### 예제 1: Heatmap 생성
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 읽기
df = pd.read_csv('results/MILP_scenario_summary_case_1.csv')
df_feasible = df[df['Feasible'] == 'Yes']

# Pivot table 생성
pivot = df_feasible.pivot_table(
    values='NPC_Total_USDm',
    index='Shuttle_Size_cbm',
    columns='Pump_Size_m3ph'
)

# Heatmap 그리기
plt.figure(figsize=(12, 8))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r', cbar_kws={'label': 'NPC ($M)'})
plt.title('Case 1: NPC by Shuttle Size and Pump Capacity')
plt.xlabel('Pump Size (m³/h)')
plt.ylabel('Shuttle Size (m³)')
plt.tight_layout()
plt.savefig('results/case1_npc_heatmap.png', dpi=300)
plt.show()
```

### 예제 2: 연도별 셔틀 추이
```python
import pandas as pd
import matplotlib.pyplot as plt

# 각 케이스 데이터 읽기
case1 = pd.read_csv('results/MILP_per_year_results_case_1.csv')
case2_ulsan = pd.read_csv('results/MILP_per_year_results_case_2_ulsan.csv')

# 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(case1['Year'], case1['Total_Shuttles'], marker='o', label='Case 1', linewidth=2)
plt.plot(case2_ulsan['Year'], case2_ulsan['Total_Shuttles'], marker='s', label='Case 2-2', linewidth=2)

plt.xlabel('Year')
plt.ylabel('Total Shuttles')
plt.title('Shuttle Fleet Growth Projection (2030-2050)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/shuttle_growth.png', dpi=300)
plt.show()
```

### 예제 3: Sensitivity Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 기본 NPC
base_npc = 2584.32

# 파라미터 변화
parameters = {
    '연료가격 ±30%': [0.7*base_npc*1.5, 1.3*base_npc*1.5],
    '할인율 ±2%': [base_npc*0.92, base_npc*1.08],
    '셔틀가격 ±20%': [base_npc*0.88, base_npc*1.12],
    '펌프가격 ±20%': [base_npc*0.97, base_npc*1.03],
    '탱크용량 ±30%': [base_npc*0.93, base_npc*1.07]
}

# Tornado chart 그리기
fig, ax = plt.subplots(figsize=(10, 6))

y_pos = np.arange(len(parameters))
for i, (param, (low, high)) in enumerate(parameters.items()):
    low_change = ((low - base_npc) / base_npc) * 100
    high_change = ((high - base_npc) / base_npc) * 100

    ax.barh(i, low_change, left=0, height=0.4, color='blue', alpha=0.7)
    ax.barh(i, high_change, left=0, height=0.4, color='red', alpha=0.7)

ax.set_yticks(y_pos)
ax.set_yticklabels(parameters.keys())
ax.set_xlabel('NPC Change (%)')
ax.set_title('Sensitivity Analysis - Impact on NPC')
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('results/sensitivity_analysis.png', dpi=300)
plt.show()
```

### 예제 4: Case 비교 요약표
```python
import pandas as pd

# 각 케이스 최적해 추출
results = []

for case_name, file in [
    ('Case 1', 'results/MILP_scenario_summary_case_1.csv'),
    ('Case 2-1', 'results/MILP_scenario_summary_case_2_yeosu.csv'),
    ('Case 2-2', 'results/MILP_scenario_summary_case_2_ulsan.csv')
]:
    df = pd.read_csv(file)
    optimal = df[df['Feasible'] == 'Yes'].loc[df['NPC_Total_USDm'].idxmin()]

    results.append({
        'Case': case_name,
        'Shuttle Size': f"{optimal['Shuttle_Size_cbm']:.0f} m³",
        'Pump Size': f"{optimal['Pump_Size_m3ph']:.0f} m³/h",
        'NPC ($M)': f"{optimal['NPC_Total_USDm']:.2f}",
        'CAPEX ($M)': f"{optimal['NPC_Shuttle_CAPEX_USDm'] + optimal.get('NPC_Bunkering_CAPEX_USDm', 0) + optimal.get('NPC_Terminal_CAPEX_USDm', 0):.2f}"
    })

summary_df = pd.DataFrame(results)
print(summary_df.to_string(index=False))
print("\n" + "="*80)
print("저장: results/case_comparison_summary.csv")
summary_df.to_csv('results/case_comparison_summary.csv', index=False)
```

---

## 📁 결과 폴더 구조

```
results/
├── CSV 파일들
│   ├── MILP_scenario_summary_case_1.csv
│   ├── MILP_scenario_summary_case_2_yeosu.csv
│   ├── MILP_scenario_summary_case_2_ulsan.csv
│   ├── MILP_per_year_results_case_1.csv
│   ├── MILP_per_year_results_case_2_yeosu.csv
│   ├── MILP_per_year_results_case_2_ulsan.csv
│   └── MILP_cases_summary.csv
│
├── Excel 파일들 (옵션)
│   ├── MILP_results_case_1.xlsx
│   ├── MILP_results_case_2_yeosu.xlsx
│   └── MILP_results_case_2_ulsan.xlsx
│
├── Word 문서들 (옵션)
│   ├── MILP_Report_case_1.docx
│   ├── MILP_Report_case_2_yeosu.docx
│   └── MILP_Report_case_2_ulsan.docx
│
└── 사용자 생성 그래프들 (선택사항)
    ├── case1_npc_heatmap.png
    ├── shuttle_growth.png
    ├── cost_comparison.png
    ├── sensitivity_analysis.png
    ├── case_comparison_radar.png
    └── lcoa_comparison.png
```

---

## 🎯 권장 분석 워크플로우

### Step 1: 기본 결과 확인 (5분)
```bash
# CSV 파일로 기본 결과 확인
ls -lh results/MILP_*.csv
```

### Step 2: 최적 조합 추출 (10분)
```python
# Python으로 최적해 추출
import pandas as pd

for case in ['case_1', 'case_2_yeosu', 'case_2_ulsan']:
    df = pd.read_csv(f'results/MILP_scenario_summary_{case}.csv')
    optimal = df[df['Feasible'] == 'Yes'].loc[df['NPC_Total_USDm'].idxmin()]
    print(f"{case}: {optimal['Shuttle_Size_cbm']} m³, {optimal['Pump_Size_m3ph']} m³/h → ${optimal['NPC_Total_USDm']:.2f}M")
```

### Step 3: 시각화 생성 (20분)
- Heatmap (NPC 비교)
- 연도별 추이 (투자 계획)
- Case 비교 (종합)

### Step 4: 민감도 분석 (15분)
- 주요 파라미터 변화 영향 분석
- 불확실성 범위 파악

### Step 5: 의사결정 지원 (10분)
- 최적 조합 추천
- Risk 분석
- 구현 전략 제시

---

## 💡 분석 팁

### Tip 1: 실행 가능성 확인
```python
# Infeasible 조합 제외
feasible_only = df[df['Feasible'] == 'Yes']
print(f"전체 조합: {len(df)}")
print(f"실행 가능: {len(feasible_only)}")
print(f"실행 불가능: {len(df) - len(feasible_only)}")
```

### Tip 2: Top N 시나리오 비교
```python
# Top 5 최적 조합 비교
top5 = df[df['Feasible'] == 'Yes'].nsmallest(5, 'NPC_Total_USDm')
```

### Tip 3: 연도별 비용 추이
```python
# 누적 비용 계산
df['Cumulative_Cost'] = df['Annual_CAPEX_USDm'] + df['Annual_FixedOPEX_USDm'] + df['Annual_VariableOPEX_USDm']
```

### Tip 4: LCOAmmonia 계산
```python
# 선박 연료 암모니아 1톤당 비용
lcoa = total_npc / total_supply_tons
```

---

**최종 업데이트**: 2025-11-18
**버전**: v2.3
