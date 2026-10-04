"""Proof-carrying projection protocol for DCS claims.

The protocol does not decide biomedical truth. It ensures that a terminal claim
cannot be emitted without an auditable trace through the required semantic
barriers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class CheckpointRole(str, Enum):
    PROVENANCE = "PROVENANCE"
    STATE_RESPONSE = "STATE_RESPONSE"
    UNCERTAINTY = "UNCERTAINTY"
    REACHABILITY = "REACHABILITY"


REQUIRED_ORDER = (
    CheckpointRole.PROVENANCE,
    CheckpointRole.STATE_RESPONSE,
    CheckpointRole.UNCERTAINTY,
    CheckpointRole.REACHABILITY,
)


class CheckStatus(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class CheckpointRecord:
    role: CheckpointRole
    status: CheckStatus
    note: str = ""


@dataclass(frozen=True)
class ProjectionCertificate:
    records: tuple[CheckpointRecord, ...]
    empirical_authority_requested: bool = False


@dataclass(frozen=True)
class CertificateValidation:
    accepted: bool
    terminal_status: CheckStatus
    violations: tuple[str, ...]


def validate_projection_certificate(
    certificate: ProjectionCertificate,
) -> CertificateValidation:
    """Validate must-pass order and fail-closed endpoint semantics."""
    records = certificate.records
    violations: list[str] = []

    # A required role must occur at least once.
    positions: dict[CheckpointRole, int] = {}
    for role in REQUIRED_ORDER:
        indexes = [
            idx for idx, record in enumerate(records)
            if record.role is role
        ]
        if not indexes:
            violations.append(f"missing_required_role:{role.value}")
        else:
            positions[role] = indexes[0]

    # The semantic roles form a protocol, not an unordered checklist.
    if len(positions) == len(REQUIRED_ORDER):
        ordered_positions = [positions[role] for role in REQUIRED_ORDER]
        if ordered_positions != sorted(ordered_positions):
            violations.append("required_roles_out_of_order")

    statuses = [record.status for record in records]
    if CheckStatus.FAIL in statuses:
        terminal = CheckStatus.FAIL
    elif CheckStatus.UNKNOWN in statuses:
        terminal = CheckStatus.UNKNOWN
    else:
        terminal = CheckStatus.PASS

    # An empirical claim may not be emitted through UNKNOWN or FAIL.
    if certificate.empirical_authority_requested and terminal is not CheckStatus.PASS:
        violations.append(
            "empirical_authority_requires_all_required_checks_pass"
        )

    return CertificateValidation(
        accepted=not violations,
        terminal_status=terminal,
        violations=tuple(violations),
    )


def canonical_trace(
    statuses: Iterable[CheckStatus] | None = None,
    *,
    empirical_authority_requested: bool = False,
) -> ProjectionCertificate:
    """Build one canonical trace for tests/examples."""
    statuses_t = tuple(statuses) if statuses is not None else (
        CheckStatus.PASS,
        CheckStatus.PASS,
        CheckStatus.PASS,
        CheckStatus.PASS,
    )
    if len(statuses_t) != len(REQUIRED_ORDER):
        raise ValueError("one status is required per mandatory role")
    return ProjectionCertificate(
        records=tuple(
            CheckpointRecord(role, status)
            for role, status in zip(REQUIRED_ORDER, statuses_t)
        ),
        empirical_authority_requested=empirical_authority_requested,
    )
