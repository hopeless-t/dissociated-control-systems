from dissociated_control_systems.checkpoint_minimizer import (
    Checkpoint,
    failure_exposure_after_removal,
    mandatory_checkpoints,
    dominated_checkpoints,
    minimum_cost_sufficient_checkpoint_sets,
    minimum_sufficient_checkpoint_sets,
    removable_checkpoints,
)


FAILURES = {
    "provenance_loss",
    "state_response_confusion",
    "uncertainty_laundering",
    "reachability_overclaim",
}


def test_equal_coverage_checkpoint_is_interchangeable_not_redundant() -> None:
    checkpoints = [
        Checkpoint("source", frozenset({"provenance_loss"})),
        Checkpoint("state_response", frozenset({"state_response_confusion"})),
        Checkpoint("uncertainty", frozenset({"uncertainty_laundering"})),
        Checkpoint("reachability", frozenset({"reachability_overclaim"})),
        Checkpoint("pretty_explanation", frozenset({"provenance_loss"})),
    ]

    solutions = minimum_sufficient_checkpoint_sets(checkpoints, FAILURES)

    assert any("source" in solution for solution in solutions)
    assert any("pretty_explanation" in solution for solution in solutions)
    assert len(solutions[0]) == 4


def test_cost_breaks_tie_between_interchangeable_implementations() -> None:
    checkpoints = [
        Checkpoint("source", frozenset({"provenance_loss"}), cost=1.0),
        Checkpoint(
            "pretty_explanation",
            frozenset({"provenance_loss"}),
            cost=2.0,
        ),
        Checkpoint(
            "state_response",
            frozenset({"state_response_confusion"}),
            cost=1.0,
        ),
        Checkpoint(
            "uncertainty",
            frozenset({"uncertainty_laundering"}),
            cost=1.0,
        ),
        Checkpoint(
            "reachability",
            frozenset({"reachability_overclaim"}),
            cost=1.0,
        ),
    ]

    solutions = minimum_cost_sufficient_checkpoint_sets(
        checkpoints,
        FAILURES,
    )

    assert solutions == (
        ("reachability", "source", "state_response", "uncertainty"),
    )
    assert dominated_checkpoints(checkpoints) == frozenset(
        {"pretty_explanation"}
    )


def test_alternative_checkpoints_are_not_both_mandatory() -> None:
    checkpoints = [
        Checkpoint("source_a", frozenset({"provenance_loss"})),
        Checkpoint("source_b", frozenset({"provenance_loss"})),
        Checkpoint("state_response", frozenset({"state_response_confusion"})),
        Checkpoint("uncertainty", frozenset({"uncertainty_laundering"})),
        Checkpoint("reachability", frozenset({"reachability_overclaim"})),
    ]

    solutions = minimum_sufficient_checkpoint_sets(checkpoints, FAILURES)
    mandatory = mandatory_checkpoints(solutions)

    assert "source_a" not in mandatory
    assert "source_b" not in mandatory
    assert {
        "state_response",
        "uncertainty",
        "reachability",
    } <= mandatory


def test_ablation_identifies_structurally_critical_checkpoint() -> None:
    checkpoints = [
        Checkpoint("source", frozenset({"provenance_loss"})),
        Checkpoint("state_response", frozenset({"state_response_confusion"})),
        Checkpoint("uncertainty", frozenset({"uncertainty_laundering"})),
        Checkpoint("reachability", frozenset({"reachability_overclaim"})),
        Checkpoint("redundant_source", frozenset({"provenance_loss"})),
    ]

    exposure = failure_exposure_after_removal(checkpoints, FAILURES)

    assert exposure["state_response"] == frozenset(
        {"state_response_confusion"}
    )
    assert exposure["source"] == frozenset()


def test_removable_checkpoints_are_defined_by_counterfactual_deletion() -> None:
    checkpoints = [
        Checkpoint("source", frozenset({"provenance_loss"})),
        Checkpoint("source_copy", frozenset({"provenance_loss"})),
        Checkpoint("state_response", frozenset({"state_response_confusion"})),
        Checkpoint("uncertainty", frozenset({"uncertainty_laundering"})),
        Checkpoint("reachability", frozenset({"reachability_overclaim"})),
    ]

    removable = removable_checkpoints(checkpoints, FAILURES)

    assert "source" in removable
    assert "source_copy" in removable
    assert "state_response" not in removable
    assert "uncertainty" not in removable
    assert "reachability" not in removable


def test_impossible_contract_returns_no_solution() -> None:
    checkpoints = [
        Checkpoint("source", frozenset({"provenance_loss"})),
    ]

    assert minimum_sufficient_checkpoint_sets(
        checkpoints,
        FAILURES,
    ) == ()
