# Optimal Ammonia Bunkering Infrastructure for Green Shipping Corridors: A Multi-Period Mixed-Integer Linear Programming Approach

---

## Abstract

Ammonia is a leading zero-carbon marine fuel candidate, yet no quantitative framework exists for sizing the port-level bunkering infrastructure -- shuttle vessels, pumps, and storage -- required to deliver it from production facilities to ship fuel tanks. We formulate a mixed-integer linear programming (MILP) model that systematically evaluates all feasible shuttle-pump combinations and optimizes fleet deployment for each configuration over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port: port-based storage (Case 1), remote supply from Yeosu at 86 nm (Case 2-1), and remote supply from Ulsan at 59 nm (Case 2-2). Demand grows linearly from 50 to 500 ammonia-fueled vessels at 12 voyages per year. The model identifies distinct optimal configurations: Case 1 selects a 2,500 m3 shuttle at a 21-year net present cost (NPC) of $410.34M and levelized cost of ammonia bunkering (LCOA) of $1.74/ton, while Cases 2-1 and 2-2 require larger shuttles (5,000 and 5,000 m3) at 2.0--2.5 times higher cost. A parametric break-even analysis establishes that remote supply becomes cheaper than port storage below approximately 84 nm one-way distance at the 10,000 m3 shuttle scale. Sensitivity analysis across four demand scenarios (250--1,000 end-vessels) demonstrates that optimal shuttle specifications are invariant, with LCOA varying only 4.0%. These results provide port authorities with quantitative decision tools for ammonia bunkering infrastructure investment in green shipping corridors.

**Keywords:** ammonia bunkering; green shipping corridor; mixed-integer linear programming; fleet sizing; levelized cost; infrastructure optimization

---

## 1. Introduction

The International Maritime Organization (IMO) has adopted a revised GHG strategy targeting at least 30% emission reduction by 2030, 80% by 2040, and net-zero by or around 2050 relative to 2008 levels [5, 29]. Achieving these targets requires a transition from conventional marine fuels to zero-carbon alternatives. Among the candidates, ammonia (NH$_3$) has emerged as a leading option due to its zero-carbon combustion, existing global production infrastructure (~180 million tons/year), and compatibility with established bulk liquid transport methods [1, 2]. Green ammonia production costs are projected to decline from $720--$1,400/ton (2022) to $310--$610/ton by 2050 [31], making it increasingly competitive as a marine fuel. As of December 2025, 144 ammonia-fueled vessels and 302 ammonia-ready vessels have been ordered, signaling that the demand side of the ammonia fuel transition is materializing. The supply side -- specifically, the port-level infrastructure required to deliver ammonia from production facilities to vessel fuel tanks -- remains unresolved.

Green shipping corridor initiatives aim to bridge this gap by establishing end-to-end infrastructure for zero-emission vessel operations along specific trade routes. The Korea--United States green corridor agreement (formalized April 2025) targets ammonia-fueled container ship operations between Busan and Seattle-Tacoma by 2027, with the Korean government investing approximately $10 billion in Busan mega-port infrastructure including alternative fuel bunkering facilities [6]. Similar corridors are planned between Korea and Australia. These initiatives specify the fuel (ammonia) and the endpoints (ports) but leave a fundamental operational question unanswered: what bunkering infrastructure -- shuttle vessels, pumps, and storage facilities -- is required, at what scale, and when should it be deployed?

### 1.1 Related Work

The technical viability of ammonia as a marine fuel has been established through multiple review papers and techno-economic assessments. Al-Enazi et al. [1] provided a comprehensive comparison of alternative marine fuels, identifying ammonia's advantages (zero-carbon combustion, existing transport infrastructure at -33 C) and disadvantages (toxicity, lower energy density than LNG). Imhoff et al. [2] quantified ammonia engine performance through thermodynamic simulation, establishing specific fuel oil consumption (SFOC) values that feed into operational cost estimates. Kim et al. [3] evaluated the economics of ammonia-fueled propulsion for individual vessels, finding cost premiums of 1.5--2.5x over conventional fuels depending on ammonia price assumptions. Korberg et al. [4] synthesized techno-economic parameters, and Wang and Wright [10] compared bunkering infrastructure requirements across fuel types qualitatively. All five studies treat the bunkering supply chain as a fixed assumption -- ammonia is available at a given price and location -- without asking how the ammonia reaches the vessel, what infrastructure is required to deliver it, or how that infrastructure should be sized.

