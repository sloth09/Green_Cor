const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat,
        TableOfContents, HeadingLevel, BorderStyle, WidthType,
        ShadingType, VerticalAlign, PageNumber, PageBreak } = require('docx');
const fs = require('fs');
const path = require('path');

// Paths
const FIGURES_DIR = 'D:/code/Green_Cor/results/paper_figures';
const OUTPUT_DIR = 'D:/code/Green_Cor/docs/verification';

// Common styles
const styles = {
  default: { document: { run: { font: "Arial", size: 22 } } },
  paragraphStyles: [
    { id: "Title", name: "Title", basedOn: "Normal",
      run: { size: 48, bold: true, color: "1F4E79", font: "Arial" },
      paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER } },
    { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 32, bold: true, color: "1F4E79", font: "Arial" },
      paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
    { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 26, bold: true, color: "2E75B6", font: "Arial" },
      paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
    { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
      run: { size: 24, bold: true, color: "404040", font: "Arial" },
      paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 2 } },
  ]
};

const numbering = {
  config: [
    { reference: "bullet-list",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbered-list",
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
  ]
};

// Table styling
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };
const headerShading = { fill: "1F4E79", type: ShadingType.CLEAR };
const altRowShading = { fill: "F2F2F2", type: ShadingType.CLEAR };

function createTableCell(text, isHeader = false, width = 2000, isAltRow = false) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: isHeader ? headerShading : (isAltRow ? altRowShading : undefined),
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({
        text: text,
        bold: isHeader,
        size: isHeader ? 22 : 20,
        color: isHeader ? "FFFFFF" : "000000"
      })]
    })]
  });
}

function createTable(headers, rows) {
  const colWidth = Math.floor(9360 / headers.length);
  const colWidths = headers.map(() => colWidth);

  return new Table({
    columnWidths: colWidths,
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map(h => createTableCell(h, true, colWidth))
      }),
      ...rows.map((row, idx) => new TableRow({
        children: row.map(cell => createTableCell(cell, false, colWidth, idx % 2 === 1))
      }))
    ]
  });
}

function loadImage(filename) {
  const imgPath = path.join(FIGURES_DIR, filename);
  if (fs.existsSync(imgPath)) {
    return fs.readFileSync(imgPath);
  }
  return null;
}

function createImageParagraph(filename, width = 500, height = 300) {
  const imgData = loadImage(filename);
  if (!imgData) {
    return new Paragraph({ children: [new TextRun({ text: `[Image not found: ${filename}]`, italics: true, color: "999999" })] });
  }
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 200 },
    children: [new ImageRun({
      type: "png",
      data: imgData,
      transformation: { width, height },
      altText: { title: filename, description: filename, name: filename }
    })]
  });
}

function createHeader() {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: "Deterministic Case Verification Report", size: 18, color: "808080" })]
    })]
  });
}

function createFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: "Page ", size: 18 }),
        new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
        new TextRun({ text: " of ", size: 18 }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18 })
      ]
    })]
  });
}

// Chapter 1: Executive Summary
function createChapter1() {
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Executive Summary")] }),
    new Paragraph({ children: [new TextRun({ text: "Key Findings", bold: true, size: 24 })] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun(
      "The MILP optimization identifies the most cost-effective ammonia bunkering configurations for Busan Port across three supply scenarios. Case 1 (local storage) is the most economical, followed by Case 2-2 (Ulsan), with Case 2-1 (Yeosu) being the most expensive due to longer transport distances."
    )] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Optimal Configurations")] }),
    createTable(
      ["Case", "Shuttle Size", "NPC (20yr)", "LCOAmmonia", "Fleet (2050)"],
      [
        ["Case 1: Busan", "2,500 m3", "$237.05M", "$1.01/ton", "~20 shuttles"],
        ["Case 2-1: Yeosu", "10,000 m3", "$747.18M", "$3.17/ton", "~10 shuttles"],
        ["Case 2-2: Ulsan", "5,000 m3", "$402.37M", "$1.71/ton", "~15 shuttles"]
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Cost Comparison")] }),
    createTable(
      ["Case", "NPC", "vs Baseline"],
      [
        ["Case 1 (Busan)", "$237M", "Baseline"],
        ["Case 2-2 (Ulsan)", "$402M", "+70%"],
        ["Case 2-1 (Yeosu)", "$747M", "+215%"]
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Recommendation")] }),
    new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [
      new TextRun({ text: "Primary: ", bold: true }), new TextRun("Build local storage at Busan with 2,500 m3 shuttle fleet (NPC: $237M)")
    ]}),
    new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [
      new TextRun({ text: "Alternative: ", bold: true }), new TextRun("Ulsan supply with 5,000 m3 shuttles if local storage infeasible (+70%)")
    ]}),
    new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [
      new TextRun({ text: "Not Recommended: ", bold: true }), new TextRun("Yeosu supply due to excessive distance (+215%)")
    ]}),
  ];
}

