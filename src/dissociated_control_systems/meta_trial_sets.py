"""Set-level reconciliation primitives for RQ-005 META-A."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


def _freeze_ids(values: Iterable[str], *, label: str) -> frozenset[str]:
    items = tuple(values)
    if not items:
        raise ValueError(f"{label} trial set must not be empty")
    cleaned: list[str] = []
    for item in items:
        if not isinstance(item, str):
            raise TypeError(f"{label} trial IDs must be strings")
        if not item or item != item.strip():
            raise ValueError(f"{label} trial IDs must be non-empty and normalized")
        cleaned.append(item)
    if len(cleaned) != len(set(cleaned)):
        raise ValueError(f"{label} trial set contains duplicate IDs")
    return frozenset(cleaned)


@dataclass(frozen=True)
class TrialSetDelta:
    shared: frozenset[str]
    left_only: frozenset[str]
    right_only: frozenset[str]

    @property
    def n_shared(self) -> int:
        return len(self.shared)

    @property
    def n_left_only(self) -> int:
        return len(self.left_only)

    @property
    def n_right_only(self) -> int:
        return len(self.right_only)

    @property
    def jaccard(self) -> float:
        union = self.shared | self.left_only | self.right_only
        return len(self.shared) / len(union)


def compare_trial_sets(
    left: Iterable[str], right: Iterable[str], *, left_label: str = "left", right_label: str = "right"
) -> TrialSetDelta:
    left_ids = _freeze_ids(left, label=left_label)
    right_ids = _freeze_ids(right, label=right_label)
    return TrialSetDelta(
        shared=left_ids & right_ids,
        left_only=left_ids - right_ids,
        right_only=right_ids - left_ids,
    )
