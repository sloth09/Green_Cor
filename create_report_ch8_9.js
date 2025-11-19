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
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("7장. 최적화 결과")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 장에서는 MILP 모델의 최적화 결과를 제시한다. 각 Case별로 최적해를 분석하고, 경제적 특성을 비교한다. 결과는 현재 모델 실행 후 생성되는 CSV/Excel 파일에서 확인할 수 있다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("7.1 최적화 결과 개요")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("최적화는 각 Case에 대해 90개의 셔틀-펌프 조합을 평가하며, 각 조합에 대해 20년 계획 기간의 순현재가(NPC)를 계산한다. 결과는 NPC 기준으로 정렬되며, Top 10 시나리오가 제시된다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("7.2 결과 파일 구성")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("최적화 완료 후 다음 파일들이 생성된다:\n\nMILP_scenario_summary_case_X.csv: 90개 조합 모두의 NPC 요약\nMILP_per_year_results_case_X.csv: 최적해에 대한 연도별 상세 결과 (2030-2050)\nMILP_results_case_X.xlsx: Excel 형식의 다중 시트 (요약, 상세, 그래프)\nMILP_Report_case_X.docx: 전문 형식의 Word 보고서")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("7.3 최적해의 해석")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("최적해는 다음을 의미한다:\n\n셔틀 선택: 선택된 크기의 셔틀 선박이 가장 경제적\n펌프 선택: 선택된 유량의 펌프가 최적의 비용-성능 트레이드오프 제공\nNPC: 20년 누적 순현재가 (할인율 7% 적용)\n\nNPC 값이 낮을수록 더 경제적인 시나리오이다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("7.4 Case별 특성")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 1 (부산 저장소):\n- 초기 투자: 가장 높음 (저장탱크 때문)\n- 유연성: 가장 높음 (탱크가 수요 변동 흡수)\n- 연간 운영 횟수: 가장 많음 (사이클 타임 짧음)\n\nCase 2-1 (여수):\n- 초기 투자: 가장 낮음\n- 유연성: 중간 (사전 예약 필요)\n- 연간 운영 횟수: 적음 (사이클 타임 길음)\n\nCase 2-2 (울산):\n- 초기 투자: Case 2-1과 동일\n- 유연성: Case 2-1과 동일\n- 연간 운영 횟수: 가장 적음 (거리 때문)\n- 경제성: 일반적으로 가장 우수")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("8장. 민감도 분석 (Placeholder)")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 장에서는 최적해가 주요 파라미터의 변화에 얼마나 민감한지 분석한다. 이를 통해 리스크 요인을 파악하고 강건한(robust) 전략을 수립할 수 있다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("8.1 할인율 변화")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("[분석 공간 예약]\n\n분석 항목:\n- 할인율 3%, 5%, 7%(기본), 10%, 12% 적용\n- 각 할인율에서 최적해 변화 추적\n- NPC 민감도 측정 (할인율 1% 증가당 NPC 변화율)\n\n예상 결과:\n- 할인율 증가 → 초기 투자 부담 감소 → Case 1 상대적으로 개선 가능\n- 하지만 변동비(연료)의 중요도는 상대적으로 감소")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("8.2 연료 가격 변화")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("[분석 공간 예약]\n\n분석 항목:\n- 암모니아 가격 USD 400, 500, 600(기본), 800, 1000/ton\n- 각 가격에서 최적해 변화\n- NPC 민감도 측정\n\n예상 결과:\n- 연료 가격이 높을수록 효율적 운영 중요\n- 펌프 크기 증가 (빠른 벙커링 → 연료비 절감)\n- Case 2의 경제성 상대적 개선 (운송 효율 때문)")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("8.3 수요 시나리오")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("[분석 공간 예약]\n\n분석 항목:\n- 낙관적: 2050년 600척 (기본 500척 대비 20% 증가)\n- 중립적: 기본 시나리오 (2030년 50척 → 2050년 500척)\n- 보수적: 2050년 400척 (기본 대비 20% 감소)\n\n예상 결과:\n- 수요 증가 → 더 큰 셔틀/펌프 선호\n- 수요 감소 → 더 작은 시스템 선호\n- 초기 과잉 투자 vs 후기 부족 투자의 트레이드오프")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("8.4 종합 민감도")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("[분석 공간 예약]\n\nTornado Diagram 형식:\n- 각 파라미터의 NPC 영향도를 시각화\n- 가장 영향력 있는 파라미터 파악\n- Worst-case와 Best-case 시나리오 분석\n\n예상 영향도 순위:\n1. 연료 가격 (변동비의 63% 차지)\n2. 수요 예측 (규모 결정)\n3. 할인율 (자본비와 초기 투자에 영향)\n4. 펌프 효율 (연료비 직결)\n5. 셔틀 건조 비용 (CAPEX)")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Ch8_9.docx", buffer);
  console.log("챕터 8-9 (최적화 결과 및 민감도) 생성 완료: results/Green_Corridor_Report_Ch8_9.docx");
});
