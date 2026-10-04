from dissociated_control_systems.cognitive_evidence_frontier import (
    REPEAT_BUDGETS,
    summarize_level,
)


def test_budget_curve_has_declared_budgets():
    result = summarize_level(0.010, samples_per_hypothesis=3)
    assert [
        row["repeats_per_dimension"]
        for row in result["rows"]
    ] == list(REPEAT_BUDGETS)


def test_total_probe_count_matches_fixed_budget():
    result = summarize_level(0.020, samples_per_hypothesis=3)
    for row in result["rows"]:
        assert row["total_probes"] == 4 * row["repeats_per_dimension"]
