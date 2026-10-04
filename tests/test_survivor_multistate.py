import pytest

from dissociated_control_systems.survivor_multistate import (
    ObservedTrajectory,
    SurvivorTrajectory,
    classify_trajectory,
    same_overall_survival_distinct_paths,
)


def test_post_recurrence_interval_only_exists_after_recurrence() -> None:
    no_recurrence = ObservedTrajectory(180.0, False)
    assert no_recurrence.post_recurrence_observation_months is None

    recurrence = ObservedTrajectory(180.0, True, 24.0)
    assert recurrence.post_recurrence_observation_months == pytest.approx(156.0)


def test_same_overall_survival_can_hide_distinct_paths() -> None:
    late, early = same_overall_survival_distinct_paths()
    assert late.overall_survival_months == early.overall_survival_months
    assert classify_trajectory(late) == SurvivorTrajectory.LATE_RECURRENCE
    assert classify_trajectory(early) == SurvivorTrajectory.EARLY_RECURRENCE_DURABLE_CONTROL


def test_early_recurrence_rapid_failure_is_separate() -> None:
    observation = ObservedTrajectory(
        overall_survival_months=46.0,
        recurrence_recorded=True,
        recurrence_months=18.0,
        disease_death=True,
    )
    assert classify_trajectory(observation) == SurvivorTrajectory.EARLY_RECURRENCE_RAPID_FAILURE


def test_invalid_transition_order_fails_closed() -> None:
    with pytest.raises(ValueError):
        ObservedTrajectory(20.0, True, 30.0)
