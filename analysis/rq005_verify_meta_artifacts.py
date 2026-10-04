"""Verify downloaded RQ-005 META-A artifacts against the frozen OSF manifest.

Usage:
    python analysis/rq005_verify_meta_artifacts.py \
        specs/RQ-005-META-A-OSF-MANIFEST.json /path/to/downloaded/artifacts

The script performs no network access. It fails closed on missing files, size
mismatches, digest mismatches, duplicate manifest names, or malformed entries.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dissociated_control_systems.artifact_verification import verify_sha256


def manifest_artifacts(payload: dict[str, object]) -> tuple[dict[str, object], ...]:
    artifacts: list[dict[str, object]] = []
    for section_name in ("supplement_s2", "supplement_s3"):
        section = payload.get(section_name)
        if not isinstance(section, dict):
            raise ValueError(f"missing manifest section {section_name}")
        values = section.get("artifacts")
        if not isinstance(values, list):
            raise ValueError(f"{section_name}.artifacts must be a list")
        for item in values:
            if not isinstance(item, dict):
                raise ValueError("artifact entries must be objects")
            artifacts.append(item)

    names = [str(item.get("name", "")) for item in artifacts]
    if any(not name for name in names):
        raise ValueError("artifact name must not be empty")
    if len(names) != len(set(names)):
        raise ValueError("artifact names must be unique across the manifest")
    return tuple(artifacts)


def verify_manifest(manifest_path: Path, artifact_dir: Path) -> dict[str, object]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest_artifacts(payload)
    verified = []

    for item in artifacts:
        name = str(item["name"])
        expected_size = item.get("size_bytes")
        expected_sha = item.get("sha256")
        if not isinstance(expected_size, int) or expected_size < 0:
            raise ValueError(f"invalid size_bytes for {name}")
        if not isinstance(expected_sha, str):
            raise ValueError(f"invalid sha256 for {name}")

        path = artifact_dir / name
        if not path.is_file():
            raise FileNotFoundError(f"missing frozen artifact: {path}")
        observed_size = path.stat().st_size
        if observed_size != expected_size:
            raise ValueError(
                f"artifact size mismatch for {name}: "
                f"expected {expected_size}, observed {observed_size}"
            )
        digest = verify_sha256(path, expected_sha)
        verified.append(
            {
                "name": name,
                "size_bytes": observed_size,
                "sha256": digest,
                "status": "VERIFIED",
            }
        )

    return {
        "manifest": str(manifest_path),
        "artifact_dir": str(artifact_dir),
        "verified_count": len(verified),
        "artifacts": verified,
        "status": "ALL_ARTIFACTS_VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("artifact_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = verify_manifest(args.manifest, args.artifact_dir)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
