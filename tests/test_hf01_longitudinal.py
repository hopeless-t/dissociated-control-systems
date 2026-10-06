import pytest

from dissociated_control_systems.hair_follicle_longitudinal import (
    canonical_longitudinal_probe,
    matched_visible_states,
)


def test_matched_states_begin_with_identical_visible_output() -> None:
    recoverable, locked = matched_visible_states()

    assert recoverable.hair_output == locked.hair_output == 0.50
    assert recoverable.structural_lock < locked.structural_lock
    assert recoverable.regeneration > locked.regeneration


def test_early_hidden_response_separates_before_large_visible_gain() -> None:
    result = canonical_longitudinal_probe()
    recoverable = result["recoverable"]
    locked = result["locked"]

    # At the early checkpoint, intervention-linked regeneration response is
    # already substantially different, while output benefit is still small.
    assert recoverable.early_regeneration_gain > 0.25
    assert locked.early_regeneration_gain > 0.10
    assert recoverable.early_regeneration_gain > locked.early_regeneration_gain
    assert abs(recoverable.early_output_gain) < 0.05
    assert abs(locked.early_output_gain) < 0.01


def test_early_response_order_matches_late_recoverability_order() -> None:
    result = canonical_longitudinal_probe()
    recoverable = result["recoverable"]
    locked = result["locked"]

    assert recoverable.early_regeneration_gain > locked.early_regeneration_gain
    assert recoverable.late_output_gain > 0.50
    assert locked.late_output_gain < 1e-4
    assert recoverable.late_output_gain > locked.late_output_gain


def test_frozen_longitudinal_known_answer_values() -> None:
    result = canonical_longitudinal_probe()

    assert result["recoverable"].early_regeneration_gain == pytest.approx(
        0.2689814792, abs=1e-9
    )
    assert result["locked"].early_regeneration_gain == pytest.approx(
        0.1419597783, abs=1e-9
    )
    assert result["recoverable"].late_output_gain == pytest.approx(
        0.5175504740, abs=1e-9
    )
    assert result["locked"].late_output_gain == pytest.approx(
        0.00000007736, abs=1e-9
    )
