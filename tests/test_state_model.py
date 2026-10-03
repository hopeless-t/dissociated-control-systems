import pytest

from dissociated_control_systems import (
    AssistedRetrievalState,
    assisted_performance,
    context_evicted_observation,
    SubsystemState,
    coarse_observation,
    dissociation_index,
    equivalence_class,
    expressed_capability,
    independent_retrieval,
    offloading_gap,
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



def test_assisted_score_can_hide_independent_retrieval_dissociation() -> None:
    scaffold_dependent = AssistedRetrievalState(
        internal_capability=1.0,
        retrieval_access=0.2,
        external_scaffold=0.9,
    )
    independently_accessible = AssistedRetrievalState(
        internal_capability=0.9,
        retrieval_access=1.0,
        external_scaffold=0.9,
    )

    assert assisted_performance(scaffold_dependent) == pytest.approx(0.9)
    assert assisted_performance(independently_accessible) == pytest.approx(0.9)
    assert context_evicted_observation(scaffold_dependent) == {
        "independent_retrieval": pytest.approx(0.2)
    }
    assert context_evicted_observation(independently_accessible) == {
        "independent_retrieval": pytest.approx(0.9)
    }


def test_offloading_gap_known_answer() -> None:
    state = AssistedRetrievalState(
        internal_capability=1.0,
        retrieval_access=0.2,
        external_scaffold=0.9,
    )
    assert independent_retrieval(state) == pytest.approx(0.2)
    assert offloading_gap(state) == pytest.approx(0.7)


def test_retrieval_state_fails_closed_on_out_of_range_inputs() -> None:
    with pytest.raises(ValueError):
        AssistedRetrievalState(1.0, 1.0, 1.01)

    with pytest.raises(TypeError):
        AssistedRetrievalState(1.0, True, 0.5)
