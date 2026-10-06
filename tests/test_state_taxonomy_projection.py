from dissociated_control_systems.state_taxonomy_projection import (
    matched_legacy_states,
    project_to_legacy,
)


def test_distinct_v2_states_can_have_identical_legacy_projection() -> None:
    left, right = matched_legacy_states()

    assert left != right
    assert project_to_legacy(left) == project_to_legacy(right)


def test_equal_legacy_state_hides_mechanical_branch_difference() -> None:
    left, right = matched_legacy_states()

    assert project_to_legacy(left).androgen == project_to_legacy(right).androgen
    assert project_to_legacy(left).structural_lock == project_to_legacy(right).structural_lock
    assert left.mechanical == 0.0
    assert right.mechanical == 1.0


def test_equal_legacy_state_hides_ecm_branch_difference() -> None:
    left, right = matched_legacy_states()

    assert left.ecm_remodeling == 1.0
    assert right.ecm_remodeling == 0.0
