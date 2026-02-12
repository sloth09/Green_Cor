---
name: paper-writer
description: "SCI-level academic paper writing with enforced multi-phase workflow. Use when the user asks to write a research paper, journal article, or scientific publication based on Green Corridor optimization results."
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, Skill
argument-hint: "[start deterministic|stochastic|combined] [phase N] [resume] [review] [assemble] [status]"
---

# Paper Writer Skill: SCI-Level Academic Paper Workflow

Write research papers based on Green Corridor MILP optimization results using a structured 10-phase workflow that enforces depth, evidence, and academic rigor.

---

## When to Use This Skill

- User asks to write a research paper, journal article, or scientific publication
- User asks to draft paper sections (methodology, results, discussion, etc.)
- User wants to assemble optimization results into an academic narrative
- User says "write a paper" or "draft a paper" about the Green Corridor project

---

## Commands

| Command | Action |
|---------|--------|
| `/paper-writer start deterministic` | Begin Phase 0 for deterministic case paper |
| `/paper-writer start stochastic` | Begin Phase 0 for stochastic case paper |
| `/paper-writer start combined` | Begin Phase 0 for combined paper (both) |
| `/paper-writer phase N` | Jump to Phase N (requires prior phases complete) |
| `/paper-writer resume` | Continue from last completed phase |
| `/paper-writer review` | Run quality review on current drafts (8-rule check) |
| `/paper-writer assemble` | Run Phase 10 (generate DOCX + PDF) |
| `/paper-writer status` | Show completion status of all phases |

---

## Paper Scope by Type

| Type | Figures Used | Sections | Focus |
|------|-------------|----------|-------|
| **deterministic** | D1-D12, S7, FIG7-FIG14, FIGS4-FIGS5 | 1-6 (no stochastic) | Infrastructure sizing + sensitivity under deterministic demand |
| **stochastic** | S1-S7, C1-C4 | Focus on uncertainty | Decision-making under demand/price uncertainty |
| **combined** | All (D+S+C+FIG+FIGS) | Full paper | Complete analysis with both approaches |

---

## Output Workspace

Paper artifacts are organized by version:

```
docs/paper/
+-- v1/                        (Original paper - frozen, do not edit)
+-- v2/                        (Current working version)
    +-- 00_gap-statement.md        (Phase 1)
    +-- 01_lit-review-matrix.md    (Phase 2)
    +-- 02_contributions.md        (Phase 3)
    +-- 03_detailed-outline.md     (Phase 4)
    +-- 04_methodology.md          (Phase 5)
    +-- 05_results.md              (Phase 6)
    +-- 06_discussion.md           (Phase 7)
    +-- 07_introduction.md         (Phase 8)
    +-- 08_abstract.md             (Phase 9)
    +-- 09_references.md           (Phase 10)
    +-- paper_final.md             (Phase 10 - merged)
    +-- paper.docx                 (Phase 10)
    +-- paper.pdf                  (Phase 10)
+-- (root is clean: only v1/ and v2/ folders)
```

**Version Policy:** All new edits MUST target `docs/paper/v2/`. The `docs/paper/v1/` folder is a frozen snapshot and must not be modified.

---

## IMPORTANT: Writing Quality Rules

**Before writing ANY prose (Phases 5-9), read the 8 anti-shallow-writing rules:**

File: `.claude/skills/paper-writer/references/writing-rules.md`

**Quick summary of the 8 rules:**
1. **Specificity Obligation** - Every claim needs a number from data
2. **So-What Test** - Every fact needs a decision consequence
3. **No Tautology** - Never restate the definition as explanation
4. **Figure Analysis Protocol** - Describe + Quantify + Explain for every figure
5. **Comparison Obligation** - Anchor every result to a reference point
6. **No Orphan Claims** - Every assertion traceable to CSV/figure/reference
7. **Transition Obligation** - Every paragraph connects to the next
8. **Limitation Honesty** - Assumption + Reason + Impact for every simplification

**Enforcement:** After each paragraph, check rules. During `/paper-writer review`, flag all violations.

---

## Phase 0: Data Ingestion

**Goal:** Load all data into working memory. No writing yet.

### Input
Read these files (use Read tool):

**Deterministic results:**
- `results/deterministic/MILP_scenario_summary_case_1.csv`
- `results/deterministic/MILP_scenario_summary_case_3.csv`
- `results/deterministic/MILP_scenario_summary_case_2.csv`
- `results/deterministic/MILP_per_year_results_case_1.csv` (sample: optimal scenario rows)
- `results/deterministic/MILP_per_year_results_case_3.csv` (sample)
- `results/deterministic/MILP_per_year_results_case_2.csv` (sample)

