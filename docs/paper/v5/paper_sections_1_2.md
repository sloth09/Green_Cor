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
