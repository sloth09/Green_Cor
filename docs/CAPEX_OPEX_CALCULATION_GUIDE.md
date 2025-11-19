# CAPEX/OPEX 계산 가이드

## 개요

이 문서는 암모니아 벙커링 인프라의 **연단위 비용 계산 방법**을 명확하게 설명합니다.

20년 프로젝트(2030-2050)에서 각 연도별로:
- **신규 자산 구매** → CAPEX (자본비)
- **기존 자산 유지** → Fixed OPEX (고정 운영비)
- **실제 운영** → Variable OPEX (변동 운영비)

최종적으로 **순현재가(NPC: Net Present Cost)**를 계산하여 경제성을 평가합니다.

---

## 1. 비용 구조 정의

### 1.1 자본비 (CAPEX: Capital Expenditure)

**정의**: 자산 구매시 일회성으로 발생하는 비용

**항목**:
```
Total CAPEX = Shuttle CAPEX + Pump CAPEX + Tank CAPEX
```

| 항목 | 설명 | 시점 |
|------|------|------|
| **Shuttle CAPEX** | 셔틀 선박 구매비 | 연도별 신규 구매시 |
| **Pump CAPEX** | 벙커링 펌프 시스템 | 연도별 신규 구매시 |
| **Tank CAPEX** | 저장 탱크 (Case 1만) | 연도별 신규 구매시 |

### 1.2 고정 운영비 (Fixed OPEX)

**정의**: 자산을 보유하는 것만으로 발생하는 연간 고정 비용 (운영량과 무관)

**항목**:
```
Fixed OPEX = Shuttle Fixed OPEX + Pump Fixed OPEX + Tank Fixed OPEX
```

**계산 원칙**:
```
Fixed OPEX = CAPEX × Fixed OPEX Ratio (%)
```

| 항목 | CAPEX 대비 비율 | 적용 대상 |
|------|----------------|---------|
| Shuttle Fixed OPEX | 5% | 누적 셔틀 수 × 개별 셔틀 CAPEX |
| Pump Fixed OPEX | 5% | 누적 펌프 수 × 개별 펌프 CAPEX |
| Tank Fixed OPEX | 3% | 누적 탱크 수 × 탱크 CAPEX |

### 1.3 변동 운영비 (Variable OPEX)

**정의**: 실제 운영량(사이클 수, 벙커링 횟수)에 따라 발생하는 비용

**항목**:
```
Variable OPEX = Shuttle Fuel Cost + Pump Fuel Cost + Tank Cooling Cost
```

**특징**: 연간 수요에 따라 달라짐

---

## 2. 항목별 상세 계산

### 2.1 셔틀(Shuttle) 비용

#### CAPEX (자본비)

**공식**:
```
Shuttle_CAPEX = Reference_CAPEX × (Size / Reference_Size)^α

예시:
  Reference_CAPEX = $61,500,000 (40,000 m³ 기준)
  α = 0.75 (규모의 경제 스케일 팩터)

계산 예:
  5,000 m³ 셔틀 CAPEX = 61,500,000 × (5,000 / 40,000)^0.75
                       = 61,500,000 × 0.1563
                       ≈ $9,612,150
```

**config 파일 참조**:
```yaml
shuttle:
  ref_capex_usd: 61500000
  ref_size_cbm: 40000
  capex_scaling_exponent: 0.75
```

#### Fixed OPEX (고정 운영비)

**공식**:
```
Shuttle_Fixed_OPEX_Annual = CAPEX × 5%

예시:
  5,000 m³ 셔틀 Annual Fixed OPEX = $9,612,150 × 5%
                                   ≈ $480,608 per year
```

**적용 방식** (연도 t에서):
```
Total Shuttle Fixed OPEX(t) = N(t) × Shuttle_Fixed_OPEX_Annual

N(t) = 연도 t의 누적 셔틀 수

예: 2030년에 셔틀 1대 구매, 2031년에 1대 추가 구매
    2031년 Fixed OPEX = (1 + 1) × $480,608 = $961,216
```

#### Variable OPEX (연료비)

**공식**:
```
Shuttle_Fuel_Per_Cycle = MCR × SFOC × Travel_Time / 1,000,000  [ton]

Cost_Per_Cycle = Fuel_Per_Cycle × Fuel_Price

연간 총 연료비 = Cost_Per_Cycle × Annual_Cycles
```

