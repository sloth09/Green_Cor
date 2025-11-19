# 1회 왕복 운항 시간 보고서화 - 최종 계획 요약

**작성일**: 2025-11-18
**상태**: ✅ 계획 완료 (Phase 1-2), Phase 3-5 준비 완료

---

## 종합 개요

**목표**: 1회 왕복 운항에 걸리는 총 시간을 상세하게 보고서에 포함하고, 시간이 전체 모델에 어떻게 반영되는지 명확히 함.

**결과물**:
- CSV: 시간 분해 컬럼 추가
- Excel: 새로운 "Time Breakdown" 시트
- Word: 새로운 "운항 시간 분석" & "시간-비용 상관성" 섹션

---

## Phase 1: 시간 계산 체계 검증 ✅

**상태**: **완료**

### 검증 완료 항목

✅ **1-1. 계층 간 일관성**
- ShuttleRoundTripCalculator (Layer 1) → CycleTimeCalculator (Layer 2) → Optimizer (Layer 3)
- 모든 계층이 동일한 시간 개념 사용
- 데이터 손실 없음

✅ **1-2. Case별 정확성**
- Case 1: 15.33시간 사이클 (2.0h 항해)
- Case 2-2: 14.67시간 사이클 (1.67h 항해) ✓ 최단
- Case 2-1: 22.79시간 사이클 (5.73h 항해) ✓ 최장 (55% 더 김)

✅ **1-3. 제약식 검증**
- **제약식 1** (작업시간): `y[t] × trips × cycle_duration ≤ N[t] × 8000`
  - 8,000시간 연간 제약이 올바르게 적용됨
  - cycle_duration이 필요한 셔틀 수를 결정

- **제약식 2** (일일 피크): `daily_capacity ≥ daily_demand`
  - cycle_duration이 일일 용량에 영향
  - 대부분 loose constraint (선택적 역할)

✅ **1-4. 비용 계산 검증**
- Shuttle 연료: travel_time이 정확히 반영 (Case별 차이)
- Pump 연료: pumping_time이 정확히 반영
- **결론**: 시간이 NPC를 직접 결정하는 핵심 요소

### 문서
- `PHASE_1_TIME_VERIFICATION.md` (상세 검증)
- `PHASE_1_SUMMARY.md` (종합 보고서)

---

## Phase 2: 보고서 형식 설계 ✅

**상태**: **완료**

### 설계 완료 항목

✅ **2-1. CSV 확장 설계**

```
기존 컬럼:
- Shuttle_Size_cbm, Pump_Size_m3ph, Call_Duration_hr, Cycle_Duration_hr

추가 컬럼 (시간 분해):
- Shore_Loading_hr
- Travel_Outbound_hr
- Travel_Return_hr
- Setup_Time_hr
- Pumping_Per_Vessel_hr
- Movement_Per_Vessel_hr
- Basic_Cycle_Duration_hr

추가 컬럼 (운영 지표):
- Annual_Cycles_Max
- Vessels_per_Trip
- Annual_Supply_m3
- Time_Utilization_Ratio
```

✅ **2-2. Excel 시트 추가 설계**

**Sheet 2: "Time Breakdown" (신규)**
```
┌─ 최적 시나리오 정보
├─ 시간 분해 테이블 (7-8개 요소별)
│  ├─ 시간 (hours)
│  ├─ 비율 (%)
│  └─ 누적 (%)
├─ 파이 차트 (시간 구성)
└─ 연간 운영 지표
   ├─ 연간 최대 항차
   ├─ 셔틀당 일정
   └─ 연간 공급 용량
```

**Sheet 3: "Case Comparison" (신규)**
```
├─ Case 1, 2-1, 2-2 시간 비교
├─ 시간 차이 분석
├─ 막대 차트 (시간 비교)
└─ 선 차트 (펌프 크기별 변화)
```

✅ **2-3. Word 섹션 추가 설계**

**Section 4: "운항 시간 분석 (Time Structure Analysis)"**
```
4.1 최적 시나리오의 운항 시간 구성
   - 시간 분해 테이블 (7개 요소)
   - 각 요소별 설명

4.2 시간별 구성 비율
   - 파이 차트
   - 주요 관찰 (펌핑이 가장 큼)

4.3 연간 운영 지표
   - 항차, 일정, 용량

4.4 펌프 크기에 따른 시간 변화 분석
   - 펌프 2배 → 사이클 15% 감소 표
   - 경제성 분석

4.5 Case별 시간 비교
   - 3가지 케이스 시간 비교 표
   - 의미 해석
```

