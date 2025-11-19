# Green Corridor Ammonia Bunkering Optimization Model

## Overview

이 프로젝트는 부산항에서의 암모니아 연료 공급 인프라를 최적화하기 위한 MILP(혼합정수선형계획) 모델입니다.

**목표**: 2030~2050년 20년 동안 친환경 해운 회랑에서의 암모니아 연료 수요를 충족하기 위해 필요한 셔틀 선박 및 저장 시설의 최적 규모와 개수를 결정하고, 전체 순현재가(Net Present Cost, NPC)를 최소화합니다.

**버전**: 2.2 (v2.1 Case 2 왕복 거리 버그 수정 + v2.2 Config 구조 개선)

---

## Key Improvements from v1

### 이전 버전 (MILPmodel_v17_250811.py)
- ❌ Case 1만 구현
- ❌ 모든 파라미터 하드코딩
- ❌ 단일 케이스만 실행 가능
- ❌ 코드 재사용성 낮음

### v2.0 → v2.2 개선사항
- ✅ **Case 1, 2-1, 2-2 모두 지원**
- ✅ **YAML 기반 설정 파일로 쉬운 파라미터 관리**
- ✅ **다중 케이스 병렬 실행 지원**
- ✅ **모듈화된 구조 (config, optimizer, cost calculator)**
- ✅ **1항차 급유량 5000 m³로 업데이트**
- ✅ **Tank 크기 35,000톤으로 수정**
- ✅ **4500, 5000 m³ 셔틀 크기 추가**

### v2.1 버그 수정 (Case 2 왕복 거리)
- 🔧 **Cycle Duration**: Case 2에서 왕복 여행 시간 적용
- 🔧 **Shuttle Fuel Cost**: Case 2에서 왕복 연료 계산 (50% 과소평가 수정)
- 🔧 **Call Duration**: Case 2에서 왕복 거리 반영

### v2.2 개선 (Config 구조 명확화)
- 🎯 **필드명 개선**: `case` → `single_case`, `cases_to_run` → `multi_cases`
- 🎯 **명확한 로직**: run_mode에 따라 어떤 필드가 사용되는지 명시
- 🎯 **후향 호환성**: 이전 필드명도 자동으로 변환

---

## Project Structure

```
D:\code\Green_Cor\
├── config/                          # YAML 설정 파일들
│   ├── base.yaml                    # 공통 파라미터
│   ├── case_1.yaml                  # Case 1: 부산항 저장소
│   ├── case_2_yeosu.yaml            # Case 2-1: 여수→부산
│   └── case_2_ulsan.yaml            # Case 2-2: 울산→부산
├── src/                             # Python 모듈
│   ├── __init__.py                  # 패키지 초기화
│   ├── config_loader.py             # YAML 설정 로더
│   ├── optimizer.py                 # MILP 최적화 엔진
│   ├── cost_calculator.py           # 비용 계산 모듈
│   └── utils.py                     # 유틸리티 함수
├── main.py                          # 단일 케이스 실행
├── run_all_cases.py                 # 다중 케이스 실행
├── results/                         # 결과 출력 폴더 (자동 생성)
├── requirements.txt                 # Python 의존성
├── claude.md                        # 이 파일
└── MILPmodel_v17_250811.py          # 원본 코드 (참조용)
```

---

## 시간 구조 (Time Structure)

### 중요: 시간 계산 vs 비용 계산

**모든 시간 계산은 육상 공급 시설을 포함합니다.**

- **시간 계산**: 항상 육상 적재 시간 포함 (예: Case 1 총 12.33h = 3.33h + 9.00h)
  - 모든 운영 제약 (constraint)에 사용됨
  - 연간 최대 항차, 활용도 계산에 사용됨
  - 모든 시나리오 (single, multi, case 1, 2)에서 일관적

- **비용 계산**: 육상 공급 시설의 CAPEX/OPEX는 config 옵션으로 포함/제외 가능
  - `shore_supply.enabled` = true: 육상 적재 시간은 포함, 비용도 포함
  - `shore_supply.enabled` = false: 육상 적재 시간은 포함, 비용만 제외 (참고용)
  - 현재: shore_supply.enabled = true (모든 경우 육상 포함)

**예시**: Case 1에서 5,000 m³ 셔틀 + 1,000 m³/h 펌프
```
시간 구조:
  - 육상 적재: 3.33h (Land Pump 1500 m³/h 사용) ← 항상 포함
  - 항해 + 벙커링 + 호스: 9.00h
  - 총 사이클: 12.33h ← 모든 계산에 사용

비용 계산:
  - 육상 적재 시간 비용: 포함 (shore_supply CAPEX/OPEX)
  - 나머지 비용: 셔틀, 펌프, 탱크 등
```

### Case 1: 부산항 내 셔틀 운영

**총 사이클 시간 구성**:
```
편도 이동 (부산항 내, 접안/계류 포함):        1시간
호스 연결 및 기체 퍼징:                      1시간
벙커링 시간 (연료 유체 흐름):                shuttle_size / pump_rate (시간)
호스 분리 및 암모니아 퍼징:                  1시간
부산항 내 회항 (편도 이동, 접안/계류):      1시간
──────────────────────────────────────
한 번의 완전한 사이클:                        3시간 + 펌핑시간

고정 시간 = 3시간 (이동 + 연결/해제)
펌핑 시간 = Shuttle_Size_m3 / Pump_Rate_m3ph
```

**육상 연료 공급 시간** (저장탱크에서 셔틀로 충전):
```
충전 시간 = Shuttle_Size_m3 / 1500 (고정값, m³/h)
예: 5000 m³ 셔틀 = 3.33시간
```

**예시 (5,000 m³ 셔틀, 1,000 m³/h 펌프)**:
```
육상 적재:                        3.33시간
편도 항해 (부산항 내 이동):       1.00시간
호스 연결 및 기체 퍼징:           1.00시간
벙커링 (선박 급유):              5.00시간 (5,000 ÷ 1,000)
호스 분리 및 암모니아 퍼징:       1.00시간
복귀 항해 (부산항 내 이동):       1.00시간
───────────────────────────────────────
기본 사이클 (육상 제외):           9.00시간
총 사이클 (육상 포함):            12.33시간

연간 최대 사이클: 8,000시간 ÷ 12.33시간 ≈ 649회
```

### Case 2: 여수/울산 → 부산 장거리 운송

**총 사이클 시간 구성**:
```
여수/울산에서 출발지 준비:                   1시간
근거지 육상 연료 탱크에서 적재:             shuttle_size / 1500 (시간)
여수 → 부산 편도 항해 (15노트):             여수: 5.63시간, 울산: 1.67시간
부산항 진입 및 대기:                        1시간
각 선박마다 반복 (vessels_per_trip회):
  - 부산항 이동 (접안/계류):                1시간
  - 호스 연결 및 기체 퍼징:                 1시간
  - 벙커링 시간 (vessel당):                 5000 / pump_rate (시간)
  - 호스 분리 및 암모니아 퍼징:             1시간
부산 → 여수/울산 편도 항해:                 여수: 5.63시간, 울산: 1.67시간
근거지 도착 및 정박:                        1시간
──────────────────────────────────────
한 번의 완전한 사이클:                        정상 시간 + (선박 수 × 펌핑 시간)
```

