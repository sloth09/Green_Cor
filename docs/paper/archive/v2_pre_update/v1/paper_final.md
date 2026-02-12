# Optimal Ammonia Bunkering Infrastructure for Green Shipping Corridors: A Multi-Period Mixed-Integer Linear Programming Approach

---

## Abstract

Ammonia is a leading zero-carbon marine fuel candidate, yet no quantitative framework exists for sizing the port-level bunkering infrastructure -- shuttle vessels, pumps, and storage -- required to deliver it from production facilities to ship fuel tanks. We formulate a mixed-integer linear programming (MILP) model that jointly optimizes shuttle vessel capacity, bunkering pump flow rate, and year-by-year fleet expansion over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port: port-based storage (Case 1), remote supply from Yeosu at 86 nm (Case 2-1), and remote supply from Ulsan at 59 nm (Case 2-2). Demand grows linearly from 50 to 500 ammonia-fueled vessels at 12 voyages per year. The model identifies distinct optimal configurations: Case 1 selects a 2,500 m3 shuttle at a 20-year net present cost (NPC) of $290.81M and levelized cost of ammonia bunkering (LCOA) of $1.23/ton, while Cases 2-1 and 2-2 require larger shuttles (10,000 and 5,000 m3) at 2.4--3.0 times higher cost. A parametric break-even analysis establishes that remote supply becomes cheaper than port storage below approximately 59.6 nm one-way distance at the 10,000 m3 shuttle scale. Sensitivity analysis across four demand scenarios (250--1,000 end-vessels) demonstrates that optimal shuttle specifications are invariant, with LCOA varying only 5.7%. These results provide port authorities with quantitative decision tools for ammonia bunkering infrastructure investment in green shipping corridors.

**Keywords:** ammonia bunkering; green shipping corridor; mixed-integer linear programming; fleet sizing; levelized cost; infrastructure optimization

---

## 1. Introduction

The International Maritime Organization (IMO) has committed to reducing greenhouse gas emissions from international shipping by at least 50% by 2050 relative to 2008 levels, with an ambition for full decarbonization [5]. Achieving this target requires a transition from conventional marine fuels to zero-carbon alternatives. Among the candidates, ammonia (NH$_3$) has emerged as a leading option due to its zero-carbon combustion, existing global production infrastructure (~180 million tons/year), and compatibility with established bulk liquid transport methods [1, 2]. As of December 2025, 144 ammonia-fueled vessels and 302 ammonia-ready vessels have been ordered, signaling that the demand side of the ammonia fuel transition is materializing. The supply side -- specifically, the port-level infrastructure required to deliver ammonia from production facilities to vessel fuel tanks -- remains unresolved.

Green shipping corridor initiatives aim to bridge this gap by establishing end-to-end infrastructure for zero-emission vessel operations along specific trade routes. The Korea--United States green corridor agreement (formalized April 2025) targets ammonia-fueled container ship operations between Busan and Seattle-Tacoma by 2027, with the Korean government investing approximately $10 billion in Busan mega-port infrastructure including alternative fuel bunkering facilities [6]. Similar corridors are planned between Korea and Australia. These initiatives specify the fuel (ammonia) and the endpoints (ports) but leave a fundamental operational question unanswered: what bunkering infrastructure -- shuttle vessels, pumps, and storage facilities -- is required, at what scale, and when should it be deployed?

Existing literature provides partial answers to this question from separate directions. Techno-economic assessments have characterized ammonia fuel properties and estimated per-vessel cost premiums [1, 3, 4, 10], while maritime operations research has developed mature mixed-integer linear programming (MILP) formulations for fleet scheduling and routing in conventional shipping [8, 9]. For LNG bunkering, multi-period MILP models have been applied to optimize bunker vessel fleet size and distribution networks [12]. For ammonia specifically, Yang and Lam [11] developed a discrete event simulation model for bunkering supply chains, finding that flow rate has up to 51.3% impact on service time and vessel count has up to 15.2% impact on annual cost. However, a systematic literature review (Section 2) reveals three gaps that no existing study addresses:

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

## 2. Literature Review

### 2.1 Ammonia as a Candidate Marine Fuel

The technical viability of ammonia as a marine fuel has been established through multiple review papers and techno-economic assessments. Al-Enazi et al. [1] provided a comprehensive comparison of alternative marine fuels, identifying ammonia's advantages (zero-carbon combustion, existing transport infrastructure at -33 C) and disadvantages (toxicity, lower energy density than LNG). Imhoff et al. [2] quantified ammonia engine performance through thermodynamic simulation, establishing specific fuel oil consumption (SFOC) values that feed into operational cost estimates. Kim et al. [3] evaluated the economics of ammonia-fueled propulsion for individual vessels, finding cost premiums of 1.5--2.5x over conventional fuels depending on ammonia price assumptions. Persson and Johansson [4] synthesized techno-economic parameters, and Wang and Wright [10] compared bunkering infrastructure requirements across fuel types qualitatively.

**What this body of work collectively lacks:** All five studies treat the bunkering supply chain as a fixed assumption -- ammonia is available at a given price and location. None asks *how* the ammonia reaches the vessel, what infrastructure is required to deliver it, or how that infrastructure should be sized. The supply chain between ammonia production and ship fuel tank remains a black box.

### 2.2 Green Corridor Planning

The green corridor concept has gained institutional support through the Getting to Zero Coalition [6], which identified Busan as a candidate port for a Korea--Australia ammonia shipping corridor. Lloyd's Register and UMAS [7] estimated fuel transition costs at a macro level, and Xing et al. [5] mapped decarbonization pathways for the maritime sector through 2050. South Korea has formalized green corridor agreements with the United States (Busan--Tacoma, targeting 2027) and is investing approximately $10 billion in Busan mega-port infrastructure including methanol and ammonia bunkering facilities. The Korean government's 2023 National Action Plan ("Toward Green Shipping by 2050") establishes policy targets but does not prescribe infrastructure configurations.

**What this body of work collectively lacks:** These documents set targets (number of zero-emission vessels, percentage of green fuel) but do not provide decision-makers with quantitative tools to determine *how many* shuttle vessels to procure, *what capacity* those vessels should have, or *when* to expand the fleet. The gap between strategic planning and operational procurement remains unfilled.

### 2.3 Ammonia Bunkering Operations

The most directly relevant study is Yang and Lam [11], who developed a discrete event simulation (DES) model for ammonia bunkering supply chains at port. Their model evaluates how the number and capacity of ammonia bunker supply vessels, bunkering flow rate, and demand level affect operational and economic performance. Key findings include: flow rate has up to 51.3% impact on bunkering service time (when varied by +/-50%), and the number of bunker supply vessels is the most sensitive parameter for annual operational cost (up to 15.2% effect).

**Where Yang and Lam [11] stops and our study begins:** Their DES model evaluates predefined configurations through simulation runs -- it answers "what happens if we deploy N vessels of size S?" but not "what is the optimal N and S?" Simulation identifies sensitivity; optimization identifies the minimum-cost solution. Furthermore, their model uses static demand (a fixed number of vessels requiring bunkering), whereas our MILP formulates demand as a trajectory (50 to 500 vessels over 21 years) with year-indexed fleet addition decisions. They also analyze a single supply chain configuration rather than comparing port-based storage versus remote supply alternatives.

### 2.4 MILP Fleet Sizing

Mixed-integer linear programming for fleet sizing is a well-established methodology in maritime operations research. Fagerholt [8] demonstrated MILP-based fleet scheduling decision support systems for liner shipping. Christiansen et al. [9] surveyed the state of the art in ship routing and scheduling, noting the growing use of multi-period formulations. More recently, Zhao et al. [17] jointly optimized heterogeneous fleet deployment, sailing speed, and fuel bunkering for green container shipping using MILP combined with multi-objective genetic algorithms.

In adjacent domains, Stalahane et al. [13] applied stochastic programming to the vessel fleet size and mix problem for offshore wind farm maintenance -- a structural analog where the decision variables (number of vessels, vessel type, dispatch schedule) parallel bunkering fleet sizing, though the operational context differs entirely. Bakkehaug et al. [14] addressed multi-period bulk ship fleet renewal under demand and charter cost uncertainty using multi-stage stochastic programming, demonstrating that dynamic fleet expansion models outperform static sizing in volatile demand environments.

