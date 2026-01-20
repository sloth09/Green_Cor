"""
Green Corridor Bunkering Optimization Model
MILP optimization for ammonia bunkering infrastructure planning at Busan Port
"""

__version__ = "2.2"
__author__ = "Green Corridor Research Team"

from .config_loader import ConfigLoader, load_config, list_available_cases
from .optimizer import BunkeringOptimizer
from .cost_calculator import CostCalculator
from .utils import (
    interpolate_mcr,
    calculate_m3_per_voyage,
    calculate_vessel_growth,
    calculate_annual_demand,
)

# Runner functions - reusable execution logic
from .runner import (
    print_cycle_time_breakdown,
    run_single_scenario,
    run_annual_simulation,
    run_yearly_simulation,
    run_single_case,
)

# Verification utilities
from .verification import (
    CalculationVerifier,
    VerificationResult,
    verify_case,
    verify_optimization_result,
)

# Stochastic analysis - vessel distribution
from .vessel_distribution import (
    VesselType,
    DistributionScenario,
    MonteCarloScenario,
    VesselDistribution,
    load_stochastic_config,
    create_vessel_distribution,
)

# Stochastic optimization
from .stochastic_optimizer import (
    StochasticOptimizer,
    StochasticResult,
    run_stochastic_optimization,
)

# Sensitivity analysis
from .sensitivity_analyzer import (
    SensitivityAnalyzer,
    ParameterSensitivityResult,
    TornadoResult,
    TwoWaySensitivityResult,
    run_sensitivity_analysis,
)

# Break-even analysis
from .breakeven_analyzer import (
    BreakevenAnalyzer,
    BreakevenResult,
    CaseComparisonResult,
    run_breakeven_analysis,
)

# Paper figure generation
from .paper_figures import (
    PaperFigureGenerator,
    generate_paper_figures,
)

__all__ = [
    # Config
    "ConfigLoader",
    "load_config",
    "list_available_cases",
    # Optimization
    "BunkeringOptimizer",
    "CostCalculator",
    # Utils
    "interpolate_mcr",
    "calculate_m3_per_voyage",
    "calculate_vessel_growth",
    "calculate_annual_demand",
    # Runner functions
    "print_cycle_time_breakdown",
    "run_single_scenario",
    "run_annual_simulation",
    "run_yearly_simulation",
    "run_single_case",
    # Verification
    "CalculationVerifier",
    "VerificationResult",
    "verify_case",
    "verify_optimization_result",
    # Stochastic - Vessel Distribution
    "VesselType",
    "DistributionScenario",
    "MonteCarloScenario",
    "VesselDistribution",
    "load_stochastic_config",
    "create_vessel_distribution",
    # Stochastic - Optimization
    "StochasticOptimizer",
    "StochasticResult",
    "run_stochastic_optimization",
    # Sensitivity Analysis
    "SensitivityAnalyzer",
    "ParameterSensitivityResult",
    "TornadoResult",
    "TwoWaySensitivityResult",
    "run_sensitivity_analysis",
    # Break-even Analysis
    "BreakevenAnalyzer",
    "BreakevenResult",
    "CaseComparisonResult",
    "run_breakeven_analysis",
    # Paper Figures
    "PaperFigureGenerator",
    "generate_paper_figures",
]
