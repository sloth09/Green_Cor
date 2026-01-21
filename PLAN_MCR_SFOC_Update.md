# MCR/SFOC 업데이트 및 Case 2-2 거리 수정 계획

**상태**: 보류 (나중에 논의 예정)
**작성일**: 2026-01-21
**관련 문서**: `docs/MCR_SFOC_Technical_Report.md`

---

## 목표
1. 셔틀의 MCR 값을 실제 선박 설계 관계에 기반하여 재계산:
   **Cargo Volume (m³) → Cargo Mass (ton) → DWT → MCR**
2. SFOC를 선박 크기별로 차등 적용
3. **Case 2-2 (울산→부산) 거리를 25해리 → 59해리로 수정**

## 배경
- 현재: cargo 용량(m³)을 직접 MCR에 매핑 (경험적 데이터)
- 문제: 실제 선박 설계 관계를 반영하지 않음
- 참조: `docs/mcr_dwt.png` - DWT vs SMCR power 그래프
- **Case 2-2 거리 수정**: 울산→부산 실제 거리 반영

---

## 1. 변환 공식

### Step 1: Cargo Volume → Cargo Mass
```
cargo_ton = cargo_m3 × 0.680 ton/m³
```

### Step 2: Cargo Mass → DWT
```
DWT = cargo_ton / cargo_fraction
DWT = cargo_ton / 0.80  (cargo가 DWT의 80% - 문헌 기반)
```

### Step 3: DWT → MCR (그래프 곡선에서 회귀 분석)
```
MCR = 17.17 × DWT^0.564
```
*그래프의 소형 선박 영역(5,000~50,000 DWT)에서 곡선 데이터 추출 후 최소제곱법 적용

---

## 2. 새 MCR 값 vs 기존 값 (새 공식: 17.17 × DWT^0.564)

| Cargo (m³) | Cargo (ton) | DWT (ton) | 새 MCR (kW) | 기존 MCR (kW) | 변화율 |
|------------|-------------|-----------|-------------|---------------|--------|
| 500 | 340 | 425 | 522 | 1,296 | -60% |
| 1,000 | 680 | 850 | 772 | 1,341 | -42% |
| 2,500 | 1,700 | 2,125 | 1,296 | 1,473 | -12% |
| 5,000 | 3,400 | 4,250 | 1,916 | 1,694 | +13% |
| 10,000 | 6,800 | 8,500 | 2,833 | 2,159 | +31% |
| 25,000 | 17,000 | 21,250 | 4,750 | 2,981 | +59% |
| 50,000 | 34,000 | 42,500 | 7,024 | 3,867 | +82% |

**특징**: 소형 셔틀 MCR 감소(-60%~-12%), 대형 셔틀 MCR 증가(+13%~+82%)
**보완**: SFOC 맵을 함께 적용하여 소형 셔틀의 연료비 균형 유지

---

## 3. 구현 단계

### Phase 1: 백업 (기존 결과 archive)
- [ ] `results/` 폴더를 `results/archive/pre_mcr_update_YYYYMMDD/`로 복사
- [ ] 기존 config 파일들 백업

### Phase 2: 새 모듈 생성
- [ ] `src/mcr_calculator.py` 생성 - MCR/SFOC 계산 로직
- [ ] `tests/test_mcr_calculator.py` 생성 - 단위 테스트

### Phase 3: Config 파일 업데이트
- [ ] `config/base.yaml`에 `mcr_calculation`, `sfoc_map` 섹션 추가
- [ ] `config/case_1.yaml` MCR 맵 업데이트
- [ ] `config/case_2_yeosu.yaml` MCR 맵 업데이트
- [ ] `config/case_2_ulsan.yaml` MCR 맵 업데이트
- [ ] **`config/case_2_ulsan.yaml` 거리 수정: 25해리 → 59해리**

### Phase 4: 코드 통합
- [ ] `src/utils.py`에 MCR/SFOC 계산 함수 추가
- [ ] `src/optimizer.py` MCR/SFOC 로딩 방식 수정
- [ ] `src/cost_calculator.py` SFOC 크기별 적용

### Phase 5: 실행 및 비교
- [ ] 모든 케이스 재실행 (`run_mode: "all"`)
- [ ] 기존 결과와 비교 분석
- [ ] `docs/changelog.md` 업데이트

---

## 4. 수정 파일 목록

| 파일 | 작업 |
|------|------|
| `src/mcr_calculator.py` | **신규** - MCR/SFOC 계산 클래스 |
| `config/base.yaml` | 수정 - mcr_calculation, sfoc_map 섹션 추가 |
| `config/case_1.yaml` | 수정 - mcr_map_kw 값 업데이트 |
| `config/case_2_yeosu.yaml` | 수정 - mcr_map_kw 값 업데이트 |
| `config/case_2_ulsan.yaml` | 수정 - mcr_map_kw 값 업데이트, 거리 59해리 |
| `src/utils.py` | 수정 - calculate_mcr_from_config, interpolate_sfoc 함수 추가 |
| `src/optimizer.py` | 수정 - SFOC 맵 로딩 및 적용 |
| `src/cost_calculator.py` | 수정 - SFOC 크기별 적용 |
| `tests/test_mcr_calculator.py` | **신규** - MCR/SFOC 테스트 |

---

## 5. 검증 방법

1. **단위 테스트**: MCR 계산 로직 검증
2. **통합 테스트**: 기존 테스트 모두 통과 확인
3. **결과 비교**:
   - NPC 변화율 확인 (예상: 연료비 증가로 NPC 상승)
   - 최적 시나리오 순위 변화 확인
   - LCOAmmonia 변화 확인

