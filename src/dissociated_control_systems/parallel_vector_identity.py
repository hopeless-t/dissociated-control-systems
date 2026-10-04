"""Identity contract for parallel evidence vectors.

Many statistical APIs can verify that parallel vectors have equal lengths but
cannot know whether element i in each vector refers to the same trial. RQ-005
makes that semantic identity explicit before analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class KeyedVector(Generic[T]):
    name: str
    trial_ids: tuple[str, ...]
    values: tuple[T, ...]

    def __post_init__(self) -> None:
        if not self.name.strip() or self.name != self.name.strip():
            raise ValueError("vector name must be non-empty and normalized")
        if len(self.trial_ids) != len(self.values):
            raise ValueError("trial_ids and values must have equal length")
        if not self.trial_ids:
            raise ValueError("keyed vector must not be empty")
        if any(not trial_id.strip() or trial_id != trial_id.strip() for trial_id in self.trial_ids):
            raise ValueError("trial IDs must be non-empty and normalized")
        if len(set(self.trial_ids)) != len(self.trial_ids):
            raise ValueError("trial IDs must be unique within one evidence vector")


def keyed_vector(name: str, trial_ids: Iterable[str], values: Iterable[T]) -> KeyedVector[T]:
    return KeyedVector(name=name, trial_ids=tuple(trial_ids), values=tuple(values))


def length_only_compatible(reference: KeyedVector[object], candidate: KeyedVector[object]) -> bool:
    """Model the weakest common API gate: vector lengths agree."""

    return len(reference.values) == len(candidate.values)


def identity_mismatches(
    reference: KeyedVector[object], candidate: KeyedVector[object]
) -> tuple[dict[str, object], ...]:
    """Return positional identity conflicts after requiring equal lengths."""

    if not length_only_compatible(reference, candidate):
        raise ValueError("parallel vectors have different lengths")
    mismatches = []
    for index, (expected, observed) in enumerate(
        zip(reference.trial_ids, candidate.trial_ids, strict=True)
    ):
        if expected != observed:
            mismatches.append(
                {
                    "index": index,
                    "reference_trial_id": expected,
                    "candidate_trial_id": observed,
                }
            )
    return tuple(mismatches)


def require_identity_alignment(
    reference: KeyedVector[object], *candidates: KeyedVector[object]
) -> None:
    """Fail closed unless every parallel vector has the same trial identity order."""

    if not candidates:
        raise ValueError("at least one candidate vector is required")
    for candidate in candidates:
        mismatches = identity_mismatches(reference, candidate)
        if mismatches:
            first = mismatches[0]
            raise ValueError(
                "evidence identity mismatch in "
                f"{candidate.name!r} at index {first['index']}: "
                f"expected {first['reference_trial_id']!r}, "
                f"observed {first['candidate_trial_id']!r}"
            )


def alignment_summary(
    reference: KeyedVector[object], candidates: Iterable[KeyedVector[object]]
) -> dict[str, object]:
    results = {}
    for candidate in candidates:
        compatible = length_only_compatible(reference, candidate)
        mismatches = identity_mismatches(reference, candidate) if compatible else ()
        results[candidate.name] = {
            "length_only_compatible": compatible,
            "identity_aligned": compatible and not mismatches,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
        }
    return {
        "reference": reference.name,
        "n": len(reference.values),
        "vectors": results,
    }
