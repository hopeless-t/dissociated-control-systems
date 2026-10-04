from dissociated_control_systems.cognitive_calibration_challenge import (
    evaluate_grid,
    l1_step_response_signal,
)


def test_l1_step_response_separates_canonical_states():
    healthy = l1_step_response_signal(frozenset(), 54321)
    faulty = l1_step_response_signal(frozenset(("l1_calibration",)), 54321)
    assert faulty > healthy


def test_calibration_challenge_metrics_are_bounded():
    rows = evaluate_grid(0.080, samples_per_hypothesis=4)
    for row in rows:
        assert 0.0 <= row["exact_accuracy"] <= 1.0
        assert 0.0 <= row["per_fault_accuracy"]["l1_calibration"] <= 1.0
        assert 4.0 <= row["mean_total_probes"] <= 4.0 * row[
            "max_repeats_per_dimension"
        ]
