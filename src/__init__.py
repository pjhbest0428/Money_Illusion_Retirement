"""
Money Illusion Retirement Analysis Package

This package provides tools for numerical analysis of retirement decisions
with money illusion considerations.
"""

from .retirement_model import (
    RetirementParameters,
    calculate_retirement_boundary,
    calculate_consumption_path,
    calculate_investment_strategy
)

from .analysis import (
    run_parameter_variation,
    comparative_statics_retirement_boundary,
    comparative_statics_consumption,
    comparative_statics_investment,
    run_two_parameter_analysis,
    calculate_lifetime_utility,
    calculate_wealth_at_retirement
)

from .plotting import (
    plot_retirement_boundary,
    plot_consumption_paths,
    plot_investment_strategy,
    plot_parameter_sensitivity,
    plot_comprehensive_analysis,
    create_heatmap
)

__all__ = [
    # Core model
    'RetirementParameters',
    'calculate_retirement_boundary',
    'calculate_consumption_path',
    'calculate_investment_strategy',
    
    # Analysis utilities
    'run_parameter_variation',
    'comparative_statics_retirement_boundary',
    'comparative_statics_consumption',
    'comparative_statics_investment',
    'run_two_parameter_analysis',
    'calculate_lifetime_utility',
    'calculate_wealth_at_retirement',
    
    # Plotting
    'plot_retirement_boundary',
    'plot_consumption_paths',
    'plot_investment_strategy',
    'plot_parameter_sensitivity',
    'plot_comprehensive_analysis',
    'create_heatmap',
]
