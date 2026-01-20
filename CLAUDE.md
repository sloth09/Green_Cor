# Green Corridor Ammonia Bunkering Optimization Model

## Overview

이 프로젝트는 부산항에서의 암모니아 연료 공급 인프라를 최적화하기 위한 MILP(혼합정수선형계획) 모델입니다.

**목표**: 2030~2050년 20년 동안 친환경 해운 회랑에서의 암모니아 연료 수요를 충족하기 위해 필요한 셔틀 선박 및 저장 시설의 최적 규모와 개수를 결정하고, 전체 순현재가(Net Present Cost, NPC)를 최소화합니다.

**버전**: v2.3.3 (Discount 제거 + v2.3.2 기능 통합)

---

## 주요 개선사항 (v2.0 → v2.3.3)

- ✅ **Case 1, 2-1, 2-2 모두 지원**
- ✅ **YAML 기반 설정 파일로 쉬운 파라미터 관리**
- ✅ **다중 케이스 병렬 실행 지원**
- ✅ **Case 1/2 아키텍처 분리 및 통일**
- ✅ **펌핑 시간 계산 정확화**
- ✅ **공통 로직 라이브러리화 (FleetSizing, CycleTime)**
- ✅ **시간 가치 할인 제거 (No Discounting)** - 모든 연도 동일 가중치

> **상세한 버전별 변경사항은** [`docs/changelog.md`](./docs/changelog.md) 참조

---

## Project Structure

```
D:\code\Green_Cor\
├── config/                          # YAML 설정 파일들
│   ├── base.yaml                    # 공통 파라미터
│   ├── case_1.yaml                  # Case 1: 부산항 저장소
│   ├── case_2_yeosu.yaml            # Case 2-1: 여수→부산
│   └── case_2_ulsan.yaml            # Case 2-2: 울산→부산
├── src/                             # Python 프로덕션 코드
│   ├── __init__.py
│   ├── config_loader.py             # YAML 설정 로더
│   ├── shuttle_round_trip_calculator.py  # 핵심 시간 계산 (Layer 1)
│   ├── cycle_time_calculator.py     # 확장 시간 계산 (Layer 1)
│   ├── fleet_sizing_calculator.py   # 함대 규모 계산 (Layer 1)
│   ├── shore_supply.py              # 육상 공급 관리 (Layer 1)
│   ├── utils.py                     # 유틸리티 함수 (Layer 1)
│   ├── optimizer.py                 # MILP 최적화 엔진 (Layer 2)
│   ├── cost_calculator.py           # 비용 계산 (Layer 2)
│   ├── export_excel.py              # Excel 출력 (Layer 3)
│   └── export_docx.py               # Word 출력 (Layer 3)
├── tests/                           # 단위/통합 테스트
│   ├── test_cycle_time_calculator.py
│   ├── test_optimizer_integration.py
│   ├── test_shore_supply.py
│   ├── test_shuttle_round_trip_calculator.py
│   └── test_annualized_capex_consistency.py
├── scripts/                         # 개발/디버그 스크립트
│   ├── debug_*.py                   # 디버깅 스크립트
│   ├── verify_*.py                  # 검증 스크립트
│   └── ...
├── docs/                            # 문서
│   ├── architecture.md              # 코드 아키텍처
│   ├── configuration.md             # 파라미터 설정 가이드
│   ├── changelog.md                 # 버전 변경 이력
│   ├── chapters/                    # 챕터별 문서
│   ├── presentations/               # 프레젠테이션
│   │   ├── slides/                  # HTML 슬라이드
│   │   └── *.pptx                   # PowerPoint 파일
│   ├── reports_docx/                # 생성된 Word 리포트
│   ├── PDFs/                        # PDF 참고자료
│   └── archive/                     # 레거시 코드 및 구 문서
├── results/                         # 결과 출력 (자동 생성, git 제외)
├── main.py                          # 메인 진입점
├── run_all_cases.py                 # 다중 케이스 실행
├── CLAUDE.md                        # 이 파일
├── README.md                        # GitHub README
├── requirements.txt                 # Python 의존성
├── .gitignore
└── .mcp.json
```

---

## Layer 아키텍처 (검증 가능한 계층 구조)

이 프로젝트는 **3계층(Layer) 구조**로 설계되어 있습니다. 각 계층을 독립적으로 검증할 수 있도록 의도적으로 분리했습니다.

