# Paper Reframing Guide: Methodological Positioning

**Purpose**: 논문 텍스트에서 모델의 방법론적 기여를 정확하게 표현하기 위한 가이드.
`paper_evaluation.md` Section 3.1 (Methodological Depth) 비판 대응.

---

## 문제

현재 논문에서 다음과 같은 과대 주장이 있음:

| 현재 표현 | 문제점 |
|-----------|--------|
| "joint optimization of shuttle size and fleet" | 실제로는 grid search (열거). 셔틀 크기는 결정변수가 아니라 입력 파라미터 |
| "MILP optimization" 강조 | 각 조합별 LP가 단순. OR 저널 기대 수준 미달 |
| Gap 1에서 "joint optimization" 부재를 문제로 지적 | 정작 우리 모델도 진정한 joint optimization이 아님 |

**핵심**: 모델 자체는 바꾸지 않음. 결과도 동일. 논문 텍스트만 수정.

---

## 수정 원칙

### 1. "Joint Optimization" -> "Systematic Parametric Evaluation"

| Before | After |
|--------|-------|
| "jointly optimizes shuttle specifications and fleet size" | "systematically evaluates all feasible shuttle-pump combinations and optimizes fleet deployment for each" |
| "joint optimization framework" | "multi-period fleet sizing framework with parametric specification search" |

### 2. 방법론 기여 -> 응용 기여로 전환

| Before | After |
|--------|-------|
| "novel MILP formulation" | "MILP-based infrastructure planning framework applied to ammonia bunkering" |
| "optimization methodology" | "comparative planning framework" |
| "algorithmic contribution" | 이 표현 자체를 사용하지 않음 |

### 3. Contribution 재정의

현재 Contribution C1-C4 중 수정 대상:

**C1 (수정 필요)**:
- Before: "First joint optimization of shuttle vessel specifications and fleet sizing for ammonia bunkering"
- After: "First systematic comparison of port-based storage vs. remote supply configurations for ammonia bunkering under identical assumptions"

**C3 (수정 필요)**:
- Before: "Demand-robust fleet sizing methodology"
- After: "Demand scenario analysis demonstrating LCOA stability across 4x demand variation"

**C2, C4**: 유지 가능 (break-even rule, multi-period fleet expansion은 정확한 표현)

### 4. 강조해야 할 실제 강점

모델이 단순하더라도 논문의 실제 가치는:

| 강점 | 근거 |
|------|------|
| **3-case controlled comparison** | 동일 가정 하에 3개 공급 구성을 비교한 첫 연구 |
| **Break-even decision rule** | ~59.6 nm 교차점 = 항만 당국 직접 활용 가능 |
| **LCOA stability** | 수요 4배 변화에도 LCO 5.7% 변동 = 규모의 경제 입증 |
| **6-type sensitivity analysis** | 동종 논문 대비 민감도 분석 깊이 우수 |
| **Multi-period investment timing** | 21년간 연도별 최적 투자 시점 결정 |

---

## 수정 대상 파일

| 파일 | 수정 위치 | 내용 |
|------|----------|------|
| `docs/paper/paper_final.md` | Abstract | "joint optimization" -> "systematic evaluation" |
| `docs/paper/paper_final.md` | Section 1 (Introduction) | Gap statement, Contribution list (C1, C3) |
| `docs/paper/paper_final.md` | Section 3 (Methodology) | 모델 설명에서 grid search 구조를 솔직하게 기술 |
| `docs/paper/paper_final.md` | Section 5 (Discussion) | 방법론 한계를 장점(투명성, 재현성)으로 전환 |
| `docs/paper/02_contributions.md` | C1, C3 | 위 수정 반영 |
| `docs/paper/00_gap-statement.md` | Gap 1 | "joint optimization 부재" 대신 "systematic comparison 부재"로 |

---

## Methodology 섹션 추가 문구 예시

현재 논문에서 모델 구조를 기술하는 부분에 다음과 같은 솔직한 설명을 추가:

> The optimization follows a two-level approach. At the outer level, all feasible combinations of shuttle capacity (S) and pump flow rate (Q) are enumerated. At the inner level, for each (S, Q) pair, a multi-period MILP determines the optimal fleet deployment schedule over the 21-year planning horizon, minimizing total Net Present Cost subject to demand satisfaction and operational constraints. The optimal infrastructure specification is then selected as the (S, Q) combination yielding the lowest NPC across all evaluated pairs.
>
> This parametric evaluation approach, while computationally straightforward, offers two practical advantages: (1) it provides decision-makers with a complete cost landscape across all feasible specifications rather than a single optimal point, and (2) it enables direct comparison of heterogeneous supply configurations (port-based storage vs. remote supply) under identical assumptions.

---

## Discussion 섹션 추가 문구 예시

> The enumeration-based approach adopted in this study trades algorithmic sophistication for transparency and reproducibility. Unlike decomposition-based methods that may converge to local optima depending on initialization, the exhaustive evaluation guarantees global optimality within the discrete specification space. The computational cost remains manageable (< 30 seconds per case) given the modest problem size (10 shuttle sizes x 1 pump rate x 21 years), making the framework accessible to port authorities without specialized optimization expertise.

---

## 수정하면 안 되는 것

- 결과 숫자 (NPC, LCO, fleet size 등)
- 그림/테이블
- 수식 (Eq. 1-26)
- 민감도 분석 결과
- Limitation 섹션 (이미 잘 작성됨)

---

## 실행 방법

Claude Code에게:

```
@REFRAMING_GUIDE.md 를 참고해서 docs/paper/paper_final.md 의
methodological claims를 수정해줘. 결과나 수식은 건드리지 말고,
텍스트 표현만 바꿔줘.
```
