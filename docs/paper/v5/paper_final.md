#!/usr/bin/env markdown
<!-- -*- coding: utf-8 -*- -->

# Optimal Ammonia Bunkering Infrastructure for Green Shipping Corridors: A Multi-Period Mixed-Integer Linear Programming Approach

---

## Abstract

Ammonia is a leading zero-carbon marine fuel candidate, yet no quantitative framework exists for sizing the port-level bunkering infrastructure required to deliver it from supply sources to vessel fuel tanks. This paper formulates a mixed-integer linear programming (MILP) model that evaluates all feasible shuttle vessel and pump rate combinations through systematic parametric enumeration and optimizes fleet deployment for each configuration over a 21-year planning horizon (2030--2050). Three ammonia supply chain configurations at Busan Port are compared: port-based storage with intra-port shuttle distribution (Case 1), remote supply from Ulsan at 59 nautical miles (Case 2), and remote supply from Yeosu at 86 nautical miles (Case 3). Ulsan and Yeosu are selected as supply origins because they host Korea's largest petrochemical and industrial complexes, respectively, with established ammonia import and storage infrastructure. Demand grows linearly from 50 to 500 ammonia-fueled vessels calling at the port, each requiring 5,000 m$^3$ of liquid ammonia per bunkering call at 12 calls per year. The model identifies distinct optimal shuttle sizes for port-based storage versus remote supply configurations, with the port-based option achieving the lowest net present cost (NPC) and levelized cost of ammonia bunkering (LCOA) among all three cases. A parametric break-even distance analysis across 10--200 nautical miles demonstrates that port-based storage dominates remote supply at all tested distances when each configuration uses its respective optimal shuttle size. Sensitivity analysis spanning four demand scenarios, six tornado parameters, fuel price variation, bunker volume variation, and discount rate variation confirms that optimal shuttle specifications are invariant to demand uncertainty and discount rate assumptions, while pump rate is the pivotal parameter determining the optimal shuttle size. These results provide port authorities and policymakers with a quantitative decision framework for ammonia bunkering infrastructure investment in green shipping corridors.

**Keywords:** ammonia bunkering; green shipping corridor; mixed-integer linear programming; fleet sizing; levelized cost; infrastructure optimization

---

## 1. Introduction

The International Maritime Organization (IMO) adopted a revised greenhouse gas (GHG) strategy in 2023 targeting at least 30% emission reduction by 2030, 80% by 2040, and net-zero emissions by or around 2050 relative to 2008 levels [1]. Achieving these milestones requires a transition from conventional petroleum-based marine fuels to zero-carbon alternatives. Among the candidate fuels, ammonia (NH$_3$) has attracted substantial attention owing to its zero-carbon combustion characteristics, its compatibility with established bulk liquid transport and storage methods, and the existence of a mature global production infrastructure exceeding 180 million tons per year [2, 3]. Thermodynamic simulations have confirmed the technical feasibility of ammonia-fueled marine engines, establishing performance benchmarks that inform operational cost estimates [4]. Green ammonia production costs, currently estimated at 720--1,400 USD/ton, are projected to decline to 310--610 USD/ton by 2050 as renewable electricity costs fall and electrolyzer technology matures [5]. As of December 2025, DNV's Alternative Fuels Insight database records 144 ammonia-fueled vessels on order and 302 ammonia-ready vessels under construction or in operation [6], signaling that demand-side momentum for the ammonia fuel transition is materializing. The supply side -- specifically, the port-level infrastructure required to deliver ammonia from production and storage facilities to vessel fuel tanks -- remains largely unresolved.

Green shipping corridor initiatives aim to bridge this infrastructure gap by establishing end-to-end logistics for zero-emission vessel operations along specific trade routes. The Korea--United States green corridor agreement, formalized in April 2025, targets ammonia-fueled container ship operations between Busan and the U.S. West Coast, with the Korean government committing approximately 10 billion USD to Busan mega-port infrastructure including alternative fuel bunkering facilities [7]. Noh and Kang [8] analyzed the operational and economic feasibility of ammonia-fueled shipping along green corridor routes connecting Korean ports. These initiatives specify the fuel type (ammonia) and the port endpoints but leave a fundamental operational planning problem unaddressed: the determination of how many shuttle bunkering vessels to procure, at what capacity, with what pump flow rate, and on what deployment schedule to meet growing ammonia demand over a multi-decade planning horizon.

This paper addresses this planning problem for Busan Port, Korea's largest container port and the designated bunkering hub for the Korea--U.S. green corridor. We compare three supply chain configurations: (i) port-based storage at Busan with small shuttle vessels distributing ammonia to receiving vessels within the port (Case 1); (ii) remote supply from Ulsan, located 59 nautical miles northeast of Busan (Case 2); and (iii) remote supply from Yeosu, located 86 nautical miles to the west (Case 3). Ulsan and Yeosu are selected as candidate ammonia supply origins for geographic and industrial reasons. Ulsan hosts Korea's largest petrochemical complex, which includes ammonia import terminals handling a substantial share of the nation's ammonia imports. Yeosu is home to the Yeosu National Industrial Complex, one of Korea's primary chemical production clusters, with ammonia manufacturing and storage facilities that could serve as supply points for maritime bunkering. Both ports thus represent the most probable near-term ammonia sourcing locations for Busan-based bunkering operations.

### 1.1 Related Work

The literature relevant to ammonia bunkering infrastructure spans five thematic areas: alternative marine fuels, green corridor policy, ammonia bunkering operations and safety, fleet sizing and maritime optimization, and LNG bunkering infrastructure.

**Alternative marine fuels.** The technical and economic viability of ammonia as a marine fuel has been established through several review papers and techno-economic assessments. Al-Enazi et al. [3] provided a comprehensive comparison of alternative marine fuels, identifying ammonia's advantages -- zero-carbon combustion and compatibility with existing transport infrastructure at minus 33 degrees Celsius -- alongside its disadvantages, principally toxicity and lower volumetric energy density relative to LNG. Kim et al. [9] evaluated the economics of ammonia-fueled propulsion for individual vessels, finding cost premiums of a factor of 1.5 to 2.5 over conventional fuels depending on ammonia price assumptions. Korberg et al. [10] synthesized techno-economic parameters for advanced marine fuels, and Wang and Wright [11] compared bunkering infrastructure requirements across fuel types in qualitative terms. These studies treat the bunkering supply chain as a fixed assumption -- ammonia is available at a given price and location -- without modeling the infrastructure required to deliver it from source to vessel.

