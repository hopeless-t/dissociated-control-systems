from dissociated_control_systems.cancer_observation_contract import (
    ForecastSupport,
    ObservationRecord,
    validate_calibration_continuity,
    validate_expected_time,
)


def _support(**overrides):
    values = dict(
        timing_semantics_valid=True,
        calibration_traceable=True,
        censoring_accounted=True,
        treatment_history_complete=True,
        future_intervention_declared=True,
        model_support_declared=True,
        correlated_error_model_declared=True,
    )
    values.update(overrides)
    return ForecastSupport(**values)


def test_complete_support_can_permit_high_confidence():
    support = _support()
    assert support.permits_high_confidence
    assert support.missing_support == ()


def test_any_missing_support_blocks_high_confidence():
    fields = (
        "timing_semantics_valid",
        "calibration_traceable",
        "censoring_accounted",
        "treatment_history_complete",
        "future_intervention_declared",
        "model_support_declared",
        "correlated_error_model_declared",
    )
    for field in fields:
        support = _support(**{field: False})
        assert not support.permits_high_confidence
        assert field in support.missing_support


def test_mislabeled_observation_time_fails_closed():
    sample = ObservationRecord(
        modality="ctDNA",
        observed_at=43,
        calibration_id="assay-v1",
        value=0.2,
    )
    try:
        validate_expected_time(sample, expected_at=60, tolerance=3)
    except ValueError:
        pass
    else:
        raise AssertionError("silently relabelled sampling time must fail closed")


def test_calibration_change_requires_explicit_bridge():
    samples = (
        ObservationRecord("ctDNA", 30, "assay-v1", value=0.3),
        ObservationRecord("ctDNA", 60, "assay-v2", value=0.2),
    )
    try:
        validate_calibration_continuity(samples)
    except ValueError:
        pass
    else:
        raise AssertionError("unbridged calibration drift must fail closed")

    validate_calibration_continuity(
        samples,
        bridged_pairs=frozenset({("assay-v1", "assay-v2")}),
    )


def test_below_detection_limit_is_censored_not_zero():
    sample = ObservationRecord(
        modality="resistance-clone",
        observed_at=30,
        calibration_id="panel-v1",
        lower_detection_limit=0.01,
        censored_below_limit=True,
    )
    assert sample.value is None
    assert sample.censored_below_limit
    assert sample.observation_kind == "below_detection_limit"

    try:
        ObservationRecord(
            modality="resistance-clone",
            observed_at=30,
            calibration_id="panel-v1",
            value=0.0,
            lower_detection_limit=0.01,
            censored_below_limit=True,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("censored result must not masquerade as exact zero")


def test_no_result_requires_explicit_reason():
    try:
        ObservationRecord(
            modality="ctDNA",
            observed_at=30,
            calibration_id="assay-v1",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("ambiguous null observation must fail closed")


def test_technical_failure_is_not_below_detection_limit():
    sample = ObservationRecord(
        modality="ctDNA",
        observed_at=30,
        calibration_id="assay-v1",
        missing_reason="technical_failure",
    )
    assert sample.value is None
    assert not sample.censored_below_limit
    assert sample.observation_kind == "technical_failure"


def test_not_collected_is_distinct_from_technical_failure():
    sample = ObservationRecord(
        modality="ctDNA",
        observed_at=30,
        calibration_id="assay-v1",
        missing_reason="not_collected",
    )
    assert sample.observation_kind == "not_collected"


def test_measured_value_cannot_also_be_missing():
    try:
        ObservationRecord(
            modality="ctDNA",
            observed_at=30,
            calibration_id="assay-v1",
            value=0.2,
            missing_reason="technical_failure",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("measured value and missing reason cannot coexist")
