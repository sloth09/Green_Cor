## 3. Results and Analysis

## 3.1 Optimal Configurations

The MILP model identifies distinct optimal shuttle-pump configurations for each supply chain case, reflecting the structural cost differences between port-based storage and remote supply (Table 5).

**Table 5: Optimal configurations for three supply chain cases**

| Parameter | Case 1 (Busan) | Case 3 (Yeosu) | Case 2 (Ulsan) |
|-----------|:-------------:|:-----------------:|:-----------------:|
| Optimal shuttle size (m$^3$) | 2,500 | 5,000 | 5,000 |
| Pump rate (m$^3$/h) | 1,000 | 1,000 | 1,000 |
| NPC (USD M) | 410.34 | 1,014.81 | 830.65 |
| LCOA (USD/ton) | 1.74 | 4.31 | 3.53 |
| Cycle time (h) | 16.07 | 34.60 | 31.00 |
| Annual cycles max | 497.78 | 231.19 | 258.04 |
| Vessels per trip | 1 | 1 | 1 |
| Annualized cost (M/yr) | 37.87 | 93.66 | 76.66 |

Fig. 2 (D1) shows the NPC as a function of shuttle size for all three cases. Each curve exhibits a piecewise cost landscape shaped by the integer-valued trip count $n_{\text{trip}}$ (Eq. 4), with a global minimum at an interior point. For Case 1, the 500 m$^3$ shuttle is infeasible: a bunkering call requires $n_{\text{trip}} = \lceil 5{,}000/500 \rceil = 10$ trips, yielding a call duration of $10 \times 11.21 = 112.1$ h, which exceeds the maximum allowable call duration of 80 h. Consequently, the NPC curve for Case 1 begins at 1,000 m$^3$. NPC decreases from $433.41M at 1,000 m$^3$ to $410.34M at 2,500 m$^3$ (global minimum), then rises steeply to higher values at intermediate sizes before dropping to $441.25M at 5,000 m$^3$ where $n_{\text{trip}}$ decreases from 2 to 1. This discontinuity creates a secondary local minimum at 5,000 m$^3$, only 7.5% above the global optimum -- a configuration worth considering if operational simplicity (single trip per call) is valued. The asymmetry arises from two competing effects: undersized shuttles incur cycle-count penalties, while oversized shuttles suffer from CAPEX scaling. The CAPEX scaling exponent ($\alpha = 0.75$) means that doubling shuttle capacity increases unit cost by $2^{0.75} = 1.68\times$ rather than $2\times$, producing diminishing savings that are eventually overwhelmed by the absolute cost increase.

For Case 3 (Yeosu), the optimal is 5,000 m$^3$ -- the same size as Case 2 (Ulsan). At this shuttle size, $N_v = \lfloor 5{,}000/5{,}000 \rfloor = 1$ vessel is served per trip. Unlike the previous expectation that larger shuttles would be preferred for longer distances to amortize the 5.73-hour one-way travel time over more delivered volume, the 5,000 m$^3$ shuttle proves more efficient because the shore loading time for a 10,000 m$^3$ shuttle ($10{,}000/1{,}500 + 2.0 = 8.67$ h) substantially increases cycle time, offsetting the travel-cost amortization benefit of serving two vessels per trip. For Case 2 (Ulsan), the 5,000 m$^3$ optimum reflects the shorter travel distance (3.93 h one-way), where the cycle time penalty of larger shuttles is similarly prohibitive.

Fig. 3 (D10) confirms the cross-case cost hierarchy: Case 3 NPC is $2.47\times$ Case 1, and Case 2 is $2.02\times$ Case 1. This ordering holds across all shuttle sizes, indicating that the port-based storage advantage is structural rather than configuration-dependent. The LCOA metric normalizes for total supply volume: at $1.74/ton (Case 1) versus $4.31/ton (Case 3), the per-ton cost of remote supply from Yeosu is $2.57/ton higher, representing a premium of 148%.

---

## 3.2 Temporal Dynamics

The MILP produces year-indexed fleet expansion schedules that reveal the discrete, lumpy nature of infrastructure investment. Fig. 7 (D8) shows cumulative fleet size over the 21-year planning horizon. For Case 1 (2,500 m$^3$ shuttle), the fleet grows in discrete steps from 3 shuttles in 2030 to 25 by 2050 as demand crosses capacity thresholds defined by Eq. (12). Each new shuttle adds 497.78 annual cycles of capacity (at $H_{\max} = 8{,}000$ h/year and $T_{\text{cycle}} = 16.07$ h), equivalent to serving approximately 249 additional bunkering calls per year (since $n_{\text{trip}} = 2$).

Fig. 8 (D3) overlays annual bunkering demand with fleet supply capacity. The demand curve is smooth (linear growth), while the supply curve follows a staircase pattern. The gap between supply capacity and demand represents fleet slack -- periods of overcapacity immediately following a shuttle addition, which erodes as demand catches up.

Fig. 6 (D2) shows the annual cost evolution from 2030 to 2050. Cost growth exhibits a step function correlated with fleet additions: each new shuttle triggers a jump in annualized CAPEX ($C_{\text{shuttle}} / \text{AF} = 7.69M / 10.8355 = 0.710$M/year for a 2,500 m$^3$ shuttle) plus fixed OPEX. Between fleet additions, annual cost growth is driven solely by increasing variable OPEX as the number of bunkering calls rises with demand. This yields two distinct growth regimes: CAPEX-driven jumps at fleet expansion years, and vOPEX-driven gradual increases between them.

---

## 3.3 Operational Efficiency

Fig. 9 (D5) reveals a sawtooth utilization pattern over time. Utilization climbs as demand grows against a fixed fleet, reaching a peak just before the next shuttle addition, then drops when new capacity enters service. For Case 1, utilization ranges from approximately 73% immediately after shuttle additions to 99% just before the next addition, a sawtooth amplitude of 26 percentage points. This pattern confirms that the MILP adds shuttles at the minimum necessary rate -- just in time to prevent the working-time constraint (Eq. 12) from becoming infeasible.

For Case 1, the theoretical maximum utilization is 100% ($\text{Annual\_Cycles\_Max} = H_{\max} / T_{\text{cycle}} = 8{,}000 / 16.07 = 497.78$, so the fleet operates at the $H_{\max} = 8{,}000$ h constraint boundary). In practice, the ceiling is lower because annual calls must be integer-compatible with demand. The high theoretical utilization means the fleet operates near capacity for much of the horizon, which minimizes capital idle time but leaves limited buffer for demand surges -- a consideration for risk-averse planners (see Section 4.5).

---

## 3.4 Cost Structure

Fig. 4 (D6) decomposes NPC into six components for each case at optimal configurations. The cost structure differs fundamentally between Case 1 and Case 2:

**Table 6: NPC cost breakdown at optimal configurations (USD M)**

