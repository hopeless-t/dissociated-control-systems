from dissociated_control_systems.projection_protocol import (
    CheckpointRecord,
    CheckpointRole,
    CheckStatus,
    ProjectionCertificate,
    canonical_trace,
    validate_projection_certificate,
)


def test_complete_ordered_trace_is_accepted() -> None:
    result = validate_projection_certificate(
        canonical_trace(empirical_authority_requested=True)
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS
    assert result.violations == ()


def test_missing_uncertainty_barrier_rejects_shortcut() -> None:
    certificate = ProjectionCertificate(
        records=(
            CheckpointRecord(
                CheckpointRole.PROVENANCE,
                CheckStatus.PASS,
            ),
            CheckpointRecord(
                CheckpointRole.STATE_RESPONSE,
                CheckStatus.PASS,
            ),
            CheckpointRecord(
                CheckpointRole.REACHABILITY,
                CheckStatus.PASS,
            ),
        ),
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate(certificate)

    assert not result.accepted
    assert "missing_required_role:UNCERTAINTY" in result.violations


def test_reordered_roles_do_not_count_as_protocol_completion() -> None:
    certificate = ProjectionCertificate(
        records=(
            CheckpointRecord(
                CheckpointRole.UNCERTAINTY,
                CheckStatus.PASS,
            ),
            CheckpointRecord(
                CheckpointRole.PROVENANCE,
                CheckStatus.PASS,
            ),
            CheckpointRecord(
                CheckpointRole.STATE_RESPONSE,
                CheckStatus.PASS,
            ),
            CheckpointRecord(
                CheckpointRole.REACHABILITY,
                CheckStatus.PASS,
            ),
        ),
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate(certificate)

    assert not result.accepted
    assert "required_roles_out_of_order" in result.violations


def test_unknown_propagates_to_terminal_status() -> None:
    result = validate_projection_certificate(
        canonical_trace(
            (
                CheckStatus.PASS,
                CheckStatus.PASS,
                CheckStatus.UNKNOWN,
                CheckStatus.UNKNOWN,
            )
        )
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.UNKNOWN


def test_unknown_cannot_be_upgraded_to_empirical_claim() -> None:
    result = validate_projection_certificate(
        canonical_trace(
            (
                CheckStatus.PASS,
                CheckStatus.PASS,
                CheckStatus.UNKNOWN,
                CheckStatus.UNKNOWN,
            ),
            empirical_authority_requested=True,
        )
    )

    assert not result.accepted
    assert (
        "empirical_authority_requires_all_required_checks_pass"
        in result.violations
    )


def test_failure_dominates_terminal_status() -> None:
    result = validate_projection_certificate(
        canonical_trace(
            (
                CheckStatus.PASS,
                CheckStatus.FAIL,
                CheckStatus.PASS,
                CheckStatus.PASS,
            )
        )
    )

    assert result.accepted
    assert result.terminal_status is CheckStatus.FAIL
