# Research Gap Statement

**Paper type:** Deterministic case
**Phase:** 1 of 10
**Status:** Complete

---

## Gap 1: No Systematic Evaluation of Shuttle Vessel Size, Fleet Count, and Pump Capacity Combinations for Ammonia Bunkering

### What is currently known

The maritime operations research community has developed mature MILP formulations for fleet scheduling, routing, and inventory management in conventional shipping [8, 9, 23]. These models optimize vessel allocation across fixed trade routes with known cargo volumes. Stochastic extensions handle demand uncertainty through multi-stage programming [14, 25] and charter flexibility [24, 26]. Separately, techno-economic assessments have evaluated ammonia as a marine fuel candidate, establishing baseline cost parameters (fuel price ranges of $400--$1,200/ton) and identifying bunkering infrastructure as the primary supply-side constraint [1, 4, 10]. Recent work on LNG bunkering has demonstrated that MILP-based fleet sizing can determine optimal bunker vessel capacities for established alternative fuels [12, 40, 42], and ILP has been applied to bunkering method selection at ports [27]. For ammonia specifically, Yang and Lam [11] developed a discrete event simulation model for bunkering supply chains, Wang et al. [38] formulated an optimization model for ammonia bunkering network configurations, and a growing safety literature [18, 19, 20, 35] has characterized bunkering risks through Bayesian networks and system-theoretic analysis. Khan et al. [36] provide the most comprehensive review of ammonia bunkering challenges to date.

### What is NOT known (the gap)

No existing study systematically evaluates all feasible combinations of the three coupled variables that define an ammonia bunkering system: (1) shuttle vessel capacity (m3), (2) fleet size over time (vessels/year), and (3) bunkering pump flow rate (m3/h). An expanded review of 42 papers (Section 2) confirms that current approaches either fix two of these variables and optimize the third, or treat them independently. Wang et al. [38] optimize ammonia bunkering network configurations but in a single-period setting without pump rate as a decision variable. Pratama et al. [40] demonstrate multi-period fleet sizing for LNG bunkering but without ammonia-specific transfer dynamics. Even the most advanced fleet sizing models [24, 25, 26] treat cargo transfer as instantaneous, ignoring flow-rate-dependent cycle time. The coupling is non-trivial: shuttle size determines cycle time through pumping duration (shuttle_size / pump_rate for port-based storage vs. bunker_volume / pump_rate for ship-to-ship transfer), cycle time determines maximum annual trips, and maximum trips determine fleet size. Ignoring this coupling leads to suboptimal infrastructure investment -- for example, a 5,000 m3 shuttle with a 400 m3/h pump requires 12.5 hours of pumping alone, which may make the configuration infeasible under annual operating hour constraints (8,000 h/year), regardless of its CAPEX advantage.

### Why it matters (practical consequence)

Port authorities and ammonia fuel suppliers planning green corridor infrastructure (e.g., Busan Port for a Korea--Australia corridor) must decide *simultaneously* on shuttle procurement specifications, pump equipment sizing, and long-term fleet expansion schedules. An error in any one dimension propagates: oversized shuttles paired with undersized pumps waste capital through low utilization; undersized fleets paired with high-capacity pumps create bottlenecks during demand peaks. Our Phase 0 data shows this coupling quantitatively -- the optimal solution for Case 1 (Busan port-based storage) is a 2,500 m3 shuttle with 1,000 m3/h pump at NPC $290.81M, while naively selecting the largest shuttle (5,000 m3) with the same pump increases NPC due to CAPEX scaling effects (exponent = 0.75), even though fewer vessels are needed.

### How our study fills it

We formulate a MILP model that systematically evaluates all feasible shuttle-pump combinations and optimizes fleet deployment for each configuration over a 21-year planning horizon (2030--2050). The model minimizes 20-year Net Present Cost (NPC) subject to demand satisfaction, annual operating hour limits, and tank capacity constraints. The shuttle size and pump rate define cycle time through explicit physical relationships; the model then determines fleet additions per year to match linearly growing demand (50 to 500 vessels). This produces a complete enumeration of all feasible shuttle-pump combinations with their associated NPC, enabling infrastructure planners to evaluate trade-offs directly.

