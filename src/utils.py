"""
Utility functions for bunkering optimization model
- MCR interpolation
- Data validation
- Helper functions
"""

import numpy as np
from typing import Dict, List, Tuple


def interpolate_mcr(mcr_map: Dict[int, float], shuttle_sizes: List[int]) -> Dict[int, float]:
    """
    Interpolate or extrapolate MCR values for shuttle sizes not in the MCR map.

    Uses linear interpolation within known range and logarithmic extrapolation beyond.

    Args:
        mcr_map: Original MCR map with known values
        shuttle_sizes: List of all required shuttle sizes

    Returns:
        Complete MCR map with interpolated/extrapolated values
    """
    complete_mcr = mcr_map.copy()
    sorted_sizes = sorted(mcr_map.keys())

    for size in shuttle_sizes:
        if size in complete_mcr:
            continue

        # Find two nearest known sizes
        below = [s for s in sorted_sizes if s < size]
        above = [s for s in sorted_sizes if s > size]

        if below and above:
            # Linear interpolation
            s1, s2 = below[-1], above[0]
            m1, m2 = mcr_map[s1], mcr_map[s2]

            # Linear interpolation formula
            mcr = m1 + (m2 - m1) * (size - s1) / (s2 - s1)
            complete_mcr[size] = mcr

        elif below:
            # Extrapolation beyond max known size
            s1, s2 = sorted_sizes[-2], sorted_sizes[-1]
            m1, m2 = mcr_map[s1], mcr_map[s2]

            # Use logarithmic extrapolation for large vessels
            # MCR scales as size^0.6 approximately (based on ship design)
            slope = (m2 - m1) / (np.log(s2) - np.log(s1))
            mcr = m2 + slope * (np.log(size) - np.log(s2))
            complete_mcr[size] = mcr

        else:
            # Before minimum (rare case)
            s1, s2 = sorted_sizes[0], sorted_sizes[1]
            m1, m2 = mcr_map[s1], mcr_map[s2]
            mcr = m1 - (m2 - m1) * (s1 - size) / (s2 - s1)
            complete_mcr[size] = mcr

    return complete_mcr


def interpolate_sfoc(sfoc_map: Dict[int, float], shuttle_sizes: List[int], default_sfoc: float = 379.0) -> Dict[int, float]:
    """
    Interpolate SFOC values for shuttle sizes not in the SFOC map.

    Uses linear interpolation within known range and nearest value extrapolation beyond.

    v4: MCR-based SFOC calculation (see docs/parameter/MCR_SFOC_Technical_Report_v4.md)
    MCR < 1,000 kW: 4-stroke high-speed -> 505 g/kWh
    MCR 1,000-2,000 kW: 4-stroke medium-speed -> 448 g/kWh
    MCR 2,000-5,000 kW: 4-stroke medium -> 425 g/kWh
    MCR 5,000-10,000 kW: 4-stroke/2-stroke transition -> 402 g/kWh
    MCR > 10,000 kW: 2-stroke -> 379 g/kWh

    Args:
        sfoc_map: SFOC map with known values (size -> SFOC in g/kWh)
        shuttle_sizes: List of all required shuttle sizes
        default_sfoc: Fallback SFOC value if map is empty

    Returns:
        Complete SFOC map with interpolated values
    """
    if not sfoc_map:
        # If no SFOC map, return default for all sizes
        return {size: default_sfoc for size in shuttle_sizes}

    complete_sfoc = sfoc_map.copy()
    sorted_sizes = sorted(sfoc_map.keys())

    for size in shuttle_sizes:
        if size in complete_sfoc:
            continue

        # Find two nearest known sizes
        below = [s for s in sorted_sizes if s < size]
        above = [s for s in sorted_sizes if s > size]

        if below and above:
            # Linear interpolation
            s1, s2 = below[-1], above[0]
            sfoc1, sfoc2 = sfoc_map[s1], sfoc_map[s2]

            # Linear interpolation formula
            sfoc = sfoc1 + (sfoc2 - sfoc1) * (size - s1) / (s2 - s1)
            complete_sfoc[size] = sfoc

        elif below:
            # Extrapolation beyond max known size - use last known value
            complete_sfoc[size] = sfoc_map[sorted_sizes[-1]]

        else:
            # Before minimum - use first known value
            complete_sfoc[size] = sfoc_map[sorted_sizes[0]]

    return complete_sfoc


