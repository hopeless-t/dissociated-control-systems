"""CGD-SIM-020: missingness-aware shifted-regime classifier.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from math import exp, log, pi, sqrt
from statistics import fmean

from .cognitive_active_diagnosis import hypotheses
from .cognitive_ood_challenge import combined_shift, train_means
from .cognitive_restoration import (
    CALIBRATION_SIZES,
    RESTORE_VALIDATION_ACCURACY,
)
from .cognitive_temporal_frontier import BASE_FEATURES, K_VALUES, WEIGHTS, make_dataset

MISSING_FOR = {
    "self_reference_gap": "_missing_self_reference_gap",
    "handoff_gap": "_missing_handoff_gap",
    "observer_disagreement": "_missing_observer_disagreement",
}


def is_observed(features, feature):
    marker = MISSING_FOR.get(feature)
    return marker is None or features.get(marker, 0.0) <= 0.5


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


def observed_norm(dataset):
    norm = {}
    for feature in BASE_FEATURES:
        values = [
            features[feature]
            for _, features in dataset
            if is_observed(features, feature)
        ]
        if len(values) < 2:
            norm[feature] = (0.0, 1.0)
            continue
        mean = fmean(values)
        variance = fmean((value - mean) ** 2 for value in values) + 1e-9
        norm[feature] = (mean, sqrt(variance))
    return norm


def masked_templates(dataset):
    templates = {}
    for label in hypotheses():
        label_rows = [
            features
            for row_label, features in dataset
            if row_label == label
        ]
        templates[label] = {}
        for feature in BASE_FEATURES:
            values = [
                features[feature]
                for features in label_rows
                if is_observed(features, feature)
            ]
            if len(values) < 2:
                templates[label][feature] = (0.0, 1e6)
                continue
            mean = fmean(values)
            variance = fmean((value - mean) ** 2 for value in values) + 1e-6
            templates[label][feature] = (mean, variance)
    return templates


def masked_bayes(features, templates):
    logp = {}
    labels = hypotheses()
    prior = -log(len(labels))
    for label in labels:
        score = prior
        used = 0
        for feature in BASE_FEATURES:
            if not is_observed(features, feature):
                continue
            mean, variance = templates[label][feature]
            value = features[feature]
            score += -0.5 * (
                ((value - mean) ** 2) / variance
                + log(2.0 * pi * variance)
            )
            used += 1
        if used == 0:
            score = prior
        logp[label] = score

    peak = max(logp.values())
    weights = {label: exp(value - peak) for label, value in logp.items()}
    total = sum(weights.values())
    return {label: value / total for label, value in weights.items()}


def masked_distance(left, right, norm):
    terms = []
    for feature in BASE_FEATURES:
        if not is_observed(left, feature) or not is_observed(right, feature):
            continue
        scale = norm[feature][1]
        terms.append(((left[feature] - right[feature]) / scale) ** 2)
    if not terms:
        return float("inf")
    return fmean(terms)


def masked_knn(features, train, norm, *, k):
    distances = [
        (masked_distance(features, train_features, norm), label)
        for label, train_features in train
    ]
    nearest = [
        label
        for distance, label in sorted(distances, key=lambda item: item[0])
        if distance != float("inf")
    ][:k]

    labels = hypotheses()
    smoothing = 0.05
    if not nearest:
        return {label: 1.0 / len(labels) for label in labels}

    counts = Counter(nearest)
    denominator = len(nearest) + smoothing * len(labels)
    return {
        label: (counts.get(label, 0) + smoothing) / denominator
        for label in labels
    }


def evaluate(dataset, train, templates, norm, *, k, bayes_weight):
    correct = 0
    oracle_correct = 0
    bayes_correct = 0
    knn_correct = 0
    confidence = []

    for true_label, features in dataset:
        bp = masked_bayes(features, templates)
        kp = masked_knn(features, train, norm, k=k)
        ep = {
            label: bayes_weight * bp[label] + (1.0 - bayes_weight) * kp[label]
            for label in bp
        }
        b = max(bp, key=bp.get)
        n = max(kp, key=kp.get)
        e = max(ep, key=ep.get)

        b_ok = b == true_label
        n_ok = n == true_label
        bayes_correct += int(b_ok)
        knn_correct += int(n_ok)
        correct += int(e == true_label)
        oracle_correct += int(b_ok or n_ok)
        confidence.append(ep[e])

    total = len(dataset)
    return {
        "accuracy": correct / total,
        "bayes_accuracy": bayes_correct / total,
        "knn_accuracy": knn_correct / total,
        "oracle_union_accuracy": oracle_correct / total,
        "mean_confidence": fmean(confidence),
    }


def fit_select(train, validation):
    templates = masked_templates(train)
    norm = observed_norm(train)
    best = None
    best_params = (7, 0.5)
    for k in K_VALUES:
        for weight in WEIGHTS:
            result = evaluate(
                validation,
                train,
                templates,
                norm,
                k=k,
                bayes_weight=weight,
            )
            if best is None or result["accuracy"] > best["accuracy"]:
                best = result
                best_params = (k, weight)
    return templates, norm, best_params, best


@lru_cache(maxsize=1)
def missingness_aware_restoration():
    clean_train = make_dataset(160, 400_000_000)
    clean_validation = make_dataset(50, 401_000_000)

    # Clean scale exists only to define the synthetic shift generator.
    from .cognitive_fixed_point import select_params

    _, clean_norm, _, _ = select_params(
        clean_train,
        clean_validation,
        BASE_FEATURES,
    )
    clean_means = train_means(clean_train)

    shifted_validation = shifted_dataset(
        samples=50,
        clean_seed=402_000_000,
        shift_seed=403_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )
    shifted_test = shifted_dataset(
        samples=100,
        clean_seed=404_000_000,
        shift_seed=405_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )

    rows = []
    for index, size in enumerate(CALIBRATION_SIZES):
        shifted_train = shifted_dataset(
            samples=size,
            clean_seed=410_000_000 + index * 2_000_000,
            shift_seed=411_000_000 + index * 2_000_000,
            clean_norm=clean_norm,
            clean_means=clean_means,
        )
        templates, norm, params, validation_result = fit_select(
            shifted_train,
            shifted_validation,
        )
        test_result = evaluate(
            shifted_test,
            shifted_train,
            templates,
            norm,
            k=params[0],
            bayes_weight=params[1],
        )
        authorized = validation_result["accuracy"] >= RESTORE_VALIDATION_ACCURACY
        rows.append(
            {
                "samples_per_hypothesis": size,
                "total_calibration_samples": size * 16,
                "validation_accuracy": validation_result["accuracy"],
                "test_accuracy": test_result["accuracy"],
                "test_bayes_accuracy": test_result["bayes_accuracy"],
                "test_knn_accuracy": test_result["knn_accuracy"],
                "test_oracle_union": test_result["oracle_union_accuracy"],
                "test_confidence": test_result["mean_confidence"],
                "k": params[0],
                "bayes_weight": params[1],
                "restore_authorized": authorized,
                "safe_on_test": test_result["accuracy"] >= RESTORE_VALIDATION_ACCURACY,
            }
        )

    authorized_rows = [row for row in rows if row["restore_authorized"]]
    first_authorized = authorized_rows[0] if authorized_rows else None
    false_restore = any(
        row["restore_authorized"] and not row["safe_on_test"]
        for row in rows
    )

    return {
        "restore_threshold": RESTORE_VALIDATION_ACCURACY,
        "rows": rows,
        "first_authorized": first_authorized,
        "false_restore": false_restore,
    }


def format_markdown() -> str:
    result = missingness_aware_restoration()
    lines = [
        "# CGD-SIM-020 missingness-aware restoration",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- authority restoration validation threshold: {result['restore_threshold']:.2f}",
        "",
        "| calibration / hypothesis | validation | held-out test | Bayes | kNN | oracle union | confidence | k | Bayes weight | restore |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['samples_per_hypothesis']} | "
            f"{row['validation_accuracy']:.3f} | "
            f"{row['test_accuracy']:.3f} | "
            f"{row['test_bayes_accuracy']:.3f} | "
            f"{row['test_knn_accuracy']:.3f} | "
            f"{row['test_oracle_union']:.3f} | "
            f"{row['test_confidence']:.3f} | "
            f"{row['k']} | {row['bayes_weight']:.2f} | "
            f"{row['restore_authorized']} |"
        )

    first = result["first_authorized"]
    restoration = (
        "none"
        if first is None
        else f"{first['samples_per_hypothesis']} samples/hypothesis"
    )
    lines.extend(
        [
            "",
            f"- first validation-authorized restoration point: {restoration}",
            f"- any false restoration on held-out test: {result['false_restore']}",
            "",
            "Representation repair:",
            "",
            "~~~text",
            "missing probe",
            "  != clean-mean observation",
            "",
            "Bayes: omit missing probe from likelihood",
            "kNN: omit probe unless observed on both sides",
            "~~~",
            "",
            "If this improves the restoration curve, SIM-019 failed because the "
            "classifier violated the missingness invariant rather than because shifted "
            "evidence itself was useless.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
