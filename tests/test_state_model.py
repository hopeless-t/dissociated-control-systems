import pytest

from dissociated_control_systems import (
    SubsystemState,
    coarse_observation,
    dissociation_index,
    equivalence_class,
    expressed_capability,
    rich_observation,
)


def test_val001_known_answer_non_identifiability() -> None:
    integrated = SubsystemState(1, 1, 1, 1)
    dissociated = SubsystemState(1, 1, 0, 0)
    assert integrated != dissociated
    assert coarse_observation(integrated) == {"complex_action": True}
    assert coarse_observation(dissociated) == {"complex_action": True}
    assert rich_observation(integrated) != rich_observation(dissociated)


def test_val001_dissociation_index_known_answers() -> None:
    assert dissociation_index((1, 1, 1, 1)) == 0.0
    assert dissociation_index((1, 1, 0, 0)) == 1.0


def test_val001_equivalence_class_size() -> None:
    states = equivalence_class({"complex_action": True})
    assert len(states) == 4


def test_dissociation_index_is_bounded_for_binary_state_space() -> None:
    states = (
        equivalence_class({"complex_action": True})
        + equivalence_class({"complex_action": False})
    )
    for state in states:
        assert 0.0 <= dissociation_index(state.values) <= 1.0


def test_accessibility_can_suppress_expression_without_erasing_capability() -> None:
    assert expressed_capability(
        (1.0, 1.0, 1.0, 1.0),
        (1.0, 1.0, 0.0, 0.0),
    ) == (1.0, 1.0, 0.0, 0.0)


@pytest.mark.parametrize("bad", [-0.01, 1.01, 2.0])
def test_invalid_state_values_fail_closed(bad: float) -> None:
    with pytest.raises(ValueError):
        SubsystemState(1.0, 1.0, 1.0, bad)


def test_boolean_is_not_silently_accepted_as_numeric_state() -> None:
    with pytest.raises(TypeError):
        SubsystemState(True, 1.0, 1.0, 1.0)