**상세 계산**:

| 파라미터 | 5,000m³ 셔틀 | 설명 |
|---------|-----------|------|
| MCR (Max Continuous Rating) | 1,694 kW | 엔진 최대 정격 전력 |
| SFOC (Specific Fuel Oil Consumption) | 379 g/kWh | 연료 소비율 |
| Travel Time | 2.0시간 (Case 1) | 편도 항해 시간 |
| Fuel Per Cycle | 1,694 × 379 × 2 / 1,000,000 = 1.285 ton | 왕복 연료 |
| Fuel Price | $600/ton | 암모니아 가격 |
| Cost Per Cycle | 1.285 × $600 = $771 | |
| Cycles/Year | ~522 (8,000h ÷ 15.33h) | 연간 가능 사이클 |
| **Annual Fuel Cost** | **~$402,600** | |

**연도 t 적용**:
```
Annual Shuttle Fuel Cost(t) = y(t) × Trips_per_Call × Cost_per_Cycle

y(t) = 연도 t의 벙커링 콜(demand call) 수
```

### 2.2 펌프(Pump) 비용

#### CAPEX (자본비)

**공식**:
```
Pump_Power = ΔP × Q / (η × 1000)  [kW]

  ΔP = 압력강하 = 4 bar = 400,000 Pa
  Q = 유량 = pump_size [m³/h]
  η = 펌프 효율 = 0.7

예: 1,000 m³/h 펌프
  Power = (4 bar × 100,000 Pa/bar) × (1,000 / 3,600) / (0.7 × 1000)
        = 400 kW × 0.278 / 0.7
        ≈ 159 kW

Pump_CAPEX = Power × Cost_per_kW
           = 159 × $2,000
           ≈ $318,000
```

**config 파일 참조**:
```yaml
propulsion:
  pump_delta_pressure_bar: 4.0
  pump_efficiency: 0.7
  pump_power_cost_usd_per_kw: 2000
```

#### Fixed OPEX (고정 운영비)

**공식**:
```
Pump_Fixed_OPEX_Annual = CAPEX × 5%

예: 1,000 m³/h 펌프
  Annual Fixed OPEX = $318,000 × 5% = $15,900/year
```

#### Variable OPEX (에너지비)

**공식**:
```
Pump_Fuel_Per_Call = Pump_Power × Pumping_Time × SFOC / 1,000,000  [ton]

Pumping_Time = 2 × Volume / Flow_Rate  (적재 + 방출)

예: 1,000 m³/h 펌프, 5,000 m³ 벙커링 콜
  Pumping_Time = 2 × 5,000 / 1,000 = 10 hours
  Fuel = 159 × 10 × 379 / 1,000,000 = 0.603 ton
  Cost = 0.603 × $600 = $362 per call

연간 비용 = $362 × Annual_Calls
```

### 2.3 저장 탱크(Tank) 비용 (Case 1만)

#### CAPEX (자본비)

**공식**:
```
Tank_CAPEX = Tank_Size_tons × 1,000 × Cost_per_kg

예: 35,000톤 탱크
  Tank_CAPEX = 35,000 × 1,000 × $1.215
             = $42,525,000
```

**config 파일 참조**:
```yaml
tank_storage:
  size_tons: 35000
  cost_per_kg_usd: 1.215
```

#### Fixed OPEX (고정 운영비)

**공식**:
```
Tank_Fixed_OPEX_Annual = CAPEX × 3%

예:
  Annual Fixed OPEX = $42,525,000 × 3%
                    = $1,275,750/year
```

#### Variable OPEX (냉각비)

**공식**:
```
Tank_Cooling_Cost = Tank_Size_kg × Energy_per_kg × Electricity_Price

예:
  Tank_Size = 35,000 tons = 35,000,000 kg
  Energy = 0.0378 kWh/kg (암모니아 냉각)
  Electricity = $0.0769/kWh

  Annual Cost = 35,000,000 × 0.0378 × $0.0769
              = $101,925/year
```

**config 파일 참조**:
```yaml
tank_storage:
  cooling_energy_kwh_per_kg: 0.0378
  fixed_opex_ratio: 0.03

economy:
  electricity_price_usd_per_kwh: 0.0769
```

---

## 3. 연단위 비용 계산 (연도 t에서)

