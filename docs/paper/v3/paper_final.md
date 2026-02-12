# Optimal Ammonia Bunkering Infrastructure for Green Shipping Corridors: A Multi-Period Mixed-Integer Linear Programming Approach

---

## Abstract

Ammonia is a leading zero-carbon marine fuel candidate, yet no quantitative framework exists for sizing the port-level bunkering infrastructure -- shuttle vessels, pumps, and storage -- required to deliver it from production facilities to ship fuel tanks. We formulate a mixed-integer linear programming (MILP) model that systematically evaluates all feasible shuttle-pump combinations and optimizes fleet deployment for each configuration over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port: port-based storage (Case 1), remote supply from Yeosu at 86 nm (Case 3), and remote supply from Ulsan at 59 nm (Case 2). Demand grows linearly from 50 to 500 ammonia-fueled vessels at 12 voyages per year. The model identifies distinct optimal configurations: Case 1 selects a 2,500 m3 shuttle at a 21-year net present cost (NPC) of \$410.34M and levelized cost of ammonia bunkering (LCOA) of \$1.74/ton, while Cases 2 and 3 require larger shuttles (5,000 and 5,000 m3) at 2.0--2.5 times higher cost. A parametric break-even analysis establishes that remote supply becomes cheaper than port storage below approximately 84 nm one-way distance at the 10,000 m3 shuttle scale. Sensitivity analysis across four demand scenarios (250--1,000 end-vessels) demonstrates that optimal shuttle specifications are invariant, with LCOA varying only 4.0%. These results provide port authorities with quantitative decision tools for ammonia bunkering infrastructure investment in green shipping corridors.

**Keywords:** ammonia bunkering; green shipping corridor; mixed-integer linear programming; fleet sizing; levelized cost; infrastructure optimization

---

## 1. Introduction

The International Maritime Organization (IMO) has adopted a revised GHG strategy targeting at least 30% emission reduction by 2030, 80% by 2040, and net-zero by or around 2050 relative to 2008 levels [5, 29]. Achieving these targets requires a transition from conventional marine fuels to zero-carbon alternatives. Among the candidates, ammonia (NH$_3$) has emerged as a leading option due to its zero-carbon combustion, existing global production infrastructure (~180 million tons/year), and compatibility with established bulk liquid transport methods [1, 2]. Green ammonia production costs are projected to decline from \$720--\$1,400/ton (2022) to \$310--\$610/ton by 2050 [31], making it increasingly competitive as a marine fuel. As of December 2025, 144 ammonia-fueled vessels and 302 ammonia-ready vessels have been ordered, signaling that the demand side of the ammonia fuel transition is materializing. The supply side -- specifically, the port-level infrastructure required to deliver ammonia from production facilities to vessel fuel tanks -- remains unresolved.

Green shipping corridor initiatives aim to bridge this gap by establishing end-to-end infrastructure for zero-emission vessel operations along specific trade routes. The Korea--United States green corridor agreement (formalized April 2025) targets ammonia-fueled container ship operations between Busan and Seattle-Tacoma by 2027, with the Korean government investing approximately \$10 billion in Busan mega-port infrastructure including alternative fuel bunkering facilities [6]. Similar corridors are planned between Korea and Australia. These initiatives specify the fuel (ammonia) and the endpoints (ports) but leave a fundamental operational question unanswered: what bunkering infrastructure -- shuttle vessels, pumps, and storage facilities -- is required, at what scale, and when should it be deployed?

### 1.1 Related Work

The technical viability of ammonia as a marine fuel has been established through multiple review papers and techno-economic assessments. Al-Enazi et al. [1] provided a comprehensive comparison of alternative marine fuels, identifying ammonia's advantages (zero-carbon combustion, existing transport infrastructure at -33 C) and disadvantages (toxicity, lower energy density than LNG). Imhoff et al. [2] quantified ammonia engine performance through thermodynamic simulation, establishing specific fuel oil consumption (SFOC) values that feed into operational cost estimates. Kim et al. [3] evaluated the economics of ammonia-fueled propulsion for individual vessels, finding cost premiums of 1.5--2.5x over conventional fuels depending on ammonia price assumptions. Korberg et al. [4] synthesized techno-economic parameters, and Wang and Wright [10] compared bunkering infrastructure requirements across fuel types qualitatively. All five studies treat the bunkering supply chain as a fixed assumption -- ammonia is available at a given price and location -- without asking how the ammonia reaches the vessel, what infrastructure is required to deliver it, or how that infrastructure should be sized.

At the strategic level, the green corridor concept has gained institutional support through the Getting to Zero Coalition [6], which identified Busan as a candidate port for a Korea--Australia ammonia shipping corridor. Lloyd's Register and UMAS [7] estimated fuel transition costs at a macro level, Xing et al. [5] mapped decarbonization pathways through 2050, and Verschuur et al. [37] quantified the socio-economic and environmental impacts of green corridor infrastructure investments. The Korean government's 2023 National Action Plan ("Toward Green Shipping by 2050") establishes policy targets, and the IMO's 2023 revised GHG strategy [30] sets binding emission reduction milestones that create the demand trajectory underlying our model. However, these documents set targets (number of zero-emission vessels, percentage of green fuel) without providing decision-makers with quantitative tools to determine how many shuttle vessels to procure, what capacity those vessels should have, or when to expand the fleet.

The most directly relevant operational study is Yang and Lam [11], who developed a discrete event simulation (DES) model for ammonia bunkering supply chains at port. Their model evaluates how the number and capacity of ammonia bunker supply vessels, bunkering flow rate, and demand level affect operational and economic performance. Key findings include: flow rate has up to 51.3% impact on bunkering service time (when varied by +/-50%), and the number of bunker supply vessels is the most sensitive parameter for annual operational cost (up to 15.2% effect). Their DES model evaluates predefined configurations through simulation runs -- it answers "what happens if we deploy N vessels of size S?" but does not identify the optimal N and S. Furthermore, their model uses static demand (a fixed number of vessels requiring bunkering), whereas operational planning requires modeling demand as a trajectory over time. They also analyze a single supply chain configuration rather than comparing port-based storage versus remote supply alternatives.

