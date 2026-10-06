"""Operational Follicular Recoverability Knee (FRK) helpers.

HF01 defines a knee in *control gain*, not in hair appearance or a static marker.
For baseline degeneration burden z and a declared control input u, the local
functional control gain is approximated by a controlled-vs-reference response
per unit input.  An operational knee candidate is an interval where that gain
falls unusually steeply across z.

This is synthetic design machinery.  A knee does not imply hysteresis,
irreversibility, or a clinical threshold.  A unique steepest interval is also
not sufficient under noise; confirmatory use requires a predeclared slope-
contrast requirement and external replication.
"""

from __future__ import annotations

from typing import Iterable


def local_control_gain(
    controlled_output: float,
    reference_output: float,
    input_strength: float,
) -> float:
    if input_strength == 0:
        raise ValueError("input_strength must be non-zero")
    return (controlled_output - reference_output) / input_strength


def gain_change_rates(
    burden: Iterable[float],
    gains: Iterable[float],
) -> tuple[tuple[float, float, float], ...]:
    z = tuple(float(v) for v in burden)
    g = tuple(float(v) for v in gains)
    if len(z) != len(g):
        raise ValueError("burden and gains must have equal length")
    if len(z) < 2:
        raise ValueError("at least two burden levels are required")
    if any(right <= left for left, right in zip(z, z[1:])):
        raise ValueError("burden must be strictly increasing")

    return tuple(
        (left, right, (g_right - g_left) / (right - left))
        for left, right, g_left, g_right in zip(z, z[1:], g, g[1:])
    )


def unique_steepest_gain_loss_interval(
    burden: Iterable[float],
    gains: Iterable[float],
    *,
    tolerance: float = 1e-12,
) -> tuple[float, float] | None:
    """Return a unique interval with the most negative gain slope, else None.

    This is an exploratory diagnostic only.  Tiny noise can create a unique
    maximum slope even when the underlying relation is smooth.
    """
    rates = gain_change_rates(burden, gains)
    min_rate = min(item[2] for item in rates)
    matches = [item for item in rates if abs(item[2] - min_rate) <= tolerance]
    if len(matches) != 1:
        return None
    left, right, _ = matches[0]
    return left, right


def qualified_gain_knee_interval(
    burden: Iterable[float],
    gains: Iterable[float],
    *,
    minimum_slope_contrast: float,
    tolerance: float = 1e-12,
) -> tuple[float, float] | None:
    """Return a knee candidate only if the steepest loss is meaningfully isolated.

    `minimum_slope_contrast` is the predeclared amount by which the most
    negative adjacent gain slope must be more negative than the second-most
    negative slope.  It must be chosen independently of the candidate outcome.
    This remains a deterministic screening rule; uncertainty and donor-held-out
    replication are separate requirements.
    """
    if minimum_slope_contrast <= 0:
        raise ValueError("minimum_slope_contrast must be > 0")

    rates = gain_change_rates(burden, gains)
    if len(rates) < 2:
        return None

    ordered = sorted(rates, key=lambda item: item[2])
    steepest = ordered[0]
    second = ordered[1]
    contrast = second[2] - steepest[2]
    if contrast + tolerance < minimum_slope_contrast:
        return None

    # Also reject tied steepest slopes within tolerance.
    if abs(second[2] - steepest[2]) <= tolerance:
        return None
    return steepest[0], steepest[1]
