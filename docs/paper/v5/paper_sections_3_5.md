## 3. Results and Analysis

### 3.1 Optimal Configurations

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

Fig. 2 shows the NPC as a function of shuttle size for all three cases. Each curve exhibits a piecewise cost landscape shaped by the integer-valued trip count $n_{\text{trip}}$ (Eq. 4), with a global minimum at an interior point. At the baseline pump rate of 500 m$^3$/h, Case 1 achieves its minimum NPC of \$447.53M at 1,000 m$^3$ -- the second-smallest candidate in the set. This small optimal shuttle reflects the slow pump rate: at 500 m$^3$/h, a 1,000 m$^3$ shuttle takes $T_{\text{pump}} = 1{,}000/500 = 2.0$ h per transfer, yielding $T_{\text{cycle}} = 13.43$ h and enabling 595.74 annual cycles per shuttle ($H_{\max}/T_{\text{cycle}} = 8{,}000/13.43$). Increasing shuttle size to 2,500 m$^3$ raises cycle time to 18.57 h (a 38% increase) but reduces trips per call from 5 to 2, resulting in a slightly higher NPC of \$454.38M (+1.5%). The 5,000 m$^3$ shuttle, which requires only 1 trip per call, costs \$519.14M (+16.0%) due to substantially longer cycle times ($T_{\text{cycle}} = 27.14$ h). The CAPEX scaling exponent ($\alpha = 0.75$) means that doubling shuttle capacity increases unit cost by a factor of $2^{0.75} = 1.68$ rather than twofold, producing economies of scale that are overwhelmed at 500 m$^3$/h pump rate by the cycle time penalty of slower pumping for larger shuttles.

The optimal 1,000 m$^3$ shuttle requires five sequential round trips to complete a single 5,000 m$^3$ bunkering call. While this is the cost-minimizing configuration under the model's deterministic assumptions, in practice multiple sequential ship-to-ship transfers increase operational complexity, cumulative connection and disconnection procedures, and the associated risk of ammonia leakage at each transfer point. The result should therefore be interpreted as an economic lower bound that assumes ideal operating conditions; operational risk considerations may favor a larger shuttle (e.g., 2,500 m$^3$, two trips per call) at a modest cost premium of 1.5%.

For Cases 2 and 3, both achieve minimum NPC at 5,000 m$^3$ -- the smallest candidate in their respective sets. At this size, $N_v = \lfloor 5{,}000/5{,}000 \rfloor = 1$ vessel is served per trip. The 2,500 m$^3$ shuttle (also available for Cases 2 and 3) is more expensive: Case 2 at 2,500 m$^3$ costs \$1,106.45M versus \$906.80M at 5,000 m$^3$ (+22.0%), because $n_{\text{trip}} = 2$ at 2,500 m$^3$ doubles the shuttle operating hours per call. For Case 3, the same pattern holds with \$1,375.75M at 2,500 m$^3$ versus \$1,094.12M at 5,000 m$^3$ (+25.7%).

Fig. 3 confirms the cross-case cost hierarchy: Case 3 NPC exceeds Case 1 by a factor of 2.45, and Case 2 exceeds Case 1 by a factor of 2.03. This ordering holds across all shuttle sizes, indicating that the port-based storage advantage is structural rather than configuration-dependent. The LCOA metric normalizes for total supply volume: at \$1.90/ton (Case 1) versus \$4.64/ton (Case 3), the per-ton cost of remote supply from Yeosu is \$2.74/ton higher, representing a premium of 144%.

---

### 3.2 Temporal Dynamics

The MILP produces year-indexed fleet expansion schedules that reveal the discrete, lumpy nature of infrastructure investment. Fig. 7 shows cumulative fleet size over the 21-year planning horizon. For Case 1 (1,000 m$^3$ shuttle), the fleet grows in discrete steps from 6 shuttles in 2030 to 51 by 2050 as demand crosses capacity thresholds defined by Eq. (12). Each new shuttle adds 595.74 annual cycles of capacity (at $H_{\max} = 8{,}000$ h/year and $T_{\text{cycle}} = 13.43$ h), equivalent to serving approximately 119 additional bunkering calls per year (since $n_{\text{trip}} = 5$). The small shuttle size means the fleet is larger in absolute count, but each shuttle costs only \$3.87M, producing lower total CAPEX despite the higher count.

For Case 2 (5,000 m$^3$ shuttle), the fleet grows from 3 shuttles in 2030 to approximately 27 by 2050. Each shuttle adds 222.20 annual cycles, equivalent to 222 bunkering calls per year ($n_{\text{trip}} = 1$). For Case 3, the fleet grows from 3 shuttles to approximately 30 over the same period, reflecting the longer cycle time (39.60 h vs 36.00 h).

