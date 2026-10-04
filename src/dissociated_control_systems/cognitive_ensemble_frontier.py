"""CGD-SIM-010: Bayes + kNN ensemble frontier.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from statistics import fmean

from .cognitive_active_diagnosis import (
    PROBES,
    hypotheses,
    train_templates,
    update_posterior,
)
from .cognitive_ceiling_audit import make_dataset, normalization, vector

K_VALUES = (3, 5, 7, 11, 15)
WEIGHTS = tuple(step / 10.0 for step in range(11))


def bayes_posterior(
    features: dict[str, float],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
) -> dict[frozenset[str], float]:
    hs = hypotheses()
    posterior = {hypothesis: 1.0 / len(hs) for hypothesis in hs}
    for probe in PROBES:
        posterior = update_posterior(
            posterior,
            probe=probe,
            value=features[probe],
            templates=templates,
        )
    return posterior


def _vote_posterior(
    nearest_labels: list[frozenset[str]],
    k: int,
) -> dict[frozenset[str], float]:
    counts = Counter(nearest_labels[:k])
    hs = hypotheses()
    smoothing = 0.05
    denominator = k + smoothing * len(hs)
    return {
        hypothesis: (counts.get(hypothesis, 0) + smoothing) / denominator
        for hypothesis in hs
    }


def precompute_posteriors(
    dataset: list[tuple[frozenset[str], dict[str, float]]],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    norm: dict[str, tuple[float, float]],
    train: list[tuple[frozenset[str], tuple[float, ...]]],
) -> list[
    tuple[
        frozenset[str],
        dict[frozenset[str], float],
        dict[int, dict[frozenset[str], float]],
    ]
]:
    result = []
    for true_label, features in dataset:
        point = vector(features, norm)
        distances = [
            (
                sum(
                    (left - right) ** 2
                    for left, right in zip(point, candidate)
                ),
                label,
            )
            for label, candidate in train
        ]
        nearest = [
            label
            for _, label in sorted(distances, key=lambda item: item[0])[: max(K_VALUES)]
        ]
        knn_by_k = {
            k: _vote_posterior(nearest, k)
            for k in K_VALUES
        }
        result.append(
            (
                true_label,
                bayes_posterior(features, templates),
                knn_by_k,
            )
        )
    return result


def mix_posteriors(
    bayes: dict[frozenset[str], float],
    knn: dict[frozenset[str], float],
    *,
    bayes_weight: float,
) -> dict[frozenset[str], float]:
    return {
        hypothesis: (
            bayes_weight * bayes[hypothesis]
            + (1.0 - bayes_weight) * knn[hypothesis]
        )
        for hypothesis in bayes
    }


def prepare(
    train_samples: int = 160,
) -> tuple[
    dict[frozenset[str], dict[str, tuple[float, float]]],
    dict[str, tuple[float, float]],
    list[tuple[frozenset[str], tuple[float, ...]]],
]:
    templates = train_templates(samples=train_samples)
    raw_train = make_dataset(train_samples, 40_000_000)
    norm = normalization(raw_train)
    train = [
        (label, vector(features, norm))
        for label, features in raw_train
    ]
    return templates, norm, train


def evaluate_precomputed(
    data: list[
        tuple[
            frozenset[str],
            dict[frozenset[str], float],
            dict[int, dict[frozenset[str], float]],
        ]
    ],
    *,
    k: int,
    bayes_weight: float,
) -> dict[str, float]:
    bayes_correct = 0
    knn_correct = 0
    ensemble_correct = 0
    oracle_union_correct = 0
    confidence: list[float] = []

    for true_label, bp, knn_by_k in data:
        kp = knn_by_k[k]
        ep = mix_posteriors(
            bp,
            kp,
            bayes_weight=bayes_weight,
        )
        b = max(bp, key=bp.get)
        n = max(kp, key=kp.get)
        e = max(ep, key=ep.get)
        bayes_ok = b == true_label
        knn_ok = n == true_label
        ensemble_ok = e == true_label
        bayes_correct += int(bayes_ok)
        knn_correct += int(knn_ok)
        ensemble_correct += int(ensemble_ok)
        oracle_union_correct += int(bayes_ok or knn_ok)
        confidence.append(ep[e])

    total = len(data)
    return {
        "bayes_accuracy": bayes_correct / total,
        "knn_accuracy": knn_correct / total,
        "ensemble_accuracy": ensemble_correct / total,
        "oracle_union_accuracy": oracle_union_correct / total,
        "mean_ensemble_confidence": fmean(confidence),
    }


@lru_cache(maxsize=1)
def optimize() -> dict[str, object]:
    templates, norm, train = prepare()
    validation_raw = make_dataset(40, 41_000_000)
    validation = precompute_posteriors(
        validation_raw,
        templates,
        norm,
        train,
    )

    best_score = -1.0
    best_params = (7, 0.5)
    for k in K_VALUES:
        for weight in WEIGHTS:
            result = evaluate_precomputed(
                validation,
                k=k,
                bayes_weight=weight,
            )
            if result["ensemble_accuracy"] > best_score:
                best_score = result["ensemble_accuracy"]
                best_params = (k, weight)

    test_raw = make_dataset(100, 42_000_000)
    test = precompute_posteriors(
        test_raw,
        templates,
        norm,
        train,
    )
    result = evaluate_precomputed(
        test,
        k=best_params[0],
        bayes_weight=best_params[1],
    )
    best_single = max(result["bayes_accuracy"], result["knn_accuracy"])
    result["ensemble_gain"] = result["ensemble_accuracy"] - best_single
    result["residual_oracle_gap"] = (
        result["oracle_union_accuracy"] - result["ensemble_accuracy"]
    )
    result["k"] = best_params[0]
    result["bayes_weight"] = best_params[1]
    result["frontier_stable"] = (
        result["ensemble_gain"] < 0.005
        and result["residual_oracle_gap"] < 0.010
    )
    return result


def format_markdown() -> str:
    result = optimize()
    return "\n".join(
        [
            "# CGD-SIM-010 Bayes + kNN ensemble frontier",
            "",
            "> Synthetic control-model result only. Clinical authority: NONE.",
            "",
            "| model | exact accuracy |",
            "| --- | ---: |",
            f"| Bayes | {result['bayes_accuracy']:.3f} |",
            f"| kNN | {result['knn_accuracy']:.3f} |",
            f"| optimized posterior ensemble | {result['ensemble_accuracy']:.3f} |",
            f"| oracle union | {result['oracle_union_accuracy']:.3f} |",
            "",
            f"- selected k: {result['k']}",
            f"- selected Bayes weight: {result['bayes_weight']:.2f}",
            f"- ensemble gain over best single classifier: {result['ensemble_gain']:+.4f}",
            f"- residual oracle-union gap: {result['residual_oracle_gap']:+.4f}",
            f"- mean ensemble confidence: {result['mean_ensemble_confidence']:.3f}",
            f"- classifier frontier stable: {result['frontier_stable']}",
            "",
            "Distance calculations are precomputed once per held-out point and reused "
            "across all k/weight candidates; this changes harness friction, not the "
            "declared search space.",
            "",
            "If residual oracle headroom remains, the next loop should learn a "
            "disagreement resolver rather than add a new meta-control layer.",
        ]
    )


if __name__ == "__main__":
    print(format_markdown())
