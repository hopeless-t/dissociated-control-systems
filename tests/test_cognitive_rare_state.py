from dissociated_control_systems.cognitive_rare_state import (
    rare_state_experiment,
)


def test_rare_state_threshold_is_from_frozen_grid():
    result = rare_state_experiment()
    assert 0.20 <= result["threshold"] <= 0.55


def test_rare_state_rates_are_bounded():
    result = rare_state_experiment()
    assert 0.0 <= result["pilot_pooled_rate"] <= 1.0
    assert 0.0 <= result["heldout_pooled_rate"] <= 1.0
    assert 0.0 <= result["heldout_selected_rate"] <= 1.0


def test_capture_sizes_are_positive_when_events_exist():
    result = rare_state_experiment()
    if result["heldout_pooled_rate"] > 0.0:
        assert result["n95_pooled"] >= 1
    if result["heldout_selected_rate"] > 0.0:
        assert result["n95_enriched"] >= 1
