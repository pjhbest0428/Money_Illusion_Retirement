## Overview

This package provides a skeleton framework for analyzing retirement decisions under money illusion. The structure includes:

- **Parameter calculation**: Computing derived economic parameters from base inputs
- **Retirement boundary determination**: Finding optimal retirement timing based on wealth
- **Modular design**: Ensuring compatibility between different calculation modules
# Money Illusion Retirement

Numerical Analysis for Money Illusion Retirement Problem

This repository provides a comprehensive framework for analyzing retirement decisions with money illusion considerations. The framework supports comparative statics analysis, allowing you to visualize how retirement boundaries, optimal consumption, and investment strategies change with different parameter values.

## Features

- **Modular Design**: Clean separation between model, analysis, and visualization
- **Easy Extension**: Add new parameters or analysis types with minimal code changes
- **Comparative Statics**: Built-in support for parameter variation analysis
- **Rich Visualizations**: Multiple plotting functions for different analysis types
- **Well-Documented**: Comprehensive docstrings and example scripts

## Project Structure

```
money_illusion_retirement/
├── money_illusion_retirement/    # Main package
│   ├── __init__.py              # Package initialization
│   ├── models.py                # Data models (RetirementParameters, RetirementBoundary)
│   ├── parameters.py            # Parameter calculation module
│   └── retirement_boundary.py   # Retirement boundary calculation module
├── tests/                       # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_parameters.py
│   └── test_retirement_boundary.py
├── example_usage.py             # Example demonstrating package usage
└── README.md                    # This file
```

## Quick Start

### Basic Usage

```python
from money_illusion_retirement import (
    RetirementParameters,
    ParameterCalculator,
    RetirementBoundaryCalculator,
)

# 1. Define parameters
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

# 2. Calculate derived parameters
param_calc = ParameterCalculator(params)
all_params = param_calc.calculate_all_parameters()

# 3. Compute retirement boundary
boundary_calc = RetirementBoundaryCalculator(params, grid_size=50)
boundary = boundary_calc.compute_boundary()

# 4. Make retirement decisions
should_retire = boundary_calc.should_retire(wealth=250.0, age=60)
```

### Running the Example

```bash
python example_usage.py
```

### Running Tests

```bash
python -m unittest discover tests
```

## Module Details

### `models.py`

Defines core data structures:
- **RetirementParameters**: Container for all model parameters
- **RetirementBoundary**: Container for computed retirement boundary results

### `parameters.py`

Contains the `ParameterCalculator` class with methods for:
- `calculate_real_return()`: Real rate of return after inflation
- `calculate_effective_discount_rate()`: Effective time preference rate
- `calculate_consumption_growth_rate()`: Optimal consumption growth
- `calculate_wealth_accumulation_factor()`: Wealth growth during working period
- `calculate_present_value_labor_income()`: PV of future labor income
- `validate_parameters()`: Check parameter validity

### `retirement_boundary.py`

Contains the `RetirementBoundaryCalculator` class with methods for:
- `compute_boundary()`: Main algorithm for finding retirement boundary
- `should_retire()`: Determine if retirement is optimal at given state
- `compute_value_function()`: Calculate value function
- `compute_optimal_consumption()`: Find optimal consumption policy
- `plot_boundary()`: Prepare data for visualization

## Implementation Status

This is a **skeleton code** framework. The following need to be implemented:

### To Be Implemented

1. **Parameter Calculation Formulas**
   - [ ] Actual real return calculation formula
   - [ ] Effective discount rate formula
   - [ ] Consumption growth rate formula
   - [ ] Other derived parameters as specified

2. **Retirement Boundary Algorithm**
   - [ ] Dynamic programming or optimal stopping algorithm
   - [ ] Value function iteration
   - [ ] Policy function computation
   - [ ] Convergence criteria

3. **Additional Features**
   - [ ] Visualization functions
   - [ ] Sensitivity analysis tools
   - [ ] Results export functionality

### Current Implementation

- ✅ Modular package structure
- ✅ Data models with validation
- ✅ Skeleton methods with placeholder implementations
- ✅ Unit tests for all modules
- ✅ Example usage script
- ✅ Documentation

## Design Principles

1. **Separation of Concerns**: Each module has a clear, single responsibility
2. **Compatibility**: Shared data models ensure consistency across modules
3. **Extensibility**: Easy to add new parameters or methods
4. **Testability**: Comprehensive unit tests for validation
5. **Documentation**: Clear docstrings and examples

## Next Steps

1. Implement actual economic formulas in `parameters.py`
2. Implement boundary calculation algorithm in `retirement_boundary.py`
3. Add visualization capabilities
4. Expand test coverage
5. Add integration tests
6. Create detailed documentation for the economic model

## Contributing

When implementing the actual formulas:
- Update the TODO comments in the code
- Add corresponding unit tests
- Update this README with formula details
- Ensure backward compatibility with the skeleton structure
Money_Illusion_Retirement/
├── src/                          # Core source code
│   ├── __init__.py              # Package initialization
│   ├── retirement_model.py      # Core retirement model calculations
│   ├── analysis.py              # Analysis utilities for comparative statics
│   └── plotting.py              # Plotting functions
├── examples/                     # Example scripts
│   ├── example1_retirement_boundary.py
│   ├── example2_consumption_path.py
│   ├── example3_investment_strategy.py
│   ├── example4_comprehensive.py
│   ├── example5_heatmap.py
│   └── example6_extension.py    # Demonstrates framework extensibility
├── tests/                        # Validation tests
│   └── validate.py              # Core functionality validation
├── outputs/                      # Generated plots (created automatically)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pjhbest0428/Money_Illusion_Retirement.git
cd Money_Illusion_Retirement
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Running Examples

