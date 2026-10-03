import pytest

from dissociated_control_systems.representation_budget import (
    RepresentationOption,
    choose_minimal_sufficient_representation,
    should_expand_representation,
)


def test_choose_minimal_sufficient_representation() -> None:
    coarse = RepresentationOption(
        name="coarse",
        representation_cost=1.0,
        execution_cost=1.0,
        expected_decision_error=0.20,
        semantic_dofs=3,
    )
    articulated = RepresentationOption(
        name="articulated",
        representation_cost=1.5,
        execution_cost=1.2,
        expected_decision_error=0.08,
        semantic_dofs=8,
    )
    physical = RepresentationOption(
        name="physical",
        representation_cost=3.0,
        execution_cost=2.0,
        expected_decision_error=0.03,
        semantic_dofs=14,
    )

    assert choose_minimal_sufficient_representation(
        (coarse, articulated, physical),
        max_expected_error=0.10,
    ) == articulated


def test_semantic_dof_count_is_not_cost_proxy() -> None:
    compact_but_semantic = RepresentationOption(
        name="compact-semantic",
        representation_cost=1.0,
        execution_cost=1.0,
        expected_decision_error=0.05,
        semantic_dofs=9,
    )
    bigger_but_weaker = RepresentationOption(
        name="bigger-weaker",
        representation_cost=2.0,
        execution_cost=2.0,
        expected_decision_error=0.08,
        semantic_dofs=5,
    )

    assert choose_minimal_sufficient_representation(
        (compact_but_semantic, bigger_but_weaker),
        max_expected_error=0.10,
    ) == compact_but_semantic


def test_no_sufficient_representation_fails_closed() -> None:
    option = RepresentationOption("coarse", 1.0, 1.0, 0.30, 3)
    with pytest.raises(ValueError):
        choose_minimal_sufficient_representation((option,), max_expected_error=0.10)


def test_representation_expands_on_large_prediction_residual() -> None:
    assert should_expand_representation(
        prediction_residual=0.25,
        residual_threshold=0.20,
        repeated_failure_count=0,
    )


def test_representation_expands_on_repeated_failure() -> None:
    assert should_expand_representation(
        prediction_residual=0.05,
        residual_threshold=0.20,
        repeated_failure_count=2,
    )


def test_representation_stays_compact_when_stable() -> None:
    assert not should_expand_representation(
        prediction_residual=0.05,
        residual_threshold=0.20,
        repeated_failure_count=0,
    )
