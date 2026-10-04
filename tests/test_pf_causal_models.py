from dissociated_control_systems.pf_causal_models import (
    observationally_equivalent_pair,
)


def test_opposite_causal_directions_can_match_observational_moments() -> None:
    f_to_p, p_to_f = observationally_equivalent_pair(0.6)

    assert f_to_p.observational_moments() == p_to_f.observational_moments()
    moments = f_to_p.observational_moments()
    assert moments.var_p == 1.0
    assert moments.var_f == 1.0
    assert moments.cov_pf == 0.6


def test_do_f_intervention_separates_the_observationally_equivalent_models() -> None:
    f_to_p, p_to_f = observationally_equivalent_pair(0.6)

    assert f_to_p.expected_p_under_do_f(1.0) == 0.6
    assert p_to_f.expected_p_under_do_f(1.0) == 0.0


def test_do_p_intervention_separates_in_opposite_direction() -> None:
    f_to_p, p_to_f = observationally_equivalent_pair(0.6)

    assert f_to_p.expected_f_under_do_p(1.0) == 0.0
    assert p_to_f.expected_f_under_do_p(1.0) == 0.6
