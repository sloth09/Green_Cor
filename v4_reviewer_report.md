# Peer Review Report -- v4 Paper

---

## REVIEWER REPORT

**Manuscript**: "Optimal Ammonia Bunkering Infrastructure for Green Shipping Corridors: A Multi-Period Mixed-Integer Linear Programming Approach"

**Reviewer Expertise**: Maritime operations research, bunkering cost modeling, infrastructure investment optimization

**Date**: 2026-02-20

**Recommendation**: **Major Revision**

---

## 1. Summary of the Manuscript

This paper formulates a mixed-integer linear programming (MILP) model to optimize ammonia bunkering infrastructure (shuttle vessels, pumps, storage) at Busan Port over a 21-year horizon (2030--2050). Three supply chain configurations are compared: port-based storage (Case 1), remote supply from Ulsan at 59 nm (Case 2), and Yeosu at 86 nm (Case 3). The model enumerates shuttle-pump combinations and solves a fleet-sizing MILP for each, yielding NPC-optimal configurations. Seven sensitivity analyses and a comparison with a published DES model are included.

The paper addresses a timely and practically relevant problem. The comprehensive sensitivity analysis and the Yang & Lam DES comparison are commendable. However, several methodological and presentation issues must be addressed before the manuscript is suitable for publication in a SCI-indexed journal.

---

## 2. Major Issues (Must Address)

### M1. Overclaimed "Joint Optimization" of Pump Rate

The paper repeatedly claims to "jointly optimize" three coupled decision variables: shuttle size, pump flow rate, and fleet size (Abstract, Section 1.2 Gap 1, Contribution 1). However, the actual solution approach (Section 2.5) fixes the pump rate at 500 m3/h for the base case and enumerates shuttle sizes. Pump rate variation is explored only in a separate sensitivity analysis (Section 3.6), not as part of the optimization.

This is **parametric evaluation**, not joint optimization. A true joint formulation would include pump rate as a decision variable within the MILP (e.g., binary selection among candidate rates), or at minimum enumerate all (V_s, Q_p) pairs in the outer loop. The current description conflates sensitivity analysis with optimization.

**Required Action**: Either (a) reformulate to enumerate all (V_s, Q_p) pairs and report the global optimum over both dimensions, or (b) reframe the contribution to accurately state that shuttle size is selected parametrically and pump rate is analyzed via sensitivity. Option (a) is straightforward given the existing code and would genuinely strengthen Contribution 1. Option (b) is acceptable but requires revising the abstract, Gap 1, and all four contribution statements.

### M2. Annualization/Discounting Inconsistency

The paper uses a 7% annualization interest rate (r = 0.07) to convert CAPEX to equivalent annual payments (Eq. 19, AF = 10.8355), while simultaneously assuming zero discounting (delta = 0, Assumption A2) for NPC summation.

This creates an internal inconsistency: the annualization implicitly assumes a 7% cost of capital (CAPEX is spread with interest), but the NPC summation treats all years as equally weighted (no time-value adjustment). The net effect inflates the effective CAPEX cost relative to OPEX. Specifically, a shuttle purchased for $3.87M in 2030 generates annualized payments of $0.357M/year x 21 years = $7.50M in cumulative NPC -- nearly double the actual purchase price.

When discounting is introduced (Section 3.9), the paper applies the discount rate to the total annual cost (annualized CAPEX + OPEX), creating potential double-counting: CAPEX is first inflated via annualization at 7%, then partially deflated via discounting.

**Required Action**:
- Clarify explicitly in Section 2.4.4 that the annualization rate represents the financing cost of capital (debt/equity blend), separate from the social discount rate used for project evaluation.
- Discuss the interaction between annualization rate and discount rate. When delta > 0, the net effect on CAPEX should be explained.
- Consider running a sensitivity on the annualization rate itself (e.g., 5%, 7%, 10%) to show whether optimal specifications are robust to this assumption.

### M3. Undocumented Constraint: Maximum Call Duration (80h)

