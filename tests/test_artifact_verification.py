from hashlib import sha256

import pytest

from dissociated_control_systems.artifact_verification import (
    normalize_sha256,
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