A complementary body of work has emerged on ammonia bunkering safety. Fan et al. [18] developed the first Bayesian network-based quantitative risk assessment for ammonia ship-to-ship bunkering, finding that toxicity poses greater risk than flammability. Yang and Lam [19] extended this to multi-scale release analysis, and Kim et al. [20] integrated STPA with Bayesian networks for port-level ammonia bunkering risk. Qu et al. [35] proposed a comprehensive QRA framework for ammonia storage and bunkering at ports. Khan et al. [36] provided a comprehensive review of ammonia bunkering in the maritime sector, cataloguing technological, operational, and regulatory challenges and confirming that no existing study has jointly optimized bunkering fleet size, shuttle vessel capacity, and pump flow rate. Wang et al. [38] formulated an optimization model for ammonia bunkering network configurations -- the first mathematical programming approach applied to ammonia bunkering -- but in a single-period setting without pump rate as a decision variable. Trivyza et al. [21] designed ammonia-based green corridor networks at the global level, Fullonton et al. [22] surveyed adoption barriers across the fuel supply chain, and Dahlke-Wallat et al. [39] performed a techno-economic evaluation of ammonia bunkering infrastructure concepts.

Mixed-integer linear programming for fleet sizing is a well-established methodology in maritime operations research. Fagerholt [8] demonstrated MILP-based fleet scheduling decision support systems, and Christiansen et al. [9] surveyed ship routing and scheduling, with Fagerholt et al. [23] updating this survey through 2023 covering over 50 maritime inventory routing papers. Zhao et al. [17] jointly optimized heterogeneous fleet deployment, sailing speed, and fuel bunkering for green container shipping. In adjacent domains, Stalahane et al. [13] applied stochastic programming to vessel fleet sizing for offshore wind farm maintenance, Vieira et al. [33] extended this to offshore supply vessel fleet composition with periodic routing, and Bakkehaug et al. [14] addressed multi-period bulk ship fleet renewal under demand uncertainty, demonstrating that dynamic fleet expansion outperforms static sizing. Pantuso et al. [25] showed that fleet renewal decisions under uncertainty benefit from stochastic formulations, Wang et al. [24] incorporated chartering flexibility into fleet composition, and Tan et al. [26] extended fleet sizing to include chartered vessels under demand uncertainty, finding that charter flexibility reduces expected cost by 8--12%. Rodrigues et al. [34] compared uncertainty modeling techniques for maritime inventory routing but focused on inventory feasibility rather than infrastructure investment.

For LNG bunkering specifically, the Turkey study [12] formulated a MILP for ship-to-ship LNG bunkering supply chains, determining the number and size of LNG bunker barges under multiple demand scenarios. Jokinen et al. [42] formulated an early MILP for small-scale LNG supply chain optimization along a coastline. Pratama et al. [40] developed a multi-period MILP for LNG bunkering vessel fleet sizing and scheduling -- the closest methodological analog to our work. Park and Park [27] used integer linear programming to determine optimal bunkering methods at a single port, He et al. [28] optimized route, speed, and bunkering decisions for LNG-fueled tramp ships, Ntakolia et al. [29] applied Monte Carlo simulation to LNG refuelling station design, and Machfudiyanto et al. [41] conducted a feasibility study of LNG bunkering infrastructure. However, all these models address LNG (cryogenic at -162 C) rather than ammonia (-33 C or pressurized), and none includes pump flow rate as a decision variable or models the flow-rate-dependent cycle time that defines ammonia bunkering system performance.

At the supply chain level, Galan-Martin et al. [15] formulated a MILP to optimize green ammonia distribution for intercontinental energy transport, and Kim et al. [16] performed a techno-economic analysis of ammonia ocean transport. Wang et al. [43] applied stochastic optimization to ammonia supply chain design under uncertainty. IRENA [31] projects green ammonia costs declining to \$310--\$610/ton by 2050, and the Oxford Institute for Energy Studies [32] finds that production contributes over 79% of total delivered ammonia cost. These supply chain models and cost projections operate at spatial scales (intercontinental routes, national networks) that do not address the port-level question: given that ammonia will arrive at or near a bunkering port, how should the last-mile infrastructure be configured?

### 1.2 Research Gaps and Contributions

A review of 43 papers reveals three gaps that no existing study addresses. First, no study jointly optimizes the three coupled decision variables that define an ammonia bunkering system -- shuttle vessel capacity, bunkering pump flow rate, and fleet size over time. The coupling is non-trivial: shuttle size determines pumping time ($V_s / Q_p$), pumping time determines cycle time, and cycle time determines fleet capacity. Wang et al. [38] optimize ammonia bunkering configurations but in a single-period setting without pump rate, and even the most advanced fleet sizing models [24, 25, 26, 40] treat cargo transfer as instantaneous, ignoring flow-rate-dependent cycle time. Second, no quantitative comparison exists between port-based ammonia storage (small shuttles, multiple trips within port) and remote supply (large shuttles, long-haul from production facilities) under identical demand assumptions, nor has a break-even distance been identified. Park and Park [27] compare bunkering modes for LNG at a single port but do not compare supply chain configurations with distance parameterization. Third, no model optimizes the timing of ammonia bunkering fleet expansion synchronized with demand growth trajectories, despite fleet renewal models existing for conventional shipping [14, 25], oil shipping [26], and LNG bunkering [12, 40, 42].

This paper addresses all three gaps through a MILP model that jointly optimizes shuttle vessel sizing (500--50,000 m$^3$), pump capacity (100--1,500 m$^3$/h), and year-by-year fleet expansion over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port: port-based storage (Case 1), remote supply from Yeosu at 86 nm (Case 3), and remote supply from Ulsan at 59 nm (Case 2). Our approach enumerates all feasible shuttle-pump combinations and solves the fleet-sizing MILP for each, yielding a complete cost landscape rather than a single optimal point. Our four contributions are:

First, we identify distinct optimal infrastructure specifications through systematic parametric evaluation across all feasible shuttle-pump combinations: Case 1 selects a 2,500 m$^3$ shuttle at NPC \$410.34M (\$1.74/ton LCOA), while Cases 2 and 3 both select 5,000 m$^3$ shuttles at 2.0--2.5$\times$ higher cost.

