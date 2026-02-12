## 3. Results and Analysis

## 3.1 Optimal Configurations

The MILP model identifies distinct optimal shuttle-pump configurations for each supply chain case, reflecting the structural cost differences between port-based storage and remote supply (Table 5).

**Table 5: Optimal configurations for three supply chain cases**

| Parameter | Case 1 (Busan) | Case 2 (Ulsan) | Case 3 (Yeosu) |
|-----------|:-------------:|:-----------------:|:-----------------:|
| Optimal shuttle size (m$^3$) | 1,000 | 5,000 | 5,000 |
| Pump rate (m$^3$/h) | 500 | 500 | 500 |
| NPC (USD M) | 447.53 | 906.80 | 1,094.12 |
| LCOA (USD/ton) | 1.90 | 3.85 | 4.64 |
| Cycle time (h) | 13.43 | 36.00 | 39.60 |
| Annual cycles max | 595.74 | 222.20 | 202.01 |
| Trips per call | 5 | 1 | 1 |
| Annualized cost (M/yr) | 41.30 | 83.69 | 100.98 |

Fig. 2 (D1) shows the NPC as a function of shuttle size for all three cases. Each curve exhibits a piecewise cost landscape shaped by the integer-valued trip count $n_{\text{trip}}$ (Eq. 4), with a global minimum at an interior point. At the baseline pump rate of 500 m$^3$/h, Case 1 achieves its minimum NPC of \$447.53M at 1,000 m$^3$ -- the second-smallest candidate in the set. This small optimal shuttle reflects the slow pump rate: at 500 m$^3$/h, a 1,000 m$^3$ shuttle takes $T_{\text{pump}} = 1{,}000/500 = 2.0$ h per transfer, yielding $T_{\text{cycle}} = 13.43$ h and enabling 595.74 annual cycles per shuttle ($H_{\max}/T_{\text{cycle}} = 8{,}000/13.43$). Increasing shuttle size to 2,500 m$^3$ raises cycle time to 18.57 h (a 38% increase) but reduces trips per call from 5 to 2, resulting in a slightly higher NPC of \$454.38M (+1.5%). The 5,000 m$^3$ shuttle, which requires only 1 trip per call, costs \$519.14M (+16.0%) due to substantially longer cycle times ($T_{\text{cycle}} = 27.14$ h). The CAPEX scaling exponent ($\alpha = 0.75$) means that doubling shuttle capacity increases unit cost by $2^{0.75} = 1.68\times$ rather than $2\times$, producing economies of scale that are overwhelmed at 500 m$^3$/h pump rate by the cycle time penalty of slower pumping for larger shuttles.

For Cases 2 and 3, both achieve minimum NPC at 5,000 m$^3$ -- the smallest candidate in their respective sets. At this size, $N_v = \lfloor 5{,}000/5{,}000 \rfloor = 1$ vessel is served per trip. The 2,500 m$^3$ shuttle (also available for Cases 2 and 3) is more expensive: Case 2 at 2,500 m$^3$ costs \$1,106.45M versus \$906.80M at 5,000 m$^3$ (+22.0%), because $n_{\text{trip}} = 2$ at 2,500 m$^3$ doubles the shuttle operating hours per call. For Case 3, the same pattern holds with \$1,375.75M at 2,500 m$^3$ versus \$1,094.12M at 5,000 m$^3$ (+25.7%).

Fig. 3 (D10) confirms the cross-case cost hierarchy: Case 3 NPC is $2.45\times$ Case 1, and Case 2 is $2.03\times$ Case 1. This ordering holds across all shuttle sizes, indicating that the port-based storage advantage is structural rather than configuration-dependent. The LCOA metric normalizes for total supply volume: at \$1.90/ton (Case 1) versus \$4.64/ton (Case 3), the per-ton cost of remote supply from Yeosu is \$2.74/ton higher, representing a premium of 144%.

---

## 3.2 Temporal Dynamics

The MILP produces year-indexed fleet expansion schedules that reveal the discrete, lumpy nature of infrastructure investment. Fig. 7 (D8) shows cumulative fleet size over the 21-year planning horizon. For Case 1 (1,000 m$^3$ shuttle), the fleet grows in discrete steps from 6 shuttles in 2030 to 51 by 2050 as demand crosses capacity thresholds defined by Eq. (12). Each new shuttle adds 595.74 annual cycles of capacity (at $H_{\max} = 8{,}000$ h/year and $T_{\text{cycle}} = 13.43$ h), equivalent to serving approximately 119 additional bunkering calls per year (since $n_{\text{trip}} = 5$). The small shuttle size means the fleet is larger in absolute count than in v3 (51 vs 25 shuttles), but each shuttle costs only \$3.87M versus \$7.69M, producing lower total CAPEX despite the higher count.

For Case 2 (5,000 m$^3$ shuttle), the fleet grows from 3 shuttles in 2030 to approximately 27 by 2050. Each shuttle adds 222.20 annual cycles, equivalent to 222 bunkering calls per year ($n_{\text{trip}} = 1$). For Case 3, the fleet grows from 3 shuttles to approximately 30 over the same period, reflecting the longer cycle time (39.60 h vs 36.00 h).

