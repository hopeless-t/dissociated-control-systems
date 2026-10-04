from dissociated_control_systems.hair_follicle_model import (
    HFControl,
    canonical_early_state,
    canonical_late_state,
    recoverability_threshold,
    robustness_fraction,
    simulate,
    state_from_lock,
)


def test_state_remains_bounded() -> None:
    final = simulate(
        canonical_early_state(),
        HFControl(
            behavioral=1.0,
            antiandrogen=1.0,
            regenerative=1.0,
            structural=1.0,
        ),
    )
    assert all(0.0 <= value <= 1.0 for value in final.as_tuple())


def test_early_state_control_ordering() -> None:
    initial = canonical_early_state()
    none = simulate(initial, HFControl()).hair_output
    behavior = simulate(initial, HFControl(behavioral=1.0)).hair_output
    drug = simulate(initial, HFControl(antiandrogen=1.0)).hair_output
    combo = simulate(
        initial,
        HFControl(behavioral=1.0, antiandrogen=1.0),
    ).hair_output

    assert combo > drug > behavior >= none


def test_late_state_exhibits_hysteresis() -> None:
    initial = canonical_late_state()

    input_only = simulate(
        initial,
        HFControl(behavioral=1.0, antiandrogen=1.0),
    )
    structural = simulate(
        initial,
        HFControl(behavioral=1.0, antiandrogen=1.0, structural=1.0),
    )

    assert input_only.hair_output < 0.30
    assert input_only.structural_lock > 0.90
    assert structural.hair_output > 0.60
    assert structural.structural_lock < 0.10


def test_nested_reachability_thresholds() -> None:
    combo = recoverability_threshold(
        HFControl(behavioral=1.0, antiandrogen=1.0)
    )
    regen = recoverability_threshold(
        HFControl(
            behavioral=1.0,
            antiandrogen=1.0,
            regenerative=1.0,
        )
    )
    structural = recoverability_threshold(
        HFControl(
            behavioral=1.0,
            antiandrogen=1.0,
            structural=1.0,
        )
    )

    assert combo == 0.35
    assert regen == 0.80
    assert structural == 1.00


def test_output_is_not_a_unique_internal_state() -> None:
    # Coarse output can be similar while latent structure differs.
    a = state_from_lock(0.20)
    b = state_from_lock(0.55)
    # Force equal visible output to make the VAL-001-style identifiability
    # failure explicit; the hidden states remain different.
    b = type(b)(
        b.androgen_pressure,
        b.stress_load,
        b.regeneration,
        b.progenitor_reserve,
        b.niche_integrity,
        b.structural_lock,
        a.hair_output,
    )

    assert a.hair_output == b.hair_output
    assert a.progenitor_reserve != b.progenitor_reserve
    assert a.niche_integrity != b.niche_integrity
    assert a.structural_lock != b.structural_lock


def test_parameter_perturbation_preserves_core_claim_most_of_the_time() -> None:
    # Fixed-seed deterministic sensitivity analysis.
    # This is evidence about this synthetic model only.
    assert robustness_fraction(samples=300, perturbation_fraction=0.20) >= 0.94
