"""CGD-SIM-018: multivariate cumulative-energy shift detector.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

from .cognitive_fixed_point import select_params
from .cognitive_ood_challenge import (
    combined_shift,
    common_mode_bias,
    noise_inflation,
    probe_dropout,
    train_means,
)
from .cognitive_ood_routing import MISSING_KEYS, predict_rows
from .cognitive_regime_shift import regime_reference
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset


CHECKPOINT = 64
SAMPLES_PER_HYPOTHESIS = 50


def shuffled(dataset, *, seed: int):
    rows = list(dataset)
    Random(seed).shuffle(rows)
    return rows


def checkpoints(total):
    points = list(range(CHECKPOINT, total + 1, CHECKPOINT))
    if not points or points[-1] != total:
        points.append(total)
    return points


def standardized_energy(features, reference):
    return fmean(
        (
            (features[feature] - reference["means"][feature])
            / sqrt(reference["variances"][feature])
        ) ** 2
        for feature in BASE_FEATURES
    )


def baseline_energy(dataset, reference):
    return fmean(
        standardized_energy(features, reference)
        for _, features in dataset
    )


def cumulative_score(rows, reference, clean_energy):
    n = len(rows)
    if any(
        features.get(key, 0.0) > 0.5
        for _, features in rows
        for key in MISSING_KEYS
    ):
        return 1_000.0

    observed_energy = fmean(
        standardized_energy(features, reference)
        for _, features in rows
    )
    energy_score = (
        abs(observed_energy - clean_energy)
        * sqrt(n * len(BASE_FEATURES))
    )

    mean_components = []
    for feature in BASE_FEATURES:
        values = [features[feature] for _, features in rows]
        std = sqrt(reference["variances"][feature])
        mean_components.append(
            (fmean(values) - reference["means"][feature])
            / (std / sqrt(n))
        )
    mean_vector_score = (
        sum(component * component for component in mean_components)
        / len(mean_components)
    ) ** 0.5

    return max(energy_score, mean_vector_score)


def max_sequence_score(dataset, reference, clean_energy, *, seed):
    rows = shuffled(dataset, seed=seed)
    return max(
        cumulative_score(rows[:point], reference, clean_energy)
        for point in checkpoints(len(rows))
    )


def calibrate_threshold(reference, clean_energy):
    maxima = []
    for block in range(20):
        clean = make_dataset(
            SAMPLES_PER_HYPOTHESIS,
            190_000_000 + block * 1_000_000,
        )
        maxima.append(
            max_sequence_score(
                clean,
                reference,
                clean_energy,
                seed=210_000_000 + block,
            )
        )
    # Strictly above the observed clean calibration maximum.
    return max(maxima) * 1.02, maxima


def detection_point(dataset, reference, clean_energy, threshold, *, seed):
    rows = shuffled(dataset, seed=seed)
    for point in checkpoints(len(rows)):
        if cumulative_score(
            rows[:point],
            reference,
            clean_energy,
        ) > threshold:
            return point, rows
    return None, rows


def routed_metrics(dataset, prepared, params, reference, clean_energy, threshold, *, seed):
    detected_at, ordered = detection_point(
        dataset,
        reference,
        clean_energy,
        threshold,
        seed=seed,
    )
    predictions = predict_rows(ordered, prepared, params)
    stop = len(ordered) if detected_at is None else detected_at

    forced_correct = 0
    accepted_correct = 0
    unsafe_accepted_errors = 0
    for index, ((_, _features), (true_label, prediction)) in enumerate(
        zip(ordered, predictions)
    ):
        correct = prediction == true_label
        forced_correct += int(correct)
        if index < stop:
            accepted_correct += int(correct)
            unsafe_accepted_errors += int(not correct)

    total = len(ordered)
    forced_error = 1.0 - forced_correct / total
    residual = unsafe_accepted_errors / total
    reduction = (
        1.0 - residual / forced_error
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
        "unsafe_accepted_error_rate": residual,
        "error_exposure_reduction": reduction,
    }


@lru_cache(maxsize=1)
def energy_experiment():
    train = make_dataset(160, 230_000_000)
    validation = make_dataset(50, 231_000_000)
    templates, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates, norm, train_vectors)
    reference = regime_reference(train)
    clean_energy = baseline_energy(train, reference)
    means = train_means(train)
    threshold, calibration_maxima = calibrate_threshold(
        reference,
        clean_energy,
    )

    clean_trials = 20
    clean_false_alarms = 0
    for block in range(clean_trials):
        clean = make_dataset(
            SAMPLES_PER_HYPOTHESIS,
            250_000_000 + block * 1_000_000,
        )
        detected, _ = detection_point(
            clean,
            reference,
            clean_energy,
            threshold,
            seed=270_000_000 + block,
        )
        clean_false_alarms += int(detected is not None)
    clean_sequence_fpr = clean_false_alarms / clean_trials

    base = make_dataset(SAMPLES_PER_HYPOTHESIS, 300_000_000)
    scenarios = {
        "clean": base,
        "common_mode_bias": common_mode_bias(base, seed=301_000_001),
        "noise_inflation": noise_inflation(
            base,
            seed=301_000_002,
            norm=norm,
        ),
        "probe_dropout": probe_dropout(
            base,
            seed=301_000_003,
            train_means=means,
        ),
        "combined_shift": combined_shift(
            base,
            seed=301_000_004,
            norm=norm,
            train_means=means,
        ),
    }
    results = {
        name: routed_metrics(
            dataset,
            prepared,
            params,
            reference,
            clean_energy,
            threshold,
            seed=302_000_000 + index,
        )
        for index, (name, dataset) in enumerate(scenarios.items())
    }

    noise = results["noise_inflation"]
    energy_gate_effective = (
        clean_sequence_fpr <= 0.10
        and noise["detected_at"] is not None
        and noise["error_exposure_reduction"] > 0.50
    )

    return {
        "clean_energy": clean_energy,
        "threshold": threshold,
        "calibration_max_mean": fmean(calibration_maxima),
        "clean_sequence_fpr": clean_sequence_fpr,
        "results": results,
        "energy_gate_effective": energy_gate_effective,
    }


def format_markdown() -> str:
    result = energy_experiment()
    lines = [
        "# CGD-SIM-018 multivariate cumulative-energy detector",
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
            f"- clean standardized-energy baseline: {result['clean_energy']:.3f}",
            f"- sequence threshold: {result['threshold']:.3f}",
            f"- mean clean calibration max-score: {result['calibration_max_mean']:.3f}",
            f"- independent clean sequence false-alarm rate: {result['clean_sequence_fpr']:.3f}",
            f"- multivariate energy gate effective for weak noise shift: {result['energy_gate_effective']}",
            "",
            "New failure-localization result:",
            "",
            "~~~text",
            "Distributed Weak Shift != Max Single-Channel Deviation",
            "~~~",
            "",
            "The detector sums standardized squared evidence across all base probes, "
            "so small persistent variance inflation can accumulate across channels "
            "instead of competing to be the single largest deviation.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
