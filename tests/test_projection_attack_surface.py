from dissociated_control_systems.projection_attack_surface import (
    full_attack_summary,
    permutation_attack_summary,
    status_attack_summary,
    subset_attack_summary,
)


def test_all_reachability_role_subsets_have_one_accepted_set() -> None:
    # 2^4 subsets. Only the complete canonical role set can satisfy a
    # reachability empirical claim.
    assert subset_attack_summary() == {
        "tested": 16,
        "accepted": 1,
    }


def test_all_full_role_permutations_have_one_accepted_order() -> None:
    # 4! permutations. Only the declared protocol order is accepted.
    assert permutation_attack_summary() == {
        "tested": 24,
        "accepted": 1,
    }


def test_all_status_assignments_have_one_empirically_accepted_vector() -> None:
    # 3^4 PASS/UNKNOWN/FAIL vectors. Only PASS/PASS/PASS/PASS can acquire
    # empirical authority.
    assert status_attack_summary() == {
        "tested": 81,
        "accepted": 1,
    }


def test_combined_attack_surface_is_frozen() -> None:
    assert full_attack_summary() == {
        "subsets": {"tested": 16, "accepted": 1},
        "permutations": {"tested": 24, "accepted": 1},
        "statuses": {"tested": 81, "accepted": 1},
    }