def get_sfoc_by_dwt(dwt_ton: float) -> float:
    """
    Get ammonia SFOC based on DWT (deadweight tonnage).

    v4.1: DWT-based SFOC calculation (see docs/parameter/MCR_SFOC_Technical_Report_v4.md)

    DWT ranges and corresponding SFOC values:
    - DWT < 3,000 ton: 4-stroke high-speed -> 505 g/kWh (diesel 220)
    - DWT 3,000-8,000 ton: 4-stroke medium-speed -> 436 g/kWh (diesel 190)
    - DWT 8,000-15,000 ton: 4-stroke medium / small 2-stroke -> 413 g/kWh (diesel 180)
    - DWT 15,000-30,000 ton: 2-stroke -> 390 g/kWh (diesel 170)
    - DWT > 30,000 ton: 2-stroke large -> 379 g/kWh (diesel 165)

    Args:
        dwt_ton: DWT value in tons

    Returns:
        SFOC in g/kWh for ammonia fuel
    """
    if dwt_ton < 3000:
        return 505.0    # 4-stroke high-speed
    elif dwt_ton < 8000:
        return 436.0    # 4-stroke medium-speed
    elif dwt_ton < 15000:
        return 413.0    # 4-stroke medium / small 2-stroke
    elif dwt_ton < 30000:
        return 390.0    # 2-stroke
    else:
        return 379.0    # 2-stroke large


def cargo_to_dwt(cargo_m3: float, density: float = 0.680, cargo_fraction: float = 0.80) -> float:
    """
    Convert cargo volume to DWT (deadweight tonnage).

    Args:
        cargo_m3: Cargo volume in m3
        density: Ammonia density in ton/m3 (default 0.680)
        cargo_fraction: Cargo as fraction of DWT (default 0.80)

    Returns:
        DWT in tons
    """
    cargo_ton = cargo_m3 * density
    dwt = cargo_ton / cargo_fraction
    return dwt


def calculate_m3_per_voyage(kg_per_voyage: float, density_storage: float) -> float:
    """
    Calculate volume per voyage from mass.

    Args:
        kg_per_voyage: Mass per voyage in kg
        density_storage: Storage density in ton/m3

    Returns:
        Volume per voyage in m3
    """
    return kg_per_voyage / (density_storage * 1000.0)


def calculate_bunker_volume_per_call(
    m3_per_voyage: float,
    k_voyages_per_call: int,
    override_volume: float = None
) -> float:
    """
    Calculate bunkering volume per call.

    Args:
        m3_per_voyage: Volume per voyage in m3
        k_voyages_per_call: Number of voyages per call
        override_volume: If provided, use this value instead of calculation

    Returns:
        Bunkering volume per call in m3
    """
    if override_volume is not None:
        return override_volume

    return k_voyages_per_call * m3_per_voyage


def calculate_vessel_growth(
    start_year: int,
    end_year: int,
    start_vessels: int,
    end_vessels: int
) -> Dict[int, int]:
    """
    Calculate vessel fleet growth over time (linear growth).

    Args:
        start_year: Starting year
        end_year: Ending year
        start_vessels: Number of vessels at start year
        end_vessels: Number of vessels at end year

    Returns:
        Dictionary mapping year to vessel count
    """
    years = range(start_year, end_year + 1)
    total_years = end_year - start_year

    vessel_growth = {}
    for year in years:
        # Linear interpolation
        fraction = (year - start_year) / total_years if total_years > 0 else 0
        vessels = int(round(start_vessels + (end_vessels - start_vessels) * fraction))
        vessel_growth[year] = vessels

    return vessel_growth


def calculate_annual_demand(
    vessel_growth: Dict[int, int],
    m3_per_voyage: float,
    voyages_per_year: int
) -> Dict[int, float]:
    """
    Calculate annual demand in m3 for each year.

    Args:
        vessel_growth: Vessel count by year
        m3_per_voyage: Volume per voyage in m3
        voyages_per_year: Voyages per vessel per year

    Returns:
        Dictionary mapping year to annual demand in m3
    """
    return {
        year: vessel_count * m3_per_voyage * voyages_per_year
        for year, vessel_count in vessel_growth.items()
    }


def calculate_pump_power(
    flow_rate_m3ph: float,
    delta_pressure_bar: float,
    efficiency: float
) -> float:
    """
    Calculate pump power required.

    Args:
        flow_rate_m3ph: Pump flow rate in m3/h
        delta_pressure_bar: Pressure drop in bar
        efficiency: Pump efficiency (0-1)

    Returns:
        Power in kW
    """
    delta_pressure_pa = delta_pressure_bar * 1e5  # Convert bar to Pa
    flow_rate_m3s = flow_rate_m3ph / 3600.0  # Convert m3/h to m3/s

    # Power = (ΔP × Q) / η
    power_w = (delta_pressure_pa * flow_rate_m3s) / efficiency
    power_kw = power_w / 1000.0

    return power_kw


