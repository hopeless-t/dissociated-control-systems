from dissociated_control_systems.belief_policy import (
    bayes_update,
    expected_terminal_loss_after_observation,
    expected_two_stage_loss,
    normalize_belief,
)


STATES = ("y0_L", "y1_L", "y0_R", "y1_R")
PRIOR = {state: 0.25 for state in STATES}


def _row(p_one):
    return {0: 1.0 - p_one, 1: p_one}


SCOUT = {
    "y0_L": _row(0.10),
    "y1_L": _row(0.10),
    "y0_R": _row(0.90),
    "y1_R": _row(0.90),
}

SPECIALIST_L = {
    "y0_L": _row(0.05),
    "y1_L": _row(0.95),
    "y0_R": _row(0.50),
    "y1_R": _row(0.50),
}

SPECIALIST_R = {
    "y0_L": _row(0.50),
    "y1_L": _row(0.50),
    "y0_R": _row(0.05),
    "y1_R": _row(0.95),
}

GENERAL = {
    "y0_L": _row(0.25),
    "y1_L": _row(0.75),
    "y0_R": _row(0.25),
    "y1_R": _row(0.75),
}


def outcome_loss(belief):
    belief = normalize_belief(belief)
    p_y1 = belief["y1_L"] + belief["y1_R"]
    return min(p_y1, 1.0 - p_y1)


def world_l_probability(belief):
    belief = normalize_belief(belief)
    return belief["y0_L"] + belief["y1_L"]


def route_specialist(belief):
    return SPECIALIST_L if world_l_probability(belief) >= 0.5 else SPECIALIST_R


def test_scout_has_zero_immediate_outcome_value():
    before = outcome_loss(PRIOR)
    after = expected_terminal_loss_after_observation(PRIOR, SCOUT, outcome_loss)
    assert abs(before - 0.5) < 1e-12
    assert abs(after - before) < 1e-12


def test_multi_step_scout_then_route_beats_direct_general_observation():
    direct = expected_terminal_loss_after_observation(PRIOR, GENERAL, outcome_loss)
    routed = expected_two_stage_loss(
        PRIOR,
        SCOUT,
        route_specialist,
        outcome_loss,
    )

    assert abs(direct - 0.25) < 1e-12
    assert abs(routed - 0.095) < 1e-12
    assert routed < direct


def test_scout_updates_model_world_without_changing_outcome_prior():
    posterior = bayes_update(PRIOR, SCOUT, 1)
    p_y1 = posterior["y1_L"] + posterior["y1_R"]
    p_world_r = posterior["y0_R"] + posterior["y1_R"]

    assert abs(p_y1 - 0.5) < 1e-12
    assert abs(p_world_r - 0.9) < 1e-12
