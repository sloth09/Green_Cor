"""
Unit tests for ShuttleRoundTripCalculator module.

Tests the core library that applies equally to all cases (Case 1, 2-1, 2-2).
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.shuttle_round_trip_calculator import ShuttleRoundTripCalculator


class TestShuttleRoundTripCalculatorBasics:
    """Test basic functionality of core calculator."""

    def setup_method(self):
        """Setup for each test."""
        # Case 1: Busan port (short travel time)
        self.calc_case1 = ShuttleRoundTripCalculator(
            travel_time_hours=2.0,
            setup_time_hours=0.5
        )
        # Case 2-2: Ulsan (medium travel time)
        self.calc_case2_ulsan = ShuttleRoundTripCalculator(
            travel_time_hours=1.67,
            setup_time_hours=0.5
        )
        # Case 2-1: Yeosu (long travel time)
        self.calc_case2_yeosu = ShuttleRoundTripCalculator(
            travel_time_hours=5.63,
            setup_time_hours=0.5
        )

    def test_initialization(self):
        """Test calculator initialization."""
        assert self.calc_case1.travel_time_hours == 2.0
        assert self.calc_case1.setup_time_hours == 0.5

    def test_basic_cycle_structure(self):
        """Test basic cycle structure."""
        result = self.calc_case1.calculate(
            shuttle_size_m3=5000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Verify all required keys exist
        required_keys = [
            'travel_outbound_h', 'travel_return_h',
            'setup_inbound_h', 'setup_outbound_h',
            'pumping_per_vessel_h', 'pumping_total_h',
            'basic_cycle_duration_h',
            'trips_per_call', 'vessels_per_trip'
        ]

        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_case1_single_vessel(self):
        """Test Case 1 with one shuttle trip for one vessel."""
        result = self.calc_case1.calculate(
            shuttle_size_m3=5000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Travel time should be 2.0 hours outbound + 2.0 hours return
        assert pytest.approx(result['travel_outbound_h']) == 2.0
        assert pytest.approx(result['travel_return_h']) == 2.0

        # Setup: 2 * 0.5 = 1.0 hour
        assert pytest.approx(result['setup_inbound_h']) == 1.0
        assert pytest.approx(result['setup_outbound_h']) == 1.0

        # Pumping per vessel: 5000 / 1000 = 5 hours
        assert pytest.approx(result['pumping_per_vessel_h']) == 5.0

        # Trips per call: 5000 / 5000 = 1
        assert result['trips_per_call'] == 1
        assert result['vessels_per_trip'] == 1

    def test_case2_multiple_vessels(self):
        """Test Case 2 with multiple vessels served per trip."""
        result = self.calc_case2_ulsan.calculate(
            shuttle_size_m3=25000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=5,
            is_round_trip=True
        )

        # Travel time: Ulsan = 1.67 hours
        assert pytest.approx(result['travel_outbound_h']) == 1.67
        assert pytest.approx(result['travel_return_h']) == 1.67

        # 5 vessels served per trip
        assert result['vessels_per_trip'] == 5

        # pumping_total_h = pumping_per_vessel * num_vessels (NOT per_vessel_time * num_vessels)
        # pumping_per_vessel = 5000 / 1000 = 5 hours
        # pumping_total = 5 * 5 = 25 hours
        assert pytest.approx(result['pumping_per_vessel_h']) == 5.0
        assert pytest.approx(result['pumping_total_h']) == 25.0

    def test_trips_per_call_small_shuttle(self):
        """Test trips_per_call for small shuttle (Case 1)."""
        result = self.calc_case1.calculate(
            shuttle_size_m3=2500.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Need 2 shuttles to deliver 5000 m³ call
        assert result['trips_per_call'] == 2

    def test_trips_per_call_large_shuttle(self):
        """Test trips_per_call for large shuttle (Case 2)."""
        result = self.calc_case2_ulsan.calculate(
            shuttle_size_m3=25000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=5,
            is_round_trip=True
        )

        # Shuttle delivers all 25000 m³ in one trip
        assert result['trips_per_call'] == 1

    def test_no_round_trip(self):
        """Test one-way cycle (no return travel)."""
        result = self.calc_case1.calculate(
            shuttle_size_m3=5000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=False
        )

        # Return travel should be 0
        assert result['travel_return_h'] == 0.0

        # Basic cycle includes movement per vessel, not just pumping
        # time_per_vessel_at_destination = movement(1) + setup_in(1) + pump(5) + setup_out(1) = 8
        # basic_cycle = travel_out(2) + time_per_vessel(8) + travel_return(0) = 10
        assert pytest.approx(result['basic_cycle_duration_h']) == 10.0

    def test_same_core_logic_different_travel_times(self):
        """Test that core logic is identical for different travel times."""
        # Case 1 (Busan): short travel
        result1 = self.calc_case1.calculate(
            shuttle_size_m3=5000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Case 2-2 (Ulsan): short travel
        result2 = self.calc_case2_ulsan.calculate(
            shuttle_size_m3=5000.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Setup, pumping, movement times should be IDENTICAL
        assert result1['setup_inbound_h'] == result2['setup_inbound_h']
        assert result1['setup_outbound_h'] == result2['setup_outbound_h']
        assert result1['pumping_per_vessel_h'] == result2['pumping_per_vessel_h']
        assert result1['pumping_total_h'] == result2['pumping_total_h']

        # Only travel times differ
        assert result1['travel_outbound_h'] != result2['travel_outbound_h']
        assert result1['travel_return_h'] != result2['travel_return_h']

    def test_call_duration_method(self):
        """Test call_duration calculation."""
        call_duration = self.calc_case1.calculate_call_duration(
            shuttle_size_m3=2500.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Need 2 trips for 5000 m³ call with 2500 m³ shuttle
        # Each trip = basic_cycle_duration
        cycle = self.calc_case1.calculate(
            shuttle_size_m3=2500.0,
            pump_size_m3ph=1000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        expected = 2 * cycle['basic_cycle_duration_h']
        assert pytest.approx(call_duration) == expected


class TestEdgeCases:
    """Test edge cases."""

    def setup_method(self):
        """Setup for each test."""
        self.calc = ShuttleRoundTripCalculator(
            travel_time_hours=2.0,
            setup_time_hours=0.5
        )

    def test_very_small_shuttle(self):
        """Test with very small shuttle."""
        result = self.calc.calculate(
            shuttle_size_m3=500.0,
            pump_size_m3ph=400.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # 10 trips needed for one call
        assert result['trips_per_call'] == 10

    def test_very_fast_pump(self):
        """Test with very fast pump."""
        result = self.calc.calculate(
            shuttle_size_m3=5000.0,
            pump_size_m3ph=5000.0,
            bunker_volume_per_call_m3=5000.0,
            num_vessels=1,
            is_round_trip=True
        )

        # Pumping time should be 1 hour
        assert pytest.approx(result['pumping_per_vessel_h']) == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
