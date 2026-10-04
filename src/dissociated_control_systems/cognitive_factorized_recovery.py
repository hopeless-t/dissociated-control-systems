"""CGD-SIM-021: factorized partial-state recovery.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import exp, log, pi
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES
from .cognitive_fixed_point import select_params
from .cognitive_missingness_aware import (
    evaluate_precomputed,
    fit_select,
    is_observed,
    precompute,
)
from .cognitive_ood_challenge import combined_shift, train_means
from .cognitive_restoration import RESTORE_VALIDATION_ACCURACY
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset

THRESHOLDS = tuple(step / 20.0 for step in range(2, 19))


def shifted_dataset(
    *,
    samples,
    clean_seed,
    shift_seed,
    clean_norm,
    clean_means,
):
    return combined_shift(
        make_dataset(samples, clean_seed),
        seed=shift_seed,
        norm=clean_norm,
        train_means=clean_means,
    )


def binary_templates(dataset, fault):
    result = {}
    for present in (False, True):
        rows = [
            features
            for label, features in dataset
            if (fault in label) == present
        ]
        result[present] = {}
        for feature in BASE_FEATURES:
            values = [
                features[feature]
                for features in rows
                if is_observed(features, feature)
            ]
            if len(values) < 2:
                result[present][feature] = (0.0, 1e6)
                continue
            mean = fmean(values)
            variance = fmean((value - mean) ** 2 for value in values) + 1e-6
            result[present][feature] = (mean, variance)
    return result


def binary_probability(features, templates):
    logp = {}
    for present in (False, True):
        score = log(0.5)
        for feature in BASE_FEATURES:
            if not is_observed(features, feature):
                continue
            mean, variance = templates[present][feature]
            value = features[feature]
            score += -0.5 * (
                ((value - mean) ** 2) / variance
                + log(2.0 * pi * variance)
            )
        logp[present] = score

    peak = max(logp.values())
    absent_weight = exp(logp[False] - peak)
    present_weight = exp(logp[True] - peak)
    return present_weight / (absent_weight + present_weight)


def binary_metrics(dataset, fault, templates, threshold):
    correct = 0
    tp = tn = fp = fn = 0
    probabilities = []

    for label, features in dataset:
        truth = fault in label
        probability = binary_probability(features, templates)
        prediction = probability >= threshold
        correct += int(prediction == truth)
        tp += int(prediction and truth)
        tn += int((not prediction) and (not truth))
        fp += int(prediction and (not truth))
        fn += int((not prediction) and truth)
        probabilities.append(probability)

    sensitivity = tp / (tp + fn) if tp + fn else 1.0
    specificity = tn / (tn + fp) if tn + fp else 1.0
    return {
        "accuracy": correct / len(dataset),
        "sensitivity": sensitivity,
        "specificity": specificity,
        "mean_probability": fmean(probabilities),
    }


def select_threshold(validation, fault, templates):
    best = None
    best_threshold = 0.5
    for threshold in THRESHOLDS:
        metrics = binary_metrics(
            validation,
            fault,
            templates,
            threshold,
        )
        score = min(metrics["sensitivity"], metrics["specificity"])
        key = (score, metrics["accuracy"], -abs(threshold - 0.5))
        if best is None or key > best[0]:
            best = (key, metrics)
            best_threshold = threshold
    assert best is not None
    return best_threshold, best[1]


def reconstruct_exact(dataset, models):
    correct = 0
    for truth, features in dataset:
        predicted = frozenset(
            fault
            for fault, model in models.items()
            if binary_probability(features, model["templates"]) >= model["threshold"]
        )
        correct += int(predicted == truth)
    return correct / len(dataset)


@lru_cache(maxsize=1)
def factorized_experiment():
    clean_train = make_dataset(160, 500_000_000)
    clean_validation = make_dataset(50, 501_000_000)
    _, clean_norm, _, _ = select_params(
        clean_train,
        clean_validation,
        BASE_FEATURES,
    )
    clean_means = train_means(clean_train)

    shifted_train = shifted_dataset(
        samples=160,
        clean_seed=502_000_000,
        shift_seed=503_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )
    shifted_validation = shifted_dataset(
        samples=60,
        clean_seed=504_000_000,
        shift_seed=505_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )
    shifted_test = shifted_dataset(
        samples=120,
        clean_seed=506_000_000,
        shift_seed=507_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )

    # Same shifted evidence, previous full-state strategy.
    full_templates, full_norm, full_params, full_validation = fit_select(
        shifted_train,
        shifted_validation,
    )
    full_test_precomputed = precompute(
        shifted_test,
        shifted_train,
        full_templates,
        full_norm,
    )
    full_test = evaluate_precomputed(
        full_test_precomputed,
        k=full_params[0],
        bayes_weight=full_params[1],
    )

    models = {}
    rows = []
    for fault in FAULT_NAMES:
        templates = binary_templates(shifted_train, fault)
        threshold, validation = select_threshold(
            shifted_validation,
            fault,
            templates,
        )
        test = binary_metrics(
            shifted_test,
            fault,
            templates,
            threshold,
        )
        restorable = validation["accuracy"] >= RESTORE_VALIDATION_ACCURACY
        rows.append(
            {
                "fault": fault,
                "threshold": threshold,
                "validation_accuracy": validation["accuracy"],
                "validation_sensitivity": validation["sensitivity"],
                "validation_specificity": validation["specificity"],
                "test_accuracy": test["accuracy"],
                "test_sensitivity": test["sensitivity"],
                "test_specificity": test["specificity"],
                "restorable": restorable,
                "safe_on_test": test["accuracy"] >= RESTORE_VALIDATION_ACCURACY,
            }
        )
        models[fault] = {
            "templates": templates,
            "threshold": threshold,
        }

    exact_reconstruction = reconstruct_exact(shifted_test, models)
    macro_test_accuracy = fmean(row["test_accuracy"] for row in rows)
    restorable_faults = [
        row["fault"]
        for row in rows
        if row["restorable"]
    ]
    false_restore = any(
        row["restorable"] and not row["safe_on_test"]
        for row in rows
    )

    return {
        "full_validation_accuracy": full_validation["accuracy"],
        "full_test_accuracy": full_test["accuracy"],
        "factorized_exact_reconstruction": exact_reconstruction,
        "macro_test_accuracy": macro_test_accuracy,
        "rows": rows,
        "restorable_faults": restorable_faults,
        "false_restore": false_restore,
    }


def format_markdown() -> str:
    result = factorized_experiment()
    lines = [
        "# CGD-SIM-021 factorized partial-state recovery",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- previous full-state validation accuracy: {result['full_validation_accuracy']:.3f}",
        f"- previous full-state held-out accuracy: {result['full_test_accuracy']:.3f}",
        f"- factorized exact reconstruction accuracy: {result['factorized_exact_reconstruction']:.3f}",
        f"- factorized macro per-fault accuracy: {result['macro_test_accuracy']:.3f}",
        "",
        "| fault dimension | threshold | validation accuracy | val sens | val spec | test accuracy | test sens | test spec | partial authority eligible |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['fault']} | {row['threshold']:.2f} | "
            f"{row['validation_accuracy']:.3f} | "
            f"{row['validation_sensitivity']:.3f} | "
            f"{row['validation_specificity']:.3f} | "
            f"{row['test_accuracy']:.3f} | "
            f"{row['test_sensitivity']:.3f} | "
            f"{row['test_specificity']:.3f} | "
            f"{row['restorable']} |"
        )

    eligible = ", ".join(result["restorable_faults"]) or "none"
    lines.extend(
        [
            "",
            f"- validation-eligible fault dimensions: {eligible}",
            f"- any false partial restoration on held-out test: {result['false_restore']}",
            "",
            "New decomposition:",
            "",
            "~~~text",
            "Full-State Recovery",
            "    != Useful Partial-State Recovery",
            "",
            "If exact 16-state reconstruction is unavailable,",
            "authority may be restored only for independently validated dimensions.",
            "~~~",
            "",
            "The 0.90 threshold is unchanged. A dimension that does not pass remains "
            "fail-closed even if other dimensions are usable.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
