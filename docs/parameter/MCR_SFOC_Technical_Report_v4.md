# MCR 및 SFOC 기술 보고서
## MAN Energy Solutions 공식 데이터 기반 MCR 및 DWT 기반 SFOC 산정

**작성일**: 2026-01-21
**버전**: 4.1
**목적**: 암모니아 셔틀 선박의 MCR(Maximum Continuous Rating) 및 SFOC(Specific Fuel Oil Consumption) 산정을 위한 기술적 근거 문서화

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0 | 2026-01-21 | 초기 버전 |
| 2.0 | 2026-01-21 | 50,000m3 SFOC 반올림 수정: 360 -> 367 g/kWh |
| 3.0 | 2026-01-21 | MCR 값을 MAN Energy Solutions 공식 데이터 기반으로 전면 수정 |
| 4.0 | 2026-01-21 | SFOC를 MCR 기반으로 재산정, Case 2-2 거리 수정 (25nm -> 59nm) |
| **4.1** | **2026-01-21** | **SFOC를 DWT 기반으로 재산정 (엔진 타입 매칭 개선)** |

---

## 1. 개요

본 보고서는 Green Corridor 프로젝트의 암모니아 셔틀 선박에 대한 다음 사항을 분석합니다:

1. **Cargo Volume (m3) -> DWT (톤) 변환**: 셔틀 화물 용량에서 선박 재화중량톤 추산
2. **DWT -> MCR (kW) 변환**: MAN Energy Solutions 공식 데이터 기반 추진 엔진 출력 산정
3. **DWT -> SFOC (g/kWh) 변환**: DWT 범위별 엔진 타입 기반 SFOC 산정 **(v4.1 개선)**
4. **Case 2-2 거리 수정**: 25해리 -> 59해리 **(v4 신규)**

### 1.1 v4.1의 주요 변경점

**v4.0에서의 변경**:
- MCR: **변경 없음** (v3 MAN 데이터 유지)
- SFOC: **DWT 기반 재산정** (MCR 기반 -> DWT 기반 엔진 타입 매칭)
- Case 2-2 거리: 59nm 유지

**v4.1 SFOC 변경 근거**:
- v4.0의 MCR 기반 매핑은 실제 선박 관행과 불일치
- 대형 벌크/가스 캐리어는 DWT 15,000톤 이상에서 2-stroke 엔진 사용이 일반적
- DWT 기반 매핑이 실제 선박 엔진 선택 관행에 더 부합

---

## 2. v3 SFOC 산정 방법의 한계점

### 2.1 문제 분석

v2/v3 보고서에서 사용된 디젤 SFOC 값(240, 225, 210, 195, 185, 170, 160 g/kWh)은:

1. **DWT 기반 공식이 없음**: MCR처럼 DWT->SFOC 변환 공식 부재
2. **엔진 타입별 대략 추정**: 문헌에서 정확한 값 추출이 아님
3. **출처 링크 불일치**: 링크된 문서에서 해당 값 확인 불가

### 2.2 v2/v3 값 vs 실제 문헌 데이터

| 엔진 타입 | v2/v3 사용값 (g/kWh) | 실제 문헌 데이터 (g/kWh) | 출처 |
|----------|----------------------|-------------------------|------|
| 4-stroke 소형 | 240, 225 | **213-227** | USEPA 2009 |
| 4-stroke 중형 | 195-210 | **176-195** | Wartsila 20/31 |
| 2-stroke | 160-185 | **155-175** | MAN Engine Guide |

**결론**:
- 소형 4-stroke: v2/v3 값이 **5-13% 과대평가**
- 중형 이상: 대체로 일치하나 근거 불명확

---

## 3. v4.1 SFOC 산정 방법: DWT 기반

### 3.1 핵심 원리

**DWT(재화중량톤)를 기준으로 엔진 타입을 분류하고, 해당 엔진 타입의 문헌 SFOC를 적용**

실제 선박 엔진 선택은 MCR보다 선박 크기(DWT)에 더 직접적으로 연관됩니다:
- 소형 선박: 4-stroke 고속/중속 엔진 (기동성, 공간 제약)
- 대형 선박: 2-stroke 저속 엔진 (연비 우선, 장거리 운항)

