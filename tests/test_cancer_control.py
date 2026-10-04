import pytest

from dissociated_control_systems.cancer_control import (
    CancerControlInputs,
    CancerControlParameters,
    CancerControlState,
    instantaneous_control_margin,
    simulate,
    step,
)


INITIAL = CancerControlState(
    tumor=0.25,
    effector=0.45,
    immunosuppression=0.20,
    stress=0.65,
)


def test_rq005_control_margin_matches_tumor_direction() -> None:
    params = CancerControlParameters()
    controlled = CancerControlState(
        tumor=0.25,
        effector=0.80,
        immunosuppression=0.10,
        stress=0.20,
    )
    uncontrolled = CancerControlState(
        tumor=0.25,
        effector=0.15,
        immunosuppression=0.80,
        stress=0.90,
    )
    inputs = CancerControlInputs(
        prescribed_treatment=0.50,
        adherence=0.90,
        stress_recovery_rate=0.40,
    )

    assert instantaneous_control_margin(controlled, inputs, params) > 0.0
    assert instantaneous_control_margin(uncontrolled, inputs, params) < 0.0
    assert step(controlled, inputs, params).tumor < controlled.tumor
    assert step(uncontrolled, inputs, params).tumor > uncontrolled.tumor


def test_rq005_measured_mediator_shift_changes_synthetic_trajectory() -> None:
    reference = CancerControlInputs(
        adherence=0.55,
        stress_recovery_rate=0.22,
    )
    shifted = CancerControlInputs(
        adherence=0.90,
        stress_recovery_rate=0.67,
    )

    reference_final = simulate(INITIAL, reference)[-1]
    shifted_final = simulate(INITIAL, shifted)[-1]

    assert shifted_final.stress < reference_final.stress
    assert shifted_final.immunosuppression < reference_final.immunosuppression
    assert shifted_final.effector > reference_final.effector
    assert shifted_final.tumor < reference_final.tumor


def test_rq005_recovery_and_adherence_are_separable_mediators() -> None:
    recovery_only = simulate(
        INITIAL,
        CancerControlInputs(
            adherence=0.55,
            stress_recovery_rate=0.42,
        ),
    )[-1]
    adherence_only = simulate(
        INITIAL,
        CancerControlInputs(
            adherence=0.90,
            stress_recovery_rate=0.22,
        ),
    )[-1]
    reference = simulate(INITIAL, CancerControlInputs())[-1]

    assert recovery_only.tumor < reference.tumor
    assert adherence_only.tumor < reference.tumor
    assert recovery_only.stress < adherence_only.stress


def test_rq005_psychological_label_has_no_structural_direct_edge() -> None:
    assert "hope" not in CancerControlInputs.__dataclass_fields__
    assert "resilience" not in CancerControlInputs.__dataclass_fields__


def test_rq005_zero_step_is_identity() -> None:
    trajectory = simulate(INITIAL, CancerControlInputs(), steps=0)
    assert trajectory == (INITIAL,)


@pytest.mark.parametrize("bad", [-0.1, 1.1])
def test_rq005_bounded_state_fails_closed(bad: float) -> None:
    with pytest.raises(ValueError):
        CancerControlState(
            tumor=0.2,
            effector=bad,
            immunosuppression=0.2,
            stress=0.2,
        )
