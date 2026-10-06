from dissociated_control_systems.assurance_dialectic import (
    DefeaterSearchLog,
    DefeaterSearchRound,
    assess_defeater_search,
)


def test_zero_recorded_defeaters_without_search_is_not_saturated() -> None:
    result = assess_defeater_search(
        DefeaterSearchLog(()),
        target_novelty_upper_bound=0.20,
        min_strategy_families=1,
    )

    assert not result.saturated_under_surrogate
    assert "no_trailing_zero_novelty_run" in result.reasons


def test_many_identical_strategy_rounds_fail_diversity_requirement() -> None:
    log = DefeaterSearchLog(
        tuple(
            DefeaterSearchRound("same-strategy")
            for _ in range(59)
        )
    )

    result = assess_defeater_search(
        log,
        target_novelty_upper_bound=0.05,
        min_strategy_families=2,
    )

    assert not result.saturated_under_surrogate
    assert "insufficient_strategy_diversity" in result.reasons


def test_diverse_zero_novelty_tail_can_meet_declared_surrogate_stop() -> None:
    rounds = []
    for i in range(59):
        strategy = "evidence-attack" if i % 2 == 0 else "reasoning-attack"
        rounds.append(DefeaterSearchRound(strategy))
    log = DefeaterSearchLog(tuple(rounds))

    result = assess_defeater_search(
        log,
        target_novelty_upper_bound=0.05,
        min_strategy_families=2,
    )

    assert result.saturated_under_surrogate
    assert result.novelty_upper_bound is not None
    assert result.novelty_upper_bound <= 0.05


def test_new_defeater_resets_trailing_zero_novelty_streak() -> None:
    rounds = [DefeaterSearchRound("evidence") for _ in range(20)]
    rounds.append(
        DefeaterSearchRound(
            "reasoning",
            frozenset({"new-circular-support-class"}),
        )
    )
    rounds.extend(DefeaterSearchRound("scope") for _ in range(3))

    log = DefeaterSearchLog(tuple(rounds))

    assert log.trailing_zero_novel_rounds == 3
    assert "new-circular-support-class" in log.discovered_classes