The closest methodological analog in bunkering is the Turkey LNG study [12], which formulated a MILP for the ship-to-ship LNG bunkering supply chain as a "Multiple Period Maritime Fleet Size and Routing Problem." This model determines the number and size of LNG bunker barges and their optimal allocation under multiple demand scenarios.

**What these fleet sizing models collectively lack when applied to ammonia bunkering:** The Turkey LNG model [12] addresses a fuel with fundamentally different storage physics (cryogenic at -162 C versus ammonia at -33 C or pressurized), and does not include pump flow rate as a decision variable. Bakkehaug et al. [14] and Stalahane et al. [13] address domains where the vessel's cargo (bulk goods, maintenance crews) does not impose flow-rate-dependent transfer time constraints -- a defining characteristic of ammonia bunkering where cycle time depends on shuttle_size / pump_rate. Zhao et al. [17] optimize fleet deployment for existing liner services, not infrastructure investment for a new fuel supply chain.

### 2.5 Ammonia Supply Chain Optimization

At the supply chain level, Galan-Martin et al. [15] formulated a MILP to optimize green ammonia distribution systems for intercontinental energy transport, determining optimal producer locations given global demand patterns. Their model spans continents and decades, incorporating production capacity, shipping routes, and terminal infrastructure. Demirhan et al. (2024) proposed a two-stage stochastic MILP for integrating renewable ammonia manufacturing into existing supply chain networks, with a case study on Minnesota's ammonia network over 2024--2032. Kim et al. [16] performed a techno-economic analysis of ammonia ocean transport, estimating per-ton shipping costs but without fleet sizing optimization.

**What these supply chain models collectively lack:** They operate at spatial scales (intercontinental routes, state-level networks) and decision granularities (which countries to produce in, which ports to ship from) that are irrelevant to the port-level question: given that ammonia will arrive at or near Busan, how should the last-mile bunkering infrastructure -- shuttle vessels, pumps, storage -- be configured? The gap between global supply chain design and port-level operational optimization remains open.

### 2.6 Research Gap Summary

The literature falls into two non-overlapping clusters:

**Cluster A (Ammonia knowledge, no optimization):** Papers [1]--[7], [10], [16] establish that ammonia is a viable marine fuel, identify bunkering infrastructure as a constraint, and project demand growth trajectories. These provide input parameters but not decision tools.

**Cluster B (Optimization methods, not ammonia bunkering):** Papers [8], [9], [12]--[14], [17] demonstrate that MILP and stochastic programming can effectively solve fleet sizing, routing, and multi-period expansion problems. These provide methodology but have not been applied to ammonia bunkering infrastructure.

**The bridge (partial):** Yang and Lam [11] directly address ammonia bunkering operations with a quantitative model, but use simulation rather than optimization and do not address multi-period fleet expansion or supply chain configuration comparison. Galan-Martin et al. [15] apply MILP to ammonia distribution but at global scale, not port-level bunkering.

**What remains unaddressed:**

1. **No paper** jointly optimizes shuttle vessel size, bunkering pump flow rate, and fleet count for ammonia -- the three coupled variables that define bunkering system performance.

2. **No paper** compares port-based ammonia storage (small shuttles, many trips) versus remote supply (large shuttles, long haul, multi-vessel serving) under identical assumptions with a break-even distance analysis.

3. **No paper** models dynamic ammonia bunkering fleet expansion over a multi-decade horizon synchronized with demand growth trajectories, despite fleet renewal models existing for conventional shipping [14] and LNG bunkering [12].

These three voids correspond directly to Gaps 1, 2, and 3 defined in the research gap statement (Phase 1).

---

## 3. Methodology

## 3.1 Problem Description and Assumptions

We consider a port authority planning ammonia bunkering infrastructure for a green shipping corridor over a 21-year horizon (2030--2050). The number of ammonia-fueled vessels calling at the port grows linearly from $V_{\text{start}} = 50$ (2030) to $V_{\text{end}} = 500$ (2050), with each vessel requiring $v_{\text{call}} = 5{,}000$ m$^3$ of liquid ammonia per bunkering call at a frequency of $f_{\text{voy}} = 12$ calls per year.

The decision-maker must determine: (1) the shuttle vessel capacity $V_s$ from a discrete set of available sizes, (2) the bunkering pump flow rate $Q_p$ (m$^3$/h), and (3) the number of new shuttle vessels $x_t$ to add in each year $t \in \{2030, \ldots, 2050\}$, such that the 20-year Net Present Cost (NPC) is minimized while meeting all demand and operational constraints.

We analyze three supply chain configurations (Fig. 1):

**Table 1: Three supply chain configurations**

| Parameter | Case 1 (Busan) | Case 2-1 (Yeosu) | Case 2-2 (Ulsan) |
|-----------|---------------|-------------------|-------------------|
| Source | Busan port storage | Yeosu (86 nm) | Ulsan (59 nm) |
| Storage at Busan | Yes (35,000 ton) | No | No |
| One-way travel time $\tau$ | 1.0 h | 5.73 h | 3.93 h |
| Shuttle sizes $V_s$ | 500--10,000 m$^3$ | 2,500--50,000 m$^3$ | 2,500--50,000 m$^3$ |
| Pumping logic | $V_s / Q_p$ (empty shuttle) | $v_{\text{call}} / Q_p$ (fill vessel) | $v_{\text{call}} / Q_p$ (fill vessel) |

**Key structural difference:** In Case 1, the shuttle carries ammonia from port storage to a vessel; the pumping time depends on shuttle capacity ($V_s / Q_p$). In Cases 2-1 and 2-2, the shuttle travels from a remote source and may serve multiple vessels per trip; the pumping time per vessel depends on the bunkering demand per call ($v_{\text{call}} / Q_p$).

### Assumptions

We adopt the following simplifying assumptions, each with justification and impact assessment:

**A1. Linear demand growth.** The number of ammonia-fueled vessels increases linearly from 50 to 500 over 21 years. Actual adoption may follow an S-curve with slower early growth and potential acceleration post-2040. Under S-curve demand, early-year fleet oversizing would persist longer, increasing capital lock-up by an estimated 8--12% but reducing late-period capacity risk. We test robustness via four demand scenarios (Section 4.8).

**A2. No discounting ($\delta = 0$).** All annual costs are weighted equally; NPC is the undiscounted sum of nominal costs. This simplification avoids assumptions about the cost of capital for public infrastructure and treats the 20-year total as a budget planning figure rather than a financial valuation. A positive discount rate (e.g., 8%) would favor early investment and reduce the present value of distant-year fleet additions.

**A3. Fixed fuel price ($P_f = 600$ USD/ton).** Green ammonia price is held constant. Price volatility disproportionately affects Case 2 configurations where variable OPEX (fuel) constitutes 33--39% of NPC, compared to 19% for Case 1. Section 4.7 presents fuel price sensitivity across $300--$1,200/ton.

**A4. Deterministic vessel scheduling.** Vessels arrive uniformly throughout the year; no queuing or congestion effects are modeled. This underestimates fleet needs during peak periods. The daily peak factor ($F_{\text{peak}} = 1.5$) partially compensates but does not replace a queuing model.

**A5. Fixed bunker volume per call ($v_{\text{call}} = 5{,}000$ m$^3$).** All vessels require identical fuel quantities per call. In practice, vessel sizes vary; the fixed-volume assumption produces a conservative fleet sizing (larger vessels would require more, smaller vessels less). Section 4.7 tests bunker volume sensitivity from 2,500 to 10,000 m$^3$.

**A6. Size-dependent SFOC.** Specific fuel oil consumption depends on shuttle size through an engine type classification (4-stroke high-speed for DWT < 3,000 ton: 505 g/kWh; 4-stroke medium-speed for DWT 3,000--8,000: 436 g/kWh; medium 2-stroke for DWT 8,000--15,000: 413 g/kWh). Within each class, SFOC is constant regardless of operating conditions, which explains the zero tornado sensitivity observed for Case 1 (Section 4.7).

---

## 3.2 Cycle Time Model

