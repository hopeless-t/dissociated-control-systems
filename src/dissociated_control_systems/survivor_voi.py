"""Discrete value-of-information primitives for RQ-005.

These functions rank candidate observations by expected reduction in uncertainty
across declared competing worlds. Likelihoods must come from frozen evidence or
an explicitly synthetic known-answer fixture; this module does not invent them.
"""

from __future__ import annotations

from math import log2
from typing import Mapping


WorldPrior = Mapping[str, float]
ObservationLikelihoods = Mapping[str, Mapping[str, float]]


def _normalize(weights: Mapping[str, float]) -> dict[str, float]:
    if not weights:
        raise ValueError("weights must not be empty")
    if any(value < 0 for value in weights.values()):
        raise ValueError("weights must be non-negative")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must have positive total mass")
    return {key: value / total for key, value in weights.items()}


def entropy_bits(probabilities: Mapping[str, float]) -> float:
    """Shannon entropy in bits after normalizing non-negative weights."""
    p = _normalize(probabilities)
    return -sum(value * log2(value) for value in p.values() if value > 0)


def expected_posterior_entropy_bits(
    prior: WorldPrior,
    likelihoods: ObservationLikelihoods,
) -> float:
    """Expected entropy after observing one categorical measurement.

    `likelihoods[outcome][world]` is P(outcome | world). For every world, the
    likelihood across outcomes must sum to one.
    """
    p_world = _normalize(prior)
    worlds = set(p_world)
    if not likelihoods:
        raise ValueError("likelihoods must not be empty")

    for outcome, row in likelihoods.items():
        if set(row) != worlds:
            raise ValueError(f"outcome {outcome!r} must define every world")
        if any(value < 0 or value > 1 for value in row.values()):
            raise ValueError("likelihoods must lie in [0, 1]")

    for world in worlds:
        total = sum(row[world] for row in likelihoods.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"likelihoods for world {world!r} must sum to one")

    expected = 0.0
    for row in likelihoods.values():
        outcome_probability = sum(p_world[w] * row[w] for w in worlds)
        if outcome_probability <= 0:
            continue
        posterior = {
            w: p_world[w] * row[w] / outcome_probability for w in worlds
        }
        expected += outcome_probability * entropy_bits(posterior)
    return expected


def expected_information_gain_bits(
    prior: WorldPrior,
    likelihoods: ObservationLikelihoods,
) -> float:
    """Expected information gain from one candidate observation."""
    return entropy_bits(prior) - expected_posterior_entropy_bits(prior, likelihoods)


def information_per_cost(
    prior: WorldPrior,
    likelihoods: ObservationLikelihoods,
    *,
    cost: float,
) -> float:
    if cost <= 0:
        raise ValueError("cost must be positive")
    return expected_information_gain_bits(prior, likelihoods) / cost


def rank_observations(
    prior: WorldPrior,
    candidates: Mapping[str, tuple[ObservationLikelihoods, float]],
) -> tuple[tuple[str, float], ...]:
    """Rank named observations by expected information gain per unit cost."""
    scored = [
        (name, information_per_cost(prior, likelihoods, cost=cost))
        for name, (likelihoods, cost) in candidates.items()
    ]
    return tuple(sorted(scored, key=lambda item: (-item[1], item[0])))
