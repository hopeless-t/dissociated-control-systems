from dissociated_control_systems.cognitive_factorized_recovery import (
    factorized_experiment,
)


def test_factorized_metrics_are_bounded():
    result = factorized_experiment()
    assert 0.0 <= result["factorized_exact_reconstruction"] <= 1.0
    assert 0.0 <= result["macro_test_accuracy"] <= 1.0
    for row in result["rows"]:
        assert 0.0 <= row["validation_accuracy"] <= 1.0
        assert 0.0 <= row["test_accuracy"] <= 1.0


def test_all_fault_dimensions_are_reported():
    result = factorized_experiment()
    assert len(result["rows"]) == 4