Second, we establish a break-even distance decision rule: remote supply becomes cheaper than port storage below approximately 84 nm (at 10,000 m$^3$ shuttle scale), providing port planners a transferable threshold for the build-vs-source decision.

Third, we demonstrate that optimal shuttle specifications are invariant to a 4$\times$ demand range (250 to 1,000 end-vessels), with LCOA varying only 4.0% (\$1.72--\$1.79/ton for Case 1), enabling early commitment to vessel procurement.

Fourth, the sensitivity analysis reveals a differentiated cost driver hierarchy: CAPEX scaling dominates port-based storage sensitivity (67.9% NPC swing), while bunker volume dominates remote supply sensitivity, informing risk management strategies for each configuration.

The remainder of the paper is organized as follows. Section 2 presents the MILP formulation, cycle time model, and cost structure. Section 3 reports optimization results, temporal dynamics, cost decomposition, and seven sensitivity analyses including discount rate sensitivity. Section 4 discusses the break-even distance rule, result robustness, cross-model comparison with published DES results, practical implications, and limitations. Section 5 concludes.

---

## 2. Methodology

## 2.1 Problem Description and Assumptions

We consider a port authority planning ammonia bunkering infrastructure for a green shipping corridor over a 21-year horizon (2030--2050). The number of ammonia-fueled vessels calling at the port grows linearly from $V_{\text{start}} = 50$ (2030) to $V_{\text{end}} = 500$ (2050), with each vessel requiring $v_{\text{call}} = 5{,}000$ m$^3$ of liquid ammonia per bunkering call at a frequency of $f_{\text{voy}} = 12$ calls per year. The terminal count of 500 vessels represents approximately 4.5% of Busan Port's current annual container vessel calls (~11,000 per year), consistent with moderate ammonia adoption projections.

The decision-maker must determine: (1) the shuttle vessel capacity $V_s$ from a discrete set of available sizes, (2) the bunkering pump flow rate $Q_p$ (m$^3$/h), and (3) the number of new shuttle vessels $x_t$ to add in each year $t \in \{2030, \ldots, 2050\}$, such that the Net Present Cost (NPC) over the 21-year planning horizon is minimized while meeting all demand and operational constraints. The planning horizon spans 21 calendar years (2030 through 2050 inclusive).

We analyze three supply chain configurations (Fig. 1):

**Table 1: Three supply chain configurations**

| Parameter | Case 1 (Busan) | Case 3 (Yeosu) | Case 2 (Ulsan) |
|-----------|---------------|-------------------|-------------------|
| Source | Busan port storage | Yeosu (86 nm) | Ulsan (59 nm) |
| Storage at Busan | Yes (35,000 ton) | No | No |
| One-way travel time $\tau$ | 1.0 h | 5.73 h | 3.93 h |
| Shuttle sizes $V_s$ | 500--10,000 m$^3$ | 2,500--50,000 m$^3$ | 2,500--50,000 m$^3$ |
| Pumping logic | $V_s / Q_p$ (empty shuttle) | $v_{\text{call}} / Q_p$ (fill vessel) | $v_{\text{call}} / Q_p$ (fill vessel) |

**Key structural difference:** In Case 1, the shuttle carries ammonia from port storage to a vessel; the pumping time depends on shuttle capacity ($V_s / Q_p$). In Cases 2 and 3, the shuttle travels from a remote source and may serve multiple vessels per trip; the pumping time per vessel depends on the bunkering demand per call ($v_{\text{call}} / Q_p$).

### Assumptions

We adopt the following simplifying assumptions, each with justification and impact assessment:

**A1. Linear demand growth.** The number of ammonia-fueled vessels increases linearly from 50 to 500 over 21 years. Actual adoption may follow an S-curve with slower early growth and potential acceleration post-2040. Under S-curve demand, early-year fleet oversizing would persist longer, increasing capital lock-up by an estimated 8--12% but reducing late-period capacity risk. We test robustness via four demand scenarios (Section 3.8).

**A2. No discounting ($\delta = 0$).** All annual costs are weighted equally; NPC is the undiscounted sum of nominal costs. This simplification avoids assumptions about the cost of capital for public infrastructure and treats the 21-year total as a budget planning figure rather than a financial valuation. A positive discount rate (e.g., 8%) would favor early investment and reduce the present value of distant-year fleet additions.

**A3. Fixed fuel price ($P_f = 600$ USD/ton).** Green ammonia price is held constant. Price volatility disproportionately affects Case 2 configurations where variable OPEX (fuel) constitutes 33--39% of NPC, compared to 19% for Case 1. Section 3.7 presents fuel price sensitivity across \$300--\$1,200/ton.

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

In Cases 2 and 3, the shuttle loads at a remote source port, transits to Busan, enters the port, serves one or more vessels sequentially, exits the port, and returns.

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

**Example calculation (Case 3, $V_s = 5{,}000$ m$^3$, $Q_p = 1{,}000$ m$^3$/h):**
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
| Fuel price | $P_f$ | \$300--\$1,200/ton | 9 | All 3 |
| Bunker volume | $v_{\text{call}}$ | 2,500--10,000 m$^3$ | 7 | All 3 |
| Two-way | $P_f \times v_{\text{call}}$ | 5$\times\$5 matrix | 25 | Case 1 |
| Demand scenarios | $V_{\text{end}}$ | 250, 500, 750, 1,000 | 4 | All 3 |
| Break-even distance | $\tau$ | 10--200 nm | 20 | Case 2 vs 1 |

The tornado analysis varies CAPEX scaling exponent, bunker volume, maximum annual hours, travel time, fuel price, and SFOC by +/-20% from baseline, measuring the NPC swing for each parameter while holding others constant.

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