**Green corridor policy and planning.** At the strategic level, the green corridor concept has gained institutional support through the Getting to Zero Coalition [7], which identified Busan as a candidate port for ammonia bunkering along Pacific corridor routes. Lloyd's Register and UMAS [12] estimated fuel transition costs at a macro level. Xing et al. [2] mapped decarbonization pathways for the maritime sector through 2050, and Verschuur et al. [13] quantified the socio-economic and environmental impacts of green corridor infrastructure investments. The IMO's 2023 revised GHG strategy [1] sets binding emission reduction milestones that generate the demand trajectory underlying the present model. However, these policy documents and macro-level studies set targets -- numbers of zero-emission vessels, percentages of green fuel uptake -- without providing decision-makers with quantitative tools to determine the required bunkering infrastructure specifications.

**Ammonia bunkering operations and safety.** The most directly relevant operational study is that of Yang and Lam [14], who developed a discrete event simulation (DES) model for ammonia bunkering supply chains. Their model evaluates how the number and capacity of bunker supply vessels, bunkering flow rate, and demand level affect operational and economic performance. Key findings include that flow rate has up to 51.3% impact on bunkering service time when varied by plus or minus 50%, and the number of bunker supply vessels is the most sensitive parameter for annual operational cost, with up to 15.2% effect. Their DES model evaluates predefined configurations through simulation runs, answering the question of what happens if a given fleet is deployed, but does not identify the optimal fleet specification. Furthermore, their model uses static demand -- a fixed number of vessels requiring bunkering at a single point in time -- whereas operational planning requires modeling demand as a trajectory growing over multiple decades. They also analyze a single supply chain configuration rather than comparing port-based storage against remote supply alternatives. A complementary body of work addresses ammonia bunkering safety. Fan et al. [15] developed the first Bayesian network-based quantitative risk assessment for ammonia ship-to-ship bunkering, finding that toxicity poses greater risk than flammability. Yang and Lam [16] extended this analysis to multi-scale release scenarios. Kim et al. [17] integrated systems-theoretic process analysis (STPA) with Bayesian networks for port-level ammonia bunkering risk quantification. Qu et al. [18] proposed a comprehensive quantitative risk assessment framework for ammonia storage and bunkering at ports. Khan et al. [19] provided a broad review of ammonia bunkering in the maritime sector, cataloguing technological, operational, and regulatory challenges and confirming that no existing study has simultaneously addressed bunkering fleet sizing, shuttle vessel capacity selection, and pump flow rate specification. Wang et al. [20] formulated an optimization model for ammonia bunkering network configurations -- the first mathematical programming approach applied to ammonia bunkering -- but in a single-period setting without pump rate as a design parameter. Dahlke-Wallat et al. [21] performed a techno-economic evaluation of ammonia bunkering infrastructure concepts, comparing ship-to-ship and truck-to-ship modalities.

**Fleet sizing and maritime optimization.** Mixed-integer linear programming for fleet sizing is a well-established methodology in maritime operations research. Fagerholt [22] demonstrated MILP-based fleet scheduling decision support systems, and Christiansen et al. [23] provided a comprehensive survey of ship routing and scheduling methods, updated by Fagerholt et al. [24] through 2023 covering more than 50 maritime inventory routing papers. Zhao et al. [25] jointly optimized heterogeneous fleet deployment, sailing speed, and fuel bunkering for green container shipping. In adjacent domains, Stalahane et al. [26] applied stochastic programming to vessel fleet sizing for offshore wind farm maintenance, Vieira et al. [27] extended fleet composition optimization to offshore supply vessels with periodic routing, and Bakkehaug et al. [28] addressed multi-period bulk ship fleet renewal under demand uncertainty, demonstrating that dynamic fleet expansion outperforms static sizing. Pantuso et al. [29] showed that fleet renewal decisions under uncertainty benefit from stochastic formulations, Wang et al. [30] incorporated chartering flexibility into fleet composition optimization, and Tan et al. [31] extended fleet sizing to include chartered vessels under demand uncertainty, finding that charter flexibility reduces expected cost by 8--12%. Rodrigues et al. [32] compared uncertainty modeling techniques for maritime inventory routing, focusing on inventory feasibility rather than infrastructure investment.

**LNG bunkering infrastructure.** For LNG bunkering specifically, Doymus et al. [33] formulated a MILP for ship-to-ship LNG bunkering supply chains in Turkey, determining the number and size of LNG bunker barges under multiple demand scenarios. Jokinen et al. [34] formulated an early MILP for small-scale LNG supply chain optimization along a coastline. Pratama et al. [35] developed a multi-period MILP for LNG bunkering vessel fleet sizing and scheduling, representing the closest methodological analog to the present work. Guo et al. [36] applied integer linear programming to determine optimal LNG bunkering methods at a single port. He et al. [37] optimized route, speed, and bunkering decisions for LNG-fueled tramp ships. Ntakolia et al. [38] applied Monte Carlo simulation to LNG refuelling station design, and Machfudiyanto et al. [39] conducted a feasibility study of LNG bunkering infrastructure in Indonesia. However, all of these models address LNG, which is stored at minus 162 degrees Celsius, rather than ammonia, which is stored at minus 33 degrees Celsius or under moderate pressure. None of them includes pump flow rate as an explicit design parameter or models the flow-rate-dependent cycle time that characterizes ammonia bunkering system performance.

At the supply chain level, Galan-Martin et al. [40] formulated a MILP to optimize green ammonia distribution for intercontinental energy transport, and Kim et al. [41] performed a techno-economic analysis of ammonia ocean transport. Wang et al. [42] applied stochastic optimization to ammonia supply chain design under uncertainty. The Oxford Institute for Energy Studies [43] finds that production contributes over 79% of total delivered ammonia cost, implying that bunkering logistics costs, while smaller in absolute terms, remain the controllable component for port-level planners. Trivyza et al. [44] designed ammonia-based green corridor networks at the global level, and Fullerton et al. [45] surveyed adoption barriers across the ammonia fuel supply chain. These supply chain models and cost projections operate at spatial scales (intercontinental routes, national networks) that do not address the port-level infrastructure sizing problem that is the focus of the present study.

### 1.2 Research Gaps and Contributions

A review of the literature reveals three gaps that no existing study addresses.

**Gap 1: No parametric evaluation across shuttle size, pump rate, and fleet expansion.** No study systematically evaluates the interaction among shuttle vessel capacity, bunkering pump flow rate, and multi-period fleet sizing for ammonia bunkering. The coupling among these parameters is operationally significant: shuttle size determines the time required to transfer a full load, which in turn determines cycle time, which governs how many bunkering operations a single shuttle can complete per year and thus how many shuttles are required. Wang et al. [20] optimize ammonia bunkering configurations but in a single-period setting without pump rate, and even the most advanced fleet sizing models in the maritime literature [30, 29, 31, 35] treat cargo transfer as instantaneous, ignoring the flow-rate-dependent cycle time that is central to bunkering operations.

