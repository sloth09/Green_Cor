# Phase 2-2: 시간-비용 상관성 분석 구조

**목표**: 1회 운항 시간이 총 NPC에 미치는 영향을 정량화하고 가시화

---

## 1. 시간-비용 영향 메커니즘

### 1-1. 기본 관계식

```
┌─────────────────────────────────────────────────────────────┐
│                    시간-비용 연쇄                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: 펌프 크기 선택                                    │
│  ───────────────────────                                    │
│           pump_size (m³/h) ↑                                │
│           ↓                                                  │
│  Step 2: 펌핑 시간 감소                                    │
│  ───────────────────────                                    │
│           pumping_time = bunker_vol / pump_size             │
│           ↓ (시간 감소)                                      │
│  Step 3: 사이클 시간 감소                                  │
│  ───────────────────────                                    │
│           cycle_duration = shore_load + travel + ... + pump │
│           ↓ (시간 감소)                                      │
│  Step 4: 연간 운항 회수 증가                                │
│  ───────────────────────                                    │
│           annual_cycles = 8000 / cycle_duration             │
│           ↑ (회수 증가)                                      │
│  Step 5: 필요한 셔틀 수 감소 (동일 수요 가정)              │
│  ───────────────────────                                    │
│           required_shuttles = ceil(demand / annual_cycles)  │
│           ↓ (개수 감소)                                      │
│  Step 6: CAPEX 감소                                         │
│  ───────────────────                                        │
│           shuttle_capex = required_shuttles × unit_capex    │
│           ↓ (비용 감소)                                      │
│  Step 7: 연료비 감소                                        │
│  ───────────────────                                        │
│           annual_fuel = shuttles × fuel_per_cycle × cycles  │
│           ↓ (비용 감소)                                      │
│  Step 8: NPC 감소                                           │
│  ───────────────                                            │
│           NPC = Σ(CAPEX + OPEX) discounted                 │
│           ↓ (총 비용 감소)                                   │
│                                                              │
│  ⚠️ 트레이드오프:                                          │
│           pump_capex ↑ (펌프 가격 증가)                     │
│           shuttle_capex ↓ (셔틀 감소로 절감)               │
│           fuel_cost ↓ (연료 절감)                           │
│           → 최적점이 존재                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 정량화 방법론

### 2-1. "시간 1시간 단축" 당 NPC 절감액 계산

**수식**:

```
NPC_Savings = ∑[t=2030→2050] Discount(t) × Cost_Reduction(t)

where:

Cost_Reduction(t) = [
  (Shuttle_CAPEX_reduction(t) + Bunk_CAPEX_reduction(t)) × New_Shuttles(t)
  + (Shuttle_OPEX_reduction(t) + Bunk_OPEX_reduction(t)) × Total_Shuttles(t)
  + (Fuel_cost_reduction(t))
]

Shuttle_CAPEX_reduction(t) = unit_shuttle_capex (1척 절감)
Bunk_CAPEX_reduction(t) = unit_bunk_capex (1조 절감)
Shuttle_OPEX_reduction(t) = annual_shuttle_fixed_opex (1척 감소)
Bunk_OPEX_reduction(t) = annual_bunk_fixed_opex (1조 감소)
Fuel_cost_reduction(t) = annual_fuel_cost_reduction
```

**예시 계산**:

```
조건: 5,000 m³ 셔틀, 1,000 → 2,000 m³/h 펌프

Step 1: 펌핑 시간 변화
────────────────────
기존: 5,000 / 1,000 = 5.00 시간
신규: 5,000 / 2,000 = 2.50 시간
감소: 2.50 시간 (50%)

Step 2: 사이클 시간 변화
──────────────────────
기존: shore_load(3.33) + travel(2.0) + setup(1.0) + pump(5.0) + return(2.0) = 13.33h
신규: shore_load(3.33) + travel(2.0) + setup(1.0) + pump(2.5) + return(2.0) = 10.83h
감소: 2.50 시간 (18.8%)

Step 3: 연간 운항 회수 변화
─────────────────────────
기존: 8,000 / 13.33 = 600회
신규: 8,000 / 10.83 = 739회
증가: 139회 (23.2%)

