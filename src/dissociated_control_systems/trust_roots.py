"""Explicit trust-boundary declarations for assurance support graphs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class TrustRootKind(str, Enum):
    RAW_OBSERVATION = "RAW_OBSERVATION"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"
    TOOL_RUNTIME = "TOOL_RUNTIME"
    HUMAN_ATTESTATION = "HUMAN_ATTESTATION"


@dataclass(frozen=True)
class TrustRoot:
    root_id: str
    kind: TrustRootKind
    assumptions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.root_id:
            raise ValueError("root_id must be non-empty")
        if not self.assumptions:
            raise ValueError("trust root must expose at least one assumption")
        if any(not item.strip() for item in self.assumptions):
            raise ValueError("trust-root assumptions must be non-empty strings")


@dataclass(frozen=True)
class TrustBoundaryReport:
    complete: bool
    missing_roots: tuple[str, ...]
    duplicate_root_ids: tuple[str, ...]


def validate_trust_boundary(
    primitive_evidence_ids: Iterable[str],
    roots: Iterable[TrustRoot],
) -> TrustBoundaryReport:
    """Require every primitive evidence node to terminate in an explicit root."""
    primitive = tuple(primitive_evidence_ids)
    roots_t = tuple(roots)

    counts: dict[str, int] = {}
    for root in roots_t:
        counts[root.root_id] = counts.get(root.root_id, 0) + 1

    duplicates = tuple(sorted(
        root_id for root_id, count in counts.items()
        if count > 1
    ))
    declared = set(counts)
    missing = tuple(sorted(set(primitive) - declared))

    return TrustBoundaryReport(
        complete=not missing and not duplicates,
        missing_roots=missing,
        duplicate_root_ids=duplicates,
    )
