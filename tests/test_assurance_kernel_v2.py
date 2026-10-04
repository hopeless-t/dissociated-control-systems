from dissociated_control_systems.assurance_kernel_v2 import validate_authority_v2
from dissociated_control_systems.assurance_versioning import DependencySnapshot
from dissociated_control_systems.projection_assurance import (
    EvidenceWitness,
    ObligationStatus,
    WitnessObligations,
)
from dissociated_control_systems.projection_protocol import (
    CheckStatus,
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
    certificate = canonical_trace(
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    witnesses = (
        EvidenceWitness(
            "prov",
            CheckpointRole.PROVENANCE,
            frozenset({"raw-data"}),
            good(),
        ),
        EvidenceWitness(
            "unc",
            CheckpointRole.UNCERTAINTY,
            frozenset({"audit-data"}),
            good(),
        ),
    )
    nodes = (
        SupportNode("raw-data", SupportNodeKind.PRIMITIVE_EVIDENCE),
        SupportNode("audit-data", SupportNodeKind.PRIMITIVE_EVIDENCE),
        SupportNode("claim", SupportNodeKind.CLAIM),
    )
    edges = (
        SupportEdge("raw-data", "claim"),
        SupportEdge("audit-data", "claim"),
    )
    snapshot = DependencySnapshot.from_mapping(
        {
            "raw-data": "sha:raw-v1",
            "audit-data": "sha:audit-v1",
            "kernel": "git:kernel-v2",
        }
    )
    current = {
        "raw-data": "sha:raw-v1",
        "audit-data": "sha:audit-v1",
        "kernel": "git:kernel-v2",
    }
    roots = (
        TrustRoot(
            "raw-data",
            TrustRootKind.RAW_OBSERVATION,
            ("bytes correspond to the declared raw dataset",),
        ),
        TrustRoot(
            "audit-data",
            TrustRootKind.RAW_OBSERVATION,
            ("audit bytes correspond to the declared observation",),
        ),
    )
    return certificate, witnesses, nodes, edges, snapshot, current, roots


def test_complete_kernel_path_accepts() -> None:
    certificate, witnesses, nodes, edges, snapshot, current, roots = fixture()

    result = validate_authority_v2(
        certificate=certificate,
        witnesses=witnesses,
        support_nodes=nodes,
        support_edges=edges,
        support_target="claim",
        dependency_snapshot=snapshot,
        current_revisions=current,
        trust_roots=roots,
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_stale_dependency_blocks_current_authority() -> None:
    certificate, witnesses, nodes, edges, snapshot, current, roots = fixture()
    current["kernel"] = "git:kernel-v3"

    result = validate_authority_v2(
        certificate=certificate,
        witnesses=witnesses,
        support_nodes=nodes,
        support_edges=edges,
        support_target="claim",
        dependency_snapshot=snapshot,
        current_revisions=current,
        trust_roots=roots,
    )

    assert not result.accepted
    assert result.terminal_status is CheckStatus.UNKNOWN
    assert "stale_dependency_changed:kernel" in result.violations


def test_missing_trust_root_blocks_authority() -> None:
    certificate, witnesses, nodes, edges, snapshot, current, roots = fixture()

    result = validate_authority_v2(
        certificate=certificate,
        witnesses=witnesses,
        support_nodes=nodes,
        support_edges=edges,
        support_target="claim",
        dependency_snapshot=snapshot,
        current_revisions=current,
        trust_roots=roots[:1],
    )

    assert not result.accepted
    assert "missing_trust_root:audit-data" in result.violations


def test_cycle_blocks_authority_even_with_primitive_inputs_present() -> None:
    certificate, witnesses, nodes, edges, snapshot, current, roots = fixture()
    cyclic_nodes = nodes + (
        SupportNode("derived", SupportNodeKind.DERIVED_EVIDENCE),
    )
    cyclic_edges = edges + (
        SupportEdge("claim", "derived"),
        SupportEdge("derived", "claim"),
    )

    result = validate_authority_v2(
        certificate=certificate,
        witnesses=witnesses,
        support_nodes=cyclic_nodes,
        support_edges=cyclic_edges,
        support_target="claim",
        dependency_snapshot=snapshot,
        current_revisions=current,
        trust_roots=roots,
    )

    assert not result.accepted
    assert "cyclic_support_graph" in result.violations


def test_witness_root_missing_from_support_graph_blocks_authority() -> None:
    certificate, witnesses, nodes, edges, snapshot, current, roots = fixture()
    bad_witnesses = witnesses + (
        EvidenceWitness(
            "extra",
            CheckpointRole.PROVENANCE,
            frozenset({"undeclared-root"}),
            good(),
        ),
    )

    result = validate_authority_v2(
        certificate=certificate,
        witnesses=bad_witnesses,
        support_nodes=nodes,
        support_edges=edges,
        support_target="claim",
        dependency_snapshot=snapshot,
        current_revisions=current,
        trust_roots=roots,
    )

    assert not result.accepted
    assert (
        "witness_root_missing_from_support_graph:undeclared-root"
        in result.violations
    )


def test_claim_node_cannot_be_used_as_witness_root() -> None:
    certificate, witnesses, nodes, edges, snapshot, current, roots = fixture()
    bad_witnesses = witnesses + (
        EvidenceWitness(
            "claim-as-evidence",
            CheckpointRole.PROVENANCE,
            frozenset({"claim"}),
            good(),
        ),
    )

    result = validate_authority_v2(
        certificate=certificate,
        witnesses=bad_witnesses,
        support_nodes=nodes,
        support_edges=edges,
        support_target="claim",
        dependency_snapshot=snapshot,
        current_revisions=current,
        trust_roots=roots,
    )

    assert not result.accepted
    assert "witness_root_is_claim:claim" in result.violations