**Gap 2: No quantitative comparison of port-based storage versus remote supply.** No existing study compares port-based ammonia storage with small-shuttle intra-port distribution against remote supply from external sources under identical demand assumptions, nor has a break-even distance been identified. Guo et al. [36] compare bunkering modes for LNG at a single port but do not compare supply chain configurations with distance as a continuous parameter.

**Gap 3: No multi-period fleet expansion model for ammonia bunkering.** No model optimizes the timing of ammonia bunkering fleet expansion synchronized with a demand growth trajectory, despite the existence of fleet renewal models for conventional shipping [28, 29], oil tanker operations [31], and LNG bunkering [33, 35, 34].

This paper addresses all three gaps through a MILP model that systematically evaluates shuttle vessel capacity (500--50,000 m$^3$), pump flow rate (100--1,500 m$^3$/h in sensitivity analysis, 500 m$^3$/h as the baseline), and year-by-year fleet expansion over a 21-year planning horizon (2030--2050) for three ammonia supply chain configurations at Busan Port. The approach enumerates all feasible shuttle-pump combinations and solves a fleet-sizing MILP for each, yielding a complete cost landscape rather than a single point estimate. Our four contributions are as follows.

First, we develop the first multi-period MILP model for ammonia bunkering infrastructure that explicitly incorporates flow-rate-dependent cycle time into the fleet sizing formulation, enabling parametric evaluation across all feasible shuttle-pump configurations to identify the cost-minimizing specification for each supply chain case.

Second, we provide a quantitative comparison of port-based storage versus remote supply under identical demand and cost assumptions, including a break-even distance analysis parameterized across 10--200 nautical miles that yields a transferable decision rule for port planners.

Third, we demonstrate through sensitivity analysis across four demand scenarios, six tornado parameters, fuel price variation, bunker volume variation, and discount rate variation that optimal shuttle specifications are robust to demand and financial uncertainty, while pump flow rate is the pivotal parameter determining the optimal shuttle size -- a finding that decouples the specification decision from demand forecasting.

Fourth, we identify a differentiated cost driver hierarchy across supply chain configurations through tornado analysis, informing distinct risk management strategies for port-based versus remote supply infrastructure.

The remainder of the paper is organized as follows. Section 2 presents the MILP formulation, cycle time model, and cost structure. Section 3 reports optimization results, temporal dynamics, cost decomposition, and sensitivity analyses. Section 4 discusses the break-even distance analysis, result robustness, cross-model comparison with published DES results, practical implications, and limitations. Section 5 concludes.

---

## 2. Methodology

### 2.1 Problem Description and Assumptions

We consider a port authority planning ammonia bunkering infrastructure for a green shipping corridor over a 21-year horizon spanning 2030 through 2050 inclusive. The number of ammonia-fueled vessels calling at the port grows linearly from $V_{\text{start}} = 50$ in 2030 to $V_{\text{end}} = 500$ in 2050, with each vessel requiring $v_{\text{call}} = 5{,}000$ m$^3$ of liquid ammonia per bunkering call at a frequency of $f_{\text{voy}} = 12$ calls per year. The terminal count of 500 vessels represents approximately 4.5% of Busan Port's current annual container vessel calls (approximately 11,000 per year [7]), consistent with moderate ammonia adoption projections.

The decision-maker must determine three design parameters: the shuttle vessel capacity $V_s$ from a discrete set of available sizes, the bunkering pump flow rate $Q_p$ in cubic meters per hour, and the number of new shuttle vessels $x_t$ to add in each year $t$ of the planning horizon, such that the net present cost (NPC) over 21 years is minimized while meeting all demand and operational constraints.

We analyze three supply chain configurations, illustrated in Fig. 1 (presented in Section 2.2 alongside the cycle time model). Table 1 summarizes the key parameters for each configuration.

**Table 1: Three supply chain configurations and their key operational parameters**

| Parameter | Case 1 (Busan) | Case 2 (Ulsan) | Case 3 (Yeosu) |
|-----------|:--------------:|:--------------:|:--------------:|
| Ammonia source | Busan port storage | Ulsan (petrochemical complex) | Yeosu (industrial complex) |
| One-way distance | Within port | 59 nm | 86 nm |
| Transit speed | -- | 15 kn | 15 kn |
| One-way travel time $\tau$ | 1.0 h | 3.93 h | 5.73 h |
| Storage at Busan | Yes | No | No |
| Shuttle size candidates $V_s$ | 500--10,000 m$^3$ | 2,500--50,000 m$^3$ | 2,500--50,000 m$^3$ |
| Bunkering pump rate $Q_p$ (baseline) | 500 m$^3$/h | 500 m$^3$/h | 500 m$^3$/h |
| Shore pump rate $Q_{\text{shore}}$ | 700 m$^3$/h | 700 m$^3$/h | 700 m$^3$/h |
| Setup time per endpoint $\sigma$ | 2.0 h | 2.0 h | 2.0 h |
| Shore loading fixed time $t_{\text{fixed}}$ | 4.0 h | 4.0 h | 4.0 h |
| Bunker volume per call $v_{\text{call}}$ | 5,000 m$^3$ | 5,000 m$^3$ | 5,000 m$^3$ |
| Maximum annual operating hours $H_{\max}$ | 8,000 h | 8,000 h | 8,000 h |
| Maximum call duration $T_{\text{max,call}}$ | 80 h | 80 h | 80 h |
| Pumping time basis | Shuttle capacity $V_s / Q_p$ | Vessel demand $v_{\text{call}} / Q_p$ | Vessel demand $v_{\text{call}} / Q_p$ |

The key structural difference between these configurations lies in the pumping time formulation. In Case 1, the shuttle carries ammonia from port storage to a receiving vessel; the pumping time equals the time to empty the shuttle, which depends on shuttle capacity divided by pump rate. In Cases 2 and 3, the shuttle travels from a remote source and may carry enough ammonia to serve multiple vessels per trip; the pumping time per vessel depends on the bunkering demand per call divided by pump rate. This structural distinction propagates through the cycle time model (Section 2.2) and ultimately determines the optimal shuttle size for each configuration.

**Table 2: Additional fixed parameters common to all cases**

