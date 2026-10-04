"""Small exact robustness metrics for evidence-witness dependency graphs."""

from __future__ import annotations

from itertools import combinations
from typing import Iterable

from .projection_assurance import EvidenceWitness
from .projection_protocol import (
    CheckpointRole,
    CheckStatus,
    ProjectionCertificate,
    required_roles_for_claim,
)


def _required_pass_roles(
    certificate: ProjectionCertificate,
) -> tuple[CheckpointRole, ...]:
    required = required_roles_for_claim(certificate.claim_type)
    passed = {
        record.role
        for record in certificate.records
        if record.status is CheckStatus.PASS
    }
    return tuple(role for role in required if role in passed)


def role_root_cut(
    role: CheckpointRole,
    witnesses: Iterable[EvidenceWitness],
) -> int | None:
    """Minimum source-root removals that destroy all usable support for role.

    Each witness is a series dependency over its declared roots: invalidating
    any one root invalidates that witness. Multiple witnesses are parallel
    support paths. The cut is therefore a minimum hitting set over witness root
    sets, solved exactly for the small HF01 contracts.
    """
    usable = tuple(w for w in witnesses if w.role is role and w.usable)
    if not usable:
        return 0

    roots = sorted({root for witness in usable for root in witness.source_roots})
    for size in range(1, len(roots) + 1):
        for removed in combinations(roots, size):
            removed_set = set(removed)
            if all(
                removed_set.intersection(witness.source_roots)
                for witness in usable
            ):
                return size
    return None


def certificate_root_cut(
    certificate: ProjectionCertificate,
    witnesses: Iterable[EvidenceWitness],
) -> int:
    """Fewest root failures needed to make any required PASS role unsupported."""
    witnesses_t = tuple(witnesses)
    roles = _required_pass_roles(certificate)
    if not roles:
        return 0
    cuts = [role_root_cut(role, witnesses_t) for role in roles]
    normalized = [cut if cut is not None else 0 for cut in cuts]
    return min(normalized)


def role_root_cuts(
    certificate: ProjectionCertificate,
    witnesses: Iterable[EvidenceWitness],
) -> dict[str, int | None]:
    witnesses_t = tuple(witnesses)
    return {
        role.value: role_root_cut(role, witnesses_t)
        for role in _required_pass_roles(certificate)
    }
