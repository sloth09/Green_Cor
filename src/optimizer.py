"""
MILP Optimization model for bunkering infrastructure.
Adapted from MILPmodel_v17_250811.py
"""

from math import ceil
from typing import Dict, List, Tuple
import pandas as pd
import pulp
import numpy as np

from .config_loader import ConfigLoader
from .cost_calculator import CostCalculator
from .cycle_time_calculator import CycleTimeCalculator
from .fleet_sizing_calculator import FleetSizingCalculator
from .shore_supply import ShoreSupply
from .utils import (
    interpolate_mcr,
    interpolate_sfoc,
    calculate_m3_per_voyage,
    calculate_bunker_volume_per_call,
    calculate_vessel_growth,
    calculate_annual_demand
)


class BunkeringOptimizer:
    """MILP optimizer for bunkering infrastructure planning."""

    def __init__(self, config: Dict):
        """
        Initialize optimizer with configuration.

        Args:
            config: Configuration dictionary from ConfigLoader
        """
        self.config = config
        self.cost_calc = CostCalculator(config)
        self.fleet_calc = FleetSizingCalculator(config)

        # Extract key parameters
        self._setup_parameters()

        # Results storage
        self.scenario_results = []
        self.yearly_results = []

    def _setup_parameters(self) -> None:
        """Setup and calculate all parameters from configuration."""
        # Time period
        self.start_year = self.config["time_period"]["start_year"]
        self.end_year = self.config["time_period"]["end_year"]
        self.years = list(range(self.start_year, self.end_year + 1))

        # Economic parameters
        self.discount_rate = self.config["economy"]["discount_rate"]
        self.fuel_price = self.config["economy"]["fuel_price_usd_per_ton"]

        # Shipping parameters
        self.kg_per_voyage = self.config["shipping"]["kg_per_voyage"]
        self.voyages_per_year = self.config["shipping"]["voyages_per_year"]

        # Bunkering call volume (load this first, as it's the source of truth for demand)
        self.bunker_volume_per_call_m3 = self.config["bunkering"]["bunker_volume_per_call_m3"]

        # Use bunker_volume_per_call_m3 as the source of truth for m3_per_voyage
        # (This overrides the kg_per_voyage conversion as intended by config)
        self.m3_per_voyage = self.bunker_volume_per_call_m3

        # Vessel growth
        self.vessel_growth = calculate_vessel_growth(
            self.start_year,
            self.end_year,
            self.config["shipping"]["start_vessels"],
            self.config["shipping"]["end_vessels"]
        )

        # Demand
        self.annual_demand = calculate_annual_demand(
            self.vessel_growth,
            self.m3_per_voyage,
            self.voyages_per_year
        )

        # Operational parameters
        self.travel_time_hours = self.config["operations"]["travel_time_hours"]
        self.setup_time_hours = self.config["operations"]["setup_time_hours"]
        self.max_annual_hours = self.config["operations"]["max_annual_hours_per_vessel"]
        self.tank_safety_factor = self.config["operations"]["tank_safety_factor"]
        self.daily_peak_factor = self.config["operations"]["daily_peak_factor"]
        self.transport_safety_factor = self.config["operations"]["transport_safety_factor"]

        # Propulsion parameters - default SFOC (fallback)
        self.sfoc_default = self.config["propulsion"]["sfoc_g_per_kwh"]

        # Shuttle sizes and MCR
        self.shuttle_sizes = self.config["shuttle"]["available_sizes_cbm"]

        # Interpolate MCR for all shuttle sizes
        base_mcr_map = self.config["shuttle"].get("mcr_map_kw", {})
        self.mcr_map = interpolate_mcr(base_mcr_map, self.shuttle_sizes)

        # Interpolate SFOC for all shuttle sizes (v4: MCR-based SFOC)
        base_sfoc_map = self.config.get("sfoc_map_g_per_kwh", {})
        self.sfoc_map = interpolate_sfoc(base_sfoc_map, self.shuttle_sizes, self.sfoc_default)

        # Pump sizes
        self.pump_sizes = self.config["pumps"]["available_flow_rates"]

        # Constraints
        self.max_call_hours = self.config["constraints"]["max_call_duration_hours"]

        # Tank parameters
        self.tank_enabled = self.config["tank_storage"]["enabled"]
        self.has_storage_at_busan = self.config["operations"].get("has_storage_at_busan", True)
        if self.tank_enabled:
            self.tank_capex = self.cost_calc.calculate_tank_capex()
            self.tank_fixed_opex = self.cost_calc.calculate_tank_fixed_opex()
            self.tank_variable_opex = self.cost_calc.calculate_tank_variable_opex()
            self.tank_volume_m3 = self.cost_calc.calculate_tank_volume_m3()

        # Shore supply parameters (controls cost inclusion, not time)
        self.shore_supply_enabled = self.config["shore_supply"].get("enabled", False)
        if self.shore_supply_enabled:
            self.shore_pump_capex = self.cost_calc.calculate_shore_pump_capex()
            self.shore_pump_fixed_opex = self.cost_calc.calculate_shore_pump_fixed_opex()
            self.shore_pump_variable_opex_per_hr = self.cost_calc.calculate_shore_pump_variable_opex_per_hour()
        else:
            self.shore_pump_capex = 0.0
            self.shore_pump_fixed_opex = 0.0
            self.shore_pump_variable_opex_per_hr = 0.0

        # Initialize cycle time calculator and shore supply manager
        self.cycle_calc = CycleTimeCalculator(self.config.get("case_id", "case_1"), self.config)
        self.shore_supply = ShoreSupply(self.config)

    def solve(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Solve optimization problem for all shuttle/pump combinations.

        Returns:
            Tuple of (scenario_results_df, yearly_results_df)
        """
        print(f"Starting optimization for case: {self.config.get('case_name', 'Unknown')}")
        print(f"Time period: {self.start_year}-{self.end_year}")
        print(f"Shuttle sizes: {len(self.shuttle_sizes)}, Pump sizes: {len(self.pump_sizes)}")

        self.scenario_results = []
        self.yearly_results = []

        # Loop over all shuttle/pump combinations
        total_combinations = len(self.shuttle_sizes) * len(self.pump_sizes)
        current = 0

        for shuttle_size in self.shuttle_sizes:
            for pump_size in self.pump_sizes:
                current += 1
                self._solve_combination(shuttle_size, pump_size)

                if current % 10 == 0:
                    progress = (current / total_combinations) * 100
                    print(f"Progress: {current}/{total_combinations} ({progress:.1f}%)")

        print(f"Optimization complete. Feasible solutions: {len(self.scenario_results)}")

        # Convert to DataFrames
        scenario_df = pd.DataFrame(self.scenario_results)
        yearly_df = pd.DataFrame(self.yearly_results)

        return scenario_df, yearly_df

    def _solve_combination(self, shuttle_size: float, pump_size: float) -> None:
        """
        Solve MILP for a specific shuttle/pump combination.

        Args:
            shuttle_size: Shuttle size in m3
            pump_size: Pump flow rate in m3/h
        """
        # Pre-screening calculations
        shuttle_size_int = int(shuttle_size)
        pump_size_int = int(pump_size)

        # Get MCR value
        mcr = self.mcr_map.get(shuttle_size_int, 0)
        if mcr == 0:
            return  # Skip if MCR not available

        # Use CycleTimeCalculator to get complete timing breakdown
        # Determine number of vessels per trip for Case 2
        if self.has_storage_at_busan:
            num_vessels = 1  # Case 1: Not used
        else:
            # Case 2: Calculate vessels per trip based on shuttle size
            num_vessels = max(1, int(shuttle_size // self.bunker_volume_per_call_m3))

        cycle_info = self.cycle_calc.calculate_single_cycle(shuttle_size, pump_size, num_vessels)

        # Extract timing information
        call_duration = cycle_info["call_duration"]
        cycle_duration = cycle_info["cycle_duration"]
        trips_per_call = cycle_info["trips_per_call"]

        # Check call duration constraint
        if call_duration > self.max_call_hours:
            return  # Skip infeasible combination

        # Get SFOC for this shuttle size (v4: MCR-based SFOC map)
        sfoc = self.sfoc_map.get(shuttle_size_int, self.sfoc_default)

        # Calculate fuel costs using timing from cycle calculator
        # For Case 1: One-way travel; Case 2: Round-trip travel
        travel_factor = 1.0 if self.has_storage_at_busan else 2.0
        shuttle_fuel_per_cycle = (mcr * sfoc * travel_factor * self.travel_time_hours) / 1e6
        shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * self.fuel_price

        # Pump fuel cost based on pumping time per bunkering call
        # Both Case 1 and Case 2: One bunkering call = one pumping event = 5000 m³
        # The difference is in how many shuttle trips are needed:
        # - Case 1: Multiple shuttle trips for one call (shuttle < bunker_volume)
        # - Case 2: Multiple calls per shuttle trip (shuttle > bunker_volume)
        # But pump is activated PER CALL, not per trip
        pumping_time_hr_call = self.bunker_volume_per_call_m3 / pump_size

        pump_fuel_per_call = (self.cost_calc.calculate_pump_power(pump_size,
                                                                   self.config["propulsion"]["pump_delta_pressure_bar"],
                                                                   self.config["propulsion"]["pump_efficiency"]) *
                             pumping_time_hr_call * sfoc) / 1e6
        pump_fuel_cost_per_call = pump_fuel_per_call * self.fuel_price

        # Cost components
        shuttle_capex = self.cost_calc.calculate_shuttle_capex(shuttle_size)
        shuttle_fixed_opex = self.cost_calc.calculate_shuttle_fixed_opex(shuttle_size)
        bunk_capex = self.cost_calc.calculate_bunkering_capex(shuttle_size, pump_size)
        bunk_fixed_opex = self.cost_calc.calculate_bunkering_fixed_opex(shuttle_size, pump_size)

        # Tank costs (only if tank is enabled AND shore_supply cost is enabled)
        if self.tank_enabled and self.shore_supply_enabled:
            tank_capex = self.tank_capex
            tank_fixed_opex = self.tank_fixed_opex
            tank_variable_opex = self.tank_variable_opex
        else:
            tank_capex = tank_fixed_opex = tank_variable_opex = 0.0

        # Shore supply pump costs (only if shore_supply cost is enabled)
        # NOTE: Shore supply TIME is always included in cycle calculations
        # Only the COST is controlled by shore_supply.enabled
        if self.shore_supply_enabled:
            shore_pump_capex = self.shore_pump_capex
            shore_pump_fixed_opex = self.shore_pump_fixed_opex
        else:
            shore_pump_capex = shore_pump_fixed_opex = 0.0

        # Build MILP model
        prob = pulp.LpProblem(f"Bunkering_{shuttle_size_int}_{pump_size_int}", pulp.LpMinimize)

        # Decision variables
        x = pulp.LpVariable.dicts("NewShuttles", self.years, lowBound=0, cat='Integer')
        N = pulp.LpVariable.dicts("TotalShuttles", self.years, lowBound=0, cat='Integer')
        y = pulp.LpVariable.dicts("AnnualCalls", self.years, lowBound=0, cat='Continuous')

        x_tank = pulp.LpVariable.dicts("NewTanks", self.years, lowBound=0, cat='Integer')
        N_tank = pulp.LpVariable.dicts("TotalTanks", self.years, lowBound=0, cat='Integer')

        # Objective function
        obj_terms = []
        for i, t in enumerate(self.years):
            disc_factor = 1.0 / ((1.0 + self.discount_rate) ** (t - self.start_year))

            cycles = y[t] * trips_per_call

            capex = (shuttle_capex + bunk_capex) * x[t]
            if self.tank_enabled and self.shore_supply_enabled:
                capex += tank_capex * x_tank[t]

            # Shore pump CAPEX: one-time cost in first year only
            if i == 0 and self.shore_supply_enabled:
                capex += shore_pump_capex

            fixed_opex = (shuttle_fixed_opex + bunk_fixed_opex) * N[t]
            if self.tank_enabled and self.shore_supply_enabled:
                fixed_opex += tank_fixed_opex * N_tank[t]

            # Shore pump Fixed OPEX: annual maintenance cost (always included if enabled)
            if self.shore_supply_enabled:
                fixed_opex += shore_pump_fixed_opex

            variable_opex = shuttle_fuel_cost_per_cycle * cycles + pump_fuel_cost_per_call * y[t]
            if self.tank_enabled and self.shore_supply_enabled:
                variable_opex += tank_variable_opex * N_tank[t]

            obj_terms.append(disc_factor * (capex + fixed_opex + variable_opex))

        prob += pulp.lpSum(obj_terms)

        # Constraints
        for i, t in enumerate(self.years):
            # Inventory balance
            if t == self.years[0]:
                prob += N[t] == x[t]
                if self.tank_enabled and self.shore_supply_enabled:
                    prob += N_tank[t] == x_tank[t]
                else:
                    # When tank is disabled, force N_tank to 0
                    prob += N_tank[t] == 0
            else:
                prob += N[t] == N[self.years[i - 1]] + x[t]
                if self.tank_enabled and self.shore_supply_enabled:
                    prob += N_tank[t] == N_tank[self.years[i - 1]] + x_tank[t]
                else:
                    # When tank is disabled, force N_tank to 0
                    prob += N_tank[t] == 0

            # Demand satisfaction
            # NOTE: y[t] represents ANNUAL VESSEL BUNKERING CALLS for BOTH cases
            # Case 1: Each call delivers bunker_volume_per_call (5000 m³)
            # Case 2: Each call ALSO delivers bunker_volume_per_call (5000 m³)
            #         (shuttle may serve multiple vessels per trip, but y[t] counts calls, not trips)
            # UNIFIED LOGIC: Both use bunker_volume_per_call
            prob += y[t] * self.bunker_volume_per_call_m3 >= self.annual_demand[t]

            # Working time capacity
            prob += y[t] * trips_per_call * cycle_duration <= N[t] * self.max_annual_hours

            # Tank capacity (if both tank and shore_supply costs are enabled)
            # CRITICAL: Tank constraint must respect shore_supply.enabled flag
            # When shore_supply.enabled=false, tank facility is not considered (constraint disabled)
            if self.tank_enabled and self.shore_supply_enabled:
                tank_capacity = N_tank[t] * self.tank_volume_m3
                prob += N[t] * shuttle_size * self.tank_safety_factor <= tank_capacity

            # Fleet sizing note:
            # Working time constraint (line 280) is the binding constraint for fleet sizing.
            # This ensures consistency with main.py's annual_simulation, which uses:
            #   required_shuttles = ceil((annual_calls × trips_per_call × cycle_duration) / max_annual_hours)
            # Removed daily peak constraint to match the proven baseline (annual_simulation)

        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        status = pulp.LpStatus[prob.status]
        if status != "Optimal":
            return  # Skip infeasible solutions

        # Extract and store results
        self._extract_results(
            shuttle_size, pump_size, x, N, y, x_tank, N_tank,
            call_duration, cycle_duration,
            shuttle_fuel_cost_per_cycle, pump_fuel_cost_per_call,
            shuttle_capex, shuttle_fixed_opex, bunk_capex, bunk_fixed_opex,
            trips_per_call,
            cycle_info  # Pass complete time breakdown
        )

    def _extract_results(self,
                        shuttle_size: float, pump_size: float,
                        x, N, y, x_tank, N_tank,
                        call_duration: float, cycle_duration: float,
                        shuttle_fuel_per_cycle: float, pump_fuel_per_call: float,
                        shuttle_capex: float, shuttle_fixed_opex: float,
                        bunk_capex: float, bunk_fixed_opex: float,
                        trips_per_call: int,
                        cycle_info: dict) -> None:
        """Extract results from optimized MILP solution."""
        shuttle_size_int = int(shuttle_size)
        pump_size_int = int(pump_size)

        # Calculate NPC using Annualized CAPEX methodology
        # This ensures fair comparison across scenarios with different asset purchase timing
        # and automatically accounts for salvage value of assets purchased late in project
        npc_total = 0.0
        npc_shuttle_cap = npc_shuttle_fop = npc_shuttle_vop = 0.0
        npc_bunk_cap = npc_bunk_fop = npc_bunk_vop = 0.0
        npc_tank_cap = npc_tank_fop = npc_tank_vop = 0.0

        for t in self.years:
            disc_factor = 1.0 / ((1.0 + self.discount_rate) ** (t - self.start_year))

            x_val = x[t].varValue
            N_val = N[t].varValue
            y_val = y[t].varValue

            cycles = y_val * trips_per_call

            # ANNUALIZED CAPEX (instead of actual CAPEX spending)
            # Calculate total asset value owned in this year
            total_shuttle_asset = N_val * shuttle_capex
            total_bunk_asset = N_val * bunk_capex
            total_tank_asset = 0.0
            if self.tank_enabled and self.shore_supply_enabled:
                N_tank_val = N_tank[t].varValue
                total_tank_asset = N_tank_val * self.tank_capex

            # Convert to annualized CAPEX (same methodology as yearly_simulation)
            annualized_shuttle_capex = self.cost_calc.calculate_annualized_capex_yearly(total_shuttle_asset)
            annualized_bunk_capex = self.cost_calc.calculate_annualized_capex_yearly(total_bunk_asset)
            annualized_tank_capex = self.cost_calc.calculate_annualized_capex_yearly(total_tank_asset)

            # Accumulate annualized CAPEX
            npc_shuttle_cap += disc_factor * annualized_shuttle_capex
            npc_bunk_cap += disc_factor * annualized_bunk_capex
            npc_tank_cap += disc_factor * annualized_tank_capex

            # Fixed OPEX (unchanged)
            npc_shuttle_fop += disc_factor * shuttle_fixed_opex * N_val
            npc_bunk_fop += disc_factor * bunk_fixed_opex * N_val
            if self.tank_enabled and self.shore_supply_enabled:
                npc_tank_fop += disc_factor * self.tank_fixed_opex * N_tank_val

            # Variable OPEX (unchanged)
            shuttle_vop = shuttle_fuel_per_cycle * cycles
            bunk_vop = pump_fuel_per_call * y_val
            npc_shuttle_vop += disc_factor * shuttle_vop
            npc_bunk_vop += disc_factor * bunk_vop
            if self.tank_enabled and self.shore_supply_enabled:
                npc_tank_vop += disc_factor * self.tank_variable_opex * N_tank_val

            # Total NPC for this year = Annualized CAPEX + OPEX
            npc_total += disc_factor * (
                annualized_shuttle_capex + annualized_bunk_capex + annualized_tank_capex +
                shuttle_fixed_opex * N_val + bunk_fixed_opex * N_val +
                shuttle_vop + bunk_vop
            )
            if self.tank_enabled and self.shore_supply_enabled:
                npc_total += disc_factor * (
                    self.tank_fixed_opex * N_tank_val +
                    self.tank_variable_opex * N_tank_val
                )

        # Calculate annualized costs and LCOAmmonia
        annuity_factor = self.cost_calc.get_annuity_factor()

        # Calculate total supply over 20 years for LCOAmmonia
        # NOTE: y[t] represents annual vessel bunkering calls for BOTH cases
        # This is now unified for consistency with demand constraint and yearly results
        total_supply_m3 = 0.0
        for t in self.years:
            y_val = y[t].varValue
            # Both Case 1 and Case 2: Each call delivers bunker_volume_per_call (5000 m³)
            total_supply_m3 += y_val * self.bunker_volume_per_call_m3

        # Convert supply from m³ to tons for LCOAmmonia calculation
        density_storage = self.config["ammonia"]["density_storage_ton_m3"]
        total_supply_ton = total_supply_m3 * density_storage

        # Avoid division by zero for LCOAmmonia
        lco_ammonia = (npc_total / total_supply_ton) if total_supply_ton > 0 else 0.0

        # Calculate annualized cost components
        npc_total_capex = npc_shuttle_cap + npc_bunk_cap + npc_tank_cap
        npc_total_fopex = npc_shuttle_fop + npc_bunk_fop + npc_tank_fop
        npc_total_vopex = npc_shuttle_vop + npc_bunk_vop + npc_tank_vop

        annualized_total = self.cost_calc.annualize_scenario_npc(npc_total)
        annualized_capex = self.cost_calc.annualize_scenario_npc(npc_total_capex)
        annualized_fopex = self.cost_calc.annualize_scenario_npc(npc_total_fopex)
        annualized_vopex = self.cost_calc.annualize_scenario_npc(npc_total_vopex)

        # Calculate additional time metrics
        # NOTE: These are THEORETICAL MAXIMUMS for a single shuttle at 100% utilization
        # Actual supply from optimization (y[t]) will be lower or equal based on demand
        annual_cycles_max = 8000 / cycle_duration if cycle_duration > 0 else 0
        annual_supply_m3 = annual_cycles_max * shuttle_size  # MAXIMUM theoretical supply
        time_utilization_ratio = (annual_cycles_max * cycle_duration / 8000) * 100 if cycle_duration > 0 else 0
        vessels_per_trip = cycle_info.get("vessels_per_trip", 1)

        # Scenario summary
        self.scenario_results.append({
            # Identification and timing
            "Shuttle_Size_cbm": shuttle_size_int,
            "Pump_Size_m3ph": pump_size_int,
            "Call_Duration_hr": round(call_duration, 4),
            "Cycle_Duration_hr": round(cycle_duration, 4),
            "Trips_per_Call": round(float(trips_per_call), 4),

            # ===== TIME BREAKDOWN (HOURS) =====
            "Shore_Loading_hr": round(cycle_info.get("shore_loading", 0), 4),
            "Travel_Outbound_hr": round(cycle_info.get("travel_outbound", 0), 4),
            "Travel_Return_hr": round(cycle_info.get("travel_return", 0), 4),
            "Setup_Inbound_hr": round(cycle_info.get("setup_inbound", 0), 4),
            "Setup_Outbound_hr": round(cycle_info.get("setup_outbound", 0), 4),
            "Pumping_Per_Vessel_hr": round(cycle_info.get("pumping_per_vessel", 0), 4),
            "Pumping_Total_hr": round(cycle_info.get("pumping_total", 0), 4),
            "Basic_Cycle_Duration_hr": round(cycle_info.get("basic_cycle_duration", 0), 4),

            # ===== OPERATIONAL METRICS (THEORETICAL MAXIMUM - 100% UTILIZATION) =====
            # NOTE: Annual_Cycles_Max, Annual_Supply_m3, Ships_Per_Year show maximum theoretical capacity
            # Actual optimization results may use lower values based on demand constraints
            "Annual_Cycles_Max": round(annual_cycles_max, 2),
            "Vessels_per_Trip": round(float(vessels_per_trip), 4),
            "Annual_Supply_m3": round(annual_supply_m3, 0),  # Maximum theoretical supply per shuttle
            "Ships_Per_Year": round(annual_supply_m3 / self.bunker_volume_per_call_m3, 2),  # Maximum theoretical
            "Time_Utilization_Ratio_percent": round(time_utilization_ratio, 2),

            # ===== NPC (20-YEAR NET PRESENT COST, MILLIONS USD) =====
            # NOTE: CAPEX components use Annualized CAPEX methodology (not actual spending)
            # This ensures fair comparison across scenarios with different asset purchase timing
            # NPC_Total = Σ(Annualized_CAPEX[year] + OPEX[year]) for years 2030-2050
            # Annualized CAPEX automatically accounts for salvage value of late purchases
            "NPC_Total_USDm": round(npc_total / 1e6, 2),
            "NPC_Annualized_Shuttle_CAPEX_USDm": round(npc_shuttle_cap / 1e6, 2),
            "NPC_Annualized_Bunkering_CAPEX_USDm": round(npc_bunk_cap / 1e6, 2),
            "NPC_Annualized_Terminal_CAPEX_USDm": round(npc_tank_cap / 1e6, 2),
            "NPC_Shuttle_fOPEX_USDm": round(npc_shuttle_fop / 1e6, 2),
            "NPC_Bunkering_fOPEX_USDm": round(npc_bunk_fop / 1e6, 2),
            "NPC_Terminal_fOPEX_USDm": round(npc_tank_fop / 1e6, 2),
            "NPC_Shuttle_vOPEX_USDm": round(npc_shuttle_vop / 1e6, 2),
            "NPC_Bunkering_vOPEX_USDm": round(npc_bunk_vop / 1e6, 2),
            "NPC_Terminal_vOPEX_USDm": round(npc_tank_vop / 1e6, 2),

            # ===== ANNUALIZED COSTS (ANNUAL EQUIVALENT, MILLIONS USD/YEAR) =====
            "Annuity_Factor": round(annuity_factor, 4),
            "Annualized_Cost_USDm_per_year": round(annualized_total / 1e6, 2),
            "Annualized_CAPEX_USDm_per_year": round(annualized_capex / 1e6, 2),
            "Annualized_FixedOPEX_USDm_per_year": round(annualized_fopex / 1e6, 2),
            "Annualized_VariableOPEX_USDm_per_year": round(annualized_vopex / 1e6, 2),

            # ===== LEVELIZED COST OF AMMONIA (USD/TON) =====
            "Total_Supply_20yr_ton": round(total_supply_ton, 2),
            "LCOAmmonia_USD_per_ton": round(lco_ammonia, 2),
        })

        # Yearly results
        for t in self.years:
            disc_factor = 1.0 / ((1.0 + self.discount_rate) ** (t - self.start_year))

            x_val = x[t].varValue
            N_val = N[t].varValue
            y_val = y[t].varValue

            cycles = y_val * trips_per_call
            supply = y_val * self.bunker_volume_per_call_m3
            demand = self.annual_demand[t]
            cycles_avail = N_val * (self.max_annual_hours / cycle_duration) if N_val > 0 else 0

            # ===== COST BREAKDOWN (DISCOUNTED) =====
            # Actual CAPEX costs (actual spending in this year - for reference)
            capex_shuttle_usd = disc_factor * shuttle_capex * x_val
            capex_pump_usd = disc_factor * bunk_capex * x_val
            capex_tank_usd = 0.0
            if self.tank_enabled and self.shore_supply_enabled:
                x_tank_val = x_tank[t].varValue
                if x_tank_val is not None:
                    capex_tank_usd = disc_factor * self.tank_capex * x_tank_val

            capex_total_usd = capex_shuttle_usd + capex_pump_usd + capex_tank_usd

            # Fixed OPEX costs
            fopex_shuttle_usd = disc_factor * shuttle_fixed_opex * N_val
            fopex_pump_usd = disc_factor * bunk_fixed_opex * N_val
            fopex_tank_usd = 0.0
            if self.tank_enabled and self.shore_supply_enabled:
                N_tank_val = N_tank[t].varValue
                if N_tank_val is not None:
                    fopex_tank_usd = disc_factor * self.tank_fixed_opex * N_tank_val

            fopex_total_usd = fopex_shuttle_usd + fopex_pump_usd + fopex_tank_usd

            # Variable OPEX costs
            shuttle_vop = shuttle_fuel_per_cycle * cycles
            pump_vop = pump_fuel_per_call * y_val
            vopex_shuttle_usd = disc_factor * shuttle_vop
            vopex_pump_usd = disc_factor * pump_vop
            vopex_tank_usd = 0.0
            if self.tank_enabled:
                N_tank_val = N_tank[t].varValue
                vopex_tank_usd = disc_factor * self.tank_variable_opex * N_tank_val

            vopex_total_usd = vopex_shuttle_usd + vopex_pump_usd + vopex_tank_usd

            # Calculate Total OPEX (Fixed + Variable)
            total_opex_usd = fopex_total_usd + vopex_total_usd

            # ===== CALCULATE ANNUALIZED CAPEX (for year-by-year comparison) =====
            # Calculate total asset value for this year (owned shuttles + equipment)
            total_shuttle_asset_usd = N_val * shuttle_capex
            total_pump_asset_usd = N_val * bunk_capex
            total_tank_asset_usd = 0.0
            if self.tank_enabled and self.shore_supply_enabled:
                N_tank_val = N_tank[t].varValue
                if N_tank_val is not None:
                    total_tank_asset_usd = N_tank_val * self.tank_capex

            # Calculate annualized CAPEX (consistent across years for owned assets)
            annualized_shuttle_capex_usd = self.cost_calc.calculate_annualized_capex_yearly(total_shuttle_asset_usd)
            annualized_pump_capex_usd = self.cost_calc.calculate_annualized_capex_yearly(total_pump_asset_usd)
            annualized_tank_capex_usd = self.cost_calc.calculate_annualized_capex_yearly(total_tank_asset_usd)
            annualized_total_capex_usd = annualized_shuttle_capex_usd + annualized_pump_capex_usd + annualized_tank_capex_usd

            # Total Year Cost = Annualized CAPEX + Total OPEX (consistent with yearly_simulation)
            total_year_cost_usd = annualized_total_capex_usd + total_opex_usd

            # Calculate additional time and efficiency metrics
            total_hours_needed = cycles * cycle_duration
            total_hours_available = N_val * self.max_annual_hours
            hours_per_shuttle_used = total_hours_needed / N_val if N_val > 0 else 0
            cycles_per_shuttle = cycles / N_val if N_val > 0 else 0
            time_per_vessel_call = cycle_duration * trips_per_call

            self.yearly_results.append({
                # Identification
                "Shuttle_Size_cbm": shuttle_size_int,
                "Pump_Size_m3ph": pump_size_int,
                "Year": t,
                # Assets
                "New_Shuttles": int(round(x_val)),
                "Total_Shuttles": int(round(N_val)),
                # ===== CYCLE TIME BREAKDOWN =====
                "Cycle_Duration_Hours": round(cycle_duration, 2),
                "Shore_Loading_Hours": round(cycle_info.get('shore_loading', 0), 2),
                "Pumping_Per_Trip_Hours": round(cycle_info.get('pumping_per_vessel', 0), 2),
                "Travel_Outbound_Hours": round(cycle_info.get('travel_outbound', 0), 4),
                "Travel_Return_Hours": round(cycle_info.get('travel_return', 0), 4),
                "Setup_Total_Hours": round(cycle_info.get('setup_inbound', 0) + cycle_info.get('setup_outbound', 0), 4),
                # ===== TRIP CALCULATION DETAILS =====
                "Trips_Per_Call": round(float(trips_per_call), 4),
                "Vessels_Per_Trip": round(float(vessels_per_trip), 4),
                "Time_Per_Vessel_Call_Hours": round(time_per_vessel_call, 2),
                # ===== OPERATIONS =====
                "Annual_Calls": round(y_val, 1),
                "Annual_Cycles": round(cycles, 0),
                "Supply_m3": round(supply, 0),
                "Demand_m3": round(demand, 0),
                "Cycles_Available": round(cycles_avail, 1),
                "Utilization_Rate": round((cycles / cycles_avail) if cycles_avail > 0 else 0, 4),
                # ===== TIME ANALYSIS =====
                "Total_Hours_Needed": round(total_hours_needed, 0),
                "Total_Hours_Available": round(total_hours_available, 0),
                "Hours_Per_Shuttle_Used": round(hours_per_shuttle_used, 0),
                "Cycles_Per_Shuttle": round(cycles_per_shuttle, 1),
                # ===== ACTUAL CAPEX (REFERENCE ONLY - actual spending in this year) =====
                "Actual_CAPEX_Shuttle_USDm": round(capex_shuttle_usd / 1e6, 4),
                "Actual_CAPEX_Pump_USDm": round(capex_pump_usd / 1e6, 4),
                "Actual_CAPEX_Tank_USDm": round(capex_tank_usd / 1e6, 4),
                "Actual_CAPEX_Total_USDm": round(capex_total_usd / 1e6, 4),
                # ===== ANNUALIZED CAPEX (USED FOR TOTAL COST CALCULATION) =====
                "Annualized_CAPEX_Shuttle_USDm": round(annualized_shuttle_capex_usd / 1e6, 4),
                "Annualized_CAPEX_Pump_USDm": round(annualized_pump_capex_usd / 1e6, 4),
                "Annualized_CAPEX_Tank_USDm": round(annualized_tank_capex_usd / 1e6, 4),
                "Annualized_CAPEX_Total_USDm": round(annualized_total_capex_usd / 1e6, 4),
                # ===== OPEX =====
                # Fixed OPEX
                "FixedOPEX_Shuttle_USDm": round(fopex_shuttle_usd / 1e6, 4),
                "FixedOPEX_Pump_USDm": round(fopex_pump_usd / 1e6, 4),
                "FixedOPEX_Tank_USDm": round(fopex_tank_usd / 1e6, 4),
                "FixedOPEX_Total_USDm": round(fopex_total_usd / 1e6, 4),
                # Variable OPEX
                "VariableOPEX_Shuttle_USDm": round(vopex_shuttle_usd / 1e6, 4),
                "VariableOPEX_Pump_USDm": round(vopex_pump_usd / 1e6, 4),
                "VariableOPEX_Tank_USDm": round(vopex_tank_usd / 1e6, 4),
                "VariableOPEX_Total_USDm": round(vopex_total_usd / 1e6, 4),
                # Total OPEX (Fixed + Variable)
                "Total_OPEX_USDm": round(total_opex_usd / 1e6, 4),
                # ===== TOTAL YEAR COST (ANNUALIZED CAPEX + OPEX) =====
                "Total_Year_Cost_USDm": round(total_year_cost_usd / 1e6, 4),
                "Discount_Factor": round(disc_factor, 4),
            })
