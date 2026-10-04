"""CGD-SIM-014: out-of-distribution world-model shift challenge.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean

from .cognitive_fixed_point import select_params
from .cognitive_temporal_frontier import (
    BASE_FEATURES,
    evaluate_precomputed,
    make_dataset,
    precompute,
    prepare_representation,
)

NONNEGATIVE = frozenset(BASE_FEATURES)


def _copy_dataset(dataset):
    return [(label, dict(features)) for label, features in dataset]


def common_mode_bias(dataset, *, seed: int):
    rng = Random(seed)
    shifted = _copy_dataset(dataset)
    for _, features in shifted:
        common = max(0.0, rng.gauss(0.035, 0.015))
        features["self_reference_gap"] += common
        features["observer_disagreement"] += 0.85 * common
        features["handoff_gap"] += 0.25 * common
    return shifted


def noise_inflation(dataset, *, seed: int, norm):
    rng = Random(seed)
    shifted = _copy_dataset(dataset)
    for _, features in shifted:
        for feature in BASE_FEATURES:
            sigma = 0.40 * norm[feature][1]
            features[feature] += rng.gauss(0.0, sigma)
            if feature in NONNEGATIVE:
                features[feature] = max(0.0, features[feature])
    return shifted


def probe_dropout(dataset, *, seed: int, train_means):
    rng = Random(seed)
    shifted = _copy_dataset(dataset)
    for _, features in shifted:
        if rng.random() < 0.50:
            features["observer_disagreement"] = train_means["observer_disagreement"]
            features["_missing_observer_disagreement"] = 1.0
        if rng.random() < 0.25:
            features["self_reference_gap"] = train_means["self_reference_gap"]
            features["_missing_self_reference_gap"] = 1.0
        if rng.random() < 0.15:
            features["handoff_gap"] = train_means["handoff_gap"]
            features["_missing_handoff_gap"] = 1.0
    return shifted


def combined_shift(dataset, *, seed: int, norm, train_means):
    biased = common_mode_bias(dataset, seed=seed)
    noisy = noise_inflation(biased, seed=seed + 1, norm=norm)
    return probe_dropout(
        noisy,
        seed=seed + 2,
        train_means=train_means,
    )


def train_means(dataset):
    return {
        feature: fmean(features[feature] for _, features in dataset)
        for feature in BASE_FEATURES
    }


def evaluate_dataset(dataset, prepared, params):
    templates, norm, train_vectors = prepared
    data = precompute(
        dataset,
        BASE_FEATURES,
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


def append_shift_calibration(clean_train, shifted_calibration):
    return list(clean_train) + list(shifted_calibration)


@lru_cache(maxsize=1)
def ood_challenge():
    train = make_dataset(160, 80_000_000)
    validation = make_dataset(50, 81_000_000)
    test = make_dataset(100, 82_000_000)

    templates, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates, norm, train_vectors)
    means = train_means(train)

    scenarios = {
        "clean": test,
        "common_mode_bias": common_mode_bias(test, seed=83_000_001),
        "noise_inflation": noise_inflation(
            test,
            seed=83_000_002,
            norm=norm,
        ),
        "probe_dropout": probe_dropout(
            test,
            seed=83_000_003,
            train_means=means,
        ),
        "combined_shift": combined_shift(
            test,
            seed=83_000_004,
            norm=norm,
            train_means=means,
        ),
    }

    results = {
        name: evaluate_dataset(dataset, prepared, params)
        for name, dataset in scenarios.items()
    }
    clean_accuracy = results["clean"]["ensemble_accuracy"]
    for name, result in results.items():
        result["accuracy_drop"] = clean_accuracy - result["ensemble_accuracy"]

    # Small shifted calibration set: new evidence from outside the old closed world.
    adaptation_clean = make_dataset(20, 84_000_000)
    adaptation_val_clean = make_dataset(15, 85_000_000)
    adaptation_test_clean = make_dataset(100, 86_000_000)

    shifted_adaptation = combined_shift(
        adaptation_clean,
        seed=87_000_001,
        norm=norm,
        train_means=means,
    )
    shifted_validation = combined_shift(
        adaptation_val_clean,
        seed=87_000_002,
        norm=norm,
        train_means=means,
    )
    shifted_test = combined_shift(
        adaptation_test_clean,
        seed=87_000_003,
        norm=norm,
        train_means=means,
    )

    adapted_train = append_shift_calibration(train, shifted_adaptation)
    adapted_templates, adapted_norm, adapted_vectors, adapted_params = select_params(
        adapted_train,
        shifted_validation,
        BASE_FEATURES,
    )
    adapted_prepared = (
        adapted_templates,
        adapted_norm,
        adapted_vectors,
    )
    frozen_combined = evaluate_dataset(
        shifted_test,
        prepared,
        params,
    )
    adapted_combined = evaluate_dataset(
        shifted_test,
        adapted_prepared,
        adapted_params,
    )

    worst_name = max(
        (name for name in results if name != "clean"),
        key=lambda name: results[name]["accuracy_drop"],
    )
    worst_drop = results[worst_name]["accuracy_drop"]
    adaptation_gain = (
        adapted_combined["ensemble_accuracy"]
        - frozen_combined["ensemble_accuracy"]
    )

    robust_fixed_point = worst_drop < 0.03
    external_evidence_has_value = adaptation_gain > 0.01

    return {
        "params": params,
        "results": results,
        "worst_shift": worst_name,
        "worst_drop": worst_drop,
        "frozen_combined": frozen_combined,
        "adapted_combined": adapted_combined,
        "adapted_params": adapted_params,
        "adaptation_gain": adaptation_gain,
        "robust_fixed_point": robust_fixed_point,
        "external_evidence_has_value": external_evidence_has_value,
    }


def format_markdown() -> str:
    result = ood_challenge()
    lines = [
        "# CGD-SIM-014 OOD world-model shift challenge",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| scenario | ensemble accuracy | drop vs clean | oracle union | disagreement |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name in (
        "clean",
        "common_mode_bias",
        "noise_inflation",
        "probe_dropout",
        "combined_shift",
    ):
        row = result["results"][name]
        lines.append(
            f"| {name} | {row['ensemble_accuracy']:.3f} | "
            f"{row['accuracy_drop']:+.4f} | "
            f"{row['oracle_union_accuracy']:.3f} | "
            f"{row['disagreement_rate']:.3f} |"
        )

    frozen = result["frozen_combined"]
    adapted = result["adapted_combined"]
    lines.extend(
        [
            "",
            f"- frozen clean-world params: k={result['params'][0]}, Bayes weight={result['params'][1]:.2f}",
            f"- worst shift: {result['worst_shift']}",
            f"- worst accuracy drop: {result['worst_drop']:+.4f}",
            f"- robust fixed point under declared OOD shifts: {result['robust_fixed_point']}",
            "",
            "## Small external-calibration test",
            "",
            f"- frozen model on fresh combined shift: {frozen['ensemble_accuracy']:.3f}",
            f"- adapted model on same fresh shift: {adapted['ensemble_accuracy']:.3f}",
            f"- adaptation gain: {result['adaptation_gain']:+.4f}",
            f"- adapted params: k={result['adapted_params'][0]}, Bayes weight={result['adapted_params'][1]:.2f}",
            f"- new shifted evidence has material value: {result['external_evidence_has_value']}",
            "",
            "Interpretation:",
            "",
            "SIM-013 established a local fixed point inside the original synthetic world. "
            "SIM-014 deliberately changes that world. If the fixed point breaks and a small "
            "amount of shifted calibration data restores accuracy, the correct next move is "
            "external evidence acquisition/adaptation rather than deeper internal recursion.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
