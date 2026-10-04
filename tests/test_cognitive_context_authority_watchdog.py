from dissociated_control_systems.cognitive_context_authority_watchdog import (
    MAX_EPOCH_SELECTION_REGRET,
    context_authority_watchdog_experiment,
)


def test_watchdog_preserves_frozen_regret_contract():
    result = context_authority_watchdog_experiment()
    watchdog = result["watchdog"]
    assert watchdog["contract_pass"]
    assert watchdog["max_regret"] <= MAX_EPOCH_SELECTION_REGRET
    assert watchdog["stale_authority_epochs"] == 0


def test_watchdog_reduces_full_qualification_work_vs_lease1():
    result = context_authority_watchdog_experiment()
    assert result["watchdog"]["qualifications"] == 3
    assert result["lease1"]["qualifications"] == 10
    assert result["qualification_reduction_vs_lease1"] == 0.7


def test_watchdog_detects_both_degradation_and_recovery():
    result = context_authority_watchdog_experiment()
    watchdog = result["watchdog"]
    assert watchdog["change_triggers"] == 2
    assert watchdog["hard_expiry_triggers"] == 0
    trigger_epochs = [
        row["epoch"]
        for row in watchdog["rows"]
        if row["trigger_reason"] == "watchdog_change"
    ]
    assert trigger_epochs == [1, 7]


def test_watchdog_never_directly_selects_route_without_full_gate():
    result = context_authority_watchdog_experiment()
    rows = result["watchdog"]["rows"]
    assert rows[0]["selected_policy"] == "context_normalized"
    assert all(row["selected_policy"] == "raw_function" for row in rows[1:7])
    assert all(row["selected_policy"] == "context_normalized" for row in rows[7:])


def test_static_authority_remains_the_negative_control():
    result = context_authority_watchdog_experiment()
    assert not result["static_once"]["contract_pass"]
    assert result["static_once"]["stale_authority_epochs"] >= 6