The `examples/` directory contains six demonstration scripts:

```bash
# Example 1: Retirement boundary for different risk aversion levels
python examples/example1_retirement_boundary.py

# Example 2: Consumption paths for different inflation rates
python examples/example2_consumption_path.py

# Example 3: Investment strategies for different risk aversion levels
python examples/example3_investment_strategy.py

# Example 4: Comprehensive analysis with multiple plots
python examples/example4_comprehensive.py

# Example 5: Two-parameter heatmap analysis
python examples/example5_heatmap.py

# Example 6: Framework extension demonstration (custom metrics and analyses)
python examples/example6_extension.py
```

All examples will generate plots in the `outputs/` directory.

### Running Tests

```bash
# Run validation tests to verify core functionality
python tests/validate.py
```

### Basic Usage

```python
from src import (
    RetirementParameters,
    comparative_statics_retirement_boundary,
    plot_retirement_boundary
)

# Create base parameters
params = RetirementParameters(
    gamma=2.0,        # Risk aversion
    beta=0.96,        # Time discount factor
    r_real=0.04,      # Real interest rate
    inflation=0.02,   # Inflation rate
    wage=1.0          # Wage rate
)

# Run comparative statics
gamma_values = [1.5, 2.0, 2.5, 3.0]
wealth_grid, retirement_ages_list, params_list = \
    comparative_statics_retirement_boundary(
        params,
        param_name='gamma',
        param_values=gamma_values
    )

# Plot results
plot_retirement_boundary(
    wealth_grid,
    retirement_ages_list,
    params_list,
    param_name='gamma',
    param_values=gamma_values,
    output_path='outputs/my_plot.png'
)
```

## Core Components

### 1. Retirement Model (`src/retirement_model.py`)

Contains the fundamental retirement model:
- `RetirementParameters`: Parameter container class
- `calculate_retirement_boundary()`: Compute optimal retirement age
- `calculate_consumption_path()`: Compute optimal consumption over lifetime
- `calculate_investment_strategy()`: Compute optimal portfolio allocation

### 2. Analysis Utilities (`src/analysis.py`)

Provides functions for comparative statics:
- `comparative_statics_retirement_boundary()`: Analyze retirement boundary
- `comparative_statics_consumption()`: Analyze consumption paths
- `comparative_statics_investment()`: Analyze investment strategies
- `run_two_parameter_analysis()`: Two-dimensional parameter analysis
- Helper functions for calculating metrics

### 3. Plotting Functions (`src/plotting.py`)

Visualization tools:
- `plot_retirement_boundary()`: Plot retirement age vs wealth
- `plot_consumption_paths()`: Plot consumption over lifetime
- `plot_investment_strategy()`: Plot portfolio allocation over age
- `plot_comprehensive_analysis()`: Multi-panel comprehensive plot
- `create_heatmap()`: Two-parameter heatmap visualization

## Extending the Framework

### Adding a New Parameter

1. Add the parameter to `RetirementParameters.__init__()`
2. Use existing comparative statics functions - they automatically handle any parameter

Example:
```python
# The framework automatically supports any parameter
new_values = [val1, val2, val3]
results = comparative_statics_consumption(
    base_params,
    param_name='your_new_parameter',  # Works automatically!
    param_values=new_values
)
```

### Adding a New Analysis Function

1. Create your analysis function in `src/retirement_model.py`:
```python
def calculate_your_metric(params, ...):
    # Your calculation
    return result
```

2. Create a comparative statics wrapper in `src/analysis.py`:
```python
def comparative_statics_your_metric(base_params, param_name, param_values, ...):
    def analysis_func(params):
        return calculate_your_metric(params, ...)
    
    return run_parameter_variation(
        base_params, param_name, param_values, analysis_func
    )
```

3. Add a plotting function in `src/plotting.py` (optional)

### Adding a New Visualization

Add new plotting functions to `src/plotting.py`:
```python
def plot_your_analysis(data, param_name, param_values, output_path=None):
    plt.figure(figsize=(10, 6))
    # Your plotting code
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
```

## Model Description

The retirement model analyzes optimal decisions considering:

- **Money Illusion**: Agents may respond differently to nominal vs real rates
- **CRRA Utility**: Constant relative risk aversion utility function
- **Life Cycle**: Decisions from current age to maximum lifespan
- **Uncertainty**: Portfolio choice between risky and safe assets

Key decisions:
1. **When to retire**: Optimal retirement age given wealth
2. **How much to consume**: Consumption-savings tradeoff
3. **Portfolio allocation**: Risk-return tradeoff in investments

## Parameters

- `gamma`: Coefficient of relative risk aversion (higher = more risk averse)
- `beta`: Time discount factor (higher = more patient)
- `delta`: Depreciation rate
- `r_real`: Real interest rate
- `inflation`: Inflation rate
- `r_nominal`: Nominal interest rate (computed from Fisher equation)
- `wage`: Wage rate during working years
- `retirement_age`: Standard retirement age
- `max_age`: Maximum lifespan

## Output

All plots are saved to the `outputs/` directory with high resolution (300 DPI) and include:
- Line plots for single-parameter comparative statics
- Multi-panel figures for comprehensive analysis
- Heatmaps for two-parameter analysis

## License

This project is open source and available for academic and research purposes.

## Contributing

Contributions are welcome! The modular design makes it easy to add:
- New model features
- Additional analysis types
- More visualization options
- Enhanced numerical methods

## Citation

If you use this code in your research, please cite this repository.