| DWT 범위 (ton) | 엔진 타입 | 디젤 SFOC (g/kWh) | 암모니아 SFOC (g/kWh) | 문헌 출처 |
|----------------|----------|------------------|---------------------|----------|
| < 3,000 | 4-stroke 고속 | 220 | **505** | USEPA 2009 (213-227) |
| 3,000-8,000 | 4-stroke 중속 | 190 | **436** | Wartsila 20 (189-192) |
| 8,000-15,000 | 4-stroke 중형/소형 2-stroke | 180 | **413** | Wartsila 31, MAN 32/44CR |
| 15,000-30,000 | 2-stroke | 170 | **390** | MAN 2-stroke |
| > 30,000 | 2-stroke 대형 | 165 | **379** | MAN 2-stroke (최적) |

**암모니아 SFOC 변환**:
```
암모니아 SFOC = 디젤 SFOC x (42.7 / 18.6) = 디젤 SFOC x 2.295
```

### 3.2 DWT 기반 매핑의 근거

**MAN "Propulsion trends in bulk carriers" 문서 참조**:
- 30,000 DWT Handymax: 2-stroke ME-B 엔진 권장
- 42,000 DWT Handymax: 2-stroke 6S50ME-C 엔진 사용
- 대형 벌크/가스 캐리어는 DWT 15,000톤 이상에서 2-stroke가 표준

### 3.2 문헌 기반 SFOC 데이터

#### 확인된 데이터

| 출처 | 엔진 타입 | 디젤 SFOC (g/kWh) | 신뢰도 |
|------|----------|------------------|--------|
| **USEPA 2009** | 중속/고속 4-stroke | **213-227** | 높음 |
| **Wartsila 31** | 4-stroke 중형 (4.9-9.7MW) | **176.5** | 높음 |
| **Wartsila 20** | 4-stroke 소형 (1.1-2MW) | **189-192** | 높음 |
| **MAN 32/44CR** | 4-stroke 중형 (4.6-7.2MW) | **172-173** | 높음 |
| **MAN 2-stroke** | 대형 저속 | **155-175** | 높음 |
| **Fleet 평균** | 전체 | **206** | 중간 |

#### 문헌 출처 상세

1. **Merien-Paul et al. (2018)**. "In-situ data vs. bottom-up approaches in estimations of marine fuel consumptions and emissions". *Transportation Research Part D*, 62, 619-632.
   - p.623: "The typical SFOC for a slow speed diesel engine is about **165-195 g/kWh** and that of a medium/high speed engine is about **213-227 g/kWh** (USEPA, 2009)"
   - 문서 위치: `docs/parameter/1-s2.0-S1361920917309173-main.pdf`

2. **Wartsila 31 Datasheet**: https://www.wartsila.com/marine/products/engines-and-generating-sets/dual-fuel-engines/wartsila-31
   - 4-stroke 중형 (4.9-9.7MW): **176.5 g/kWh**

3. **Wartsila 20 Datasheet**
   - 4-stroke 소형 (1.1-2MW): **189-192 g/kWh**

4. **MAN 32/44CR Datasheet**: https://www.man-es.com/docs/default-source/document-sync/v32-44cr-propulsion-eng.pdf
   - 4-stroke 중형 (4.6-7.2MW): **172-173 g/kWh**

5. **MAN 2-stroke Engine Guide**: https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf
   - 대형 저속: **155-175 g/kWh**

---

## 4. v4.1 MCR 및 SFOC 값 산정

### 4.1 전체 MCR 및 SFOC 맵 (DWT 기반)

