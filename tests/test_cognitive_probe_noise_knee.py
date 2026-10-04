from dissociated_control_systems.cognitive_probe_noise_knee import (
    evaluate_level,
)


def test_fixed_five_is_actually_twenty_probes():
    result = evaluate_level(0.010, samples_per_hypothesis=4)
    assert result["fixed_five"]["mean_total_probes"] == 20.0


def test_noise_knee_policy_metrics_are_bounded():
    result = evaluate_level(0.020, samples_per_hypothesis=4)
    for policy in ("single", "sequential", "fixed_five"):
        assert 0.0 <= result[policy]["exact_accuracy"] <= 1.0
        assert 4.0 <= result[policy]["mean_total_probes"] <= 20.0
