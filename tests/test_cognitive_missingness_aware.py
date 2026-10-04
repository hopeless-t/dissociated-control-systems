from dissociated_control_systems.cognitive_missingness_aware import (
    is_observed,
    missingness_aware_restoration,
)


def test_missing_marker_overrides_imputed_value():
    row = {
        "self_reference_gap": 0.123,
        "_missing_self_reference_gap": 1.0,
    }
    assert not is_observed(row, "self_reference_gap")


def test_missingness_aware_curve_is_bounded():
    result = missingness_aware_restoration()
    for row in result["rows"]:
        assert 0.0 <= row["validation_accuracy"] <= 1.0
        assert 0.0 <= row["test_accuracy"] <= 1.0
        assert row["test_oracle_union"] >= max(
            row["test_bayes_accuracy"],
            row["test_knn_accuracy"],
        )
