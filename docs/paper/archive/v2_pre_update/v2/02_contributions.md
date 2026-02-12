# Contributions Statement

**Paper type:** Deterministic case
**Phase:** 3 of 10
**Status:** Complete

---

## Contribution 1: Systematic Parametric Evaluation of Infrastructure Specifications

We identify non-obvious optimal infrastructure specifications through systematic evaluation of all feasible shuttle-pump combinations for three ammonia supply chain configurations, using a MILP that couples these three decision variables through physical cycle time relationships. The coupling produces non-obvious optimal specifications: Case 1 (port-based storage) selects the mid-range shuttle (2,500 m3, not the largest available 5,000 m3), because CAPEX scaling (exponent 0.75) penalizes larger vessels more than the operational savings from fewer trips can offset. In contrast, Case 2-1 (Yeosu, 86 nm) selects a 10,000 m3 shuttle, where the longer travel distance justifies the higher CAPEX to reduce trip frequency. Case 2-2 (Ulsan, 25 nm) selects 5,000 m3 as an intermediate optimum.

**Gap filled:** Gap 1 -- No prior study systematically evaluates all feasible combinations of shuttle vessel size, bunkering pump capacity, and fleet count for ammonia.

**Evidence:**
- Fig. 2 (D1): NPC vs shuttle size curves showing distinct optima per case
- Fig. S1 (D12): NPC heatmaps over shuttle-pump grid confirming single global minimum per case
- Fig. 14 (S7): Pump rate sensitivity showing diminishing returns above 1,000 m3/h
- Fig. 1 (D7): Cycle time decomposition quantifying the shuttle-pump coupling
- Table: Scenario summary CSVs (`MILP_scenario_summary_case_*.csv`)

**Key quantitative results:**

| Case | Optimal Shuttle | Optimal Pump | NPC (USD M) | LCOA (USD/ton) | Cycle Time (hr) |
|------|----------------|-------------|-------------|-----------------|-----------------|
| Case 1 (Busan) | 2,500 m3 | 1,000 m3/h | 290.81 | 1.23 | 10.17 |
| Case 2-1 (Yeosu) | 10,000 m3 | 1,000 m3/h | 879.88 | 3.73 | 38.13 |
| Case 2-2 (Ulsan) | 5,000 m3 | 1,000 m3/h | 700.68 | 2.97 | 23.19 |

**Distinctiveness from literature:** Yang and Lam [11] evaluated ammonia bunkering configurations through simulation (DES); they identified sensitivity but not optima. The Turkey LNG study [12] optimized fleet size/routing but for LNG with fixed pump rates. Our model is the first to systematically evaluate all feasible combinations of these three variables for ammonia.

---

## Contribution 2: Break-Even Distance Decision Rule for Port-Based Storage vs. Remote Ammonia Supply

We provide port planners with a quantitative decision rule for choosing between constructing local ammonia storage and relying on shuttle deliveries from remote production facilities. By applying the same MILP to three supply chain configurations under identical demand (50 to 500 vessels, 21 years) and fuel price ($600/ton) assumptions, we isolate the effect of supply chain topology on total system cost. We then parameterize the one-way travel distance from 10 to 200 nm (20 points) and identify the break-even distance at which remote supply matches port-based storage cost.

**Gap filled:** Gap 2 -- No prior quantitative comparison exists between port-based storage and remote supply for ammonia bunkering with distance as a variable.

**Evidence:**
- Fig. 12 (FIG9): Break-even distance curves showing crossover at ~59.6 nm for Yeosu (10,000 m3) and no crossover for Ulsan (5,000 m3)
- Fig. 3 (D10): NPC comparison across three cases at optimal configurations
- Fig. 5 (D9): LCOA comparison showing Case 1 at $1.23/ton vs Case 2-1 at $3.73/ton
- Fig. 4 (D6): Cost breakdown revealing structural difference (CAPEX-dominated vs vOPEX-dominated)
- Table: Break-even CSVs (`breakeven_distance_yeosu.csv`, `breakeven_distance_ulsan.csv`)