Fig. 8 overlays annual bunkering demand with fleet supply capacity. The demand curve is smooth (linear growth from 600 calls in 2030 to 6,000 in 2050), while the supply curve follows a staircase pattern. The gap between supply capacity and demand represents fleet slack -- periods of overcapacity immediately following a shuttle addition, which erodes as demand catches up.

Fig. 6 shows the annual cost evolution from 2030 to 2050. Cost growth exhibits a step function correlated with fleet additions: each new Case 1 shuttle triggers a jump in annualized CAPEX ($C_{\text{shuttle}} / \text{AF} = 3.87\text{M} / 10.8355 = 0.357$M/year) plus fixed OPEX. Between fleet additions, annual cost growth is driven solely by increasing variable OPEX as the number of bunkering calls rises with demand. This yields two distinct growth regimes: CAPEX-driven jumps at fleet expansion years, and vOPEX-driven gradual increases between them.

---

### 3.3 Operational Efficiency

Fig. 9 reveals a sawtooth utilization pattern over time. Utilization climbs as demand grows against a fixed fleet, reaching a peak just before the next shuttle addition, then drops when new capacity enters service. For Case 1, the theoretical maximum utilization is 100% ($\text{Annual\_Cycles\_Max} = H_{\max} / T_{\text{cycle}} = 8{,}000 / 13.43 = 595.74$, so the fleet operates at the $H_{\max}$ constraint boundary). In practice, utilization oscillates between approximately 84% immediately after shuttle additions and 99% just before the next addition, a sawtooth amplitude of roughly 15 percentage points. This tight oscillation reflects the small shuttle size: each 1,000 m$^3$ shuttle adds only 119 calls of annual capacity, meaning demand grows to fill the increment quickly.

This pattern confirms that the MILP adds shuttles at the minimum necessary rate -- just in time to prevent the working-time constraint (Eq. 12) from becoming infeasible. The high average utilization minimizes capital idle time but leaves limited buffer for demand surges -- a consideration for risk-averse planners (see Section 4.5).

---

### 3.4 Cost Structure

Fig. 4 decomposes NPC into six components for each case at optimal configurations. The cost structure differs fundamentally between Case 1 and Cases 2/3:

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

Case 1 is capital-intensive: shuttle CAPEX (\$211.97M, 47.4%) and shuttle fOPEX (\$114.84M, 25.7%) together account for 73.1% of NPC, while shuttle vOPEX is only 18.1% (\$80.84M). This reflects the intra-port transit distance (1.0 h one-way), which minimizes fuel consumption per cycle. However, the shuttle vOPEX share is higher than might be expected for an intra-port operation, because the small 1,000 m$^3$ shuttle requires 5 trips per bunkering call, accumulating fuel consumption across multiple transits.

Cases 2 and 3 are operations-intensive: shuttle vOPEX rises to 30.3% (\$275.01M) and 36.6% (\$400.97M) respectively, driven by the longer round-trip travel times (7.86 h for Ulsan, 11.46 h for Yeosu) and correspondingly higher fuel consumption per cycle. The vOPEX increase from Case 1 to Case 3 is \$320.13M -- representing the cumulative fuel cost of traversing 172 nm (86 nm round trip) per shuttle cycle over 21 years. This structural shift from CAPEX-dominated to vOPEX-dominated cost has practical consequences: Case 1 costs are front-loaded (CAPEX at procurement) and predictable, while Cases 2 and 3 costs are distributed over the operating life and sensitive to fuel price fluctuations.

---

### 3.5 LCOA Comparison

Fig. 5 presents LCOA across all cases. Case 1 achieves \$1.90/ton, which represents the minimum unit cost of ammonia delivery from storage to vessel. Case 2 at \$3.85/ton is 103% higher, and Case 3 at \$4.64/ton is 144% higher. These differences persist across all shuttle size configurations, confirming that the cost advantage is structural (driven by travel distance and cycle time) rather than incidental.

The total ammonia supply over the 21-year horizon (2030--2050) is 235,620,000 tons across all three cases, because all share the same demand trajectory (50 to 500 vessels, 12 voyages/year, 5,000 m$^3$/call, 0.681 ton/m$^3$ ammonia density). The annualized cost ranges from \$41.30M/year (Case 1) to \$100.98M/year (Case 3), indicating that the additional annual cost of sourcing from Yeosu rather than local storage is \$59.68M/year.

---