**Sensitivity results (pump rate):**
- `results/sensitivity/pump_sensitivity_case_1.csv`
- `results/sensitivity/pump_sensitivity_case_3.csv`
- `results/sensitivity/pump_sensitivity_case_2.csv`

**Sensitivity results (deterministic - NEW):**
- `results/sensitivity/fuel_price_case_1.csv` (+ case_2, case_3)
- `results/sensitivity/tornado_det_case_1.csv` (+ case_2, case_3)
- `results/sensitivity/bunker_volume_case_1.csv` (+ case_2, case_3)
- `results/sensitivity/two_way_det_case_1.csv`
- `results/sensitivity/demand_scenarios_case_1.csv` (+ case_2, case_3)
- `results/sensitivity/demand_scenarios_summary.csv`
- `results/sensitivity/breakeven_distance_ulsan.csv` (+ yeosu, combined)

**Discount rate sensitivity (v2 NEW):**
- `results/discount_rate_analysis/data/discount_rate_comparison.csv` (9 rows: 3 cases x 3 rates)
- `results/discount_rate_analysis/data/discount_rate_yearly_case_1.csv`
- `results/discount_rate_analysis/data/discount_rate_yearly_case_3.csv`
- `results/discount_rate_analysis/data/discount_rate_yearly_case_2.csv`

**Yang & Lam DES comparison (v2 NEW):**
- `results/yang_lam_des_comparison/data/service_time_comparison.csv`
- `results/yang_lam_des_comparison/data/methodology_comparison.csv`
- `results/yang_lam_des_comparison/data/cost_structure_comparison.csv`
- `results/yang_lam_des_comparison/data/flow_rate_sensitivity_comparison.csv`
- `results/yang_lam_des_comparison/data/sensitivity_summary_comparison.csv`
- `results/yang_lam_des_comparison/data/yang_lam_reference_data.csv`
- `results/yang_lam_des_comparison/data/comparison_summary.txt`

**Configuration (for methodology section):**
- `config/base.yaml`
- `config/case_1.yaml`
- `config/case_3.yaml`
- `config/case_2.yaml`

**If stochastic or combined:**
- `results/stochastic/stochastic_summary_case_1.csv`
- `results/stochastic/tornado_case_1.csv`
- `results/stochastic/case_comparison.csv`
- (and case 2 variants)

**Reference files:**
- `.claude/skills/paper-writer/references/data-inventory.md`
- `.claude/skills/paper-writer/references/figure-map.md`

### Activity
1. Read all CSV files and extract key numbers following data-inventory.md Section 5 extraction guide
2. Read config files and note all parameter values
3. **CRITICAL: All numbers must come from CSV/config files directly. NEVER copy values from reference files (data-inventory.md, figure-map.md, etc.) -- these contain extraction INSTRUCTIONS only, not data.**
4. List all available figures in `results/paper_figures/`

### Output
Confirm to user: "Phase 0 complete. Loaded data for N scenarios across 3 cases. Key numbers verified. Ready for Phase 1."

### Quality Gate
- [ ] All deterministic CSV files read (6 base + 20 sensitivity = 26 total)
- [ ] Optimal scenario identified for each case
- [ ] Key numbers extracted directly from CSV/config (NOT from reference files)
- [ ] Sensitivity key results extracted from CSV (tornado top drivers, break-even distances, demand LCOA stability)
- [ ] Figure files confirmed present (D1-D12 + Fig7-Fig14 + FigS4-FigS5 + S7)
- [ ] Discount rate data confirmed (9 rows in discount_rate_comparison.csv)
- [ ] Yang & Lam data confirmed (7 files in yang_lam_des_comparison/data/)

---

## Phase 1: Research Gap Statement

**Goal:** Define precisely what existing literature does NOT address.

### Input
- Data from Phase 0 (what our model does)
- `.claude/skills/paper-writer/references/bibliography.md` (seed references)

### Activity
1. Identify 2-3 specific research gaps based on what our model uniquely provides
2. Frame gaps as questions that existing literature cannot answer
3. Each gap must be falsifiable (someone could prove us wrong)

### Gaps to Explore
- **Gap 1 (Infrastructure Sizing):** No existing study jointly optimizes shuttle vessel size, fleet count, and bunkering pump capacity for ammonia supply chains over a multi-decade horizon.
- **Gap 2 (Supply Chain Comparison):** No quantitative comparison exists between port-based storage (Case 1) and remote supply (Case 2) configurations for ammonia bunkering, with distance as a variable.
- **Gap 3 (Temporal Dynamics):** Existing studies assume static fleet sizes; none model dynamic fleet expansion synchronized with demand growth trajectories.

