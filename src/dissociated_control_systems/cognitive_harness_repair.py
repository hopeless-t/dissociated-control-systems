"""CGD-SIM-005: harness fault localization and repair loop.

Synthetic control-system experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import exp, log, pi
from random import Random
from statistics import fmean

FAULTS = (
    "healthy",
    "l0_decline",
    "l1_calibration",
    "l2_handoff",
    "observer_bias",
)
REPAIR_FOR = {
    "healthy": "none",
    "l0_decline": "slow_root",
    "l1_calibration": "recalibrate",
    "l2_handoff": "redundant_handoff",
    "observer_bias": "redundant_observer",
}
FEATURES = (
    "performance_loss",
    "performance_drop",
    "self_reference_gap",
    "handoff_gap",
    "observer_disagreement",
)
ACTIVE_SIGNATURE = {
    "l0_decline": "reference_drop",
    "l1_calibration": "self_reference_gap",
    "l2_handoff": "handoff_gap",
    "observer_bias": "observer_disagreement",
}
ACTIVE_PRIORITY = (
    "observer_bias",
    "l2_handoff",
    "l1_calibration",
    "l0_decline",
)


@dataclass(frozen=True)
class HarnessState:
    capability: float = 1.0
    self_estimate: float = 1.0


@dataclass(frozen=True)
class Episode:
    state: HarnessState
    features: dict[str, float]
    mean_function: float
    minimum_function: float
    mean_true_gap: float
    mean_handoff_gap: float
    mean_feedback_error: float


def _clamp(value: float) -> float:
    return min(1.0, max(0.0, value))


def _optimal_compensation(capability: float, cost: float = 0.2) -> float:
    deficit = 1.0 - _clamp(capability)
    return deficit * deficit / (deficit * deficit + cost)


def run_episode(
    faults: frozenset[str],
    seed: int,
    *,
    steps: int = 70,
    state: HarnessState | None = None,
    repairs: frozenset[str] = frozenset(),
) -> Episode:
    """Run one bounded synthetic observation/control episode."""
    unknown = set(faults) - set(FAULTS[1:])
    if unknown:
        raise ValueError(f"unknown faults: {sorted(unknown)}")

    rng = Random(seed)
    capability = 1.0 if state is None else state.capability
    self_estimate = 1.0 if state is None else state.self_estimate
    base_decline = max(0.001, rng.gauss(0.0035, 0.0006))
    intervention_burden = 0.003 * len(repairs)

    performance: list[float] = []
    true_gap: list[float] = []
    self_reference_gap: list[float] = []
    handoff_gap: list[float] = []
    feedback_error: list[float] = []
    observer_disagreement: list[float] = []
    reference_observation: list[float] = []

    for _ in range(steps):
        decline = base_decline
        feedback_gain = 0.35
        handoff_reliability = 1.0
        primary_bias = 0.0

        if "l0_decline" in faults:
            decline *= rng.uniform(1.8, 2.5)
        if "l1_calibration" in faults:
            feedback_gain = rng.uniform(0.025, 0.075)
        if "l2_handoff" in faults:
            handoff_reliability = rng.uniform(0.3, 0.5)
        if "observer_bias" in faults:
            primary_bias = rng.uniform(0.07, 0.12)

        if "slow_root" in repairs:
            decline *= 0.4
        if "recalibrate" in repairs:
            feedback_gain = max(feedback_gain, 0.45)
        if "redundant_handoff" in repairs:
            handoff_reliability += 0.85 * (1.0 - handoff_reliability)

        primary = _clamp(
            capability + primary_bias + rng.gauss(0.0, 0.03)
        )
        reference = _clamp(capability + rng.gauss(0.0, 0.03))
        feedback = (
            reference if "redundant_observer" in repairs else primary
        )

        desired = _optimal_compensation(self_estimate)
        applied = handoff_reliability * desired
        function = _clamp(
            capability
            + (1.0 - capability) * applied
            - intervention_burden
        )

        performance.append(function)
        true_gap.append(abs(self_estimate - capability))
        self_reference_gap.append(abs(self_estimate - reference))
        handoff_gap.append(max(0.0, desired - applied))
        feedback_error.append(abs(feedback - capability))
        observer_disagreement.append(abs(primary - reference))
        reference_observation.append(reference)

        self_estimate = _clamp(
            self_estimate
            + feedback_gain * (feedback - self_estimate)
        )
        rare_shock = 0.008 if rng.random() < 0.03 else 0.0
        capability = _clamp(capability - decline - rare_shock)

    tail = 20
    window = 15
    features = {
        "performance_loss": 1.0 - fmean(performance[-window:]),
        "performance_drop": max(
            0.0,
            fmean(performance[:window]) - fmean(performance[-window:]),
        ),
        "self_reference_gap": fmean(self_reference_gap[-tail:]),
        "handoff_gap": fmean(handoff_gap[-tail:]),
        "observer_disagreement": fmean(observer_disagreement[-tail:]),
        "reference_drop": max(
            0.0,
            fmean(reference_observation[:window])
            - fmean(reference_observation[-window:]),
        ),
    }
    return Episode(
        state=HarnessState(capability, self_estimate),
        features=features,
        mean_function=fmean(performance),
        minimum_function=min(performance),
        mean_true_gap=fmean(true_gap[-tail:]),
        mean_handoff_gap=fmean(handoff_gap[-tail:]),
        mean_feedback_error=fmean(feedback_error[-tail:]),
    )


def train_passive_templates(samples: int = 200) -> dict[str, dict[str, tuple[float, float]]]:
    templates: dict[str, dict[str, tuple[float, float]]] = {}
    for fault_index, fault in enumerate(FAULTS):
        rows: list[dict[str, float]] = []
        fault_set = (
            frozenset()
            if fault == "healthy"
            else frozenset((fault,))
        )
        for seed in range(samples):
            episode = run_episode(
                fault_set,
                100_000 * fault_index + seed,
            )
            rows.append(episode.features)

        templates[fault] = {}
        for feature in FEATURES:
            values = [row[feature] for row in rows]
            mean = fmean(values)
            variance = fmean((value - mean) ** 2 for value in values) + 1e-6
            templates[fault][feature] = (mean, variance)
    return templates


def diagnose_passive(
    features: dict[str, float],
    templates: dict[str, dict[str, tuple[float, float]]],
    *,
    abstain_threshold: float = 0.60,
) -> tuple[str, float, dict[str, float]]:
    """Naive Gaussian Bayes classifier with a fail-closed abstain state."""
    log_probability: dict[str, float] = {}
    prior = -log(len(FAULTS))
    for fault in FAULTS:
        score = prior
        for feature in FEATURES:
            mean, variance = templates[fault][feature]
            value = features[feature]
            score += -0.5 * (
                ((value - mean) ** 2) / variance
                + log(2.0 * pi * variance)
            )
        log_probability[fault] = score

    peak = max(log_probability.values())
    probability = {
        fault: exp(score - peak)
        for fault, score in log_probability.items()
    }
    total = sum(probability.values())
    probability = {
        fault: value / total
        for fault, value in probability.items()
    }
    best = max(probability, key=probability.get)
    confidence = probability[best]
    if confidence < abstain_threshold:
        return "abstain", confidence, probability
    return best, confidence, probability


def _best_balanced_threshold(
    healthy: list[float],
    faulty: list[float],
) -> tuple[float, float]:
    best_score = -1.0
    best_threshold = 0.0
    for threshold in sorted(set(healthy + faulty)):
        sensitivity = fmean(float(value >= threshold) for value in faulty)
        specificity = fmean(float(value < threshold) for value in healthy)
        score = 0.5 * (sensitivity + specificity)
        if score > best_score:
            best_score = score
            best_threshold = threshold
    return best_threshold, best_score


def train_active_thresholds(
    samples: int = 500,
) -> dict[str, tuple[float, float]]:
    """Train one component-specific probe threshold per fault."""
    result: dict[str, tuple[float, float]] = {}
    for fault_index, fault in enumerate(FAULTS[1:], start=1):
        feature = ACTIVE_SIGNATURE[fault]
        healthy: list[float] = []
        faulty: list[float] = []
        for seed in range(samples):
            healthy.append(
                run_episode(
                    frozenset(),
                    500_000 + seed,
                ).features[feature]
            )
            faulty.append(
                run_episode(
                    frozenset((fault,)),
                    600_000 + 100_000 * fault_index + seed,
                ).features[feature]
            )
        result[fault] = _best_balanced_threshold(healthy, faulty)
    return result


def active_detect(
    features: dict[str, float],
    thresholds: dict[str, tuple[float, float]],
) -> set[str]:
    return {
        fault
        for fault, feature in ACTIVE_SIGNATURE.items()
        if features[feature] >= thresholds[fault][0]
    }


def passive_single_fault_experiment(
    samples: int = 500,
) -> dict[str, object]:
    templates = train_passive_templates()
    total = 0
    correct = 0
    abstained = 0
    confidence: list[float] = []

    targeted: dict[str, dict[str, list[float]]] = {
        fault: {
            "baseline_function": [],
            "repaired_function": [],
            "baseline_target": [],
            "repaired_target": [],
        }
        for fault in FAULTS[1:]
    }

    for fault_index, fault in enumerate(FAULTS):
        fault_set = (
            frozenset()
            if fault == "healthy"
            else frozenset((fault,))
        )
        for seed in range(samples):
            pre = run_episode(
                fault_set,
                1_000_000 + 100_000 * fault_index + seed,
            )
            prediction, posterior, _ = diagnose_passive(
                pre.features,
                templates,
            )
            total += 1
            correct += int(prediction == fault)
            abstained += int(prediction == "abstain")
            confidence.append(posterior)

            if fault == "healthy":
                continue

            repair = (
                "none"
                if prediction == "abstain"
                else REPAIR_FOR[prediction]
            )
            chosen = (
                frozenset()
                if repair == "none"
                else frozenset((repair,))
            )
            recovery_seed = 2_000_000 + 100_000 * fault_index + seed
            baseline = run_episode(
                fault_set,
                recovery_seed,
                state=pre.state,
            )
            repaired = run_episode(
                fault_set,
                recovery_seed,
                state=pre.state,
                repairs=chosen,
            )
            bucket = targeted[fault]
            bucket["baseline_function"].append(baseline.mean_function)
            bucket["repaired_function"].append(repaired.mean_function)

            if fault == "l0_decline":
                bucket["baseline_target"].append(baseline.state.capability)
                bucket["repaired_target"].append(repaired.state.capability)
            elif fault == "l1_calibration":
                bucket["baseline_target"].append(baseline.mean_true_gap)
                bucket["repaired_target"].append(repaired.mean_true_gap)
            elif fault == "l2_handoff":
                bucket["baseline_target"].append(baseline.mean_handoff_gap)
                bucket["repaired_target"].append(repaired.mean_handoff_gap)
            elif fault == "observer_bias":
                bucket["baseline_target"].append(baseline.mean_feedback_error)
                bucket["repaired_target"].append(repaired.mean_feedback_error)

    target_summary: dict[str, dict[str, float]] = {}
    for fault, values in targeted.items():
        target_summary[fault] = {
            "baseline_function": fmean(values["baseline_function"]),
            "repaired_function": fmean(values["repaired_function"]),
            "baseline_target": fmean(values["baseline_target"]),
            "repaired_target": fmean(values["repaired_target"]),
        }

    return {
        "accuracy": correct / total,
        "abstain_rate": abstained / total,
        "mean_confidence": fmean(confidence),
        "targeted": target_summary,
    }


def passive_pair_recovery(
    samples: int = 200,
) -> dict[str, float]:
    """Apply the single-fault classifier sequentially to two-fault mixtures."""
    templates = train_passive_templates()
    coverage: list[float] = []
    extras: list[float] = []
    exact = 0
    total = 0

    for pair_index, pair in enumerate(combinations(FAULTS[1:], 2)):
        needed = {REPAIR_FOR[fault] for fault in pair}
        for seed in range(samples):
            repairs: set[str] = set()
            state: HarnessState | None = None
            for cycle in range(4):
                episode = run_episode(
                    frozenset(pair),
                    3_000_000 + 100_000 * pair_index + seed + cycle * 10_000,
                    steps=60,
                    state=state,
                    repairs=frozenset(repairs),
                )
                state = episode.state
                prediction, _, _ = diagnose_passive(
                    episode.features,
                    templates,
                )
                if prediction in ("healthy", "abstain"):
                    break
                repair = REPAIR_FOR[prediction]
                if repair == "none" or repair in repairs:
                    break
                repairs.add(repair)

            coverage.append(len(repairs & needed) / len(needed))
            extras.append(len(repairs - needed))
            exact += int(repairs == needed)
            total += 1

    return {
        "mean_repair_coverage": fmean(coverage),
        "mean_extra_repairs": fmean(extras),
        "exact_recovery_rate": exact / total,
    }


def active_pair_recovery(
    samples: int = 200,
) -> dict[str, float]:
    """Probe, repair one component, re-observe, and repeat."""
    thresholds = train_active_thresholds()
    coverage: list[float] = []
    extras: list[float] = []
    exact = 0
    cycles_used: list[float] = []
    total = 0

    for pair_index, pair in enumerate(combinations(FAULTS[1:], 2)):
        needed = {REPAIR_FOR[fault] for fault in pair}
        for seed in range(samples):
            repairs: set[str] = set()
            state: HarnessState | None = None
            cycles = 0
            for cycle in range(5):
                episode = run_episode(
                    frozenset(pair),
                    4_000_000 + 100_000 * pair_index + seed + cycle * 10_000,
                    steps=60,
                    state=state,
                    repairs=frozenset(repairs),
                )
                state = episode.state
                detected = active_detect(episode.features, thresholds)
                unresolved = [
                    fault
                    for fault in ACTIVE_PRIORITY
                    if fault in detected and REPAIR_FOR[fault] not in repairs
                ]
                cycles += 1
                if not unresolved:
                    break
                repairs.add(REPAIR_FOR[unresolved[0]])

            coverage.append(len(repairs & needed) / len(needed))
            extras.append(len(repairs - needed))
            exact += int(repairs == needed)
            cycles_used.append(cycles)
            total += 1

    return {
        "mean_repair_coverage": fmean(coverage),
        "mean_extra_repairs": fmean(extras),
        "exact_recovery_rate": exact / total,
        "mean_cycles": fmean(cycles_used),
    }


def format_markdown() -> str:
    single = passive_single_fault_experiment()
    passive_pair = passive_pair_recovery()
    active_pair = active_pair_recovery()
    thresholds = train_active_thresholds()

    lines = [
        "# CGD-SIM-005 harness fault localization and repair",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "## Passive Bayesian localization — single faults",
        "",
        f"- accuracy: {single['accuracy']:.3f}",
        f"- abstain rate: {single['abstain_rate']:.3f}",
        f"- mean posterior confidence: {single['mean_confidence']:.3f}",
        "",
        "| fault | baseline function | repaired function | target before | target after |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for fault in FAULTS[1:]:
        row = single["targeted"][fault]
        lines.append(
            f"| {fault} | {row['baseline_function']:.3f} | "
            f"{row['repaired_function']:.3f} | "
            f"{row['baseline_target']:.3f} | "
            f"{row['repaired_target']:.3f} |"
        )

    lines.extend(
        [
            "",
            "Target semantics:",
            "- l0_decline: final latent capability (higher is better);",
            "- l1_calibration: true self/capability gap (lower is better);",
            "- l2_handoff: command/receipt gap (lower is better);",
            "- observer_bias: feedback/latent-state error (lower is better).",
            "",
            "## Two simultaneous faults",
            "",
            "| harness | repair coverage | extra repairs | exact recovery | mean cycles |",
            "| --- | ---: | ---: | ---: | ---: |",
            (
                "| passive single-fault Bayes loop | "
                f"{passive_pair['mean_repair_coverage']:.3f} | "
                f"{passive_pair['mean_extra_repairs']:.3f} | "
                f"{passive_pair['exact_recovery_rate']:.3f} | n/a |"
            ),
            (
                "| active probe -> repair -> re-observe loop | "
                f"{active_pair['mean_repair_coverage']:.3f} | "
                f"{active_pair['mean_extra_repairs']:.3f} | "
                f"{active_pair['exact_recovery_rate']:.3f} | "
                f"{active_pair['mean_cycles']:.3f} |"
            ),
            "",
            "## Learned active-probe thresholds",
            "",
            "| component | feature | threshold | training balanced accuracy |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    for fault in FAULTS[1:]:
        threshold, balanced = thresholds[fault]
        lines.append(
            f"| {fault} | {ACTIVE_SIGNATURE[fault]} | "
            f"{threshold:.4f} | {balanced:.3f} |"
        )

    l0 = single["targeted"]["l0_decline"]
    lines.extend(
        [
            "",
            "Important proxy result:",
            (
                "- the l0 repair can preserve latent capability while surface "
                "mean function temporarily falls, because the uncompensated "
                "surface metric had been partially masked by stronger "
                "compensation. Therefore repair success cannot be judged by "
                "surface function alone."
            ),
            (
                f"- frozen l0 aggregate: function "
                f"{l0['baseline_function']:.3f} -> "
                f"{l0['repaired_function']:.3f}, while final latent capability "
                f"{l0['baseline_target']:.3f} -> "
                f"{l0['repaired_target']:.3f}."
            ),
            "",
            "Interpretation ceiling: the experiment validates a synthetic "
            "fault-localization/repair harness, not a medical diagnostic or "
            "treatment system.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
