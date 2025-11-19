const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType, VerticalAlign, PageBreak } = require('docx');
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
      // 2장 문제 정의 및 연구 범위
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("2. 문제 정의 및 연구 범위")]
      }),

      // 2.1 부산항 그린 코리도어 개념
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.1 부산항 그린 코리도어 개념")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("부산항은 한국 최대의 컨테이너 항만으로, 2023년 기준 연간 2,200만 TEU 이상을 처리하는 세계 7위 규모의 항만이다. 동북아시아의 전략적 위치에 자리잡고 있어, 한국-중국, 한국-일본, 한국-동남아시아를 연결하는 주요 해상 물류 거점이다.")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("그린 코리도어는 특정 항로에서 무탄소 또는 저탄소 연료만을 사용하는 선박을 운항하도록 하여, 해운 부문의 온실가스 배출을 획기적으로 감축하는 개념이다. 부산항을 중심으로 한 그린 코리도어가 조성되면, 다음과 같은 효과를 기대할 수 있다:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 부산항 입출항 선박의 대기오염 물질 배출 저감 (SOx, NOx, PM)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 역내 해운 산업의 탄소중립 전환 선도")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 친환경 선박 기술 및 연료 공급 산업 육성")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 국제 환경 규제 대응 및 글로벌 경쟁력 강화")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 연구에서는 부산항을 기점으로 하는 그린 코리도어에서 암모니아 추진 선박이 운항하는 시나리오를 상정한다. 이들 선박은 부산항에 기항하여 암모니아 연료를 공급받으며, 이를 위한 벙커링 인프라가 필요하다.")]
      }),

      // 2.2 선박 수요 예측
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.2 선박 수요 예측")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.2.1 암모니아 추진 선박의 성장 시나리오", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("IMO의 탄소중립 목표와 각국의 환경 규제 강화에 따라, 암모니아 추진 선박은 2030년부터 본격적으로 상용화될 것으로 예상된다. 본 연구에서는 다음과 같은 가정을 적용한다:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 2030년: 50척의 암모니아 추진 선박이 부산항을 이용")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 2050년: 500척으로 증가 (10배 성장)")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 증가 패턴: 선형 성장 (연간 약 23.7척씩 증가)")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("이는 보수적 추정치이며, 실제로는 기술 발전과 정책 지원에 따라 더 빠른 성장도 가능하다. 선박 수 N(t)는 다음 식으로 계산된다:")]
      }),
      new Paragraph({
        spacing: { after: 240, before: 120 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "N(t) = 50 + (500 - 50) × (t - 2030) / (2050 - 2030)", italics: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("예를 들어, 2040년의 선박 수는:")]
      }),
      new Paragraph({
        spacing: { after: 240, before: 120 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "N(2040) = 50 + 450 × 10/20 = 275척", italics: true })]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.2.2 선박당 연료 수요", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("각 선박은 부산항에 기항할 때마다 암모니아 연료를 공급받는다. 본 연구에서 가정하는 벙커링 파라미터는 다음과 같다:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 항차당 급유량: 5,000 m³ (약 3,395톤, 밀도 0.679 ton/m³ 가정)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 선박당 연간 항차 수: 12회")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 선박당 연간 소비량: 5,000 m³ × 12 = 60,000 m³")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("따라서 연도별 연간 총 수요는 다음과 같이 계산된다:")]
      }),
      new Paragraph({
        spacing: { after: 240, before: 120 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "연간 수요(t) = N(t) × 60,000 m³", italics: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("예시:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 2030년: 50척 × 60,000 = 3,000,000 m³ (약 2.04백만 톤)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 2040년: 275척 × 60,000 = 16,500,000 m³ (약 11.2백만 톤)")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 2050년: 500척 × 60,000 = 30,000,000 m³ (약 20.4백만 톤)")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.2.3 벙커링 횟수", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("연간 총 벙커링 횟수는 선박 수와 항차 수의 곱이다:")]
      }),
      new Paragraph({
        spacing: { after: 240, before: 120 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "연간 콜 수(t) = N(t) × 12", italics: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("예시:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 2030년: 50 × 12 = 600회")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 2040년: 275 × 12 = 3,300회")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 2050년: 500 × 12 = 6,000회")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("이는 평균적으로 하루 1.6회(2030년)에서 16.4회(2050년)의 벙커링이 필요함을 의미한다.")]
      }),

      // 2.3 세 가지 인프라 시나리오 개요
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.3 세 가지 인프라 시나리오 개요")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("암모니아 벙커링 인프라는 암모니아 저장 위치와 운송 방식에 따라 크게 세 가지 시나리오로 구분할 수 있다. 각 시나리오는 초기 투자비, 운영비, 운영 복잡도 측면에서 상이한 특성을 갖는다.")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.3.1 Case 1: 부산항 저장소 기반", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "개념", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("부산항 내부에 대규모 암모니아 저장 탱크를 건설하고, 소형 셔틀 선박이 저장소와 정박 중인 선박 사이를 왕복하며 연료를 전달하는 방식이다.")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "주요 특징", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 저장 탱크: 35,000톤 규모 (필요 시 복수 탱크)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 셔틀 크기: 500 ~ 5,000 m³ (소형)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 편도 이동 시간: 1.0시간 (항만 내부 이동)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 운영 방식: 소형 셔틀이 여러 번 왕복하여 1회 선박 급유 완료")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 장점: 짧은 운송 거리, 신속한 대응")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 단점: 높은 초기 탱크 건설비, 토지 확보 필요")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.3.2 Case 2-1: 여수 원거리 운송", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "개념", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("전라남도 여수시의 암모니아 생산 시설에서 대형 셔틀 선박에 암모니아를 적재하여 부산항까지 운송하고, 한 번의 항해로 여러 척의 선박에 급유하는 방식이다.")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "주요 특징", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 저장 탱크: 여수 생산시설에만 존재 (부산항에는 없음)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 셔틀 크기: 5,000 ~ 50,000 m³ (대형)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 거리: 86해리 (약 159 km)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 편도 항해 시간: 5.73시간 (15노트 속도)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 운영 방식: 대형 셔틀 1회 왕복으로 여러 선박 급유")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 장점: 탱크 건설비 없음, 대규모 운송 가능")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 단점: 긴 운송 시간, 높은 연료비")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.3.3 Case 2-2: 울산 근거리 운송", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "개념", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("울산광역시의 암모니아 생산 시설에서 대형 셔틀 선박으로 부산항까지 운송하는 방식으로, Case 2-1과 유사하나 거리가 훨씬 짧다.")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun({ text: "주요 특징", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 저장 탱크: 울산 생산시설에만 존재 (부산항에는 없음)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 셔틀 크기: 5,000 ~ 50,000 m³ (대형)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 거리: 25해리 (약 46 km)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 편도 항해 시간: 1.67시간 (15노트 속도)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun("• 운영 방식: 대형 셔틀 1회 왕복으로 여러 선박 급유")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 장점: 탱크 건설비 없음, 짧은 운송 거리로 연료비 절감")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• 단점: 울산 생산시설 의존도 높음")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.3.4 세 가지 Case 비교", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("표 2.1은 세 가지 시나리오의 주요 특성을 비교한다.")]
      }),

      // 표 2.1: Case 비교
      new Paragraph({
        spacing: { before: 120, after: 120 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "표 2.1 세 가지 인프라 시나리오 비교", bold: true })]
      }),
      new Table({
        columnWidths: [2340, 2340, 2340, 2340],
        margins: { top: 100, bottom: 100, left: 180, right: 180 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "구분", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Case 1\n부산항 저장소", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Case 2-1\n여수 운송", bold: true, size: 20 })]
                })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                verticalAlign: VerticalAlign.CENTER,
                children: [new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Case 2-2\n울산 운송", bold: true, size: 20 })]
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "저장 탱크", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "부산항 (35,000톤)", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "여수 생산시설", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "울산 생산시설", size: 20 })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "셔틀 크기", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "500~5,000 m³", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "5,000~50,000 m³", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "5,000~50,000 m³", size: 20 })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "거리", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "항만 내부", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "86 해리", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "25 해리", size: 20 })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "편도 이동시간", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "1.0 시간", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "5.73 시간", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "1.67 시간", size: 20 })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "운영 특성", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "여러 트립/콜", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "여러 선박/항해", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "여러 선박/항해", size: 20 })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "초기 CAPEX 특징", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "탱크비 높음", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "탱크비 없음", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "탱크비 없음", size: 20 })] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "OPEX 특징", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "연료비 낮음", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "연료비 높음", size: 20 })] })]
              }),
              new TableCell({
                borders: cellBorders,
                width: { size: 2340, type: WidthType.DXA },
                children: [new Paragraph({ children: [new TextRun({ text: "연료비 중간", size: 20 })] })]
              })
            ]
          })
        ]
      }),

      // 2.4 의사결정 변수 및 목표
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.4 의사결정 변수 및 목표")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.4.1 의사결정 변수", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("본 연구에서 최적화를 통해 결정해야 할 변수는 다음과 같다:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "1. 셔틀 선박 크기 (Shuttle Size)", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 1080 },
        children: [new TextRun("Case 1: 500, 1,000, 1,500, 2,000, 2,500, 3,000, 3,500, 4,000, 4,500, 5,000 m³ (10종)")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("Case 2: 5,000, 10,000, 15,000, 20,000, 25,000, 30,000, 35,000, 40,000, 45,000, 50,000 m³ (10종)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "2. 펌프 용량 (Pump Capacity)", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("400, 600, 800, 1,000, 1,200, 1,400, 1,600, 1,800, 2,000 m³/h (9종)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "3. 연도별 셔틀 선박 추가 수 (x[t])", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("t년도에 신규로 구매하는 셔틀 선박 대수 (정수)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "4. 연도별 누적 셔틀 수 (N[t])", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("t년도의 총 셔틀 선박 보유 대수 (정수)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "5. 연도별 연간 벙커링 횟수 (y[t])", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("t년도의 연간 총 벙커링 콜 수 또는 항해 수 (연속 변수)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "6. 연도별 저장 탱크 추가 수 (z[t]) - Case 1만", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("t년도에 신규로 건설하는 저장 탱크 개수 (정수)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "7. 연도별 누적 탱크 수 (Z[t]) - Case 1만", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("t년도의 총 저장 탱크 보유 개수 (정수)")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("각 Case별로 셔틀 크기와 펌프 용량의 조합은 10 × 9 = 90가지이며, 각 조합에 대해 연도별 변수가 최적화된다.")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.4.2 목표 함수", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("연구의 목표는 2030-2050년 20년간의 순현재가(Net Present Cost, NPC)를 최소화하는 것이다:")]
      }),
      new Paragraph({
        spacing: { after: 240, before: 120 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Minimize: NPC = Σ[t=2030 to 2050] Discount(t) × TotalCost(t)", italics: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("여기서:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun("• Discount(t) = 1 / (1 + r)^(t - 2030)  (할인율 r = 7%)")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 720 },
        children: [new TextRun("• TotalCost(t) = CAPEX(t) + FixedOPEX(t) + VariableOPEX(t)")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [new TextRun({ text: "2.4.3 주요 제약 조건", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("최적화 모델은 다음 제약 조건을 만족해야 한다:")]
      }),
      new Paragraph({
        spacing: { after: 120, before: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "1. 수요 충족 제약", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("연간 공급량이 연간 수요 이상이어야 함")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "2. 작업시간 제약", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("연간 총 작업시간이 셔틀 수 × 8,000시간 이하")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "3. 저장 용량 제약 (Case 1만)", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("저장 탱크 총 용량이 셔틀 용량의 2배 이상 (안전 여유)")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "4. 누적 제약", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("N[t] = N[t-1] + x[t], Z[t] = Z[t-1] + z[t]")]
      }),
      new Paragraph({
        spacing: { after: 120 },
        indent: { left: 720 },
        children: [new TextRun({ text: "5. 비음수 및 정수 제약", bold: true })]
      }),
      new Paragraph({
        spacing: { after: 240 },
        indent: { left: 1080 },
        children: [new TextRun("x[t], N[t], z[t], Z[t] ≥ 0 및 정수, y[t] ≥ 0")]
      }),
      new Paragraph({
        spacing: { after: 240 },
        children: [new TextRun("상세한 수식은 제3장 방법론에서 다룬다.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report_Ch3.docx", buffer);
  console.log("챕터 3 (문제 정의 및 연구 범위) 생성 완료: results/Green_Corridor_Report_Ch3.docx");
});
