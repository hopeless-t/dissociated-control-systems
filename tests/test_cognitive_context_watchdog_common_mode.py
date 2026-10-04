from dissociated_control_systems.cognitive_context_watchdog_common_mode import (
    MAX_EPOCH_SELECTION_REGRET,
    common_mode_watchdog_attack,
)


def test_pairwise_watchdog_is_blind_to_common_mode_bias_change():
    result = common_mode_watchdog_attack()
    watchdog = result["pairwise_watchdog"]
    assert watchdog["change_triggers"] == 0
    assert watchdog["hard_expiry_triggers"] == 1


def test_common_mode_blindness_breaks_regret_contract():
    result = common_mode_watchdog_attack()
    watchdog = result["pairwise_watchdog"]
    assert not watchdog["contract_pass"]
    assert watchdog["max_regret"] > MAX_EPOCH_SELECTION_REGRET
    assert watchdog["stale_authority_epochs"] >= 5


def test_hard_expiry_bounds_but_does_not_detect_common_mode_failure():
    result = common_mode_watchdog_attack()
    rows = result["pairwise_watchdog"]["rows"]
    hard_expiry_rows = [row for row in rows if row["trigger_reason"] == "hard_expiry"]
    assert [row["epoch"] for row in hard_expiry_rows] == [6]
    assert rows[1]["stale_authority"]
    assert rows[1]["trigger_reason"] == "none"


def test_full_requalification_control_still_tracks_route_quality():
    result = common_mode_watchdog_attack()
    lease1 = result["lease1"]
    assert lease1["stale_authority_epochs"] == 0
    assert lease1["max_regret"] <= MAX_EPOCH_SELECTION_REGRET


def test_common_mode_bias_cancels_from_pairwise_watchdog_statistic():
    result = common_mode_watchdog_attack()
    rows = result["pairwise_watchdog"]["rows"]
    baseline = rows[0]["watchdog_statistic"]
    biased = [row["watchdog_statistic"] for row in rows[1:7]]
    assert max(abs(value - baseline) for value in biased) < 0.03
