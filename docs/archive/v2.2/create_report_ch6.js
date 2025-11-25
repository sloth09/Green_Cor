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
        children: [new TextRun("5장. 비용 계산 체계")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("부산항 암모니아 벙커링 인프라의 경제성 평가는 자본지출(CAPEX)과 운영비(OPEX)를 정확히 계산하는 것에서 시작된다. 본 장에서는 각 비용 요소의 계산 방법, 비용 요소별 분해, 그리고 순현재가(NPC) 및 암모니아 균등화 비용(LCOA)의 계산을 설명한다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.1 CAPEX 계산 (자본지출)")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "5.1.1 셔틀 선박 CAPEX", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("셔틀 선박의 자본비는 크기에 따른 스케일링 공식으로 계산된다: CAPEX_shuttle(h) = 61,500,000 × (h / 40,000)^0.75 (USD)\n\n여기서 h는 셔틀 크기(m³), 기준값은 40,000 m³ 셔틀의 기준 가격 61.5M USD, 스케일링 계수는 0.75이다.\n\n예시 (Case 1):\n- 500 m³: 3,894,000 USD\n- 1,000 m³: 6,273,000 USD\n- 5,000 m³: 18,917,000 USD\n\n예시 (Case 2):\n- 10,000 m³: 30,384,000 USD\n- 25,000 m³: 56,219,000 USD\n- 50,000 m³: 98,456,000 USD")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "5.1.2 펌프 시스템 CAPEX", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("펌프 자본비는 펌프 파워를 기반으로 한다:\n\nPump_Power(kW) = 158.73 × Q (m³/h)\nCAPEX_pump(p) = Pump_Power(p) × 2,000 (USD/kW)\n\n펌프 파워 예시: 400 m³/h는 101.2 kW, 1,000 m³/h는 252.8 kW이다.\n\n펌프 CAPEX 예시:\n- 400 m³/h: 202,400 USD\n- 1,000 m³/h: 505,600 USD\n- 1,500 m³/h: 758,400 USD")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "5.1.3 저장탱크 CAPEX (Case 1만)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("35,000톤 저장탱크의 자본비:\n\nCAPEX_tank = 35,000 × 1,000 × 1.215 = 42,525,000 USD\n\n암모니아 저장탱크는 특수 재료가 필요하며, 비용은 저장 용량과 냉각 시스템을 포함한다. Case 1에서만 필요하고, Case 2는 원산지 저장소를 사용한다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.2 OPEX 계산 (운영비)")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "5.2.1 고정 운영비 (FIXED_OPEX)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("고정 운영비는 연간 유지보수비로, CAPEX의 일정 비율이다:\n\n셔틀: OPEX_shuttle = CAPEX_shuttle × 0.05\n예: 5,000 m³ = 945,850 USD/년\n\n펌프: OPEX_pump = CAPEX_pump × 0.05\n예: 1,000 m³/h = 25,280 USD/년\n\n탱크 (Case 1만): OPEX_tank = 42,525,000 × 0.03 = 1,275,750 USD/년")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "5.2.2 변동 운영비 (VARIABLE_OPEX)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("변동 운영비는 실제 운영에 비례한다:\n\n1) 셔틀 연료비\nFuel_per_cycle = MCR × 379(SFOC) × Travel_Time / 1,000,000\n\n5,000 m³ 셔틀 (2시간 왕복):\nFuel = 1,694 × 379 × 2 / 1,000,000 = 1.284 ton\nCost_per_cycle = 1.284 × 600 = 770.40 USD\n\n2) 펌프 전력비\nEnergy_per_cycle = 252.8 kW × 5h = 1,264 kWh\nCost_per_cycle = 1,264 × 0.0769 = 97.16 USD\n\n3) 탱크 냉각비 (Case 1만)\nOPEX_tank_cooling = 35,000 × 1,000 × 0.0378 × 0.0769 = 104,403 USD/년")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.3 순현재가(NPC) 계산")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("NPC는 모든 비용을 현재 가치로 할인한 합계이다:\n\nNPC = Sum(t=2030~2050) [DF(t) × (CAPEX(t) + FIXED_OPEX(t) + VARIABLE_OPEX(t))]\n\n여기서 DF(t) = 1 / 1.07^(t - 2030)이다.\n\n할인인자:\n- 2030년: 1.000\n- 2035년: 0.713\n- 2040년: 0.508\n- 2050년: 0.258\n\n초기 투자의 가중치가 높고, 후기 비용은 더 낮은 가중치를 받으므로 초기에 적절한 규모 구축이 경제적으로 유리하다.")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.4 암모니아 균등화 비용(LCOA)")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("LCOA는 암모니아 1톤당 평균 비용이다:\n\nLCOA = NPC / Total_Supply\n\nTotal_Supply = Sum(t=2030~2050) [DF(t) × Annual_Supply(t)]\n\n예시: NPC = 2,584M USD, Total_Supply = 325M ton\nLCOA = 2,584 / 325 = USD 7.96/ton\n\n참고: 이 값은 추가 비용을 나타낸다. 암모니아 시장 가격(USD 600/ton)에 이를 더하면 전체 비용이다.\n\nCase별 LCOA: Case 1은 USD 250-350/ton, Case 2-1은 USD 220-290/ton, Case 2-2는 USD 200-270/ton (가장 경제적)")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.5 비용 요소별 분해 (사례 분석)")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 1의 최적 시나리오 (5,000 m³ 셔틀 + 1,000 m³/h 펌프) 20년 누적 비용 (USD, 할인 적용):")]
      }),

      new Table({
        columnWidths: [3000, 2000, 2500],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3000, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "비용 항목", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "금액 (M)", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "비중", bold: true, size: 20 })]
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "자본비 (CAPEX)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "  셔틀 + 펌프 + 탱크", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "95.4", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "31.7%", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "고정 운영비 (OPEX_fixed)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "15.0", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "5.0%", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "변동 운영비 (OPEX_variable)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "190.5", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "63.3%", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 3000, type: WidthType.DXA },
                shading: { fill: "E2EFDA", type: ShadingType.CLEAR },
                children: [new Paragraph(new TextRun({ text: "총 순현재가 (NPC)", bold: true, size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                shading: { fill: "E2EFDA", type: ShadingType.CLEAR },
                children: [new Paragraph(new TextRun({ text: "300.9", bold: true, size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                shading: { fill: "E2EFDA", type: ShadingType.CLEAR },
                children: [new Paragraph(new TextRun({ text: "100%", bold: true, size: 20 }))]
              })
            ]
          })
        ]
      }),

      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("")] }),

      new Paragraph({
        spacing: { before: 240, after: 120 },
        children: [new TextRun({ text: "주요 발견사항", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("초기 투자(CAPEX)는 저장탱크 때문에 매우 높다(약 USD 50.2M). 20년 누적 NPC에서 변동비(연료/전력)가 대부분(63.3%)을 차지하므로, 연료 가격과 전기요금이 경제성을 크게 좌우한다. LCOA는 약 USD 7.96/ton이며, 시장 가격 600 USD/ton과 비교하면 벙커링 서비스 프리미엄은 약 1.3%이다.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Ch6.docx", buffer);
  console.log("챕터 6 (비용 계산 체계) 생성 완료: results/Green_Corridor_Report_Ch6.docx");
});
