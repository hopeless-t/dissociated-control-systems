from hashlib import sha256

import pytest

from dissociated_control_systems.artifact_verification import (
    normalize_sha256,
    safe_artifact_path,
    sha256_file,
    verify_sha256,
)


def test_verify_known_bytes(tmp_path) -> None:
    payload = b"rq005-known-answer\n"
    path = tmp_path / "artifact.bin"
    path.write_bytes(payload)
    expected = sha256(payload).hexdigest()

    assert sha256_file(path) == expected
    assert verify_sha256(path, expected) == expected
    assert verify_sha256(path, f"sha256:{expected}") == expected


def test_one_byte_mutation_fails_closed(tmp_path) -> None:
    original = b"same artifact? no"
    mutated = b"same artifact? NO"
    path = tmp_path / "artifact.bin"
    path.write_bytes(mutated)
    expected = sha256(original).hexdigest()

    with pytest.raises(ValueError, match="mismatch"):
        verify_sha256(path, expected)


def test_invalid_digest_format_fails_closed() -> None:
    with pytest.raises(ValueError):
        normalize_sha256("not-a-digest")


def test_chunk_size_validation(tmp_path) -> None:
    path = tmp_path / "artifact.bin"
    path.write_bytes(b"x")
    with pytest.raises(ValueError):
        sha256_file(path, chunk_size=0)


def test_safe_artifact_path_accepts_direct_regular_file(tmp_path) -> None:
    path = tmp_path / "artifact.bin"
    path.write_bytes(b"known")
    assert safe_artifact_path(tmp_path, "artifact.bin") == path.resolve()


@pytest.mark.parametrize("name", ["../artifact.bin", "sub/artifact.bin", "/tmp/x", " artifact.bin"])
def test_safe_artifact_path_rejects_non_frozen_name_shapes(tmp_path, name) -> None:
    with pytest.raises((ValueError, FileNotFoundError)):
        safe_artifact_path(tmp_path, name)


def test_safe_artifact_path_rejects_symlink(tmp_path) -> None:
    target = tmp_path / "target.bin"
    target.write_bytes(b"known")
    link = tmp_path / "artifact.bin"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this platform")

    with pytest.raises(ValueError, match="symlink"):
        safe_artifact_path(tmp_path, "artifact.bin")