**Key quantitative results:**

| Comparison | Shuttle Size | Break-even Distance | Result |
|-----------|-------------|-------------------|--------|
| Yeosu (Case 2-1) vs Case 1 | 10,000 m3 | ~59.6 nm | Remote supply cheaper below 59.6 nm; port storage cheaper above |
| Ulsan (Case 2-2) vs Case 1 | 5,000 m3 | No crossover (10--200 nm) | Port storage always cheaper at this shuttle size |

| Metric | Case 1 | Case 2-1 | Case 2-2 | Ratio (Case 2/Case 1) |
|--------|--------|----------|----------|----------------------|
| NPC (USD M) | 290.81 | 879.88 | 700.68 | 3.02x / 2.41x |
| LCOA (USD/ton) | 1.23 | 3.73 | 2.97 | 3.03x / 2.41x |
| Shuttle vOPEX share | 18.9% | 33.4% | 39.2% | Distance-driven |

**Distinctiveness from literature:** Lloyd's Register and UMAS [7] estimated macro-level fuel transition costs but at resolution too coarse for port-specific decisions. Galan-Martin et al. [15] optimized ammonia distribution at intercontinental scale. Our analysis operates at the port-level granularity where the build-vs-source decision is actually made, with an explicit distance parameterization that produces a transferable decision rule.

---

## Contribution 3: Demand Scenario Analysis Demonstrating LCOA Stability

We demonstrate that the optimal shuttle vessel size remains unchanged across a four-fold range of demand scenarios (250 to 1,000 end-vessels), while LCOA varies by only $0.07/ton (5.7%) for Case 1. This finding has a direct practical implication: port authorities can commit to shuttle vessel specifications (2,500 m3 for Case 1) without waiting for demand uncertainty to resolve, because the sizing decision is insensitive to how many ammonia-fueled vessels ultimately enter service. In contrast, the fleet expansion *schedule* (when to add each shuttle) is demand-sensitive, meaning the timing of procurement -- but not the specifications -- requires demand monitoring.

**Gap filled:** Gap 3 -- No prior study models dynamic fleet expansion synchronized with demand growth for ammonia bunkering, or tests whether optimal specifications are robust to demand uncertainty.

**Evidence:**
- Fig. 13 (FIG10): NPC and LCO across 4 demand scenarios for all 3 cases
- Fig. 7 (D8): Fleet evolution showing cumulative shuttle additions over 21 years
- Fig. 8 (D3): Annual demand and fleet response showing step-function fleet growth
- Fig. 6 (D2): Annual cost evolution (2030--2050)
- Table: Demand scenarios summary CSV (`demand_scenarios_summary.csv`)

**Key quantitative results:**

| Scenario | End Vessels | Case 1 NPC (USD M) | Case 1 LCO (USD/ton) | Optimal Shuttle |
|----------|-----------|-------|--------|-----------------|
| Low | 250 | 164.48 | 1.28 | 2,500 m3 |
| Base | 500 | 290.81 | 1.23 | 2,500 m3 |
| High | 750 | 414.80 | 1.21 | 2,500 m3 |
| VeryHigh | 1,000 | 543.47 | 1.21 | 2,500 m3 |

LCO range: $1.21--$1.28/ton across 4x demand (5.7% variation). NPC scales near-linearly with demand, confirming constant marginal cost of fleet expansion. Optimal shuttle size is 2,500 m3 in all four scenarios.

**Distinctiveness from literature:** Bakkehaug et al. [14] modeled multi-period fleet renewal for bulk carriers under demand uncertainty but addressed conventional shipping without fuel-specific constraints. Our model introduces ammonia-specific cycle time coupling and tests whether the infrastructure specification (not just fleet size) is robust to demand uncertainty -- a question not posed in existing fleet sizing literature.

---

## Contribution 4: Differentiated Cost Driver Hierarchy Across Supply Chain Configurations

