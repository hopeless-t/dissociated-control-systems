"""CGD-SIM-018: template-residual CUSUM for weak variance shift.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean

from .cognitive_active_diagnosis import PROBES, hypotheses, train_templates
from .cognitive_fixed_point import select_params
from .cognitive_ood_challenge import (
    combined_shift,
    common_mode_bias,
    noise_inflation,
    probe_dropout,
    train_means,
)
from .cognitive_ood_routing import MISSING_KEYS, predict_rows
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset

SEQUENCE_SIZE = 800
K_GRID = (0.10, 0.20, 0.30, 0.40, 0.50)
TARGET_CLEAN_FPR = 0.10


def shuffled(dataset, *, seed: int):
    rows = list(dataset)
    Random(seed).shuffle(rows)
    return rows


def residual_energy(features, templates):
    """Best clean-template standardized residual energy.

    The minimum over hypotheses removes between-state mean differences before
    monitoring within-state surprise.
    """
    if any(features.get(key, 0.0) > 0.5 for key in MISSING_KEYS):
        return 1_000.0

    energies = []
    for hypothesis in hypotheses():
        squared = []
        for probe in PROBES:
            mean, variance = templates[hypothesis][probe]
            squared.append((features[probe] - mean) ** 2 / variance)
        energies.append(fmean(squared))
    return min(energies)


def score_stats(dataset, templates):
    values = [residual_energy(features, templates) for _, features in dataset]
    mean = fmean(values)
    variance = fmean((value - mean) ** 2 for value in values) + 1e-9
    return mean, variance ** 0.5


def standardized_scores(dataset, templates, stats):
    mean, std = stats
    return [
        (residual_energy(features, templates) - mean) / std
        for _, features in dataset
    ]


def cusum_trace(scores, *, kappa: float):
    current = 0.0
    trace = []
    for score in scores:
        current = max(0.0, current + score - kappa)
        trace.append(current)
    return trace


def max_cusum(dataset, templates, stats, *, kappa: float, seed: int):
    ordered = shuffled(dataset, seed=seed)
    trace = cusum_trace(
        standardized_scores(ordered, templates, stats),
        kappa=kappa,
    )
    return max(trace) if trace else 0.0


def detection_point(dataset, templates, stats, *, kappa: float, threshold: float, seed: int):
    ordered = shuffled(dataset, seed=seed)
    scores = standardized_scores(ordered, templates, stats)
    trace = cusum_trace(scores, kappa=kappa)
    for index, value in enumerate(trace, start=1):
        if value > threshold:
            return index, ordered
    return None, ordered


def quantile(values, q):
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(q * len(ordered))))
    return ordered[index]


def clean_sequences(*, count: int, seed_base: int):
    return [
        make_dataset(50, seed_base + index * 1_000_000)
        for index in range(count)
    ]


def calibrate_detector(templates, stats):
    clean_calibration = clean_sequences(count=20, seed_base=200_000_000)
    weak_shift_base = make_dataset(50, 221_000_000)
    # A declared tuning shift; held-out test uses different seeds.
    weak_shift = noise_inflation(
        weak_shift_base,
        seed=222_000_000,
        norm={
            probe: (
                0.0,
                stats[1],
            )
            for probe in BASE_FEATURES
        },
    )

    best = None
    for kappa in K_GRID:
        maxima = [
            max_cusum(
                dataset,
                templates,
                stats,
                kappa=kappa,
                seed=223_000_000 + index,
            )
            for index, dataset in enumerate(clean_calibration)
        ]
        threshold = quantile(maxima, 0.90)
        clean_alarm_rate = sum(value > threshold for value in maxima) / len(maxima)
        detected_at, _ = detection_point(
            weak_shift,
            templates,
            stats,
            kappa=kappa,
            threshold=threshold,
            seed=224_000_000,
        )
        delay = SEQUENCE_SIZE + 1 if detected_at is None else detected_at

        candidate = {
            "kappa": kappa,
            "threshold": threshold,
            "clean_alarm_rate": clean_alarm_rate,
            "tuning_delay": delay,
        }
        if clean_alarm_rate <= TARGET_CLEAN_FPR:
            if best is None or delay < best["tuning_delay"]:
                best = candidate

    if best is None:
        raise RuntimeError("no detector candidate met the clean false-alarm target")
    return best


def route_metrics(dataset, prepared, params, templates, stats, detector, *, seed):
    detected_at, ordered = detection_point(
        dataset,
        templates,
        stats,
        kappa=detector["kappa"],
        threshold=detector["threshold"],
        seed=seed,
    )
    predictions = predict_rows(ordered, prepared, params)
    stop = len(ordered) if detected_at is None else max(0, detected_at - 1)

    forced_correct = 0
    accepted_correct = 0
    accepted_errors = 0

    for index, ((_, _features), (true_label, prediction)) in enumerate(
        zip(ordered, predictions)
    ):
        correct = prediction == true_label
        forced_correct += int(correct)
        if index < stop:
            accepted_correct += int(correct)
            accepted_errors += int(not correct)

    total = len(ordered)
    forced_error = 1.0 - forced_correct / total
    residual_error = accepted_errors / total
    reduction = (
        1.0 - residual_error / forced_error
        if forced_error > 0.0
        else 0.0
    )

    return {
        "forced_accuracy": forced_correct / total,
        "detected_at": detected_at,
        "coverage": stop / total,
        "selective_accuracy": (
            accepted_correct / stop if stop else 1.0
        ),
        "unsafe_accepted_error_rate": residual_error,
        "error_exposure_reduction": reduction,
    }


@lru_cache(maxsize=1)
def residual_cusum_experiment():
    train = make_dataset(160, 230_000_000)
    validation = make_dataset(50, 231_000_000)
    templates_classifier, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates_classifier, norm, train_vectors)

    residual_templates = train_templates(samples=160)
    baseline = make_dataset(80, 232_000_000)
    stats = score_stats(baseline, residual_templates)
    detector = calibrate_detector(residual_templates, stats)

    clean_test_sequences = clean_sequences(count=20, seed_base=240_000_000)
    clean_false_alarms = 0
    for index, dataset in enumerate(clean_test_sequences):
        detected, _ = detection_point(
            dataset,
            residual_templates,
            stats,
            kappa=detector["kappa"],
            threshold=detector["threshold"],
            seed=260_000_000 + index,
        )
        clean_false_alarms += int(detected is not None)
    clean_test_fpr = clean_false_alarms / len(clean_test_sequences)

    base = make_dataset(50, 270_000_000)
    means = train_means(train)
    scenarios = {
        "clean": base,
        "common_mode_bias": common_mode_bias(base, seed=271_000_001),
        "noise_inflation": noise_inflation(
            base,
            seed=271_000_002,
            norm=norm,
        ),
        "probe_dropout": probe_dropout(
            base,
            seed=271_000_003,
            train_means=means,
        ),
        "combined_shift": combined_shift(
            base,
            seed=271_000_004,
            norm=norm,
            train_means=means,
        ),
    }

    results = {
        name: route_metrics(
            dataset,
            prepared,
            params,
            residual_templates,
            stats,
            detector,
            seed=272_000_000 + index,
        )
        for index, (name, dataset) in enumerate(scenarios.items())
    }

    noise = results["noise_inflation"]
    detector_effective = (
        clean_test_fpr <= 0.10
        and noise["detected_at"] is not None
        and noise["error_exposure_reduction"] > 0.50
    )

    return {
        "detector": detector,
        "score_mean": stats[0],
        "score_std": stats[1],
        "clean_test_fpr": clean_test_fpr,
        "results": results,
        "detector_effective": detector_effective,
    }


def format_markdown() -> str:
    result = residual_cusum_experiment()
    detector = result["detector"]
    lines = [
        "# CGD-SIM-018 template-residual CUSUM",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| scenario | forced accuracy | detected at sample | execution coverage | selective accuracy | unsafe accepted errors | error exposure reduction |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in (
        "clean",
        "common_mode_bias",
        "noise_inflation",
        "probe_dropout",
        "combined_shift",
    ):
        row = result["results"][name]
        detected = "none" if row["detected_at"] is None else str(row["detected_at"])
        lines.append(
            f"| {name} | {row['forced_accuracy']:.3f} | {detected} | "
            f"{row['coverage']:.3f} | {row['selective_accuracy']:.3f} | "
            f"{row['unsafe_accepted_error_rate']:.3f} | "
            f"{row['error_exposure_reduction']:.1%} |"
        )

    lines.extend(
        [
            "",
            f"- residual-energy clean mean: {result['score_mean']:.3f}",
            f"- residual-energy clean std: {result['score_std']:.3f}",
            f"- selected kappa: {detector['kappa']:.2f}",
            f"- selected threshold: {detector['threshold']:.3f}",
            f"- calibration clean alarm rate: {detector['clean_alarm_rate']:.3f}",
            f"- independent clean sequence false-alarm rate: {result['clean_test_fpr']:.3f}",
            f"- weak-noise residual CUSUM effective: {result['detector_effective']}",
            "",
            "Failure localization used by this generation:",
            "",
            "~~~text",
            "Global Regime Mixture",
            "    -> remove between-state structure with nearest clean template",
            "    -> monitor within-template residual energy",
            "    -> one-sided CUSUM on persistent excess surprise",
            "~~~",
            "",
            "This tests whether the SIM-017 failure came from monitoring the wrong "
            "state variable rather than from insufficient recursion depth.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
