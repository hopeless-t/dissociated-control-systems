from dissociated_control_systems.assurance_kernel_v2 import validate_authority_v2
from dissociated_control_systems.assurance_versioning import DependencySnapshot
from dissociated_control_systems.claim_semantics import ClaimSemantics
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
    semantics = ClaimSemantics(describes_observation=True)
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
    return certificate, semantics, witnesses, nodes, edges, snapshot, current, roots


def run_fixture(
    *,
    certificate=None,
    semantics=None,
    witnesses=None,
    nodes=None,
    edges=None,
    snapshot=None,
    current=None,
    roots=None,
):
    base = fixture()
    return validate_authority_v2(
        certificate=base[0] if certificate is None else certificate,
        claim_semantics=base[1] if semantics is None else semantics,
        witnesses=base[2] if witnesses is None else witnesses,
        support_nodes=base[3] if nodes is None else nodes,
        support_edges=base[4] if edges is None else edges,
        support_target="claim",
        dependency_snapshot=base[5] if snapshot is None else snapshot,
        current_revisions=base[6] if current is None else current,
        trust_roots=base[7] if roots is None else roots,
    )


def test_complete_kernel_path_accepts() -> None:
    result = run_fixture()
    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_reachability_semantics_cannot_use_descriptive_certificate() -> None:
    result = run_fixture(
        semantics=ClaimSemantics(asserts_target_reachability=True),
    )

    assert not result.accepted
    assert any(
        violation.startswith("claim_type_semantic_mismatch:")
        for violation in result.violations
    )


def test_stale_dependency_blocks_current_authority() -> None:
    base = fixture()
    current = dict(base[6])
    current["kernel"] = "git:kernel-v3"

    result = run_fixture(current=current)

    assert not result.accepted
    assert result.terminal_status is CheckStatus.UNKNOWN
    assert "stale_dependency_changed:kernel" in result.violations


def test_missing_trust_root_blocks_authority() -> None:
    base = fixture()
    result = run_fixture(roots=base[7][:1])

    assert not result.accepted
    assert "missing_trust_root:audit-data" in result.violations


def test_cycle_blocks_authority_even_with_primitive_inputs_present() -> None:
    base = fixture()
    cyclic_nodes = base[3] + (
        SupportNode("derived", SupportNodeKind.DERIVED_EVIDENCE),
    )
    cyclic_edges = base[4] + (
        SupportEdge("claim", "derived"),
        SupportEdge("derived", "claim"),
    )

    result = run_fixture(nodes=cyclic_nodes, edges=cyclic_edges)

    assert not result.accepted
    assert "cyclic_support_graph" in result.violations


def test_witness_root_missing_from_support_graph_blocks_authority() -> None:
    base = fixture()
    bad_witnesses = base[2] + (
        EvidenceWitness(
            "extra",
            CheckpointRole.PROVENANCE,
            frozenset({"undeclared-root"}),
            good(),
        ),
    )

    result = run_fixture(witnesses=bad_witnesses)

    assert not result.accepted
    assert (
        "witness_root_missing_from_support_graph:undeclared-root"
        in result.violations
    )


def test_orphan_support_node_cannot_be_used_as_witness_root() -> None:
    base = fixture()
    orphan_nodes = base[3] + (
        SupportNode("orphan", SupportNodeKind.PRIMITIVE_EVIDENCE),
    )
    bad_witnesses = base[2] + (
        EvidenceWitness(
            "orphan-witness",
            CheckpointRole.PROVENANCE,
            frozenset({"orphan"}),
            good(),
        ),
    )

    result = run_fixture(nodes=orphan_nodes, witnesses=bad_witnesses)

    assert not result.accepted
    assert "witness_root_not_ancestor_of_claim:orphan" in result.violations


def test_claim_node_cannot_be_used_as_witness_root() -> None:
    base = fixture()
    bad_witnesses = base[2] + (
        EvidenceWitness(
            "claim-as-evidence",
            CheckpointRole.PROVENANCE,
            frozenset({"claim"}),
            good(),
        ),
    )

    result = run_fixture(witnesses=bad_witnesses)

    assert not result.accepted
    assert "witness_root_is_claim:claim" in result.violations


def test_duplicate_support_node_id_fails_closed() -> None:
    base = fixture()
    duplicate_nodes = base[3] + (
        SupportNode("raw-data", SupportNodeKind.DERIVED_EVIDENCE),
    )

    result = run_fixture(nodes=duplicate_nodes)

    assert not result.accepted
    assert "duplicate_support_node:raw-data" in result.violations


def test_invalid_support_edge_fails_closed_instead_of_crashing() -> None:
    base = fixture()
    invalid_edges = base[4] + (
        SupportEdge("missing-node", "claim"),
    )

    result = run_fixture(edges=invalid_edges)

    assert not result.accepted
    assert any(
        violation.startswith("invalid_support_graph:")
        for violation in result.violations
    )
