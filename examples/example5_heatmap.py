"""
Example 5: Two-parameter heatmap analysis.

This script demonstrates how to analyze how outcomes vary with
two parameters simultaneously, visualized as a heatmap.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src import (
    RetirementParameters,
    run_two_parameter_analysis,
    calculate_retirement_boundary,
    create_heatmap
)


def main():
    """Run two-parameter heatmap analysis."""
    print("=" * 60)
    print("Example 5: Two-Parameter Heatmap Analysis")
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
    
    # Define parameter ranges
    print("\n\nAnalyzing how average retirement age varies with gamma and inflation...")
    gamma_values = np.linspace(1.5, 3.5, 10)
    inflation_values = np.linspace(0.0, 0.06, 10)
    
    # Define metric function
    def average_retirement_age(params):
        """Calculate average retirement age across wealth levels."""
        wealth_grid = np.linspace(0, 100, 30)
        retirement_ages = calculate_retirement_boundary(params, wealth_grid)
        return np.mean(retirement_ages)
    
    # Run two-parameter analysis
    print(f"Computing {len(gamma_values)} x {len(inflation_values)} = "
          f"{len(gamma_values) * len(inflation_values)} scenarios...")
    
    outcomes = run_two_parameter_analysis(
        base_params,
        param1_name='gamma',
        param1_values=gamma_values,
        param2_name='inflation',
        param2_values=inflation_values,
        metric_function=average_retirement_age
    )
    
    print(f"Analysis complete. Outcome range: {outcomes.min():.2f} to {outcomes.max():.2f}")
    
    # Create heatmap
    print("\nGenerating heatmap...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'heatmap_gamma_inflation.png')
    
    create_heatmap(
        gamma_values,
        inflation_values,
        outcomes,
        param1_name='Risk Aversion (gamma)',
        param2_name='Inflation Rate',
        outcome_name='Average Retirement Age',
        output_path=output_path
    )
    
    print("\n" + "=" * 60)
    print("Heatmap analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
