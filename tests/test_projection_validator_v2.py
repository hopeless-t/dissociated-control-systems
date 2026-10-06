from dissociated_control_systems.projection_protocol import (
    CheckpointRecord,
    CheckpointRole,
    CheckStatus,
    ClaimType,
    ProjectionCertificate,
    canonical_trace,
)
from dissociated_control_systems.projection_validator_v2 import (
    validate_projection_certificate_v2,
)


def test_canonical_reachability_trace_still_passes() -> None:
    result = validate_projection_certificate_v2(
        canonical_trace(
            claim_type=ClaimType.REACHABILITY,
            empirical_authority_requested=True,
        )
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_irrelevant_extra_unknown_does_not_false_block_descriptive_claim() -> None:
    certificate = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.REACHABILITY, CheckStatus.UNKNOWN),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate_v2(certificate)

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_irrelevant_extra_fail_does_not_false_block_state_claim() -> None:
    certificate = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.STATE_RESPONSE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.REACHABILITY, CheckStatus.FAIL),
        ),
        claim_type=ClaimType.STATE_INFERENCE,
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate_v2(certificate)

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_duplicate_required_role_is_rejected() -> None:
    certificate = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate_v2(certificate)

    assert not result.accepted
    assert "duplicate_required_role:PROVENANCE" in result.violations


def test_required_unknown_still_blocks_empirical_authority() -> None:
    certificate = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.UNKNOWN),
            CheckpointRecord(CheckpointRole.REACHABILITY, CheckStatus.PASS),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate_v2(certificate)

    assert not result.accepted
    assert result.terminal_status is CheckStatus.UNKNOWN
