"""
Analysis utilities for conducting comparative statics.

This module provides helper functions to easily run parameter variations
and comparative statics analyses.
"""

import numpy as np
from .retirement_model import (
    RetirementParameters, 
    calculate_retirement_boundary,
    calculate_consumption_path,
    calculate_investment_strategy
)


def run_parameter_variation(base_params, param_name, param_values, 
                            analysis_function, **kwargs):
    """
    Run analysis for multiple values of a single parameter.
    
    Args:
        base_params: Base RetirementParameters object
        param_name: Name of parameter to vary
        param_values: List/array of values to test
        analysis_function: Function to call for each parameter value
        **kwargs: Additional arguments to pass to analysis_function
        
    Returns:
        List of results from analysis_function for each parameter value
    """
    results = []
    
    for param_val in param_values:
        # Create copy of parameters
        params = base_params.copy()
        
        # Update the specified parameter
        setattr(params, param_name, param_val)
        
        # Update nominal rate if real rate or inflation changed
        if param_name in ['r_real', 'inflation']:
            params.update_nominal_rate()
        
        # Run analysis
        result = analysis_function(params, **kwargs)
        results.append(result)
    
    return results


def comparative_statics_retirement_boundary(base_params, param_name, param_values,
                                            wealth_min=0, wealth_max=100, n_points=50):
    """
    Perform comparative statics on retirement boundary.
    
    Args:
        base_params: Base RetirementParameters object
        param_name: Name of parameter to vary
        param_values: List/array of parameter values
        wealth_min: Minimum wealth level
        wealth_max: Maximum wealth level
        n_points: Number of wealth points to evaluate
        
    Returns:
        tuple: (wealth_grid, retirement_ages_list, params_list)
    """
    wealth_grid = np.linspace(wealth_min, wealth_max, n_points)
    
    def analysis_func(params):
        return calculate_retirement_boundary(params, wealth_grid)
    
    retirement_ages_list = run_parameter_variation(
        base_params, param_name, param_values, analysis_func
    )
    
    # Get parameters for each variation
    params_list = []
    for param_val in param_values:
        params = base_params.copy()
        setattr(params, param_name, param_val)
        if param_name in ['r_real', 'inflation']:
            params.update_nominal_rate()
        params_list.append(params)
    
    return wealth_grid, retirement_ages_list, params_list


def comparative_statics_consumption(base_params, param_name, param_values,
                                   wealth=50, age=30, retirement_age=65):
    """
    Perform comparative statics on consumption path.
    
    Args:
        base_params: Base RetirementParameters object
        param_name: Name of parameter to vary
        param_values: List/array of parameter values
        wealth: Starting wealth level
        age: Starting age
        retirement_age: Planned retirement age
        
    Returns:
        tuple: (ages_list, consumption_list, params_list)
    """
    def analysis_func(params):
        return calculate_consumption_path(params, wealth, age, retirement_age)
    
    results = run_parameter_variation(
        base_params, param_name, param_values, analysis_func
    )
    
    ages_list = [r[0] for r in results]
    consumption_list = [r[1] for r in results]
    
    # Get parameters for each variation
    params_list = []
    for param_val in param_values:
        params = base_params.copy()
        setattr(params, param_name, param_val)
        if param_name in ['r_real', 'inflation']:
            params.update_nominal_rate()
        params_list.append(params)
    
    return ages_list, consumption_list, params_list


def comparative_statics_investment(base_params, param_name, param_values,
                                  wealth=50, age_min=25, age_max=75):
    """
    Perform comparative statics on investment strategy.
    
    Args:
        base_params: Base RetirementParameters object
        param_name: Name of parameter to vary
        param_values: List/array of parameter values
        wealth: Wealth level
        age_min: Minimum age to evaluate
        age_max: Maximum age to evaluate
        
    Returns:
        tuple: (ages, risky_shares_list, params_list)
    """
    ages = np.arange(age_min, age_max + 1)
    risky_shares_list = []
    
    for param_val in param_values:
        params = base_params.copy()
        setattr(params, param_name, param_val)
        if param_name in ['r_real', 'inflation']:
            params.update_nominal_rate()
        
        risky_shares = np.zeros(len(ages))
        for i, age in enumerate(ages):
            strategy = calculate_investment_strategy(params, wealth, age)
            risky_shares[i] = strategy['risky_share']
        
        risky_shares_list.append(risky_shares)
    
    # Get parameters for each variation
    params_list = []
    for param_val in param_values:
        params = base_params.copy()
        setattr(params, param_name, param_val)
        if param_name in ['r_real', 'inflation']:
            params.update_nominal_rate()
        params_list.append(params)
    
    return ages, risky_shares_list, params_list


def run_two_parameter_analysis(base_params, param1_name, param1_values,
                               param2_name, param2_values, metric_function):
    """
    Analyze how an outcome varies with two parameters simultaneously.
    
    Args:
        base_params: Base RetirementParameters object
        param1_name: Name of first parameter to vary
        param1_values: Array of first parameter values
        param2_name: Name of second parameter to vary
        param2_values: Array of second parameter values
        metric_function: Function(params) that returns a scalar metric
        
    Returns:
        2D numpy array of outcomes (shape: len(param1_values) x len(param2_values))
    """
    outcomes = np.zeros((len(param1_values), len(param2_values)))
    
    for i, val1 in enumerate(param1_values):
        for j, val2 in enumerate(param2_values):
            params = base_params.copy()
            setattr(params, param1_name, val1)
            setattr(params, param2_name, val2)
            
            if param1_name in ['r_real', 'inflation'] or param2_name in ['r_real', 'inflation']:
                params.update_nominal_rate()
            
            outcomes[i, j] = metric_function(params)
    
    return outcomes


def calculate_lifetime_utility(params, wealth, age, retirement_age):
    """
    Calculate expected lifetime utility (simplified).
    
    Args:
        params: RetirementParameters object
        wealth: Starting wealth
        age: Starting age
        retirement_age: Retirement age
        
    Returns:
        Total discounted lifetime utility
    """
    ages, consumption = calculate_consumption_path(params, wealth, age, retirement_age)
    
    # CRRA utility: u(c) = c^(1-gamma) / (1-gamma)
    if params.gamma != 1:
        period_utility = (consumption ** (1 - params.gamma)) / (1 - params.gamma)
    else:
        period_utility = np.log(consumption)
    
    # Discount utilities
    discount_factors = params.beta ** np.arange(len(ages))
    discounted_utility = period_utility * discount_factors
    
    return np.sum(discounted_utility)


def calculate_wealth_at_retirement(params, initial_wealth, current_age, retirement_age):
    """
    Calculate expected wealth at retirement.
    
    Args:
        params: RetirementParameters object
        initial_wealth: Current wealth
        current_age: Current age
        retirement_age: Planned retirement age
        
    Returns:
        Expected wealth at retirement
    """
    years_to_retirement = retirement_age - current_age
    
    if years_to_retirement <= 0:
        return initial_wealth
    
    # Assume saving some fraction of wage and earning return on wealth
    savings_rate = 0.1  # 10% savings rate
    annual_savings = params.wage * savings_rate
    
    # Future value calculation
    wealth = initial_wealth
    for _ in range(years_to_retirement):
        wealth = wealth * (1 + params.r_real) + annual_savings
    
    return wealth