### 왜 Layer 구조인가?

**문제**: 최종 코드만 있으면 어디서 오류가 발생했는지 파악이 불가능
**해결**: 기초 계산 → 확장 계산 → 최종 결과로 단계별 검증 가능

### 계층 다이어그램

```
┌─────────────────────────────────────────────────────┐
│  Layer 3: 최종 실행 (Presentation)                   │
│  main.py, run_all_cases.py, export_*.py             │
│  → 사용자 인터페이스, 결과 출력                        │
└────────────────────┬────────────────────────────────┘
                     │ depends on
┌────────────────────▼────────────────────────────────┐
│  Layer 2: 최적화 & 비용 (Optimization)               │
│  optimizer.py, cost_calculator.py                   │
│  → MILP 최적화, 비용 계산                            │
└────────────────────┬────────────────────────────────┘
                     │ depends on
┌────────────────────▼────────────────────────────────┐
│  Layer 1: 기초 계산 (Foundation)                     │
│  shuttle_round_trip_calculator.py, shore_supply.py  │
│  cycle_time_calculator.py, fleet_sizing_calculator.py│
│  → 핵심 시간 계산, 독립적으로 검증 가능                │
└─────────────────────────────────────────────────────┘
```

### 각 Layer 상세

| Layer | 파일 | 역할 | 의존성 |
|-------|------|------|--------|
| **1 (기초)** | `shuttle_round_trip_calculator.py` | 핵심 시간 계산 (Case 1/2 분기) | 없음 (독립) |
| | `shore_supply.py` | 육상 공급 시설 관리 | 없음 (독립) |
| | `cycle_time_calculator.py` | 시간 계산 통합 | Layer 1 내부 |
| | `fleet_sizing_calculator.py` | 함대 규모 계산 | 없음 (독립) |
| | `utils.py` | MCR 보간, 수요 계산 | numpy만 |
| | `config_loader.py` | YAML 설정 로드 | utils |
| **2 (최적화)** | `optimizer.py` | MILP 최적화 엔진 | Layer 1 전체 |
| | `cost_calculator.py` | CAPEX/OPEX 계산 | utils |
| **3 (최종)** | `main.py` | 진입점, 실행 모드 제어 | Layer 1+2 |
| | `run_all_cases.py` | 다중 케이스 병렬 실행 | Layer 1+2 |
| | `export_excel.py` | Excel 출력 | pandas |
| | `export_docx.py` | Word 출력 | pandas |

### 검증 흐름

```
Layer 1만 테스트     →  시간 계산이 맞는지 확인
        ↓
Layer 1+2 테스트    →  비용 계산이 맞는지 확인
        ↓
Layer 1+2+3 통합    →  최종 결과 검증
```

**main.py의 실행 모드가 이 검증 흐름을 지원합니다:**

| 실행 모드 | 사용 Layer | 용도 |
|-----------|------------|------|
| `single_scenario` | Layer 1만 | 빠른 시간 계산 검증 |
| `annual_simulation` | Layer 1 + 일부 2 | 연간 계산 검증 |
| `single` / `all` | Layer 1+2+3 | 완전 최적화 |

### 핵심 분기점: Case 1 vs Case 2

**Layer 1의 `shuttle_round_trip_calculator.py`에서 핵심 로직이 분기됩니다:**

```python
if has_storage_at_busan:  # Case 1
    pumping_time = shuttle_size / pump_rate
    # 셔틀이 얼마나 빨리 비워지는가?
else:  # Case 2
    pumping_time = bunker_volume / pump_rate
    # 각 선박이 얼마나 빨리 채워지는가?
```

이 핵심 차이가 전체 최적화 결과를 결정하며, Layer 1에서 명확하게 분리되어 있어 각 케이스별 검증이 용이합니다.

---

## 시간 구조 (Time Structure)

### 중요: 시간 계산 vs 비용 계산

**모든 시간 계산은 육상 공급 시설을 포함합니다.**

- **시간 계산**: 항상 육상 적재 시간 포함
  - 모든 운영 제약(constraint)에 사용됨
  - 연간 최대 항차, 활용도 계산에 사용됨

- **비용 계산**: 육상 공급 시설의 CAPEX/OPEX는 config 옵션으로 포함/제외 가능
  - `shore_supply.enabled` = true: 비용 포함
  - `shore_supply.enabled` = false: 비용만 제외