At the strategic level, the green corridor concept has gained institutional support through the Getting to Zero Coalition [6], which identified Busan as a candidate port for a Korea--Australia ammonia shipping corridor. Lloyd's Register and UMAS [7] estimated fuel transition costs at a macro level, Xing et al. [5] mapped decarbonization pathways through 2050, and Verschuur et al. [37] quantified the socio-economic and environmental impacts of green corridor infrastructure investments. The Korean government's 2023 National Action Plan ("Toward Green Shipping by 2050") establishes policy targets, and the IMO's 2023 revised GHG strategy [30] sets binding emission reduction milestones that create the demand trajectory underlying our model. However, these documents set targets (number of zero-emission vessels, percentage of green fuel) without providing decision-makers with quantitative tools to determine how many shuttle vessels to procure, what capacity those vessels should have, or when to expand the fleet.

The most directly relevant operational study is Yang and Lam [11], who developed a discrete event simulation (DES) model for ammonia bunkering supply chains at port. Their model evaluates how the number and capacity of ammonia bunker supply vessels, bunkering flow rate, and demand level affect operational and economic performance. Key findings include: flow rate has up to 51.3% impact on bunkering service time (when varied by +/-50%), and the number of bunker supply vessels is the most sensitive parameter for annual operational cost (up to 15.2% effect). Their DES model evaluates predefined configurations through simulation runs -- it answers "what happens if we deploy N vessels of size S?" but does not identify the optimal N and S. Furthermore, their model uses static demand (a fixed number of vessels requiring bunkering), whereas operational planning requires modeling demand as a trajectory over time. They also analyze a single supply chain configuration rather than comparing port-based storage versus remote supply alternatives.

A complementary body of work has emerged on ammonia bunkering safety. Fan et al. [18] developed the first Bayesian network-based quantitative risk assessment for ammonia ship-to-ship bunkering, finding that toxicity poses greater risk than flammability. Yang and Lam [19] extended this to multi-scale release analysis, and Kim et al. [20] integrated STPA with Bayesian networks for port-level ammonia bunkering risk. Qu et al. [35] proposed a comprehensive QRA framework for ammonia storage and bunkering at ports. Khan et al. [36] provided a comprehensive review of ammonia bunkering in the maritime sector, cataloguing technological, operational, and regulatory challenges and confirming that no existing study has jointly optimized bunkering fleet size, shuttle vessel capacity, and pump flow rate. Wang et al. [38] formulated an optimization model for ammonia bunkering network configurations -- the first mathematical programming approach applied to ammonia bunkering -- but in a single-period setting without pump rate as a decision variable. Trivyza et al. [21] designed ammonia-based green corridor networks at the global level, Fullonton et al. [22] surveyed adoption barriers across the fuel supply chain, and Dahlke-Wallat et al. [39] performed a techno-economic evaluation of ammonia bunkering infrastructure concepts.

Mixed-integer linear programming for fleet sizing is a well-established methodology in maritime operations research. Fagerholt [8] demonstrated MILP-based fleet scheduling decision support systems, and Christiansen et al. [9] surveyed ship routing and scheduling, with Fagerholt et al. [23] updating this survey through 2023 covering over 50 maritime inventory routing papers. Zhao et al. [17] jointly optimized heterogeneous fleet deployment, sailing speed, and fuel bunkering for green container shipping. In adjacent domains, Stalahane et al. [13] applied stochastic programming to vessel fleet sizing for offshore wind farm maintenance, Vieira et al. [33] extended this to offshore supply vessel fleet composition with periodic routing, and Bakkehaug et al. [14] addressed multi-period bulk ship fleet renewal under demand uncertainty, demonstrating that dynamic fleet expansion outperforms static sizing. Pantuso et al. [25] showed that fleet renewal decisions under uncertainty benefit from stochastic formulations, Wang et al. [24] incorporated chartering flexibility into fleet composition, and Tan et al. [26] extended fleet sizing to include chartered vessels under demand uncertainty, finding that charter flexibility reduces expected cost by 8--12%. Rodrigues et al. [34] compared uncertainty modeling techniques for maritime inventory routing but focused on inventory feasibility rather than infrastructure investment.

