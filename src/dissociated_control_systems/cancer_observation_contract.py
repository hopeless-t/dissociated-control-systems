"""Observation-support primitives for the synthetic DCS cancer twin.

These types model whether a forecast has enough declared observational and
intervention context to permit a high-confidence synthetic result. They are
not clinical decision rules.
"""

from __future__ import annotations

from dataclasses import dataclass


def _nonempty(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty")
    return value


def _nonnegative_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative int")
    return value


@dataclass(frozen=True)
class ObservationRecord:
    modality: str
    observed_at: int
    calibration_id: str
    value: float | None = None
    lower_detection_limit: float | None = None
    censored_below_limit: bool = False

    def __post_init__(self) -> None:
        _nonempty(self.modality, "modality")
        _nonempty(self.calibration_id, "calibration_id")
        _nonnegative_int(self.observed_at, "observed_at")
        if self.value is not None:
            object.__setattr__(self, "value", float(self.value))
        if self.lower_detection_limit is not None:
            limit = float(self.lower_detection_limit)
            if limit < 0.0:
                raise ValueError("lower_detection_limit must be >= 0")
            object.__setattr__(self, "lower_detection_limit", limit)
        if self.censored_below_limit and self.lower_detection_limit is None:
            raise ValueError("censored observation requires lower_detection_limit")
        if self.censored_below_limit and self.value is not None:
            raise ValueError("censored observation must not masquerade as an exact value")


@dataclass(frozen=True)
class ForecastSupport:
    """Declared support for a synthetic high-confidence forecast."""

    timing_semantics_valid: bool
    calibration_traceable: bool
    censoring_accounted: bool
    treatment_history_complete: bool
    future_intervention_declared: bool
    model_support_declared: bool
    correlated_error_model_declared: bool

    @property
    def permits_high_confidence(self) -> bool:
        return all(
            (
                self.timing_semantics_valid,
                self.calibration_traceable,
                self.censoring_accounted,
                self.treatment_history_complete,
                self.future_intervention_declared,
                self.model_support_declared,
                self.correlated_error_model_declared,
            )
        )

    @property
    def missing_support(self) -> tuple[str, ...]:
        names = (
            "timing_semantics_valid",
            "calibration_traceable",
            "censoring_accounted",
            "treatment_history_complete",
            "future_intervention_declared",
            "model_support_declared",
            "correlated_error_model_declared",
        )
        return tuple(name for name in names if not getattr(self, name))


def validate_expected_time(
    observation: ObservationRecord,
    expected_at: int,
    tolerance: int = 0,
) -> None:
    """Fail closed when a sample is silently relabelled to another time slot."""

    _nonnegative_int(expected_at, "expected_at")
    _nonnegative_int(tolerance, "tolerance")
    if abs(observation.observed_at - expected_at) > tolerance:
        raise ValueError("observation timing is outside declared tolerance")


def validate_calibration_continuity(
    observations: tuple[ObservationRecord, ...],
    bridged_pairs: frozenset[tuple[str, str]] = frozenset(),
) -> None:
    """Require an explicit bridge when calibration identity changes."""

    by_modality: dict[str, list[ObservationRecord]] = {}
    for observation in observations:
        by_modality.setdefault(observation.modality, []).append(observation)

    for series in by_modality.values():
        series.sort(key=lambda item: item.observed_at)
        for previous, current in zip(series, series[1:]):
            if previous.calibration_id == current.calibration_id:
                continue
            pair = (previous.calibration_id, current.calibration_id)
            if pair not in bridged_pairs:
                raise ValueError("calibration change requires explicit bridge evidence")
