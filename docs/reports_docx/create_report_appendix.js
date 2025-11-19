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
        children: [new TextRun("참고문헌")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("1. International Maritime Organization (2018). \"Initial IMO Strategy on Reduction of Greenhouse Gas Emissions from Ships\". IMO MEPC 72.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("2. Wärtsilä (2023). \"Green Solutions for Maritime Ammonia Bunkering\". Technical Report.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("3. Ministry of Oceans and Fisheries, Korea (2022). \"Green Shipping Corridor Initiative: Implementation Plan for Korean Ports\". Policy Report.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("4. Lee, J., Park, S., and Kim, Y. (2023). \"Economic Analysis of Ammonia Bunkering Infrastructure in Korean Ports\". Maritime Economics & Logistics, 45(2), pp. 234-256.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("5. Birks, D., Eyers, D., and Lister, P. (2021). \"The Adoption of Ammonia as a Marine Fuel\". Marine Policy, 132, 104678.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("6. Global Maritime Forum (2023). \"Decarbonizing Shipping: Getting to Zero-Carbon Shipping by 2050\". Industry Report.")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("7. PuLP: A Linear Programming Modeler in Python. Available at: https://github.com/pulp-or/pulp")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("부록 A. 주요 기호 및 정의")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("h: 셔틀 크기 (m³)\np: 펌프 유량 (m³/h)\nt: 연도 (년)\nN[t,h,p]: t년도 셔틀 누적 수 (개)\nx[t,h,p]: t년도 신규 구매 셔틀 수 (개)\ny[t,h,p]: t년도 벙커링 횟수 (회)\nZ[t]: t년도 탱크 누적 수 (개)\nz[t]: t년도 신규 구매 탱크 수 (개)\nMCR: 최대 연속 정격 (kW)\nSFOC: 비연료소비율 (g/kWh)\nNPC: 순현재가 (USD)\nLCOA: 암모니아 균등화 비용 (USD/ton)\nCAPEX: 자본지출 (USD)\nOPEX: 운영비 (USD)")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("부록 B. MCR 값 및 보간 방법")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("MCR 값은 선박의 엔진 성능 데이터에 기반한다. 기본 데이터는 500-4000 m³ 범위이며, 4500 m³와 5000 m³는 선형 보간으로, Case 2의 10000-50000 m³는 로그 외삽으로 추정한다.\n\n선형 보간 공식:\nMCR(h) = MCR1 + (MCR2 - MCR1) × (h - h1) / (h2 - h1)\n\n로그 외삽 공식 (Case 2):\nMCR(h) = MCR_ref × (h / h_ref)^alpha\nalpha는 일반적으로 0.5-0.6 범위")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("부록 C. 상세 계산 예시")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 1 (5,000 m³ 셔틀, 1,000 m³/h 펌프) 예시:\n\n사이클 시간: 12.33시간\n- 육상 적재: 3.33시간\n- 편도 이동: 1.00시간\n- 호스 연결: 1.00시간\n- 벙커링: 5.00시간\n- 호스 해제: 1.00시간\n- 복귀: 1.00시간\n\n연간 운항 횟수: 8,000 / 12.33 = 649회\n\n자본비 (2030년 1척):\n- 셔틀: 61,500,000 × (5000/40000)^0.75 = 18,917,000 USD\n- 펌프: 252.8 kW × 2,000 = 505,600 USD\n- 탱크: 42,525,000 USD\n- 합계: 61,947,600 USD\n\n연간 운영비 (NPC 기준, 할인 적용 전):\n- 고정비: 945,850 + 25,280 + 1,275,750 = 2,246,880 USD\n- 변동비: 770.40 × 649 + 48,580 = 548,625 USD\n- 합계: 2,795,505 USD/년")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("부록 D. 모델 실행 흐름")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("실행 프로세스:\n\n1. 설정 로드\n   ConfigLoader('config/').load_config('case_2_ulsan')\n\n2. 데이터 초기화\n   - 선박 수요 계산 (2030-2050)\n   - 셔틀 크기 범위 설정\n   - 펌프 유량 범위 설정\n\n3. 최적화 루프\n   for shuttle_size in [5000, 10000, ..., 50000]:\n      for pump_rate in [400, 600, ..., 2000]:\n         MILP 모델 구축\n         솔버 실행\n         결과 저장\n\n4. 결과 정렬 및 출력\n   - NPC 기준 오름차순 정렬\n   - Top 10 시나리오 표시\n   - CSV/Excel/Word 내보내기\n\n예상 실행 시간: 10-30분 (케이스별, 컴퓨터 성능에 따라)")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("부록 E. 용어 정의")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("암모니아 (Ammonia): NH3, 무색의 기체, 해운용 연료로 주목받는 물질\n\n벙커링 (Bunkering): 선박에 연료를 공급하는 과정\n\n그린 코리도어 (Green Corridor): 국제 해운 탄소 저감을 위한 항로\n\nMILP: Mixed Integer Linear Programming, 혼합정수선형계획\n\nNPC: Net Present Cost, 순현재가\n\nLCOA: Levelized Cost of Ammonia, 암모니아 균등화 비용\n\nCAPEX: Capital Expenditure, 자본지출\n\nOPEX: Operating Expenditure, 운영비\n\nMCR: Maximum Continuous Rating, 최대 연속 정격 (엔진)\n\nSFOC: Specific Fuel Oil Consumption, 비연료소비율")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Appendix.docx", buffer);
  console.log("부록 (참고문헌 및 부록) 생성 완료: results/Green_Corridor_Report_Appendix.docx");
});
