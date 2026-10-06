from dissociated_control_systems.cancer_twin import (
    CancerDynamics,
    CancerSensors,
    CancerState,
    ctdna,
    imaging,
    resistant_net_drift,
    simulate,
)


def _dynamics(**overrides):
    values = dict(
        growth_s=0.015,
        growth_r=0.012,
        immune_kill_s=0.010,
        immune_kill_r=0.007,
        drug_kill_s=0.055,
        drug_kill_r=0.010,
        selection=0.0002,
    )
    values.update(overrides)
    return CancerDynamics(**values)


def test_imaging_cannot_identify_resistant_fraction():
    a = CancerState(0.9, 0.1, 0.5, 0.3, 0.8)
    b = CancerState(0.1, 0.9, 0.5, 0.3, 0.8)
    assert imaging(a) == imaging(b) == 1.0
    assert a.resistant_fraction != b.resistant_fraction


def test_ctdna_confounds_burden_and_shedding():
    a = CancerState(1.0, 0.0, 0.5, 0.3, 0.8)
    b = CancerState(2.0, 0.0, 0.5, 0.3, 0.8)
    sensor_a = CancerSensors(shedding_s=1.0, shedding_r=1.0)
    sensor_b = CancerSensors(shedding_s=0.5, shedding_r=1.0)
    assert ctdna(a, sensor_a) == ctdna(b, sensor_b) == 1.0
    assert a.total != b.total


def test_same_current_state_can_have_different_resistant_transition_law():
    state = CancerState(0.7, 0.3, 0.45, 0.35, 0.8)
    controlled = _dynamics(growth_r=0.009, drug_kill_r=0.018)
    fragile = _dynamics(growth_r=0.020, drug_kill_r=0.004)

    assert imaging(state) == 1.0
    assert resistant_net_drift(state, controlled, treatment=1.0) < 0.0
    assert resistant_net_drift(state, fragile, treatment=1.0) > 0.0


def test_equal_observation_can_diverge_after_treatment_transition():
    state = CancerState(0.7, 0.3, 0.45, 0.35, 0.8)
    sensor = CancerSensors()
    slow = _dynamics(growth_r=0.009, drug_kill_r=0.018)
    fast = _dynamics(growth_r=0.022, drug_kill_r=0.004)

    assert imaging(state) == imaging(state)
    assert ctdna(state, sensor) == ctdna(state, sensor)

    # Existing clinically justified treatment is represented as the input; the
    # synthetic experiment does not recommend changing a real patient's care.
    schedule = (1.0,) * 20 + (0.0,) * 80
    slow_states = simulate(state, slow, schedule)
    fast_states = simulate(state, fast, schedule)

    assert fast_states[-1].br > slow_states[-1].br
    assert fast_states[-1].total > slow_states[-1].total


def test_invalid_state_fails_closed():
    try:
        CancerState(-0.1, 0.0, 0.5, 0.3, 0.8)
    except ValueError:
        pass
    else:
        raise AssertionError("negative tumor burden must fail closed")
