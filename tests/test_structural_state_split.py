from dissociated_control_systems.structural_state_split import (
    ecm_remodeling_intervention,
    matched_reduced_states,
    mechanical_relaxation,
)


def test_matched_states_have_same_reduced_structural_coordinate() -> None:
    e_high, m_high = matched_reduced_states()

    assert e_high.reduced_f == 0.5
    assert m_high.reduced_f == 0.5
    assert e_high != m_high


def test_mechanical_actuator_separates_equal_reduced_states() -> None:
    e_high, m_high = matched_reduced_states()

    e_response = mechanical_relaxation(e_high)
    m_response = mechanical_relaxation(m_high)

    assert e_response.final.reduced_f == 0.5
    assert m_response.final.reduced_f == 0.0
    assert e_response.reduced_change == 0.0
    assert m_response.reduced_change == -0.5


def test_ecm_actuator_reverses_which_hidden_state_responds() -> None:
    e_high, m_high = matched_reduced_states()

    e_response = ecm_remodeling_intervention(e_high)
    m_response = ecm_remodeling_intervention(m_high)

    assert e_response.final.reduced_f == 0.0
    assert m_response.final.reduced_f == 0.5


def test_partial_mechanical_relaxation_preserves_hidden_specificity() -> None:
    e_high, m_high = matched_reduced_states()

    e_response = mechanical_relaxation(e_high, strength=0.5)
    m_response = mechanical_relaxation(m_high, strength=0.5)

    assert e_response.final.reduced_f == 0.5
    assert m_response.final.reduced_f == 0.25