| Parameter | Symbol | Value | Unit |
|-----------|--------|------:|------|
| Planning horizon | $\mathcal{T}$ | 2030--2050 | years |
| Starting vessel count | $V_{\text{start}}$ | 50 | vessels |
| Terminal vessel count | $V_{\text{end}}$ | 500 | vessels |
| Voyages per vessel per year | $f_{\text{voy}}$ | 12 | calls/year |
| Bunker volume per call | $v_{\text{call}}$ | 5,000 | m$^3$ |
| Maximum annual operating hours | $H_{\max}$ | 8,000 | h/year |
| Maximum call duration | $T_{\text{max,call}}$ | 80 | h |
| Shore pump rate | $Q_{\text{shore}}$ | 700 | m$^3$/h |
| Shore loading fixed time | $t_{\text{fixed}}$ | 4.0 | h |
| Setup time per endpoint | $\sigma$ | 2.0 | h |
| Ammonia density (bunkering) | $\rho$ | 0.681 | ton/m$^3$ |
| Fuel price (baseline) | $P_f$ | 600 | USD/ton |
| CAPEX scaling exponent | $\alpha$ | 0.75 | -- |
| Annualization interest rate | $r$ | 0.07 | -- |
| Annualization period | $n$ | 21 | years |
| Social discount rate | $\delta$ | 0 | -- |

#### Assumptions

We adopt six simplifying assumptions.

**A1. Linear demand growth.** The number of ammonia-fueled vessels increases linearly from 50 to 500 over 21 years. Actual adoption may follow an S-curve with slower early growth and potential acceleration after 2040. Sensitivity analysis across four demand scenarios (250 to 1,000 end-vessels) in Section 3 tests the robustness of results to this assumption.

**A2. No social discounting.** All annual costs are weighted equally in the NPC summation, with the social discount rate set to zero. This treats the 21-year total as a budget planning figure. The annualization interest rate $r = 0.07$ used to convert lump-sum capital expenditures to equivalent annual payments is distinct from this social discount rate and represents the financing cost of capital (Section 2.4). Section 3 presents discount rate sensitivity at 0%, 5%, and 8%.

**A3. Fixed fuel price.** Green ammonia price is held constant at 600 USD/ton over the planning horizon [5]. Section 3 presents fuel price sensitivity across 300--1,200 USD/ton.

**A4. Deterministic vessel scheduling.** Vessels arrive uniformly throughout the year; no queuing or congestion effects are modeled. This underestimates fleet requirements during peak demand periods. The annual working-time constraint (Section 2.3) governs fleet sizing based on aggregate annual capacity.

**A5. Fixed bunker volume per call.** All vessels require an identical 5,000 m$^3$ of ammonia per bunkering call. In practice, vessel sizes vary; Section 3 tests bunker volume sensitivity from 2,500 to 10,000 m$^3$.

**A6. Size-dependent SFOC.** Specific fuel oil consumption (SFOC) depends on shuttle size through an engine type classification described in Section 2.4. The tornado sensitivity analysis in Section 3 tests the impact of SFOC variation on results.

---

### 2.2 Cycle Time Model

The cycle time $T_{\text{cycle}}$ determines how many bunkering operations a single shuttle can complete per year, and thus how many shuttles are required to serve a given level of demand. The cycle time formulation differs structurally between Case 1 (port-based storage) and Cases 2 and 3 (remote supply). Fig. 1 illustrates the cycle time components for all three configurations.

#### 2.2.1 Case 1: Port-Based Storage

In Case 1, the shuttle loads ammonia from a shore-side storage terminal, transits within the port to the receiving vessel, transfers fuel via ship-to-ship (STS) bunkering, and returns to the storage terminal. The total cycle time for a single shuttle round trip in Case 1 is:

$$T_{\text{cycle}}^{\text{Case 1}} = T_{\text{shore}} + \tau_{\text{out}} + \sigma_{\text{connect}} + T_{\text{pump}}^{\text{Case 1}} + \sigma_{\text{disconnect}} + \tau_{\text{return}}$$
(1)

The shore loading time $T_{\text{shore}}$ comprises the time to pump ammonia from the storage terminal into the shuttle plus a fixed component for setup and shutdown procedures:

$$T_{\text{shore}} = \frac{V_s}{Q_{\text{shore}}} + t_{\text{fixed}}$$
(2)

where $Q_{\text{shore}} = 700$ m$^3$/h is the shore pump rate and $t_{\text{fixed}} = 4.0$ h accounts for inbound maneuvering, hose connection, purging, hose disconnection, and outbound maneuvering at the shore terminal. The outbound and return transit times are each equal to the one-way travel time, $\tau_{\text{out}} = \tau_{\text{return}} = \tau = 1.0$ h. The connection and disconnection times at the receiving vessel are each $\sigma_{\text{connect}} = \sigma_{\text{disconnect}} = \sigma = 2.0$ h; connection includes mooring, hose attachment, and pressure testing, while disconnection includes nitrogen purging and hose detachment.

The pumping time for Case 1 is defined as the time required to empty the shuttle into the receiving vessel:

$$T_{\text{pump}}^{\text{Case 1}} = \frac{V_s}{Q_p}$$
(3)

where $Q_p$ is the bunkering pump flow rate. Because the shuttle capacity may be smaller than the bunker demand per call, multiple trips may be required. The number of shuttle trips per bunkering call is:

$$n_{\text{trip}} = \left\lceil \frac{v_{\text{call}}}{V_s} \right\rceil$$
(4)

The total duration of a single bunkering call is therefore $n_{\text{trip}} \times T_{\text{cycle}}^{\text{Case 1}}$, and this duration must not exceed the maximum acceptable call duration $T_{\text{max,call}}$ (see Section 2.3). Worked numerical examples for all three cases are provided in Appendix A.

#### 2.2.2 Cases 2 and 3: Remote Supply

In Cases 2 and 3, the shuttle loads ammonia at a remote source port (Ulsan or Yeosu), transits to Busan, enters the port, serves one or more receiving vessels sequentially through STS bunkering, exits the port, and returns to the source. The cycle time for remote supply cases is:

$$T_{\text{cycle}}^{\text{Case 2/3}} = T_{\text{shore}} + \tau_{\text{out}} + T_{\text{port,entry}} + \sum_{j=1}^{N_v} \left( T_{\text{move},j} + 2\sigma + T_{\text{pump},j}^{\text{Case 2/3}} \right) + T_{\text{port,exit}} + \tau_{\text{return}}$$
(5)

The number of vessels served per shuttle trip, denoted $N_v$, is determined by the ratio of shuttle capacity to per-call demand:

$$N_v = \left\lfloor \frac{V_s}{v_{\text{call}}} \right\rfloor$$
(6)

The port entry and exit times are each $T_{\text{port,entry}} = T_{\text{port,exit}} = 1.0$ h. The inter-vessel movement time is $T_{\text{move},j} = 1.0$ h for each vessel served. The pumping time per vessel in Cases 2 and 3 is based on the bunkering demand per call rather than the shuttle capacity:

$$T_{\text{pump},j}^{\text{Case 2/3}} = \frac{v_{\text{call}}}{Q_p}$$
(7)

The number of shuttle trips required per bunkering call in the remote supply cases accounts for the shuttle's ability to serve multiple vessels per trip:

$$n_{\text{trip}} = \frac{1}{N_v}$$
(8)

This fractional value reflects that each shuttle trip serves $N_v$ vessels; a single vessel's bunkering call therefore consumes $1 / N_v$ of a shuttle trip's capacity. For example, when a shuttle carries 5,000 m$^3$ and each vessel requires 5,000 m$^3$, then $N_v = 1$ and $n_{\text{trip}} = 1$. When a shuttle carries 10,000 m$^3$, then $N_v = 2$ and $n_{\text{trip}} = 0.5$, meaning each vessel consumes half of a shuttle trip's resources. This fractional allocation ensures that the annual working-time constraint (Eq. 12) correctly accounts for shared shuttle capacity across multiple vessels served per trip.

---

### 2.3 MILP Formulation

#### 2.3.1 Notation

**Table 3: Sets, parameters, and decision variables**

| Symbol | Definition | Unit | Value |
|--------|-----------|------|-------|
| **Sets** | | | |
| $\mathcal{T}$ | Planning years | -- | $\{2030, 2031, \ldots, 2050\}$ |
| **Parameters** | | | |
| $V_s$ | Shuttle vessel capacity | m$^3$ | Case-dependent (Table 1) |
| $Q_p$ | Bunkering pump flow rate | m$^3$/h | 500 (base); 100--1,500 (sensitivity) |
| $T_{\text{cycle}}$ | Cycle duration (from Section 2.2) | h | Case- and configuration-dependent |
| $n_{\text{trip}}$ | Trips per bunkering call | -- | Eq. (4) or (8) |
| $H_{\max}$ | Maximum annual operating hours | h/year | 8,000 |
| $T_{\text{max,call}}$ | Maximum bunkering call duration | h | 80 |
| $D_t$ | Annual bunkering calls demanded in year $t$ | calls | $V_t \times f_{\text{voy}}$ |
| $V_t$ | Number of vessels in year $t$ | count | Linear interpolation from 50 to 500 |
| $f_{\text{voy}}$ | Voyages per vessel per year | calls/year | 12 |
| $v_{\text{call}}$ | Bunker volume per call | m$^3$ | 5,000 |
| $T_{\text{shore}}$ | Shore loading time per shuttle trip | h | Eq. (2) |
| $T_{\text{pump}}$ | Bunkering pump time per trip | h | Eq. (3) or (7) |
| **Decision variables** | | | |
| $x_t \in \mathbb{Z}^+$ | New shuttles added in year $t$ | count | -- |
| $N_t \in \mathbb{Z}^+$ | Cumulative shuttle fleet size in year $t$ | count | -- |
| $y_t \in \mathbb{R}^+$ | Annual bunkering calls served in year $t$ | calls | -- |

The decision variable $x_t$ represents the number of new shuttle vessels procured in year $t$; once added, shuttles remain in the fleet for the remainder of the planning horizon. The cumulative fleet size $N_t$ tracks the total number of operational shuttles available in year $t$. The variable $y_t$ represents the total number of bunkering calls served in year $t$, which must at least equal the demand $D_t$.

#### 2.3.2 Objective Function

The objective minimizes the total net present cost over the 21-year planning horizon:

$$\min \; \text{NPC} = \sum_{t \in \mathcal{T}} \left[ C_t^{\text{ann}} + C_t^{\text{fOPEX}} + C_t^{\text{vOPEX}} \right]$$
(9)

where $C_t^{\text{ann}}$ is the annualized capital expenditure (CAPEX) in year $t$, $C_t^{\text{fOPEX}}$ is the fixed operational expenditure, and $C_t^{\text{vOPEX}}$ is the variable operational expenditure. No social discounting is applied ($\delta = 0$; Assumption A2). The cost components are defined in Section 2.4.

#### 2.3.3 Constraints

**Fleet inventory balance.** The cumulative fleet size in each year equals the prior year's fleet plus new additions. The fleet starts at zero before the planning horizon begins:

$$N_t = N_{t-1} + x_t, \quad \forall \, t \in \mathcal{T}; \quad N_{2029} = 0$$
(10)

**Demand satisfaction.** The number of bunkering calls served in each year must meet or exceed the demand, which equals the number of ammonia-fueled vessels in that year multiplied by the annual voyage frequency:

$$y_t \geq D_t = V_t \times f_{\text{voy}}, \quad \forall \, t \in \mathcal{T}$$
(11)

**Working time capacity.** The total shuttle operating hours required to fulfill all bunkering calls must not exceed the fleet's aggregate annual capacity. This constraint is typically the binding constraint that determines fleet size:

$$y_t \times n_{\text{trip}} \times T_{\text{cycle}} \leq N_t \times H_{\max}, \quad \forall \, t \in \mathcal{T}$$
(12)

The left-hand side represents the total hours consumed: each bunkering call requires $n_{\text{trip}}$ shuttle trips, and each trip requires $T_{\text{cycle}}$ hours. The right-hand side is the total available operating hours across all $N_t$ shuttles in the fleet.

**Maximum call duration.** The total time for a single bunkering call -- comprising all required shuttle trips -- must not exceed the maximum acceptable call duration. This constraint reflects the operational requirement that a receiving vessel cannot be occupied by bunkering operations indefinitely:

$$n_{\text{trip}} \times T_{\text{cycle}} \leq T_{\text{max,call}}$$
(13)

where $T_{\text{max,call}} = 80$ h. This constraint is evaluated at the configuration level (for each shuttle-pump combination) rather than year by year, since cycle time and trips per call are time-invariant for a given configuration. Configurations that violate this constraint are excluded from the optimization as infeasible. The 80-hour limit represents an upper bound on the acceptable bunkering duration for a receiving vessel in port; exceeding this duration would create unacceptable scheduling conflicts and berth occupancy costs. This constraint becomes binding when small shuttles are combined with large per-call demand, as each additional trip adds a full cycle time to the total call duration.

**Non-negativity and integrality:**

$$x_t \geq 0, \quad x_t \in \mathbb{Z}, \quad \forall \, t \in \mathcal{T}$$
(14)

---

### 2.4 Cost Model

#### 2.4.1 Shuttle CAPEX (Scaling Law)

Shuttle vessel capital cost follows a power-law scaling relationship commonly used in marine engineering cost estimation:

$$C_{\text{shuttle}}(V_s) = C_{\text{ref}} \times \left( \frac{V_s}{V_{\text{ref}}} \right)^{\alpha}$$
(15)

where $C_{\text{ref}} = 61.5$ million USD is the reference cost for a vessel of capacity $V_{\text{ref}} = 40{,}000$ m$^3$, and $\alpha = 0.75$ is the scaling exponent. The scaling exponent reflects economies of scale in shipbuilding: doubling vessel capacity increases cost by a factor of $2^{0.75} \approx 1.68$ rather than a factor of 2.