Fig. 2 (D1) shows the NPC as a function of shuttle size for all three cases. Each curve exhibits a piecewise cost landscape shaped by the integer-valued trip count $n_{\text{trip}}$ (Eq. 4), with a global minimum at an interior point. For Case 1, the 500 m$^3$ shuttle is infeasible: a bunkering call requires $n_{\text{trip}} = \lceil 5{,}000/500 \rceil = 10$ trips, yielding a call duration of \$10 \times 11.21 = 112.1$ h, which exceeds the maximum allowable call duration of 80 h. Consequently, the NPC curve for Case 1 begins at 1,000 m$^3$. NPC decreases from \$433.41M at 1,000 m$^3$ to \$410.34M at 2,500 m$^3$ (global minimum), then rises steeply to higher values at intermediate sizes before dropping to \$441.25M at 5,000 m$^3$ where $n_{\text{trip}}$ decreases from 2 to 1. This discontinuity creates a secondary local minimum at 5,000 m$^3$, only 7.5% above the global optimum -- a configuration worth considering if operational simplicity (single trip per call) is valued. The asymmetry arises from two competing effects: undersized shuttles incur cycle-count penalties, while oversized shuttles suffer from CAPEX scaling. The CAPEX scaling exponent ($\alpha = 0.75$) means that doubling shuttle capacity increases unit cost by \$2^{0.75} = 1.68\times$ rather than $2\times$, producing diminishing savings that are eventually overwhelmed by the absolute cost increase.

For Case 3 (Yeosu), the optimal is 5,000 m$^3$ -- the same size as Case 2 (Ulsan). At this shuttle size, $N_v = \lfloor 5{,}000/5{,}000 \rfloor = 1$ vessel is served per trip. Unlike the previous expectation that larger shuttles would be preferred for longer distances to amortize the 5.73-hour one-way travel time over more delivered volume, the 5,000 m$^3$ shuttle proves more efficient because the shore loading time for a 10,000 m$^3$ shuttle (\$10{,}000/1{,}500 + 2.0 = 8.67$ h) substantially increases cycle time, offsetting the travel-cost amortization benefit of serving two vessels per trip. For Case 2 (Ulsan), the 5,000 m$^3$ optimum reflects the shorter travel distance (3.93 h one-way), where the cycle time penalty of larger shuttles is similarly prohibitive.

Fig. 3 (D10) confirms the cross-case cost hierarchy: Case 3 NPC is $2.47\times$ Case 1, and Case 2 is $2.02\times$ Case 1. This ordering holds across all shuttle sizes, indicating that the port-based storage advantage is structural rather than configuration-dependent. The LCOA metric normalizes for total supply volume: at \$1.74/ton (Case 1) versus \$4.31/ton (Case 3), the per-ton cost of remote supply from Yeosu is \$2.57/ton higher, representing a premium of 148%.

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

Case 1 is capital-intensive: shuttle CAPEX (\$205.04M, 49.97%) and shuttle fOPEX (\$111.08M, 27.07%) together account for 77.0% of NPC, while shuttle vOPEX is only 13.4% (\$55.01M). This reflects the short travel distance (1.0 h one-way), which minimizes fuel consumption per cycle.

Cases 2 and 3 are operations-intensive: shuttle vOPEX rises to 39.5% (\$400.97M) and 33.1% (\$275.01M) respectively, driven by the longer round-trip travel times (11.46 h for Yeosu, 7.86 h for Ulsan) and correspondingly higher fuel consumption per cycle. The vOPEX increase from Case 1 to Case 3 is \$345.96M -- representing the cumulative fuel cost of traversing 172 nm (86 nm round trip) per shuttle cycle over 21 years. This structural shift from CAPEX-dominated to vOPEX-dominated cost has practical consequences: Case 1 costs are front-loaded (CAPEX at procurement) and predictable, while Case 2 costs are distributed over the operating life and sensitive to fuel price fluctuations.

---

## 3.5 LCOA Comparison

Fig. 5 (D9) presents LCOA across all cases. Case 1 achieves \$1.74/ton, which represents the minimum unit cost of ammonia delivery from storage to vessel. Case 3 at \$4.31/ton is 148% higher, and Case 2 at \$3.53/ton is 103% higher. These differences persist across all shuttle size configurations, confirming that the cost advantage is structural (driven by travel distance and cycle time) rather than incidental.

The total ammonia supply over the 21-year horizon (2030--2050) is identical across all three cases ($235{,}620{,}000$ tons), because all share the same demand trajectory (50 to 500 vessels, 12 voyages/year, 5,000 m$^3$/call). The annualized cost ranges from \$37.87M/year (Case 1) to \$93.66M/year (Case 3), indicating that the additional annual cost of sourcing from Yeosu rather than local storage is \$55.79M/year.

---

## 3.6 Pump Rate Sensitivity

Fig. 14 (S7) shows how NPC responds to pump rate variation from 100 to 1,500 m$^3$/h. For Case 1, NPC decreases substantially as pump rate increases from the low end of the range, with the relationship exhibiting strong concavity: the marginal benefit of pump rate increases falls rapidly at higher flow rates. At the baseline pump rate of 1,000 m$^3$/h, further pump rate investment yields diminishing returns for all three cases.

The optimal shuttle size remains 2,500 m$^3$ across all pump rates above a threshold for Case 1. At very low pump rates, the optimal shifts to smaller shuttles because the low pump rate creates extremely long cycle times for larger shuttles ($T_{\text{pump}} = 2{,}500/Q_p$ grows rapidly as $Q_p$ decreases), making smaller, faster shuttles more cost-effective despite requiring more trips. This interaction between pump rate and optimal shuttle size demonstrates the coupling identified in Gap 1.

---

## 3.7 Parametric Sensitivity

### Tornado Analysis

Fig. 10 (FIG7) presents tornado diagrams showing the NPC swing from +/-20% variation of six parameters. For Case 1:

**Table 7: Tornado sensitivity ranking (Case 1, base NPC = \$410.34M)**

| Rank | Parameter | Low NPC (USD M) | High NPC (USD M) | Swing (USD M) | Swing (%) |
|:----:|-----------|:---------------:|:-----------------:|:-------------:|:---------:|
| 1 | CAPEX Scaling Exponent | 299.55 | 578.26 | 278.71 | 67.9 |
| 2 | Bunker Volume | 407.01 | 605.24 | 198.23 | 48.3 |
| 3 | Max Annual Hours | 356.43 | 492.37 | 135.94 | 33.1 |
| 4 | Travel Time | 392.31 | 429.55 | 37.24 | 9.1 |
| 5 | Fuel Price | 396.00 | 424.68 | 28.68 | 7.0 |
| 6 | SFOC | 396.00 | 424.68 | 28.68 | 7.0 |