Fig. 8 (D3) overlays annual bunkering demand with fleet supply capacity. The demand curve is smooth (linear growth from 600 calls in 2030 to 6,000 in 2050), while the supply curve follows a staircase pattern. The gap between supply capacity and demand represents fleet slack -- periods of overcapacity immediately following a shuttle addition, which erodes as demand catches up.

Fig. 6 (D2) shows the annual cost evolution from 2030 to 2050. Cost growth exhibits a step function correlated with fleet additions: each new Case 1 shuttle triggers a jump in annualized CAPEX ($C_{\text{shuttle}} / \text{AF} = 3.87\text{M} / 10.8355 = 0.357$M/year) plus fixed OPEX. Between fleet additions, annual cost growth is driven solely by increasing variable OPEX as the number of bunkering calls rises with demand. This yields two distinct growth regimes: CAPEX-driven jumps at fleet expansion years, and vOPEX-driven gradual increases between them.

---

## 3.3 Operational Efficiency

Fig. 9 (D5) reveals a sawtooth utilization pattern over time. Utilization climbs as demand grows against a fixed fleet, reaching a peak just before the next shuttle addition, then drops when new capacity enters service. For Case 1, the theoretical maximum utilization is 100% ($\text{Annual\_Cycles\_Max} = H_{\max} / T_{\text{cycle}} = 8{,}000 / 13.43 = 595.74$, so the fleet operates at the $H_{\max}$ constraint boundary). In practice, utilization oscillates between approximately 84% immediately after shuttle additions and 99% just before the next addition, a sawtooth amplitude of roughly 15 percentage points. This tight oscillation reflects the small shuttle size: each 1,000 m$^3$ shuttle adds only 119 calls of annual capacity, meaning demand grows to fill the increment quickly.

This pattern confirms that the MILP adds shuttles at the minimum necessary rate -- just in time to prevent the working-time constraint (Eq. 12) from becoming infeasible. The high average utilization minimizes capital idle time but leaves limited buffer for demand surges -- a consideration for risk-averse planners (see Section 4.5).

---

## 3.4 Cost Structure

Fig. 4 (D6) decomposes NPC into six components for each case at optimal configurations. The cost structure differs fundamentally between Case 1 and Cases 2/3:

**Table 6: NPC cost breakdown at optimal configurations (USD M)**

| Component | Case 1 | % | Case 2 | % | Case 3 | % |
|-----------|-------:|--:|--------:|--:|--------:|--:|
| Shuttle CAPEX | 211.97 | 47.4 | 384.21 | 42.4 | 422.39 | 38.6 |
| Bunkering CAPEX | 15.06 | 3.4 | 16.24 | 1.8 | 17.86 | 1.6 |
| Shuttle fOPEX | 114.84 | 25.7 | 208.15 | 23.0 | 228.84 | 20.9 |
| Shuttle vOPEX | 80.84 | 18.1 | 275.01 | 30.3 | 400.97 | 36.6 |
| Bunkering fOPEX | 8.16 | 1.8 | 8.80 | 1.0 | 9.67 | 0.9 |
| Bunkering vOPEX | 16.67 | 3.7 | 14.39 | 1.6 | 14.39 | 1.3 |
| **Total NPC** | **447.53** | **100** | **906.80** | **100** | **1,094.12** | **100** |

Case 1 is capital-intensive: shuttle CAPEX (\$211.97M, 47.4%) and shuttle fOPEX (\$114.84M, 25.7%) together account for 73.1% of NPC, while shuttle vOPEX is only 18.1% (\$80.84M). This reflects the short travel distance (1.0 h one-way), which minimizes fuel consumption per cycle. However, the shuttle vOPEX share is higher than might be expected for an intra-port operation, because the small 1,000 m$^3$ shuttle requires 5 trips per bunkering call, accumulating fuel consumption across multiple transits.

Cases 2 and 3 are operations-intensive: shuttle vOPEX rises to 30.3% (\$275.01M) and 36.6% (\$400.97M) respectively, driven by the longer round-trip travel times (7.86 h for Ulsan, 11.46 h for Yeosu) and correspondingly higher fuel consumption per cycle. The vOPEX increase from Case 1 to Case 3 is \$320.13M -- representing the cumulative fuel cost of traversing 172 nm (86 nm round trip) per shuttle cycle over 21 years. This structural shift from CAPEX-dominated to vOPEX-dominated cost has practical consequences: Case 1 costs are front-loaded (CAPEX at procurement) and predictable, while Cases 2 and 3 costs are distributed over the operating life and sensitive to fuel price fluctuations.

---

## 3.5 LCOA Comparison

Fig. 5 (D9) presents LCOA across all cases. Case 1 achieves \$1.90/ton, which represents the minimum unit cost of ammonia delivery from storage to vessel. Case 2 at \$3.85/ton is 103% higher, and Case 3 at \$4.64/ton is 144% higher. These differences persist across all shuttle size configurations, confirming that the cost advantage is structural (driven by travel distance and cycle time) rather than incidental.

The total ammonia supply over the 21-year horizon (2030--2050) is identical across all three cases ($235{,}620{,}000$ tons), because all share the same demand trajectory (50 to 500 vessels, 12 voyages/year, 5,000 m$^3$/call). The annualized cost ranges from \$41.30M/year (Case 1) to \$100.98M/year (Case 3), indicating that the additional annual cost of sourcing from Yeosu rather than local storage is \$59.68M/year.