For LNG bunkering specifically, the Turkey study [12] formulated a MILP for ship-to-ship LNG bunkering supply chains, determining the number and size of LNG bunker barges under multiple demand scenarios. Jokinen et al. [42] formulated an early MILP for small-scale LNG supply chain optimization along a coastline. Pratama et al. [40] developed a multi-period MILP for LNG bunkering vessel fleet sizing and scheduling -- the closest methodological analog to our work. Park and Park [27] used integer linear programming to determine optimal bunkering methods at a single port, He et al. [28] optimized route, speed, and bunkering decisions for LNG-fueled tramp ships, Ntakolia et al. [29] applied Monte Carlo simulation to LNG refuelling station design, and Machfudiyanto et al. [41] conducted a feasibility study of LNG bunkering infrastructure. However, all these models address LNG (cryogenic at -162 C) rather than ammonia (-33 C or pressurized), and none includes pump flow rate as a decision variable or models the flow-rate-dependent cycle time that defines ammonia bunkering system performance.

At the supply chain level, Galan-Martin et al. [15] formulated a MILP to optimize green ammonia distribution for intercontinental energy transport, and Kim et al. [16] performed a techno-economic analysis of ammonia ocean transport. Wang et al. [43] applied stochastic optimization to ammonia supply chain design under uncertainty. IRENA [31] projects green ammonia costs declining to $310--$610/ton by 2050, and the Oxford Institute for Energy Studies [32] finds that production contributes over 79% of total delivered ammonia cost. These supply chain models and cost projections operate at spatial scales (intercontinental routes, national networks) that do not address the port-level question: given that ammonia will arrive at or near a bunkering port, how should the last-mile infrastructure be configured?

### 1.2 Research Gaps and Contributions

A review of 43 papers reveals three gaps that no existing study addresses. First, no study jointly optimizes the three coupled decision variables that define an ammonia bunkering system -- shuttle vessel capacity, bunkering pump flow rate, and fleet size over time. The coupling is non-trivial: shuttle size determines pumping time ($V_s / Q_p$), pumping time determines cycle time, and cycle time determines fleet capacity. Wang et al. [38] optimize ammonia bunkering configurations but in a single-period setting without pump rate, and even the most advanced fleet sizing models [24, 25, 26, 40] treat cargo transfer as instantaneous, ignoring flow-rate-dependent cycle time. Second, no quantitative comparison exists between port-based ammonia storage (small shuttles, multiple trips within port) and remote supply (large shuttles, long-haul from production facilities) under identical demand assumptions, nor has a break-even distance been identified. Park and Park [27] compare bunkering modes for LNG at a single port but do not compare supply chain configurations with distance parameterization. Third, no model optimizes the timing of ammonia bunkering fleet expansion synchronized with demand growth trajectories, despite fleet renewal models existing for conventional shipping [14, 25], oil shipping [26], and LNG bunkering [12, 40, 42].

This paper addresses all three gaps through a MILP model that jointly optimizes shuttle vessel sizing (500--50,000 m$^3$), pump capacity (100--1,500 m$^3$/h), and year-by-year fleet expansion over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port: port-based storage (Case 1), remote supply from Yeosu at 86 nm (Case 2-1), and remote supply from Ulsan at 59 nm (Case 2-2). Our approach enumerates all feasible shuttle-pump combinations and solves the fleet-sizing MILP for each, yielding a complete cost landscape rather than a single optimal point. Our four contributions are:

