"""Trajectory-survival toy models for dissociated-control research.

These functions are generic probability utilities. They do not model a person,
clinical condition, or a specific language model.
"""

from __future__ import annotations

import math


def independent_survival(local_loss_probability: float, required_branches: int) -> float:
    """Probability all required branches survive under an independent toy model."""
    if isinstance(local_loss_probability, bool) or not isinstance(
        local_loss_probability, (int, float)
    ):
        raise TypeError("local_loss_probability must be numeric")
    if not 0.0 <= float(local_loss_probability) <= 1.0:
        raise ValueError("local_loss_probability must be in [0, 1]")
    if isinstance(required_branches, bool) or not isinstance(required_branches, int):
        raise TypeError("required_branches must be an integer")
    if required_branches < 0:
        raise ValueError("required_branches must be non-negative")
    return math.pow(1.0 - float(local_loss_probability), required_branches)


def equivalent_constant_loss_probability(
    observed_survival: float, required_branches: int
) -> float:
    """Invert the independent model to a constant per-branch loss probability."""
    if isinstance(observed_survival, bool) or not isinstance(observed_survival, (int, float)):
        raise TypeError("observed_survival must be numeric")
    if not 0.0 <= float(observed_survival) <= 1.0:
        raise ValueError("observed_survival must be in [0, 1]")
    if isinstance(required_branches, bool) or not isinstance(required_branches, int):
        raise TypeError("required_branches must be an integer")
    if required_branches <= 0:
        raise ValueError("required_branches must be positive")
    return 1.0 - math.pow(float(observed_survival), 1.0 / required_branches)
