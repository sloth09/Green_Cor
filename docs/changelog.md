# Green Corridor - 버전 변경 이력 (Changelog)

## v2.3.2 개선 (공통 로직 라이브러리화 및 Case 1/2 Constraint 통일) ⭐

**문제 분석 (비통일 로직)**:
- ❌ FleetSizingCalculator 없음: main.py와 optimizer.py의 함대 규모 계산 로직 다름
- ❌ Case 2에서 y[t] 의미 불일치: demand constraint와 total_supply에서 다른 정의
- ❌ cost_calculator.py 펌프 연료비: v2.3.1에서 "수정됨"이라 했지만 아직 2.0 factor 있음

**수정 내용**:
- ✅ **FleetSizingCalculator 라이브러리 생성**
  - `calculate_required_shuttles_working_time_only()`: 공통 함대 규모 계산
  - main.py + optimizer.py 모두 사용하도록 통일
  - Fleet sizing 로직 완전 일치

- ✅ **Case 1/2 제약식 통일** (y[t] 의미 명확화)
  - y[t] = annual vessel bunkering calls (항상 동일)
  - Demand constraint: `y[t] × bunker_volume_per_call_m3 >= annual_demand[t]` (통일)
  - Total supply: `y[t] × bunker_volume_per_call_m3` (모두 동일)
  - 이제 Case 1과 Case 2가 동일한 로직 사용 ✅

- ✅ **cost_calculator.py 펌프 연료비 수정** (v2.3.1 미완료 부분)
  - Line 214: `2.0 * (bunker_volume_m3 / pump_flow_m3ph)` → `bunker_volume_m3 / pump_flow_m3ph`
  - 주석 업데이트: v2.3.1 fix 명시

---

## v2.3.1 버그 수정 (펌프 연료비 계산 오류) ⭐

**문제 분석**:
- ❌ 펌프 연료비 계산에 오류: `2.0 × (volume / pump_rate)` 사용
- 이로 인해 Case 2에서 펌프 비용이 **2배 과다계산**
- annual_simulation과 optimizer 간 불일치 발생

**수정 내용**:
- 🔧 **optimizer.py**: 펌프 연료비 계산에서 2.0 계수 제거
  - 변경 전: `pumping_time_hr_call = 2.0 * (volume / pump_size)` ❌
  - 변경 후: `pumping_time_hr_call = bunker_volume_per_call_m3 / pump_size` ✅
- 🔧 **main.py**: annual_simulation의 펌프 비용 계산 동기화
  - 동일한 로직 적용: 모든 케이스에서 `pumping_time = 5000m³ / pump_rate`

**핵심 원리**:
```
펌프는 "vessel call" 기준으로 작동:
- Case 1: 각 vessel call = 5000m³ 펌핑
- Case 2: 각 vessel call = 5000m³ 펌핑 (여러 vessel도 각각 5000m³)

따라서 양쪽 모두 pumping_time = 5000 / pump_rate (동일)
    ↓
펌프 비용은 "셔틀 크기와 무관"하게 계산되어야 함 ✅
```

**검증 결과**:
- ✅ Case 1: 2500m³과 5000m³ 펌프 비용 동일 ($0.108M/year)
- ✅ Case 2-2: 10000m³과 25000m³ 펌프 비용 동일 ($0.108M/year)
- ✅ Case 1 최적값: 2500m³ + 2000m³/h = $223.29M NPC (정확함)

---

## v2.3 개선 (Case 1/2 아키텍처 통합 + 펌핑 시간 수정)

- 🔧 **펌핑 시간 계산 수정**: `bunker_volume / pump_rate` → `shuttle_size / pump_rate` (Case 1)
  - Example: 1000 m³ shuttle + 1000 m³/h pump = 1.00h (이전: 5.00h ❌)
- 🔧 **선박당 왕복 일정 공식 수정**: `365 / annual_cycles` → `cycle_duration / 24`
  - Example: 5.67h ÷ 24 = 0.236일/회 (이전: 0.3일/회 ❌)
- ✅ **벙커링 가능선박 메트릭 추가**: `ships_per_year = annual_supply_m3 / bunker_volume`
- ✅ **Case 1 vs Case 2 아키텍처 분리**:
  - Case 1: 펌핑 = shuttle_size / pump (여러 트립)
  - Case 2: 펌핑 = bunker_volume / pump (여러 선박)
