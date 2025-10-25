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
│   └── example5_heatmap.py
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

The `examples/` directory contains five demonstration scripts:

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
```

All examples will generate plots in the `outputs/` directory.

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
