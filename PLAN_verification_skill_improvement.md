# Verification Skill 개선 및 보고서 재생성 계획

> 생성일: 2026-01-20
> 상태: 검토 대기

## 목표
1. Skill 수정: 수동 계산 → Python 결과 비교 → 반복 검증 워크플로우 추가
2. OPEX 검증을 각 Case 챕터의 서브 섹션으로 통합
3. 기존 보고서 archive 후 재생성

---

## Phase 1: 파일 정리 (Archive)

### 작업 내용
```
docs/verification/archive/  ← 새 폴더 생성
```

### 이동할 파일
- `00_index.md` ~ `11_formula_errors_report.md` (모든 md 파일)
- 타임스탬프 추가: `*_v1_20260120.md`

---

## Phase 2: Skill 파일 수정

### 대상 파일
`D:\code\Green_Cor\skills\verification-report.md`

### 2.1 챕터 구조 (8개 챕터)

**OPEX는 별도 챕터 없이 Case 챕터 내 서브 섹션으로 통합:**
```
docs/verification/
├── 00_index.md              # 목차
├── 01_executive_summary.md  # 요약
├── 02_parameters.md         # 파라미터
├── 03_case1_busan.md        # Case 1 (CAPEX + OPEX 통합)
├── 04_case2_yeosu.md        # Case 2-1 (CAPEX + OPEX 통합)
├── 05_case2_ulsan.md        # Case 2-2 (CAPEX + OPEX 통합)
├── 06_comparison.md         # 케이스 비교
├── 07_conclusion.md         # 결론
└── 08_error_report.md       # 오류 보고서 (필요시만 생성)
```

### 2.2 새 섹션 추가: "5단계 검증 워크플로우"

```markdown
## 5-Step Verification Workflow

### Step 1: 수동 계산 (Manual Calculation)
- 공식 적용, 모든 중간 단계 표시
- 예: CAPEX = 61,500,000 × (2500/40000)^0.75 = $7,687,500

### Step 2: Python 결과 추출
- CSV 파일에서 해당 값 찾기
- 컬럼 매핑 테이블 참조

### Step 3: 비교 및 판단
- Tolerance: CAPEX 1%, 시간 0.1%, NPC 0.5%
- |수동 - Python| / Python × 100% 계산

### Step 4: 불일치 시 처리
IF 불일치:
    1차: 수동 계산 재검토
    2차: Python 코드 추적
    IF Python 버그 발견:
        → 08_error_report.md에 기록
        → [FAIL - Python Bug] 표시
    ELSE:
        → 수동 계산 수정 후 Step 3 반복

### Step 5: 결과 테이블 생성
| Item | Manual | Python | Diff | Status |
|------|--------|--------|------|--------|
```

### 2.3 새 섹션 추가: "CSV 컬럼 매핑"

```markdown
## CSV Column Mapping

### Scenario Summary CSV (`MILP_scenario_summary_case_X.csv`)
| 검증 항목 | CSV 컬럼명 |
|----------|-----------|
| Cycle Duration | `Cycle_Duration_hr` |
| Annual Cycles | `Annual_Cycles_Max` |
| NPC Total | `NPC_Total_USDm` |
| Shuttle Fixed OPEX | `NPC_Shuttle_fOPEX_USDm` |
| Shuttle Variable OPEX | `NPC_Shuttle_vOPEX_USDm` |
| Bunkering Fixed OPEX | `NPC_Bunkering_fOPEX_USDm` |
| Bunkering Variable OPEX | `NPC_Bunkering_vOPEX_USDm` |
| Tank Fixed OPEX | `NPC_Terminal_fOPEX_USDm` |
| Tank Variable OPEX | `NPC_Terminal_vOPEX_USDm` |
| LCO Ammonia | `LCOAmmonia_USD_per_ton` |
| Annuity Factor | `Annuity_Factor` |
```

### 2.4 새 섹션 추가: "Case 챕터 구조 (CAPEX + OPEX 통합)"

