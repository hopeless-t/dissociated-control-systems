import pytest

from dissociated_control_systems.mechanism_scope import (
    Transition,
    classic_pre_recurrence_dormancy_claim,
    require_transition_support,
)


def test_classic_dormancy_is_scoped_to_recurrence_timing() -> None:
    claim = classic_pre_recurrence_dormancy_claim()
    require_transition_support(claim, Transition.DIAGNOSIS_TO_RECURRENCE)


def test_classic_dormancy_cannot_be_laundered_into_post_recurrence_control() -> None:
    claim = classic_pre_recurrence_dormancy_claim()
    with pytest.raises(ValueError, match="recurrence_to_cancer_death"):
        require_transition_support(claim, Transition.RECURRENCE_TO_CANCER_DEATH)
