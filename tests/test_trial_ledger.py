import pytest

from dissociated_control_systems.trial_ledger import (
    TrialPublication,
    count_independent_trials,
    publications_for_trial,
    validate_trial_ledger,
)


def test_multiple_publications_from_one_randomization_count_once() -> None:
    records = [
        TrialPublication(
            trial_id="TRIAL-A",
            publication_id="PMID-primary",
            publication_role="primary",
            randomized_population_id="RPOP-A",
            endpoint="OS",
            effect_metric="HR",
            followup_months=60,
        ),
        TrialPublication(
            trial_id="TRIAL-A",
            publication_id="PMID-followup",
            publication_role="long_term_followup",
            randomized_population_id="RPOP-A",
            endpoint="OS",
            effect_metric="HR",
            followup_months=120,
        ),
        TrialPublication(
            trial_id="TRIAL-A",
            publication_id="PMID-recurrence",
            publication_role="post_recurrence_mechanistic",
            randomized_population_id="RPOP-A",
            endpoint="post_recurrence_OS",
            effect_metric="HR",
            post_randomization_selection=True,
        ),
    ]

    assert count_independent_trials(records) == 1
    assert len(publications_for_trial(records, "TRIAL-A")) == 3


def test_distinct_randomizations_count_as_distinct_trials() -> None:
    records = [
        TrialPublication("A", "P1", "primary", "R1", "OS", "HR"),
        TrialPublication("B", "P2", "primary", "R2", "OS", "HR"),
    ]
    assert count_independent_trials(records) == 2


def test_same_trial_cannot_map_to_two_randomized_populations() -> None:
    records = [
        TrialPublication("A", "P1", "primary", "R1", "OS", "HR"),
        TrialPublication("A", "P2", "followup", "R2", "OS", "HR"),
    ]
    with pytest.raises(ValueError, match="multiple randomized populations"):
        validate_trial_ledger(records)


def test_duplicate_publication_id_fails_closed() -> None:
    records = [
        TrialPublication("A", "P1", "primary", "R1", "OS", "HR"),
        TrialPublication("B", "P1", "primary", "R2", "OS", "HR"),
    ]
    with pytest.raises(ValueError, match="duplicate publication_id"):
        validate_trial_ledger(records)