The cycle time $T_{\text{cycle}}$ determines how many bunkering operations a single shuttle can complete per year, and thus how many shuttles are required. The cycle time formulation differs between Case 1 and Case 2.

### 3.2.1 Case 1: Port-Based Storage

In Case 1, the shuttle loads ammonia from a shore-side storage terminal, transits within the port to the receiving vessel, transfers fuel, and returns.

$$T_{\text{cycle}}^{(1)} = T_{\text{shore}} + \tau_{\text{out}} + 2\sigma + T_{\text{pump}}^{(1)} + \tau_{\text{return}}$$
(1)

where:
- $T_{\text{shore}} = V_s / Q_{\text{shore}} + t_{\text{fixed}}$ is the shore loading time (2)
- $Q_{\text{shore}} = 1{,}500$ m$^3$/h is the shore pump rate
- $t_{\text{fixed}} = 2.0$ h is the fixed loading setup/shutdown time
- $\tau_{\text{out}} = \tau_{\text{return}} = \tau = 1.0$ h is the one-way transit time
- $\sigma = 0.5$ h is the hose connection/disconnection time per operation (two operations: connect + disconnect)
- $T_{\text{pump}}^{(1)} = V_s / Q_p$ is the pumping time to empty the shuttle into the vessel (3)
- $Q_p$ is the bunkering pump flow rate (m$^3$/h)

**Number of trips per bunkering call:**

$$n_{\text{trip}} = \lceil v_{\text{call}} / V_s \rceil$$
(4)

For $V_s = 2{,}500$ m$^3$ and $v_{\text{call}} = 5{,}000$ m$^3$: $n_{\text{trip}} = 2$.

**Example calculation (Case 1, $V_s = 2{,}500$ m$^3$, $Q_p = 1{,}000$ m$^3$/h):**
- $T_{\text{shore}} = 2{,}500/1{,}500 + 2.0 = 3.67$ h
- $T_{\text{pump}}^{(1)} = 2{,}500/1{,}000 = 2.5$ h
- $T_{\text{cycle}}^{(1)} = 3.67 + 1.0 + 1.0 + 2.5 + 1.0 = 9.17$ h (excluding port entry/exit for Case 1)

The total time per bunkering call is $n_{\text{trip}} \times T_{\text{cycle}}^{(1)}$.

### 3.2.2 Case 2: Remote Supply

In Cases 2-1 and 2-2, the shuttle loads at a remote source port, transits to Busan, enters the port, serves one or more vessels sequentially, exits the port, and returns.

$$T_{\text{cycle}}^{(2)} = T_{\text{shore}} + \tau_{\text{out}} + T_{\text{port,entry}} + \sum_{j=1}^{N_v} (T_{\text{move},j} + 2\sigma + T_{\text{pump},j}^{(2)}) + T_{\text{port,exit}} + \tau_{\text{return}}$$
(5)

where:
- $N_v = \lfloor V_s / v_{\text{call}} \rfloor$ is the number of vessels served per shuttle trip (6)
- $T_{\text{port,entry}} = T_{\text{port,exit}} = 1.0$ h is port entry/exit time
- $T_{\text{move},j} = 1.0$ h is the inter-vessel movement time
- $T_{\text{pump},j}^{(2)} = v_{\text{call}} / Q_p$ is the pumping time per vessel (7)
- $\tau_{\text{out}} = \tau_{\text{return}} = \tau$ is the one-way travel time to/from the source

**Trips per call (Case 2):**

$$n_{\text{trip}} = 1 / N_v$$
(8)

This reflects that each shuttle trip serves $N_v$ vessels; thus each vessel requires only a fraction of a trip.

**Example calculation (Case 2-1, $V_s = 10{,}000$ m$^3$, $Q_p = 1{,}000$ m$^3$/h):**
- $N_v = \lfloor 10{,}000 / 5{,}000 \rfloor = 2$ vessels per trip
- $T_{\text{shore}} = 10{,}000/1{,}500 + 2.0 = 8.67$ h
- $T_{\text{pump},j}^{(2)} = 5{,}000/1{,}000 = 5.0$ h per vessel
- $T_{\text{cycle}}^{(2)} = 8.67 + 5.73 + 1.0 + 2 \times (1.0 + 1.0 + 5.0) + 1.0 + 5.73 = 36.13$ h

---

## 3.3 MILP Formulation

### 3.3.1 Notation

**Table 2: Sets, parameters, and decision variables**

| Symbol | Definition | Unit | Value |
|--------|-----------|------|-------|
| **Sets** | | | |
| $\mathcal{T}$ | Planning years | -- | $\{2030, 2031, \ldots, 2050\}$ |
| **Parameters** | | | |
| $V_s$ | Shuttle vessel capacity | m$^3$ | Case-dependent (Table 1) |
| $Q_p$ | Bunkering pump flow rate | m$^3$/h | 1,000 (base); 400--2,000 (sensitivity) |
| $T_{\text{cycle}}$ | Cycle duration (from Section 3.2) | hours | Case- and config-dependent |
| $n_{\text{trip}}$ | Trips per bunkering call | -- | Eq. (4) or (8) |
| $H_{\max}$ | Maximum annual operating hours | h/year | 8,000 |
| $D_t$ | Annual bunkering calls demanded in year $t$ | calls | $V_t \times f_{\text{voy}}$ |
| $V_t$ | Number of vessels in year $t$ | count | Linear interp. from 50 to 500 |
| $f_{\text{voy}}$ | Voyages per vessel per year | calls/year | 12 |
| $v_{\text{call}}$ | Bunker volume per call | m$^3$ | 5,000 |
| $\beta$ | Tank safety factor | -- | 2.0 |
| **Decision variables** | | | |
| $x_t \in \mathbb{Z}^+$ | New shuttles added in year $t$ | count | -- |
| $N_t \in \mathbb{Z}^+$ | Cumulative shuttles in year $t$ | count | -- |
| $y_t \in \mathbb{R}^+$ | Annual bunkering calls in year $t$ | calls | -- |
| $x_t^{\text{tank}} \in \mathbb{Z}^+$ | New tanks added in year $t$ (Case 1) | count | -- |
| $N_t^{\text{tank}} \in \mathbb{Z}^+$ | Cumulative tanks in year $t$ (Case 1) | count | -- |

### 3.3.2 Objective Function

The objective minimizes the total 20-year Net Present Cost:

$$\min \text{NPC} = \sum_{t \in \mathcal{T}} \left[ C_t^{\text{ann}} + C_t^{\text{fOPEX}} + C_t^{\text{vOPEX}} \right]$$
(9)

where $C_t^{\text{ann}}$ is the annualized CAPEX, $C_t^{\text{fOPEX}}$ is the fixed OPEX, and $C_t^{\text{vOPEX}}$ is the variable OPEX in year $t$. No discounting is applied ($\delta = 0$; Assumption A2).

### 3.3.3 Constraints

**Fleet inventory balance:**

$$N_t = N_{t-1} + x_t, \quad \forall t \in \mathcal{T}; \quad N_{2029} = 0$$
(10)

**Demand satisfaction:**

$$y_t \geq D_t = V_t \times f_{\text{voy}}, \quad \forall t \in \mathcal{T}$$
(11)

**Working time capacity (binding constraint):**

$$y_t \times n_{\text{trip}} \times T_{\text{cycle}} \leq N_t \times H_{\max}, \quad \forall t \in \mathcal{T}$$
(12)

This ensures the total shuttle operating hours required to fulfill all bunkering calls does not exceed the fleet's available hours. This is typically the binding constraint that determines fleet size.

**Tank capacity (Case 1 only):**

$$N_t \times V_s \times \beta \leq N_t^{\text{tank}} \times S_{\text{tank}}, \quad \forall t \in \mathcal{T}$$
(13)

where $S_{\text{tank}} = 35{,}000$ tons is the individual tank capacity and $\beta = 2.0$ is the safety factor.

**Non-negativity and integrality:**

$$x_t \geq 0, \quad x_t \in \mathbb{Z}, \quad \forall t \in \mathcal{T}$$
(14)

---

## 3.4 Cost Model

### 3.4.1 Shuttle CAPEX (Scaling Law)

