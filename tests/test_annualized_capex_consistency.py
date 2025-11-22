"""
Test script to verify Annualized CAPEX implementation.

Verifies that:
1. Single mode NPC_Total equals Yearly Simulation 21-year sum of Total_Year_Cost
2. Optimizer runs without errors
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import load_config, BunkeringOptimizer
from main import run_yearly_simulation

def test_annualized_capex_consistency():
    """
    Test that Single mode NPC_Total matches Yearly Simulation 21-year sum.
    """
    print("\n" + "="*80)
    print("Testing Annualized CAPEX Consistency")
    print("="*80)
    
    # Load config
    config = load_config("case_1")
    
    # Limit to one shuttle/pump combination for quick test
    config["shuttle"]["available_sizes_cbm"] = [5000]
    config["pumps"]["available_flow_rates"] = [500]
    
    shuttle_size = 5000
    pump_size = 500
    
    print(f"\nTest Configuration:")
    print(f"  Case: {config.get('case_name', 'Unknown')}")
    print(f"  Shuttle: {shuttle_size} m³")
    print(f"  Pump: {pump_size} m³/h")
    
    # Run yearly_simulation
    print("\n[1/2] Running yearly_simulation mode...")
    output_path = Path("results")
    output_path.mkdir(exist_ok=True)
    
    yearly_df = run_yearly_simulation(config, shuttle_size, pump_size, output_path)
    
    if yearly_df is None:
        print("[FAIL] Yearly simulation failed")
        return False
    
    yearly_total = yearly_df['Total_Year_Cost_USDm'].sum()
    print(f"  Yearly Simulation 21-year sum: ${yearly_total:.2f}M")
    
    # Run single mode optimization
    print("\n[2/2] Running single mode optimization...")
    optimizer = BunkeringOptimizer(config)
    scenario_df, yearly_results_df = optimizer.solve()
    
    if scenario_df.empty:
        print("[FAIL] Optimization produced no results")
        return False
    
    # Find matching scenario
    matching = scenario_df[
        (scenario_df['Shuttle_Size_cbm'] == shuttle_size) & 
        (scenario_df['Pump_Size_m3ph'] == pump_size)
    ]
    
    if matching.empty:
        print(f"[FAIL] No matching scenario found for {shuttle_size}/{pump_size}")
        return False
    
    single_npc = matching['NPC_Total_USDm'].values[0]
    print(f"  Single Mode NPC_Total: ${single_npc:.2f}M")
    
    # Also calculate sum from yearly_results_df
    yearly_opt_df = yearly_results_df[
        (yearly_results_df['Shuttle_Size_cbm'] == shuttle_size) &
        (yearly_results_df['Pump_Size_m3ph'] == pump_size)
    ]
    yearly_opt_total = yearly_opt_df['Total_Year_Cost_USDm'].sum()
    print(f"  Single Mode Yearly Sum: ${yearly_opt_total:.2f}M")
    
    # Verify they match
    print("\n" + "="*80)
    print("Verification Results:")
    print("="*80)
    
    diff_pct = abs(yearly_total - single_npc) / single_npc * 100 if single_npc > 0 else 0
    diff_opt_pct = abs(yearly_opt_total - single_npc) / single_npc * 100 if single_npc > 0 else 0
    
    print(f"Yearly Simulation vs Single NPC:")
    print(f"  Difference: ${abs(yearly_total - single_npc):.4f}M ({diff_pct:.4f}%)")
    
    print(f"\nSingle Yearly Sum vs Single NPC:")
    print(f"  Difference: ${abs(yearly_opt_total - single_npc):.4f}M ({diff_opt_pct:.4f}%)")
    
    # Check if within tolerance (0.25% - accounting for rounding differences)
    tolerance = 0.0025  # 0.25%
    
    if diff_pct < tolerance:
        print(f"\n✓ [PASS] Yearly Simulation matches Single NPC (within {tolerance*100}% tolerance)")
        success1 = True
    else:
        print(f"\n✗ [FAIL] Yearly Simulation does NOT match Single NPC")
        success1 = False
    
    if diff_opt_pct < tolerance:
        print(f"✓ [PASS] Single Yearly Sum matches Single NPC (within {tolerance*100}% tolerance)")
        success2 = True
    else:
        print(f"✗ [FAIL] Single Yearly Sum does NOT match Single NPC")
        success2 = False
    
    print("="*80)
    
    return success1 and success2


if __name__ == "__main__":
    try:
        success = test_annualized_capex_consistency()
        
        if success:
            print("\n" + "="*80)
            print("ALL TESTS PASSED ✓")
            print("="*80)
            sys.exit(0)
        else:
            print("\n" + "="*80)
            print("TESTS FAILED ✗")
            print("="*80)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
