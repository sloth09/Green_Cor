# Paper Outline: Optimal Ammonia Bunkering Infrastructure for Green Shipping Corridors -- A Multi-Period Mixed-Integer Linear Programming Approach

**Paper type:** Deterministic case
**Phase:** 4 of 10
**Status:** Complete

**Target length:** 6,000--8,000 words (excluding references and appendices)

---

## 1. Introduction (Phase 8 -- written last)

### 1.1 Maritime Decarbonization and Ammonia as Fuel
- **Purpose:** Establish the urgency and context of the problem
- **Core argument:** IMO 2050 targets require alternative fuels; ammonia is a leading candidate but lacks bunkering infrastructure
- **Evidence:** IMO regulations, fleet statistics (144 ammonia-fueled vessels ordered as of 2025), fuel property comparison [1, 2, 5]
- **Transition:** Ammonia properties are established, but the supply chain from production to vessel fuel tank remains unresolved

### 1.2 Green Corridors and Infrastructure Challenge
- **Purpose:** Narrow from global decarbonization to the specific infrastructure problem
- **Core argument:** Green corridor initiatives (Korea--US, Korea--Australia) require port-level ammonia bunkering infrastructure, but planning tools are absent
- **Evidence:** Korea--US green corridor agreement (2025), Busan mega-port $10B investment, Getting to Zero Coalition [6, 7]
- **Transition:** The infrastructure gap is acknowledged; we now review what quantitative tools exist

### 1.3 Research Gaps
- **Purpose:** State precisely what existing literature cannot answer
- **Core argument:** Three specific gaps exist (from Phase 1)
- **Evidence:** Literature matrix showing no paper covers joint optimization + supply chain comparison + multi-period dynamics [8, 9, 11, 12, 14]
- **Transition:** These three gaps define the scope of our contributions

### 1.4 Contributions and Paper Structure
- **Purpose:** State what this paper delivers
- **Core argument:** Four contributions (from Phase 3) with preview of key results
- **Evidence:** Preview numbers: Case 1 NPC $290.81M, LCOA $1.23/ton; break-even ~59.6 nm; LCO stability $1.21--$1.28/ton
- **Transition:** Section 2 reviews literature; Section 3 presents methodology; Section 4 presents results; Section 5 discusses implications

---

## 2. Literature Review

### 2.1 Ammonia as a Marine Fuel
- **Purpose:** Establish ammonia's viability and cost parameters
- **Core argument:** Technical properties are well-characterized; economic viability depends on infrastructure costs not yet quantified at port level
- **Evidence:** Fuel comparison data [1], SFOC values [2], single-vessel economics [3], cost parameters [4]
- **Transition:** Properties are known; supply chain logistics are not

### 2.2 Maritime Fleet Sizing and MILP Optimization
- **Purpose:** Review optimization methods available for fleet sizing
- **Core argument:** MILP is the standard tool for fleet sizing in maritime; mature formulations exist but not for ammonia bunkering
- **Evidence:** Fleet scheduling DSS [8], routing review [9], LNG supply chain MILP [12], offshore wind fleet sizing [13], bulk fleet renewal [14], green container fleet [17]
- **Transition:** MILP methods are proven; application to ammonia bunkering is missing

### 2.3 Ammonia Bunkering Operations
- **Purpose:** Review the closest existing work
- **Core argument:** Yang and Lam [11] used DES for ammonia bunkering -- simulation identifies sensitivity but not optimal configurations
- **Evidence:** DES model: flow rate 51.3% impact on service time, vessel count 15.2% impact on cost [11]
- **Transition:** Simulation provides insights; optimization provides decisions. Our MILP bridges this gap

### 2.4 Research Gap Summary
- **Purpose:** Synthesize the three gaps as one paragraph
- **Core argument:** Two non-overlapping literature clusters (ammonia knowledge vs. optimization methods) with no study at the intersection
- **Evidence:** Literature matrix (Phase 2, Section 3.6)
- **Transition:** We address these gaps with a MILP model described next

---

## 3. Methodology

### 3.1 Problem Description and Assumptions
- **Purpose:** Define the optimization problem in plain language
- **Core argument:** A port authority must determine shuttle vessel size, pump rate, and fleet expansion schedule to minimize 20-year ammonia bunkering cost
- **Evidence:** Planning horizon (2030--2050), demand trajectory (50 to 500 vessels, 12 voyages/year), bunker volume (5,000 m3/call)
- **Transition:** We formalize this as three supply chain configurations

