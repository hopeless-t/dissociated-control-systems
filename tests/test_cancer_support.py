from dissociated_control_systems.cancer_support import (
    SupportEvidence,
    SupportStatus,
    classify_support,
    permits_confident_forecast,
)


def _evidence(**overrides):
    values = dict(
        semantic_contract_valid=True,
        feature_support_valid=True,
        transition_residual_valid=True,
        future_intervention_declared=True,
        model_family_supported=True,
        predictive_uncertainty_acceptable=True,
    )
    values.update(overrides)
    return SupportEvidence(**values)


def test_supported_forecast_requires_all_gates():
    evidence = _evidence()
    assert classify_support(evidence) is SupportStatus.SUPPORTED
    assert permits_confident_forecast(evidence)


def test_semantic_failure_precedes_model_confidence():
    evidence = _evidence(
        semantic_contract_valid=False,
        predictive_uncertainty_acceptable=True,
    )
    assert classify_support(evidence) is SupportStatus.SEMANTICS_UNKNOWN
    assert not permits_confident_forecast(evidence)


def test_missing_future_path_is_underspecified_not_low_confidence():
    evidence = _evidence(future_intervention_declared=False)
    assert classify_support(evidence) is SupportStatus.FORECAST_UNDERSPECIFIED


def test_feature_or_model_family_shift_is_out_of_support():
    assert classify_support(
        _evidence(feature_support_valid=False)
    ) is SupportStatus.OUT_OF_SUPPORT
    assert classify_support(
        _evidence(model_family_supported=False)
    ) is SupportStatus.OUT_OF_SUPPORT


def test_transition_failure_is_distinct_from_feature_ood():
    evidence = _evidence(transition_residual_valid=False)
    assert classify_support(evidence) is SupportStatus.TRANSITION_UNRESOLVED


def test_uncertainty_is_last_gate():
    evidence = _evidence(predictive_uncertainty_acceptable=False)
    assert classify_support(evidence) is SupportStatus.UNCERTAIN
