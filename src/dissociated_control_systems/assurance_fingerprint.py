"""Canonical content fingerprint for HF01 assurance inputs.

The digest is an integrity/change detector, not a digital signature and not a
scientific confidence score.  It prevents a proof object from remaining
nominally 'the same' while its claim semantics, witnesses, support graph,
defeaters, or trust assumptions silently change.
"""

from __future__ import annotations

import hashlib
import json
from typing import Iterable, Mapping

from .claim_semantics import ClaimSemantics
from .projection_assurance import Defeater, EvidenceWitness
from .projection_protocol import ProjectionCertificate
from .support_graph import SupportEdge, SupportNode
from .trust_roots import TrustRoot


def _canonical_payload(
    *,
    certificate: ProjectionCertificate,
    claim_semantics: ClaimSemantics,
    witnesses: Iterable[EvidenceWitness],
    defeaters: Iterable[Defeater],
    support_nodes: Iterable[SupportNode],
    support_edges: Iterable[SupportEdge],
    support_target: str,
    trust_roots: Iterable[TrustRoot],
    extra_dependencies: Mapping[str, str] | None = None,
) -> dict[str, object]:
    witnesses_t = tuple(witnesses)
    defeaters_t = tuple(defeaters)
    nodes_t = tuple(support_nodes)
    edges_t = tuple(support_edges)
    roots_t = tuple(trust_roots)

    return {
        "certificate": {
            "claim_type": certificate.claim_type.value,
            "empirical_authority_requested": certificate.empirical_authority_requested,
            "records": sorted(
                (
                    record.role.value,
                    record.status.value,
                    record.note,
                )
                for record in certificate.records
            ),
        },
        "claim_semantics": {
            "describes_observation": claim_semantics.describes_observation,
            "infers_latent_state": claim_semantics.infers_latent_state,
            "infers_intervention_response": claim_semantics.infers_intervention_response,
            "asserts_target_reachability": claim_semantics.asserts_target_reachability,
        },
        "witnesses": sorted(
            {
                "witness_id": witness.witness_id,
                "role": witness.role.value,
                "source_roots": sorted(witness.source_roots),
                "obligations": {
                    "source_authenticity": witness.obligations.source_authenticity.value,
                    "claim_relevance": witness.obligations.claim_relevance.value,
                    "scope_compatibility": witness.obligations.scope_compatibility.value,
                    "transformation_reproducibility": witness.obligations.transformation_reproducibility.value,
                },
            }
            for witness in witnesses_t
        , key=lambda item: item["witness_id"]),
        "defeaters": sorted(
            {
                "defeater_id": defeater.defeater_id,
                "target_role": defeater.target_role.value,
                "status": defeater.status.value,
                "note": defeater.note,
                "resolution_witness_id": defeater.resolution_witness_id,
            }
            for defeater in defeaters_t
        , key=lambda item: item["defeater_id"]),
        "support_nodes": sorted(
            (node.node_id, node.kind.value)
            for node in nodes_t
        ),
        "support_edges": sorted(
            (edge.source, edge.target)
            for edge in edges_t
        ),
        "support_target": support_target,
        "trust_roots": sorted(
            {
                "root_id": root.root_id,
                "kind": root.kind.value,
                "assumptions": list(root.assumptions),
            }
            for root in roots_t
        , key=lambda item: item["root_id"]),
        "extra_dependencies": sorted((extra_dependencies or {}).items()),
    }


def assurance_fingerprint(
    *,
    certificate: ProjectionCertificate,
    claim_semantics: ClaimSemantics,
    witnesses: Iterable[EvidenceWitness],
    defeaters: Iterable[Defeater] = (),
    support_nodes: Iterable[SupportNode],
    support_edges: Iterable[SupportEdge],
    support_target: str,
    trust_roots: Iterable[TrustRoot],
    extra_dependencies: Mapping[str, str] | None = None,
) -> str:
    payload = _canonical_payload(
        certificate=certificate,
        claim_semantics=claim_semantics,
        witnesses=witnesses,
        defeaters=defeaters,
        support_nodes=support_nodes,
        support_edges=support_edges,
        support_target=support_target,
        trust_roots=trust_roots,
        extra_dependencies=extra_dependencies,
    )
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()
