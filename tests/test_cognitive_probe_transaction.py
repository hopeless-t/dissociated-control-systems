from dissociated_control_systems.cognitive_probe_transaction import (
    run_transaction,
    scenarios,
    transaction_experiment,
)


def test_response_loss_after_dispatch_never_redispatches():
    scenario = next(
        s for s in scenarios() if s.name == "lost_after_dispatch"
    )
    result = run_transaction(scenario)
    assert result.terminal == "UNKNOWN"
    assert result.dispatch_count == 1
    assert result.attempts == 4
    assert not result.duplicate_intervention


def test_invalidated_and_missing_are_not_negative_results():
    for name in ("stale_before_probe", "invalidated_mid_probe", "missing_measurement"):
        scenario = next(s for s in scenarios() if s.name == name)
        result = run_transaction(scenario)
        assert result.terminal in {"INVALIDATED", "DEFER"}
        assert result.result is None


def test_accepted_result_correctness_and_duplicate_safety():
    result = transaction_experiment()
    assert result["accepted_result_correctness"] == 1.0
    assert result["duplicate_interventions"] == 0
    assert result["naive_duplicate_intervention_scenarios"] >= 1
