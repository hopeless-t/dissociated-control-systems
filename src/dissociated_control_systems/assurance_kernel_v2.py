"""Normative HF01 assurance kernel v2.

This module is the single authority path that composes claim semantics,
proof-carrying checkpoints, evidence applicability, support topology, explicit
trust boundaries, and dependency freshness.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping

from .assurance_versioning import DependencySnapshot, compare_snapshot
from .claim_semantics import ClaimSemantics, derive_claim_type
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


def _ancestor_nodes(
    target: str,
    nodes: tuple[SupportNode, ...],
    edges: tuple[SupportEdge, ...],
) -> frozenset[str]:
    names = {node.node_id for node in nodes}
    if target not in names:
        return frozenset()
    reverse: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge.source not in names or edge.target not in names:
            raise ValueError("edge references unknown support node")
        reverse[edge.target].append(edge.source)

    found: set[str] = set()
    stack = [target]
    while stack:
        current = stack.pop()
        for parent in reverse.get(current, []):
            if parent in found:
                continue
            found.add(parent)
            stack.append(parent)
    return frozenset(found)


def validate_authority_v2(
    *,
    certificate: ProjectionCertificate,
    claim_semantics: ClaimSemantics,
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

    derived_claim_type = derive_claim_type(claim_semantics)
    if derived_claim_type is not certificate.claim_type:
        violations.append(
            "claim_type_semantic_mismatch:"
            f"declared={certificate.claim_type.value}:"
            f"derived={derived_claim_type.value}"
        )

    assurance = validate_evidence_bound_certificate(
        certificate,
        witnesses_t,
        defeaters,
    )
    violations.extend(assurance.violations)
    warnings.extend(assurance.warnings)
    terminal = assurance.terminal_status

    node_ids = [node.node_id for node in nodes_t]
    duplicate_nodes = sorted(
        node_id
        for node_id in set(node_ids)
        if node_ids.count(node_id) > 1
    )
    for node_id in duplicate_nodes:
        violations.append(f"duplicate_support_node:{node_id}")

    node_kind = {node.node_id: node.kind for node in nodes_t}
    graph_valid = not duplicate_nodes
    ancestors: frozenset[str] = frozenset()

    if support_target not in node_kind:
        violations.append("support_target_missing")
        graph_valid = False
    elif node_kind[support_target] is not SupportNodeKind.CLAIM:
        violations.append("support_target_not_claim")
        graph_valid = False

    cycles: tuple[tuple[str, ...], ...] = ()
    if graph_valid:
        try:
            cycles = find_cycles(nodes_t, edges_t)
            ancestors = _ancestor_nodes(support_target, nodes_t, edges_t)
        except ValueError as exc:
            violations.append(f"invalid_support_graph:{exc}")
            graph_valid = False

    if graph_valid:
        if cycles:
            violations.append("cyclic_support_graph")
        elif not claim_is_grounded(support_target, nodes_t, edges_t):
            violations.append("support_target_not_primitive_grounded")

    # Every usable witness root must be an actual non-claim ancestor of the
    # endpoint claim, not merely an arbitrary node somewhere in the graph.
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
                continue
            if graph_valid and root not in ancestors:
                violations.append(f"witness_root_not_ancestor_of_claim:{root}")

    if graph_valid and not cycles:
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

    if violations and terminal is CheckStatus.PASS:
        terminal = CheckStatus.UNKNOWN

    return KernelDecision(
        accepted=not violations,
        terminal_status=terminal,
        violations=tuple(dict.fromkeys(violations)),
        warnings=tuple(dict.fromkeys(warnings)),
    )