The CAPEX scaling exponent dominates Case 1 sensitivity, with a swing of \$278.71M (67.9% of base NPC). This occurs because $\alpha$ enters the cost function exponentially (Eq. 15): reducing $\alpha$ from 0.75 to 0.60 (i.e., $-20\%$) substantially flattens the CAPEX curve, making larger shuttles cheaper, while increasing to 0.90 steepens it, penalizing all but the smallest sizes. Bunker volume ranks second (\$198.23M, 48.3%) because it directly determines both annual demand and per-call logistics.

SFOC and Fuel Price produce identical swings (\$28.68M, 7.0%) for Case 1 because both scale shuttle fuel costs (Eq. 23) proportionally: a 20% SFOC increase has the same NPC effect as a 20% fuel price increase. The moderate magnitude reflects Case 1's low variable OPEX share (13.4% of NPC, Table 6), which limits the leverage of any fuel-cost parameter. Note that the SFOC sensitivity is evaluated at the optimal shuttle size, where the engine type classification (Table 3) assigns a fixed SFOC value. Because the +/-20% perturbation does not change the shuttle size or its engine class, the SFOC swing reflects only the proportional fuel cost effect without triggering a discrete engine-class transition.

For Case 3 (Yeosu, base NPC = \$1,014.81M), bunker volume becomes the top-ranked parameter with a swing of \$803.83M (75.5%), followed by CAPEX scaling (\$312.37M, 29.4%) and maximum annual hours (\$300.56M, 28.2%). For Case 2 (Ulsan, base NPC = \$830.65M), bunker volume similarly dominates with a swing of \$847.24M (102.0%), followed by CAPEX scaling (\$335.16M, 40.3%) and maximum annual hours (\$217.27M, 26.2%). The shift in sensitivity ranking across cases -- from CAPEX-driven (Case 1) to demand-driven (Case 2) -- mirrors the cost structure shift observed in Section 3.4.

### Fuel Price Sensitivity

Fig. 11 (FIG8) shows NPC and LCOA response to fuel price across \$300--\$1,200/ton. For Case 1, NPC ranges from \$374.50M (\$300/ton, $-8.7\%$) to \$482.02M (\$1,200/ton, $+17.5\%$). The response is linear, consistent with fuel cost being a constant fraction of NPC (vOPEX = 13.4% at baseline). LCOA scales linearly from \$1.59/ton to \$2.05/ton.

Case 2 configurations exhibit steeper fuel price sensitivity, consistent with their higher vOPEX shares (33--40%). At \$1,200/ton, the Case 3 to Case 1 NPC ratio widens further, reinforcing the port-based storage advantage under high fuel price scenarios.

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

**Finding 1: LCOA stability.** Case 1 LCOA ranges from \$1.72 to \$1.79/ton across a 4$\times$ demand variation (250 to 1,000 end-vessels), a variation of only 4.0% (\$0.07/ton). This near-constant marginal cost arises because the MILP scales fleet size proportionally with demand -- doubling demand approximately doubles both total cost and total supply, leaving LCOA unchanged. The slight decline at higher demand (\$1.79 $\to$ \$1.72) reflects economies of scale: fixed components (e.g., bunkering CAPEX per shuttle) are spread over more delivered ammonia.

**Finding 2: Optimal shuttle size invariance.** The optimal shuttle remains 2,500 m$^3$ (Case 1), 5,000 m$^3$ (Case 3), and 5,000 m$^3$ (Case 2) across all four demand scenarios. This invariance -- including Case 3's consistent selection of 5,000 m$^3$ from Low through VeryHigh -- confirms that the optimal shuttle specification is determined by the cycle time structure (shore loading time, transit time, pumping time) rather than by demand volume. Because all three cases maintain their optimal shuttle sizes across a 4$\times$ demand range, the specification decision is fully decoupled from the demand forecast.

The practical implication for port planners is that shuttle vessel specifications can be committed early in the planning process without waiting for demand clarity. The timing of fleet additions (not the specifications) is the demand-sensitive decision. This separation of specification-robustness from scheduling-sensitivity reduces planning risk.

---

### 3.9 Discount Rate Sensitivity

The base case assumes zero discounting (Assumption A2), treating all years equally. To validate this assumption, we test three discount rates: $r$ = 0%, 5%, and 8% across all three cases. Table 9 summarizes the results.

**Table 9: Discount rate sensitivity -- optimal configurations remain invariant**

| Case | $r$ = 0% NPC | $r$ = 5% NPC | $r$ = 8% NPC | Optimal Shuttle | Optimal Pump |
|------|-------------|-------------|-------------|-----------------|--------------|
| Case 1 | \$410.34M | \$226.71M | \$166.42M | 2,500 m$^3$ | 1,000 m$^3$/h |
| Case 3 | \$1,014.81M | \$561.19M | \$412.34M | 5,000 m$^3$ | 1,000 m$^3$/h |
| Case 2 | \$830.65M | \$458.60M | \$336.56M | 5,000 m$^3$ | 1,000 m$^3$/h |

The key finding is that **optimal shuttle specifications are invariant across all discount rates**. While NPC decreases by approximately 59% from $r$ = 0% to $r$ = 8% (because future costs are discounted more heavily), the relative cost ranking across shuttle sizes remains unchanged. Case 1 selects 2,500 m$^3$, and both Case 3 and Case 2 select 5,000 m$^3$ regardless of discounting assumptions.

Empirically, the cost ranking is preserved because the Case 1 advantage stems from lower cycle times and CAPEX, not from temporal cost distribution. Different shuttle sizes produce different fleet expansion schedules, so identical discounting factors cannot be guaranteed theoretically; the invariance is an empirical finding for these specific configurations.

Fig. 15 presents the NPC and LCOA response to discount rate for all three cases. The LCOA follows the same pattern: Case 1 ranges from \$1.74/ton ($r$ = 0%) to \$0.71/ton ($r$ = 8%), while maintaining the cost advantage over Cases 2 and 3 at every discount rate.

Fig. 16 shows fleet evolution under different discount rates. The physical fleet requirement (number of shuttles needed to serve demand) is determined by cycle time and demand volume, not by financial discounting. Consequently, fleet expansion timelines are similar across discount rates, with only minor differences in the timing of discrete fleet additions.

