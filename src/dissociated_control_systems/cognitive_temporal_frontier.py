"""CGD-SIM-012: temporal evidence frontier.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache

from collections import Counter
from itertools import combinations
from math import exp, log, pi, sqrt
from statistics import fmean

from .cognitive_active_diagnosis import PROBES, hypotheses
from .cognitive_harness_repair import run_episode

BASE_FEATURES = tuple(PROBES)
TEMPORAL_FEATURES = BASE_FEATURES + (
    "reference_drop_early",
    "reference_drop_late",
    "reference_drop_acceleration",
    "self_reference_gap_trend",
    "handoff_gap_trend",
    "observer_disagreement_trend",
    "feedback_error_trend",
)
K_VALUES = (3, 5, 7, 11, 15)
WEIGHTS = tuple(step / 10.0 for step in range(11))


def make_dataset(
    samples: int,
    seed_base: int,
):
    rows = []
    for hypothesis_index, label in enumerate(hypotheses()):
        for sample in range(samples):
            episode = run_episode(
                label,
                seed_base + hypothesis_index * 100_000 + sample,
                steps=60,
            )
            rows.append((label, episode.features))
    return rows


def gaussian_templates(dataset, features):
    result = {}
    for label in hypotheses():
        rows = [
            feature_map
            for row_label, feature_map in dataset
            if row_label == label
        ]
        result[label] = {}
        for feature in features:
            values = [row[feature] for row in rows]
            mean = fmean(values)
            variance = fmean((value - mean) ** 2 for value in values) + 1e-6
            result[label][feature] = (mean, variance)
    return result


def bayes_posterior(feature_map, templates, features):
    hs = hypotheses()
    logp = {}
    prior = -log(len(hs))
    for label in hs:
        score = prior
        for feature in features:
            mean, variance = templates[label][feature]
            value = feature_map[feature]
            score += -0.5 * (
                ((value - mean) ** 2) / variance
                + log(2.0 * pi * variance)
            )
        logp[label] = score
    peak = max(logp.values())
    weights = {label: exp(value - peak) for label, value in logp.items()}
    total = sum(weights.values())
    return {label: value / total for label, value in weights.items()}


def normalization(dataset, features):
    result = {}
    for feature in features:
        values = [row[feature] for _, row in dataset]
        mean = fmean(values)
        variance = fmean((value - mean) ** 2 for value in values) + 1e-9
        result[feature] = (mean, sqrt(variance))
    return result


def vector(feature_map, features, norm):
    return tuple(
        (feature_map[feature] - norm[feature][0]) / norm[feature][1]
        for feature in features
    )


def prepare_representation(train_dataset, features):
    templates = gaussian_templates(train_dataset, features)
    norm = normalization(train_dataset, features)
    train_vectors = [
        (label, vector(feature_map, features, norm))
        for label, feature_map in train_dataset
    ]
    return templates, norm, train_vectors


def precompute(dataset, features, templates, norm, train_vectors):
    result = []
    max_k = max(K_VALUES)
    hs = hypotheses()
    for true_label, feature_map in dataset:
        point = vector(feature_map, features, norm)
        distances = [
            (
                sum(
                    (left - right) ** 2
                    for left, right in zip(point, candidate)
                ),
                label,
            )
            for label, candidate in train_vectors
        ]
        nearest = [
            label
            for _, label in sorted(distances, key=lambda item: item[0])[:max_k]
        ]
        knn_by_k = {}
        for k in K_VALUES:
            counts = Counter(nearest[:k])
            smoothing = 0.05
            denominator = k + smoothing * len(hs)
            knn_by_k[k] = {
                label: (counts.get(label, 0) + smoothing) / denominator
                for label in hs
            }
        result.append(
            (
                true_label,
                bayes_posterior(feature_map, templates, features),
                knn_by_k,
            )
        )
    return result


def evaluate_precomputed(data, *, k, bayes_weight):
    bayes_correct = 0
    knn_correct = 0
    ensemble_correct = 0
    oracle_correct = 0
    disagreements = 0

    for true_label, bp, knn_by_k in data:
        kp = knn_by_k[k]
        ep = {
            label: (
                bayes_weight * bp[label]
                + (1.0 - bayes_weight) * kp[label]
            )
            for label in bp
        }
        b = max(bp, key=bp.get)
        n = max(kp, key=kp.get)
        e = max(ep, key=ep.get)
        b_ok = b == true_label
        n_ok = n == true_label
        bayes_correct += int(b_ok)
        knn_correct += int(n_ok)
        ensemble_correct += int(e == true_label)
        oracle_correct += int(b_ok or n_ok)
        disagreements += int(b != n)

    total = len(data)
    return {
        "bayes_accuracy": bayes_correct / total,
        "knn_accuracy": knn_correct / total,
        "ensemble_accuracy": ensemble_correct / total,
        "oracle_union_accuracy": oracle_correct / total,
        "disagreement_rate": disagreements / total,
    }


def optimize_representation(train, validation, test, features):
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

    heldout = precompute(test, features, templates, norm, train_vectors)
    result = evaluate_precomputed(
        heldout,
        k=best_params[0],
        bayes_weight=best_params[1],
    )
    result["k"] = best_params[0]
    result["bayes_weight"] = best_params[1]
    result["residual_oracle_gap"] = (
        result["oracle_union_accuracy"] - result["ensemble_accuracy"]
    )
    return result


@lru_cache(maxsize=1)
def temporal_frontier():
    train = make_dataset(160, 60_000_000)
    validation = make_dataset(50, 61_000_000)
    test = make_dataset(120, 62_000_000)

    base = optimize_representation(
        train,
        validation,
        test,
        BASE_FEATURES,
    )
    temporal = optimize_representation(
        train,
        validation,
        test,
        TEMPORAL_FEATURES,
    )
    gain = temporal["ensemble_accuracy"] - base["ensemble_accuracy"]
    representation_stable = (
        gain < 0.005
        and temporal["residual_oracle_gap"] < 0.010
    )
    return {
        "base": base,
        "temporal": temporal,
        "temporal_gain": gain,
        "representation_stable": representation_stable,
    }


def format_markdown() -> str:
    result = temporal_frontier()
    lines = [
        "# CGD-SIM-012 temporal evidence frontier",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| representation | Bayes | kNN | ensemble | oracle union | residual oracle gap | disagreement |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in ("base", "temporal"):
        row = result[name]
        lines.append(
            f"| {name} | {row['bayes_accuracy']:.3f} | "
            f"{row['knn_accuracy']:.3f} | {row['ensemble_accuracy']:.3f} | "
            f"{row['oracle_union_accuracy']:.3f} | "
            f"{row['residual_oracle_gap']:.4f} | "
            f"{row['disagreement_rate']:.3f} |"
        )
    temporal = result["temporal"]
    lines.extend(
        [
            "",
            f"- temporal ensemble gain over same-family base representation: {result['temporal_gain']:+.4f}",
            f"- temporal selected k: {temporal['k']}",
            f"- temporal selected Bayes weight: {temporal['bayes_weight']:.2f}",
            f"- temporal representation stable: {result['representation_stable']}",
            "",
            "Added trajectory evidence:",
            "",
            "- early and late independent-reference decline;",
            "- decline acceleration;",
            "- self/reference-gap trend;",
            "- handoff-gap trend;",
            "- observer-disagreement trend;",
            "- feedback-error trend.",
            "",
            "If temporal evidence materially improves the frontier, the prior residual "
            "was an observation/representation problem rather than a missing meta layer.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
