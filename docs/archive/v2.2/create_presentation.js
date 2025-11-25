const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Green Corridor Research Team';
    pptx.title = 'Green Corridor Ammonia Bunkering Optimization';

    const figuresDir = './results/figures';
    const primaryColor = '1f4788';
    const secondaryColor = '2e5c8a';
    const accentColor = '28a745';

    console.log('[INFO] Creating presentation slides...');

    // Slide 1: Title
    console.log('[SLIDE 1/18] Title');
    let slide = pptx.addSlide();
    slide.background = { color: primaryColor };
    slide.addText('Green Corridor', {
        x: 0.5, y: 1.5, w: 9, h: 0.6,
        fontSize: 54, bold: true, color: 'FFFFFF', align: 'center'
    });
    slide.addText('Ammonia Bunkering Optimization', {
        x: 0.5, y: 2.2, w: 9, h: 0.5,
        fontSize: 28, color: 'FFFFFF', align: 'center'
    });
    slide.addText('MILP Model Analysis & Results', {
        x: 0.5, y: 2.9, w: 9, h: 0.4,
        fontSize: 18, color: 'FFFFFF', align: 'center'
    });

    // Slide 2: Executive Summary
    console.log('[SLIDE 2/18] Executive Summary');
    slide = pptx.addSlide();
    slide.addText('Executive Summary', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    const summaryTable = [
        [{ text: 'Metric', options: { fill: { color: primaryColor }, color: 'FFFFFF', bold: true } },
         { text: 'Value', options: { fill: { color: primaryColor }, color: 'FFFFFF', bold: true } }],
        ['Operational Scenarios', '3 cases'],
        ['Feasible Solutions', '270 total'],
        ['Case 1 Optimal NPC', '$153.5M'],
        ['Best Case (Ulsan)', '$94.9M (-38%)'],
        ['Optimal Shuttle Size', '2,500-5,000 m³']
    ];
    slide.addTable(summaryTable, {
        x: 0.8, y: 1.0, w: 8.4, h: 2.8,
        border: { pt: 1, color: 'CCCCCC' },
        fontSize: 13, align: 'left'
    });

    // Slide 3: Case 1 - Busan
    console.log('[SLIDE 3/18] Case 1: Busan');
    slide = pptx.addSlide();
    slide.addText('Case 1: Busan Port Storage', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    slide.addText('Storage-based bunkering at Busan Port (intra-port transfer)', {
        x: 0.5, y: 0.8, w: 9, h: 0.3, fontSize: 14, color: '666666'
    });
    const case1Content = [
        'Optimal Configuration:',
        '• Shuttle Size: 2,500 m³',
        '• Pump Capacity: 2,000 m³/h',
        '• NPC (20 years): $153.5M',
        '',
        'Characteristics:',
        '• Large storage tank (35,000 tons)',
        '• 2.0 hour intra-port travel time',
        '• Higher storage cost burden'
    ];
    let y = 1.3;
    for (const line of case1Content) {
        slide.addText(line, {
            x: 1.0, y: y, w: 8, h: 0.25,
            fontSize: line.startsWith('•') ? 12 : (line === '' ? 0.1 : 13),
            bold: line.endsWith(':'),
            color: line === '' ? 'FFFFFF' : '333333'
        });
        y += 0.28;
    }

    // Slide 4: Case 2-1 - Yeosu
    console.log('[SLIDE 4/18] Case 2-1: Yeosu');
    slide = pptx.addSlide();
    slide.addText('Case 2-1: Yeosu Route', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    slide.addText('Long-distance shuttle route: Yeosu → Busan (86 nm)', {
        x: 0.5, y: 0.8, w: 9, h: 0.3, fontSize: 14, color: '666666'
    });
    const case2_1Content = [
        'Optimal Configuration:',
        '• Shuttle Size: 5,000 m³',
        '• Pump Capacity: 2,000 m³/h',
        '• NPC (20 years): $158.2M',
        '',
        'Performance vs Case 1:',
        '• +3.1% more expensive',
        '• Travel Time: 5.73 hours',
        '• No storage cost (26% savings)',
        '• Higher fuel consumption'
    ];
    y = 1.3;
    for (const line of case2_1Content) {
        slide.addText(line, {
            x: 1.0, y: y, w: 8, h: 0.25,
            fontSize: line.startsWith('•') ? 12 : (line === '' ? 0.1 : 13),
            bold: line.endsWith(':'),
            color: line === '' ? 'FFFFFF' : '333333'
        });
        y += 0.28;
    }

    // Slide 5: Case 2-2 - Ulsan (OPTIMAL)
    console.log('[SLIDE 5/18] Case 2-2: Ulsan');
    slide = pptx.addSlide();
    slide.background = { color: 'F0FDF4' };
    slide.addText('Case 2-2: Ulsan Route', {
        x: 0.5, y: 0.3, w: 8.2, h: 0.4,
        fontSize: 32, bold: true, color: accentColor
    });
    slide.addText('OPTIMAL', {
        x: 8.2, y: 0.3, w: 1.3, h: 0.4,
        fontSize: 16, bold: true, color: 'FFFFFF',
        fill: { color: accentColor }, align: 'center'
    });
    slide.addText('Short-distance shuttle route: Ulsan → Busan (25 nm)', {
        x: 0.5, y: 0.8, w: 9, h: 0.3, fontSize: 14, color: '666666'
    });
    const case2_2Content = [
        'Optimal Configuration:',
        '• Shuttle Size: 5,000 m³',
        '• Pump Capacity: 2,000 m³/h',
        '• NPC (20 years): $94.9M',
        '',
        'Performance vs Case 1:',
        '✓ -38.2% cost reduction (BEST OPTION)',
        '• Travel Time: 1.67 hours (shortest)',
        '• 33% lower fuel consumption vs Yeosu',
        '• Lowest total NPC'
    ];
    y = 1.3;
    for (const line of case2_2Content) {
        slide.addText(line, {
            x: 1.0, y: y, w: 8, h: 0.25,
            fontSize: line.startsWith('•') || line.startsWith('✓') ? 12 : (line === '' ? 0.1 : 13),
            bold: line.includes('BEST') || line.endsWith(':'),
            color: line.includes('38.2%') ? accentColor : '333333'
        });
        y += 0.28;
    }

    // Slides 6-10: Figures
    const figures = [
        { num: 6, name: 'NPC Heatmaps', file: '01_npc_heatmaps.png', title: 'NPC Heatmaps: Shuttle Size vs Pump Flow Rate' },
        { num: 7, name: 'Cost Breakdown', file: '02_top10_breakdown.png', title: 'Top 10 Cost Breakdown by Component' },
        { num: 8, name: 'Case Comparison', file: '03_case_comparison.png', title: 'Case Comparison: NPC, Equipment, Cost' },
        { num: 9, name: 'NPC Distribution', file: '04_npc_distribution.png', title: 'NPC Distribution Analysis' },
        { num: 10, name: 'Sensitivity', file: '05_shuttle_sensitivity.png', title: 'Sensitivity Analysis: Shuttle Size Impact' }
    ];

    for (const fig of figures) {
        console.log(`[SLIDE ${fig.num}/18] ${fig.name}`);
        slide = pptx.addSlide();
        slide.addText(fig.title, {
            x: 0.5, y: 0.3, w: 9, h: 0.4,
            fontSize: 32, bold: true, color: primaryColor
        });
        const figPath = path.join(figuresDir, fig.file);
        if (fs.existsSync(figPath)) {
            slide.addImage({ path: figPath, x: 0.3, y: 0.95, w: 9.4, h: 3.3 });
        } else {
            slide.addText(`[Figure not found: ${fig.file}]`, {
                x: 1, y: 1.5, w: 8, h: 1, fontSize: 14, color: 'CC0000'
            });
        }
    }

    // Slide 11: Key Findings
    console.log('[SLIDE 11/18] Key Findings');
    slide = pptx.addSlide();
    slide.addText('Key Findings', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    const findings = [
        { title: 'Ulsan Route Optimal', text: '38.2% cost reduction vs Busan ($94.9M vs $153.5M)' },
        { title: 'Storage Tank Burden', text: 'Tank CAPEX ($28.9M) limits Case 1 competitiveness' },
        { title: 'Equipment Sizing', text: '5,000 m³ shuttles optimal for long-distance routes' },
        { title: 'Distance Critical', text: '25 nm route reduces fuel by 33% vs 86 nm route' }
    ];
    y = 1.0;
    for (const f of findings) {
        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: 0.8, y: y, w: 8.4, h: 0.65,
            fill: { color: 'F5F5F5' },
            line: { color: primaryColor, width: 2 }
        });
        slide.addText(f.title, {
            x: 1.1, y: y + 0.05, w: 7.8, h: 0.25,
            fontSize: 13, bold: true, color: primaryColor
        });
        slide.addText(f.text, {
            x: 1.1, y: y + 0.32, w: 7.8, h: 0.25,
            fontSize: 11, color: '333333'
        });
        y += 0.75;
    }

    // Slide 12: Cost Structure Table
    console.log('[SLIDE 12/18] Cost Structure');
    slide = pptx.addSlide();
    slide.addText('NPC Breakdown by Component (20-Year Horizon)', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    const costTable = [
        [{ text: 'Cost Component', options: { fill: { color: primaryColor }, color: 'FFFFFF', bold: true } },
         { text: 'Case 1', options: { fill: { color: primaryColor }, color: 'FFFFFF', bold: true } },
         { text: 'Case 2-1', options: { fill: { color: primaryColor }, color: 'FFFFFF', bold: true } },
         { text: 'Case 2-2', options: { fill: { color: primaryColor }, color: 'FFFFFF', bold: true } }],
        [{ text: 'Total NPC', options: { bold: true } }, '$153.5M', '$158.2M', '$94.9M'],
        ['Shuttle CAPEX', '$24.8M', '$24.1M', '$24.1M'],
        ['Bunkering CAPEX', '$9.8M', '$9.8M', '$9.8M'],
        ['Tank CAPEX', '$28.9M', '$0', '$0'],
        ['Total OPEX', '$90.0M', '$124.3M', '$61.0M']
    ];
    slide.addTable(costTable, {
        x: 0.8, y: 0.9, w: 8.4, h: 2.5,
        border: { pt: 1, color: 'CCCCCC' },
        fontSize: 11, align: 'center'
    });

    // Slide 13: Economic Analysis
    console.log('[SLIDE 13/18] Economic Analysis');
    slide = pptx.addSlide();
    slide.addText('Economic Analysis & Equipment Requirements', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    const metrics = [
        { label: 'Case 1 Initial Shuttles', value: '6' },
        { label: 'Case 2-1 Initial Shuttles', value: '8' },
        { label: 'Case 2-2 Initial Shuttles', value: '8' },
        { label: 'Cost per Tonne (Case 1)', value: '~$45' },
        { label: 'Cost per Tonne (Case 2-2)', value: '~$28' }
    ];
    y = 1.1;
    for (const m of metrics) {
        slide.addText(m.label, {
            x: 1.0, y: y, w: 5.5, h: 0.35,
            fontSize: 12, color: '333333'
        });
        slide.addText(m.value, {
            x: 6.8, y: y, w: 2.2, h: 0.35,
            fontSize: 13, bold: true, color: primaryColor, align: 'center',
            fill: { color: 'F5F5F5' }
        });
        y += 0.48;
    }
    slide.addText('Ulsan route fuel consumption 33% lower due to shorter distance (25 nm vs 86 nm)', {
        x: 1.0, y: 3.5, w: 8, h: 0.6,
        fontSize: 12, italic: true, color: '666666'
    });

    // Slide 14: Recommendations
    console.log('[SLIDE 14/18] Recommendations');
    slide = pptx.addSlide();
    slide.background = { color: 'F0FDF4' };
    slide.addText('Strategic Recommendations', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: accentColor
    });
    const recs = [
        '1. Prioritize Ulsan Route: Deploy infrastructure toward Case 2-2 for 38% cost savings',
        '2. Optimize Fleet: Use 5,000 m³ shuttles for long-distance, 2,500 m³ for storage-based',
        '3. Reassess Storage: High tank CAPEX ($28.9M) limits Case 1 competitiveness',
        '4. Phased Deployment: Start with 6-8 shuttles in 2030, grow 10% annually'
    ];
    y = 1.1;
    for (const rec of recs) {
        slide.addText(rec, {
            x: 1.0, y: y, w: 8, h: 0.45,
            fontSize: 12, color: '333333',
            valign: 'top'
        });
        y += 0.55;
    }

    // Slide 15: Implementation Roadmap
    console.log('[SLIDE 15/18] Implementation Roadmap');
    slide = pptx.addSlide();
    slide.addText('Implementation Roadmap', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    const phases = [
        { year: '2030', title: 'Foundation', desc: '6-8 shuttles, 35 vessels' },
        { year: '2035', title: 'Growth', desc: '10-12 shuttles, 100+ vessels' },
        { year: '2040', title: 'Scaling', desc: 'Optimize efficiency, 200+ vessels' },
        { year: '2050', title: 'Maturity', desc: '500 vessels, integrated supply chain' }
    ];
    y = 1.0;
    for (const p of phases) {
        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: 0.8, y: y, w: 2, h: 0.55,
            fill: { color: primaryColor },
            line: { color: primaryColor }
        });
        slide.addText(p.year, {
            x: 0.8, y: y + 0.08, w: 2, h: 0.4,
            fontSize: 14, bold: true, color: 'FFFFFF', align: 'center'
        });
        slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
            x: 2.9, y: y, w: 6.3, h: 0.55,
            fill: { color: 'F5F5F5' },
            line: { color: primaryColor, width: 1 }
        });
        slide.addText(`${p.title}: ${p.desc}`, {
            x: 3.1, y: y + 0.08, w: 6, h: 0.4,
            fontSize: 12, color: '333333', valign: 'middle'
        });
        y += 0.68;
    }

    // Slide 16: Methodology
    console.log('[SLIDE 16/18] Methodology');
    slide = pptx.addSlide();
    slide.addText('Methodology Overview', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: primaryColor
    });
    const methods = [
        { title: 'Optimization Model', text: 'MILP (Mixed-Integer Linear Programming)' },
        { title: 'Objective', text: 'Minimize total Net Present Cost across 2030-2050' },
        { title: 'Decision Variables', text: 'Fleet size, shuttle/pump specifications, bunkering cycles' },
        { title: 'Cost Components', text: 'CAPEX (vessels, equipment, storage), OPEX (fuel, maintenance, cooling)' },
        { title: 'Discount Rate', text: '7% annual for NPV calculations' },
        { title: 'Solver', text: 'CBC (Coin-or Branch and Cut) via PuLP with <0.1% optimality gap' }
    ];
    y = 1.0;
    for (const m of methods) {
        slide.addText(m.title + ':', {
            x: 1.0, y: y, w: 2.5, h: 0.25,
            fontSize: 12, bold: true, color: primaryColor
        });
        slide.addText(m.text, {
            x: 3.6, y: y, w: 5.4, h: 0.25,
            fontSize: 11, color: '333333'
        });
        y += 0.35;
    }

    // Slide 17: Conclusion
    console.log('[SLIDE 17/18] Conclusion');
    slide = pptx.addSlide();
    slide.background = { color: 'F0FDF4' };
    slide.addText('Conclusion', {
        x: 0.5, y: 0.3, w: 9, h: 0.4,
        fontSize: 32, bold: true, color: accentColor
    });
    const conclusions = [
        'Ulsan Route (Case 2-2) is the Economically Optimal Solution',
        'Achieves $94.9M NPC over 20 years—38.2% cost reduction vs Busan storage scenario',
        '',
        'Strategic Implications',
        'Development should focus on Ulsan infrastructure with 5,000 m³ shuttles and 2,000 m³/h pumps',
        'to serve Green Corridor vessels economically through 2050',
        '',
        'Next Steps',
        'Proceed with detailed feasibility analysis for Ulsan infrastructure, port coordination, and phased fleet deployment'
    ];
    y = 1.0;
    for (const c of conclusions) {
        const size = c === '' ? 0.15 : (c.includes('Implications') || c.includes('Next Steps') ? 13 :
                           (c.includes('Ulsan Route') || c.includes('Strategic') || c.includes('Next') ? 12 : 11));
        slide.addText(c, {
            x: 1.0, y: y, w: 8, h: size === 12 ? 0.3 : (size === 13 ? 0.35 : 0.25),
            fontSize: size, bold: c.includes('Optimal') || c.includes('Implications') || c.includes('Next'),
            color: c.includes('Ulsan Route') || c.includes('38.2%') ? accentColor : '333333'
        });
        y += (size === 12 ? 0.38 : (size === 13 ? 0.43 : 0.3));
    }

    // Slide 18: Q&A
    console.log('[SLIDE 18/18] Q&A');
    slide = pptx.addSlide();
    slide.background = { color: primaryColor };
    slide.addText('Questions?', {
        x: 0.5, y: 1.5, w: 9, h: 0.6,
        fontSize: 56, bold: true, color: 'FFFFFF', align: 'center'
    });
    slide.addText('Green Corridor Ammonia Bunkering Optimization', {
        x: 0.5, y: 2.4, w: 9, h: 0.4,
        fontSize: 20, color: 'FFFFFF', align: 'center'
    });
    slide.addText('Infrastructure Planning 2030-2050', {
        x: 0.5, y: 3.0, w: 9, h: 0.3,
        fontSize: 14, color: 'FFFFFF', align: 'center', opacity: 0.9
    });

    // Save presentation
    const outputPath = path.join('./results', 'Green_Corridor_Presentation.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\n[SUCCESS] Presentation created: ${outputPath}`);
    console.log(`[SUCCESS] 18 slides with embedded figures and analysis`);
}

createPresentation().catch(err => {
    console.error('[ERROR]', err.message);
    process.exit(1);
});