### Output
Write to `docs/paper/00_gap-statement.md`:
- 2-3 gap statements, each with:
  - What is currently known
  - What is NOT known (the gap)
  - Why it matters (practical consequence)
  - How our study fills it

### Quality Gate
- [ ] At least 2 specific gaps identified
- [ ] No gap uses vague language ("important", "significant", "novel")
- [ ] Each gap references what IS known (from seed bibliography)
- [ ] Each gap is connected to a practical decision problem
- [ ] **FAIL if any gap is merely "this topic has not been studied enough"**

---

## Phase 2: Literature Matrix

**Goal:** Systematically map existing literature and identify what each paper did NOT do.

### Input
- Gap statement from Phase 1
- Seed references from `bibliography.md`

### Activity
1. Use WebSearch with queries from bibliography.md Section 2 to find 10+ relevant papers
2. For each paper found, record:
   - Full citation
   - Method used
   - Fuel type studied
   - Whether they did fleet sizing, cost modeling, multi-period analysis, infrastructure optimization
   - **Most important: What they did NOT do** (feeds directly into contributions)
3. Organize into a comparison matrix

### Output
Write to `docs/paper/01_lit-review-matrix.md`:
- Literature matrix table (see bibliography.md Section 3 for template)
- Narrative summary: 3-4 paragraphs organizing literature by theme
- Clear statement of how existing work collectively fails to address our gaps

### Quality Gate
- [ ] Minimum 10 papers in matrix (prefer 15-20)
- [ ] Each paper has "What they did NOT do" filled in
- [ ] Matrix covers all 3 gap areas from Phase 1
- [ ] At least 3 papers from 2023 or later
- [ ] WebSearch was actually used (not just seed references)
- [ ] **FAIL if literature review reads as a list of summaries without synthesis**

---

## Phase 3: Contributions Statement

**Goal:** Define 3-5 specific contributions, each mapped to evidence.

### Input
- Gap statement (Phase 1)
- Literature matrix (Phase 2)
- Available data and figures (Phase 0)

### Activity
1. Define 3-5 contributions that directly address the identified gaps
2. For each contribution, specify:
   - What we contribute (concise statement)
   - Which data/figures prove it (figure IDs from figure-map.md)
   - Which literature gap it fills (reference to Phase 1)
   - The key quantitative result that demonstrates the contribution

### Output
Write to `docs/paper/02_contributions.md`:

Example format:
```
## Contribution 1: Multi-period fleet-infrastructure co-optimization
We develop a MILP model that jointly optimizes shuttle vessel sizing (500-50,000 m3),
fleet expansion timing, and bunkering pump capacity over a 21-year planning horizon
(2030-2050), addressing Gap 1.

Evidence: Fig. 2 (D1), Fig. 7 (D8), Table 3
Key result: Optimal fleet grows from 6 to 52 shuttles (Case 1, 2500 m3)
Gap filled: No prior study jointly optimizes these three decisions dynamically.
```

### Quality Gate
- [ ] 3-5 contributions defined
- [ ] Each contribution maps to at least one figure and one CSV metric
- [ ] Each contribution references a specific gap from Phase 1
- [ ] No contribution is a restatement of methodology ("we use MILP" is not a contribution)
- [ ] **FAIL if any contribution lacks quantitative evidence mapping**

---

## Phase 4: Detailed Outline

**Goal:** Create a section-by-section outline with purpose, argument, evidence, and transitions.

### Input
- All previous phases
- Figure map from `figure-map.md`

### Activity
Create a detailed outline for each paper section. For each section/subsection:
1. **Purpose:** What this section accomplishes
2. **Core argument:** The main claim of this section
3. **Evidence:** Which figures and data support it
4. **Transition:** How it connects to the next section

### Output
Write to `docs/paper/03_detailed-outline.md`:

```
# Paper Outline: [Title]

## 1. Introduction (Phase 8 - written last)
   Purpose: Frame problem, state gaps, preview contributions
   Subsections:
   1.1 Maritime decarbonization and ammonia as fuel [refs: 1,2,5]
   1.2 Green corridors and infrastructure needs [refs: 6,7]
   1.3 Research gaps [from Phase 1]
   1.4 Contributions and paper structure [from Phase 3]

## 2. Literature Review
   Purpose: Establish what is known and unknown
   [Map to literature matrix from Phase 2]

## 3. Methodology
   Purpose: Explain the MILP model completely and reproducibly
   3.1 Problem description and assumptions
   3.2 Three supply chain configurations (Case 1, 2-1, 2-2)
   3.3 Mathematical formulation
       - Decision variables
       - Objective function
       - Constraints
   3.4 Cost model (CAPEX, OPEX, annualization)
   3.5 Cycle time calculation
   3.6 Solution approach
   Evidence: D7 (cycle time comparison), parameter tables

## 4. Results and Analysis
   [Map each subsection to specific figures from figure-map.md]
   4.1 Optimal configurations (D1, D10, D11, D12)
   4.2 Temporal dynamics (D2, D3, D4, D8)
   4.3 Operational efficiency (D5)
   4.4 Cost structure (D6)
   4.5 LCOA comparison (D9)
   4.6 Pump rate sensitivity (S7)
   4.7 Parametric sensitivity (FIG7: tornado, FIG8: fuel price)
   4.8 Demand scenario analysis (FIG10: 4 demand levels)

## 5. Discussion
   Purpose: Interpret results in broader context
   5.1 Local vs remote supply: break-even analysis (FIG9)
   5.2 Robustness of results (demand stability, parameter sensitivity)
   5.3 Practical implications for port authorities
   5.4 Comparison with literature
   5.5 Limitations and future work

## 6. Conclusions
```

