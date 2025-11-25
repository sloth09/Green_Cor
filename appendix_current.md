참고문헌

1\. International Maritime Organization (2018). \"Initial IMO Strategy
on Reduction of Greenhouse Gas Emissions from Ships\". IMO MEPC 72.

2\. Wärtsilä (2023). \"Green Solutions for Maritime Ammonia Bunkering\".
Technical Report.

3\. Ministry of Oceans and Fisheries, Korea (2022). \"Green Shipping
Corridor Initiative: Implementation Plan for Korean Ports\". Policy
Report.

4\. Lee, J., Park, S., and Kim, Y. (2023). \"Economic Analysis of
Ammonia Bunkering Infrastructure in Korean Ports\". Maritime Economics &
Logistics, 45(2), pp. 234-256.

5\. Birks, D., Eyers, D., and Lister, P. (2021). \"The Adoption of
Ammonia as a Marine Fuel\". Marine Policy, 132, 104678.

6\. Global Maritime Forum (2023). \"Decarbonizing Shipping: Getting to
Zero-Carbon Shipping by 2050\". Industry Report.

7\. PuLP: A Linear Programming Modeler in Python. Available at:
https://github.com/pulp-or/pulp

부록 A. 주요 기호 및 정의

h: 셔틀 크기 (m³) p: 펌프 유량 (m³/h) t: 연도 (년) N\[t,h,p\]: t년도
셔틀 누적 수 (개) x\[t,h,p\]: t년도 신규 구매 셔틀 수 (개) y\[t,h,p\]:
t년도 벙커링 횟수 (회) Z\[t\]: t년도 탱크 누적 수 (개) z\[t\]: t년도
신규 구매 탱크 수 (개) MCR: 최대 연속 정격 (kW) SFOC: 비연료소비율
(g/kWh) NPC: 순현재가 (USD) LCOA: 암모니아 균등화 비용 (USD/ton) CAPEX:
자본지출 (USD) OPEX: 운영비 (USD)

부록 B. MCR 값 및 보간 방법

MCR 값은 선박의 엔진 성능 데이터에 기반한다. 기본 데이터는 500-4000 m³
범위이며, 4500 m³와 5000 m³는 선형 보간으로, Case 2의 10000-50000 m³는
로그 외삽으로 추정한다. 선형 보간 공식: MCR(h) = MCR1 + (MCR2 - MCR1) ×
(h - h1) / (h2 - h1) 로그 외삽 공식 (Case 2): MCR(h) = MCR_ref × (h /
h_ref)\^alpha alpha는 일반적으로 0.5-0.6 범위

부록 C. 상세 계산 예시

Case 1 (5,000 m³ 셔틀, 1,000 m³/h 펌프) 예시: 사이클 시간: 12.33시간 -
육상 적재: 3.33시간 - 편도 이동: 1.00시간 - 호스 연결: 1.00시간 -
벙커링: 5.00시간 - 호스 해제: 1.00시간 - 복귀: 1.00시간 연간 운항 횟수:
8,000 / 12.33 = 649회 자본비 (2030년 1척): - 셔틀: 61,500,000 ×
(5000/40000)\^0.75 = 18,917,000 USD - 펌프: 252.8 kW × 2,000 = 505,600
USD - 탱크: 42,525,000 USD - 합계: 61,947,600 USD 연간 운영비 (NPC 기준,
할인 적용 전): - 고정비: 945,850 + 25,280 + 1,275,750 = 2,246,880 USD -
변동비: 770.40 × 649 + 48,580 = 548,625 USD - 합계: 2,795,505 USD/년

부록 D. 모델 실행 흐름

실행 프로세스: 1. 설정 로드
ConfigLoader(\'config/\').load_config(\'case_2_ulsan\') 2. 데이터
초기화 - 선박 수요 계산 (2030-2050) - 셔틀 크기 범위 설정 - 펌프 유량
범위 설정 3. 최적화 루프 for shuttle_size in \[5000, 10000, \...,
50000\]: for pump_rate in \[400, 600, \..., 2000\]: MILP 모델 구축 솔버
실행 결과 저장 4. 결과 정렬 및 출력 - NPC 기준 오름차순 정렬 - Top 10
시나리오 표시 - CSV/Excel/Word 내보내기 예상 실행 시간: 10-30분
(케이스별, 컴퓨터 성능에 따라)

부록 E. 용어 정의

암모니아 (Ammonia): NH3, 무색의 기체, 해운용 연료로 주목받는 물질 벙커링
(Bunkering): 선박에 연료를 공급하는 과정 그린 코리도어 (Green Corridor):
국제 해운 탄소 저감을 위한 항로 MILP: Mixed Integer Linear Programming,
혼합정수선형계획 NPC: Net Present Cost, 순현재가 LCOA: Levelized Cost of
Ammonia, 암모니아 균등화 비용 CAPEX: Capital Expenditure, 자본지출 OPEX:
Operating Expenditure, 운영비 MCR: Maximum Continuous Rating, 최대 연속
정격 (엔진) SFOC: Specific Fuel Oil Consumption, 비연료소비율
