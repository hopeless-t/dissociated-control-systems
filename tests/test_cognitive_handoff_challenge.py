from dissociated_control_systems.cognitive_handoff_challenge import (
    evaluate_redesigned_grid,
    l2_controlled_input_signal,
)


def test_l2_controlled_input_signal_separates_canonical_states():
    healthy = l2_controlled_input_signal(frozenset(), 12345)
    faulty = l2_controlled_input_signal(frozenset(("l2_handoff",)), 12345)
    assert faulty > healthy


def test_redesigned_grid_metrics_are_bounded():
    rows = evaluate_redesigned_grid(0.040, samples_per_hypothesis=4)
    for row in rows:
        assert 0.0 <= row["exact_accuracy"] <= 1.0
        assert 0.0 <= row["per_fault_accuracy"]["l2_handoff"] <= 1.0
        assert 4.0 <= row["mean_total_probes"] <= 4.0 * row[
            "max_repeats_per_dimension"
        ]
