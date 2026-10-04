from dissociated_control_systems.cognitive_environment_confounding import (
    environment_confounding_experiment,
)


def test_raw_functional_sentinel_degrades_with_environment_shift_rate():
    result = environment_confounding_experiment()
    assert result["raw_auc_degrades_monotonically"]


def test_context_normalization_preserves_useful_auc():
    result = environment_confounding_experiment()
    assert result["normalized_min_auc"] > 0.80


def test_raw_sentinel_has_environment_pressure_knee():
    result = environment_confounding_experiment()
    assert result["raw_pressure_knee"] is not None


def test_environment_accounts_for_many_raw_false_alarms_at_high_shift_rate():
    result = environment_confounding_experiment()
    high = result["rows"][-1]
    assert high["raw_trigger"]["shifted_fraction_of_false_positives"] > 0.50