| Component | Case 1 | % | Case 3 | % | Case 2 | % |
|-----------|-------:|--:|--------:|--:|--------:|--:|
| Shuttle CAPEX | 205.04 | 49.97 | 368.69 | 36.33 | 332.90 | 40.08 |
| Bunkering CAPEX | 14.62 | 3.56 | 20.11 | 1.98 | 18.16 | 2.19 |
| Shuttle fOPEX | 111.08 | 27.07 | 199.75 | 19.68 | 180.36 | 21.71 |
| Shuttle vOPEX | 55.01 | 13.40 | 400.97 | 39.51 | 275.01 | 33.11 |
| Bunkering fOPEX | 7.92 | 1.93 | 10.90 | 1.07 | 9.84 | 1.18 |
| Bunkering vOPEX | 16.67 | 4.06 | 14.39 | 1.42 | 14.39 | 1.73 |
| **Total NPC** | **410.34** | **100** | **1,014.81** | **100** | **830.65** | **100** |

Case 1 is capital-intensive: shuttle CAPEX ($205.04M, 49.97%) and shuttle fOPEX ($111.08M, 27.07%) together account for 77.0% of NPC, while shuttle vOPEX is only 13.4% ($55.01M). This reflects the short travel distance (1.0 h one-way), which minimizes fuel consumption per cycle.

Cases 2-1 and 2-2 are operations-intensive: shuttle vOPEX rises to 39.5% ($400.97M) and 33.1% ($275.01M) respectively, driven by the longer round-trip travel times (11.46 h for Yeosu, 7.86 h for Ulsan) and correspondingly higher fuel consumption per cycle. The vOPEX increase from Case 1 to Case 3 is $345.96M -- representing the cumulative fuel cost of traversing 172 nm (86 nm round trip) per shuttle cycle over 21 years. This structural shift from CAPEX-dominated to vOPEX-dominated cost has practical consequences: Case 1 costs are front-loaded (CAPEX at procurement) and predictable, while Case 2 costs are distributed over the operating life and sensitive to fuel price fluctuations.

---

## 3.5 LCOA Comparison

Fig. 5 (D9) presents LCOA across all cases. Case 1 achieves $1.74/ton, which represents the minimum unit cost of ammonia delivery from storage to vessel. Case 3 at $4.31/ton is 148% higher, and Case 2 at $3.53/ton is 103% higher. These differences persist across all shuttle size configurations, confirming that the cost advantage is structural (driven by travel distance and cycle time) rather than incidental.

The total ammonia supply over the 21-year horizon (2030--2050) is identical across all three cases ($235{,}620{,}000$ tons), because all share the same demand trajectory (50 to 500 vessels, 12 voyages/year, 5,000 m$^3$/call). The annualized cost ranges from $37.87M/year (Case 1) to $93.66M/year (Case 3), indicating that the additional annual cost of sourcing from Yeosu rather than local storage is $55.79M/year.

---

## 3.6 Pump Rate Sensitivity

Fig. 14 (S7) shows how NPC responds to pump rate variation from 100 to 1,500 m$^3$/h. For Case 1, NPC decreases substantially as pump rate increases from the low end of the range, with the relationship exhibiting strong concavity: the marginal benefit of pump rate increases falls rapidly at higher flow rates. At the baseline pump rate of 1,000 m$^3$/h, further pump rate investment yields diminishing returns for all three cases.

The optimal shuttle size remains 2,500 m$^3$ across all pump rates above a threshold for Case 1. At very low pump rates, the optimal shifts to smaller shuttles because the low pump rate creates extremely long cycle times for larger shuttles ($T_{\text{pump}} = 2{,}500/Q_p$ grows rapidly as $Q_p$ decreases), making smaller, faster shuttles more cost-effective despite requiring more trips. This interaction between pump rate and optimal shuttle size demonstrates the coupling identified in Gap 1.

---

## 3.7 Parametric Sensitivity

### Tornado Analysis

Fig. 10 (FIG7) presents tornado diagrams showing the NPC swing from +/-20% variation of six parameters. For Case 1:

**Table 7: Tornado sensitivity ranking (Case 1, base NPC = $410.34M)**

| Rank | Parameter | Low NPC (USD M) | High NPC (USD M) | Swing (USD M) | Swing (%) |
|:----:|-----------|:---------------:|:-----------------:|:-------------:|:---------:|
| 1 | CAPEX Scaling Exponent | 299.55 | 578.26 | 278.71 | 67.9 |
| 2 | Bunker Volume | 407.01 | 605.24 | 198.23 | 48.3 |
| 3 | Max Annual Hours | 356.43 | 492.37 | 135.94 | 33.1 |
| 4 | Travel Time | 392.31 | 429.55 | 37.24 | 9.1 |
| 5 | Fuel Price | 396.00 | 424.68 | 28.68 | 7.0 |
| 6 | SFOC | 396.00 | 424.68 | 28.68 | 7.0 |

The CAPEX scaling exponent dominates Case 1 sensitivity, with a swing of $278.71M (67.9% of base NPC). This occurs because $\alpha$ enters the cost function exponentially (Eq. 15): reducing $\alpha$ from 0.75 to 0.60 (i.e., $-20\%$) substantially flattens the CAPEX curve, making larger shuttles cheaper, while increasing to 0.90 steepens it, penalizing all but the smallest sizes. Bunker volume ranks second ($198.23M, 48.3%) because it directly determines both annual demand and per-call logistics.

SFOC and Fuel Price produce identical swings ($28.68M, 7.0%) for Case 1 because both scale shuttle fuel costs (Eq. 23) proportionally: a 20% SFOC increase has the same NPC effect as a 20% fuel price increase. The moderate magnitude reflects Case 1's low variable OPEX share (13.4% of NPC, Table 6), which limits the leverage of any fuel-cost parameter. Note that the SFOC sensitivity is evaluated at the optimal shuttle size, where the engine type classification (Table 3) assigns a fixed SFOC value. Because the +/-20% perturbation does not change the shuttle size or its engine class, the SFOC swing reflects only the proportional fuel cost effect without triggering a discrete engine-class transition.

For Case 3 (Yeosu, base NPC = $1,014.81M), bunker volume becomes the top-ranked parameter with a swing of $803.83M (75.5%), followed by CAPEX scaling ($312.37M, 29.4%) and maximum annual hours ($300.56M, 28.2%). For Case 2 (Ulsan, base NPC = $830.65M), bunker volume similarly dominates with a swing of $847.24M (102.0%), followed by CAPEX scaling ($335.16M, 40.3%) and maximum annual hours ($217.27M, 26.2%). The shift in sensitivity ranking across cases -- from CAPEX-driven (Case 1) to demand-driven (Case 2) -- mirrors the cost structure shift observed in Section 3.4.

### Fuel Price Sensitivity