| Cargo (m3) | DWT (ton) | MCR (kW) | DWT 범위 | 엔진 타입 | 디젤 SFOC | **암모니아 SFOC** |
|------------|-----------|----------|----------|----------|-----------|------------------|
| 500 | 425 | 380 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 1,000 | 850 | 620 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 1,500 | 1,275 | 820 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 2,000 | 1,700 | 1,000 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 2,500 | 2,125 | 1,160 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 3,000 | 2,550 | 1,310 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 3,500 | 2,975 | 1,450 | <3,000 | 4-stroke 고속 | 220 | **505** |
| 4,000 | 3,400 | 1,580 | 3,000-8,000 | 4-stroke 중속 | 190 | **436** |
| 4,500 | 3,825 | 1,700 | 3,000-8,000 | 4-stroke 중속 | 190 | **436** |
| 5,000 | 4,250 | 1,810 | 3,000-8,000 | 4-stroke 중속 | 190 | **436** |
| 7,500 | 6,375 | 2,180 | 3,000-8,000 | 4-stroke 중속 | 190 | **436** |
| 10,000 | 8,500 | 2,420 | 8,000-15,000 | 4-stroke/소형 2-stroke | 180 | **413** |
| 15,000 | 12,750 | 3,080 | 8,000-15,000 | 4-stroke/소형 2-stroke | 180 | **413** |
| 20,000 | 17,000 | 3,660 | 15,000-30,000 | 2-stroke | 170 | **390** |
| 25,000 | 21,250 | 4,090 | 15,000-30,000 | 2-stroke | 170 | **390** |
| 30,000 | 25,500 | 4,510 | 15,000-30,000 | 2-stroke | 170 | **390** |
| 35,000 | 29,750 | 5,030 | 15,000-30,000 | 2-stroke | 170 | **390** |
| 40,000 | 34,000 | 5,620 | >30,000 | 2-stroke 대형 | 165 | **379** |
| 45,000 | 38,250 | 6,070 | >30,000 | 2-stroke 대형 | 165 | **379** |
| 50,000 | 42,500 | 6,510 | >30,000 | 2-stroke 대형 | 165 | **379** |

### 4.2 v4.0 vs v4.1 SFOC 비교

| Cargo (m3) | DWT (ton) | v4.0 SFOC | **v4.1 SFOC** | 변화 |
|------------|-----------|-----------|---------------|------|
| 500 | 425 | 505 | **505** | 0% |
| 1,000 | 850 | 505 | **505** | 0% |
| 3,500 | 2,975 | 448 | **505** | +13% |
| 5,000 | 4,250 | 448 | **436** | -3% |
| 10,000 | 8,500 | 425 | **413** | -3% |
| 15,000 | 12,750 | 425 | **413** | -3% |
| 20,000 | 17,000 | 425 | **390** | **-8%** |
| 30,000 | 25,500 | 425 | **390** | **-8%** |
| 35,000 | 29,750 | 402 | **390** | -3% |
| 50,000 | 42,500 | 402 | **379** | **-6%** |

**주요 변화 분석**:
- **소형 셔틀 (500-3,500m3)**: SFOC 증가 또는 유지 (4-stroke 고속 범위 확대)
- **중형 셔틀 (4,000-15,000m3)**: SFOC 소폭 감소 (-3%)
- **대형 셔틀 (20,000-50,000m3)**: SFOC 감소 (-6% ~ -8%) - 2-stroke 엔진 적용

---

## 5. 연료비 영향 분석 (v2 vs v4.1: MCR x SFOC)

### 5.1 MCR x SFOC 비교 (연료비 지표)

| Cargo (m3) | v2 (MCR x SFOC) | **v4.1 (MCR x SFOC)** | 변화율 |
|------------|-----------------|----------------------|--------|
| 500 | 287,100 | 380 x 505 = **191,900** | **-33%** |
| 1,000 | 401,440 | 620 x 505 = **313,100** | **-22%** |
| 2,500 | 622,080 | 1,160 x 505 = **585,800** | **-6%** |
| 5,000 | 862,200 | 1,810 x 436 = **789,160** | **-8%** |
| 10,000 | 1,189,860 | 2,420 x 413 = **999,460** | **-16%** |
| 25,000 | 1,852,500 | 4,090 x 390 = **1,595,100** | **-14%** |
| 50,000 | 2,577,808 | 6,510 x 379 = **2,467,290** | **-4%** |

### 5.2 결론

**v4.1 적용 시 연료비 변화 (v2 대비)**:
- **소형 셔틀 (500-1,000m3)**: MCR 감소 -> 연료비 **대폭 감소 (-22% ~ -33%)**
- **중형 셔틀 (2,500-15,000m3)**: MCR 감소 + SFOC 감소 -> 연료비 **감소 (-6% ~ -16%)**
- **대형 셔틀 (20,000-50,000m3)**: MCR 감소 + SFOC 감소(2-stroke) -> 연료비 **감소 (-4% ~ -14%)**

### 5.3 단위 화물당 연료비 (규모의 경제)

