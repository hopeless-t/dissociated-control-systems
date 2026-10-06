"""Path-aware bridge accounting for META-A reconciliation.

Changing a trial set, effect extraction rule, and meta-analytic model can alter
weights and heterogeneity jointly. Sequential contributions are therefore not
assumed to be unique. Exact Shapley averaging is provided for small factor sets
as an accounting device, not as a causal attribution method.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from itertools import permutations
from math import isfinite
from typing import TypeVar


T = TypeVar("T")
Evaluator = Callable[[Mapping[str, T]], float]


def _score(evaluator: Evaluator[T], state: Mapping[str, T]) -> float:
    value = evaluator(state)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("bridge evaluator must return a numeric scalar")
    value = float(value)
    if not isfinite(value):
        raise ValueError("bridge evaluator must return a finite scalar")
    return value


def _validate(
    baseline: Mapping[str, T], target: Mapping[str, T], factors: Sequence[str]
) -> tuple[str, ...]:
    names = tuple(factors)
    if not names:
        raise ValueError("at least one bridge factor is required")
    if len(names) != len(set(names)):
        raise ValueError("bridge factors must be unique")
    for name in names:
        if name not in baseline or name not in target:
            raise KeyError(name)
    return names


def sequential_bridge(
    baseline: Mapping[str, T],
    target: Mapping[str, T],
    factors: Sequence[str],
    evaluator: Evaluator[T],
) -> dict[str, float]:
    """Attribute change along one declared factor-replacement path."""
    names = _validate(baseline, target, factors)
    state = dict(baseline)
    previous = _score(evaluator, state)
    contributions: dict[str, float] = {}

    for name in names:
        state[name] = target[name]
        current = _score(evaluator, state)
        contributions[name] = current - previous
        previous = current

    return contributions


def exact_shapley_bridge(
    baseline: Mapping[str, T],
    target: Mapping[str, T],
    factors: Sequence[str],
    evaluator: Evaluator[T],
    *,
    max_factors: int = 8,
) -> dict[str, float]:
    """Average sequential bridge contributions over every factor order.

    The factor cap prevents accidental factorial explosion. This decomposition
    allocates interactions symmetrically but remains descriptive accounting.
    """
    names = _validate(baseline, target, factors)
    if isinstance(max_factors, bool) or not isinstance(max_factors, int):
        raise TypeError("max_factors must be an integer")
    if max_factors <= 0:
        raise ValueError("max_factors must be positive")
    if len(names) > max_factors:
        raise ValueError("too many factors for exact Shapley enumeration")

    totals = {name: 0.0 for name in names}
    n_paths = 0
    for order in permutations(names):
        path = sequential_bridge(baseline, target, order, evaluator)
        for name, value in path.items():
            totals[name] += value
        n_paths += 1

    return {name: totals[name] / n_paths for name in names}