The paper's MILP formulation (Section 2.3.3, Eqs. 10--14) includes four constraints: fleet inventory balance, demand satisfaction, working time capacity, and tank capacity. However, the implementation includes a fifth constraint -- maximum call duration of 80 hours -- that silently excludes infeasible (V_s, Q_p) combinations before the MILP is solved.

This constraint is operationally important: it is the binding constraint that causes infeasibility in the tornado analysis when bunker volume increases by 20% (Section 3.7, Table 7). Yet it appears nowhere in the formal problem statement.

**Required Action**: Add the call duration constraint to Section 2.3.3:

$$n_{\text{trip}} \times T_{\text{cycle}} \leq T_{\text{max,call}}, \quad T_{\text{max,call}} = 80 \text{ h}$$

Explain its physical meaning (maximum acceptable waiting time for a receiving vessel) and discuss its origin (regulatory requirement, operational practice, or assumption).

### M4. Terminal Value / Asset Life Mismatch

The planning horizon (21 years, 2030--2050) is equated with the asset annualization period (n = 21 in Eq. 19). A shuttle purchased in 2045 is annualized over 21 years, but only 6 years of operation fall within the planning horizon. The remaining 15 years of annualized payments contribute to NPC but the corresponding demand fulfillment is not captured.

This systematically penalizes late-period shuttle additions, potentially distorting the optimal fleet expansion timing. It also means NPC overestimates the true cost of shuttles purchased in later years.

**Required Action**: Either (a) annualize each shuttle over its actual remaining service life within the horizon (min(asset_life, 2050 - purchase_year + 1)), or (b) use a salvage value / terminal value correction for assets purchased late in the horizon, or (c) acknowledge this as a limitation with a direction-of-error estimate. Option (c) is acceptable but should include a quantitative bound (e.g., "late-period shuttles purchased after 2045 contribute approximately X% of total NPC; their effective cost is overestimated by Y%").

### M5. Paper Length and Redundancy

The manuscript is approximately 12,000--14,000 words with 18 figures and 10 tables. Most target journals (Ocean Engineering, Transportation Research Part D) have word limits of 8,000--10,000 words and 10--12 figures.

Specific redundancies:
- The break-even finding is stated with nearly identical wording in the Abstract, Contribution 2, Section 4.1, and Section 5.
- Internal figure codes (D1, D10, S7, FIG7, etc.) appear throughout and should be removed.
- Sections 3.1--3.5 each contain extensive numerical examples that repeat Table 5 values. Some can be consolidated.
- The worked examples in Section 2.2 (cycle time calculations) are valuable but could move to supplementary material.

**Required Action**: Reduce to 9,000--10,000 words. Move supplementary details (worked examples, extended sensitivity tables) to an appendix or online supplement. Remove all internal figure codes. Consolidate Tables 1 and 5.

---

## 3. Minor Issues (Should Address)

### m1. LCOA Terminology Ambiguity

LCOA is defined as "Levelized Cost of Ammonia bunkering" but the formula (Eq. 26) computes the cost of *delivering* ammonia, not the cost of ammonia itself. Readers may confuse this with the total delivered cost including ammonia procurement (~$600/ton). Consider renaming to "Levelized Cost of Ammonia Delivery" (LCOAD) or "Levelized Bunkering Service Cost" (LBSC) to avoid ambiguity.

### m2. Peak Factor F_peak Confusion

Assumption A4 mentions F_peak = 1.5 but explicitly states it is NOT used in the current formulation. This is confusing. Either remove the mention entirely or explain why it is defined but unused (e.g., "reserved for future queuing extension").

### m3. Break-Even Analysis Configuration

The main break-even analysis (Section 4.1) compares Case 1 at 5,000 m3 shuttle versus Cases 2/3 at varying distances. However, Case 1's optimal shuttle is 1,000 m3. The "optimal-vs-optimal" comparison appears as a secondary paragraph. For a fair comparison, the primary analysis should use each case's optimal configuration, with the same-shuttle comparison as a supplementary robustness check.

### m4. Discount Rate Effect on LCOA

