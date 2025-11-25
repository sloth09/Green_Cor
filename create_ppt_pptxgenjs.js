const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Green Corridor Team';
pptx.title = 'Case 1: Busan Port Ammonia Bunkering Optimization';

// 슬라이드 1: 타이틀
let slide = pptx.addSlide();
slide.background = { color: '2C3E50' };
slide.addText('Case 1: 부산항 저장소', {
  x: 0.5, y: 1.5, w: 9, h: 1,
  fontSize: 44, bold: true, color: 'FFFFFF', align: 'center', fontFace: 'Arial'
});
slide.addText('암모니아 벙커링 최적화', {
  x: 0.5, y: 2.6, w: 9, h: 0.5,
  fontSize: 24, bold: true, color: '27AE60', align: 'center', fontFace: 'Arial'
});
slide.addText('Green Corridor Ammonia Optimization Model', {
  x: 0.5, y: 3.2, w: 9, h: 0.4,
  fontSize: 16, color: 'ECF0F1', align: 'center', fontFace: 'Arial'
});
slide.addText('2030-2050 20년 분석', {
  x: 0.5, y: 3.8, w: 9, h: 0.4,
  fontSize: 14, color: 'BDC3C7', align: 'center', fontFace: 'Arial'
});
console.log('[OK] Slide 1: Title');

// 슬라이드 2: Executive Summary
slide = pptx.addSlide();
slide.background = { color: 'F8F9FA' };
slide.addText('Executive Summary', {
  x: 0.3, y: 0.2, w: 9.4, h: 0.4,
  fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
});

const summaryItems = [
  { label: '최적 구성', value: '2,500 m³ Shuttle + 2,000 m³/h Pump', y: 0.8 },
  { label: '20년 NPC', value: '$217.14 Million', y: 1.4 },
  { label: 'LCOAmmonia', value: '$0.92 per ton', y: 2.0 },
  { label: '사이클 타임', value: '6.92 hours', y: 2.6 }
];

summaryItems.forEach(item => {
  slide.addText(item.label, {
    x: 0.5, y: item.y, w: 2, h: 0.25,
    fontSize: 10, color: '666666', bold: true, fontFace: 'Arial'
  });
  slide.addText(item.value, {
    x: 2.6, y: item.y, w: 6.8, h: 0.25,
    fontSize: 11, color: '2C3E50', bold: true, fontFace: 'Arial'
  });
});
console.log('[OK] Slide 2: Executive Summary');

// 슬라이드 3-12: 나머지 콘텐트
const contentSlides = [
  {
    title: 'Case 1: 부산항 저장소 시나리오',
    items: ['운영 구조: 부산항 저장탱크 → 부산항 내 선박 (2 nm)', '주요 특징: 유연한 운영, 빠른 사이클 vs 저장탱크 CAPEX', '저장 탱크: 35,000톤 | 셔틀: 500-5,000 m³', 'NPC: $217.14M | LCOAmmonia: $0.92/ton']
  },
  {
    title: 'MILP 최적화 모델',
    items: ['목적함수: 20년 순현재가(NPC) 최소화', '의사결정 변수: 셔틀 크기, 펌프 용량, 연도별 셧틀 수', '주요 제약식: 수요 충족, 정박시간, 운영시간, 탱크용량', '할인율: No Discounting (0%) - 모든 연도 동일 가중치']
  },
  {
    title: 'NPC 히트맵 분석',
    items: ['행축: 셔틀 크기 (m³) | 열축: 펌프 용량 (m³/h)', '최적 영역: 2,500 m³ 셔틀, 1,600-2,000 m³/h, NPC $217-220M', '회피 영역: <1,200 m³/h 펌프, >4,000 m³ 셔틀', '[이미지: case1_01_npc_heatmap.png]']
  },
  {
    title: 'Top 10 시나리오 비교',
    items: ['1위: 2,500×2,000 $217.14M (최적)', '2위-5위: 2,500×(1,800~1,200) $219-230M', '6위-10위: 2,000×(2,000~1,600), 3,000×(1,400~1,200)', '[이미지: case1_02_top10_breakdown.png]']
  },
  {
    title: '사이클 타임 분석',
    items: ['육상 적재: 1.67시간 (2,500 m³ ÷ 1,500 m³/h)', '왕복 이동: 2.00시간 (부산항 내 2 nm)', '펌핑: 1.25시간 (선박 적재)', '총 사이클 타임: 6.92 시간 (연간 1,157회 가능)']
  },
  {
    title: '비용 구조 분석 (20년)',
    items: ['셔틀 CAPEX: $92.23M (42.4%)', '저장탱크 CAPEX: $28.9M (13.3%) - 주의', '연료/에너지 OPEX: $49.97M (23.0%)', '20년 NPC: $217.14M']
  },
  {
    title: '운영 지표 및 효율성',
    items: ['시간 활용도: 100% | 연간 사이클: 1,157회', '연간 급유: 578회 | 연간 공급: 2.89M ton', '초기 (2030): 3-4 셔틀 | 최대 (2050): 30-40 셔틀', '[이미지: case1_10_cost_vs_demand.png]']
  },
  {
    title: '민감도 분석',
    items: ['연료 가격: 매우 높은 영향도 (±10% → NPC ±$21.7M)', '셀틀/펌프 크기: 중간 영향도', '수요 증가: 높은 영향도 (셸틀 투자 필요)', '[이미지: case1_11_tornado_diagram.png]']
  },
  {
    title: '구축 로드맵 (2030-2050)',
    items: ['Phase 1 (2030-33): 초기 인프라, 셔틀 3-4척, 저장탱크 35,000톤', 'Phase 2 (2034-40): 확대, 셔틀 10-12척 추가', 'Phase 3 (2041-50): 대규모 운영, 셔틀 30-40척 누적', '[이미지: case1_08_year_shuttles.png]']
  },
  {
    title: '전략적 권고사항',
    items: ['Case 1 장점: 단거리 운영, 빠른 사이클, 유연성', 'Case 1 단점: 저장탱크 CAPEX $28.9M, 냉각 필수, 높은 NPC', '권고: 펌프 1,200-2,000 m³/h | 셔틀 2,500 m³ (최적)', '결론: 부산항 중심 운영 필수시만 선택. Case 2-2보다 38% 비쌈.']
  }
];

let slideNum = 3;
for (const slideContent of contentSlides) {
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };

  slide.addText(slideContent.title, {
    x: 0.3, y: 0.2, w: 9.4, h: 0.4,
    fontSize: 26, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  let itemY = 0.75;
  for (const item of slideContent.items) {
    slide.addText(item, {
      x: 0.5, y: itemY, w: 9, h: 0.5,
      fontSize: 10, color: '555555', fontFace: 'Arial'
    });
    itemY += 0.55;
  }

  console.log(`[OK] Slide ${slideNum}: ${slideContent.title}`);
  slideNum++;
}

// 파일 저장
pptx.writeFile({ fileName: 'Case1_Presentation_Final.pptx' })
  .then(() => {
    const fs = require('fs');
    const stats = fs.statSync('Case1_Presentation_Final.pptx');
    const sizeMB = (stats.size / 1024 / 1024).toFixed(2);
    console.log('[INFO] 파일 저장 완료!');
    console.log(`[OK] 파일: Case1_Presentation_Final.pptx`);
    console.log(`[OK] 슬라이드: 12장`);
    console.log(`[OK] 크기: ${sizeMB} MB`);
  })
  .catch(err => {
    console.error(`[ERROR] ${err.message}`);
    process.exit(1);
  });
