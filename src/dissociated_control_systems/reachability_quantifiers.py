"""Quantifier-order helpers for partially observed reachability.

For a set of latent states X and controls U:

    statewise reachability:  for every x there exists some u that succeeds
    uniform policy reachability: there exists one u that succeeds for every x

These are not equivalent.  Under partial observability, statewise reachability
can require an observer capable of selecting the appropriate control.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class QuantifiedReachability(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ReachabilityMatrix:
    """Boolean rows are latent states; columns are allowed controls."""

    rows: tuple[tuple[bool, ...], ...]

    @classmethod
    def from_rows(cls, rows: Iterable[Iterable[bool]]) -> "ReachabilityMatrix":
        rows_t = tuple(tuple(bool(v) for v in row) for row in rows)
        if not rows_t:
            return cls(())
        width = len(rows_t[0])
        if width == 0:
            raise ValueError("at least one control column is required")
        if any(len(row) != width for row in rows_t):
            raise ValueError("all reachability rows must have equal width")
        return cls(rows_t)


def statewise_reachability(matrix: ReachabilityMatrix) -> QuantifiedReachability:
    """Evaluate forall state, exists control."""
    if not matrix.rows:
        return QuantifiedReachability.UNKNOWN
    return (
        QuantifiedReachability.PASS
        if all(any(row) for row in matrix.rows)
        else QuantifiedReachability.FAIL
    )


def uniform_policy_reachability(matrix: ReachabilityMatrix) -> QuantifiedReachability:
    """Evaluate exists one control, forall states."""
    if not matrix.rows:
        return QuantifiedReachability.UNKNOWN
    width = len(matrix.rows[0])
    exists_common = any(
        all(row[column] for row in matrix.rows)
        for column in range(width)
    )
    return QuantifiedReachability.PASS if exists_common else QuantifiedReachability.FAIL


def observer_selection_gap(matrix: ReachabilityMatrix) -> bool:
    """True when recovery is statewise possible but no uniform control exists."""
    return (
        statewise_reachability(matrix) is QuantifiedReachability.PASS
        and uniform_policy_reachability(matrix) is QuantifiedReachability.FAIL
    )