### 3.6 Pump Rate Sensitivity

Fig. 14 shows how NPC responds to pump rate variation from 100 to 1,500 m$^3$/h. For Case 1, NPC decreases from \$838.62M at 100 m$^3$/h to \$397.76M at 1,500 m$^3$/h, exhibiting strong concavity: the marginal benefit of pump rate increases falls rapidly at higher flow rates. At the baseline pump rate of 500 m$^3$/h (NPC = \$447.53M), a doubling to 1,000 m$^3$/h saves \$37.19M (8.3%), whereas halving to 250 m$^3$/h would increase NPC by approximately \$149M (33%).

The optimal shuttle size exhibits a pump-rate-dependent transition. At 300--500 m$^3$/h, the 1,000 m$^3$ shuttle is optimal because the slow pump rate penalizes larger shuttles disproportionately (pumping time = $V_s/Q_p$ grows linearly with shuttle size). Above 600 m$^3$/h, the optimum shifts to 2,500 m$^3$ because faster pumping reduces the cycle time penalty of larger shuttles, allowing CAPEX economies of scale to dominate. This interaction between pump rate and optimal shuttle size demonstrates the coupling identified in Gap 1: the three decision variables (shuttle size, pump rate, fleet size) cannot be optimized independently.

For Case 2, the optimal shuttle remains 5,000 m$^3$ across all tested pump rates, with NPC decreasing from \$1,558.15M (100 m$^3$/h) to \$820.25M (1,100 m$^3$/h). NPC stabilizes above 1,100 m$^3$/h, with a slight increase at 1,200+ m$^3$/h due to diminishing cycle time reduction being offset by increased pump CAPEX. Case 3 shows a similar pattern, with NPC declining from \$1,744.89M to \$996.28M over the same range. The practical implication is that pump rates above 1,000--1,100 m$^3$/h yield diminishing returns for all configurations.

---

### 3.7 Parametric Sensitivity

#### Tornado Analysis

Fig. 10 presents tornado diagrams showing the NPC swing from $\pm$20% variation of six parameters. All parameters are varied by the same $\pm$20% relative perturbation from their baseline values to enable fair comparison of sensitivity magnitudes across parameters. For Case 1:

**Table 7: Tornado sensitivity ranking (Case 1, base NPC = \$447.53M)**

| Rank | Parameter | Low NPC (USD M) | High NPC (USD M) | Swing (USD M) | Swing (%) |
|:----:|-----------|:---------------:|:-----------------:|:-------------:|:---------:|
| 1 | CAPEX Scaling | 304.48 | 696.30 | 391.82 | 87.6 |
| 2 | Max Annual Hours | 389.78 | 531.80 | 142.02 | 31.7 |
| 3 | Travel Time | 420.17 | 472.54 | 52.37 | 11.7 |
| 4 | Fuel Cost | 428.03 | 467.03 | 39.00 | 8.7 |
| -- | Bunker Volume | 359.09 | Infeasible | -- | -- |

The CAPEX scaling exponent dominates Case 1 sensitivity, with a swing of \$391.82M (87.6% of base NPC). This occurs because $\alpha$ enters the cost function exponentially (Eq. 15): reducing $\alpha$ from 0.75 to 0.60 substantially flattens the CAPEX curve, while increasing to 0.90 steepens it. Bunker volume is not ranked because a +20% increase (from 5,000 to 6,000 m$^3$) renders the 1,000 m$^3$ shuttle infeasible: $n_{\text{trip}} = \lceil 6{,}000/1{,}000 \rceil = 6$ trips at 13.43 h each yields a call duration of 80.57 h, exceeding the 80 h maximum call duration constraint (Eq. 14a). This infeasibility boundary is itself a finding: the optimal 1,000 m$^3$ shuttle operates with essentially zero margin on the call duration constraint, meaning that any increase in per-call demand would necessitate a larger shuttle or faster pump.

SFOC and fuel price produce identical NPC swings in this model because both enter the shuttle fuel cost equation (Eq. 23) as linear multiplicative factors. A 20% increase in SFOC has the same cost effect as a 20% increase in fuel price. In the tornado diagram, these two parameters are therefore consolidated as a single "fuel cost" entry (Table 7, rank 4), since they are perfectly correlated in the deterministic formulation and represent a single effective degree of freedom.

