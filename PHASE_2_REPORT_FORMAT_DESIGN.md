# Phase 2: 보고서 형식 설계

**목표**: 1회 왕복 운항 시간을 상세하게 보고서에 포함할 형식 설계

---

## 1. 출력 위치별 시간 정보 포함 전략

### 1-1. CSV 파일 (`MILP_scenario_summary_{case_id}.csv`)

**현재 상태**: 이미 일부 시간 정보 포함
- `Call_Duration_hr`: 1회 콜 시간
- `Cycle_Duration_hr`: 1회 사이클 시간
- `Trips_per_Call`: 콜당 왕복 횟수

**추가할 컬럼**:
```
기존:
Shuttle_Size_cbm, Pump_Size_m3ph, Call_Duration_hr, Cycle_Duration_hr,
Trips_per_Call, ...

추가 (시간 구성 요소):
├─ Shore_Loading_hr          : 육상 적재 시간
├─ Travel_Outbound_hr        : 편도 항해 시간
├─ Travel_Return_hr          : 복귀 항해 시간
├─ Setup_Time_hr             : 호스 작업 시간 (connection + disconnection)
├─ Pumping_Per_Vessel_hr     : 선박당 펌핑 시간
├─ Movement_Per_Vessel_hr    : 선박당 이동 시간
├─ Basic_Cycle_Duration_hr   : 육상 제외 사이클 시간

추가 (운영 효율성):
├─ Annual_Cycles_Max         : 셔틀당 연간 최대 가능 항차
├─ Vessels_per_Trip          : 1회 항해당 서빙 선박 수
├─ Annual_Supply_m3          : 연간 공급 가능량 (m³)
└─ Time_Utilization_Ratio    : 시간 활용도 (%)
```

**예시**:
```csv
Shuttle_Size_cbm,Pump_Size_m3ph,Call_Duration_hr,Cycle_Duration_hr,
Shore_Loading_hr,Travel_Outbound_hr,Travel_Return_hr,Setup_Time_hr,
Pumping_Per_Vessel_hr,Movement_Per_Vessel_hr,Basic_Cycle_Duration_hr,
Annual_Cycles_Max,Vessels_per_Trip,Annual_Supply_m3,Time_Utilization_Ratio,
...

5000,1000,12.00,15.33,3.33,2.00,2.00,1.00,5.00,1.00,12.00,522,1,2610000,65.2%,...
5000,1500,10.00,13.33,3.33,2.00,2.00,1.00,3.33,1.00,10.00,600,1,3000000,75.0%,...
```

---

### 1-2. Excel 보고서 (`MILP_results_{case_id}.xlsx`)

#### Sheet 1: "Scenario Summary" (기존)
- 현재 구조 유지 + 시간 컬럼 추가

#### Sheet 2: "Time Breakdown" (NEW)
**목표**: 각 최적 시나리오별 시간을 상세히 분석