First, we identify distinct optimal infrastructure specifications through systematic parametric evaluation across all feasible shuttle-pump combinations: Case 1 selects a 2,500 m$^3$ shuttle at NPC $410.34M ($1.74/ton LCOA), while Cases 2-1 and 2-2 both select 5,000 m$^3$ shuttles at 2.0--2.5$\times$ higher cost.

Second, we establish a break-even distance decision rule: remote supply becomes cheaper than port storage below approximately 84 nm (at 10,000 m$^3$ shuttle scale), providing port planners a transferable threshold for the build-vs-source decision.

Third, we demonstrate that optimal shuttle specifications are invariant to a 4$\times$ demand range (250 to 1,000 end-vessels), with LCOA varying only 4.0% ($1.72--$1.79/ton for Case 1), enabling early commitment to vessel procurement.

Fourth, the sensitivity analysis reveals a differentiated cost driver hierarchy: CAPEX scaling dominates port-based storage sensitivity (67.9% NPC swing), while bunker volume dominates remote supply sensitivity, informing risk management strategies for each configuration.

The remainder of the paper is organized as follows. Section 2 presents the MILP formulation, cycle time model, and cost structure. Section 3 reports optimization results, temporal dynamics, cost decomposition, and seven sensitivity analyses including discount rate sensitivity. Section 4 discusses the break-even distance rule, result robustness, cross-model comparison with published DES results, practical implications, and limitations. Section 5 concludes.

---

## 2. Methodology

## 2.1 Problem Description and Assumptions

We consider a port authority planning ammonia bunkering infrastructure for a green shipping corridor over a 21-year horizon (2030--2050). The number of ammonia-fueled vessels calling at the port grows linearly from $V_{\text{start}} = 50$ (2030) to $V_{\text{end}} = 500$ (2050), with each vessel requiring $v_{\text{call}} = 5{,}000$ m$^3$ of liquid ammonia per bunkering call at a frequency of $f_{\text{voy}} = 12$ calls per year. The terminal count of 500 vessels represents approximately 4.5% of Busan Port's current annual container vessel calls (~11,000 per year), consistent with moderate ammonia adoption projections.

The decision-maker must determine: (1) the shuttle vessel capacity $V_s$ from a discrete set of available sizes, (2) the bunkering pump flow rate $Q_p$ (m$^3$/h), and (3) the number of new shuttle vessels $x_t$ to add in each year $t \in \{2030, \ldots, 2050\}$, such that the Net Present Cost (NPC) over the 21-year planning horizon is minimized while meeting all demand and operational constraints. The planning horizon spans 21 calendar years (2030 through 2050 inclusive).

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

**A1. Linear demand growth.** The number of ammonia-fueled vessels increases linearly from 50 to 500 over 21 years. Actual adoption may follow an S-curve with slower early growth and potential acceleration post-2040. Under S-curve demand, early-year fleet oversizing would persist longer, increasing capital lock-up by an estimated 8--12% but reducing late-period capacity risk. We test robustness via four demand scenarios (Section 3.8).

**A2. No discounting ($\delta = 0$).** All annual costs are weighted equally; NPC is the undiscounted sum of nominal costs. This simplification avoids assumptions about the cost of capital for public infrastructure and treats the 21-year total as a budget planning figure rather than a financial valuation. A positive discount rate (e.g., 8%) would favor early investment and reduce the present value of distant-year fleet additions.

**A3. Fixed fuel price ($P_f = 600$ USD/ton).** Green ammonia price is held constant. Price volatility disproportionately affects Case 2 configurations where variable OPEX (fuel) constitutes 33--39% of NPC, compared to 19% for Case 1. Section 3.7 presents fuel price sensitivity across $300--$1,200/ton.

**A4. Deterministic vessel scheduling.** Vessels arrive uniformly throughout the year; no queuing or congestion effects are modeled. This underestimates fleet needs during peak periods. The daily peak factor ($F_{\text{peak}} = 1.5$) partially compensates but does not replace a queuing model. Note: $F_{\text{peak}}$ is a design reference parameter; in the current MILP formulation, fleet sizing is governed by the annual working-time constraint (Eq. 12) rather than a daily peak constraint. Explicit peak-period modeling is deferred to Future Work F2.

