"""Synthetic trajectory-divergence primitives for RQ-005.

The functions in this module operate on already-standardized group-difference
series. They are for known-answer method validation only. They do not infer
causality or prognosis in patients.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def _real_sequence(values: Sequence[float], name: str) -> tuple[float, ...]:
    out: list[float] = []
    for i, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name}[{i}] must be a real number")
        out.append(float(value))
    return tuple(out)


def first_persistent_divergence(
    values: Sequence[float],
    *,
    threshold: float = 0.5,
    persistence: int = 2,
) -> int | None:
    """Return first index with a persistent absolute standardized difference.

    A one-time spike does not qualify. Real studies must choose threshold and
    persistence before outcome inspection.
    """

    series = _real_sequence(values, "values")
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    if isinstance(persistence, bool) or not isinstance(persistence, int):
        raise TypeError("persistence must be an integer")
    if persistence <= 0:
        raise ValueError("persistence must be positive")

    for start in range(0, len(series) - persistence + 1):
        window = series[start : start + persistence]
        if all(abs(value) >= threshold for value in window):
            return start
    return None


def divergence_times(
    layer_effects: Mapping[str, Sequence[float]],
    *,
    threshold: float = 0.5,
    persistence: int = 2,
) -> dict[str, int | None]:
    """Measure the first persistent divergence time for each observed layer."""

    return {
        layer: first_persistent_divergence(
            values,
            threshold=threshold,
            persistence=persistence,
        )
        for layer, values in layer_effects.items()
    }


def divergence_order(
    layer_effects: Mapping[str, Sequence[float]],
    *,
    threshold: float = 0.5,
    persistence: int = 2,
) -> tuple[tuple[str, int], ...]:
    """Return observed divergence order; tied layers sort by name."""

    times = divergence_times(
        layer_effects,
        threshold=threshold,
        persistence=persistence,
    )
    observed = [(layer, time) for layer, time in times.items() if time is not None]
    return tuple(sorted(observed, key=lambda item: (item[1], item[0])))


def classify_precedence_pattern(
    layer_effects: Mapping[str, Sequence[float]],
    *,
    threshold: float = 0.5,
    persistence: int = 2,
) -> str:
    """Classify a synthetic known-answer precedence pattern.

    Required keys for meaningful classification are:
    tumor, immune, treatment, neuroendocrine, psychological.

    The labels are candidate causal patterns, never causal conclusions.
    """

    required = {
        "tumor",
        "immune",
        "treatment",
        "neuroendocrine",
        "psychological",
    }
    missing = required.difference(layer_effects)
    if missing:
        raise ValueError(f"missing required layers: {sorted(missing)}")

    times = divergence_times(
        layer_effects,
        threshold=threshold,
        persistence=persistence,
    )
    tumor = times["tumor"]
    immune = times["immune"]
    treatment = times["treatment"]
    psychological = times["psychological"]
    neuroendocrine = times["neuroendocrine"]

    if tumor is None:
        return "no_tumor_divergence"

    psych_neuro = [
        time
        for time in (psychological, neuroendocrine)
        if time is not None
    ]
    first_psych_neuro = min(psych_neuro) if psych_neuro else None

    if (
        treatment is not None
        and treatment < tumor
        and (first_psych_neuro is None or treatment < first_psych_neuro)
    ):
        return "treatment_first"

    if (
        first_psych_neuro is not None
        and immune is not None
        and first_psych_neuro < immune < tumor
    ):
        return "psych_neuroimmune_precedence_candidate"

    other_times = [
        time
        for time in (immune, treatment, psychological, neuroendocrine)
        if time is not None
    ]
    if tumor < min(other_times or [10**9]):
        return "tumor_first_reverse_causality_candidate"

    return "ambiguous"
