# 기술보고서 작성 진행상황

**작성일**: 2025-11-19
**목표**: 부산항 그린 코리도어 암모니아 벙커링 인프라 최적화 기술보고서 (한글, DOCX)

---

## 1. 현재까지 완료된 작업

### ✅ 완료된 챕터

#### 챕터 1-2: 표지, 요약, 서론
- **파일**: `results/Green_Corridor_Report_Ch1_2.docx`
- **생성 스크립트**: `create_report_ch1_2.js`
- **내용**:
  - 표지 (제목, 부제목, 버전, 연도)
  - 요약 (연구 배경, 목적, 방법론, 주요 결과 예정, 기대 효과)
  - 1장 서론
    - 1.1 연구 배경 (해운 탈탄소화, 암모니아 연료, 그린 코리도어)
    - 1.2 연구의 필요성
    - 1.3 연구 목적 및 범위
    - 1.4 보고서 구성

#### 챕터 3: 문제 정의 및 연구 범위
- **파일**: `create_report_ch3.js` (생성됨, 실행 필요)
- **내용**:
  - 2장 문제 정의 및 연구 범위
    - 2.1 부산항 그린 코리도어 개념
    - 2.2 선박 수요 예측 (2030: 50척 → 2050: 500척)
    - 2.3 세 가지 인프라 시나리오 개요 (Case 1, 2-1, 2-2 비교표 포함)
    - 2.4 의사결정 변수 및 목표

---

## 2. 다음 세션에서 작업할 내용

### 📋 작업 순서

#### Step 1: 챕터 3 생성 (즉시 실행 가능)
```bash
node create_report_ch3.js
```
- 결과: `results/Green_Corridor_Report_Ch3.docx` 생성됨

#### Step 2: 챕터 4 작성 (MILP 방법론)
- **파일**: `create_report_ch4.js` (신규 작성 필요)
- **내용**:
  - 3장 MILP 최적화 모델
    - 3.1 모델 개요 및 가정
    - 3.2 결정 변수 정의
    - 3.3 목적함수 (NPC 최소화)
    - 3.4 제약 조건
      - 수요 충족 제약
      - 작업시간 제약
      - 저장 용량 제약 (Case 1)
      - 누적 제약
    - 3.5 할인율 및 시간가치
    - 표: 주요 모델 파라미터 요약

#### Step 3: 챕터 5 작성 (Case 시나리오 상세)
- **파일**: `create_report_ch5.js` (신규 작성 필요)
- **내용**:
  - 4장 시스템 설계: 3가지 Case 시나리오
    - 4.1 Case 1: 부산항 저장소 기반
      - 인프라 구성
      - 운영 시간 구조 (상세 breakdown)
      - 예시 계산 (5,000 m³ 셔틀, 1,000 m³/h 펌프)
    - 4.2 Case 2-1: 여수 원거리 운송
      - 인프라 구성
      - 운영 시간 구조
      - 예시 계산
    - 4.3 Case 2-2: 울산 근거리 운송
      - 인프라 구성
      - 운영 시간 구조
      - 예시 계산
    - 표: 시간 구조 비교
    - [그림 공간 확보]: 운영 흐름도

#### Step 4: 챕터 6 작성 (비용 계산)
- **파일**: `create_report_ch6.js` (신규 작성 필요)
- **내용**:
  - 5장 비용 계산 체계
    - 5.1 CAPEX 계산
      - 셔틀 선박 (스케일링 공식)
      - 펌프 시스템
      - 저장 탱크 (Case 1)
    - 5.2 OPEX 계산
      - 고정 OPEX (유지보수)
      - 변동 OPEX (연료, 전력)
    - 5.3 순현재가(NPC) 계산
    - 5.4 암모니아 균등화 비용(LCOA)
    - 표: 비용 요소 및 계산식 정리

#### Step 5: 챕터 7 작성 (모델 구현)
- **파일**: `create_report_ch7.js` (신규 작성 필요)
- **내용**:
  - 6장 모델 구현
    - Python 기반 구조
    - YAML 설정 관리
    - 모듈 설명 (config_loader, optimizer, cost_calculator)
    - [그림 공간 확보]: 시스템 아키텍처 다이어그램