| Cargo (m3) | v4.1 MCR x SFOC | 화물당 연료비 | 규모의 경제 |
|------------|-----------------|--------------|------------|
| 500 | 191,900 | **384** | 기준 |
| 1,000 | 313,100 | **313** | 1.2배 효율 |
| 5,000 | 789,160 | **158** | 2.4배 효율 |
| 10,000 | 999,460 | **100** | 3.8배 효율 |
| 50,000 | 2,467,290 | **49** | **7.8배 효율** |

**결론**: 대형 셔틀의 규모의 경제 효과가 v4.0 대비 개선 (7.4배 -> 7.8배) - 2-stroke 엔진의 낮은 SFOC 반영

---

## 6. Case 2-2 거리 수정 (울산 -> 부산)

### 6.1 변경 내용

| 항목 | v3 | **v4** |
|------|-----|--------|
| 거리 | 25 해리 | **59 해리** |
| 편도 항해 시간 | 1.67 시간 | **3.93 시간** |

### 6.2 사이클 시간 영향

- 왕복 추가 시간: (59 - 25) x 2 / 15 = **4.53시간 증가**
- 예: 10,000m3 셔틀, 1,000 m3/h 펌프
  - v3 사이클: ~28시간
  - v4 사이클: ~33시간 (약 18% 증가)

### 6.3 NPC 영향

- 사이클 시간 증가 -> 연간 최대 항차 감소
- 동일 수요 충족을 위해 더 많은 셔틀 필요
- Case 2-2 NPC 증가 예상

---

## 7. Config 파일용 데이터

### 7.1 MCR 맵 (v3 유지)

#### Case 1 (부산항 내부, 500-10,000 m3)

```yaml
mcr_map_kw:
  500: 380
  1000: 620
  1500: 820
  2000: 1000
  2500: 1160
  3000: 1310
  3500: 1450
  4000: 1580
  4500: 1700
  5000: 1810
  7500: 2180
  10000: 2420
```

#### Case 2 (여수/울산 -> 부산, 2,500-50,000 m3)

```yaml
mcr_map_kw:
  2500: 1160
  5000: 1810
  10000: 2420
  15000: 3080
  20000: 3660
  25000: 4090
  30000: 4510
  35000: 5030
  40000: 5620
  45000: 6070
  50000: 6510
```

### 7.2 SFOC 맵 (v4.1 - DWT 기반)

```yaml
# SFOC 맵 (DWT 기반, 암모니아 연료)
sfoc_map_g_per_kwh:
  # DWT < 3,000 ton: 4-stroke 고속 (diesel 220 g/kWh)
  500: 505      # DWT 425
  1000: 505     # DWT 850
  1500: 505     # DWT 1,275
  2000: 505     # DWT 1,700
  2500: 505     # DWT 2,125
  3000: 505     # DWT 2,550
  3500: 505     # DWT 2,975
  # DWT 3,000-8,000 ton: 4-stroke 중속 (diesel 190 g/kWh)
  4000: 436     # DWT 3,400
  4500: 436     # DWT 3,825
  5000: 436     # DWT 4,250
  7500: 436     # DWT 6,375
  # DWT 8,000-15,000 ton: 4-stroke 중형/소형 2-stroke (diesel 180 g/kWh)
  10000: 413    # DWT 8,500
  15000: 413    # DWT 12,750
  # DWT 15,000-30,000 ton: 2-stroke (diesel 170 g/kWh)
  20000: 390    # DWT 17,000
  25000: 390    # DWT 21,250
  30000: 390    # DWT 25,500
  35000: 390    # DWT 29,750
  # DWT > 30,000 ton: 2-stroke 대형 (diesel 165 g/kWh)
  40000: 379    # DWT 34,000
  45000: 379    # DWT 38,250
  50000: 379    # DWT 42,500
```

### 7.3 Case 2-2 거리 설정 (v4 신규)

```yaml
route:
  source: "Ulsan"
  destination: "Busan"
  distance_nautical_miles: 59.0  # v3: 25.0 -> v4: 59.0
  ship_speed_knots: 15.0

operations:
  travel_time_hours: 3.93  # v3: 1.67 -> v4: 3.93
```

---

## 8. 참고문헌

### 8.1 MCR 관련 (v3)

