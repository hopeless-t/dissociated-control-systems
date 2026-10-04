from dissociated_control_systems.cognitive_restoration import (
    restoration_experiment,
)


def test_restoration_curve_is_ordered_by_calibration_size():
    result = restoration_experiment()
    sizes = [row["samples_per_hypothesis"] for row in result["rows"]]
    assert sizes == sorted(sizes)


def test_restoration_metrics_are_bounded():
    result = restoration_experiment()
    assert 0.0 <= result["frozen_test_accuracy"] <= 1.0
    for row in result["rows"]:
        assert 0.0 <= row["validation_accuracy"] <= 1.0
        assert 0.0 <= row["test_accuracy"] <= 1.0
        assert isinstance(row["restore_authorized"], bool)
