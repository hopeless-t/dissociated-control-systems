"""Exhaustive small-state attack surface for proof-carrying projections."""

from __future__ import annotations

from itertools import combinations, permutations, product

from .projection_protocol import (
    CheckpointRecord,
    CheckpointRole,
    CheckStatus,
    ClaimType,
    ProjectionCertificate,
    REQUIRED_ORDER,
    validate_projection_certificate,
)


def subset_attack_summary() -> dict[str, int]:
    """Enumerate every subset of the four reachability roles.

    Records are kept in canonical order when present.
    """
    tested = 0
    accepted = 0
    for size in range(len(REQUIRED_ORDER) + 1):
        for subset in combinations(REQUIRED_ORDER, size):
            tested += 1
            cert = ProjectionCertificate(
                records=tuple(
                    CheckpointRecord(role, CheckStatus.PASS)
                    for role in subset
                ),
                claim_type=ClaimType.REACHABILITY,
                empirical_authority_requested=True,
            )
            accepted += int(validate_projection_certificate(cert).accepted)
    return {"tested": tested, "accepted": accepted}


def permutation_attack_summary() -> dict[str, int]:
    """Enumerate every ordering of the complete four-role set."""
    tested = 0
    accepted = 0
    for ordering in permutations(REQUIRED_ORDER):
        tested += 1
        cert = ProjectionCertificate(
            records=tuple(
                CheckpointRecord(role, CheckStatus.PASS)
                for role in ordering
            ),
            claim_type=ClaimType.REACHABILITY,
            empirical_authority_requested=True,
        )
        accepted += int(validate_projection_certificate(cert).accepted)
    return {"tested": tested, "accepted": accepted}


def status_attack_summary() -> dict[str, int]:
    """Enumerate every PASS/UNKNOWN/FAIL assignment in canonical order."""
    tested = 0
    accepted = 0
    for statuses in product(tuple(CheckStatus), repeat=len(REQUIRED_ORDER)):
        tested += 1
        cert = ProjectionCertificate(
            records=tuple(
                CheckpointRecord(role, status)
                for role, status in zip(REQUIRED_ORDER, statuses)
            ),
            claim_type=ClaimType.REACHABILITY,
            empirical_authority_requested=True,
        )
        accepted += int(validate_projection_certificate(cert).accepted)
    return {"tested": tested, "accepted": accepted}


def full_attack_summary() -> dict[str, dict[str, int]]:
    return {
        "subsets": subset_attack_summary(),
        "permutations": permutation_attack_summary(),
        "statuses": status_attack_summary(),
    }
