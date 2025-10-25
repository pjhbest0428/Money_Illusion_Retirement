"""
Example 1: Basic comparative statics for retirement boundary.

This script demonstrates how to analyze the retirement boundary
as wealth varies, for different levels of risk aversion (gamma).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src import (
    RetirementParameters,
    comparative_statics_retirement_boundary,
    plot_retirement_boundary
)


def main():
    """Run retirement boundary comparative statics."""
    print("=" * 60)
    print("Example 1: Retirement Boundary Comparative Statics")
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
    print("\n\nAnalyzing retirement boundary for different risk aversion levels...")
    gamma_values = [1.5, 2.0, 2.5, 3.0]
    
    wealth_grid, retirement_ages_list, params_list = comparative_statics_retirement_boundary(
        base_params,
        param_name='gamma',
        param_values=gamma_values,
        wealth_min=0,
        wealth_max=100,
        n_points=50
    )
    
    print(f"Analyzed {len(gamma_values)} different gamma values")
    print(f"Wealth range: {wealth_grid.min():.1f} to {wealth_grid.max():.1f}")
    
    # Plot results
    print("\nGenerating plot...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 
                               'retirement_boundary_gamma.png')
    
    plot_retirement_boundary(
        wealth_grid,
        retirement_ages_list,
        params_list,
        param_name='gamma',
        param_values=gamma_values,
        output_path=output_path
    )
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
