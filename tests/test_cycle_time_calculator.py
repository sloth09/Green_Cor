"""
Unit tests for CycleTimeCalculator module.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.cycle_time_calculator import CycleTimeCalculator


# Test configurations
CASE1_CONFIG = {
    "operations": {
        "travel_time_hours": 2.0,
        "setup_time_hours": 2.0,
        "has_storage_at_busan": True,
    },
    "bunkering": {
        "bunker_volume_per_call_m3": 5000.0,
    }
}

CASE2_ULSAN_CONFIG = {
    "operations": {
        "travel_time_hours": 1.67,
        "setup_time_hours": 2.0,
        "has_storage_at_busan": False,
    },
    "bunkering": {
        "bunker_volume_per_call_m3": 5000.0,
    }
}

CASE2_YEOSU_CONFIG = {
    "operations": {
        "travel_time_hours": 5.63,
        "setup_time_hours": 2.0,
        "has_storage_at_busan": False,
    },
    "bunkering": {
        "bunker_volume_per_call_m3": 5000.0,
    }
}


class TestCycleTimeCalculatorCase1:
    """Test Case 1 (Busan port-based storage)."""

    def setup_method(self):
        """Setup for each test."""
        self.calc = CycleTimeCalculator("case_1", CASE1_CONFIG)

    def test_initialization(self):
        """Test calculator initialization."""
        assert self.calc.case_type == "case_1"
        assert self.calc.travel_time_hours == 2.0
        assert self.calc.has_storage_at_busan is True
        assert self.calc.SHORE_PUMP_RATE_M3PH == 700.0

    def test_shore_loading_time_5000m3(self):
        """Test shore loading time for 5,000 m³ shuttle."""
        # Expected: 5000 / 700 = 7.143 hours
        time = self.calc.calculate_shore_loading_time(5000.0)
        assert pytest.approx(time, rel=1e-3) == 7.143

    def test_shore_loading_time_25000m3(self):
        """Test shore loading time for 25,000 m³ shuttle."""
        # Expected: 25000 / 700 = 35.714 hours
        time = self.calc.calculate_shore_loading_time(25000.0)
        assert pytest.approx(time, rel=1e-3) == 35.714

    def test_pumping_time_5000m3_1000m3ph(self):
        """Test pumping time calculation."""
        # 5000 / 1000 = 5 hours
        time = self.calc.calculate_pumping_time(5000.0, 1000.0)
        assert pytest.approx(time) == 5.0

    def test_single_cycle_5000m3_1000m3ph(self):
        """Test complete Case 1 cycle for 5000m3 shuttle, 1000 m³/h pump."""
        result = self.calc.calculate_single_cycle(5000.0, 1000.0)

        # Verify structure
        assert "shore_loading" in result
        assert "travel_outbound" in result
        assert "cycle_duration" in result

        # Case 1 specific checks
        assert result["case_type"] == "case_1"

        # Check individual components
        # shore_loading = 5000/700 = 7.143h
        assert pytest.approx(result["shore_loading"], rel=1e-3) == 7.143
        assert pytest.approx(result["travel_outbound"]) == 2.0
        assert pytest.approx(result["travel_return"]) == 2.0

        # basic_cycle = travel(2) + setup_in(2) + pump(5) + setup_out(2) + travel(2) = 13.0
        # cycle_duration = shore_loading(7.143) + basic_cycle(13.0) = 20.143
        # call_duration = trips_per_call(1) * cycle_duration = 20.143
        assert pytest.approx(result["call_duration"], abs=0.1) == 20.143
        assert pytest.approx(result["cycle_duration"], abs=0.1) == 20.143

    def test_single_cycle_3000m3_1200m3ph(self):
        """Test Case 1 cycle with 3000 m³ shuttle."""
        result = self.calc.calculate_single_cycle(3000.0, 1200.0)

        # 3000 < 5000, so trips_per_call = 2
        assert result["trips_per_call"] == 2

        # Shore loading = 3000 / 700 = 4.286 hours
        assert pytest.approx(result["shore_loading"], rel=1e-3) == 4.286

    def test_annual_operations_case1(self):
        """Test annual operations calculation for Case 1."""
        result = self.calc.calculate_single_cycle(5000.0, 1000.0)
        cycle_duration = result["cycle_duration"]

        # Annual ops = 8000 / cycle_duration
        annual_ops = self.calc.get_annual_operations_per_shuttle(cycle_duration)
        # cycle_duration = 20.143h
        # annual_ops = 8000 / 20.143 ≈ 397
        assert pytest.approx(annual_ops, abs=1) == 397


class TestCycleTimeCalculatorCase2:
    """Test Case 2 (Production-based, long-distance)."""

    def setup_method(self):
        """Setup for each test."""
        self.calc_ulsan = CycleTimeCalculator("case_2", CASE2_ULSAN_CONFIG)
        self.calc_yeosu = CycleTimeCalculator("case_3", CASE2_YEOSU_CONFIG)

    def test_initialization_case2_ulsan(self):
        """Test Case 2 initialization."""
        assert self.calc_ulsan.case_type == "case_2"
        assert self.calc_ulsan.travel_time_hours == 1.67
        assert self.calc_ulsan.has_storage_at_busan is False

    def test_single_cycle_case2_ulsan_25000m3_1000m3ph(self):
        """Test complete Case 2 cycle for 25000 m³ shuttle, 5 vessels."""
        result = self.calc_ulsan.calculate_single_cycle(25000.0, 1000.0, num_vessels=5)

        # Verify structure
        assert result["case_type"] == "case_2"
        assert result["vessels_per_trip"] == 5  # 25000 / 5000 = 5 vessels

        # Shore loading = 25000 / 700 = 35.714 hours
        assert pytest.approx(result["shore_loading"], rel=1e-3) == 35.714

        # Check travel times (Ulsan specific)
        assert pytest.approx(result["travel_outbound"]) == 1.67
        assert pytest.approx(result["travel_return"]) == 1.67

        # Per vessel pumping = 5000 / 1000 = 5 hours
        assert pytest.approx(result["pumping_per_vessel"]) == 5.0

        # Total pumping = pumping_per_vessel * num_vessels
        # = 5 * 5 = 25 hours
        assert pytest.approx(result["pumping_total"]) == 25.0

    def test_cycle_duration_case2_ulsan_vs_yeosu(self):
        """Test that Ulsan is significantly faster than Yeosu."""
        result_ulsan = self.calc_ulsan.calculate_single_cycle(25000.0, 1000.0, num_vessels=5)
        result_yeosu = self.calc_yeosu.calculate_single_cycle(25000.0, 1000.0, num_vessels=5)

        cycle_ulsan = result_ulsan["cycle_duration"]
        cycle_yeosu = result_yeosu["cycle_duration"]

        # Ulsan should be faster
        assert cycle_ulsan < cycle_yeosu

        # Difference should be approximately 2 * (5.63 - 1.67) = 7.92 hours
        time_diff = cycle_yeosu - cycle_ulsan
        assert pytest.approx(time_diff, abs=0.5) == 7.92

    def test_case2_small_shuttle(self):
        """Test Case 2 with small shuttle (5000 m³) serving 1 vessel."""
        result = self.calc_ulsan.calculate_single_cycle(5000.0, 1000.0, num_vessels=1)

        assert result["vessels_per_trip"] == 1
        # pumping_total = pumping_per_vessel * num_vessels
        # = 5 * 1 = 5 hours
        assert pytest.approx(result["pumping_total"]) == 5.0

    def test_case2_large_shuttle(self):
        """Test Case 2 with large shuttle (50000 m³) serving 10 vessels."""
        result = self.calc_ulsan.calculate_single_cycle(50000.0, 1000.0, num_vessels=10)

        assert result["vessels_per_trip"] == 10
        # Shore loading = 50000 / 700 = 71.429 hours
        assert pytest.approx(result["shore_loading"], rel=1e-3) == 71.429


class TestShoreLoadingComparison:
    """Compare shore loading across all cases."""

    def test_standard_5000m3_shuttle(self):
        """Test that 5000 m³ shuttle takes 7.143 hours to load."""
        calc1 = CycleTimeCalculator("case_1", CASE1_CONFIG)
        calc2 = CycleTimeCalculator("case_2", CASE2_ULSAN_CONFIG)

        # Both should have identical shore loading time
        time1 = calc1.calculate_shore_loading_time(5000.0)
        time2 = calc2.calculate_shore_loading_time(5000.0)

        assert pytest.approx(time1, rel=1e-3) == pytest.approx(time2, rel=1e-3)
        assert pytest.approx(time1, rel=1e-3) == 7.143

    def test_shore_loading_proportional_to_size(self):
        """Test that shore loading time scales linearly with shuttle size."""
        calc = CycleTimeCalculator("case_1", CASE1_CONFIG)

        time_5000 = calc.calculate_shore_loading_time(5000.0)
        time_10000 = calc.calculate_shore_loading_time(10000.0)
        time_25000 = calc.calculate_shore_loading_time(25000.0)

        # Should scale linearly
        assert pytest.approx(time_10000) == time_5000 * 2
        assert pytest.approx(time_25000) == time_5000 * 5


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_small_shuttle(self):
        """Test with very small shuttle (500 m³)."""
        calc = CycleTimeCalculator("case_1", CASE1_CONFIG)
        result = calc.calculate_single_cycle(500.0, 400.0)

        # Should require 10 trips to satisfy 5000 m³ call
        assert result["trips_per_call"] == 10

    def test_very_large_pump(self):
        """Test with very large pump (2000 m³/h)."""
        calc = CycleTimeCalculator("case_1", CASE1_CONFIG)
        result = calc.calculate_single_cycle(5000.0, 2000.0)

        # Pumping time per vessel = bunker_volume / pump_rate = 5000 / 2000 = 2.5 hours
        # Pumping total = pumping_per_vessel * num_vessels = 2.5 * 1 = 2.5
        assert pytest.approx(result["pumping_per_vessel"]) == 2.5
        assert pytest.approx(result["pumping_total"]) == 2.5

    def test_zero_fixed_time(self):
        """Test that fixed time components are non-zero."""
        calc = CycleTimeCalculator("case_1", CASE1_CONFIG)
        result = calc.calculate_single_cycle(5000.0, 1000.0)

        # Travel, setup, and shore loading should all be non-zero
        assert result["travel_outbound"] > 0
        assert result["setup_inbound"] > 0
        assert result["shore_loading"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
