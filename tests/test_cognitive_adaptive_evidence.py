from dissociated_control_systems.cognitive_adaptive_evidence import (
    evaluate_adaptive_grid,
)


def test_adaptive_evidence_metrics_are_bounded():
    rows = evaluate_adaptive_grid(0.020, samples_per_hypothesis=4)
    for row in rows:
        assert 0.0 <= row["exact_accuracy"] <= 1.0
        assert 0.0 <= row["macro_bit_accuracy"] <= 1.0
        assert 4.0 <= row["mean_total_probes"] <= 4.0 * row[
            "max_repeats_per_dimension"
        ]


def test_adaptive_mean_probe_count_is_monotone_with_cap():
    rows = evaluate_adaptive_grid(0.040, samples_per_hypothesis=4)
    probes = [row["mean_total_probes"] for row in rows]
    assert probes == sorted(probes)