**예시 (Case 2-2: 울산, 25,000 m³ 셔틀, 1,000 m³/h 펌프, 5척 서빙)**:
```
울산 준비:           1시간
육상 적재:           16.67시간 (25,000 ÷ 1,500)
울산 → 부산:         1.67시간
부산 진입:           1시간
───────────────────────
[5척의 선박, 각각 5,000 m³씩]
  - 선박 1: 이동(1) + 연결(1) + 펌핑(5) + 해제(1) = 8시간
  - 선박 2~5: 동일하게 8시간씩 = 32시간
───────────────────────
부산 → 울산:         1.67시간
울산 도착:           1시간
───────────────────────
총 사이클:           63.01시간

연간 최대 항해: 8,000시간 ÷ 63시간 = 127회
```

**Case 2-1 (여수) vs Case 2-2 (울산) 시간 비교**:
```
여수 → 부산 편도: 5.63시간 vs 울산 → 부산: 1.67시간
───────────────────────────────────────────────
Case 2-1 총 사이클: ~75시간 (5척 서빙)
Case 2-2 총 사이클: ~63시간 (5척 서빙)

Case 2-2의 시간 절감: 12시간 (약 16% 단축)
연간 항해 능력: Case 2-1: 107회 < Case 2-2: 127회
```

---

## 세 가지 Case 설명

### Case 1: 부산항 저장소 기반
**시나리오**: 부산항에 대규모 저장 탱크가 있고, 셔틀이 탱크에서 선박으로 연료를 전달

| 항목 | 값 |
|-----|-----|
| **출발지** | 부산항 저장소 |
| **목적지** | 부산항 내 선박 |
| **거리** | 항만 내부 이동 (약 1시간, 접안/계류 포함) |
| **셔틀 크기** | 500 ~ 5000 m³ (10종류) |
| **저장 탱크** | 있음 (35,000톤) |
| **이동 시간** | 1.0 시간 |

**비용 구조**:
- CAPEX: 셔틀 + 펌프 + 저장 탱크
- OPEX: 셔틀 연료 + 펌프 전력 + 탱크 냉각

### Case 2-1: 여수 → 부산 (거리 기반)
**시나리오**: 여수의 암모니아 생산 시설에서 부산으로 셔틀이 대량 운송, 부산에는 저장시설 없음

| 항목 | 값 |
|-----|-----|
| **출발지** | 여수 (암모니아 생산시설) |
| **목적지** | 부산항 |
| **거리** | 86 해리 |
| **항해 속도** | 15 노트 |
| **이동 시간** | 86 / 15 ≈ 5.73시간 |
| **셔틀 크기** | 5000 ~ 50000 m³ (10종류) |
| **저장 탱크** | 없음 (출발지에만) |

### Case 2-2: 울산 → 부산 (근거리)
**시나리오**: 울산의 암모니아 시설에서 부산으로 근거리 운송

| 항목 | 값 |
|-----|-----|
| **출발지** | 울산 |
| **목적지** | 부산항 |
| **거리** | 25 해리 |
| **항해 속도** | 15 노트 |
| **이동 시간** | 25 / 15 ≈ 1.67시간 |
| **셔틀 크기** | 5000 ~ 50000 m³ (10종류) |
| **저장 탱크** | 없음 (출발지에만) |

---

## 설정 파일 (YAML) 구조

### base.yaml - 공통 파라미터

```yaml
time_period:
  start_year: 2030
  end_year: 2050

economy:
  discount_rate: 0.07              # 7% 할인율
  fuel_price_usd_per_ton: 600.0   # 암모니아 가격

shipping:
  kg_per_voyage: 2158995.0        # 항차당 연료량
  voyages_per_year: 12            # 선박당 연간 항차수
  start_vessels: 50               # 2030년 선박 수
  end_vessels: 500                # 2050년 선박 수

operations:
  travel_time_hours: [CASE별로 설정]
  travel_time_hours: 1.0          # Case 1 (부산항 내 이동)
  # 또는 5.73 (Case 2-1), 1.67 (Case 2-2)

  max_annual_hours_per_vessel: 8000  # 연간 최대 가동시간
  setup_time_hours: 0.5              # 호스 연결 시간
  tank_safety_factor: 2.0            # 탱크 여유계수
  daily_peak_factor: 1.5             # 일일 피크 계수
```

### case_X.yaml - 케이스별 파라미터

```yaml
case_name: "Case 1: Busan Port with Storage"
case_id: "case_1"

shuttle:
  available_sizes_cbm: [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]

  mcr_map_kw:  # MCR (최대 연속 정격) 값
    500: 1296
    1000: 1341
    ...
    4500: 1650      # 선형 보간
    5000: 1694      # 선형 보간

operations:
  travel_time_hours: 1.0           # 편도 이동 시간 (부산항 내 이동, 접안/계류 포함)
  has_storage_at_busan: true       # Case 1만 true

bunkering:
  k_voyages_per_call: 1
  bunker_volume_per_call_m3: 5000.0  # 콜당 급유량 (5000 m³로 변경)

tank_storage:
  enabled: true                      # Case 1만 enabled
  size_tons: 35000.0                 # 탱크 용량 (35,000톤)
```

---

## 사용 방법

### 1. 설치

```bash
# 의존성 설치
pip install -r requirements.txt

# Excel/Word 내보내기 (선택사항)
pip install openpyxl python-docx
```

### 2. Config를 통한 프로그램 제어

**모든 실행은 `config/base.yaml`의 `execution` 섹션에서 제어됩니다. CLI arguments를 사용하지 않습니다.**

#### base.yaml의 execution 섹션 (v2.3 - single_scenario 모드 추가)

