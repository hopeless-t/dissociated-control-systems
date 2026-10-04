from dissociated_control_systems.assurance_versioning import (
    DependencySnapshot,
    compare_snapshot,
    snapshot_matches,
)


def test_identical_dependency_revisions_keep_certificate_fresh() -> None:
    snapshot = DependencySnapshot.from_mapping(
        {
            "raw-data": "sha:data-v1",
            "analysis-code": "git:abc123",
            "model-spec": "git:def456",
        }
    )

    assert snapshot_matches(
        snapshot,
        {
            "raw-data": "sha:data-v1",
            "analysis-code": "git:abc123",
            "model-spec": "git:def456",
        },
    )


def test_changed_analysis_revision_marks_certificate_stale() -> None:
    snapshot = DependencySnapshot.from_mapping(
        {
            "raw-data": "sha:data-v1",
            "analysis-code": "git:abc123",
        }
    )

    report = compare_snapshot(
        snapshot,
        {
            "raw-data": "sha:data-v1",
            "analysis-code": "git:abc999",
        },
    )

    assert report.stale
    assert report.changed == ("analysis-code",)


def test_removed_dependency_marks_certificate_stale() -> None:
    snapshot = DependencySnapshot.from_mapping(
        {
            "raw-data": "sha:data-v1",
            "analysis-code": "git:abc123",
        }
    )

    report = compare_snapshot(
        snapshot,
        {"raw-data": "sha:data-v1"},
    )

    assert report.stale
    assert report.missing == ("analysis-code",)


def test_new_declared_dependency_also_invalidates_old_certificate() -> None:
    snapshot = DependencySnapshot.from_mapping(
        {"raw-data": "sha:data-v1"}
    )

    report = compare_snapshot(
        snapshot,
        {
            "raw-data": "sha:data-v1",
            "new-model-rule": "git:new1",
        },
    )

    assert report.stale
    assert report.added == ("new-model-rule",)
