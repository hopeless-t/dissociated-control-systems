"""Minimal arithmetic audits for published meta-analysis forest plots."""

from __future__ import annotations

from math import exp, isfinite, log
from typing import Iterable


def pooled_ratio_from_displayed_weights(
    ratios: Iterable[float], weights_percent: Iterable[float]
) -> float:
    """Reconstruct a displayed pooled ratio from log-scale meta-analysis weights.

    This only checks arithmetic consistency of the values printed in a forest
    plot. It does not validate how weights, standard errors, or study effects
    were originally estimated.
    """
    effects = tuple(ratios)
    weights = tuple(weights_percent)
    if not effects or len(effects) != len(weights):
        raise ValueError("effects and weights must be non-empty and have equal length")

    for value in effects:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("ratios must be numeric")
        if value <= 0 or not isfinite(float(value)):
            raise ValueError("ratios must be finite and positive")

    for value in weights:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("weights must be numeric")
        if value < 0 or not isfinite(float(value)):
            raise ValueError("weights must be finite and non-negative")

    total_weight = sum(float(value) for value in weights)
    if abs(total_weight - 100.0) > 0.05:
        raise ValueError("displayed weights must sum to approximately 100 percent")

    normalized = [float(value) / total_weight for value in weights]
    return exp(sum(weight * log(float(effect)) for weight, effect in zip(normalized, effects)))