---

## 3.6 Pump Rate Sensitivity

Fig. 14 (S7) shows how NPC responds to pump rate variation from 100 to 1,500 m$^3$/h. For Case 1, NPC decreases from \$838.62M at 100 m$^3$/h to \$397.76M at 1,500 m$^3$/h, exhibiting strong concavity: the marginal benefit of pump rate increases falls rapidly at higher flow rates. At the baseline pump rate of 500 m$^3$/h (NPC = \$447.53M), a doubling to 1,000 m$^3$/h saves \$37.19M (8.3%), whereas halving to 250 m$^3$/h would increase NPC by approximately \$149M (33%).

The optimal shuttle size exhibits a pump-rate-dependent transition. At 300--500 m$^3$/h, the 1,000 m$^3$ shuttle is optimal because the slow pump rate penalizes larger shuttles disproportionately (pumping time = $V_s/Q_p$ grows linearly with shuttle size). Above 600 m$^3$/h, the optimum shifts to 2,500 m$^3$ because faster pumping reduces the cycle time penalty of larger shuttles, allowing CAPEX economies of scale to dominate. This interaction between pump rate and optimal shuttle size demonstrates the coupling identified in Gap 1: the three decision variables (shuttle size, pump rate, fleet size) cannot be optimized independently.

For Case 2, the optimal shuttle remains 5,000 m$^3$ across all tested pump rates, with NPC decreasing from \$1,558.15M (100 m$^3$/h) to \$820.25M (1,100 m$^3$/h). NPC stabilizes above 1,100 m$^3$/h, with a slight increase at 1,200+ m$^3$/h due to diminishing cycle time reduction being offset by increased pump CAPEX. Case 3 shows a similar pattern, with NPC declining from \$1,744.89M to \$996.28M over the same range. The practical implication is that pump rates above 1,000--1,100 m$^3$/h yield diminishing returns for all configurations.

---

## 3.7 Parametric Sensitivity

### Tornado Analysis

Fig. 10 (FIG7) presents tornado diagrams showing the NPC swing from +/-20% variation of six parameters. For Case 1:

**Table 7: Tornado sensitivity ranking (Case 1, base NPC = \$447.53M)**

| Rank | Parameter | Low NPC (USD M) | High NPC (USD M) | Swing (USD M) | Swing (%) |
|:----:|-----------|:---------------:|:-----------------:|:-------------:|:---------:|
| 1 | CAPEX Scaling | 304.48 | 696.30 | 391.82 | 87.6 |
| 2 | Max Annual Hours | 389.78 | 531.80 | 142.02 | 31.7 |
| 3 | Travel Time | 420.17 | 472.54 | 52.37 | 11.7 |
| 4 | Fuel Price | 428.03 | 467.03 | 39.00 | 8.7 |
| 5 | SFOC | 428.03 | 467.03 | 39.00 | 8.7 |
| -- | Bunker Volume | 359.09 | Infeasible | -- | -- |

The CAPEX scaling exponent dominates Case 1 sensitivity, with a swing of \$391.82M (87.6% of base NPC). This occurs because $\alpha$ enters the cost function exponentially (Eq. 15): reducing $\alpha$ from 0.75 to 0.60 substantially flattens the CAPEX curve, while increasing to 0.90 steepens it. Bunker volume is not ranked because a +20% increase (from 5,000 to 6,000 m$^3$) renders the 1,000 m$^3$ shuttle infeasible: $n_{\text{trip}} = \lceil 6{,}000/1{,}000 \rceil = 6$ trips at 13.43 h each yields a call duration of 80.57 h, exceeding the 80 h maximum. This infeasibility boundary is itself a finding: the optimal 1,000 m$^3$ shuttle operates with essentially zero margin on the call duration constraint, meaning that any increase in per-call demand would necessitate a larger shuttle or faster pump.

SFOC and Fuel Price produce identical swings (\$39.00M, 8.7%) for Case 1 because both scale shuttle fuel costs proportionally (Eq. 23): a 20% SFOC increase has the same NPC effect as a 20% fuel price increase.

For Case 2 (Ulsan, base NPC = \$906.80M), bunker volume becomes the top-ranked parameter with a swing of \$974.86M (107.5%), followed by CAPEX scaling (\$386.82M, 42.7%) and maximum annual hours (\$245.43M, 27.1%). For Case 3 (Yeosu, base NPC = \$1,094.12M), CAPEX scaling ranks first among finite swings (\$425.26M, 38.9%), followed by maximum annual hours (\$278.02M, 25.4%) and travel time (\$239.00M, 21.8%); bunker volume also causes infeasibility at +20%. The shift in sensitivity ranking across cases -- from CAPEX-driven (Case 1) to demand-driven (Cases 2/3) -- mirrors the cost structure shift observed in Section 3.4.

### Fuel Price Sensitivity

Fig. 11 (FIG8) shows NPC and LCOA response to fuel price across \$300--\$1,200/ton. For Case 1, NPC ranges from \$398.78M (\$300/ton, $-10.9\%$) to \$545.04M (\$1,200/ton, $+21.8\%$). The response is linear, consistent with fuel cost being a constant fraction of NPC. LCOA scales linearly from \$1.69/ton to \$2.31/ton across the same range.

