"""Fail-closed artifact identity verification for RQ-005.

External datasets and analysis code are only eligible for reproduction after
byte-level identity has been checked against a frozen manifest.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path


_HEX = frozenset("0123456789abcdef")


def normalize_sha256(value: str) -> str:
    """Normalize and validate a bare or `sha256:`-prefixed digest."""
    digest = value.strip().lower()
    if digest.startswith("sha256:"):
        digest = digest.removeprefix("sha256:")
    if len(digest) != 64 or any(char not in _HEX for char in digest):
        raise ValueError("expected a 64-character hexadecimal SHA256 digest")
    return digest


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    """Hash a file without loading the whole artifact into memory."""
    if isinstance(chunk_size, bool) or not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an integer")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    file_path = Path(path)
    digest = sha256()
    with file_path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path: str | Path, expected: str) -> str:
    """Return the verified digest, raising on any byte mismatch."""
    wanted = normalize_sha256(expected)
    observed = sha256_file(path)
    if observed != wanted:
        raise ValueError(
            f"artifact SHA256 mismatch: expected {wanted}, observed {observed}"
        )
    return observed