These results validate Assumption A2: while the choice of discount rate affects the reported NPC magnitude, it does not affect the infrastructure specification recommendations or the relative ranking of supply chain configurations. Port authorities can use the zero-discount results as a conservative upper bound on NPC while maintaining confidence in the shuttle sizing recommendations.

---

## 4. Discussion

## 4.1 Local Storage vs Remote Supply: Break-Even Analysis

The results in Section 3.1 establish that port-based storage (Case 1) is cheaper than remote supply at the actual distances of Yeosu (86 nm) and Ulsan (59 nm). However, this comparison is distance-specific. Port planners at other locations face the same build-vs-source decision at different distances. We address this by parameterizing the one-way travel distance from 10 to 200 nm and identifying break-even crossover points.

Fig. 12 (FIG9) presents the break-even distance analysis. For the Yeosu comparison (10,000 m$^3$ shuttle), Case 1 NPC remains constant at \$1,057.15M (independent of remote supply distance, as it uses port-internal shuttles only), while Case 3 NPC increases linearly with distance. The curves cross at approximately 84 nm: below this distance, remote supply at 10,000 m$^3$ scale is cheaper; above it, port-based storage at 10,000 m$^3$ dominates. At 80 nm, Case 3 costs \$1,033.87M (cheaper than Case 1 by \$23.28M); at 90 nm, Case 3 costs \$1,084.24M (more expensive than Case 1 by \$27.09M). At the actual Yeosu distance of 86 nm, Case 1 is marginally cheaper, placing Yeosu very close to the break-even threshold.

For the Ulsan comparison (5,000 m$^3$ shuttle), no crossover occurs within the 10--200 nm range. Case 1 at 5,000 m$^3$ costs \$441.25M, while even at 10 nm, the remote supply configuration costs \$473.16M. This absence of crossover reflects that at the 5,000 m$^3$ shuttle scale, the shuttle serves only $N_v = 1$ vessel per trip, and the per-trip cost structure cannot achieve the travel-cost amortization efficiency that would make remote supply competitive.

The break-even asymmetry has a practical interpretation: remote ammonia supply becomes competitive with port storage only when (a) the shuttle is large enough to serve multiple vessels per trip ($N_v \geq 2$, requiring $V_s \geq 10{,}000$ m$^3$), AND (b) the source is closer than approximately 84 nm. For Busan, where the nearest ammonia sources are Ulsan (59 nm) and Yeosu (86 nm), port-based storage is the cost-minimizing configuration under baseline assumptions, though the Yeosu distance falls very close to the break-even threshold at the 10,000 m$^3$ shuttle scale.

**Optimal-vs-optimal comparison.** The above break-even analysis uses the same shuttle size for both cases, which isolates the effect of distance but does not reflect actual decision-making where each case would use its own optimal shuttle. When Case 1 uses its optimal 2,500 m$^3$ shuttle (\$410.34M) and Case 2 uses its respective optimal size (5,000 m$^3$ for both Ulsan and Yeosu), no break-even crossover occurs within the 10--200 nm range. Even at 10 nm, the cheapest Case 2 option (5,000 m$^3$) costs \$473.16M -- still 15.3% above Case 1's optimal. This happens because port-based storage enables a fundamentally smaller shuttle (2,500 vs 5,000 m$^3$), with correspondingly lower CAPEX. The practical implication is that the 84 nm break-even applies only when comparing the same shuttle size; when each case is free to choose its optimal configuration, port-based storage dominates at all distances for the Busan demand profile.

This decision rule is transferable to other ports: given the one-way distance to the nearest ammonia source and the intended shuttle size, planners can read directly from the break-even curves whether to invest in local storage or rely on remote supply. However, when port storage enables the use of smaller, cheaper shuttles, the build-local option may dominate regardless of distance.

---

## 4.2 Robustness of Infrastructure Decisions

The sensitivity analyses in Sections 3.6--3.8 collectively address the question: how confident can planners be in the optimal specifications?

**Shuttle size specification** is robust across all tested uncertainty dimensions. The Case 1 optimal (2,500 m$^3$) is unchanged by: pump rate variation across the tested range (Section 3.6), fuel price variation from \$300 to \$1,200/ton (Section 3.7), and demand variation from 250 to 1,000 end-vessels (Section 3.8). Only at very low pump rates does the optimal shift to smaller shuttles -- a scenario unlikely in practice given available pump technology.

**LCOA** is remarkably stable: \$1.72--\$1.79/ton across a 4$\times$ demand range (Section 3.8), and \$1.59--\$2.05/ton across a 4$\times$ fuel price range (Section 3.7). The combined uncertainty envelope (demand $\times$ fuel price) produces an LCOA range of approximately \$1.40--\$2.50/ton for Case 1 -- primarily driven by fuel price.

**Fleet expansion timing** is the demand-sensitive component. While the shuttle specification is fixed, the year in which each new shuttle must be procured depends on when cumulative demand crosses the capacity threshold of the existing fleet. Under the High scenario (750 end-vessels), fleet additions occur earlier and more frequently than under Base (500), but the procurement decision remains the same 2,500 m$^3$ vessel. This separation allows port authorities to commit to vessel specifications while maintaining scheduling flexibility.

**Primary risk factor:** The tornado analysis identifies the CAPEX scaling exponent ($\alpha$) as the dominant uncertainty for Case 1 (67.9% NPC swing, Section 3.7). In practical terms, this means that the accuracy of shipyard cost estimates matters more than fuel price forecasts or demand projections. A 20% error in the scaling exponent -- equivalent to using $\alpha = 0.60$ rather than \$0.75$ -- would change the NPC by \$278.71M, dwarfing the impact of fuel price uncertainty (\$28.68M) or travel time variation (\$37.24M). Port authorities should invest in detailed shipyard quotations for ammonia shuttle vessels before committing to fleet procurement.

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

**L2. Fixed fuel price.** The \$600/ton baseline is held constant over 21 years. Green ammonia production costs are projected to decline from \$700--\$1,400/ton (2025) to \$310--\$660/ton (2030--2040) as electrolyzer costs fall. A declining price trajectory would reduce Case 2 vOPEX over time, potentially narrowing the Case 1 vs Case 2 cost gap in later years. Direction: break-even distance may shift by 10--20 nm under declining fuel price scenarios.

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

