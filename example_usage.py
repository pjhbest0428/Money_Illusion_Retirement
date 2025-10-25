"""
Example usage of the Money Illusion Retirement analysis package.

This script demonstrates how to use the skeleton code to:
1. Create retirement parameters
2. Calculate derived parameters
3. Compute retirement boundaries
4. Make retirement decisions
"""

from money_illusion_retirement import (
    RetirementParameters,
    ParameterCalculator,
    RetirementBoundaryCalculator,
)


def main():
    """Main example demonstrating package usage."""
    
    print("=" * 70)
    print("Money Illusion Retirement Analysis - Example Usage")
    print("=" * 70)
    print()
    
    # Step 1: Define base retirement parameters
    print("Step 1: Creating retirement parameters...")
    params = RetirementParameters(
        discount_rate=0.03,
        interest_rate=0.05,
        inflation_rate=0.02,
        initial_wealth=100.0,
        labor_income=50.0,
        risk_aversion=2.0,
        time_horizon=80,
        retirement_age=65
    )
    print(f"  Working period: {params.get_working_period()} years")
    print(f"  Retirement period: {params.get_retirement_period()} years")
    print()
    
    # Step 2: Calculate derived parameters
    print("Step 2: Calculating derived parameters...")
    param_calc = ParameterCalculator(params)
    
    # Validate parameters first
    is_valid, errors = param_calc.validate_parameters()
    if not is_valid:
        print("  Parameter validation errors:")
        for error in errors:
            print(f"    - {error}")
        return
    else:
        print("  Parameters are valid.")
    
    # Calculate individual parameters
    real_return = param_calc.calculate_real_return()
    print(f"  Real return: {real_return:.4f}")
    
    effective_discount = param_calc.calculate_effective_discount_rate()
    print(f"  Effective discount rate: {effective_discount:.4f}")
    
    consumption_growth = param_calc.calculate_consumption_growth_rate()
    print(f"  Consumption growth rate: {consumption_growth:.4f}")
    
    wealth_factor = param_calc.calculate_wealth_accumulation_factor()
    print(f"  Wealth accumulation factor: {wealth_factor:.4f}")
    
    pv_income = param_calc.calculate_present_value_labor_income()
    print(f"  PV of labor income: {pv_income:.2f}")
    
    # Get all parameters at once
    all_params = param_calc.calculate_all_parameters()
    print(f"  Total derived parameters: {len(all_params)}")
    print()
    
    # Step 3: Compute retirement boundary
    print("Step 3: Computing retirement boundary...")
    boundary_calc = RetirementBoundaryCalculator(
        params=params,
        grid_size=50,
        wealth_min=0.0,
        wealth_max=500.0
    )
    
    boundary = boundary_calc.compute_boundary(
        max_iterations=1000,
        tolerance=1e-6
    )
    
    print(f"  Grid size: {len(boundary.wealth_grid)}")
    print(f"  Boundary computed: {boundary.is_optimal}")
    if boundary.convergence_info:
        print(f"  Convergence iterations: {boundary.convergence_info.get('iterations', 'N/A')}")
        print(f"  Converged: {boundary.convergence_info.get('converged', 'N/A')}")
    print()
    
    # Step 4: Make retirement decisions for specific scenarios
    print("Step 4: Evaluating retirement decisions...")
    scenarios = [
        (100.0, 60),   # Low wealth, age 60
        (250.0, 60),   # Medium wealth, age 60
        (400.0, 60),   # High wealth, age 60
        (100.0, 65),   # Low wealth, at retirement age
        (250.0, 70),   # Medium wealth, past retirement age
    ]
    
    for wealth, age in scenarios:
        should_retire = boundary_calc.should_retire(wealth, age)
        boundary_age = boundary.get_boundary_at_wealth(wealth)
        optimal_consumption = boundary_calc.compute_optimal_consumption(
            wealth, age, should_retire
        )
        
        print(f"  Wealth=${wealth:6.0f}, Age={age:2d}: ", end="")
        print(f"Retire={'Yes' if should_retire else 'No ':3s} ", end="")
        print(f"(boundary age: {boundary_age:5.1f}, ", end="")
        print(f"consumption: ${optimal_consumption:6.2f})")
    
    print()
    
    # Step 5: Get plotting data
    print("Step 5: Preparing data for visualization...")
    plot_data = boundary_calc.plot_boundary()
    print(f"  Plot title: {plot_data['title']}")
    print(f"  X-axis: {plot_data['xlabel']}")
    print(f"  Y-axis: {plot_data['ylabel']}")
    print(f"  Data points: {len(plot_data['wealth'])}")
    print()
    
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Implement actual formulas in ParameterCalculator methods")
    print("  2. Implement actual boundary algorithm in RetirementBoundaryCalculator")
    print("  3. Add unit tests for each module")
    print("  4. Add visualization functions for results")
    print()


if __name__ == "__main__":
    main()
