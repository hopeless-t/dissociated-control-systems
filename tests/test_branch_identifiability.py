import pytest

from dissociated_control_systems.branch_identifiability import (
    BranchProbe,
    branches_locally_identifiable,
    canonical_probe_set,
    design_rank,
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


def test_orthogonal_branch_perturbations_raise_rank_to_two() -> None:
    probes = canonical_probe_set()
    assert design_rank(probes) == 2
    assert branches_locally_identifiable(probes)


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
