"""Risk-asymmetric checkpoint decisions for declared support intervals.

This is a synthetic decision-theory helper.  It does not turn qualitative
scientific evidence into calibrated probabilities; callers must supply a
meaningful support interval if they use it.
"""

from __future__ import annotations

from .projection_protocol import CheckStatus


def pass_threshold(
    *,
    false_pass_cost: float,
    false_block_cost: float,
) -> float:
    """Expected-loss threshold for PASS under two-action decision theory.

    Let q be the probability that the checkpoint condition is actually true.

        L(PASS)  = C_fp * (1 - q)
        L(BLOCK) = C_fb * q

    PASS minimizes expected loss when:

        q >= C_fp / (C_fp + C_fb)
    """
    if false_pass_cost <= 0 or false_block_cost <= 0:
        raise ValueError("costs must be > 0")
    return false_pass_cost / (false_pass_cost + false_block_cost)


def interval_decision(
    support_lower: float,
    support_upper: float,
    *,
    false_pass_cost: float,
    false_block_cost: float,
) -> CheckStatus:
    """Fail closed when the support interval straddles the decision threshold."""
    if not 0 <= support_lower <= support_upper <= 1:
        raise ValueError("support interval must satisfy 0 <= lower <= upper <= 1")

    threshold = pass_threshold(
        false_pass_cost=false_pass_cost,
        false_block_cost=false_block_cost,
    )

    if support_lower >= threshold:
        return CheckStatus.PASS
    if support_upper < threshold:
        return CheckStatus.FAIL
    return CheckStatus.UNKNOWN
