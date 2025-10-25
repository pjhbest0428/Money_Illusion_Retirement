"""
Unit tests for retirement boundary calculator.

Tests the RetirementBoundaryCalculator class and its methods.
"""

import unittest
from money_illusion_retirement.models import RetirementParameters
from money_illusion_retirement.retirement_boundary import RetirementBoundaryCalculator


class TestRetirementBoundaryCalculator(unittest.TestCase):
    """Test cases for RetirementBoundaryCalculator class."""
    
    def setUp(self):
        """Set up test parameters and calculator."""
        self.params = RetirementParameters(
            discount_rate=0.03,
            interest_rate=0.05,
            inflation_rate=0.02,
            initial_wealth=100.0,
            labor_income=50.0,
            risk_aversion=2.0,
            time_horizon=80,
            retirement_age=65
        )
        self.calculator = RetirementBoundaryCalculator(
            params=self.params,
            grid_size=50,
            wealth_min=0.0,
            wealth_max=500.0
        )
    
    def test_initialization(self):
        """Test that calculator initializes properly."""
        self.assertEqual(self.calculator.params, self.params)
        self.assertEqual(self.calculator.grid_size, 50)
        self.assertEqual(self.calculator.wealth_min, 0.0)
        self.assertEqual(self.calculator.wealth_max, 500.0)
        self.assertFalse(self.calculator._boundary_computed)
    
    def test_create_wealth_grid(self):
        """Test wealth grid creation."""
        grid = self.calculator._wealth_grid
        
        # Check grid size
        self.assertEqual(len(grid), 50)
        
        # Check grid bounds
        self.assertEqual(grid[0], 0.0)
        self.assertEqual(grid[-1], 500.0)
        
        # Check grid is sorted
        self.assertTrue(all(grid[i] <= grid[i+1] for i in range(len(grid)-1)))
    
    def test_compute_boundary(self):
        """Test boundary computation."""
        boundary = self.calculator.compute_boundary()
        
        # Check boundary is computed
        self.assertIsNotNone(boundary)
        self.assertTrue(self.calculator._boundary_computed)
        
        # Check boundary structure
        self.assertEqual(len(boundary.wealth_grid), 50)
        self.assertEqual(len(boundary.boundary_values), 50)
        self.assertTrue(boundary.is_optimal)
        
        # Check convergence info
        self.assertIsNotNone(boundary.convergence_info)
        self.assertIn('converged', boundary.convergence_info)
    
    def test_should_retire(self):
        """Test retirement decision making."""
        # Compute boundary first
        self.calculator.compute_boundary()
        
        # Test various scenarios
        # These tests use placeholder logic, will change with real implementation
        result1 = self.calculator.should_retire(wealth=100.0, age=60)
        self.assertIsInstance(result1, bool)
        
        result2 = self.calculator.should_retire(wealth=300.0, age=70)
        self.assertIsInstance(result2, bool)
    
    def test_compute_value_function(self):
        """Test value function computation."""
        value = self.calculator.compute_value_function(wealth=100.0, age=50)
        
        # Should return a finite value
        self.assertIsInstance(value, float)
        self.assertTrue(value > 0 or value == float('-inf'))
        
        # Value at zero wealth should be very low
        value_zero = self.calculator.compute_value_function(wealth=0.0, age=50)
        self.assertEqual(value_zero, float('-inf'))
        
        # Value with no remaining time should be zero
        value_end = self.calculator.compute_value_function(wealth=100.0, age=80)
        self.assertEqual(value_end, 0.0)
    
    def test_compute_optimal_consumption(self):
        """Test optimal consumption computation."""
        # While working
        consumption_work = self.calculator.compute_optimal_consumption(
            wealth=100.0,
            age=50,
            retired=False
        )
        self.assertGreater(consumption_work, 0.0)
        
        # While retired
        consumption_retired = self.calculator.compute_optimal_consumption(
            wealth=100.0,
            age=70,
            retired=True
        )
        self.assertGreater(consumption_retired, 0.0)
        
        # At end of life
        consumption_end = self.calculator.compute_optimal_consumption(
            wealth=100.0,
            age=80,
            retired=True
        )
        self.assertEqual(consumption_end, 0.0)
    
    def test_get_boundary(self):
        """Test getting computed boundary."""
        # Before computation
        self.assertIsNone(self.calculator.get_boundary())
        
        # After computation
        self.calculator.compute_boundary()
        boundary = self.calculator.get_boundary()
        self.assertIsNotNone(boundary)
    
    def test_plot_boundary(self):
        """Test preparing plot data."""
        plot_data = self.calculator.plot_boundary()
        
        # Check plot data structure
        self.assertIn('wealth', plot_data)
        self.assertIn('boundary', plot_data)
        self.assertIn('xlabel', plot_data)
        self.assertIn('ylabel', plot_data)
        self.assertIn('title', plot_data)
        
        # Check data consistency
        self.assertEqual(len(plot_data['wealth']), len(plot_data['boundary']))


if __name__ == '__main__':
    unittest.main()