Cases 2 and 3 exhibit steeper fuel price sensitivity due to their higher vOPEX shares. Case 2 NPC ranges from \$762.10M (\$300/ton, $-16.0\%$) to \$1,196.20M (\$1,200/ton, $+31.9\%$), while Case 3 ranges from \$886.44M ($-19.0\%$) to \$1,509.48M ($+38.0\%$). The steeper slope for remote supply cases reinforces the finding that fuel price uncertainty disproportionately affects configurations with longer travel distances. At \$1,200/ton, the Case 3 to Case 1 NPC ratio rises to 2.77$\times$ (from 2.45$\times$ at baseline), widening the port-based storage advantage under high fuel price scenarios.

---

## 3.8 Demand Scenario Analysis

Fig. 13 (FIG10) compares NPC and LCOA across four demand scenarios (Table 8).

**Table 8: Demand scenario results (all cases)**

| Scenario | End Vessels | Case 1 NPC (M) | Case 1 LCOA | Case 2 NPC (M) | Case 2 LCOA | Case 3 NPC (M) | Case 3 LCOA |
|----------|:---------:|:-------------:|:----------:|:----------------:|:------------:|:----------------:|:------------:|
| Low | 250 | 251.18 | 1.95 | 502.99 | 3.91 | 604.29 | 4.70 |
| Base | 500 | 447.53 | 1.90 | 906.80 | 3.85 | 1,094.12 | 4.64 |
| High | 750 | 646.83 | 1.89 | 1,310.62 | 3.82 | 1,582.03 | 4.62 |
| VeryHigh | 1,000 | 847.31 | 1.88 | 1,714.43 | 3.81 | 2,066.11 | 4.59 |

Two findings are central:

**Finding 1: LCOA stability.** Case 1 LCOA ranges from \$1.88 to \$1.95/ton across a 4$\times$ demand variation (250 to 1,000 end-vessels), a variation of only 3.7% (\$0.07/ton). This near-constant marginal cost arises because the MILP scales fleet size proportionally with demand -- doubling demand approximately doubles both total cost and total supply, leaving LCOA unchanged. The slight decline at higher demand (\$1.95 $\to$ \$1.88) reflects economies of scale: fixed components (e.g., bunkering CAPEX per shuttle) are spread over more delivered ammonia. Cases 2 and 3 show similar LCOA stability: 2.6% (\$3.81--\$3.91) and 2.4% (\$4.59--\$4.70) variation respectively.

**Finding 2: Optimal shuttle size invariance.** The optimal shuttle remains 1,000 m$^3$ (Case 1), 5,000 m$^3$ (Case 2), and 5,000 m$^3$ (Case 3) across all four demand scenarios. This invariance confirms that the optimal shuttle specification is determined by the cycle time structure (shore loading time, transit time, pumping time) rather than by demand volume. Because all three cases maintain their optimal shuttle sizes across a 4$\times$ demand range, the specification decision is fully decoupled from the demand forecast.

The practical implication for port planners is that shuttle vessel specifications can be committed early in the planning process without waiting for demand clarity. The timing of fleet additions (not the specifications) is the demand-sensitive decision. This separation of specification-robustness from scheduling-sensitivity reduces planning risk.

---

### 3.9 Discount Rate Sensitivity

The base case assumes zero discounting (Assumption A2), treating all years equally. To validate this assumption, we test three discount rates: $r$ = 0%, 5%, and 8% across all three cases. Table 9 summarizes the results.

**Table 9: Discount rate sensitivity -- optimal configurations remain invariant**

| Case | $r$ = 0% NPC | $r$ = 5% NPC | $r$ = 8% NPC | Optimal Shuttle | Optimal Pump |
|------|-------------|-------------|-------------|-----------------|--------------|
| Case 1 | \$447.53M | \$246.30M | \$180.36M | 1,000 m$^3$ | 500 m$^3$/h |
| Case 2 | \$906.80M | \$499.03M | \$365.39M | 5,000 m$^3$ | 500 m$^3$/h |
| Case 3 | \$1,094.12M | \$601.94M | \$440.64M | 5,000 m$^3$ | 500 m$^3$/h |

The key finding is that **optimal shuttle specifications are invariant across all discount rates**. While NPC decreases by approximately 59.7% from $r$ = 0% to $r$ = 8% (because future costs are discounted more heavily), the relative cost ranking across shuttle sizes remains unchanged. Case 1 selects 1,000 m$^3$, and both Cases 2 and 3 select 5,000 m$^3$ regardless of discounting assumptions.

Fig. 15 presents the NPC and LCOA response to discount rate for all three cases. The LCOA follows the same pattern: Case 1 ranges from \$1.90/ton ($r$ = 0%) to \$0.77/ton ($r$ = 8%), while maintaining the cost advantage over Cases 2 and 3 at every discount rate.

Fig. 16 shows fleet evolution under different discount rates. The physical fleet requirement (number of shuttles needed to serve demand) is determined by cycle time and demand volume, not by financial discounting. Consequently, fleet expansion timelines are identical across discount rates -- the same number of 1,000 m$^3$ shuttles are added in the same years regardless of $r$, because the physical constraint (Eq. 12) is independent of the discount rate.