Fig. 11 (FIG8) shows NPC and LCOA response to fuel price across $300--$1,200/ton. For Case 1, NPC ranges from $374.50M ($300/ton, $-8.7\%$) to $482.02M ($1,200/ton, $+17.5\%$). The response is linear, consistent with fuel cost being a constant fraction of NPC (vOPEX = 13.4% at baseline). LCOA scales linearly from $1.59/ton to $2.05/ton.

Case 2 configurations exhibit steeper fuel price sensitivity, consistent with their higher vOPEX shares (33--40%). At $1,200/ton, the Case 3 to Case 1 NPC ratio widens further, reinforcing the port-based storage advantage under high fuel price scenarios.

---

## 3.8 Demand Scenario Analysis

Fig. 13 (FIG10) compares NPC and LCOA across four demand scenarios (Table 8).

**Table 8: Demand scenario results (all cases)**

| Scenario | End Vessels | Case 1 NPC (M) | Case 1 LCOA | Case 3 NPC (M) | Case 3 LCOA | Case 2 NPC (M) | Case 2 LCOA |
|----------|:---------:|:-------------:|:----------:|:----------------:|:------------:|:----------------:|:------------:|
| Low | 250 | 230.11 | 1.79 | 562.18 | 4.37 | 462.43 | 3.60 |
| Base | 500 | 410.34 | 1.74 | 1,014.81 | 4.31 | 830.65 | 3.53 |
| High | 750 | 591.74 | 1.73 | 1,471.33 | 4.29 | 1,196.94 | 3.49 |
| VeryHigh | 1,000 | 771.98 | 1.72 | 1,922.03 | 4.27 | 1,567.10 | 3.48 |

Two findings are central:

**Finding 1: LCOA stability.** Case 1 LCOA ranges from $1.72 to $1.79/ton across a 4$\times$ demand variation (250 to 1,000 end-vessels), a variation of only 4.0% ($0.07/ton). This near-constant marginal cost arises because the MILP scales fleet size proportionally with demand -- doubling demand approximately doubles both total cost and total supply, leaving LCOA unchanged. The slight decline at higher demand ($1.79 $\to$ $1.72) reflects economies of scale: fixed components (e.g., bunkering CAPEX per shuttle) are spread over more delivered ammonia.

**Finding 2: Optimal shuttle size invariance.** The optimal shuttle remains 2,500 m$^3$ (Case 1), 5,000 m$^3$ (Case 3), and 5,000 m$^3$ (Case 2) across all four demand scenarios. This invariance -- including Case 3's consistent selection of 5,000 m$^3$ from Low through VeryHigh -- confirms that the optimal shuttle specification is determined by the cycle time structure (shore loading time, transit time, pumping time) rather than by demand volume. Because all three cases maintain their optimal shuttle sizes across a 4$\times$ demand range, the specification decision is fully decoupled from the demand forecast.

The practical implication for port planners is that shuttle vessel specifications can be committed early in the planning process without waiting for demand clarity. The timing of fleet additions (not the specifications) is the demand-sensitive decision. This separation of specification-robustness from scheduling-sensitivity reduces planning risk.

---

### 3.9 Discount Rate Sensitivity

The base case assumes zero discounting (Assumption A2), treating all years equally. To validate this assumption, we test three discount rates: $r$ = 0%, 5%, and 8% across all three cases. Table 9 summarizes the results.

**Table 9: Discount rate sensitivity -- optimal configurations remain invariant**

| Case | $r$ = 0% NPC | $r$ = 5% NPC | $r$ = 8% NPC | Optimal Shuttle | Optimal Pump |
|------|-------------|-------------|-------------|-----------------|--------------|
| Case 1 | $410.34M | $226.71M | $166.42M | 2,500 m$^3$ | 1,000 m$^3$/h |
| Case 3 | $1,014.81M | $561.19M | $412.34M | 5,000 m$^3$ | 1,000 m$^3$/h |
| Case 2 | $830.65M | $458.60M | $336.56M | 5,000 m$^3$ | 1,000 m$^3$/h |

The key finding is that **optimal shuttle specifications are invariant across all discount rates**. While NPC decreases by approximately 59% from $r$ = 0% to $r$ = 8% (because future costs are discounted more heavily), the relative cost ranking across shuttle sizes remains unchanged. Case 1 selects 2,500 m$^3$, and both Case 3 and Case 2 select 5,000 m$^3$ regardless of discounting assumptions.

Empirically, the cost ranking is preserved because the Case 1 advantage stems from lower cycle times and CAPEX, not from temporal cost distribution. Different shuttle sizes produce different fleet expansion schedules, so identical discounting factors cannot be guaranteed theoretically; the invariance is an empirical finding for these specific configurations.

Fig. 15 presents the NPC and LCOA response to discount rate for all three cases. The LCOA follows the same pattern: Case 1 ranges from $1.74/ton ($r$ = 0%) to $0.71/ton ($r$ = 8%), while maintaining the cost advantage over Cases 2-1 and 2-2 at every discount rate.

Fig. 16 shows fleet evolution under different discount rates. The physical fleet requirement (number of shuttles needed to serve demand) is determined by cycle time and demand volume, not by financial discounting. Consequently, fleet expansion timelines are similar across discount rates, with only minor differences in the timing of discrete fleet additions.

These results validate Assumption A2: while the choice of discount rate affects the reported NPC magnitude, it does not affect the infrastructure specification recommendations or the relative ranking of supply chain configurations. Port authorities can use the zero-discount results as a conservative upper bound on NPC while maintaining confidence in the shuttle sizing recommendations.

---

## 4. Discussion

## 4.1 Local Storage vs Remote Supply: Break-Even Analysis

The results in Section 3.1 establish that port-based storage (Case 1) is cheaper than remote supply at the actual distances of Yeosu (86 nm) and Ulsan (59 nm). However, this comparison is distance-specific. Port planners at other locations face the same build-vs-source decision at different distances. We address this by parameterizing the one-way travel distance from 10 to 200 nm and identifying break-even crossover points.

Fig. 12 (FIG9) presents the break-even distance analysis. For the Yeosu comparison (10,000 m$^3$ shuttle), Case 1 NPC remains constant at $1,057.15M (independent of remote supply distance, as it uses port-internal shuttles only), while Case 3 NPC increases linearly with distance. The curves cross at approximately 84 nm: below this distance, remote supply at 10,000 m$^3$ scale is cheaper; above it, port-based storage at 10,000 m$^3$ dominates. At 80 nm, Case 3 costs $1,033.87M (cheaper than Case 1 by $23.28M); at 90 nm, Case 3 costs $1,084.24M (more expensive than Case 1 by $27.09M). At the actual Yeosu distance of 86 nm, Case 1 is marginally cheaper, placing Yeosu very close to the break-even threshold.

