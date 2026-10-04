import pytest

from dissociated_control_systems.active_probe_recovery import (
    ProbeRecoveryEvidence,
    ProbeRecoveryStatus,
    assess_probe_recovery,
)


def evidence(**overrides):
    values = dict(
        post_washout_effect=0.0,
        ci_low=-0.04,
        ci_high=0.04,
        equivalence_margin=0.1,
        sham_challenge_control=True,
        washout_interval_predeclared=True,
        same_state_proxy_remeasured=True,
        later_function_controlled=True,
    )
    values.update(overrides)
    return ProbeRecoveryEvidence(**values)


def test_equivalent_post_washout_state_passes() -> None:
    result = assess_probe_recovery(evidence())
    assert result.status is ProbeRecoveryStatus.PASS


def test_persistent_effect_outside_margin_fails() -> None:
    result = assess_probe_recovery(evidence(ci_low=0.15, ci_high=0.25))
    assert result.status is ProbeRecoveryStatus.FAIL
    assert "persistent_probe_effect_outside_equivalence_region" in result.violations


def test_boundary_overlap_is_unknown() -> None:
    result = assess_probe_recovery(evidence(ci_low=-0.04, ci_high=0.12))
    assert result.status is ProbeRecoveryStatus.UNKNOWN
    assert "post_probe_recovery_not_established" in result.violations


def test_missing_post_washout_remeasurement_blocks_pass() -> None:
    result = assess_probe_recovery(evidence(same_state_proxy_remeasured=False))
    assert result.status is ProbeRecoveryStatus.UNKNOWN


def test_missing_sham_challenge_blocks_pass() -> None:
    result = assess_probe_recovery(evidence(sham_challenge_control=False))
    assert result.status is ProbeRecoveryStatus.UNKNOWN


def test_invalid_interval_rejected() -> None:
    with pytest.raises(ValueError):
        evidence(ci_low=0.2, ci_high=-0.2)