### 3.2 Three Supply Chain Configurations
- **Purpose:** Define Cases 1, 2-1, 2-2 with all parameters
- **Core argument:** Each configuration has distinct cost/time structures due to different shuttle sizes, travel distances, and storage requirements
- **Evidence:** Fig. 1 (D7) -- cycle time comparison; parameter table from config files
- **Transition:** The key physical difference is cycle time, which we now formalize

### 3.3 Cycle Time Model
- **Purpose:** Show the mathematical relationship between shuttle size, pump rate, and cycle time
- **Core argument:** Cycle time differs structurally between Case 1 (pump time = shuttle_size/pump_rate) and Case 2 (pump time = bunker_volume/pump_rate per vessel served)
- **Evidence:** Equations (1)--(6) with parameter values; Fig. 1 (D7) validation
- **Transition:** Cycle time determines fleet capacity, which enters the MILP formulation

### 3.4 MILP Formulation
- **Purpose:** Present the optimization model formally
- **Core argument:** The MILP minimizes 20-year NPC subject to demand, capacity, and operational constraints
- **Evidence:** Equations (7)--(15) -- objective function, decision variables, constraints
- **Transition:** The NPC calculation requires a cost model

### 3.5 Cost Model
- **Purpose:** Define all cost components
- **Core argument:** Costs comprise shuttle CAPEX (scaling law), bunkering equipment CAPEX, fixed OPEX, and variable OPEX (fuel-based)
- **Evidence:** Equations (16)--(22) -- CAPEX scaling, annuity factor, OPEX formulas; parameter table with all values
- **Transition:** We solve this model across all feasible shuttle-pump combinations

### 3.6 Solution Approach and Sensitivity Design
- **Purpose:** Describe how the model is solved and sensitivity analyses structured
- **Core argument:** Full enumeration of shuttle-pump grid with CBC solver; six sensitivity analyses (tornado, fuel price, bunker volume, two-way, demand scenarios, break-even distance)
- **Evidence:** Solver details, grid dimensions, sensitivity parameter ranges
- **Transition:** Section 4 presents the results

---

## 4. Results and Analysis

### 4.1 Optimal Configurations (Contribution C1)
- **Purpose:** Identify cost-minimizing infrastructure for each case
- **Core argument:** Optimal shuttle size differs across cases (2,500 / 10,000 / 5,000 m3) due to the interaction between CAPEX scaling and cycle time
- **Evidence:** Fig. 2 (D1) -- NPC vs shuttle curves; Fig. 3 (D10) -- cross-case comparison; Fig. S1 (D12) -- heatmaps; Table 1 (optimal solutions)
- **Key numbers:** Case 1: 2,500 m3, $290.81M, $1.23/ton; Case 2-1: 10,000 m3, $879.88M; Case 2-2: 5,000 m3, $700.68M
- **Transition:** These static optima evolve over the 21-year planning horizon

### 4.2 Temporal Dynamics (Contribution C3)
- **Purpose:** Show how fleet and costs evolve year by year
- **Core argument:** Fleet expansion follows a staircase pattern; cost growth is driven by fleet additions in discrete years
- **Evidence:** Fig. 6 (D2) -- annual cost evolution; Fig. 7 (D8) -- fleet evolution; Fig. 8 (D3) -- demand vs fleet response
- **Key numbers:** Fleet sizes at 2030, 2040, 2050; annual cost growth trajectory
- **Transition:** Fleet utilization reveals whether the sizing is efficient

### 4.3 Operational Efficiency
- **Purpose:** Assess whether the optimal fleet is well-utilized
- **Core argument:** Utilization shows a sawtooth pattern -- high before each fleet addition, dropping when new shuttles are added
- **Evidence:** Fig. 9 (D5) -- utilization rates; D4 -- cycle counts
- **Key numbers:** Average utilization, min/max utilization years
- **Transition:** Utilization patterns reflect the underlying cost structure

### 4.4 Cost Structure (Contribution C4)
- **Purpose:** Break down NPC into components and compare across cases
- **Core argument:** Case 1 is CAPEX-dominant (shuttle CAPEX 45.6%); Case 2 is vOPEX-dominant (33--39% from fuel)
- **Evidence:** Fig. 4 (D6) -- cost breakdown; Table 2 (cost components)
- **Key numbers:** Shuttle CAPEX: $132.67M (Case 1) vs $355.18M (Case 2-1); vOPEX: $55.01M vs $294.21M
- **Transition:** Cost per ton (LCOA) normalizes these differences for comparison