For the Ulsan comparison (5,000 m$^3$ shuttle), no crossover occurs within the 10--200 nm range. Case 1 at 5,000 m$^3$ costs $441.25M, while even at 10 nm, the remote supply configuration costs $473.16M. This absence of crossover reflects that at the 5,000 m$^3$ shuttle scale, the shuttle serves only $N_v = 1$ vessel per trip, and the per-trip cost structure cannot achieve the travel-cost amortization efficiency that would make remote supply competitive.

The break-even asymmetry has a practical interpretation: remote ammonia supply becomes competitive with port storage only when (a) the shuttle is large enough to serve multiple vessels per trip ($N_v \geq 2$, requiring $V_s \geq 10{,}000$ m$^3$), AND (b) the source is closer than approximately 84 nm. For Busan, where the nearest ammonia sources are Ulsan (59 nm) and Yeosu (86 nm), port-based storage is the cost-minimizing configuration under baseline assumptions, though the Yeosu distance falls very close to the break-even threshold at the 10,000 m$^3$ shuttle scale.

**Optimal-vs-optimal comparison.** The above break-even analysis uses the same shuttle size for both cases, which isolates the effect of distance but does not reflect actual decision-making where each case would use its own optimal shuttle. When Case 1 uses its optimal 2,500 m$^3$ shuttle ($410.34M) and Case 2 uses its respective optimal size (5,000 m$^3$ for both Ulsan and Yeosu), no break-even crossover occurs within the 10--200 nm range. Even at 10 nm, the cheapest Case 2 option (5,000 m$^3$) costs $473.16M -- still 15.3% above Case 1's optimal. This happens because port-based storage enables a fundamentally smaller shuttle (2,500 vs 5,000 m$^3$), with correspondingly lower CAPEX. The practical implication is that the 84 nm break-even applies only when comparing the same shuttle size; when each case is free to choose its optimal configuration, port-based storage dominates at all distances for the Busan demand profile.

This decision rule is transferable to other ports: given the one-way distance to the nearest ammonia source and the intended shuttle size, planners can read directly from the break-even curves whether to invest in local storage or rely on remote supply. However, when port storage enables the use of smaller, cheaper shuttles, the build-local option may dominate regardless of distance.

---

## 4.2 Robustness of Infrastructure Decisions

The sensitivity analyses in Sections 3.6--3.8 collectively address the question: how confident can planners be in the optimal specifications?

**Shuttle size specification** is robust across all tested uncertainty dimensions. The Case 1 optimal (2,500 m$^3$) is unchanged by: pump rate variation across the tested range (Section 3.6), fuel price variation from $300 to $1,200/ton (Section 3.7), and demand variation from 250 to 1,000 end-vessels (Section 3.8). Only at very low pump rates does the optimal shift to smaller shuttles -- a scenario unlikely in practice given available pump technology.

**LCOA** is remarkably stable: $1.72--$1.79/ton across a 4$\times$ demand range (Section 3.8), and $1.59--$2.05/ton across a 4$\times$ fuel price range (Section 3.7). The combined uncertainty envelope (demand $\times$ fuel price) produces an LCOA range of approximately $1.40--$2.50/ton for Case 1 -- primarily driven by fuel price.

**Fleet expansion timing** is the demand-sensitive component. While the shuttle specification is fixed, the year in which each new shuttle must be procured depends on when cumulative demand crosses the capacity threshold of the existing fleet. Under the High scenario (750 end-vessels), fleet additions occur earlier and more frequently than under Base (500), but the procurement decision remains the same 2,500 m$^3$ vessel. This separation allows port authorities to commit to vessel specifications while maintaining scheduling flexibility.

**Primary risk factor:** The tornado analysis identifies the CAPEX scaling exponent ($\alpha$) as the dominant uncertainty for Case 1 (67.9% NPC swing, Section 3.7). In practical terms, this means that the accuracy of shipyard cost estimates matters more than fuel price forecasts or demand projections. A 20% error in the scaling exponent -- equivalent to using $\alpha = 0.60$ rather than $0.75$ -- would change the NPC by $278.71M, dwarfing the impact of fuel price uncertainty ($28.68M) or travel time variation ($37.24M). Port authorities should invest in detailed shipyard quotations for ammonia shuttle vessels before committing to fleet procurement.

The enumeration-based approach adopted for shuttle-pump specification search (Section 3.5) contributes to this robustness finding. Because all feasible combinations are evaluated exhaustively, the optimality is guaranteed to be global within the discrete candidate set -- unlike decomposition-based methods that may converge to local optima depending on initialization. The transparency of the complete cost landscape (visible in Fig. 2 and Fig. S1) allows decision-makers to assess not only the optimal specification but also the cost penalty of deviating from it, supporting procurement flexibility.

---

## 4.3 Practical Implications for Green Corridor Planning

The results support three actionable recommendations for port authorities:

**Recommendation 1: Build port-based storage.** For ports with demand profiles similar to Busan, port-based storage with small-shuttle intra-port distribution minimizes 21-year cost. The controlled comparison (same shuttle size) yields a break-even distance of ~84 nm, but the optimal-vs-optimal comparison (Section 4.1) shows that port storage dominates at all distances up to 200 nm because it enables smaller, cheaper shuttles. This strengthens the case for local storage investment (Section 4.1, Fig. 12).

**Recommendation 2: Commit to shuttle specifications early.** The optimal shuttle size (2,500 m$^3$ for port-based storage) is invariant to demand uncertainty across a 4$\times$ range (Section 3.8). Port authorities can issue vessel procurement contracts without waiting for demand clarity, reducing the risk of delayed infrastructure deployment. The vessel specification -- not the fleet size -- should be fixed first.

**Recommendation 3: Monitor shipyard costs as the primary risk variable.** The CAPEX scaling exponent accounts for 67.9% of NPC sensitivity (Section 3.7), making shipyard cost accuracy the highest-priority uncertainty to reduce. Fuel price and demand uncertainty, while non-negligible, have proportionally smaller impact on the infrastructure sizing decision. Competitive bidding among multiple shipyards and fixed-price construction contracts would mitigate this risk.

These recommendations apply to the Korea--US and Korea--Australia green corridor initiatives where ammonia bunkering at Busan Port is under active planning, as formalized in the April 2025 bilateral agreement between Korea and the United States.

---

### 4.4 Comparison with Published DES Model

To position our results within the existing literature, we compare our MILP framework with the discrete event simulation (DES) model of Yang and Lam [11], the most directly relevant published study on ammonia bunkering operations. Table 10 summarizes the key methodological differences.

**Table 10: Methodology comparison -- MILP vs. DES for ammonia bunkering**

