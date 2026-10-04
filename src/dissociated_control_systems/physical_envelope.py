"""Physics-informed envelope primitives for synthetic control research.

This module validates projected support/load and derives lightweight drawing
priors. It is not a biomechanical simulator.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


@dataclass(frozen=True)
class SupportPair:
    left_force: float
    right_force: float
    total_weight: float
    force_residual: float
    moment_residual: float
    stable: bool
    stability_margin: float


def solve_vertical_support_pair(
    *,
    left_x: float,
    right_x: float,
    com_x: float,
    mass: float,
    gravity: float = 9.81,
) -> SupportPair:
    """Solve 2D static vertical reactions for a projected two-support system."""

    left_x = _finite(left_x, "left_x")
    right_x = _finite(right_x, "right_x")
    com_x = _finite(com_x, "com_x")
    mass = _finite(mass, "mass")
    gravity = abs(_finite(gravity, "gravity"))
    if mass <= 0:
        raise ValueError("mass must be positive")
    if right_x <= left_x:
        raise ValueError("right_x must be greater than left_x")

    weight = mass * gravity
    span = right_x - left_x
    left_force = weight * (right_x - com_x) / span
    right_force = weight * (com_x - left_x) / span

    force_residual = abs((left_force + right_force) - weight)
    moment_residual = abs(
        left_force * left_x + right_force * right_x - weight * com_x
    )
    stable = left_force >= 0.0 and right_force >= 0.0
    margin = min(com_x - left_x, right_x - com_x) / span
    return SupportPair(
        left_force=left_force,
        right_force=right_force,
        total_weight=weight,
        force_residual=force_residual,
        moment_residual=moment_residual,
        stable=stable,
        stability_margin=margin,
    )


def load_fraction(force: float, total_weight: float) -> float:
    force = _finite(force, "force")
    total_weight = _finite(total_weight, "total_weight")
    if total_weight <= 0:
        raise ValueError("total_weight must be positive")
    return max(0.0, force / total_weight)


def envelope_scale(
    *,
    load_fraction_value: float,
    depth_scale: float,
    proximal_gain: float = 0.45,
    distal_gain: float = 0.12,
) -> tuple[float, float]:
    """Return proximal/distal thickness scales for a stylized soft envelope."""

    load_fraction_value = max(
        0.0, _finite(load_fraction_value, "load_fraction_value")
    )
    depth_scale = _finite(depth_scale, "depth_scale")
    proximal_gain = _finite(proximal_gain, "proximal_gain")
    distal_gain = _finite(distal_gain, "distal_gain")
    if depth_scale <= 0 or proximal_gain < 0 or distal_gain < 0:
        raise ValueError("depth scale must be positive and gains non-negative")

    proximal = depth_scale * (1.0 + proximal_gain * load_fraction_value)
    distal = depth_scale * (1.0 + distal_gain * load_fraction_value)
    return proximal, distal


def contact_compression(
    *,
    force: float,
    stiffness: float,
    max_compression: float = 1.0,
) -> float:
    """Hooke-law-style compression proxy used only as a drawing prior."""

    force = max(0.0, _finite(force, "force"))
    stiffness = _finite(stiffness, "stiffness")
    max_compression = _finite(max_compression, "max_compression")
    if stiffness <= 0 or max_compression < 0:
        raise ValueError("invalid stiffness or compression ceiling")
    return min(force / stiffness, max_compression)
