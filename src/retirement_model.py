"""
Core retirement model parameters and calculations.

This module contains the fundamental parameters and calculations for 
retirement analysis with money illusion considerations.
"""

import numpy as np


class RetirementParameters:
    """
    Container for retirement model parameters.
    
    Attributes:
        gamma: Coefficient of relative risk aversion
        beta: Time discount factor
        delta: Depreciation rate
        r_real: Real interest rate
        r_nominal: Nominal interest rate
        inflation: Inflation rate
        wage: Wage rate
        retirement_age: Standard retirement age
        max_age: Maximum lifespan
    """
    
    def __init__(self, 
                 gamma=2.0,
                 beta=0.96,
                 delta=0.05,
                 r_real=0.04,
                 inflation=0.02,
                 wage=1.0,
                 retirement_age=65,
                 max_age=100):
        """
        Initialize retirement parameters.
        
        Args:
            gamma: Risk aversion coefficient (default: 2.0)
            beta: Time discount factor (default: 0.96)
            delta: Depreciation rate (default: 0.05)
            r_real: Real interest rate (default: 0.04)
            inflation: Inflation rate (default: 0.02)
            wage: Wage rate (default: 1.0)
            retirement_age: Standard retirement age (default: 65)
            max_age: Maximum lifespan (default: 100)
        """
        self.gamma = gamma
        self.beta = beta
        self.delta = delta
        self.r_real = r_real
        self.inflation = inflation
        self.r_nominal = (1 + r_real) * (1 + inflation) - 1
        self.wage = wage
        self.retirement_age = retirement_age
        self.max_age = max_age
    
    def update_nominal_rate(self):
        """Update nominal interest rate based on Fisher equation."""
        self.r_nominal = (1 + self.r_real) * (1 + self.inflation) - 1
    
    def copy(self):
        """Create a copy of the parameters."""
        return RetirementParameters(
            gamma=self.gamma,
            beta=self.beta,
            delta=self.delta,
            r_real=self.r_real,
            inflation=self.inflation,
            wage=self.wage,
            retirement_age=self.retirement_age,
            max_age=self.max_age
        )
    
    def __repr__(self):
        """String representation of parameters."""
        return (f"RetirementParameters(gamma={self.gamma}, beta={self.beta}, "
                f"delta={self.delta}, r_real={self.r_real}, "
                f"inflation={self.inflation}, wage={self.wage}, "
                f"retirement_age={self.retirement_age}, max_age={self.max_age})")


def calculate_retirement_boundary(params, wealth_grid):
    """
    Calculate the retirement boundary as a function of wealth.
    
    The retirement boundary determines the optimal age to retire given
    current wealth level, considering money illusion effects.
    
    Args:
        params: RetirementParameters object
        wealth_grid: Array of wealth levels to evaluate
        
    Returns:
        Array of optimal retirement ages corresponding to wealth levels
    """
    # Simple retirement boundary model
    # Higher wealth allows earlier retirement
    min_wealth_for_retirement = params.wage * (params.max_age - params.retirement_age)
    
    retirement_ages = np.zeros_like(wealth_grid)
    for i, w in enumerate(wealth_grid):
        if w >= min_wealth_for_retirement:
            # Can retire earlier with more wealth
            years_earlier = (w - min_wealth_for_retirement) / (params.wage * 2)
            retirement_ages[i] = max(params.retirement_age - years_earlier, 25)
        else:
            # Need to work longer with less wealth
            years_later = (min_wealth_for_retirement - w) / params.wage
            retirement_ages[i] = min(params.retirement_age + years_later, params.max_age - 10)
    
    return retirement_ages


def calculate_consumption_path(params, wealth, age, retirement_age):
    """
    Calculate optimal consumption path from current age to max_age.
    
    Uses Euler equation with CRRA utility to determine consumption.
    
    Args:
        params: RetirementParameters object
        wealth: Current wealth level
        age: Current age
        retirement_age: Planned retirement age
        
    Returns:
        tuple: (ages, consumption_path)
            ages: Array of ages from current to max_age
            consumption_path: Array of optimal consumption at each age
    """
    n_periods = params.max_age - age
    ages = np.arange(age, params.max_age)
    consumption = np.zeros(n_periods)
    
    # Calculate consumption growth rate from Euler equation
    # c_{t+1}/c_t = (beta * (1+r))^(1/gamma)
    if age < retirement_age:
        # Use nominal rate if considering money illusion
        growth_rate = (params.beta * (1 + params.r_nominal)) ** (1 / params.gamma)
    else:
        # Use real rate after retirement
        growth_rate = (params.beta * (1 + params.r_real)) ** (1 / params.gamma)
    
    # Initial consumption determined by budget constraint
    # Simplified: distribute wealth over remaining lifetime
    total_resources = wealth
    if age < retirement_age:
        # Add expected wage income
        working_years = retirement_age - age
        total_resources += params.wage * working_years
    
    # Present value of consumption stream
    pv_factor = sum([growth_rate ** t for t in range(n_periods)])
    c0 = total_resources / pv_factor
    
    # Generate consumption path
    for t in range(n_periods):
        consumption[t] = c0 * (growth_rate ** t)
    
    return ages, consumption


def calculate_investment_strategy(params, wealth, age, risk_free_rate=None):
    """
    Calculate optimal portfolio allocation between risky and risk-free assets.
    
    Uses mean-variance framework with CRRA preferences.
    
    Args:
        params: RetirementParameters object
        wealth: Current wealth level
        age: Current age
        risk_free_rate: Risk-free rate (default: use params.r_real)
        
    Returns:
        dict: Dictionary with investment strategy details
            - risky_share: Fraction of wealth in risky assets
            - safe_share: Fraction of wealth in safe assets
            - risky_amount: Dollar amount in risky assets
            - safe_amount: Dollar amount in safe assets
    """
    if risk_free_rate is None:
        risk_free_rate = params.r_real
    
    # Simplified optimal portfolio share in risky asset
    # Merton's portfolio rule: w* = (mu - r) / (gamma * sigma^2)
    # Assume equity premium of 4% and volatility of 20%
    equity_premium = 0.04
    volatility = 0.20
    
    # Optimal share in risky asset
    risky_share = equity_premium / (params.gamma * volatility ** 2)
    risky_share = np.clip(risky_share, 0, 1)  # Constrain to [0, 1]
    
    # Adjust for age (reduce risk as age increases)
    age_factor = 1 - (age - 25) / (params.max_age - 25)
    risky_share = risky_share * max(age_factor, 0.2)  # Maintain at least 20% of optimal
    
    safe_share = 1 - risky_share
    
    return {
        'risky_share': risky_share,
        'safe_share': safe_share,
        'risky_amount': wealth * risky_share,
        'safe_amount': wealth * safe_share
    }