First, the optimal infrastructure specifications differ across cases due to the interaction between CAPEX scaling and cycle time. Case 1 selects a 2,500 m$^3$ shuttle (NPC \$410.34M, LCOA \$1.74/ton), while Cases 2 and 3 both require 5,000 m$^3$ shuttles at 2.0--2.5 times higher cost.

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

![Fig. 1](../../../results/paper_figures/D7_cycle_time.png)

**Fig. 1.** Cycle time components for three supply chain configurations. The stacked bar chart decomposes each cycle into shore loading, transit, connection/disconnection, and pumping phases. Case 1 (Busan port storage) has the shortest cycle at 16.07 h due to minimal transit time (1.0 h one-way), while Case 3 (Yeosu, 86 nm) requires 34.60 h per cycle with long-haul transit dominating. The visual comparison reveals that transit time, not pumping, is the primary differentiator between port-based and remote supply configurations.

![Fig. 2](../../../results/paper_figures/D1_npc_vs_shuttle.png)

**Fig. 2.** Net present cost as a function of shuttle vessel size for all three cases. Each curve exhibits a piecewise cost landscape shaped by the integer-valued trip count, with discontinuities at shuttle sizes where the number of trips per bunkering call changes. The 500 m$^3$ shuttle is infeasible for Case 1 (call duration exceeds the maximum allowable limit), so the Case 1 curve begins at 1,000 m$^3$. Case 1 achieves its global minimum of \$410.34M at 2,500 m$^3$, with a secondary local minimum at 5,000 m$^3$ (7.5% above optimal). Cases 2 and 3 both show optima at 5,000 m$^3$, reflecting the cycle time penalties associated with larger shuttles due to increased shore loading time.

![Fig. 3](../../../results/paper_figures/D10_case_npc_comparison.png)

**Fig. 3.** NPC comparison across cases at optimal configurations. The bar chart confirms the cross-case cost hierarchy: Case 3 (Yeosu) NPC is 2.47$\times$ Case 1, and Case 2 (Ulsan) is 2.02$\times$ Case 1. This ordering holds across all shuttle sizes evaluated, demonstrating that the port-based storage advantage is structural rather than configuration-dependent.

![Fig. 4](../../../results/paper_figures/D6_cost_breakdown.png)

**Fig. 4.** Cost component breakdown showing six NPC components (shuttle CAPEX, bunkering CAPEX, shuttle fOPEX, shuttle vOPEX, bunkering fOPEX, bunkering vOPEX) at optimal configurations. Case 1 is capital-intensive with shuttle CAPEX and fOPEX accounting for 77.0% of NPC, whereas Cases 2 and 3 shift toward operations-intensive cost structures with shuttle vOPEX rising to 33--40% due to higher fuel consumption on longer routes. This structural shift has practical implications: Case 1 costs are front-loaded and predictable, while Case 2 costs are fuel-price sensitive and distributed over the operating life.

![Fig. 5](../../../results/paper_figures/D9_lco_comparison.png)

**Fig. 5.** Levelized cost of ammonia bunkering (LCOA) across all cases and shuttle sizes. Case 1 achieves \$1.74/ton at the optimal 2,500 m$^3$ shuttle, representing the minimum unit cost of ammonia delivery from storage to vessel. The 148% premium for Case 3 (\$4.31/ton) and 103% premium for Case 2 (\$3.53/ton) persist across all configurations, confirming that the cost advantage is driven by travel distance and cycle time rather than by shuttle selection.

![Fig. 6](../../../results/paper_figures/D2_yearly_cost_evolution.png)

**Fig. 6.** Annual cost evolution from 2030 to 2050 for the optimal configuration of each case. Cost growth exhibits a step function correlated with fleet additions: each new shuttle triggers a jump in annualized CAPEX plus fixed OPEX, followed by gradual vOPEX-driven increases as demand grows between additions. The two distinct growth regimes (CAPEX jumps and vOPEX ramps) are visible for all three cases, with Case 3 showing the steepest vOPEX ramps due to its higher per-cycle fuel consumption.

![Fig. 7](../../../results/paper_figures/D8_fleet_evolution.png)

**Fig. 7.** Cumulative fleet size evolution over the 21-year planning horizon. Fleet growth follows a staircase pattern as demand crosses capacity thresholds defined by the working-time constraint. Case 1 grows from 3 shuttles in 2030 to 25 by 2050, while Cases 2 and 3 require larger fleets to compensate for longer cycle times. The discrete, lumpy nature of fleet investment is clearly visible, with each step representing a procurement decision.

![Fig. 8](../../../results/paper_figures/D3_yearly_fleet_demand.png)

**Fig. 8.** Annual bunkering demand overlaid with fleet supply capacity. The smooth demand curve (linear growth) contrasts with the staircase supply capacity, revealing fleet slack -- periods of overcapacity immediately following each shuttle addition that erode as demand catches up. The narrowing gap between demand and capacity in later years indicates increasing fleet utilization as the horizon progresses.

![Fig. 9](../../../results/paper_figures/D5_yearly_utilization.png)

**Fig. 9.** Fleet utilization rates over time showing a sawtooth pattern. Utilization climbs as demand grows against a fixed fleet (reaching 99% just before additions) and drops when new capacity enters service (to approximately 73%). This pattern confirms just-in-time fleet expansion: the MILP adds shuttles at the minimum necessary rate to prevent the working-time constraint from becoming infeasible, minimizing capital idle time at the cost of limited peak-period buffer.

![Fig. 10](../../../results/paper_figures/Fig7_tornado_deterministic.png)

**Fig. 10.** Tornado diagrams showing NPC sensitivity to +/-20% variation of six parameters for all three cases. For Case 1, the CAPEX scaling exponent dominates with a 67.9% NPC swing (\$278.71M), followed by bunker volume (48.3%) and maximum annual hours (33.1%). For Cases 2 and 3, bunker volume becomes the top-ranked parameter, replacing CAPEX scaling, with swings of 75.5% and 102.0% respectively. This shift in sensitivity ranking mirrors the cost structure transition from CAPEX-dominated (Case 1) to operations-dominated (Case 2).

