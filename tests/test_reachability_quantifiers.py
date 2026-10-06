import pytest

from dissociated_control_systems.reachability_quantifiers import (
    QuantifiedReachability,
    ReachabilityMatrix,
    observer_selection_gap,
    statewise_reachability,
    uniform_policy_reachability,
)


def test_statewise_recovery_can_exist_without_uniform_policy() -> None:
    matrix = ReachabilityMatrix.from_rows(
        (
            (True, False),
            (False, True),
        )
    )

    assert statewise_reachability(matrix) is QuantifiedReachability.PASS
    assert uniform_policy_reachability(matrix) is QuantifiedReachability.FAIL
    assert observer_selection_gap(matrix)


def test_common_control_closes_observer_selection_gap() -> None:
    matrix = ReachabilityMatrix.from_rows(
        (
            (True, True),
            (False, True),
        )
    )

    assert statewise_reachability(matrix) is QuantifiedReachability.PASS
    assert uniform_policy_reachability(matrix) is QuantifiedReachability.PASS
    assert not observer_selection_gap(matrix)


def test_unreachable_state_fails_statewise_reachability() -> None:
    matrix = ReachabilityMatrix.from_rows(
        (
            (True, False),
            (False, False),
        )
    )

    assert statewise_reachability(matrix) is QuantifiedReachability.FAIL
    assert uniform_policy_reachability(matrix) is QuantifiedReachability.FAIL


def test_empty_state_set_is_unknown() -> None:
    matrix = ReachabilityMatrix.from_rows(())
    assert statewise_reachability(matrix) is QuantifiedReachability.UNKNOWN
    assert uniform_policy_reachability(matrix) is QuantifiedReachability.UNKNOWN


def test_ragged_matrix_rejected() -> None:
    with pytest.raises(ValueError):
        ReachabilityMatrix.from_rows(((True, False), (True,)))
