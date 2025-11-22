"""
Cost calculator for bunkering infrastructure.
Calculates CAPEX and OPEX for shuttles, bunkering systems, and storage tanks.
"""

from typing import Dict, Tuple
from .utils import (
    calculate_shuttle_capex,
    calculate_pump_power,
    calculate_tank_volume_m3,
    calculate_annuity_factor,
    annualize_npc
)


class CostCalculator:
    """Calculate costs for bunkering infrastructure components."""

    def __init__(self, config: Dict):
        """
        Initialize cost calculator with configuration.

        Args:
            config: Configuration dictionary
        """
        self.config = config

    # ========== SHUTTLE COSTS ==========

    def calculate_shuttle_capex(self, shuttle_size_cbm: float) -> float:
        """
        Calculate capital cost for a single shuttle vessel.

        Uses scaling law: CAPEX = ref_capex × (size / ref_size)^alpha

        Args:
            shuttle_size_cbm: Shuttle size in m3

        Returns:
            CAPEX in USD
        """
        ref_capex = self.config["shuttle"]["ref_capex_usd"]
        ref_size = self.config["shuttle"]["ref_size_cbm"]
        alpha = self.config["shuttle"]["capex_scaling_exponent"]

        return calculate_shuttle_capex(shuttle_size_cbm, ref_capex, ref_size, alpha)

    def calculate_shuttle_equipment_cost(self, shuttle_size_cbm: float) -> float:
        """
        Calculate equipment cost for shuttle (as % of CAPEX).

        Args:
            shuttle_size_cbm: Shuttle size in m3

        Returns:
            Equipment cost in USD
        """
        capex = self.calculate_shuttle_capex(shuttle_size_cbm)
        equipment_ratio = self.config["shuttle"]["equipment_ratio"]
        return capex * equipment_ratio

    def calculate_shuttle_fixed_opex(self, shuttle_size_cbm: float) -> float:
        """
        Calculate annual fixed OPEX for shuttle vessel.

        Args:
            shuttle_size_cbm: Shuttle size in m3

        Returns:
            Annual fixed OPEX in USD
        """
        capex = self.calculate_shuttle_capex(shuttle_size_cbm)
        opex_ratio = self.config["shuttle"]["fixed_opex_ratio"]
        return capex * opex_ratio

    def calculate_shuttle_fuel_cost_per_cycle(
        self,
        shuttle_size_cbm: float,
        travel_time_hours: float,
        travel_factor: float = 1.0
    ) -> float:
        """
        Calculate fuel cost for shuttle per operating cycle.

        Fuel consumed = MCR × SFOC × travel_time × travel_factor / 1e6

        Args:
            shuttle_size_cbm: Shuttle size in m3
            travel_time_hours: Travel time per leg in hours
            travel_factor: Multiplier for round-trip vs one-way
                          - Case 1 (Busan port, one-way): 1.0
                          - Case 2 (long distance, round-trip): 2.0

        Returns:
            Fuel cost in USD per cycle
        """
        if shuttle_size_cbm not in self.config["shuttle"].get("mcr_map_kw", {}):
            # If MCR not defined, estimate from size
            # Rough approximation: MCR increases with size
            mcr_map = self.config["shuttle"].get("mcr_map_kw", {})
            if not mcr_map:
                return 0.0

        mcr = self.config["shuttle"]["mcr_map_kw"].get(int(shuttle_size_cbm), 0)
        if mcr == 0:
            return 0.0

        sfoc = self.config["propulsion"]["sfoc_g_per_kwh"]
        fuel_price = self.config["economy"]["fuel_price_usd_per_ton"]

        # Fuel per cycle in tons (with travel_factor for Case 1 vs Case 2)
        fuel_ton = (mcr * sfoc * travel_time_hours * travel_factor) / 1e6

        return fuel_ton * fuel_price

    # ========== PUMP COSTS ==========

    def calculate_pump_power(
        self,
        pump_flow_m3ph: float,
        delta_pressure_bar: float = None,
        efficiency: float = None
    ) -> float:
        """
        Calculate pump power required.

        Args:
            pump_flow_m3ph: Pump flow rate in m3/h
            delta_pressure_bar: Pressure drop in bar (uses config if None)
            efficiency: Pump efficiency (uses config if None)

        Returns:
            Power in kW
        """
        if delta_pressure_bar is None:
            delta_pressure_bar = self.config["propulsion"]["pump_delta_pressure_bar"]
        if efficiency is None:
            efficiency = self.config["propulsion"]["pump_efficiency"]

        return calculate_pump_power(pump_flow_m3ph, delta_pressure_bar, efficiency)

    def calculate_pump_capex(self, pump_flow_m3ph: float) -> float:
        """
        Calculate capital cost for pump system.

        CAPEX = pump_power (kW) × cost_per_kW

        Args:
            pump_flow_m3ph: Pump flow rate in m3/h

        Returns:
            CAPEX in USD
        """
        delta_pressure = self.config["propulsion"]["pump_delta_pressure_bar"]
        efficiency = self.config["propulsion"]["pump_efficiency"]
        cost_per_kw = self.config["propulsion"]["pump_power_cost_usd_per_kw"]

        power_kw = calculate_pump_power(pump_flow_m3ph, delta_pressure, efficiency)
        return power_kw * cost_per_kw

    def calculate_bunkering_capex(
        self,
        shuttle_size_cbm: float,
        pump_flow_m3ph: float
    ) -> float:
        """
        Calculate total bunkering system CAPEX (shuttle + pump equipment).

        Args:
            shuttle_size_cbm: Shuttle size in m3
            pump_flow_m3ph: Pump flow rate in m3/h

        Returns:
            Total bunkering CAPEX in USD
        """
        shuttle_equip = self.calculate_shuttle_equipment_cost(shuttle_size_cbm)
        pump_capex = self.calculate_pump_capex(pump_flow_m3ph)
        return shuttle_equip + pump_capex

    def calculate_bunkering_fixed_opex(
        self,
        shuttle_size_cbm: float,
        pump_flow_m3ph: float
    ) -> float:
        """
        Calculate annual fixed OPEX for bunkering system.

        Args:
            shuttle_size_cbm: Shuttle size in m3
            pump_flow_m3ph: Pump flow rate in m3/h

        Returns:
            Annual fixed OPEX in USD
        """
        capex = self.calculate_bunkering_capex(shuttle_size_cbm, pump_flow_m3ph)
        opex_ratio = self.config["bunkering"]["fixed_opex_ratio"]
        return capex * opex_ratio

    def calculate_bunkering_fuel_cost_per_call(
        self,
        pump_flow_m3ph: float,
        bunker_volume_m3: float
    ) -> float:
        """
        Calculate fuel cost for pump operation per bunkering call.

        Pumping time = volume / flow_rate
        Fuel per call = pump_power × pumping_time × SFOC / 1e6

        Args:
            pump_flow_m3ph: Pump flow rate in m3/h
            bunker_volume_m3: Volume to pump per call in m3

        Returns:
            Fuel cost in USD per call
        """
        # Pumping time for one bunkering call (one pumping event)
        # NOTE: v2.3.1 fix - removed erroneous 2.0 coefficient that was causing 2x cost overestimation
        pumping_time_hr = bunker_volume_m3 / pump_flow_m3ph

        delta_pressure = self.config["propulsion"]["pump_delta_pressure_bar"]
        efficiency = self.config["propulsion"]["pump_efficiency"]
        sfoc = self.config["propulsion"]["sfoc_g_per_kwh"]
        fuel_price = self.config["economy"]["fuel_price_usd_per_ton"]

        power_kw = calculate_pump_power(pump_flow_m3ph, delta_pressure, efficiency)

        # Fuel per call in tons
        fuel_ton = (power_kw * pumping_time_hr * sfoc) / 1e6

        return fuel_ton * fuel_price

    # ========== TANK STORAGE COSTS ==========

    def calculate_tank_capex(self) -> float:
        """
        Calculate capital cost for one storage tank.

        Args:
            None (uses config)

        Returns:
            CAPEX in USD per tank
        """
        tank_ton = self.config["tank_storage"]["size_tons"]
        tank_kg = tank_ton * 1000.0
        cost_per_kg = self.config["tank_storage"]["cost_per_kg_usd"]
        return tank_kg * cost_per_kg

    def calculate_tank_fixed_opex(self) -> float:
        """
        Calculate annual fixed OPEX for one storage tank.

        Args:
            None (uses config)

        Returns:
            Annual fixed OPEX in USD per tank
        """
        capex = self.calculate_tank_capex()
        opex_ratio = self.config["tank_storage"]["fixed_opex_ratio"]
        return capex * opex_ratio

    def calculate_tank_variable_opex(self) -> float:
        """
        Calculate annual variable OPEX for one storage tank (refrigeration).

        Variable OPEX = tank_volume × energy_per_kg × electricity_price

        Args:
            None (uses config)

        Returns:
            Annual variable OPEX in USD per tank
        """
        tank_ton = self.config["tank_storage"]["size_tons"]
        tank_kg = tank_ton * 1000.0
        energy_per_kg = self.config["tank_storage"]["cooling_energy_kwh_per_kg"]
        elec_price = self.config["economy"]["electricity_price_usd_per_kwh"]

        return tank_kg * energy_per_kg * elec_price

    def calculate_tank_volume_m3(self) -> float:
        """
        Calculate storage tank volume.

        Args:
            None (uses config)

        Returns:
            Tank volume in m3
        """
        tank_ton = self.config["tank_storage"]["size_tons"]
        density = self.config["ammonia"]["density_storage_ton_m3"]
        return calculate_tank_volume_m3(tank_ton, density)

    # ========== SHORE SUPPLY PUMP COSTS ==========
    # Fixed capacity: 1500 m³/h shore supply pump

    def calculate_shore_pump_capex(self) -> float:
        """
        Calculate capital cost for shore supply pump (1500 m³/h).

        CAPEX = pump_power (kW) × cost_per_kW

        Args:
            None (uses fixed 1500 m³/h and config)

        Returns:
            CAPEX in USD for shore pump
        """
        shore_pump_flow = 1500.0  # Fixed shore pump capacity
        delta_pressure = self.config["propulsion"]["pump_delta_pressure_bar"]
        efficiency = self.config["propulsion"]["pump_efficiency"]
        cost_per_kw = self.config["propulsion"]["pump_power_cost_usd_per_kw"]

        power_kw = calculate_pump_power(shore_pump_flow, delta_pressure, efficiency)
        return power_kw * cost_per_kw

    def calculate_shore_pump_fixed_opex(self) -> float:
        """
        Calculate annual fixed OPEX for shore supply pump.

        Fixed OPEX = CAPEX × fixed_opex_ratio (maintenance)

        Args:
            None (uses config)

        Returns:
            Annual fixed OPEX in USD per year
        """
        capex = self.calculate_shore_pump_capex()
        opex_ratio = 0.05  # 5% maintenance ratio
        return capex * opex_ratio

    def calculate_shore_pump_variable_opex_per_hour(self) -> float:
        """
        Calculate variable OPEX for shore supply pump per hour of operation.

        Variable OPEX per hour = pump_power × SFOC / 1e6 × fuel_price

        Args:
            None (uses config)

        Returns:
            Variable OPEX in USD per operating hour
        """
        shore_pump_flow = 1500.0  # Fixed shore pump capacity
        delta_pressure = self.config["propulsion"]["pump_delta_pressure_bar"]
        efficiency = self.config["propulsion"]["pump_efficiency"]
        sfoc = self.config["propulsion"]["sfoc_g_per_kwh"]
        fuel_price = self.config["economy"]["fuel_price_usd_per_ton"]

        power_kw = calculate_pump_power(shore_pump_flow, delta_pressure, efficiency)
        fuel_ton_per_hour = (power_kw * sfoc) / 1e6  # Convert g to ton
        return fuel_ton_per_hour * fuel_price

    # ========== SUMMARY METHODS ==========

    def get_shuttle_costs(self, shuttle_size_cbm: float) -> Dict[str, float]:
        """
        Get all cost components for a shuttle vessel.

        Args:
            shuttle_size_cbm: Shuttle size in m3

        Returns:
            Dictionary with cost components
        """
        return {
            "capex": self.calculate_shuttle_capex(shuttle_size_cbm),
            "fixed_opex": self.calculate_shuttle_fixed_opex(shuttle_size_cbm),
            "equipment_cost": self.calculate_shuttle_equipment_cost(shuttle_size_cbm),
        }

    def get_pump_costs(self, pump_flow_m3ph: float) -> Dict[str, float]:
        """
        Get all cost components for a pump system.

        Args:
            pump_flow_m3ph: Pump flow rate in m3/h

        Returns:
            Dictionary with cost components
        """
        return {
            "capex": self.calculate_pump_capex(pump_flow_m3ph),
        }

    def get_bunkering_costs(
        self,
        shuttle_size_cbm: float,
        pump_flow_m3ph: float
    ) -> Dict[str, float]:
        """
        Get all cost components for bunkering system (shuttle + pump).

        Args:
            shuttle_size_cbm: Shuttle size in m3
            pump_flow_m3ph: Pump flow rate in m3/h

        Returns:
            Dictionary with cost components
        """
        return {
            "capex": self.calculate_bunkering_capex(shuttle_size_cbm, pump_flow_m3ph),
            "fixed_opex": self.calculate_bunkering_fixed_opex(shuttle_size_cbm, pump_flow_m3ph),
        }

    def get_tank_costs(self) -> Dict[str, float]:
        """
        Get all cost components for storage tank.

        Args:
            None (uses config)

        Returns:
            Dictionary with cost components
        """
        return {
            "capex": self.calculate_tank_capex(),
            "fixed_opex": self.calculate_tank_fixed_opex(),
            "variable_opex": self.calculate_tank_variable_opex(),
            "volume_m3": self.calculate_tank_volume_m3(),
        }

    # ========== ANNUALIZATION METHODS ==========

    def get_annuity_factor(self) -> float:
        """
        Calculate annuity factor for asset annualization.

        IMPORTANT: This uses annualization_interest_rate (NOT discount_rate).
        - discount_rate: Controls time value of money for NPV calculation (currently 0%, no discounting)
        - annualization_interest_rate: Used to convert asset values to uniform annual payments (7%)

        Formula:
            Annuity_Factor = [1 - (1 + r)^(-n)] / r

        Where:
            r = annualization_interest_rate (e.g., 0.07 for 7%)
            n = project_years (e.g., 21 for 2030-2050)

        Returns:
            Annuity factor for asset annualization

        Example:
            >>> cost_calc = CostCalculator(config)
            >>> factor = cost_calc.get_annuity_factor()
            >>> factor  # approximately 10.594 for r=7%, n=21
        """
        # Use annualization_interest_rate for converting assets to annual costs
        annualization_rate = self.config["economy"]["annualization_interest_rate"]

        # Calculate project years dynamically from time_period config
        # Range: 2030 to 2050 inclusive = 21 years (2050 - 2030 + 1)
        start_year = self.config["time_period"]["start_year"]
        end_year = self.config["time_period"]["end_year"]
        project_years = end_year - start_year + 1

        # Calculate annuity factor using the annualization interest rate
        return calculate_annuity_factor(annualization_rate, project_years)

    def annualize_scenario_npc(self, npc_total: float) -> float:
        """
        Convert total Net Present Cost to annualized annual cost.

        This represents the equivalent constant annual payment that equals
        the total discounted costs over the 20-year project period.

        Args:
            npc_total: Total Net Present Cost in USD

        Returns:
            Annualized annual cost in USD

        Example:
            >>> cost_calc = CostCalculator(config)
            >>> npc = 2_650_000_000  # $2,650M
            >>> annualized = cost_calc.annualize_scenario_npc(npc)
            >>> annualized  # approximately $250M per year
        """
        annuity_factor = self.get_annuity_factor()
        return annualize_npc(npc_total, annuity_factor)

    def annualize_npc_components(
        self,
        npc_capex: float,
        npc_fixed_opex: float,
        npc_variable_opex: float
    ) -> Dict[str, float]:
        """
        Convert NPC components to annualized costs.

        Allows analysis of which cost components dominate on an annual basis.

        Args:
            npc_capex: Total capital costs (discounted)
            npc_fixed_opex: Total fixed operating costs (discounted)
            npc_variable_opex: Total variable operating costs (discounted)

        Returns:
            Dictionary with annualized components:
            {
                "capex": annualized CAPEX,
                "fixed_opex": annualized Fixed OPEX,
                "variable_opex": annualized Variable OPEX,
                "total": annualized total
            }
        """
        annuity_factor = self.get_annuity_factor()

        return {
            "capex": annualize_npc(npc_capex, annuity_factor),
            "fixed_opex": annualize_npc(npc_fixed_opex, annuity_factor),
            "variable_opex": annualize_npc(npc_variable_opex, annuity_factor),
            "total": annualize_npc(npc_capex + npc_fixed_opex + npc_variable_opex, annuity_factor),
        }

    def calculate_annualized_capex_yearly(
        self,
        asset_value: float
    ) -> float:
        """
        Calculate annualized CAPEX for year-by-year comparison.

        Converts a capital asset value to equivalent constant annual depreciation.
        This allows fair year-to-year comparison even when CAPEX is lumpy.

        Formula:
            Annualized CAPEX = Asset Value / Annuity Factor

        Args:
            asset_value: Total asset value in USD (shuttle + equipment currently owned)

        Returns:
            Annualized annual CAPEX in USD

        Example:
            >>> cost_calc = CostCalculator(config)
            >>> shuttle_value = 18_917_000  # $18.917M per shuttle
            >>> pump_value = 505_600  # $0.5056M per pump
            >>> total_asset = shuttle_value + pump_value  # 2 shuttles + pumps
            >>> annualized = cost_calc.calculate_annualized_capex_yearly(total_asset)
            >>> annualized  # approximately $1.8M per year (consistent across all years)
        """
        annuity_factor = self.get_annuity_factor()
        return asset_value / annuity_factor if annuity_factor > 0 else 0.0
