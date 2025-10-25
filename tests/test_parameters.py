"""
Unit tests for parameter calculator.

Tests the ParameterCalculator class and its methods.
"""

import unittest
from money_illusion_retirement.models import RetirementParameters
from money_illusion_retirement.parameters import ParameterCalculator


class TestParameterCalculator(unittest.TestCase):
    """Test cases for ParameterCalculator class."""
    
    def setUp(self):
        """Set up test parameters."""
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
        self.calculator = ParameterCalculator(self.params)
    
    def test_initialization(self):
        """Test that calculator initializes properly."""
        self.assertEqual(self.calculator.base_params, self.params)
        self.assertEqual(self.calculator._derived_params, {})
    
    def test_calculate_real_return(self):
        """Test real return calculation."""
        real_return = self.calculator.calculate_real_return()
        
        # (1.05 / 1.02) - 1 ≈ 0.0294
        self.assertAlmostEqual(real_return, 0.0294117647, places=5)
    
    def test_calculate_effective_discount_rate(self):
        """Test effective discount rate calculation."""
        effective_rate = self.calculator.calculate_effective_discount_rate()
        
        # Currently returns discount_rate as placeholder
        self.assertEqual(effective_rate, 0.03)
    
    def test_calculate_consumption_growth_rate(self):
        """Test consumption growth rate calculation."""
        growth_rate = self.calculator.calculate_consumption_growth_rate()
        
        # (real_return - discount_rate) / risk_aversion
        # Approximately (0.0294 - 0.03) / 2.0 ≈ -0.0003
        self.assertIsInstance(growth_rate, float)
        self.assertLess(abs(growth_rate), 1.0)  # Should be reasonable
    
    def test_calculate_wealth_accumulation_factor(self):
        """Test wealth accumulation factor calculation."""
        factor = self.calculator.calculate_wealth_accumulation_factor()
        
        # (1.05)^65
        self.assertGreater(factor, 1.0)
        self.assertIsInstance(factor, float)
    
    def test_calculate_present_value_labor_income(self):
        """Test PV of labor income calculation."""
        pv = self.calculator.calculate_present_value_labor_income()
        
        # Should be positive and reasonable
        self.assertGreater(pv, 0.0)
        self.assertIsInstance(pv, float)
    
    def test_calculate_all_parameters(self):
        """Test calculating all parameters at once."""
        all_params = self.calculator.calculate_all_parameters()
        
        # Should contain all derived parameters
        expected_keys = [
            'real_return',
            'effective_discount_rate',
            'consumption_growth_rate',
            'wealth_accumulation_factor',
            'pv_labor_income'
        ]
        
        for key in expected_keys:
            self.assertIn(key, all_params)
    
    def test_get_parameter(self):
        """Test retrieving a specific parameter."""
        self.calculator.calculate_real_return()
        
        real_return = self.calculator.get_parameter('real_return')
        self.assertIsNotNone(real_return)
        self.assertIsInstance(real_return, float)
        
        # Non-existent parameter should return None
        self.assertIsNone(self.calculator.get_parameter('nonexistent'))
    
    def test_validate_parameters_valid(self):
        """Test parameter validation with valid parameters."""
        is_valid, errors = self.calculator.validate_parameters()
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_parameters_invalid_discount_rate(self):
        """Test parameter validation with invalid discount rate."""
        invalid_params = RetirementParameters(
            discount_rate=1.5,  # Invalid: > 1
            time_horizon=80,
            retirement_age=65
        )
        calculator = ParameterCalculator(invalid_params)
        
        is_valid, errors = calculator.validate_parameters()
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_parameters_negative_wealth(self):
        """Test parameter validation with negative wealth."""
        invalid_params = RetirementParameters(
            initial_wealth=-100.0,  # Invalid: negative
            time_horizon=80,
            retirement_age=65
        )
        calculator = ParameterCalculator(invalid_params)
        
        is_valid, errors = calculator.validate_parameters()
        
        self.assertFalse(is_valid)
        self.assertTrue(any('wealth' in error.lower() for error in errors))


if __name__ == '__main__':
    unittest.main()
