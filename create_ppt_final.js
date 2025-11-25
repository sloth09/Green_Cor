const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Green Corridor Team';
  pptx.title = 'Case 1: Busan Port Ammonia Bunkering Optimization';

  const slidesDir = path.join(__dirname, 'slides_correct');
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
  console.log(`[INFO] 슬라이드 디렉토리: ${slidesDir}`);

  // HTML to PPTX 변환을 위한 html2pptx 로드
  let html2pptx;
  try {
    html2pptx = require('C:\\Users\\user\\.claude\\plugins\\marketplaces\\anthropic-agent-skills\\document-skills\\pptx\\scripts\\html2pptx.js');
    console.log('[OK] html2pptx 모듈 로드 완료');
  } catch (err) {
    console.log(`[ERROR] html2pptx 로드 실패: ${err.message}`);
    return;
  }

  let slideCount = 0;
  for (const slide of slides) {
    const slidePath = path.join(slidesDir, slide);

    if (!fs.existsSync(slidePath)) {
      console.log(`[WARN] 파일 없음: ${slide}`);
      continue;
    }

    try {
      console.log(`[${slideCount + 1}/${slides.length}] 처리 중: ${slide}`);
      const result = await html2pptx(slidePath, pptx);
      console.log(`[OK] 완료: ${slide}`);
      slideCount++;
    } catch (error) {
      console.log(`[ERROR] ${slide}: ${error.message.split('\n')[0]}`);
      // Continue with next slide even if one fails
    }
  }

  const outputPath = path.join(__dirname, 'Case1_Presentation_Final.pptx');

  try {
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\n[OK] PPT 생성 완료!`);
    console.log(`[OK] 파일: ${outputPath}`);
    console.log(`[OK] 총 슬라이드: ${slideCount}장`);

    // 파일 크기 확인
    const stats = fs.statSync(outputPath);
    console.log(`[OK] 파일 크기: ${(stats.size / 1024).toFixed(1)} KB`);
  } catch (err) {
    console.error(`[ERROR] 파일 저장 실패: ${err.message}`);
  }
}

createPresentation().catch(err => {
  console.error('[FATAL] 프레젠테이션 생성 실패:', err.message);
  process.exit(1);
});