For Case 2 (Ulsan, base NPC = \$906.80M), bunker volume becomes the top-ranked parameter with a swing of \$974.86M (107.5%), followed by CAPEX scaling (\$386.82M, 42.7%) and maximum annual hours (\$245.43M, 27.1%). For Case 3 (Yeosu, base NPC = \$1,094.12M), CAPEX scaling ranks first among finite swings (\$425.26M, 38.9%), followed by maximum annual hours (\$278.02M, 25.4%) and travel time (\$239.00M, 21.8%); bunker volume also causes infeasibility at +20%. The shift in sensitivity ranking across cases -- from CAPEX-driven (Case 1) to demand-driven (Cases 2/3) -- mirrors the cost structure shift observed in Section 3.4.

#### Fuel Price Sensitivity

Fig. 11 shows NPC and LCOA response to fuel price across \$300--\$1,200/ton. For Case 1, NPC ranges from \$398.78M (\$300/ton, $-10.9\%$) to \$545.04M (\$1,200/ton, $+21.8\%$). The response is linear, consistent with fuel cost being a constant fraction of NPC. LCOA scales linearly from \$1.69/ton to \$2.31/ton across the same range.

Cases 2 and 3 exhibit steeper fuel price sensitivity due to their higher vOPEX shares. Case 2 NPC ranges from \$762.10M (\$300/ton, $-16.0\%$) to \$1,196.20M (\$1,200/ton, $+31.9\%$), while Case 3 ranges from \$886.44M ($-19.0\%$) to \$1,509.48M ($+38.0\%$). The steeper slope for remote supply cases reinforces the finding that fuel price uncertainty disproportionately affects configurations with longer travel distances. At \$1,200/ton, the Case 3 to Case 1 NPC ratio rises to 2.77 (from 2.45 at baseline), widening the port-based storage advantage under high fuel price scenarios.

---

### 3.8 Demand Scenario Analysis

Fig. 13 compares NPC and LCOA across four demand scenarios (Table 8). The sensitivity analysis fixes the optimal shuttle specification from the base case (1,000 m$^3$ for Case 1, 5,000 m$^3$ for Cases 2 and 3) and re-evaluates NPC by re-solving the fleet-sizing MILP under each demand trajectory.

**Table 8: Demand scenario results (all cases)**

| Scenario | End Vessels | Case 1 NPC (M) | Case 1 LCOA | Case 2 NPC (M) | Case 2 LCOA | Case 3 NPC (M) | Case 3 LCOA |
|----------|:---------:|:-------------:|:----------:|:----------------:|:------------:|:----------------:|:------------:|
| Low | 250 | 251.18 | 1.95 | 502.99 | 3.91 | 604.29 | 4.70 |
| Base | 500 | 447.53 | 1.90 | 906.80 | 3.85 | 1,094.12 | 4.64 |
| High | 750 | 646.83 | 1.89 | 1,310.62 | 3.82 | 1,582.03 | 4.62 |
| VeryHigh | 1,000 | 847.31 | 1.88 | 1,714.43 | 3.81 | 2,066.11 | 4.59 |

Two findings are central. First, LCOA is nearly invariant to demand scale. Case 1 LCOA ranges from \$1.88 to \$1.95/ton across a fourfold demand variation (250 to 1,000 end-vessels), a variation of only 3.7% (\$0.07/ton). This near-constant marginal cost arises because the MILP scales fleet size proportionally with demand -- doubling demand approximately doubles both total cost and total supply, leaving LCOA unchanged. The slight decline at higher demand (\$1.95 to \$1.88) reflects economies of scale: fixed components (e.g., bunkering CAPEX per shuttle) are spread over more delivered ammonia. Cases 2 and 3 show similar LCOA stability: 2.6% (\$3.81--\$3.91) and 2.4% (\$4.59--\$4.70) variation respectively.

Second, the optimal shuttle size is invariant across demand scenarios. The optimal shuttle remains 1,000 m$^3$ (Case 1), 5,000 m$^3$ (Case 2), and 5,000 m$^3$ (Case 3) across all four scenarios. This invariance confirms that the optimal shuttle specification is determined by the cycle time structure (shore loading time, transit time, pumping time) rather than by demand volume. Because all three cases maintain their optimal shuttle sizes across a fourfold demand range, the specification decision is fully decoupled from the demand forecast.

The practical implication for port planners is that shuttle vessel specifications can be committed early in the planning process without waiting for demand clarity. The timing of fleet additions (not the specifications) is the demand-sensitive decision. This separation of specification-robustness from scheduling-sensitivity reduces planning risk.

---

### 3.9 Discount Rate Sensitivity

The base case assumes zero discounting (Assumption A2), treating all years equally. To validate this assumption, we test three discount rates: $r$ = 0%, 5%, and 8% across all three cases. The sensitivity analysis again fixes the optimal shuttle specification from the base case and re-evaluates NPC under each discount rate. Table 9 summarizes the results.

