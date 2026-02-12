"""
Configuration loader for bunkering optimization model.
Loads and merges base and case-specific YAML configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any
import sys
from .utils import validate_config


# Alias mapping: canonical case_id -> config filename stem
# Allows load_config("case_2") to find "case_2_ulsan.yaml"
CASE_ALIASES = {
    "case_2": "case_2_ulsan",
    "case_3": "case_3_yeosu",
}

# Reverse mapping for get_available_cases()
_REVERSE_ALIASES = {v: k for k, v in CASE_ALIASES.items()}


class ConfigLoader:
    """Load and manage configuration from YAML files."""

    def __init__(self, config_dir: str = "config"):
        """
        Initialize the config loader.

        Args:
            config_dir: Directory containing YAML config files
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {config_dir}")

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load a single YAML file.

        Args:
            filename: Name of YAML file (without directory)

        Returns:
            Dictionary from YAML file

        Raises:
            FileNotFoundError: If file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        filepath = self.config_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if data is not None else {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing {filename}: {e}")

    def merge_dicts(self, base: Dict, override: Dict) -> Dict:
        """
        Recursively merge override dict into base dict.

        Args:
            base: Base dictionary
            override: Dictionary to merge in

        Returns:
            Merged dictionary
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_dicts(result[key], value)
            else:
                result[key] = value

        return result

    def load_config(self, case_name: str = "case_1") -> Dict[str, Any]:
        """
        Load configuration for a specific case.

        Merges base.yaml with case-specific YAML file.

        Args:
            case_name: Case identifier (e.g., "case_1", "case_2", "case_3")

        Returns:
            Complete configuration dictionary

        Raises:
            FileNotFoundError: If required files not found
            ValueError: If configuration is invalid
        """
        # Load base configuration
        base_config = self.load_yaml("base.yaml")

        # Load case-specific configuration (resolve alias if needed)
        resolved_name = CASE_ALIASES.get(case_name, case_name)
        case_filename = f"{resolved_name}.yaml"
        case_config = self.load_yaml(case_filename)

        # Merge configurations (case overrides base)
        config = self.merge_dicts(base_config, case_config)

        # Validate
        errors = validate_config(config)
        if errors:
            error_msg = "\n".join(errors)
            raise ValueError(f"Configuration validation failed:\n{error_msg}")

        # Post-processing
        self._post_process_config(config)

        return config

    def _post_process_config(self, config: Dict[str, Any]) -> None:
        """
        Post-process configuration to calculate derived values.

        Args:
            config: Configuration dictionary (modified in-place)
        """
        # Ensure all required nested dicts exist
        for key in ["economy", "shipping", "ammonia", "propulsion",
                   "operations", "tank_storage", "shuttle", "bunkering"]:
            if key not in config:
                config[key] = {}

        # Convert string booleans if needed
        if isinstance(config.get("output", {}).get("make_plots"), str):
            config["output"]["make_plots"] = config["output"]["make_plots"].lower() == "true"

        # Backward compatibility: Convert old field names to new names
        # This allows old config files to still work without changes
        execution_config = config.get("execution", {})

        # Old name 'case' -> new name 'single_case'
        if "case" in execution_config and "single_case" not in execution_config:
            execution_config["single_case"] = execution_config["case"]

        # Old name 'cases_to_run' -> new name 'multi_cases'
        if "cases_to_run" in execution_config and "multi_cases" not in execution_config:
            execution_config["multi_cases"] = execution_config["cases_to_run"]

    def get_available_cases(self) -> list:
        """
        Get list of available cases.

        Returns:
            List of case names (without .yaml extension)
        """
        case_files = [f.stem for f in self.config_dir.glob("case_*.yaml")]
        return sorted([_REVERSE_ALIASES.get(f, f) for f in case_files])

    def load_config_from_file(self, filepath: str) -> Dict[str, Any]:
        """
        Load configuration directly from a file path.

        Args:
            filepath: Full path to YAML file

        Returns:
            Configuration dictionary
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing {filepath}: {e}")


def load_config(case_name: str = "case_1", config_dir: str = "config") -> Dict[str, Any]:
    """
    Convenience function to load configuration.

    Args:
        case_name: Case identifier (e.g., "case_1")
        config_dir: Configuration directory

    Returns:
        Configuration dictionary
    """
    loader = ConfigLoader(config_dir)
    return loader.load_config(case_name)


def list_available_cases(config_dir: str = "config") -> list:
    """
    List all available cases.

    Args:
        config_dir: Configuration directory

    Returns:
        List of case names
    """
    loader = ConfigLoader(config_dir)
    return loader.get_available_cases()