### 3.1 해당 연도 비용 (Undiscounted)

```
Year_t_Cost = CAPEX(t) + Fixed_OPEX(t) + Variable_OPEX(t)
```

**상세 분해**:

```
CAPEX(t) = 신규셔틀수(t) × 셔틀CAPEX
         + 신규펌프수(t) × 펌프CAPEX
         + 신규탱크수(t) × 탱크CAPEX

Fixed_OPEX(t) = 누적셔틀수(t) × 셔틀고정운영비/년
              + 누적펌프수(t) × 펌프고정운영비/년
              + 누적탱크수(t) × 탱크고정운영비/년

Variable_OPEX(t) = 셔틀연료비(t) + 펌프연료비(t) + 탱크냉각비(t)
```

### 3.2 누적 변수

```
누적셔틀수(t) = 누적셔틀수(t-1) + 신규셔틀수(t)
             = Σ(신규셔틀수) from 2030 to t

예:
  2030: 신규 1대 → 누적 1대
  2031: 신규 1대 → 누적 2대
  2032: 신규 2대 → 누적 4대
  ...
```

---

## 4. 순현재가(NPC) 계산

### 4.1 할인 인자

**공식**:
```
Discount_Factor(t) = 1 / (1 + r)^(t - start_year)

r = 할인율 (기본값: 7% = 0.07)
start_year = 2030
t = 평가 연도 (2030 ~ 2050)

예:
  2030년 (t=0): 1 / (1.07)^0 = 1.000
  2035년 (t=5): 1 / (1.07)^5 = 0.713
  2040년 (t=10): 1 / (1.07)^10 = 0.508
  2050년 (t=20): 1 / (1.07)^20 = 0.258
```

### 4.2 할인된 비용

**공식**:
```
Discounted_Cost(t) = Year_t_Cost × Discount_Factor(t)
```

### 4.3 총 순현재가

**공식**:
```
NPC_Total = Σ [Discounted_Cost(t)] for t = 2030 to 2050
          = Σ [Year_t_Cost(t) × Discount_Factor(t)]
```

**항목별 분해**:
```
NPC_Total = NPC_Shuttle_CAPEX + NPC_Shuttle_Fixed_OPEX + NPC_Shuttle_Variable_OPEX
          + NPC_Pump_CAPEX + NPC_Pump_Fixed_OPEX + NPC_Pump_Variable_OPEX
          + NPC_Tank_CAPEX + NPC_Tank_Fixed_OPEX + NPC_Tank_Variable_OPEX
```

---

## 5. 구체적 예시

### 5.1 Case 1 (부산, 5,000 m³ 셔틀, 1,000 m³/h 펌프)

#### 2030년 비용

**CAPEX**:
```
신규 셔틀 1대 구매:
  Shuttle CAPEX = $9,612,150

신규 펌프 1대 구매:
  Pump CAPEX = $318,000

신규 탱크 1대 구매 (Case 1):
  Tank CAPEX = $42,525,000

해당 연도 CAPEX = $9,612,150 + $318,000 + $42,525,000
                = $52,455,150
```

**Fixed OPEX**:
```
누적 자산 = 셔틀 1대, 펌프 1대, 탱크 1대

Shuttle Fixed OPEX = 1 × ($9,612,150 × 5%) = $480,608
Pump Fixed OPEX = 1 × ($318,000 × 5%) = $15,900
Tank Fixed OPEX = 1 × ($42,525,000 × 3%) = $1,275,750

해당 연도 Fixed OPEX = $480,608 + $15,900 + $1,275,750
                    = $1,772,258
```

**Variable OPEX**:
```
2030년 수요 (선박 50척, 12회/년):
  Annual_Demand = 50 × 12 × 5,000 m³ = 3,000,000 m³

필요 사이클 수 (5,000 m³/셔틀):
  y(2030) = 3,000,000 / 5,000 = 600 콜

필요 작동 시간:
  Required_Hours = 600 × 15.33 hours = 9,198 hours
  Available_Hours = 1 셔틀 × 8,000 = 8,000 hours
  → 부족! 추가 셔틀 필요

실제 가능 공급량:
  Max_Supply = 8,000 / 15.33 × 5,000 = 2,609,500 m³
  (수요를 충족하려면 셔틀 추가 필요)

셔틀 연료비:
  Cycles = 600 (충족 가정)
  Cost = 600 × $771 = $462,600

펌프 에너지비:
  Calls = 600
  Cost = 600 × $362 = $217,200

탱크 냉각비:
  Cost = $101,925

해당 연도 Variable OPEX = $462,600 + $217,200 + $101,925
                       = $781,725
```

