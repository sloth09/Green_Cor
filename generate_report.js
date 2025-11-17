const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        AlignmentType, WidthType, BorderStyle, ShadingType, VerticalAlign, HeadingLevel,
        PageBreak, Header, Footer, PageNumber, LevelFormat } = require('docx');
const path = require('path');

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

function loadImage(filename) {
  const filepath = path.join(__dirname, 'results/figures', filename);
  return fs.readFileSync(filepath);
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "1f4788", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "1f4788", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "2e5c8a", font: "Arial" },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 1 }
      }
    ]
  },
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } }
      }]
    }]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT, spacing: { after: 100 },
          border: { bottom: { color: "1f4788", space: 1, style: BorderStyle.SINGLE, size: 6 } },
          children: [new TextRun({ text: "Green Corridor Ammonia Bunkering Optimization", size: 20, color: "666666" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 20, color: "666666" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 20, color: "666666" }),
            new TextRun({ text: " of ", size: 20, color: "666666" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 20, color: "666666" })
          ]
        })]
      })
    },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Green Corridor Ammonia Bunkering")] }),
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Infrastructure Optimization Report")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: "MILP Model Analysis & Results (2030-2050)", italics: true, size: 26 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: "November 2025", size: 22, color: "666666" })] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Executive Summary")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun("This report presents a comprehensive MILP optimization analysis for ammonia bunkering infrastructure at Busan Port over a 20-year planning horizon (2030-2050). The analysis evaluates 270 system configurations across three scenarios to minimize Net Present Cost (NPC).")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Key Findings")] }),

      new Table({
        columnWidths: [2340, 1560, 1560, 1560],
        margins: { top: 80, bottom: 80, left: 100, right: 100 },
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders: cellBorders, shading: { fill: "1f4788", type: ShadingType.CLEAR }, width: { size: 2340, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Case", bold: true, color: "FFFFFF" })] })] }),
              new TableCell({ borders: cellBorders, shading: { fill: "1f4788", type: ShadingType.CLEAR }, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Shuttle (m3)", bold: true, color: "FFFFFF" })] })] }),
              new TableCell({ borders: cellBorders, shading: { fill: "1f4788", type: ShadingType.CLEAR }, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Pump (m3/h)", bold: true, color: "FFFFFF" })] })] }),
              new TableCell({ borders: cellBorders, shading: { fill: "1f4788", type: ShadingType.CLEAR }, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "NPC ($M)", bold: true, color: "FFFFFF" })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2340, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Case 1: Busan")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("2,500")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("2,000")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "153.5", bold: true })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2340, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Case 2-1: Yeosu")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("5,000")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("2,000")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "158.2", bold: true })] })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ borders: cellBorders, width: { size: 2340, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun("Case 2-2: Ulsan")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("5,000")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun("2,000")] })] }),
              new TableCell({ borders: cellBorders, width: { size: 1560, type: WidthType.DXA }, children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "94.9", bold: true, color: "008000" })] })] })
            ]
          })
        ]
      }),

      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Strategic Recommendation: ", bold: true }), new TextRun("Case 2-2 (Ulsan) offers 38% cost advantage over Case 1, representing the most cost-effective bunkering solution.")] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. Introduction")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Background")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun("The maritime industry is transforming towards decarbonization. Ammonia has emerged as a viable zero-carbon fuel for deep-sea shipping. This study optimizes ammonia bunkering infrastructure at Busan Port, a critical hub in the Green Shipping Corridor.")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Objectives")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Determine optimal fleet composition and port infrastructure")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Minimize Net Present Cost over 20-year horizon")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Compare three operational scenarios")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 240 }, children: [new TextRun("Provide actionable infrastructure investment recommendations")] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. Methodology")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("MILP Model Framework")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun("Mixed Integer Linear Programming (MILP) solves: Minimize NPV = Sum[DISC(t) x (CAPEX(t) + OPEX(t))]")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun("Subject to demand satisfaction, operational capacity, and infrastructure constraints.")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Key Parameters")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Time Period: ", bold: true }), new TextRun("2030-2050 (20 years)")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Discount Rate: ", bold: true }), new TextRun("7%")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Fleet Growth: ", bold: true }), new TextRun("50 vessels (2030) to 500 vessels (2050)")] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "Ammonia Price: ", bold: true }), new TextRun("$600/ton baseline")] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. System Scenarios")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Case 1: Busan Port Storage")] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("Port-side 35,000-ton storage tank with shuttle-to-ship bunkering. Absorbs demand variability and enables economies of scale.")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Case 2-1: Yeosu Production")] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("Long-distance (86 nm, 5.73 hours) shuttle transport from Yeosu ammonia facility. Requires larger vessels.")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Case 2-2: Ulsan Production")] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("Short-distance (25 nm, 1.67 hours) shuttle transport from Ulsan. Minimizes operational costs.")] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. Optimization Results")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Figure 1: NPC Landscape")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new ImageRun({ type: "png", data: loadImage("01_npc_heatmaps.png"), transformation: { width: 520, height: 160 }, altText: { title: "NPC", description: "NPC heatmaps", name: "fig1" } })] }),

      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Figure 2: Cost Breakdown")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new ImageRun({ type: "png", data: loadImage("02_top10_breakdown.png"), transformation: { width: 520, height: 180 }, altText: { title: "Cost", description: "Cost breakdown", name: "fig2" } })] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Figure 3: Case Comparison")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new ImageRun({ type: "png", data: loadImage("03_case_comparison.png"), transformation: { width: 480, height: 340 }, altText: { title: "Comparison", description: "Case comparison", name: "fig3" } })] }),

      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Figure 4: NPC Distribution")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new ImageRun({ type: "png", data: loadImage("04_npc_distribution.png"), transformation: { width: 520, height: 160 }, altText: { title: "Distribution", description: "Distribution", name: "fig4" } })] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Figure 5: Sensitivity Analysis")] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new ImageRun({ type: "png", data: loadImage("05_shuttle_sensitivity.png"), transformation: { width: 520, height: 160 }, altText: { title: "Sensitivity", description: "Sensitivity", name: "fig5" } })] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("5. Detailed Analysis")] }),
      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Case 1: Busan Storage")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Configuration: ", bold: true }), new TextRun("2,500 m3 shuttle, 2,000 m3/h pump")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Total NPC: $153.5M USD", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Shuttle CAPEX: $37.91M (24.7%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Bunkering CAPEX: $4.27M (2.8%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Tank CAPEX: $42.53M (27.7%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 240 }, children: [new TextRun("Total OPEX: $68.67M (44.8%)")] }),

      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Case 2-1: Yeosu")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Configuration: ", bold: true }), new TextRun("5,000 m3 shuttle, 2,000 m3/h pump")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Total NPC: $158.2M USD ", bold: true }), new TextRun("(+3.0% vs Case 1)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Shuttle CAPEX: $68.94M (43.6%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Bunkering CAPEX: $5.45M (3.4%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 240 }, children: [new TextRun("Total OPEX: $83.81M (53.0%)")] }),

      new Paragraph({ spacing: { after: 120 }, heading: HeadingLevel.HEADING_2, children: [new TextRun("Case 2-2: Ulsan (OPTIMAL)")] }),
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Configuration: ", bold: true }), new TextRun("5,000 m3 shuttle, 2,000 m3/h pump")] }),
      new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Total NPC: $94.9M USD ", bold: true, color: "008000" }), new TextRun({ text: "(-38.2% vs Case 1)", bold: true, color: "008000" })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Shuttle CAPEX: $47.67M (50.2%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Bunkering CAPEX: $3.77M (4.0%)")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 240 }, children: [new TextRun("Total OPEX: $43.46M (45.8%)")] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("6. Key Insights")] }),
      new Paragraph({ spacing: { after: 120 }, numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "Distance Critical: ", bold: true }), new TextRun("Short-distance operations reduce NPC by 38%")] }),
      new Paragraph({ spacing: { after: 120 }, numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "Shuttle Sizing: ", bold: true }), new TextRun("Larger shuttles (5,000 m3) optimal for inter-facility transport")] }),
      new Paragraph({ spacing: { after: 120 }, numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "CAPEX Dominance: ", bold: true }), new TextRun("Infrastructure costs drive 70-80% of NPC")] }),
      new Paragraph({ spacing: { after: 240 }, numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: "Operational Efficiency: ", bold: true }), new TextRun("Optimized pump sizing (2,000 m3/h) balances costs")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("7. Recommendations")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Prioritize Ulsan corridor as primary supply route")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Invest in 5,000 m3 shuttle vessels")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Coordinate with ammonia producers for integrated logistics")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 240 }, children: [new TextRun("Implement demand-responsive infrastructure sizing")] }),

      new Paragraph({ children: [new PageBreak()] }),

      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("8. Conclusion")] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("This MILP optimization study demonstrates that short-distance ammonia supply chains significantly outperform port-based infrastructure models. The 38% cost advantage of Case 2-2 indicates that integrated logistics coordination with production facilities offers superior economic returns.")] }),
      new Paragraph({ spacing: { after: 240 }, children: [new TextRun("Infrastructure planners should prioritize the Ulsan route, standardize on 5,000 m3 shuttle vessels, and implement flexible pump systems to accommodate demand growth through 2050.")] }),

      new Paragraph({ spacing: { before: 240 }, children: [new TextRun({ text: "---", bold: true })] }),
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Report Generated: November 2025", italics: true, size: 20, color: "666666" })] }),
      new Paragraph({ children: [new TextRun({ text: "Green Corridor MILP Optimization Model v2.0", italics: true, size: 20, color: "666666" })] })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("results/Green_Corridor_Report.docx", buffer);
  console.log("Word report created successfully: results/Green_Corridor_Report.docx");
});
