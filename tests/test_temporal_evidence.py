import pytest

from dissociated_control_systems.temporal_evidence import (
    TimedObservation,
    split_by_landmark,
    validate_available_by_landmark,
)


def test_future_response_cannot_enter_diagnosis_origin_model() -> None:
    observations = [
        TimedObservation("baseline_npi", 0.0),
        TimedObservation("radiologic_complete_response", 12.0),
    ]
    with pytest.raises(ValueError, match="radiologic_complete_response"):
        validate_available_by_landmark(observations, landmark_month=0.0)


def test_same_response_is_allowed_after_landmark_moves_forward() -> None:
    observations = [
        TimedObservation("baseline_npi", 0.0),
        TimedObservation("radiologic_complete_response", 12.0),
    ]
    assert validate_available_by_landmark(observations, landmark_month=12.0) == tuple(
        observations
    )


def test_split_exposes_future_information_explicitly() -> None:
    observations = [
        TimedObservation("recurrence_site", 20.0),
        TimedObservation("response_depth", 26.0),
        TimedObservation("survivor_narrative", 180.0),
    ]
    available, future = split_by_landmark(observations, landmark_month=26.0)
    assert [item.name for item in available] == ["recurrence_site", "response_depth"]
    assert [item.name for item in future] == ["survivor_narrative"]