- **할인율 (Discount Rate)**: **NO DISCOUNTING**
  - `discount_rate: 0.0` - 모든 연도가 동일한 가중치로 취급됨
  - 비용 값은 명목 비용(nominal costs)이며 시간값 조정 없음
  - 2030년 비용 = 2050년 비용 (같은 규모의 경우)

### Case 1: 부산항 내 셔틀 운영

| 항목 | 설명 |
|------|------|
| 기본 사이클 | 3시간 (이동 + 연결/해제) + 펌핑시간 |
| 펌핑 시간 | Shuttle_Size_m3 / Pump_Rate_m3ph |
| 육상 적재 | Shuttle_Size_m3 / 1500 (고정 펌프 유량) |
| **예시** | 5,000 m³ 셔틀 + 1,000 m³/h: **12.33시간/사이클** |

### Case 2: 여수/울산 → 부산 장거리 운송

**KEY**: 한 번의 항해로 **여러 선박에 급유**

| 항목 | Case 2-1 (여수) | Case 2-2 (울산) |
|------|-----------------|-----------------|
| 편도 항해 | 86해리 → 5.73시간 | 25해리 → 1.67시간 |
| 셔틀 크기 예 | 10,000 m³ | 10,000 m³ |
| 총 사이클 | ~36시간 | ~28시간 |
| 연간 항해 | ~217회 | ~282회 |

---

## 세 가지 Case 설명

### Case 1: 부산항 저장소 기반

| 항목 | 값 |
|------|-----|
| **출발지** | 부산항 저장소 |
| **목적지** | 부산항 내 선박 |
| **특징** | 여러 트립 필요 (shuttle_size < bunker_volume) |
| **셔틀 크기** | 500 ~ 5000 m³ |
| **저장 탱크** | 있음 (35,000톤) |
| **펌핑 시간** | shuttle_size / pump_rate |

### Case 2-1: 여수 → 부산 (장거리)

| 항목 | 값 |
|------|-----|
| **출발지** | 여수 (암모니아 생산시설) |
| **거리** | 86 해리 |
| **특징** | 한 번의 항해로 여러 선박 서빙 |
| **셔틀 크기** | 5000 ~ 50000 m³ |
| **펌핑 시간** | bunker_volume / pump_rate (선박 요구량 기준) |

### Case 2-2: 울산 → 부산 (근거리)

| 항목 | 값 |
|------|-----|
| **출발지** | 울산 |
| **거리** | 25 해리 |
| **특징** | 한 번의 항해로 여러 선박 서빙 |
| **셔틀 크기** | 5000 ~ 50000 m³ |
| **펌핑 시간** | bunker_volume / pump_rate (선박 요구량 기준) |

---

## 설정 파일 (YAML) 구조

### base.yaml - 공통 파라미터

```yaml
time_period:
  start_year: 2030
  end_year: 2050

economy:
  discount_rate: 0.0               # No discounting - all years weighted equally
  fuel_price_usd_per_ton: 600.0   # 암모니아 가격

shipping:
  start_vessels: 50               # 2030년 선박 수
  end_vessels: 500                # 2050년 선박 수
  voyages_per_year: 12            # 선박당 연간 항차수

operations:
  max_annual_hours_per_vessel: 8000  # 연간 최대 가동시간
  setup_time_hours: 0.5              # 호스 연결 시간
  tank_safety_factor: 2.0            # 탱크 여유계수
```

### case_X.yaml - 케이스별 파라미터

```yaml
case_name: "Case 1: Busan Port with Storage"
case_id: "case_1"

shuttle:
  available_sizes_cbm: [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
  mcr_map_kw:
    500: 1296
    1000: 1341
    # ... MCR 값들

operations:
  travel_time_hours: 1.0
  has_storage_at_busan: true       # Case 1만 true

bunkering:
  bunker_volume_per_call_m3: 5000.0

tank_storage:
  enabled: true
  size_tons: 35000.0
```

---

## 사용 방법

### 1. 설치

```bash
pip install -r requirements.txt
```

### 2. Config를 통한 프로그램 제어

**모든 실행은 `config/base.yaml`의 `execution` 섹션에서 제어됩니다.**