**Section 5: "시간-비용 상관성 분석 (Time-Cost Correlation)" (신규)**
```
5.1 개요
   - 시간 → 필요 셔틀 → NPC 메커니즘

5.2 펌프 크기별 시간-비용 변화
   - 펌프 크기 vs. Cycle Time vs. NPC 테이블
   - 트레이드오프 설명

5.3 셔틀 감소를 통한 절감액
   - 연도별 셔틀 필요 수 비교
   - CAPEX 절감액 정량화

5.4 연료비 절감
   - 펌프 크기별 연료비 분석
   - 20년 할인액 계산

5.5 최적 펌프 크기 선택 기준
   - 초기 vs. 중후기 트레이드오프
   - 의사결정 기준

5.6 Case별 시간-비용 비교
   - 3가지 케이스의 시간-NPC 비교
   - 위치 선택의 중요성
```

### 문서
- `PHASE_2_REPORT_FORMAT_DESIGN.md` (형식 설계)
- `PHASE_2_TIME_COST_CORRELATION.md` (시간-비용 분석)

---

## Phase 3: 코드 구현 (예정) ⏳

**상태**: 준비 완료, 실행 대기

### 구현 필요 항목

⏳ **3-1. CSV 확장**
- `src/report_generator.py` 수정
- 시간 정보 컬럼 추가 (10개)
- 연간 운영 지표 계산 추가

⏳ **3-2. Excel 시트 추가**
- Sheet 2: "Time Breakdown" 생성 로직
  - 시간 분해 테이블 작성
  - 파이 차트 추가
  - 연간 지표 작성
- Sheet 3: "Case Comparison" 생성 로직
  - Case별 시간 비교 표
  - 비교 차트 추가

⏳ **3-3. Word 섹션 추가**
- Section 4: "운항 시간 분석" 추가
  - 시간 분해 테이블
  - 파이 차트
  - 펌프 크기 변화 표
- Section 5: "시간-비용 상관성 분석" 추가
  - 메커니즘 설명
  - 민감도 분석 테이블
  - 시간-NPC 차트

⏳ **3-4. 신규 모듈**
- `src/time_structure.py`: TimeBreakdown 클래스
- `src/time_cost_analysis.py`: TimeCorrelationAnalysis 클래스

### 예상 작업량
- CSV 확장: ~30분 (간단)
- Excel 시트: ~1시간 (테이블 + 차트)
- Word 섹션: ~1.5시간 (내용 + 차트)
- 신규 모듈: ~30분
- 총합: ~3시간

---

## Phase 4: 실제 케이스 검증 (예정) ⏳

**상태**: 준비 완료, 실행 대기

### 검증 항목

⏳ **4-1. 제약식 바인딩 분석**
- 최적 시나리오에서 어느 제약식이 활성화되는가?
- 초기 연도 vs. 후기 연도 차이

⏳ **4-2. Case 2 시간 계산 검증**
- Case 2-1과 Case 2-2의 시간 차이
- 예상: Case 2-1이 55% 더 길어야 함
- 실제 결과와 비교

⏳ **4-3. 보고서 생성 검증**
- CSV: 시간 컬럼 정상 생성
- Excel: "Time Breakdown", "Case Comparison" 시트 생성
- Word: "운항 시간 분석", "시간-비용 상관성" 섹션 생성

⏳ **4-4. 시각화 검증**
- 파이 차트: 시간 구성이 정확히 표현되는가?
- 막대 차트: Case별 비교가 명확한가?
- 선 차트: 펌프 크기별 변화가 명확한가?

### 테스트 시나리오
1. Case 1 (부산) - 5,000 m³ 셔틀
2. Case 2-2 (울산) - 5,000 m³ 셔틀
3. Case 2-1 (여수) - 5,000 m³ 셔틀

**비교 점검**:
- 사이클 시간: Case 2-2 < Case 1 < Case 2-1
- 연간 항차: Case 2-2 > Case 1 > Case 2-1
- NPC: Case 2-2 < Case 1 < Case 2-1