```markdown
## Case Chapter Structure (03-05)

### 각 Case 챕터의 표준 구조
# Chapter N: Case X - [Name]

## N.1 Overview
## N.2 Cycle Time Calculation     ← 시간 검증
## N.3 CAPEX Verification         ← CAPEX 검증
   ### N.3.1 Shuttle CAPEX
   ### N.3.2 Bunkering CAPEX
   ### N.3.3 Tank CAPEX (Case 1 only)
## N.4 OPEX Verification          ← OPEX 검증 (통합)
   ### N.4.1 Shuttle Fixed OPEX
   ### N.4.2 Shuttle Variable OPEX (Fuel)
   ### N.4.3 Bunkering Fixed OPEX
   ### N.4.4 Bunkering Variable OPEX (Pump Fuel)
   ### N.4.5 Tank OPEX (Case 1 only)
## N.5 NPC Summary
## N.6 Shuttle Size Comparison
## N.7 Verification Summary

### OPEX 공식 (모든 Case 공통)
1. Shuttle Fixed OPEX = CAPEX × 0.05
2. Shuttle Variable OPEX = MCR × SFOC × Travel × Factor / 1e6 × Price
3. Bunkering Fixed OPEX = Bunkering_CAPEX × 0.05
4. Bunkering Variable OPEX = Pump_Power × Pump_hr × SFOC / 1e6 × Price
5. Tank OPEX (Case 1 only): Fixed + Variable (Cooling)

### Case별 차이점
| Parameter | Case 1 | Case 2-1 | Case 2-2 |
|-----------|--------|----------|----------|
| Travel Factor | 1.0 | 2.0 | 2.0 |
| Travel Time | 1.0 hr | 5.73 hr | 1.67 hr |
| Tank OPEX | Yes | No | No |
```

### 2.5 새 섹션 추가: "오류 처리 및 보고"

```markdown
## Error Handling

### 심각도 분류
| Severity | 설명 | 조치 |
|----------|------|------|
| HIGH | 최종 결과(NPC, LCO) 오류 | 즉시 중단, 보고 |
| MEDIUM | 중간값 불일치 | 계속, 보고서 기록 |
| LOW | 반올림 차이 (<0.5%) | 계속, 메모 |

### 중단 조건
1. HIGH 심각도 오류 발견 시 즉시 중단
2. 동일 섹션에서 3개 이상 오류 시 중단
3. 사용자에게 보고 후 진행 여부 결정
```

---

## Phase 3: 보고서 재생성

### 생성 순서 (총 8개 챕터)
1. `02_parameters.md` - 모든 파라미터 정의 (기초)
2. `03_case1_busan.md` - Case 1 (Cycle Time + CAPEX + **OPEX** 통합)
3. `04_case2_yeosu.md` - Case 2-1 (Cycle Time + CAPEX + **OPEX** 통합)
4. `05_case2_ulsan.md` - Case 2-2 (Cycle Time + CAPEX + **OPEX** 통합)
5. `06_comparison.md` - 케이스 비교 (모든 케이스 검증 후)
6. `08_error_report.md` - 오류 보고서 (검증 중 오류 발견 시만)
7. `01_executive_summary.md` - 요약 (모든 데이터 검증 후)
8. `07_conclusion.md` - 결론 체크리스트
9. `00_index.md` - 목차 업데이트 (마지막)

### 각 Case 챕터 (03-05) 작성 절차
각 섹션마다 5단계 워크플로우 적용:
1. **Cycle Time** - 수동 계산 → CSV 비교 → 검증
2. **CAPEX** - 수동 계산 → CSV 비교 → 검증
3. **OPEX** - 수동 계산 → CSV 비교 → 검증
4. **NPC** - 수동 계산 → CSV 비교 → 검증
5. 불일치 발견 시 즉시 보고 후 진행 여부 결정

---

## Phase 4: 검증 (QA)

### Cross-Document 일관성 검사
- 동일 셔틀 크기 → 동일 CAPEX (모든 문서)
- 동일 펌프 유량 → 동일 Pump Power (모든 문서)
- Annuity Factor = 10.8355 (모든 문서)

### CSV 정합성 검사
- 모든 검증된 값이 CSV 값과 tolerance 내 일치
- 컬럼명 정확히 참조

---

## 수정 대상 파일

| 파일 | 작업 |
|------|------|
| `skills/verification-report.md` | 5단계 워크플로우, Case 챕터 구조(OPEX 포함), 오류 처리 추가 |
| `docs/verification/archive/` | 기존 파일 이동 |
| `docs/verification/*.md` | 전체 재생성 (8개 파일 + 오류 보고서) |

---

## 예상 소요 시간

| Phase | 작업 | 예상 시간 |
|-------|------|----------|
| 1 | Archive 이동 | 5분 |
| 2 | Skill 파일 수정 | 30분 |
| 3 | 보고서 재생성 (8개) | 2시간 |
| 4 | QA 검증 | 15분 |

---

## 핵심 CSV 파일

```
results/MILP_scenario_summary_case_1.csv
results/MILP_scenario_summary_case_2_yeosu.csv
results/MILP_scenario_summary_case_2_ulsan.csv
```

### 주요 컬럼 (검증용)
- `Cycle_Duration_hr`, `Annual_Cycles_Max`
- `NPC_Total_USDm`, `LCOAmmonia_USD_per_ton`
- `NPC_Shuttle_fOPEX_USDm`, `NPC_Shuttle_vOPEX_USDm`
- `NPC_Bunkering_fOPEX_USDm`, `NPC_Bunkering_vOPEX_USDm`
- `Annuity_Factor` (10.8355)