---

## Gap 2: No Quantitative Comparison Between Port-Based Storage and Remote Supply Configurations for Ammonia Bunkering

### What is currently known

Green corridor planning documents [6] and techno-economic reviews [5, 7] acknowledge that ammonia can be supplied to bunkering ports either through on-site storage (receiving ammonia by pipeline or large carrier and distributing via small shuttles within the port) or through dedicated shuttle operations from nearby ammonia production facilities (e.g., petrochemical complexes). Lloyd's Register and UMAS [7] provide macro-level cost estimates for both approaches but at a resolution too coarse for port-specific investment decisions. Trivyza et al. [21] designed ammonia-based green corridor networks identifying bunkering ports but without comparing supply configurations at individual ports. The LNG bunkering literature has explored truck-to-ship vs. ship-to-ship vs. terminal-to-ship comparisons [27], but these address a fuel with fundamentally different storage requirements (cryogenic at -162C vs. ammonia at -33C or pressurized).

### What is NOT known (the gap)

No study provides a quantitative, cost-optimized comparison of these two supply configurations for ammonia under identical demand assumptions, nor has a break-even distance been identified. Dahlke-Wallat et al. [39] evaluate ammonia bunkering infrastructure concepts but do not compare port-based vs. remote supply under identical demand. The key structural difference is that port-based storage (our Case 1) requires smaller shuttles making multiple trips per bunkering call (because shuttle_size < bunker_volume), while remote supply (our Case 2) uses larger shuttles that can serve multiple vessels per trip (because shuttle_size >> bunker_volume). This structural difference produces fundamentally different cost profiles: Case 1 is CAPEX-light but operationally intensive; Case 2 requires high CAPEX for large shuttles but achieves economies of scale on variable costs. Furthermore, no study has quantified the *break-even distance* at which port-based storage becomes cheaper than remote supply -- the threshold parameter that port planners choosing between building local ammonia storage infrastructure and relying on nearby production hubs.

### Why it matters (practical consequence)

Busan Port faces exactly this decision. Ammonia could be sourced from Yeosu (86 nm away, major petrochemical complex) or Ulsan (25 nm away, refinery cluster), or a dedicated storage terminal could be built at Busan Port itself. Our optimization results demonstrate that the choice is not obvious: Case 1 (Busan storage) achieves NPC $290.81M with LCOA $1.23/ton; Case 2-1 (Yeosu remote supply) requires NPC $879.88M with LCOA $3.73/ton; Case 2-2 (Ulsan remote supply) requires NPC $700.68M with LCOA $2.97/ton. However, these results are distance-dependent. Our break-even analysis shows that Yeosu-type remote supply becomes cheaper than port storage only below approximately 59.6 nm -- meaning if a production facility were closer to Busan than Yeosu currently is, the preferred strategy would reverse. For Ulsan (25 nm), no break-even crossover exists within the 10--200 nm range analyzed, suggesting Ulsan could be competitive under modified assumptions.

### How our study fills it

We apply the same MILP framework to three supply chain configurations under identical demand trajectories (50 to 500 vessels over 21 years), fuel prices ($600/ton baseline), and operating constraints (8,000 h/year). By holding all parameters constant except the supply chain topology, we isolate the effect of infrastructure configuration on total system cost. We further conduct a parametric break-even distance analysis (10--200 nm, 20 points) that identifies the crossover distance at which each remote supply case matches the port-based storage cost. This gives port planners a decision rule: for a given distance to the nearest ammonia source, which infrastructure configuration minimizes 20-year cost.

---

## Gap 3: No Multi-Period Fleet Expansion Model Synchronized with Ammonia Demand Growth

### What is currently known

Maritime fleet sizing studies [8, 9] typically solve static problems: given a fixed annual demand, determine the optimal fleet. When demand growth is considered, it is increasingly handled through multi-period formulations [14, 25, 26] or stochastic programming [24], but these advances have not been applied to ammonia bunkering infrastructure. Recent ammonia fuel adoption studies [1, 3, 5, 22] project demand growth curves and identify adoption barriers but do not connect these projections to infrastructure investment timing. The IMO's 2023 revised strategy [30] and IRENA's cost projections [31] provide the policy and economic context for demand trajectories, yet the demand scenario approach in existing literature treats 2030 and 2050 as separate snapshots rather than as endpoints of a continuous investment trajectory.

