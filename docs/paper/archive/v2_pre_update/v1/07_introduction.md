# 1. Introduction

**Paper type:** Deterministic case
**Phase:** 8 of 10
**Status:** Complete

---

The International Maritime Organization (IMO) has adopted a revised GHG strategy targeting at least 30% emission reduction by 2030, 80% by 2040, and net-zero by or around 2050 relative to 2008 levels [5, 30]. Achieving these targets requires a transition from conventional marine fuels to zero-carbon alternatives. Among the candidates, ammonia (NH$_3$) has emerged as a leading option due to its zero-carbon combustion, existing global production infrastructure (~180 million tons/year), and compatibility with established bulk liquid transport methods [1, 2]. Green ammonia production costs are projected to decline from $720--$1,400/ton (2022) to $310--$610/ton by 2050 [31], making it increasingly competitive as a marine fuel. As of December 2025, 144 ammonia-fueled vessels and 302 ammonia-ready vessels have been ordered, signaling that the demand side of the ammonia fuel transition is materializing. The supply side -- specifically, the port-level infrastructure required to deliver ammonia from production facilities to vessel fuel tanks -- remains unresolved.

Green shipping corridor initiatives aim to bridge this gap by establishing end-to-end infrastructure for zero-emission vessel operations along specific trade routes. The Korea--United States green corridor agreement (formalized April 2025) targets ammonia-fueled container ship operations between Busan and Seattle-Tacoma by 2027, with the Korean government investing approximately $10 billion in Busan mega-port infrastructure including alternative fuel bunkering facilities [6]. Similar corridors are planned between Korea and Australia. These initiatives specify the fuel (ammonia) and the endpoints (ports) but leave a fundamental operational question unanswered: what bunkering infrastructure -- shuttle vessels, pumps, and storage facilities -- is required, at what scale, and when should it be deployed?

Existing literature provides partial answers to this question from separate directions. Techno-economic assessments have characterized ammonia fuel properties and estimated per-vessel cost premiums [1, 3, 4, 10], while a growing body of work addresses ammonia bunkering safety through Bayesian networks [18] and system-theoretic analysis [20], and Khan et al. [36] provide a comprehensive review of ammonia bunkering challenges. Maritime operations research has developed mature MILP formulations for fleet scheduling, routing, and inventory management [8, 9, 23], with stochastic extensions for fleet composition under demand uncertainty [14, 24, 25, 26]. For LNG bunkering, multi-period MILP models have been applied to optimize bunker vessel fleet size and distribution networks [12, 40, 42], and integer programming has been used to select optimal bunkering methods at individual ports [27]. For ammonia specifically, Yang and Lam [11] developed a discrete event simulation model for bunkering supply chains, finding that flow rate has up to 51.3% impact on service time and vessel count has up to 15.2% impact on annual cost. Wang et al. [38] formulated an optimization model for ammonia bunkering network configurations -- the first mathematical programming approach applied to ammonia bunkering -- but in a single-period setting without pump rate as a decision variable. Trivyza et al. [21] designed ammonia-based green corridor networks, and Fullonton et al. [22] surveyed adoption barriers across the fuel supply chain. However, a systematic literature review of 43 papers (Section 2) reveals three gaps that no existing study addresses:

**Gap 1:** No study jointly optimizes the three coupled decision variables that define an ammonia bunkering system -- shuttle vessel capacity, bunkering pump flow rate, and fleet size over time. The coupling is non-trivial: shuttle size determines pumping time ($V_s / Q_p$), pumping time determines cycle time, and cycle time determines fleet capacity.

**Gap 2:** No quantitative comparison exists between port-based ammonia storage (small shuttles, multiple trips within port) and remote supply (large shuttles, long-haul from production facilities) under identical demand assumptions, nor has a break-even distance been identified.

**Gap 3:** No model optimizes the timing of ammonia bunkering fleet expansion synchronized with demand growth trajectories, or tests whether optimal infrastructure specifications are robust to demand uncertainty.

This paper addresses all three gaps through a MILP model that jointly optimizes shuttle vessel sizing (500--50,000 m$^3$), pump capacity (400--2,000 m$^3$/h), and year-by-year fleet expansion over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port: port-based storage (Case 1), remote supply from Yeosu at 86 nm (Case 2-1), and remote supply from Ulsan at 59 nm (Case 2-2). Our four contributions are:

(C1) We identify non-obvious optimal infrastructure specifications through joint shuttle-pump-fleet co-optimization: Case 1 selects a 2,500 m$^3$ shuttle at NPC $290.81M ($1.23/ton LCOA), while Cases 2-1 and 2-2 select 10,000 m$^3$ and 5,000 m$^3$ respectively, at 2.4--3.0$\times$ higher cost.

(C2) We establish a break-even distance decision rule: remote supply becomes cheaper than port storage below approximately 59.6 nm (at 10,000 m$^3$ shuttle scale), providing port planners a transferable threshold for the build-vs-source decision.

(C3) We demonstrate that optimal shuttle specifications are invariant to a 4$\times$ demand range (250 to 1,000 end-vessels), with LCOA varying only 5.7% ($1.21--$1.28/ton for Case 1), enabling early commitment to vessel procurement.

(C4) We identify a differentiated cost driver hierarchy: CAPEX scaling dominates port-based storage sensitivity (62% NPC swing), while bunker volume dominates remote supply sensitivity, informing risk management strategies for each configuration.

The remainder of the paper is organized as follows. Section 2 reviews related literature on ammonia bunkering, maritime fleet optimization, and green corridor planning. Section 3 presents the MILP formulation, cycle time model, and cost structure. Section 4 reports optimization results, temporal dynamics, cost decomposition, and six sensitivity analyses. Section 5 discusses the break-even distance rule, result robustness, practical implications, and limitations. Section 6 concludes.

---

## Quality Gate Checklist

- [x] Opening paragraph engages without being generic (IMO targets + specific vessel order numbers + supply-side gap)
- [x] Gap statement is specific and supported by citations ([1]-[12])
- [x] Contributions match Phase 3 exactly (C1--C4, identical framing)
- [x] At least one quantitative result previewed ($290.81M, $1.23/ton, 59.6 nm, 5.7% LCO range)
- [x] Paper structure paragraph at the end
- [x] 20+ citations in introduction ([1]-[6], [8]-[12], [14], [18], [20]-[27], [30], [31], [36], [38], [40], [42])
- [x] No promises not supported by the paper body