```yaml
execution:
  # 실행 모드 선택: "single", "single_scenario", "all", "multiple"
  #
  # "single"           : 한 케이스의 모든 조합 실행 (90개 시나리오)
  #                     느리지만 전체 최적화 가능
  #
  # "single_scenario"  : 한 케이스의 특정 조합 1개만 실행 (빠른 시간 계산)
  #                     최적화 없이 지정된 셔틀+펌프의 시간만 계산
  #                     필수: single_case, single_scenario_shuttle_cbm, single_scenario_pump_m3ph
  #
  # "all"              : 모든 케이스의 모든 조합 실행 (매우 느림)
  #
  # "multiple"         : 특정 여러 케이스의 모든 조합 실행
  #                     multi_cases 리스트 사용
  run_mode: "single"

  # run_mode="single", "single_scenario", "all"일 때: 케이스 선택
  # 예시: "case_1", "case_2_yeosu", "case_2_ulsan"
  # run_mode="multiple"이면 이 필드는 무시됨
  single_case: "case_2_ulsan"

  # run_mode="single_scenario"일 때: 셔틀 크기 지정 (m³)
  # 예시: 500, 1000, 2000, 5000, 10000
  # run_mode="single_scenario"일 때만 사용
  single_scenario_shuttle_cbm: 5000

  # run_mode="single_scenario"일 때: 펌프 유량 지정 (m³/h)
  # 예시: 400, 600, 800, 1000, 1200, 1500, 2000
  # run_mode="single_scenario"일 때만 사용
  single_scenario_pump_m3ph: 1000

  # run_mode="multiple"일 때: 실행할 여러 케이스 지정
  # 예시: Case 1과 Case 2-2(울산)만 실행
  # run_mode="single", "single_scenario", "all"이면 무시됨
  multi_cases:
    - "case_1"
    - "case_2_ulsan"

  # 병렬 실행 작업자 수 (run_mode="all" 또는 "multiple"일 때만 사용)
  # 1 = 순차 실행 (느리지만 메모리 효율적)
  # >1 = 병렬 실행 (예: 4 = 4개 케이스 동시 실행)
  num_jobs: 1

  # 결과 저장 위치 (모든 모드)
  output_directory: "results"

  # 내보내기 형식 선택 (독립적으로 활성화/비활성화 가능)
  export:
    csv: true       # CSV 형식 (추천: 가볍고 빠름)
    excel: true     # Excel (.xlsx) 다중 시트
    docx: true      # Word 문서 (.docx) 전문 리포트
    pptx: false     # PowerPoint (미구현)
```

### 3. 실행 시나리오

#### 시나리오 1: Case 2-2 (울산) 단일 실행

```yaml
# config/base.yaml
execution:
  run_mode: "single"
  single_case: "case_2_ulsan"
  num_jobs: 1
  output_directory: "results"
  export:
    csv: true
    excel: true
    docx: true
```

```bash
python main.py
```

**출력**:
- `results/MILP_scenario_summary_case_2_ulsan.csv`
- `results/MILP_per_year_results_case_2_ulsan.csv`
- `results/MILP_results_case_2_ulsan.xlsx`
- `results/MILP_Report_case_2_ulsan.docx`

---

#### 시나리오 1-B: 단일 운항 시간 계산만 (빠른 실행)

**목적**: 특정 셔틀+펌프 조합의 1회 왕복 시간만 빠르게 계산
**특징**: 최적화 없이 지정된 조합만 계산 (2-3초)

```yaml
# config/base.yaml
execution:
  run_mode: "single_scenario"
  single_case: "case_2_ulsan"
  single_scenario_shuttle_cbm: 5000      # 5,000 m³ 셔틀
  single_scenario_pump_m3ph: 1000        # 1,000 m³/h 펌프
  num_jobs: 1
  output_directory: "results"
  export:
    csv: true
    excel: false
    docx: false
```

```bash
python main.py
```

**출력**:
- Console: 시간 정보 출력 (육상 적재, 항해, 호스, 펌핑 등)
- `results/time_calculation_case_2_ulsan_5000_1000.csv` (시간 상세 정보)

**사용 사례**:
- 빠른 시간 계산이 필요할 때
- 특정 조합의 시간만 확인하고 싶을 때
- 최적화 비용 없이 시간 분석만 필요할 때

```yaml
# 예시 1: Case 1 (부산) - 5,000 m³ + 2,000 m³/h
single_case: "case_1"
single_scenario_shuttle_cbm: 5000
single_scenario_pump_m3ph: 2000

# 예시 2: Case 2-1 (여수) - 10,000 m³ + 1,500 m³/h
single_case: "case_2_yeosu"
single_scenario_shuttle_cbm: 10000
single_scenario_pump_m3ph: 1500
```

---

#### 시나리오 2: 모든 케이스 실행 (순차)

```yaml
# config/base.yaml
execution:
  run_mode: "all"
  num_jobs: 1              # 순차 실행
  output_directory: "results"
  export:
    csv: true
    excel: true
    docx: false
```

```bash
python main.py
```

**출력** (3개 케이스 × 2 파일 = 6개 CSV):
- `results/MILP_scenario_summary_case_1.csv`
- `results/MILP_scenario_summary_case_2_yeosu.csv`
- `results/MILP_scenario_summary_case_2_ulsan.csv`
- (각 케이스마다 yearly results도 생성)

---

#### 시나리오 3: Case 1과 Case 2-2만 병렬 실행

```yaml
# config/base.yaml
execution:
  run_mode: "multiple"
  multi_cases:
    - "case_1"
    - "case_2_ulsan"
  num_jobs: 4              # 4개 프로세스 병렬 (실제로는 2개만 사용)
  output_directory: "results"
  export:
    csv: true
    excel: true
    docx: true
```

```bash
python main.py
# 또는
python run_all_cases.py
```

**특징**:
- 2개 케이스를 병렬로 실행
- `run_all_cases.py` 사용하면 더 효율적인 병렬화
- 결과 요약: `results/MILP_cases_summary.csv`

---

#### 시나리오 4: 최대 병렬 실행 (모든 케이스, 4 프로세스)

```yaml
# config/base.yaml
execution:
  run_mode: "all"
  num_jobs: 4              # 최대 4개 케이스 동시 실행
  output_directory: "results"
  export:
    csv: true
    excel: true
    docx: true
```

```bash
python run_all_cases.py
```

**성능**:
- 순차 (1 job): ~5분 (3 케이스)
- 병렬 (4 jobs): ~2분

### 4. 결과 해석

실행 후 `results/` 디렉토리에 다음 파일이 생성됩니다:

#### MILP_scenario_summary_case_X.csv
- 각 셔틀/펌프 조합별 NPC 요약
- 컬럼:
  - `Shuttle_Size_cbm`: 셔틀 크기 (m³)
  - `Pump_Size_m3ph`: 펌프 용량 (m³/h)
  - `NPC_Total_USDm`: 20년 순현재가 (백만 USD)
  - `NPC_Shuttle_CAPEX_USDm`: 셔틀 자본비
  - `NPC_Bunkering_CAPEX_USDm`: 벙커링 장비 자본비
  - `NPC_Terminal_CAPEX_USDm`: 탱크 자본비
  - (각 항목별 고정/변동 OPEX)

#### MILP_per_year_results_case_X.csv
- 연도별 상세 결과 (2030-2050)
- 컬럼:
  - `Year`: 연도
  - `New_Shuttles`: 당해 신규 추가 셔틀 수
  - `Total_Shuttles`: 누적 셔틀 수
  - `Annual_Calls`: 연간 벙커링 횟수
  - `Supply_m3`: 연간 공급량
  - `Demand_m3`: 연간 수요량
  - `Utilization_Rate`: 활용도

