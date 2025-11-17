"""
Cost calculator for bunkering infrastructure.
Calculates CAPEX and OPEX for shuttles, bunkering systems, and storage tanks.
"""

from typing import Dict, Tuple
from .utils import (
    calculate_shuttle_capex,
    calculate_pump_power,
    calculate_tank_volume_m3
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
        travel_time_hours: float
    ) -> float:
        """
        Calculate fuel cost for shuttle per operating cycle.

        Fuel consumed = MCR × SFOC × travel_time / 1e6

        Args:
            shuttle_size_cbm: Shuttle size in m3
            travel_time_hours: Travel time in hours

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

        # Fuel per cycle in tons
        fuel_ton = (mcr * sfoc * travel_time_hours) / 1e6

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

        Pumping time = 2 × volume / flow_rate (load + unload)
        Fuel per call = pump_power × pumping_time × SFOC / 1e6

        Args:
            pump_flow_m3ph: Pump flow rate in m3/h
            bunker_volume_m3: Volume to pump per call in m3

        Returns:
            Fuel cost in USD per call
        """
        # Pumping time = 2 × (load + unload)
        pumping_time_hr = 2.0 * (bunker_volume_m3 / pump_flow_m3ph)

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