Table 9 and Section 3.9 show LCOA declining from $1.90/ton to $0.77/ton as discount rate increases from 0% to 8%. This is mathematically correct (numerator is discounted but denominator -- physical tons -- is not) but economically misleading. A declining LCOA with higher discount rate suggests "ammonia delivery gets cheaper if we value money more," which is counterintuitive. Consider discounting both numerator and denominator, or reporting LCOA only for the base case and presenting discount rate effects solely through NPC.

### m5. SFOC and Fuel Price Identical Tornado Swings

The tornado analysis (Table 7) shows SFOC and Fuel Price produce identical swings ($39.00M, 8.7%). While correctly explained (both scale fuel cost linearly), this means only one of the two is an independent parameter. Consider combining them as a single "fuel cost" parameter in the tornado, or noting explicitly that they are perfectly correlated in this model.

### m6. Reference Numbering

Reference numbers do not appear in sequential order of first citation. For example, [5] and [29] appear in the first paragraph, then [1, 2] in the next. Most journals require sequential numbering. Renumber references in order of first appearance.

### m7. Missing Sensitivity: Shore Pump Rate

The shore pump rate (Q_shore = 700 m3/h) significantly affects Case 1 cycle time but is not included in the tornado analysis. Given that shore loading time is a major cycle time component (5.43 h out of 13.43 h for the 1,000 m3 shuttle), this parameter deserves sensitivity testing.

### m8. Total Ammonia Volume Verification

The paper states total ammonia supply of 235,620,000 tons (Section 3.5). An independent calculation using the stated parameters (50--500 vessels, 21 years, 12 voyages/year, 5,000 m3/call, 0.681 ton/m3) yields approximately 235,967,000 tons. The discrepancy (~0.15%) suggests a rounding issue in the linear interpolation of vessel counts. Verify and correct.

---

## 4. Specific Technical Comments

### T1. Equation (20) Clarification

The annualized CAPEX formula (Eq. 20) divides the *cumulative* asset cost by the annuity factor. This means that in year t, the annual CAPEX payment reflects ALL shuttles purchased from 2030 to year t. However, standard annualization treats each asset independently from its purchase date. Please clarify: does the implementation annualize each shuttle from its purchase year, or does it treat all shuttles as if purchased in 2030? If the latter, late-purchased shuttles are over-annualized (see M4).

### T2. Equation (8) -- Trips Per Call for Remote Supply

Equation (8) defines n_trip = 1/N_v for Cases 2/3. While the explanation is correct (shared shuttle capacity), the notation is unconventional. For N_v = 1 (optimal case), n_trip = 1, which is intuitive. But for N_v = 2, n_trip = 0.5, meaning "half a trip per call." Consider reformulating as "shuttle trips required per call = ceiling(v_call / V_s)" uniformly across all cases, which equals the same values but is more intuitive.

### T3. Table 6 -- Missing Shore Supply / Tank Costs

Table 6 decomposes NPC into six components, but Case 1 includes tank storage and shore supply infrastructure. Are tank CAPEX, tank fOPEX, and cooling costs included in the listed components? If so, under which line items? If tank costs are subsumed into "Shuttle CAPEX" or "Bunkering CAPEX," this should be made explicit. The current breakdown may understate the cost advantage of Cases 2/3 (which have no tank costs).

### T4. Section 4.4 -- DES Comparison Gap Attribution

The 4.6--5.9% gap between MILP and DES service times is attributed to "operational overhead (mooring ~1.55h and documentation ~0.84h)." These specific numbers (1.55h, 0.84h) need sourcing. Are they from Yang & Lam's paper, estimated by the authors, or calibrated to minimize the gap? If calibrated, this is a post-hoc adjustment that weakens the validation claim.

### T5. Sensitivity Range Justification

The +/-20% range for tornado analysis is standard but arbitrary. For the CAPEX scaling exponent (alpha = 0.75), a +/-20% variation means testing alpha = 0.60 to 0.90. The literature on vessel cost scaling reports alpha values from 0.6 to 0.85 (Stopford, 2009; Clarksons Research). The upper bound of 0.90 may exceed realistic values, inflating the apparent sensitivity. Consider using literature-justified ranges rather than uniform +/-20% for all parameters.