### Quality Gate
- [ ] Every section has Purpose + Core Argument + Evidence
- [ ] Every MUST figure from figure-map.md is assigned to a section
- [ ] Transitions connect all sections into a coherent narrative arc
- [ ] Results section organized thematically (not just case-by-case)
- [ ] **FAIL if any section lacks an evidence mapping**

---

## Phase 5: Methodology

**Goal:** Write a complete, reproducible methodology section.

### Input
- Config files (parameter values)
- Source code for formulas: `src/optimizer.py`, `src/cost_calculator.py`, `src/shuttle_round_trip_calculator.py`
- Outline from Phase 4

### Activity
1. Read actual source code to extract exact formulas
2. Write methodology with:
   - Every variable defined with name, symbol, unit, and value
   - Every equation numbered
   - Every assumption explicitly stated with justification
   - Case 1 vs Case 2 differences clearly delineated
3. Create parameter table(s)
4. Apply Rule 8 (Limitation Honesty) to every assumption

### Key Formulas to Include

**Objective function:**
```
Minimize NPC = SUM over years [Annualized_CAPEX + Fixed_OPEX + Variable_OPEX]
```

**Shuttle CAPEX (scaling law):**
```
CAPEX_shuttle = C_base * (V / V_base)^alpha
where C_base = 61.5M USD, V_base = 40,000 m3, alpha = 0.75
```

**Annuity factor:**
```
AF = [1 - (1 + r)^(-n)] / r
where r = 0.07, n = 21 years -> AF = 10.8355
```

**Cycle time (Case 1):**
```
T_cycle = T_shore + T_travel_out + T_travel_return + T_setup + T_pump
where T_pump = V_shuttle / Q_pump
```

**Cycle time (Case 2):**
```
T_cycle = T_shore + T_travel_out + T_travel_return + T_port
         + N_vessels * (T_movement + T_setup + T_pump_vessel)
where N_vessels = floor(V_shuttle / V_bunker)
      T_pump_vessel = V_bunker / Q_pump
```

### Output
Write to `docs/paper/04_methodology.md`

### Quality Gate
- [ ] Every variable has symbol, definition, unit, and value
- [ ] Every equation is numbered
- [ ] All parameters from config files are documented in a table
- [ ] Case 1 and Case 2 cycle time formulas are both shown and differentiated
- [ ] At least 3 assumptions listed with justification (Rule 8)
- [ ] A reader could reimplement the model from this section alone
- [ ] **FAIL if any variable appears in an equation without definition**

---

## Phase 6: Results and Analysis

**Goal:** Present optimization results with deep, evidence-based analysis.

### Input
- All CSV data (Phase 0)
- All figures from `results/paper_figures/`
- Figure analysis instructions from `figure-map.md`
- Writing rules from `writing-rules.md`

### Activity
1. For each subsection in the outline:
   - State the finding
   - Present the evidence (figure reference + specific numbers from CSV)
   - Explain WHY (causal mechanism, not just description)
   - Compare across cases
2. Apply Figure Analysis Protocol (Rule 4) for every figure reference
3. Apply Specificity Obligation (Rule 1) for every claim

### Subsection Structure (for deterministic paper)

**4.1 Optimal Configurations**
- Present optimal shuttle/pump/NPC for each case (Table)
- Analyze D1: NPC vs shuttle size curves -- explain the U-shape
- Analyze D10: Cross-case NPC comparison -- quantify differences
- Analyze D11/D12: Sensitivity of NPC to configuration choices

**4.2 Temporal Dynamics**
- Analyze D2: Cost evolution 2030-2050
- Analyze D3: Fleet/demand growth
- Analyze D8: Fleet expansion timeline
- Key insight: Investment timing and lumpiness

