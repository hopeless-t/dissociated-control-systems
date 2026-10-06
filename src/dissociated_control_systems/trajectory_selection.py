"""Small deterministic helpers for longitudinal trajectory-selection bias.

Complete-case analysis can create an apparent early-state/late-output relation
when retention depends on post-baseline biology.  This module is a synthetic
counterexample generator, not an estimator for real missing data.
"""

from __future__ import annotations

from typing import Iterable

from .temporal_linkage import population_covariance


def retained_pairs(
    early: Iterable[float],
    late: Iterable[float],
    retained: Iterable[bool],
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    early_t = tuple(float(v) for v in early)
    late_t = tuple(float(v) for v in late)
    retained_t = tuple(bool(v) for v in retained)
    if not (len(early_t) == len(late_t) == len(retained_t)):
        raise ValueError("early, late and retained must have equal length")
    selected = [
        (e, h)
        for e, h, keep in zip(early_t, late_t, retained_t)
        if keep
    ]
    if not selected:
        raise ValueError("at least one trajectory must be retained")
    return (
        tuple(pair[0] for pair in selected),
        tuple(pair[1] for pair in selected),
    )


def complete_case_covariance(
    early: Iterable[float],
    late: Iterable[float],
    retained: Iterable[bool],
) -> float:
    selected_early, selected_late = retained_pairs(early, late, retained)
    return population_covariance(selected_early, selected_late)


def attrition_shift(
    early: Iterable[float],
    late: Iterable[float],
    retained: Iterable[bool],
) -> float:
    early_t = tuple(float(v) for v in early)
    late_t = tuple(float(v) for v in late)
    full = population_covariance(early_t, late_t)
    selected = complete_case_covariance(early_t, late_t, retained)
    return selected - full
