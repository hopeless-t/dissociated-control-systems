"""Source-aware estimate reconciliation for RQ-005 META-A.

A meta-analysis result is not treated as one scalar if the same declared
analysis is reported differently across abstract, main text, figure, preprint,
or supplement. Conflicts remain explicit until upstream provenance is resolved.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class PublishedEstimate:
    report_id: str
    analysis_id: str
    source_location: str
    endpoint: str
    effect_metric: str
    estimate: float
    lower: float
    upper: float
    n_studies: int | None = None
    n_participants: int | None = None

    def __post_init__(self) -> None:
        for name in (
            "report_id",
            "analysis_id",
            "source_location",
            "endpoint",
            "effect_metric",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
            if value != value.strip():
                raise ValueError(f"{name} must not contain surrounding whitespace")

        values = (self.estimate, self.lower, self.upper)
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
            raise TypeError("estimate and interval bounds must be numeric")
        if not all(isfinite(float(value)) for value in values):
            raise ValueError("estimate and interval bounds must be finite")
        if self.lower > self.estimate or self.estimate > self.upper:
            raise ValueError("estimate must lie within [lower, upper]")

        for name in ("n_studies", "n_participants"):
            value = getattr(self, name)
            if value is not None:
                if isinstance(value, bool) or not isinstance(value, int):
                    raise TypeError(f"{name} must be an integer or None")
                if value <= 0:
                    raise ValueError(f"{name} must be positive when provided")

    @property
    def estimand_key(self) -> tuple[str, str, str, str]:
        return (self.report_id, self.analysis_id, self.endpoint, self.effect_metric)


@dataclass(frozen=True)
class ReconciliationResult:
    key: tuple[str, str, str, str]
    status: str
    records: tuple[PublishedEstimate, ...]
    max_point_difference: float
    max_lower_difference: float
    max_upper_difference: float


def reconcile_same_analysis(
    records: Iterable[PublishedEstimate],
    *,
    tolerance: float = 0.005,
) -> ReconciliationResult:
    items = tuple(records)
    if not items:
        raise ValueError("at least one estimate is required")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)):
        raise TypeError("tolerance must be numeric")
    if tolerance < 0 or not isfinite(float(tolerance)):
        raise ValueError("tolerance must be finite and non-negative")

    key = items[0].estimand_key
    if any(item.estimand_key != key for item in items[1:]):
        raise ValueError("cannot reconcile records from different declared analyses")

    if len({item.source_location for item in items}) != len(items):
        raise ValueError("source_location must be unique within one reconciliation set")

    point_values = [float(item.estimate) for item in items]
    lower_values = [float(item.lower) for item in items]
    upper_values = [float(item.upper) for item in items]
    max_point = max(point_values) - min(point_values)
    max_lower = max(lower_values) - min(lower_values)
    max_upper = max(upper_values) - min(upper_values)

    conflict = max(max_point, max_lower, max_upper) > float(tolerance)
    return ReconciliationResult(
        key=key,
        status="INTERNAL_CONFLICT" if conflict else "CONSISTENT_WITHIN_TOLERANCE",
        records=items,
        max_point_difference=max_point,
        max_lower_difference=max_lower,
        max_upper_difference=max_upper,
    )


def require_canonicalizable(result: ReconciliationResult) -> PublishedEstimate:
    """Return a representative only when source reports agree within tolerance."""
    if result.status != "CONSISTENT_WITHIN_TOLERANCE":
        raise ValueError("estimate cannot be canonicalized while source conflict is open")
    return result.records[0]
