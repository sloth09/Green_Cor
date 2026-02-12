# Academic Writing Rules: Anti-Shallow Writing Protocol

These 8 rules prevent "A is A"-level shallow writing. Every sentence in the paper must pass at least one of these rules. Apply them during drafting (Phase 5-9) and during review (`/paper-writer review`).

---

## Rule 1: Specificity Obligation

Every claim about results MUST include at least one specific number from the data.

| BAD | GOOD |
|-----|------|
| "Case 1 is more economical than Case 2." | "Case 1 NPC of $[NPC_c1]M is [X]% of Case 3's $[NPC_c3]M, primarily due to eliminating [distance] nmi round-trip transit." |
| "The optimal shuttle is relatively small." | "The optimal shuttle for Case 1 is [size] m3, the smallest in the candidate set that can complete a bunkering call in [N] trips rather than [N+1]." |
| "Costs increase over the planning horizon." | "Annual total cost rises from $[cost_2030]M (2030) to $[cost_2050]M (2050), a CAGR of [Y]%, driven primarily by fleet expansion from [N_start] to [N_end] shuttles." |

**Test:** Remove the number. Does the sentence still say something meaningful? If yes, the number is decoration. If no, it is structural. Only structural numbers count.

---

## Rule 2: So-What Test

After every factual statement, ask: "So what does this mean for the decision-maker?" If you cannot answer, the statement is incomplete.

| BAD | GOOD |
|-----|------|
| "The optimal shuttle size is [X] m3." | "The [X] m3 optimal shuttle is compatible with existing Busan Port berth infrastructure (max LOA 90m), avoiding costly terminal modifications." |
| "Fleet utilization averages [X]%." | "Average utilization of [X]% leaves only [Y] hours/year of slack per shuttle, suggesting that even modest demand surges could trigger fleet shortages." |
| "Case 2 has higher variable OPEX." | "Case 3's variable OPEX ($[vOPEX]M, [X]% of NPC) makes it highly sensitive to fuel price fluctuations, creating hedging requirements absent in Case 1." |

**Test:** Does the sentence help someone make a decision? If it only states a fact without consequence, add the consequence.

---

## Rule 3: No Tautology

Never explain results by restating the objective function or the definition.

| BAD | GOOD |
|-----|------|
| "The optimal solution minimizes cost because it has the lowest NPC." | "The [optimal_size] m3 shuttle achieves the lowest NPC because CAPEX scaling (exponent 0.75) yields diminishing cost savings beyond this size, while the reduction in annual cycles fails to offset the CAPEX increase." |
| "Larger shuttles carry more ammonia per trip." | "Doubling shuttle size from [X] to [2X] m3 halves required trips per call but increases cycle time by [Y]% ([T1] to [T2] hr), yielding a net [Z]% NPC increase." |
| "The model finds the optimal fleet size for each year." | "Fleet expansion follows a staircase pattern, adding [N] shuttles in years when cumulative demand exceeds capacity by more than one cycle's worth of supply." |

**Test:** Can the sentence be derived purely from definitions without looking at data? If yes, it is tautological.

---

## Rule 4: Figure Analysis Protocol

When referencing a figure, you MUST do ALL THREE:
1. **Describe** what the figure shows (pattern, trend, shape)
2. **Quantify** the key observation (with numbers)
3. **Explain** why the pattern exists (causal mechanism)

| BAD | GOOD |
|-----|------|
| "Fig. 2 shows the NPC for different shuttle sizes." | "Fig. 2 reveals a convex NPC curve for all three cases, with Case 1 exhibiting the shallowest U-shape ($[min]M-$[max]M range) compared to Case 3's steep descent from $[NPC_high]M at [size_high] m3 to $[NPC_low]M at [size_low] m3. The asymmetry arises because undersized shuttles incur cycle-count penalties (more trips), while oversized shuttles suffer from CAPEX scaling (0.75 exponent) and reduced annual cycle capacity." |
| "Fig. 5 presents the cost breakdown." | "Fig. 5 shows that shuttle CAPEX dominates Case 1 costs ([X]% of NPC), while variable OPEX dominates Case 3 ([Y]%), reflecting the fundamental trade-off between capital-intensive local storage and operations-intensive remote supply." |

**Test:** Cover the figure. Can the reader reconstruct the key insight from your text alone? If not, add more description/quantification.

---

## Rule 5: Comparison Obligation

Every result for one case MUST be compared with at least one of:
- Another case in this study
- A literature value
- A theoretical bound or benchmark

