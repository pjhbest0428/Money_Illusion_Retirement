"""
Data models for Money Illusion Retirement analysis.

This module defines the core data structures used across the package
to ensure compatibility between different calculation modules.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RetirementParameters:
    """
    Container for retirement model parameters.
    
    This class holds all parameters needed for retirement calculations.
    Specific parameters will be added based on the economic model being used.
    
    Attributes:
        discount_rate: The subjective discount rate
        interest_rate: The real interest rate
        inflation_rate: The inflation rate
        initial_wealth: Initial wealth at start of working period
        labor_income: Labor income during working period
        risk_aversion: Coefficient of relative risk aversion
        time_horizon: Total time horizon for the model
        retirement_age: Age at retirement
    """
    
    discount_rate: float = 0.0
    interest_rate: float = 0.0
    inflation_rate: float = 0.0
    initial_wealth: float = 0.0
    labor_income: float = 0.0
    risk_aversion: float = 1.0
    time_horizon: int = 100
    retirement_age: int = 65
    
    # Additional parameters can be added as needed
    custom_params: Optional[dict] = None
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if self.time_horizon <= 0:
            raise ValueError("time_horizon must be positive")
        if self.retirement_age < 0:
            raise ValueError("retirement_age cannot be negative")
        if self.retirement_age >= self.time_horizon:
            raise ValueError("retirement_age must be less than time_horizon")
    
    def get_working_period(self) -> int:
        """Return the length of the working period."""
        return self.retirement_age
    
    def get_retirement_period(self) -> int:
        """Return the length of the retirement period."""
        return self.time_horizon - self.retirement_age


@dataclass
class RetirementBoundary:
    """
    Container for retirement boundary results.
    
    This class holds the computed retirement boundary, which represents
    the optimal retirement decision as a function of state variables.
    
    Attributes:
        wealth_grid: Array of wealth levels
        boundary_values: Corresponding boundary values at each wealth level
        is_optimal: Whether the boundary represents an optimal solution
        convergence_info: Information about numerical convergence
    """
    
    wealth_grid: list
    boundary_values: list
    is_optimal: bool = True
    convergence_info: Optional[dict] = None
    
    def __post_init__(self):
        """Validate boundary data after initialization."""
        if len(self.wealth_grid) != len(self.boundary_values):
            raise ValueError(
                "wealth_grid and boundary_values must have the same length"
            )
        if len(self.wealth_grid) == 0:
            raise ValueError("boundary data cannot be empty")
    
    def get_boundary_at_wealth(self, wealth: float) -> Optional[float]:
        """
        Get the boundary value at a specific wealth level using interpolation.
        
        Args:
            wealth: The wealth level to query
            
        Returns:
            Interpolated boundary value, or None if wealth is out of range
        """
        if not self.wealth_grid:
            return None
            
        # Simple linear interpolation (can be enhanced with scipy)
        if wealth <= self.wealth_grid[0]:
            return self.boundary_values[0]
        if wealth >= self.wealth_grid[-1]:
            return self.boundary_values[-1]
            
        # Find bracketing points
        for i in range(len(self.wealth_grid) - 1):
            if self.wealth_grid[i] <= wealth <= self.wealth_grid[i + 1]:
                # Linear interpolation
                t = (wealth - self.wealth_grid[i]) / (
                    self.wealth_grid[i + 1] - self.wealth_grid[i]
                )
                return (1 - t) * self.boundary_values[i] + t * self.boundary_values[i + 1]
        
        return None