#### Step 6: 챕터 8-9 작성 (결과 및 분석 - Placeholder)
- **파일**: `create_report_ch8_9.js` (신규 작성 필요)
- **내용**:
  - 7장 최적화 결과 (Placeholder)
    - 7.1 Case 1 결과
      - [표 공간]: 최적 조합 Top 10
      - [그림 공간]: 셔틀-펌프 조합별 NPC 히트맵
      - [그림 공간]: 연도별 셔틀 수 증가
    - 7.2 Case 2-1 결과
    - 7.3 Case 2-2 결과
    - 7.4 3가지 Case 종합 비교
      - [표 공간]: 최적해 비교
      - [그림 공간]: NPC 구성요소 비교 차트
  - 8장 민감도 분석 (Placeholder)
    - 8.1 할인율 변화
    - 8.2 연료 가격 변화
    - 8.3 수요 시나리오 변화
    - [그림 공간]: Tornado diagram

#### Step 7: 챕터 10-11 작성 (토의 및 결론)
- **파일**: `create_report_ch10_11.js` (신규 작성 필요)
- **내용**:
  - 9장 토의
    - 9.1 주요 발견사항
    - 9.2 실무 적용 가이드라인
    - 9.3 모델의 한계점
    - 9.4 향후 연구 방향
  - 10장 결론

#### Step 8: 참고문헌 및 부록
- **파일**: `create_report_appendix.js` (신규 작성 필요)
- **내용**:
  - 참고문헌
  - 부록
    - A. 수학 표기법 정리
    - B. MCR 값 및 보간 방법
    - C. 상세 계산 예시
    - D. 코드 사용 설명서

#### Step 9: 전체 통합
- 모든 챕터를 하나의 DOCX로 통합하는 스크립트 작성
- 또는 Word에서 수동으로 병합

---

## 3. 참고 자료

### 주요 문서
- `CLAUDE.md`: 프로젝트 전체 개요, 시간 구조, Case 설명, v2.3 개선사항
- `PROJECT_ANALYSIS_REPORT.md`: (존재 시) 분석 보고서
- `CAPEX_OPEX_CALCULATION_GUIDE.md`: (존재 시) 비용 계산 가이드

### 핵심 파라미터 (CLAUDE.md 참조)
- **수요**: 2030년 50척 → 2050년 500척 (선형 증가)
- **항차당 급유량**: 5,000 m³
- **선박당 연간 항차**: 12회
- **최대 연간 운영시간**: 8,000시간/년
- **할인율**: 7%
- **암모니아 가격**: $600/ton
- **전기요금**: $0.0769/kWh
- **탱크 크기**: 35,000톤 (Case 1)
- **육상 펌프 유량**: 1,500 m³/h (고정)

### Case별 특징
| Case | 셔틀 크기 | 거리 | 편도 시간 | 저장 탱크 |
|------|----------|------|---------|----------|
| 1 (부산) | 500-5,000 m³ | 항만 내부 | 1.0h | 부산항 (35,000톤) |
| 2-1 (여수) | 5,000-50,000 m³ | 86 해리 | 5.73h | 여수 생산시설 |
| 2-2 (울산) | 5,000-50,000 m³ | 25 해리 | 1.67h | 울산 생산시설 |

### 시간 구조 예시 (CLAUDE.md 참조)
**Case 1 (5,000 m³ 셔틀, 1,000 m³/h 펌프)**:
```
육상 적재:     3.33h (5,000 ÷ 1,500)
편도 항해:     1.00h
호스 연결:     1.00h
벙커링:        5.00h (5,000 ÷ 1,000)
호스 해제:     1.00h
복귀 항해:     1.00h
─────────────────────
총 사이클:    12.33h
```

**Case 2-2 울산 (10,000 m³ 셔틀, 1,000 m³/h 펌프)**:
```
육상 적재:     6.67h (10,000 ÷ 1,500)
울산→부산:     1.67h
부산항 진입:   1.00h
선박 서빙:    16.00h (2척 × 8h)
부산→울산:     1.67h
부산항 퇴출:   1.00h
─────────────────────
총 사이클:    28.01h
```

---

## 4. 코드 템플릿