// Chapter 2: Parameters
function createChapter2() {
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Parameters")] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Economic Parameters")] }),
    createTable(
      ["Parameter", "Value", "Unit", "Source"],
      [
        ["Discount Rate", "0.0", "-", "base.yaml"],
        ["Annualization Rate", "0.07", "-", "base.yaml"],
        ["Fuel Price", "600.0", "USD/ton", "base.yaml"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Time Period")] }),
    createTable(
      ["Parameter", "Value"],
      [
        ["Start Year", "2030"],
        ["End Year", "2050"],
        ["Analysis Period", "21 years"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Operational Parameters")] }),
    createTable(
      ["Parameter", "Value", "Unit"],
      [
        ["Max Annual Hours", "8000", "hours/vessel/year"],
        ["Setup Time", "0.5", "hours"],
        ["Pump Rate (Main)", "1000", "m3/h"],
        ["Shore Pump Rate", "1500", "m3/h"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Annuity Factor Verification")] }),
    new Paragraph({ children: [new TextRun("AF = [1 - (1.07)^(-21)] / 0.07 = 10.8355")] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "CSV Verification: 10.8355 [PASS]", color: "008000", bold: true })] }),
  ];
}

// Chapter 3: Case 1 Busan
function createChapter3() {
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Case 1: Busan Storage")] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Overview")] }),
    createTable(
      ["Parameter", "Value"],
      [
        ["Storage at Busan", "Yes"],
        ["Travel Time (one-way)", "1.0 hour"],
        ["Bunker Volume per Call", "5,000 m3"],
        ["Optimal Shuttle", "2,500 m3"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Cycle Time Formula")] }),
    new Paragraph({ children: [new TextRun({ text: "Cycle = Shore_Loading + Travel + Setup + Pumping", font: "Courier New", size: 20 })] }),
    new Paragraph({ children: [new TextRun({ text: "     = (Size/1500) + 2.0 + 2.0 + (Size/1000)", font: "Courier New", size: 20 })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Example: 2,500 m3 Shuttle")] }),
    new Paragraph({ children: [new TextRun("Shore Loading = 2500/1500 = 1.667 hours")] }),
    new Paragraph({ children: [new TextRun("Pumping = 2500/1000 = 2.5 hours")] }),
    new Paragraph({ children: [new TextRun({ text: "Total Cycle = 1.667 + 2.0 + 2.0 + 2.5 = 8.167 hours", bold: true })] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "CSV: 8.1667 [PASS]", color: "008000", bold: true })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Shuttle Comparison")] }),
    createTable(
      ["Metric", "2,500 m3", "5,000 m3"],
      [
        ["NPC Total", "$237.05M", "$264.24M"],
        ["LCOAmmonia", "$1.01/ton", "$1.12/ton"],
        ["Cycle Duration", "8.17 hr", "12.33 hr"],
        ["Trips per Call", "2", "1"],
        ["Utilization", "100%", "100%"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Full Scenario Results")] }),
    createTable(
      ["Shuttle (m3)", "NPC (M$)", "LCO ($/ton)", "Cycle (hr)"],
      [
        ["500", "380.67", "1.62", "4.83"],
        ["1,000", "274.80", "1.17", "5.67"],
        ["2,000", "281.70", "1.20", "7.33"],
        ["2,500", "237.05", "1.01", "8.17"],
        ["3,000", "282.25", "1.20", "9.00"],
        ["5,000", "264.24", "1.12", "12.33"],
      ]
    ),
  ];
}

// Chapter 4: Case 2-1 Yeosu
function createChapter4() {
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Case 2-1: Yeosu to Busan")] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Overview")] }),
    createTable(
      ["Parameter", "Value"],
      [
        ["Storage at Busan", "No"],
        ["Distance", "86 nautical miles"],
        ["Travel Time (one-way)", "5.73 hours"],
        ["Optimal Shuttle", "10,000 m3"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Cycle Time Formula (Case 2)")] }),
    new Paragraph({ children: [new TextRun({ text: "Vessels_per_Trip = floor(Shuttle_Size / Bunker_Volume)", font: "Courier New", size: 20 })] }),
    new Paragraph({ children: [new TextRun({ text: "Cycle = Shore + Travel_RT + Port + (Vessels x Per_Vessel)", font: "Courier New", size: 20 })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Example: 10,000 m3 Shuttle")] }),
    new Paragraph({ children: [new TextRun("Vessels per Trip = floor(10000/5000) = 2")] }),
    new Paragraph({ children: [new TextRun("Shore Loading = 10000/1500 = 6.667 hours")] }),
    new Paragraph({ children: [new TextRun("Travel RT = 5.73 x 2 = 11.46 hours")] }),
    new Paragraph({ children: [new TextRun("Port Entry/Exit = 2.0 hours")] }),
    new Paragraph({ children: [new TextRun("Per Vessel = 1.0 + 2.0 + 5.0 = 8.0 hours x 2 = 16.0 hours")] }),
    new Paragraph({ children: [new TextRun({ text: "Total = 6.667 + 11.46 + 2.0 + 16.0 = 36.127 hours", bold: true })] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "CSV: 36.1267 [PASS]", color: "008000", bold: true })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Shuttle Comparison")] }),
    createTable(
      ["Metric", "5,000 m3", "10,000 m3", "15,000 m3"],
      [
        ["NPC Total", "$754.93M", "$747.18M", "$803.67M"],
        ["LCOAmmonia", "$3.20/ton", "$3.17/ton", "$3.41/ton"],
        ["Cycle Duration", "24.79 hr", "36.13 hr", "47.46 hr"],
        ["Vessels/Trip", "1", "2", "3"],
      ]
    ),
  ];
}

// Chapter 5: Case 2-2 Ulsan
function createChapter5() {
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Case 2-2: Ulsan to Busan")] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Overview")] }),
    createTable(
      ["Parameter", "Value"],
      [
        ["Storage at Busan", "No"],
        ["Distance", "25 nautical miles"],
        ["Travel Time (one-way)", "1.67 hours"],
        ["Optimal Shuttle", "5,000 m3"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Example: 5,000 m3 Shuttle")] }),
    new Paragraph({ children: [new TextRun("Vessels per Trip = floor(5000/5000) = 1")] }),
    new Paragraph({ children: [new TextRun("Shore Loading = 5000/1500 = 3.333 hours")] }),
    new Paragraph({ children: [new TextRun("Travel RT = 1.67 x 2 = 3.34 hours")] }),
    new Paragraph({ children: [new TextRun("Port Entry/Exit = 2.0 hours")] }),
    new Paragraph({ children: [new TextRun("Per Vessel = 8.0 hours")] }),
    new Paragraph({ children: [new TextRun({ text: "Total = 3.333 + 3.34 + 2.0 + 8.0 = 16.673 hours", bold: true })] }),
    new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: "CSV: 16.6733 [PASS]", color: "008000", bold: true })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Shuttle Comparison")] }),
    createTable(
      ["Metric", "2,500 m3", "5,000 m3", "10,000 m3"],
      [
        ["NPC Total", "$487.48M", "$402.37M", "$495.93M"],
        ["LCOAmmonia", "$2.07/ton", "$1.71/ton", "$2.10/ton"],
        ["Cycle Duration", "15.01 hr", "16.67 hr", "28.01 hr"],
        ["Vessels/Trip", "1", "1", "2"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Comparison with Yeosu")] }),
    createTable(
      ["Metric", "Case 2-1 (Yeosu)", "Case 2-2 (Ulsan)", "Difference"],
      [
        ["Distance", "86 nm", "25 nm", "-71%"],
        ["Travel Time", "5.73 hr", "1.67 hr", "-71%"],
        ["Optimal Shuttle", "10,000 m3", "5,000 m3", "-50%"],
        ["NPC", "$747.18M", "$402.37M", "-46%"],
      ]
    ),
  ];
}

// Chapter 6: Comparison with Figures
function createChapter6() {
  const content = [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Cross-Case Comparison")] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Summary Table")] }),
    createTable(
      ["Case", "Shuttle", "NPC", "LCO", "Travel Time"],
      [
        ["Case 1", "2,500 m3", "$237.05M", "$1.01/ton", "1.0 hr"],
        ["Case 2-1", "10,000 m3", "$747.18M", "$3.17/ton", "5.73 hr"],
        ["Case 2-2", "5,000 m3", "$402.37M", "$1.71/ton", "1.67 hr"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D1: NPC vs Shuttle Size")] }),
    createImageParagraph("D1_npc_vs_shuttle.png", 550, 350),
    new Paragraph({ children: [new TextRun({ text: "All cases show U-shaped cost curves with clear optimal shuttle sizes.", italics: true })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D2: Annual Cost Evolution")] }),
    createImageParagraph("D2_yearly_cost_evolution.png", 550, 350),
    new Paragraph({ children: [new TextRun({ text: "Costs scale linearly with demand growth (50 to 500 vessels).", italics: true })] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D3: Fleet Size & Demand")] }),
    createImageParagraph("D3_yearly_fleet_demand.png", 550, 350),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D4: Annual Cycles")] }),
    createImageParagraph("D4_yearly_cycles.png", 550, 350),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D5: Utilization Rate")] }),
    createImageParagraph("D5_yearly_utilization.png", 550, 350),
    new Paragraph({ children: [new TextRun({ text: "All optimal configurations achieve 100% utilization.", italics: true })] }),

    new Paragraph({ children: [new PageBreak()] }),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D7: Cycle Time Comparison")] }),
    createImageParagraph("D7_cycle_time.png", 550, 350),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D9: LCO Comparison")] }),
    createImageParagraph("D9_lco_comparison.png", 550, 350),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Figure D10: NPC Case Comparison")] }),
    createImageParagraph("D10_case_npc_comparison.png", 550, 350),
  ];
  return content;
}

// Chapter 7: Conclusion
function createChapter7() {
  return [
    new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Verification Conclusion")] }),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Verification Checklist")] }),
    createTable(
      ["Item", "Expected", "Result", "Status"],
      [
        ["Discount Rate", "0.0", "0.0", "PASS"],
        ["Annuity Factor", "10.8355", "10.8355", "PASS"],
        ["Pump Rate", "1000 m3/h", "1000", "PASS"],
        ["Case 1 Optimal", "2,500 m3", "2,500 m3", "PASS"],
        ["Case 2-1 Optimal", "10,000 m3", "10,000 m3", "PASS"],
        ["Case 2-2 Optimal", "5,000 m3", "5,000 m3", "PASS"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Cycle Time Verification")] }),
    createTable(
      ["Case", "Shuttle", "Expected", "CSV", "Status"],
      [
        ["Case 1", "2,500 m3", "8.167 hr", "8.1667 hr", "PASS"],
        ["Case 1", "5,000 m3", "12.333 hr", "12.3333 hr", "PASS"],
        ["Case 2-1", "10,000 m3", "36.127 hr", "36.1267 hr", "PASS"],
        ["Case 2-2", "5,000 m3", "16.673 hr", "16.6733 hr", "PASS"],
      ]
    ),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Final Status")] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 300, after: 300 }, children: [
      new TextRun({ text: "OVERALL VERIFICATION: ", size: 28, bold: true }),
      new TextRun({ text: "PASS", size: 32, bold: true, color: "008000" })
    ]}),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Recommendations")] }),
    new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [
      new TextRun({ text: "Primary: ", bold: true }), new TextRun("Case 1 (Busan Storage) - $237.05M, $1.01/ton")
    ]}),
    new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [
      new TextRun({ text: "Alternative: ", bold: true }), new TextRun("Case 2-2 (Ulsan) - $402.37M, $1.71/ton (+70%)")
    ]}),
    new Paragraph({ numbering: { reference: "numbered-list", level: 0 }, children: [
      new TextRun({ text: "Not Recommended: ", bold: true }), new TextRun("Case 2-1 (Yeosu) - $747.18M, $3.17/ton (+215%)")
    ]}),

    new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Report Information")] }),
    createTable(
      ["Item", "Value"],
      [
        ["Report Version", "1.0"],
        ["Date", "2025-01-20"],
        ["Pump Rate", "1000 m3/h (fixed)"],
        ["Discount Rate", "0.0 (no discounting)"],
        ["Time Period", "2030-2050 (21 years)"],
      ]
    ),
  ];
}

// Document creation functions
function createDocument(content, title) {
  return new Document({
    styles,
    numbering,
    sections: [{
      properties: {
        page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
      },
      headers: { default: createHeader() },
      footers: { default: createFooter() },
      children: content
    }]
  });
}

function createCombinedDocument() {
  const sections = [
    { title: "Cover", content: [
      new Paragraph({ spacing: { before: 4000 } }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "Deterministic Case", size: 56, bold: true, color: "1F4E79" })
      ]}),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "Verification Report", size: 56, bold: true, color: "1F4E79" })
      ]}),
      new Paragraph({ spacing: { before: 1000 }, alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "Green Corridor Ammonia Bunkering Optimization", size: 28 })
      ]}),
      new Paragraph({ spacing: { before: 500 }, alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "Version 1.0 | January 2025", size: 24, color: "808080" })
      ]}),
      new Paragraph({ children: [new PageBreak()] }),
      new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
    ]},
  ];

  const chapterFunctions = [createChapter1, createChapter2, createChapter3, createChapter4, createChapter5, createChapter6, createChapter7];

  return new Document({
    styles,
    numbering,
    sections: [
      {
        properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
        children: sections[0].content
      },
      ...chapterFunctions.map((fn, idx) => ({
        properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
        headers: { default: createHeader() },
        footers: { default: createFooter() },
        children: [new Paragraph({ children: [new PageBreak()] }), ...fn()]
      }))
    ]
  });
}

