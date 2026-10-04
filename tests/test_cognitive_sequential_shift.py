from dissociated_control_systems.cognitive_sequential_shift import (
    sequential_experiment,
)


def test_sequential_metrics_are_bounded():
    result = sequential_experiment()
    for row in result["results"].values():
        assert 0.0 <= row["coverage"] <= 1.0
        assert 0.0 <= row["unsafe_accepted_error_rate"] <= 1.0
        assert 0.0 <= row["error_exposure_reduction"] <= 1.0


def test_clean_sequence_false_alarm_is_bounded():
    result = sequential_experiment()
    assert 0.0 <= result["clean_sequence_fpr"] <= 1.0