### What is NOT known (the gap)

No existing model optimizes the *timing* of fleet additions for ammonia bunkering infrastructure, where the decision in year t constrains available capacity in years t+1 through T. Pratama et al. [40] and Jokinen et al. [42] demonstrate multi-period MILP for LNG bunkering, but neither addresses ammonia. The temporal dimension matters because ammonia-fueled vessel adoption follows an S-curve (or in our model, a linear ramp from 50 to 500 vessels), creating a period of underutilization in early years (few ships to bunker) and potential capacity shortfall in later years (many ships competing for shuttle time). Static fleet sizing cannot capture this dynamic: it either over-invests early (based on 2050 demand) or under-invests (based on 2030 demand). Furthermore, no study has examined how demand uncertainty (growth rate, terminal fleet size) affects infrastructure sizing -- specifically, whether the optimal shuttle size *changes* under different demand scenarios or remains robust.

### Why it matters (practical consequence)

Infrastructure procurement lead times for specialized ammonia shuttle vessels are 2--4 years. A port authority that determines in 2030 that it needs a fleet of 2,500 m3 shuttles cannot simply add vessels on-demand as ammonia adoption accelerates. Our per-year results show that fleet expansion is discontinuous: Case 1 adds shuttles in specific years when demand growth crosses capacity thresholds. If the wrong shuttle size is selected, the expansion schedule changes entirely -- a 5,000 m3 shuttle requires fewer additions but each addition represents a larger capital outlay. Our demand scenario analysis demonstrates quantitative robustness: across a 4x demand range (250 to 1,000 end-vessels), LCOA varies only from $1.21 to $1.28/ton, and the optimal shuttle size remains 2,500 m3 for Case 1. This stability is a non-obvious result that static analysis cannot reveal.

### How our study fills it

Our MILP formulation includes year-indexed decision variables for shuttle additions (New_Shuttles_t) with cumulative fleet tracking (Total_Shuttles_t = sum of New_Shuttles from 2030 to t). The demand constraint ensures Supply_t >= Demand_t for every year t in [2030, 2050]. The model determines both the optimal fleet expansion schedule and the infrastructure specifications (shuttle size, pump rate) that minimize total 20-year cost across the entire trajectory. We further validate robustness through four demand scenarios (Low: 250, Base: 500, High: 750, VeryHigh: 1,000 end-vessels) and a six-parameter tornado sensitivity analysis, quantifying the relative impact of CAPEX scaling, bunker volume, operating hours, travel time, fuel price, and SFOC on total cost.

---

## Summary: Three Gaps and Their Connections

| Gap | Core Question | Decision Served | Key Evidence |
|-----|--------------|-----------------|--------------|
| **Gap 1** | What shuttle size + pump rate + fleet count minimizes 20-year cost? | Procurement specification | NPC surface across shuttle-pump grid (D1, D12) |
| **Gap 2** | When is port-based storage cheaper than remote supply? | Build-vs-source decision | Break-even distance analysis (Fig9), 3-case LCOA comparison (D9) |
| **Gap 3** | How should fleet expand as demand grows? | Investment timing | Per-year fleet additions (D2), demand scenario stability (Fig10) |

**Inter-gap logic:** Gap 1 provides the optimization framework. Gap 2 applies it to compare supply chain configurations. Gap 3 extends the temporal dimension and tests robustness. Together, they address the complete decision space facing a port authority planning ammonia bunkering infrastructure for a green corridor.

---

## Quality Gate Checklist

- [x] At least 2 specific gaps identified (3 gaps defined)
- [x] No gap uses vague language ("important", "significant", "novel") -- all gaps framed with specific decision problems and quantitative evidence
- [x] Each gap references what IS known (from expanded bibliography: [1]-[42])
- [x] Each gap is connected to a practical decision problem (procurement specification, build-vs-source, investment timing)
- [x] No gap is merely "this topic has not been studied enough" -- each specifies what is missing and why it matters operationally
- [x] Gaps validated against expanded literature (42 papers) -- all three remain genuine gaps
