from dissociated_control_systems.projection_assurance import (
    Defeater,
    DefeaterStatus,
    EvidenceWitness,
    root_blast_radius,
    validate_evidence_bound_certificate,
)
from dissociated_control_systems.projection_protocol import (
    CheckStatus,
    CheckpointRole,
    ClaimType,
    canonical_trace,
)


def _full_reachability_witnesses():
    return (
        EvidenceWitness("w-prov", CheckpointRole.PROVENANCE, frozenset({"src-prov"})),
        EvidenceWitness("w-state", CheckpointRole.STATE_RESPONSE, frozenset({"src-state"})),
        EvidenceWitness("w-unc", CheckpointRole.UNCERTAINTY, frozenset({"src-unc"})),
        EvidenceWitness("w-reach", CheckpointRole.REACHABILITY, frozenset({"src-reach"})),
    )


def test_syntactic_pass_without_witness_is_rejected() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )

    result = validate_evidence_bound_certificate(cert, witnesses=())

    assert not result.accepted
    assert "pass_without_verified_witness:PROVENANCE" in result.violations
    assert "pass_without_verified_witness:REACHABILITY" in result.violations


def test_verified_witness_per_required_pass_role_is_accepted() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=_full_reachability_witnesses(),
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_open_defeater_downgrades_pass_to_unknown() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    defeater = Defeater(
        "d-reach-1",
        CheckpointRole.REACHABILITY,
        DefeaterStatus.OPEN,
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=_full_reachability_witnesses(),
        defeaters=(defeater,),
    )

    assert not result.accepted
    assert result.terminal_status is CheckStatus.UNKNOWN
    assert "open_defeater_blocks_empirical_pass" in result.violations


def test_resolved_defeater_does_not_block_pass() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    defeater = Defeater(
        "d-reach-1",
        CheckpointRole.REACHABILITY,
        DefeaterStatus.RESOLVED,
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=_full_reachability_witnesses(),
        defeaters=(defeater,),
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_shared_root_is_reported_as_common_mode_dependency() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    witnesses = tuple(
        EvidenceWitness(
            f"w-{role.value}",
            role,
            frozenset({"single-root"}),
        )
        for role in (
            CheckpointRole.PROVENANCE,
            CheckpointRole.STATE_RESPONSE,
            CheckpointRole.UNCERTAINTY,
            CheckpointRole.REACHABILITY,
        )
    )

    blast = root_blast_radius(cert, witnesses)
    result = validate_evidence_bound_certificate(cert, witnesses)

    assert blast["single-root"] == 4
    assert any(
        warning == "common_mode_root:single-root:loses_4_of_4_roles"
        for warning in result.warnings
    )


def test_independent_duplicate_witnesses_remove_single_root_blast() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    witnesses = (
        EvidenceWitness("p-a", CheckpointRole.PROVENANCE, frozenset({"a"})),
        EvidenceWitness("p-b", CheckpointRole.PROVENANCE, frozenset({"b"})),
        EvidenceWitness("u-a", CheckpointRole.UNCERTAINTY, frozenset({"c"})),
        EvidenceWitness("u-b", CheckpointRole.UNCERTAINTY, frozenset({"d"})),
    )

    assert root_blast_radius(cert, witnesses) == {
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
    }