We identify that the parameter with the largest influence on total cost differs fundamentally between port-based storage and remote supply configurations. Through a six-parameter tornado analysis (+/-20%), we find that Case 1 (port storage) is most sensitive to the CAPEX scaling exponent (swing $180.34M, 62% of base NPC), while Cases 2-1 and 2-2 (remote supply) are most sensitive to bunker volume. This differentiation has a practical consequence: reducing infrastructure cost uncertainty for Case 1 requires tighter control of shipyard cost estimates, while for Case 2, the primary risk is demand-side (how much ammonia each vessel needs per call).

**Gap filled:** Supports Gaps 1 and 2 -- provides the sensitivity context needed to interpret optimal configurations and supply chain comparison results under parameter uncertainty.

**Evidence:**
- Fig. 10 (FIG7): Tornado diagrams for all 3 cases showing parameter ranking
- Fig. 11 (FIG8): Fuel price sensitivity showing NPC and LCO response ($300--$1,200/ton)
- Fig. S4 (FIGS4): Two-way sensitivity heatmap (fuel price x bunker volume, Case 1)
- Fig. S5 (FIGS5): Bunker volume sensitivity (NPC and LCO response)
- Table: Tornado CSVs (`tornado_det_case_*.csv`), fuel price CSVs (`fuel_price_case_*.csv`)

**Key quantitative results:**

| Parameter | Case 1 Swing (USD M) | Case 1 Swing (%) | Rank |
|-----------|---------------------|------------------|------|
| CAPEX Scaling Exponent | 180.34 | 62.0% | 1 |
| Bunker Volume | 134.95 | 46.4% | 2 |
| Max Annual Hours | 27.50 | 9.5% | 3 |
| Travel Time | 15.83 | 5.4% | 4 |
| Fuel Price | 35.74 | 12.3% | 5 |
| SFOC | 0.00 | 0.0% | 6 |

Case 1 fuel price range: NPC $255M--$362M across $300--$1,200/ton (37% variation). The SFOC swing of $0.0M is a structural artifact: SFOC values are fixed per shuttle size in the MCR map, so +/-20% variation does not change the optimal configuration.

**Distinctiveness from literature:** While tornado analysis is standard in TEA literature [4, 7], no prior study has compared parameter sensitivity *across fundamentally different supply chain topologies* for ammonia bunkering, revealing that the dominant cost uncertainty shifts from supply-side (CAPEX) to demand-side (bunker volume) as the supply chain extends geographically.

---

## Contributions Summary Table

| # | Contribution | Gap | Key Figure(s) | Key Metric |
|---|-------------|-----|--------------|------------|
| C1 | Optimal infrastructure specs through systematic parametric evaluation | Gap 1 | Fig. 2 (D1), Fig. 14 (S7) | Case 1: 2,500 m3, $290.81M, $1.23/ton |
| C2 | Break-even distance decision rule | Gap 2 | Fig. 12 (FIG9), Fig. 3 (D10) | Yeosu crossover ~59.6 nm; Ulsan no crossover |
| C3 | Demand scenario analysis demonstrating LCOA stability | Gap 3 | Fig. 13 (FIG10), Fig. 7 (D8) | LCO $1.21--$1.28/ton across 4x demand |
| C4 | Differentiated cost driver hierarchy | Gaps 1+2 | Fig. 10 (FIG7), Fig. 11 (FIG8) | Case 1: CAPEX Scaling 62%; Case 2: Bunker Volume dominant |

---

## Quality Gate Checklist

- [x] 3-5 contributions defined (4 contributions)
- [x] Each contribution maps to at least one figure and one CSV metric
- [x] Each contribution references a specific gap from Phase 1
- [x] No contribution is a restatement of methodology ("we use MILP" is not a contribution -- all contributions are framed as findings and decision tools)
- [x] No contribution lacks quantitative evidence mapping (all have specific USD M, USD/ton, %, nm values)
