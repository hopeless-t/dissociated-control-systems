from dissociated_control_systems.cognitive_regime_shift import (
    regime_shift_experiment,
)


def test_regime_shift_metrics_are_bounded():
    result = regime_shift_experiment()
    for row in result["results"].values():
        assert 0.0 <= row["window_flag_rate"] <= 1.0
        assert 0.0 <= row["coverage"] <= 1.0
        assert 0.0 <= row["unsafe_accepted_error_rate"] <= 1.0
        assert 0.0 <= row["error_exposure_reduction"] <= 1.0


def test_clean_false_alarm_is_not_catastrophic():
    result = regime_shift_experiment()
    assert result["clean_window_false_alarm"] < 0.20
