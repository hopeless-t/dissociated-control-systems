import pytest

from dissociated_control_systems.branch_identifiability import (
    BranchProbe,
    best_pair_separation,
    branches_locally_identifiable,
    canonical_probe_set,
    design_rank,
    pair_separation_score,
    solve_two_branch_effects,
)


def test_dht_only_is_rank_one() -> None:
    dht = BranchProbe("DHT", 1.0, 1.0)
    assert design_rank((dht,)) == 1
    assert not branches_locally_identifiable((dht,))


def test_repeated_same_direction_does_not_add_identifiability() -> None:
    probes = (
        BranchProbe("DHT_low", 0.5, 0.5),
        BranchProbe("DHT_high", 1.0, 1.0),
    )
    assert design_rank(probes) == 1
    assert best_pair_separation(probes) == pytest.approx(0.0)


def test_orthogonal_branch_perturbations_raise_rank_to_two() -> None:
    probes = canonical_probe_set()
    assert design_rank(probes) == 2
    assert branches_locally_identifiable(probes)
    assert best_pair_separation(probes) == pytest.approx(1.0)


def test_almost_parallel_probes_are_rank_two_but_poorly_separated() -> None:
    first = BranchProbe("probe1", 1.0, 1.0)
    second = BranchProbe("probe2", 0.99, 1.0)

    assert design_rank((first, second)) == 2
    assert 0.0 < pair_separation_score(first, second) < 0.01


def test_cross_talk_can_reduce_separation_without_destroying_rank() -> None:
    selective_ar = BranchProbe("AR_block", 0.1, 1.0)
    selective_m = BranchProbe("M_relax", 1.0, 0.1)
    cross_talk_ar = BranchProbe("AR_block_cross_talk", 0.4, 0.7)
    cross_talk_m = BranchProbe("M_relax_cross_talk", 0.7, 0.4)

    clean = pair_separation_score(selective_ar, selective_m)
    contaminated = pair_separation_score(cross_talk_ar, cross_talk_m)

    assert design_rank((cross_talk_ar, cross_talk_m)) == 2
    assert contaminated < clean


def test_ar_block_and_mechanical_relaxation_recover_distinct_effects() -> None:
    ar_block = BranchProbe("AR_block", 0.0, 1.0)
    mechanical_relax = BranchProbe("M_relax", 1.0, 0.0)

    alpha, mu = solve_two_branch_effects(
        ar_block,
        mechanical_relax,
        first_effect=0.3,
        second_effect=0.7,
    )

    assert alpha == pytest.approx(0.7)
    assert mu == pytest.approx(0.3)


def test_rank_deficient_pair_cannot_be_solved() -> None:
    with pytest.raises(ValueError):
        solve_two_branch_effects(
            BranchProbe("same1", 1.0, 1.0),
            BranchProbe("same2", 0.5, 0.5),
            1.0,
            0.5,
        )
