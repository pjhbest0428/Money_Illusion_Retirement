"""
Plotting utilities for comparative statics analysis.

This module provides functions to visualize how retirement decisions,
consumption, and investment strategies change with different parameters.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os


def plot_retirement_boundary(wealth_grid, retirement_ages, params_list, 
                             param_name, param_values, output_path=None):
    """
    Plot retirement boundary for different parameter values.
    
    Args:
        wealth_grid: Array of wealth levels
        retirement_ages: List of retirement age arrays (one per parameter value)
        params_list: List of RetirementParameters objects
        param_name: Name of the varying parameter
        param_values: List of parameter values
        output_path: Path to save figure (optional)
    """
    plt.figure(figsize=(10, 6))
    
    for i, (ages, param_val) in enumerate(zip(retirement_ages, param_values)):
        plt.plot(wealth_grid, ages, label=f'{param_name}={param_val:.3f}', linewidth=2)
    
    plt.xlabel('Wealth', fontsize=12)
    plt.ylabel('Optimal Retirement Age', fontsize=12)
    plt.title(f'Retirement Boundary: Comparative Statics for {param_name}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {output_path}")
    
    plt.show()


def plot_consumption_paths(ages_list, consumption_list, param_name, 
                           param_values, output_path=None):
    """
    Plot consumption paths over lifetime for different parameter values.
    
    Args:
        ages_list: List of age arrays
        consumption_list: List of consumption arrays
        param_name: Name of the varying parameter
        param_values: List of parameter values
        output_path: Path to save figure (optional)
    """
    plt.figure(figsize=(10, 6))
    
    for i, (ages, consumption, param_val) in enumerate(zip(ages_list, consumption_list, param_values)):
        plt.plot(ages, consumption, label=f'{param_name}={param_val:.3f}', linewidth=2)
    
    plt.xlabel('Age', fontsize=12)
    plt.ylabel('Consumption', fontsize=12)
    plt.title(f'Optimal Consumption Path: Comparative Statics for {param_name}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {output_path}")
    
    plt.show()


def plot_investment_strategy(ages, risky_shares_list, param_name, 
                             param_values, output_path=None):
    """
    Plot investment strategy (risky asset share) over lifetime.
    
    Args:
        ages: Array of ages
        risky_shares_list: List of risky share arrays
        param_name: Name of the varying parameter
        param_values: List of parameter values
        output_path: Path to save figure (optional)
    """
    plt.figure(figsize=(10, 6))
    
    for risky_shares, param_val in zip(risky_shares_list, param_values):
        plt.plot(ages, risky_shares * 100, label=f'{param_name}={param_val:.3f}', linewidth=2)
    
    plt.xlabel('Age', fontsize=12)
    plt.ylabel('Risky Asset Share (%)', fontsize=12)
    plt.title(f'Optimal Investment Strategy: Comparative Statics for {param_name}', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 100)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {output_path}")
    
    plt.show()


def plot_parameter_sensitivity(param_values, outcomes, param_name, 
                               outcome_name, output_path=None):
    """
    Plot how a single outcome varies with a parameter.
    
    Args:
        param_values: Array of parameter values
        outcomes: Array of outcome values
        param_name: Name of the parameter
        outcome_name: Name of the outcome variable
        output_path: Path to save figure (optional)
    """
    plt.figure(figsize=(10, 6))
    
    plt.plot(param_values, outcomes, 'o-', linewidth=2, markersize=8)
    
    plt.xlabel(param_name, fontsize=12)
    plt.ylabel(outcome_name, fontsize=12)
    plt.title(f'Sensitivity Analysis: {outcome_name} vs {param_name}', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {output_path}")
    
    plt.show()


def plot_comprehensive_analysis(wealth_grid, retirement_ages_list, 
                                ages_list, consumption_list,
                                investment_ages, risky_shares_list,
                                param_name, param_values, output_path=None):
    """
    Create a comprehensive plot with multiple subplots showing all analyses.
    
    Args:
        wealth_grid: Array of wealth levels for retirement boundary
        retirement_ages_list: List of retirement age arrays
        ages_list: List of age arrays for consumption
        consumption_list: List of consumption arrays
        investment_ages: Array of ages for investment strategy
        risky_shares_list: List of risky share arrays
        param_name: Name of the varying parameter
        param_values: List of parameter values
        output_path: Path to save figure (optional)
    """
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Plot 1: Retirement Boundary
    ax1 = fig.add_subplot(gs[0, 0])
    for i, (ages, param_val) in enumerate(zip(retirement_ages_list, param_values)):
        ax1.plot(wealth_grid, ages, label=f'{param_name}={param_val:.3f}', linewidth=2)
    ax1.set_xlabel('Wealth', fontsize=10)
    ax1.set_ylabel('Optimal Retirement Age', fontsize=10)
    ax1.set_title('Retirement Boundary', fontsize=12)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Consumption Path
    ax2 = fig.add_subplot(gs[0, 1])
    for i, (ages, consumption, param_val) in enumerate(zip(ages_list, consumption_list, param_values)):
        ax2.plot(ages, consumption, label=f'{param_name}={param_val:.3f}', linewidth=2)
    ax2.set_xlabel('Age', fontsize=10)
    ax2.set_ylabel('Consumption', fontsize=10)
    ax2.set_title('Optimal Consumption Path', fontsize=12)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Investment Strategy
    ax3 = fig.add_subplot(gs[1, 0])
    for risky_shares, param_val in zip(risky_shares_list, param_values):
        ax3.plot(investment_ages, risky_shares * 100, 
                label=f'{param_name}={param_val:.3f}', linewidth=2)
    ax3.set_xlabel('Age', fontsize=10)
    ax3.set_ylabel('Risky Asset Share (%)', fontsize=10)
    ax3.set_title('Optimal Investment Strategy', fontsize=12)
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 100)
    
    # Plot 4: Summary statistics or additional analysis
    ax4 = fig.add_subplot(gs[1, 1])
    # Calculate average retirement age for each parameter value
    avg_retirement_ages = [np.mean(ages) for ages in retirement_ages_list]
    ax4.plot(param_values, avg_retirement_ages, 'o-', linewidth=2, markersize=8)
    ax4.set_xlabel(param_name, fontsize=10)
    ax4.set_ylabel('Average Retirement Age', fontsize=10)
    ax4.set_title('Parameter Sensitivity', fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    fig.suptitle(f'Comprehensive Retirement Analysis: {param_name} Variations', 
                 fontsize=14, fontweight='bold')
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved comprehensive plot to {output_path}")
    
    plt.show()


def create_heatmap(param1_values, param2_values, outcomes, 
                   param1_name, param2_name, outcome_name, output_path=None):
    """
    Create a heatmap showing how an outcome varies with two parameters.
    
    Args:
        param1_values: Array of first parameter values
        param2_values: Array of second parameter values
        outcomes: 2D array of outcomes (shape: len(param1_values) x len(param2_values))
        param1_name: Name of first parameter
        param2_name: Name of second parameter
        outcome_name: Name of outcome variable
        output_path: Path to save figure (optional)
    """
    plt.figure(figsize=(10, 8))
    
    im = plt.imshow(outcomes, aspect='auto', origin='lower', cmap='viridis')
    
    # Set ticks
    plt.xticks(range(len(param2_values)), [f'{v:.2f}' for v in param2_values])
    plt.yticks(range(len(param1_values)), [f'{v:.2f}' for v in param1_values])
    
    plt.xlabel(param2_name, fontsize=12)
    plt.ylabel(param1_name, fontsize=12)
    plt.title(f'Heatmap: {outcome_name}', fontsize=14)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label(outcome_name, fontsize=12)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved heatmap to {output_path}")
    
    plt.show()
