import pytest

from dissociated_control_systems.trust_roots import (
    TrustRoot,
    TrustRootKind,
    validate_trust_boundary,
)


def test_every_primitive_evidence_node_needs_explicit_trust_root() -> None:
    report = validate_trust_boundary(
        ("raw-data", "external-paper"),
        (
            TrustRoot(
                "raw-data",
                TrustRootKind.RAW_OBSERVATION,
                ("downloaded bytes correspond to declared dataset accession",),
            ),
        ),
    )

    assert not report.complete
    assert report.missing_roots == ("external-paper",)


def test_complete_unique_trust_boundary_passes() -> None:
    report = validate_trust_boundary(
        ("raw-data", "external-paper"),
        (
            TrustRoot(
                "raw-data",
                TrustRootKind.RAW_OBSERVATION,
                ("dataset bytes correspond to declared accession",),
            ),
            TrustRoot(
                "external-paper",
                TrustRootKind.EXTERNAL_SOURCE,
                ("bibliographic source is authentic and correctly identified",),
            ),
        ),
    )

    assert report.complete
    assert report.missing_roots == ()
    assert report.duplicate_root_ids == ()


def test_duplicate_root_identity_is_rejected() -> None:
    roots = (
        TrustRoot(
            "same",
            TrustRootKind.RAW_OBSERVATION,
            ("assumption a",),
        ),
        TrustRoot(
            "same",
            TrustRootKind.EXTERNAL_SOURCE,
            ("assumption b",),
        ),
    )

    report = validate_trust_boundary(("same",), roots)

    assert not report.complete
    assert report.duplicate_root_ids == ("same",)


def test_trust_root_must_state_assumption() -> None:
    with pytest.raises(ValueError):
        TrustRoot("root", TrustRootKind.TOOL_RUNTIME, ())
