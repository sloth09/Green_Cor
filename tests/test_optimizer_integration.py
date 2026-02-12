"""
Integration test for BunkeringOptimizer with new modules.

Tests that the optimizer works correctly with CycleTimeCalculator and ShoreSupply.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config_loader import ConfigLoader
from src.optimizer import BunkeringOptimizer


def test_optimizer_case1_with_new_modules():
    """Test optimizer with new modules for Case 1."""
    # Load configuration
    config_loader = ConfigLoader()
    config = config_loader.load_config("case_1")

    # Create optimizer
    optimizer = BunkeringOptimizer(config)

    # Verify new modules are initialized
    assert optimizer.cycle_calc is not None
    assert optimizer.shore_supply is not None

    # Shore supply cost is disabled by default in base.yaml (enabled: false)
    # but pump rate is still set and used for time calculations
    assert optimizer.shore_supply.pump_rate_m3ph == 700.0

    print("[PASS] Optimizer Case 1 initialization with new modules")


def test_optimizer_case2_ulsan_with_new_modules():
    """Test optimizer with new modules for Case 2 (Ulsan)."""
    # Load configuration
    config_loader = ConfigLoader()
    config = config_loader.load_config("case_2")

    # Create optimizer
    optimizer = BunkeringOptimizer(config)

    # Verify new modules are initialized
    assert optimizer.cycle_calc is not None
    assert optimizer.shore_supply is not None

    # Verify shore supply pump rate
    assert optimizer.shore_supply.get_pump_rate() == 700.0

    print("[PASS] Optimizer Case 2 (Ulsan) initialization with new modules")


def test_cycle_time_calculation_case1():
    """Test that cycle time is calculated correctly for Case 1."""
    config_loader = ConfigLoader()
    config = config_loader.load_config("case_1")

    optimizer = BunkeringOptimizer(config)

    # Test a specific shuttle/pump combination
    cycle_info = optimizer.cycle_calc.calculate_single_cycle(5000.0, 1000.0)

    # Verify result structure
    assert "cycle_duration" in cycle_info
    assert "call_duration" in cycle_info
    assert "shore_loading" in cycle_info

    # Verify reasonable values
    assert cycle_info["shore_loading"] > 0  # Should include shore loading time
    assert cycle_info["cycle_duration"] > cycle_info["shore_loading"]  # Cycle should be longer

    print("[PASS] Case 1 cycle time calculation includes shore loading")
    print(f"  Shore loading: {cycle_info['shore_loading']:.2f}h")
    print(f"  Cycle duration: {cycle_info['cycle_duration']:.2f}h")


def test_cycle_time_calculation_case2():
    """Test that cycle time is calculated correctly for Case 2."""
    config_loader = ConfigLoader()
    config = config_loader.load_config("case_2")

    optimizer = BunkeringOptimizer(config)

    # Test a larger shuttle for Case 2
    cycle_info = optimizer.cycle_calc.calculate_single_cycle(25000.0, 1000.0, num_vessels=5)

    # Verify result structure
    assert "cycle_duration" in cycle_info
    assert "call_duration" in cycle_info
    assert "shore_loading" in cycle_info

    # Verify reasonable values for long-distance
    assert cycle_info["shore_loading"] > 0
    assert cycle_info["travel_outbound"] > 0  # Should include travel time
    assert cycle_info["travel_return"] > 0

    print("[PASS] Case 2 cycle time calculation with travel times")
    print(f"  Shore loading: {cycle_info['shore_loading']:.2f}h")
    print(f"  Travel outbound: {cycle_info['travel_outbound']:.2f}h")
    print(f"  Travel return: {cycle_info['travel_return']:.2f}h")
    print(f"  Cycle duration: {cycle_info['cycle_duration']:.2f}h")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("BunkeringOptimizer Integration Tests")
    print("="*60 + "\n")

    try:
        test_optimizer_case1_with_new_modules()
        test_optimizer_case2_ulsan_with_new_modules()
        test_cycle_time_calculation_case1()
        test_cycle_time_calculation_case2()

        print("\n" + "="*60)
        print("All integration tests passed!")
        print("="*60)

    except Exception as e:
        print(f"\n[FAIL] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
