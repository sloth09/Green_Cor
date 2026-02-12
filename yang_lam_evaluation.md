# Yang & Lam DES Comparison - Critical Evaluation

## Overview

`scripts/run_yang_lam_comparison.py` 결과물에 대한 정직한 평가.
논문 삽입 전 반드시 검토해야 할 강점과 약점을 정리한다.

---

## 1. 강한 부분 (논문에 적극 활용)

### 1-1. Methodology Comparison Table (14 aspects)

가장 가치 있는 산출물. DES vs MILP의 구조적 차이를 명확히 보여준다.

| 핵심 차이 | Yang & Lam DES | Our MILP |
|-----------|---------------|----------|
| 목적 | 운영 성능 평가 | 투자 최적화 |
| Fleet | 고정 입력 (2-4척) | 최적화 출력 (1-14척) |
| 시간 범위 | 1년 snapshot | 21년 (2030-2050) |
| 비용 범위 | OPEX only | CAPEX + OPEX lifecycle |
| Queuing | 명시적 | 암묵적 (utilization 제약) |

- 리뷰어 질문 "왜 DES 대신 MILP?"에 대한 직접적 답변
- 상호보완성 논거 (DES = queuing dynamics, MILP = fleet optimization)가 sound
- Future Work F2 (hybrid DES-MILP)로 자연스럽게 연결

### 1-2. Flow Rate Sensitivity (58.8% vs 51.3%)

실질적으로 의미 있는 비교.

- deterministic formula가 DES보다 극단값에 더 민감 (7.5pp gap)
- 원인: DES의 삼각분포(TRIA) 평균화가 극단값을 smoothing
- 방법론적 차이에서 오는 체계적 편차이므로 논문에서 논의 가치 있음
- 다만 "matched params" 비교이므로 완전히 동일 조건은 아님

---

## 2. 약한 부분 (논문에서 과대해석 주의)

### 2-1. Service Time "1.1% Agreement" - 과장 위험

**문제**: raw gap이 24-31% (2.4h)인데, 우리가 모델링하지 않은 overhead를 더해서 1.1%로 맞춤.

```
Our raw:     setup(1.0h) + pumping(vol/flow) + setup(1.0h)
Yang DES:    mooring(1.55h) + doc(0.84h) + setup + pumping + setup
Adjusted:    Our raw + 2.39h overhead = Yang DES ~= 일치
```

이건 **pumping time 공식이 동일함을 확인**한 것이지, 모델 전체의 cross-validation이 아니다.
volume/flow_rate는 물리 법칙이므로 양쪽이 같은 건 당연하다.

**논문 권장 표현**:
- (X) "Service time agrees within 1.1%"
- (O) "Pumping time component is consistent across both models, confirming shared physical basis. The 2.4h gap is attributable to operational overhead (mooring, documentation) outside our model scope."

### 2-2. Annual Cost "1.1% Difference" - 우연의 일치

**문제**: 근본적으로 다른 것을 비교하고 있다.

| 항목 | Yang & Lam | Ours |
|------|-----------|------|
| 비용 범위 | OPEX only (charter + fuel) | CAPEX + OPEX (lifecycle) |
| 위치 | Singapore | Busan |
| 연료 | MFO (기존 연료) | Ammonia (대체 연료) |
| 연료가격 | $451/ton (MFO) | $600/ton (NH3) |
| 기간 | 1년 | 21년 평균 |

$13.7M vs $13.85M가 비슷한 건 **우연**이다.
OPEX-only와 CAPEX+OPEX 평균이 비슷하게 나온 건 CAPEX가 초기 집중되고 OPEX가 시간에 따라 증가하는 구조적 특성 때문이지, 모델이 일치해서가 아니다.

**논문 권장 표현**:
- (X) "Annual cost matches within 1.1%, validating our cost model"
- (O) "Both models yield annual costs in the same order of magnitude ($13-14M/yr), suggesting reasonable cost calibration despite fundamentally different scope and location"

### 2-3. Hardcoded Reference Data - 검증 필요

현재 Yang & Lam의 service time 값(actual: 7.95, 8.85, 10.10h / DES: 8.05, 8.98, 10.22h)은 **결과가 잘 나오도록 추정한 값**이다.

**반드시 해야 할 일**:
1. Yang & Lam (2023) 원논문에서 Table 4의 정확한 service time 값 확인
2. `YANG_VALIDATION_POINTS`의 `actual_h`, `des_h` 값을 원논문 값으로 교체
3. overhead 값(mooring 1.55h, documentation 0.84h)도 원논문에서 확인
4. 교체 후 adjusted difference가 여전히 합리적인지 재확인

---

## 3. 논문 삽입 전략

### 권장하는 프레이밍

> Section 5.x "Comparison with Published DES Model"

**단락 1**: 방법론 차이 (methodology table 기반)
- DES는 queuing과 stochastic service time을 포착
- MILP는 fleet sizing과 multi-year investment를 최적화
- 두 접근법은 상호배타적이 아닌 상호보완적

**단락 2**: 서비스 시간 일관성 (과장 없이)
- pumping time component가 양 모델에서 일치 (물리적 기반 공유)
- 2.4h gap은 DES가 모델링하는 operational overhead (mooring + documentation)
- MILP의 setup time (2.0h)은 이를 단순화한 것

**단락 3**: 민감도 구조 비교 (가장 강한 기여)
- flow rate가 양 모델에서 dominant factor
- deterministic이 stochastic보다 8pp 높은 민감도 (smoothing 효과)
- MILP는 추가로 CAPEX scaling, annual hours 등 투자 관련 파라미터 분석 가능

**단락 4**: Future Work 연결
- hybrid DES-MILP 접근: MILP로 fleet sizing -> DES로 operational validation
- DES의 queuing 결과를 MILP의 utilization constraint에 반영하는 iterative approach

### 피해야 할 표현

| 피할 것 | 대안 |
|---------|------|
| "validates our model" | "shows consistency in shared components" |
| "1.1% agreement" (헤드라인) | "same order of magnitude" |
| "cross-validation" | "benchmarking against published results" |
| "confirms accuracy" | "demonstrates reasonable calibration" |

---

## 4. 최종 판단

| 항목 | 등급 | 논문 활용도 |
|------|------|-----------|
| Methodology comparison | **A** | 메인 contribution, Table로 삽입 |
| Flow rate sensitivity | **B+** | Discussion에서 방법론 차이 논의 |
| Service time consistency | **B-** | 보조 근거로만, 과장 금지 |
| Annual cost similarity | **C** | 언급 정도, validation 주장 불가 |
| Hardcoded reference data | **D** | 원논문 확인 전까지 사용 불가 |

**결론**: 정성적 비교(방법론 차이, 상호보완성)는 강하고 논문의 약점을 보완한다. 정량적 비교(% 일치)는 supporting evidence 수준으로만 사용하고, headline claim으로 쓰면 리뷰어에게 오히려 신뢰를 잃을 수 있다.
