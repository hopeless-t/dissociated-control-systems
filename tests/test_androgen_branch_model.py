from dissociated_control_systems.androgen_branch_model import (
    block_ar,
    inhibit_dht_production,
    relax_mechanics,
    state_from_dht,
)


def test_upstream_dht_reduction_moves_both_downstream_branches() -> None:
    state = state_from_dht(1.0)
    final = inhibit_dht_production(state, strength=1.0)

    assert final.upstream_dht == 0.0
    assert final.ar_branch == 0.0
    assert final.mechanical_branch == 0.0


def test_ar_blockade_does_not_imply_mechanical_relaxation() -> None:
    state = state_from_dht(1.0)
    final = block_ar(state, strength=1.0)

    assert final.ar_branch == 0.0
    assert final.mechanical_branch == 1.0
    assert final.upstream_dht == 1.0


def test_mechanical_relaxation_does_not_imply_ar_blockade() -> None:
    state = state_from_dht(1.0)
    final = relax_mechanics(state, strength=1.0)

    assert final.ar_branch == 1.0
    assert final.mechanical_branch == 0.0


def test_same_reduced_burden_can_hide_opposite_active_branches() -> None:
    state = state_from_dht(1.0)
    ar_blocked = block_ar(state, strength=1.0)
    mechanics_relaxed = relax_mechanics(state, strength=1.0)

    assert ar_blocked.reduced_androgen_burden == 0.5
    assert mechanics_relaxed.reduced_androgen_burden == 0.5
    assert ar_blocked.ar_branch != mechanics_relaxed.ar_branch
    assert ar_blocked.mechanical_branch != mechanics_relaxed.mechanical_branch
