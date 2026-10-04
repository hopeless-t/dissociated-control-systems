from dissociated_control_systems.cognitive_two_stage_cascade import (
    cascade_experiment,
)


def test_cascade_reduces_expensive_challenge_coverage():
    result = cascade_experiment()
    assert result["heldout_causal_candidates"] < result["heldout_total"]


def test_cascade_metrics_are_bounded():
    result = cascade_experiment()
    for row in result["results"]:
        metrics = row["metrics"]
        if metrics is None:
            continue
        for key in (
            "sensitivity",
            "specificity",
            "precision",
            "selection_rate",
            "challenge_fraction",
        ):
            assert 0.0 <= metrics[key] <= 1.0


def test_both_policy_families_present():
    result = cascade_experiment()
    assert {row["name"] for row in result["results"]} == {
        "current_state_only",
        "causal_then_current_state",
    }