### JavaScript DOCX 생성 기본 템플릿

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageBreak } = require('docx');
const fs = require('fs');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Malgun Gothic", size: 22 }
      }
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Malgun Gothic" },
        paragraph: { spacing: { before: 480, after: 240 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Malgun Gothic" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 1 }
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 24, bold: true, color: "000000", font: "Malgun Gothic" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 2 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // 여기에 내용 추가
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("챕터 제목")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("섹션 제목")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본문 내용...")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_ChX.docx", buffer);
  console.log("챕터 X 생성 완료: results/Green_Corridor_Report_ChX.docx");
});
```

### 표 생성 템플릿

```javascript
new Table({
  columnWidths: [3120, 3120, 3120],  // 3 columns
  margins: { top: 100, bottom: 100, left: 180, right: 180 },
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 3120, type: WidthType.DXA },
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "헤더1", bold: true, size: 20 })]
          })]
        }),
        // 나머지 헤더 셀...
      ]
    }),
    new TableRow({
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 3120, type: WidthType.DXA },
          children: [new Paragraph({ children: [new TextRun({ text: "데이터1", size: 20 })] })]
        }),
        // 나머지 데이터 셀...
      ]
    })
  ]
})
```

### Placeholder 그림 공간 템플릿

```javascript
new Paragraph({
  spacing: { before: 240, after: 240 },
  alignment: AlignmentType.CENTER,
  children: [new TextRun({
    text: "[그림 X.X 삽입 예정: 셔틀-펌프 조합별 NPC 히트맵]",
    italics: true,
    color: "666666"
  })]
}),
new Paragraph({
  spacing: { after: 240 },
  children: [new TextRun({
    text: "이 그림은 90개 셔틀-펌프 조합의 NPC를 히트맵으로 시각화하여, 최적 영역을 식별한다.",
    size: 20,
    color: "666666"
  })]
})
```

---

## 5. 다음 세션 시작 시 프롬프트

다음 세션에서 작업을 이어갈 때 Claude에게 다음과 같이 요청하세요:

```
REPORT_PROGRESS.md 파일을 읽고, 부산항 암모니아 벙커링 기술보고서 작성을 이어서 진행해줘.

현재 상태:
- 챕터 1-2 (표지, 요약, 서론) 완료: results/Green_Corridor_Report_Ch1_2.docx
- 챕터 3 (문제 정의) 스크립트 작성 완료: create_report_ch3.js

다음 작업:
1. create_report_ch3.js 실행 (node create_report_ch3.js)
2. 챕터 4 (MILP 방법론) 작성 시작

CLAUDE.md, REPORT_PROGRESS.md를 참고해서 이어서 작성해줘.
한 번에 모든 챕터를 작성하지 말고, 챕터별로 나눠서 작성하고 확인하면서 진행하자.
```

---

## 6. 최종 통합 방법

모든 챕터가 완성되면 다음 두 가지 방법 중 하나로 통합:

### 방법 1: JavaScript로 통합 (권장)
- 모든 챕터의 children 배열을 하나로 합쳐서 단일 DOCX 생성
- 스크립트: `create_report_full.js`

### 방법 2: Word에서 수동 병합
1. 챕터 1-2 파일 열기
2. 삽입 > 개체 > 파일의 텍스트 선택
3. 챕터 3, 4, 5... 순서대로 삽입
4. 최종 파일 저장: `Green_Corridor_Ammonia_Bunkering_Technical_Report.docx`

---

## 7. 주의사항

### JavaScript 작성 시
- 한글 폰트: `Malgun Gothic` 사용
- 크기: Heading1=32pt, Heading2=28pt, Heading3=24pt, Body=22pt (size는 half-point 단위)
- 간격: before/after spacing으로 여백 조절
- 표: columnWidths + 각 셀의 width 모두 설정
- PageBreak: 반드시 Paragraph 안에 넣기

### 내용 작성 시
- 중복 없이 작성
- 보고서만 보면 전체 내용을 파악할 수 있도록 상세하게
- 결과 섹션은 placeholder로 공간만 확보
- 그림 위치는 설명과 함께 표시

### 참고 문서
- CLAUDE.md의 시간 구조와 비용 계산 공식을 정확히 반영
- v2.3 개선사항 (펌핑 시간 수정, Case 1/2 아키텍처 통합) 포함

---

**작성자 노트**: 이 문서를 기반으로 다음 세션에서 챕터별로 순차적으로 작성을 이어가면 됩니다. 각 챕터를 완성할 때마다 실행하고 확인한 후 다음 챕터로 진행하세요.
