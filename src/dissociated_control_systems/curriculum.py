"""Curriculum-selection primitives for meta-meta adaptive control research."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, FrozenSet


def _nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


@dataclass(frozen=True)
class CurriculumTask:
    """A candidate training task selected for information gain rather than repetition."""

    name: str
    information_gain: float
    gap_coverage: float
    transfer_value: float
    redundancy: float
    execution_cost: float
    observation_cost: float
    integration_cost: float
    tags: FrozenSet[str] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        for field in (
            "information_gain",
            "gap_coverage",
            "transfer_value",
            "redundancy",
            "execution_cost",
            "observation_cost",
            "integration_cost",
        ):
            object.__setattr__(self, field, _nonnegative(getattr(self, field), field))
        if not isinstance(self.tags, frozenset):
            raise TypeError("tags must be a frozenset")

    @property
    def total_cost(self) -> float:
        return self.execution_cost + self.observation_cost + self.integration_cost

    def score(
        self,
        *,
        gap_weight: float = 1.0,
        transfer_weight: float = 1.0,
        redundancy_weight: float = 1.0,
        epsilon: float = 1e-9,
    ) -> float:
        gap_weight = _nonnegative(gap_weight, "gap_weight")
        transfer_weight = _nonnegative(transfer_weight, "transfer_weight")
        redundancy_weight = _nonnegative(redundancy_weight, "redundancy_weight")
        epsilon = _nonnegative(epsilon, "epsilon")
        if epsilon == 0.0 and self.total_cost == 0.0:
            raise ValueError("epsilon must be positive when total cost is zero")
        numerator = (
            self.information_gain
            + gap_weight * self.gap_coverage
            + transfer_weight * self.transfer_value
            - redundancy_weight * self.redundancy
        )
        return numerator / (self.total_cost + epsilon)


def choose_curriculum_task(
    tasks: Iterable[CurriculumTask],
    *,
    gap_weight: float = 1.0,
    transfer_weight: float = 1.0,
    redundancy_weight: float = 1.0,
) -> CurriculumTask:
    """Choose the highest-value next training task.

    Ties prefer lower total cost, then lexical name for deterministic replay.
    """

    candidates = tuple(tasks)
    if not candidates:
        raise ValueError("at least one curriculum task is required")
    return max(
        candidates,
        key=lambda task: (
            task.score(
                gap_weight=gap_weight,
                transfer_weight=transfer_weight,
                redundancy_weight=redundancy_weight,
            ),
            -task.total_cost,
            task.name,
        ),
    )