**2030년 총 비용**:
```
Total_Cost(2030) = $52,455,150 + $1,772,258 + $781,725
                 = $55,009,133

Discount_Factor(2030) = 1.0
Discounted_Cost(2030) = $55,009,133 × 1.0 = $55,009,133
```

#### 2035년 비용 (예시)

```
누적 자산: 셔틀 3대, 펌프 3대, 탱크 1대
수요 증가: 선박 100척, 12회/년 → 6,000,000 m³

CAPEX(2035) = 신규자산CAPEX (최적화에서 결정)
Fixed OPEX(2035) = 3 × $480,608 + 3 × $15,900 + 1 × $1,275,750
                 = $2,572,474
Variable OPEX(2035) = 계산된 사이클수 × 비용

Discount_Factor(2035) = 1 / (1.07)^5 = 0.713
```

### 5.2 Case 2-2 (울산, 25,000 m³ 셔틀, 1,000 m³/h 펌프)

#### 비용 특징

```
Case 1 vs Case 2-2 비교 (동일 5,000 m³ 콜, 1,000 m³/h 펌프):

Case 1:
  - 셔틀 CAPEX: $9.6M (5,000 m³)
  - 탱크 CAPEX: $42.5M (필수)
  - 사이클당 운영시간: 15.33시간

Case 2-2:
  - 셔틀 CAPEX: $35.0M (25,000 m³)
  - 탱크 CAPEX: $0 (출발지에만 있음)
  - 사이클당 운영시간: 60.0시간 (하지만 5척 동시 서빙)
  - 실제 초소비: 60 / 5 = 12시간/척
```

---

## 6. 코드 구현 참조

### 6.1 CostCalculator 클래스

**위치**: `src/cost_calculator.py`

```python
# 셔틀 CAPEX
def calculate_shuttle_capex(self, shuttle_size_cbm: float) -> float:
    ref_capex = self.config["shuttle"]["ref_capex_usd"]
    ref_size = self.config["shuttle"]["ref_size_cbm"]
    alpha = self.config["shuttle"]["capex_scaling_exponent"]
    return ref_capex * (shuttle_size_cbm / ref_size) ** alpha

# 셔틀 고정 OPEX
def calculate_shuttle_fixed_opex(self, shuttle_size_cbm: float) -> float:
    capex = self.calculate_shuttle_capex(shuttle_size_cbm)
    opex_ratio = self.config["shuttle"]["fixed_opex_ratio"]
    return capex * opex_ratio

# 펌프 파워 계산
def calculate_pump_power(self, pump_flow_m3ph: float) -> float:
    delta_pressure = self.config["propulsion"]["pump_delta_pressure_bar"]
    efficiency = self.config["propulsion"]["pump_efficiency"]
    power_kw = (delta_pressure * 100000) * (pump_flow_m3ph / 3600) / (efficiency * 1000)
    return power_kw

# 펌프 CAPEX
def calculate_pump_capex(self, pump_flow_m3ph: float) -> float:
    power_kw = self.calculate_pump_power(pump_flow_m3ph)
    cost_per_kw = self.config["propulsion"]["pump_power_cost_usd_per_kw"]
    return power_kw * cost_per_kw
```

### 6.2 Optimizer 클래스

**위치**: `src/optimizer.py`

```python
# 연도 t의 목적함수 항 계산
for t in self.years:
    disc_factor = 1.0 / ((1.0 + self.discount_rate) ** (t - self.start_year))

    # CAPEX: 신규 자산
    capex = (shuttle_capex + bunk_capex) * x[t]
    if self.tank_enabled:
        capex += tank_capex * x_tank[t]

    # Fixed OPEX: 누적 자산
    fixed_opex = (shuttle_fixed_opex + bunk_fixed_opex) * N[t]
    if self.tank_enabled:
        fixed_opex += tank_fixed_opex * N_tank[t]

    # Variable OPEX: 운영량
    variable_opex = shuttle_fuel_cost_per_cycle * cycles + pump_fuel_cost_per_call * y[t]
    if self.tank_enabled:
        variable_opex += tank_variable_opex * N_tank[t]

    # 할인된 연간 비용
    obj_terms.append(disc_factor * (capex + fixed_opex + variable_opex))

# NPC 계산
prob += pulp.lpSum(obj_terms)
```

