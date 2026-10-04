"""Trial/publication identity ledger primitives for RQ-005 META-A.

Meta-analysis must count randomized cohorts, not papers. Multiple publications
may attach to one stable trial identity without becoming independent trials.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TrialPublication:
    trial_id: str
    publication_id: str
    publication_role: str
    randomized_population_id: str
    endpoint: str
    effect_metric: str
    followup_months: float | None = None
    post_randomization_selection: bool = False

    def __post_init__(self) -> None:
        for field in (
            "trial_id",
            "publication_id",
            "publication_role",
            "randomized_population_id",
            "endpoint",
            "effect_metric",
        ):
            if not getattr(self, field).strip():
                raise ValueError(f"{field} must not be empty")
        if self.followup_months is not None and self.followup_months < 0:
            raise ValueError("followup_months must be non-negative")


def validate_trial_ledger(
    records: Iterable[TrialPublication],
) -> tuple[TrialPublication, ...]:
    items = tuple(records)
    if not items:
        raise ValueError("trial ledger must not be empty")

    publication_ids: set[str] = set()
    trial_to_population: dict[str, str] = {}
    for record in items:
        if record.publication_id in publication_ids:
            raise ValueError(f"duplicate publication_id: {record.publication_id}")
        publication_ids.add(record.publication_id)

        previous = trial_to_population.setdefault(
            record.trial_id, record.randomized_population_id
        )
        if previous != record.randomized_population_id:
            raise ValueError(
                f"trial {record.trial_id!r} maps to multiple randomized populations"
            )
    return items


def unique_trial_ids(records: Iterable[TrialPublication]) -> tuple[str, ...]:
    items = validate_trial_ledger(records)
    return tuple(sorted({record.trial_id for record in items}))


def count_independent_trials(records: Iterable[TrialPublication]) -> int:
    return len(unique_trial_ids(records))


def publications_for_trial(
    records: Iterable[TrialPublication], trial_id: str
) -> tuple[TrialPublication, ...]:
    items = validate_trial_ledger(records)
    matches = tuple(record for record in items if record.trial_id == trial_id)
    if not matches:
        raise KeyError(trial_id)
    return matches
