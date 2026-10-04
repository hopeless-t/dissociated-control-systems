from dissociated_control_systems.cognitive_external_evidence_allocator import (
    BUDGETS,
    evidence_allocator_experiment,
    exhaustive_optimum,
    ratio_allocation,
    trace_mse,
)


def test_ratio_candidate_matches_exhaustive_optimum():
    for budget in BUDGETS:
        assert ratio_allocation(budget) == exhaustive_optimum(budget)


def test_optimum_beats_or_matches_frozen_baselines():
    result = evidence_allocator_experiment()
    for row in result["rows"]:
        assert row["optimum_mse"] <= row["equal_mse"]
        assert row["optimum_mse"] <= row["objective_pressure_mse"]


def test_trace_mse_rejects_missing_channel():
    try:
        trace_mse((4, 1, 1, 0))
    except ValueError:
        pass
    else:
        raise AssertionError("zero-observation channel must be rejected")


def test_continuous_ratio_is_four_to_one():
    result = evidence_allocator_experiment()["continuous_ratio"]
    assert result == {
        "objective": 4.0,
        "self": 1.0,
        "informant": 1.0,
        "function": 1.0,
    }
