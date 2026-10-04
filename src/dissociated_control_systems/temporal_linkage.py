"""Synthetic helpers for temporal linkage and ecological ambiguity.

Matching early-state and late-output marginals do not determine their within-unit
association.  This matters when an early assay destroys the follicle and the
later functional readout comes from a different replicate.
"""

from __future__ import annotations

from itertools import permutations
from typing import Iterable


def population_covariance(x: Iterable[float], y: Iterable[float]) -> float:
    xs = tuple(float(v) for v in x)
    ys = tuple(float(v) for v in y)
    if len(xs) != len(ys):
        raise ValueError("x and y must have equal length")
    if not xs:
        raise ValueError("at least one paired observation is required")
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    return sum((a - mean_x) * (b - mean_y) for a, b in zip(xs, ys)) / len(xs)


def possible_covariances_from_unlinked_marginals(
    early: Iterable[float],
    late: Iterable[float],
) -> tuple[float, ...]:
    """Enumerate covariance values compatible with unlinked marginals.

    Intended only for small deterministic counterexamples/tests.
    """
    early_t = tuple(float(v) for v in early)
    late_t = tuple(float(v) for v in late)
    if len(early_t) != len(late_t):
        raise ValueError("early and late marginals must have equal length")
    if len(early_t) > 8:
        raise ValueError("exact permutation enumeration is limited to n <= 8")
    values = {
        round(population_covariance(early_t, permuted), 12)
        for permuted in permutations(late_t)
    }
    return tuple(sorted(values))


def covariance_identified_from_marginals(
    early: Iterable[float],
    late: Iterable[float],
) -> bool:
    return len(possible_covariances_from_unlinked_marginals(early, late)) == 1