```yaml
execution:
  run_mode: "single"                # single, single_scenario, all, multiple
  single_case: "case_2_ulsan"       # run_mode=single일 때
  num_jobs: 1                       # 병렬 작업 수
  output_directory: "results"
  export:
    csv: true
    excel: true
    docx: true
```

### 3. 실행 시나리오 (빠른 시작)

**단일 케이스 최적화**:
```yaml
execution:
  run_mode: "single"
  single_case: "case_2_ulsan"
```

**모든 케이스 병렬 실행**:
```yaml
execution:
  run_mode: "all"
  num_jobs: 4
```

**특정 시간 계산만** (빠른 실행):
```yaml
execution:
  run_mode: "single_scenario"
  single_case: "case_2_ulsan"
  single_scenario_shuttle_cbm: 5000
  single_scenario_pump_m3ph: 1000
```

> **상세한 실행 시나리오는** [`docs/configuration.md`](./docs/configuration.md) 참조

### 4. 결과 해석

실행 후 `results/` 디렉토리에 다음 파일이 생성됩니다:

- **MILP_scenario_summary_case_X.csv**: 각 셔틀/펌프 조합별 NPC 요약
- **MILP_per_year_results_case_X.csv**: 연도별 상세 결과 (2030-2050)
- **MILP_results_case_X.xlsx**: Excel 형식 (다중 시트)
- **MILP_Report_case_X.docx**: Word 형식 리포트

결과 컬럼:
- `Shuttle_Size_cbm`: 셔틀 크기 (m³)
- `Pump_Size_m3ph`: 펌프 용량 (m³/h)
- `NPC_Total_USDm`: 20년 순현재가 (백만 USD)
- `Year`: 연도
- `New_Shuttles`: 당해 신규 추가 셔틀 수
- `Total_Shuttles`: 누적 셔틀 수
- `Annual_Calls`: 연간 벙커링 횟수

---

## 기술 세부 사항

**MILP 최적화 모델**:
- 목적함수: 20년 순현재가(NPC) 최소화
- 결정변수: 셔틀 수, 벙커링 횟수, 탱크 수 (연도별)
- 주요 제약식: 수요 충족, 작업시간, 탱크 용량

**비용 계산**:
- CAPEX: 셔틀, 펌프, 저장 탱크 구매 비용
- OPEX: 연료비, 유지보수비, 냉각비

> **상세한 기술 정보는** [`docs/architecture.md`](./docs/architecture.md) 참조

---

## 주요 파라미터 (Configurable Variables)

모든 파라미터는 YAML 파일에서 변경 가능:

| 항목 | 기본값 | 설명 |
|------|--------|------|
| **셔틀 크기** | 500-5000 m³ | Case별로 다름 |
| **펌프 유량** | 1000 m³/h | pumps.available_flow_rates (고정) |
| **펌프 유량 (민감도)** | 400-2000 m³/h | pumps.sensitivity_flow_rates (S7 분석용) |
| **할인율** | 0% (No discounting) | economy.discount_rate - 모든 연도 동일 가중치 |
| **연료 가격** | 600 USD/ton | economy.fuel_price_usd_per_ton |
| **초기 선박 수** | 50척 (2030년) | shipping.start_vessels |
| **최종 선박 수** | 500척 (2050년) | shipping.end_vessels |
| **최대 운영시간** | 8,000 시간/년 | operations.max_annual_hours_per_vessel |

> **상세한 파라미터 가이드는** [`docs/configuration.md`](./docs/configuration.md) 참조

---

## 문제 해결

### 1. "No module named 'pulp'" 오류
```bash
pip install pulp
```

### 2. "Config file not found" 오류
```bash
ls config/  # 또는 dir config (Windows)
```

### 3. 최적해 없음 (Infeasible)
- 최대 작업시간 (H_max) 증가
- 펌프 크기 증가
- 셋틀 크기 증가

### 4. 느린 실행 속도
- 셔틀/펌프 조합 줄이기
- 병렬 처리 사용 (run_all_cases.py)

---

## 개발 및 확장

### 새로운 케이스 추가
1. `config/case_X.yaml` 파일 생성
2. 파라미터 설정 (travel_time_hours, shuttle sizes, MCR map 등)