| BAD | GOOD |
|-----|------|
| "The LCOA for Case 1 is $[X]/ton." | "Case 1 LCOA of $[LCOA_c1]/ton is [X]% lower than Case 3 ($[LCOA_c3]/ton) and [Y]% lower than Case 2 ($[LCOA_c2]/ton). This advantage narrows if port storage costs (excluded from Case 1) are internalized." |
| "The annualized cost is $[X]M/year." | "The annualized cost of $[ann_cost]M/year for Case 1 represents [X]% of Busan Port's annual throughput value (est. $24B), suggesting ammonia bunkering infrastructure is economically marginal relative to existing port operations." |

**Test:** Is the number floating alone, or is it anchored to a reference point?

---

## Rule 6: No Orphan Claims

Every assertion must be traceable to one of:
- A specific CSV value (cite column and row)
- A specific figure (cite figure number)
- A specific reference (cite author and year)
- A mathematical derivation (show the equation)

| BAD | GOOD |
|-----|------|
| "The model demonstrates good scalability." | "Fleet sizing scales linearly with demand: the optimal Case 1 fleet grows from [N_start] shuttles (2030, [calls_start] calls/year) to [N_end] shuttles (2050, [calls_end] calls/year), maintaining utilization above [X]% throughout (Fig. 7, Table 3)." |
| "This approach is novel." | "Unlike Al-Enazi et al. (2021) who assumed fixed fleet sizes, our MILP formulation optimizes fleet expansion timing jointly with shuttle sizing, capturing the [X-Y]% cost reduction from deferred investment (Table 5)." |

**Test:** Can the reader verify this claim using information available in the paper? If not, it is an orphan.

---

## Rule 7: Transition Obligation

Every paragraph must connect to the next. The last sentence of each paragraph should either:
- Preview the next topic
- Raise a question that the next paragraph answers
- Show how the current finding leads to the next analysis

| BAD (abrupt ending) | GOOD (transition) |
|---------------------|-------------------|
| "The optimal shuttle size for Case 1 is 2,500 m3." [New paragraph starts new topic] | "While 2,500 m3 minimizes NPC for Case 1, this conclusion assumes a fixed pump rate of 1,000 m3/h. Section 4.6 examines how pump rate variation affects both optimal shuttle sizing and total cost." |
| "Fleet utilization averages 92% across the planning horizon." | "This high average utilization masks significant year-to-year variation, with early years showing excess capacity and later years approaching operational limits, as detailed in the temporal analysis below." |

**Test:** Remove the transition sentence. Does the reader feel a jarring topic shift? If yes, the transition was doing its job.

---

## Rule 8: Limitation Honesty

For every assumption in the model, acknowledge:
1. **What** the assumption is
2. **Why** it was made (practical reason)
3. **How** relaxing it would affect results (direction and magnitude if possible)

| BAD | GOOD |
|-----|------|
| "We assume a fixed fuel price." | "We assume a fixed ammonia fuel price of $[price]/ton throughout the planning horizon. This simplification avoids forecasting uncertainty but likely underestimates NPC for Case 2 scenarios, where variable OPEX ([X]% of NPC) is directly proportional to fuel cost. A +30% price increase would raise Case 3 NPC by approximately $[Y]M ([Z]%) versus only $[W]M ([V]%) for Case 1." |
| "The model uses a deterministic demand forecast." | "Demand is modeled as a deterministic linear increase from [start] to [end] vessels. Actual adoption may follow an S-curve, with slower early growth and potential acceleration post-2040. Under S-curve demand, early-year fleet oversizing (currently [N] excess shuttles) would persist longer, increasing capital lock-up by an estimated [X-Y]%." |

**Test:** Would a reviewer flag this as an unacknowledged limitation? If yes, you must address it.

---

## Application Protocol

### During Drafting (Phases 5-9)
1. After writing each paragraph, mentally check all 8 rules
2. Pay special attention to:
   - Rule 1 (Specificity) for Results section
   - Rule 4 (Figure Protocol) whenever a figure is referenced
   - Rule 5 (Comparison) for Discussion section
   - Rule 8 (Limitations) for Methodology and Discussion

### During Review (`/paper-writer review`)
1. Read each paragraph
2. Flag violations with rule number: `[RULE-3 VIOLATION]`
3. Provide specific fix suggestion with data from CSV
4. Count total violations per section
5. Report: section name, violation count, severity (critical/minor)

### Severity Classification
| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Claim without evidence, tautology, or factual error | Rule 3, 6 violations |
| **Major** | Missing quantification or comparison | Rule 1, 5 violations |
| **Minor** | Missing transition or incomplete so-what | Rule 2, 7 violations |

### Quality Gate Threshold
- **PASS:** 0 critical, <= 2 major per section
- **REVISE:** Any critical violation or > 2 major per section
- **REWRITE:** > 3 critical violations in any section
