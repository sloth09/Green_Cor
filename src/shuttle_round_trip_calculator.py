"""
Shuttle Round-Trip Calculator - Core Library

Calculates the basic time components for one shuttle's complete round-trip cycle.
This is the fundamental logic that applies equally to all cases (Case 1, 2-1, 2-2).

This module extracts the core shuttle operation logic independent of shore supply.
"""

from typing import Dict


class ShuttleRoundTripCalculator:
    """
    Core library for calculating one shuttle's round-trip cycle time.

    This is the fundamental logic layer that calculates:
    - Travel time (outbound and return)
    - Setup/connection time at destination
    - Pumping time per vessel
    - Total cycle time (excluding shore supply)

    Key principle: Same logic for all cases (Case 1, 2-1, 2-2)
    Case-specific differences (travel time, num_vessels) are passed as parameters.
    """

    def __init__(self, travel_time_hours: float, setup_time_hours: float):
        """
        Initialize with case-specific travel and setup times.

        Args:
            travel_time_hours: One-way travel time (case-specific)
                - Case 1 (Busan port): 1.0-2.0 hours
                - Case 2-1 (Yeosu): 5.63 hours
                - Case 2-2 (Ulsan): 1.67 hours
            setup_time_hours: Connection/disconnection setup time per endpoint
                - Usually 0.5 hours per operation
        """
        self.travel_time_hours = travel_time_hours
        self.setup_time_hours = setup_time_hours

    def calculate(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        bunker_volume_per_call_m3: float = 5000.0,
        num_vessels: int = 1,
        is_round_trip: bool = True
    ) -> Dict:
        """
        Calculate all time components for one shuttle round-trip.

        This is the CORE LOGIC that applies equally to Case 1, 2-1, 2-2.

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
            Whether to include return travel (True for Case 2, True for Case 1 within port)

        Returns:
        --------
        dict with all time components (excluding shore supply):
            'travel_outbound_h': One-way travel time
            'travel_return_h': Return travel time (0 if not round-trip)
            'setup_inbound_h': Connection setup time at destination
            'setup_outbound_h': Disconnection setup time at destination
            'pumping_per_vessel_h': Pumping time per individual vessel
            'pumping_total_h': Total pumping time for all vessels
            'basic_cycle_duration_h': Complete cycle (travel + setup + pumping)
            'trips_per_call': Number of shuttle trips needed per demand call
            'vessels_per_trip': Number of vessels served per trip
        """
        # Travel times
        travel_outbound = self.travel_time_hours
        travel_return = self.travel_time_hours if is_round_trip else 0.0

        # Setup times (connection + venting)
        setup_inbound = 2.0 * self.setup_time_hours
        setup_outbound = 2.0 * self.setup_time_hours

        # Pumping time per vessel
        pumping_per_vessel = bunker_volume_per_call_m3 / pump_size_m3ph

        # Total pumping time (all vessels)
        pumping_total = pumping_per_vessel * num_vessels

        # Movement time at destination per vessel (loading/unloading/docking)
        movement_per_vessel = 1.0  # Fixed 1 hour for movement/docking per vessel
        time_per_vessel_at_destination = movement_per_vessel + setup_inbound + pumping_per_vessel + setup_outbound

        # Total time at destination for all vessels
        time_all_vessels_at_destination = time_per_vessel_at_destination * num_vessels

        # Basic cycle duration (excluding shore supply)
        basic_cycle_duration = travel_outbound + time_all_vessels_at_destination + travel_return

        # Calculate trips per demand call (how many shuttle trips to fulfill one call)
        # For Case 1: how many small shuttles needed to deliver 5000 m³
        # For Case 2: always 1 (shuttle delivers full load in one trip)
        trips_per_call = max(1, -(-bunker_volume_per_call_m3 // shuttle_size_m3))

        return {
            # Individual time components (hours)
            'travel_outbound_h': travel_outbound,
            'travel_return_h': travel_return,
            'setup_inbound_h': setup_inbound,
            'setup_outbound_h': setup_outbound,
            'movement_per_vessel_h': movement_per_vessel,
            'pumping_per_vessel_h': pumping_per_vessel,
            'pumping_total_h': pumping_total,

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
        }

    def calculate_call_duration(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        bunker_volume_per_call_m3: float = 5000.0,
        num_vessels: int = 1,
        is_round_trip: bool = True
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
            is_round_trip
        )

        trips = cycle_info['trips_per_call']
        time_per_trip = cycle_info['basic_cycle_duration_h']

        return trips * time_per_trip
