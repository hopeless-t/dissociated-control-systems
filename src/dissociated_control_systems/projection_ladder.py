"""Projection-ladder primitives for DCS explanations.

These equations are a synthetic cognitive-friction surrogate, not a model of
human neurobiology.

A direct jump across semantic distance D incurs superlinear jump cost. Adding
more stages reduces local jump size but adds per-stage overhead. The resulting
trade-off has a finite optimum.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class ProjectionPlan:
    transitions: int
    total_distance: float
    jump_cost: float
    stage_overhead: float
    total_cost: float
    max_gap: float


@dataclass(frozen=True)
class LocalProjectionSpan:
    distance: float
    difficulty: float = 1.0


def homogeneous_projection_cost(
    total_distance: float,
    transitions: int,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> ProjectionPlan:
    """Cost for equally spaced transitions across one semantic distance.

    J(n) = alpha * D^2 / n + beta * n

    alpha: penalty for large semantic jumps.
    beta: overhead paid for every explanatory transition.
    """
    if total_distance < 0:
        raise ValueError("total_distance must be >= 0")
    if transitions < 1:
        raise ValueError("transitions must be >= 1")
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be > 0")

    jump_cost = alpha * total_distance * total_distance / transitions
    stage_overhead = beta * transitions
    return ProjectionPlan(
        transitions=transitions,
        total_distance=total_distance,
        jump_cost=jump_cost,
        stage_overhead=stage_overhead,
        total_cost=jump_cost + stage_overhead,
        max_gap=total_distance / transitions,
    )


def continuous_optimum_transitions(
    total_distance: float,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> float:
    """Continuous optimum n* = D * sqrt(alpha / beta)."""
    if total_distance < 0:
        raise ValueError("total_distance must be >= 0")
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be > 0")
    return total_distance * math.sqrt(alpha / beta)


def optimal_integer_projection(
    total_distance: float,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> ProjectionPlan:
    """Return the globally optimal positive integer transition count."""
    n_star = continuous_optimum_transitions(
        total_distance,
        alpha=alpha,
        beta=beta,
    )
    candidates = {
        1,
        max(1, math.floor(n_star)),
        max(1, math.ceil(n_star)),
    }
    return min(
        (
            homogeneous_projection_cost(
                total_distance,
                n,
                alpha=alpha,
                beta=beta,
            )
            for n in candidates
        ),
        key=lambda plan: (plan.total_cost, plan.transitions),
    )


def optimal_local_subdivisions(
    spans: Iterable[LocalProjectionSpan],
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> tuple[int, ...]:
    """Allocate more explanatory steps where distance/difficulty is larger.

    For independent span j:

        J_j(n_j) = alpha * difficulty_j * distance_j^2 / n_j + beta * n_j

    so the continuous optimum is:

        n_j* = distance_j * sqrt(alpha * difficulty_j / beta)
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be > 0")

    allocations: list[int] = []
    for span in spans:
        if span.distance < 0:
            raise ValueError("span distance must be >= 0")
        if span.difficulty <= 0:
            raise ValueError("span difficulty must be > 0")

        n_star = span.distance * math.sqrt(
            alpha * span.difficulty / beta
        )
        candidates = {
            1,
            max(1, math.floor(n_star)),
            max(1, math.ceil(n_star)),
        }

        def local_cost(n: int) -> float:
            return (
                alpha * span.difficulty * span.distance * span.distance / n
                + beta * n
            )

        allocations.append(
            min(candidates, key=lambda n: (local_cost(n), n))
        )

    return tuple(allocations)


def weighted_ladder_cost(
    spans: Iterable[LocalProjectionSpan],
    subdivisions: Iterable[int],
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
) -> float:
    """Evaluate an adaptive projection ladder."""
    spans_t = tuple(spans)
    n_t = tuple(subdivisions)
    if len(spans_t) != len(n_t):
        raise ValueError("spans/subdivisions length mismatch")

    total = 0.0
    for span, n in zip(spans_t, n_t):
        if n < 1:
            raise ValueError("every span needs >= 1 transition")
        total += (
            alpha * span.difficulty * span.distance * span.distance / n
            + beta * n
        )
    return total
