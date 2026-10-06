"""Claim-relative validator for proof-carrying projection certificates.

The v1 protocol module remains the schema/constructor source for compatibility.
This validator corrects two authority bugs without changing those data types:

1. extra non-required checkpoint roles must not downgrade a weaker claim;
2. duplicate required roles are ambiguous and therefore rejected.
"""

from __future__ import annotations

from .projection_protocol import (
    CertificateValidation,
    CheckStatus,
    CheckpointRole,
    ProjectionCertificate,
    required_roles_for_claim,
)


def validate_projection_certificate_v2(
    certificate: ProjectionCertificate,
) -> CertificateValidation:
    records = certificate.records
    violations: list[str] = []
    required_roles = required_roles_for_claim(certificate.claim_type)

    positions: dict[CheckpointRole, int] = {}
    for role in required_roles:
        indexes = [
            idx
            for idx, record in enumerate(records)
            if record.role is role
        ]
        if not indexes:
            violations.append(f"missing_required_role:{role.value}")
            continue
        if len(indexes) > 1:
            violations.append(f"duplicate_required_role:{role.value}")
        positions[role] = indexes[0]

    if len(positions) == len(required_roles):
        ordered_positions = [positions[role] for role in required_roles]
        if ordered_positions != sorted(ordered_positions):
            violations.append("required_roles_out_of_order")

    # Authority is claim-relative. Extra records may remain in the audit trace,
    # but they cannot raise or lower the status of a weaker endpoint claim.
    required_statuses = [
        record.status
        for record in records
        if record.role in required_roles
    ]
    if CheckStatus.FAIL in required_statuses:
        terminal = CheckStatus.FAIL
    elif CheckStatus.UNKNOWN in required_statuses:
        terminal = CheckStatus.UNKNOWN
    else:
        terminal = CheckStatus.PASS

    if certificate.empirical_authority_requested and terminal is not CheckStatus.PASS:
        violations.append(
            "empirical_authority_requires_all_required_checks_pass"
        )

    return CertificateValidation(
        accepted=not violations,
        terminal_status=terminal,
        violations=tuple(violations),
    )
