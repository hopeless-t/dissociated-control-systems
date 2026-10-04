"""Representation-granularity primitives for meta-adaptive control research."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


def _finite_nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


@dataclass(frozen=True)
class RepresentationOption:
    """One candidate internal representation for a controller."""

    name: str
    representation_cost: float
    execution_cost: float
    expected_decision_error: float
    semantic_dofs: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        object.__setattr__(
            self,
            "representation_cost",
            _finite_nonnegative(self.representation_cost, "representation_cost"),
        )
        object.__setattr__(
            self,
            "execution_cost",
            _finite_nonnegative(self.execution_cost, "execution_cost"),
        )
        object.__setattr__(
            self,
            "expected_decision_error",
            _finite_nonnegative(self.expected_decision_error, "expected_decision_error"),
        )
        if isinstance(self.semantic_dofs, bool) or not isinstance(self.semantic_dofs, int):
            raise TypeError("semantic_dofs must be an integer")
        if self.semantic_dofs < 0:
            raise ValueError("semantic_dofs must be non-negative")

    @property
    def total_cost(self) -> float:
        return self.representation_cost + self.execution_cost


def choose_minimal_sufficient_representation(
    options: Iterable[RepresentationOption],
    *,
    max_expected_error: float,
) -> RepresentationOption:
    """Choose the cheapest representation that satisfies the error ceiling.

    Semantic degree count is a descriptive state variable, not a cost proxy.
    A representation with fewer objects can still expose more useful semantics.
    """

    max_error = _finite_nonnegative(max_expected_error, "max_expected_error")
    candidates = tuple(option for option in options if option.expected_decision_error <= max_error)
    if not candidates:
        raise ValueError("no representation satisfies the expected-error ceiling")
    return min(
        candidates,
        key=lambda option: (
            option.total_cost,
            option.expected_decision_error,
            -option.semantic_dofs,
            option.name,
        ),
    )


def should_expand_representation(
    *,
    prediction_residual: float,
    residual_threshold: float,
    repeated_failure_count: int,
    repeated_failure_threshold: int = 2,
) -> bool:
    """Return whether a latent representation should be expanded."""

    residual = _finite_nonnegative(prediction_residual, "prediction_residual")
    threshold = _finite_nonnegative(residual_threshold, "residual_threshold")
    if isinstance(repeated_failure_count, bool) or not isinstance(repeated_failure_count, int):
        raise TypeError("repeated_failure_count must be an integer")
    if isinstance(repeated_failure_threshold, bool) or not isinstance(repeated_failure_threshold, int):
        raise TypeError("repeated_failure_threshold must be an integer")
    if repeated_failure_count < 0 or repeated_failure_threshold < 1:
        raise ValueError("failure counts must be non-negative and threshold must be positive")
    return residual > threshold or repeated_failure_count >= repeated_failure_threshold
