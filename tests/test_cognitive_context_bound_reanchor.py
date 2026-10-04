from dissociated_control_systems.cognitive_context_bound_reanchor import (
    ACCEPTED_STALE_RMSE_CONTRACT,
    context_bound_scheduler_experiment,
)


def test_context_normalized_policy_holds_selective_freshness_contract():
    result = context_bound_scheduler_experiment()
    for level in result["levels"]:
        assert (
            level["normalized"]["accepted_stale_rmse"]
            <= ACCEPTED_STALE_RMSE_CONTRACT
        )


def test_fixed16_remains_stale_prone():
    result = context_bound_scheduler_experiment()
    for level in result["levels"]:
        assert not level["fixed16"]["accepted_stale_contract"]


def test_context_normalization_beats_raw_under_environment_events():
    result = context_bound_scheduler_experiment()
    for level in result["levels"][1:]:
        assert level["normalized"]["loss"] < level["raw"]["loss"]
        assert level["normalized"]["anchor_rate"] < level["raw"]["anchor_rate"]


def test_normalized_policy_remains_competitive_with_fixed8():
    result = context_bound_scheduler_experiment()
    for level in result["levels"]:
        assert level["normalized"]["loss"] < level["fixed8"]["loss"]
