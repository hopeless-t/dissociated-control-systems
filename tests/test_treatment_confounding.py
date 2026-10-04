from dissociated_control_systems.treatment_confounding import (
    confounding_by_indication_fixture,
    observational_treated_survival,
    observational_untreated_survival,
    standardized_causal_risk_difference,
)


def test_treatment_helps_within_both_strata() -> None:
    low, high = confounding_by_indication_fixture()
    assert low.causal_risk_difference > 0
    assert high.causal_risk_difference > 0


def test_naive_pooled_association_reverses_treatment_direction() -> None:
    strata = confounding_by_indication_fixture()
    treated = observational_treated_survival(strata)
    untreated = observational_untreated_survival(strata)

    assert treated == 0.455
    assert untreated == 0.83
    assert treated - untreated < 0


def test_standardization_recovers_positive_average_causal_direction() -> None:
    strata = confounding_by_indication_fixture()
    assert standardized_causal_risk_difference(strata) == 0.125