---

## 6. 문헌 조사 결과: Cargo/DWT 비율

### 참조 데이터 (LNG Carrier 실측)

| 선박 | Cargo (m³) | DWT (ton) | Cargo 무게 (ton) | Cargo/DWT |
|------|------------|-----------|------------------|-----------|
| Q-Max Mozah | 266,000 | 128,900 | 119,700* | 92.9% |
| Q-Max (기타) | 266,476 | 143,309 | 119,914* | 83.6% |
| 180,000 m³ LNG | 180,000 | 98,300 | 81,000* | 82.4% |
| Kool Firn | 174,096 | 82,287 | 78,343* | 95.2% |

*LNG 밀도 0.45 ton/m³ 적용

### 문헌 출처
- [LNG carrier - Wikipedia](https://en.wikipedia.org/wiki/LNG_carrier)
- [What Are LNG Carrier Ships? - Marine Insight](https://www.marineinsight.com/know-more/what-are-lng-carrier-ships/)
- [Gas carrier - Wikipedia](https://en.wikipedia.org/wiki/Gas_carrier)
- [Cargo Deadweight - ScienceDirect](https://www.sciencedirect.com/topics/engineering/cargo-deadweight)

### 결론
- **대형 LNG 캐리어**: Cargo/DWT ≈ **82-95%**
- **암모니아 캐리어**: 유사한 구조이나, 밀도가 높음 (0.68 vs 0.45 ton/m³)
- **권장값**: **80%** (보수적 추정, 작은 셔틀의 추가 장비 고려)

### 최종 결정
- **cargo_fraction = 0.80** (기존 0.60에서 변경)
- 그래프(mcr_dwt.png): bulk carrier 기준 그대로 적용 (사용자 확인됨)

---

## 7. SFOC (Specific Fuel Oil Consumption) 업데이트

### 문헌 조사 결과

| 엔진 타입 | 디젤 SFOC (g/kWh) | 암모니아 SFOC (g/kWh)* |
|----------|------------------|----------------------|
| 2-stroke 대형 (>10MW) | 155-180 | 350-400 |
| 4-stroke 중형 (2-10MW) | 180-225 | 400-500 |
| 4-stroke 소형 (<2MW) | 200-300 | 450-650 |

*암모니아 SFOC = 디젤 SFOC × (42.7/18.6) ≈ 2.3배 (발열량 비율)

### 문헌 출처
- [Specific Fuel Consumption for Marine Engines - Sustainable Ships](https://www.sustainable-ships.org/stories/2022/sfc)
- [SFOC Marine Engine - MDPI](https://www.mdpi.com/2077-1312/7/2/20)
- [MAN Engine Guide](https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf)

### 선박 크기별 SFOC 맵 (암모니아 연료 기준)

| Cargo (m³) | 엔진 타입 | 암모니아 SFOC (g/kWh) |
|------------|----------|---------------------|
| 500 | 4-stroke 소형 | 550 |
| 1,000 | 4-stroke 소형 | 520 |
| 2,500 | 4-stroke 중형 | 480 |
| 5,000 | 4-stroke 중형 | 450 |
| 10,000 | 4-stroke/2-stroke | 420 |
| 25,000 | 2-stroke | 390 |
| 50,000 | 2-stroke 대형 | 360 |

### 현재 vs 새로운 SFOC
- **현재**: 모든 크기에 379 g/kWh 고정
- **새로운**: 크기별 SFOC 맵 적용 (360-550 g/kWh)

---

## 8. 최종 연료비 영향 분석

**연료 소비 공식**: `Fuel = MCR × SFOC × Time / 10^6`

| Cargo (m³) | 기존 MCR×SFOC | 새 MCR×SFOC | 변화율 |
|------------|--------------|-------------|--------|
| 500 | 1296×379 = 491,184 | 522×550 = 287,100 | -42% |
| 1,000 | 1341×379 = 508,239 | 772×520 = 401,440 | -21% |
| 5,000 | 1694×379 = 642,026 | 1916×450 = 862,200 | +34% |
| 10,000 | 2159×379 = 818,261 | 2833×420 = 1,189,860 | +45% |
| 50,000 | 3867×379 = 1,465,593 | 7024×360 = 2,528,640 | +73% |

**결론**:
- 소형 셔틀(500-1000m³): 연료비 **감소** (MCR 감소 효과 > SFOC 증가 효과)
- 대형 셔틀(5000m³+): 연료비 **증가** (MCR 증가 효과 > SFOC 감소 효과)

**단위 화물당 연료비** (규모의 경제):
| Cargo (m³) | MCR×SFOC | 단위당 |
|------------|----------|--------|
| 500 | 287,100 | 574 |
| 5,000 | 862,200 | 172 |
| 50,000 | 2,528,640 | 51 |

대형 셔틀이 단위 화물당 **11배 효율적** (574 vs 51)

---

## 9. Case 2-2 거리 수정

### 현재 설정
- **Case 2-2 (울산→부산)**: 25 해리
- 편도 항해 시간: 25 / 15 = 1.67 시간

### 수정 설정
- **Case 2-2 (울산→부산)**: **59 해리**
- 편도 항해 시간: 59 / 15 = **3.93 시간**

### 영향
- 사이클 시간 증가: 왕복 추가 (59-25) × 2 / 15 = **4.53시간 증가**
- 연간 최대 항차 감소
- NPC 증가 예상

### 수정 파일
- `config/case_2_ulsan.yaml`: `travel_distance_nm: 59`