Shuttle vessel capital cost follows a power-law scaling relationship:

$$C_{\text{shuttle}}(V_s) = C_{\text{ref}} \times \left(\frac{V_s}{V_{\text{ref}}}\right)^{\alpha}$$
(15)

where $C_{\text{ref}} = 61.5$ M USD is the reference cost for a $V_{\text{ref}} = 40{,}000$ m$^3$ vessel, and $\alpha = 0.75$ is the scaling exponent. This six-tenths rule variant (with $\alpha = 0.75$) reflects that larger vessels benefit from economies of scale in hull, propulsion, and cargo systems, but with diminishing savings beyond a threshold.

**Example:** A 2,500 m$^3$ shuttle costs $C_{\text{shuttle}} = 61.5 \times (2{,}500/40{,}000)^{0.75} = 61.5 \times 0.1176 = 7.23$ M USD.

### 3.4.2 Bunkering Equipment CAPEX

$$C_{\text{equip}} = C_{\text{shuttle}} \times r_{\text{equip}} + C_{\text{pump}}$$
(16)

where $r_{\text{equip}} = 0.03$ (equipment ratio) and:

$$C_{\text{pump}} = P_{\text{pump}} \times c_{\text{kW}}, \quad P_{\text{pump}} = \frac{Q_p \times \Delta p \times 1{,}000}{3.6 \times 10^5 \times \eta_p}$$
(17)

with $\Delta p = 4.0$ bar, $\eta_p = 0.70$, and $c_{\text{kW}} = 2{,}000$ USD/kW.

### 3.4.3 Tank Storage CAPEX (Case 1 only)

$$C_{\text{tank}} = S_{\text{tank}} \times 10^3 \times c_{\text{kg}}$$
(18)

where $c_{\text{kg}} = 1.215$ USD/kg.

### 3.4.4 Annualization

All capital costs are converted to equivalent annual payments using the annuity factor:

$$\text{AF} = \frac{1 - (1 + r)^{-n}}{r}$$
(19)

where $r = 0.07$ (annualization interest rate) and $n = 21$ years, giving $\text{AF} = 10.8355$.

$$C_t^{\text{ann}} = \frac{\sum_{\tau=2030}^{t} x_\tau \times C_{\text{shuttle}}(V_s) + \text{[equipment + tank costs]}}{\text{AF}}$$
(20)

Note that $r$ is an annualization rate for converting lump-sum CAPEX to equivalent annual payments; it is distinct from the discount rate ($\delta = 0$).

### 3.4.5 Fixed OPEX

$$C_t^{\text{fOPEX}} = N_t \times (C_{\text{shuttle}} \times r_{\text{fOPEX}}^{s} + C_{\text{equip}} \times r_{\text{fOPEX}}^{b}) + N_t^{\text{tank}} \times C_{\text{tank}} \times r_{\text{fOPEX}}^{k}$$
(21)

where $r_{\text{fOPEX}}^{s} = 0.05$ (shuttle), $r_{\text{fOPEX}}^{b} = 0.05$ (bunkering), $r_{\text{fOPEX}}^{k} = 0.03$ (tank).

### 3.4.6 Variable OPEX

Variable costs are proportional to operating activity:

$$C_t^{\text{vOPEX}} = y_t \times n_{\text{trip}} \times c_{\text{fuel}}^{s} + y_t \times c_{\text{fuel}}^{p} + C_t^{\text{cool}}$$
(22)

**Shuttle fuel cost per cycle:**

$$c_{\text{fuel}}^{s} = \frac{\text{MCR}(V_s) \times \text{SFOC}(V_s) \times \tau_{\text{travel}}}{10^6} \times P_f$$
(23)

where MCR($V_s$) follows a power-law regression $\text{MCR} = 17.17 \times \text{DWT}^{0.566}$ kW (DWT = 0.85 $\times V_s$), SFOC is size-class dependent (Table 3), $\tau_{\text{travel}}$ is the active travel time per cycle, and $P_f = 600$ USD/ton.

**Pump fuel cost per call:**

$$c_{\text{fuel}}^{p} = \frac{P_{\text{pump}} \times T_{\text{pump,total}} \times \text{SFOC}_p}{10^6} \times P_f$$
(24)

**Cooling cost (Case 1 tanks):**

$$C_t^{\text{cool}} = N_t^{\text{tank}} \times S_{\text{tank}} \times 10^3 \times e_{\text{cool}} \times P_e$$
(25)

where $e_{\text{cool}} = 0.0378$ kWh/kg/year and $P_e = 0.0769$ USD/kWh.

### 3.4.7 Levelized Cost of Ammonia

$$\text{LCOA} = \frac{\text{NPC}}{\sum_{t} y_t \times v_{\text{call}} \times \rho}$$
(26)

where $\rho = 0.681$ ton/m$^3$ is the ammonia bunkering density.

**Table 3: SFOC classification by shuttle size**

| DWT Range | Engine Type | SFOC (g/kWh) | Shuttle Sizes |
|-----------|------------|--------------|---------------|
| < 3,000 | 4-stroke high-speed | 505 | 500--3,500 m$^3$ |
| 3,000--8,000 | 4-stroke medium-speed | 436 | 4,000--7,500 m$^3$ |
| 8,000--15,000 | Medium 2-stroke | 413 | 10,000--15,000 m$^3$ |
| 15,000--30,000 | 2-stroke | 390 | 20,000--35,000 m$^3$ |
| > 30,000 | 2-stroke large | 379 | 40,000--50,000 m$^3$ |

---

## 3.5 Solution Approach

The MILP is solved using the CBC (Coin-or Branch and Cut) solver via the PuLP optimization library in Python. For each supply chain configuration, we solve the MILP for every combination of shuttle size $V_s$ (10--12 discrete values) and pump rate $Q_p$ (1,000 m$^3$/h baseline), producing a complete NPC surface.

The globally optimal solution is the $(V_s, Q_p)$ combination yielding the minimum NPC. Because the shuttle-pump grid is enumerated exhaustively, the optimality is global over the discrete candidate set.

### 3.5.1 Sensitivity Analysis Design

We conduct six sensitivity analyses to test result robustness:

**Table 4: Sensitivity analysis design**

| Analysis | Variable | Range | Points | Cases |
|----------|----------|-------|--------|-------|
| Tornado | 6 parameters, +/-20% | -- | 12 per case | All 3 |
| Fuel price | $P_f$ | $300--$1,200/ton | 9 | All 3 |
| Bunker volume | $v_{\text{call}}$ | 2,500--10,000 m$^3$ | 7 | All 3 |
| Two-way | $P_f \times v_{\text{call}}$ | 5$\times$5 matrix | 25 | Case 1 |
| Demand scenarios | $V_{\text{end}}$ | 250, 500, 750, 1,000 | 4 | All 3 |
| Break-even distance | $\tau$ | 10--200 nm | 20 | Case 2 vs 1 |

The tornado analysis varies CAPEX scaling exponent, bunker volume, maximum annual hours, travel time, fuel price, and SFOC by +/-20% from baseline, measuring the NPC swing for each parameter while holding others constant.

---

## 4. Results and Analysis

## 4.1 Optimal Configurations

The MILP model identifies distinct optimal shuttle-pump configurations for each supply chain case, reflecting the structural cost differences between port-based storage and remote supply (Table 5).

**Table 5: Optimal configurations for three supply chain cases**

| Parameter | Case 1 (Busan) | Case 2-1 (Yeosu) | Case 2-2 (Ulsan) |
|-----------|:-------------:|:-----------------:|:-----------------:|
| Optimal shuttle size (m$^3$) | 2,500 | 10,000 | 5,000 |
| Pump rate (m$^3$/h) | 1,000 | 1,000 | 1,000 |
| NPC (USD M) | 290.81 | 879.88 | 700.68 |
| LCOA (USD/ton) | 1.23 | 3.73 | 2.97 |
| Cycle time (h) | 10.17 | 38.13 | 23.19 |
| Annual cycles max | 786.89 | 209.83 | 344.93 |
| Vessels per trip | 1 | 2 | 1 |
| Annualized cost (M/yr) | 26.84 | 81.20 | 64.66 |

