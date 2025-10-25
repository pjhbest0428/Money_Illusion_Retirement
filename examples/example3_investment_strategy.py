"""
Example 3: Investment strategy comparative statics.

This script demonstrates how optimal portfolio allocation changes
with age for different levels of risk aversion.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src import (
    RetirementParameters,
    comparative_statics_investment,
    plot_investment_strategy
)


def main():
    """Run investment strategy comparative statics."""
    print("=" * 60)
    print("Example 3: Investment Strategy Comparative Statics")
    print("=" * 60)
    
    # Create base parameters
    base_params = RetirementParameters(
        gamma=2.0,
        beta=0.96,
        r_real=0.04,
        inflation=0.02,
        wage=1.0,
        retirement_age=65
    )
    
    print("\nBase Parameters:")
    print(base_params)
    
    # Vary risk aversion parameter
    print("\n\nAnalyzing investment strategy for different risk aversion levels...")
    gamma_values = [1.5, 2.0, 2.5, 3.0]
    
    ages, risky_shares_list, params_list = comparative_statics_investment(
        base_params,
        param_name='gamma',
        param_values=gamma_values,
        wealth=50,
        age_min=25,
        age_max=75
    )
    
    print(f"Analyzed {len(gamma_values)} different gamma values")
    print(f"Age range: {ages.min()} to {ages.max()}")
    print(f"Wealth level: 50")
    
    # Plot results
    print("\nGenerating plot...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'investment_strategy_gamma.png')
    
    plot_investment_strategy(
        ages,
        risky_shares_list,
        param_name='gamma',
        param_values=gamma_values,
        output_path=output_path
    )
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
