import pytest

from dissociated_control_systems.meta_reconciliation import (
    PublishedEstimate,
    reconcile_same_analysis,
    require_canonicalizable,
)


def estimate(source: str, value: float, lower: float, upper: float) -> PublishedEstimate:
    return PublishedEstimate(
        report_id="REPORT-2024",
        analysis_id="primary_pooled_os",
        source_location=source,
        endpoint="OS",
        effect_metric="HR",
        estimate=value,
        lower=lower,
        upper=upper,
    )


def test_rounding_scale_difference_can_remain_consistent() -> None:
    result = reconcile_same_analysis(
        [
            estimate("abstract", 0.800, 0.710, 0.900),
            estimate("body", 0.802, 0.711, 0.899),
        ],
        tolerance=0.005,
    )
    assert result.status == "CONSISTENT_WITHIN_TOLERANCE"
    assert require_canonicalizable(result).source_location == "abstract"


def test_bognar_2024_abstract_vs_body_known_answer_is_conflict() -> None:
    result = reconcile_same_analysis(
        [
            estimate("published_abstract", 0.97, 0.87, 1.08),
            estimate("published_results", 1.01, 0.95, 1.07),
        ],
        tolerance=0.005,
    )
    assert result.status == "INTERNAL_CONFLICT"
    assert result.max_point_difference == pytest.approx(0.04)
    assert result.max_lower_difference == pytest.approx(0.08)
    with pytest.raises(ValueError, match="cannot be canonicalized"):
        require_canonicalizable(result)


def test_different_declared_analyses_cannot_be_silently_reconciled() -> None:
    first = estimate("abstract", 0.97, 0.87, 1.08)
    second = PublishedEstimate(
        report_id="REPORT-2024",
        analysis_id="sensitivity_os",
        source_location="supplement",
        endpoint="OS",
        effect_metric="HR",
        estimate=0.97,
        lower=0.87,
        upper=1.08,
    )
    with pytest.raises(ValueError, match="different declared analyses"):
        reconcile_same_analysis([first, second])


def test_duplicate_source_location_fails_closed() -> None:
    with pytest.raises(ValueError, match="source_location"):
        reconcile_same_analysis(
            [
                estimate("abstract", 0.97, 0.87, 1.08),
                estimate("abstract", 0.97, 0.87, 1.08),
            ]
        )
