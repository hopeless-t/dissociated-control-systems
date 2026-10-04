import pytest

from dissociated_control_systems.pipeline_convergence import (
    PipelineObservation,
    reconcile_pipelines,
)


def obs(pipeline, snapshot, estimate, lower, upper):
    return PipelineObservation(
        pipeline_id=pipeline,
        snapshot_id=snapshot,
        analysis_id="pooled_os_hr",
        estimate=estimate,
        lower=lower,
        upper=upper,
    )


def test_independent_pipelines_can_converge() -> None:
    result = reconcile_pipelines(
        [
            obs("model", "v2", 0.800, 0.710, 0.900),
            obs("figure", "v2", 0.802, 0.711, 0.899),
        ],
        tolerance=0.005,
    )
    assert result["status"] == "PIPELINES_CONVERGED"


def test_bognar_final_observers_are_not_converged() -> None:
    result = reconcile_pipelines(
        [
            obs("results_text_model_observer", "final_publication", 1.01, 0.95, 1.07),
            obs("forest_plot_observer", "final_publication", 0.97, 0.87, 1.08),
            obs("abstract_observer", "final_publication", 0.97, 0.87, 1.08),
        ],
        tolerance=0.005,
    )
    assert result["status"] == "PIPELINE_STATE_DIVERGENCE"
    assert result["point_span"] == pytest.approx(0.04)
    assert result["lower_span"] == pytest.approx(0.08)


def test_preprint_and_final_are_not_same_snapshot_by_default() -> None:
    result = reconcile_pipelines(
        [
            obs("preprint_model", "preprint_v1", 1.01, 0.95, 1.07),
            obs("final_figure", "version_of_record", 0.97, 0.87, 1.08),
        ]
    )
    assert result["status"] == "PIPELINE_STATE_DIVERGENCE"
    assert result["snapshot_ids"] == ("preprint_v1", "version_of_record")


def test_different_analysis_ids_fail_closed() -> None:
    first = obs("a", "s", 1.0, 0.9, 1.1)
    second = PipelineObservation(
        pipeline_id="b",
        snapshot_id="s",
        analysis_id="rfs_hr",
        estimate=1.0,
        lower=0.9,
        upper=1.1,
    )
    with pytest.raises(ValueError, match="different declared analyses"):
        reconcile_pipelines([first, second])
