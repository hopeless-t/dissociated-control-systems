from dissociated_control_systems.cognitive_probe_budget import (
    evidence_budget_experiment,
)


def test_probe_budget_metrics_are_bounded():
    result = evidence_budget_experiment()
    for name in ("single", "fixed_five", "sequential"):
        row = result[name]
        assert 0.0 <= row["exact_accuracy"] <= 1.0
        assert 0.0 <= row["macro_bit_accuracy"] <= 1.0
        assert 4.0 <= row["mean_total_probes"] <= 20.0


def test_sequential_policy_respects_fixed_budget():
    result = evidence_budget_experiment()
    assert result["sequential"]["mean_total_probes"] <= 20.0
