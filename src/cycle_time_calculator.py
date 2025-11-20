"""
Cycle Time Calculator for ammonia bunkering shuttle operations.

3-Layer Architecture:
1. ShuttleRoundTripCalculator (core library) - Basic cycle logic
2. CycleTimeCalculator (this layer) - Core + ShoreSupply integration
3. optimizer.py (top layer) - Optimization logic

Handles time structure calculations for all cases, including:
- Shore supply loading time (fixed 1,500 m³/h pump)
- Basic shuttle round-trip time (from ShuttleRoundTripCalculator)
- Transit time
- Bunkering time
- Setup/connection time
"""

from typing import Dict, Optional
from .shuttle_round_trip_calculator import ShuttleRoundTripCalculator


class CycleTimeCalculator:
    """
    Calculates complete cycle time breakdown for shuttle operations.

    Supports three cases:
    - Case 1: Port-based storage (Busan)
    - Case 2-1: Production-based (Yeosu) long-distance
    - Case 2-2: Production-based (Ulsan) short-distance
    """

    # Fixed shore supply pump rate (m³/h)
    SHORE_PUMP_RATE_M3PH = 1500.0

    def __init__(self, case_type: str, config: Dict):
        """
        Initialize calculator with case type and configuration.

        Args:
            case_type: One of "case_1", "case_2_yeosu", "case_2_ulsan"
            config: Configuration dictionary containing operational parameters
        """
        self.case_type = case_type
        self.config = config

        # Extract operational parameters
        self.travel_time_hours = config["operations"]["travel_time_hours"]
        self.setup_time_hours = config["operations"]["setup_time_hours"]
        self.has_storage_at_busan = config["operations"].get("has_storage_at_busan", True)

        # Bunkering parameters
        self.bunker_volume_per_call_m3 = config["bunkering"]["bunker_volume_per_call_m3"]

        # Initialize core library (ShuttleRoundTripCalculator)
        # This is the fundamental logic that applies to all cases
        self.shuttle_calculator = ShuttleRoundTripCalculator(
            travel_time_hours=self.travel_time_hours,
            setup_time_hours=self.setup_time_hours
        )

        # Import ShoreSupply here to avoid circular imports
        from .shore_supply import ShoreSupply
        self.shore_supply = ShoreSupply(config)

    def calculate_single_cycle(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        num_vessels: int = 1
    ) -> Dict:
        """
        Calculate a single complete cycle time breakdown.

        This method combines three components in order:
        1. ShuttleRoundTripCalculator (core library) - basic cycle
        2. ShoreSupply (optional) - shore loading time
        3. Final metrics - call_duration, etc.

        The same logic applies to all cases (Case 1, 2-1, 2-2).

        Parameters:
        -----------
        shuttle_size_m3 : float
            Shuttle capacity in m³
        pump_size_m3ph : float
            Bunkering pump flow rate in m³/h
        num_vessels : int
            Number of vessels serviced per round-trip

        Returns:
        --------
        dict with complete time breakdown including shore supply
        """
        # Step 1: Use core library (applies equally to all cases, but with different logic for Case 1 vs 2)
        is_round_trip = True  # All cases have return travel
        shuttle_cycle = self.shuttle_calculator.calculate(
            shuttle_size_m3=shuttle_size_m3,
            pump_size_m3ph=pump_size_m3ph,
            bunker_volume_per_call_m3=self.bunker_volume_per_call_m3,
            num_vessels=num_vessels,
            is_round_trip=is_round_trip,
            has_storage_at_busan=self.has_storage_at_busan
        )

        # Step 2: Add shore supply loading time (ALWAYS INCLUDED - not optional)
        # Shore supply pump (1500 m³/h) is a mandatory operational step for all cases
        # Only the COST of this facility is controlled by shore_supply.enabled
        shore_loading = self.shore_supply.load_shuttle(shuttle_size_m3)

        # Step 3: Calculate final metrics
        basic_cycle = shuttle_cycle['basic_cycle_duration_h']
        cycle_duration = shore_loading + basic_cycle

        # Call duration: time to fulfill one complete demand "call"
        trips_per_call = shuttle_cycle['trips_per_call']
        call_duration = trips_per_call * basic_cycle

        # Annual operations and supply metrics
        # NOTE: These represent MAXIMUM THEORETICAL values for a single shuttle at 100% utilization
        # Actual optimization (y[t]) may use lower values based on demand constraints
        annual_cycles = 8000.0 / cycle_duration if cycle_duration > 0 else 0
        annual_supply_m3 = annual_cycles * shuttle_size_m3

        # Ships per year: maximum theoretical ships that can be bunkered annually
        # Example: 828 cycles × 1000 m³ = 828,000 m³ / 5000 m³ per ship = 165 ships
        ships_per_year = annual_supply_m3 / self.bunker_volume_per_call_m3

        # Aggregate result for backward compatibility and clarity
        return {
            # Individual time components (hours)
            'shore_loading': shore_loading,
            'travel_outbound': shuttle_cycle['travel_outbound_h'],
            'travel_return': shuttle_cycle['travel_return_h'],
            'port_entry': shuttle_cycle['port_entry_h'],
            'port_exit': shuttle_cycle['port_exit_h'],
            'movement_per_vessel': shuttle_cycle['movement_per_vessel_h'],
            'movement_total': shuttle_cycle['movement_total_h'],
            'setup_inbound': shuttle_cycle['setup_inbound_h'],
            'setup_outbound': shuttle_cycle['setup_outbound_h'],
            'pumping_per_vessel': shuttle_cycle['pumping_per_vessel_h'],
            'pumping_total': shuttle_cycle['pumping_total_h'],

            # Complete cycle time
            'basic_cycle_duration': basic_cycle,  # Before shore loading
            'cycle_duration': cycle_duration,     # After shore loading

            # Call duration (fulfilling one demand call)
            'call_duration': call_duration,

            # Operational metrics (theoretical maximum)
            'trips_per_call': trips_per_call,
            'vessels_per_trip': num_vessels,
            'annual_cycles': annual_cycles,
            'annual_supply_m3': annual_supply_m3,
            'ships_per_year': ships_per_year,

            # Case info for debugging
            'case_type': self.case_type,
            'has_storage_at_busan': self.has_storage_at_busan,
        }


    def calculate_shore_loading_time(self, shuttle_size_m3: float) -> float:
        """
        Calculate shore supply loading time.

        Delegates to ShoreSupply module for consistency.

        Args:
            shuttle_size_m3: Shuttle capacity in m³

        Returns:
            Loading time in hours (shuttle_size / 1500)
        """
        return self.shore_supply.load_shuttle(shuttle_size_m3)

    def calculate_pumping_time(
        self,
        volume_m3: float,
        pump_size_m3ph: float
    ) -> float:
        """
        Calculate bunkering pumping time.

        Args:
            volume_m3: Volume to pump in m³
            pump_size_m3ph: Pump flow rate in m³/h

        Returns:
            Pumping time in hours
        """
        return volume_m3 / pump_size_m3ph

    def get_annual_operations_per_shuttle(self, cycle_duration: float) -> float:
        """
        Calculate maximum annual operations per shuttle.

        Assumes 8,000 hours per year operational availability.

        Args:
            cycle_duration: Duration of one complete cycle in hours

        Returns:
            Number of complete cycles per year
        """
        annual_hours = 8000.0
        return annual_hours / cycle_duration
