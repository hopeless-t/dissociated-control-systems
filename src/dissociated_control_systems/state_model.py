"""Deterministic primitives for the VAL-001 synthetic state model."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import floor
from typing import Iterable


def _bounded(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


@dataclass(frozen=True)
class SubsystemState:
    motor: float
    procedural: float
    executive: float
    memory: float

    def __post_init__(self) -> None:
        for name in ("motor", "procedural", "executive", "memory"):
            object.__setattr__(self, name, _bounded(getattr(self, name), name))

    @property
    def values(self) -> tuple[float, float, float, float]:
        return (self.motor, self.procedural, self.executive, self.memory)


def coarse_observation(state: SubsystemState) -> dict[str, bool]:
    return {"complex_action": state.motor >= 0.5 and state.procedural >= 0.5}


def rich_observation(state: SubsystemState) -> dict[str, bool]:
    return {
        "complex_action": state.motor >= 0.5 and state.procedural >= 0.5,
        "executive_available": state.executive >= 0.5,
        "memory_encoding_available": state.memory >= 0.5,
    }


def dissociation_index(values: Iterable[float]) -> float:
    bounded = tuple(_bounded(v, f"state[{i}]") for i, v in enumerate(values))
    n = len(bounded)
    if n < 2:
        return 0.0
    denominator = floor((n * n) / 4)
    numerator = sum(
        abs(bounded[i] - bounded[j])
        for i in range(n)
        for j in range(i + 1, n)
    )
    result = numerator / denominator
    if not 0.0 <= result <= 1.0:
        raise AssertionError("normalized dissociation index escaped [0, 1]")
    return result


def expressed_capability(
    capability: Iterable[float],
    accessibility: Iterable[float],
) -> tuple[float, ...]:
    c = tuple(_bounded(v, f"capability[{i}]") for i, v in enumerate(capability))
    g = tuple(_bounded(v, f"accessibility[{i}]") for i, v in enumerate(accessibility))
    if len(c) != len(g):
        raise ValueError("capability and accessibility must have the same length")
    return tuple(ci * gi for ci, gi in zip(c, g, strict=True))


def _binary_states() -> tuple[SubsystemState, ...]:
    return tuple(SubsystemState(*bits) for bits in product((0.0, 1.0), repeat=4))


def equivalence_class(target: dict[str, bool]) -> tuple[SubsystemState, ...]:
    if set(target) != {"complex_action"} or not isinstance(target["complex_action"], bool):
        raise ValueError("target must contain exactly boolean complex_action")
    return tuple(state for state in _binary_states() if coarse_observation(state) == target)
