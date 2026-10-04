"""CGD-SIM-049: context reliability authority gate.

Synthetic evidence-routing experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random

PILOT_SAMPLES = 20_000
HELDOUT_SAMPLES = 40_000
SIGMA_STATE_ERROR = 0.04
ENVIRONMENT_EVENT_PROBABILITY = 0.10
ENVIRONMENT_SHIFT = 0.12
SIGMA_FUNCTION = 0.02
CONTEXT_NOISE_LEVELS = (0.0, 0.01, 0.02, 0.04, 0.06, 0.08, 0.12)
TARGET_QUANTILE = 0.90
NORMALIZATION_AUTHORITY_MARGIN = 0.01
MAX_HELDOUT_SELECTION_REGRET = 0.02


def _auc(scores: list[float], labels: list[int]) -> float:
    """Mann-Whitney AUC with average ranks for exact score ties."""

    pairs = sorted(zip(scores, labels, strict=True), key=lambda pair: pair[0])
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        raise ValueError("AUC requires both positive and negative labels")

    rank_sum = 0.0
    index = 0
    rank = 1
    while index < len(pairs):
        stop = index + 1
        while stop < len(pairs) and pairs[stop][0] == pairs[index][0]:
            stop += 1
        width = stop - index
        average_rank = (rank + rank + width - 1) / 2.0
        rank_sum += average_rank * sum(label for _, label in pairs[index:stop])
        rank += width
        index = stop

    return (
        rank_sum - positives * (positives + 1) / 2.0
    ) / (positives * negatives)


def _sample_auc(sample_count: int, seed: int, sigma_context: float):
    rng = Random(seed)
    absolute_errors = []
    raw_scores = []
    normalized_scores = []

    for _ in range(sample_count):
        state_error = rng.gauss(0.0, SIGMA_STATE_ERROR)
        environment = 0.0
        if rng.random() < ENVIRONMENT_EVENT_PROBABILITY:
            environment = ENVIRONMENT_SHIFT * (
                1.0 if rng.random() < 0.5 else -1.0
            )

        function_noise = rng.gauss(0.0, SIGMA_FUNCTION)
        context_noise = rng.gauss(0.0, sigma_context)

        absolute_errors.append(abs(state_error))
        raw_scores.append(abs(environment + function_noise - state_error))
        normalized_scores.append(abs(function_noise - context_noise - state_error))

    cutoff = sorted(absolute_errors)[int(TARGET_QUANTILE * sample_count)]
    labels = [int(value >= cutoff) for value in absolute_errors]
    return {
        "target_cutoff": cutoff,
        "raw_auc": _auc(raw_scores, labels),
        "normalized_auc": _auc(normalized_scores, labels),
    }


def _select_authority(pilot_metrics):
    if (
        pilot_metrics["normalized_auc"]
        >= pilot_metrics["raw_auc"] + NORMALIZATION_AUTHORITY_MARGIN
    ):
        return "context_normalized"
    return "raw_function"


@lru_cache(maxsize=1)
def context_authority_gate_experiment():
    levels = []
    for level_index, sigma_context in enumerate(CONTEXT_NOISE_LEVELS):
        pilot = _sample_auc(
            PILOT_SAMPLES,
            5_000_000_000 + level_index * 100_000,
            sigma_context,
        )
        selected_policy = _select_authority(pilot)
        heldout = _sample_auc(
            HELDOUT_SAMPLES,
            5_100_000_000 + level_index * 100_000,
            sigma_context,
        )
        selected_auc = (
            heldout["normalized_auc"]
            if selected_policy == "context_normalized"
            else heldout["raw_auc"]
        )
        best_auc = max(heldout["raw_auc"], heldout["normalized_auc"])

        levels.append(
            {
                "sigma_context": sigma_context,
                "pilot_raw_auc": pilot["raw_auc"],
                "pilot_normalized_auc": pilot["normalized_auc"],
                "selected_policy": selected_policy,
                "normalization_authorized": selected_policy == "context_normalized",
                "heldout_raw_auc": heldout["raw_auc"],
                "heldout_normalized_auc": heldout["normalized_auc"],
                "selected_auc": selected_auc,
                "best_auc": best_auc,
                "selection_regret": best_auc - selected_auc,
            }
        )

    first_raw_fallback = next(
        level["sigma_context"]
        for level in levels
        if not level["normalization_authorized"]
    )
    first_normalized_auc_below_070 = next(
        level["sigma_context"]
        for level in levels
        if level["heldout_normalized_auc"] < 0.70
    )

    return {
        "levels": levels,
        "first_raw_fallback_sigma": first_raw_fallback,
        "first_normalized_auc_below_070_sigma": first_normalized_auc_below_070,
        "max_selection_regret": max(level["selection_regret"] for level in levels),
    }


def format_markdown() -> str:
    result = context_authority_gate_experiment()
    lines = [
        "# CGD-SIM-049 context reliability authority gate",
        "",
        "> Synthetic evidence-routing experiment only. Clinical authority: NONE.",
        "",
        f"- pilot samples / level: {PILOT_SAMPLES}",
        f"- held-out samples / level: {HELDOUT_SAMPLES}",
        f"- environment event probability: {ENVIRONMENT_EVENT_PROBABILITY:.1%}",
        f"- environment shift magnitude: +/- {ENVIRONMENT_SHIFT:.2f}",
        f"- functional noise std: {SIGMA_FUNCTION:.2f}",
        f"- normalization authority margin: +{NORMALIZATION_AUTHORITY_MARGIN:.2f} pilot AUC",
        "- target: top 10% absolute propagated state-estimation error",
        "",
        "Authority rule:",
        "",
        "~~~text",
        "authorize context normalization",
        "    only if pilot AUC_normalized >= pilot AUC_raw + 0.01",
        "otherwise",
        "    fail back to raw functional innovation",
        "~~~",
        "",
        "| context noise std | pilot raw AUC | pilot normalized AUC | selected policy | held-out raw AUC | held-out normalized AUC | selected AUC | regret |",
        "| ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
    ]

    for level in result["levels"]:
        lines.append(
            f"| {level['sigma_context']:.2f} | "
            f"{level['pilot_raw_auc']:.3f} | "
            f"{level['pilot_normalized_auc']:.3f} | "
            f"{level['selected_policy']} | "
            f"{level['heldout_raw_auc']:.3f} | "
            f"{level['heldout_normalized_auc']:.3f} | "
            f"{level['selected_auc']:.3f} | "
            f"{level['selection_regret']:.3f} |"
        )

    lines.extend(
        [
            "",
            (
                "- first frozen context-noise level where normalization authority "
                f"is denied: {result['first_raw_fallback_sigma']:.2f}"
            ),
            (
                "- first frozen context-noise level where held-out normalized AUC "
                f"falls below 0.70: {result['first_normalized_auc_below_070_sigma']:.2f}"
            ),
            f"- maximum held-out selection regret: {result['max_selection_regret']:.3f}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Context Observation != Environment State",
            "Context Binding != Context Authority",
            "Normalization Requires Incremental Reliability Evidence",
            "Failed Qualification -> Fail Back, Not Blind Correction",
            "~~~",
            "",
            "All noise levels, event rates, shifts and AUC gates are synthetic scenario",
            "parameters. This experiment qualifies an evidence-routing structure, not",
            "a real cognitive, clinical, caregiver, sensor or home-monitoring system.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
