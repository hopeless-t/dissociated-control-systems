"""Last-responsible-moment placement for mandatory checkpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Hazard:
    name: str
    first_unsafe_step: int


@dataclass(frozen=True)
class Gate:
    name: str
    covers: frozenset[str]
    presentation_cost_per_step: float = 1.0

    def __post_init__(self) -> None:
        if self.presentation_cost_per_step < 0:
            raise ValueError("presentation_cost_per_step must be >= 0")


def latest_safe_position(
    gate: Gate,
    hazards: Iterable[Hazard],
) -> int | None:
    """Latest position that occurs before every covered hazard activates."""
    hazard_map = {hazard.name: hazard for hazard in hazards}
    covered = [
        hazard_map[name]
        for name in gate.covers
        if name in hazard_map
    ]
    if not covered:
        return None
    return min(hazard.first_unsafe_step for hazard in covered)


def placement_is_safe(
    gate: Gate,
    hazards: Iterable[Hazard],
    position: int,
) -> bool:
    latest = latest_safe_position(gate, hazards)
    if latest is None:
        return True
    return position <= latest


def premature_exposure_cost(
    gate: Gate,
    hazards: Iterable[Hazard],
    position: int,
) -> float:
    """Cost of showing/enforcing a gate earlier than necessary.

    Unsafe late placement has infinite cost.
    """
    latest = latest_safe_position(gate, hazards)
    if latest is None:
        return 0.0
    if position > latest:
        return float("inf")
    return gate.presentation_cost_per_step * (latest - position)


def optimal_position(
    gate: Gate,
    hazards: Iterable[Hazard],
) -> int | None:
    """For the declared cost, the optimum is the latest safe position."""
    return latest_safe_position(gate, hazards)