---

## 기술 세부 사항

### MILP 모델 구조

**목적함수**:
```
Minimize: NPV = Σ_t [DISC_FACTOR(t) × (CAPEX(t) + FIXED_OPEX(t) + VARIABLE_OPEX(t))]

where:
- DISC_FACTOR(t) = 1 / (1 + r)^(t - 2030)  (할인율 r=7%)
- CAPEX(t) = 셔틀CAPEX × x_t + 벙커링CAPEX × x_t + 탱크CAPEX × z_t
- FIXED_OPEX(t) = 셔틀고정운영비 × N_t + 벙커링고정운영비 × N_t + 탱크고정운영비 × Z_t
- VARIABLE_OPEX(t) = 셔틀연료비 + 펌프연료비 + 탱크냉각비
```

**결정변수**:
- `x[t]`: t년도 신규 추가 셔틀 수 (정수)
- `N[t]`: t년도 누적 셔틀 수 (정수)
- `y[t]`: t년도 연간 벙커링 횟수 (연속)
- `z[t]`: t년도 신규 추가 탱크 수 (정수)
- `Z[t]`: t년도 누적 탱크 수 (정수)

**주요 제약식**:
1. **누적 제약**: N[t] = N[t-1] + x[t]
2. **수요 충족**: y[t] × BUNKER_VOL ≥ DEMAND[t]
3. **작업시간**: y[t] × trips_per_call × cycle_time ≤ N[t] × H_max
4. **탱크 용량**: N[t] × shuttle_size × β ≤ Z[t] × tank_volume (Case 1만)
5. **일일 피크**: daily_capacity ≥ daily_demand × F_peak

### MCR 보간

셔틀 크기별 MCR(최대 연속 정격) 값:
- 기존 데이터: 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000 m³
- **새로 추가**: 4500, 5000 m³ (선형 보간)
- **Case 2 추가**: 10000~50000 m³ (로그 외삽)

**보간 공식**:
```
MCR(4500) = MCR(4000) + (MCR(5000) - MCR(4000)) × (4500 - 4000) / (5000 - 4000)
          = 1606 + (1694 - 1606) × 0.5
          = 1650 kW
```

### 비용 계산

**셔틀 CAPEX** (자본비):
```
CAPEX[i] = ref_capex × (size[i] / ref_size)^α
         = 61,500,000 × (size / 40,000)^0.75
```

**펌프 CAPEX**:
```
pump_power = ΔP × Q / (η × 1000)  [kW]
           = (4 bar × 100,000 Pa) × (Q / 3600) / 0.7 / 1000

CAPEX = pump_power × 2,000 USD/kW
```

**탱크 CAPEX** (35,000톤):
```
CAPEX = 35,000 tons × 1,000 kg/ton × 1.215 USD/kg
      = 42,525,000 USD per tank
```

**연료비** (변동 OPEX):
```
shuttle_fuel_per_cycle = MCR × SFOC × travel_time / 1e6  [ton]
                       = 1300 × 379 × 2 / 1e6 ≈ 0.985 ton

pump_fuel_per_call = pump_power × pumping_time × SFOC / 1e6  [ton]
                   = 400 × 1.5 × 379 / 1e6 ≈ 0.227 ton
```

---

## 파이썬 모듈 설명

### src/config_loader.py
- YAML 파일 로드 및 병합
- 설정 검증
- ConfigLoader 클래스 제공

### src/cost_calculator.py
- CAPEX/OPEX 계산
- 비용 요소별 분해
- CostCalculator 클래스 제공

### src/optimizer.py
- MILP 모델 구축 및 풀이
- PuLP 기반 최적화
- BunkeringOptimizer 클래스 제공

### src/utils.py
- MCR 보간/외삽
- 선박 성장 계산
- 수요 계산
- 유틸리티 함수 모음

---

## 출력 예시

```
============================================================
Case: Case 1: Busan Port with Storage
============================================================
[SOLVER] H=500, P=400 -> Optimal
[SOLVER] H=500, P=600 -> Optimal
...
Progress: 10/72 (13.9%)
...
Optimization complete. Feasible solutions: 42

============================================================
Top 10 Scenarios (by NPC)
============================================================
 Shuttle_Size_cbm  Pump_Size_m3ph  NPC_Total_USDm  NPC_Shuttle_CAPEX_USDm  NPC_Bunkering_CAPEX_USDm
              3500            1200         2584.32                   452.10                    143.67
              3000            1200         2651.45                   412.32                    143.67
              4000            1000         2698.12                   485.23                    127.45
              ...
```

---

## 변경 가능한 변수 목록 (Configurable Variables)

본 모델에서 사용자가 YAML 파일을 통해 직접 조정 가능한 변수들:

### 1. 셔틀 (Shuttle) 파라미터
- **가용 크기**: Case 1: 500~5,000 m³, Case 2: 5,000~50,000 m³
- **MCR (최대 연속 정격)**: 셔틀 크기별 엔진 파워 (kW)
  - 기본값: 기존 데이터 + 선형 보간(4500, 5000) + 로그 외삽(Case 2)
  - 수정 가능: case_X.yaml의 mcr_map_kw 수정

### 2. 펌프 (Pump) 파라미터
- **가용 유량**: 400, 600, 800, 1,000, 1,200, 1,400, 1,600, 1,800, 2,000 m³/h
  - 기본 9종 모두 최적화 대상
  - 특정 펌프 크기만 사용하고 싶으면 base.yaml의 pumps.available_flow_rates 수정

### 3. 저장탱크 (Tank) 파라미터 (Case 1만)
- **탱크 용량**: 기본값 35,000톤
  - config/case_1.yaml의 tank_storage.size_tons 수정
  - 예: 40,000톤, 50,000톤 등으로 변경 가능
- **냉각 에너지**: 0.0378 kWh/kg (암모니아 냉각 유지용)
- **여유 계수**: 2.0배 (안전 재고, 1.5~3.0 범위)
  - config/base.yaml의 operations.tank_safety_factor 수정

### 4. 시간 파라미터 (Time-related)
- **Case 1 편도 이동 시간**: 기본값 2.0시간 (항만 내부)
  - operations.travel_time_hours
- **Case 2 항해 거리 기반**:
  - Case 2-1 (여수): 86해리 → 5.63시간 (자동 계산)
  - Case 2-2 (울산): 25해리 → 1.67시간 (자동 계산)
- **호스 연결/해제 시간**: 각 0.5시간 (총 1시간)
  - operations.setup_time_hours (기본값 0.5시간)
- **육상 연료 공급 펌프 유량**: 1,500 m³/h (고정값, 변경 가능)
  - config/base.yaml의 shore_supply_pump_rate_m3ph

