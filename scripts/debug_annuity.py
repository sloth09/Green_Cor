"""Debug script to trace annuity factor calculation."""

import sys
from pathlib import Path

# Import modules
from src.config_loader import load_config
from src.cost_calculator import CostCalculator

# Load config
config = load_config("case_1")

print("="*80)
print("DEBUGGING ANNUITY FACTOR CALCULATION")
print("="*80)

# Check config values
print("\n1. Config values:")
print(f"   discount_rate: {config['economy']['discount_rate']}")
print(f"   start_year: {config['time_period']['start_year']}")
print(f"   end_year: {config['time_period']['end_year']}")
print(f"   project_years: {config['time_period']['end_year'] - config['time_period']['start_year'] + 1}")

# Create CostCalculator
cost_calc = CostCalculator(config)

# Test get_annuity_factor
annuity_factor = cost_calc.get_annuity_factor()
print(f"\n2. CostCalculator.get_annuity_factor():")
print(f"   Result: {annuity_factor}")

# Test calculate_annualized_capex_yearly with known values
shuttle_capex = 7.6875e6  # $7.6875M per shuttle
pump_capex = 0.865545e6   # $0.865545M per pump
num_shuttles = 2

total_shuttle_asset = num_shuttles * shuttle_capex
total_pump_asset = num_shuttles * pump_capex

annualized_shuttle = cost_calc.calculate_annualized_capex_yearly(total_shuttle_asset)
annualized_pump = cost_calc.calculate_annualized_capex_yearly(total_pump_asset)

print(f"\n3. Test calculate_annualized_capex_yearly (2 shuttles @ 2500m3):")
print(f"   Total shuttle asset: ${total_shuttle_asset/1e6:.6f}M")
print(f"   Total pump asset: ${total_pump_asset/1e6:.6f}M")
print(f"   Annualized shuttle CAPEX: ${annualized_shuttle/1e6:.6f}M")
print(f"   Annualized pump CAPEX: ${annualized_pump/1e6:.6f}M")
print(f"   Annualized total: ${(annualized_shuttle + annualized_pump)/1e6:.6f}M")

# Calculate expected values
expected_annualized_shuttle = total_shuttle_asset / annuity_factor
expected_annualized_pump = total_pump_asset / annuity_factor

print(f"\n4. Expected values (manual calculation):")
print(f"   Expected annualized shuttle: ${expected_annualized_shuttle/1e6:.6f}M")
print(f"   Expected annualized pump: ${expected_annualized_pump/1e6:.6f}M")
print(f"   Expected annualized total: ${(expected_annualized_shuttle + expected_annualized_pump)/1e6:.6f}M")

# Check if they match
shuttle_match = abs(annualized_shuttle - expected_annualized_shuttle) < 1e-3
pump_match = abs(annualized_pump - expected_annualized_pump) < 1e-3

print(f"\n5. Verification:")
print(f"   Shuttle calculation matches: {shuttle_match}")
print(f"   Pump calculation matches: {pump_match}")

if shuttle_match and pump_match:
    print("\n✓ CostCalculator is working correctly!")
else:
    print("\n✗ PROBLEM DETECTED in CostCalculator!")
    
    # Reverse engineer what annuity factor is being used
    if annualized_shuttle > 0:
        actual_annuity_shuttle = total_shuttle_asset / annualized_shuttle
        print(f"   Actual annuity factor (from shuttle): {actual_annuity_shuttle:.4f}")
    
    if annualized_pump > 0:
        actual_annuity_pump = total_pump_asset / annualized_pump
        print(f"   Actual annuity factor (from pump): {actual_annuity_pump:.4f}")

print("\n" + "="*80)

