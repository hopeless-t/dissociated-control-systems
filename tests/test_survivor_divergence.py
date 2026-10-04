import pytest

from dissociated_control_systems.survivor_divergence import (
    classify_precedence_pattern,
    divergence_order,
    first_persistent_divergence,
)


def test_transient_spike_is_not_a_divergence() -> None:
    assert first_persistent_divergence(
        [0.0, 0.7, 0.1, 0.2],
        threshold=0.5,
        persistence=2,
    ) is None


def test_persistent_divergence_known_answer() -> None:
    assert first_persistent_divergence(
        [0.0, 0.2, 0.6, 0.7, 0.8],
        threshold=0.5,
        persistence=2,
    ) == 2


def test_mediated_precedence_world_is_identified() -> None:
    layers = {
        "psychological": [0.0, 0.6, 0.7, 0.7, 0.7, 0.7],
        "neuroendocrine": [0.0, 0.1, 0.6, 0.7, 0.7, 0.7],
        "immune": [0.0, 0.1, 0.2, 0.6, 0.7, 0.7],
        "treatment": [0.0, 0.1, 0.1, 0.1, 0.1, 0.1],
        "tumor": [0.0, 0.1, 0.2, 0.3, 0.6, 0.7],
    }

    assert classify_precedence_pattern(layers) == (
        "psych_neuroimmune_precedence_candidate"
    )
    assert divergence_order(layers) == (
        ("psychological", 1),
        ("neuroendocrine", 2),
        ("immune", 3),
        ("tumor", 4),
    )


def test_tumor_first_world_is_not_laundered_into_psychological_causality() -> None:
    layers = {
        "psychological": [0.0, 0.1, 0.1, 0.6, 0.7, 0.7],
        "neuroendocrine": [0.0, 0.1, 0.1, 0.5, 0.6, 0.7],
        "immune": [0.0, 0.1, 0.6, 0.7, 0.7, 0.7],
        "treatment": [0.0, 0.1, 0.1, 0.1, 0.1, 0.1],
        "tumor": [0.0, 0.6, 0.7, 0.7, 0.7, 0.7],
    }

    assert classify_precedence_pattern(layers) == (
        "tumor_first_reverse_causality_candidate"
    )


def test_treatment_first_world_is_separate() -> None:
    layers = {
        "psychological": [0.0, 0.1, 0.2, 0.3, 0.4, 0.4],
        "neuroendocrine": [0.0, 0.1, 0.2, 0.3, 0.4, 0.4],
        "immune": [0.0, 0.1, 0.2, 0.6, 0.7, 0.7],
        "treatment": [0.0, 0.6, 0.7, 0.7, 0.7, 0.7],
        "tumor": [0.0, 0.1, 0.2, 0.6, 0.7, 0.7],
    }

    assert classify_precedence_pattern(layers) == "treatment_first"


def test_missing_required_layer_fails_closed() -> None:
    with pytest.raises(ValueError):
        classify_precedence_pattern({"tumor": [0.0, 1.0, 1.0]})
