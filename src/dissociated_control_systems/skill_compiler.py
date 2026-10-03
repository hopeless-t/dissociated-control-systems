"""Reusable skill-capsule primitives for meta-adaptive control research."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import FrozenSet, Iterable


def _nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


@dataclass(frozen=True)
class CompiledSkill:
    """A bounded reusable policy compiled from previously successful episodes."""

    name: str
    required_tags: FrozenSet[str]
    replay_cost: float
    discovery_cost: float
    verification_cost: float
    confidence: float

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.required_tags, frozenset):
            raise TypeError("required_tags must be a frozenset")
        if not all(isinstance(tag, str) and tag for tag in self.required_tags):
            raise ValueError("required_tags must contain non-empty strings")
        object.__setattr__(self, "replay_cost", _nonnegative(self.replay_cost, "replay_cost"))
        object.__setattr__(
            self, "discovery_cost", _nonnegative(self.discovery_cost, "discovery_cost")
        )
        object.__setattr__(
            self, "verification_cost", _nonnegative(self.verification_cost, "verification_cost")
        )
        confidence = _nonnegative(self.confidence, "confidence")
        if confidence > 1.0:
            raise ValueError("confidence must be in [0, 1]")
        object.__setattr__(self, "confidence", confidence)

    def is_applicable(self, context_tags: Iterable[str]) -> bool:
        context = frozenset(context_tags)
        return self.required_tags.issubset(context)

    @property
    def total_replay_cost(self) -> float:
        return self.replay_cost + self.verification_cost

    @property
    def one_replay_savings(self) -> float:
        return max(0.0, self.discovery_cost - self.total_replay_cost)

    def amortized_cost_per_use(self, compile_cost: float, uses: int) -> float:
        compile_cost = _nonnegative(compile_cost, "compile_cost")
        if isinstance(uses, bool) or not isinstance(uses, int):
            raise TypeError("uses must be an integer")
        if uses <= 0:
            raise ValueError("uses must be positive")
        return self.total_replay_cost + compile_cost / uses


def select_compiled_skill(
    skills: Iterable[CompiledSkill],
    context_tags: Iterable[str],
) -> CompiledSkill | None:
    """Select the highest-confidence applicable skill, preferring cheaper replay."""

    context = frozenset(context_tags)
    applicable = tuple(skill for skill in skills if skill.is_applicable(context))
    if not applicable:
        return None
    return max(
        applicable,
        key=lambda skill: (
            skill.confidence,
            skill.one_replay_savings,
            -skill.total_replay_cost,
            skill.name,
        ),
    )


def replay_is_economical(
    skill: CompiledSkill,
    *,
    compile_cost: float,
    expected_uses: int,
) -> bool:
    """Return whether amortized replay is cheaper than repeated rediscovery."""

    return skill.amortized_cost_per_use(compile_cost, expected_uses) < skill.discovery_cost