---

## 7. 결과 해석

### 7.1 NPC 분해 (결과 파일)

결과 CSV 파일에서 확인 가능:

```
Shuttle_Size_cbm, Pump_Size_m3ph, NPC_Total_USDm,
NPC_Shuttle_CAPEX_USDm, NPC_Shuttle_fOPEX_USDm, NPC_Shuttle_vOPEX_USDm,
NPC_Bunkering_CAPEX_USDm, NPC_Bunkering_fOPEX_USDm, NPC_Bunkering_vOPEX_USDm,
NPC_Terminal_CAPEX_USDm, NPC_Terminal_fOPEX_USDm, NPC_Terminal_vOPEX_USDm
```

### 7.2 Annualized Cost

20년 NPC를 연단위로 환산:

```
Annualized_Cost = NPC / Annuity_Factor

Annuity_Factor = [1 - (1+r)^(-n)] / r
               = [1 - (1.07)^(-20)] / 0.07
               ≈ 10.594

Annualized = NPC / 10.594  [USD/year]
```

### 7.3 LCOAmmonia (암모니아 한 톤당 원가)

```
LCOAmmonia = NPC / Total_Supply_20years  [USD/ton]

총 공급량 = Σ(연간공급량) for 2030 to 2050
```

---

## 8. 설정 파일 (config/base.yaml)

```yaml
shuttle:
  ref_capex_usd: 61500000
  ref_size_cbm: 40000
  capex_scaling_exponent: 0.75
  fixed_opex_ratio: 0.05

propulsion:
  pump_delta_pressure_bar: 4.0
  pump_efficiency: 0.7
  sfoc_g_per_kwh: 379
  pump_power_cost_usd_per_kw: 2000

bunkering:
  fixed_opex_ratio: 0.05

tank_storage:
  size_tons: 35000
  cost_per_kg_usd: 1.215
  cooling_energy_kwh_per_kg: 0.0378
  fixed_opex_ratio: 0.03

economy:
  discount_rate: 0.07
  fuel_price_usd_per_ton: 600
  electricity_price_usd_per_kwh: 0.0769
```

---

## 9. 요약

### 비용 계산 체계

```
연도 t의 총 비용 = CAPEX(t) + Fixed OPEX(t) + Variable OPEX(t)

CAPEX(t): 신규 자산 구매 (일회성)
          ├─ 신규셔틀 × 셔틀CAPEX
          ├─ 신규펌프 × 펌프CAPEX
          └─ 신규탱크 × 탱크CAPEX

Fixed OPEX(t): 자산 보유 비용 (연간 누적)
               ├─ 누적셔틀 × 셔틀CAPEX × 5%
               ├─ 누적펌프 × 펌프CAPEX × 5%
               └─ 누적탱크 × 탱크CAPEX × 3%

Variable OPEX(t): 운영 비용 (사이클 수에 따라)
                 ├─ 셔틀 연료비 = 사이클 수 × MCR × SFOC × 항해시간 × 유가
                 ├─ 펌프 에너지비 = 콜 수 × 펌프파워 × 펌핑시간 × 전기료
                 └─ 탱크 냉각비 = 탱크용량 × 냉각에너지 × 전기료

NPC = Σ [Year_t_Cost × Discount_Factor(t)]  for t=2030~2050
```

### 할인 적용

```
모든 비용은 2030년 기준 현가로 변환:
  할인인자 = 1 / (1 + 7%)^(년도-2030)

2030년: 1.0배
2035년: 0.713배 (~30% 감소)
2040년: 0.508배 (~50% 감소)
2050년: 0.258배 (~75% 감소)
```

---

## 참고 자료

- **Config 파일**: `config/base.yaml`, `config/case_*.yaml`
- **구현 코드**:
  - `src/cost_calculator.py` - 모든 CAPEX/OPEX 계산
  - `src/optimizer.py` (lines 240-275) - NPC 목적함수
  - `src/optimizer.py` (lines 323-391) - 결과 추출
