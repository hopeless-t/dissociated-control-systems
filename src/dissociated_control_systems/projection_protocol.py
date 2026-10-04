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


class ClaimType(str, Enum):
    DESCRIPTIVE = "DESCRIPTIVE"
    STATE_INFERENCE = "STATE_INFERENCE"
    RESPONSE_INFERENCE = "RESPONSE_INFERENCE"
    REACHABILITY = "REACHABILITY"


def required_roles_for_claim(
    claim_type: ClaimType,
) -> tuple[CheckpointRole, ...]:
    if claim_type is ClaimType.DESCRIPTIVE:
        return (
            CheckpointRole.PROVENANCE,
            CheckpointRole.UNCERTAINTY,
        )
    if claim_type in (
        ClaimType.STATE_INFERENCE,
        ClaimType.RESPONSE_INFERENCE,
    ):
        return (
            CheckpointRole.PROVENANCE,
            CheckpointRole.STATE_RESPONSE,
            CheckpointRole.UNCERTAINTY,
        )
    return REQUIRED_ORDER


@dataclass(frozen=True)
class CheckpointRecord:
    role: CheckpointRole
    status: CheckStatus
    note: str = ""


@dataclass(frozen=True)
class ProjectionCertificate:
    records: tuple[CheckpointRecord, ...]
    claim_type: ClaimType = ClaimType.REACHABILITY
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

    required_roles = required_roles_for_claim(certificate.claim_type)

    # Only roles required by the terminal claim type are mandatory.
    positions: dict[CheckpointRole, int] = {}
    for role in required_roles:
        indexes = [
            idx for idx, record in enumerate(records)
            if record.role is role
        ]
        if not indexes:
            violations.append(f"missing_required_role:{role.value}")
        else:
            positions[role] = indexes[0]

    # The selected required roles remain a protocol, not an unordered checklist.
    if len(positions) == len(required_roles):
        ordered_positions = [positions[role] for role in required_roles]
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
    claim_type: ClaimType = ClaimType.REACHABILITY,
    empirical_authority_requested: bool = False,
) -> ProjectionCertificate:
    """Build one canonical trace for tests/examples."""
    roles = required_roles_for_claim(claim_type)
    statuses_t = tuple(statuses) if statuses is not None else tuple(
        CheckStatus.PASS for _ in roles
    )
    if len(statuses_t) != len(roles):
        raise ValueError("one status is required per claim-conditioned role")
    return ProjectionCertificate(
        records=tuple(
            CheckpointRecord(role, status)
            for role, status in zip(roles, statuses_t)
        ),
        claim_type=claim_type,
        empirical_authority_requested=empirical_authority_requested,
    )
