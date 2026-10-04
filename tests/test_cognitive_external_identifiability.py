from dissociated_control_systems.cognitive_external_identifiability import (
    analyze_channels,
    identifiability_experiment,
    noiseless_observations,
    recover_with_four_channels,
)


def test_self_informant_pair_is_not_full_state_identifying():
    result = analyze_channels(("self_report", "informant_report"))
    assert result.rank == 2
    assert result.nullity == 2
    assert not result.identifiable


def test_all_four_channels_are_full_rank():
    result = analyze_channels(
        (
            "self_report",
            "informant_report",
            "objective_performance",
            "daily_function",
        )
    )
    assert result.rank == 4
    assert result.identifiable


def test_noiseless_four_channel_reconstruction_is_exact():
    observations = noiseless_observations(z=0.61, a=0.17, b=-0.08, e=0.12)
    recovered = recover_with_four_channels(observations)
    assert abs(recovered["Z_current_state"] - 0.61) < 1e-12
    assert abs(recovered["A_self_bias"] - 0.17) < 1e-12
    assert abs(recovered["B_informant_bias"] + 0.08) < 1e-12
    assert abs(recovered["E_scaffold"] - 0.12) < 1e-12


def test_dyadic_discrepancy_aliases_two_biases():
    result = identifiability_experiment()
    assert abs(result["dyadic_discrepancy"] - result["expected_alias"]) < 1e-12