**Table 9: Discount rate sensitivity -- optimal configurations remain invariant**

| Case | $r$ = 0% NPC | $r$ = 5% NPC | $r$ = 8% NPC | Optimal Shuttle | Optimal Pump |
|------|-------------|-------------|-------------|-----------------|--------------|
| Case 1 | \$447.53M | \$246.30M | \$180.36M | 1,000 m$^3$ | 500 m$^3$/h |
| Case 2 | \$906.80M | \$499.03M | \$365.39M | 5,000 m$^3$ | 500 m$^3$/h |
| Case 3 | \$1,094.12M | \$601.94M | \$440.64M | 5,000 m$^3$ | 500 m$^3$/h |

The key finding is that optimal shuttle specifications are invariant across all discount rates. While NPC decreases by approximately 59.7% from $r$ = 0% to $r$ = 8% (because future costs are discounted more heavily), the relative cost ranking across shuttle sizes remains unchanged. Case 1 selects 1,000 m$^3$, and both Cases 2 and 3 select 5,000 m$^3$ regardless of discounting assumptions.

Fig. 15 presents the NPC and LCOA response to discount rate for all three cases. The LCOA follows the same pattern: Case 1 ranges from \$1.90/ton ($r$ = 0%) to \$0.77/ton ($r$ = 8%), while maintaining the cost advantage over Cases 2 and 3 at every discount rate. The decline in LCOA with increasing discount rate is a mathematical artifact of the LCOA definition (Eq. 26): the numerator (NPC) is discounted, reducing its value, while the denominator (total physical ammonia delivered) is not discounted because it represents physical tonnage rather than a monetary quantity. Consequently, higher discount rates mechanically reduce LCOA without any change in the physical cost of delivering ammonia. LCOA comparisons across discount rates should therefore be interpreted with caution; the metric is most meaningful when compared across supply chain configurations at a fixed discount rate.

The physical fleet requirement (number of shuttles needed to serve demand) is determined by cycle time and demand volume, not by financial discounting. Consequently, fleet expansion timelines are identical across discount rates -- the same number of 1,000 m$^3$ shuttles are added in the same years regardless of $r$, because the physical constraint (Eq. 12) is independent of the discount rate.

These results validate Assumption A2: while the choice of discount rate affects the reported NPC magnitude, it does not affect the infrastructure specification recommendations or the relative ranking of supply chain configurations. Port authorities can use the zero-discount results as a conservative upper bound on NPC while maintaining confidence in the shuttle sizing recommendations.

---

## 4. Discussion

### 4.1 Local Storage vs Remote Supply: Break-Even Analysis

The results in Section 3.1 establish that port-based storage (Case 1) is substantially cheaper than remote supply at the actual distances of Ulsan (59 nm) and Yeosu (86 nm). To determine whether a crossover distance exists at which remote supply becomes competitive, we parameterize the one-way travel distance from 10 to 200 nm.

The primary comparison uses each configuration at its own optimal shuttle size: Case 1 with a 1,000 m$^3$ shuttle (NPC = \$447.53M, independent of remote supply distance) versus the remote supply alternatives with 5,000 m$^3$ shuttles at varying distances. Under this optimal-versus-optimal comparison, Case 2 NPC at its actual distance of 59 nm is \$906.80M, exceeding Case 1 by a factor of 2.03. Case 3 at 86 nm costs \$1,094.12M, exceeding Case 1 by a factor of 2.45. Even at the minimum tested distance of 10 nm, remote supply with 5,000 m$^3$ shuttles costs substantially more than port-based storage with its optimal 1,000 m$^3$ shuttle, and no crossover occurs within the 10--200 nm range. This dominance arises because port-based storage enables a fundamentally smaller shuttle (1,000 vs 5,000 m$^3$), with correspondingly lower per-unit CAPEX and shorter cycle times.

Fig. 12 presents the break-even analysis in a supplementary same-shuttle comparison, where both Case 1 and the remote supply alternative use identical 5,000 m$^3$ shuttles to isolate the effect of travel distance. In this comparison, Case 1 NPC is \$519.14M (the Case 1 cost at 5,000 m$^3$, independent of remote supply distance). For the Ulsan configuration, remote supply NPC increases with distance from \$546.81M at 10 nm to \$1,447.75M at 200 nm. Case 1 is cheaper at every distance, including at 10 nm where the difference is \$27.67M. For the Yeosu configuration, remote supply NPC ranges from \$584.46M at 10 nm to \$1,876.82M at 200 nm, again exceeding Case 1 at every distance. The two remote supply configurations exhibit different cost-distance slopes in Fig. 12 because the Yeosu comparison involves slightly different operational parameters (port entry/exit procedures scaled to the longer voyage), resulting in higher per-nautical-mile cost increments.

