"""Synthetic stopping rule for repeated adversarial defeater search.

The model is intentionally narrow: after k comparable search rounds with zero
new defeater classes, it bounds the per-round probability of discovering a new
class under a Bernoulli/iid-like surrogate.  It does not prove completeness.
"""

from __future__ import annotations

import math


def zero_novelty_upper_bound(
    zero_novel_rounds: int,
    *,
    alpha: float = 0.05,
) -> float:
    """One-sided upper bound on per-round novelty probability.

    With zero discoveries in k Bernoulli rounds, solve:

        (1 - p_upper)^k = alpha

    giving p_upper = 1 - alpha**(1/k).
    """
    if zero_novel_rounds < 1:
        raise ValueError("zero_novel_rounds must be >= 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    return 1.0 - alpha ** (1.0 / zero_novel_rounds)


def minimum_zero_novel_rounds(
    target_upper_bound: float,
    *,
    alpha: float = 0.05,
) -> int:
    """Minimum consecutive zero-novelty rounds to meet a target upper bound."""
    if not 0 < target_upper_bound < 1:
        raise ValueError("target_upper_bound must be in (0, 1)")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")

    # Need 1 - alpha**(1/k) <= target.
    # Rearrangement yields k >= log(alpha)/log(1-target).
    raw = math.log(alpha) / math.log(1.0 - target_upper_bound)
    return math.ceil(raw)


def should_pause_defeater_search(
    zero_novel_rounds: int,
    *,
    target_upper_bound: float,
    alpha: float = 0.05,
) -> bool:
    """Return True when the declared surrogate stopping threshold is met."""
    return zero_novelty_upper_bound(
        zero_novel_rounds,
        alpha=alpha,
    ) <= target_upper_bound
