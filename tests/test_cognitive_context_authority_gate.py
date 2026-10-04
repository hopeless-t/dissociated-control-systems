from dissociated_control_systems.cognitive_context_authority_gate import (
    MAX_HELDOUT_SELECTION_REGRET,
    context_authority_gate_experiment,
)


def test_low_noise_context_is_authorized():
    result = context_authority_gate_experiment()
    low_noise = result["levels"][:3]
    assert all(level["normalization_authorized"] for level in low_noise)


def test_context_authority_is_revoked_at_frozen_break_even():
    result = context_authority_gate_experiment()
    assert result["first_raw_fallback_sigma"] == 0.04
    for level in result["levels"][3:]:
        assert not level["normalization_authorized"]


def test_noisy_context_normalization_can_fall_below_useful_discrimination():
    result = context_authority_gate_experiment()
    assert result["first_normalized_auc_below_070_sigma"] == 0.06


def test_pilot_gate_keeps_heldout_regret_small():
    result = context_authority_gate_experiment()
    assert result["max_selection_regret"] <= MAX_HELDOUT_SELECTION_REGRET


def test_selected_policy_matches_heldout_winner_on_frozen_grid():
    result = context_authority_gate_experiment()
    for level in result["levels"]:
        if level["selected_policy"] == "context_normalized":
            assert level["heldout_normalized_auc"] >= level["heldout_raw_auc"]
        else:
            assert level["heldout_raw_auc"] >= level["heldout_normalized_auc"]
