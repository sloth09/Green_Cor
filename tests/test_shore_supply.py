"""
Unit tests for ShoreSupply module.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.shore_supply import ShoreSupply


# Test configurations
SHORE_SUPPLY_ENABLED = {
    "shore_supply": {
        "enabled": True,
        "pump_rate_m3ph": 1500.0,
        "loading_time_fixed_hours": 0.0,
    }
}

SHORE_SUPPLY_CUSTOM = {
    "shore_supply": {
        "enabled": True,
        "pump_rate_m3ph": 2000.0,
        "loading_time_fixed_hours": 0.5,
    }
}

SHORE_SUPPLY_DISABLED = {
    "shore_supply": {
        "enabled": False,
    }
}

SHORE_SUPPLY_DEFAULTS = {}  # Should use default values


class TestShoreSupplyInitialization:
    """Test ShoreSupply initialization."""

    def test_standard_configuration(self):
        """Test initialization with standard config."""
        ss = ShoreSupply(SHORE_SUPPLY_ENABLED)

        assert ss.enabled is True
        assert ss.pump_rate_m3ph == 1500.0
        assert ss.fixed_time_hours == 0.0

    def test_custom_configuration(self):
        """Test initialization with custom pump rate and fixed time."""
        ss = ShoreSupply(SHORE_SUPPLY_CUSTOM)

        assert ss.enabled is True
        assert ss.pump_rate_m3ph == 2000.0
        assert ss.fixed_time_hours == 0.5

    def test_disabled_configuration(self):
        """Test initialization with disabled shore supply."""
        ss = ShoreSupply(SHORE_SUPPLY_DISABLED)

        assert ss.enabled is False

    def test_default_configuration(self):
        """Test initialization with missing shore_supply config."""
        ss = ShoreSupply(SHORE_SUPPLY_DEFAULTS)

        assert ss.enabled is True
        assert ss.pump_rate_m3ph == 1500.0  # Standard rate
        assert ss.fixed_time_hours == 0.0


class TestShoreSupplyMethods:
    """Test ShoreSupply methods."""

    def setup_method(self):
        """Setup for each test."""
        self.ss = ShoreSupply(SHORE_SUPPLY_ENABLED)
        self.ss_custom = ShoreSupply(SHORE_SUPPLY_CUSTOM)

    def test_is_enabled(self):
        """Test is_enabled method."""
        assert self.ss.is_enabled() is True
        assert ShoreSupply(SHORE_SUPPLY_DISABLED).is_enabled() is False

    def test_get_pump_rate(self):
        """Test get_pump_rate method."""
        assert self.ss.get_pump_rate() == 1500.0
        assert self.ss_custom.get_pump_rate() == 2000.0

    def test_load_shuttle_5000m3(self):
        """Test loading time for 5000 m³ shuttle."""
        # Time = 5000 / 1500 = 3.33 hours
        time = self.ss.load_shuttle(5000.0)
        assert pytest.approx(time, rel=1e-3) == 3.333

    def test_load_shuttle_25000m3(self):
        """Test loading time for 25000 m³ shuttle."""
        # Time = 25000 / 1500 = 16.67 hours
        time = self.ss.load_shuttle(25000.0)
        assert pytest.approx(time, rel=1e-3) == 16.667

    def test_load_shuttle_custom_pump_rate(self):
        """Test loading with custom pump rate."""
        # Time = (5000 / 2000) + 0.5 (fixed) = 2.5 + 0.5 = 3.0 hours
        time = self.ss_custom.load_shuttle(5000.0)
        assert pytest.approx(time) == 3.0

    def test_load_shuttle_with_fixed_time(self):
        """Test loading time includes fixed overhead."""
        # Time = (5000 / 2000) + 0.5 = 2.5 + 0.5 = 3.0 hours
        time = self.ss_custom.load_shuttle(5000.0)
        assert pytest.approx(time) == 3.0

    def test_load_shuttle_disabled(self):
        """Test loading time when disabled."""
        ss_disabled = ShoreSupply(SHORE_SUPPLY_DISABLED)
        time = ss_disabled.load_shuttle(5000.0)
        assert time == 0.0

    def test_unload_shuttle(self):
        """Test unloading returns zero."""
        # Standard: no offloading at source
        time = self.ss.unload_shuttle(5000.0)
        assert time == 0.0

    def test_unload_shuttle_disabled(self):
        """Test unloading when disabled."""
        ss_disabled = ShoreSupply(SHORE_SUPPLY_DISABLED)
        time = ss_disabled.unload_shuttle(5000.0)
        assert time == 0.0

    def test_calculate_load_unload_time_load_only(self):
        """Test combined load time (unload not included)."""
        time = self.ss.calculate_load_unload_time(5000.0, include_unload=False)
        assert pytest.approx(time, rel=1e-3) == 3.333

    def test_calculate_load_unload_time_both(self):
        """Test combined load+unload time."""
        # Since unload is 0, should be same as load
        time = self.ss.calculate_load_unload_time(5000.0, include_unload=True)
        assert pytest.approx(time, rel=1e-3) == 3.333

    def test_calculate_pump_capacity(self):
        """Test pump capacity getter."""
        assert self.ss.calculate_pump_capacity() == 1500.0
        assert self.ss_custom.calculate_pump_capacity() == 2000.0

    def test_get_annual_loading_capacity(self):
        """Test annual loading capacity calculation."""
        # 8000 hours * 1500 m³/h = 12,000,000 m³
        capacity = self.ss.get_annual_loading_capacity()
        assert capacity == 12_000_000.0

        # Custom: 8000 * 2000 = 16,000,000 m³
        capacity_custom = self.ss_custom.get_annual_loading_capacity()
        assert capacity_custom == 16_000_000.0


class TestShoreSupplyValidation:
    """Test configuration validation."""

    def test_validate_valid_configuration(self):
        """Test validation of valid configuration."""
        ss = ShoreSupply(SHORE_SUPPLY_ENABLED)
        assert ss.validate_configuration() is True

    def test_validate_negative_pump_rate(self):
        """Test validation fails with negative pump rate."""
        config = {
            "shore_supply": {
                "pump_rate_m3ph": -1500.0,
            }
        }
        ss = ShoreSupply(config)

        with pytest.raises(ValueError, match="Invalid shore supply pump rate"):
            ss.validate_configuration()

    def test_validate_zero_pump_rate(self):
        """Test validation fails with zero pump rate."""
        config = {
            "shore_supply": {
                "pump_rate_m3ph": 0.0,
            }
        }
        ss = ShoreSupply(config)

        with pytest.raises(ValueError, match="Invalid shore supply pump rate"):
            ss.validate_configuration()

    def test_validate_negative_fixed_time(self):
        """Test validation fails with negative fixed time."""
        config = {
            "shore_supply": {
                "pump_rate_m3ph": 1500.0,
                "loading_time_fixed_hours": -1.0,
            }
        }
        ss = ShoreSupply(config)

        with pytest.raises(ValueError, match="Invalid fixed loading time"):
            ss.validate_configuration()

    def test_validate_zero_fixed_time_ok(self):
        """Test validation passes with zero fixed time."""
        config = {
            "shore_supply": {
                "pump_rate_m3ph": 1500.0,
                "loading_time_fixed_hours": 0.0,
            }
        }
        ss = ShoreSupply(config)
        assert ss.validate_configuration() is True


class TestShoreSupplyRepresentation:
    """Test string representation."""

    def test_repr_enabled(self):
        """Test __repr__ for enabled shore supply."""
        ss = ShoreSupply(SHORE_SUPPLY_ENABLED)
        repr_str = repr(ss)

        assert "ShoreSupply" in repr_str
        assert "Enabled" in repr_str
        assert "1500" in repr_str

    def test_repr_disabled(self):
        """Test __repr__ for disabled shore supply."""
        ss = ShoreSupply(SHORE_SUPPLY_DISABLED)
        repr_str = repr(ss)

        assert "ShoreSupply" in repr_str
        assert "Disabled" in repr_str


class TestShoreSupplyScaling:
    """Test shore supply scaling and proportions."""

    def setup_method(self):
        """Setup for each test."""
        self.ss = ShoreSupply(SHORE_SUPPLY_ENABLED)

    def test_loading_time_proportional_to_size(self):
        """Test that loading time scales linearly with shuttle size."""
        time_5000 = self.ss.load_shuttle(5000.0)
        time_10000 = self.ss.load_shuttle(10000.0)
        time_25000 = self.ss.load_shuttle(25000.0)

        # Should be linear
        assert pytest.approx(time_10000) == time_5000 * 2
        assert pytest.approx(time_25000) == time_5000 * 5

    def test_loading_time_scales_inversely_with_pump_rate(self):
        """Test that loading time scales inversely with pump rate."""
        ss_1500 = ShoreSupply({"shore_supply": {"pump_rate_m3ph": 1500.0}})
        ss_3000 = ShoreSupply({"shore_supply": {"pump_rate_m3ph": 3000.0}})

        time_1500 = ss_1500.load_shuttle(5000.0)
        time_3000 = ss_3000.load_shuttle(5000.0)

        # Double pump rate should halve loading time
        assert pytest.approx(time_3000) == time_1500 / 2

    def test_various_shuttle_sizes(self):
        """Test loading times for various shuttle sizes."""
        expected_times = {
            500.0: 500.0 / 1500.0,
            1000.0: 1000.0 / 1500.0,
            2500.0: 2500.0 / 1500.0,
            5000.0: 5000.0 / 1500.0,
            10000.0: 10000.0 / 1500.0,
            25000.0: 25000.0 / 1500.0,
            50000.0: 50000.0 / 1500.0,
        }

        for size, expected_time in expected_times.items():
            actual_time = self.ss.load_shuttle(size)
            assert pytest.approx(actual_time, rel=1e-6) == expected_time


class TestShoreSupplyStandardPump:
    """Test standard pump rate constant."""

    def test_standard_pump_rate(self):
        """Test that standard pump rate is 1500 m³/h."""
        assert ShoreSupply.STANDARD_PUMP_RATE_M3PH == 1500.0

    def test_default_uses_standard_pump_rate(self):
        """Test that default config uses standard pump rate."""
        ss = ShoreSupply({})
        assert ss.pump_rate_m3ph == ShoreSupply.STANDARD_PUMP_RATE_M3PH


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
