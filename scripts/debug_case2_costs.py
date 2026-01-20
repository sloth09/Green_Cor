"""
Debug script to analyze Case 2 cost calculations in detail
"""

import sys
from src.config_loader import ConfigLoader
from src.cost_calculator import CostCalculator
from src.utils import interpolate_mcr, calculate_annual_demand, calculate_vessel_growth, calculate_m3_per_voyage

# Load Case 2-2 (Ulsan) configuration
config = ConfigLoader().load_config("case_2_ulsan")

print("="*80)
print("CASE 2-2 (ULSAN → BUSAN) COST ANALYSIS")
print("="*80)
print()

# Basic parameters
print("BASIC PARAMETERS:")
print(f"  Travel time (one-way): {config['operations']['travel_time_hours']} hours")
print(f"  Bunker volume per call: {config['bunkering']['bunker_volume_per_call_m3']} m³")
print(f"  2050 vessel count: {config['shipping']['end_vessels']} vessels")
print()

# Calculate demand
start_year = config['time_period']['start_year']
end_year = config['time_period']['end_year']
kg_per_voyage = config['shipping']['kg_per_voyage']
voyages_per_year = config['shipping']['voyages_per_year']
density = config['ammonia']['density_storage_ton_m3']

vessel_growth = calculate_vessel_growth(start_year, end_year,
                                        config['shipping']['start_vessels'],
                                        config['shipping']['end_vessels'])
m3_per_voyage = calculate_m3_per_voyage(kg_per_voyage, density)
annual_demand = calculate_annual_demand(vessel_growth, m3_per_voyage, voyages_per_year)
demand_2050 = annual_demand[end_year]

print(f"Annual demand in 2050: {demand_2050:,.0f} m³")
print()

# Cost calculator
cost_calc = CostCalculator(config)

# Shuttle sizes
shuttle_sizes = config['shuttle']['available_sizes_cbm']
mcr_map = config['shuttle']['mcr_map_kw']

print("="*80)
print("DETAILED COST COMPARISON FOR DIFFERENT SHUTTLE SIZES (2050)")
print("="*80)
print()

# Prepare comparison data
comparisons = []

