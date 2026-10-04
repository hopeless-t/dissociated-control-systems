from dissociated_control_systems.cognitive_intervention_probe import (
    intervention_probe_experiment,
)


def test_intervention_probe_metrics_are_bounded():
    result = intervention_probe_experiment()
    assert 0.0 <= result["exact_reconstruction"] <= 1.0
    assert 0.0 <= result["macro_accuracy"] <= 1.0
    for row in result["rows"]:
        assert 0.0 <= row["test_accuracy"] <= 1.0
        assert 0.0 <= row["sensitivity"] <= 1.0
        assert 0.0 <= row["specificity"] <= 1.0


def test_all_fault_dimensions_receive_a_probe():
    result = intervention_probe_experiment()
    assert len(result["rows"]) == 4