### 5. 경제 파라미터
- **할인율**: 기본값 7%
  - economy.discount_rate
- **암모니아 연료 가격**: 기본값 600 USD/톤
  - economy.fuel_price_usd_per_ton
- **전기요금**: 기본값 0.0769 USD/kWh
  - economy.electricity_price_usd_per_kwh
- **유지보수비율**:
  - 셔틀: CAPEX의 5%
  - 펌프: CAPEX의 5%
  - 탱크: CAPEX의 3%

### 6. 수요 예측 파라미터
- **초기 선박 수 (2030년)**: 50척
  - shipping.start_vessels
- **최종 선박 수 (2050년)**: 500척
  - shipping.end_vessels
- **항차당 연료량**: 기본값 5,000 m³
  - bunkering.bunker_volume_per_call_m3
- **선박당 연간 항차**: 12회
  - shipping.voyages_per_year
- **최대 연간 운영시간**: 8,000시간/년 (선박당)
  - operations.max_annual_hours_per_vessel

---

## 도출 결과 목록 (Output Results)

최적화 실행 후 다음과 같은 결과가 생성됩니다:

### 1. 최적 Shuttle 크기 및 개수
- **선택된 셔틀 크기**: 500~5,000 m³ (Case 1) 또는 5,000~50,000 m³ (Case 2)
- **연도별 누적 셔틀 수**: 2030년부터 2050년까지의 선박 증감 일정
- **신규 추가 셔틀 수**: 각 연도의 추가 구매 필요 선박 수

**예시 출력** (MILP_per_year_results_case_X.csv):
```
Year,New_Shuttles,Total_Shuttles,Annual_Calls
2030,1,1,382
2035,2,3,896
2040,2,5,1410
2050,5,15,2856
```

### 2. 최적 펌프 유량
- **선택된 펌프 크기**: 400~2,000 m³/h 중 최적값
- **벙커링 시간 단축**: 펌프 크기에 따른 사이클 타임 감소
- **CAPEX vs OPEX 트레이드오프**:
  - 큰 펌프: 시간 단축 → 운영비 감소, 장비비 증가
  - 작은 펌프: 시간 증가 → 셔틀 수 증가, 장비비 감소

**선택 기준**:
```
pump_size = argmin(NPC)
           = min(CAPEX(pump) + OPEX(all components))

결과: 대부분 1,000~1,200 m³/h가 최적
```

### 3. 연도별 총 비용 (Annualized)
생성되는 파일: MILP_per_year_results_case_X.csv

**비용 항목별 분해**:
```
2030년 예시:
├── CAPEX (자본비)
│   ├── 셔틀 신규 구매: $18,917,000 × 1척 = $18.9M
│   ├── 펌프: $505,600
│   └── 탱크 (Case 1): $42,525,000
│   총 CAPEX: $62.0M (2030년)
│
├── 고정 OPEX (유지보수비)
│   ├── 셔틀: $945,850/년
│   ├── 펌프: $25,280/년
│   └── 탱크: $1,275,750/년
│   총 고정: $2.2M/년
│
└── 변동 OPEX (연료비, 에너지비)
    ├── 셔틀 연료: $293,000/년
    ├── 펌프 에너지: $219,500/년
    └── 탱크 냉각: $104,400/년
    총 변동: $616,900/년
```

### 4. 선박 연료 암모니아 1톤당 가격 (LCOAmmonia)
**계산식**:
```
LCOA = (20년 NPC 할인액) / (20년 총 공급량)
     = Σ_t [Discount(t) × (CAPEX(t) + OPEX(t))] / Σ_t [Supply(t)]
     = [USD] / [ton]
```

**예시**:
```
Case 1 (부산 저장소):   LCOA ≈ $280~350/ton
Case 2-2 (울산):      LCOA ≈ $200~270/ton
Case 2-1 (여수):      LCOA ≈ $220~290/ton

참고: 시장가 600 USD/ton 대비
20년 평균 추가 비용: 30~58%
```

### 5. 항차별 평균 시간 (Average Call Duration)
각 벙커링 콜(Case 1) 또는 항해(Case 2)의 평균 소요 시간

**Case 1 예시** (5,000 m³ 셔틀, 1,000 m³/h 펌프):
```
육상 적재:    3.33시간
셔틀 항해:    2시간 (편도 × 2)
호스 작업:    1시간
벙커링:       5시간
──────────
총 시간:     11.33시간 (1회 완전 사이클)

그러나 "콜"의 정의: 1회 선박 급유
→ 콜당 시간 = 11.33 / (1회 왕복당 콜 수)
             = 11.33 / 1 = 11.33시간/콜
```

**Case 2-2 예시** (25,000 m³ 셔틀, 1,000 m³/h 펌프):
```
근거지 준비:  1시간
육상 적재:    16.67시간
항해:         3.34시간 (편도 × 2)
선박 서빙:    40시간 (5척 × 8시간)
──────────
총 시간:     61시간/항해

항해당 서빙 선박: 5척
→ 항해당 평균: 61 / 5 = 12.2시간/선박
```

### 6. 결과 파일 형식

#### MILP_scenario_summary_case_X.csv
```
Shuttle_Size_cbm,Pump_Size_m3ph,NPC_Total_USDm,NPC_Shuttle_CAPEX_USDm,...
3000,1000,2651.45,412.32,...
3500,1200,2584.32,452.10,...
5000,1000,2698.12,485.23,...
```

#### MILP_per_year_results_case_X.csv
```
Year,New_Shuttles,Total_Shuttles,Annual_Calls,Supply_m3,Demand_m3,Utilization_Rate
2030,1,1,382,1910000,1905000,0.997
2031,1,2,764,3820000,3810000,0.997
```

#### MILP_cases_summary.csv (다중 케이스)
```
Case,Shuttle_Size_cbm,Pump_Size_m3ph,NPC_Total_USDm,Ranking
case_1,5000,1000,2698.12,1
case_2_ulsan,5000,1000,1884.56,2
case_2_yeosu,5000,1000,2015.23,3
```

---

## 코드 구조 개선 계획 (Code Architecture Refactoring)

### v2.3 예정 사항: 모듈화 및 구조 개선

#### 1. 육상 연료 공급 모듈 분리 (Shore Supply Module)

**현재 구조**:
- 육상 연료 공급 로직이 optimizer.py에 섞여있음
- Case별로 다르게 적용되지 않음

**개선된 구조**:
```
src/
├── shore_supply.py         [새 파일] 육상 연료 공급 관리
│   ├── ShoreSupply 클래스
│   ├── load_shuttle()      셔틀 적재 시간 계산
│   ├── unload_shuttle()    셔틀 언로드 시간 계산
│   └── is_shore_supply_enabled()
│
├── config_loader.py        (수정)
│   └── shore_supply 섹션 추가
│
├── optimizer.py            (수정)
│   └── ShoreSupply 인스턴스 호출
│
└── base.yaml               (수정)
    └── shore_supply:
          enabled: true/false
          pump_rate_m3ph: 1500
```

