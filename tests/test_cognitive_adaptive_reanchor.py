from dissociated_control_systems.cognitive_adaptive_reanchor import (
    ACCEPTED_STALE_RMSE_CONTRACT,
    adaptive_reanchor_experiment,
)


def test_pilot_selected_adaptive_policies_hold_stale_rmse_contract():
    result = adaptive_reanchor_experiment()
    for level in result["levels"]:
        assert level["sentinel"]["accepted_stale_rmse"] <= ACCEPTED_STALE_RMSE_CONTRACT
        assert level["dyad"]["accepted_stale_rmse"] <= ACCEPTED_STALE_RMSE_CONTRACT


def test_independent_sentinel_reduces_anchor_rate_vs_fixed8():
    result = adaptive_reanchor_experiment()
    for level in result["levels"]:
        assert level["sentinel"]["anchor_rate"] < level["fixed8"]["anchor_rate"]


def test_independent_sentinel_beats_dyad_loss():
    result = adaptive_reanchor_experiment()
    for level in result["levels"]:
        assert level["sentinel"]["loss"] < level["dyad"]["loss"]


def test_fixed16_fails_selective_stale_contract():
    result = adaptive_reanchor_experiment()
    for level in result["levels"]:
        assert not level["fixed16"]["accepted_stale_contract"]
