from dissociated_control_systems.checkpoint_placement import (
    Gate,
    Hazard,
    optimal_position,
    placement_is_safe,
    premature_exposure_cost,
)


HAZARDS = [
    Hazard("provenance_loss", first_unsafe_step=2),
    Hazard("state_response_confusion", first_unsafe_step=4),
    Hazard("uncertainty_laundering", first_unsafe_step=6),
    Hazard("reachability_overclaim", first_unsafe_step=8),
]


def test_single_hazard_gate_is_best_at_last_responsible_moment() -> None:
    gate = Gate(
        "reachability",
        frozenset({"reachability_overclaim"}),
    )

    assert optimal_position(gate, HAZARDS) == 8
    assert premature_exposure_cost(gate, HAZARDS, 8) == 0
    assert premature_exposure_cost(gate, HAZARDS, 4) == 4


def test_late_gate_is_invalid() -> None:
    gate = Gate(
        "uncertainty",
        frozenset({"uncertainty_laundering"}),
    )

    assert placement_is_safe(gate, HAZARDS, 6)
    assert not placement_is_safe(gate, HAZARDS, 7)
    assert premature_exposure_cost(
        gate,
        HAZARDS,
        7,
    ) == float("inf")


def test_multi_hazard_gate_must_precede_earliest_covered_hazard() -> None:
    gate = Gate(
        "combined",
        frozenset(
            {
                "state_response_confusion",
                "reachability_overclaim",
            }
        ),
    )

    assert optimal_position(gate, HAZARDS) == 4


def test_irrelevant_gate_needs_no_forced_position() -> None:
    gate = Gate("other", frozenset({"unseen_failure"}))

    assert optimal_position(gate, HAZARDS) is None
    assert premature_exposure_cost(gate, HAZARDS, 0) == 0
