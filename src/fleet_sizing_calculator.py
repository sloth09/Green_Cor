"""
Fleet Sizing Calculator - Shared library for fleet sizing across all modes.

This module provides a unified interface for calculating required fleet size
based on operational demands, ensuring consistency between optimizer.py and main.py.
"""

from math import ceil
from typing import Dict


class FleetSizingCalculator:
    """
    Unified fleet sizing calculator for all operational modes.

    Ensures that both MILP optimizer and annual simulation use the same fleet sizing logic.
    """

    def __init__(self, config: Dict):
        """
        Initialize fleet sizing calculator.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.max_annual_hours = config["operations"]["max_annual_hours_per_vessel"]
        self.daily_peak_factor = config["operations"].get("daily_peak_factor", 1.5)

    def calculate_required_shuttles_working_time_only(self,
                                                     annual_calls: float,
                                                     trips_per_call: int,
                                                     cycle_duration: float) -> int:
        """
        Calculate required fleet size using ONLY working time constraint.

        This is the basic fleet sizing that accounts for:
        - Annual demand (in number of calls)
        - Shuttle trips needed per call (Case 1: may need multiple trips)
        - Total cycle time per trip
        - Maximum annual operating hours per vessel

        Formula:
            total_trips = annual_calls × trips_per_call
            total_hours = total_trips × cycle_duration
            required_shuttles = ceil(total_hours / max_annual_hours)

        Args:
            annual_calls: Number of bunkering calls needed annually
            trips_per_call: Shuttle trips required per bunkering call
                           (Case 1: ceil(bunker_volume / shuttle_size)
                            Case 2: 1)
            cycle_duration: Hours for one complete cycle (from cycle_calculator)

        Returns:
            Minimum number of shuttles required

        Example (Case 1: 5000m³ shuttle + 2000m³/h pump, 2030):
            annual_calls = 600 (3,000,000 m³ / 5,000 m³)
            trips_per_call = 1 (5000m³ shuttle >= 5000m³ call)
            cycle_duration = 9.83 hours
            total_hours = 600 × 1 × 9.83 = 5,898 hours
            required_shuttles = ceil(5,898 / 8,000) = 1 ✓
        """
        total_trips = annual_calls * trips_per_call
        total_hours_needed = total_trips * cycle_duration
        required_shuttles = ceil(total_hours_needed / self.max_annual_hours)
        return required_shuttles

    def calculate_required_shuttles_with_daily_peak(self,
                                                   annual_calls: float,
                                                   trips_per_call: int,
                                                   cycle_duration: float,
                                                   shuttle_size: float) -> int:
        """
        Calculate required fleet size using BOTH working time and daily peak constraints.

        This adds a safety factor based on daily peak demand distribution:
        - Assumes demand is uniformly distributed across 365 days
        - Applies daily_peak_factor (typically 1.5) to account for peak concentration
        - Ensures fleet can handle peak demand days

        Constraints:
            1. Working time: total_hours <= shuttles × max_annual_hours
            2. Daily peak: daily_capacity >= daily_demand × daily_peak_factor

        Formula (for daily peak):
            daily_demand = (annual_calls / 365) × bunker_volume × daily_peak_factor
            daily_capacity = shuttles × (max_annual_hours / cycle_duration) × shuttle_size / 365
            daily_capacity >= daily_demand
            shuttles >= daily_demand × 365 / (max_annual_hours / cycle_duration) / shuttle_size

        Args:
            annual_calls: Number of bunkering calls needed annually
            trips_per_call: Shuttle trips required per bunkering call
            cycle_duration: Hours for one complete cycle
            shuttle_size: Shuttle capacity in m³

        Returns:
            Number of shuttles needed to satisfy both constraints

        Example (Case 1: 5000m³ shuttle + 2000m³/h pump, 2030):
            Daily peak would calculate:
            - daily_demand ≈ 12,329 m³/day × 1.5 = 18,494 m³
            - daily_capacity (1 shuttle) ≈ 11,140 m³/day
            - Result: Need 2 shuttles due to peak factor ✗

        WARNING: This constraint is only applied if explicitly enabled in config.
        """
        # First, try working time only
        required_wt = self.calculate_required_shuttles_working_time_only(
            annual_calls, trips_per_call, cycle_duration
        )

        # Then check daily peak constraint
        bunker_volume = self.config["bunkering"]["bunker_volume_per_call_m3"]

        # Daily demand with peak factor
        daily_demand_with_peak = (annual_calls / 365.0) * bunker_volume * self.daily_peak_factor

        # Daily capacity per shuttle
        cycles_per_day_per_shuttle = self.max_annual_hours / cycle_duration / 365.0
        daily_capacity_per_shuttle = cycles_per_day_per_shuttle * shuttle_size

        # Shuttles needed for daily peak
        required_peak = ceil(daily_demand_with_peak / daily_capacity_per_shuttle)

        # Return the binding constraint (whichever is larger)
        return max(required_wt, required_peak)

    def get_constraint_details(self,
                              annual_calls: float,
                              trips_per_call: int,
                              cycle_duration: float,
                              shuttle_size: float) -> Dict:
        """
        Get detailed breakdown of fleet sizing constraints.

        Useful for debugging and understanding which constraint is binding.

        Returns:
            Dictionary with:
                - working_time_shuttles: Shuttles needed for working time
                - daily_peak_shuttles: Shuttles needed for daily peak
                - binding_constraint: Which constraint requires more shuttles
                - total_hours_needed: Total hours for annual operations
                - daily_demand: Daily demand with peak factor
        """
        required_wt = self.calculate_required_shuttles_working_time_only(
            annual_calls, trips_per_call, cycle_duration
        )

        # Calculate working time hours
        total_trips = annual_calls * trips_per_call
        total_hours = total_trips * cycle_duration

        # Calculate daily peak details
        bunker_volume = self.config["bunkering"]["bunker_volume_per_call_m3"]
        daily_demand_with_peak = (annual_calls / 365.0) * bunker_volume * self.daily_peak_factor
        cycles_per_day_per_shuttle = self.max_annual_hours / cycle_duration / 365.0
        daily_capacity_per_shuttle = cycles_per_day_per_shuttle * shuttle_size
        required_peak = ceil(daily_demand_with_peak / daily_capacity_per_shuttle)

        return {
            'working_time_shuttles': required_wt,
            'daily_peak_shuttles': required_peak,
            'binding_constraint': 'daily_peak' if required_peak > required_wt else 'working_time',
            'total_hours_needed': total_hours,
            'daily_demand_m3_with_peak': daily_demand_with_peak,
            'daily_capacity_per_shuttle_m3': daily_capacity_per_shuttle,
        }
