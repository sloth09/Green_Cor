"""
Shuttle Round-Trip Calculator - Core Library

Calculates the basic time components for one shuttle's complete round-trip cycle.
This is the fundamental logic that applies to all cases (Case 1, 2-1, 2-2).

KEY DIFFERENCE BETWEEN CASES:
- Case 1: Shuttle makes multiple trips per vessel (pumping_per_vessel = shuttle_size / pump_rate)
- Case 2: One trip serves multiple vessels (pumping_per_vessel = bunker_volume / pump_rate)

This module extracts the core shuttle operation logic independent of shore supply.
"""

from typing import Dict


class ShuttleRoundTripCalculator:
    """
    Core library for calculating one shuttle's round-trip cycle time.

    Supports both:
    - Case 1: Multiple small shuttles delivering to single/multiple vessels
    - Case 2: Large shuttle delivering to multiple vessels in one trip

    Case-specific differences (travel time, num_vessels, has_storage) are passed as parameters.
    """

    def __init__(self, travel_time_hours: float, setup_time_hours: float):
        """
        Initialize with case-specific travel and setup times.

        Args:
            travel_time_hours: One-way travel time (case-specific)
                - Case 1 (Busan port): 1.0-2.0 hours
                - Case 2 (Ulsan): 1.67 hours
                - Case 3 (Yeosu): 5.63 hours
            setup_time_hours: Connection/disconnection setup time per endpoint
                - Direct per-endpoint value (2.0 hours), no multiplier applied
        """
        self.travel_time_hours = travel_time_hours
        self.setup_time_hours = setup_time_hours

    def calculate(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        bunker_volume_per_call_m3: float = 5000.0,
        num_vessels: int = 1,
        is_round_trip: bool = True,
        has_storage_at_busan: bool = True
    ) -> Dict:
        """
        Calculate all time components for one shuttle round-trip.

        This method handles both Case 1 and Case 2 logic based on has_storage_at_busan flag.

        Parameters:
        -----------
        shuttle_size_m3 : float
            Shuttle capacity in m³
        pump_size_m3ph : float
            Bunkering pump flow rate in m³/h
        bunker_volume_per_call_m3 : float
            Volume per vessel bunkering call (default 5000 m³)
        num_vessels : int
            Number of vessels served per round-trip
        is_round_trip : bool
            Whether to include return travel
        has_storage_at_busan : bool
            True for Case 1 (port storage), False for Case 2 (long-distance transfer)

        Returns:
        --------
        dict with all time components (excluding shore supply)
        """
        # Travel times
        travel_outbound = self.travel_time_hours
        travel_return = self.travel_time_hours if is_round_trip else 0.0

        # ===== CRITICAL: Case 1 vs Case 2 pumping difference =====
        # Case 1: Shuttle makes multiple small trips; pumping limited by SHUTTLE capacity
        #   Example: 1000m³ shuttle, 5000m³ demand → 5 trips of 1h each
        # Case 2: One trip serves multiple vessels; pumping limited by SHIP demand
        #   Example: 10000m³ shuttle, 5000m³/ship × 2 ships → 5h per ship
        if has_storage_at_busan:
            # CASE 1: Pumping time = how fast shuttle gets emptied
            pumping_per_vessel = shuttle_size_m3 / pump_size_m3ph
        else:
            # CASE 2: Pumping time = how fast each ship gets filled
            pumping_per_vessel = bunker_volume_per_call_m3 / pump_size_m3ph

        # Setup times (direct per-endpoint value, no multiplier)
        setup_inbound = self.setup_time_hours   # Direct per-endpoint setup time (2.0h)
        setup_outbound = self.setup_time_hours  # Direct per-endpoint setup time (2.0h)

        # ===== Case 2 specific: Port operations =====
        port_entry = 1.0 if not has_storage_at_busan else 0.0   # Port entry time
        port_exit = 1.0 if not has_storage_at_busan else 0.0    # Port exit time

        # Movement at destination (docking/maneuvering per vessel)
        # Case 1: included in travel_time (port operations)
        # Case 2: 1 hour per vessel for docking/repositioning
        movement_per_vessel = 1.0 if not has_storage_at_busan else 0.0
        movement_total = movement_per_vessel * num_vessels

        # Time per vessel at destination
        # Case 1: setup_inbound + pumping + setup_outbound
        # Case 2: movement + setup_inbound + pumping + setup_outbound
        time_per_vessel_at_destination = setup_inbound + pumping_per_vessel + setup_outbound
        if not has_storage_at_busan:
            time_per_vessel_at_destination = movement_per_vessel + time_per_vessel_at_destination

        # Total time at destination for all vessels
        time_all_vessels_at_destination = time_per_vessel_at_destination * num_vessels

        # Basic cycle duration (excluding shore supply)
        # Case 1: outbound + (trips × destination time) + return
        # Case 2: outbound + port_entry + (vessels × destination time) + port_exit + return
        basic_cycle_duration = (
            travel_outbound +
            port_entry +
            time_all_vessels_at_destination +
            port_exit +
            travel_return
        )

        # Calculate trips per demand call (how many shuttle trips to fulfill one call)
        # For Case 1: how many small shuttles needed to deliver 5000 m³
        # For Case 2: if shuttle > bunker_volume, one trip serves multiple calls (trips_per_call < 1)
        if shuttle_size_m3 >= bunker_volume_per_call_m3:
            trips_per_call = 1.0 / num_vessels
        else:
            trips_per_call = max(1, -(-bunker_volume_per_call_m3 // shuttle_size_m3))

        return {
            # Individual time components (hours)
            'travel_outbound_h': travel_outbound,
            'travel_return_h': travel_return,
            'port_entry_h': port_entry,
            'port_exit_h': port_exit,
            'movement_per_vessel_h': movement_per_vessel,
            'movement_total_h': movement_total,
            'setup_inbound_h': setup_inbound,
            'setup_outbound_h': setup_outbound,
            'pumping_per_vessel_h': pumping_per_vessel,
            'pumping_total_h': pumping_per_vessel * num_vessels,

            # Aggregated metrics
            'time_per_vessel_at_destination_h': time_per_vessel_at_destination,
            'time_all_vessels_at_destination_h': time_all_vessels_at_destination,

            # Final cycle duration (basic, before shore supply)
            'basic_cycle_duration_h': basic_cycle_duration,

            # Operational metrics
            'trips_per_call': trips_per_call,
            'vessels_per_trip': num_vessels,
            'shuttle_size_m3': shuttle_size_m3,
            'pump_size_m3ph': pump_size_m3ph,
            'has_storage_at_busan': has_storage_at_busan,
        }

    def calculate_call_duration(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        bunker_volume_per_call_m3: float = 5000.0,
        num_vessels: int = 1,
        is_round_trip: bool = True,
        has_storage_at_busan: bool = True
    ) -> float:
        """
        Calculate duration for fulfilling one demand "call" (5000 m³).

        For Case 1: Multiple shuttle trips to deliver 5000 m³
        For Case 2: One trip delivers multiple vessels (5000 m³ each)

        Returns:
            Call duration in hours
        """
        cycle_info = self.calculate(
            shuttle_size_m3,
            pump_size_m3ph,
            bunker_volume_per_call_m3,
            num_vessels,
            is_round_trip,
            has_storage_at_busan
        )

        trips = cycle_info['trips_per_call']
        time_per_trip = cycle_info['basic_cycle_duration_h']

        return trips * time_per_trip
