from math import log

from dissociated_control_systems.meta_input_failure_fixture import (
    compare_metadata_bindings,
    inverse_variance_pooled_ratio,
)


def test_effect_pool_does_not_depend_on_sample_metadata_fixture() -> None:
    result = compare_metadata_bindings(
        log_effects=[log(0.8), log(1.0), log(1.2)],
        standard_errors=[0.2, 0.15, 0.25],
        correct_intervention_n=[100, 120, 90],
        correct_control_n=[100, 120, 90],
        alternate_intervention_n=[25, 400, 10],
        alternate_control_n=[30, 350, 15],
    )

    assert result["pooled_effect_unchanged"] is True
    assert result["pooled_effect_correct_metadata"] == result[
        "pooled_effect_alternate_metadata"
    ]
    assert result["correct_sample_total"] == 620
    assert result["alternate_sample_total"] == 830
    assert result["sample_total_changed"] is True


def test_identical_effect_and_se_vectors_have_identical_pool() -> None:
    effects = [log(0.7), log(0.9), log(1.1), log(1.3)]
    se = [0.2, 0.3, 0.25, 0.15]
    first = inverse_variance_pooled_ratio(effects, se)
    second = inverse_variance_pooled_ratio(list(effects), list(se))
    assert first == second