### 새로운 제약식 추가
`src/optimizer.py`의 `_solve_combination` 메서드에서:
```python
# 새 제약식 추가
prob += some_condition_expression
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

- 프로젝트 문서: `docs/` 폴더 참조
- 상세한 설정 가이드: `docs/configuration.md`
- 버전 변경 이력: `docs/changelog.md`
- 아키텍처 설명: `docs/architecture.md`

**마지막 업데이트**: 2025-11-22 (v2.4 - Annualized CAPEX 수정, Annualization Rate 도입)

---

## AI Assistant Instructions (Claude Code 전용)

### 중요: 문서 생성 가이드

**다음의 경우에만 마크다운 문서(.md)를 생성하세요:**
- 사용자가 명시적으로 요청한 문서
- 프로젝트에 필수적인 기술 문서 (`docs/` 폴더 내)
  - `architecture.md`, `configuration.md`, `changelog.md` 등

**절대 금지:**
- 요청하지 않은 요약 문서 생성
- 작업 완료 후 자동 보고서 작성
- 설명 목적의 추가 문서 창작
- 토큰 낭비를 초래하는 불필요한 파일

**원칙:**
- 사용자 요청에 정확히 응답
- 코드 수정만 수행
- 과도한 문서화 피하기
- 토큰 효율성 우선

### 작업 완료 시
- 간단한 텍스트 요약만 제공 (마크다운 파일 생성 금지)
- Git 커밋 메시지로 변경사항 기록
- 추가 설명 없이 작업 사실만 보고

---

## 파일 인코딩 및 코딩 스타일 가이드

### 중요: UTF-8 인코딩 설정

**모든 Python 파일에서 반드시 다음을 따르세요:**

1. **파일 첫 줄에 UTF-8 선언** (Windows 호환성)
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

2. **print문에서 유니코드/이모지 사용 금지**
- 다음 대신 (FAIL):
  ```python
  print(f"✓ Optimal Scenario Found:")
  print(f"❌ FAIL - Values Differ")
  print(f"✅ PASS - Values Match!")
  ```

- 다음처럼 사용 (SUCCESS):
  ```python
  print(f"[OK] Optimal Scenario Found:")
  print(f"[FAIL] Values Differ")
  print(f"[PASS] Values Match!")
  ```

3. **한국어는 사용 가능** (UTF-8이므로)
```python
print("LCOAmmonia 일치성 검증")  # OK
print(f"결과: ${lco_value:.2f}/ton")  # OK
```

4. **Windows 콘솔 호환성**
- 파일 저장: UTF-8 (BOM 없음)
- print 문: ASCII 문자만 (숫자, 영문, 한글, 기호)
- 이모지/특수 유니코드: 절대 금지

### 예시: 올바른 형식

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모듈 설명 (한글 가능)
"""

import sys

def test_case():
    """테스트 함수"""
    print("\n[OK] 테스트 시작")  # 한글 + ASCII = 안전
    print(f"  Shuttle: {size} m3")  # ASCII만 = 안전
    print(f"  Difference: {diff:.2f}/ton")
    print("[PASS] 테스트 통과")  # ASCII 대괄호 + 한글 = 안전
    return True

if __name__ == "__main__":
    success = test_case()
    sys.exit(0 if success else 1)
```

### 콘솔 출력 패턴 (모든 파일에서 일관성 유지)

| 목적 | 패턴 | 예시 |
|------|------|------|
| 성공 | `[OK]` | `[OK] Results saved` |
| 실패 | `[ERROR]` | `[ERROR] File not found` |
| 경고 | `[WARN]` | `[WARN] Memory low` |
| 진행 | `[N/M]` | `[2/3] Running step 2` |
| 통과 | `[PASS]` | `[PASS] Values match` |
| 실패 | `[FAIL]` | `[FAIL] Mismatch detected` |
| 정보 | `[INFO]` | `[INFO] Configuration loaded` |
| 구분선 | `=======` | 섹션 분리용 |

### 파이썬 파일 생성 체크리스트

- [ ] 첫 줄: `#!/usr/bin/env python3`
- [ ] 둘째 줄: `# -*- coding: utf-8 -*-`
- [ ] print문에 이모지/특수 유니코드 없음
- [ ] 한글 문자열은 `""` 또는 `''` 안에만 (f-string 외부)
- [ ] `[OK]`, `[FAIL]` 등의 ASCII 패턴 사용
- [ ] 파일 저장: UTF-8 (BOM 없음) 설정