**설정 파일 (config/base.yaml)**:
```yaml
shore_supply:
  enabled: true                    # 활성화/비활성화
  pump_rate_m3ph: 1500            # 육상 펌프 유량
  loading_time_fixed_hours: 0      # 추가 고정 시간
```

**사용 예시**:
```python
# Case 1: 부산 저장탱크에서 적재 (활성화)
# Case 2: 근거지 탱크에서 적재 (활성화)

if config['shore_supply']['enabled']:
    shore_supply = ShoreSupply(config)
    load_time = shore_supply.load_shuttle(shuttle_size, pump_rate)
    cycle_time += load_time
```

#### 2. 핵심 시간 로직 라이브러리화 (Core Time Calculation Library)

**목표**: 1개 셔틀 왕복 시간 계산을 핵심 로직으로 독립화

**새로운 파일**: `src/cycle_time_calculator.py`

```python
class CycleTimeCalculator:
    """
    한 번의 완전한 셔틀 왕복 사이클 시간 계산
    """

    def __init__(self, case_type, config):
        self.case_type = case_type  # "case_1", "case_2_yeosu", "case_2_ulsan"
        self.config = config

    def calculate_single_cycle(self, shuttle_size, pump_rate, num_vessels=1):
        """
        단일 사이클 타임 계산 (모든 Case에 공통 적용)

        Parameters:
        -----------
        shuttle_size : float
            셔틀 용량 (m³)
        pump_rate : float
            펌프 유량 (m³/h)
        num_vessels : int
            한 항해에 서빙하는 선박 수 (Case 2에서만 사용, 기본값 1)

        Returns:
        --------
        dict : {
            'shore_loading': 시간,
            'travel_outbound': 시간,
            'setup_inbound': 시간,
            'pumping': 시간,
            'setup_outbound': 시간,
            'travel_return': 시간,
            'shore_unloading': 시간,
            'total': 시간
        }
        """
        pass
```

**구현 로직**:

Case 1용:
```python
def calculate_single_cycle_case1(self, shuttle_size, pump_rate):
    shore_loading = shuttle_size / 1500
    travel_outbound = 1.0
    setup = 1.0
    pumping = shuttle_size / pump_rate
    travel_return = 1.0
    shore_unloading = 0  # Case 1에서는 펌핑 후 바로 복귀

    return {
        'shore_loading': shore_loading,
        'travel': travel_outbound + travel_return,
        'setup': setup,
        'pumping': pumping,
        'total': shore_loading + travel_outbound + setup + pumping + travel_return
    }
```

Case 2용:
```python
def calculate_single_cycle_case2(self, shuttle_size, pump_rate, num_vessels):
    shore_loading = shuttle_size / 1500
    travel_outbound = self.config['operations']['travel_time_hours']
    port_entry = 1.0

    # 각 선박마다의 시간 (반복)
    per_vessel = 1.0 + 1.0 + (5000 / pump_rate) + 1.0  # 이동+연결+펌핑+해제
    pumping_total = per_vessel * num_vessels

    travel_return = self.config['operations']['travel_time_hours']

    return {
        'shore_loading': shore_loading,
        'travel_outbound': travel_outbound,
        'port_entry': port_entry,
        'per_vessel_time': per_vessel,
        'pumping_total': pumping_total,
        'travel_return': travel_return,
        'total': shore_loading + travel_outbound + port_entry + pumping_total + travel_return
    }
```

#### 3. Case별 최적화 호출 구조

**현재 구조** (optimizer.py):
```python
class BunkeringOptimizer:
    def __init__(self, config):
        # 모든 로직이 혼합됨

    def _solve_combination(self, shuttle_size, pump_size):
        # Case 구분이 scattered
        if self.has_storage_at_busan:
            trips = ceil(bunker_vol / shuttle_size)
        else:
            vessels = floor(shuttle_size / bunker_vol)
```

**개선된 구조** (v2.3):
```python
class BunkeringOptimizer:
    def __init__(self, config):
        self.case_type = config['case_id']
        self.cycle_calculator = CycleTimeCalculator(self.case_type, config)

    def _solve_combination(self, shuttle_size, pump_size):
        # 핵심 계산을 라이브러리에 위임
        cycle_info = self.cycle_calculator.calculate_single_cycle(
            shuttle_size,
            pump_size,
            num_vessels=self._calculate_vessels_per_trip(shuttle_size)
        )

        # Case별 제약식 적용
        if self.case_type == 'case_1':
            self._apply_case1_constraints(cycle_info)
        elif self.case_type in ['case_2_yeosu', 'case_2_ulsan']:
            self._apply_case2_constraints(cycle_info)
```

#### 4. 일일 피크 제약 삭제

**현재 상태**:
- 2.6.3절에서 일일 피크 제약식 존재:
  ```
  Daily_Capacity >= Daily_Demand × 1.5
  ```

**삭제 이유**:
- 작업시간 제약(2.6.2)과 중복
- 평균 수요 기반 일일 피크 가정이 비현실적
- 실제 선박 스케줄은 예약 시스템으로 관리 가능

**삭제 계획**:
1. `src/optimizer.py` 라인 280-290 제약식 제거
2. `PROJECT_ANALYSIS_REPORT.md` 2.6.3절 삭제
3. 세 Case 비교 테이블 업데이트 (제약식 개수 감소)

**수정 후**:
```python
# 제약식: 작업시간 제약만 남음 (이미 peak 처리 포함)
y[t] × Trips_per_Call × Cycle_Duration <= N[t] × 8,000
```

#### 5. YAML 설정 최적화

**Base.yaml 확장**:
```yaml
execution:
  # ... 기존 필드 ...

time_structure:
  case_1:
    travel_time_hours: 2.0
    setup_time_hours: 0.5
  case_2_yeosu:
    travel_time_hours: 5.63
    setup_time_hours: 0.5
  case_2_ulsan:
    travel_time_hours: 1.67
    setup_time_hours: 0.5

shore_supply:
  enabled: true
  pump_rate_m3ph: 1500

cycle_calculation:
  method: "lib"  # "lib" (라이브러리) or "legacy" (기존 방식)
```

#### 6. 구현 순서

**Phase 1 (v2.3.1)**: 기초 작업
- [ ] CycleTimeCalculator 클래스 구현
- [ ] ShoreSupply 클래스 구현
- [ ] 단위 테스트 작성

**Phase 2 (v2.3.2)**: 통합
- [ ] optimizer.py 리팩토링 (라이브러리 호출)
- [ ] 일일 피크 제약 삭제
- [ ] 회귀 테스트 (기존 결과와 동일 확인)

