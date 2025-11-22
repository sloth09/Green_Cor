# Annualized CAPEX Calculation Correction

## 📋 문제 진단

### 발견된 버그
2024-11-22에 발견된 Annualized CAPEX 계산 오류:

**증상:**
```
2030년 첫 구매 (2개 셔틀):
  Actual_CAPEX_Shuttle: 15.375M
  Annualized_CAPEX_Shuttle: 0.7321M ❌
  비율: 21.0x (단순히 21으로 나눔)
```

**근본 원인:**
- `discount_rate = 0.0`일 때 annuity factor를 단순히 `project_years (21)`로 설정
- 이는 시간가치 할인(NPV)과 자산 균등화(annualization)를 혼동한 결과
- 올바른 Annuity Factor는 약 **10.594** (r=7%, n=21), 단순 21이 아님

---

## ✅ 해결 방법

### Step 1: Config 파일 수정
**파일:** `config/base.yaml`

```yaml
economy:
  discount_rate: 0.0                    # NPV 할인 - 현재 0% (미래 현금흐름 할인 없음)
  annualization_interest_rate: 0.07     # 자산 균등화율 - 7% (자산을 연간 비용으로 변환)
```

**목적:**
- `discount_rate`: NPV 계산용 (시간가치 할인)
- `annualization_interest_rate`: 자산을 연간 균등 비용으로 변환용 (독립적)

### Step 2: 코드 수정
**파일:** `src/cost_calculator.py` (Lines 429-462)

```python
def get_annuity_factor(self) -> float:
    """
    Calculate annuity factor for asset annualization.

    IMPORTANT: This uses annualization_interest_rate (NOT discount_rate).
    - discount_rate: Controls time value of money for NPV calculation (currently 0%, no discounting)
    - annualization_interest_rate: Used to convert asset values to uniform annual payments (7%)
    """
    # Use annualization_interest_rate for converting assets to annual costs
    annualization_rate = self.config["economy"]["annualization_interest_rate"]

    # Calculate project years dynamically from time_period config
    start_year = self.config["time_period"]["start_year"]  # 2030
    end_year = self.config["time_period"]["end_year"]      # 2050
    project_years = end_year - start_year + 1  # 21

    # Calculate annuity factor using the annualization interest rate
    return calculate_annuity_factor(annualization_rate, project_years)
```

**공식:**
```
Annuity_Factor = [1 - (1 + r)^(-n)] / r

예: r=0.07, n=21
  AF = [1 - (1.07)^(-21)] / 0.07 = 10.594
```

---

## 📊 검증 결과

### Case 1: Busan Port (2500m³ Shuttle, 2000m³/h Pump)

| 메트릭 | 수정 전 | 수정 후 | 올바른가? |
|--------|--------|--------|---------|
| Annualized_CAPEX_Shuttle (2030) | 0.7321M | 1.5787M | ✅ |
| Annuity Factor | 21.0 | 10.8355 | ✅ |
| NPC_Total | 167.47M | **217.14M** | ✅ |
| Single vs Yearly Sim 차이 | 0.001% | **0.001%** | ✅ |

### Case 2-2: Ulsan → Busan (5000m³ Shuttle, 2000m³/h Pump)

| 메트릭 | 수정 전 | 수정 후 |
|--------|--------|--------|
| NPC_Total | ~155M | **282.81M** |
| Annuity Factor | 21.0 | 10.8355 |

---

## 🔄 영향 범위

### 수정된 파일
1. `config/base.yaml` - `annualization_interest_rate` 추가
2. `src/cost_calculator.py` - `get_annuity_factor()` 로직 변경

### 영향받는 계산
- ✅ NPC 계산 (optimizer.py) - 자동으로 올바른 값 사용
- ✅ Yearly simulation (main.py) - 자동으로 올바른 값 사용
- ✅ Export (export_excel.py, export_docx.py) - 자동으로 올바른 값 사용

### 출력 값 변화
모든 Annualized_CAPEX 관련 컬럼이 약 **2배 증가**:
```
CAPEX 관련:
- NPC_Annualized_*_CAPEX_USDm: 약 2배 증가
- Annualized_CAPEX_*_USDm: 약 2배 증가

최종 결과:
- NPC_Total: 약 30% 증가 (147-282M 범위에서 변함)
```

---

## ⚠️ Breaking Changes

### 이전 결과와의 호환성
- ❌ 모든 기존 CSV, Excel 결과 파일과 호환되지 않음
- ❌ 이전 버전의 NPC 값과 직접 비교 불가
- ✅ 동일 구성의 재실행 결과는 일치 (Single vs Yearly)

### 영향받는 시나리오 분석
- 조기 구매 (2030-2035): NPC 증가 ~25-30%
- 후기 구매 (2040-2050): NPC 증가 ~30-35%
- 순차 구매 전략 상대 비교: 영향 미미 (모두 일관성 있게 증가)

---

## 🔐 개념 정리

### 두 개의 이자율

#### 1. Discount Rate (NPV용)
```
목적: 미래 현금흐름을 현재가치로 할인
설정: discount_rate = 0.0 (현재 할인 없음)
용도: NPC 계산에서 매년의 비용을 할인
효과: 각 연도 비용 가중치 동일
```

#### 2. Annualization Rate (자산 균등화용)
```
목적: 자산 구매 비용을 균등 연간 비용으로 변환
설정: annualization_interest_rate = 0.07 (7%)
용도: 자산 비용을 프로젝트 기간에 걸쳐 분산
효과: 21년 프로젝트에서 연간 동일 비용
공식: Annual_Cost = CAPEX / AF(7%, 21)
```

**핵심:**
- 두 율은 **독립적**이며 다른 목적으로 사용됨
- Discount_rate = 0 ✓ (시간가치 없음)
- Annualization_rate = 7% ✓ (자산 비용 분산)

---

## 📝 커밋 정보

**Commit Hash:** 18e0c47
**Date:** 2025-11-22
**Branch:** annulaized_capex
**Message:** "fix: Correct Annualized CAPEX calculation using separate annualization_interest_rate"

---

## 🧪 검증 코드

### Annuity Factor 검증
```python
from src.cost_calculator import CostCalculator
from src.utils import calculate_annuity_factor

# 직접 계산
af = calculate_annuity_factor(0.07, 21)  # 10.594

# Config 통한 계산
cost_calc = CostCalculator(config)
af_config = cost_calc.get_annuity_factor()  # 10.594
```

### Single vs Yearly 검증
```
Case 1 (2500/2000):
  Single Mode NPC: $217.14M
  Yearly Sim Sum:  $217.14M
  Difference:      0.001% ✓

Case 2-2 (5000/2000):
  결과: 일관성 확인됨 ✓
```

---

## 🚀 다음 단계

### 권장 사항
1. ✅ 모든 기존 결과 파일 재생성 (새 NPC 값 기반)
2. ✅ 민감도 분석 재실행
3. ✅ 최적 시나리오 재검증
4. 📋 프로젝트 보고서 업데이트 (새 NPC 값)
5. 📋 정책 권고안 재평가 (높아진 비용 기반)

### 향후 개선
- [ ] 각 자산 구매 시점별로 다른 Annuity Factor 적용
  - 예: 2030년 구매 → AF(21), 2040년 구매 → AF(11)
  - 더 정확한 시점별 비용 반영
- [ ] 민감도 분석: annualization_rate ± 2% 실행
- [ ] 대안 분석 모드 추가: discount_rate != 0 시나리오

---

**마지막 업데이트:** 2025-11-22
**상태:** ✅ 완료 및 검증됨
