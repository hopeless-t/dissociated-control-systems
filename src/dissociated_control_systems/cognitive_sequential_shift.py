"""CGD-SIM-017: sequential weak-shift accumulation.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import log, sqrt
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
from .cognitive_regime_shift import _variance, regime_reference
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset


CHECKPOINT = 64
SAMPLES_PER_HYPOTHESIS = 50


def shuffled(dataset, *, seed: int):
    rows = list(dataset)
    Random(seed).shuffle(rows)
    return rows


def prefix_score(rows, reference):
    n = len(rows)
    if any(
        features.get(key, 0.0) > 0.5
        for _, features in rows
        for key in MISSING_KEYS
    ):
        return 1_000.0

    mean_scores = []
    variance_scores = []
    for feature in BASE_FEATURES:
        values = [features[feature] for _, features in rows]
        std = sqrt(reference["variances"][feature])
        mean_scores.append(
            abs(fmean(values) - reference["means"][feature])
            / (std / sqrt(n))
        )
        observed_var = _variance(values)
        variance_scores.append(
            abs(log(observed_var / reference["variances"][feature]))
            * sqrt(n / 2.0)
        )
    return max(max(mean_scores), max(variance_scores))


def prefix_checkpoints(total):
    points = list(range(CHECKPOINT, total + 1, CHECKPOINT))
    if not points or points[-1] != total:
        points.append(total)
    return points


def max_sequence_score(dataset, reference, *, seed):
    rows = shuffled(dataset, seed=seed)
    return max(
        prefix_score(rows[:point], reference)
        for point in prefix_checkpoints(len(rows))
    )


def quantile(values, q):
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(q * len(ordered))))
    return ordered[index]


def calibrate_sequence_threshold(reference):
    maxima = []
    for block in range(12):
        clean = make_dataset(
            SAMPLES_PER_HYPOTHESIS,
            130_000_000 + block * 1_000_000,
        )
        maxima.append(
            max_sequence_score(
                clean,
                reference,
                seed=142_000_000 + block,
            )
        )
    return quantile(maxima, 0.92), maxima


def detection_point(dataset, reference, threshold, *, seed):
    rows = shuffled(dataset, seed=seed)
    for point in prefix_checkpoints(len(rows)):
        if prefix_score(rows[:point], reference) > threshold:
            return point, rows
    return None, rows


def routed_sequence_metrics(dataset, prepared, params, reference, threshold, *, seed):
    detected_at, ordered = detection_point(
        dataset,
        reference,
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
    accepted = stop
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
        "coverage": accepted / total,
        "selective_accuracy": (
            accepted_correct / accepted if accepted else 1.0
        ),
        "unsafe_accepted_error_rate": residual,
        "error_exposure_reduction": reduction,
    }


@lru_cache(maxsize=1)
def sequential_experiment():
    train = make_dataset(160, 150_000_000)
    validation = make_dataset(50, 151_000_000)
    templates, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates, norm, train_vectors)
    reference = regime_reference(train)
    means = train_means(train)

    threshold, calibration_maxima = calibrate_sequence_threshold(reference)

    clean_false_alarms = 0
    clean_trials = 12
    for block in range(clean_trials):
        clean = make_dataset(
            SAMPLES_PER_HYPOTHESIS,
            163_000_000 + block * 1_000_000,
        )
        detected, _ = detection_point(
            clean,
            reference,
            threshold,
            seed=175_000_000 + block,
        )
        clean_false_alarms += int(detected is not None)
    clean_sequence_fpr = clean_false_alarms / clean_trials

    base = make_dataset(SAMPLES_PER_HYPOTHESIS, 180_000_000)
    scenarios = {
        "clean": base,
        "common_mode_bias": common_mode_bias(base, seed=181_000_001),
        "noise_inflation": noise_inflation(
            base,
            seed=181_000_002,
            norm=norm,
        ),
        "probe_dropout": probe_dropout(
            base,
            seed=181_000_003,
            train_means=means,
        ),
        "combined_shift": combined_shift(
            base,
            seed=181_000_004,
            norm=norm,
            train_means=means,
        ),
    }

    results = {
        name: routed_sequence_metrics(
            dataset,
            prepared,
            params,
            reference,
            threshold,
            seed=182_000_000 + index,
        )
        for index, (name, dataset) in enumerate(scenarios.items())
    }

    noise = results["noise_inflation"]
    sequential_gate_effective = (
        clean_sequence_fpr <= 0.10
        and noise["detected_at"] is not None
        and noise["error_exposure_reduction"] > 0.50
    )

    return {
        "threshold": threshold,
        "calibration_maxima_mean": fmean(calibration_maxima),
        "clean_sequence_fpr": clean_sequence_fpr,
        "results": results,
        "sequential_gate_effective": sequential_gate_effective,
    }


def format_markdown() -> str:
    result = sequential_experiment()
    lines = [
        "# CGD-SIM-017 sequential weak-shift accumulation",
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
            f"- checkpoint interval: {CHECKPOINT}",
            f"- sequence threshold: {result['threshold']:.3f}",
            f"- mean clean calibration max-score: {result['calibration_maxima_mean']:.3f}",
            f"- independent clean sequence false-alarm rate: {result['clean_sequence_fpr']:.3f}",
            f"- sequential gate effective for weak noise shift: {result['sequential_gate_effective']}",
            "",
            "New control distinction:",
            "",
            "~~~text",
            "Weak Persistent Shift != Benign Local Noise",
            "~~~",
            "",
            "SIM-016 showed that a 64-sample window can miss mild variance inflation. "
            "SIM-017 accumulates evidence across checkpoints and measures the cost of "
            "detection delay directly as exposed wrong executions before authority drops.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