The absence of any break-even crossover -- even at distances as short as 10 nm -- is a stronger finding than might be anticipated. It occurs because at 500 m$^3$/h pump rate, the shuttle pumping time ($v_{\text{call}}/Q_p = 5{,}000/500 = 10.0$ h per vessel) dominates the cycle time budget for remote supply cases. Even minimal travel distance cannot offset this pumping time penalty when combined with the shore loading overhead (11.14 h) and port entry/exit procedures. The fixed components of remote supply cycle time (shore loading + port procedures + pumping = 11.14 + 2.0 + 15.0 = 28.14 h for a single vessel) already exceed the entire Case 1 cycle time (13.43 h), before any travel time is added.

This decision rule is transferable to other ports: for ammonia bunkering at 500 m$^3$/h pump rate with 5,000 m$^3$ per-call demand, port-based storage dominates remote supply at all distances. The dominance is driven by the high pumping time at moderate pump rates, which makes the remote supply cycle time inherently longer regardless of travel distance.

---

### 4.2 Robustness of Infrastructure Decisions

The sensitivity analyses in Sections 3.6--3.9 collectively demonstrate the robustness of the optimal specifications across most tested uncertainty dimensions.

Shuttle size specification is robust to fuel price variation from \$300 to \$1,200/ton (Section 3.7), demand variation from 250 to 1,000 end-vessels (Section 3.8), and discount rate variation from 0% to 8% (Section 3.9). The Case 1 optimal (1,000 m$^3$) is unchanged across all these dimensions. The specification does change with pump rate: above 600 m$^3$/h, the optimal shifts from 1,000 to 2,500 m$^3$ (Section 3.6). This pump-rate dependence underscores the importance of the pump sizing decision -- it is the key parameter that determines the optimal shuttle size.

LCOA is remarkably stable: \$1.88--\$1.95/ton across a fourfold demand range (Section 3.8), and \$1.69--\$2.31/ton across a fourfold fuel price range (Section 3.7). The combined uncertainty envelope (demand and fuel price) produces an LCOA range of approximately \$1.50--\$2.80/ton for Case 1 -- primarily driven by fuel price.

Fleet expansion timing is the demand-sensitive component. While the shuttle specification is fixed, the year in which each new shuttle must be procured depends on when cumulative demand crosses the capacity threshold. Under the VeryHigh scenario (1,000 end-vessels), the fleet grows to approximately 101 shuttles (vs 51 under Base), but the same 1,000 m$^3$ vessel specification is procured throughout.

The tornado analysis identifies the CAPEX scaling exponent ($\alpha$) as the dominant uncertainty for Case 1 (87.6% NPC swing, Section 3.7). In practical terms, this means that the accuracy of shipyard cost estimates matters more than fuel price forecasts or demand projections. A 20% error in the scaling exponent would change NPC by \$391.82M, dwarfing the impact of fuel cost uncertainty (\$39.00M) or travel time variation (\$52.37M). Port authorities should invest in detailed shipyard quotations for ammonia shuttle vessels before committing to fleet procurement.

A second risk factor unique to the 1,000 m$^3$ shuttle is the call duration constraint. At 5,000 m$^3$ per call, the 1,000 m$^3$ shuttle requires 5 trips totaling 67.14 h, leaving only 12.86 h of margin below the 80 h maximum. A 20% increase in bunker volume (to 6,000 m$^3$) causes infeasibility. This constraint margin is tighter than for larger shuttles and suggests that if per-call demand may exceed 5,000 m$^3$, a larger shuttle (e.g., 1,500 or 2,500 m$^3$) should be considered as a hedge, accepting a modest NPC penalty (\$521.98M and \$454.38M respectively).

---

### 4.3 Practical Implications for Green Corridor Planning

The results support three actionable recommendations for port authorities planning ammonia bunkering infrastructure for green corridor initiatives.

First, port-based storage with small-shuttle intra-port distribution minimizes 21-year cost for ports with demand profiles similar to Busan. The break-even analysis (Section 4.1) shows no distance at which remote supply becomes cheaper at the 500 m$^3$/h pump rate baseline. Even at 10 nm -- closer than any realistic ammonia source -- port-based storage costs less than remote supply when using the same shuttle size, and the advantage widens substantially when each configuration uses its optimal specification.