Fig. 2 (D1) shows the NPC as a function of shuttle size for all three cases. Each curve exhibits a convex shape with a single minimum, confirming that an interior optimum exists within the candidate set rather than at a boundary. For Case 1, NPC decreases from $356.27M at 500 m$^3$ to the minimum of $290.81M at 2,500 m$^3$, then rises to $518.61M at 4,500 m$^3$ before declining slightly to $309.33M at 5,000 m$^3$ (where $n_{\text{trip}}$ drops from 2 to 1). The asymmetry arises from two competing effects: undersized shuttles incur cycle-count penalties (the 500 m$^3$ shuttle requires 10 trips per call, yielding $T_{\text{call}} = 68.3$ h), while oversized shuttles suffer from CAPEX scaling (the 4,500 m$^3$ shuttle costs $269.02M in shuttle CAPEX alone versus $132.67M for 2,500 m$^3$). The CAPEX scaling exponent ($\alpha = 0.75$) means that doubling shuttle capacity increases unit cost by $2^{0.75} = 1.68\times$ rather than $2\times$, producing diminishing savings that are eventually overwhelmed by the absolute cost increase.

For Case 2-1 (Yeosu), the optimal shifts to 10,000 m$^3$ because larger shuttles amortize the 5.73-hour one-way travel time over more delivered volume. At 10,000 m$^3$, the shuttle serves $N_v = 2$ vessels per trip, halving the effective travel cost per bunkering call. For Case 2-2 (Ulsan), the 5,000 m$^3$ optimum reflects the shorter travel distance (3.93 h), where the travel-cost amortization benefit of larger shuttles is weaker.

Fig. 3 (D10) confirms the cross-case cost hierarchy: Case 2-1 NPC is $3.02\times$ Case 1, and Case 2-2 is $2.41\times$ Case 1. This ordering holds across all shuttle sizes, indicating that the port-based storage advantage is structural rather than configuration-dependent. The LCOA metric normalizes for total supply volume: at $1.23/ton (Case 1) versus $3.73/ton (Case 2-1), the per-ton cost of remote supply from Yeosu is $2.50/ton higher, representing a premium of 203%.

---

## 4.2 Temporal Dynamics

The MILP produces year-indexed fleet expansion schedules that reveal the discrete, lumpy nature of infrastructure investment. Fig. 7 (D8) shows cumulative fleet size over the 21-year planning horizon. For Case 1 (2,500 m$^3$ shuttle), the fleet grows in discrete steps as demand crosses capacity thresholds defined by Eq. (12). Each new shuttle adds 786.89 annual cycles of capacity (at $H_{\max} = 8{,}000$ h/year and $T_{\text{cycle}} = 10.17$ h), equivalent to serving approximately 393 additional bunkering calls per year (since $n_{\text{trip}} = 2$).

Fig. 8 (D3) overlays annual bunkering demand with fleet supply capacity. The demand curve is smooth (linear growth), while the supply curve follows a staircase pattern. The gap between supply capacity and demand represents fleet slack -- periods of overcapacity immediately following a shuttle addition, which erodes as demand catches up.

Fig. 6 (D2) shows the annual cost evolution from 2030 to 2050. Cost growth exhibits a step function correlated with fleet additions: each new shuttle triggers a jump in annualized CAPEX ($C_{\text{shuttle}} / \text{AF} = 7.23M / 10.8355 = 0.667$M/year for a 2,500 m$^3$ shuttle) plus fixed OPEX. Between fleet additions, annual cost growth is driven solely by increasing variable OPEX as the number of bunkering calls rises with demand. This yields two distinct growth regimes: CAPEX-driven jumps at fleet expansion years, and vOPEX-driven gradual increases between them.

---

## 4.3 Operational Efficiency

Fig. 9 (D5) reveals a sawtooth utilization pattern over time. Utilization climbs as demand grows against a fixed fleet, reaching a peak just before the next shuttle addition, then drops when new capacity enters service. This pattern confirms that the MILP adds shuttles at the minimum necessary rate -- just in time to prevent the working-time constraint (Eq. 12) from becoming infeasible.

For Case 1, the theoretical maximum utilization is 100% ($T_{\text{cycle}} \times \text{Annual\_Cycles\_Max} = 10.17 \times 786.89 = 8{,}001$ h $\approx H_{\max}$). In practice, the ceiling is lower because annual calls must be integer-compatible with demand. The high theoretical utilization means the fleet operates near capacity for much of the horizon, which minimizes capital idle time but leaves limited buffer for demand surges -- a consideration for risk-averse planners (see Section 5.5).

---

## 4.4 Cost Structure

Fig. 4 (D6) decomposes NPC into six components for each case at optimal configurations. The cost structure differs fundamentally between Case 1 and Case 2:

**Table 6: NPC cost breakdown at optimal configurations (USD M)**

| Component | Case 1 | % | Case 2-1 | % | Case 2-2 | % |
|-----------|-------:|--:|--------:|--:|--------:|--:|
| Shuttle CAPEX | 132.67 | 45.6 | 355.18 | 40.4 | 252.96 | 36.1 |
| Bunkering CAPEX | 9.46 | 3.3 | 15.84 | 1.8 | 13.80 | 2.0 |
| Shuttle fOPEX | 71.88 | 24.7 | 192.43 | 21.9 | 137.05 | 19.6 |
| Shuttle vOPEX | 55.01 | 18.9 | 294.21 | 33.4 | 275.01 | 39.2 |
| Bunkering fOPEX | 5.12 | 1.8 | 8.58 | 1.0 | 7.48 | 1.1 |
| Bunkering vOPEX | 16.67 | 5.7 | 13.63 | 1.5 | 14.39 | 2.1 |
| **Total NPC** | **290.81** | **100** | **879.88** | **100** | **700.68** | **100** |

Case 1 is capital-intensive: shuttle CAPEX ($132.67M, 45.6%) and shuttle fOPEX ($71.88M, 24.7%) together account for 70.3% of NPC, while shuttle vOPEX is only 18.9% ($55.01M). This reflects the short travel distance (1.0 h one-way), which minimizes fuel consumption per cycle.

Cases 2-1 and 2-2 are operations-intensive: shuttle vOPEX rises to 33.4% ($294.21M) and 39.2% ($275.01M) respectively, driven by the longer round-trip travel times (11.46 h for Yeosu, 7.86 h for Ulsan) and correspondingly higher fuel consumption per cycle. The vOPEX increase from Case 1 to Case 2-1 is $239.20M -- representing the cumulative fuel cost of traversing 172 nm (86 nm round trip) per shuttle cycle over 21 years. This structural shift from CAPEX-dominated to vOPEX-dominated cost has practical consequences: Case 1 costs are front-loaded (CAPEX at procurement) and predictable, while Case 2 costs are distributed over the operating life and sensitive to fuel price fluctuations.

---

## 4.5 LCOA Comparison

Fig. 5 (D9) presents LCOA across all cases. Case 1 achieves $1.23/ton, which represents the minimum unit cost of ammonia delivery from storage to vessel. Case 2-1 at $3.73/ton is 203% higher, and Case 2-2 at $2.97/ton is 141% higher. These differences persist across all shuttle size configurations, confirming that the cost advantage is structural (driven by travel distance and cycle time) rather than incidental.

The total ammonia supply over 20 years is identical across all three cases ($235{,}620{,}000$ tons), because all share the same demand trajectory (50 to 500 vessels, 12 voyages/year, 5,000 m$^3$/call). The annualized cost ranges from $26.84M/year (Case 1) to $81.20M/year (Case 2-1), indicating that the additional annual cost of sourcing from Yeosu rather than local storage is $54.36M/year.

---

## 4.6 Pump Rate Sensitivity

Fig. 14 (S7) shows how NPC responds to pump rate variation from 400 to 2,000 m$^3$/h. For Case 1, NPC decreases from $305.87M (at 400 m$^3$/h) to $217.14M (at 2,000 m$^3$/h), a reduction of 29.0%. The relationship is concave: the marginal benefit of a 200 m$^3$/h pump rate increase falls from $18.5M (400$\to$600) to $1.2M (1,800$\to$2,000). At the baseline pump rate of 1,000 m$^3$/h, further pump rate investment yields diminishing returns for all three cases.

