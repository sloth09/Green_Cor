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
      // 4장: 시스템 설계 (3가지 Case 시나리오)
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("4장. 시스템 설계: 3가지 Case 시나리오")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 모델은 암모니아 벙커링 인프라의 지리적 위치와 운영 방식에 따라 3가지 Case로 구분된다. 이 장에서는 각 Case의 인프라 구성, 운영 시간 구조, 그리고 구체적인 예시 계산을 설명한다.")]
      }),

      // 4.1 Case 1: 부산항 저장소 기반
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("4.1 Case 1: 부산항 저장소 기반")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.1.1 인프라 구성", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 1은 부산항에 대규모 저장탱크가 이미 존재하는 상황을 모델링한다:\n\n[암모니아 공급 터미널]\n      ↓ (대량 운송)\n[부산항 저장탱크: 35,000톤]\n      ↓ (셔틀 적재)\n[소형 셔틀: 500~5,000 m³]\n      ↓ (항만 내 이동)\n[부산항 내 선박들]\n\n주요 특징:\n• 저장탱크: 35,000톤 (고정 용량)\n• 셔틀 크기: 500, 1,000, 1,500, 2,000, 2,500, 3,000, 3,500, 4,000, 4,500, 5,000 m³\n• 편도 이동: 부산항 내부 (약 1시간)\n• 운영 개념: 소형 셔틀이 여러 번 왕복하여 선박들에게 연료 공급")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.1.2 운영 시간 구조", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 1의 완전한 사이클 시간은 다음과 같이 구성된다:\n\n1) 육상 적재 (부산항 저장탱크)\n   - 육상 펌프 유량: 1,500 m³/h (고정)\n   - 적재 시간 = Shuttle_Size / 1,500 (시간)\n\n2) 항만 내 운송 (편도)\n   - 저장탱크 → 선박 이동: 1.0시간\n\n3) 호스 연결 및 기체 퍼징\n   - 호스 연결 및 기체 제거: 1.0시간\n\n4) 벙커링 (연료 유체 흐름)\n   - 벙커링 시간 = 5,000 / Pump_Rate (시간)\n   - 주의: 벙커링 양은 항상 5,000 m³ (한 척의 항차 수요)\n   - 펌프가 크면 벙커링 시간이 짧아짐\n\n5) 호스 분리 및 암모니아 퍼징\n   - 호스 분리 및 기체 제거: 1.0시간\n\n6) 항만 내 복귀\n   - 선박 → 저장탱크 복귀: 1.0시간\n\n총 사이클 시간 = 적재시간 + 1.0 + 1.0 + 벙커링시간 + 1.0 + 1.0")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.1.3 예시 계산 (5,000 m³ 셔틀, 1,000 m³/h 펌프)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("구체적인 예시를 통해 Case 1의 운영 시간을 계산한다:\n\n1) 육상 적재\n   5,000 m³ ÷ 1,500 m³/h = 3.33시간\n\n2) 편도 이동\n   1.00시간\n\n3) 호스 연결 및 퍼징\n   1.00시간\n\n4) 벙커링\n   5,000 m³ ÷ 1,000 m³/h = 5.00시간\n\n5) 호스 분리 및 퍼징\n   1.00시간\n\n6) 복귀\n   1.00시간\n\n─────────────────\n총 사이클: 12.33시간\n\n의미:\n• 한 척의 셔틀이 12.33시간마다 5,000 m³를 공급\n• 연간 최대 가동 시간: 8,000시간/년\n• 연간 최대 사이클: 8,000 ÷ 12.33 = 649회\n• 연간 최대 공급량: 649 × 5,000 = 3,245,000 m³/년")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.1.4 저장탱크의 역할", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("35,000톤 저장탱크는 Case 1의 핵심 인프라다:\n\n1) 수요 변동 흡수\n   선박들의 언제든 연료 요청을 받을 수 있도록 준비\n\n2) 셔틀 효율화\n   셔틀이 필요한 시점에 즉시 적재 가능\n\n3) 유연성\n   저장탱크 덕분에 사전 예약 없이도 운영 가능\n\n제약식: N[t] × h × 2.0 ≤ Tank_Volume\n(모든 셔틀의 최대 적재량 × 2배 안전계수 ≤ 탱크 용량)\n\nCapEx: 42,525,000 USD (약 4.25억 달러)\nAnnual OpEx: 1,275,750 USD (유지보수 + 냉각)")]
      }),

      // 4.2 Case 2-1: 여수 원거리 운송
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("4.2 Case 2-1: 여수 원거리 운송")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.2.1 인프라 구성", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 2-1은 부산항에 저장탱크가 없고, 여수의 암모니아 생산시설에서 직접 운송하는 시나리오다:\n\n[여수 암모니아 생산시설]\n(저장탱크: 30,000~50,000톤)\n      ↓ (대형 셔틀 적재)\n[대형 셔틀: 5,000~50,000 m³]\n      ↓ (86해리, 약 5.73시간)\n[부산항 선박들]\n\n주요 특징:\n• 근거지 저장탱크: 여수 시설 (본 모델 미포함)\n• 셔틀 크기: 5,000, 10,000, 15,000, 20,000, 25,000, 30,000, 35,000, 40,000, 45,000, 50,000 m³\n• 항해 거리: 86해리\n• 항해 속도: 15노트\n• 편도 항해 시간: 86 / 15 = 5.73시간\n• 운영 개념: 한 번의 대형 셔틀 항해로 여러 선박에게 일괄 공급")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.2.2 운영 시간 구조", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 2-1의 완전한 사이클은 다음과 같이 구성된다:\n\n1) 근거지 준비 및 적재\n   - 근거지 접근: 1.0시간\n   - 육상 펌프 유량: 1,500 m³/h (고정)\n   - 적재 시간 = Shuttle_Size / 1,500 (시간)\n\n2) 여수 → 부산 항해\n   - 거리: 86해리\n   - 속도: 15노트\n   - 항해 시간: 5.73시간\n\n3) 부산항 진입\n   - 항만 진입: 1.0시간\n\n4) 여러 선박에 대한 벙커링 (반복)\n   각 선박마다 다음을 반복:\n   - 선박 이동/접안: 1.0시간\n   - 호스 연결 및 퍼징: 1.0시간\n   - 벙커링 (5,000 m³): 5,000 / Pump_Rate (시간)\n   - 호스 분리 및 퍼징: 1.0시간\n   - 소계: 8시간 + 벙커링 시간\n\n   Vessels_per_trip = floor(Shuttle_Size / 5,000)\n   반복 횟수: Vessels_per_trip회\n\n5) 부산 → 여수 복귀\n   - 항만 퇴출: 1.0시간\n   - 항해: 5.73시간\n\n총 사이클 = 적재 + 5.73 + 1.0 + (8.0 × Vessels_per_trip) + 5.73 + 1.0")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.2.3 예시 계산 (10,000 m³ 셔틀, 1,000 m³/h 펌프)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1) 근거지 적재\n   10,000 m³ ÷ 1,500 m³/h = 6.67시간\n\n2) 여수 → 부산 항해\n   5.73시간\n\n3) 부산항 진입\n   1.00시간\n\n4) 선박 서빙 (10,000 ÷ 5,000 = 2척)\n   각 선박 (1시간 + 1시간 + 5시간 + 1시간) × 2척\n   = 8시간 × 2척 = 16.00시간\n\n5) 부산항 퇴출\n   1.00시간\n\n6) 부산 → 여수 복귀\n   5.73시간\n\n─────────────────\n총 사이클: 36.13시간\n\n의미:\n• 한 번의 항해로 2척의 선박을 주유\n• 연간 최대 항해: 8,000 ÷ 36.13 = 221회\n• 연간 최대 선박 처리: 221 × 2 = 442척\n• 연간 최대 공급량: 221 × 10,000 = 2,210,000 m³/년")]
      }),

      // 4.3 Case 2-2: 울산 근거리 운송
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("4.3 Case 2-2: 울산 근거리 운송")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.3.1 인프라 구성", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 2-2는 Case 2-1과 동일한 구조이지만, 울산에서 출발하므로 거리가 훨씬 짧다:\n\n[울산 암모니아 생산시설]\n(저장탱크: 30,000~50,000톤)\n      ↓ (대형 셔틀 적재)\n[대형 셔틀: 5,000~50,000 m³]\n      ↓ (25해리, 약 1.67시간)\n[부산항 선박들]\n\n주요 특징:\n• 근거지 저장탱크: 울산 시설 (본 모델 미포함)\n• 셔틀 크기: 5,000, 10,000, 15,000, 20,000, 25,000, 30,000, 35,000, 40,000, 45,000, 50,000 m³\n• 항해 거리: 25해리 (여수 86해리 대비 71% 단축)\n• 항해 속도: 15노트\n• 편도 항해 시간: 25 / 15 = 1.67시간 (여수 대비 4.06시간 절감)\n• 운영 개념: Case 2-1과 동일하나, 빠른 회전율로 더 높은 활용도")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.3.2 운영 시간 구조", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 2-2의 시간 구조는 Case 2-1과 동일하나, 항해 시간이 짧다:\n\n1) 근거지 준비 및 적재: 1.0 + Shuttle_Size/1,500\n2) 울산 → 부산 항해: 1.67시간\n3) 부산항 진입: 1.0시간\n4) 선박 벙커링 (반복): 8시간 × Vessels_per_trip\n5) 부산항 퇴출: 1.0시간\n6) 부산 → 울산 복귀: 1.67시간\n\n총 사이클 = 적재 + 1.67 + 1.0 + (8.0 × Vessels_per_trip) + 1.0 + 1.67")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "4.3.3 예시 계산 (10,000 m³ 셔틀, 1,000 m³/h 펌프)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1) 근거지 준비 및 적재\n   1.00시간 + (10,000 ÷ 1,500시간) = 7.67시간\n\n2) 울산 → 부산 항해\n   1.67시간\n\n3) 부산항 진입\n   1.00시간\n\n4) 선박 서빙 (10,000 ÷ 5,000 = 2척)\n   각 선박 (1시간 + 1시간 + 5시간 + 1시간) × 2척\n   = 8시간 × 2척 = 16.00시간\n\n5) 부산항 퇴출\n   1.00시간\n\n6) 부산 → 울산 복귀\n   1.67시간\n\n─────────────────\n총 사이클: 28.34시간\n\n의미:\n• 한 번의 항해로 2척의 선박을 주유\n• 연간 최대 항해: 8,000 ÷ 28.34 = 282회\n• 연간 최대 선박 처리: 282 × 2 = 564척\n• 연간 최대 공급량: 282 × 10,000 = 2,820,000 m³/년\n\nCase 2-1 대비:\n• 사이클 단축: 36.13 → 28.34 (7.79시간, 22% 단축)\n• 항해 능력 증가: 221 → 282 (27% 증가)")]
      }),

      // 4.4 Case별 시간 구조 비교 표
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("4.4 Case별 시간 구조 비교")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("아래 표는 3가지 Case의 운영 시간을 비교한다. 모두 5,000 m³ 셔틀 + 1,000 m³/h 펌프 기준이다:")]
      }),

      new Table({
        columnWidths: [1800, 1400, 1400, 1400],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "항목", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Case 1", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Case 2-1", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Case 2-2", bold: true, size: 20 })]
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "위치", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "부산", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "여수", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "울산", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "적재 시간 (h)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "3.33", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "3.33", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "3.33", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "항해 시간 (h)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "2.00", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "11.46", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "3.34", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "호스 작업 (h)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "2.00", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "2.00", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "2.00", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "벙커링 (h)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "5.00", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "8.00", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "8.00", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "총 사이클 (h)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
                children: [new Paragraph(new TextRun({ text: "12.33", bold: true, size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
                children: [new Paragraph(new TextRun({ text: "36.13", bold: true, size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
                children: [new Paragraph(new TextRun({ text: "28.34", bold: true, size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "연간 최대 횟수", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "649", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "221", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "282", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "동시 서빙 선박", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "1", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "1", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "1", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 1800, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "연간 최대 공급 (M m³)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "3.24", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "1.11", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 1400, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "1.41", size: 20 }))]
              })
            ]
          })
        ]
      }),

      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("")] }),

      // 정리
      new Paragraph({
        spacing: { before: 240, after: 240 },
        children: [new TextRun("본 장에서는 3가지 Case의 기본적인 구성과 운영 시간 구조를 설명했다. 핵심은:\n\n1) Case 1 (부산 저장소): 작은 셔틀이 여러 번 왕복하므로 높은 유연성과 높은 운영 비용\n2) Case 2-1 (여수): 큰 셔틀이 장거리를 운반하므로 낮은 초기 비용이지만 긴 사이클 타임\n3) Case 2-2 (울산): Case 2-1과 동일 구조이지만 거리가 짧아 더 높은 활용도\n\n다음 장에서는 이러한 시간 구조를 기반으로 한 비용 계산 체계를 상세히 다룬다.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Ch5.docx", buffer);
  console.log("챕터 5 (Case 시나리오 상세) 생성 완료: results/Green_Corridor_Report_Ch5.docx");
});