**Phase 3 (v2.3.3)**: 문서화
- [ ] CLAUDE.md 업데이트
- [ ] PROJECT_ANALYSIS_REPORT.md 업데이트
- [ ] 코드 주석 추가

---

## 주요 파라미터 변경 가이드

모든 파라미터는 YAML 설정 파일에서 변경하며, 프로그램을 재시작한 후 실행하면 됩니다.

### 1. 실행 제어 (config/base.yaml)

#### 케이스 선택
```yaml
execution:
  case: "case_2_yeosu"  # case_1, case_2_yeosu, case_2_ulsan
  run_mode: "single"
```

#### 병렬 실행 (4개 CPU 사용)
```yaml
execution:
  run_mode: "multiple"
  cases_to_run:
    - "case_1"
    - "case_2_yeosu"
  num_jobs: 4
```

#### 출력 형식 변경
```yaml
execution:
  export:
    csv: true      # 항상 생성
    excel: true    # Excel 다중 시트
    docx: true     # Word 리포트
```

---

### 2. 경제 파라미터 (config/base.yaml)

#### 1항차 급유량 변경
```yaml
# config/case_1.yaml (케이스별로 다를 수 있음)
bunkering:
  bunker_volume_per_call_m3: 5000.0  # 변경 가능 (현재: 5000)
```

#### 할인율 변경
```yaml
# config/base.yaml
economy:
  discount_rate: 0.05  # 5% (기본: 7%)
  discount_rate: 0.10  # 10%
```

#### 연료 가격 변경
```yaml
# config/base.yaml
economy:
  fuel_price_usd_per_ton: 500.0  # USD/ton (기본: 600)
```

#### 전기요금 변경
```yaml
# config/base.yaml
economy:
  electricity_price_usd_per_kwh: 0.10  # USD/kWh (기본: 0.0769)
```

---

### 3. 운영 파라미터 (config/base.yaml)

#### 선박 수요 변경
```yaml
shipping:
  start_vessels: 50    # 2030년 선박 수 (기본: 50)
  end_vessels: 500     # 2050년 선박 수 (기본: 500)
```

#### 최대 연간 작업시간 변경
```yaml
operations:
  max_annual_hours_per_vessel: 8000.0  # 시간/년 (기본: 8000)
```

#### 탱크 여유계수 변경
```yaml
operations:
  tank_safety_factor: 2.0  # 2배 여유 (기본: 2.0, 범위: 1.5~3.0)
```

#### 일일 피크 계수 변경
```yaml
operations:
  daily_peak_factor: 1.5  # 일일 피크의 1.5배 (기본: 1.5)
```

---

### 4. 셔틀 및 펌프 (config/case_X.yaml)

#### 사용 가능한 셔틀 크기 변경
```yaml
# config/case_1.yaml
shuttle:
  available_sizes_cbm:
    - 500
    - 1000
    - 2000     # 1500 제외하고 싶다면
    - 3000
    # ... 원하는 크기만 선택
```

#### MCR 값 커스터마이징
```yaml
# config/case_2_yeosu.yaml
shuttle:
  mcr_map_kw:
    5000: 1694
    10000: 2159
    15000: 2485
    # ... 사용자 정의 값으로 변경
```

#### 펌프 유량 범위 변경
```yaml
# config/base.yaml
pumps:
  available_flow_rates:
    - 400
    - 600
    - 800
    # ... 큰 펌프 제외하고 싶으면 제거
```

---

### 5. 탱크 저장소 (config/base.yaml)

#### 탱크 크기 변경
```yaml
tank_storage:
  size_tons: 35000.0  # 톤 (기본: 35,000)
  size_tons: 40000.0  # 더 큰 탱크
```

#### 탱크 냉각비용 변경
```yaml
tank_storage:
  cooling_energy_kwh_per_kg: 0.0378  # kWh/kg (기본: 0.0378)
```

---

### 예제: Case 커스터마이징

Case 1을 기반으로 더 큰 선박 수를 가정하는 새 케이스 만들기:

```yaml
# config/case_1_large_demand.yaml
case_name: "Case 1: Large Demand Scenario"
case_id: "case_1_large"

# case_1.yaml의 모든 설정 상속, 다음만 변경:
# (아래만 추가하면 base.yaml + case_1.yaml + 이 파일이 병합됨)
```

그 다음 base.yaml에서:
```yaml
execution:
  case: "case_1_large"
  run_mode: "single"
```

```bash
python main.py
```

---

## 문제 해결

### 1. "No module named 'pulp'" 오류
```bash
pip install pulp
```

### 2. "Config file not found" 오류
현재 디렉토리 확인 및 config 폴더 위치 확인:
```bash
ls config/  # 또는 dir config (Windows)
```

### 3. 최적해 없음 (Infeasible)
다음 중 하나 시도:
- 최대 작업시간 (H_max) 증가
- 72시간 콜 제약 완화
- 펌프 크기 증가
- 셔틀 크기 증가

### 4. 느린 실행 속도
- 셔틀/펌프 조합 줄이기
- 시간 해상도 낮추기 (5년 간격으로)
- 병렬 처리 사용 (run_all_cases.py --jobs 4)

---

## 개발 및 확장

### 새로운 케이스 추가

1. `config/case_X.yaml` 파일 생성
2. 파라미터 설정 (travel_time_hours, shuttle sizes, MCR map 등)
3. 실행:
```bash
python main.py --case case_X
```

### 새로운 제약식 추가

`src/optimizer.py`의 `_solve_combination` 메서드에서:
```python
# 기존 제약식들...

# 새 제약식 추가
prob += some_condition_expression
```

### 결과 시각화 추가

`main.py` 또는 `src/optimizer.py`에 matplotlib 코드 추가:
```python
import matplotlib.pyplot as plt

# Top 10 시나리오 시각화
scenario_df.nsmallest(10, "NPC_Total_USDm").plot(...)
```

---

## 참고 문헌