Second, shuttle vessel specifications can be committed early in the planning process, provided the bunkering pump rate is finalized first. The optimal shuttle size is invariant to demand uncertainty across a fourfold range (Section 3.8) and to discount rate (Section 3.9). However, it is sensitive to pump rate: 1,000 m$^3$ is optimal at 500 m$^3$/h, while 2,500 m$^3$ is optimal at 600+ m$^3$/h. Port authorities should therefore finalize the bunkering pump specification before committing to shuttle vessel procurement. Once the pump rate is fixed, the shuttle specification follows deterministically.

Third, shipyard costs and bunker volume are the primary risk variables requiring monitoring. The CAPEX scaling exponent accounts for 87.6% of NPC sensitivity (Section 3.7), making shipyard cost accuracy the highest-priority uncertainty. Additionally, the 1,000 m$^3$ shuttle has a tight call duration margin (67.14 h of 80 h maximum), meaning that any increase in per-call bunker volume could force a shuttle size increase. Competitive bidding among shipyards and conservative bunker volume estimates would mitigate these risks.

---

### 4.4 Comparison with Published DES Model

To position the MILP framework within existing operational research on ammonia bunkering, we compare key outputs with the discrete event simulation (DES) model of Yang and Lam [11], the only published quantitative study of ammonia bunkering operations. This comparison serves to validate the deterministic cycle time formulation against a stochastic simulation benchmark and to delineate the complementary analytical scopes of the two approaches. Table 10 summarizes the key methodological differences.

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

The pumping time component -- the time required to transfer ammonia from shuttle to receiving vessel, calculated as $V / Q_p$ -- is consistent across both models, as it is derived from the same physical relationship. At three validation points from Yang and Lam's Table 4 (855, 1,384, and 2,000 tons), the raw gap between our MILP service time estimates and their DES output is 4.6--5.9%. This gap is attributable to operational overhead components that their DES explicitly models through triangular distributions but that our MILP subsumes into the setup time parameter: specifically, mooring procedures (approximately 1.55 h, estimated from Yang and Lam's reported TRIA distribution means for vessel approach and berthing) and documentation and inspection (approximately 0.84 h, similarly derived from their reported administrative time distributions). This difference reflects scope rather than inconsistency: the MILP's purpose is infrastructure sizing, not operational scheduling. Detailed service time comparison data are presented in Appendix B.

A more substantive comparison emerges from flow rate sensitivity analysis. Both models identify bunkering flow rate as the dominant operational parameter: Yang and Lam report a 51.3% impact on service time when flow rate varies by $\pm$50%, while our MILP yields a 37.7% variation over a matched parameter range (see Appendix B). The 13.6 percentage-point gap is structural: the DES uses triangular (TRIA) distributions for service time components, which smooth extreme values through probabilistic averaging, whereas our deterministic formula amplifies the effect of flow rate at the extremes. This difference is expected and informative -- it quantifies the extent to which stochastic modeling attenuates parameter sensitivity relative to deterministic analysis.

Beyond flow rate, our MILP framework enables sensitivity analysis across investment-side parameters (CAPEX scaling exponent, bunker volume, demand trajectory) that the DES framework, focused on operational performance, does not address. The tornado analysis (Section 3.7) reveals that CAPEX scaling exponent dominates NPC sensitivity for Case 1 at 87.6% swing -- a finding inaccessible through operational simulation alone.

These complementary strengths suggest a hybrid DES-MILP approach as a promising research direction: use the MILP to determine optimal fleet size and specifications, then validate operational feasibility through DES simulation incorporating queuing effects and stochastic service times.

---

### 4.5 Limitations

The model incorporates several simplifying assumptions whose impact on the results merits explicit acknowledgment.

The demand trajectory assumes linear growth from 50 to 500 vessels. Actual ammonia adoption may follow an S-curve, with slower initial uptake and potential acceleration post-2040 as regulations tighten. Under S-curve demand, early-year fleet overcapacity would persist longer, while late-period demand surges could outpace fleet additions if procurement lead times exceed 2--3 years.

The fuel price of \$600/ton is held constant over 21 years. Green ammonia production costs are projected to decline from \$700--\$1,400/ton (2025) to \$310--\$660/ton (2030--2040) as electrolyzer costs fall [31]. A declining price trajectory would reduce Cases 2 and 3 vOPEX over time, potentially narrowing the Case 1 cost gap in later years.

The zero discount rate treats a dollar spent in 2030 equally to a dollar spent in 2050. Section 3.9 shows that while NPC decreases by approximately 60% at $r$ = 8%, optimal specifications are invariant, confirming that this assumption affects cost magnitudes but not infrastructure recommendations.

