"""Confounding-by-indication known answers for RQ-005.

This module demonstrates why treatment-category associations in retrospective
survivor data are not treatment effects. It is synthetic arithmetic only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskStratum:
    population_weight: float
    treatment_probability: float
    untreated_survival_probability: float
    treated_survival_probability: float

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")

    @property
    def causal_risk_difference(self) -> float:
        return self.treated_survival_probability - self.untreated_survival_probability


def observational_treated_survival(strata: tuple[RiskStratum, ...]) -> float:
    numerator = sum(
        s.population_weight * s.treatment_probability * s.treated_survival_probability
        for s in strata
    )
    denominator = sum(s.population_weight * s.treatment_probability for s in strata)
    if denominator == 0:
        raise ValueError("no treated observations")
    return numerator / denominator


def observational_untreated_survival(strata: tuple[RiskStratum, ...]) -> float:
    numerator = sum(
        s.population_weight
        * (1.0 - s.treatment_probability)
        * s.untreated_survival_probability
        for s in strata
    )
    denominator = sum(
        s.population_weight * (1.0 - s.treatment_probability) for s in strata
    )
    if denominator == 0:
        raise ValueError("no untreated observations")
    return numerator / denominator


def standardized_causal_risk_difference(strata: tuple[RiskStratum, ...]) -> float:
    total_weight = sum(s.population_weight for s in strata)
    if total_weight <= 0:
        raise ValueError("population weight must be positive")
    return sum(
        s.population_weight * s.causal_risk_difference for s in strata
    ) / total_weight


def confounding_by_indication_fixture() -> tuple[RiskStratum, RiskStratum]:
    """Treatment helps within each stratum but looks harmful when pooled.

    Low-risk patients are rarely treated; high-risk patients are usually
    treated. This creates a Simpson-type reversal in the naive pooled contrast.
    """
    low = RiskStratum(
        population_weight=0.5,
        treatment_probability=0.1,
        untreated_survival_probability=0.90,
        treated_survival_probability=0.95,
    )
    high = RiskStratum(
        population_weight=0.5,
        treatment_probability=0.9,
        untreated_survival_probability=0.20,
        treated_survival_probability=0.40,
    )
    return low, high