These results validate Assumption A2: while the choice of discount rate affects the reported NPC magnitude, it does not affect the infrastructure specification recommendations or the relative ranking of supply chain configurations. Port authorities can use the zero-discount results as a conservative upper bound on NPC while maintaining confidence in the shuttle sizing recommendations.

---

## 4. Discussion

## 4.1 Local Storage vs Remote Supply: Break-Even Analysis

The results in Section 3.1 establish that port-based storage (Case 1) is substantially cheaper than remote supply at the actual distances of Ulsan (59 nm) and Yeosu (86 nm). We parameterize the one-way travel distance from 10 to 200 nm to identify whether break-even crossover points exist.

Fig. 12 (FIG9) presents the break-even distance analysis. For the Ulsan comparison (5,000 m$^3$ shuttle for both cases), Case 1 NPC remains constant at \$519.14M (the Case 1 NPC at 5,000 m$^3$ shuttle, independent of remote supply distance), while Case 2 NPC increases with distance from \$546.81M at 10 nm to \$1,447.75M at 200 nm. Case 1 is cheaper at every distance tested, including at the minimum distance of 10 nm where the difference is \$27.67M. No crossover occurs within the 10--200 nm range.

For the Yeosu comparison (also using 5,000 m$^3$ shuttle), no crossover occurs either. Case 3 NPC ranges from \$584.46M at 10 nm to \$1,876.82M at 200 nm, always exceeding Case 1's \$519.14M. Even at the shortest distance tested (10 nm), remote supply costs \$65.32M more than port-based storage.

The absence of any break-even crossover -- even at distances as short as 10 nm -- is a stronger finding than previously expected. It occurs because at 500 m$^3$/h pump rate, the shuttle pumping time ($v_{\text{call}}/Q_p = 5{,}000/500 = 10.0$ h per vessel) dominates the cycle time budget for remote supply cases. Even minimal travel distance cannot offset this pumping time penalty when combined with the shore loading overhead (11.14 h) and port entry/exit procedures. The fixed components of remote supply cycle time (shore loading + port procedures + pumping = 11.14 + 2.0 + 15.0 = 28.14 h for a single vessel) already exceed the entire Case 1 cycle time (13.43 h), before any travel time is added.

**Optimal-vs-optimal comparison.** When Case 1 uses its optimal 1,000 m$^3$ shuttle (\$447.53M) versus remote supply using their optimal 5,000 m$^3$ shuttles (\$906.80M for Case 2, \$1,094.12M for Case 3), the cost advantage widens further. Port-based storage with a small, efficient shuttle is 2.0--2.4$\times$ cheaper than remote supply at actual distances, with no prospect of equalization within the 10--200 nm range. This happens because port-based storage enables a fundamentally smaller shuttle (1,000 vs 5,000 m$^3$), with correspondingly lower CAPEX per unit.

This decision rule is transferable to other ports: for ammonia bunkering at 500 m$^3$/h pump rate with 5,000 m$^3$ per-call demand, port-based storage dominates remote supply at all distances. The dominance is driven by the high pumping time at moderate pump rates, which makes the remote supply cycle time inherently longer regardless of travel distance.

---

## 4.2 Robustness of Infrastructure Decisions

The sensitivity analyses in Sections 3.6--3.9 collectively address the question: how confident can planners be in the optimal specifications?

**Shuttle size specification** is robust across most tested uncertainty dimensions. The Case 1 optimal (1,000 m$^3$) is unchanged by: fuel price variation from \$300 to \$1,200/ton (Section 3.7), demand variation from 250 to 1,000 end-vessels (Section 3.8), and discount rate variation from 0% to 8% (Section 3.9). The specification does change with pump rate: above 600 m$^3$/h, the optimal shifts from 1,000 to 2,500 m$^3$ (Section 3.6). This pump-rate dependence underscores the importance of the pump sizing decision -- it is the key parameter that determines the optimal shuttle size.

**LCOA** is remarkably stable: \$1.88--\$1.95/ton across a 4$\times$ demand range (Section 3.8), and \$1.69--\$2.31/ton across a 4$\times$ fuel price range (Section 3.7). The combined uncertainty envelope (demand $\times$ fuel price) produces an LCOA range of approximately \$1.50--\$2.80/ton for Case 1 -- primarily driven by fuel price.

**Fleet expansion timing** is the demand-sensitive component. While the shuttle specification is fixed, the year in which each new shuttle must be procured depends on when cumulative demand crosses the capacity threshold. Under the VeryHigh scenario (1,000 end-vessels), the fleet grows to approximately 101 shuttles (vs 51 under Base), but the same 1,000 m$^3$ vessel specification is procured throughout.

**Primary risk factor:** The tornado analysis identifies the CAPEX scaling exponent ($\alpha$) as the dominant uncertainty for Case 1 (87.6% NPC swing, Section 3.7). In practical terms, this means that the accuracy of shipyard cost estimates matters more than fuel price forecasts or demand projections. A 20% error in the scaling exponent would change NPC by \$391.82M, dwarfing the impact of fuel price uncertainty (\$39.00M) or travel time variation (\$52.37M). Port authorities should invest in detailed shipyard quotations for ammonia shuttle vessels before committing to fleet procurement.

