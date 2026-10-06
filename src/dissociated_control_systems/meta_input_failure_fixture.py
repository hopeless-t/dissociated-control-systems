"""Synthetic failure fixture for generic inverse-variance meta-analysis inputs.

The fixture demonstrates a class of failure only: effect estimates and standard
errors may be correctly aligned while optional sample-size metadata are
misbound. A pooling rule based on effect/se remains unchanged while displayed
sample totals change.

This does not reproduce or attribute any specific publication's code path.
"""

from __future__ import annotations

from math import exp
from typing import Sequence


def inverse_variance_pooled_log_effect(
    log_effects: Sequence[float],
    standard_errors: Sequence[float],
) -> float:
    if len(log_effects) != len(standard_errors) or not log_effects:
        raise ValueError("effect and standard-error vectors must be non-empty and aligned")
    weights = []
    for se in standard_errors:
        value = float(se)
        if value <= 0:
            raise ValueError("standard errors must be positive")
        weights.append(1.0 / (value * value))
    total_weight = sum(weights)
    return sum(w * float(effect) for w, effect in zip(weights, log_effects, strict=True)) / total_weight


def inverse_variance_pooled_ratio(
    log_effects: Sequence[float], standard_errors: Sequence[float]
) -> float:
    return exp(inverse_variance_pooled_log_effect(log_effects, standard_errors))


def sample_total(intervention_n: Sequence[int], control_n: Sequence[int]) -> int:
    if len(intervention_n) != len(control_n) or not intervention_n:
        raise ValueError("sample-size vectors must be non-empty and aligned")
    total = 0
    for left, right in zip(intervention_n, control_n, strict=True):
        for value in (left, right):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError("sample counts must be positive integers")
        total += left + right
    return total


def compare_metadata_bindings(
    *,
    log_effects: Sequence[float],
    standard_errors: Sequence[float],
    correct_intervention_n: Sequence[int],
    correct_control_n: Sequence[int],
    alternate_intervention_n: Sequence[int],
    alternate_control_n: Sequence[int],
) -> dict[str, float | int | bool]:
    """Show that metadata replacement does not alter an effect/se-only pool."""

    k = len(log_effects)
    lengths = (
        len(standard_errors),
        len(correct_intervention_n),
        len(correct_control_n),
        len(alternate_intervention_n),
        len(alternate_control_n),
    )
    if any(length != k for length in lengths):
        raise ValueError("all parallel vectors must have equal length")

    pooled = inverse_variance_pooled_ratio(log_effects, standard_errors)
    correct_total = sample_total(correct_intervention_n, correct_control_n)
    alternate_total = sample_total(alternate_intervention_n, alternate_control_n)
    return {
        "k": k,
        "pooled_effect_correct_metadata": pooled,
        "pooled_effect_alternate_metadata": pooled,
        "pooled_effect_unchanged": True,
        "correct_sample_total": correct_total,
        "alternate_sample_total": alternate_total,
        "sample_total_changed": correct_total != alternate_total,
    }