for shuttle_size in [5000, 10000, 25000, 50000]:
    if shuttle_size not in shuttle_sizes:
        continue

    mcr = mcr_map.get(shuttle_size, 0)
    if mcr == 0:
        continue

    # Cost components
    shuttle_capex = cost_calc.calculate_shuttle_capex(shuttle_size)
    shuttle_fixed_opex = cost_calc.calculate_shuttle_fixed_opex(shuttle_size)
    pump_capex = cost_calc.calculate_pump_capex(1200)  # Reference pump size
    bunk_fixed_opex = cost_calc.calculate_bunkering_fixed_opex(shuttle_size, 1200)

    # Fuel costs per cycle (one trip from Ulsan to Busan + back)
    # Case 2: shuttle delivers full capacity per trip
    travel_hours = config['operations']['travel_time_hours']
    sfoc = config['propulsion']['sfoc_g_per_kwh']
    fuel_price = config['economy']['fuel_price_usd_per_ton']

    shuttle_fuel_per_cycle = (mcr * sfoc * travel_hours) / 1e6
    shuttle_fuel_cost_per_cycle = shuttle_fuel_per_cycle * fuel_price

    # Annual trips needed for 2050
    annual_trips = demand_2050 / shuttle_size
    annual_vessels_needed = max(1, int((annual_trips * travel_hours * 2 + annual_trips * 0.5 * 2) / 8000))

    print(f"SHUTTLE SIZE: {shuttle_size} m³")
    print(f"{'─'*76}")
    print(f"  MCR: {mcr} kW")
    print(f"  Annual trips needed: {annual_trips:.0f}")
    print(f"  Estimated vessels needed: {annual_vessels_needed}")
    print()
    print(f"  CAPEX:")
    print(f"    Shuttle CAPEX (per unit): ${shuttle_capex:,.0f}")
    print(f"    Pump CAPEX (1200 m³/h):  ${pump_capex:,.0f}")
    print(f"    Total CAPEX (per combo):  ${shuttle_capex + pump_capex:,.0f}")
    print()
    print(f"  ANNUAL OPEX (per shuttle):")
    print(f"    Shuttle fuel per cycle: {shuttle_fuel_per_cycle:.3f} ton")
    print(f"    Shuttle fuel cost per cycle: ${shuttle_fuel_cost_per_cycle:,.0f}")
    print(f"    Annual shuttle fuel cost (2050): ${shuttle_fuel_cost_per_cycle * annual_trips:,.0f}")
    print(f"    Fixed OPEX (Shuttle): ${shuttle_fixed_opex:,.0f}")
    print(f"    Fixed OPEX (Bunkering): ${bunk_fixed_opex:,.0f}")
    print()

    # Pump fuel cost
    pump_size = 1200
    pump_hours_per_trip = 2 * (shuttle_size / pump_size)
    pump_power = cost_calc.calculate_pump_power(pump_size, 4.0, 0.7)
    pump_fuel_per_trip = (pump_power * pump_hours_per_trip * sfoc) / 1e6
    pump_fuel_cost_per_trip = pump_fuel_per_trip * fuel_price

    print(f"  PUMP FUEL (1200 m³/h):")
    print(f"    Pumping hours per trip: {pump_hours_per_trip:.2f} hours")
    print(f"    Pump fuel per trip: {pump_fuel_per_trip:.3f} ton")
    print(f"    Pump fuel cost per trip: ${pump_fuel_cost_per_trip:,.0f}")
    print(f"    Annual pump fuel cost (2050): ${pump_fuel_cost_per_trip * annual_trips:,.0f}")
    print()

    # Fuel cost per m³ delivered
    fuel_cost_per_m3_delivered = (shuttle_fuel_cost_per_cycle + pump_fuel_cost_per_trip) / shuttle_size
    print(f"  FUEL COST PER M³ DELIVERED: ${fuel_cost_per_m3_delivered:.2f}/m³")
    print()

    # 20-year NPC (rough estimate)
    discount_rate = config['economy']['discount_rate']
    years = list(range(start_year, end_year + 1))
    npc_capex = 0
    npc_shuttle_fuel = 0
    npc_pump_fuel = 0
    npc_fixed_opex = 0

    for year in years:
        disc_factor = 1 / ((1 + discount_rate) ** (year - start_year))
        year_demand = annual_demand[year]
        year_trips = year_demand / shuttle_size
        year_vessels = max(1, int((year_trips * travel_hours * 2 + year_trips * 0.5 * 2) / 8000))

        # CAPEX only in first year or when adding vessels
        if year == start_year:
            npc_capex += disc_factor * (shuttle_capex + pump_capex) * year_vessels

        # OPEX every year
        npc_shuttle_fuel += disc_factor * shuttle_fuel_cost_per_cycle * year_trips
        npc_pump_fuel += disc_factor * pump_fuel_cost_per_trip * year_trips
        npc_fixed_opex += disc_factor * (shuttle_fixed_opex + bunk_fixed_opex) * year_vessels

    npc_total = npc_capex + npc_shuttle_fuel + npc_pump_fuel + npc_fixed_opex

    print(f"  ESTIMATED 20-YEAR NPC:")
    print(f"    CAPEX (initial):        ${npc_capex/1e6:>10.2f}M")
    print(f"    Shuttle Fuel (20yr):    ${npc_shuttle_fuel/1e6:>10.2f}M")
    print(f"    Pump Fuel (20yr):       ${npc_pump_fuel/1e6:>10.2f}M")
    print(f"    Fixed OPEX (20yr):      ${npc_fixed_opex/1e6:>10.2f}M")
    print(f"    {'─'*48}")
    print(f"    TOTAL NPC:              ${npc_total/1e6:>10.2f}M")
    print()

    comparisons.append({
        'Shuttle Size': shuttle_size,
        'MCR (kW)': mcr,
        'Trips (2050)': annual_trips,
        'Fuel Cost/Trip': shuttle_fuel_cost_per_cycle + pump_fuel_cost_per_trip,
        'CAPEX': shuttle_capex + pump_capex,
        'NPC_Total (M)': npc_total / 1e6,
        'Fuel/m³': fuel_cost_per_m3_delivered
    })

print()
print("="*80)
print("SUMMARY COMPARISON")
print("="*80)
print()

import pandas as pd
df = pd.DataFrame(comparisons)
print(df.to_string(index=False))
print()

# Calculate efficiency per m³
print("EFFICIENCY ANALYSIS:")
print()
for row in comparisons:
    print(f"{row['Shuttle Size']:>6} m³: Fuel cost/m³ = ${row['Fuel/m³']:.2f}")
print()

print("KEY INSIGHTS:")
print("─" * 80)
print("1. Large shuttles have HIGHER MCR → higher fuel consumption per cycle")
print("   Example: 25,000 m³ (MCR 2,981) vs 5,000 m³ (MCR 1,694)")
print("   MCR ratio: 2,981 / 1,694 = 1.76x")
print()
print("2. Although large shuttles make fewer trips, they consume more fuel per trip")
print("   due to their higher MCR ratings, making per-m³ fuel cost higher")
print()
print("3. However, CAPEX scaling (exponent 0.75) means large shuttles are more")
print("   expensive to build, but cheaper per-m³ delivered in CAPEX terms")
print()
print("4. The OPTIMIZATION is searching for the TOTAL COST MINIMUM, which")
print("   balances CAPEX, OPEX, and FUEL COSTS")
print()
print("="*80)
