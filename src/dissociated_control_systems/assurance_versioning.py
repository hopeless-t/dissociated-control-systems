"""Version binding for proof-carrying assurance artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class DependencySnapshot:
    revisions: tuple[tuple[str, str], ...]

    @classmethod
    def from_mapping(cls, revisions: Mapping[str, str]) -> "DependencySnapshot":
        if any(not key or not value for key, value in revisions.items()):
            raise ValueError("dependency ids and revisions must be non-empty")
        return cls(tuple(sorted(revisions.items())))

    def as_dict(self) -> dict[str, str]:
        return dict(self.revisions)


@dataclass(frozen=True)
class StalenessReport:
    stale: bool
    changed: tuple[str, ...]
    missing: tuple[str, ...]
    added: tuple[str, ...]


def compare_snapshot(
    certificate_snapshot: DependencySnapshot,
    current_revisions: Mapping[str, str],
) -> StalenessReport:
    """Compare bound dependency revisions with current declared revisions."""
    old = certificate_snapshot.as_dict()
    current = dict(current_revisions)

    changed = tuple(sorted(
        key for key in old.keys() & current.keys()
        if old[key] != current[key]
    ))
    missing = tuple(sorted(old.keys() - current.keys()))
    added = tuple(sorted(current.keys() - old.keys()))

    # Added dependencies can change the semantics of the current claim even if
    # old inputs are unchanged, so they also invalidate the old snapshot.
    return StalenessReport(
        stale=bool(changed or missing or added),
        changed=changed,
        missing=missing,
        added=added,
    )


def snapshot_matches(
    certificate_snapshot: DependencySnapshot,
    current_revisions: Mapping[str, str],
) -> bool:
    return not compare_snapshot(certificate_snapshot, current_revisions).stale