| Dimension | Yang & Lam DES [11] | This study (MILP) |
|-----------|--------------------|--------------------|
| Objective | Operational performance evaluation | Infrastructure investment optimization |
| Fleet sizing | Fixed input (2--4 vessels) | Optimized output (3--25+ vessels) |
| Time horizon | 1-year snapshot | 21-year dynamic (2030--2050) |
| Cost scope | OPEX only (charter + fuel) | Full lifecycle (CAPEX + OPEX) |
| Demand | Static | Growing trajectory (50--500 vessels) |
| Service time | Stochastic (TRIA distribution) | Deterministic (formula-based) |
| Queuing | Explicit (event-driven) | Implicit (utilization constraint) |
| Supply configs | Single | Three (port storage, Yeosu, Ulsan) |

The two approaches are complementary rather than competing: DES captures queuing dynamics and stochastic service time variability that our deterministic MILP does not model, while the MILP optimizes fleet sizing and multi-year investment timing that DES evaluates but does not optimize.

The pumping time component -- the time required to transfer ammonia from shuttle to receiving vessel, calculated as $V / Q_p$ -- is consistent across both models, as it is derived from the same physical relationship. The gap between our total service time estimate and Yang and Lam's DES output is attributable to operational overhead (mooring procedures and documentation) that their DES explicitly models but our MILP subsumes into setup time parameters ($T_{setup}$ = 2.0 hours per endpoint). This difference reflects scope rather than inconsistency: the MILP's purpose is infrastructure sizing, not operational scheduling, and the setup time parameterization is sufficient for fleet-level capacity planning (Fig. 17).

A more substantive comparison emerges from sensitivity analysis. Both models identify bunkering flow rate as the dominant operational parameter: Yang and Lam report a 51.3% impact on service time when flow rate varies by +/-50%, while our MILP yields a 58.8% NPC change over a comparable range (Fig. 18). The 7.5 percentage-point gap is structural: the DES uses triangular (TRIA) distributions for service time components, which smooth extreme values through probabilistic averaging, whereas our deterministic formula amplifies the effect of flow rate at the extremes. This difference is expected and informative -- it quantifies the extent to which stochastic modeling attenuates parameter sensitivity relative to deterministic analysis.

Beyond flow rate, our MILP framework enables sensitivity analysis across investment-side parameters (CAPEX scaling exponent, bunker volume, demand trajectory) that the DES framework, focused on operational performance, does not address. The tornado analysis (Section 3.7) reveals that CAPEX scaling exponent dominates NPC sensitivity for Case 1 at 67.9% swing -- a finding inaccessible through operational simulation alone.

These complementary strengths suggest a hybrid DES-MILP approach as a promising research direction (Future Work item F2): use the MILP to determine optimal fleet size and specifications, then validate operational feasibility through DES simulation incorporating queuing effects and stochastic service times. Such an iterative approach would address Limitation L5 (no explicit congestion modeling) while preserving the MILP's investment optimization capability.

---

## 4.5 Limitations and Future Work

### Limitations

**L1. Deterministic demand (linear growth).** We model demand as a linear trajectory from 50 to 500 vessels. Actual ammonia adoption may follow an S-curve, with slower initial uptake and potential acceleration post-2040 as regulations tighten (IMO CII trajectory). Under S-curve demand, early-year fleet overcapacity would persist longer, increasing capital lock-up by an estimated 8--12%. Conversely, late-period demand surges could outpace fleet additions if procurement lead times exceed 2--3 years. Direction of error: NPC may be underestimated by 5--10% under S-curve demand.

**L2. Fixed fuel price.** The $600/ton baseline is held constant over 21 years. Green ammonia production costs are projected to decline from $700--$1,400/ton (2025) to $310--$660/ton (2030--2040) as electrolyzer costs fall. A declining price trajectory would reduce Case 2 vOPEX over time, potentially narrowing the Case 1 vs Case 2 cost gap in later years. Direction: break-even distance may shift by 10--20 nm under declining fuel price scenarios.

**L3. No discounting.** The zero discount rate treats a dollar spent in 2030 equally to a dollar spent in 2050. With a standard 8% social discount rate, distant-year costs would be heavily discounted, favoring configurations with lower early-year investment. Case 1 (smaller fleet, lower initial CAPEX) would benefit more from discounting than Case 2 (larger fleet, higher initial CAPEX). Direction: Case 1 advantage may widen by 10--15% under positive discounting.

**L4. SFOC fixed per size class.** The engine SFOC map assigns constant values per size class (Table 3). Real-world SFOC varies with engine load (typically +10--15% at partial load vs design point). For Case 2, where shuttles may operate below design speed during port maneuvering, actual fuel consumption could be 5--10% higher than modeled. Direction: Case 2 NPC may be underestimated by 3--5%.

**L5. No port congestion or queuing.** We assume vessels arrive uniformly throughout the year. In practice, seasonal and weekly demand peaks create queuing effects that could increase effective cycle time by 10--20% during peak periods. The daily peak factor ($F_{\text{peak}} = 1.5$) provides partial mitigation but does not replace a queuing model. Direction: fleet size may be underestimated by 1--2 shuttles during peak years.

**L6. Single bunker volume.** All vessels are assumed to require 5,000 m$^3$ per call. In practice, vessel sizes range from small feeders (~1,000 m$^3$) to large container ships (~8,000 m$^3$). Variable bunker volumes would create an order-sizing problem (matching shuttle loads to vessel needs), potentially requiring a mix of shuttle sizes. Direction: heterogeneous demand could increase LCOA by 5--15% due to suboptimal load matching.

**L7. Ammonia toxicity and safety costs not modeled.** Ammonia is acutely toxic and requires safety exclusion zones, gas detection systems, and emergency response capabilities during bunkering [18, 19, 20]. These safety infrastructure costs are not included in NPC. The additional safety costs could increase bunkering infrastructure cost by an estimated 5--15%, with potentially larger relative impact on Case 1 where bunkering occurs within the congested port area. Direction: NPC may be underestimated for all cases.

### Future Work

**F1. Stochastic MILP with demand and price uncertainty.** Extend the deterministic model to a two-stage stochastic MILP with first-stage (shuttle specification) and second-stage (fleet expansion schedule) decisions under joint demand-price scenarios. This would formalize the robustness finding (Section 3.8) within an optimization framework.

**F2. Port queuing simulation coupled with MILP.** Develop a hybrid DES-MILP approach where the DES captures queuing effects (building on Yang and Lam [11]) and the MILP optimizes fleet sizing given queuing-adjusted cycle times. This would address Limitation L5.

**F3. Multi-fuel bunkering comparison.** Apply the framework to methanol and LNG bunkering infrastructure at Busan, enabling a cross-fuel comparison of LCOA and fleet requirements. This would inform ports considering multi-fuel strategies.

**F4. Real-options analysis for staged investment.** Replace the deterministic planning horizon with a real-options model that values the flexibility to defer or accelerate shuttle procurement in response to demand signals. This would quantify the option value of smaller (more flexible) shuttles versus larger (more efficient) ones.