- **원본 모델**: MILPmodel_v17_250811.py (2025-08-10)
- **최적화 라이브러리**: PuLP (https://coin-or.github.io/pulp/)
- **솔버**: CBC (Coin-or Branch and Cut)

---

## 라이선스 및 저작권

Green Corridor Research Team, 2025

---

## 지원 및 문의

현재 구조 및 사용법에 대한 질문은 프로젝트 문서를 참조하세요.

문제 발생 시:
1. 설정 파일 검증 (config/*.yaml)
2. 의존성 확인 (pip list)
3. 로그 확인 및 재실행

---

## v2.1 개선사항 (Case 2 벙커링 로직 수정)

### 문제점 분석

v2.0에서 Case 2 (여수→부산, 울산→부산) 의 벙커링 로직이 잘못 구현되었습니다:

**기존 로직의 오류**:
```python
# 잘못된 코드 (Line 165)
trips_per_call = int(ceil(bunker_volume_per_call / shuttle_size))
```

이 로직은 **Case 1 시나리오에만 맞습니다**:
- Case 1: 500 m³ 셔틀이 5,000 m³ 콜을 여러 트립으로 나눠서 충족 (O)
- Case 2: 25,000 m³ 셔틀 = ceil(5000/25000) = 1 트립 (X)
  - 25,000 m³ 셔틀이 5,000 m³만 운반하므로 **용량 80% 낭비**
  - 5,000과 25,000 m³ 셔틀이 동일하게 평가됨 (비현실적)

### 수정 내용

**1. 초기화 부분 추가 (src/optimizer.py Line 106)**
```python
self.has_storage_at_busan = self.config["operations"].get("has_storage_at_busan", True)
```
- `has_storage_at_busan` 플래그로 Case 1과 Case 2 구분
- Case 1: True (부산에 저장탱크 있음)
- Case 2: False (부산에 저장탱크 없음, 여수/울산 출발지에만 있음)

**2. 트립 계산 로직 수정 (src/optimizer.py Lines 165-176)**
```python
if self.has_storage_at_busan:
    # Case 1: 소형 셔틀이 콜당 여러 번 왕복
    trips_per_call = int(ceil(bunker_volume_per_call / shuttle_size))
    volume_per_trip = shuttle_size
else:
    # Case 2: 대형 셔틀이 한 번의 왕복으로 여러 척 급유
    vessels_per_trip = max(1, int(shuttle_size // bunker_volume_per_call))
    trips_per_call = 1  # 한 번의 왕복
    volume_per_trip = shuttle_size  # 전체 용량 운반
```

**예제**:
- 5,000 m³ 셔틀: 1척 급유 (5,000 ÷ 5,000 = 1)
- 25,000 m³ 셔틀: 5척 급유 (25,000 ÷ 5,000 = 5)
- 50,000 m³ 셔틀: 10척 급유 (50,000 ÷ 5,000 = 10)

**3. 펌핑 시간 계산 수정 (src/optimizer.py Lines 184-187)**
```python
if self.has_storage_at_busan:
    pumping_time_hr_call = 2.0 * (self.bunker_volume_per_call_m3 / pump_size)
else:
    pumping_time_hr_call = 2.0 * (shuttle_size / pump_size)
```
- Case 2: 전체 셔틀 용량을 펌핑하는 시간 계산

**4. 수요 충족 제약식 수정 (src/optimizer.py Lines 263-269)**
```python
if self.has_storage_at_busan:
    prob += y[t] * self.bunker_volume_per_call_m3 >= self.annual_demand[t]
else:
    prob += y[t] * shuttle_size >= self.annual_demand[t]
```
- Case 2: y[t]는 "트립 수"이므로 shuttle_size 전체를 전달

**5. 일일 피크 제약식 수정 (src/optimizer.py Lines 282-285)**
```python
if self.has_storage_at_busan:
    daily_demand = (y[t] / 365.0) * self.bunker_volume_per_call_m3 * self.daily_peak_factor
else:
    daily_demand = (y[t] / 365.0) * shuttle_size * self.daily_peak_factor
```

### 결과 영향

수정 후 Case 2 결과:
- **가능한 조합 감소**: 90개 → 62-64개 (일부 조합이 현재 실행 불가능)
- **대형 셔틀의 정확한 비용 평가**: 이제 대형 셔틀의 효율성이 올바르게 반영됨
- **최적해는 유지**: Case 2-2 (울산)의 최적해는 여전히 5,000 m³ + 2,000 m³/h
  - $94.9M NPC (Case 1 대비 -38.2% 여전히 최적)

### 설정 파일 확인

모든 설정 파일에서 `has_storage_at_busan` 값이 올바르게 설정됨:
- `config/case_1.yaml`: `has_storage_at_busan: true`
- `config/case_2_yeosu.yaml`: `has_storage_at_busan: false`
- `config/case_2_ulsan.yaml`: `has_storage_at_busan: false`

### 다음 단계

1. ✅ Case 2 벙커링 로직 수정 완료
2. ✅ 최적화 재실행 및 검증
3. ✅ 분석 시각화 재생성
4. 추가 개선사항 필요시 구현 예정

---

---

## v2.2 개선사항 (Config 구조 명확화)

### 문제점

v2.0-v2.1의 Config 구조가 혼동스러웠습니다:

```yaml
# 혼동스러운 구조
execution:
  case: "case_1"              # case vs single_case?
  run_mode: "single"
  cases_to_run: [...]         # cases_to_run vs multi_cases?
```

- `case`와 `cases_to_run`: 필드명이 유사해서 혼동
- `run_mode`와 실제 사용되는 필드의 관계가 불명확
- 어떤 필드를 언제 설정해야 하는지 불명확

### 해결책

필드명 명확화 및 구조 개선:

```yaml
# v2.2: 명확한 구조
execution:
  run_mode: "single"        # single, all, multiple

  # run_mode="single" 전용
  single_case: "case_2_ulsan"

  # run_mode="multiple" 전용
  multi_cases:
    - "case_1"
    - "case_2_ulsan"
```

### 변경 내용

**1. base.yaml 필드명 변경**
- `case` → `single_case` (더 명확한 의도)
- `cases_to_run` → `multi_cases` (단수/복수 구분 명확)

**2. main.py 및 run_all_cases.py 로직 업데이트**
- 새 필드명 적용
- 주석 개선으로 각 필드의 용도 명시

**3. config_loader.py 후향 호환성 추가**
```python
# 이전 필드명도 자동으로 변환
if "case" in execution_config and "single_case" not in execution_config:
    execution_config["single_case"] = execution_config["case"]

if "cases_to_run" in execution_config and "multi_cases" not in execution_config:
    execution_config["multi_cases"] = execution_config["cases_to_run"]
```

기존 설정 파일도 자동으로 변환되므로 업데이트 불필요!

### 사용 예시

**명확한 구조로 설정:**

```yaml
# Case 2-2 단일 실행
execution:
  run_mode: "single"
  single_case: "case_2_ulsan"  # ← 단 한 개 케이스

# 모든 케이스 병렬 실행
execution:
  run_mode: "all"
  num_jobs: 4                  # ← multi_cases 필드 불필요

# 특정 여러 케이스만 실행
execution:
  run_mode: "multiple"
  multi_cases:                 # ← 여러 케이스 명시
    - "case_1"
    - "case_2_ulsan"
```

### 호환성

✅ **이전 설정 파일도 그대로 작동**
- v2.0-v2.1 설정 → 자동 변환
- 업데이트 불필요

✅ **모든 코드 수정 완료**
- main.py: 새 필드명 적용
- run_all_cases.py: 새 필드명 적용
- config_loader.py: 후향 호환성 추가

---

**마지막 업데이트**: 2025-11-17 (v2.2 - Config 구조 명확화 + v2.1 Case 2 버그 수정)