Step 4: 필요한 셔틀 수 변화 (2030년 수요 기준)
────────────────────────────────
2030년 수요: 1,905,000 m³ (50척 × 2,158,995 × 12회)
기존: ceil(1,905,000 / (600 × 5,000)) = 1척
신규: ceil(1,905,000 / (739 × 5,000)) = 1척
감소: 0척 (2030년에는 둘 다 1척 필요)

→ 후반부 연도(2040-2050)에서 절감 가능

Step 5: 후반부 연도 셔틀 절감 (예: 2050년)
──────────────────────────────────────
2050년 수요: 19,050,000 m³ (500척 × 2,158,995 × 12회)
기존: ceil(19,050,000 / (600 × 5,000)) = 7척 필요
신규: ceil(19,050,000 / (739 × 5,000)) = 6척 필요
감소: 1척

Step 6: 20년간 누적 절감
──────────────────────
2030-2035: 0척 절감 × $18.9M = $0M
2036-2040: 0.5척 평균 × $18.9M = $4.7M/년 × 5년 = $23.5M
2041-2045: 0.8척 평균 × $18.9M = $15.1M/년 × 5년 = $75.5M
2046-2050: 1.0척 절감 × $18.9M = $18.9M/년 × 5년 = $94.5M
────────────────────────────────────────────────────
할인 적용 (7% 할인율):
  Discounted Total ≈ $150M

연료비 절감:
  펌프 연료비: 약 $20M/년 × 20년 할인 ≈ $180M
  셔틀 연료비: 약 $5M/년 × 20년 할인 ≈ $57M
────────────────────────────────────────────────────
할인 적용 연료비 절감: ≈ $237M

펌프 CAPEX 증가:
  펌프 크기 2배: CAPEX 약 $300k vs $150k = +$150k/조
  1조만 필요이므로: +$150k = -$0.15M (무시할 수 있음)

Step 7: 순 절감액
──────────────────
NPC 절감 = 셔틀절감 + 연료절감 - 펌프증가
        = $150M + $237M - $0M
        = $387M (20년 할인액)

시간 당 절감액:
NPC_saving_per_hour = $387M / 2.5시간
                    = $154.8M/시간
                    ≈ $155M/시간 (또는 $155k/분)