**4.3 Operational Efficiency**
- Analyze D5: Utilization rates and sawtooth pattern
- Analyze D4: Cycle count evolution

**4.4 Cost Structure**
- Analyze D6: CAPEX vs OPEX breakdown
- Calculate and compare ratios across cases
- Key insight: CAPEX-dominant (Case 1) vs OPEX-dominant (Case 2)

**4.5 LCOA Comparison**
- Analyze D9: Levelized cost across cases
- Benchmark against literature if available

**4.6 Pump Rate Sensitivity**
- Analyze S7 and pump sensitivity CSV data
- Show how pump rate affects optimal shuttle size and NPC

**4.7 Parametric Sensitivity**
- Analyze FIG7 (tornado): rank parameters by NPC impact for each case
  - Extract swing values and percentages from `tornado_det_*.csv`
  - Note if SFOC has minimal swing (explain: fixed map per shuttle size)
- Analyze FIG8 (fuel price): NPC and LCO across $300~$1,200/ton
  - Extract NPC range for each case from `fuel_price_*.csv`
  - Compare sensitivity slopes across cases
- Reference FIGS4 (two-way) and FIGS5 (bunker volume) in supplementary

**4.8 Demand Scenario Analysis**
- Analyze FIG10: 4 demand levels (Low:250 ~ VeryHigh:1000 end_vessels)
- Key check: is Case 1 LCOA stable across demand range? (extract from `demand_scenarios_summary.csv`)
- Check if optimal shuttle size changes across scenarios (robust to demand uncertainty?)
- If stable: policy insight about infrastructure sizing decisions without waiting for demand certainty

**4.9 Discount Rate Sensitivity (v2 NEW)**
- Motivation: Validate Assumption A2 (zero discounting) by testing r = 0%, 5%, 8%
- Table 9: 3 cases x 3 rates showing NPC, LCOA, and optimal shuttle specification
- Key check: is optimal shuttle specification INVARIANT across all discount rates? (extract from `discount_rate_comparison.csv`)
- Calculate NPC reduction percentage from r=0% to r=8% across all cases
- Fig. 15 (FIG11): NPC and LCO vs discount rate
- Fig. 16 (FIG12): Fleet evolution under different discount rates
- Data: `results/discount_rate_analysis/data/discount_rate_comparison.csv`

### Critical Rule for This Phase
**Every analysis paragraph MUST contain at least one specific number from the CSV data.**
If a paragraph has no number, it fails Rule 1 and must be revised.

### Output
Write to `docs/paper/05_results.md`

### Quality Gate
- [ ] Every MUST figure from figure-map.md is referenced and analyzed
- [ ] Every figure reference follows the 3-step protocol (Describe + Quantify + Explain)
- [ ] Every paragraph contains at least one CSV-sourced number (Rule 1)
- [ ] Cross-case comparison appears in every subsection (Rule 5)
- [ ] No tautological explanations (Rule 3)
- [ ] **FAIL if any figure is merely "shown" without analysis**

---

## Phase 7: Discussion

**Goal:** Interpret results in the context of existing literature and practical implications.

### Input
- Results from Phase 6
- Literature matrix from Phase 2
- Contributions from Phase 3

### Activity
1. **Interpretation:** What do the results mean beyond the numbers?
2. **Literature comparison:** Compare key findings with at least 3 papers from Phase 2
3. **Practical implications:** What should port authorities / shipping companies do?
4. **Limitations:** Honest assessment of model assumptions (Rule 8)
5. **Future work:** Specific extensions, not vague directions

### Discussion Structure

**5.1 Local Storage vs Remote Supply: Break-even Analysis**
- Analyze FIG9: find crossover distances from `breakeven_distance_*.csv`
- When does each strategy dominate? (frame using NPC, LCOA, and distance)
- Explain asymmetry: shuttle size choice changes the break-even fundamentally
- Generalizability: framework for other ports (input their distance, check if above/below threshold)

**5.2 Robustness of Results**
- Synthesize sensitivity findings from Section 4.7-4.8:
  - Identify #1 uncertainty for each case from tornado data
  - Quantify fuel price impact range from fuel price sensitivity CSV
  - Check if demand level changes optimal shuttle size
  - Report LCOA stability range across demand scenarios
- Policy implication: if shuttle sizing is invariant to demand, infrastructure decisions are robust

**5.3 Practical Implications for Green Corridor Planning**
- Investment timing recommendations
- Infrastructure sequencing (what to build first)
- Scale-dependent decisions
- Sensitivity-informed risk management

