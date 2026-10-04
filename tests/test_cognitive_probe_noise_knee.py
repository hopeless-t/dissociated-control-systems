from dissociated_control_systems.cognitive_probe_noise_knee import (
    noise_knee_experiment,
)


def test_fixed_five_is_actually_twenty_probes():
    result = noise_knee_experiment()
    for row in result["rows"]:
        assert row["fixed_five"]["mean_total_probes"] == 20.0


def test_noise_knee_metrics_are_bounded():
    result = noise_knee_experiment()
    for row in result["rows"]:
        for policy in ("single", "sequential", "fixed_five"):
            assert 0.0 <= row[policy]["exact_accuracy"] <= 1.0
            assert 4.0 <= row[policy]["mean_total_probes"] <= 20.0
