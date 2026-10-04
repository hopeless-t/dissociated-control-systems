from dissociated_control_systems.cognitive_active_diagnosis import (
    diagnose_adaptive,
    evaluate,
    hypotheses,
    train_templates,
)
from dissociated_control_systems.cognitive_harness_repair import run_episode


def test_hypothesis_space_covers_all_fault_subsets():
    assert len(hypotheses()) == 16


def test_adaptive_diagnosis_can_stop_before_all_probes():
    templates = train_templates(samples=50)
    features = run_episode(frozenset(), 42, steps=60).features
    _, _, cost, count = diagnose_adaptive(
        features,
        templates,
        confidence_threshold=0.80,
        cost_weight=0.50,
    )
    assert count <= 4
    assert cost <= 1.0


def test_adaptive_policy_reduces_probe_cost_with_small_accuracy_loss():
    result = evaluate(samples=30)
    assert (
        result["adaptive"]["mean_probe_cost"]
        < result["all_probes"]["mean_probe_cost"] * 0.85
    )
    assert (
        result["adaptive"]["exact_accuracy"]
        >= result["all_probes"]["exact_accuracy"] - 0.08
    )
    assert result["adaptive"]["mean_extra_repairs"] < 0.20
