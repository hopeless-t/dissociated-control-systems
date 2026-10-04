"""Minimum sufficient checkpoint sets for DCS projection/control paths.

A checkpoint is retained only if it covers at least one declared catastrophic
failure mode that would otherwise remain unguarded. The exact solver is intended
for small research contracts, not large operational graphs.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Mapping


@dataclass(frozen=True)
class Checkpoint:
    name: str
    covers: frozenset[str]
    cost: float = 1.0

    def __post_init__(self) -> None:
        if self.cost <= 0:
            raise ValueError("checkpoint cost must be > 0")


def covered_failures(checkpoints: Iterable[Checkpoint]) -> frozenset[str]:
    covered: set[str] = set()
    for checkpoint in checkpoints:
        covered.update(checkpoint.covers)
    return frozenset(covered)


def is_sufficient(
    checkpoints: Iterable[Checkpoint],
    required_failures: Iterable[str],
) -> bool:
    required = frozenset(required_failures)
    return required <= covered_failures(checkpoints)


def minimum_sufficient_checkpoint_sets(
    checkpoints: Iterable[Checkpoint],
    required_failures: Iterable[str],
) -> tuple[tuple[str, ...], ...]:
    """Return every minimum-cardinality checkpoint set covering all failures."""
    cps = tuple(checkpoints)
    required = frozenset(required_failures)

    if not required:
        return ((),)

    if not is_sufficient(cps, required):
        return ()

    solutions: list[tuple[str, ...]] = []
    for size in range(1, len(cps) + 1):
        for chosen in combinations(cps, size):
            if is_sufficient(chosen, required):
                solutions.append(tuple(cp.name for cp in chosen))
        if solutions:
            return tuple(sorted(solutions))

    return ()


def mandatory_checkpoints(
    minimum_sets: Iterable[Iterable[str]],
) -> frozenset[str]:
    """Checkpoints present in every minimum sufficient solution."""
    sets = [frozenset(x) for x in minimum_sets]
    if not sets:
        return frozenset()
    result = sets[0]
    for item in sets[1:]:
        result = result.intersection(item)
    return frozenset(result)


def removable_checkpoints(
    checkpoints: Iterable[Checkpoint],
    required_failures: Iterable[str],
) -> frozenset[str]:
    """Checkpoints whose individual deletion preserves total coverage."""
    cps = tuple(checkpoints)
    required = frozenset(required_failures)
    removable: set[str] = set()

    for i, cp in enumerate(cps):
        remaining = cps[:i] + cps[i + 1 :]
        if is_sufficient(remaining, required):
            removable.add(cp.name)

    return frozenset(removable)


def failure_exposure_after_removal(
    checkpoints: Iterable[Checkpoint],
    required_failures: Iterable[str],
) -> Mapping[str, frozenset[str]]:
    """For each checkpoint, list catastrophic failures exposed if it is removed."""
    cps = tuple(checkpoints)
    required = frozenset(required_failures)
    exposure: dict[str, frozenset[str]] = {}

    for i, cp in enumerate(cps):
        remaining = cps[:i] + cps[i + 1 :]
        missing = required - covered_failures(remaining)
        exposure[cp.name] = frozenset(missing)

    return exposure


def minimum_cost_sufficient_checkpoint_sets(
    checkpoints: Iterable[Checkpoint],
    required_failures: Iterable[str],
    *,
    tolerance: float = 1e-12,
) -> tuple[tuple[str, ...], ...]:
    """Return all lowest-cost sufficient checkpoint sets.

    Cardinality alone cannot distinguish interchangeable implementations with
    different presentation/measurement cost.
    """
    cps = tuple(checkpoints)
    required = frozenset(required_failures)
    if not required:
        return ((),)
    if not is_sufficient(cps, required):
        return ()

    best_cost: float | None = None
    solutions: list[tuple[str, ...]] = []

    for size in range(1, len(cps) + 1):
        for chosen in combinations(cps, size):
            if not is_sufficient(chosen, required):
                continue
            cost = sum(cp.cost for cp in chosen)
            names = tuple(sorted(cp.name for cp in chosen))
            if best_cost is None or cost < best_cost - tolerance:
                best_cost = cost
                solutions = [names]
            elif abs(cost - best_cost) <= tolerance:
                solutions.append(names)

    return tuple(sorted(set(solutions)))


def dominated_checkpoints(
    checkpoints: Iterable[Checkpoint],
) -> frozenset[str]:
    """Return checkpoints weakly dominated by another single checkpoint.

    c_i is dominated if another checkpoint covers every failure c_i covers at
    no greater cost, with at least one strict improvement in coverage or cost.
    """
    cps = tuple(checkpoints)
    dominated: set[str] = set()
    for i, left in enumerate(cps):
        for j, right in enumerate(cps):
            if i == j:
                continue
            coverage_dominates = left.covers <= right.covers
            cost_dominates = right.cost <= left.cost
            strict = right.covers != left.covers or right.cost < left.cost
            if coverage_dominates and cost_dominates and strict:
                dominated.add(left.name)
                break
    return frozenset(dominated)
