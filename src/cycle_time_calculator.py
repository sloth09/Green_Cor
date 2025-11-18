"""
Cycle Time Calculator for ammonia bunkering shuttle operations.

Handles time structure calculations for all cases, including:
- Shore supply loading time (fixed 1,500 m³/h pump)
- Transit time
- Bunkering time
- Setup/connection time
"""

from typing import Dict, Optional


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

    def calculate_single_cycle(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        num_vessels: int = 1
    ) -> Dict:
        """
        Calculate a single complete cycle time breakdown.

        Parameters:
        -----------
        shuttle_size_m3 : float
            Shuttle capacity in m³
        pump_size_m3ph : float
            Bunkering pump flow rate in m³/h
        num_vessels : int
            Number of vessels serviced per cycle (Case 2 only)

        Returns:
        --------
        dict with keys:
            'shore_loading': Time to load shuttle at shore (hours)
            'travel_outbound': One-way travel time (hours)
            'setup_inbound': Connection/setup time at destination (hours)
            'pumping_per_vessel': Pumping time per individual vessel (hours)
            'pumping_total': Total pumping time (hours)
            'setup_outbound': Disconnection/setup time at destination (hours)
            'travel_return': Return travel time (hours)
            'shore_unloading': Time to offload at shore (hours, Case 2 only)
            'call_duration': Time for one "call" event (hours)
            'cycle_duration': Complete round-trip cycle time (hours)
            'trips_per_call': Number of trips per demand call
        """
        # Shore supply loading time (common to all cases)
        shore_loading = shuttle_size_m3 / self.SHORE_PUMP_RATE_M3PH

        # Case-specific calculations
        if self.has_storage_at_busan:
            return self._calculate_case1_cycle(
                shuttle_size_m3, pump_size_m3ph, shore_loading
            )
        else:
            return self._calculate_case2_cycle(
                shuttle_size_m3, pump_size_m3ph, shore_loading, num_vessels
            )

    def _calculate_case1_cycle(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        shore_loading: float
    ) -> Dict:
        """
        Calculate Case 1 cycle (Busan port-based storage).

        Case 1 Structure:
        - Shore loading (at Busan storage): shuttle_size / 1500
        - Shuttle travel out (within port): 1 hour
        - Connection setup: 1 hour
        - Bunkering one call: bunker_volume / pump_rate
        - Disconnection setup: 1 hour
        - Shuttle travel back (within port): 1 hour

        Returns full cycle breakdown.
        """
        # Determine trips needed to satisfy one call
        trips_per_call = max(1, -(-self.bunker_volume_per_call_m3 // shuttle_size_m3))

        # Time components per cycle
        travel_out = self.travel_time_hours
        setup_in = 2.0 * self.setup_time_hours  # Connection + venting
        pumping_per_call = self.bunker_volume_per_call_m3 / pump_size_m3ph
        setup_out = 2.0 * self.setup_time_hours  # Disconnection + venting
        travel_back = self.travel_time_hours

        # Pumping for full cycle
        pumping_full_cycle = (shuttle_size_m3 / pump_size_m3ph) * 2.0  # Load + unload

        # Call duration (serving one demand call = 5000 m³)
        call_duration = (
            trips_per_call * (travel_out + setup_in + pumping_per_call + setup_out + travel_back)
        )

        # Full cycle duration (round-trip, including shore operations)
        cycle_duration = shore_loading + travel_out + setup_in + pumping_full_cycle + setup_out + travel_back

        return {
            "case_type": self.case_type,
            "shuttle_size_m3": shuttle_size_m3,
            "pump_size_m3ph": pump_size_m3ph,
            # Time breakdown (hours)
            "shore_loading": shore_loading,
            "travel_outbound": travel_out,
            "setup_inbound": setup_in,
            "pumping_per_vessel": pumping_per_call,
            "pumping_total": pumping_full_cycle,
            "setup_outbound": setup_out,
            "travel_return": travel_back,
            "shore_unloading": 0.0,  # Case 1: No offloading at shore
            # Summary times
            "call_duration": call_duration,
            "cycle_duration": cycle_duration,
            "trips_per_call": trips_per_call,
            "vessels_per_trip": 1,  # Case 1 serves one vessel per trip
            "num_vessels_per_cycle": trips_per_call,
        }

    def _calculate_case2_cycle(
        self,
        shuttle_size_m3: float,
        pump_size_m3ph: float,
        shore_loading: float,
        num_vessels: int
    ) -> Dict:
        """
        Calculate Case 2 cycle (Yeosu/Ulsan production-based).

        Case 2 Structure:
        - Preparation at source: 1 hour
        - Shore loading (at production site): shuttle_size / 1500
        - Travel to Busan: travel_time_hours (5.63h for Yeosu, 1.67h for Ulsan)
        - Port entry/waiting: 1 hour
        - [For each vessel]:
          - Shuttle movement (docking): 1 hour
          - Connection setup: 1 hour
          - Bunkering: 5000 / pump_rate
          - Disconnection setup: 1 hour
        - Travel back to source: travel_time_hours
        - Port arrival/setup: 1 hour

        Returns full cycle breakdown.
        """
        # Determine vessels served per trip
        vessels_per_trip = max(1, int(shuttle_size_m3 // self.bunker_volume_per_call_m3))

        # Time components
        prep_time = 1.0
        travel_out = self.travel_time_hours
        port_entry = 1.0

        # Per-vessel time at Busan
        per_vessel_time = (
            1.0  # Movement/docking
            + 2.0 * self.setup_time_hours  # Connection + disconnection
            + (self.bunker_volume_per_call_m3 / pump_size_m3ph)  # Bunkering
        )
        pumping_total = per_vessel_time * vessels_per_trip

        travel_back = self.travel_time_hours
        port_exit = 1.0

        # Call duration (one trip) = voyage time
        call_duration = prep_time + shore_loading + travel_out + port_entry + pumping_total + travel_back + port_exit

        # Cycle duration (includes round-trip travel)
        cycle_duration = shore_loading + travel_out + port_entry + pumping_total + travel_back

        return {
            "case_type": self.case_type,
            "shuttle_size_m3": shuttle_size_m3,
            "pump_size_m3ph": pump_size_m3ph,
            # Time breakdown (hours)
            "shore_loading": shore_loading,
            "travel_outbound": travel_out,
            "setup_inbound": port_entry,
            "pumping_per_vessel": self.bunker_volume_per_call_m3 / pump_size_m3ph,
            "pumping_total": pumping_total,
            "setup_outbound": port_exit,
            "travel_return": travel_back,
            "shore_unloading": 0.0,  # Case 2: Handled as shore_loading in source port
            # Summary times
            "call_duration": call_duration,
            "cycle_duration": cycle_duration,
            "trips_per_call": 1,  # Case 2: One trip per "mega-call"
            "vessels_per_trip": vessels_per_trip,
            "num_vessels_per_cycle": vessels_per_trip,
        }

    def calculate_shore_loading_time(self, shuttle_size_m3: float) -> float:
        """
        Calculate shore supply loading time.

        Args:
            shuttle_size_m3: Shuttle capacity in m³

        Returns:
            Loading time in hours (shuttle_size / 1500)
        """
        return shuttle_size_m3 / self.SHORE_PUMP_RATE_M3PH

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
