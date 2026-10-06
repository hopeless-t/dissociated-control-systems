import pytest

from dissociated_control_systems.survivor_voi import (
    entropy_bits,
    expected_information_gain_bits,
    information_per_cost,
    rank_observations,
)


def test_uniform_four_world_prior_has_two_bits_entropy() -> None:
    prior = {"A": 1, "B": 1, "C": 1, "D": 1}
    assert entropy_bits(prior) == pytest.approx(2.0)


def test_noninformative_observation_has_zero_information_gain() -> None:
    prior = {"A": 0.5, "B": 0.5}
    likelihoods = {
        "positive": {"A": 0.5, "B": 0.5},
        "negative": {"A": 0.5, "B": 0.5},
    }
    assert expected_information_gain_bits(prior, likelihoods) == pytest.approx(0.0)


def test_perfect_binary_discriminator_returns_one_bit() -> None:
    prior = {"A": 0.5, "B": 0.5}
    likelihoods = {
        "positive": {"A": 1.0, "B": 0.0},
        "negative": {"A": 0.0, "B": 1.0},
    }
    assert expected_information_gain_bits(prior, likelihoods) == pytest.approx(1.0)


def test_information_per_cost_can_prefer_cheaper_partial_probe() -> None:
    prior = {"A": 0.5, "B": 0.5}
    perfect = {
        "positive": {"A": 1.0, "B": 0.0},
        "negative": {"A": 0.0, "B": 1.0},
    }
    partial = {
        "positive": {"A": 0.8, "B": 0.2},
        "negative": {"A": 0.2, "B": 0.8},
    }

    assert information_per_cost(prior, partial, cost=1.0) > information_per_cost(
        prior, perfect, cost=10.0
    )


def test_rank_observations_is_deterministic() -> None:
    prior = {"A": 0.5, "B": 0.5}
    noninformative = {
        "yes": {"A": 0.5, "B": 0.5},
        "no": {"A": 0.5, "B": 0.5},
    }
    informative = {
        "yes": {"A": 0.9, "B": 0.1},
        "no": {"A": 0.1, "B": 0.9},
    }

    ranked = rank_observations(
        prior,
        {
            "uninformative": (noninformative, 1.0),
            "informative": (informative, 1.0),
        },
    )
    assert ranked[0][0] == "informative"
    assert ranked[-1][1] == pytest.approx(0.0)


def test_invalid_likelihood_mass_fails_closed() -> None:
    prior = {"A": 0.5, "B": 0.5}
    invalid = {
        "yes": {"A": 0.9, "B": 0.1},
        "no": {"A": 0.9, "B": 0.1},
    }
    with pytest.raises(ValueError):
        expected_information_gain_bits(prior, invalid)