**F5. Multi-port network extension.** Extend the single-port model to a network of Korean ports (Busan, Ulsan, Incheon) with shared shuttle fleets and inter-port transfers, capturing portfolio diversification benefits.

---

## 5. Conclusions

This study developed a mixed-integer linear programming model for optimizing ammonia bunkering infrastructure at Busan Port over a 21-year planning horizon (2030--2050). The model systematically evaluates all feasible shuttle-pump combinations and optimizes year-by-year fleet expansion for three supply chain configurations: port-based storage (Case 1), remote supply from Yeosu (Case 3, 86 nm), and remote supply from Ulsan (Case 2, 59 nm).

Four main findings emerge:

First, the optimal infrastructure specifications differ across cases due to the interaction between CAPEX scaling and cycle time. Case 1 selects a 2,500 m$^3$ shuttle (NPC $410.34M, LCOA $1.74/ton), while Cases 2-1 and 2-2 both require 5,000 m$^3$ shuttles at 2.0--2.5 times higher cost.

Second, a break-even distance of approximately 84 nm separates the domains where port-based storage and remote supply are respectively cheaper (for 10,000 m$^3$ shuttles). This threshold provides a transferable decision rule for ports evaluating ammonia bunkering infrastructure alternatives.

Third, optimal shuttle specifications are robust to demand uncertainty: across a 4$\times$ demand range (250 to 1,000 end-vessels), the optimal shuttle size remains unchanged and LCOA varies by only 4.0%. This enables early commitment to vessel procurement without waiting for demand clarity.

Fourth, the cost driver hierarchy differs fundamentally between configurations: CAPEX scaling dominates port-based storage (67.9% NPC swing), while bunker volume dominates remote supply. This informs targeted risk management strategies for each infrastructure type.

These results provide quantitative decision tools for port authorities, shipping companies, and policymakers planning ammonia bunkering infrastructure for green shipping corridors. The framework is readily applicable to other ports by substituting local distances, shuttle candidate sets, and demand projections.

---

## References

[1] Al-Enazi, A., Okonkwo, E. C., Bicer, Y., & Al-Ansari, T. (2021). A review of cleaner alternative fuels for maritime transportation. Energy Reports, 7, 1962--1985.

[2] Imhoff, T. B., Gkantonas, S., & Mastorakos, E. (2021). Analysing the performance of ammonia powertrains in the marine environment. Energies, 14(21), 7447.

[3] Kim, K., Roh, G., Kim, W., & Chun, K. (2020). A preliminary study on an alternative ship propulsion system fueled by ammonia: Environmental and economic assessments. Journal of Marine Science and Engineering, 8(3), 183.

[4] Korberg, A. D., Brynolf, S., Grahn, M., & Skov, I. R. (2021). Techno-economic assessment of advanced fuels and propulsion systems in future fossil-free ships. Renewable and Sustainable Energy Reviews, 142, 110861.

[5] Xing, H., Stuart, C., Spence, S., & Chen, H. (2021). Alternative fuel options for low carbon maritime transportation: Pathways to 2050. Journal of Cleaner Production, 297, 126651.

[6] Getting to Zero Coalition. (2021). The Next Wave: Green Corridors. Global Maritime Forum.

[7] Lloyd's Register & UMAS. (2020). Techno-economic assessment of zero-carbon fuels.

[8] Fagerholt, K. (2004). A computer-based decision support system for vessel fleet scheduling -- Experience and future research. Decision Support Systems, 37(1), 35--47.

[9] Christiansen, M., Fagerholt, K., Nygreen, B., & Ronen, D. (2013). Ship routing and scheduling in the new millennium. European Journal of Operational Research, 228(3), 467--483.

[10] Wang, Y., & Wright, L. A. (2021). A comparative review of alternative fuels for the maritime sector: Economic, technology, and policy challenges for clean energy implementation. World, 2(4), 456--481.

[11] Yang, M., & Lam, J. S. L. (2023). Operational and economic evaluation of ammonia bunkering -- Bunkering supply chain perspective. Transportation Research Part D: Transport and Environment, 117, 103662.

[12] Doymus, M., Denktas-Sakar, G., Topaloglu Yildiz, S., & Acik, A. (2022). Small-scale LNG supply chain optimization for LNG bunkering in Turkey. Computers and Chemical Engineering, 162, 107789.

[13] Stalahane, M., Halvorsen-Weare, E. E., Nonas, L. M., & Pantuso, G. (2019). Optimizing vessel fleet size and mix to support maintenance operations at offshore wind farms. European Journal of Operational Research, 276(2), 495--509.

[14] Bakkehaug, R., Eidem, E. S., Fagerholt, K., & Hvattum, L. M. (2014). A stochastic programming formulation for strategic fleet renewal in shipping. Transportation Research Part E, 72, 60--76.

[15] Salmon, N., Banares-Alcantara, R., & Nayak-Luke, R. (2021). Optimization of green ammonia distribution systems for intercontinental energy transport. iScience, 24(8), 102903.

[16] Kim, H., Kim, J., & Lee, S. (2024). Technical-economic analysis for ammonia ocean transportation using an ammonia-fueled carrier. Sustainability, 16(2), 827.

[17] Zhao, X., Wang, W., Song, X., & Peng, Y. (2025). Toward green container liner shipping: Joint optimization of heterogeneous fleet deployment, speed optimization, and fuel bunkering. International Transactions in Operational Research, 32(3), 1552--1580.

[18] Fan, H., Enshaei, H., Jayasinghe, S. G., Tan, S. H., & Zhang, C. (2022). Quantitative risk assessment for ammonia ship-to-ship bunkering based on Bayesian network. Process Safety Progress, 41(3), 395--410.

[19] Yang, M., & Lam, J. S. L. (2024). Risk assessment of ammonia bunkering operations: Perspectives on different release scales. Journal of Hazardous Materials, 465, 133237.

[20] Khan, R. U., Yin, J., Wang, S., Hussein, M., Alqurashi, Y., & Al Sulaie, S. (2025). A system theoretic quantitative risk assessment for port ammonia bunkering operations. International Journal of Hydrogen Energy, 114, 556--569.

[21] Fullonton, A., Lea-Langton, A. R., Madugu, F., & Larkin, A. (2025). Green ammonia adoption in shipping: Opportunities and challenges across the fuel supply chain. Marine Policy, 171, 106444.

[22] Fagerholt, K., Hvattum, L. M., Johnsen, T. A. V., & Korsvik, J. E. (2023). Maritime inventory routing: Recent trends and future directions. International Transactions in Operational Research, 30(6), 3013--3056.

[23] Wang, Y., Fagerholt, K., & Wallace, S. W. (2018). Planning for charters: A stochastic maritime fleet composition and deployment problem. Omega, 79, 54--66.

[24] Pantuso, G., Fagerholt, K., & Wallace, S. W. (2016). Uncertainty in fleet renewal: A case from maritime transportation. Transportation Science, 50(2), 390--407.

