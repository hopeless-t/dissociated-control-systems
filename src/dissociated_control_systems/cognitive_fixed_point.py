"""CGD-SIM-013: replicated local fixed-point audit.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache

from statistics import fmean

from .cognitive_temporal_frontier import (
    BASE_FEATURES,
    K_VALUES,
    TEMPORAL_FEATURES,
    WEIGHTS,
    evaluate_precomputed,
    make_dataset,
    precompute,
    prepare_representation,
)


def select_params(train, validation, features):
    templates, norm, train_vectors = prepare_representation(train, features)
    val = precompute(validation, features, templates, norm, train_vectors)
    best_accuracy = -1.0
    best_params = (7, 0.5)
    for k in K_VALUES:
        for weight in WEIGHTS:
            result = evaluate_precomputed(
                val,
                k=k,
                bayes_weight=weight,
            )
            if result["ensemble_accuracy"] > best_accuracy:
                best_accuracy = result["ensemble_accuracy"]
                best_params = (k, weight)
    return templates, norm, train_vectors, best_params


def evaluate_block(
    dataset,
    features,
    prepared,
    params,
):
    templates, norm, train_vectors = prepared
    data = precompute(
        dataset,
        features,
        templates,
        norm,
        train_vectors,
    )
    result = evaluate_precomputed(
        data,
        k=params[0],
        bayes_weight=params[1],
    )
    result["residual_oracle_gap"] = (
        result["oracle_union_accuracy"] - result["ensemble_accuracy"]
    )
    return result


@lru_cache(maxsize=None)
def replicated_audit(
    *,
    blocks: int = 5,
    samples_per_hypothesis: int = 60,
):
    train = make_dataset(160, 70_000_000)
    validation = make_dataset(50, 71_000_000)

    base_templates, base_norm, base_vectors, base_params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    temporal_templates, temporal_norm, temporal_vectors, temporal_params = select_params(
        train,
        validation,
        TEMPORAL_FEATURES,
    )

    base_prepared = (base_templates, base_norm, base_vectors)
    temporal_prepared = (
        temporal_templates,
        temporal_norm,
        temporal_vectors,
    )

    rows = []
    for block in range(blocks):
        test = make_dataset(
            samples_per_hypothesis,
            72_000_000 + block * 2_000_000,
        )
        base = evaluate_block(
            test,
            BASE_FEATURES,
            base_prepared,
            base_params,
        )
        temporal = evaluate_block(
            test,
            TEMPORAL_FEATURES,
            temporal_prepared,
            temporal_params,
        )
        rows.append(
            {
                "block": block,
                "base_accuracy": base["ensemble_accuracy"],
                "base_oracle_gap": base["residual_oracle_gap"],
                "base_disagreement": base["disagreement_rate"],
                "temporal_accuracy": temporal["ensemble_accuracy"],
                "temporal_oracle_gap": temporal["residual_oracle_gap"],
                "temporal_gain": (
                    temporal["ensemble_accuracy"] - base["ensemble_accuracy"]
                ),
            }
        )

    mean_base_accuracy = fmean(row["base_accuracy"] for row in rows)
    mean_base_gap = fmean(row["base_oracle_gap"] for row in rows)
    max_base_gap = max(row["base_oracle_gap"] for row in rows)
    mean_temporal_gain = fmean(row["temporal_gain"] for row in rows)
    positive_temporal_blocks = sum(
        row["temporal_gain"] > 0.005
        for row in rows
    )

    converged = (
        mean_base_gap < 0.010
        and max_base_gap < 0.015
        and mean_temporal_gain < 0.005
        and positive_temporal_blocks <= 1
    )

    return {
        "rows": rows,
        "base_params": base_params,
        "temporal_params": temporal_params,
        "mean_base_accuracy": mean_base_accuracy,
        "mean_base_oracle_gap": mean_base_gap,
        "max_base_oracle_gap": max_base_gap,
        "mean_temporal_gain": mean_temporal_gain,
        "positive_temporal_blocks": positive_temporal_blocks,
        "converged": converged,
    }


def format_markdown() -> str:
    result = replicated_audit()
    lines = [
        "# CGD-SIM-013 replicated local fixed-point audit",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| block | base accuracy | base oracle gap | temporal accuracy | temporal gain | temporal oracle gap |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['block']} | {row['base_accuracy']:.3f} | "
            f"{row['base_oracle_gap']:.4f} | "
            f"{row['temporal_accuracy']:.3f} | "
            f"{row['temporal_gain']:+.4f} | "
            f"{row['temporal_oracle_gap']:.4f} |"
        )

    lines.extend(
        [
            "",
            f"- frozen base params: k={result['base_params'][0]}, Bayes weight={result['base_params'][1]:.2f}",
            f"- frozen temporal params: k={result['temporal_params'][0]}, Bayes weight={result['temporal_params'][1]:.2f}",
            f"- mean base accuracy: {result['mean_base_accuracy']:.3f}",
            f"- mean base residual oracle gap: {result['mean_base_oracle_gap']:.4f}",
            f"- max base residual oracle gap: {result['max_base_oracle_gap']:.4f}",
            f"- mean temporal gain: {result['mean_temporal_gain']:+.4f}",
            f"- blocks with temporal gain > 0.005: {result['positive_temporal_blocks']}",
            f"- declared synthetic local fixed point reached: {result['converged']}",
            "",
            "Fixed-point criterion:",
            "",
            "1. mean residual oracle gap < 0.010;",
            "2. worst-block residual oracle gap < 0.015;",
            "3. a genuinely richer temporal representation adds < 0.005 mean accuracy;",
            "4. temporal gain > 0.005 occurs in at most one independent block.",
            "",
            "If TRUE, further recursion in the current synthetic family is no longer "
            "the productive axis. The next scientific advance requires a changed "
            "world model, new independent evidence, or external validation.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
