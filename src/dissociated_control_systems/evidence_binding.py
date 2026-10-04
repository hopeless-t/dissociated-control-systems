"""Identity-preserving evidence binding checks for RQ-005 META-A.

A meta-analysis row is treated as a tuple of identities, not just an effect
estimate. These helpers detect exact cross-row reuse of randomized counts and
near-exact reuse of effect estimates without inferring why the reuse occurred.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CanonicalEvidence:
    trial_id: str
    intervention_n: int | None = None
    control_n: int | None = None
    hr: float | None = None
    lower: float | None = None
    upper: float | None = None

    def __post_init__(self) -> None:
        if not self.trial_id.strip() or self.trial_id != self.trial_id.strip():
            raise ValueError("trial_id must be non-empty and normalized")
        for name in ("intervention_n", "control_n"):
            value = getattr(self, name)
            if value is not None and (isinstance(value, bool) or value <= 0):
                raise ValueError(f"{name} must be a positive integer or None")
        effect = (self.hr, self.lower, self.upper)
        if any(value is not None for value in effect):
            if any(value is None for value in effect):
                raise ValueError("hr/lower/upper must be all present or all absent")
            if not all(isfinite(float(value)) and float(value) > 0 for value in effect):
                raise ValueError("effect values must be positive finite numbers")
            if not float(self.lower) <= float(self.hr) <= float(self.upper):
                raise ValueError("effect estimate must lie within its interval")


@dataclass(frozen=True)
class DisplayedEvidence:
    row_id: str
    displayed_trial_id: str
    intervention_n: int
    control_n: int
    hr: float
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if not self.row_id.strip() or self.row_id != self.row_id.strip():
            raise ValueError("row_id must be non-empty and normalized")
        if not self.displayed_trial_id.strip() or self.displayed_trial_id != self.displayed_trial_id.strip():
            raise ValueError("displayed_trial_id must be non-empty and normalized")
        if self.intervention_n <= 0 or self.control_n <= 0:
            raise ValueError("displayed counts must be positive")
        if not (0 < self.lower <= self.hr <= self.upper):
            raise ValueError("displayed effect must be positive and internally ordered")


def build_canonical_index(records: Iterable[CanonicalEvidence]) -> dict[str, CanonicalEvidence]:
    index: dict[str, CanonicalEvidence] = {}
    for record in records:
        if record.trial_id in index:
            raise ValueError(f"duplicate canonical trial_id: {record.trial_id}")
        index[record.trial_id] = record
    if not index:
        raise ValueError("canonical evidence index must not be empty")
    return index


def count_matches(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
) -> tuple[str, ...]:
    """Return all canonical records with the exact displayed allocation counts."""

    matches = []
    for trial_id, record in canonical.items():
        if record.intervention_n is None or record.control_n is None:
            continue
        if (record.intervention_n, record.control_n) == (
            row.intervention_n,
            row.control_n,
        ):
            matches.append(trial_id)
    return tuple(sorted(matches))


def effect_matches(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
    *,
    point_tolerance: float = 0.006,
    interval_tolerance: float = 0.006,
) -> tuple[str, ...]:
    """Return canonical effects matching the displayed rounded HR and interval."""

    if point_tolerance < 0 or interval_tolerance < 0:
        raise ValueError("tolerances must be non-negative")
    matches = []
    for trial_id, record in canonical.items():
        if record.hr is None:
            continue
        if (
            abs(row.hr - float(record.hr)) <= point_tolerance
            and abs(row.lower - float(record.lower)) <= interval_tolerance
            and abs(row.upper - float(record.upper)) <= interval_tolerance
        ):
            matches.append(trial_id)
    return tuple(sorted(matches))


def classify_binding(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
    *,
    point_tolerance: float = 0.006,
    interval_tolerance: float = 0.006,
) -> dict[str, object]:
    """Describe identity consistency without guessing the mechanism of mismatch."""

    counts = count_matches(row, canonical)
    effects = effect_matches(
        row,
        canonical,
        point_tolerance=point_tolerance,
        interval_tolerance=interval_tolerance,
    )
    own_count = row.displayed_trial_id in counts
    own_effect = row.displayed_trial_id in effects

    if own_count and own_effect:
        status = "OWN_IDENTITY_CONSISTENT"
    elif not own_count and own_effect:
        status = "COUNT_CROSS_BINDING_CANDIDATE"
    elif own_count and not own_effect:
        status = "EFFECT_SOURCE_CONFLICT_OR_DERIVATION"
    elif counts or effects:
        status = "CROSS_BINDING_CANDIDATE"
    else:
        status = "UNRESOLVED_IDENTITY"

    return {
        "row_id": row.row_id,
        "displayed_trial_id": row.displayed_trial_id,
        "count_matches": counts,
        "effect_matches": effects,
        "own_count_match": own_count,
        "own_effect_match": own_effect,
        "status": status,
    }
