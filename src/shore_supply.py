"""
Shore Supply Management for ammonia bunkering operations.

Handles loading and unloading operations at shore facilities,
including pump rate management and time calculations.
"""

from typing import Dict, Optional


class ShoreSupply:
    """
    Manages shore supply (dock/terminal) operations for shuttle loading/unloading.

    Key features:
    - Fixed pump rate (1,500 m³/h standard)
    - Configurable for different shore facilities
    - Supports both loading and unloading operations
    """

    # Standard shore supply pump rate (m³/h)
    STANDARD_PUMP_RATE_M3PH = 1500.0

    def __init__(self, config: Dict):
        """
        Initialize shore supply management.

        Args:
            config: Configuration dictionary containing:
                - shore_supply.enabled: bool
                - shore_supply.pump_rate_m3ph: float (optional, defaults to 1500)
                - shore_supply.loading_time_fixed_hours: float (optional additional fixed time)
        """
        self.config = config

        # Extract shore supply config
        shore_config = config.get("shore_supply", {})
        self.enabled = shore_config.get("enabled", True)
        self.pump_rate_m3ph = shore_config.get(
            "pump_rate_m3ph",
            self.STANDARD_PUMP_RATE_M3PH
        )
        self.fixed_time_hours = shore_config.get("loading_time_fixed_hours", 0.0)

    def is_enabled(self) -> bool:
        """Check if shore supply is enabled in configuration."""
        return self.enabled

    def get_pump_rate(self) -> float:
        """Get current shore supply pump rate in m³/h."""
        return self.pump_rate_m3ph

    def load_shuttle(self, shuttle_size_m3: float) -> float:
        """
        Calculate time to load shuttle from shore facility.

        Parameters:
        -----------
        shuttle_size_m3 : float
            Shuttle capacity in m³

        Returns:
        --------
        float : Time required to load shuttle in hours

        Formula:
        --------
        loading_time = (shuttle_size / pump_rate) + fixed_time
        """
        if not self.enabled:
            return 0.0

        pumping_time = shuttle_size_m3 / self.pump_rate_m3ph
        return pumping_time + self.fixed_time_hours

    def unload_shuttle(self, shuttle_size_m3: float) -> float:
        """
        Calculate time to unload shuttle at shore facility.

        In typical ammonia bunkering operations, unloading may be minimal
        or zero if the shuttle is not returned to the source port for offloading.

        Parameters:
        -----------
        shuttle_size_m3 : float
            Shuttle capacity in m³

        Returns:
        --------
        float : Time required to unload shuttle in hours
        """
        if not self.enabled:
            return 0.0

        # For Case 1: Shuttles typically don't return to loading point for unloading
        # For Case 2: Shuttles return to source but may not offload (keep residual)
        # Default: Zero unloading time (no return offloading)
        return 0.0

    def calculate_load_unload_time(
        self,
        shuttle_size_m3: float,
        include_unload: bool = False
    ) -> float:
        """
        Calculate combined load and unload time.

        Parameters:
        -----------
        shuttle_size_m3 : float
            Shuttle capacity in m³
        include_unload : bool
            Whether to include unload time (default False)

        Returns:
        --------
        float : Combined time in hours
        """
        load_time = self.load_shuttle(shuttle_size_m3)
        unload_time = self.unload_shuttle(shuttle_size_m3) if include_unload else 0.0
        return load_time + unload_time

    def calculate_pump_capacity(self) -> float:
        """Get shore supply pump capacity in m³/h."""
        return self.pump_rate_m3ph

    def get_annual_loading_capacity(self) -> float:
        """
        Calculate annual loading capacity assuming 8,000 hours availability.

        Returns:
        --------
        float : Annual capacity in m³
        """
        annual_hours = 8000.0
        return annual_hours * self.pump_rate_m3ph

    def validate_configuration(self) -> bool:
        """
        Validate shore supply configuration.

        Returns:
        --------
        bool : True if configuration is valid

        Raises:
        -------
        ValueError : If configuration is invalid
        """
        if not isinstance(self.pump_rate_m3ph, (int, float)) or self.pump_rate_m3ph <= 0:
            raise ValueError(
                f"Invalid shore supply pump rate: {self.pump_rate_m3ph} m³/h. "
                "Must be positive number."
            )

        if self.fixed_time_hours < 0:
            raise ValueError(
                f"Invalid fixed loading time: {self.fixed_time_hours} hours. "
                "Must be non-negative."
            )

        return True

    def __repr__(self) -> str:
        """String representation of shore supply configuration."""
        status = "Enabled" if self.enabled else "Disabled"
        return (
            f"ShoreSupply({status}, "
            f"pump_rate={self.pump_rate_m3ph} m³/h, "
            f"fixed_time={self.fixed_time_hours}h)"
        )
