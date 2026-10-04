import json
from pathlib import Path


def test_assurance_kernel_manifest_has_disjoint_existing_paths() -> None:
    root = Path(__file__).parents[1]
    manifest = json.loads(
        (root / "specs" / "HF01_ASSURANCE_KERNEL.json").read_text()
    )

    normative = tuple(manifest["normative_kernel"])
    advisory = tuple(manifest["diagnostic_or_advisory"])

    assert normative
    assert not (set(normative) & set(advisory))
    assert len(normative) == len(set(normative))
    assert len(advisory) == len(set(advisory))

    for relative in normative + advisory:
        assert (root / relative).is_file(), relative


def test_authority_kernel_is_smaller_than_advisory_surface() -> None:
    root = Path(__file__).parents[1]
    manifest = json.loads(
        (root / "specs" / "HF01_ASSURANCE_KERNEL.json").read_text()
    )

    assert len(manifest["normative_kernel"]) < len(
        manifest["diagnostic_or_advisory"]
    )
