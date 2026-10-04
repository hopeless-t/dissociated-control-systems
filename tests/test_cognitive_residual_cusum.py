from dissociated_control_systems.cognitive_residual_cusum import (
    residual_cusum_experiment,
)


def test_residual_cusum_metrics_are_bounded():
    result = residual_cusum_experiment()
    assert 0.0 <= result["clean_test_fpr"] <= 1.0
    for row in result["results"].values():
        assert 0.0 <= row["coverage"] <= 1.0
        assert 0.0 <= row["unsafe_accepted_error_rate"] <= 1.0
        assert 0.0 <= row["error_exposure_reduction"] <= 1.0


def test_detector_has_selected_parameters():
    result = residual_cusum_experiment()
    detector = result["detector"]
    assert detector["kappa"] > 0.0
    assert detector["threshold"] > 0.0
