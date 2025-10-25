"""
Example 4: Comprehensive analysis with multiple plots.

This script demonstrates how to create a comprehensive analysis
showing retirement boundary, consumption, and investment strategy
in a single figure with multiple subplots.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src import (
    RetirementParameters,
    comparative_statics_retirement_boundary,
    comparative_statics_consumption,
    comparative_statics_investment,
    plot_comprehensive_analysis
)


def main():
    """Run comprehensive comparative statics analysis."""
    print("=" * 60)
    print("Example 4: Comprehensive Comparative Statics Analysis")
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
    
    # Vary discount factor (beta)
    print("\n\nRunning comprehensive analysis for different discount factors...")
    beta_values = [0.94, 0.96, 0.98]
    
    # Retirement boundary
    print("  Computing retirement boundaries...")
    wealth_grid, retirement_ages_list, _ = comparative_statics_retirement_boundary(
        base_params,
        param_name='beta',
        param_values=beta_values,
        wealth_min=0,
        wealth_max=100,
        n_points=50
    )
    
    # Consumption path
    print("  Computing consumption paths...")
    ages_list, consumption_list, _ = comparative_statics_consumption(
        base_params,
        param_name='beta',
        param_values=beta_values,
        wealth=50,
        age=30,
        retirement_age=65
    )
    
    # Investment strategy
    print("  Computing investment strategies...")
    investment_ages, risky_shares_list, _ = comparative_statics_investment(
        base_params,
        param_name='beta',
        param_values=beta_values,
        wealth=50,
        age_min=25,
        age_max=75
    )
    
    # Create comprehensive plot
    print("\nGenerating comprehensive plot...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'comprehensive_analysis_beta.png')
    
    plot_comprehensive_analysis(
        wealth_grid,
        retirement_ages_list,
        ages_list,
        consumption_list,
        investment_ages,
        risky_shares_list,
        param_name='beta',
        param_values=beta_values,
        output_path=output_path
    )
    
    print("\n" + "=" * 60)
    print("Comprehensive analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
