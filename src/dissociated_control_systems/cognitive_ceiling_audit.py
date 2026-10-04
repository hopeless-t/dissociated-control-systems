"""CGD-SIM-009: classifier ceiling audit.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from collections import Counter
from math import sqrt
from statistics import fmean

from .cognitive_active_diagnosis import (
    PROBES,
    diagnose_all_probes,
    hypotheses,
    train_templates,
)
from .cognitive_harness_repair import run_episode

FEATURE_ORDER = tuple(PROBES)


def make_dataset(
    samples: int,
    seed_base: int,
) -> list[tuple[frozenset[str], dict[str, float]]]:
    data: list[tuple[frozenset[str], dict[str, float]]] = []
    for hypothesis_index, true_faults in enumerate(hypotheses()):
        for sample in range(samples):
            data.append(
                (
                    true_faults,
                    run_episode(
                        true_faults,
                        seed_base + hypothesis_index * 100_000 + sample,
                        steps=60,
                    ).features,
                )
            )
    return data


def normalization(
    dataset: list[tuple[frozenset[str], dict[str, float]]],
) -> dict[str, tuple[float, float]]:
    result: dict[str, tuple[float, float]] = {}
    for feature in FEATURE_ORDER:
        values = [features[feature] for _, features in dataset]
        mean = fmean(values)
        variance = fmean((value - mean) ** 2 for value in values) + 1e-9
        result[feature] = (mean, sqrt(variance))
    return result


def vector(
    features: dict[str, float],
    norm: dict[str, tuple[float, float]],
) -> tuple[float, ...]:
    return tuple(
        (features[feature] - norm[feature][0]) / norm[feature][1]
        for feature in FEATURE_ORDER
    )


def knn_predict(
    train: list[tuple[frozenset[str], tuple[float, ...]]],
    point: tuple[float, ...],
    *,
    k: int = 7,
) -> tuple[frozenset[str], float]:
    distances = []
    for label, candidate in train:
        distance = sum(
            (left - right) ** 2
            for left, right in zip(point, candidate)
        )
        distances.append((distance, label))
    nearest = sorted(distances, key=lambda item: item[0])[:k]
    counts = Counter(label for _, label in nearest)
    best_count = max(counts.values())
    tied = sorted(
        (label for label, count in counts.items() if count == best_count),
        key=lambda label: (len(label), tuple(sorted(label))),
    )
    prediction = tied[0]
    return prediction, best_count / k


def evaluate_ceiling(
    *,
    train_samples: int = 120,
    test_samples: int = 100,
    k: int = 7,
) -> dict[str, float]:
    templates = train_templates(samples=train_samples)
    raw_train = make_dataset(train_samples, 30_000_000)
    test = make_dataset(test_samples, 31_000_000)
    norm = normalization(raw_train)
    train = [
        (label, vector(features, norm))
        for label, features in raw_train
    ]

    bayes_correct = 0
    knn_correct = 0
    shared_error = 0
    disagreement = 0
    either_correct = 0
    total = 0
    knn_confidence: list[float] = []

    for true_label, features in test:
        bayes_prediction, _, _, _ = diagnose_all_probes(
            features,
            templates,
        )
        knn_prediction, confidence = knn_predict(
            train,
            vector(features, norm),
            k=k,
        )

        bayes_ok = bayes_prediction == true_label
        knn_ok = knn_prediction == true_label
        bayes_correct += int(bayes_ok)
        knn_correct += int(knn_ok)
        shared_error += int((not bayes_ok) and (not knn_ok))
        disagreement += int(bayes_prediction != knn_prediction)
        either_correct += int(bayes_ok or knn_ok)
        knn_confidence.append(confidence)
        total += 1

    bayes_accuracy = bayes_correct / total
    knn_accuracy = knn_correct / total
    best_accuracy = max(bayes_accuracy, knn_accuracy)
    union_accuracy = either_correct / total

    return {
        "bayes_accuracy": bayes_accuracy,
        "knn_accuracy": knn_accuracy,
        "shared_error_rate": shared_error / total,
        "classifier_disagreement_rate": disagreement / total,
        "oracle_union_accuracy": union_accuracy,
        "ensemble_headroom": union_accuracy - best_accuracy,
        "knn_mean_vote_confidence": fmean(knn_confidence),
    }


def training_scale_experiment() -> dict[int, float]:
    result: dict[int, float] = {}
    fixed_test = make_dataset(60, 32_000_000)
    for train_samples in (40, 80, 160):
        raw_train = make_dataset(
            train_samples,
            33_000_000 + train_samples * 10_000,
        )
        norm = normalization(raw_train)
        train = [
            (label, vector(features, norm))
            for label, features in raw_train
        ]
        correct = 0
        for true_label, features in fixed_test:
            prediction, _ = knn_predict(
                train,
                vector(features, norm),
                k=7,
            )
            correct += int(prediction == true_label)
        result[train_samples] = correct / len(fixed_test)
    return result


def audit() -> dict[str, object]:
    ceiling = evaluate_ceiling()
    scale = training_scale_experiment()
    scale_gain = scale[160] - scale[80]
    classifier_gain = ceiling["knn_accuracy"] - ceiling["bayes_accuracy"]
    ceiling_stable = (
        abs(classifier_gain) < 0.005
        and ceiling["ensemble_headroom"] < 0.010
        and abs(scale_gain) < 0.005
    )
    return {
        **ceiling,
        "training_scale": scale,
        "scale_gain_80_to_160": scale_gain,
        "ceiling_stable": ceiling_stable,
    }


def format_markdown() -> str:
    result = audit()
    scale = result["training_scale"]
    lines = [
        "# CGD-SIM-009 classifier ceiling audit",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| classifier | exact accuracy |",
        "| --- | ---: |",
        f"| Gaussian independent-likelihood | {result['bayes_accuracy']:.3f} |",
        f"| standardized 7-NN | {result['knn_accuracy']:.3f} |",
        "",
        f"- shared error rate: {result['shared_error_rate']:.3f}",
        f"- classifier disagreement rate: {result['classifier_disagreement_rate']:.3f}",
        f"- oracle union accuracy (either classifier correct): {result['oracle_union_accuracy']:.3f}",
        f"- ensemble headroom over best single classifier: {result['ensemble_headroom']:+.4f}",
        f"- kNN mean vote confidence: {result['knn_mean_vote_confidence']:.3f}",
        "",
        "## Training-scale check",
        "",
        "| train samples / hypothesis | 7-NN exact accuracy |",
        "| ---: | ---: |",
        f"| 40 | {scale[40]:.3f} |",
        f"| 80 | {scale[80]:.3f} |",
        f"| 160 | {scale[160]:.3f} |",
        "",
        f"- gain from 80 -> 160 samples: {result['scale_gain_80_to_160']:+.4f}",
        f"- observation/classifier ceiling stable: {result['ceiling_stable']}",
        "",
        "The audit asks whether the residual error is mostly a weak classifier or "
        "persistent overlap in the declared observation space. A materially better "
        "classifier or a large oracle-union gap means the previous ceiling was too low.",
        "",
        "Interpretation ceiling: synthetic classifier audit only. If stable, the "
        "next frontier is a new observation channel or temporal representation, not "
        "another policy/meta layer.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
