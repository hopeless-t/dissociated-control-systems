from dissociated_control_systems.assurance_fingerprint import assurance_fingerprint
from dissociated_control_systems.claim_semantics import ClaimSemantics
from dissociated_control_systems.projection_assurance import (
    EvidenceWitness,
    ObligationStatus,
    WitnessObligations,
)
from dissociated_control_systems.projection_protocol import (
    CheckpointRole,
    ClaimType,
    canonical_trace,
)
from dissociated_control_systems.support_graph import (
    SupportEdge,
    SupportNode,
    SupportNodeKind,
)
from dissociated_control_systems.trust_roots import TrustRoot, TrustRootKind


def good() -> WitnessObligations:
    return WitnessObligations(
        source_authenticity=ObligationStatus.PASS,
        claim_relevance=ObligationStatus.PASS,
        scope_compatibility=ObligationStatus.PASS,
        transformation_reproducibility=ObligationStatus.PASS,
    )


def fixture():
    return {
        "certificate": canonical_trace(
            claim_type=ClaimType.DESCRIPTIVE,
            empirical_authority_requested=True,
        ),
        "claim_semantics": ClaimSemantics(describes_observation=True),
        "witnesses": (
            EvidenceWitness(
                "prov",
                CheckpointRole.PROVENANCE,
                frozenset({"raw"}),
                good(),
            ),
            EvidenceWitness(
                "unc",
                CheckpointRole.UNCERTAINTY,
                frozenset({"audit"}),
                good(),
            ),
        ),
        "support_nodes": (
            SupportNode("raw", SupportNodeKind.PRIMITIVE_EVIDENCE),
            SupportNode("audit", SupportNodeKind.PRIMITIVE_EVIDENCE),
            SupportNode("claim", SupportNodeKind.CLAIM),
        ),
        "support_edges": (
            SupportEdge("raw", "claim"),
            SupportEdge("audit", "claim"),
        ),
        "support_target": "claim",
        "trust_roots": (
            TrustRoot(
                "raw",
                TrustRootKind.RAW_OBSERVATION,
                ("raw bytes correspond to declared source",),
            ),
            TrustRoot(
                "audit",
                TrustRootKind.RAW_OBSERVATION,
                ("audit bytes correspond to declared source",),
            ),
        ),
    }


def test_fingerprint_is_order_invariant_for_set_like_inputs() -> None:
    payload = fixture()
    first = assurance_fingerprint(**payload)

    payload["witnesses"] = tuple(reversed(payload["witnesses"]))
    payload["support_nodes"] = tuple(reversed(payload["support_nodes"]))
    payload["support_edges"] = tuple(reversed(payload["support_edges"]))
    payload["trust_roots"] = tuple(reversed(payload["trust_roots"]))
    second = assurance_fingerprint(**payload)

    assert first == second


def test_claim_semantic_change_changes_fingerprint() -> None:
    payload = fixture()
    first = assurance_fingerprint(**payload)
    payload["claim_semantics"] = ClaimSemantics(infers_latent_state=True)
    second = assurance_fingerprint(**payload)

    assert first != second


def test_trust_assumption_change_changes_fingerprint() -> None:
    payload = fixture()
    first = assurance_fingerprint(**payload)
    payload["trust_roots"] = (
        TrustRoot(
            "raw",
            TrustRootKind.RAW_OBSERVATION,
            ("CHANGED assumption",),
        ),
        payload["trust_roots"][1],
    )
    second = assurance_fingerprint(**payload)

    assert first != second


def test_witness_obligation_change_changes_fingerprint() -> None:
    payload = fixture()
    first = assurance_fingerprint(**payload)
    payload["witnesses"] = (
        EvidenceWitness(
            "prov",
            CheckpointRole.PROVENANCE,
            frozenset({"raw"}),
            WitnessObligations(
                source_authenticity=ObligationStatus.PASS,
                claim_relevance=ObligationStatus.UNKNOWN,
                scope_compatibility=ObligationStatus.PASS,
                transformation_reproducibility=ObligationStatus.PASS,
            ),
        ),
        payload["witnesses"][1],
    )
    second = assurance_fingerprint(**payload)

    assert first != second


def test_extra_dependency_change_changes_fingerprint() -> None:
    payload = fixture()
    first = assurance_fingerprint(
        **payload,
        extra_dependencies={"kernel": "v2"},
    )
    second = assurance_fingerprint(
        **payload,
        extra_dependencies={"kernel": "v3"},
    )

    assert first != second