**Infeasibility boundary:** A second risk factor unique to the 1,000 m$^3$ shuttle is the call duration constraint. At 5,000 m$^3$ per call, the 1,000 m$^3$ shuttle requires 5 trips totaling 67.14 h, leaving only 12.86 h of margin below the 80 h maximum. A 20% increase in bunker volume (to 6,000 m$^3$) causes infeasibility. This constraint margin is tighter than for larger shuttles and suggests that if per-call demand may exceed 5,000 m$^3$, a larger shuttle (e.g., 1,500 or 2,500 m$^3$) should be considered as a hedge, accepting a modest NPC penalty (\$521.98M and \$454.38M respectively).

---

## 4.3 Practical Implications for Green Corridor Planning

The results support three actionable recommendations for port authorities:

**Recommendation 1: Build port-based storage.** For ports with demand profiles similar to Busan, port-based storage with small-shuttle intra-port distribution minimizes 21-year cost. The break-even analysis (Section 4.1) shows no distance at which remote supply becomes cheaper at the 500 m$^3$/h pump rate baseline. Even at 10 nm -- closer than any realistic ammonia source -- port-based storage costs less than remote supply when using the same shuttle size, and the advantage widens dramatically at optimal configurations.

**Recommendation 2: Commit to shuttle specifications early, but fix pump rate first.** The optimal shuttle size is invariant to demand uncertainty across a 4$\times$ range (Section 3.8) and to discount rate (Section 3.9). However, it is sensitive to pump rate: 1,000 m$^3$ is optimal at 500 m$^3$/h, while 2,500 m$^3$ is optimal at 600+ m$^3$/h. Port authorities should therefore finalize the bunkering pump specification before committing to shuttle vessel procurement. Once the pump rate is fixed, the shuttle specification follows deterministically.

**Recommendation 3: Monitor shipyard costs and bunker volume as primary risk variables.** The CAPEX scaling exponent accounts for 87.6% of NPC sensitivity (Section 3.7), making shipyard cost accuracy the highest-priority uncertainty. Additionally, the 1,000 m$^3$ shuttle has a tight call duration margin (67.14 h of 80 h maximum), meaning that any increase in per-call bunker volume could force a shuttle size increase. Competitive bidding among shipyards and conservative bunker volume estimates would mitigate these risks.

These recommendations apply to the Korea--US and Korea--Australia green corridor initiatives where ammonia bunkering at Busan Port is under active planning.

---

### 4.4 Comparison with Published DES Model

To position our results within the existing literature, we compare our MILP framework with the discrete event simulation (DES) model of Yang and Lam [11], the most directly relevant published study on ammonia bunkering operations. Table 10 summarizes the key methodological differences.

**Table 10: Methodology comparison -- MILP vs. DES for ammonia bunkering**

| Dimension | Yang & Lam DES [11] | This study (MILP) |
|-----------|--------------------|--------------------|
| Objective | Operational performance evaluation | Infrastructure investment optimization |
| Fleet sizing | Fixed input (2--4 vessels) | Optimized output (6--51 vessels, Case 1) |
| Time horizon | 1-year snapshot | 21-year dynamic (2030--2050) |
| Cost scope | OPEX only (charter + fuel) | Full lifecycle (CAPEX + OPEX) |
| Demand | Static | Growing trajectory (50--500 vessels) |
| Service time | Stochastic (TRIA distribution) | Deterministic (formula-based) |
| Queuing | Explicit (event-driven) | Implicit (utilization constraint) |
| Supply configs | Single | Three (port storage, Ulsan, Yeosu) |

The two approaches are complementary rather than competing: DES captures queuing dynamics and stochastic service time variability that our deterministic MILP does not model, while the MILP optimizes fleet sizing and multi-year investment timing that DES evaluates but does not optimize.

The pumping time component -- the time required to transfer ammonia from shuttle to receiving vessel, calculated as $V / Q_p$ -- is consistent across both models, as it is derived from the same physical relationship. At three validation points from Yang and Lam's Table 4 (855, 1,384, and 2,000 tons), the raw gap between our MILP service time estimates and their DES output is 4.6--5.9%, attributable to operational overhead (mooring procedures ~1.55 h and documentation ~0.84 h) that their DES explicitly models but our MILP subsumes into the setup time parameter (Fig. 17). This difference reflects scope rather than inconsistency: the MILP's purpose is infrastructure sizing, not operational scheduling.

A more substantive comparison emerges from flow rate sensitivity analysis. Both models identify bunkering flow rate as the dominant operational parameter: Yang and Lam report a 51.3% impact on service time when flow rate varies by +/-50%, while our MILP yields a 37.7% variation over a matched parameter range (Fig. 18). The 13.6 percentage-point gap is structural: the DES uses triangular (TRIA) distributions for service time components, which smooth extreme values through probabilistic averaging, whereas our deterministic formula amplifies the effect of flow rate at the extremes. This difference is expected and informative -- it quantifies the extent to which stochastic modeling attenuates parameter sensitivity relative to deterministic analysis.

