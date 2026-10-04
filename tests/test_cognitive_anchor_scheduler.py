from dissociated_control_systems.cognitive_anchor_scheduler import (
    ANCHOR_COSTS,
    anchor_scheduler_experiment,
    interval_contract_safe,
    interval_max_rmse,
    select_contract_constrained,
    select_unconstrained,
)


def test_freshness_contract_separates_eight_from_sixteen():
    assert interval_contract_safe(8)
    assert not interval_contract_safe(16)
    assert interval_max_rmse(8) <= 0.10
    assert interval_max_rmse(16) > 0.10


def test_high_anchor_cost_can_make_unconstrained_optimum_unsafe():
    assert select_unconstrained(0.08) == 16
    assert select_contract_constrained(0.08) == 8


def test_contract_never_selects_unsafe_interval():
    for cost in ANCHOR_COSTS:
        interval = select_contract_constrained(cost)
        assert interval is not None
        assert interval_contract_safe(interval)


def test_contract_binds_for_some_but_not_all_costs():
    result = anchor_scheduler_experiment()
    assert result["binding_costs"]
    assert len(result["binding_costs"]) < len(ANCHOR_COSTS)
