"""Reusable retrospective baseline primitives for RQ-005.

These helpers are for method validation and exploratory cohort comparison.
They are not prognostic or clinical decision tools.
"""

from __future__ import annotations

from math import exp, log, sqrt
from statistics import mean
from typing import Iterable, Sequence


def fixed_horizon_survivor_label(
    os_months: float,
    vital_status: str,
    *,
    short_horizon_months: float = 60.0,
    long_horizon_months: float = 120.0,
) -> str | None:
    """Return a strict retrospective LTS/STS discovery label.

    STS:
        disease-specific death at or before the short horizon.
    LTS:
        observed overall-survival follow-up at or beyond the long horizon.

    Everyone else is intentionally unclassified to avoid pretending that
    right-censored patients with insufficient follow-up have a known class.
    """

    if isinstance(os_months, bool) or not isinstance(os_months, (int, float)):
        raise TypeError("os_months must be a real number")
    os_months = float(os_months)
    if os_months < 0:
        raise ValueError("os_months must be non-negative")
    if short_horizon_months <= 0 or long_horizon_months <= short_horizon_months:
        raise ValueError("require 0 < short_horizon < long_horizon")

    if vital_status == "Died of Disease" and os_months <= short_horizon_months:
        return "STS"
    if os_months >= long_horizon_months:
        return "LTS"
    return None


def standardized_mean_difference(
    group_a: Sequence[float],
    group_b: Sequence[float],
) -> float:
    """Return pooled-SD standardized mean difference."""

    if len(group_a) < 2 or len(group_b) < 2:
        raise ValueError("both groups need at least two observations")
    a = tuple(float(v) for v in group_a)
    b = tuple(float(v) for v in group_b)
    ma, mb = mean(a), mean(b)
    va = sum((v - ma) ** 2 for v in a) / (len(a) - 1)
    vb = sum((v - mb) ** 2 for v in b) / (len(b) - 1)
    pooled = sqrt(
        ((len(a) - 1) * va + (len(b) - 1) * vb)
        / (len(a) + len(b) - 2)
    )
    if pooled == 0:
        if ma == mb:
            return 0.0
        raise ValueError("standardized difference is undefined at zero pooled SD")
    return (ma - mb) / pooled


def sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + exp(-value))
    e = exp(value)
    return e / (1.0 + e)


def fit_logistic(
    x: Sequence[Sequence[float]],
    y: Sequence[int],
    *,
    l2: float = 0.2,
    steps: int = 2500,
    learning_rate: float = 0.08,
) -> tuple[float, ...]:
    """Fit a small deterministic L2-regularized logistic model.

    x must already include an intercept column when desired.
    """

    if len(x) != len(y) or not x:
        raise ValueError("x and y must be non-empty and aligned")
    width = len(x[0])
    if width == 0 or any(len(row) != width for row in x):
        raise ValueError("x must be rectangular")
    if any(value not in (0, 1) for value in y):
        raise ValueError("y must be binary")
    if l2 < 0 or steps <= 0 or learning_rate <= 0:
        raise ValueError("invalid optimization parameter")

    weights = [0.0] * width
    for _ in range(steps):
        gradient = [0.0] * width
        for row, target in zip(x, y, strict=True):
            score = sum(w * v for w, v in zip(weights, row, strict=True))
            error = sigmoid(score) - target
            for j, value in enumerate(row):
                gradient[j] += error * value

        for j in range(1, width):
            gradient[j] += l2 * weights[j]

        scale = learning_rate / len(x)
        for j in range(width):
            weights[j] -= scale * gradient[j]

    return tuple(weights)


def predict_logistic(
    x: Sequence[Sequence[float]],
    weights: Sequence[float],
) -> tuple[float, ...]:
    return tuple(
        sigmoid(sum(w * v for w, v in zip(weights, row, strict=True)))
        for row in x
    )


def binary_log_loss(y: Sequence[int], probabilities: Sequence[float]) -> float:
    if len(y) != len(probabilities) or not y:
        raise ValueError("y and probabilities must be non-empty and aligned")
    total = 0.0
    for target, probability in zip(y, probabilities, strict=True):
        q = min(1.0 - 1e-9, max(1e-9, float(probability)))
        total -= target * log(q) + (1 - target) * log(1 - q)
    return total / len(y)


def binary_auc(y: Sequence[int], scores: Sequence[float]) -> float:
    """Mann-Whitney AUC with exact tie averaging."""

    if len(y) != len(scores) or not y:
        raise ValueError("y and scores must be non-empty and aligned")
    pairs = sorted(zip(scores, y, strict=True), key=lambda pair: pair[0])
    n_pos = sum(y)
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        raise ValueError("AUC needs both classes")

    rank = 1
    positive_rank_sum = 0.0
    i = 0
    while i < len(pairs):
        j = i
        while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        average_rank = (rank + rank + (j - i)) / 2.0
        for k in range(i, j + 1):
            if pairs[k][1] == 1:
                positive_rank_sum += average_rank
        rank += j - i + 1
        i = j + 1

    return (
        positive_rank_sum - n_pos * (n_pos + 1) / 2.0
    ) / (n_pos * n_neg)


def risk_difference(
    group_a: Iterable[bool],
    group_b: Iterable[bool],
) -> float:
    a = tuple(bool(v) for v in group_a)
    b = tuple(bool(v) for v in group_b)
    if not a or not b:
        raise ValueError("both groups must be non-empty")
    return sum(a) / len(a) - sum(b) / len(b)
