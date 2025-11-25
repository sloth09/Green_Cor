const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Green Corridor Team';
  pptx.title = 'Case 1: Busan Port Ammonia Bunkering Optimization';

  const slidesDir = path.join(__dirname, 'slides_simple');
  const slides = [
    'slide_title.html',
    'slide_01_summary.html',
    'slide_02_scenario.html',
    'slide_03_model.html',
    'slide_04_heatmap.html',
    'slide_05_top10.html',
    'slide_06_cycletime.html',
    'slide_07_costanalysis.html',
    'slide_08_metrics.html',
    'slide_09_sensitivity.html',
    'slide_10_roadmap.html',
    'slide_11_conclusion.html'
  ];

  console.log('[INFO] 최종 PPT 생성 시작...');

  let html2pptx;
  try {
    html2pptx = require('C:\\Users\\user\\.claude\\plugins\\marketplaces\\anthropic-agent-skills\\document-skills\\pptx\\scripts\\html2pptx.js');
  } catch (err) {
    console.error(`[ERROR] html2pptx 로드 실패: ${err.message}`);
    return;
  }

  let slideCount = 0;
  for (let i = 0; i < slides.length; i++) {
    const slide = slides[i];
    const slidePath = path.join(slidesDir, slide);

    if (!fs.existsSync(slidePath)) {
      console.log(`[WARN] 파일 없음: ${slide}`);
      continue;
    }

    try {
      console.log(`[${i + 1}/${slides.length}] ${slide.replace('slide_', '').replace('.html', '')}`);
      const result = await html2pptx(slidePath, pptx);
      slideCount++;
    } catch (error) {
      console.log(`  → 오류 있음 (계속 진행)`);
    }
  }

  const outputPath = path.join(__dirname, 'Case1_Presentation_Final.pptx');

  try {
    await pptx.writeFile({ fileName: outputPath });

    const stats = fs.statSync(outputPath);
    const sizeMB = (stats.size / 1024 / 1024).toFixed(2);
    const sizeKB = (stats.size / 1024).toFixed(1);

    console.log(`\n=== 완료 ===`);
    console.log(`[OK] 파일: ${outputPath}`);
    console.log(`[OK] 슬라이드: ${slideCount}장`);
    console.log(`[OK] 크기: ${sizeKB} KB`);
  } catch (err) {
    console.error(`[ERROR] 파일 저장 실패: ${err.message}`);
  }
}

createPresentation().catch(err => {
  console.error('[FATAL]:', err.message);
  process.exit(1);
});