Beyond flow rate, our MILP framework enables sensitivity analysis across investment-side parameters (CAPEX scaling exponent, bunker volume, demand trajectory) that the DES framework, focused on operational performance, does not address. The tornado analysis (Section 3.7) reveals that CAPEX scaling exponent dominates NPC sensitivity for Case 1 at 87.6% swing -- a finding inaccessible through operational simulation alone.

These complementary strengths suggest a hybrid DES-MILP approach as a promising research direction (Future Work item F2): use the MILP to determine optimal fleet size and specifications, then validate operational feasibility through DES simulation incorporating queuing effects and stochastic service times.

---

## 4.5 Limitations and Future Work

### Limitations

**L1. Deterministic demand (linear growth).** We model demand as a linear trajectory from 50 to 500 vessels. Actual ammonia adoption may follow an S-curve, with slower initial uptake and potential acceleration post-2040 as regulations tighten (IMO CII trajectory). Under S-curve demand, early-year fleet overcapacity would persist longer, increasing capital lock-up by an estimated 8--12%. Conversely, late-period demand surges could outpace fleet additions if procurement lead times exceed 2--3 years. Direction of error: NPC may be underestimated by 5--10% under S-curve demand.

**L2. Fixed fuel price.** The \$600/ton baseline is held constant over 21 years. Green ammonia production costs are projected to decline from \$700--\$1,400/ton (2025) to \$310--\$660/ton (2030--2040) as electrolyzer costs fall. A declining price trajectory would reduce Cases 2 and 3 vOPEX over time, potentially narrowing the Case 1 cost gap in later years. Direction: the cost advantage of port-based storage may narrow by 5--15% under declining fuel price scenarios.

**L3. No discounting.** The zero discount rate treats a dollar spent in 2030 equally to a dollar spent in 2050. Section 3.9 shows that while NPC decreases by ~60% at $r$ = 8%, optimal specifications are invariant. Direction: NPC magnitude changes but infrastructure recommendations do not.

**L4. SFOC fixed per size class.** The engine SFOC map assigns constant values per size class (Table 3). Real-world SFOC varies with engine load (typically +10--15% at partial load vs design point). For Cases 2 and 3, where shuttles may operate below design speed during port maneuvering, actual fuel consumption could be 5--10% higher than modeled. Direction: Cases 2 and 3 NPC may be underestimated by 3--5%.

**L5. No port congestion or queuing.** We assume vessels arrive uniformly throughout the year. In practice, seasonal and weekly demand peaks create queuing effects that could increase effective cycle time by 10--20% during peak periods. The daily peak factor ($F_{\text{peak}} = 1.5$) provides partial mitigation but does not replace a queuing model. Direction: fleet size may be underestimated by 1--2 shuttles during peak years.

**L6. Single bunker volume.** All vessels are assumed to require 5,000 m$^3$ per call. In practice, vessel sizes range from small feeders (~1,000 m$^3$) to large container ships (~8,000 m$^3$). Variable bunker volumes would create an order-sizing problem (matching shuttle loads to vessel needs). Direction: heterogeneous demand could increase LCOA by 5--15% due to suboptimal load matching. This is particularly relevant for the 1,000 m$^3$ shuttle, which is near the call duration constraint boundary and cannot accommodate larger per-call demands.

**L7. Ammonia toxicity and safety costs not modeled.** Ammonia is acutely toxic and requires safety exclusion zones, gas detection systems, and emergency response capabilities during bunkering [18, 19, 20]. These safety infrastructure costs are not included in NPC. The additional safety costs could increase bunkering infrastructure cost by an estimated 5--15%, with potentially larger relative impact on Case 1 where bunkering occurs within the congested port area. Direction: NPC may be underestimated for all cases.

### Future Work

**F1. Stochastic MILP with demand and price uncertainty.** Extend the deterministic model to a two-stage stochastic MILP with first-stage (shuttle specification) and second-stage (fleet expansion schedule) decisions under joint demand-price scenarios.

**F2. Port queuing simulation coupled with MILP.** Develop a hybrid DES-MILP approach where the DES captures queuing effects (building on Yang and Lam [11]) and the MILP optimizes fleet sizing given queuing-adjusted cycle times.

**F3. Multi-fuel bunkering comparison.** Apply the framework to methanol and LNG bunkering infrastructure at Busan, enabling a cross-fuel comparison of LCOA and fleet requirements.

**F4. Real-options analysis for staged investment.** Replace the deterministic planning horizon with a real-options model that values the flexibility to defer or accelerate shuttle procurement in response to demand signals.

**F5. Multi-port network extension.** Extend the single-port model to a network of Korean ports (Busan, Ulsan, Incheon) with shared shuttle fleets and inter-port transfers.

---

## 5. Conclusions

This study developed a mixed-integer linear programming model for optimizing ammonia bunkering infrastructure at Busan Port over a 21-year planning horizon (2030--2050). The model systematically evaluates all feasible shuttle-pump combinations and optimizes year-by-year fleet expansion for three supply chain configurations: port-based storage (Case 1), remote supply from Ulsan (Case 2, 59 nm), and remote supply from Yeosu (Case 3, 86 nm).

Four main findings emerge:

