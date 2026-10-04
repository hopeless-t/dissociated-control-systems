from dissociated_control_systems.curriculum import (
    CurriculumTask,
    choose_curriculum_task,
)


def test_curriculum_prefers_high_information_low_redundancy_task() -> None:
    repeat_walk = CurriculumTask(
        name="repeat-walk",
        information_gain=0.4,
        gap_coverage=0.3,
        transfer_value=0.3,
        redundancy=0.8,
        execution_cost=1.0,
        observation_cost=1.0,
        integration_cost=0.5,
    )
    foreshortening = CurriculumTask(
        name="foreshortening",
        information_gain=0.9,
        gap_coverage=0.9,
        transfer_value=0.8,
        redundancy=0.1,
        execution_cost=1.5,
        observation_cost=1.0,
        integration_cost=0.5,
    )
    assert choose_curriculum_task((repeat_walk, foreshortening)) == foreshortening


def test_total_cost_is_additive() -> None:
    task = CurriculumTask(
        name="x",
        information_gain=1.0,
        gap_coverage=1.0,
        transfer_value=1.0,
        redundancy=0.0,
        execution_cost=2.0,
        observation_cost=3.0,
        integration_cost=4.0,
    )
    assert task.total_cost == 9.0


def test_empty_curriculum_fails_closed() -> None:
    try:
        choose_curriculum_task(())
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
