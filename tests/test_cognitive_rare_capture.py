from dissociated_control_systems.cognitive_rare_capture import (
    capture_policy_experiment,
)


def test_causal_capture_uses_less_than_biopsy_all():
    result = capture_policy_experiment()
    assert result["causal"]["biopsy_count"] < result["all"]["biopsy_count"]


def test_random_baseline_has_same_budget_as_causal():
    result = capture_policy_experiment()
    assert result["random"]["biopsy_count"] == result["causal"]["biopsy_count"]


def test_capture_metrics_are_bounded():
    result = capture_policy_experiment()
    for name in ("all", "random", "causal", "oracle"):
        row = result[name]
        assert 0.0 <= row["biopsy_fraction"] <= 1.0
        assert 0.0 <= row["rare_recall"] <= 1.0
        assert 0.0 <= row["biopsy_precision"] <= 1.0
