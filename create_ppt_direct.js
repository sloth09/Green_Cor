const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Green Corridor Team';
  pptx.title = 'Case 1: Busan Port Ammonia Bunkering Optimization';

  const figuresPath = 'C:\\code\\Green_Cor\\results\\figures';

  console.log('[INFO] PPT 생성 시작...');

  // Slide 0: Title
  let slide = pptx.addSlide();
  slide.background = { color: '2C3E50' };
  slide.addText('Case 1: 부산항 저장소', {
    x: 0.5, y: 1.5, w: 9, h: 1,
    fontSize: 48, bold: true, color: 'FFFFFF', align: 'center', fontFace: 'Arial'
  });
  slide.addText('암모니아 벙커링 최적화', {
    x: 0.5, y: 2.7, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: '27AE60', align: 'center', fontFace: 'Arial'
  });
  slide.addText('Green Corridor Ammonia Optimization Model', {
    x: 0.5, y: 3.4, w: 9, h: 0.4,
    fontSize: 20, color: 'ECF0F1', align: 'center', fontFace: 'Arial'
  });
  console.log('[OK] Slide 0: Title');

  // Slide 1: Executive Summary
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('Executive Summary', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const metrics = [
    { label: '최적 구성 (Optimal Configuration)', value: '2,500 m³ Shuttle + 2,000 m³/h Pump', y: 1.0 },
    { label: '20년 순현재가 (20-Year NPC)', value: '$217.14 Million', y: 1.8 },
    { label: '암모니아 물류 비용 (LCOAmmonia)', value: '$0.92 per ton', y: 2.6 },
    { label: '사이클 타임 (Cycle Duration)', value: '6.92 hours (부산항 내 단거리)', y: 3.4 }
  ];

  metrics.forEach((m, idx) => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: m.y, w: 8.8, h: 0.5,
      fill: { color: 'FFFFFF' },
      line: { color: 'CCCCCC', width: 1 },
      rectRadius: 0.1
    });
    slide.addText(m.label, {
      x: 0.7, y: m.y + 0.05, w: 4, h: 0.2,
      fontSize: 11, color: '999999', fontFace: 'Arial'
    });
    slide.addText(m.value, {
      x: 0.7, y: m.y + 0.25, w: 8, h: 0.2,
      fontSize: 14, bold: true, color: '2C3E50', fontFace: 'Arial'
    });
  });
  console.log('[OK] Slide 1: Executive Summary');

  // Slide 2: Scenario
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('Case 1: 부산항 저장소 시나리오', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const scenarioData = [
    { title: '운영 구조', items: ['출발지: 부산항 저장 탱크', '목적지: 부산항 내 선박', '거리: ~2 nm (단거리)'], x: 0.5, y: 1.0 },
    { title: '주요 특징', items: ['장점: 유연한 운영, 빠른 주기', '단점: 저장탱크 CAPEX, 냉각'], x: 5.2, y: 1.0 },
    { title: '기술 사양', items: ['저장 탱크: 35,000톤', '셔틀 크기: 500-5,000 m³', '트립당: 2-10회'], x: 0.5, y: 2.6 },
    { title: '경제성', items: ['NPC: $217.14M', 'LCOAmmonia: $0.92/ton', '2030: 3-4 셔틀, 2050: 30-40'], x: 5.2, y: 2.6 }
  ];

  scenarioData.forEach(box => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: box.x, y: box.y, w: 4.3, h: 1.3,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 2 },
      rectRadius: 0.1
    });
    slide.addText(box.title, {
      x: box.x + 0.15, y: box.y + 0.1, w: 4, h: 0.25,
      fontSize: 13, bold: true, color: '2C3E50', fontFace: 'Arial'
    });

    let itemY = box.y + 0.4;
    box.items.forEach(item => {
      slide.addText(item, {
        x: box.x + 0.2, y: itemY, w: 4, h: 0.22,
        fontSize: 10, color: '555555', fontFace: 'Arial'
      });
      itemY += 0.23;
    });
  });
  console.log('[OK] Slide 2: Scenario');

  // Slide 3: Model Overview
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('MILP 최적화 모델', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const sections = [
    { title: '목적함수 (Objective Function)', content: '20년간 순현재가(NPC) 최소화\n= CAPEX + OPEX (20년 누계)', y: 1.0 },
    { title: '의사결정 변수 (Decision Variables)', content: '셔틀 크기: 500-5,000 m³\n펌프 용량: 400-2,000 m³/h\n연도별 셔틀 수, 저장 탱크: 35,000톤', y: 1.9 },
    { title: '주요 제약식 (Constraints)', content: '연간 암모니아 수요 충족\n선박당 최대 4시간 정박\n셔틀 최대 8,000시간/년\n저장 탱크 용량 (35,000톤)', y: 3.0 },
    { title: '할인율 설정', content: 'No Discounting (0%)\n모든 연도가 동일한 가중치', y: 4.1 }
  ];

  sections.forEach(sec => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: sec.y, w: 8.8, h: 0.8,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 2 },
      rectRadius: 0.1
    });
    slide.addText(sec.title, {
      x: 0.7, y: sec.y + 0.08, w: 3, h: 0.25,
      fontSize: 12, bold: true, color: '2C3E50', fontFace: 'Arial'
    });
    slide.addText(sec.content, {
      x: 0.7, y: sec.y + 0.35, w: 8, h: 0.42,
      fontSize: 10, color: '555555', fontFace: 'Arial', valign: 'top'
    });
  });
  console.log('[OK] Slide 3: Model Overview');

  // Slide 4: NPC Heatmap
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('NPC 히트맵 분석', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  // Left info box
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 1.0, w: 3.5, h: 3.5,
    fill: { color: 'FFFFFF' },
    line: { color: '27AE60', width: 2 },
    rectRadius: 0.1
  });

  slide.addText('셔틀 크기 vs 펌프 용량', {
    x: 0.7, y: 1.15, w: 3.1, h: 0.3,
    fontSize: 12, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const heatmapInfo = [
    '행축: 셔틀 크기 (m³)',
    '열축: 펌프 용량 (m³/h)',
    '',
    '최적 영역:',
    '- 2,500 m³ 셔틀',
    '- 1,600-2,000 m³/h',
    '- NPC: $217-220M',
    '',
    '회피 영역:',
    '- <1,200 m³/h 펌프',
    '- >4,000 m³ 셔틀'
  ];

  let infoY = 1.5;
  heatmapInfo.forEach(line => {
    slide.addText(line, {
      x: 0.7, y: infoY, w: 3.1, h: 0.2,
      fontSize: 10, color: line.includes('-') ? 'E67E22' : '555555', fontFace: 'Arial'
    });
    infoY += 0.22;
  });

  // Right placeholder for image
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.2, y: 1.0, w: 5.2, h: 3.5,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_01_npc_heatmap.png]', {
    x: 4.2, y: 2.4, w: 5.2, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 4: NPC Heatmap');

  // Slide 5: Top 10 Scenarios
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('Top 10 시나리오 비교', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const top10Data = [
    ['순위', 'Shuttle×Pump', 'NPC ($M)'],
    ['1', '2,500×2,000', '217.14'],
    ['2', '2,500×1,800', '219.59'],
    ['3', '2,500×1,600', '220.79'],
    ['4', '2,500×1,400', '227.90'],
    ['5', '2,500×1,200', '230.16'],
    ['6', '2,000×2,000', '262.66'],
    ['7', '2,000×1,800', '264.18'],
    ['8', '2,000×1,600', '266.67'],
    ['9', '3,000×1,200', '274.33'],
    ['10', '3,000×1,400', '266.28']
  ];

  slide.addTable(top10Data, {
    x: 0.5, y: 1.0, w: 3.8, h: 3.3,
    border: { pt: 1, color: 'CCCCCC' },
    fill: { color: 'F8F9FA' },
    colW: [0.8, 1.5, 1.5],
    fontSize: 9,
    fontFace: 'Arial'
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.5, y: 1.0, w: 5.0, h: 3.3,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_02_top10_breakdown.png]', {
    x: 4.5, y: 2.3, w: 5.0, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 5: Top 10 Scenarios');

  // Slide 6: Cycle Time
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('사이클 타임 분석 (최적해 기준)', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const cycleComponents = [
    { label: '육상 적재 시간', value: '1.67 시간', desc: '2,500 m³ ÷ 1,500 m³/h', y: 1.0 },
    { label: '왕복 이동 시간', value: '2.00 시간', desc: '부산항 내 2 nm 거리', y: 1.45 },
    { label: '펌핑 시간', value: '1.25 시간', desc: '선박 적재 (선박당)', y: 1.9 },
    { label: '호스 연결/해제', value: '2.00 시간', desc: '2회 연결/해제', y: 2.35 }
  ];

  cycleComponents.forEach(comp => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: comp.y, w: 3.8, h: 0.4,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 1 },
      rectRadius: 0.05
    });
    slide.addText(comp.label, {
      x: 0.65, y: comp.y + 0.05, w: 2.5, h: 0.15,
      fontSize: 10, bold: true, color: '2C3E50', fontFace: 'Arial'
    });
    slide.addText(comp.value, {
      x: 3.3, y: comp.y + 0.05, w: 1, h: 0.15,
      fontSize: 11, bold: true, color: 'E67E22', align: 'right', fontFace: 'Arial'
    });
    slide.addText(comp.desc, {
      x: 0.65, y: comp.y + 0.22, w: 3.1, h: 0.12,
      fontSize: 9, color: '999999', fontFace: 'Arial'
    });
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 2.85, w: 3.8, h: 0.7,
    fill: { color: '27AE60' },
    line: { color: '27AE60', width: 1 },
    rectRadius: 0.05
  });
  slide.addText('총 사이클 타임', {
    x: 0.65, y: 2.92, w: 3.1, h: 0.18,
    fontSize: 11, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });
  slide.addText('6.92 시간', {
    x: 0.65, y: 3.12, w: 3.1, h: 0.25,
    fontSize: 16, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });
  slide.addText('연간 약 1,157회 주기 가능', {
    x: 0.65, y: 3.38, w: 3.1, h: 0.12,
    fontSize: 9, color: 'ECF0F1', fontFace: 'Arial'
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.5, y: 1.0, w: 5.0, h: 3.55,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_05_cycle_time_breakdown.png]', {
    x: 4.5, y: 2.3, w: 5.0, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 6: Cycle Time');

  // Slide 7: Cost Analysis
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('비용 구조 분석 (20년)', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const costs = [
    { label: '셔틀 CAPEX', value: '$92.23M', pct: '42.4%', y: 1.0 },
    { label: '펌프/벙커링 CAPEX', value: '$10.38M', pct: '4.8%', y: 1.35 },
    { label: '저장탱크 CAPEX', value: '$28.9M', pct: '13.3% ⚠️', y: 1.7 },
    { label: '연료/에너지 OPEX', value: '$49.97M', pct: '23.0%', y: 2.05 },
    { label: '기타 OPEX', value: '$58.74M', pct: '27.1%', y: 2.4 }
  ];

  costs.forEach(cost => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: cost.y, w: 3.8, h: 0.32,
      fill: { color: 'FFFFFF' },
      line: { color: 'CCCCCC', width: 1 },
      rectRadius: 0.05
    });
    slide.addText(cost.label, {
      x: 0.65, y: cost.y + 0.05, w: 1.8, h: 0.22,
      fontSize: 10, color: '2C3E50', fontFace: 'Arial'
    });
    slide.addText(cost.value, {
      x: 2.5, y: cost.y + 0.05, w: 1.0, h: 0.22,
      fontSize: 10, bold: true, color: '27AE60', fontFace: 'Arial'
    });
    slide.addText(cost.pct, {
      x: 3.5, y: cost.y + 0.05, w: 0.75, h: 0.22,
      fontSize: 9, color: '999999', align: 'right', fontFace: 'Arial'
    });
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 2.8, w: 3.8, h: 0.75,
    fill: { color: '2C3E50' },
    line: { color: '27AE50', width: 1 },
    rectRadius: 0.05
  });
  slide.addText('20년 NPC', {
    x: 0.65, y: 2.85, w: 3.1, h: 0.18,
    fontSize: 11, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });
  slide.addText('$217.14M', {
    x: 0.65, y: 3.05, w: 3.1, h: 0.4,
    fontSize: 18, bold: true, color: 'FFFFFF', fontFace: 'Arial'
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.5, y: 1.0, w: 5.0, h: 3.55,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_07_cost_pie_chart.png]', {
    x: 4.5, y: 2.3, w: 5.0, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 7: Cost Analysis');

  // Slide 8: Operating Metrics
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('운영 지표 및 효율성', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const metrics2 = [
    { left: '시간 활용도: 100%', right: '연간 사이클: 1,157' },
    { left: '연간 급유: 578회', right: '연간 공급: 2.89M ton' },
    { left: '2030년 셔틀: 3-4척', right: '2050년 셔틀: 30-40척' }
  ];

  let metricsY = 1.0;
  metrics2.forEach(row => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: metricsY, w: 4.3, h: 0.6,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 1 },
      rectRadius: 0.05
    });
    slide.addText(row.left, {
      x: 0.7, y: metricsY + 0.12, w: 3.9, h: 0.36,
      fontSize: 11, color: '555555', fontFace: 'Arial'
    });

    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 5.2, y: metricsY, w: 4.3, h: 0.6,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 1 },
      rectRadius: 0.05
    });
    slide.addText(row.right, {
      x: 5.4, y: metricsY + 0.12, w: 3.9, h: 0.36,
      fontSize: 11, color: '555555', fontFace: 'Arial'
    });
    metricsY += 0.75;
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 3.3, w: 9.0, h: 1.15,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_10_cost_vs_demand.png]', {
    x: 0.5, y: 3.8, w: 9.0, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 8: Operating Metrics');

  // Slide 9: Sensitivity Analysis
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('민감도 분석', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const sensitivity = [
    { factor: '연료 가격', impact: '영향도: 매우 높음 ⚠️', desc: '±10%: NPC ±$21.7M' },
    { factor: '셔틀 크기', impact: '영향도: 중간', desc: '1,000-3,000 m³ 범위' },
    { factor: '펌프 용량', impact: '영향도: 중간', desc: '1,200-2,000 m³/h 최적' },
    { factor: '수요 증가', impact: '영향도: 높음', desc: '셔틀 신규 투자 필요' },
    { factor: '냉각 비용', impact: '영향도: 낮음', desc: '2-3% of total cost' }
  ];

  let sensY = 1.0;
  sensitivity.forEach(s => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: sensY, w: 3.8, h: 0.55,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 1 },
      rectRadius: 0.05
    });
    slide.addText(s.factor, {
      x: 0.65, y: sensY + 0.05, w: 3.5, h: 0.15,
      fontSize: 10, bold: true, color: '2C3E50', fontFace: 'Arial'
    });
    slide.addText(s.impact, {
      x: 0.65, y: sensY + 0.22, w: 3.5, h: 0.14,
      fontSize: 9, color: 'E67E22', fontFace: 'Arial'
    });
    slide.addText(s.desc, {
      x: 0.65, y: sensY + 0.37, w: 3.5, h: 0.12,
      fontSize: 9, color: '999999', fontFace: 'Arial'
    });
    sensY += 0.62;
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.5, y: 1.0, w: 5.0, h: 3.55,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_11_tornado_diagram.png]', {
    x: 4.5, y: 2.3, w: 5.0, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 9: Sensitivity Analysis');

  // Slide 10: Roadmap
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('구축 로드맵 (2030-2050)', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const phases = [
    { year: 'Phase 1: 2030-2033', items: ['초기 인프라 구축', '셔틀 3-4척', '펌프 2,000 m³/h'], y: 1.0 },
    { year: 'Phase 2: 2034-2040', items: ['수요 대응 확대', '셔틀 10-12척'], y: 1.7 },
    { year: 'Phase 3: 2041-2050', items: ['대규모 운영', '셔틀 30-40척', '연간 2,900M ton'], y: 2.4 }
  ];

  phases.forEach(p => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: p.y, w: 3.8, h: 1.3,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 2 },
      rectRadius: 0.1
    });
    slide.addText(p.year, {
      x: 0.7, y: p.y + 0.1, w: 3.4, h: 0.25,
      fontSize: 11, bold: true, color: 'E67E22', fontFace: 'Arial'
    });
    let itemY = p.y + 0.4;
    p.items.forEach(item => {
      slide.addText('• ' + item, {
        x: 0.85, y: itemY, w: 3.2, h: 0.22,
        fontSize: 10, color: '555555', fontFace: 'Arial'
      });
      itemY += 0.25;
    });
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.5, y: 1.0, w: 5.0, h: 3.1,
    fill: { color: 'F0F0F0' },
    line: { color: 'CCCCCC', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('[이미지 자리: case1_08_year_shuttles.png]', {
    x: 4.5, y: 2.3, w: 5.0, h: 0.5,
    fontSize: 13, color: '999999', align: 'center', valign: 'middle', fontFace: 'Arial'
  });
  console.log('[OK] Slide 10: Roadmap');

  // Slide 11: Conclusion
  slide = pptx.addSlide();
  slide.background = { color: 'F8F9FA' };
  slide.addText('전략적 권고사항 및 결론', {
    x: 0.3, y: 0.2, w: 9.4, h: 0.5,
    fontSize: 28, bold: true, color: '2C3E50', fontFace: 'Arial'
  });

  const sections2 = [
    { title: 'Case 1 장점', items: ['부산항 내 단거리 운영 (2 nm)', '빠른 사이클 타임 (6.92시간)', '안정적이고 유연한 운영', '기존 부산항 인프라 활용'] },
    { title: 'Case 1 단점', items: ['저장탱크 CAPEX: $28.9M (중대)', '냉각 시스템 필수', '다중 트립 필요 (2회)', '높은 총 NPC ($217M)'] },
    { title: '운영 권장사항', items: ['펌프 크기: 1,200-2,000 m³/h', '셔틀 크기: 2,500 m³ (최적)', '4,000 m³ 이상 셔틀 회피', '단기 안정성, 장기 비용 부담'] }
  ];

  let secY = 1.0;
  sections2.forEach(sec => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y: secY, w: 9.0, h: 0.9,
      fill: { color: 'FFFFFF' },
      line: { color: '27AE60', width: 1 },
      rectRadius: 0.05
    });
    slide.addText(sec.title, {
      x: 0.7, y: secY + 0.08, w: 3, h: 0.22,
      fontSize: 11, bold: true, color: '2C3E50', fontFace: 'Arial'
    });

    let itemY = secY + 0.32;
    sec.items.forEach(item => {
      slide.addText('• ' + item, {
        x: 0.85, y: itemY, w: 8.7, h: 0.18,
        fontSize: 9, color: '555555', fontFace: 'Arial'
      });
      itemY += 0.19;
    });
    secY += 1.05;
  });

  // Final conclusion box
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 3.8, w: 9.0, h: 0.95,
    fill: { color: 'FFF8E1' },
    line: { color: 'E67E22', width: 2 },
    rectRadius: 0.1
  });
  slide.addText('최종 결론', {
    x: 0.7, y: 3.87, w: 8.6, h: 0.2,
    fontSize: 11, bold: true, color: '333333', fontFace: 'Arial'
  });
  slide.addText('Case 1은 부산항 중심의 운영이 필요한 경우 선택 가능하지만, 저장탱크로 인한 높은 초기 투자와 냉각 비용으로 인해 Case 2-2 (울산 루트)보다 38% 비싼 구조입니다. 운영의 유연성을 필요로 할 때만 권장됩니다.', {
    x: 0.7, y: 4.1, w: 8.6, h: 0.6,
    fontSize: 9, color: '333333', fontFace: 'Arial', valign: 'top'
  });
  console.log('[OK] Slide 11: Conclusion');

  // Save presentation
  const outputPath = 'C:\\code\\Green_Cor\\Case1_Busan_Storage_Presentation.pptx';
  await pptx.writeFile({ fileName: outputPath });
  console.log(`[OK] PPT 생성 완료: ${outputPath}`);
  console.log(`[INFO] 총 12장 슬라이드 생성 (타이틀 + 11장)\\n`);
}

createPresentation().catch(err => {
  console.error('[ERROR] PPT 생성 실패:', err.message);
  process.exit(1);
});