#### 2.4.2 Bunkering Equipment CAPEX

Bunkering equipment cost comprises an equipment surcharge proportional to shuttle CAPEX plus the pump cost:

$$C_{\text{equip}} = C_{\text{shuttle}} \times r_{\text{equip}} + C_{\text{pump}}$$
(16)

where $r_{\text{equip}} = 0.03$ is the equipment cost ratio. The pump cost is derived from the required pump power:

$$C_{\text{pump}} = P_{\text{pump}} \times c_{\text{kW}}, \quad P_{\text{pump}} = \frac{Q_p \times \Delta p \times 10^5}{3.6 \times 10^6 \times \eta_p}$$
(17)

with pump differential pressure $\Delta p = 4.0$ bar, pump efficiency $\eta_p = 0.70$, and pump unit cost $c_{\text{kW}} = 2{,}000$ USD/kW.

#### 2.4.3 Annualization

All capital costs are converted to equivalent annual payments using a capital recovery factor derived from the annuity formula:

$$\text{AF} = \frac{1 - (1 + r)^{-n}}{r}$$
(18)

where $r = 0.07$ is the annualization interest rate and $n = 21$ years is the annualization period, yielding $\text{AF} = 10.8355$ years.

The annualized CAPEX in year $t$ is:

$$C_t^{\text{ann}} = \frac{\displaystyle\sum_{\tau=2030}^{t} x_\tau \times \left[ C_{\text{shuttle}}(V_s) + C_{\text{equip}} \right]}{\text{AF}}$$
(19)

The annualization rate $r = 0.07$ represents the financing cost of capital -- the blended cost of debt and equity used to fund shuttle vessel procurement. This is conceptually and numerically distinct from the social discount rate $\delta = 0$ used for aggregating annual costs across the planning horizon. The annualization rate converts a lump-sum purchase price into a stream of equivalent annual payments that reflect the time-value cost of financing, analogous to a mortgage payment schedule. The social discount rate, by contrast, would reflect the decision-maker's preference for present versus future consumption; setting $\delta = 0$ means that a dollar of cost incurred in 2030 is weighted identically to a dollar incurred in 2050 in the NPC summation. When a positive social discount rate is introduced (tested in Section 3), the annual cost stream (annualized CAPEX plus OPEX) is discounted, which reduces reported NPC but does not affect optimal specifications because the discount factor applies uniformly across all configurations.

#### 2.4.4 Fixed OPEX

Fixed operational expenditures are proportional to the cumulative fleet size and asset values:

$$C_t^{\text{fOPEX}} = N_t \times \left( C_{\text{shuttle}} \times r_{\text{fOPEX}}^{s} + C_{\text{equip}} \times r_{\text{fOPEX}}^{b} \right)$$
(20)

where $r_{\text{fOPEX}}^{s} = 0.05$ is the shuttle fixed OPEX ratio (covering maintenance, insurance, crew, and docking costs as a fraction of shuttle CAPEX) and $r_{\text{fOPEX}}^{b} = 0.05$ is the bunkering equipment fixed OPEX ratio.

#### 2.4.5 Variable OPEX

Variable costs are proportional to operating activity in each year:

$$C_t^{\text{vOPEX}} = y_t \times n_{\text{trip}} \times c_{\text{fuel}}^{s} + y_t \times c_{\text{fuel}}^{p}$$
(21)

The first term is the shuttle fuel cost, and the second term is the pump fuel cost. The shuttle fuel cost per trip is:

$$c_{\text{fuel}}^{s} = \frac{\text{MCR}(V_s) \times \text{SFOC}(V_s) \times \tau_{\text{travel}}}{10^6} \times P_f$$
(22)

where MCR($V_s$) is the maximum continuous rating of the shuttle engine in kilowatts, obtained from a power-law regression $\text{MCR} = 17.17 \times \text{DWT}^{0.566}$ kW with DWT $ = 0.85 \times V_s$. The term SFOC($V_s$) is the specific fuel oil consumption in grams per kilowatt-hour, classified by engine type according to shuttle deadweight tonnage as shown in Table 4. The variable $\tau_{\text{travel}}$ is the active travel time per cycle (i.e., the sum of outbound and return transit times), and $P_f = 600$ USD/ton is the ammonia fuel price.

The pump fuel cost per bunkering call is:

$$c_{\text{fuel}}^{p} = \frac{P_{\text{pump}} \times T_{\text{pump,total}} \times \text{SFOC}_p}{10^6} \times P_f$$
(23)

where $P_{\text{pump}}$ is the pump power as defined in Eq. (17), $T_{\text{pump,total}}$ is the total pumping time per bunkering call (equal to $n_{\text{trip}} \times T_{\text{pump}}$), and SFOC$_p$ is the specific fuel oil consumption of the pump drive engine. In this model, SFOC$_p$ is assigned the same value as the shuttle engine SFOC for the corresponding shuttle size class, on the assumption that the pump is driven by an auxiliary engine of similar type aboard the shuttle vessel.

**Table 4: SFOC classification by shuttle deadweight tonnage**

| DWT Range (ton) | Engine Type | SFOC (g/kWh) | Corresponding Shuttle Sizes |
|:---------------:|:-----------:|:------------:|:---------------------------:|
| < 3,000 | 4-stroke high-speed | 505 | 500--3,500 m$^3$ |
| 3,000--8,000 | 4-stroke medium-speed | 436 | 4,000--7,500 m$^3$ |
| 8,000--15,000 | Medium 2-stroke | 413 | 10,000--15,000 m$^3$ |
| 15,000--30,000 | 2-stroke | 390 | 20,000--35,000 m$^3$ |
| > 30,000 | 2-stroke large | 379 | 40,000--50,000 m$^3$ |

The SFOC classification follows standard marine engineering practice, in which engine type selection is determined by vessel size. Smaller shuttle vessels (DWT below 3,000 ton) are fitted with high-speed four-stroke engines that offer compact installation but operate at higher specific fuel consumption. Mid-range vessels (DWT 3,000--8,000 ton) use medium-speed four-stroke engines with improved thermal efficiency. Larger vessels employ two-stroke engines with progressively lower SFOC, reflecting the superior thermodynamic efficiency of slow-speed, long-stroke engine designs. The SFOC values in Table 4 are based on ammonia fuel, which has approximately 2.3 times the specific consumption of conventional marine diesel oil on a mass basis due to its lower heating value; the diesel-equivalent SFOC values are 220, 190, 180, 170, and 165 g/kWh for the five size classes respectively [4].

#### 2.4.6 Levelized Cost of Ammonia Bunkering

The levelized cost of ammonia bunkering (LCOA) normalizes the total NPC by the cumulative mass of ammonia delivered over the planning horizon:

$$\text{LCOA} = \frac{\text{NPC}}{\displaystyle\sum_{t \in \mathcal{T}} y_t \times v_{\text{call}} \times \rho}$$
(24)

where $\rho = 0.681$ ton/m$^3$ is the ammonia density under bunkering conditions. The denominator represents the total tonnage of ammonia physically delivered to receiving vessels over 21 years. LCOA thus measures the infrastructure service cost per ton of ammonia delivered, excluding the ammonia procurement cost itself (approximately 600 USD/ton at baseline). This metric enables comparison across configurations that deliver the same total quantity of ammonia but at different infrastructure costs.

---

### 2.5 Solution Approach

The MILP is solved using the CBC (Coin-or Branch and Cut) solver accessed through the PuLP optimization library in Python. For each supply chain configuration, the optimization proceeds in two levels. At the outer level, all feasible combinations of shuttle capacity ($V_s$) and pump flow rate ($Q_p$) are enumerated. For the baseline analysis, $Q_p$ is fixed at 500 m$^3$/h, with 10--12 shuttle sizes per case yielding 10--12 combinations. At the inner level, for each ($V_s$, $Q_p$) pair that satisfies the maximum call duration constraint (Eq. 13), the multi-period MILP determines the optimal fleet deployment schedule $\{x_t\}_{t \in \mathcal{T}}$ that minimizes total NPC subject to the demand satisfaction (Eq. 11) and working time capacity (Eq. 12) constraints. The optimal infrastructure specification is then selected as the ($V_s$, $Q_p$) combination yielding the lowest NPC across all evaluated pairs.

This approach identifies the optimal solution over the discrete candidate set of shuttle sizes and pump rates. Because the shuttle-pump grid is enumerated exhaustively, no feasible combination is excluded from evaluation. The parametric enumeration approach, while computationally straightforward, offers two practical advantages. First, it provides decision-makers with a complete cost landscape across all feasible specifications rather than a single point estimate, enabling assessment of near-optimal alternatives and cost plateaus. Second, it enables direct comparison of structurally heterogeneous supply configurations (port-based storage versus remote supply) under identical demand and cost assumptions. Computation time is under 30 seconds per case on a standard desktop workstation equipped with an Intel i7 processor and 32 GB of RAM, reflecting the modest problem dimensionality (10--12 shuttle sizes multiplied by one pump rate multiplied by 21 annual time periods).

#### 2.5.1 Sensitivity Analysis Design

We conduct seven sensitivity analyses to test the robustness of results to parameter uncertainty. Table 5 summarizes the design of each analysis.

**Table 5: Sensitivity analysis design**

| Analysis | Variable Varied | Range | Points | Cases Tested |
|:--------:|:---------------:|:-----:|:------:|:------------:|
| Tornado | 6 parameters, each +/-20% | -- | 12 per case | All 3 |
| Fuel price | $P_f$ | 300--1,200 USD/ton | 9 | All 3 |
| Bunker volume | $v_{\text{call}}$ | 2,500--10,000 m$^3$ | 7 | All 3 |
| Two-way | $P_f \times v_{\text{call}}$ | 5 x 5 matrix | 25 | Case 1 |
| Demand scenarios | $V_{\text{end}}$ | 250, 500, 750, 1,000 | 4 | All 3 |
| Break-even distance | One-way distance | 10--200 nm | 20 | Cases 2, 3 vs. 1 |
| Discount rate | $\delta$ | 0%, 5%, 8% | 3 | All 3 |

The tornado analysis varies six parameters -- CAPEX scaling exponent, bunker volume per call, maximum annual operating hours, one-way travel time, fuel price, and SFOC -- by plus or minus 20% from their baseline values, measuring the resulting NPC swing for each parameter while holding all others constant. The break-even distance analysis parameterizes the one-way travel distance from 10 to 200 nautical miles for Cases 2 and 3 while holding Case 1 constant, identifying whether a crossover distance exists at which remote supply becomes cheaper than port-based storage. The demand scenario analysis tests four growth trajectories defined by the terminal vessel count (250, 500, 750, and 1,000 end-vessels in 2050) to assess whether optimal shuttle specifications change with demand scale.

---

## References

[1] IMO. (2023). 2023 IMO Strategy on Reduction of GHG Emissions from Ships. Resolution MEPC.377(80), adopted 7 July 2023.

[2] Xing, H., Stuart, C., Spence, S., & Chen, H. (2021). Alternative fuel options for low carbon maritime transportation: Pathways to 2050. Journal of Cleaner Production, 297, 126651.

[3] Al-Enazi, A., Okonkwo, E. C., Bicer, Y., & Al-Ansari, T. (2021). A review of cleaner alternative fuels for maritime transportation. Energy Reports, 7, 1962--1985.

[4] Imhoff, T. B., Gkantonas, S., & Mastorakos, E. (2021). Analysing the performance of ammonia powertrains in the marine environment. Energies, 14(21), 7447.

[5] IRENA & AEA. (2022). Innovation Outlook: Renewable Ammonia. International Renewable Energy Agency, Abu Dhabi.

[6] DNV. (2025). Alternative Fuels Insight Platform. Retrieved December 2025 from https://afi.dnv.com.

[7] Getting to Zero Coalition. (2021). The Next Wave: Green Corridors. Global Maritime Forum.

[8] Noh, H., & Kang, D. (2025). Operational and economic feasibility of ammonia-fueled shipping in green corridor routes. [Journal and volume details to be completed].

[9] Kim, K., Roh, G., Kim, W., & Chun, K. (2020). A preliminary study on an alternative ship propulsion system fueled by ammonia: Environmental and economic assessments. Journal of Marine Science and Engineering, 8(3), 183.

[10] Korberg, A. D., Brynolf, S., Grahn, M., & Skov, I. R. (2021). Techno-economic assessment of advanced fuels and propulsion systems in future fossil-free ships. Renewable and Sustainable Energy Reviews, 142, 110861.

[11] Wang, Y., & Wright, L. A. (2021). A comparative review of alternative fuels for the maritime sector: Economic, technology, and policy challenges for clean energy implementation. World, 2(4), 456--481.

[12] Lloyd's Register & UMAS. (2020). Techno-economic assessment of zero-carbon fuels.

[13] Verschuur, J., et al. (2024). Green shipping corridor infrastructure investment: Socio-economic and environmental impacts. Environmental Research: Infrastructure and Sustainability, 4(1), 015001.

[14] Yang, M., & Lam, J. S. L. (2023). Operational and economic evaluation of ammonia bunkering -- Bunkering supply chain perspective. Transportation Research Part D: Transport and Environment, 117, 103662.

