"""Dialectic/defeater-search metadata for DCS assurance artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from .defeater_saturation import (
    should_pause_defeater_search,
    zero_novelty_upper_bound,
)


@dataclass(frozen=True)
class DefeaterSearchRound:
    strategy_family: str
    novel_classes: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.strategy_family:
            raise ValueError("strategy_family must be non-empty")


@dataclass(frozen=True)
class DefeaterSearchLog:
    rounds: tuple[DefeaterSearchRound, ...]

    @property
    def unique_strategy_families(self) -> frozenset[str]:
        return frozenset(round.strategy_family for round in self.rounds)

    @property
    def discovered_classes(self) -> frozenset[str]:
        found: set[str] = set()
        for round in self.rounds:
            found.update(round.novel_classes)
        return frozenset(found)

    @property
    def trailing_zero_novel_rounds(self) -> int:
        count = 0
        for round in reversed(self.rounds):
            if round.novel_classes:
                break
            count += 1
        return count


@dataclass(frozen=True)
class SearchAssessment:
    saturated_under_surrogate: bool
    novelty_upper_bound: float | None
    strategy_family_count: int
    discovered_class_count: int
    reasons: tuple[str, ...]


def assess_defeater_search(
    log: DefeaterSearchLog,
    *,
    target_novelty_upper_bound: float,
    alpha: float = 0.05,
    min_strategy_families: int = 2,
) -> SearchAssessment:
    """Assess search sufficiency without claiming defeater completeness."""
    if min_strategy_families < 1:
        raise ValueError("min_strategy_families must be >= 1")

    reasons: list[str] = []
    trailing = log.trailing_zero_novel_rounds
    if trailing:
        bound = zero_novelty_upper_bound(trailing, alpha=alpha)
        statistical_stop = should_pause_defeater_search(
            trailing,
            target_upper_bound=target_novelty_upper_bound,
            alpha=alpha,
        )
    else:
        bound = None
        statistical_stop = False
        reasons.append("no_trailing_zero_novelty_run")

    family_count = len(log.unique_strategy_families)
    strategy_ok = family_count >= min_strategy_families
    if not strategy_ok:
        reasons.append("insufficient_strategy_diversity")
    if not statistical_stop:
        reasons.append("novelty_upper_bound_above_target")

    return SearchAssessment(
        saturated_under_surrogate=statistical_stop and strategy_ok,
        novelty_upper_bound=bound,
        strategy_family_count=family_count,
        discovered_class_count=len(log.discovered_classes),
        reasons=tuple(dict.fromkeys(reasons)),
    )
