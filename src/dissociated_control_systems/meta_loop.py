"""Deterministic primitives for meta-adaptive closed improvement loops.

These helpers model loop-level efficiency and active observation policy.
They are generic control primitives, not a claim about any biological mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


def _nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


def _probability(value: float, name: str) -> float:
    value = _nonnegative(value, name)
    if value > 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


@dataclass(frozen=True)
class ObservationOption:
    """One candidate sensor action."""

    name: str
    information_gain: float
    cost: float

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        object.__setattr__(
            self, "information_gain", _nonnegative(self.information_gain, "information_gain")
        )
        object.__setattr__(self, "cost", _nonnegative(self.cost, "cost"))
        if self.cost == 0.0:
            raise ValueError("cost must be greater than zero")

    @property
    def information_per_cost(self) -> float:
        return self.information_gain / self.cost


def choose_observation(options: Iterable[ObservationOption]) -> ObservationOption:
    """Select the observation with highest expected information per unit cost.

    Ties are resolved by lower cost, then lexical name for deterministic replay.
    """

    candidates = tuple(options)
    if not candidates:
        raise ValueError("at least one observation option is required")
    return max(
        candidates,
        key=lambda option: (
            option.information_per_cost,
            -option.cost,
            tuple(-ord(ch) for ch in option.name),
        ),
    )


def expected_cascade_cost(
    tier_costs: Iterable[float],
    conditional_stop_probabilities: Iterable[float],
) -> float:
    """Expected cost of a sequential coarse-to-fine observation cascade.

    For costs c0,c1,... and conditional stop probabilities p0,p1,...,
    the expected cost is:

        c0 + (1-p0)c1 + (1-p0)(1-p1)c2 + ...

    There must be exactly one fewer stop probability than costs.
    """

    costs = tuple(_nonnegative(v, f"tier_costs[{i}]") for i, v in enumerate(tier_costs))
    stops = tuple(
        _probability(v, f"conditional_stop_probabilities[{i}]")
        for i, v in enumerate(conditional_stop_probabilities)
    )
    if not costs:
        raise ValueError("at least one tier cost is required")
    if len(stops) != len(costs) - 1:
        raise ValueError("expected exactly one fewer stop probability than tier costs")

    expected = costs[0]
    survival = 1.0
    for index, stop_probability in enumerate(stops):
        survival *= 1.0 - stop_probability
        expected += survival * costs[index + 1]
    return expected


def two_tier_break_even_stop_probability(coarse_cost: float, fine_cost: float) -> float:
    """Minimum coarse-stage stop rate needed to beat unconditional fine sensing."""

    coarse = _nonnegative(coarse_cost, "coarse_cost")
    fine = _nonnegative(fine_cost, "fine_cost")
    if fine == 0.0:
        raise ValueError("fine_cost must be greater than zero")
    if coarse >= fine:
        return 1.0
    return coarse / fine


def learning_velocity(
    learning_gain: float,
    *,
    render_cost: float,
    observation_cost: float,
    decision_cost: float,
) -> float:
    """Useful learning gain per unit total loop cost."""

    gain = _nonnegative(learning_gain, "learning_gain")
    total = (
        _nonnegative(render_cost, "render_cost")
        + _nonnegative(observation_cost, "observation_cost")
        + _nonnegative(decision_cost, "decision_cost")
    )
    if total == 0.0:
        raise ValueError("total loop cost must be greater than zero")
    return gain / total


def effective_pressure(
    *,
    issue_count: int,
    negative_interaction_strengths: Iterable[float],
    intervention_magnitudes: Iterable[float],
    execution_cost: float,
    issue_weight: float = 1.0,
    interaction_weight: float = 1.0,
    magnitude_weight: float = 1.0,
    execution_weight: float = 1.0,
) -> float:
    """State-aware pressure proxy for a multi-critic improvement step.

    This intentionally replaces raw issue count with a richer proxy:

      P_eff =
        alpha * |S|
        + beta * sum(negative interactions)
        + gamma * sum(intervention magnitude^2)
        + eta * execution cost
    """

    if isinstance(issue_count, bool) or not isinstance(issue_count, int):
        raise TypeError("issue_count must be an integer")
    if issue_count < 0:
        raise ValueError("issue_count must be non-negative")

    interactions = tuple(
        _nonnegative(v, f"negative_interaction_strengths[{i}]")
        for i, v in enumerate(negative_interaction_strengths)
    )
    magnitudes = tuple(
        _nonnegative(v, f"intervention_magnitudes[{i}]")
        for i, v in enumerate(intervention_magnitudes)
    )
    weights = {
        "issue_weight": _nonnegative(issue_weight, "issue_weight"),
        "interaction_weight": _nonnegative(interaction_weight, "interaction_weight"),
        "magnitude_weight": _nonnegative(magnitude_weight, "magnitude_weight"),
        "execution_weight": _nonnegative(execution_weight, "execution_weight"),
    }
    execution = _nonnegative(execution_cost, "execution_cost")

    return (
        weights["issue_weight"] * issue_count
        + weights["interaction_weight"] * sum(interactions)
        + weights["magnitude_weight"] * sum(value * value for value in magnitudes)
        + weights["execution_weight"] * execution
    )
