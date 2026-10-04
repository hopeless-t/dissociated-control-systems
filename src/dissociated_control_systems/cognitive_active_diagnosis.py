"""CGD-SIM-007: cost-aware active diagnosis.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from itertools import combinations
from math import exp, log, pi
from statistics import fmean

from .cognitive_harness_repair import FAULTS, REPAIR_FOR, run_episode

FAULT_NAMES = tuple(FAULTS[1:])
PROBES = {
    "reference_drop": 0.40,
    "self_reference_gap": 0.20,
    "handoff_gap": 0.15,
    "observer_disagreement": 0.25,
}


def hypotheses() -> tuple[frozenset[str], ...]:
    result: list[frozenset[str]] = [frozenset()]
    for count in range(1, len(FAULT_NAMES) + 1):
        result.extend(frozenset(x) for x in combinations(FAULT_NAMES, count))
    return tuple(result)


def train_templates(
    samples: int = 120,
) -> dict[frozenset[str], dict[str, tuple[float, float]]]:
    templates: dict[frozenset[str], dict[str, tuple[float, float]]] = {}
    for hypothesis_index, hypothesis in enumerate(hypotheses()):
        rows = [
            run_episode(
                hypothesis,
                11_000_000 + hypothesis_index * 100_000 + seed,
                steps=60,
            ).features
            for seed in range(samples)
        ]
        templates[hypothesis] = {}
        for probe in PROBES:
            values = [row[probe] for row in rows]
            mean = fmean(values)
            variance = fmean((value - mean) ** 2 for value in values) + 1e-6
            templates[hypothesis][probe] = (mean, variance)
    return templates


def _normalize(logp: dict[frozenset[str], float]) -> dict[frozenset[str], float]:
    peak = max(logp.values())
    weights = {h: exp(value - peak) for h, value in logp.items()}
    total = sum(weights.values())
    return {h: value / total for h, value in weights.items()}


def update_posterior(
    posterior: dict[frozenset[str], float],
    *,
    probe: str,
    value: float,
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
) -> dict[frozenset[str], float]:
    logp: dict[frozenset[str], float] = {}
    for hypothesis, prior in posterior.items():
        mean, variance = templates[hypothesis][probe]
        logp[hypothesis] = (
            log(max(prior, 1e-300))
            - 0.5 * (
                ((value - mean) ** 2) / variance
                + log(2.0 * pi * variance)
            )
        )
    return _normalize(logp)


def probe_information_score(
    posterior: dict[frozenset[str], float],
    *,
    probe: str,
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    cost_weight: float,
) -> float:
    """Posterior-weighted separation/noise score minus declared probe cost."""
    means = {
        hypothesis: templates[hypothesis][probe][0]
        for hypothesis in posterior
    }
    mean_bar = sum(
        posterior[hypothesis] * means[hypothesis]
        for hypothesis in posterior
    )
    between = sum(
        posterior[hypothesis] * (means[hypothesis] - mean_bar) ** 2
        for hypothesis in posterior
    )
    within = sum(
        posterior[hypothesis] * templates[hypothesis][probe][1]
        for hypothesis in posterior
    )
    signal_to_noise = between / (within + 1e-12)
    return log(1.0 + signal_to_noise) - cost_weight * PROBES[probe]


def diagnose_all_probes(
    features: dict[str, float],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
) -> tuple[frozenset[str], float, float, int]:
    hs = hypotheses()
    posterior = {hypothesis: 1.0 / len(hs) for hypothesis in hs}
    for probe in PROBES:
        posterior = update_posterior(
            posterior,
            probe=probe,
            value=features[probe],
            templates=templates,
        )
    best = max(posterior, key=posterior.get)
    return best, posterior[best], sum(PROBES.values()), len(PROBES)


def diagnose_adaptive(
    features: dict[str, float],
    templates: dict[frozenset[str], dict[str, tuple[float, float]]],
    *,
    confidence_threshold: float = 0.90,
    cost_weight: float = 0.50,
    minimum_probes: int = 1,
) -> tuple[frozenset[str], float, float, int]:
    hs = hypotheses()
    posterior = {hypothesis: 1.0 / len(hs) for hypothesis in hs}
    remaining = set(PROBES)
    spent = 0.0
    count = 0

    while remaining:
        best_hypothesis = max(posterior, key=posterior.get)
        if count >= minimum_probes and posterior[best_hypothesis] >= confidence_threshold:
            break

        ranked = sorted(
            remaining,
            key=lambda probe: (
                probe_information_score(
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
        score = probe_information_score(
            posterior,
            probe=probe,
            templates=templates,
            cost_weight=cost_weight,
        )
        if count >= minimum_probes and score <= 0.0:
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


def _repair_set(hypothesis: frozenset[str]) -> frozenset[str]:
    return frozenset(REPAIR_FOR[fault] for fault in hypothesis)


def evaluate(
    *,
    samples: int = 100,
    confidence_threshold: float = 0.90,
    cost_weight: float = 0.50,
) -> dict[str, dict[str, float]]:
    templates = train_templates()
    accum = {
        "all_probes": {
            "exact": [],
            "coverage": [],
            "extra": [],
            "cost": [],
            "probes": [],
            "confidence": [],
        },
        "adaptive": {
            "exact": [],
            "coverage": [],
            "extra": [],
            "cost": [],
            "probes": [],
            "confidence": [],
        },
    }

    for hypothesis_index, true_faults in enumerate(hypotheses()):
        true_repairs = _repair_set(true_faults)
        for seed in range(samples):
            features = run_episode(
                true_faults,
                12_000_000 + hypothesis_index * 100_000 + seed,
                steps=60,
            ).features

            all_result = diagnose_all_probes(features, templates)
            adaptive_result = diagnose_adaptive(
                features,
                templates,
                confidence_threshold=confidence_threshold,
                cost_weight=cost_weight,
            )

            for name, result in (
                ("all_probes", all_result),
                ("adaptive", adaptive_result),
            ):
                prediction, confidence, cost, probe_count = result
                predicted_repairs = _repair_set(prediction)
                denominator = max(1, len(true_repairs))
                accum[name]["exact"].append(float(prediction == true_faults))
                accum[name]["coverage"].append(
                    1.0 if not true_repairs else len(predicted_repairs & true_repairs) / denominator
                )
                accum[name]["extra"].append(len(predicted_repairs - true_repairs))
                accum[name]["cost"].append(cost)
                accum[name]["probes"].append(probe_count)
                accum[name]["confidence"].append(confidence)

    output: dict[str, dict[str, float]] = {}
    for name, metrics in accum.items():
        output[name] = {
            "exact_accuracy": fmean(metrics["exact"]),
            "mean_repair_coverage": fmean(metrics["coverage"]),
            "mean_extra_repairs": fmean(metrics["extra"]),
            "mean_probe_cost": fmean(metrics["cost"]),
            "mean_probe_count": fmean(metrics["probes"]),
            "mean_confidence": fmean(metrics["confidence"]),
        }
    return output


def format_markdown() -> str:
    result = evaluate()
    lines = [
        "# CGD-SIM-007 cost-aware active diagnosis",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "Candidate fault sets: all 16 subsets of {L0, L1, L2, observer}.",
        "",
        "| policy | exact accuracy | repair coverage | extra repairs | mean probe cost | mean probes | confidence |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in ("all_probes", "adaptive"):
        row = result[name]
        lines.append(
            f"| {name} | {row['exact_accuracy']:.3f} | "
            f"{row['mean_repair_coverage']:.3f} | "
            f"{row['mean_extra_repairs']:.3f} | "
            f"{row['mean_probe_cost']:.3f} | "
            f"{row['mean_probe_count']:.3f} | "
            f"{row['mean_confidence']:.3f} |"
        )

    all_row = result["all_probes"]
    adaptive = result["adaptive"]
    cost_reduction = 1.0 - adaptive["mean_probe_cost"] / all_row["mean_probe_cost"]
    probe_reduction = 1.0 - adaptive["mean_probe_count"] / all_row["mean_probe_count"]
    accuracy_delta = adaptive["exact_accuracy"] - all_row["exact_accuracy"]

    lines.extend(
        [
            "",
            f"- probe-cost reduction: {cost_reduction:.1%}",
            f"- probe-count reduction: {probe_reduction:.1%}",
            f"- exact-accuracy delta vs all probes: {accuracy_delta:+.4f}",
            "",
            "Selection score:",
            "",
            "V(j|p) = log(1 + between_hypothesis_variance / within_hypothesis_noise)",
            "         - cost_weight * probe_cost",
            "",
            "The adaptive harness stops once posterior confidence is high enough or "
            "no remaining probe has positive declared net value.",
            "",
            "Interpretation ceiling: symbolic probe costs and synthetic fault "
            "distributions only; this is not a clinical test-selection rule.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
