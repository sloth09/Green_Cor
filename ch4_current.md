3장. MILP 최적화 모델

부산항 암모니아 벙커링 인프라의 최적화 문제는 혼합정수선형계획(Mixed
Integer Linear Programming, MILP) 모델로 수립된다. 본 장에서는 모델의
개요, 결정변수, 목적함수, 제약식, 그리고 경제적 파라미터를 상세히
설명한다.

3.1 모델 개요 및 가정

**모델 목표**

본 모델의 목표는 2030년부터 2050년까지 20년 계획 기간 동안 부산항에서의
암모니아 벙커링 인프라 구축 및 운영에 소요되는 순현재가(Net Present
Cost, NPC)를 최소화하는 것이다. 의사결정 변수는 다음 세 가지이다: 1)
셔틀 선박의 최적 크기 및 필요 개수 2) 벙커링 펌프의 최적 용량 3)
저장탱크의 필요 크기 (Case 1만 해당) 이를 통해 수요 증가에 따른 확장
가능하고 경제적인 인프라를 설계할 수 있다.

**주요 가정사항**

다음의 주요 가정사항이 모델에 적용된다: • 시간 계획 기간: 2030-2050년
(21년, 매년 단위) • 선박 수요: 선형 성장 (2030년 50척 → 2050년 500척) •
선박당 연간 항차: 12회 (고정) • 항차당 급유량: 5,000 m³ (고정) • 할인율:
7% (경제적 평가) • 셔틀과 탱크는 내구 연한 동안 운영 가능 • 육상 연료
공급 펌프 유량: 1,500 m³/h (고정, 모든 Case 동일) • 최대 연간 운영시간:
8,000시간/년/셔틀

3.2 결정변수 정의

MILP 모델의 결정변수는 다음과 같이 정의된다:

*h ∈ H: 셔틀 크기 (m³)*

Case 1: 500, 1,000, 1,500, 2,000, 2,500, 3,000, 3,500, 4,000, 4,500,
5,000 m³ Case 2: 5,000, 10,000, 15,000, 20,000, 25,000, 30,000, 35,000,
40,000, 45,000, 50,000 m³

*p ∈ P: 펌프 용량 (m³/h)*

400, 600, 800, 1,000, 1,200, 1,400, 1,600, 1,800, 2,000 m³/h

*x\[t, h, p\]: t년도에 구입하는 크기 h, 펌프 p의 셔틀 수 (개, 정수변수)*

연도 t = 2030, 2031, \..., 2050

*N\[t, h, p\]: t년도 누적 셔틀 수 (개, 정수변수)*

N\[t, h, p\] = Σ\_{τ=2030}\^{t} x\[τ, h, p\]

*y\[t, h, p\]: t년도 연간 벙커링 횟수 (회, 연속변수)*

각 h, p 조합에 대해 연간 벙커링 작업 횟수

*z\[t\]: t년도 신규 추가 저장탱크 수 (개, 정수변수, Case 1만)*

Z\[t\]: t년도 누적 탱크 수 (개, 정수변수, Case 1만)

3.3 목적함수 (NPC 최소화)

목적함수는 20년 계획 기간의 순현재가를 최소화하는 것이다:

***Minimize: NPC = Σ\_{t=2030}\^{2050} \[DF(t) × (CAPEX(t) +
FIXED_OPEX(t) + VARIABLE_OPEX(t))\]***

여기서:

DF(t) = 할인인자 = 1 / (1 + r)\^(t - 2030), r = 0.07 CAPEX(t) = t년도
자본지출 (자본비) FIXED_OPEX(t) = t년도 고정 운영비 VARIABLE_OPEX(t) =
t년도 변동 운영비

**자본지출 (CAPEX)**

CAPEX(t) = Σ\_{h,p} \[x\[t,h,p\] × (CAPEX_shuttle(h) +
CAPEX_pump(p))\] + z\[t\] × CAPEX_tank CAPEX_shuttle(h)는 스케일링
공식으로 계산: CAPEX_shuttle(h) = 61,500,000 × (h / 40,000)\^0.75 (USD)
CAPEX_pump(p)는 펌프 파워 기반 계산: Pump_Power(p) = (4 × 10\^5 Pa ×
p/3600) / 0.7 (kW) CAPEX_pump(p) = Pump_Power(p) × 2,000 (USD/kW)
CAPEX_tank = 42,525,000 USD (35,000톤 저장탱크, Case 1만)

**고정 운영비 (FIXED_OPEX)**

FIXED_OPEX(t) = Σ\_{h,p} \[N\[t,h,p\] × (OPEX_shuttle(h) +
OPEX_pump(p))\] + Z\[t\] × OPEX_tank 여기서 고정 운영비는 CAPEX의 연간
백분율: OPEX_shuttle(h) = CAPEX_shuttle(h) × 0.05 (5% 유지보수)
OPEX_pump(p) = CAPEX_pump(p) × 0.05 (5% 유지보수) OPEX_tank = CAPEX_tank
× 0.03 (3% 유지보수)

