"""Post-randomization recurrence-selection bias primitives for RQ-005.

Conditioning on recurrence can destroy baseline randomization when the assigned
intervention changes recurrence probability. This module provides a synthetic
known answer only; it does not estimate any trial effect.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LatentRiskStratum:
    name: str
    population_weight: float
    recurrence_control: float
    recurrence_intervention: float
    post_recurrence_survival: float

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        for field in (
            "population_weight",
            "recurrence_control",
            "recurrence_intervention",
            "post_recurrence_survival",
        ):
            value = getattr(self, field)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be in [0, 1]")


def recurrent_stratum_weights(
    strata: tuple[LatentRiskStratum, ...],
    *,
    intervention: bool,
) -> dict[str, float]:
    """Latent-risk composition among patients selected by recurrence."""
    masses: dict[str, float] = {}
    for stratum in strata:
        recurrence = (
            stratum.recurrence_intervention
            if intervention
            else stratum.recurrence_control
        )
        masses[stratum.name] = stratum.population_weight * recurrence
    total = sum(masses.values())
    if total <= 0:
        raise ValueError("no recurrent probability mass")
    return {name: mass / total for name, mass in masses.items()}


def observed_post_recurrence_survival(
    strata: tuple[LatentRiskStratum, ...],
    *,
    intervention: bool,
) -> float:
    """Observed survival among the post-randomization recurrent subset."""
    weights = recurrent_stratum_weights(strata, intervention=intervention)
    survival = {stratum.name: stratum.post_recurrence_survival for stratum in strata}
    return sum(weights[name] * survival[name] for name in weights)


def selection_bias_fixture() -> tuple[LatentRiskStratum, LatentRiskStratum]:
    """No direct post-recurrence effect, but selected recurrent groups differ.

    The intervention reduces recurrence especially strongly in the latent
    high-risk stratum. Post-recurrence survival is determined only by latent
    risk, with no intervention term. Conditioning on recurrence therefore makes
    recurrent intervention patients look better even though the intervention
    has zero direct post-recurrence effect in this fixture.
    """
    low = LatentRiskStratum(
        name="low",
        population_weight=0.5,
        recurrence_control=0.2,
        recurrence_intervention=0.2,
        post_recurrence_survival=0.8,
    )
    high = LatentRiskStratum(
        name="high",
        population_weight=0.5,
        recurrence_control=0.8,
        recurrence_intervention=0.2,
        post_recurrence_survival=0.2,
    )
    return low, high
