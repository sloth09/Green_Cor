# Green Corridor - 코드 아키텍처 (Code Architecture)

## v2.3 완료된 아키텍처: 3-Layer 모듈화 구조

### 1. 육상 연료 공급 모듈 (Shore Supply Module) ✅

**구현된 구조**:
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

### 2. 핵심 시간 로직 라이브러리화 (Core Time Calculation Library) ✅

**구현된 3-Layer 아키텍처**:

```
Layer 1: ShuttleRoundTripCalculator (기본 셔틀 왕복 로직)
  └─ calculate(shuttle_size, pump_size, num_vessels, has_storage_at_busan)
     - Case 1: 셔틀이 반복 왕복 (여러 트립)
     - Case 2: 한 번의 항해로 여러 선박 (복수 선박)
     - 반환: 여행시간, 포트작업, 펌핑시간 등의 상세 정보

        ↓

Layer 2: CycleTimeCalculator (통합 계산 레이어)
  └─ calculate_single_cycle(shuttle_size, pump_size, num_vessels)
     - ShuttleRoundTripCalculator 호출
     - ShoreSupply 모듈 통합
     - 연간 메트릭 계산 (annual_cycles, ships_per_year)
     - 반환: 완전한 사이클 타임 정보

        ↓

Layer 3: main.py & optimizer.py (실행 레이어)
  ├─ run_single_scenario(): 단일 시나리오 계산 (빠른 테스트)
  └─ BunkeringOptimizer: 전체 최적화 (90개 조합)
```

**Case 1 vs Case 2 핵심 차이**:
```python
# Case 1: 펌핑 = 셔틀 용량 / 펌프 유량
if has_storage_at_busan:
    pumping_per_vessel = shuttle_size_m3 / pump_size_m3ph  # 1회 트립 시간

# Case 2: 펌핑 = 선박 요구량 / 펌프 유량
else:
    pumping_per_vessel = bunker_volume_per_call_m3 / pump_size_m3ph  # 선박당 시간
    # 여러 선박은 자동으로 반복 (num_vessels)
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

### 3. Case별 최적화 호출 구조

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

### 4. 단일 진실 공급원 (Single Source of Truth)

```
계산 로직 통합 현황:
├── CycleTimeCalculator: 모든 시간 계산 ✅ (v2.2 완료)
├── FleetSizingCalculator: 함대 규모 계산 ✅ (v2.3.2 완료)
├── Demand/Supply Constraint: Case 1/2 통일 ✅ (v2.3.2 완료)
└── Cost Calculation: cost_calculator.py 완전화 진행 중...
```

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

### src/shuttle_round_trip_calculator.py
- 기본 셔틀 왕복 시간 계산
- Case 1/2 구분 로직

### src/cycle_time_calculator.py
- 통합 사이클 시간 계산
- 연간 메트릭 계산

### src/fleet_sizing_calculator.py
- 통합 함대 규모 계산
- main.py + optimizer.py에서 공통 사용

### src/shore_supply.py
- 육상 연료 공급 시간 계산
- 셔틀 적재/언로드 시간

## MILP 모델 구조

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

## 비용 계산

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

## MCR 보간

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