**변동 운영비 (VARIABLE_OPEX)**

VARIABLE_OPEX(t) = Σ\_{h,p} \[y\[t,h,p\] × (OPEX_shuttle_fuel +
OPEX_pump_power)\] + Z\[t\] × OPEX_tank_cooling 셔틀 연료비:
OPEX_shuttle_fuel = MCR(h) × SFOC × Travel_time × SFOC_weight ×
Fuel_price MCR(h): 셔틀 최대 연속 정격 (kW) SFOC: 비연료소비율 = 379
g/kWh Travel_time: 왕복 항해 시간 (h) Fuel_price: 600 USD/ton 펌프 전력
비용: OPEX_pump_power = Pump_Power(p) × Pumping_time × Electricity_price
Pumping_time: 해당 조합의 벙커링 시간 (h/회) Electricity_price: 0.0769
USD/kWh 탱크 냉각비 (Case 1만): OPEX_tank_cooling = Tank_Volume ×
Cooling_Energy × Electricity_price Cooling_Energy: 0.0378 kWh/kg

3.4 제약식

**3.4.1 누적 제약 (Accumulation Constraint)**

N\[t, h, p\] = N\[t-1, h, p\] + x\[t, h, p\] 셔틀은 한번 구입하면 내구
연한 동안 운영되며, 매년 신규 구입분이 누적된다.

**3.4.2 수요 충족 제약 (Demand Satisfaction)**

Σ\_{h,p} \[y\[t,h,p\] × Bunker_Volume\] ≥ Demand\[t\] 여기서:
Bunker_Volume = 5,000 m³ (항차당 급유량) Demand\[t\] = Vessels\[t\] ×
Voyages_per_year × Bunker_Volume Vessels\[t\]: t년도 암모니아 선박 수
Voyages_per_year: 12회/년

**3.4.3 운영시간 제약 (Operating Hour Constraint)**

Σ\_{h,p} \[y\[t,h,p\] × trips_per_call(h) × Cycle_Time(h,p)\] ≤
N\[t,h,p\] × H_max 여기서: trips_per_call(h): h 크기 셔틀이 5,000 m³를
전달하는데 필요한 트립 수 Case 1: ceil(5,000 / h) Case 2: 1 (한 번의
항해에 여러 척 서빙) Cycle_Time(h,p): h 크기 셔틀과 p 용량 펌프의 왕복
사이클 시간 Case 1: 육상적재 + 편도이동 + 호스작업 + 벙커링 + 복귀 Case
2: 육상적재 + 항해 + 부산진입 + 각선박서빙 + 복귀 H_max =
8,000시간/년/셔틀 (최대 연간 운영시간)

**3.4.4 저장탱크 용량 제약 (Tank Capacity Constraint, Case 1만)**

N\[t,h,p\] × h × β ≤ Z\[t\] × Tank_Volume 여기서: β = 안전계수 = 2.0
(재고 운영의 여유) Tank_Volume = 35,000톤 (2.857 × 10\^4 m³ at 1.225
kg/m³ 밀도) 탱크 용량이 셔틀 적재량의 여러 배가 되어야 안정적 운영이
가능하다.

**3.4.5 비음수 제약 (Non-negativity Constraints)**

x\[t,h,p\] ≥ 0 (정수) N\[t,h,p\] ≥ 0 (정수) y\[t,h,p\] ≥ 0 (연속) z\[t\]
≥ 0 (정수, Case 1만) Z\[t\] ≥ 0 (정수, Case 1만)

3.5 할인율 및 시간가치

경제 평가에 사용되는 할인율은 7%이다. 이는 해운 산업의 자본 비용과 투자
수익률을 반영한 표준 할인율이다. 할인인자 DF(t) = 1 / (1.07)\^(t - 2030)
예시: - 2030년: DF(2030) = 1.00 - 2035년: DF(2035) = 1 / 1.07\^5 =
0.713 - 2050년: DF(2050) = 1 / 1.07\^20 = 0.258 이를 통해 초기 투자의
가중치가 높고, 이후 연도의 비용은 더 낮은 가중치를 받는다. 따라서 초기에
적절한 규모의 인프라를 구축하는 것이 경제적으로 유리하다.

3.6 주요 모델 파라미터 요약

아래 표는 모델에 사용되는 주요 파라미터를 요약한다:

  ---------------------------------------------------
  **파라미터**        **값**          **단위**
  ------------------- --------------- ---------------
                                      

                                      

                                      

                                      

                                      

                                      

                                      

                                      
  ---------------------------------------------------

본 장에서 설명한 MILP 모델은 Case별로 약간의 변형이 있으며, 다음
장에서는 3가지 Case 시나리오의 구체적인 구현을 상세히 다룬다. 특히 Case
1과 Case 2의 기본적인 운영 개념의 차이(다중 왕복 vs 단일 항해)가 모델의
제약식과 경제성 분석에 어떤 영향을 미치는지 살펴볼 것이다.