**A5. Fixed bunker volume per call ($v_{\text{call}} = 5{,}000$ m$^3$).** All vessels require identical fuel quantities per call. In practice, vessel sizes vary; the fixed-volume assumption produces a conservative fleet sizing (larger vessels would require more, smaller vessels less). Section 3.7 tests bunker volume sensitivity from 2,500 to 10,000 m$^3$.

**A6. Size-dependent SFOC.** Specific fuel oil consumption depends on shuttle size through an engine type classification (4-stroke high-speed for DWT < 3,000 ton: 505 g/kWh; 4-stroke medium-speed for DWT 3,000--8,000: 436 g/kWh; medium 2-stroke for DWT 8,000--15,000: 413 g/kWh). Within each class, SFOC is constant regardless of operating conditions. The tornado analysis (Section 3.7) shows moderate SFOC sensitivity, consistent with fuel costs representing 18.9% of Case 1 NPC.

---

## 2.2 Cycle Time Model

The cycle time $T_{\text{cycle}}$ determines how many bunkering operations a single shuttle can complete per year, and thus how many shuttles are required. The cycle time formulation differs between Case 1 and Case 2.

### 2.2.1 Case 1: Port-Based Storage

In Case 1, the shuttle loads ammonia from a shore-side storage terminal, transits within the port to the receiving vessel, transfers fuel, and returns.

$$T_{\text{cycle}}^{(1)} = T_{\text{shore}} + \tau_{\text{out}} + \sigma_{\text{connect}} + T_{\text{pump}}^{(1)} + \sigma_{\text{disconnect}} + \tau_{\text{return}}$$
(1)

where:
- $T_{\text{shore}} = V_s / Q_{\text{shore}} + t_{\text{fixed}}$ is the shore loading time (2)
- $Q_{\text{shore}} = 700$ m$^3$/h is the shore pump rate
- $t_{\text{fixed}} = 4.0$ h is the fixed loading setup/shutdown time (including inbound and outbound maneuvering at the shore terminal)
- $\tau_{\text{out}} = \tau_{\text{return}} = \tau = 1.0$ h is the one-way transit time
- $\sigma_{\text{connect}} = \sigma_{\text{disconnect}} = 2.0$ h each; connection includes hose attachment plus pressure testing, disconnection includes purging plus hose detachment
- $T_{\text{pump}}^{(1)} = V_s / Q_p$ is the pumping time to empty the shuttle into the vessel (3)
- $Q_p$ is the bunkering pump flow rate (m$^3$/h)

**Number of trips per bunkering call:**

$$n_{\text{trip}} = \lceil v_{\text{call}} / V_s \rceil$$
(4)

For $V_s = 2{,}500$ m$^3$ and $v_{\text{call}} = 5{,}000$ m$^3$: $n_{\text{trip}} = 2$.

**Example calculation (Case 1, $V_s = 2{,}500$ m$^3$, $Q_p = 1{,}000$ m$^3$/h):**
- $T_{\text{shore}} = 2{,}500/700 + 4.0 = 7.57$ h
- $T_{\text{pump}}^{(1)} = 2{,}500/1{,}000 = 2.5$ h
- $T_{\text{cycle}}^{(1)} = 7.57 + 1.0 + 2.0 + 2.5 + 2.0 + 1.0 = 16.07$ h

The total time per bunkering call is $n_{\text{trip}} \times T_{\text{cycle}}^{(1)}$.

### 2.2.2 Case 2: Remote Supply

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

This reflects that each shuttle trip serves $N_v$ vessels; thus each vessel requires only a fraction of a trip. In other words, if a shuttle carries enough ammonia for $N_v$ vessels per trip, then a single vessel's bunkering call consumes $1/N_v$ of that trip's resources (shuttle time and fuel). This fractional allocation ensures the working-time constraint (Eq. 12) correctly accounts for shared shuttle capacity.

