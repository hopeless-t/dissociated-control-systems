from dissociated_control_systems.cognitive_disagreement_trigger import (
    analytic_signed_correlation,
    disagreement_trigger_experiment,
)


def test_equal_drift_has_zero_analytic_correlation():
    assert analytic_signed_correlation(0.04, 0.04) == 0.0


def test_asymmetric_drift_has_expected_signed_correlation():
    assert abs(analytic_signed_correlation(0.04, 0.08) - 0.6) < 1e-12
    assert abs(analytic_signed_correlation(0.08, 0.04) + 0.6) < 1e-12


def test_equal_drift_disagreement_trigger_is_near_chance():
    result = disagreement_trigger_experiment()
    assert result["equal_auc_near_chance"]
    assert result["equal_signed_corr_near_zero"]


def test_asymmetry_can_create_trigger_signal():
    result = disagreement_trigger_experiment()
    assert result["asymmetry_creates_signal"]
