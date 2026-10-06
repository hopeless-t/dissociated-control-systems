"""Dependency-free observation-selection primitives for DCS research.

These helpers are intentionally domain-agnostic. They support synthetic panel
selection experiments and are not clinical decision rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Iterable


@dataclass(frozen=True)
class ObservationCandidate:
    name: str
    burden: float
    delay: float = 0.0
    success_probability: float = 1.0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")
        if self.burden <= 0:
            raise ValueError("burden must be > 0")
        if self.delay < 0:
            raise ValueError("delay must be >= 0")
        if not 0.0 <= self.success_probability <= 1.0:
            raise ValueError("success_probability must be in [0, 1]")


def panel_burden(panel: Iterable[ObservationCandidate]) -> float:
    return sum(item.burden for item in panel)


def panel_fits_burden_ceiling(
    panel: Iterable[ObservationCandidate],
    burden_ceiling: float,
) -> bool:
    """Return whether the declared observation panel fits a patient's ceiling."""

    if burden_ceiling < 0:
        raise ValueError("burden_ceiling must be >= 0")
    return panel_burden(panel) <= burden_ceiling


def available_before_deadline(
    candidates: Iterable[ObservationCandidate],
    current_time: float,
    decision_deadline: float,
) -> tuple[ObservationCandidate, ...]:
    """Return observations whose deterministic results can arrive by deadline."""

    if current_time < 0:
        raise ValueError("current_time must be >= 0")
    if decision_deadline < current_time:
        return ()
    return tuple(
        item
        for item in candidates
        if current_time + item.delay <= decision_deadline
    )


def sequential_completion_time(panel: Iterable[ObservationCandidate]) -> float:
    """Completion time when observations are acquired strictly one after another."""

    return sum(item.delay for item in panel)


def parallel_completion_time(panel: Iterable[ObservationCandidate]) -> float:
    """Completion time when all observations are launched at the same time."""

    delays = tuple(item.delay for item in panel)
    return max(delays, default=0.0)


def expected_successful_value(
    candidate: ObservationCandidate,
    information_value: float,
) -> float:
    """Reliability-adjust a synthetic information value.

    This is a deliberately simple expectation primitive. It does not assume
    that failed observations are missing at random, and should not be used as a
    substitute for an explicit failure model when missingness is informative.
    """

    return float(information_value) * candidate.success_probability


def _candidate_panels(
    candidates: tuple[ObservationCandidate, ...],
    burden_budget: float,
):
    if burden_budget <= 0:
        raise ValueError("burden_budget must be > 0")
    for size in range(1, len(candidates) + 1):
        for group in combinations(candidates, size):
            burden = panel_burden(group)
            if burden <= burden_budget:
                yield group, burden


def exhaustive_best_panel(
    candidates: tuple[ObservationCandidate, ...],
    value_fn: Callable[[tuple[str, ...]], float],
    burden_budget: float,
) -> tuple[str, ...]:
    """Return the highest-value non-empty panel within a burden budget.

    Ties prefer lower burden and then lexical order for deterministic tests.
    """

    best: tuple[str, ...] = ()
    best_value = float("-inf")
    best_burden = float("inf")

    for group, burden in _candidate_panels(candidates, burden_budget):
        names = tuple(item.name for item in group)
        value = float(value_fn(names))
        if (
            value > best_value
            or (value == best_value and burden < best_burden)
            or (value == best_value and burden == best_burden and names < best)
        ):
            best = names
            best_value = value
            best_burden = burden

    return best


def robust_best_panel(
    candidates: tuple[ObservationCandidate, ...],
    world_value_fns: tuple[Callable[[tuple[str, ...]], float], ...],
    burden_budget: float,
) -> tuple[str, ...]:
    """Choose a panel maximizing its worst-case value across declared worlds.

    This is a small exact minimax-style research primitive. It only protects
    against the alternative worlds supplied by the caller; omitted worlds are
    not magically covered.
    """

    if not world_value_fns:
        raise ValueError("at least one world_value_fn is required")

    best: tuple[str, ...] = ()
    best_worst = float("-inf")
    best_burden = float("inf")

    for group, burden in _candidate_panels(candidates, burden_budget):
        names = tuple(item.name for item in group)
        worst = min(float(value_fn(names)) for value_fn in world_value_fns)
        if (
            worst > best_worst
            or (worst == best_worst and burden < best_burden)
            or (worst == best_worst and burden == best_burden and names < best)
        ):
            best = names
            best_worst = worst
            best_burden = burden

    return best


def greedy_information_per_burden(
    candidates: tuple[ObservationCandidate, ...],
    value_fn: Callable[[tuple[str, ...]], float],
    burden_budget: float,
) -> tuple[str, ...]:
    """Simple greedy baseline using marginal value per incremental burden.

    This routine is deliberately kept as a falsifiable baseline. It is not
    guaranteed optimal when observations have complementarity / synergy.
    """

    if burden_budget <= 0:
        raise ValueError("burden_budget must be > 0")

    chosen: list[ObservationCandidate] = []
    remaining = list(candidates)

    while remaining:
        current_names = tuple(item.name for item in chosen)
        current_value = float(value_fn(current_names))
        feasible = [
            item
            for item in remaining
            if panel_burden((*chosen, item)) <= burden_budget
        ]
        if not feasible:
            break

        scored: list[tuple[float, float, str, ObservationCandidate]] = []
        for item in feasible:
            next_names = tuple(candidate.name for candidate in (*chosen, item))
            gain = float(value_fn(next_names)) - current_value
            ratio = gain / item.burden
            scored.append((ratio, gain, item.name, item))

        scored.sort(key=lambda row: (-row[0], -row[1], row[2]))
        ratio, gain, _, selected = scored[0]
        if gain <= 0:
            break
        chosen.append(selected)
        remaining.remove(selected)

    return tuple(item.name for item in chosen)