---

## 5. Positive Aspects

Despite the issues above, the manuscript has substantial merit:

1. **Timely topic**: Ammonia bunkering infrastructure is a genuine planning need with no existing quantitative framework. The paper fills a real gap.

2. **Comprehensive sensitivity analysis**: Seven sensitivity dimensions (tornado, fuel price, bunker volume, two-way, demand scenarios, break-even distance, discount rate) exceed what most comparable papers provide. The demand scenario invariance finding (3.7% LCOA variation across 4x demand) is genuinely useful.

3. **Quantitative DES comparison**: The Yang & Lam comparison (Section 4.4) with specific validation points and gap attribution is well-executed and positions the MILP within the existing literature.

4. **Transparent assumptions**: The seven assumptions (A1--A7 across the Limitations section) with direction-of-error estimates and magnitude assessments demonstrate methodological rigor.

5. **Reproducible formulation**: The cycle time model is fully specified with worked examples, enabling independent verification. This is a strength for an infrastructure planning paper.

6. **Actionable recommendations**: The three recommendations (build local storage, fix pump rate first, monitor CAPEX uncertainty) are specific, justified by the analysis, and relevant to the Korea--US green corridor initiative.

7. **Literature coverage**: 43 references with thematic organization across five domains (alternative fuels, green corridors, ammonia safety, fleet sizing MILP, LNG bunkering) is thorough.

---

## 6. Recommendation to Editor

**Decision: Major Revision**

The paper addresses a timely and relevant problem with a well-executed comparative analysis of ammonia bunkering infrastructure options. The sensitivity analysis depth and DES comparison distinguish it from a simple optimization exercise. However, five major issues must be resolved:

1. The "joint optimization" claim must be either substantiated (by actually enumerating all V_s x Q_p pairs) or reframed (M1).
2. The annualization/discounting interaction must be clarified (M2).
3. The missing 80h call duration constraint must be added to the formulation (M3).
4. Terminal value treatment needs addressing (M4).
5. The paper must be shortened to journal word limits (M5).

Issues M1 and M3 are the most critical: M1 affects the paper's central contribution claim, and M3 affects reproducibility of the MILP formulation. Both are addressable within a standard revision cycle.

After addressing these issues, the paper would be competitive for mid-tier SCI journals such as **Ocean Engineering**, **Transportation Research Part D**, or **Applied Energy**.

---

## 7. Summary Table for v5 Revision

| Issue | ID | Priority | Estimated Effort | Impact on Acceptance |
|-------|-----|----------|-----------------|---------------------|
| Reframe or substantiate "joint optimization" | M1 | Critical | Low (reframe) or Medium (rerun) | High |
| Clarify annualization vs. discounting | M2 | Critical | Low (text) or Medium (add sensitivity) | High |
| Add call duration constraint to formulation | M3 | Critical | Low | High |
| Address terminal value / asset life | M4 | Major | Low-Medium | Medium |
| Reduce paper length to ~10,000 words | M5 | Major | Medium | Medium |
| Fix LCOA terminology | m1 | Minor | Low | Low |
| Remove or clarify F_peak | m2 | Minor | Low | Low |
| Restructure break-even as optimal-vs-optimal | m3 | Minor | Low | Medium |
| Fix LCOA under discounting | m4 | Minor | Low-Medium | Low |
| Combine SFOC/Fuel Price in tornado | m5 | Minor | Low | Low |
| Sequential reference numbering | m6 | Minor | Low | Low |
| Add shore pump rate sensitivity | m7 | Minor | Medium | Low |
| Verify total ammonia volume | m8 | Minor | Low | Low |
| Clarify Eq. (20) annualization scope | T1 | Technical | Low | Medium |
| Reformulate Eq. (8) notation | T2 | Technical | Low | Low |
| Clarify Table 6 tank/shore costs | T3 | Technical | Low | Medium |
| Source DES gap attribution values | T4 | Technical | Low | Medium |
| Justify tornado sensitivity ranges | T5 | Technical | Low-Medium | Low |

---

*End of Review*