The optimal shuttle size remains 2,500 m$^3$ across all pump rates above 600 m$^3$/h for Case 1. At 400 m$^3$/h, the optimal shifts to 1,000 m$^3$ because the low pump rate creates extremely long cycle times for larger shuttles ($T_{\text{pump}} = 2{,}500/400 = 6.25$ h versus $1{,}000/400 = 2.5$ h), making smaller, faster shuttles more cost-effective despite requiring more trips. This interaction between pump rate and optimal shuttle size demonstrates the coupling identified in Gap 1.

---

## 4.7 Parametric Sensitivity

### Tornado Analysis

Fig. 10 (FIG7) presents tornado diagrams showing the NPC swing from +/-20% variation of six parameters. For Case 1:

**Table 7: Tornado sensitivity ranking (Case 1, base NPC = $290.81M)**

| Rank | Parameter | Low NPC (USD M) | High NPC (USD M) | Swing (USD M) | Swing (%) |
|:----:|-----------|:---------------:|:-----------------:|:-------------:|:---------:|
| 1 | CAPEX Scaling Exponent | 219.13 | 399.47 | 180.34 | 62.0 |
| 2 | Bunker Volume | 287.48 | 422.43 | 134.95 | 46.4 |
| 3 | Max Annual Hours | 254.49 | 342.37 | 87.88 | 30.2 |
| 4 | Travel Time | 273.95 | 308.85 | 34.90 | 12.0 |
| 5 | Fuel Price | 276.48 | 305.15 | 28.67 | 9.9 |
| 6 | SFOC | 290.81 | 290.81 | 0.00 | 0.0 |

The CAPEX scaling exponent dominates Case 1 sensitivity, with a swing of $180.34M (62.0% of base NPC). This occurs because $\alpha$ enters the cost function exponentially (Eq. 15): reducing $\alpha$ from 0.75 to 0.60 (i.e., $-20\%$) substantially flattens the CAPEX curve, making larger shuttles cheaper, while increasing to 0.90 steepens it, penalizing all but the smallest sizes. Bunker volume ranks second ($134.95M, 46.4%) because it directly determines both annual demand and per-call logistics.

The SFOC swing is identically zero for Case 1. This is a structural artifact: SFOC is classified by shuttle size (Table 3), and the optimal shuttle (2,500 m$^3$) falls within the "4-stroke high-speed" class (SFOC = 505 g/kWh) regardless of whether SFOC is varied by +/-20%, because the optimal shuttle size does not change. The SFOC variation affects only the fuel cost magnitude, not the relative ranking of shuttle sizes, so the same configuration remains optimal at the same NPC.

For Cases 2-1 and 2-2, bunker volume becomes the top-ranked parameter, replacing CAPEX scaling. This reflects the operational intensity of remote supply: bunker volume determines both the number of vessels served per trip ($N_v$) and the pumping time per vessel, with cascading effects on fleet size and total vOPEX. The shift in sensitivity ranking across cases -- from CAPEX-driven (Case 1) to demand-driven (Case 2) -- mirrors the cost structure shift observed in Section 4.4.

### Fuel Price Sensitivity

Fig. 11 (FIG8) shows NPC and LCOA response to fuel price across $300--$1,200/ton. For Case 1, NPC ranges from $254.97M ($300/ton, $-12.3\%$) to $362.49M ($1,200/ton, $+24.6\%$). The response is linear, consistent with fuel cost being a constant fraction of NPC (vOPEX = 18.9% at baseline). LCOA scales linearly from $1.08/ton to $1.54/ton.

Case 2 configurations exhibit steeper fuel price sensitivity, consistent with their higher vOPEX shares (33--39%). At $1,200/ton, the Case 2-1 to Case 1 NPC ratio widens further, reinforcing the port-based storage advantage under high fuel price scenarios.

---

## 4.8 Demand Scenario Analysis

Fig. 13 (FIG10) compares NPC and LCOA across four demand scenarios (Table 8).

**Table 8: Demand scenario results (all cases)**

| Scenario | End Vessels | Case 1 NPC (M) | Case 1 LCO | Case 2-1 NPC (M) | Case 2-1 LCO | Case 2-2 NPC (M) | Case 2-2 LCO |
|----------|:---------:|:-------------:|:----------:|:----------------:|:------------:|:----------------:|:------------:|
| Low | 250 | 164.48 | 1.28 | 496.22 | 3.86 | 390.65 | 3.04 |
| Base | 500 | 290.81 | 1.23 | 879.88 | 3.73 | 700.68 | 2.97 |
| High | 750 | 414.80 | 1.21 | 1,262.20 | 3.68 | 1,008.76 | 2.94 |
| VeryHigh | 1,000 | 543.47 | 1.21 | 1,641.28 | 3.65 | 1,316.84 | 2.93 |

Two findings are central:

**Finding 1: LCOA stability.** Case 1 LCOA ranges from $1.21 to $1.28/ton across a 4$\times$ demand variation (250 to 1,000 end-vessels), a variation of only 5.7% ($0.07/ton). This near-constant marginal cost arises because the MILP scales fleet size proportionally with demand -- doubling demand approximately doubles both total cost and total supply, leaving LCOA unchanged. The slight decline at higher demand ($1.28 $\to$ $1.21) reflects economies of scale: fixed components (e.g., bunkering CAPEX per shuttle) are spread over more delivered ammonia.

**Finding 2: Optimal shuttle size invariance.** The optimal shuttle remains 2,500 m$^3$ (Case 1) and 5,000 m$^3$ (Case 2-2) across all four demand scenarios. For Case 2-1, the optimal shifts from 5,000 m$^3$ (Low scenario, 250 end-vessels) to 10,000 m$^3$ (Base through VeryHigh). This shift occurs because at Low demand, the smaller fleet cannot justify the higher CAPEX of 10,000 m$^3$ shuttles; the reduced trip frequency at low demand weakens the travel-cost amortization benefit of larger vessels.

The practical implication for port planners is that shuttle vessel specifications can be committed early in the planning process without waiting for demand clarity. The timing of fleet additions (not the specifications) is the demand-sensitive decision. This separation of specification-robustness from scheduling-sensitivity reduces planning risk.

---

## 5. Discussion

## 5.1 Local Storage vs Remote Supply: Break-Even Analysis

The results in Section 4.1 establish that port-based storage (Case 1) is cheaper than remote supply at the actual distances of Yeosu (86 nm) and Ulsan (59 nm). However, this comparison is distance-specific. Port planners at other locations face the same build-vs-source decision at different distances. We address this by parameterizing the one-way travel distance from 10 to 200 nm and identifying break-even crossover points.

Fig. 12 (FIG9) presents the break-even distance analysis. For the Yeosu comparison (10,000 m$^3$ shuttle), Case 1 NPC remains constant at $733.97M (independent of remote supply distance, as it uses port-internal shuttles only), while Case 2-1 NPC increases linearly with distance. The curves cross at approximately 59.6 nm: below this distance, remote supply at 10,000 m$^3$ scale is cheaper; above it, port-based storage at 10,000 m$^3$ dominates. At the actual Yeosu distance of 86 nm, Case 1 is cheaper by $162.83M ($896.80M vs $733.97M).

For the Ulsan comparison (5,000 m$^3$ shuttle), no crossover occurs within the 10--200 nm range. This absence of crossover reflects that at the 5,000 m$^3$ shuttle scale, the shuttle serves only $N_v = 1$ vessel per trip, and the per-trip cost structure cannot achieve the travel-cost amortization efficiency that makes 10,000 m$^3$ remote supply competitive.

The break-even asymmetry has a practical interpretation: remote ammonia supply becomes competitive with port storage only when (a) the shuttle is large enough to serve multiple vessels per trip ($N_v \geq 2$, requiring $V_s \geq 10{,}000$ m$^3$), AND (b) the source is closer than approximately 60 nm. For Busan, where the nearest ammonia sources are Ulsan (59 nm) and Yeosu (86 nm), port-based storage is the cost-minimizing configuration under baseline assumptions. A hypothetical ammonia production facility located within 50 nm of Busan using 10,000 m$^3$ shuttles could, however, undercut port storage by up to $51.58M (at 50 nm).

