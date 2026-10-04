import pytest

from dissociated_control_systems.cancer_control import (
    CancerControlInputs,
    CancerControlParameters,
    CancerControlState,
    instantaneous_control_margin,
    simulate,
)


INITIAL = CancerControlState(
    tumor=0.25,
    effector=0.45,
    immunosuppression=0.20,
    stress=0.65,
)


def test_rq005_control_margin_has_expected_sign() -> None:
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
        baseline_adherence=0.90,
    )

    assert instantaneous_control_margin(controlled, inputs, params) > 0.0
    assert instantaneous_control_margin(uncontrolled, inputs, params) < 0.0


def test_rq005_mediated_control_package_changes_synthetic_attractor() -> None:
    reference = CancerControlInputs()
    mediated = CancerControlInputs(
        adherence_boost=0.35,
        recovery_boost=0.45,
    )

    reference_final = simulate(INITIAL, reference)[-1]
    mediated_final = simulate(INITIAL, mediated)[-1]

    assert mediated_final.stress < reference_final.stress
    assert mediated_final.immunosuppression < reference_final.immunosuppression
    assert mediated_final.effector > reference_final.effector
    assert mediated_final.tumor < reference_final.tumor


def test_rq005_recovery_and_adherence_are_separable_mediators() -> None:
    recovery_only = simulate(
        INITIAL, CancerControlInputs(recovery_boost=0.20)
    )[-1]
    adherence_only = simulate(
        INITIAL, CancerControlInputs(adherence_boost=0.35)
    )[-1]
    reference = simulate(INITIAL, CancerControlInputs())[-1]

    assert recovery_only.tumor < reference.tumor
    assert adherence_only.tumor < reference.tumor
    assert recovery_only.stress < adherence_only.stress


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