**5.4 Cross-Model Comparison with Published DES Model (v2 NEW)**
- Compare with Yang & Lam (2023) DES model (5 dimensions)
- Framing: complementary methods, NOT cross-validation (see `yang_lam_evaluation.md`)
- Paragraph 1: Methodology difference table (DES=queuing, MILP=fleet sizing)
- Paragraph 2: Service time consistency -- pumping time shared, check gap = operational overhead
- Paragraph 3: Flow rate sensitivity -- extract percentages from CSV, explain gap from TRIA smoothing
- Paragraph 4: Future work -- hybrid DES-MILP approach
- Fig. 17 (FIG13): Service time comparison (3 points)
- Fig. 18 (FIG14): Sensitivity comparison
- Data: `results/yang_lam_des_comparison/data/`
- **AVOID**: "validates", "cross-validation", "confirms accuracy"
- **USE**: "consistency in shared components", "benchmarking", "reasonable calibration"

**5.5 Comparison with Existing Studies**
- Compare LCOA with literature values (from Phase 2)
- Compare fleet sizing approach with existing methods
- Position contribution within the field

**5.6 Limitations and Future Work**
- List each assumption from methodology
- For each: assess direction and magnitude of potential error
- Note SFOC fixed-map limitation (zero tornado sensitivity)
- Specific future work items (not generic)

### Output
Write to `docs/paper/06_discussion.md`

### Quality Gate
- [ ] At least 3 literature papers compared quantitatively
- [ ] Practical implications stated for at least 2 stakeholder types
- [ ] At least 5 limitations acknowledged with impact assessment (Rule 8)
- [ ] Future work items are specific and actionable
- [ ] **FAIL if discussion merely repeats results without interpretation**

---

## Phase 8: Introduction

**Goal:** Frame the paper, state the problem, identify gaps, and preview contributions.

**WHY PHASE 8 (not Phase 1)?** The introduction is written AFTER results and discussion are complete, so it can accurately preview what the paper delivers. Writing the introduction first leads to promises the paper cannot keep.

### Input
- Gap statement (Phase 1)
- Contributions (Phase 3)
- Literature matrix (Phase 2)
- Results highlights (Phase 6)

### Activity
Write the introduction following this structure:
1. **Opening hook:** Maritime decarbonization challenge (1-2 paragraphs)
2. **Background:** Ammonia as marine fuel, green corridors, bunkering challenge (2-3 paragraphs)
3. **Literature gap:** Summarize what is missing (from Phase 1), supported by Phase 2 references (1-2 paragraphs)
4. **This paper:** State contributions (from Phase 3) with specific preview of key results (1 paragraph)
5. **Paper structure:** Brief roadmap (1 paragraph)

### Output
Write to `docs/paper/07_introduction.md`

### Quality Gate
- [ ] Opening paragraph engages without being generic
- [ ] Gap statement is specific and supported by citations
- [ ] Contributions match Phase 3 exactly (no new claims)
- [ ] At least one quantitative result previewed (e.g., "We find that...")
- [ ] Paper structure paragraph at the end
- [ ] 8-12 citations in introduction
- [ ] **FAIL if introduction promises results not in the paper**

---

## Phase 9: Abstract

**Goal:** Write a concise abstract with quantitative results.

**WHY PHASE 9 (last text phase)?** The abstract must accurately reflect the final paper content. It is a compression of everything, not a preview.

### Input
- All completed sections (Phases 5-8)
- Key numbers from Phase 0

### Activity
Write abstract following this structure (aim for 200-250 words):
1. **Context:** One sentence on the problem (maritime decarbonization, ammonia bunkering)
2. **Gap:** One sentence on what is missing
3. **Method:** Two sentences on what we did (MILP, 3 cases, 2030-2050)
4. **Results:** Three sentences with specific numbers:
   - Optimal configurations for each case
   - NPC comparison across cases
   - Key insight (e.g., LCOA comparison or cost structure finding)
5. **Implication:** One sentence on practical significance

### Output
Write to `docs/paper/08_abstract.md`

### Quality Gate
- [ ] 200-250 words
- [ ] At least 3 specific quantitative results (numbers from CSV)
- [ ] No claims not supported by the paper body
- [ ] No citations in abstract
- [ ] Covers: problem, gap, method, results, implication
- [ ] **FAIL if abstract exceeds 300 words or has fewer than 3 numbers**

---

## Phase 10: Assembly

**Goal:** Merge all sections into a final paper and generate output files.

### Activity

**Step 1: Create merged markdown (VERBATIM MERGE -- NO COMPRESSION)**

**CRITICAL RULE: Each section file MUST be included in its ENTIRETY.**
- Do NOT summarize, compress, shorten, or paraphrase any section.
- Do NOT rewrite equations in simplified form. Keep all LaTeX notation.
- Do NOT drop tables, worked examples, or subsections.
- The ONLY permitted removals are: Phase metadata headers (`**Paper type:**`, `**Phase:**`, `**Status:**`) and Quality Gate Checklists at the end of each file.
- After merge, verify word count: paper_final.md MUST be >= 80% of the sum of individual section word counts (excluding metadata/checklists).