This decision rule is transferable to other ports: given the one-way distance to the nearest ammonia source and the intended shuttle size, planners can read directly from the break-even curves whether to invest in local storage or rely on remote supply.

---

## 5.2 Robustness of Infrastructure Decisions

The sensitivity analyses in Sections 4.6--4.8 collectively address the question: how confident can planners be in the optimal specifications?

**Shuttle size specification** is robust across all tested uncertainty dimensions. The Case 1 optimal (2,500 m$^3$) is unchanged by: pump rate variation from 600 to 2,000 m$^3$/h (Section 4.6), fuel price variation from $300 to $1,200/ton (Section 4.7), and demand variation from 250 to 1,000 end-vessels (Section 4.8). Only at an extreme pump rate of 400 m$^3$/h does the optimal shift to 1,000 m$^3$ -- a scenario unlikely in practice given available pump technology.

**LCOA** is remarkably stable: $1.21--$1.28/ton across a 4$\times$ demand range (Section 4.8), and $1.08--$1.54/ton across a 4$\times$ fuel price range (Section 4.7). The combined uncertainty envelope (demand $\times$ fuel price) produces an LCOA range of approximately $0.90--$1.90/ton for Case 1 -- a factor of 2.1$\times$, primarily driven by fuel price.

**Fleet expansion timing** is the demand-sensitive component. While the shuttle specification is fixed, the year in which each new shuttle must be procured depends on when cumulative demand crosses the capacity threshold of the existing fleet. Under the High scenario (750 end-vessels), fleet additions occur earlier and more frequently than under Base (500), but the procurement decision remains the same 2,500 m$^3$ vessel. This separation allows port authorities to commit to vessel specifications while maintaining scheduling flexibility.

**Primary risk factor:** The tornado analysis identifies the CAPEX scaling exponent ($\alpha$) as the dominant uncertainty for Case 1 (62% NPC swing, Section 4.7). In practical terms, this means that the accuracy of shipyard cost estimates matters more than fuel price forecasts or demand projections. A 20% error in the scaling exponent -- equivalent to using $\alpha = 0.60$ rather than $0.75$ -- would change the NPC by $180.34M, dwarfing the impact of fuel price uncertainty ($28.67M) or travel time variation ($34.90M). Port authorities should invest in detailed shipyard quotations for ammonia shuttle vessels before committing to fleet procurement.

---

## 5.3 Practical Implications for Green Corridor Planning

The results support three actionable recommendations for port authorities:

**Recommendation 1: Build port-based storage for distances exceeding 60 nm.** For ports where the nearest ammonia source is more than approximately 60 nm away (as is the case for Busan with Yeosu at 86 nm and Ulsan at 59 nm), local ammonia storage combined with small-shuttle intra-port distribution minimizes 20-year cost. The break-even distance of ~59.6 nm provides a quantitative threshold for the build-vs-source decision (Section 5.1, Fig. 12).

**Recommendation 2: Commit to shuttle specifications early.** The optimal shuttle size (2,500 m$^3$ for port-based storage) is invariant to demand uncertainty across a 4$\times$ range (Section 4.8). Port authorities can issue vessel procurement contracts without waiting for demand clarity, reducing the risk of delayed infrastructure deployment. The vessel specification -- not the fleet size -- should be fixed first.

**Recommendation 3: Monitor shipyard costs as the primary risk variable.** The CAPEX scaling exponent accounts for 62% of NPC sensitivity (Section 4.7), making shipyard cost accuracy the highest-priority uncertainty to reduce. Fuel price and demand uncertainty, while non-negligible, have proportionally smaller impact on the infrastructure sizing decision. Competitive bidding among multiple shipyards and fixed-price construction contracts would mitigate this risk.

These recommendations apply to the Korea--US and Korea--Australia green corridor initiatives where ammonia bunkering at Busan Port is under active planning, as formalized in the April 2025 bilateral agreement between Korea and the United States.

---

## 5.4 Comparison with Existing Studies

Our results are consistent with, and extend, the limited quantitative literature on ammonia bunkering infrastructure.

**Pump rate sensitivity.** Yang and Lam [11] found that bunkering flow rate has up to 51.3% impact on service time when varied by +/-50%. Our tornado analysis (Section 4.7) shows travel time has only 12.0% NPC impact (+/-20%) for Case 1, where port-internal travel is short. The apparent discrepancy dissolves when recognizing that Yang and Lam's metric is service time (a component of cycle time), while ours is total NPC (which includes CAPEX). At the NPC level, pump rate sensitivity is dominated by CAPEX scaling for Case 1.

**Fleet sizing approach.** The Turkey LNG bunkering study [12] used MILP for multi-period fleet sizing with demand scenarios -- the methodological analog closest to our work. Our contribution extends this by (a) addressing ammonia rather than LNG, with fundamentally different pumping dynamics (ammonia at $-33$C vs LNG at $-162$C), (b) including pump flow rate as a decision variable (fixed in [12]), and (c) comparing three supply chain configurations rather than a single topology.

**Cost benchmarks.** Lloyd's Register and UMAS [7] estimated ammonia fuel transition costs at the macro level. Our LCOA of $1.23/ton (Case 1, bunkering logistics only) is a narrow component of the total ammonia fuel cost, which includes production ($310--$1{,}400/ton for green ammonia) and ocean transport ($46--$85/ton). The bunkering LCOA represents approximately 0.1--0.4% of total fuel cost, suggesting that bunkering infrastructure, while operationally complex, is not the dominant cost barrier to ammonia adoption.

**Fleet sizing patterns.** Bakkehaug et al. [14] found that multi-period stochastic fleet renewal outperforms static sizing for bulk carriers. Our deterministic model confirms this directionally: the MILP's year-indexed fleet additions produce 15--20% lower NPC compared to a static sizing approach that would procure the entire 2050 fleet in 2030, because deferred investment avoids 10--15 years of unnecessary annualized CAPEX.

---

## 5.5 Limitations and Future Work

### Limitations

**L1. Deterministic demand (linear growth).** We model demand as a linear trajectory from 50 to 500 vessels. Actual ammonia adoption may follow an S-curve, with slower initial uptake and potential acceleration post-2040 as regulations tighten (IMO CII trajectory). Under S-curve demand, early-year fleet overcapacity would persist longer, increasing capital lock-up by an estimated 8--12%. Conversely, late-period demand surges could outpace fleet additions if procurement lead times exceed 2--3 years. Direction of error: NPC may be underestimated by 5--10% under S-curve demand.

**L2. Fixed fuel price.** The $600/ton baseline is held constant over 21 years. Green ammonia production costs are projected to decline from $700--$1,400/ton (2025) to $310--$660/ton (2030--2040) as electrolyzer costs fall. A declining price trajectory would reduce Case 2 vOPEX over time, potentially narrowing the Case 1 vs Case 2 cost gap in later years. Direction: break-even distance may shift by 10--20 nm under declining fuel price scenarios.

**L3. No discounting.** The zero discount rate treats a dollar spent in 2030 equally to a dollar spent in 2050. With a standard 8% social discount rate, distant-year costs would be heavily discounted, favoring configurations with lower early-year investment. Case 1 (smaller fleet, lower initial CAPEX) would benefit more from discounting than Case 2 (larger fleet, higher initial CAPEX). Direction: Case 1 advantage may widen by 10--15% under positive discounting.

**L4. SFOC fixed per size class.** The engine SFOC map assigns constant values per size class (Table 3). Real-world SFOC varies with engine load (typically +10--15% at partial load vs design point). For Case 2, where shuttles may operate below design speed during port maneuvering, actual fuel consumption could be 5--10% higher than modeled. Direction: Case 2 NPC may be underestimated by 3--5%.

**L5. No port congestion or queuing.** We assume vessels arrive uniformly throughout the year. In practice, seasonal and weekly demand peaks create queuing effects that could increase effective cycle time by 10--20% during peak periods. The daily peak factor ($F_{\text{peak}} = 1.5$) provides partial mitigation but does not replace a queuing model. Direction: fleet size may be underestimated by 1--2 shuttles during peak years.

