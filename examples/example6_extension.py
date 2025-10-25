"""
Example 6: Custom extension demonstration.

This example shows how easy it is to extend the framework with:
1. Custom analysis metrics
2. Custom plotting
3. New parameter variations

This demonstrates the extensibility of the framework as requested.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt
from src import (
    RetirementParameters,
    calculate_retirement_boundary,
    calculate_consumption_path,
    run_parameter_variation,
)


# Example 1: Adding a custom metric
def calculate_consumption_volatility(params, wealth=50, age=30, retirement_age=65):
    """
    Custom metric: Calculate consumption volatility over lifetime.
    This is a new analysis that wasn't in the original framework.
    """
    ages, consumption = calculate_consumption_path(params, wealth, age, retirement_age)
    # Calculate coefficient of variation
    volatility = np.std(consumption) / np.mean(consumption)
    return volatility


# Example 2: Adding a custom comparative statics analysis
def analyze_consumption_volatility_by_inflation():
    """Analyze how consumption volatility varies with inflation."""
    print("\n" + "=" * 60)
    print("Custom Analysis 1: Consumption Volatility vs Inflation")
    print("=" * 60)
    
    base_params = RetirementParameters(gamma=2.0, beta=0.96, r_real=0.04)
    inflation_values = np.linspace(0.0, 0.08, 20)
    
    # Use the framework's run_parameter_variation with our custom metric
    volatilities = run_parameter_variation(
        base_params,
        param_name='inflation',
        param_values=inflation_values,
        analysis_function=calculate_consumption_volatility,
        wealth=50,
        age=30,
        retirement_age=65
    )
    
    # Custom plotting
    plt.figure(figsize=(10, 6))
    plt.plot(inflation_values * 100, volatilities, 'o-', linewidth=2, markersize=6)
    plt.xlabel('Inflation Rate (%)', fontsize=12)
    plt.ylabel('Consumption Volatility (CV)', fontsize=12)
    plt.title('How Consumption Volatility Changes with Inflation', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'custom_volatility_analysis.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    plt.close()


# Example 3: Adding a custom multi-metric analysis
def analyze_tradeoffs():
    """Analyze tradeoffs between different metrics."""
    print("\n" + "=" * 60)
    print("Custom Analysis 2: Risk-Return Tradeoff Analysis")
    print("=" * 60)
    
    base_params = RetirementParameters()
    gamma_values = np.linspace(1.0, 4.0, 15)
    
    # Calculate multiple metrics for each gamma value
    avg_retirement_ages = []
    consumption_volatilities = []
    
    for gamma in gamma_values:
        params = base_params.copy()
        params.gamma = gamma
        
        # Metric 1: Average retirement age
        wealth_grid = np.linspace(0, 100, 50)
        retirement_ages = calculate_retirement_boundary(params, wealth_grid)
        avg_retirement_ages.append(np.mean(retirement_ages))
        
        # Metric 2: Consumption volatility
        volatility = calculate_consumption_volatility(params)
        consumption_volatilities.append(volatility)
    
    # Create a custom dual-axis plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color1 = 'tab:blue'
    ax1.set_xlabel('Risk Aversion (gamma)', fontsize=12)
    ax1.set_ylabel('Average Retirement Age', fontsize=12, color=color1)
    ax1.plot(gamma_values, avg_retirement_ages, 'o-', color=color1, 
             linewidth=2, markersize=6, label='Retirement Age')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    color2 = 'tab:orange'
    ax2.set_ylabel('Consumption Volatility', fontsize=12, color=color2)
    ax2.plot(gamma_values, consumption_volatilities, 's-', color=color2,
             linewidth=2, markersize=6, label='Volatility')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    plt.title('Risk Aversion Tradeoffs: Retirement Age vs Consumption Volatility',
              fontsize=14)
    fig.tight_layout()
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'custom_tradeoff_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    plt.close()


# Example 4: Custom parameter combination analysis
def analyze_optimal_parameters():
    """Find parameter combinations that achieve specific goals."""
    print("\n" + "=" * 60)
    print("Custom Analysis 3: Parameter Optimization")
    print("=" * 60)
    
    # Goal: Find combination of beta and r_real that achieves 
    # smooth consumption (low volatility) with reasonable retirement age
    
    beta_values = np.linspace(0.92, 0.98, 10)
    r_real_values = np.linspace(0.02, 0.06, 10)
    
    results = np.zeros((len(beta_values), len(r_real_values)))
    
    base_params = RetirementParameters()
    
    for i, beta in enumerate(beta_values):
        for j, r_real in enumerate(r_real_values):
            params = base_params.copy()
            params.beta = beta
            params.r_real = r_real
            params.update_nominal_rate()
            
            # Combined metric: weighted average of normalized volatility and retirement age
            volatility = calculate_consumption_volatility(params)
            wealth_grid = np.linspace(0, 100, 30)
            retirement_ages = calculate_retirement_boundary(params, wealth_grid)
            avg_age = np.mean(retirement_ages)
            
            # Lower is better for both (earlier retirement, lower volatility)
            # Normalize and combine
            results[i, j] = volatility * 100 + (avg_age - 50) / 20
    
    # Plot heatmap
    plt.figure(figsize=(10, 8))
    im = plt.imshow(results, aspect='auto', origin='lower', cmap='RdYlGn_r')
    
    plt.xticks(range(len(r_real_values)), [f'{v:.3f}' for v in r_real_values])
    plt.yticks(range(len(beta_values)), [f'{v:.3f}' for v in beta_values])
    
    plt.xlabel('Real Interest Rate', fontsize=12)
    plt.ylabel('Discount Factor (beta)', fontsize=12)
    plt.title('Parameter Optimization: Combined Quality Score\n(Lower is Better)',
              fontsize=14)
    
    cbar = plt.colorbar(im)
    cbar.set_label('Combined Score', fontsize=12)
    
    # Mark the best combination
    best_idx = np.unravel_index(np.argmin(results), results.shape)
    plt.plot(best_idx[1], best_idx[0], 'w*', markersize=20, 
             markeredgecolor='black', markeredgewidth=1.5)
    plt.text(best_idx[1], best_idx[0] + 0.5, 'Optimal', 
             ha='center', va='bottom', fontsize=10, color='white',
             bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'outputs',
                               'custom_optimization_analysis.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    print(f"Optimal parameters: beta={beta_values[best_idx[0]]:.3f}, "
          f"r_real={r_real_values[best_idx[1]]:.3f}")
    plt.close()


def main():
    """Run all custom analysis examples."""
    print("=" * 60)
    print("Example 6: Framework Extension Demonstration")
    print("=" * 60)
    print("\nThis example demonstrates how easily you can extend")
    print("the framework with custom metrics and analyses.")
    
    # Run custom analyses
    analyze_consumption_volatility_by_inflation()
    analyze_tradeoffs()
    analyze_optimal_parameters()
    
    print("\n" + "=" * 60)
    print("All custom analyses complete!")
    print("=" * 60)
    print("\nKey takeaways:")
    print("1. New metrics can be added by defining simple functions")
    print("2. Existing utilities (like run_parameter_variation) work with new metrics")
    print("3. Custom plots can combine multiple metrics easily")
    print("4. Complex multi-parameter analyses are straightforward to implement")
    print("\nThe framework is designed for easy extension!")


if __name__ == "__main__":
    main()
