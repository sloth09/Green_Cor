# Green Corridor Ammonia Bunkering Optimization Model

친환경 해운 회랑에서의 암모니아 연료 공급 인프라 최적화 모델입니다.

## 📚 문서 구조

### 빠른 시작
- **[CLAUDE.md](./CLAUDE.md)** - 프로젝트 개요 및 빠른 시작 가이드 (핵심 정보)

### 상세 문서
- **[docs/architecture.md](./docs/architecture.md)** - 코드 아키텍처 및 기술 세부사항
- **[docs/configuration.md](./docs/configuration.md)** - YAML 파라미터 설정 가이드
- **[docs/changelog.md](./docs/changelog.md)** - 버전별 변경사항 (v2.0 → v2.3.2)

## 🚀 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. 설정
`config/base.yaml`의 `execution` 섹션을 수정:
```yaml
execution:
  run_mode: "single"        # single, all, multiple, single_scenario
  single_case: "case_2"
```

### 3. 실행
```bash
python main.py
```

### 4. 결과 확인
`results/` 폴더에서 CSV, Excel, Word 형식 결과 확인

## 🎯 핵심 내용

### 세 가지 시나리오 (Case)
1. **Case 1**: 부산항 저장소 기반 (셔틀 왕복)
2. **Case 2**: 울산 → 부산 (근거리)
3. **Case 3**: 여수 → 부산 (장거리)

### 주요 파라미터
| 항목 | 기본값 |
|------|--------|
| 셔틀 크기 | 500-5000 m³ |
| 펌프 유량 | 400-2000 m³/h |
| 할인율 | 7% |
| 연료 가격 | 600 USD/ton |

더 자세한 내용은 [CLAUDE.md](./CLAUDE.md)를 참조하세요.

## 📁 프로젝트 구조

```
Green_Cor/
├── config/                    # YAML 설정 파일
├── src/                       # Python 모듈
├── docs/                      # 상세 문서
├── results/                   # 결과 폴더 (자동 생성)
├── CLAUDE.md                  # 프로젝트 문서 (핵심)
├── README.md                  # 이 파일
├── main.py                    # 단일 케이스 실행
├── run_all_cases.py           # 다중 케이스 실행
└── requirements.txt           # 의존성
```

## 🔧 설정 방법

### 빠른 시간 계산만 (2-3초)
```yaml
execution:
  run_mode: "single_scenario"
  single_case: "case_2"
  single_scenario_shuttle_cbm: 5000
  single_scenario_pump_m3ph: 1000
```

### 모든 조합 최적화 (5분)
```yaml
execution:
  run_mode: "single"
  single_case: "case_2"
```

### 모든 케이스 병렬 실행 (10분)
```yaml
execution:
  run_mode: "all"
  num_jobs: 4
```

더 자세한 정보는 [docs/configuration.md](./docs/configuration.md)를 참조하세요.

## 📊 주요 기능

- ✅ **3가지 케이스 지원** (부산, 여수, 울산)
- ✅ **YAML 기반 설정** (파라미터 쉽게 변경)
- ✅ **병렬 실행** (다중 케이스 동시 처리)
- ✅ **다중 출력 형식** (CSV, Excel, Word)
- ✅ **MILP 최적화** (20년 순현재가 최소화)

## 🐛 문제 해결

| 문제 | 해결방법 |
|------|---------|
| `No module named 'pulp'` | `pip install pulp` 실행 |
| Config 파일 없음 | `config/` 폴더 확인 |
| 최적해 없음 | 펌프 크기나 셔틀 크기 증가 |
| 느린 실행 | 병렬 처리 사용 (`num_jobs: 4`) |

## 📖 버전 정보

- **최신 버전**: v2.3.2
- **주요 개선**:
  - Case 1/2 아키텍처 통합
  - 펌핑 시간 계산 정확화
  - 공통 로직 라이브러리화

버전별 상세 변경사항은 [docs/changelog.md](./docs/changelog.md)를 참조하세요.

## 🔗 관련 링크

- [프로젝트 개요](./CLAUDE.md)
- [설정 가이드](./docs/configuration.md)
- [기술 아키텍처](./docs/architecture.md)
- [변경 이력](./docs/changelog.md)

## 📞 지원

문제가 발생하면:
1. [CLAUDE.md](./CLAUDE.md)의 문제 해결 섹션 확인
2. [docs/](./docs/) 폴더의 상세 문서 참조
3. 코드의 로그 확인

---

**마지막 업데이트**: 2025-11-22 (v2.3.2)
