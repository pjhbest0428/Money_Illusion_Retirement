"""
Money Illusion Retirement Analysis Package

This package provides numerical analysis tools for studying money illusion
in retirement problems.
"""

from .models import RetirementParameters, RetirementBoundary
from .parameters import ParameterCalculator
from .retirement_boundary import RetirementBoundaryCalculator

__version__ = "0.1.0"

__all__ = [
    "RetirementParameters",
    "RetirementBoundary",
    "ParameterCalculator",
    "RetirementBoundaryCalculator",
]