[25] Tan, Z., Du, Z., Wang, X., Yang, Z., & Wu, L. (2024). Fleet sizing with time and voyage-chartered vessels under demand uncertainty. Transportation Research Part E, 192, 103810.

[26] Guo, Y., Yan, R., Qi, J., Liu, Y., Wang, S., & Zhen, L. (2024). LNG bunkering infrastructure planning at port. Multimodal Transportation, 3, 100134.

[27] He, J., Jin, Y., Pan, K., & Chen, J. (2024). Route, speed, and bunkering optimization for LNG-fueled tramp ship with alternative bunkering ports. Ocean Engineering, 305, 117996.

[28] Ntakolia, C., Douloumpekis, M., Papaleonidas, C., Tsiampa, V., & Lyridis, D. V. (2023). A stochastic modelling and optimization for the design of an LNG refuelling system in the Piraeus Port region. SN Operations Research Forum, 4, 59.

[29] IMO. (2023). 2023 IMO Strategy on Reduction of GHG Emissions from Ships. Resolution MEPC.377(80), adopted 7 July 2023.

[30] IRENA & AEA. (2022). Innovation Outlook: Renewable Ammonia. International Renewable Energy Agency, Abu Dhabi.

[31] Oxford Institute for Energy Studies. (2024). Fuelling the future: A techno-economic evaluation of e-ammonia production for maritime (ET40). Oxford, UK.

[32] Vieira, B. S., Mayerle, S. F., Campos, L. M. S., & Coelho, L. C. (2021). Exact and heuristic algorithms for the fleet composition and periodic routing problem of offshore supply vessels with berth allocation decisions. European Journal of Operational Research, 295(3), 908--923.

[33] Rodrigues, F., Agra, A., Christiansen, M., Hvattum, L. M., & Requejo, C. (2019). Comparing techniques for modelling uncertainty in a maritime inventory routing problem. European Journal of Operational Research, 277(3), 831--845.

[34] Qu, W., Duinkerken, M. B., & Schott, D. L. (2024). A framework for risk assessment of ammonia storage and bunkering at ports. In Proceedings of the International Physical Internet Conference (IPIC 2024), TU Delft.

[35] Khan, M. S., Effendy, S., & Karimi, I. A. (2025). Ammonia bunkering in the maritime sector: A review. Ocean Engineering, 338, 121960.

[36] Verschuur, J., et al. (2024). Green shipping corridor infrastructure investment: Socio-economic and environmental impacts. Environmental Research: Infrastructure and Sustainability, 4(1), 015001.

[37] Wang, S. S., et al. (2022). Optimization of ammonia bunkering network configurations. Computer Aided Chemical Engineering, 49, 589--594.

[38] Dahlke-Wallat, F., et al. (2024). Ammonia bunkering infrastructure concepts: A techno-economic evaluation. In Proceedings of the International Marine Design Conference (IMDC 2024), TU Delft.

[39] Pratama, G. A., et al. (2025). Multi-period optimization for LNG bunkering vessel fleet sizing and scheduling. Gas Science and Engineering, 143, 205742.

[40] Machfudiyanto, R. A., et al. (2023). LNG bunkering infrastructure feasibility at Indonesian ports. Heliyon, 9(8), e19047.

[41] Jokinen, R., Pettersson, F., & Saxen, H. (2015). An MILP model for optimization of a small-scale LNG supply chain along a coastline. Applied Energy, 138, 423--431.

[42] Wang, Y., Daoutidis, P., & Zhang, Q. (2023). Ammonia-based green corridors for sustainable maritime transportation. Digital Chemical Engineering, 6, 100082.

---

## List of Figures

**Fig. 1.** Cycle time components for three supply chain configurations. The stacked bar chart decomposes each cycle into shore loading, transit, connection/disconnection, and pumping phases. Case 1 (Busan port storage) has the shortest cycle at 16.07 h due to minimal transit time (1.0 h one-way), while Case 3 (Yeosu, 86 nm) requires 34.60 h per cycle with long-haul transit dominating. The visual comparison reveals that transit time, not pumping, is the primary differentiator between port-based and remote supply configurations.

**Fig. 2.** Net present cost as a function of shuttle vessel size for all three cases. Each curve exhibits a piecewise cost landscape shaped by the integer-valued trip count, with discontinuities at shuttle sizes where the number of trips per bunkering call changes. The 500 m$^3$ shuttle is infeasible for Case 1 (call duration exceeds the maximum allowable limit), so the Case 1 curve begins at 1,000 m$^3$. Case 1 achieves its global minimum of $410.34M at 2,500 m$^3$, with a secondary local minimum at 5,000 m$^3$ (7.5% above optimal). Cases 2-1 and 2-2 both show optima at 5,000 m$^3$, reflecting the cycle time penalties associated with larger shuttles due to increased shore loading time.

**Fig. 3.** NPC comparison across cases at optimal configurations. The bar chart confirms the cross-case cost hierarchy: Case 3 (Yeosu) NPC is 2.47$\times$ Case 1, and Case 2 (Ulsan) is 2.02$\times$ Case 1. This ordering holds across all shuttle sizes evaluated, demonstrating that the port-based storage advantage is structural rather than configuration-dependent.

**Fig. 4.** Cost component breakdown showing six NPC components (shuttle CAPEX, bunkering CAPEX, shuttle fOPEX, shuttle vOPEX, bunkering fOPEX, bunkering vOPEX) at optimal configurations. Case 1 is capital-intensive with shuttle CAPEX and fOPEX accounting for 77.0% of NPC, whereas Cases 2-1 and 2-2 shift toward operations-intensive cost structures with shuttle vOPEX rising to 33--40% due to higher fuel consumption on longer routes. This structural shift has practical implications: Case 1 costs are front-loaded and predictable, while Case 2 costs are fuel-price sensitive and distributed over the operating life.

**Fig. 5.** Levelized cost of ammonia bunkering (LCOA) across all cases and shuttle sizes. Case 1 achieves $1.74/ton at the optimal 2,500 m$^3$ shuttle, representing the minimum unit cost of ammonia delivery from storage to vessel. The 148% premium for Case 3 ($4.31/ton) and 103% premium for Case 2 ($3.53/ton) persist across all configurations, confirming that the cost advantage is driven by travel distance and cycle time rather than by shuttle selection.

**Fig. 6.** Annual cost evolution from 2030 to 2050 for the optimal configuration of each case. Cost growth exhibits a step function correlated with fleet additions: each new shuttle triggers a jump in annualized CAPEX plus fixed OPEX, followed by gradual vOPEX-driven increases as demand grows between additions. The two distinct growth regimes (CAPEX jumps and vOPEX ramps) are visible for all three cases, with Case 3 showing the steepest vOPEX ramps due to its higher per-cycle fuel consumption.

