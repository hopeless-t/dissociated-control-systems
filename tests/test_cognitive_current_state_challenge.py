from dissociated_control_systems.cognitive_current_state_challenge import (
    current_state_challenge_experiment,
)


def test_current_state_metrics_are_bounded():
    result = current_state_challenge_experiment()
    for row in result["rows"]:
        metrics = row["heldout_metrics"]
        if metrics is None:
            continue
        assert 0.0 <= metrics["sensitivity"] <= 1.0
        assert 0.0 <= metrics["specificity"] <= 1.0
        assert 0.0 <= metrics["precision"] <= 1.0
        assert 0.0 <= metrics["selection_rate"] <= 1.0


def test_current_state_challenge_improves_over_fault_partition_ppv():
    result = current_state_challenge_experiment()
    assert result["best_research"]["heldout_metrics"]["precision"] > 0.0175


def test_all_trial_counts_are_evaluated():
    result = current_state_challenge_experiment()
    assert {row["trials"] for row in result["rows"]} == {8, 16, 32, 64, 128}
