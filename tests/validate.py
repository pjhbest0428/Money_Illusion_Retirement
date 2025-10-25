"""
Simple validation script to verify core functionality.

This script tests that all core functions work correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src import (
    RetirementParameters,
    calculate_retirement_boundary,
    calculate_consumption_path,
    calculate_investment_strategy,
    comparative_statics_retirement_boundary,
    comparative_statics_consumption,
    comparative_statics_investment,
)


def test_retirement_parameters():
    """Test RetirementParameters class."""
    print("Testing RetirementParameters...")
    params = RetirementParameters()
    assert params.gamma > 0, "gamma should be positive"
    assert params.beta > 0 and params.beta < 1, "beta should be in (0, 1)"
    assert params.r_real >= 0, "r_real should be non-negative"
    assert params.r_nominal > params.r_real, "nominal rate should exceed real rate with positive inflation"
    
    # Test copy
    params2 = params.copy()
    assert params2.gamma == params.gamma, "copy should preserve gamma"
    
    print("  ✓ RetirementParameters works correctly")


def test_retirement_boundary():
    """Test retirement boundary calculation."""
    print("Testing retirement boundary calculation...")
    params = RetirementParameters()
    wealth_grid = np.linspace(0, 100, 10)
    
    retirement_ages = calculate_retirement_boundary(params, wealth_grid)
    
    assert len(retirement_ages) == len(wealth_grid), "output length should match input"
    assert all(retirement_ages > 0), "all retirement ages should be positive"
    assert all(retirement_ages <= params.max_age), "retirement ages should not exceed max_age"
    
    print("  ✓ Retirement boundary calculation works correctly")


def test_consumption_path():
    """Test consumption path calculation."""
    print("Testing consumption path calculation...")
    params = RetirementParameters()
    
    ages, consumption = calculate_consumption_path(params, wealth=50, age=30, retirement_age=65)
    
    assert len(ages) == len(consumption), "ages and consumption should have same length"
    assert all(consumption > 0), "consumption should be positive"
    assert ages[0] == 30, "should start at specified age"
    assert ages[-1] == params.max_age - 1, "should end at max_age - 1"
    
    print("  ✓ Consumption path calculation works correctly")


def test_investment_strategy():
    """Test investment strategy calculation."""
    print("Testing investment strategy calculation...")
    params = RetirementParameters()
    
    strategy = calculate_investment_strategy(params, wealth=50, age=30)
    
    assert 'risky_share' in strategy, "should return risky_share"
    assert 'safe_share' in strategy, "should return safe_share"
    assert 0 <= strategy['risky_share'] <= 1, "risky_share should be in [0, 1]"
    assert abs(strategy['risky_share'] + strategy['safe_share'] - 1) < 1e-10, "shares should sum to 1"
    assert abs(strategy['risky_amount'] + strategy['safe_amount'] - 50) < 1e-10, "amounts should sum to wealth"
    
    print("  ✓ Investment strategy calculation works correctly")


def test_comparative_statics():
    """Test comparative statics functions."""
    print("Testing comparative statics functions...")
    params = RetirementParameters()
    
    # Test retirement boundary comparative statics
    gamma_values = [1.5, 2.0, 2.5]
    wealth_grid, retirement_ages_list, params_list = comparative_statics_retirement_boundary(
        params, 'gamma', gamma_values, wealth_min=0, wealth_max=50, n_points=10
    )
    assert len(retirement_ages_list) == len(gamma_values), "should have one result per parameter value"
    
    # Test consumption comparative statics
    ages_list, consumption_list, _ = comparative_statics_consumption(
        params, 'beta', [0.94, 0.96, 0.98], wealth=50, age=30, retirement_age=65
    )
    assert len(consumption_list) == 3, "should have three consumption paths"
    
    # Test investment comparative statics
    ages, risky_shares_list, _ = comparative_statics_investment(
        params, 'gamma', [1.5, 2.0, 2.5], wealth=50, age_min=25, age_max=40
    )
    assert len(risky_shares_list) == 3, "should have three risky share arrays"
    
    print("  ✓ Comparative statics functions work correctly")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Running Validation Tests")
    print("=" * 60)
    print()
    
    try:
        test_retirement_parameters()
        test_retirement_boundary()
        test_consumption_path()
        test_investment_strategy()
        test_comparative_statics()
        
        print()
        print("=" * 60)
        print("All validation tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
