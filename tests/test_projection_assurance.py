import pytest

from dissociated_control_systems.projection_assurance import (
    Defeater,
    DefeaterStatus,
    EvidenceWitness,
    ObligationStatus,
    WitnessObligations,
    root_blast_radius,
    validate_evidence_bound_certificate,
)
from dissociated_control_systems.projection_protocol import (
    CheckStatus,
    CheckpointRole,
    ClaimType,
    canonical_trace,
)


def _good_obligations() -> WitnessObligations:
    return WitnessObligations(
        source_authenticity=ObligationStatus.PASS,
        claim_relevance=ObligationStatus.PASS,
        scope_compatibility=ObligationStatus.PASS,
        transformation_reproducibility=ObligationStatus.PASS,
    )


def _witness(witness_id: str, role: CheckpointRole, root: str) -> EvidenceWitness:
    return EvidenceWitness(
        witness_id,
        role,
        frozenset({root}),
        _good_obligations(),
    )


def _full_reachability_witnesses():
    return (
        _witness("w-prov", CheckpointRole.PROVENANCE, "src-prov"),
        _witness("w-state", CheckpointRole.STATE_RESPONSE, "src-state"),
        _witness("w-unc", CheckpointRole.UNCERTAINTY, "src-unc"),
        _witness("w-reach", CheckpointRole.REACHABILITY, "src-reach"),
    )


def test_syntactic_pass_without_witness_is_rejected() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    result = validate_evidence_bound_certificate(cert, witnesses=())

    assert not result.accepted
    assert "pass_without_usable_witness:PROVENANCE" in result.violations
    assert "pass_without_usable_witness:REACHABILITY" in result.violations


def test_usable_witness_per_required_pass_role_is_accepted() -> None:
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


def test_authentic_but_irrelevant_witness_cannot_support_pass() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    irrelevant = EvidenceWitness(
        "authentic-but-irrelevant",
        CheckpointRole.PROVENANCE,
        frozenset({"paper-1"}),
        WitnessObligations(
            source_authenticity=ObligationStatus.PASS,
            claim_relevance=ObligationStatus.FAIL,
            scope_compatibility=ObligationStatus.PASS,
            transformation_reproducibility=ObligationStatus.PASS,
        ),
    )
    uncertainty = _witness("uncertainty", CheckpointRole.UNCERTAINTY, "analysis-1")

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=(irrelevant, uncertainty),
    )

    assert not result.accepted
    assert "pass_without_usable_witness:PROVENANCE" in result.violations


def test_scope_unknown_witness_cannot_support_empirical_pass() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    witness = EvidenceWitness(
        "scope-unknown",
        CheckpointRole.PROVENANCE,
        frozenset({"paper-1"}),
        WitnessObligations(
            source_authenticity=ObligationStatus.PASS,
            claim_relevance=ObligationStatus.PASS,
            scope_compatibility=ObligationStatus.UNKNOWN,
            transformation_reproducibility=ObligationStatus.PASS,
        ),
    )
    uncertainty = _witness("uncertainty", CheckpointRole.UNCERTAINTY, "analysis-1")

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=(witness, uncertainty),
    )

    assert not result.accepted


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


def test_resolved_defeater_requires_resolution_witness() -> None:
    with pytest.raises(ValueError):
        Defeater(
            "d-reach-1",
            CheckpointRole.REACHABILITY,
            DefeaterStatus.RESOLVED,
        )


def test_residual_defeater_requires_explicit_rationale() -> None:
    with pytest.raises(ValueError):
        Defeater(
            "d-reach-1",
            CheckpointRole.REACHABILITY,
            DefeaterStatus.RESIDUAL,
        )


def test_fake_resolution_witness_id_does_not_close_defeater() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    defeater = Defeater(
        "d-reach-1",
        CheckpointRole.REACHABILITY,
        DefeaterStatus.RESOLVED,
        resolution_witness_id="missing-witness",
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=_full_reachability_witnesses(),
        defeaters=(defeater,),
    )

    assert not result.accepted
    assert (
        "resolved_defeater_without_usable_resolution_witness:d-reach-1"
        in result.violations
    )


def test_resolved_defeater_with_registered_usable_witness_does_not_block_pass() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.REACHABILITY,
        empirical_authority_requested=True,
    )
    defeater = Defeater(
        "d-reach-1",
        CheckpointRole.REACHABILITY,
        DefeaterStatus.RESOLVED,
        resolution_witness_id="w-reach",
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=_full_reachability_witnesses(),
        defeaters=(defeater,),
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_residual_doubt_is_visible_but_does_not_silently_disappear() -> None:
    cert = canonical_trace(
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    defeater = Defeater(
        "d-scope-1",
        CheckpointRole.UNCERTAINTY,
        DefeaterStatus.RESIDUAL,
        note="small cohort remains a declared residual limitation",
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=(
            _witness("p", CheckpointRole.PROVENANCE, "source"),
            _witness("u", CheckpointRole.UNCERTAINTY, "analysis"),
        ),
        defeaters=(defeater,),
    )

    assert result.accepted
    assert any(
        warning == "residual_doubt:d-scope-1:UNCERTAINTY"
        for warning in result.warnings
    )


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
            _good_obligations(),
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
        _witness("p-a", CheckpointRole.PROVENANCE, "a"),
        _witness("p-b", CheckpointRole.PROVENANCE, "b"),
        _witness("u-a", CheckpointRole.UNCERTAINTY, "c"),
        _witness("u-b", CheckpointRole.UNCERTAINTY, "d"),
    )

    assert root_blast_radius(cert, witnesses) == {
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
    }
