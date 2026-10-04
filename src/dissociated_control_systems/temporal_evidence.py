"""Temporal provenance gates for RQ-005 observations.

A feature cannot predict from a time before it was observed. Later measurements
may be used only after moving the prediction origin / landmark forward.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TimedObservation:
    name: str
    observed_at_month: float

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if self.observed_at_month < 0:
            raise ValueError("observed_at_month must be non-negative")


def validate_available_by_landmark(
    observations: Iterable[TimedObservation],
    *,
    landmark_month: float,
) -> tuple[TimedObservation, ...]:
    """Fail if any declared model feature is observed after the landmark."""
    if landmark_month < 0:
        raise ValueError("landmark_month must be non-negative")
    items = tuple(observations)
    leaked = [item.name for item in items if item.observed_at_month > landmark_month]
    if leaked:
        raise ValueError(
            "future-information leakage after landmark: " + ", ".join(sorted(leaked))
        )
    return items


def split_by_landmark(
    observations: Iterable[TimedObservation],
    *,
    landmark_month: float,
) -> tuple[tuple[TimedObservation, ...], tuple[TimedObservation, ...]]:
    """Return observations available by landmark and observations still future."""
    if landmark_month < 0:
        raise ValueError("landmark_month must be non-negative")
    available = []
    future = []
    for item in observations:
        (available if item.observed_at_month <= landmark_month else future).append(item)
    return tuple(available), tuple(future)
