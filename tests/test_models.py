"""
Unit tests for data models.

Tests the RetirementParameters and RetirementBoundary data classes.
"""

import unittest
from money_illusion_retirement.models import RetirementParameters, RetirementBoundary


class TestRetirementParameters(unittest.TestCase):
    """Test cases for RetirementParameters class."""
    
    def test_initialization_with_defaults(self):
        """Test that parameters can be initialized with default values."""
        params = RetirementParameters()
        self.assertEqual(params.discount_rate, 0.0)
        self.assertEqual(params.interest_rate, 0.0)
        self.assertEqual(params.time_horizon, 100)
        self.assertEqual(params.retirement_age, 65)
    
    def test_initialization_with_custom_values(self):
        """Test that parameters can be initialized with custom values."""
        params = RetirementParameters(
            discount_rate=0.03,
            interest_rate=0.05,
            inflation_rate=0.02,
            time_horizon=80,
            retirement_age=60
        )
        self.assertEqual(params.discount_rate, 0.03)
        self.assertEqual(params.interest_rate, 0.05)
        self.assertEqual(params.inflation_rate, 0.02)
        self.assertEqual(params.time_horizon, 80)
        self.assertEqual(params.retirement_age, 60)
    
    def test_invalid_time_horizon(self):
        """Test that invalid time_horizon raises ValueError."""
        with self.assertRaises(ValueError):
            RetirementParameters(time_horizon=0)
        
        with self.assertRaises(ValueError):
            RetirementParameters(time_horizon=-10)
    
    def test_invalid_retirement_age(self):
        """Test that invalid retirement_age raises ValueError."""
        with self.assertRaises(ValueError):
            RetirementParameters(retirement_age=-5)
        
        with self.assertRaises(ValueError):
            RetirementParameters(time_horizon=80, retirement_age=90)
    
    def test_get_working_period(self):
        """Test working period calculation."""
        params = RetirementParameters(retirement_age=65)
        self.assertEqual(params.get_working_period(), 65)
    
    def test_get_retirement_period(self):
        """Test retirement period calculation."""
        params = RetirementParameters(time_horizon=100, retirement_age=65)
        self.assertEqual(params.get_retirement_period(), 35)


class TestRetirementBoundary(unittest.TestCase):
    """Test cases for RetirementBoundary class."""
    
    def test_initialization(self):
        """Test that boundary can be initialized properly."""
        wealth_grid = [0.0, 10.0, 20.0, 30.0]
        boundary_values = [60.0, 62.0, 64.0, 66.0]
        
        boundary = RetirementBoundary(
            wealth_grid=wealth_grid,
            boundary_values=boundary_values
        )
        
        self.assertEqual(boundary.wealth_grid, wealth_grid)
        self.assertEqual(boundary.boundary_values, boundary_values)
        self.assertTrue(boundary.is_optimal)
    
    def test_mismatched_lengths(self):
        """Test that mismatched grid and values raise ValueError."""
        with self.assertRaises(ValueError):
            RetirementBoundary(
                wealth_grid=[0.0, 10.0, 20.0],
                boundary_values=[60.0, 62.0]
            )
    
    def test_empty_boundary(self):
        """Test that empty boundary data raises ValueError."""
        with self.assertRaises(ValueError):
            RetirementBoundary(
                wealth_grid=[],
                boundary_values=[]
            )
    
    def test_get_boundary_at_wealth_exact(self):
        """Test getting boundary value at exact grid point."""
        boundary = RetirementBoundary(
            wealth_grid=[0.0, 10.0, 20.0],
            boundary_values=[60.0, 62.0, 64.0]
        )
        
        self.assertEqual(boundary.get_boundary_at_wealth(10.0), 62.0)
    
    def test_get_boundary_at_wealth_interpolation(self):
        """Test getting boundary value with interpolation."""
        boundary = RetirementBoundary(
            wealth_grid=[0.0, 10.0, 20.0],
            boundary_values=[60.0, 62.0, 64.0]
        )
        
        # Midpoint between 10 and 20 should give 63.0
        result = boundary.get_boundary_at_wealth(15.0)
        self.assertAlmostEqual(result, 63.0, places=5)
    
    def test_get_boundary_at_wealth_out_of_range(self):
        """Test getting boundary value outside grid range."""
        boundary = RetirementBoundary(
            wealth_grid=[0.0, 10.0, 20.0],
            boundary_values=[60.0, 62.0, 64.0]
        )
        
        # Below range should return first value
        self.assertEqual(boundary.get_boundary_at_wealth(-5.0), 60.0)
        
        # Above range should return last value
        self.assertEqual(boundary.get_boundary_at_wealth(100.0), 64.0)


if __name__ == '__main__':
    unittest.main()