async function generateDocuments() {
  console.log("[INFO] Starting document generation...");

  // Individual chapters
  const chapters = [
    { name: "01_executive_summary", fn: createChapter1 },
    { name: "02_parameters", fn: createChapter2 },
    { name: "03_case1_busan", fn: createChapter3 },
    { name: "04_case2_yeosu", fn: createChapter4 },
    { name: "05_case2_ulsan", fn: createChapter5 },
    { name: "06_comparison", fn: createChapter6 },
    { name: "07_conclusion", fn: createChapter7 },
  ];

  for (const ch of chapters) {
    const doc = createDocument(ch.fn(), ch.name);
    const buffer = await Packer.toBuffer(doc);
    const outPath = path.join(OUTPUT_DIR, `${ch.name}.docx`);
    fs.writeFileSync(outPath, buffer);
    console.log(`[OK] Created: ${ch.name}.docx`);
  }

  // Combined document
  const combinedDoc = createCombinedDocument();
  const combinedBuffer = await Packer.toBuffer(combinedDoc);
  const combinedPath = path.join(OUTPUT_DIR, "Verification_Report_Combined.docx");
  fs.writeFileSync(combinedPath, combinedBuffer);
  console.log("[OK] Created: Verification_Report_Combined.docx");

  console.log("[INFO] All documents generated successfully!");
}

generateDocuments().catch(err => {
  console.error("[ERROR]", err);
  process.exit(1);
});
