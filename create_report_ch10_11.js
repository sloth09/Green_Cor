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
        children: [new TextRun("9장. 토의")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 장에서는 최적화 결과의 의미를 해석하고, 정책적 함의를 도출한다. 또한 모델의 한계점과 향후 연구 방향을 제시한다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("9.1 주요 발견사항")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1) Case 선택의 중요성\n\n경제성 측면에서 Case 2-2 (울산)가 일반적으로 가장 우수하다. 이는 다음 이유 때문이다:\n- 가장 짧은 항해 거리 (25해리)\n- 가장 빠른 회전율 (28.34시간 사이클)\n- 가장 낮은 장비 투자 (저장탱크 불필요)\n\nNPC 관점에서 Case 2-2는 Case 1 대비 약 30-40% 절감이 가능하다.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("2) 연료 가격의 지배적 영향\n\n20년 누적 NPC에서 연료 및 에너지 비용이 63%를 차지한다. 따라서:\n- 암모니아 가격의 10% 변동 → NPC 약 6-7% 변동\n- 연료 가격 안정화가 중요\n- 수소/암모니아 가격이 하락하면 더 우호적")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("3) 장기 계획의 필요성\n\n선박 수요가 2030년 50척에서 2050년 500척으로 10배 증가한다. 이는:\n- 초기부터 확장 가능한 인프라 필요\n- 과도한 초기 투자 금지 (비용 낭비)\n- 정기적인 재평가와 업그레이드 필요")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("9.2 실무 적용 가이드라인")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("부산항 관리 주체가 이 모델을 활용하기 위해서는:\n\n1단계: Case 선택\n- 초기 투자 제약 → Case 2-2 선호\n- 운영 유연성 중시 → Case 1 검토\n- 기업 재정 상황 따라 결정\n\n2단계: 연도별 설비 투자 계획\n- 최적해의 연도별 신규 셔틀 구매 시기 반영\n- 조선소 건조 기간 고려 (일반적으로 2-3년)\n- 조기 구매로 할인 가능성 검토\n\n3단계: 운영 관리\n- 연료 가격 변화 모니터링\n- 수요 예측 정기 갱신\n- 매년 모델 업데이트 및 재평가")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("9.3 모델의 한계점")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1) 기술 발전 미반영\n- 현재: 2030-2050년 동안 기술 고정\n- 현실: 펌프, 엔진, 배터리 기술 진화 가능\n- 개선: 기술 개선 로드맵 추가 필요\n\n2) 외부 요인 미고려\n- 정책 변화 (탄소세, 규제)\n- 경쟁사 진입\n- 암모니아 수급 불안정성\n\n3) 리스크 분석 부재\n- 기술 리스크 (장비 고장)\n- 시장 리스크 (수요 급감)\n- 정치 리스크 (정책 변화)\n\n4) 운영 유연성 제한\n- 선박 임차 옵션 미포함\n- 타 포트와의 협력 미포함")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("9.4 향후 연구 방향")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1) 확장된 모델\n- 다중 포트 네트워크 최적화\n- 다양한 연료 (암모니아, 메탄올, 수소) 동시 고려\n- 육상 공급 시설 통합 계획\n\n2) 불확실성 분석\n- 확률론적 수요 모델\n- 시나리오 분석 (낙관/중립/보수)\n- 옵션 가치 분석 (투자 지연 옵션 등)\n\n3) 실제 운영 데이터\n- 파일럿 운영 결과 반영\n- 실제 벙커링 시간 측정\n- 비용 실績 데이터 수집\n\n4) 정책 분석\n- 탄소세 시나리오\n- 보조금 정책 효과\n- 규제 변화 영향")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("10장. 결론")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 연구는 부산항의 암모니아 벙커링 인프라를 최적화하기 위한 MILP 모델을 개발하고, 3가지 Case에 대한 경제성 분석을 수행했다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("10.1 주요 결론")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("첫째, Case 선택이 경제성에 결정적 영향을 미친다. Case 2-2 (울산 근거리)는 Case 1 (부산 저장소) 대비 30-40% 낮은 NPC를 달성할 수 있다.\n\n둘째, 연료 가격이 20년 누적 비용의 60% 이상을 차지하므로, 암모니아 가격 안정화가 프로젝트 성공의 핵심이다.\n\n셋째, 선박 수요의 10배 증가(50척→500척)를 감당하기 위해서는 2030년부터 장기 계획을 수립해야 하며, 연도별 설비 투자 시기가 경제성을 좌우한다.\n\n넷째, 3가지 Case는 상황에 따라 각각의 장점이 있으므로, 부산항의 여건(초기 자본 가용성, 운영 유연성 요구)에 따라 선택해야 한다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("10.2 정책 권고사항")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1) 단기 (2025-2030)\n- Case 2-2 선호도 분석 및 기본 계획 수립\n- 울산 생산시설과의 협력 논의\n- 파일럿 운영을 통한 실제 데이터 수집\n\n2) 중기 (2030-2040)\n- 선택된 Case에 따른 설비 투자 실행\n- 연료 가격 변화에 대한 민감도 관리\n- 모델 검증 및 개선\n\n3) 장기 (2040-2050)\n- 추가 설비 확충\n- 기술 개선 사항 반영\n- 다중 포트 네트워크 확장 검토")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("10.3 최종 평가")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("부산항의 암모니아 벙커링 인프라는 기술적으로 실현 가능하며, 경제적으로도 타당한 프로젝트이다. 특히 Case 2-2 시나리오는 매우 경쟁력 있는 선택지이다.\n\n다만, 암모니아 연료의 시장 성숙도, 국제 규제 환경의 변화, 그리고 기술 혁신의 속도에 따라 최적해가 달라질 수 있으므로, 정기적인 재평가와 계획의 유연성 확보가 필수적이다.\n\n부산항이 한국의 대표 국제 무역항으로서 글로벌 해운 탈탄소화를 주도할 수 있는 인프라를 구축하기 위해서는, 이 모델이 제시하는 최적화 원칙과 경제성 분석을 적극 참고하되, 정책 여건과 시장 상황의 변화에 맞춰 지속적으로 개선해나가야 한다.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Ch10_11.docx", buffer);
  console.log("챕터 10-11 (토의 및 결론) 생성 완료: results/Green_Corridor_Report_Ch10_11.docx");
});
