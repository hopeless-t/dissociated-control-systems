import pytest

from dissociated_control_systems.post_randomization_selection import (
    observed_post_recurrence_survival,
    recurrent_stratum_weights,
    selection_bias_fixture,
)


def test_conditioning_on_recurrence_changes_latent_risk_composition() -> None:
    strata = selection_bias_fixture()
    control = recurrent_stratum_weights(strata, intervention=False)
    intervention = recurrent_stratum_weights(strata, intervention=True)

    assert control["high"] == pytest.approx(0.8)
    assert intervention["high"] == pytest.approx(0.5)


def test_selected_recurrent_subset_can_create_apparent_post_recurrence_effect() -> None:
    strata = selection_bias_fixture()
    control = observed_post_recurrence_survival(strata, intervention=False)
    intervention = observed_post_recurrence_survival(strata, intervention=True)

    assert control == pytest.approx(0.32)
    assert intervention == pytest.approx(0.50)
    assert intervention - control == pytest.approx(0.18)


def test_fixture_contains_no_direct_post_recurrence_intervention_term() -> None:
    low, high = selection_bias_fixture()

    # One post-recurrence survival probability is declared per latent-risk
    # stratum, not one per randomized arm. The apparent arm difference above is
    # generated only by conditioning on recurrence.
    assert low.post_recurrence_survival == pytest.approx(0.8)
    assert high.post_recurrence_survival == pytest.approx(0.2)
