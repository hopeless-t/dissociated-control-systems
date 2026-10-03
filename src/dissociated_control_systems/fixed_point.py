"""Deterministic probes for fixed-point and attractor-style state dynamics.

These utilities are mathematical research primitives. They do not identify a
biological mechanism and do not imply that a hidden state is a literal neural
state.
"""

from __future__ import annotations

from math import sqrt
from typing import Iterable


Vector = tuple[float, ...]


def _vector(values: Iterable[float], name: str) -> Vector:
    result = tuple(float(value) for value in values)
    if not result:
        raise ValueError(f"{name} must not be empty")
    return result


def _same_dimension(left: Vector, right: Vector) -> None:
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimension")


def dot(left: Iterable[float], right: Iterable[float]) -> float:
    a = _vector(left, "left")
    b = _vector(right, "right")
    _same_dimension(a, b)
    return sum(x * y for x, y in zip(a, b, strict=True))


def l2_norm(values: Iterable[float]) -> float:
    vector = _vector(values, "values")
    return sqrt(sum(value * value for value in vector))


def distance(left: Iterable[float], right: Iterable[float]) -> float:
    a = _vector(left, "left")
    b = _vector(right, "right")
    _same_dimension(a, b)
    return l2_norm(x - y for x, y in zip(a, b, strict=True))


def step_norms(trajectory: Iterable[Iterable[float]]) -> tuple[float, ...]:
    states = tuple(_vector(state, "state") for state in trajectory)
    if len(states) < 2:
        return ()
    dimension = len(states[0])
    if any(len(state) != dimension for state in states):
        raise ValueError("trajectory states must have the same dimension")
    return tuple(distance(previous, current) for previous, current in zip(states, states[1:]))


def contraction_ratios(
    trajectory: Iterable[Iterable[float]],
    *,
    zero_tolerance: float = 1e-15,
) -> tuple[float, ...]:
    if zero_tolerance < 0:
        raise ValueError("zero_tolerance must be non-negative")
    steps = step_norms(trajectory)
    ratios: list[float] = []
    for previous, current in zip(steps, steps[1:]):
        if previous <= zero_tolerance:
            ratios.append(0.0 if current <= zero_tolerance else float("inf"))
        else:
            ratios.append(current / previous)
    return tuple(ratios)


def iterate_affine_contraction(
    initial: Iterable[float],
    target: Iterable[float],
    *,
    retention: float,
    steps: int,
) -> tuple[Vector, ...]:
    """Iterate x_(t+1) = target + retention * (x_t - target).

    The synthetic map is a known-answer contraction when 0 <= retention < 1.
    """

    state = _vector(initial, "initial")
    fixed_point = _vector(target, "target")
    _same_dimension(state, fixed_point)
    if not 0.0 <= retention < 1.0:
        raise ValueError("retention must satisfy 0 <= retention < 1")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a non-negative integer")

    trajectory = [state]
    for _ in range(steps):
        state = tuple(
            target_value + retention * (value - target_value)
            for value, target_value in zip(state, fixed_point, strict=True)
        )
        trajectory.append(state)
    return tuple(trajectory)


def convergence_depth(
    trajectory: Iterable[Iterable[float]],
    target: Iterable[float],
    *,
    tolerance: float,
) -> int | None:
    """Return the first index after which every state stays within tolerance."""

    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    states = tuple(_vector(state, "state") for state in trajectory)
    fixed_point = _vector(target, "target")
    if not states:
        return None
    if any(len(state) != len(fixed_point) for state in states):
        raise ValueError("trajectory states and target must have the same dimension")

    within = tuple(distance(state, fixed_point) <= tolerance for state in states)
    for index in range(len(states)):
        if all(within[index:]):
            return index
    return None


def fixed_point_residual(
    state: Iterable[float],
    next_state: Iterable[float],
) -> float:
    """Measure ||F(x) - x|| from an observed state and its next iterate."""

    return distance(state, next_state)


def drive_gain(state: Iterable[float], drive: Iterable[float]) -> float:
    """Return the scalar projection coefficient of state onto drive."""

    x = _vector(state, "state")
    u = _vector(drive, "drive")
    _same_dimension(x, u)
    denominator = dot(u, u)
    if denominator == 0.0:
        raise ValueError("drive must be non-zero")
    return dot(x, u) / denominator


def orthogonal_injection(
    state: Iterable[float],
    drive: Iterable[float],
) -> Vector:
    """Remove the state's drive-parallel component, then inject one drive unit.

    For non-zero drive u, the returned state y satisfies
    dot(y, u) / dot(u, u) == 1 up to floating-point error, independent of the
    incoming state's component along u.
    """

    x = _vector(state, "state")
    u = _vector(drive, "drive")
    _same_dimension(x, u)
    denominator = dot(u, u)
    if denominator == 0.0:
        raise ValueError("drive must be non-zero")
    scale = dot(x, u) / denominator
    orthogonal = tuple(value - scale * drive_value for value, drive_value in zip(x, u, strict=True))
    return tuple(value + drive_value for value, drive_value in zip(orthogonal, u, strict=True))
