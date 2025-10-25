"""
Example 2: Consumption path comparative statics.

This script demonstrates how to analyze optimal consumption paths
for different inflation rates, showing money illusion effects.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src import (
    RetirementParameters,
    comparative_statics_consumption,
    plot_consumption_paths
)


def main():
    """Run consumption path comparative statics."""
    print("=" * 60)
    print("Example 2: Consumption Path Comparative Statics")
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
    
    # Vary inflation rate to show money illusion effects
    print("\n\nAnalyzing consumption paths for different inflation rates...")
    inflation_values = [0.0, 0.02, 0.04, 0.06]
    
    ages_list, consumption_list, params_list = comparative_statics_consumption(
        base_params,
        param_name='inflation',
        param_values=inflation_values,
        wealth=50,
        age=30,
        retirement_age=65
    )
    
    print(f"Analyzed {len(inflation_values)} different inflation rates")
    print(f"Starting age: 30, Retirement age: 65, Initial wealth: 50")
    
    # Plot results
    print("\nGenerating plot...")
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'consumption_path_inflation.png')
    
    plot_consumption_paths(
        ages_list,
        consumption_list,
        param_name='inflation',
        param_values=inflation_values,
        output_path=output_path
    )
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