def calculate_shuttle_capex(
    size_cbm: float,
    ref_capex_usd: float,
    ref_size_cbm: float,
    scaling_exponent: float
) -> float:
    """
    Calculate shuttle CAPEX using scaling law.

    CAPEX = ref_capex × (size / ref_size)^alpha

    Args:
        size_cbm: Shuttle size in m3
        ref_capex_usd: Reference CAPEX for reference size
        ref_size_cbm: Reference size in m3
        scaling_exponent: Scaling exponent (typically 0.75)

    Returns:
        CAPEX in USD
    """
    return ref_capex_usd * (size_cbm / ref_size_cbm) ** scaling_exponent


def calculate_tank_volume_m3(
    tank_capacity_tons: float,
    density_storage: float
) -> float:
    """
    Calculate tank volume from capacity mass.

    Args:
        tank_capacity_tons: Tank capacity in tons
        density_storage: Storage density in ton/m3

    Returns:
        Tank volume in m3
    """
    tank_capacity_kg = tank_capacity_tons * 1000.0
    return tank_capacity_kg / (density_storage * 1000.0)


def validate_config(config: Dict) -> List[str]:
    """
    Validate configuration dictionary.

    Args:
        config: Configuration dictionary

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check required fields
    required_fields = [
        "economy.discount_rate",
        "shipping.kg_per_voyage",
        "operations.travel_time_hours",
        "shuttle.available_sizes_cbm",
        "bunkering.bunker_volume_per_call_m3"
    ]

    def check_nested(d, path):
        keys = path.split(".")
        current = d
        for key in keys[:-1]:
            if key not in current:
                return False
            current = current[key]
        return keys[-1] in current

    for field in required_fields:
        if not check_nested(config, field):
            errors.append(f"Missing required field: {field}")

    # Validate value ranges
    if config.get("economy", {}).get("discount_rate", 0) < 0 or \
       config.get("economy", {}).get("discount_rate", 1) > 1:
        errors.append("Discount rate must be between 0 and 1")

    if config.get("operations", {}).get("travel_time_hours", 0) <= 0:
        errors.append("Travel time must be positive")

    shuttle_sizes = config.get("shuttle", {}).get("available_sizes_cbm", [])
    if not shuttle_sizes or any(s <= 0 for s in shuttle_sizes):
        errors.append("Shuttle sizes must be positive numbers")

    return errors


def round_values(value: float, decimals: int) -> float:
    """
    Round a value to specified decimal places.

    Args:
        value: Value to round
        decimals: Number of decimal places

    Returns:
        Rounded value
    """
    return round(value, decimals)


def format_currency(value: float, decimals: int = 2) -> str:
    """
    Format value as currency string.

    Args:
        value: Value in USD (typically in millions)
        decimals: Number of decimal places

    Returns:
        Formatted currency string
    """
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.{decimals}f}B"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.{decimals}f}M"
    else:
        return f"${value:.{decimals}f}"


# ========== FINANCIAL ANNUALIZATION ==========

def calculate_annuity_factor(
    discount_rate: float,
    years: int
) -> float:
    """
    Calculate annuity factor for discounted cash flows.

    Used to convert Net Present Cost (NPC) into annualized cost.

    Formula:
        Annuity_Factor = [1 - (1 + r)^(-n)] / r

    Where:
        r = discount rate (e.g., 0.07 for 7%)
        n = number of years (e.g., 20)

    Args:
        discount_rate: Annual discount rate (0-1)
        years: Number of years

    Returns:
        Annuity factor for converting NPC to annualized cost

    Example:
        >>> factor = calculate_annuity_factor(0.07, 20)
        >>> factor  # approximately 10.594
    """
    if discount_rate == 0:
        return float(years)

    factor = (1.0 - (1.0 + discount_rate) ** (-years)) / discount_rate
    return factor


def annualize_npc(
    npc_value: float,
    annuity_factor: float
) -> float:
    """
    Convert Net Present Cost (NPC) to annualized annual cost.

    This represents the equivalent constant annual payment that equals
    the total discounted costs over the project period.

    Formula:
        Annualized_Cost = NPC / Annuity_Factor

    Args:
        npc_value: Total Net Present Cost in USD
        annuity_factor: Annuity factor from calculate_annuity_factor()

    Returns:
        Annualized annual cost in USD

    Example:
        >>> npc = 2_650_000_000  # $2,650M
        >>> factor = 10.594
        >>> annualized = annualize_npc(npc, factor)
        >>> annualized  # approximately $250M per year
    """
    return npc_value / annuity_factor
