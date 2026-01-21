# MCR 및 SFOC 기술 보고서
## Cargo Volume → DWT → MCR 변환 및 SFOC 분석

**작성일**: 2026-01-21
**버전**: 1.0
**목적**: 암모니아 셔틀 선박의 MCR(Maximum Continuous Rating) 및 SFOC(Specific Fuel Oil Consumption) 산정을 위한 기술적 근거 문서화

---

## 1. 개요

본 보고서는 Green Corridor 프로젝트의 암모니아 셔틀 선박에 대한 다음 사항을 분석합니다:

1. **Cargo Volume (m³) → DWT (톤) 변환**: 셔틀 화물 용량에서 선박 재화중량톤 추산
2. **DWT → MCR (kW) 변환**: 선박 크기에 따른 추진 엔진 출력 산정
3. **SFOC (g/kWh) 맵**: 엔진 크기별 연료 소비율 산정

---

## 2. Cargo Volume → DWT 변환

### 2.1 DWT (Deadweight Tonnage) 정의

DWT(재화중량톤)는 선박이 안전하게 운반할 수 있는 총 중량으로, 화물, 연료, 담수, 평형수, 승무원 및 물자를 포함합니다 ([Deadweight Tonnage - Holistic Training](https://holistiquetraining.com/en/news/a-complete-guide-to-deadweight-tonnage-dwt)).

**DWT 구성요소**:
- Cargo (화물)
- Fuel oil
- Fresh water
- Ballast water
- Provisions & stores
- Crew & passengers

**DWCC (Deadweight Cargo Capacity)**는 실제 수익 창출 화물 용량으로, DWT에서 연료, 물, 물자 등을 제외한 값입니다 ([ScienceDirect - Cargo Deadweight](https://www.sciencedirect.com/topics/engineering/cargo-deadweight)).

### 2.2 LNG 캐리어 실측 데이터

가스 캐리어의 경우 화물 밀도가 낮아(0.42~0.97 ton/m³), 용량은 주로 체적(m³)으로 표기됩니다 ([Gas Tankers - Cult of Sea](https://www.cultofsea.com/cargo-work/gas-tankers-basic-definitions-hazards/)).

다음은 실제 LNG 캐리어의 Cargo/DWT 비율 분석입니다:

| 선박명 | Cargo 용량 (m³) | DWT (ton) | Cargo 무게 (ton)* | Cargo/DWT 비율 | 출처 |
|--------|----------------|-----------|-------------------|----------------|------|
| Q-Max Mozah | 266,000 | 128,900 | 119,700 | **92.9%** | [Wikipedia - LNG Carrier](https://en.wikipedia.org/wiki/LNG_carrier) |
| Q-Max (기타) | 266,476 | 143,309 | 119,914 | **83.6%** | [Marine Insight - Biggest LNG Ships](https://www.marineinsight.com/types-of-ships/biggest-lng-ships/) |
| 180,000 m³ LNG | 180,000 | 98,300 | 81,000 | **82.4%** | [Maritime Optima - LNG Carriers](https://maritimeoptima.com/insights/different-type-and-sizes-of-liquefied-natural-gas-lng-carriers) |
| Kool Firn | 174,096 | 82,287 | 78,343 | **95.2%** | [Marine Insight - Biggest LNG Ships](https://www.marineinsight.com/types-of-ships/biggest-lng-ships/) |

*LNG 밀도 0.45 ton/m³ 적용

### 2.3 암모니아 캐리어 특성

암모니아 캐리어는 LPG/가스 캐리어와 유사한 구조를 사용합니다:

- **저장 온도**: -33°C ~ -48°C (LNG의 -163°C보다 높음)
- **탱크 타입**: Type A 탱크 사용 가능 ([Wikipedia - Gas Carrier](https://en.wikipedia.org/wiki/Gas_carrier))
- **암모니아 밀도**: 0.680 ton/m³ (LNG 0.45 ton/m³보다 높음)

현재 암모니아는 주로 약 1,000 m³ 용량의 연안 선박으로 운송됩니다. 대형 암모니아 캐리어(VLAC)는 100,000 m³까지 가능합니다 ([Ammonia Energy - MOL Ammonia Carriers](https://ammoniaenergy.org/articles/mitsui-o-s-k-lines-ammonia-fueled-capesize-bulkers-chemical-tankers-to-hit-the-water-from-next-year/)).

### 2.4 Cargo/DWT 비율 결정

**분석 결과**:
- 대형 LNG 캐리어: Cargo/DWT ≈ 82-95%
- 평균값: 약 88%
- 소형 가스 캐리어: 추가 장비 비중이 높아 비율이 다소 낮을 수 있음

**본 프로젝트 적용값**: **cargo_fraction = 0.80 (80%)**

선정 근거:
1. LNG 캐리어 실측 데이터 평균(88%)보다 보수적으로 설정
2. 소형 셔틀의 상대적으로 높은 장비 비중 고려
3. 암모니아 캐리어의 추가 안전 장비 고려

### 2.5 변환 공식

```
Step 1: Cargo Volume → Cargo Mass
        cargo_ton = cargo_m3 × 0.680 ton/m³

Step 2: Cargo Mass → DWT
        DWT = cargo_ton / 0.80
```

**예시 계산**:
| Cargo 체적 (m³) | Cargo 무게 (ton) | 추산 DWT (ton) | 검증: Cargo/DWT |
|----------------|-----------------|----------------|-----------------|
| 500 | 340 | 425 | 340/425 = 80% ✓ |
| 5,000 | 3,400 | 4,250 | 3,400/4,250 = 80% ✓ |
| 50,000 | 34,000 | 42,500 | 34,000/42,500 = 80% ✓ |

**주의**:
- Cargo 무게(ton) < DWT(ton): **정상** (DWT = cargo + 연료 + 물 + 기타)
- Cargo 체적(m³)과 DWT(ton)는 **단위가 달라 직접 비교 불가**
- 암모니아 밀도(0.68 ton/m³)가 LNG(0.45 ton/m³)보다 높아 같은 체적에 더 무거운 cargo

---

## 3. DWT → MCR 변환

### 3.1 MCR (Maximum Continuous Rating) 정의

MCR은 선박 엔진이 안전하게 연속 운전할 수 있는 최대 출력(kW)입니다.

선박 크기와 추진 동력 간에는 비선형적 관계가 있습니다. 일반적으로:
- 선박 저항은 속도의 약 3승에 비례
- 필요 동력은 DWT의 약 0.5~0.7승에 비례

([Sustainable Ships - Specific Fuel Consumption](https://www.sustainable-ships.org/stories/2022/sfc))

### 3.2 참조 그래프 분석

본 프로젝트는 `docs/mcr_dwt.png` 그래프(Fig. 13: Propulsion SMCR power as a function of dwt)를 참조합니다.

**그래프에서 추출한 데이터 포인트**:

| 선박 타입 | DWT (ton) | SMCR (kW) | 출처 |
|----------|-----------|-----------|------|
| Small Handysize | ~25,000 | ~5,500 | docs/mcr_dwt.png |
| Handymax | ~50,000 | ~7,500 | docs/mcr_dwt.png |
| Kamsarmax | ~80,000 | ~10,000 | docs/mcr_dwt.png |
| Newcastlemax (AUS) | ~180,000 | ~15,500 | docs/mcr_dwt.png |
| Dunkirkmax | ~180,000 | ~15,000 | docs/mcr_dwt.png |
| Chinamax | ~400,000 | ~25,000 | docs/mcr_dwt.png |

### 3.3 회귀 분석 및 공식 도출

그래프의 **곡선**에서 소형 선박 영역(5,000~50,000 DWT)의 데이터를 추출하여 회귀 분석:

**곡선에서 추출한 데이터**:
| DWT (ton) | SMCR (kW) |
|-----------|-----------|
| 5,000 | ~2,000 |
| 10,000 | ~3,200 |
| 15,000 | ~4,000 |
| 20,000 | ~4,700 |
| 25,000 | ~5,300 |
| 30,000 | ~5,800 |
| 40,000 | ~6,700 |
| 50,000 | ~7,400 |

**Power Law 회귀 분석** (최소제곱법):
```
MCR = a × DWT^b

여기서:
- a = 17.17 (계수)
- b = 0.564 (지수)
```

**검증**:
| DWT (ton) | 곡선 실측 (kW) | 공식 계산 (kW) | 오차 |
|-----------|---------------|----------------|------|
| 5,000 | ~2,000 | 2,100 | +5.0% |
| 10,000 | ~3,200 | 3,105 | -3.0% |
| 15,000 | ~4,000 | 3,903 | -2.4% |
| 20,000 | ~4,700 | 4,591 | -2.3% |
| 25,000 | ~5,300 | 5,207 | -1.8% |
| 30,000 | ~5,800 | 5,771 | -0.5% |
| 40,000 | ~6,700 | 6,788 | +1.3% |
| 50,000 | ~7,400 | 7,699 | +4.0% |

**오차 범위**: ±5% 이내 (우리 셔틀 범위에 최적화)

**참고**: 그래프는 bulk carrier 기준이며, 암모니아/가스 캐리어와 다소 차이가 있을 수 있습니다. 그러나 추진 시스템의 기본 원리는 유사하므로 적용 가능합니다 ([MAN Engine Guide](https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf)).

### 3.4 산정된 MCR 값

| Cargo (m³) | Cargo (ton)* | DWT (ton) | MCR (kW) | 계산식 |
|------------|-------------|-----------|----------|--------|
| 500 | 340 | 425 | 522 | 17.17 × 425^0.564 |
| 1,000 | 680 | 850 | 772 | 17.17 × 850^0.564 |
| 1,500 | 1,020 | 1,275 | 979 | 17.17 × 1275^0.564 |
| 2,000 | 1,360 | 1,700 | 1,153 | 17.17 × 1700^0.564 |
| 2,500 | 1,700 | 2,125 | 1,296 | 17.17 × 2125^0.564 |
| 3,000 | 2,040 | 2,550 | 1,438 | 17.17 × 2550^0.564 |
| 3,500 | 2,380 | 2,975 | 1,565 | 17.17 × 2975^0.564 |
| 4,000 | 2,720 | 3,400 | 1,684 | 17.17 × 3400^0.564 |
| 4,500 | 3,060 | 3,825 | 1,803 | 17.17 × 3825^0.564 |
| 5,000 | 3,400 | 4,250 | 1,916 | 17.17 × 4250^0.564 |
| 7,500 | 5,100 | 6,375 | 2,429 | 17.17 × 6375^0.564 |
| 10,000 | 6,800 | 8,500 | 2,833 | 17.17 × 8500^0.564 |
| 15,000 | 10,200 | 12,750 | 3,577 | 17.17 × 12750^0.564 |
| 20,000 | 13,600 | 17,000 | 4,191 | 17.17 × 17000^0.564 |
| 25,000 | 17,000 | 21,250 | 4,750 | 17.17 × 21250^0.564 |
| 30,000 | 20,400 | 25,500 | 5,269 | 17.17 × 25500^0.564 |
| 35,000 | 23,800 | 29,750 | 5,754 | 17.17 × 29750^0.564 |
| 40,000 | 27,200 | 34,000 | 6,216 | 17.17 × 34000^0.564 |
| 45,000 | 30,600 | 38,250 | 6,654 | 17.17 × 38250^0.564 |
| 50,000 | 34,000 | 42,500 | 7,024 | 17.17 × 42500^0.564 |

*Cargo (ton) = Cargo (m³) × 0.680 ton/m³ (암모니아 밀도)
**DWT = Cargo (ton) / 0.80 (cargo가 DWT의 80%)

---

## 4. SFOC (Specific Fuel Oil Consumption) 분석

### 4.1 SFOC 정의

SFOC(비연료소비율)는 단위 출력당 연료 소비량으로, g/kWh 단위로 표시됩니다 ([Marine Gyaan - What is SFOC?](https://marinegyaan.com/what-is-sfoc-how-to-calculate-sfoc/)).

```
SFOC (g/kWh) = 연료 소비량 (g/h) / 출력 (kW)
```

### 4.2 엔진 타입별 SFOC

해양 엔진의 SFOC는 엔진 타입, 크기, 부하에 따라 크게 달라집니다:

| 엔진 타입 | 일반적 SFOC 범위 | 최적 부하 | 출처 |
|----------|-----------------|----------|------|
| 2-stroke 대형 (저속) | 155-180 g/kWh | 75-85% MCR | [Sustainable Ships - SFC](https://www.sustainable-ships.org/stories/2022/sfc) |
| 4-stroke 중형 (중속) | 180-225 g/kWh | 70-80% MCR | [MDPI - SFOC Prediction](https://www.mdpi.com/2077-1312/7/2/20) |
| 4-stroke 소형 (고속) | 200-300 g/kWh | 70-80% MCR | [DG Marine - SFOC](https://www.dgmarine.in/2023/04/improving-fuel-efficiency-in-marine-Engines.html) |
| 구형/비효율 엔진 | 400-600 g/kWh | - | [Marine Site - SFOC](https://www.marinesite.info/2014/03/specific-fuel-oil-consumption.html) |

**2-stroke vs 4-stroke 엔진**:
- **2-stroke**: 대형 선박에 사용, 높은 효율, 낮은 SFOC (155-180 g/kWh)
- **4-stroke**: 중소형 선박에 사용, 상대적으로 낮은 효율, 높은 SFOC (180-300 g/kWh)

([MAN Engine Guide - STG Online](https://www.stg-online.org/onTEAM/shipefficiency/programm/Clausen.pdf))

### 4.3 암모니아 연료 SFOC

암모니아는 디젤/HFO 대비 낮은 발열량을 가집니다:

| 연료 | 저위발열량 (LHV) | 출처 |
|------|-----------------|------|
| Heavy Fuel Oil (HFO) | 40.2 MJ/kg | Industry standard |
| Marine Gas Oil (MGO) | 42.7 MJ/kg | Industry standard |
| Ammonia (NH3) | 18.6 MJ/kg | [Nature - Ammonia-Diesel Engine](https://www.nature.com/articles/s41598-025-04997-z) |

**암모니아 SFOC 변환**:
```
암모니아 SFOC = 디젤 SFOC × (디젤 LHV / 암모니아 LHV)
             = 디젤 SFOC × (42.7 / 18.6)
             = 디젤 SFOC × 2.295
```

([ScienceDirect - Ammonia Dual-Fuel Review](https://www.sciencedirect.com/science/article/pii/S0378382025000293))

### 4.4 선박 크기별 SFOC 맵 (암모니아 연료)

**기준점 데이터** (문헌 기반):

| Cargo (m³) | 추정 엔진 타입 | 디젤 SFOC (g/kWh) | 암모니아 SFOC (g/kWh) | 근거 |
|------------|--------------|------------------|---------------------|------|
| 500 | 4-stroke 소형 | 240 | 550 | 소형 엔진 효율 저하 ([Sustainable Ships](https://www.sustainable-ships.org/stories/2022/sfc)) |
| 1,000 | 4-stroke 소형 | 225 | 520 | 소형 엔진 ([Sustainable Ships](https://www.sustainable-ships.org/stories/2022/sfc)) |
| 2,500 | 4-stroke 중형 | 210 | 480 | 중형 엔진 ([MDPI](https://www.mdpi.com/2077-1312/7/2/20)) |
| 5,000 | 4-stroke 중형 | 195 | 450 | 중형 엔진 효율 개선 ([MDPI](https://www.mdpi.com/2077-1312/7/2/20)) |
| 10,000 | 4-stroke/2-stroke | 185 | 420 | 대형화 전환점 ([MAN Guide](https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf)) |
| 25,000 | 2-stroke | 170 | 390 | 2-stroke 대형 ([MAN Guide](https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf)) |
| 50,000 | 2-stroke 대형 | 160 | 360 | 대형 2-stroke 고효율 ([MAN Guide](https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf)) |

### 4.5 산정된 SFOC 값 (전체 셔틀 범위)

| Cargo (m³) | Cargo (ton)* | DWT (ton) | 엔진 타입 | 디젤 SFOC (g/kWh) | 암모니아 SFOC (g/kWh)** |
|------------|-------------|-----------|----------|------------------|----------------------|
| 500 | 340 | 425 | 4-stroke 소형 | 240 | 550 |
| 1,000 | 680 | 850 | 4-stroke 소형 | 225 | 520 |
| 1,500 | 1,020 | 1,275 | 4-stroke 소형 | 217 | 500 |
| 2,000 | 1,360 | 1,700 | 4-stroke 중형 | 213 | 490 |
| 2,500 | 1,700 | 2,125 | 4-stroke 중형 | 210 | 480 |
| 3,000 | 2,040 | 2,550 | 4-stroke 중형 | 205 | 470 |
| 3,500 | 2,380 | 2,975 | 4-stroke 중형 | 201 | 462 |
| 4,000 | 2,720 | 3,400 | 4-stroke 중형 | 198 | 456 |
| 4,500 | 3,060 | 3,825 | 4-stroke 중형 | 196 | 453 |
| 5,000 | 3,400 | 4,250 | 4-stroke 중형 | 195 | 450 |
| 7,500 | 5,100 | 6,375 | 4-stroke 중형 | 190 | 435 |
| 10,000 | 6,800 | 8,500 | 4-stroke/2-stroke | 185 | 420 |
| 15,000 | 10,200 | 12,750 | 2-stroke | 178 | 408 |
| 20,000 | 13,600 | 17,000 | 2-stroke | 174 | 399 |
| 25,000 | 17,000 | 21,250 | 2-stroke | 170 | 390 |
| 30,000 | 20,400 | 25,500 | 2-stroke | 167 | 384 |
| 35,000 | 23,800 | 29,750 | 2-stroke | 165 | 378 |
| 40,000 | 27,200 | 34,000 | 2-stroke 대형 | 163 | 372 |
| 45,000 | 30,600 | 38,250 | 2-stroke 대형 | 161 | 366 |
| 50,000 | 34,000 | 42,500 | 2-stroke 대형 | 160 | 360 |

*Cargo (ton) = Cargo (m³) × 0.680 ton/m³ (암모니아 밀도)
**암모니아 SFOC = 디젤 SFOC × 2.295 (발열량 비율: 42.7/18.6)
***중간값은 선형 보간 적용

### 4.6 SFOC의 부하 의존성

SFOC는 엔진 부하에 따라 비선형적으로 변화합니다:

| 상대 부하 | 상대 SFOC | 비고 | 출처 |
|----------|----------|------|------|
| 70-80% | 100% (최소) | 최적 운전점 | [Sustainable Ships](https://www.sustainable-ships.org/stories/2022/sfc) |
| 50% | ~105-110% | 부분 부하 | [MIC Journal - SFOC Models](https://www.mic-journal.no/PDF/2024/MIC-2024-1-1.pdf) |
| 30% | ~115-125% | 저부하 | [MIC Journal](https://www.mic-journal.no/PDF/2024/MIC-2024-1-1.pdf) |
| Idle (~7%) | ~200% | 공회전 | [Sustainable Ships](https://www.sustainable-ships.org/stories/2022/sfc) |

본 프로젝트에서는 최적 운전점(75% MCR)에서의 SFOC를 기준으로 합니다.

---

## 5. 기존값 대비 새 값 비교

### 5.1 MCR 비교

| Cargo (m³) | 기존 MCR (kW) | 새 MCR (kW) | 변화율 | 비고 |
|------------|--------------|-------------|--------|------|
| 500 | 1,296 | 522 | -60% | 소형 셔틀 |
| 1,000 | 1,341 | 772 | -42% | 소형 셔틀 |
| 2,500 | 1,473 | 1,296 | -12% | 전환점 |
| 5,000 | 1,694 | 1,916 | +13% | 중형 셔틀 |
| 10,000 | 2,159 | 2,833 | +31% | 대형 셔틀 |
| 25,000 | 2,981 | 4,750 | +59% | 대형 셔틀 |
| 50,000 | 3,867 | 7,024 | +82% | 초대형 셔틀 |

### 5.2 SFOC 비교

| Cargo (m³) | 기존 SFOC (g/kWh) | 새 SFOC (g/kWh) | 변화율 |
|------------|------------------|-----------------|--------|
| 모든 크기 | 379 (고정) | 360-550 (가변) | 가변 |

### 5.3 연료비 영향 (MCR × SFOC)

| Cargo (m³) | 기존 MCR×SFOC | 새 MCR×SFOC | 변화율 |
|------------|--------------|-------------|--------|
| 500 | 491,184 | 287,100 | -42% |
| 1,000 | 508,239 | 401,440 | -21% |
| 5,000 | 642,026 | 862,200 | +34% |
| 10,000 | 818,261 | 1,189,860 | +45% |
| 50,000 | 1,465,593 | 2,528,640 | +73% |

### 5.4 단위 화물당 연료비 (규모의 경제 분석)

**핵심**: 총 연료비는 증가하지만, **단위 화물당(m³당) 연료비**는 감소합니다.

| Cargo (m³) | MCR×SFOC | 화물당 연료비 (MCR×SFOC / Cargo) | 규모의 경제 |
|------------|----------|--------------------------------|------------|
| 500 | 287,100 | **574** | 기준 |
| 1,000 | 401,440 | **401** | 1.4배 효율 |
| 5,000 | 862,200 | **172** | 3.3배 효율 |
| 10,000 | 1,189,860 | **119** | 4.8배 효율 |
| 50,000 | 2,528,640 | **51** | **11배 효율** |

**결론**:
- 대형 셔틀(50,000m³)은 소형(500m³) 대비 **11배 효율적**
- 이는 규모의 경제 효과를 정확히 반영
- 총 연료비 증가는 더 많은 화물 운반량을 반영

**기존 모델의 문제점**:
- 기존 MCR 값이 대형 셔틀에 과소 평가됨 (50,000m³: 3,867kW vs 그래프 기준 ~7,000kW)
- 새 값이 실제 선박 설계 관계를 더 정확히 반영

---

## 6. 참고문헌

### 6.1 DWT 및 가스 캐리어 관련

1. Wikipedia. "LNG carrier." https://en.wikipedia.org/wiki/LNG_carrier
2. Marine Insight. "Top 16 Biggest LNG Ships." https://www.marineinsight.com/types-of-ships/biggest-lng-ships/
3. Maritime Optima. "Different type and sizes of Liquefied natural gas (LNG) carriers." https://maritimeoptima.com/insights/different-type-and-sizes-of-liquefied-natural-gas-lng-carriers
4. Wikipedia. "Gas carrier." https://en.wikipedia.org/wiki/Gas_carrier
5. ScienceDirect. "Cargo Deadweight." https://www.sciencedirect.com/topics/engineering/cargo-deadweight
6. Holistic Training. "A Complete Guide to Deadweight Tonnage (DWT)." https://holistiquetraining.com/en/news/a-complete-guide-to-deadweight-tonnage-dwt
7. Cult of Sea. "Gas Tankers - Basic definitions and Hazards." https://www.cultofsea.com/cargo-work/gas-tankers-basic-definitions-hazards/
8. Ammonia Energy. "Mitsui O.S.K. Lines: ammonia-fueled Capesize bulkers & chemical tankers." https://ammoniaenergy.org/articles/mitsui-o-s-k-lines-ammonia-fueled-capesize-bulkers-chemical-tankers-to-hit-the-water-from-next-year/

### 6.2 MCR 및 엔진 출력 관련

9. MAN Energy Solutions. "Engine power range and fuel oil consumption." https://man-es.com/applications/projectguides/2stroke/content/198491724.pdf
10. STG Online. "Marine Diesel Engines - How Efficient can a Two-Stroke Engine be?" https://www.stg-online.org/onTEAM/shipefficiency/programm/Clausen.pdf
11. ResearchGate. "The relative specific fuel-oil consumption (SFOC) as a function of the relative engine load." https://www.researchgate.net/figure/The-relative-specific-fuel-oil-consumption-SFOC-as-a-function-of-the-relative-engine_fig2_252392578

### 6.3 SFOC 관련

12. Sustainable Ships. "Specific Fuel Consumption [g/kWh] for Marine Engines." https://www.sustainable-ships.org/stories/2022/sfc
13. MDPI. "An Approach for Predicting the Specific Fuel Consumption of Dual-Fuel Two-Stroke Marine Engines." https://www.mdpi.com/2077-1312/7/2/20
14. DG Marine. "Improving Fuel Efficiency in Marine Engines | Formula and Calculation of SFOC." https://www.dgmarine.in/2023/04/improving-fuel-efficiency-in-marine-Engines.html
15. Marine Site. "Specific Fuel Oil Consumption (SFOC) Definition, Formula And Calculation." https://www.marinesite.info/2014/03/specific-fuel-oil-consumption.html
16. Marine Gyaan. "What is SFOC? How to calculate SFOC?" https://marinegyaan.com/what-is-sfoc-how-to-calculate-sfoc/
17. MIC Journal. "Specific Fuel Oil Consumption Models for Simulating." https://www.mic-journal.no/PDF/2024/MIC-2024-1-1.pdf

### 6.4 암모니아 연료 관련

18. Nature Scientific Reports. "Combustion and emission characteristics of ammonia-diesel marine high pressure direct injection low-speed dual-fuel engine." https://www.nature.com/articles/s41598-025-04997-z
19. ScienceDirect. "Ammonia as fuel for marine dual-fuel technology: A comprehensive review." https://www.sciencedirect.com/science/article/pii/S0378382025000293
20. ScienceDirect. "Pilot diesel-ignited ammonia dual fuel low-speed marine engines." https://www.sciencedirect.com/science/article/abs/pii/S1364032122009893
21. WinGD. "Ammonia Dual-Fuel Engines FAQs." https://wingd.com/media/2gyl3j0v/wingd-ammonia-faq-booklet.pdf

---

## 7. 부록: 변환 공식 요약

### A. Cargo Volume → DWT
```python
def cargo_to_dwt(cargo_m3, density=0.680, cargo_fraction=0.80):
    cargo_ton = cargo_m3 * density
    dwt = cargo_ton / cargo_fraction
    return dwt
```

### B. DWT → MCR
```python
def dwt_to_mcr(dwt, coefficient=17.17, exponent=0.564):
    mcr = coefficient * (dwt ** exponent)
    return mcr
```

### C. SFOC 보간
```python
def interpolate_sfoc(cargo_m3, sfoc_map):
    # sfoc_map = {500: 550, 1000: 520, 2500: 480, 5000: 450,
    #             10000: 420, 25000: 390, 50000: 360}
    # 선형 보간 적용
    ...
```

---

*본 보고서는 Green Corridor 암모니아 벙커링 최적화 프로젝트의 기술 문서입니다.*