![Fig. 11](../../../results/paper_figures/Fig8_fuel_price_sensitivity.png)

**Fig. 11.** Fuel price sensitivity showing NPC and LCOA response across \$300--\$1,200/ton for all three cases. The response is linear for all cases, with Case 1 NPC ranging from \$374.50M to \$482.02M and LCOA from \$1.59/ton to \$2.05/ton. Case 2 configurations exhibit steeper slopes consistent with their higher vOPEX shares (33--40% vs 13% for Case 1), and the Case 2-to-Case 1 NPC ratio widens at higher fuel prices, reinforcing the port-based storage advantage under high fuel price scenarios.

![Fig. 12](../../../results/paper_figures/Fig9_breakeven_distance.png)

**Fig. 12.** Break-even distance analysis comparing Case 1 and Case 2 NPC as a function of one-way travel distance (10--200 nm). For the Yeosu comparison (10,000 m$^3$ shuttle), the curves cross at approximately 84 nm, below which remote supply is cheaper. For the Ulsan comparison (5,000 m$^3$ shuttle), no crossover occurs because the smaller shuttle serves only one vessel per trip and cannot achieve sufficient travel-cost amortization. This asymmetry establishes that remote supply competitiveness requires both large shuttles ($N_v \geq 2$) and short distances (< 84 nm).

![Fig. 13](../../../results/paper_figures/Fig10_demand_scenarios.png)

**Fig. 13.** Demand scenario analysis comparing NPC and LCOA across four scenarios (250--1,000 end-vessels) for all three cases. LCOA stability is the central finding: Case 1 LCOA varies by only 4.0% (\$1.72--\$1.79/ton) across a 4$\times$ demand range, because the MILP scales fleet size proportionally with demand. The optimal shuttle size remains invariant (2,500 m$^3$ for Case 1, 5,000 m$^3$ for Cases 2 and 3) across all scenarios, enabling early commitment to vessel specifications regardless of demand uncertainty.

![Fig. 14](../../../results/paper_figures/S7_pump_sensitivity.png)

**Fig. 14.** Pump rate sensitivity showing NPC response to pump flow rate variation from 100 to 1,500 m$^3$/h. The relationship exhibits diminishing returns: the marginal benefit of pump rate increases falls rapidly at higher flow rates. The optimal shuttle size remains 2,500 m$^3$ across pump rates above a threshold for Case 1, demonstrating that the shuttle specification is robust to pump rate uncertainty within the practical range.

**Fig. 15.** Discount rate sensitivity showing NPC and LCOA response across 0%, 5%, and 8% rates for all three cases. While NPC decreases by approximately 59% from 0% to 8% discount rate, the optimal shuttle specifications remain invariant across all discount rates. Case 1 maintains its cost advantage over Cases 2 and 3 at every discount rate, validating that the zero-discount base case produces conservative NPC estimates without affecting infrastructure sizing recommendations.

**Fig. 16.** Fleet evolution under different discount rates (0%, 5%, 8%) for all three cases. Physical fleet requirements are determined by cycle time and demand volume rather than financial discounting, resulting in similar fleet expansion timelines across discount rates with only minor differences in the timing of discrete additions.

![Fig. 17](../../../results/paper_figures/Fig13_yang_lam_service_time.png)

**Fig. 17.** Service time comparison between our deterministic MILP and the DES model of Yang and Lam [11] at three transfer volumes (855, 1,384, and 2,000 tons). The pumping time component is consistent across both models as it derives from the same physical relationship. The gap in total service time is attributable to operational overhead (mooring and documentation) that the DES explicitly models but our MILP subsumes into setup time parameters (2.0 hours per endpoint).

![Fig. 18](../../../results/paper_figures/Fig14_yang_lam_sensitivity.png)

**Fig. 18.** Flow rate sensitivity comparison between deterministic MILP (58.8% NPC impact) and stochastic DES (51.3% service time impact) over a comparable flow rate variation range. The 7.5 percentage-point gap is structural: the DES uses triangular distributions that smooth extreme values through probabilistic averaging, whereas our deterministic formula amplifies the effect at the extremes. This quantifies the extent to which stochastic modeling attenuates parameter sensitivity.

![Fig. S1](../../../results/paper_figures/D12_npc_heatmaps.png)

**Fig. S1.** NPC sensitivity heatmap showing the complete cost landscape across all shuttle size and pump rate combinations for each case. The heatmap reveals the cost valley around the optimal configuration and visualizes the penalty for deviating from it in either dimension, supporting procurement flexibility by showing which near-optimal alternatives exist.

![Fig. S2](../../../results/paper_figures/D11_top_configurations.png)

**Fig. S2.** Top configurations ranked by NPC for each case. The ranking confirms that the optimal configuration has a clear cost advantage over alternatives, with the cost penalty increasing steeply for suboptimal shuttle sizes due to CAPEX scaling effects.

![Fig. S3](../../../results/paper_figures/D4_yearly_cycles.png)

**Fig. S3.** Annual cycle count evolution over the planning horizon. The number of bunkering cycles per shuttle per year increases as demand grows, approaching the theoretical maximum (497.78 for Case 1) just before each fleet addition. This confirms that fleet utilization is driven to the constraint boundary by the MILP.

![Fig. S4](../../../results/paper_figures/FigS4_twoway_deterministic.png)

**Fig. S4.** Two-way sensitivity heatmap showing NPC response to simultaneous variation of fuel price (\$300--\$1,200/ton) and bunker volume (2,500--10,000 m$^3$) for Case 1. The heatmap reveals that bunker volume dominates the interaction: high bunker volume drives NPC up regardless of fuel price, while fuel price has a comparatively uniform effect across volume levels.

![Fig. S5](../../../results/paper_figures/FigS5_bunker_volume_sensitivity.png)

**Fig. S5.** Bunker volume sensitivity showing NPC and LCOA response to bunker volume variation from 2,500 to 10,000 m$^3$ for all three cases. NPC increases approximately linearly with bunker volume for all cases, as larger per-call demands require more shuttle cycles and fleet capacity. The LCOA remains relatively stable because the cost increase is proportional to the volume increase.