### 4.5 LCOA Comparison
- **Purpose:** Provide the key metric for decision-makers
- **Core argument:** LCOA captures the full supply chain cost per ton of ammonia delivered; Case 1 is 2.4--3.0x cheaper per ton
- **Evidence:** Fig. 5 (D9) -- LCOA comparison
- **Key numbers:** $1.23/ton (Case 1) vs $3.73/ton (Case 2-1) vs $2.97/ton (Case 2-2)
- **Transition:** These results assume a fixed pump rate; we now test sensitivity

### 4.6 Pump Rate Sensitivity
- **Purpose:** Test whether pump rate changes the optimal shuttle size
- **Core argument:** Above 1,000 m3/h, pump rate has diminishing returns; optimal shuttle size is robust
- **Evidence:** Fig. 14 (S7) -- pump rate sensitivity curves; pump_sensitivity CSVs
- **Key numbers:** NPC at 400 / 1,000 / 2,000 m3/h for each case
- **Transition:** Pump rate is one of six parameters tested; we now present the full sensitivity analysis

### 4.7 Parametric Sensitivity (Contribution C4)
- **Purpose:** Identify which parameters most affect results and quantify uncertainty impact
- **Core argument:** Cost driver hierarchy differs by case -- CAPEX scaling dominates Case 1 (62%), bunker volume dominates Case 2
- **Evidence:** Fig. 10 (FIG7) -- tornado diagrams; Fig. 11 (FIG8) -- fuel price sensitivity; Fig. S4 (FIGS4) -- two-way heatmap; Fig. S5 (FIGS5) -- bunker volume sensitivity
- **Key numbers:** Tornado swings for top 3 parameters per case; fuel price NPC range $255M--$362M (Case 1)
- **Transition:** Sensitivity to individual parameters is established; we now test robustness to demand uncertainty

### 4.8 Demand Scenario Analysis (Contribution C3)
- **Purpose:** Test whether optimal specifications change under demand uncertainty
- **Core argument:** Optimal shuttle size is invariant to 4x demand range; LCOA varies only 5.7% for Case 1
- **Evidence:** Fig. 13 (FIG10) -- demand scenario NPC/LCO comparison; demand_scenarios_summary.csv
- **Key numbers:** LCO $1.21--$1.28/ton across Low(250)--VeryHigh(1000) end_vessels; optimal shuttle stays 2,500 m3
- **Transition:** Section 5 interprets these findings for green corridor planning

---

## 5. Discussion

### 5.1 Local Storage vs Remote Supply: Break-Even Analysis (Contribution C2)
- **Purpose:** Provide a transferable decision rule for port planners
- **Core argument:** Break-even distance depends on shuttle size: ~59.6 nm at 10,000 m3 (Yeosu), no crossover at 5,000 m3 (Ulsan)
- **Evidence:** Fig. 12 (FIG9) -- break-even curves; breakeven_distance CSVs
- **Key numbers:** Yeosu crossover 59.6 nm; at 86 nm (actual), Case 1 cheaper by $589M; Ulsan no crossover within 10--200 nm
- **Transition:** The break-even finding is robust under the sensitivity analysis results

### 5.2 Robustness of Infrastructure Decisions
- **Purpose:** Synthesize all sensitivity findings into a confidence statement
- **Core argument:** Shuttle sizing is robust to demand, fuel price, and pump rate uncertainty; the primary risk factor is CAPEX scaling (shipyard cost)
- **Evidence:** Sections 4.6--4.8 combined; CAPEX scaling 62% swing vs fuel price 12.3% vs demand LCO range 5.7%
- **Transition:** These findings translate into specific recommendations

### 5.3 Practical Implications for Green Corridor Planning
- **Purpose:** Convert results into actionable guidance
- **Core argument:** Three recommendations for port authorities: (1) build port-based storage for distances >60 nm, (2) commit to shuttle specs early, (3) monitor CAPEX scaling as primary cost risk
- **Evidence:** Break-even result (C2), demand robustness (C3), tornado ranking (C4)
- **Transition:** We now position our findings relative to existing literature

