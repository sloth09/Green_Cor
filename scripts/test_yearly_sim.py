"""Test script to run yearly_simulation with current code."""

from pathlib import Path
from src.config_loader import load_config
from main import run_yearly_simulation

# Load config
config = load_config("case_1")

# Run yearly simulation
output_path = Path("results")
output_path.mkdir(exist_ok=True)

result = run_yearly_simulation(config, 2500, 2000, output_path)

print("\nDone!")