1. **MAN Energy Solutions** (2022). "Propulsion trends in bulk carriers".
   - Table 4 (p.20): Ship particulars, SMCR point (5,000-42,000 DWT)
   - Table 5 (p.21): Ship particulars, SMCR point (55,000-120,000 DWT)
   - 문서 위치: `docs/parameter/propulsion-trends-in-bulk-carriers.pdf`

### 8.2 SFOC 관련 (v4 신규)

2. **Merien-Paul et al.** (2018). "In-situ data vs. bottom-up approaches in estimations of marine fuel consumptions and emissions". *Transportation Research Part D*, 62, 619-632.
   - 문서 위치: `docs/parameter/1-s2.0-S1361920917309173-main.pdf`
   - p.623: 저속 2-stroke **165-195 g/kWh**, 중속/고속 4-stroke **213-227 g/kWh**

3. **USEPA** (2009). "Current methodologies in preparing mobile source port-related emission inventories"
   - 중속/고속 4-stroke SFOC: **213-227 g/kWh**

4. **Wartsila 31 Datasheet**
   - https://www.wartsila.com/marine/products/engines-and-generating-sets/dual-fuel-engines/wartsila-31
   - 4-stroke 중형 (4.9-9.7MW): **176.5 g/kWh**

5. **Wartsila 20 Datasheet**
   - 4-stroke 소형 (1.1-2MW): **189-192 g/kWh**

6. **MAN 32/44CR Datasheet**
   - https://www.man-es.com/docs/default-source/document-sync/v32-44cr-propulsion-eng.pdf
   - 4-stroke 중형 (4.6-7.2MW): **172-173 g/kWh**

7. **MAN 2-stroke Engine Guide**
   - https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf
   - 대형 저속: **155-175 g/kWh**

### 8.3 DWT 및 가스 캐리어 관련

8. Wikipedia. "LNG carrier." https://en.wikipedia.org/wiki/LNG_carrier
9. Marine Insight. "Top 16 Biggest LNG Ships." https://www.marineinsight.com/types-of-ships/biggest-lng-ships/
10. ScienceDirect. "Cargo Deadweight." https://www.sciencedirect.com/topics/engineering/cargo-deadweight

---

## 9. 부록: 변환 공식 요약

### A. Cargo Volume -> DWT
```python
def cargo_to_dwt(cargo_m3, density=0.680, cargo_fraction=0.80):
    cargo_ton = cargo_m3 * density
    dwt = cargo_ton / cargo_fraction
    return dwt
```

### B. DWT -> MCR (v3: MAN 데이터 보간)
```python
def dwt_to_mcr_v3(dwt):
    """MAN Energy Solutions Table 4-6 기반 MCR 보간"""
    man_data = {
        5000: 1950, 8000: 2370, 10000: 2550,
        20000: 3940, 30000: 5090, 35000: 5760, 42000: 6500
    }
    # 선형 보간 적용
    ...
```

### C. DWT -> SFOC (v4.1)
```python
def dwt_to_sfoc(dwt_ton):
    """DWT 기반 암모니아 SFOC 산정 (g/kWh)"""
    if dwt_ton < 3000:
        return 505      # 4-stroke 고속
    elif dwt_ton < 8000:
        return 436      # 4-stroke 중속
    elif dwt_ton < 15000:
        return 413      # 4-stroke 중형/소형 2-stroke
    elif dwt_ton < 30000:
        return 390      # 2-stroke
    else:
        return 379      # 2-stroke 대형
```

### D. SFOC 보간 (Cargo 크기 기반)
```python
def interpolate_sfoc(cargo_m3, sfoc_map):
    """
    sfoc_map (v4.1 DWT 기반) = {
        500: 505, 1000: 505, 1500: 505, 2000: 505, 2500: 505, 3000: 505, 3500: 505,
        4000: 436, 4500: 436, 5000: 436, 7500: 436,
        10000: 413, 15000: 413,
        20000: 390, 25000: 390, 30000: 390, 35000: 390,
        40000: 379, 45000: 379, 50000: 379
    }
    """
    # 선형 보간 적용
    ...
```

---

*본 보고서는 Green Corridor 암모니아 벙커링 최적화 프로젝트의 기술 문서입니다.*
*v4.1 업데이트: DWT 기반 SFOC 재산정 (엔진 타입 매칭 개선), Case 2-2 거리 수정 (25nm -> 59nm)*
