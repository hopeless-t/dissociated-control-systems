"""Identity-preserving evidence binding checks for RQ-005 META-A.

A meta-analysis row is treated as a tuple of identities, not just an effect
estimate. Canonical records may contain multiple evidence snapshots from one
trial and may contain semantically different count pairs (for example
population sizes versus recurrence-event counts). Equal numbers do not imply
equal field semantics.
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
    evidence_id: str | None = None
    count_semantics: str = "population_size"

    def __post_init__(self) -> None:
        if not self.trial_id.strip() or self.trial_id != self.trial_id.strip():
            raise ValueError("trial_id must be non-empty and normalized")
        if self.evidence_id is not None:
            if not self.evidence_id.strip() or self.evidence_id != self.evidence_id.strip():
                raise ValueError("evidence_id must be non-empty and normalized")
        if not self.count_semantics.strip() or self.count_semantics != self.count_semantics.strip():
            raise ValueError("count_semantics must be non-empty and normalized")
        for name in ("intervention_n", "control_n"):
            value = getattr(self, name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value <= 0
            ):
                raise ValueError(f"{name} must be a positive integer or None")
        effect = (self.hr, self.lower, self.upper)
        if any(value is not None for value in effect):
            if any(value is None for value in effect):
                raise ValueError("hr/lower/upper must be all present or all absent")
            if not all(isfinite(float(value)) and float(value) > 0 for value in effect):
                raise ValueError("effect values must be positive finite numbers")
            if not float(self.lower) <= float(self.hr) <= float(self.upper):
                raise ValueError("effect estimate must lie within its interval")

    @property
    def key(self) -> str:
        return self.evidence_id or self.trial_id


@dataclass(frozen=True)
class DisplayedEvidence:
    row_id: str
    displayed_trial_id: str
    intervention_n: int
    control_n: int
    hr: float
    lower: float
    upper: float
    count_semantics: str = "population_size"

    def __post_init__(self) -> None:
        if not self.row_id.strip() or self.row_id != self.row_id.strip():
            raise ValueError("row_id must be non-empty and normalized")
        if (
            not self.displayed_trial_id.strip()
            or self.displayed_trial_id != self.displayed_trial_id.strip()
        ):
            raise ValueError("displayed_trial_id must be non-empty and normalized")
        if not self.count_semantics.strip() or self.count_semantics != self.count_semantics.strip():
            raise ValueError("count_semantics must be non-empty and normalized")
        if self.intervention_n <= 0 or self.control_n <= 0:
            raise ValueError("displayed counts must be positive")
        if not (0 < self.lower <= self.hr <= self.upper):
            raise ValueError("displayed effect must be positive and internally ordered")


def build_canonical_index(
    records: Iterable[CanonicalEvidence],
) -> dict[str, CanonicalEvidence]:
    """Index evidence snapshots while preserving shared underlying trial IDs."""

    index: dict[str, CanonicalEvidence] = {}
    for record in records:
        if record.key in index:
            raise ValueError(f"duplicate canonical evidence_id: {record.key}")
        index[record.key] = record
    if not index:
        raise ValueError("canonical evidence index must not be empty")
    return index


def count_matches(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
    *,
    same_semantics: bool = True,
) -> tuple[str, ...]:
    """Return exact count-pair matches, optionally requiring field semantics."""

    matches = []
    for evidence_id, record in canonical.items():
        if record.intervention_n is None or record.control_n is None:
            continue
        if same_semantics and record.count_semantics != row.count_semantics:
            continue
        if (record.intervention_n, record.control_n) == (
            row.intervention_n,
            row.control_n,
        ):
            matches.append(evidence_id)
    return tuple(sorted(matches))


def cross_semantic_count_matches(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
) -> tuple[str, ...]:
    """Return equal count pairs whose declared field semantics differ."""

    all_matches = count_matches(row, canonical, same_semantics=False)
    return tuple(
        evidence_id
        for evidence_id in all_matches
        if canonical[evidence_id].count_semantics != row.count_semantics
    )


def effect_matches(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
    *,
    point_tolerance: float = 0.006,
    interval_tolerance: float = 0.006,
) -> tuple[str, ...]:
    """Return evidence snapshot IDs matching rounded displayed HR and interval."""

    if point_tolerance < 0 or interval_tolerance < 0:
        raise ValueError("tolerances must be non-negative")
    matches = []
    for evidence_id, record in canonical.items():
        if record.hr is None:
            continue
        if (
            abs(row.hr - float(record.hr)) <= point_tolerance
            and abs(row.lower - float(record.lower)) <= interval_tolerance
            and abs(row.upper - float(record.upper)) <= interval_tolerance
        ):
            matches.append(evidence_id)
    return tuple(sorted(matches))


def _trial_ids_for_matches(
    matches: tuple[str, ...], canonical: Mapping[str, CanonicalEvidence]
) -> tuple[str, ...]:
    return tuple(sorted({canonical[evidence_id].trial_id for evidence_id in matches}))


def classify_binding(
    row: DisplayedEvidence,
    canonical: Mapping[str, CanonicalEvidence],
    *,
    point_tolerance: float = 0.006,
    interval_tolerance: float = 0.006,
) -> dict[str, object]:
    """Describe identity consistency without guessing the mechanism of mismatch."""

    counts = count_matches(row, canonical)
    semantic_collisions = cross_semantic_count_matches(row, canonical)
    effects = effect_matches(
        row,
        canonical,
        point_tolerance=point_tolerance,
        interval_tolerance=interval_tolerance,
    )
    count_trial_ids = _trial_ids_for_matches(counts, canonical)
    semantic_collision_trial_ids = _trial_ids_for_matches(semantic_collisions, canonical)
    effect_trial_ids = _trial_ids_for_matches(effects, canonical)
    own_count = row.displayed_trial_id in count_trial_ids
    own_effect = row.displayed_trial_id in effect_trial_ids

    if own_count and own_effect:
        status = "OWN_IDENTITY_CONSISTENT"
    elif not own_count and own_effect:
        status = "COUNT_CROSS_BINDING_CANDIDATE"
    elif own_count and not own_effect:
        status = "EFFECT_SOURCE_CONFLICT_OR_DERIVATION"
    elif counts or effects:
        status = "CROSS_BINDING_CANDIDATE"
    elif semantic_collisions:
        status = "COUNT_SEMANTIC_COLLISION_CANDIDATE"
    else:
        status = "UNRESOLVED_IDENTITY"

    return {
        "row_id": row.row_id,
        "displayed_trial_id": row.displayed_trial_id,
        "displayed_count_semantics": row.count_semantics,
        "count_matches": counts,
        "count_match_trial_ids": count_trial_ids,
        "cross_semantic_count_matches": semantic_collisions,
        "cross_semantic_count_match_trial_ids": semantic_collision_trial_ids,
        "effect_matches": effects,
        "effect_match_trial_ids": effect_trial_ids,
        "own_count_match": own_count,
        "own_effect_match": own_effect,
        "status": status,
    }