---

## Phase 5: 최종 완성 (예정) ⏳

**상태**: 준비 완료, 실행 대기

### 최종화 항목

⏳ **5-1. 문서화**
- CLAUDE.md 업데이트 (시간 분석 추가)
- README 업데이트 (새로운 보고서 형식)
- 예시 보고서 생성

⏳ **5-2. 통합 테스트**
- 모든 Case (1, 2-1, 2-2) 동시 실행
- 모든 출력 형식 (CSV, Excel, Word) 검증
- 성능 확인

⏳ **5-3. 최종 검토**
- 보고서 가독성 확인
- 수치 정확성 재검증
- 차트 레이아웃 최적화

⏳ **5-4. Git Commit**
- 모든 변경사항 커밋
- 브랜치 푸시

---

## 예상 효과

### 사용자 관점
✅ **투명성 증가**
- 1회 운항 시간을 상세히 이해 가능
- 왜 이 펌프/셔틀 조합이 최적인지 명확해짐

✅ **의사결정 지원**
- 시간과 비용의 직접적 연계 가시화
- "펌프 크기 증가 → NPC 절감" 정량화

✅ **Case 비교 용이**
- Case 1, 2-1, 2-2의 시간 차이 명확
- 위치 선택의 중요성 증명

### 기술적 관점
✅ **모델 검증**
- 시간 계산이 전체 모델에 일관되게 반영됨을 증명
- 제약식과 비용 계산이 정상 작동함을 확인

✅ **확장성**
- TimeBreakdown, TimeCorrelationAnalysis 클래스 추가
- 향후 다른 분석에 재사용 가능

---

## 핵심 발견사항 요약

### ✅ 검증된 사항

1. **시간 계산은 정확함**
   - 3계층 아키텍처가 일관되게 작동
   - Case별 차이가 올바르게 반영됨

2. **시간이 NPC를 직접 결정함**
   - 펌프 크기 → 사이클 시간 → NPC
   - 시간-비용 트레이드오프 명확

3. **Case별 차이가 명확함**
   - Case 2-1의 긴 항해 = NPC 증가 (30%)
   - Case 2-2의 짧은 항해 = NPC 감소 (32%)

4. **제약식이 올바르게 작동함**
   - 작업시간 제약이 필요한 셔틀 수 결정
   - 일일 피크 제약은 대부분 loose

---

## 사용자에게 보여줄 최종 보고서 포함 내용

### CSV 예시
```
Shuttle_Size_cbm,Pump_Size_m3ph,Call_Duration_hr,Cycle_Duration_hr,
Shore_Loading_hr,Travel_Outbound_hr,Travel_Return_hr,Setup_Time_hr,
Pumping_Per_Vessel_hr,Movement_Per_Vessel_hr,Basic_Cycle_Duration_hr,
Annual_Cycles_Max,Vessels_per_Trip,Annual_Supply_m3,Time_Utilization_Ratio,
NPC_Total_USDm,...

5000,1000,12.00,15.33,3.33,2.00,2.00,1.00,5.00,1.00,12.00,522,1,2610000,65.2%,2768.12,...
5000,1200,10.00,13.75,3.33,2.00,2.00,1.00,3.33,1.00,10.42,582,1,2910000,75.0%,2751.45,...
```

### Excel 시트
- Sheet 2: Time Breakdown (최적 시나리오의 시간 분해)
- Sheet 3: Case Comparison (3가지 케이스의 시간 비교)

### Word 섹션
- Section 4: 운항 시간 분석 (시간 구성, 펌프 변화, Case 비교)
- Section 5: 시간-비용 상관성 (메커니즘, 절감액, 의사결정)

---

## 다음 단계

**지금**: Phase 1-2 계획 완료, 사용자 승인 대기 또는 Phase 3 진행 준비

**Phase 3**: 코드 구현 (~3시간)
**Phase 4**: 실제 케이스 검증 (~1시간)
**Phase 5**: 최종 완성 및 Git 커밋 (~1시간)

**전체 예상 소요 시간**: ~5시간

---

**작성자**: Claude Code Assistant
**최종 검토**: 2025-11-18

