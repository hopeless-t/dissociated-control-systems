import pytest

from dissociated_control_systems.measurement_backaction import (
    BackactionEvidence,
    BackactionStatus,
    assess_backaction,
)


def evidence(**overrides):
    values = dict(
        effect=0.0,
        ci_low=-0.05,
        ci_high=0.05,
        equivalence_margin=0.1,
        sham_controlled=True,
        environment_matched=True,
        time_matched=True,
        downstream_function_measured=True,
        dose_or_frequency_challenge=True,
    )
    values.update(overrides)
    return BackactionEvidence(**values)


def test_full_interval_inside_predeclared_margin_passes() -> None:
    result = assess_backaction(evidence())
    assert result.status is BackactionStatus.PASS
    assert result.violations == ()


def test_crossing_equivalence_boundary_is_unknown_not_pass() -> None:
    result = assess_backaction(evidence(ci_low=-0.05, ci_high=0.15))
    assert result.status is BackactionStatus.UNKNOWN
    assert "backaction_equivalence_not_established" in result.violations


def test_interval_wholly_outside_margin_fails() -> None:
    result = assess_backaction(evidence(effect=0.3, ci_low=0.2, ci_high=0.4))
    assert result.status is BackactionStatus.FAIL
    assert "effect_interval_outside_equivalence_region" in result.violations


def test_missing_sham_control_blocks_pass_even_with_small_effect_interval() -> None:
    result = assess_backaction(evidence(sham_controlled=False))
    assert result.status is BackactionStatus.UNKNOWN
    assert "missing_sham_control" in result.violations


def test_missing_frequency_challenge_blocks_pass() -> None:
    result = assess_backaction(evidence(dose_or_frequency_challenge=False))
    assert result.status is BackactionStatus.UNKNOWN


def test_invalid_confidence_interval_is_rejected() -> None:
    with pytest.raises(ValueError):
        evidence(ci_low=0.2, ci_high=-0.2)


def test_equivalence_margin_must_be_positive() -> None:
    with pytest.raises(ValueError):
        evidence(equivalence_margin=0.0)