- ✅ **Case 2 포트 작업 추가**: 부산항 진입(1h) + 선박당 이동(1h) + 퇴출(1h)
- ✅ **단일 시나리오 동적 계산**: Case 2에서 vessels_per_trip 자동 계산

---

## v2.2 개선 (Config 구조 명확화)

### 문제점
v2.0-v2.1의 Config 구조가 혼동스러웠습니다:
- `case`와 `cases_to_run`: 필드명이 유사해서 혼동
- `run_mode`와 실제 사용되는 필드의 관계가 불명확
- 어떤 필드를 언제 설정해야 하는지 불명확

### 해결책
필드명 명확화 및 구조 개선:
- `case` → `single_case` (더 명확한 의도)
- `cases_to_run` → `multi_cases` (단수/복수 구분 명확)
- 후향 호환성 추가: 이전 필드명도 자동으로 변환

### 호환성
✅ **이전 설정 파일도 그대로 작동**
- v2.0-v2.1 설정 → 자동 변환
- 업데이트 불필요

---

## v2.1 개선사항 (Case 2 벙커링 로직 수정)

### 문제점 분석
v2.0에서 Case 2 (여수→부산, 울산→부산)의 벙커링 로직이 잘못 구현:

**기존 로직의 오류**:
```python
# 잘못된 코드 (Line 165)
trips_per_call = int(ceil(bunker_volume_per_call / shuttle_size))
```

이 로직은 **Case 1 시나리오에만 맞음**:
- Case 1: 500 m³ 셔틀이 5,000 m³ 콜을 여러 트립으로 나눠서 충족 (O)
- Case 2: 25,000 m³ 셔틀 = ceil(5000/25000) = 1 트립 (X)
  - 25,000 m³ 셔틀이 5,000 m³만 운반하므로 **용량 80% 낭비**
  - 5,000과 25,000 m³ 셔틀이 동일하게 평가됨 (비현실적)

### 수정 내용
1. **초기화 부분 추가 (src/optimizer.py Line 106)**
   - `has_storage_at_busan` 플래그로 Case 1과 Case 2 구분
   - Case 1: True (부산에 저장탱크 있음)
   - Case 2: False (부산에 저장탱크 없음, 여수/울산 출발지에만 있음)

2. **트립 계산 로직 수정 (src/optimizer.py Lines 165-176)**
   - Case 1: 소형 셔틀이 콜당 여러 번 왕복
   - Case 2: 대형 셔틀이 한 번의 왕복으로 여러 척 급유

3. **펌핑 시간 계산 수정 (src/optimizer.py Lines 184-187)**
   - Case 1: 선박 요구량 기준 펌핑
   - Case 2: 전체 셔틀 용량 기준 펌핑

4. **수요 충족 제약식 수정 (src/optimizer.py Lines 263-269)**
   - Case 2: y[t]는 "트립 수"이므로 shuttle_size 전체를 전달

5. **일일 피크 제약식 수정 (src/optimizer.py Lines 282-285)**
   - Case별로 다른 수요 정의 적용

### 결과 영향
- **가능한 조합 감소**: 90개 → 62-64개 (일부 조합이 현재 실행 불가능)
- **대형 셔틀의 정확한 비용 평가**: 이제 대형 셔틀의 효율성이 올바르게 반영됨
- **최적해는 유지**: Case 2-2 (울산)의 최적해는 여전히 5,000 m³ + 2,000 m³/h
  - $94.9M NPC (Case 1 대비 -38.2% 여전히 최적)

---

## v2.0 → v2.2 개선사항

- ✅ **Case 1, 2-1, 2-2 모두 지원**
- ✅ **YAML 기반 설정 파일로 쉬운 파라미터 관리**
- ✅ **다중 케이스 병렬 실행 지원**
- ✅ **모듈화된 구조 (config, optimizer, cost calculator)**
- ✅ **1항차 급유량 5000 m³로 업데이트**
- ✅ **Tank 크기 35,000톤으로 수정**
- ✅ **4500, 5000 m³ 셔틀 크기 추가**

---

## v1 이전 버전

이전 버전 (MILPmodel_v17_250811.py):
- ❌ Case 1만 구현
- ❌ 모든 파라미터 하드코딩
- ❌ 단일 케이스만 실행 가능
- ❌ 코드 재사용성 낮음

v2.0에서 전체 아키텍처가 개선되어 위의 모든 문제가 해결됨
