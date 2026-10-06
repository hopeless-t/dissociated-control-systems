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

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")
        if self.burden <= 0:
            raise ValueError("burden must be > 0")


def panel_burden(panel: Iterable[ObservationCandidate]) -> float:
    return sum(item.burden for item in panel)


def exhaustive_best_panel(
    candidates: tuple[ObservationCandidate, ...],
    value_fn: Callable[[tuple[str, ...]], float],
    burden_budget: float,
) -> tuple[str, ...]:
    """Return the highest-value non-empty panel within a burden budget.

    Ties prefer lower burden and then lexical order for deterministic tests.
    """

    if burden_budget <= 0:
        raise ValueError("burden_budget must be > 0")

    best: tuple[str, ...] = ()
    best_value = float("-inf")
    best_burden = float("inf")

    for size in range(1, len(candidates) + 1):
        for group in combinations(candidates, size):
            burden = panel_burden(group)
            if burden > burden_budget:
                continue
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