**구조**:
```
┌─────────────────────────────────────────────────────────────┐
│ 【최적 시나리오 시간 분석】                                  │
├─────────────────────────────────────────────────────────────┤
│ Case: Case 1 (Busan Storage)                                │
│ 최적 조합: Shuttle 5,000 m³ + Pump 1,200 m³/h               │
│ NPC: $2,584.32M (20년)                                      │
│ LCOA: $324/ton                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌─ 1회 왕복 운항 시간 분해 (Time Breakdown)                 │
│ │                                                            │
│ │  시간 구성요소           시간(hr)   비율(%)   누적(%)     │
│ │  ────────────────────────────────────────────────────    │
│ │  1. 육상 연료 적재        3.33     21.7%    21.7%       │
│ │     (5000 ÷ 1500)                                         │
│ │                                                            │
│ │  2. 편도 항해             2.00     13.0%    34.7%       │
│ │  3. 호스 연결             1.00      6.5%    41.2%       │
│ │  4. 벙커링 (펌핑)         4.17     27.1%    68.3%       │
│ │     (5000 ÷ 1200)                                         │
│ │  5. 호스 분리             1.00      6.5%    74.8%       │
│ │  6. 복귀 항해             2.00     13.0%    87.8%       │
│ │  7. 이동 시간             1.00      6.5%   100.0%       │
│ │                                                            │
│ │  ─────────────────────────────────────────────────────  │
│ │  【총 사이클 시간】       15.33     100%                  │
│ │  (육상 포함)                                              │
│ │                                                            │
│ │  기본 사이클 (육상 제외): 12.00 시간                       │
│ │                                                            │
│ └─ 연간 운영 지표                                           │
│                                                              │
│    연간 최대 항차         522회     (8000 ÷ 15.33)          │
│    셔틀 1척당 평균        14일/회   (365 ÷ 522 × 20)        │
│    연간 공급 용량        2,610,000 m³  (522 × 5000)        │
│    해상 운영 효율         78.3%      (12.0 ÷ 15.33)        │
│    시간 활용도            65.2%      (522 × 15.33 ÷ 8000)  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**세부 시트 내용**:
- 상단: 최적 시나리오 요약 (Case, 선택 조합, NPC, LCOA)
- 중앙: 시간 구성 요소 분해표 (7-8개 요소, 시간 + 비율 + 누적)
- 차트: 시간 분해 파이 차트 (시각적 이해 용이)
- 하단: 연간 운영 지표 (항차, 일정, 용량, 효율)

**추가 행**: Case별로 반복

---

#### Sheet 3: "Case Comparison" (NEW)
**목표**: Case 1, 2-1, 2-2의 시간 차이를 시각적으로 비교

**구조**:
```
┌──────────────────────────────────────────────────────────────┐
│ 【Case별 시간 비교】                                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  운항 요소              Case 1    Case 2-2    Case 2-1       │
│  ────────────────────────────────────────────────────────   │
│  Location           부산항     울산        여수             │
│  설정 거리           2.0h      1.67h      5.73h            │
│                                                               │
│  (예시: 5,000 m³ 셔틀, 1,000 m³/h 펌프)                     │
│                                                               │
│  1. 육상 적재          3.33h     3.33h      3.33h           │
│  2. 편도 항해          2.00h     1.67h      5.73h  ⬅ 차이  │
│  3. 호스 작업          1.00h     1.00h      1.00h           │
│  4. 펌핑               5.00h     5.00h      5.00h           │
│  5. 호스 분리          1.00h     1.00h      1.00h           │
│  6. 복귀 항해          2.00h     1.67h      5.73h  ⬅ 차이  │
│  7. 이동               1.00h     1.00h      1.00h           │
│                                                               │
│  ─────────────────────────────────────────────────────────  │
│  【총 사이클】         15.33h    14.67h     22.79h          │
│  시간 차이             +4.6%     기준       +55.4%         │
│                                                               │
│  ─────────────────────────────────────────────────────────  │
│  연간 항차             522회     546회      351회           │
│  효율 변화             -4.4%     +4.6%     -35.7%         │
│                                                               │
│  의미:
│  • Case 2-1의 항해 시간이 가장 김
│    → 같은 수요 충족에 더 많은 셔틀 필요
│    → NPC 증가
│
│  • Case 2-2가 가장 효율적 (짧은 거리)
│    → 더 적은 셔틀로 더 많은 수요 충족 가능
│    → NPC 감소
│
└──────────────────────────────────────────────────────────────┘
```

**차트**:
- 막대 차트 1: Case별 사이클 시간 비교 (누적형 또는 그룹형)
- 막대 차트 2: Case별 연간 항차 비교
- 선 차트: 펌프 크기별 사이클 시간 변화

---

### 1-3. Word 보고서 (`MILP_Report_{case_id}.docx`)

#### New Section: "운항 시간 분석 (Time Structure Analysis)"

**위치**: Executive Summary 바로 다음

**구조**:

```
4. 운항 시간 분석 (Time Structure Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4.1 최적 시나리오의 운항 시간 구성

  최적 시나리오: Shuttle 5,000 m³ + Pump 1,200 m³/h

  1회 왕복 운항의 총 시간: 15.33시간

  ┌─────────────────────────────────────────────────┐
  │ 시간 구성 요소 (Time Components)                │
  ├─────────────────────────────────────────────────┤
  │                                                  │
  │ ① 육상 연료 적재                   3.33시간    │
  │    (shuttle 5,000 m³ / shore pump 1,500 m³/h)  │
  │                                                  │
  │ ② 편도 항해 (부산항)               2.00시간    │
  │    (항만 내 이동)                              │
  │                                                  │
  │ ③ 호스 연결 및 기체 퍼징           1.00시간    │
  │    (각 0.5시간 × 2)                            │
  │                                                  │
  │ ④ 벙커링 펌핑 (1회 콜)             4.17시간    │
  │    (5,000 m³ / 1,200 m³/h pump)                │
  │                                                  │
  │ ⑤ 호스 분리 및 암모니아 퍼징      1.00시간    │
  │    (각 0.5시간 × 2)                            │
  │                                                  │
  │ ⑥ 복귀 항해                        2.00시간    │
  │    (항만 내 반대 방향 이동)                     │
  │                                                  │
  │ ⑦ 선박 이동 및 계류                1.00시간    │
  │    (벙커링 지점 이동/정박)                      │
  │                                                  │
  ├─────────────────────────────────────────────────┤
  │ 【총 사이클 시간】                 15.33시간   │
  │ 사이클 기본 시간 (육상 제외)        12.00시간   │
  │ 시간 활용도 (기본/전체)            78.3%      │
  └─────────────────────────────────────────────────┘

4.2 시간별 구성 비율

  벙커링 펌핑이 전체 시간의 27.2%를 차지하여,
  펌프 크기 선택이 가장 중요한 최적화 포인트임을 보여줍니다.

  ┌─── Pie Chart ──────────────────────────────────┐
  │                                                │
  │        [ 육상 적재 ]                          │
  │           21.7%                              │
  │         / \                                  │
  │        /   \                                 │
  │      /       \                               │
  │    [호스작업][편도항해]  [펌핑]             │
  │     6.5%      13.0%      27.2%              │
  │     \         \           /                  │
  │      \         \         /                   │
  │       \ _____[복귀항해]                     │
  │             13.0%                           │
  │                                              │
  │  기타 이동: 12.0%                           │
  │                                              │
  └────────────────────────────────────────────────┘

4.3 연간 운영 지표

  연간 최대 항차:           522회 (8,000시간 ÷ 15.33시간)
  셔틀당 평균 일정:         14일/회 (365일 ÷ 522회)
  연간 공급 용량:           2,610,000 m³ (522회 × 5,000 m³)

  ※ 이 수치는 이상적인 시나리오입니다. 실제 운영은
    기상, 유지보수, 항만 혼잡도 등으로 인해 감소합니다.

4.4 펌프 크기에 따른 시간 변화 분석

  펌프 크기 증가 → 펌핑 시간 감소 → 전체 사이클 시간 감소

  ┌────────────────┬──────────────────────────────┐
  │ Pump 크기      │ 사이클 시간 │ 연간 항차      │
  ├────────────────┼────────────┼──────────────┤
  │ 600 m³/h       │ 17.75h     │ 451회        │
  │ 800 m³/h       │ 16.00h     │ 500회        │
  │ 1,000 m³/h     │ 15.33h     │ 522회        │ ⬅ 최적
  │ 1,200 m³/h     │ 14.75h     │ 542회        │
  │ 1,500 m³/h     │ 14.00h     │ 571회        │
  │ 2,000 m³/h     │ 13.00h     │ 615회        │
  └────────────────┴────────────┴──────────────┘

  관찰: 펌프 크기를 2배 증가(1,000→2,000)하면
       사이클 시간은 15% 감소하지만,
       펌프 CAPEX는 2배 이상 증가하므로
       NPC 관점에서 최적점이 존재합니다.

4.5 Case별 시간 비교 (3가지 시나리오)

  [표: Case별 시간 비교 - 2행 × 3열]

  모두 동일한 셔틀(5,000m³)과 펌프(1,200m³/h) 가정:

  Case 1 (부산)    Case 2-2 (울산)    Case 2-1 (여수)
  ─────────────    ─────────────      ──────────────
  사이클: 15.33h   사이클: 14.67h     사이클: 22.79h
  항차: 522회      항차: 546회        항차: 351회

  → Case 2-1은 항해 시간이 57% 더 길어
    같은 수요 충족에 더 많은 셔틀 필요
    결과: NPC 약 30% 증가 예상
```

---

## 2. 데이터 구조 설계

### 2-1. Time Breakdown Data Class

```python
# src/time_structure.py (새 파일)

@dataclass
class TimeBreakdown:
    """1회 왕복 운항의 시간 구성 요소"""

    # 기본 구성 요소 (시간 단위)
    shore_loading: float          # 육상 적재
    travel_outbound: float        # 편도 항해
    setup_inbound: float          # 호스 연결
    pumping_per_vessel: float     # 선박당 펌핑
    movement: float               # 이동
    setup_outbound: float         # 호스 분리
    travel_return: float          # 복귀 항해

    # 집계 값
    basic_cycle: float            # 육상 제외 사이클
    cycle_duration: float         # 전체 사이클
    call_duration: float          # 콜 시간 (여러 왕복의 합)

    # 운영 지표
    annual_cycles_max: float      # 연간 최대 항차
    annual_supply_m3: float       # 연간 공급량
    vessels_per_trip: int         # 1회 항해당 선박 수

    def get_breakdown_dict(self) -> Dict:
        """보고서 용 딕셔너리로 변환"""
        return {
            '육상 적재': self.shore_loading,
            '편도 항해': self.travel_outbound,
            '호스 연결': self.setup_inbound,
            '펌핑': self.pumping_per_vessel,
            '이동': self.movement,
            '호스 분리': self.setup_outbound,
            '복귀 항해': self.travel_return,
        }

    def get_percentages(self) -> Dict:
        """각 요소의 비율 계산"""
        total = self.basic_cycle
        return {k: (v / total * 100) for k, v in self.get_breakdown_dict().items()}
```

---

## 3. 보고서 생성 로직 설계

### 3-1. CSV 확장 로직

```python
# src/report_generator.py (기존 파일 확장)

def generate_scenario_summary_csv_with_time(self, results, case_id, output_dir):
    """
    시간 정보를 포함한 시나리오 요약 CSV 생성

    추가 컬럼:
    - Shore_Loading_hr
    - Travel_Outbound_hr
    - Travel_Return_hr
    - Setup_Time_hr
    - Pumping_Per_Vessel_hr
    - Movement_Per_Vessel_hr
    - Basic_Cycle_Duration_hr
    - Annual_Cycles_Max
    - Vessels_per_Trip
    - Time_Utilization_Ratio
    """

    # 각 시나리오별로 시간 정보 추가
    for scenario in results:
        breakdown = scenario.get('time_breakdown')  # TimeBreakdown 객체

        scenario['Shore_Loading_hr'] = breakdown.shore_loading
        scenario['Travel_Outbound_hr'] = breakdown.travel_outbound
        # ... 모든 요소 추가
        scenario['Annual_Cycles_Max'] = breakdown.annual_cycles_max
        scenario['Time_Utilization_Ratio'] = (
            breakdown.cycle_duration * breakdown.annual_cycles_max / 8000 * 100
        )

    # CSV로 저장
    df = pd.DataFrame(results)
    df.to_csv(f"{output_dir}/MILP_scenario_summary_{case_id}.csv", index=False)
```

### 3-2. Excel 시트 추가 로직

```python
def add_time_breakdown_sheet(self, workbook, scenario):
    """
    "Time Breakdown" 시트 추가

    내용:
    - 최적 시나리오 정보
    - 시간 분해 테이블
    - 시간 분해 파이 차트
    - 연간 운영 지표
    """

    ws = workbook.create_sheet('Time Breakdown')

    # 제목 및 기본 정보
    ws['A1'] = '【최적 시나리오 시간 분석】'
    ws['A2'] = f"Case: {scenario['case_name']}"
    ws['A3'] = f"Shuttle: {scenario['shuttle_size']} m³"

    # 시간 분해 테이블
    breakdown = scenario['time_breakdown']
    components = [
        ('육상 적재', breakdown.shore_loading),
        ('편도 항해', breakdown.travel_outbound),
        ('호스 연결', breakdown.setup_inbound),
        ('펌핑', breakdown.pumping_per_vessel),
        ('호스 분리', breakdown.setup_outbound),
        ('복귀 항해', breakdown.travel_return),
        ('이동', breakdown.movement),
    ]

    row = 5
    for name, hours in components:
        percentage = (hours / breakdown.basic_cycle) * 100
        ws[f'A{row}'] = name
        ws[f'B{row}'] = hours
        ws[f'C{row}'] = f"{percentage:.1f}%"
        row += 1

    # 총합
    ws[f'A{row}'] = '【총 사이클】'
    ws[f'B{row}'] = breakdown.cycle_duration
    ws[f'C{row}'] = '100%'

    # 차트 추가
    pie = PieChart()
    pie.title = "운항 시간 구성"
    # 차트 데이터 설정...
    ws.add_chart(pie)
```

### 3-3. Word 섹션 추가 로직

```python
def add_time_analysis_section(self, doc, scenario):
    """
    Word 문서에 운항 시간 분석 섹션 추가

    내용:
    - 시간 구성 요소 표
    - 시간별 구성 비율 설명
    - 연간 운영 지표
    - 펌프 크기별 시간 변화 표
    - Case별 시간 비교
    """

    breakdown = scenario['time_breakdown']

    # 제목
    doc.add_heading('4. 운항 시간 분석 (Time Structure Analysis)', level=1)

    # 부제목
    doc.add_heading('4.1 최적 시나리오의 운항 시간 구성', level=2)

    # 시간 분해 표
    table = doc.add_table(rows=9, cols=2)
    table.style = 'Light Grid Accent 1'

    components = [
        ('육상 연료 적재', breakdown.shore_loading),
        ('편도 항해', breakdown.travel_outbound),
        ('호스 연결 및 퍼징', breakdown.setup_inbound),
        ('벙커링 펌핑', breakdown.pumping_per_vessel),
        ('호스 분리 및 퍼징', breakdown.setup_outbound),
        ('복귀 항해', breakdown.travel_return),
        ('이동 및 계류', breakdown.movement),
    ]

    for i, (name, hours) in enumerate(components, start=1):
        table.rows[i].cells[0].text = name
        table.rows[i].cells[1].text = f"{hours:.2f} 시간"

    table.rows[8].cells[0].text = '【총 사이클 시간】'
    table.rows[8].cells[1].text = f"{breakdown.cycle_duration:.2f} 시간"

    # 설명 추가
    doc.add_paragraph(...)

    # ... 나머지 섹션
```

---

## 4. CSV/Excel/Word 추가 컬럼 명세

### 4-1. CSV 추가 컬럼

```
기존 컬럼:
- Shuttle_Size_cbm
- Pump_Size_m3ph
- Call_Duration_hr
- Cycle_Duration_hr
- Trips_per_Call
- NPC_Total_USDm
- (기타 비용 관련)

추가 컬럼 (시간 분해):
- Shore_Loading_hr                  ← NEW
- Travel_Outbound_hr                ← NEW
- Travel_Return_hr                  ← NEW
- Setup_Time_hr (sum of in+out)     ← NEW
- Pumping_Per_Vessel_hr             ← NEW
- Movement_Per_Vessel_hr            ← NEW
- Basic_Cycle_Duration_hr           ← 명확화

추가 컬럼 (운영 지표):
- Annual_Cycles_Max                 ← NEW
- Vessels_per_Trip                  ← NEW (Case 2에서 의미)
- Annual_Supply_m3                  ← NEW
- Time_Utilization_Ratio            ← NEW
- Operating_Days_per_Cycle          ← NEW (365 / annual_cycles)
```

---

## 5. 시간 분석 보고서 아웃라인

### Word 문서 신규 섹션 목차

```
4. 운항 시간 분석 (Time Structure Analysis)
   4.1 최적 시나리오의 운항 시간 구성
   4.2 시간별 구성 비율
   4.3 연간 운영 지표
   4.4 펌프 크기에 따른 시간 변화 분석
   4.5 Case별 시간 비교

5. 결론 및 권장사항
   5.1 주요 발견
   5.2 운영 시뮬레이션
```

---

## 다음 단계

✅ **Phase 2 설계 완료**

진행 순서:
1. **Phase 3**: 설계를 바탕으로 코드 구현
2. **Phase 4**: 실제 케이스 실행 및 검증
3. **Phase 5**: 최종 보고서 생성 및 완료

---

**작성일**: 2025-11-18
