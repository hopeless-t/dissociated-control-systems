"""Normative HF01 assurance kernel v2.

This module is the single authority path that composes the proof-carrying
projection protocol with evidence applicability, support topology, explicit
trust boundaries, and dependency freshness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .assurance_versioning import DependencySnapshot, compare_snapshot
from .projection_assurance import (
    Defeater,
    EvidenceWitness,
    validate_evidence_bound_certificate,
)
from .projection_protocol import CheckStatus, ProjectionCertificate
from .support_graph import (
    SupportEdge,
    SupportNode,
    SupportNodeKind,
    claim_is_grounded,
    find_cycles,
    primitive_ancestors,
)
from .trust_roots import TrustRoot, validate_trust_boundary


@dataclass(frozen=True)
class KernelDecision:
    accepted: bool
    terminal_status: CheckStatus
    violations: tuple[str, ...]
    warnings: tuple[str, ...]


def validate_authority_v2(
    *,
    certificate: ProjectionCertificate,
    witnesses: Iterable[EvidenceWitness],
    defeaters: Iterable[Defeater] = (),
    support_nodes: Iterable[SupportNode],
    support_edges: Iterable[SupportEdge],
    support_target: str,
    dependency_snapshot: DependencySnapshot,
    current_revisions: Mapping[str, str],
    trust_roots: Iterable[TrustRoot],
) -> KernelDecision:
    witnesses_t = tuple(witnesses)
    nodes_t = tuple(support_nodes)
    edges_t = tuple(support_edges)
    violations: list[str] = []
    warnings: list[str] = []

    assurance = validate_evidence_bound_certificate(
        certificate,
        witnesses_t,
        defeaters,
    )
    violations.extend(assurance.violations)
    warnings.extend(assurance.warnings)
    terminal = assurance.terminal_status

    node_kind = {node.node_id: node.kind for node in nodes_t}
    if support_target not in node_kind:
        violations.append("support_target_missing")
    else:
        cycles = find_cycles(nodes_t, edges_t)
        if cycles:
            violations.append("cyclic_support_graph")
        elif not claim_is_grounded(support_target, nodes_t, edges_t):
            violations.append("support_target_not_primitive_grounded")

    # Every source root used by an otherwise usable witness must be represented
    # inside the support graph and must not be another claim masquerading as
    # primitive support.
    for witness in witnesses_t:
        if not witness.usable:
            continue
        for root in witness.source_roots:
            kind = node_kind.get(root)
            if kind is None:
                violations.append(f"witness_root_missing_from_support_graph:{root}")
                continue
            if kind is SupportNodeKind.CLAIM:
                violations.append(f"witness_root_is_claim:{root}")

    if support_target in node_kind and not find_cycles(nodes_t, edges_t):
        primitive_ids = primitive_ancestors(support_target, nodes_t, edges_t)
        boundary = validate_trust_boundary(primitive_ids, trust_roots)
        if not boundary.complete:
            for root in boundary.missing_roots:
                violations.append(f"missing_trust_root:{root}")
            for root in boundary.duplicate_root_ids:
                violations.append(f"duplicate_trust_root:{root}")

    staleness = compare_snapshot(dependency_snapshot, current_revisions)
    if staleness.stale:
        for dep in staleness.changed:
            violations.append(f"stale_dependency_changed:{dep}")
        for dep in staleness.missing:
            violations.append(f"stale_dependency_missing:{dep}")
        for dep in staleness.added:
            violations.append(f"stale_dependency_added:{dep}")

    # Kernel-level violations cannot preserve PASS authority.
    if violations and terminal is CheckStatus.PASS:
        terminal = CheckStatus.UNKNOWN

    return KernelDecision(
        accepted=not violations,
        terminal_status=terminal,
        violations=tuple(dict.fromkeys(violations)),
        warnings=tuple(dict.fromkeys(warnings)),
    )
