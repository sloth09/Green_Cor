const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

// Load html2pptx module
const html2pptx = require('C:\\Users\\user\\.claude\\plugins\\marketplaces\\anthropic-agent-skills\\document-skills\\pptx\\scripts\\html2pptx.js');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Green Corridor Team';
  pptx.title = 'Case 1: Busan Port Ammonia Bunkering Optimization';

  const slidesDir = __dirname;
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

  console.log('[INFO] PPT 생성 시작...');

  for (const slide of slides) {
    const slidePath = path.join(slidesDir, slide);
    if (!fs.existsSync(slidePath)) {
      console.log(`[WARN] 파일 없음: ${slidePath}`);
      continue;
    }

    try {
      console.log(`[OK] 처리 중: ${slide}`);
      const { slide: newSlide, placeholders } = await html2pptx(slidePath, pptx);
      console.log(`[OK] 완료: ${slide} (placeholders: ${placeholders.length})`);
    } catch (error) {
      console.log(`[ERROR] ${slide}: ${error.message}`);
      // Continue with next slide even if one fails
    }
  }

  const outputPath = path.join(slidesDir, 'Case1_Busan_Storage_Presentation.pptx');
  await pptx.writeFile({ fileName: outputPath });
  console.log(`[OK] PPT 생성 완료: ${outputPath}`);
}

createPresentation().catch(err => {
  console.error('[ERROR] 프레젠테이션 생성 실패:', err);
  process.exit(1);
});
