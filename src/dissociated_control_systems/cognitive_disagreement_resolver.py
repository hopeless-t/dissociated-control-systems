"""CGD-SIM-011: learned disagreement resolver.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from collections import defaultdict

from .cognitive_ceiling_audit import make_dataset
from .cognitive_ensemble_frontier import (
    K_VALUES,
    prepare,
    precompute_posteriors,
)


def _winner(posterior: dict[frozenset[str], float]) -> tuple[frozenset[str], float]:
    label = max(posterior, key=posterior.get)
    return label, posterior[label]


def train_pair_preferences(
    data,
    *,
    k: int,
    min_support: int = 5,
    preference_threshold: float = 0.65,
):
    stats = defaultdict(lambda: [0, 0, 0])
    for true_label, bp, knn_by_k in data:
        kp = knn_by_k[k]
        b, _ = _winner(bp)
        n, _ = _winner(kp)
        if b == n:
            continue
        key = (b, n)
        stats[key][0] += int(b == true_label)
        stats[key][1] += int(n == true_label)
        stats[key][2] += 1

    preferences = {}
    for key, (b_correct, n_correct, support) in stats.items():
        if support < min_support:
            continue
        total_correct = b_correct + n_correct
        if total_correct == 0:
            continue
        if b_correct / total_correct >= preference_threshold:
            preferences[key] = "bayes"
        elif n_correct / total_correct >= preference_threshold:
            preferences[key] = "knn"
    return preferences


def resolve(
    bp,
    kp,
    preferences,
    *,
    gamma: float,
    delta: float,
):
    b, bc = _winner(bp)
    n, nc = _winner(kp)
    if b == n:
        return b

    preferred = preferences.get((b, n))
    if preferred == "bayes":
        return b
    if preferred == "knn":
        return n

    # Confidence fallback learned on validation.
    return n if nc - gamma * bc > delta else b


def evaluate(
    data,
    *,
    k: int,
    preferences,
    gamma: float,
    delta: float,
):
    bayes_correct = 0
    knn_correct = 0
    resolver_correct = 0
    oracle_correct = 0
    disagreements = 0

    for true_label, bp, knn_by_k in data:
        kp = knn_by_k[k]
        b, _ = _winner(bp)
        n, _ = _winner(kp)
        r = resolve(
            bp,
            kp,
            preferences,
            gamma=gamma,
            delta=delta,
        )
        bayes_ok = b == true_label
        knn_ok = n == true_label
        bayes_correct += int(bayes_ok)
        knn_correct += int(knn_ok)
        resolver_correct += int(r == true_label)
        oracle_correct += int(bayes_ok or knn_ok)
        disagreements += int(b != n)

    total = len(data)
    return {
        "bayes_accuracy": bayes_correct / total,
        "knn_accuracy": knn_correct / total,
        "resolver_accuracy": resolver_correct / total,
        "oracle_union_accuracy": oracle_correct / total,
        "disagreement_rate": disagreements / total,
    }


def optimize():
    templates, norm, train = prepare()
    validation = precompute_posteriors(
        make_dataset(60, 50_000_000),
        templates,
        norm,
        train,
    )

    best = None
    best_params = None
    for k in K_VALUES:
        preferences = train_pair_preferences(validation, k=k)
        for gamma in (0.50, 0.75, 1.00, 1.25, 1.50):
            for delta in (-0.20, -0.10, 0.0, 0.10, 0.20):
                result = evaluate(
                    validation,
                    k=k,
                    preferences=preferences,
                    gamma=gamma,
                    delta=delta,
                )
                if best is None or result["resolver_accuracy"] > best["resolver_accuracy"]:
                    best = result
                    best_params = (k, gamma, delta, preferences)

    assert best_params is not None
    k, gamma, delta, preferences = best_params
    test = precompute_posteriors(
        make_dataset(120, 51_000_000),
        templates,
        norm,
        train,
    )
    result = evaluate(
        test,
        k=k,
        preferences=preferences,
        gamma=gamma,
        delta=delta,
    )
    best_single = max(result["bayes_accuracy"], result["knn_accuracy"])
    result["resolver_gain"] = result["resolver_accuracy"] - best_single
    result["residual_oracle_gap"] = (
        result["oracle_union_accuracy"] - result["resolver_accuracy"]
    )
    result["k"] = k
    result["gamma"] = gamma
    result["delta"] = delta
    result["learned_pair_rules"] = len(preferences)
    result["resolver_stable"] = (
        result["resolver_gain"] < 0.005
        and result["residual_oracle_gap"] < 0.010
    )
    return result


def format_markdown() -> str:
    result = optimize()
    return "\n".join(
        [
            "# CGD-SIM-011 learned disagreement resolver",
            "",
            "> Synthetic control-model result only. Clinical authority: NONE.",
            "",
            "| model | exact accuracy |",
            "| --- | ---: |",
            f"| Bayes | {result['bayes_accuracy']:.3f} |",
            f"| kNN | {result['knn_accuracy']:.3f} |",
            f"| learned disagreement resolver | {result['resolver_accuracy']:.3f} |",
            f"| oracle union | {result['oracle_union_accuracy']:.3f} |",
            "",
            f"- selected k: {result['k']}",
            f"- selected gamma: {result['gamma']:.2f}",
            f"- selected delta: {result['delta']:.2f}",
            f"- learned pair-specific rules: {result['learned_pair_rules']}",
            f"- classifier disagreement rate: {result['disagreement_rate']:.3f}",
            f"- resolver gain over best single: {result['resolver_gain']:+.4f}",
            f"- residual oracle-union gap: {result['residual_oracle_gap']:+.4f}",
            f"- resolver frontier stable: {result['resolver_stable']}",
            "",
            "The resolver only acts at the integration fault: when the two "
            "classifiers disagree. Agreement cases are untouched.",
            "",
            "If a substantial oracle gap survives, the remaining ambiguity is not "
            "solved by simple classifier arbitration and the next frontier should "
            "add genuinely new temporal evidence.",
        ]
    )


if __name__ == "__main__":
    print(format_markdown())
