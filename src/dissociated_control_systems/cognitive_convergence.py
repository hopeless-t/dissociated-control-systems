"""CGD-SIM-008: information frontier and local convergence search.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache

from math import log
from statistics import fmean

from .cognitive_active_diagnosis import (
    PROBES,
    _repair_set,
    diagnose_adaptive,
    diagnose_all_probes,
    hypotheses,
    train_templates,
    update_posterior,
)
from .cognitive_harness_repair import run_episode


def entropy(posterior: dict[frozenset[str], float]) -> float:
    return -sum(
        probability * log(probability)
        for probability in posterior.values()
        if probability > 0.0
    )


def entropy_probe_value(
    posterior: dict[frozenset[str], float],
    *,
    probe: str,
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    cost_weight: float,
) -> float:
    """Approximate expected entropy reduction minus symbolic probe friction."""
    before = entropy(posterior)
    expected_after = 0.0
    for hypothesis, probability in posterior.items():
        representative_value = templates[hypothesis][probe][0]
        after = update_posterior(
            posterior,
            probe=probe,
            value=representative_value,
            templates=templates,
        )
        expected_after += probability * entropy(after)
    return before - expected_after - cost_weight * PROBES[probe]


def diagnose_entropy_adaptive(
    features: dict[str, float],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    *,
    confidence_threshold: float,
    cost_weight: float,
) -> tuple[frozenset[str], float, float, int]:
    hs = hypotheses()
    posterior = {hypothesis: 1.0 / len(hs) for hypothesis in hs}
    remaining = set(PROBES)
    spent = 0.0
    count = 0

    while remaining:
        best_hypothesis = max(posterior, key=posterior.get)
        if count >= 1 and posterior[best_hypothesis] >= confidence_threshold:
            break

        ranked = sorted(
            remaining,
            key=lambda probe: (
                entropy_probe_value(
                    posterior,
                    probe=probe,
                    templates=templates,
                    cost_weight=cost_weight,
                ),
                -PROBES[probe],
                probe,
            ),
            reverse=True,
        )
        probe = ranked[0]
        value = entropy_probe_value(
            posterior,
            probe=probe,
            templates=templates,
            cost_weight=cost_weight,
        )
        if count >= 1 and value <= 0.0:
            break

        posterior = update_posterior(
            posterior,
            probe=probe,
            value=features[probe],
            templates=templates,
        )
        remaining.remove(probe)
        spent += PROBES[probe]
        count += 1

    best = max(posterior, key=posterior.get)
    return best, posterior[best], spent, count


def make_dataset(samples: int, seed_base: int) -> list[tuple[frozenset[str], dict[str, float]]]:
    data: list[tuple[frozenset[str], dict[str, float]]] = []
    for hypothesis_index, true_faults in enumerate(hypotheses()):
        for sample in range(samples):
            episode = run_episode(
                true_faults,
                seed_base + hypothesis_index * 100_000 + sample,
                steps=60,
            )
            data.append((true_faults, episode.features))
    return data


def utility(
    *,
    exact_accuracy: float,
    coverage: float,
    extra_repairs: float,
    probe_cost: float,
) -> float:
    return (
        0.70 * exact_accuracy
        + 0.30 * coverage
        - 0.20 * extra_repairs
        - 0.12 * probe_cost
    )


def evaluate_policy(
    dataset: list[tuple[frozenset[str], dict[str, float]]],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    *,
    kind: str,
    confidence_threshold: float = 0.90,
    cost_weight: float = 0.50,
) -> dict[str, float]:
    exact: list[float] = []
    coverage: list[float] = []
    extra: list[float] = []
    costs: list[float] = []
    probes: list[float] = []

    for true_faults, features in dataset:
        if kind == "all":
            prediction, _, cost, count = diagnose_all_probes(
                features,
                templates,
            )
        elif kind == "snr":
            prediction, _, cost, count = diagnose_adaptive(
                features,
                templates,
                confidence_threshold=confidence_threshold,
                cost_weight=cost_weight,
            )
        elif kind == "entropy":
            prediction, _, cost, count = diagnose_entropy_adaptive(
                features,
                templates,
                confidence_threshold=confidence_threshold,
                cost_weight=cost_weight,
            )
        else:
            raise ValueError("unknown policy kind")

        true_repairs = _repair_set(true_faults)
        predicted_repairs = _repair_set(prediction)
        denominator = max(1, len(true_repairs))
        exact.append(float(prediction == true_faults))
        coverage.append(
            1.0 if not true_repairs else len(predicted_repairs & true_repairs) / denominator
        )
        extra.append(len(predicted_repairs - true_repairs))
        costs.append(cost)
        probes.append(count)

    result = {
        "exact_accuracy": fmean(exact),
        "coverage": fmean(coverage),
        "extra_repairs": fmean(extra),
        "probe_cost": fmean(costs),
        "probe_count": fmean(probes),
    }
    result["utility"] = utility(
        exact_accuracy=result["exact_accuracy"],
        coverage=result["coverage"],
        extra_repairs=result["extra_repairs"],
        probe_cost=result["probe_cost"],
    )
    return result


def optimize(
    dataset: list[tuple[frozenset[str], dict[str, float]]],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    *,
    kind: str,
) -> tuple[dict[str, float], tuple[float, float]]:
    best_result: dict[str, float] | None = None
    best_params = (0.90, 0.50)
    for confidence in (0.65, 0.75, 0.85, 0.90, 0.95, 0.98):
        for cost_weight in (0.0, 0.20, 0.50, 1.0, 2.0):
            result = evaluate_policy(
                dataset,
                templates,
                kind=kind,
                confidence_threshold=confidence,
                cost_weight=cost_weight,
            )
            if best_result is None or result["utility"] > best_result["utility"]:
                best_result = result
                best_params = (confidence, cost_weight)
    assert best_result is not None
    return best_result, best_params


@lru_cache(maxsize=1)
def convergence_experiment() -> dict[str, object]:
    templates = train_templates(samples=120)
    validation = make_dataset(35, 20_000_000)
    test = make_dataset(100, 21_000_000)

    all_result = evaluate_policy(test, templates, kind="all")
    _, snr_params = optimize(validation, templates, kind="snr")
    _, entropy_params = optimize(validation, templates, kind="entropy")

    snr_result = evaluate_policy(
        test,
        templates,
        kind="snr",
        confidence_threshold=snr_params[0],
        cost_weight=snr_params[1],
    )
    entropy_result = evaluate_policy(
        test,
        templates,
        kind="entropy",
        confidence_threshold=entropy_params[0],
        cost_weight=entropy_params[1],
    )

    best_adaptive = (
        entropy_result
        if entropy_result["utility"] >= snr_result["utility"]
        else snr_result
    )
    best_name = (
        "entropy_voi"
        if entropy_result["utility"] >= snr_result["utility"]
        else "snr_value"
    )

    information_ceiling_gap = (
        all_result["exact_accuracy"] - best_adaptive["exact_accuracy"]
    )
    generation_gain = entropy_result["utility"] - snr_result["utility"]
    locally_saturated = (
        abs(generation_gain) < 0.005
        and information_ceiling_gap < 0.015
    )

    return {
        "all_probes": all_result,
        "snr_value": snr_result,
        "entropy_voi": entropy_result,
        "snr_params": snr_params,
        "entropy_params": entropy_params,
        "best_adaptive_name": best_name,
        "information_ceiling_gap": information_ceiling_gap,
        "generation_gain": generation_gain,
        "locally_saturated": locally_saturated,
    }


def format_markdown() -> str:
    result = convergence_experiment()
    lines = [
        "# CGD-SIM-008 information frontier and convergence search",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| policy | exact accuracy | coverage | extra repairs | probe cost | probes | utility |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in ("all_probes", "snr_value", "entropy_voi"):
        row = result[name]
        lines.append(
            f"| {name} | {row['exact_accuracy']:.3f} | "
            f"{row['coverage']:.3f} | {row['extra_repairs']:.3f} | "
            f"{row['probe_cost']:.3f} | {row['probe_count']:.3f} | "
            f"{row['utility']:.3f} |"
        )

    lines.extend(
        [
            "",
            (
                "Optimized SNR parameters: "
                f"confidence={result['snr_params'][0]:.2f}, "
                f"cost_weight={result['snr_params'][1]:.2f}"
            ),
            (
                "Optimized entropy-VOI parameters: "
                f"confidence={result['entropy_params'][0]:.2f}, "
                f"cost_weight={result['entropy_params'][1]:.2f}"
            ),
            (
                "Best adaptive policy: "
                f"{result['best_adaptive_name']}"
            ),
            (
                "Accuracy gap to all-probe information ceiling: "
                f"{result['information_ceiling_gap']:+.4f}"
            ),
            (
                "Entropy-VOI utility gain over optimized SNR generation: "
                f"{result['generation_gain']:+.4f}"
            ),
            (
                "Local saturation criterion met: "
                f"{result['locally_saturated']}"
            ),
            "",
            "Convergence criterion is deliberately local: the adaptive family is "
            "called saturated only when a new selection rule adds <0.005 utility "
            "and remains within 0.015 exact accuracy of the all-probe information ceiling.",
            "",
            "Interpretation ceiling: this is convergence inside the declared "
            "synthetic observation/policy family, not a global optimum and not a "
            "clinical diagnostic limit.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
