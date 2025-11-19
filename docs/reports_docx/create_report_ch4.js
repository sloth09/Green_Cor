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
      // 3장: MILP 최적화 모델
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("3장. MILP 최적화 모델")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("부산항 암모니아 벙커링 인프라의 최적화 문제는 혼합정수선형계획(Mixed Integer Linear Programming, MILP) 모델로 수립된다. 본 장에서는 모델의 개요, 결정변수, 목적함수, 제약식, 그리고 경제적 파라미터를 상세히 설명한다.")]
      }),

      // 3.1 모델 개요 및 가정
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.1 모델 개요 및 가정")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "모델 목표", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 모델의 목표는 2030년부터 2050년까지 20년 계획 기간 동안 부산항에서의 암모니아 벙커링 인프라 구축 및 운영에 소요되는 순현재가(Net Present Cost, NPC)를 최소화하는 것이다. 의사결정 변수는 다음 세 가지이다:\n\n1) 셔틀 선박의 최적 크기 및 필요 개수\n2) 벙커링 펌프의 최적 용량\n3) 저장탱크의 필요 크기 (Case 1만 해당)\n\n이를 통해 수요 증가에 따른 확장 가능하고 경제적인 인프라를 설계할 수 있다.")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "주요 가정사항", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("다음의 주요 가정사항이 모델에 적용된다:\n\n• 시간 계획 기간: 2030-2050년 (21년, 매년 단위)\n• 선박 수요: 선형 성장 (2030년 50척 → 2050년 500척)\n• 선박당 연간 항차: 12회 (고정)\n• 항차당 급유량: 5,000 m³ (고정)\n• 할인율: 7% (경제적 평가)\n• 셔틀과 탱크는 내구 연한 동안 운영 가능\n• 육상 연료 공급 펌프 유량: 1,500 m³/h (고정, 모든 Case 동일)\n• 최대 연간 운영시간: 8,000시간/년/셔틀")]
      }),

      // 3.2 결정변수 정의
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.2 결정변수 정의")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("MILP 모델의 결정변수는 다음과 같이 정의된다:")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "h ∈ H: 셔틀 크기 (m³)", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Case 1: 500, 1,000, 1,500, 2,000, 2,500, 3,000, 3,500, 4,000, 4,500, 5,000 m³\nCase 2: 5,000, 10,000, 15,000, 20,000, 25,000, 30,000, 35,000, 40,000, 45,000, 50,000 m³")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "p ∈ P: 펌프 용량 (m³/h)", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("400, 600, 800, 1,000, 1,200, 1,400, 1,600, 1,800, 2,000 m³/h")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "x[t, h, p]: t년도에 구입하는 크기 h, 펌프 p의 셔틀 수 (개, 정수변수)", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("연도 t = 2030, 2031, ..., 2050")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "N[t, h, p]: t년도 누적 셔틀 수 (개, 정수변수)", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("N[t, h, p] = Σ_{τ=2030}^{t} x[τ, h, p]")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "y[t, h, p]: t년도 연간 벙커링 횟수 (회, 연속변수)", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("각 h, p 조합에 대해 연간 벙커링 작업 횟수")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "z[t]: t년도 신규 추가 저장탱크 수 (개, 정수변수, Case 1만)", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Z[t]: t년도 누적 탱크 수 (개, 정수변수, Case 1만)")]
      }),

      // 3.3 목적함수 (NPC 최소화)
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.3 목적함수 (NPC 최소화)")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("목적함수는 20년 계획 기간의 순현재가를 최소화하는 것이다:")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Minimize: NPC = Σ_{t=2030}^{2050} [DF(t) × (CAPEX(t) + FIXED_OPEX(t) + VARIABLE_OPEX(t))]", italics: true, bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("여기서:")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("DF(t) = 할인인자 = 1 / (1 + r)^(t - 2030), r = 0.07\nCAPEX(t) = t년도 자본지출 (자본비)\nFIXED_OPEX(t) = t년도 고정 운영비\nVARIABLE_OPEX(t) = t년도 변동 운영비")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "자본지출 (CAPEX)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("CAPEX(t) = Σ_{h,p} [x[t,h,p] × (CAPEX_shuttle(h) + CAPEX_pump(p))] + z[t] × CAPEX_tank\n\nCAPEX_shuttle(h)는 스케일링 공식으로 계산:\nCAPEX_shuttle(h) = 61,500,000 × (h / 40,000)^0.75 (USD)\n\nCAPEX_pump(p)는 펌프 파워 기반 계산:\nPump_Power(p) = (4 × 10^5 Pa × p/3600) / 0.7 (kW)\nCAPEX_pump(p) = Pump_Power(p) × 2,000 (USD/kW)\n\nCAPEX_tank = 42,525,000 USD (35,000톤 저장탱크, Case 1만)")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "고정 운영비 (FIXED_OPEX)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("FIXED_OPEX(t) = Σ_{h,p} [N[t,h,p] × (OPEX_shuttle(h) + OPEX_pump(p))] + Z[t] × OPEX_tank\n\n여기서 고정 운영비는 CAPEX의 연간 백분율:\nOPEX_shuttle(h) = CAPEX_shuttle(h) × 0.05 (5% 유지보수)\nOPEX_pump(p) = CAPEX_pump(p) × 0.05 (5% 유지보수)\nOPEX_tank = CAPEX_tank × 0.03 (3% 유지보수)")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "변동 운영비 (VARIABLE_OPEX)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("VARIABLE_OPEX(t) = Σ_{h,p} [y[t,h,p] × (OPEX_shuttle_fuel + OPEX_pump_power)] + Z[t] × OPEX_tank_cooling\n\n셔틀 연료비:\nOPEX_shuttle_fuel = MCR(h) × SFOC × Travel_time × SFOC_weight × Fuel_price\n  MCR(h): 셔틀 최대 연속 정격 (kW)\n  SFOC: 비연료소비율 = 379 g/kWh\n  Travel_time: 왕복 항해 시간 (h)\n  Fuel_price: 600 USD/ton\n\n펌프 전력 비용:\nOPEX_pump_power = Pump_Power(p) × Pumping_time × Electricity_price\n  Pumping_time: 해당 조합의 벙커링 시간 (h/회)\n  Electricity_price: 0.0769 USD/kWh\n\n탱크 냉각비 (Case 1만):\nOPEX_tank_cooling = Tank_Volume × Cooling_Energy × Electricity_price\n  Cooling_Energy: 0.0378 kWh/kg")]
      }),

      // 3.4 제약식 (Constraints)
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.4 제약식")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "3.4.1 누적 제약 (Accumulation Constraint)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("N[t, h, p] = N[t-1, h, p] + x[t, h, p]\n\n셔틀은 한번 구입하면 내구 연한 동안 운영되며, 매년 신규 구입분이 누적된다.")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "3.4.2 수요 충족 제약 (Demand Satisfaction)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Σ_{h,p} [y[t,h,p] × Bunker_Volume] ≥ Demand[t]\n\n여기서:\nBunker_Volume = 5,000 m³ (항차당 급유량)\nDemand[t] = Vessels[t] × Voyages_per_year × Bunker_Volume\n  Vessels[t]: t년도 암모니아 선박 수\n  Voyages_per_year: 12회/년")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "3.4.3 운영시간 제약 (Operating Hour Constraint)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("Σ_{h,p} [y[t,h,p] × trips_per_call(h) × Cycle_Time(h,p)] ≤ N[t,h,p] × H_max\n\n여기서:\ntrips_per_call(h): h 크기 셔틀이 5,000 m³를 전달하는데 필요한 트립 수\n  Case 1: ceil(5,000 / h)\n  Case 2: 1 (한 번의 항해에 여러 척 서빙)\n\nCycle_Time(h,p): h 크기 셔틀과 p 용량 펌프의 왕복 사이클 시간\n  Case 1: 육상적재 + 편도이동 + 호스작업 + 벙커링 + 복귀\n  Case 2: 육상적재 + 항해 + 부산진입 + 각선박서빙 + 복귀\n\nH_max = 8,000시간/년/셔틀 (최대 연간 운영시간)")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "3.4.4 저장탱크 용량 제약 (Tank Capacity Constraint, Case 1만)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("N[t,h,p] × h × β ≤ Z[t] × Tank_Volume\n\n여기서:\nβ = 안전계수 = 2.0 (재고 운영의 여유)\nTank_Volume = 35,000톤 (2.857 × 10^4 m³ at 1.225 kg/m³ 밀도)\n\n탱크 용량이 셔틀 적재량의 여러 배가 되어야 안정적 운영이 가능하다.")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "3.4.5 비음수 제약 (Non-negativity Constraints)", bold: true })]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("x[t,h,p] ≥ 0 (정수)\nN[t,h,p] ≥ 0 (정수)\ny[t,h,p] ≥ 0 (연속)\nz[t] ≥ 0 (정수, Case 1만)\nZ[t] ≥ 0 (정수, Case 1만)")]
      }),

      // 3.5 할인율 및 시간가치
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.5 할인율 및 시간가치")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("경제 평가에 사용되는 할인율은 7%이다. 이는 해운 산업의 자본 비용과 투자 수익률을 반영한 표준 할인율이다.\n\n할인인자 DF(t) = 1 / (1.07)^(t - 2030)\n\n예시:\n- 2030년: DF(2030) = 1.00\n- 2035년: DF(2035) = 1 / 1.07^5 = 0.713\n- 2050년: DF(2050) = 1 / 1.07^20 = 0.258\n\n이를 통해 초기 투자의 가중치가 높고, 이후 연도의 비용은 더 낮은 가중치를 받는다. 따라서 초기에 적절한 규모의 인프라를 구축하는 것이 경제적으로 유리하다.")]
      }),

      // 3.6 주요 모델 파라미터 요약 (표)
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.6 주요 모델 파라미터 요약")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("아래 표는 모델에 사용되는 주요 파라미터를 요약한다:")]
      }),

      new Table({
        columnWidths: [2500, 2000, 2000],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "파라미터", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "값", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "단위", bold: true, size: 20 })]
                })]
              })
            ]
          }),
          // 경제 파라미터
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "할인율", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "0.07 (7%)", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "%", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "암모니아 가격", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "600", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "USD/ton", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "전기요금", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "0.0769", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "USD/kWh", size: 20 }))]
              })
            ]
          }),
          // 운영 파라미터
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "최대 연간 운영시간", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "8,000", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "시간/년", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "항차당 급유량", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "5,000", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "m³", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "선박당 연간 항차", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "12", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "회/년", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "육상 펌프 유량", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "1,500", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "m³/h", size: 20 }))]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2500, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "탱크 안전계수", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "2.0", size: 20 }))]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2000, type: WidthType.DXA },
                children: [new Paragraph(new TextRun({ text: "배", size: 20 }))]
              })
            ]
          })
        ]
      }),

      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("")] }),

      // 정리
      new Paragraph({
        spacing: { before: 240, after: 240 },
        children: [new TextRun("본 장에서 설명한 MILP 모델은 Case별로 약간의 변형이 있으며, 다음 장에서는 3가지 Case 시나리오의 구체적인 구현을 상세히 다룬다. 특히 Case 1과 Case 2의 기본적인 운영 개념의 차이(다중 왕복 vs 단일 항해)가 모델의 제약식과 경제성 분석에 어떤 영향을 미치는지 살펴볼 것이다.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Ch4.docx", buffer);
  console.log("챕터 4 (MILP 방법론) 생성 완료: results/Green_Corridor_Report_Ch4.docx");
});
