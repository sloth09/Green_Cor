# Green Corridor - 설정 및 파라미터 가이드 (Configuration Guide)

모든 파라미터는 YAML 설정 파일에서 변경하며, 프로그램을 재시작한 후 실행하면 됩니다.

## 1. 실행 제어 (config/base.yaml)

### 케이스 선택
```yaml
execution:
  case: "case_2_yeosu"  # case_1, case_2_yeosu, case_2_ulsan
  run_mode: "single"
```

### 병렬 실행 (4개 CPU 사용)
```yaml
execution:
  run_mode: "multiple"
  cases_to_run:
    - "case_1"
    - "case_2_yeosu"
  num_jobs: 4
```

### 출력 형식 변경
```yaml
execution:
  export:
    csv: true      # 항상 생성
    excel: true    # Excel 다중 시트
    docx: true     # Word 리포트
```

---

## 2. 경제 파라미터 (config/base.yaml)

### 1항차 급유량 변경
```yaml
# config/case_1.yaml (케이스별로 다를 수 있음)
bunkering:
  bunker_volume_per_call_m3: 5000.0  # 변경 가능 (현재: 5000)
```

### 할인율 설정
```yaml
# config/base.yaml
economy:
  discount_rate: 0.0   # No discounting (권장: 모든 연도 동일 가중치)
  # discount_rate: 0.05  # 5% (선택사항)
  # discount_rate: 0.10  # 10% (선택사항)

# 참고: discount_rate = 0.0일 때, 모든 연도가 동일한 가중치로 취급됩니다.
# 비용 값은 명목 비용(nominal costs)이며 시간값 조정 없음
```

### 연료 가격 변경
```yaml
# config/base.yaml
economy:
  fuel_price_usd_per_ton: 500.0  # USD/ton (기본: 600)
```

### 전기요금 변경
```yaml
# config/base.yaml
economy:
  electricity_price_usd_per_kwh: 0.10  # USD/kWh (기본: 0.0769)
```

---

## 3. 운영 파라미터 (config/base.yaml)

### 선박 수요 변경
```yaml
shipping:
  start_vessels: 50    # 2030년 선박 수 (기본: 50)
  end_vessels: 500     # 2050년 선박 수 (기본: 500)
```

### 최대 연간 작업시간 변경
```yaml
operations:
  max_annual_hours_per_vessel: 8000.0  # 시간/년 (기본: 8000)
```

### 탱크 여유계수 변경
```yaml
operations:
  tank_safety_factor: 2.0  # 2배 여유 (기본: 2.0, 범위: 1.5~3.0)
```

### 일일 피크 계수 변경
```yaml
operations:
  daily_peak_factor: 1.5  # 일일 피크의 1.5배 (기본: 1.5)
```

---

## 4. 셔틀 및 펌프 (config/case_X.yaml)

### 사용 가능한 셔틀 크기 변경
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

### MCR 값 커스터마이징
```yaml
# config/case_2_yeosu.yaml
shuttle:
  mcr_map_kw:
    5000: 1694
    10000: 2159
    15000: 2485
    # ... 사용자 정의 값으로 변경
```

### 펌프 유량 범위 변경
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

## 5. 탱크 저장소 (config/base.yaml)

### 탱크 크기 변경
```yaml
tank_storage:
  size_tons: 35000.0  # 톤 (기본: 35,000)
  size_tons: 40000.0  # 더 큰 탱크
```

### 탱크 냉각비용 변경
```yaml
tank_storage:
  cooling_energy_kwh_per_kg: 0.0378  # kWh/kg (기본: 0.0378)
```

---

## 6. 변경 가능한 변수 목록 (Configurable Variables)

본 모델에서 사용자가 YAML 파일을 통해 직접 조정 가능한 변수들:

### 셔틀 (Shuttle) 파라미터
- **가용 크기**: Case 1: 500~5,000 m³, Case 2: 5,000~50,000 m³
- **MCR (최대 연속 정격)**: 셔틀 크기별 엔진 파워 (kW)
  - 기본값: 기존 데이터 + 선형 보간(4500, 5000) + 로그 외삽(Case 2)
  - 수정 가능: case_X.yaml의 mcr_map_kw 수정

### 펌프 (Pump) 파라미터
- **가용 유량**: 400, 600, 800, 1,000, 1,200, 1,400, 1,600, 1,800, 2,000 m³/h
  - 기본 9종 모두 최적화 대상
  - 특정 펌프 크기만 사용하고 싶으면 base.yaml의 pumps.available_flow_rates 수정

### 저장탱크 (Tank) 파라미터 (Case 1만)
- **탱크 용량**: 기본값 35,000톤
  - config/case_1.yaml의 tank_storage.size_tons 수정
  - 예: 40,000톤, 50,000톤 등으로 변경 가능
- **냉각 에너지**: 0.0378 kWh/kg (암모니아 냉각 유지용)
- **여유 계수**: 2.0배 (안전 재고, 1.5~3.0 범위)
  - config/base.yaml의 operations.tank_safety_factor 수정

### 시간 파라미터 (Time-related)
- **Case 1 편도 이동 시간**: 기본값 2.0시간 (항만 내부)
  - operations.travel_time_hours
- **Case 2 항해 거리 기반**:
  - Case 2-1 (여수): 86해리 → 5.63시간 (자동 계산)
  - Case 2-2 (울산): 25해리 → 1.67시간 (자동 계산)
- **호스 연결/해제 시간**: 각 0.5시간 (총 1시간)
  - operations.setup_time_hours (기본값 0.5시간)
- **육상 연료 공급 펌프 유량**: 1,500 m³/h (고정값, 변경 가능)
  - config/base.yaml의 shore_supply_pump_rate_m3ph

### 경제 파라미터
- **할인율**: 기본값 0% (No Discounting - 모든 연도 동일 가중치)
  - economy.discount_rate
  - 참고: 0.0 = 할인 없음, 값을 높이면 미래 비용을 할인 (예: 0.07 = 7%)
- **암모니아 연료 가격**: 기본값 600 USD/톤
  - economy.fuel_price_usd_per_ton
- **전기요금**: 기본값 0.0769 USD/kWh
  - economy.electricity_price_usd_per_kwh
- **유지보수비율**:
  - 셔틀: CAPEX의 5%
  - 펌프: CAPEX의 5%
  - 탱크: CAPEX의 3%

### 수요 예측 파라미터
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

## 7. 예제: Case 커스터마이징

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

## 8. base.yaml - 공통 파라미터 (요약)

```yaml
time_period:
  start_year: 2030
  end_year: 2050

economy:
  discount_rate: 0.0               # No discounting - 모든 연도 동일 가중치
  fuel_price_usd_per_ton: 600.0   # 암모니아 가격

shipping:
  kg_per_voyage: 2158995.0        # 항차당 연료량
  voyages_per_year: 12            # 선박당 연간 항차수
  start_vessels: 50               # 2030년 선박 수
  end_vessels: 500                # 2050년 선박 수

operations:
  max_annual_hours_per_vessel: 8000  # 연간 최대 가동시간
  setup_time_hours: 0.5              # 호스 연결 시간
  tank_safety_factor: 2.0            # 탱크 여유계수
  daily_peak_factor: 1.5             # 일일 피크 계수
```

---

## 9. case_X.yaml - 케이스별 파라미터 (요약)

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