The SFOC map assigns constant values per size class (Table 3). Real-world SFOC varies with engine load, typically increasing by 10--15% at partial load versus the design point. For Cases 2 and 3, where shuttles may operate below design speed during port maneuvering, actual fuel consumption could exceed modeled values.

The model assumes vessels arrive uniformly throughout the year. In practice, seasonal and weekly demand peaks create queuing effects that could increase effective cycle time during peak periods. The daily peak factor ($F_{\text{peak}} = 1.5$) provides partial design margin but does not replace a queuing model.

All vessels are assumed to require 5,000 m$^3$ per call. In practice, vessel sizes range from small feeders (~1,000 m$^3$) to large container ships (~8,000 m$^3$). Heterogeneous bunker volumes would create an order-sizing problem, with potentially larger LCOA impact for the 1,000 m$^3$ shuttle, which is near the call duration constraint boundary and cannot accommodate larger per-call demands.

Ammonia is acutely toxic and requires safety exclusion zones, gas detection systems, and emergency response capabilities during bunkering [18, 19, 20]. These safety infrastructure costs are not included in NPC, and could increase bunkering infrastructure cost by an estimated 5--15%, with potentially larger relative impact on Case 1 where bunkering occurs within the congested port area.

The planning horizon coincides with the annualization period (21 years). Assets purchased late in the horizon (e.g., after 2045) are annualized over 21 years despite providing only 6 years of in-horizon service, which may overestimate their cost contribution. This systematically penalizes late-period shuttle additions and could influence the modeled timing of fleet expansion in the final years of the planning horizon.

Two directions for extending this work warrant particular attention. First, a two-stage stochastic MILP with joint demand and price uncertainty would test whether the deterministic specification robustness observed in Sections 3.8--3.9 persists under correlated stochastic scenarios. Second, coupling the MILP with a discrete event simulation of port queuing dynamics -- building on Yang and Lam [11] -- would incorporate congestion effects into fleet sizing decisions, addressing the operational complexity that the deterministic formulation necessarily omits.

---

## 5. Conclusions

This study developed a mixed-integer linear programming model for optimizing ammonia bunkering infrastructure at Busan Port over a 21-year planning horizon (2030--2050). The model systematically evaluates all feasible shuttle-pump combinations through parametric enumeration and solves a fleet-sizing MILP for each configuration across three supply chain cases: port-based storage (Case 1), remote supply from Ulsan (Case 2, 59 nm), and remote supply from Yeosu (Case 3, 86 nm).

Four principal findings emerge from the analysis.

First, optimal shuttle specifications are determined by the interaction between pump rate, CAPEX scaling, and cycle time, and differ across supply chain configurations. At 500 m$^3$/h pump rate, Case 1 selects a 1,000 m$^3$ shuttle (NPC \$447.53M, LCOA \$1.90/ton), while Cases 2 and 3 both require 5,000 m$^3$ shuttles at higher cost (\$906.80M and \$1,094.12M respectively). The cost differential arises from the fundamentally shorter cycle time achievable with intra-port operations (13.43 h vs 36.00--39.60 h).

Second, port-based storage dominates remote supply at all tested distances (10--200 nm). The fixed-time components of the remote supply cycle -- shore loading, pumping, and port procedures -- exceed the entire Case 1 cycle time before any travel time is added, eliminating the possibility of a break-even crossover at moderate pump rates.

Third, the optimal shuttle specification is robust to demand uncertainty (invariant across a fourfold range), fuel price variation (\$300--\$1,200/ton), and discount rate (0--8%). This robustness enables early commitment to vessel procurement. However, the specification is sensitive to pump rate, with the optimum shifting from 1,000 to 2,500 m$^3$ above 600 m$^3$/h, establishing the pump specification as the pivotal upstream decision.

Fourth, the dominant cost driver differs by configuration. CAPEX scaling governs port-based storage costs (87.6% NPC swing), while bunker volume governs remote supply costs (107.5% for Case 2). For the 1,000 m$^3$ shuttle, the tight call duration margin (67.14 h of 80 h maximum) creates an infeasibility boundary if per-call demand increases, warranting consideration of a 1,500 or 2,500 m$^3$ shuttle as an operational hedge.

The parametric evaluation framework is transferable to other ports by substituting local distances, candidate shuttle sizes, pump flow rates, and demand projections. The principal methodological contribution is demonstrating that ammonia bunkering infrastructure specifications can be committed independently of demand forecasts -- an operationally useful finding for the early stages of green corridor planning.