Merge order into `docs/paper/v2/paper_final.md`:

```
# [Paper Title]

---
## Abstract
  -> FULL content of 08_abstract.md (excluding metadata header)

---
## 1. Introduction
  -> Merge 07_introduction.md + literature review from 01_lit-review-matrix.md
     into a single chapter with subsections:
     ### 1.1 Related Work
       -> Literature narrative (from 01_lit-review-matrix.md Sections 2.1-2.4,
          excluding comparison matrix table)
     ### 1.2 Research Gaps and Contributions
       -> Research gaps and contributions (from 07_introduction.md or 02_contributions.md)
  NOTE: Do NOT create a separate "Literature Review" chapter.

---
## 2. Methodology
  -> FULL content of 04_methodology.md (ALL equations, ALL tables, ALL worked examples, excluding metadata header and quality gate)

---
## 3. Results and Analysis
  -> FULL content of 05_results.md (ALL subsections 3.1-3.8, ALL tables, excluding metadata header and quality gate)

---
## 4. Discussion
  -> FULL content of 06_discussion.md (ALL subsections 4.1-4.5, excluding metadata header and quality gate)

---
## 5. Conclusions
  -> Extract from Discussion or write as a separate section summarizing 4 main findings

---
## References
  -> Content of 09_references.md

---
## List of Figures
  -> Figure numbering table
```

**Merge verification checklist (MUST pass before proceeding to Step 2):**
- [ ] Count equations: paper_final.md equation count >= individual section equation count
- [ ] Count tables: paper_final.md table count >= individual section table count
- [ ] Count words: paper_final.md words >= 7,000 (SCI minimum)
- [ ] Spot-check: pick 3 random paragraphs from 04_methodology.md and verify they appear verbatim in paper_final.md
- [ ] No draft artifacts: grep for "wait,", "TODO", "FIXME", "TBD" in paper_final.md

**Step 2: Create reference list**
Write `docs/paper/09_references.md` with all cited references in numbered format.

**Step 3: Renumber figures**
Apply the figure numbering from figure-map.md to create consistent Fig. 1, Fig. 2, etc.

**Step 4: Generate DOCX and PDF**

**DOCX**: Use python-docx script to create `docs/paper/v2/paper.docx`:
```bash
python scripts/generate_paper_docx.py
```
The script parses markdown headings, bold text, tables, and equations from paper_final.md,
and inserts figure images inline at their first reference point using FIGURE_MAP.

**PDF**: Use the dedicated PDF script to create `docs/paper/v2/paper.pdf`:
```bash
python scripts/generate_paper_pdf.py
```
This script pre-processes paper_final.md to insert `![Fig. X](path)` image references
before running pandoc+xelatex. This is necessary because paper_final.md uses text-based
figure references (e.g., "Fig. 1") without markdown image syntax.

**WARNING: Do NOT use plain `pandoc paper_final.md -o paper.pdf`** -- this produces a
text-only PDF without any figures. Always use `generate_paper_pdf.py`.

**WARNING: Do NOT use COM automation** (Word.Application) to open/convert files. The lab
environment has security policies that block COM file opening.

### Output
- `docs/paper/v2/paper_final.md` (merged markdown -- FULL content, >= 7,000 words)
- `docs/paper/v2/09_references.md` (reference list)
- `docs/paper/v2/paper.docx` (Word document with figures, ~4-5 MB)
- `docs/paper/v2/paper.pdf` (PDF with figures via xelatex, ~5-6 MB)

### Quality Gate
- [ ] paper_final.md word count >= 7,000
- [ ] paper_final.md equation count matches sum of individual sections
- [ ] paper_final.md table count matches sum of individual sections
- [ ] All figure references use consistent numbering (Fig. 1, Fig. 2, ...)
- [ ] All citations use consistent numbering ([1], [2], ...)
- [ ] Reference list includes all cited works
- [ ] No draft artifacts ("wait,", "TODO", etc.)
- [ ] DOCX generated via python-docx (no COM) with figures embedded
- [ ] PDF generated via `generate_paper_pdf.py` (not plain pandoc) with figures embedded
- [ ] **FAIL if paper_final.md word count < 7,000 -- re-check merge completeness**

---

## `/paper-writer review` Command

Run this at any time to quality-check existing drafts.

### Procedure
1. Read all files in `docs/paper/`
2. Read `writing-rules.md`
3. For each section, check every paragraph against all 8 rules
4. Output a review report:

```
## Review Report

### Section: 05_results.md
- Paragraph 3: [RULE-1 VIOLATION] Claim "Case 1 is cheaper" lacks specific numbers.
  FIX: "Case 1 NPC $290.81M is 33% of Case 3's $879.88M"
- Paragraph 7: [RULE-3 VIOLATION] "The optimal solution minimizes cost" is tautological.
  FIX: Explain WHY 2500 m3 is optimal (CAPEX scaling vs cycle count trade-off)
- Paragraph 12: [RULE-4 VIOLATION] Fig. 5 only described, not quantified.
  FIX: Add numbers from D6 cost breakdown data

### Summary
| Section | Critical | Major | Minor | Status |
|---------|----------|-------|-------|--------|
| 04_methodology | 0 | 1 | 2 | PASS |
| 05_results | 2 | 3 | 1 | REVISE |
| 06_discussion | 0 | 2 | 3 | PASS |
| 07_introduction | 0 | 0 | 1 | PASS |

Overall: REVISE (2 critical violations in results section)
```

---

## `/paper-writer status` Command

Show current progress:

```
## Paper Writer Status

Paper Type: deterministic
Workspace: docs/paper/

| Phase | Name | File | Status |
|-------|------|------|--------|
| 0 | Data Ingestion | (memory) | [DONE] |
| 1 | Research Gap | 00_gap-statement.md | [DONE] |
| 2 | Literature Matrix | 01_lit-review-matrix.md | [IN PROGRESS] |
| 3 | Contributions | 02_contributions.md | [PENDING] |
| 4 | Detailed Outline | 03_detailed-outline.md | [PENDING] |
| 5 | Methodology | 04_methodology.md | [PENDING] |
| 6 | Results & Analysis | 05_results.md | [PENDING] |
| 7 | Discussion | 06_discussion.md | [PENDING] |
| 8 | Introduction | 07_introduction.md | [PENDING] |
| 9 | Abstract | 08_abstract.md | [PENDING] |
| 10 | Assembly | paper.docx + paper.pdf | [PENDING] |

Next action: Complete Phase 2 (Literature Matrix)
```

To determine status, check which files exist in `docs/paper/` and their content completeness.

---

## Language and Style Guidelines

- **Language:** English (academic)
- **Tense:** Past tense for methods and results; present tense for established facts
- **Voice:** Active voice preferred ("We formulate..." not "A model was formulated...")
- **Person:** First person plural ("We", "Our")
- **Numbers:** Spell out below 10 in text; use digits in technical contexts
- **Units:** Always include units; use SI where possible (m3, hours, USD)
- **Figures:** "Fig. 1" in text, "Figure 1" at start of sentence
- **Tables:** "Table 1" always capitalized
- **Equations:** Numbered as (1), (2), etc.
- **Citations:** Numbered style [1], [2], [3]
- **Target length:** 6,000-8,000 words (excluding references and appendices)

---

## Data Source Paths

### Working Pipeline (scripts read/write here - always current)

```
results/deterministic/MILP_*.csv          # live optimization data
results/sensitivity/*.csv                 # live sensitivity data
results/paper_figures/*.png, *.pdf        # volatile - regenerated by Python
results/stochastic*/*.csv                 # stochastic results
```

### Preserved/Stable (frozen snapshots - won't be overwritten by scripts)

```
results/paper1_deterministic/data/        # frozen MILP CSVs for Paper 1
results/paper1_deterministic/sensitivity/ # frozen sensitivity CSVs
results/paper1_deterministic/figures/     # preserved D*, Fig*, FigS* figures
results/paper2_stochastic/data/           # frozen stochastic CSVs for Paper 2
results/paper2_stochastic/figures/        # preserved S*, C* figures
```

**Principle:** READ from working pipeline dirs (always current). REFERENCE preserved dirs when embedding stable figure paths in the paper. Run `python scripts/preserve_paper_results.py` after figure regeneration to sync.

---

## Cross-References to Skill Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Writing Rules | `.claude/skills/paper-writer/references/writing-rules.md` | 8 anti-shallow rules + BAD/GOOD examples |
| Figure Map | `.claude/skills/paper-writer/references/figure-map.md` | 29 figures -> section mapping + analysis instructions (D1-D12, FIG7-FIG10, FIGS4-FIGS5, S1-S7, C1-C4) |
| Data Inventory | `.claude/skills/paper-writer/references/data-inventory.md` | 26 CSV paths (6 base + 20 sensitivity), columns, key numbers |
| Bibliography | `.claude/skills/paper-writer/references/bibliography.md` | Seed references + WebSearch queries |
| Verification Skill | `.claude/skills/verification-report/reference.md` | Exact calculation formulas (cross-check) |
