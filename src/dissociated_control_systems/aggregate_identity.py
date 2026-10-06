"""Aggregate sample-size provenance checks for RQ-005 META-A.

A reported total can be arithmetically correct for a displayed count vector
while the displayed rows are not correctly bound to trial identities. This
module keeps those questions separate.
"""

from __future__ import annotations

from collections.abc import Iterable


def pair_total(pairs: Iterable[tuple[int, int]]) -> int:
    total = 0
    seen = 0
    for intervention_n, control_n in pairs:
        for value in (intervention_n, control_n):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError("sample counts must be positive integers")
        total += intervention_n + control_n
        seen += 1
    if seen == 0:
        raise ValueError("at least one count pair is required")
    return total


def compare_aggregate_n(
    *,
    reported_n: int,
    displayed_pairs: Iterable[tuple[int, int]],
    own_identity_pairs: Iterable[tuple[int, int]],
) -> dict[str, object]:
    """Compare reported N to displayed and independently bound count vectors.

    This is a provenance diagnostic. A mismatch does not prove that the
    published total is wrong because endpoint-specific exclusions may exist.
    """

    if isinstance(reported_n, bool) or not isinstance(reported_n, int) or reported_n <= 0:
        raise ValueError("reported_n must be a positive integer")
    displayed_n = pair_total(displayed_pairs)
    own_n = pair_total(own_identity_pairs)
    return {
        "reported_n": reported_n,
        "displayed_count_total": displayed_n,
        "own_identity_count_total": own_n,
        "reported_matches_displayed": reported_n == displayed_n,
        "reported_matches_own_identity": reported_n == own_n,
        "displayed_minus_reported": displayed_n - reported_n,
        "own_identity_minus_reported": own_n - reported_n,
        "status": (
            "AGGREGATE_N_IDENTITY_CONFLICT_CANDIDATE"
            if reported_n == displayed_n and reported_n != own_n
            else "NO_SPECIFIC_DISPLAY_VECTOR_CONFLICT"
        ),
    }