### 5.4 Comparison with Existing Studies
- **Purpose:** Validate our findings against related work
- **Core argument:** Our LCOA values, fleet sizing patterns, and sensitivity rankings are consistent with (but more specific than) existing literature
- **Evidence:** Yang & Lam [11] pump flow rate impact (51.3% vs our tornado finding); LR/UMAS [7] cost ranges; Turkey LNG study [12] multi-period pattern
- **Transition:** Agreement with related work supports our model validity; we now acknowledge limitations

### 5.5 Limitations and Future Work
- **Purpose:** Honest assessment of model scope (Rule 8)
- **Core argument:** Six limitations with assessed impact direction/magnitude; five specific future work extensions
- **Evidence:** Model assumptions from methodology
- **Limitations:**
  1. Deterministic demand (linear growth) -- S-curve may increase early overcapacity
  2. Fixed fuel price ($600/ton) -- price volatility affects Case 2 more (+21.5% NPC for +30% price)
  3. No discount rate (0%) -- standard 8% rate would favor early investment
  4. SFOC fixed per shuttle size -- zero tornado sensitivity is a structural artifact
  5. No port congestion or queuing -- may underestimate fleet needs at peak demand
  6. Single bunker volume (5,000 m3/call) -- variable bunker demand per vessel not modeled
- **Future work:**
  1. Stochastic demand/price MILP (two-stage)
  2. Port queuing simulation coupled with MILP
  3. Multi-fuel comparison (ammonia vs methanol vs LNG)
  4. Real-options analysis for staged investment
  5. Extension to multi-port networks

---

## 6. Conclusions
- **Purpose:** Summarize key findings and their significance (no new information)
- **Core argument:** Four contributions answered three gaps; the MILP framework provides a transferable decision tool for ammonia bunkering infrastructure planning
- **Evidence:** Key numbers repeated: Case 1 optimal $290.81M / $1.23/ton; break-even 59.6 nm; LCO stability 5.7%
- **Key takeaway:** Port authorities can commit to shuttle vessel specifications (2,500 m3 for port-based storage) without waiting for demand clarity; the build-vs-source decision depends primarily on distance to ammonia supply

---

## Figure Assignment Verification

### MUST Figures (all assigned)

| Fig # | Source ID | Section | Status |
|-------|-----------|---------|--------|
| Fig. 1 | D7 | 3.2 | Assigned |
| Fig. 2 | D1 | 4.1 | Assigned |
| Fig. 3 | D10 | 4.1 | Assigned |
| Fig. 4 | D6 | 4.4 | Assigned |
| Fig. 5 | D9 | 4.5 | Assigned |
| Fig. 6 | D2 | 4.2 | Assigned |
| Fig. 7 | D8 | 4.2 | Assigned |
| Fig. 8 | D3 | 4.2 | Assigned |
| Fig. 9 | D5 | 4.3 | Assigned |
| Fig. 10 | FIG7 | 4.7 | Assigned |
| Fig. 11 | FIG8 | 4.7 | Assigned |
| Fig. 12 | FIG9 | 5.1 | Assigned |
| Fig. 13 | FIG10 | 4.8 | Assigned |
| Fig. 14 | S7 | 4.6 | Assigned |

### Supplementary Figures (all assigned)

| Fig # | Source ID | Section | Status |
|-------|-----------|---------|--------|
| Fig. S1 | D12 | 4.1 | Assigned |
| Fig. S2 | D11 | 4.1 | Assigned |
| Fig. S3 | D4 | 4.3 | Assigned |
| Fig. S4 | FIGS4 | 4.7 | Assigned |
| Fig. S5 | FIGS5 | 4.7 | Assigned |

---

## Narrative Arc Summary

```
INTRODUCTION: Ammonia bunkering infrastructure is the missing link for green corridors
       |
LITERATURE: Optimization methods exist; ammonia knowledge exists; intersection is empty
       |
METHODOLOGY: MILP coupling shuttle-pump-fleet decisions through cycle time physics
       |
RESULTS: Optimal specs differ by case; costs evolve over time; sensitivity identifies risks
       |
DISCUSSION: Port storage beats remote supply above ~60 nm; specs robust to demand; act now
       |
CONCLUSION: Decision tool ready for port authorities planning ammonia infrastructure
```

---

## Quality Gate Checklist

- [x] Every section has Purpose + Core Argument + Evidence
- [x] Every MUST figure from figure-map.md is assigned to a section (14 main + 5 supplementary)
- [x] Transitions connect all sections into a coherent narrative arc
- [x] Results section organized thematically (4.1--4.8), not case-by-case
- [x] No section lacks evidence mapping
