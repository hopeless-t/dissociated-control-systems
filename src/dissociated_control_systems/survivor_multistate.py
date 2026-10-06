"""Multi-state survivor trajectory primitives for RQ-005.

The observed long-survival endpoint is decomposed into transition paths.
These helpers validate arithmetic and state typing only; they are not a
clinical prognosis model and do not identify biological mechanisms.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SurvivorTrajectory(str, Enum):
    NO_RECORDED_RECURRENCE = "no_recorded_recurrence"
    LATE_RECURRENCE = "late_recurrence"
    EARLY_RECURRENCE_DURABLE_CONTROL = "early_recurrence_durable_control"
    EARLY_RECURRENCE_RAPID_FAILURE = "early_recurrence_rapid_failure"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class ObservedTrajectory:
    overall_survival_months: float
    recurrence_recorded: bool
    recurrence_months: float | None = None
    disease_death: bool = False

    def __post_init__(self) -> None:
        if self.overall_survival_months < 0:
            raise ValueError("overall_survival_months must be non-negative")
        if self.recurrence_recorded:
            if self.recurrence_months is None:
                raise ValueError("recurrence_months required when recurrence is recorded")
            if self.recurrence_months < 0:
                raise ValueError("recurrence_months must be non-negative")
            if self.recurrence_months > self.overall_survival_months:
                raise ValueError("recurrence cannot occur after observed survival time")
        elif self.recurrence_months is not None:
            raise ValueError("recurrence_months must be absent when no recurrence is recorded")

    @property
    def post_recurrence_observation_months(self) -> float | None:
        """Observed recurrence-to-death/censor interval, only if recurrence exists."""
        if not self.recurrence_recorded:
            return None
        assert self.recurrence_months is not None
        return self.overall_survival_months - self.recurrence_months


def classify_trajectory(
    observation: ObservedTrajectory,
    *,
    early_recurrence_months: float = 60.0,
    durable_post_recurrence_months: float = 120.0,
) -> SurvivorTrajectory:
    """Classify an observed transition path without assigning mechanism.

    `durable_post_recurrence_months` is a research threshold, not a clinical
    definition. The threshold must be frozen before comparative analyses.
    """
    if early_recurrence_months <= 0 or durable_post_recurrence_months <= 0:
        raise ValueError("thresholds must be positive")

    if not observation.recurrence_recorded:
        return SurvivorTrajectory.NO_RECORDED_RECURRENCE

    recurrence = observation.recurrence_months
    assert recurrence is not None
    post = observation.post_recurrence_observation_months
    assert post is not None

    if recurrence > early_recurrence_months:
        return SurvivorTrajectory.LATE_RECURRENCE
    if post >= durable_post_recurrence_months:
        return SurvivorTrajectory.EARLY_RECURRENCE_DURABLE_CONTROL
    return SurvivorTrajectory.EARLY_RECURRENCE_RAPID_FAILURE


def same_overall_survival_distinct_paths() -> tuple[ObservedTrajectory, ObservedTrajectory]:
    """Known-answer pair: same OS can hide very different transition paths."""
    late = ObservedTrajectory(
        overall_survival_months=180.0,
        recurrence_recorded=True,
        recurrence_months=150.0,
    )
    early = ObservedTrajectory(
        overall_survival_months=180.0,
        recurrence_recorded=True,
        recurrence_months=24.0,
    )
    return late, early