**Fig. 7.** Cumulative fleet size evolution over the 21-year planning horizon. Fleet growth follows a staircase pattern as demand crosses capacity thresholds defined by the working-time constraint. Case 1 grows from 3 shuttles in 2030 to 25 by 2050, while Cases 2-1 and 2-2 require larger fleets to compensate for longer cycle times. The discrete, lumpy nature of fleet investment is clearly visible, with each step representing a procurement decision.

**Fig. 8.** Annual bunkering demand overlaid with fleet supply capacity. The smooth demand curve (linear growth) contrasts with the staircase supply capacity, revealing fleet slack -- periods of overcapacity immediately following each shuttle addition that erode as demand catches up. The narrowing gap between demand and capacity in later years indicates increasing fleet utilization as the horizon progresses.

**Fig. 9.** Fleet utilization rates over time showing a sawtooth pattern. Utilization climbs as demand grows against a fixed fleet (reaching 99% just before additions) and drops when new capacity enters service (to approximately 73%). This pattern confirms just-in-time fleet expansion: the MILP adds shuttles at the minimum necessary rate to prevent the working-time constraint from becoming infeasible, minimizing capital idle time at the cost of limited peak-period buffer.

**Fig. 10.** Tornado diagrams showing NPC sensitivity to +/-20% variation of six parameters for all three cases. For Case 1, the CAPEX scaling exponent dominates with a 67.9% NPC swing ($278.71M), followed by bunker volume (48.3%) and maximum annual hours (33.1%). For Cases 2-1 and 2-2, bunker volume becomes the top-ranked parameter, replacing CAPEX scaling, with swings of 75.5% and 102.0% respectively. This shift in sensitivity ranking mirrors the cost structure transition from CAPEX-dominated (Case 1) to operations-dominated (Case 2).

**Fig. 11.** Fuel price sensitivity showing NPC and LCOA response across $300--$1,200/ton for all three cases. The response is linear for all cases, with Case 1 NPC ranging from $374.50M to $482.02M and LCOA from $1.59/ton to $2.05/ton. Case 2 configurations exhibit steeper slopes consistent with their higher vOPEX shares (33--40% vs 13% for Case 1), and the Case 2-to-Case 1 NPC ratio widens at higher fuel prices, reinforcing the port-based storage advantage under high fuel price scenarios.

**Fig. 12.** Break-even distance analysis comparing Case 1 and Case 2 NPC as a function of one-way travel distance (10--200 nm). For the Yeosu comparison (10,000 m$^3$ shuttle), the curves cross at approximately 84 nm, below which remote supply is cheaper. For the Ulsan comparison (5,000 m$^3$ shuttle), no crossover occurs because the smaller shuttle serves only one vessel per trip and cannot achieve sufficient travel-cost amortization. This asymmetry establishes that remote supply competitiveness requires both large shuttles ($N_v \geq 2$) and short distances (< 84 nm).

**Fig. 13.** Demand scenario analysis comparing NPC and LCOA across four scenarios (250--1,000 end-vessels) for all three cases. LCOA stability is the central finding: Case 1 LCOA varies by only 4.0% ($1.72--$1.79/ton) across a 4$\times$ demand range, because the MILP scales fleet size proportionally with demand. The optimal shuttle size remains invariant (2,500 m$^3$ for Case 1, 5,000 m$^3$ for Cases 2-1 and 2-2) across all scenarios, enabling early commitment to vessel specifications regardless of demand uncertainty.

**Fig. 14.** Pump rate sensitivity showing NPC response to pump flow rate variation from 100 to 1,500 m$^3$/h. The relationship exhibits diminishing returns: the marginal benefit of pump rate increases falls rapidly at higher flow rates. The optimal shuttle size remains 2,500 m$^3$ across pump rates above a threshold for Case 1, demonstrating that the shuttle specification is robust to pump rate uncertainty within the practical range.

**Fig. 15.** Discount rate sensitivity showing NPC and LCOA response across 0%, 5%, and 8% rates for all three cases. While NPC decreases by approximately 59% from 0% to 8% discount rate, the optimal shuttle specifications remain invariant across all discount rates. Case 1 maintains its cost advantage over Cases 2-1 and 2-2 at every discount rate, validating that the zero-discount base case produces conservative NPC estimates without affecting infrastructure sizing recommendations.

**Fig. 16.** Fleet evolution under different discount rates (0%, 5%, 8%) for all three cases. Physical fleet requirements are determined by cycle time and demand volume rather than financial discounting, resulting in similar fleet expansion timelines across discount rates with only minor differences in the timing of discrete additions.

**Fig. 17.** Service time comparison between our deterministic MILP and the DES model of Yang and Lam [11] at three transfer volumes (855, 1,384, and 2,000 tons). The pumping time component is consistent across both models as it derives from the same physical relationship. The gap in total service time is attributable to operational overhead (mooring and documentation) that the DES explicitly models but our MILP subsumes into setup time parameters (2.0 hours per endpoint).

**Fig. 18.** Flow rate sensitivity comparison between deterministic MILP (58.8% NPC impact) and stochastic DES (51.3% service time impact) over a comparable flow rate variation range. The 7.5 percentage-point gap is structural: the DES uses triangular distributions that smooth extreme values through probabilistic averaging, whereas our deterministic formula amplifies the effect at the extremes. This quantifies the extent to which stochastic modeling attenuates parameter sensitivity.

**Fig. S1.** NPC sensitivity heatmap showing the complete cost landscape across all shuttle size and pump rate combinations for each case. The heatmap reveals the cost valley around the optimal configuration and visualizes the penalty for deviating from it in either dimension, supporting procurement flexibility by showing which near-optimal alternatives exist.

**Fig. S2.** Top configurations ranked by NPC for each case. The ranking confirms that the optimal configuration has a clear cost advantage over alternatives, with the cost penalty increasing steeply for suboptimal shuttle sizes due to CAPEX scaling effects.

**Fig. S3.** Annual cycle count evolution over the planning horizon. The number of bunkering cycles per shuttle per year increases as demand grows, approaching the theoretical maximum (497.78 for Case 1) just before each fleet addition. This confirms that fleet utilization is driven to the constraint boundary by the MILP.

**Fig. S4.** Two-way sensitivity heatmap showing NPC response to simultaneous variation of fuel price ($300--$1,200/ton) and bunker volume (2,500--10,000 m$^3$) for Case 1. The heatmap reveals that bunker volume dominates the interaction: high bunker volume drives NPC up regardless of fuel price, while fuel price has a comparatively uniform effect across volume levels.

**Fig. S5.** Bunker volume sensitivity showing NPC and LCOA response to bunker volume variation from 2,500 to 10,000 m$^3$ for all three cases. NPC increases approximately linearly with bunker volume for all cases, as larger per-call demands require more shuttle cycles and fleet capacity. The LCOA remains relatively stable because the cost increase is proportional to the volume increase.