First, the optimal infrastructure specifications differ across cases due to the interaction between pump rate, CAPEX scaling, and cycle time. At 500 m$^3$/h pump rate, Case 1 selects a 1,000 m$^3$ shuttle (NPC \$447.53M, LCOA \$1.90/ton), while Cases 2 and 3 both require 5,000 m$^3$ shuttles at 2.0--2.4 times higher cost (\$906.80M and \$1,094.12M respectively). The small optimal shuttle for Case 1 reflects the slow pump rate, which penalizes larger shuttles through longer cycle times.

Second, port-based storage dominates remote supply at all distances within 10--200 nm when the bunkering pump rate is 500 m$^3$/h. No break-even crossover exists even at 10 nm, because the fixed components of the remote supply cycle (shore loading, pumping, port procedures) already exceed the entire Case 1 cycle time. This provides a transferable decision rule: at moderate pump rates, build local storage rather than relying on remote supply.

Third, optimal shuttle specifications are robust to demand uncertainty: across a 4$\times$ demand range (250 to 1,000 end-vessels), the optimal shuttle size remains unchanged and LCOA varies by only 3.7% for Case 1. Specifications are also invariant to discount rate (0--8%). However, they are sensitive to pump rate, making the pump specification the pivotal decision.

Fourth, the cost driver hierarchy differs fundamentally between configurations: CAPEX scaling dominates port-based storage (87.6% NPC swing), while bunker volume dominates remote supply (107.5% for Case 2). The 1,000 m$^3$ shuttle operates near the call duration constraint boundary (67.14 h of 80 h maximum), creating an infeasibility risk if per-call demand increases -- a risk that can be mitigated by choosing a 1,500 or 2,500 m$^3$ shuttle at modest cost premium.

These results provide quantitative decision tools for port authorities, shipping companies, and policymakers planning ammonia bunkering infrastructure for green shipping corridors. The framework is readily applicable to other ports by substituting local distances, shuttle candidate sets, pump rates, and demand projections.

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

**Fig. 1.** Cycle time components for three supply chain configurations. The stacked bar chart decomposes each cycle into shore loading, transit, connection/disconnection, and pumping phases. Case 1 (Busan port storage) has the shortest cycle at 13.43 h due to minimal transit time (1.0 h one-way), while Case 3 (Yeosu, 86 nm) requires 39.60 h per cycle.

**Fig. 2.** Net present cost as a function of shuttle vessel size for all three cases at 500 m$^3$/h pump rate. Case 1 achieves its minimum of \$447.53M at 1,000 m$^3$. Cases 2 and 3 both show optima at 5,000 m$^3$, reflecting the cycle time penalties of larger shuttles due to increased shore loading time.

**Fig. 3.** NPC comparison across cases at optimal configurations. Case 3 (Yeosu) NPC is 2.45$\times$ Case 1, and Case 2 (Ulsan) is 2.03$\times$ Case 1.

**Fig. 4.** Cost component breakdown showing six NPC components at optimal configurations. Case 1 is capital-intensive (73.1% CAPEX+fOPEX), whereas Cases 2 and 3 shift toward operations-intensive cost structures with shuttle vOPEX rising to 30--37%.

**Fig. 5.** Levelized cost of ammonia bunkering (LCOA) across all cases and shuttle sizes. Case 1 achieves \$1.90/ton, with 103% premium for Case 2 (\$3.85/ton) and 144% premium for Case 3 (\$4.64/ton).

**Fig. 6.** Annual cost evolution (2030--2050) showing step-function growth correlated with fleet additions.

**Fig. 7.** Fleet size evolution over the planning horizon. Case 1 fleet grows from 6 to 51 shuttles (1,000 m$^3$); Cases 2 and 3 grow from 3 to approximately 27--30 shuttles (5,000 m$^3$).

**Fig. 8.** Annual bunkering demand and fleet response showing staircase supply capacity versus smooth demand growth.

**Fig. 9.** Fleet utilization rates over time displaying sawtooth pattern as demand grows against fixed fleet capacity.

**Fig. 10.** Tornado diagram showing parametric sensitivity of NPC for all three cases. CAPEX scaling dominates Case 1 (87.6% swing); bunker volume dominates Case 2 (107.5% swing).

**Fig. 11.** Fuel price sensitivity: NPC and LCOA response across \$300--\$1,200/ton. Remote supply cases show steeper sensitivity due to higher vOPEX shares.

**Fig. 12.** Break-even distance analysis: Case 1 vs Cases 2 and 3. No crossover occurs within 10--200 nm; port-based storage dominates at all distances.

**Fig. 13.** Demand scenario analysis: NPC and LCOA across four growth trajectories (250--1,000 end-vessels). Optimal shuttle sizes remain invariant.

**Fig. 14.** Pump rate sensitivity analysis showing NPC response from 100 to 1,500 m$^3$/h. Case 1 optimal shifts from 1,000 to 2,500 m$^3$ above 600 m$^3$/h.

**Fig. 15.** Discount rate sensitivity: NPC and LCOA across 0%, 5%, 8%. Optimal specifications invariant.

**Fig. 16.** Fleet evolution under different discount rates showing identical fleet expansion timelines.

**Fig. 17.** Service time comparison with Yang & Lam DES model at three validation points. Raw gap of 4.6--5.9% attributable to operational overhead outside MILP scope.

**Fig. 18.** Flow rate sensitivity comparison: MILP vs DES. Gap of 13.6 percentage points explained by DES stochastic averaging.
