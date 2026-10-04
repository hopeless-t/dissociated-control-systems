"""Evidence-bound assurance layer for proof-carrying projections.

This module distinguishes syntactic checkpoint completion from substantive
witness support.  It does not decide scientific truth; it makes support and
common-mode dependency explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .projection_protocol import (
    CheckpointRole,
    CheckStatus,
    ClaimType,
    ProjectionCertificate,
    required_roles_for_claim,
    validate_projection_certificate,
)


class DefeaterStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    RESIDUAL = "RESIDUAL"


@dataclass(frozen=True)
class EvidenceWitness:
    witness_id: str
    role: CheckpointRole
    source_roots: frozenset[str]
    verified: bool = True

    def __post_init__(self) -> None:
        if not self.witness_id:
            raise ValueError("witness_id must be non-empty")
        if not self.source_roots:
            raise ValueError("source_roots must be non-empty")


@dataclass(frozen=True)
class Defeater:
    defeater_id: str
    target_role: CheckpointRole
    status: DefeaterStatus
    note: str = ""


@dataclass(frozen=True)
class AssuranceResult:
    accepted: bool
    terminal_status: CheckStatus
    violations: tuple[str, ...]
    warnings: tuple[str, ...]


def _required_pass_roles(certificate: ProjectionCertificate) -> tuple[CheckpointRole, ...]:
    required = required_roles_for_claim(certificate.claim_type)
    pass_roles = {
        record.role
        for record in certificate.records
        if record.status is CheckStatus.PASS
    }
    return tuple(role for role in required if role in pass_roles)


def root_blast_radius(
    certificate: ProjectionCertificate,
    witnesses: Iterable[EvidenceWitness],
) -> dict[str, int]:
    """Number of required PASS roles whose support disappears with each root.

    A witness is invalidated when any one of its declared source roots fails.
    Multiple independent witnesses can protect a role from a single-root loss.
    """
    witnesses_t = tuple(w for w in witnesses if w.verified)
    roles = _required_pass_roles(certificate)
    all_roots = sorted({root for w in witnesses_t for root in w.source_roots})
    blast: dict[str, int] = {}

    for root in all_roots:
        lost = 0
        for role in roles:
            remaining = [
                w
                for w in witnesses_t
                if w.role is role and root not in w.source_roots
            ]
            if not remaining:
                lost += 1
        blast[root] = lost
    return blast


def validate_evidence_bound_certificate(
    certificate: ProjectionCertificate,
    witnesses: Iterable[EvidenceWitness],
    defeaters: Iterable[Defeater] = (),
) -> AssuranceResult:
    """Validate protocol plus witness binding and explicit defeaters."""
    base = validate_projection_certificate(certificate)
    violations = list(base.violations)
    warnings: list[str] = []
    witnesses_t = tuple(witnesses)
    defeaters_t = tuple(defeaters)

    required = required_roles_for_claim(certificate.claim_type)
    record_by_role = {record.role: record for record in certificate.records}

    for role in required:
        record = record_by_role.get(role)
        if record is None or record.status is not CheckStatus.PASS:
            continue
        verified = [
            w for w in witnesses_t
            if w.role is role and w.verified
        ]
        if not verified:
            violations.append(f"pass_without_verified_witness:{role.value}")

    open_defeaters = [
        d for d in defeaters_t
        if d.status is DefeaterStatus.OPEN and d.target_role in required
    ]
    residual_defeaters = [
        d for d in defeaters_t
        if d.status is DefeaterStatus.RESIDUAL and d.target_role in required
    ]

    if open_defeaters:
        warnings.extend(
            f"open_defeater:{d.defeater_id}:{d.target_role.value}"
            for d in open_defeaters
        )
    if residual_defeaters:
        warnings.extend(
            f"residual_doubt:{d.defeater_id}:{d.target_role.value}"
            for d in residual_defeaters
        )

    terminal = base.terminal_status
    if open_defeaters and terminal is CheckStatus.PASS:
        terminal = CheckStatus.UNKNOWN
        if certificate.empirical_authority_requested:
            violations.append("open_defeater_blocks_empirical_pass")

    blast = root_blast_radius(certificate, witnesses_t)
    required_count = len(_required_pass_roles(certificate))
    if required_count:
        for root, lost in sorted(blast.items()):
            if lost > 1:
                warnings.append(
                    f"common_mode_root:{root}:loses_{lost}_of_{required_count}_roles"
                )

    return AssuranceResult(
        accepted=not violations,
        terminal_status=terminal,
        violations=tuple(violations),
        warnings=tuple(warnings),
    )