**Example calculation (Case 2-1, $V_s = 5{,}000$ m$^3$, $Q_p = 1{,}000$ m$^3$/h):**
- $N_v = \lfloor 5{,}000 / 5{,}000 \rfloor = 1$ vessel per trip
- $T_{\text{shore}} = 5{,}000/700 + 4.0 = 11.14$ h
- $T_{\text{pump},j}^{(2)} = 5{,}000/1{,}000 = 5.0$ h per vessel
- $T_{\text{cycle}}^{(2)} = 11.14 + 5.73 + 1.0 + 1 \times (1.0 + 2 \times 2.0 + 5.0) + 1.0 + 5.73 = 34.60$ h

---

## 2.3 MILP Formulation

### 2.3.1 Notation

**Table 2: Sets, parameters, and decision variables**

| Symbol | Definition | Unit | Value |
|--------|-----------|------|-------|
| **Sets** | | | |
| $\mathcal{T}$ | Planning years | -- | $\{2030, 2031, \ldots, 2050\}$ |
| **Parameters** | | | |
| $V_s$ | Shuttle vessel capacity | m$^3$ | Case-dependent (Table 1) |
| $Q_p$ | Bunkering pump flow rate | m$^3$/h | 1,000 (base); 100--1,500 (sensitivity) |
| $T_{\text{cycle}}$ | Cycle duration (from Section 2.2) | hours | Case- and config-dependent |
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

### 2.3.2 Objective Function

The objective minimizes the total 21-year Net Present Cost:

$$\min \text{NPC} = \sum_{t \in \mathcal{T}} \left[ C_t^{\text{ann}} + C_t^{\text{fOPEX}} + C_t^{\text{vOPEX}} \right]$$
(9)

where $C_t^{\text{ann}}$ is the annualized CAPEX, $C_t^{\text{fOPEX}}$ is the fixed OPEX, and $C_t^{\text{vOPEX}}$ is the variable OPEX in year $t$. No discounting is applied ($\delta = 0$; Assumption A2).

### 2.3.3 Constraints

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

where $S_{\text{tank}} = 35{,}000$ tons is the individual tank capacity and $\beta = 2.0$ is the safety factor. This constraint ensures the shore storage facility can buffer the simultaneous inventory of all active shuttles. The safety factor ($\beta = 2.0$) accounts for the possibility of multiple shuttles loading concurrently at the shore terminal, requiring storage capacity equal to twice the fleet's total shuttle volume.

**Non-negativity and integrality:**

$$x_t \geq 0, \quad x_t \in \mathbb{Z}, \quad \forall t \in \mathcal{T}$$
(14)

---

## 2.4 Cost Model

### 2.4.1 Shuttle CAPEX (Scaling Law)

Shuttle vessel capital cost follows a power-law scaling relationship:

$$C_{\text{shuttle}}(V_s) = C_{\text{ref}} \times \left(\frac{V_s}{V_{\text{ref}}}\right)^{\alpha}$$
(15)

where $C_{\text{ref}} = 61.5$ M USD is the reference cost for a $V_{\text{ref}} = 40{,}000$ m$^3$ vessel, and $\alpha = 0.75$ is the scaling exponent. This six-tenths rule variant (with $\alpha = 0.75$) reflects that larger vessels benefit from economies of scale in hull, propulsion, and cargo systems, but with diminishing savings beyond a threshold.

**Example:** A 2,500 m$^3$ shuttle costs $C_{\text{shuttle}} = 61.5 \times (2{,}500/40{,}000)^{0.75} = 61.5 \times 0.1250 = 7.69$ M USD.

### 2.4.2 Bunkering Equipment CAPEX

$$C_{\text{equip}} = C_{\text{shuttle}} \times r_{\text{equip}} + C_{\text{pump}}$$
(16)

where $r_{\text{equip}} = 0.03$ (equipment ratio) and:

$$C_{\text{pump}} = P_{\text{pump}} \times c_{\text{kW}}, \quad P_{\text{pump}} = \frac{Q_p \times \Delta p \times 10^5}{3.6 \times 10^6 \times \eta_p}$$
(17)

