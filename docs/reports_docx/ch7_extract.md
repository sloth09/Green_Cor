6장. 모델 구현

본 장에서는 MILP 모델의 Python 기반 구현 구조를 설명한다. 모델은
모듈화되어 있으며, 각 모듈이 특정한 기능을 담당한다. 이를 통해 코드의
재사용성과 유지보수성을 높이고, 다양한 시나리오를 쉽게 실행할 수 있다.

6.1 프로젝트 구조 개요

프로젝트는 다음과 같은 폴더 구조를 가진다: config/ (설정 파일), src/
(Python 모듈), results/ (결과 폴더), main.py (단일 케이스 실행),
run_all_cases.py (다중 케이스 실행), requirements.txt (의존성)

6.2 주요 모듈 설명

**6.2.1 ConfigLoader (설정 로드)**

ConfigLoader는 YAML 설정 파일들을 로드하여 파이썬 딕셔너리로 변환한다.
base.yaml과 case_X.yaml을 병합하고 설정을 검증한다.

**6.2.2 CycleTimeCalculator (시간 계산)**

CycleTimeCalculator는 각 셔틀-펌프 조합의 사이클 시간을 계산한다. Case
1은 부산항 내 다중 왕복을, Case 2는 장거리 항해 후 다중 선박 서빙의
시간을 계산한다. 연간 최대 운항 횟수와 공급 능력도 산정한다.

**6.2.3 CostCalculator (비용 계산)**

CostCalculator는 모든 비용 요소를 계산한다. CAPEX(셔틀, 펌프, 저장탱크),
OPEX(고정/변동), 그리고 NPC를 계산하며, 비용 요소별 분해를 제공한다.

**6.2.4 Optimizer (MILP 최적화)**

Optimizer는 PuLP 라이브러리를 사용하여 MILP 모델을 구축하고 풀이한다.
모든 셔틀-펌프 조합에 대해 20년 계획 기간의 최적 구매 시점을 결정하고
최소 NPC를 가진 조합을 도출한다.

6.3 실행 흐름

실행 흐름: (1) 설정 로드, (2) 시간 계산 초기화, (3) 비용 계산 초기화,
(4) 최적화 실행, (5) 결과 정렬 (NPC 기준), (6) 결과 내보내기 (CSV,
Excel, Word)

6.4 YAML 설정 파일 구조

base.yaml의 주요 섹션: time_period (2030-2050), economy (할인율,
연료가격, 전기요금), shipping (선박 수, 항차 수), operations (최대
운영시간), execution (실행 모드, 출력 형식)

6.5 의존성 및 설치

주요 의존성: PuLP (MILP 솔버), pandas (데이터 처리), PyYAML (설정 파일),
openpyxl (Excel), python-docx (Word). pip install -r requirements.txt로
설치한다.

6.6 실행 예시

config/base.yaml에서 execution 섹션을 설정한 후 python main.py를
실행하면, 최적화 진행률이 표시되고 완료 후 결과가 CSV, Excel, Word
형식으로 저장된다.