[15] Fan, H., Enshaei, H., Jayasinghe, S. G., Tan, S. H., & Zhang, C. (2022). Quantitative risk assessment for ammonia ship-to-ship bunkering based on Bayesian network. Process Safety Progress, 41(3), 395--410.

[16] Yang, M., & Lam, J. S. L. (2024). Risk assessment of ammonia bunkering operations: Perspectives on different release scales. Journal of Hazardous Materials, 465, 133237.

[17] Kim, R. U., Yin, J., Wang, S., Hussein, M., Alqurashi, Y., & Al Sulaie, S. (2025). A system theoretic quantitative risk assessment for port ammonia bunkering operations. International Journal of Hydrogen Energy, 114, 556--569.

[18] Qu, W., Duinkerken, M. B., & Schott, D. L. (2024). A framework for risk assessment of ammonia storage and bunkering at ports. In Proceedings of the International Physical Internet Conference (IPIC 2024), TU Delft.

[19] Khan, M. S., Effendy, S., & Karimi, I. A. (2025). Ammonia bunkering in the maritime sector: A review. Ocean Engineering, 338, 121960.

[20] Wang, S. S., et al. (2022). Optimization of ammonia bunkering network configurations. Computer Aided Chemical Engineering, 49, 589--594.

[21] Dahlke-Wallat, F., et al. (2024). Ammonia bunkering infrastructure concepts: A techno-economic evaluation. In Proceedings of the International Marine Design Conference (IMDC 2024), TU Delft.

[22] Fagerholt, K. (2004). A computer-based decision support system for vessel fleet scheduling -- Experience and future research. Decision Support Systems, 37(1), 35--47.

[23] Christiansen, M., Fagerholt, K., Nygreen, B., & Ronen, D. (2013). Ship routing and scheduling in the new millennium. European Journal of Operational Research, 228(3), 467--483.

[24] Fagerholt, K., Hvattum, L. M., Johnsen, T. A. V., & Korsvik, J. E. (2023). Maritime inventory routing: Recent trends and future directions. International Transactions in Operational Research, 30(6), 3013--3056.

[25] Zhao, X., Wang, W., Song, X., & Peng, Y. (2025). Toward green container liner shipping: Joint optimization of heterogeneous fleet deployment, speed optimization, and fuel bunkering. International Transactions in Operational Research, 32(3), 1552--1580.

[26] Stalahane, M., Halvorsen-Weare, E. E., Nonas, L. M., & Pantuso, G. (2019). Optimizing vessel fleet size and mix to support maintenance operations at offshore wind farms. European Journal of Operational Research, 276(2), 495--509.

[27] Vieira, B. S., Mayerle, S. F., Campos, L. M. S., & Coelho, L. C. (2021). Exact and heuristic algorithms for the fleet composition and periodic routing problem of offshore supply vessels with berth allocation decisions. European Journal of Operational Research, 295(3), 908--923.

[28] Bakkehaug, R., Eidem, E. S., Fagerholt, K., & Hvattum, L. M. (2014). A stochastic programming formulation for strategic fleet renewal in shipping. Transportation Research Part E, 72, 60--76.

[29] Pantuso, G., Fagerholt, K., & Wallace, S. W. (2016). Uncertainty in fleet renewal: A case from maritime transportation. Transportation Science, 50(2), 390--407.

[30] Wang, Y., Fagerholt, K., & Wallace, S. W. (2018). Planning for charters: A stochastic maritime fleet composition and deployment problem. Omega, 79, 54--66.

[31] Tan, Z., Du, Z., Wang, X., Yang, Z., & Wu, L. (2024). Fleet sizing with time and voyage-chartered vessels under demand uncertainty. Transportation Research Part E, 192, 103810.

[32] Rodrigues, F., Agra, A., Christiansen, M., Hvattum, L. M., & Requejo, C. (2019). Comparing techniques for modelling uncertainty in a maritime inventory routing problem. European Journal of Operational Research, 277(3), 831--845.

[33] Doymus, M., Denktas-Sakar, G., Topaloglu Yildiz, S., & Acik, A. (2022). Small-scale LNG supply chain optimization for LNG bunkering in Turkey. Computers and Chemical Engineering, 162, 107789.

[34] Jokinen, R., Pettersson, F., & Saxen, H. (2015). An MILP model for optimization of a small-scale LNG supply chain along a coastline. Applied Energy, 138, 423--431.

[35] Pratama, G. A., et al. (2025). Multi-period optimization for LNG bunkering vessel fleet sizing and scheduling. Gas Science and Engineering, 143, 205742.

[36] Guo, Y., Yan, R., Qi, J., Liu, Y., Wang, S., & Zhen, L. (2024). LNG bunkering infrastructure planning at port. Multimodal Transportation, 3, 100134.

[37] He, J., Jin, Y., Pan, K., & Chen, J. (2024). Route, speed, and bunkering optimization for LNG-fueled tramp ship with alternative bunkering ports. Ocean Engineering, 305, 117996.

[38] Ntakolia, C., Douloumpekis, M., Papaleonidas, C., Tsiampa, V., & Lyridis, D. V. (2023). A stochastic modelling and optimization for the design of an LNG refuelling system in the Piraeus Port region. SN Operations Research Forum, 4, 59.

[39] Machfudiyanto, R. A., et al. (2023). LNG bunkering infrastructure feasibility at Indonesian ports. Heliyon, 9(8), e19047.

[40] Salmon, N., Banares-Alcantara, R., & Nayak-Luke, R. (2021). Optimization of green ammonia distribution systems for intercontinental energy transport. iScience, 24(8), 102903.

[41] Kim, H., Kim, J., & Lee, S. (2024). Technical-economic analysis for ammonia ocean transportation using an ammonia-fueled carrier. Sustainability, 16(2), 827.

[42] Wang, Y., Daoutidis, P., & Zhang, Q. (2023). Ammonia-based green corridors for sustainable maritime transportation. Digital Chemical Engineering, 6, 100082.

[43] Oxford Institute for Energy Studies. (2024). Fuelling the future: A techno-economic evaluation of e-ammonia production for maritime (ET40). Oxford, UK.

[44] Trivyza, N. L., Rentizelas, A., & Theotokatos, G. (2021). Design of ammonia-based green corridor networks. [Journal details to be completed].

[45] Fullerton, A., Lea-Langton, A. R., Madugu, F., & Larkin, A. (2025). Green ammonia adoption in shipping: Opportunities and challenges across the fuel supply chain. Marine Policy, 171, 106444.

---

*End of Sections 1--2. Sections 3--5 follow in a separate document.*
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

The model assumes vessels arrive uniformly throughout the year. In practice, seasonal and weekly demand peaks create queuing effects that could increase effective cycle time during peak periods. A conservative design margin partially compensates but does not replace a queuing model.

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