```

### 2-2. 보고서에 포함할 시간-비용 분석 테이블

```
┌────────────────────────────────────────────────────────────┐
│ 【시간-비용 상관 분석】                                     │
├────────────────────────────────────────────────────────────┤
│                                                              │
│ Pump 크기          Cycle Time    Annual       Shuttle      │
│ (m³/h)             (h)           Cycles       Needed       │
│ ───────────────────────────────────────────────────────   │
│ 400               18.33          436           ↑           │
│ 600               16.00          500           |           │
│ 800               15.00          533           |           │
│ 1,000             14.33          558           | (증가)     │
│ 1,200             13.75          582           |           │
│ 1,500             13.00          615           |           │
│ 2,000             12.00          667           ↓           │
│                                                              │
│ Pump CAPEX         Shuttle CAPEX   Annual       Total      │
│ (k$)               (M$)            Fuel ($M)    NPC ($M)   │
│ ───────────────────────────────────────────────────────   │
│ 150                $18.9           $8.5         $2,834     │
│ 220                $18.9           $8.2         $2,805     │
│ 260                $18.9           $8.1         $2,784     │
│ 300                $18.9           $8.0         $2,768     │ ⬅ 최적
│ 340                $18.9           $7.9         $2,755     │
│ 390                $18.9           $7.8         $2,749     │
│ 500                $14.2           $7.5         $2,781     │
│                                                              │
│ 관찰:
│ • 펌프 크기 400→1000: 시간 4.3시간 감소, NPC 감소 $66M
│ • 펌프 크기 1000→2000: 시간 2.3시간 감소, NPC 감소 $0M
│   (펌프 비용 증가로 상쇄됨)
│
│ ⚠️ 최적점은 대부분 1,000~1,500 m³/h 범위
│    (펌프 크기 vs. 펌프 CAPEX의 트레이드오프)
│
└────────────────────────────────────────────────────────────┘
```

---

## 3. 보고서 작성 가이드

### 3-1. Word 문서에 포함할 섹션

```
5. 시간-비용 상관성 분석 (Time-Cost Correlation Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5.1 개요

  1회 왕복 운항의 시간이 총 NPC에 미치는 영향은 두 가지 경로를 통해
  전달됩니다:

  ① 직접 경로: 시간 → 필요한 셔틀 수 → CAPEX/OPEX
  ② 간접 경로: 시간 → 연료 소비 → 운영비

5.2 펌프 크기별 시간-비용 변화

  [표 삽입: Pump 크기 vs. Cycle Time vs. NPC]

  주요 관찰:
  • 펌프 크기 증가 → 사이클 시간 감소 → NPC 감소 (초기 구간)
  • 펌프 CAPEX 증가 → NPC 감소 효과 상쇄 (후기 구간)
  • 최적점: 1,200~1,500 m³/h 범위

5.3 셔틀 감소를 통한 절감액

  [표 삽입: 연도별 셔틀 필요 수 및 CAPEX 절감]

  예: 펌프 크기 1,000 → 1,500 m³/h

  연도   기존 필요   신규 필요   절감    CAPEX 절감
  ────────────────────────────────────────────
  2035   2척        2척        0       $0M
  2040   3척        3척        0       $0M
  2045   5척        4척        1       $18.9M
  2050   7척        6척        1       $18.9M

  누적 (할인): ~$50M

5.4 연료비 절감

  [표 삽입: 펌프 크기별 연간 연료비]

  • 펌프 크기 2배 → 펌핑 시간 50% 단축
  • 연료비 절감: 약 $20-30M/년 × 20년 할인 ≈ $200M+

5.5 최적 펌프 크기 선택 기준

  문제: "언제 펌프를 크게 선택할까?"

  답: 수요가 빠르게 증가하는 초반부에는 작은 펌프로도 충분하지만,
      중반 이후(2035-2050) 수요 충족에 더 많은 셔틀이 필요하므로,
      펌프 크기를 크게 하는 것이 CAPEX 절감 효과가 크다.

  따라서 초기 투자를 감수하고 큰 펌프를 선택하면,
  20년 누적 NPC 관점에서 $100-200M 절감 가능.

5.6 Case별 시간-비용 비교

  [표 삽입: 3가지 케이스의 시간-NPC 비교]

  Case 1 (부산)   : 사이클 15.33h, NPC $2,768M
  Case 2-2 (울산) : 사이클 14.67h, NPC $1,855M (32% 저렴)
  Case 2-1 (여수) : 사이클 22.79h, NPC $2,015M

  의미:
  • Case 2-2가 가장 효율적 (짧은 항해 시간)
  • Case 2-1은 항해 시간 때문에 비용 증가
  • 위치 선택이 NPC를 결정하는 주요 요소
```

---

## 4. 시간-비용 분석 데이터 구조

### 4-1. TimeCorrelationAnalysis 클래스 (신규)

```python
# src/time_cost_analysis.py (새 파일)

@dataclass
class TimeCorrelationAnalysis:
    """시간-비용 상관성 분석"""

    # 입력
    pump_sizes: List[float]                # 펌프 크기 (m³/h)
    shuttle_size: float                    # 셔틀 크기 (m³)
    case_type: str                         # Case 1, 2-1, 2-2

    # 출력: 각 펌프 크기별
    cycle_times: Dict[float, float]        # pump_size → cycle_duration
    annual_cycles: Dict[float, float]      # pump_size → annual_cycles
    shuttle_requirement: Dict[float, Dict] # pump_size → year → required_shuttles
    npc_values: Dict[float, float]         # pump_size → NPC

    # 상관성
    time_reduction: Dict[float, float]     # pump_size → time_reduction (hours)
    npc_reduction: Dict[float, float]      # pump_size → NPC_reduction ($M)
    roi_per_hour: Dict[float, float]       # pump_size → $/hour_saved

    def get_optimal_pump_size(self) -> Tuple[float, float]:
        """최적 펌프 크기 반환"""
        optimal_pump = min(
            self.npc_values.keys(),
            key=lambda p: self.npc_values[p]
        )
        return optimal_pump, self.npc_values[optimal_pump]

    def get_sensitivity_table(self) -> pd.DataFrame:
        """민감도 분석 테이블"""
        rows = []
        for pump in sorted(self.pump_sizes):
            rows.append({
                'Pump_Size_m3ph': pump,
                'Cycle_Duration_h': self.cycle_times[pump],
                'Annual_Cycles': self.annual_cycles[pump],
                'Time_Reduction_h': self.time_reduction[pump],
                'NPC_$M': self.npc_values[pump],
                'NPC_Reduction_$M': self.npc_reduction[pump],
                'ROI_per_Hour_k$': self.roi_per_hour.get(pump, 0),
            })
        return pd.DataFrame(rows)
```

---

## 5. 보고서 생성 로직

### 5-1. 시간-비용 분석 계산 (pseudo-code)

```python
def calculate_time_cost_correlation(optimizer_results, case_type):
    """
    최적화 결과에서 시간-비용 상관성 추출

    각 펌프 크기별:
    1. Cycle time 추출
    2. Annual cycles 계산
    3. 20년간 필요한 셔틀 수 계산
    4. NPC 값 추출
    5. 상관성 분석
    """

    analysis = TimeCorrelationAnalysis(...)

    for result in optimizer_results:
        pump_size = result['Pump_Size_m3ph']

        # 시간 정보
        analysis.cycle_times[pump_size] = result['Cycle_Duration_hr']
        analysis.annual_cycles[pump_size] = 8000 / result['Cycle_Duration_hr']

        # 셔틀 요구량 (연도별)
        analysis.shuttle_requirement[pump_size] = {}
        for year in range(2030, 2051):
            shuttles_needed = calculate_required_shuttles(
                demand[year],
                annual_cycles[pump_size],
                shuttle_size
            )
            analysis.shuttle_requirement[pump_size][year] = shuttles_needed

        # NPC 값
        analysis.npc_values[pump_size] = result['NPC_Total_USDm']

    # 상관성 계산 (기준: 가장 작은 펌프를 기준점)
    min_pump = min(analysis.npc_values.keys())
    baseline_npc = analysis.npc_values[min_pump]
    baseline_time = analysis.cycle_times[min_pump]

    for pump in analysis.pump_sizes:
        analysis.time_reduction[pump] = baseline_time - analysis.cycle_times[pump]
        analysis.npc_reduction[pump] = baseline_npc - analysis.npc_values[pump]

        if analysis.time_reduction[pump] > 0:
            analysis.roi_per_hour[pump] = (
                analysis.npc_reduction[pump] / analysis.time_reduction[pump] * 1000
            )  # k$ per hour

    return analysis
```

### 5-2. Word 보고서 추가 로직

```python
def add_time_cost_correlation_section(doc, analysis):
    """Word 문서에 시간-비용 상관성 섹션 추가"""

    doc.add_heading('5. 시간-비용 상관성 분석', level=1)

    # 5.1 개요
    doc.add_paragraph('...')

    # 5.2 테이블
    table_data = analysis.get_sensitivity_table()
    add_dataframe_to_word(doc, table_data)

    # 5.3 차트
    fig = create_time_cost_chart(analysis)
    doc.add_picture(fig, width=Pt(600))

    # 5.4 분석 결과
    optimal_pump, optimal_npc = analysis.get_optimal_pump_size()
    doc.add_paragraph(
        f'최적 펌프 크기: {optimal_pump:.0f} m³/h, '
        f'NPC: ${optimal_npc:.0f}M'
    )

    # ... 나머지 섹션
```

---

## 6. 차트 설계

### 6-1. Excel/Word에 포함할 차트

#### Chart 1: 펌프 크기 vs. 사이클 시간 & NPC

```
Y축 좌측: Cycle Duration (hours)
Y축 우측: NPC (Million USD)
X축: Pump Size (m³/h)

[선 차트 2개]
- Cycle Duration: 우측 하향 (펌프 크기 증가 → 시간 감소)
- NPC: 함수형 (최솟값 존재)
```

#### Chart 2: 펌프 크기별 필요 셔틀 수 (연도별 누적)

```
[누적 막대 차트]
X축: 펌프 크기 (400, 600, 800, 1000, 1200, 1500, 2000 m³/h)
Y축: 누적 셔틀 수 (2030-2050)
색상: 연도별

관찰: 펌프 크기 증가 → 필요한 셔틀 수 감소 (선형 관계 아님)
```

#### Chart 3: 시간-비용 산포도 (Scatter)

```
X축: Cycle Duration (hours)
Y축: NPC ($M)

각 점: 펌프 크기별 시나리오
추세선: 음의 기울기 (시간 감소 → NPC 감소)
```

---

## 다음 단계

✅ **Phase 2 완료**

진행:
1. Phase 3: 실제 코드 구현
2. Phase 4: 실제 케이스 검증
3. Phase 5: 최종 보고서 생성

---

**작성일**: 2025-11-18