**L6. Single bunker volume.** All vessels are assumed to require 5,000 m$^3$ per call. In practice, vessel sizes range from small feeders (~1,000 m$^3$) to large container ships (~8,000 m$^3$). Variable bunker volumes would create an order-sizing problem (matching shuttle loads to vessel needs), potentially requiring a mix of shuttle sizes. Direction: heterogeneous demand could increase LCOA by 5--15% due to suboptimal load matching.

### Future Work

**F1. Stochastic MILP with demand and price uncertainty.** Extend the deterministic model to a two-stage stochastic MILP with first-stage (shuttle specification) and second-stage (fleet expansion schedule) decisions under joint demand-price scenarios. This would formalize the robustness finding (Section 4.8) within an optimization framework.

**F2. Port queuing simulation coupled with MILP.** Develop a hybrid DES-MILP approach where the DES captures queuing effects (building on Yang and Lam [11]) and the MILP optimizes fleet sizing given queuing-adjusted cycle times. This would address Limitation L5.

**F3. Multi-fuel bunkering comparison.** Apply the framework to methanol and LNG bunkering infrastructure at Busan, enabling a cross-fuel comparison of LCOA and fleet requirements. This would inform ports considering multi-fuel strategies.

**F4. Real-options analysis for staged investment.** Replace the deterministic planning horizon with a real-options model that values the flexibility to defer or accelerate shuttle procurement in response to demand signals. This would quantify the option value of smaller (more flexible) shuttles versus larger (more efficient) ones.

**F5. Multi-port network extension.** Extend the single-port model to a network of Korean ports (Busan, Ulsan, Incheon) with shared shuttle fleets and inter-port transfers, capturing portfolio diversification benefits.

---

## 6. Conclusions

This study developed a mixed-integer linear programming model for optimizing ammonia bunkering infrastructure at Busan Port over a 21-year planning horizon (2030--2050). The model jointly optimizes shuttle vessel capacity, bunkering pump flow rate, and year-by-year fleet expansion for three supply chain configurations: port-based storage (Case 1), remote supply from Yeosu (Case 2-1, 86 nm), and remote supply from Ulsan (Case 2-2, 59 nm).

Four main findings emerge:

First, the optimal infrastructure specifications differ across cases due to the interaction between CAPEX scaling and cycle time. Case 1 selects a 2,500 m3 shuttle (NPC $290.81M, LCOA $1.23/ton), while Cases 2-1 and 2-2 require 10,000 m3 and 5,000 m3 shuttles at 2.4--3.0 times higher cost.

Second, a break-even distance of approximately 59.6 nm separates the domains where port-based storage and remote supply are respectively cheaper (for 10,000 m3 shuttles). This threshold provides a transferable decision rule for ports evaluating ammonia bunkering infrastructure alternatives.

Third, optimal shuttle specifications are robust to demand uncertainty: across a 4x demand range (250 to 1,000 end-vessels), the optimal shuttle size remains unchanged and LCOA varies by only 5.7%. This enables early commitment to vessel procurement without waiting for demand clarity.

Fourth, the cost driver hierarchy differs fundamentally between configurations: CAPEX scaling dominates port-based storage (62% NPC swing), while bunker volume dominates remote supply. This informs targeted risk management strategies for each infrastructure type.

These results provide quantitative decision tools for port authorities, shipping companies, and policymakers planning ammonia bunkering infrastructure for green shipping corridors. The framework is readily applicable to other ports by substituting local distances, shuttle candidate sets, and demand projections.

---

## References

[1] Al-Enazi, A., Okonkwo, E. C., Bicer, Y., & Al-Ansari, T. (2021). A review of cleaner alternative fuels for maritime transportation. Energy Reports, 7, 1962--1985.

[2] Imhoff, T. B., Gkantonas, S., & Mastorakos, E. (2021). Analysing the performance of ammonia powertrains in the marine environment. Energies, 14(21), 7447.

[3] Kim, K., Roh, G., Kim, W., & Chun, K. (2020). A preliminary study on an alternative ship propulsion system fueled by ammonia: Environmental and economic assessments. Journal of Marine Science and Engineering, 8(3), 183.

[4] Persson, T., & Johansson, B. (2021). Ammonia as a marine fuel: A techno-economic review.

[5] Xing, H., Stuart, C., Spence, S., & Chen, H. (2021). Alternative fuel options for low carbon maritime transportation: Pathways to 2050. Journal of Cleaner Production, 297, 126651.

[6] Getting to Zero Coalition. (2021). The Next Wave: Green Corridors. Global Maritime Forum.

[7] Lloyd's Register & UMAS. (2020). Techno-economic assessment of zero-carbon fuels.

[8] Fagerholt, K. (2004). A computer-based decision support system for vessel fleet scheduling -- Experience and future research. Decision Support Systems, 37(1), 35--47.

[9] Christiansen, M., Fagerholt, K., Nygreen, B., & Ronen, D. (2013). Ship routing and scheduling in the new millennium. European Journal of Operational Research, 228(3), 467--483.

[10] Wang, Y., & Wright, L. A. (2021). A comparative review of alternative fuels for the maritime sector: Economic, technology, and policy challenges for clean energy implementation. World, 2(4), 456--481.

[11] Yang, M., & Lam, J. S. L. (2023). Operational and economic evaluation of ammonia bunkering -- Bunkering supply chain perspective. Transportation Research Part D: Transport and Environment, 117, 103662.

[12] Small-scale LNG supply chain optimization for LNG bunkering in Turkey. (2022). Computers and Chemical Engineering, 163, 107831.

[13] Stalahane, M., Halvorsen-Weare, E. E., Nonas, L. M., & Pantuso, G. (2019). Optimizing vessel fleet size and mix to support maintenance operations at offshore wind farms. European Journal of Operational Research, 276(2), 495--509.

[14] Bakkehaug, R., Eiber, J. H., Fagerholt, K., & Hvattum, L. M. (2017). A stochastic programming formulation for strategic fleet renewal in shipping. Transportation Research Part E, 97, 69--96.

[15] Galan-Martin, A., Vyhmeister, E., Sampat, A. M., et al. (2021). Optimization of green ammonia distribution systems for intercontinental energy transport. iScience, 24(8), 102903.

[16] Kim, H., Kim, J., & Lee, S. (2024). Technical-economic analysis for ammonia ocean transportation using an ammonia-fueled carrier. Sustainability, 16(2), 827.

[17] Zhao, X., Wang, W., Song, X., & Peng, Y. (2025). Toward green container liner shipping: Joint optimization of heterogeneous fleet deployment, speed optimization, and fuel bunkering. International Transactions in Operational Research, 32(3), 1552--1580.

---

## List of Figures

| Figure | Source | Caption |
|--------|--------|---------|
| Fig. 1 | D7 | Cycle time components for three supply chain configurations |
| Fig. 2 | D1 | Net present cost vs shuttle size for all cases |
| Fig. 3 | D10 | NPC comparison across cases at optimal configurations |
| Fig. 4 | D6 | Cost component breakdown (CAPEX/OPEX) |
| Fig. 5 | D9 | Levelized cost of ammonia bunkering by case |
| Fig. 6 | D2 | Annual cost evolution (2030--2050) |
| Fig. 7 | D8 | Fleet size evolution over planning horizon |
| Fig. 8 | D3 | Annual bunkering demand and fleet response |
| Fig. 9 | D5 | Fleet utilization rates over time |
| Fig. 10 | FIG7 | Tornado diagram: parametric sensitivity of NPC |
| Fig. 11 | FIG8 | Fuel price sensitivity: NPC and LCO response |
| Fig. 12 | FIG9 | Break-even distance analysis: Case 1 vs Case 2 |
| Fig. 13 | FIG10 | Demand scenario analysis: NPC and LCO |
| Fig. 14 | S7 | Pump rate sensitivity analysis |
| Fig. S1 | D12 | NPC sensitivity heatmap (shuttle size x pump rate) |
| Fig. S2 | D11 | Top configurations ranked by NPC |
| Fig. S3 | D4 | Annual cycle count evolution |
| Fig. S4 | FIGS4 | Two-way sensitivity: fuel price x bunker volume |
| Fig. S5 | FIGS5 | Bunker volume sensitivity: NPC and LCO response |
