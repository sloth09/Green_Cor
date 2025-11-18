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
from .shore_supply import ShoreSupply
from .utils import (
    interpolate_mcr,
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
        self.m3_per_voyage = calculate_m3_per_voyage(
            self.kg_per_voyage,
            self.config["ammonia"]["density_storage_ton_m3"]
        )

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

        # Bunkering call volume
        self.bunker_volume_per_call_m3 = self.config["bunkering"]["bunker_volume_per_call_m3"]

        # Operational parameters
        self.travel_time_hours = self.config["operations"]["travel_time_hours"]
        self.setup_time_hours = self.config["operations"]["setup_time_hours"]
        self.max_annual_hours = self.config["operations"]["max_annual_hours_per_vessel"]
        self.tank_safety_factor = self.config["operations"]["tank_safety_factor"]
        self.daily_peak_factor = self.config["operations"]["daily_peak_factor"]
        self.transport_safety_factor = self.config["operations"]["transport_safety_factor"]

        # Propulsion parameters
        self.sfoc = self.config["propulsion"]["sfoc_g_per_kwh"]

        # Shuttle sizes and MCR
        self.shuttle_sizes = self.config["shuttle"]["available_sizes_cbm"]

        # Interpolate MCR for all shuttle sizes
        base_mcr_map = self.config["shuttle"].get("mcr_map_kw", {})
        self.mcr_map = interpolate_mcr(base_mcr_map, self.shuttle_sizes)

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

        # Calculate fuel costs using timing from cycle calculator
        # For Case 1: One-way travel; Case 2: Round-trip travel
        travel_factor = 1.0 if self.has_storage_at_busan else 2.0
        shuttle_fuel_per_cycle = (mcr * self.sfoc * travel_factor * self.travel_time_hours) / 1e6
        shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * self.fuel_price

        # Pump fuel cost based on actual pumping time
        # Case 1: Time to pump one call (5000 m³)
        # Case 2: Time to pump full shuttle
        if self.has_storage_at_busan:
            pumping_time_hr_call = 2.0 * (self.bunker_volume_per_call_m3 / pump_size)
        else:
            pumping_time_hr_call = 2.0 * (shuttle_size / pump_size)

        pump_fuel_per_call = (self.cost_calc.calculate_pump_power(pump_size,
                                                                   self.config["propulsion"]["pump_delta_pressure_bar"],
                                                                   self.config["propulsion"]["pump_efficiency"]) *
                             pumping_time_hr_call * self.sfoc) / 1e6
        pump_fuel_cost_per_call = pump_fuel_per_call * self.fuel_price

        # Cost components
        shuttle_capex = self.cost_calc.calculate_shuttle_capex(shuttle_size)
        shuttle_fixed_opex = self.cost_calc.calculate_shuttle_fixed_opex(shuttle_size)
        bunk_capex = self.cost_calc.calculate_bunkering_capex(shuttle_size, pump_size)
        bunk_fixed_opex = self.cost_calc.calculate_bunkering_fixed_opex(shuttle_size, pump_size)

        if self.tank_enabled:
            tank_capex = self.tank_capex
            tank_fixed_opex = self.tank_fixed_opex
            tank_variable_opex = self.tank_variable_opex
        else:
            tank_capex = tank_fixed_opex = tank_variable_opex = 0.0

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
        for t in self.years:
            disc_factor = 1.0 / ((1.0 + self.discount_rate) ** (t - self.start_year))

            cycles = y[t] * trips_per_call

            capex = (shuttle_capex + bunk_capex) * x[t]
            if self.tank_enabled:
                capex += tank_capex * x_tank[t]

            fixed_opex = (shuttle_fixed_opex + bunk_fixed_opex) * N[t]
            if self.tank_enabled:
                fixed_opex += tank_fixed_opex * N_tank[t]

            variable_opex = shuttle_fuel_cost_per_cycle * cycles + pump_fuel_cost_per_call * y[t]
            if self.tank_enabled:
                variable_opex += tank_variable_opex * N_tank[t]

            obj_terms.append(disc_factor * (capex + fixed_opex + variable_opex))

        prob += pulp.lpSum(obj_terms)

        # Constraints
        for i, t in enumerate(self.years):
            # Inventory balance
            if t == self.years[0]:
                prob += N[t] == x[t]
                if self.tank_enabled:
                    prob += N_tank[t] == x_tank[t]
            else:
                prob += N[t] == N[self.years[i - 1]] + x[t]
                if self.tank_enabled:
                    prob += N_tank[t] == N_tank[self.years[i - 1]] + x_tank[t]

            # Demand satisfaction
            # For Case 2 (no storage): y[t] represents trips, each delivering full shuttle capacity
            # For Case 1 (with storage): y[t] represents calls, each delivering bunker_volume_per_call
            if self.has_storage_at_busan:
                prob += y[t] * self.bunker_volume_per_call_m3 >= self.annual_demand[t]
            else:
                prob += y[t] * shuttle_size >= self.annual_demand[t]

            # Working time capacity
            prob += y[t] * trips_per_call * cycle_duration <= N[t] * self.max_annual_hours

            # Tank capacity (if enabled)
            if self.tank_enabled:
                tank_capacity = N_tank[t] * self.tank_volume_m3
                prob += N[t] * shuttle_size * self.tank_safety_factor <= tank_capacity

            # Daily peak demand
            # Case 2: y[t] is trips, each delivering full shuttle_size
            # Case 1: y[t] is calls, each delivering bunker_volume_per_call
            if self.has_storage_at_busan:
                daily_demand = (y[t] / 365.0) * self.bunker_volume_per_call_m3 * self.daily_peak_factor
            else:
                daily_demand = (y[t] / 365.0) * shuttle_size * self.daily_peak_factor
            daily_capacity = (N[t] * (self.max_annual_hours / cycle_duration) / 365.0) * shuttle_size
            prob += daily_capacity >= daily_demand

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
            trips_per_call
        )

    def _extract_results(self,
                        shuttle_size: float, pump_size: float,
                        x, N, y, x_tank, N_tank,
                        call_duration: float, cycle_duration: float,
                        shuttle_fuel_per_cycle: float, pump_fuel_per_call: float,
                        shuttle_capex: float, shuttle_fixed_opex: float,
                        bunk_capex: float, bunk_fixed_opex: float,
                        trips_per_call: int) -> None:
        """Extract results from optimized MILP solution."""
        shuttle_size_int = int(shuttle_size)
        pump_size_int = int(pump_size)

        # Calculate NPV and components
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

            # CAPEX
            npc_shuttle_cap += disc_factor * shuttle_capex * x_val
            npc_bunk_cap += disc_factor * bunk_capex * x_val
            if self.tank_enabled:
                x_tank_val = x_tank[t].varValue
                npc_tank_cap += disc_factor * self.tank_capex * x_tank_val

            # Fixed OPEX
            npc_shuttle_fop += disc_factor * shuttle_fixed_opex * N_val
            npc_bunk_fop += disc_factor * bunk_fixed_opex * N_val
            if self.tank_enabled:
                N_tank_val = N_tank[t].varValue
                npc_tank_fop += disc_factor * self.tank_fixed_opex * N_tank_val

            # Variable OPEX
            shuttle_vop = shuttle_fuel_per_cycle * cycles
            bunk_vop = pump_fuel_per_call * y_val
            npc_shuttle_vop += disc_factor * shuttle_vop
            npc_bunk_vop += disc_factor * bunk_vop
            if self.tank_enabled:
                N_tank_val = N_tank[t].varValue
                npc_tank_vop += disc_factor * self.tank_variable_opex * N_tank_val

            npc_total += disc_factor * (
                shuttle_capex * x_val + bunk_capex * x_val +
                shuttle_fixed_opex * N_val + bunk_fixed_opex * N_val +
                shuttle_vop + bunk_vop
            )
            if self.tank_enabled:
                npc_total += disc_factor * (
                    self.tank_capex * x_tank_val +
                    self.tank_fixed_opex * N_tank_val +
                    self.tank_variable_opex * N_tank_val
                )

        # Scenario summary
        self.scenario_results.append({
            "Shuttle_Size_cbm": shuttle_size_int,
            "Pump_Size_m3ph": pump_size_int,
            "Call_Duration_hr": round(call_duration, 4),
            "Cycle_Duration_hr": round(cycle_duration, 4),
            "Trips_per_Call": trips_per_call,
            "NPC_Total_USDm": npc_total / 1e6,
            "NPC_Shuttle_CAPEX_USDm": npc_shuttle_cap / 1e6,
            "NPC_Bunkering_CAPEX_USDm": npc_bunk_cap / 1e6,
            "NPC_Terminal_CAPEX_USDm": npc_tank_cap / 1e6,
            "NPC_Shuttle_fOPEX_USDm": npc_shuttle_fop / 1e6,
            "NPC_Bunkering_fOPEX_USDm": npc_bunk_fop / 1e6,
            "NPC_Terminal_fOPEX_USDm": npc_tank_fop / 1e6,
            "NPC_Shuttle_vOPEX_USDm": npc_shuttle_vop / 1e6,
            "NPC_Bunkering_vOPEX_USDm": npc_bunk_vop / 1e6,
            "NPC_Terminal_vOPEX_USDm": npc_tank_vop / 1e6,
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

            self.yearly_results.append({
                "Shuttle_Size_cbm": shuttle_size_int,
                "Pump_Size_m3ph": pump_size_int,
                "Year": t,
                "New_Shuttles": int(round(x_val)),
                "Total_Shuttles": int(round(N_val)),
                "Annual_Calls": round(y_val, 4),
                "Annual_Cycles": round(cycles, 4),
                "Supply_m3": round(supply, 4),
                "Demand_m3": round(demand, 4),
                "Cycles_Available": round(cycles_avail, 4),
                "Utilization_Rate": round((cycles / cycles_avail) if cycles_avail > 0 else 0, 6),
            })