with $\Delta p = 4.0$ bar, $\eta_p = 0.70$, and $c_{\text{kW}} = 2{,}000$ USD/kW. The numerator converts pressure from bar to Pa ($\times 10^5$) and the denominator converts flow rate from m$^3$/h to m$^3$/s ($\times 3{,}600$) and power from W to kW ($\times 1{,}000$). At $Q_p = 1{,}000$ m$^3$/h: $P_{\text{pump}} = 1{,}000 \times 4.0 \times 10^5 / (3.6 \times 10^6 \times 0.70) = 158.7$ kW, giving $C_{\text{pump}} = 158.7 \times 2{,}000 = 317{,}460$ USD.

### 2.4.3 Tank Storage CAPEX (Case 1 only)

$$C_{\text{tank}} = S_{\text{tank}} \times 10^3 \times c_{\text{kg}}$$
(18)

where $c_{\text{kg}} = 1.215$ USD/kg.

### 2.4.4 Annualization

All capital costs are converted to equivalent annual payments using the annuity factor:

$$\text{AF} = \frac{1 - (1 + r)^{-n}}{r}$$
(19)

where $r = 0.07$ (annualization interest rate) and $n = 21$ years, giving $\text{AF} = 10.8355$.

$$C_t^{\text{ann}} = \frac{\sum_{\tau=2030}^{t} x_\tau \times C_{\text{shuttle}}(V_s) + \text{[equipment + tank costs]}}{\text{AF}}$$
(20)

Note that $r$ is an annualization rate for converting lump-sum CAPEX to equivalent annual payments; it is distinct from the discount rate ($\delta = 0$).

### 2.4.5 Fixed OPEX

$$C_t^{\text{fOPEX}} = N_t \times (C_{\text{shuttle}} \times r_{\text{fOPEX}}^{s} + C_{\text{equip}} \times r_{\text{fOPEX}}^{b}) + N_t^{\text{tank}} \times C_{\text{tank}} \times r_{\text{fOPEX}}^{k}$$
(21)

where $r_{\text{fOPEX}}^{s} = 0.05$ (shuttle), $r_{\text{fOPEX}}^{b} = 0.05$ (bunkering), $r_{\text{fOPEX}}^{k} = 0.03$ (tank).

### 2.4.6 Variable OPEX

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

### 2.4.7 Levelized Cost of Ammonia

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

## 2.5 Solution Approach

The MILP is solved using the CBC (Coin-or Branch and Cut) solver via the PuLP optimization library in Python. For each supply chain configuration, we solve the MILP for every combination of shuttle size $V_s$ (10--12 discrete values) and pump rate $Q_p$ (1,000 m$^3$/h baseline), producing a complete NPC surface.

The globally optimal solution is the $(V_s, Q_p)$ combination yielding the minimum NPC. Because the shuttle-pump grid is enumerated exhaustively, the optimality is global over the discrete candidate set.

The optimization follows a two-level approach. At the outer level, all feasible combinations of shuttle capacity ($V_s$) and pump flow rate ($Q_p$) are enumerated. At the inner level, for each ($V_s$, $Q_p$) pair, the multi-period MILP determines the optimal fleet deployment schedule over the 21-year planning horizon, minimizing total NPC subject to demand satisfaction and operational constraints. The optimal infrastructure specification is then selected as the ($V_s$, $Q_p$) combination yielding the lowest NPC across all evaluated pairs.

This parametric evaluation approach, while computationally straightforward, offers two practical advantages: (1) it provides decision-makers with a complete cost landscape across all feasible specifications rather than a single optimal point, and (2) it enables direct comparison of heterogeneous supply configurations (port-based storage vs. remote supply) under identical assumptions. The computational cost remains manageable (< 30 seconds per case on a standard workstation), given the modest problem size (10--12 shuttle sizes $\times$ 1 pump rate $\times$ 21 years).

### 2.5.1 Sensitivity Analysis Design

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
