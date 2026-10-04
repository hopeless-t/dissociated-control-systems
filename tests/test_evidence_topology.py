from dissociated_control_systems.evidence_topology import (
    certificate_root_cut,
    role_root_cut,
    role_root_cuts,
)
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


def good() -> WitnessObligations:
    return WitnessObligations(
        source_authenticity=ObligationStatus.PASS,
        claim_relevance=ObligationStatus.PASS,
        scope_compatibility=ObligationStatus.PASS,
        transformation_reproducibility=ObligationStatus.PASS,
    )


def w(name: str, role: CheckpointRole, *roots: str) -> EvidenceWitness:
    return EvidenceWitness(name, role, frozenset(roots), good())


def test_one_shared_root_can_destroy_all_roles_but_cut_is_still_one() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    witnesses = tuple(
        w(f"w-{role.value}", role, "shared-root")
        for role in (
            CheckpointRole.PROVENANCE,
            CheckpointRole.STATE_RESPONSE,
            CheckpointRole.UNCERTAINTY,
            CheckpointRole.REACHABILITY,
        )
    )

    assert certificate_root_cut(cert, witnesses) == 1
    assert role_root_cuts(cert, witnesses) == {
        "PROVENANCE": 1,
        "STATE_RESPONSE": 1,
        "UNCERTAINTY": 1,
        "REACHABILITY": 1,
    }


def test_two_disjoint_parallel_witnesses_raise_role_cut_to_two() -> None:
    witnesses = (
        w("p-a", CheckpointRole.PROVENANCE, "a"),
        w("p-b", CheckpointRole.PROVENANCE, "b"),
    )

    assert role_root_cut(CheckpointRole.PROVENANCE, witnesses) == 2


def test_multi_root_single_witness_is_series_dependency_cut_one() -> None:
    witnesses = (
        w(
            "pipeline-result",
            CheckpointRole.STATE_RESPONSE,
            "raw-data",
            "analysis-code",
        ),
    )

    assert role_root_cut(CheckpointRole.STATE_RESPONSE, witnesses) == 1


def test_certificate_cut_tracks_weakest_required_role() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    witnesses = (
        w("p-a", CheckpointRole.PROVENANCE, "a"),
        w("p-b", CheckpointRole.PROVENANCE, "b"),
        w("u-only", CheckpointRole.UNCERTAINTY, "u"),
    )

    assert role_root_cuts(cert, witnesses) == {
        "PROVENANCE": 2,
        "UNCERTAINTY": 1,
    }
    assert certificate_root_cut(cert, witnesses) == 1


def test_missing_usable_support_has_zero_cut() -> None:
    assert role_root_cut(CheckpointRole.REACHABILITY, ()) == 0
