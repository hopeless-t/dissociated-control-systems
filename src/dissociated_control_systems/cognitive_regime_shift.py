"""CGD-SIM-016: window-level regime-shift detection.

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
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset


PAIR_FEATURES = (
    ("self_reference_gap", "observer_disagreement"),
    ("self_reference_gap", "handoff_gap"),
    ("handoff_gap", "observer_disagreement"),
)


def shuffled(dataset, *, seed: int):
    rows = list(dataset)
    Random(seed).shuffle(rows)
    return rows


def chunks(dataset, size: int):
    return [
        dataset[index : index + size]
        for index in range(0, len(dataset), size)
        if len(dataset[index : index + size]) == size
    ]


def _variance(values):
    mean = fmean(values)
    return fmean((value - mean) ** 2 for value in values) + 1e-9


def _corr(xs, ys):
    mx = fmean(xs)
    my = fmean(ys)
    vx = fmean((x - mx) ** 2 for x in xs) + 1e-9
    vy = fmean((y - my) ** 2 for y in ys) + 1e-9
    cov = fmean((x - mx) * (y - my) for x, y in zip(xs, ys))
    return cov / sqrt(vx * vy)


def regime_reference(dataset):
    means = {}
    variances = {}
    for feature in BASE_FEATURES:
        values = [features[feature] for _, features in dataset]
        means[feature] = fmean(values)
        variances[feature] = _variance(values)

    correlations = {}
    for left, right in PAIR_FEATURES:
        xs = [features[left] for _, features in dataset]
        ys = [features[right] for _, features in dataset]
        correlations[(left, right)] = _corr(xs, ys)

    return {
        "means": means,
        "variances": variances,
        "correlations": correlations,
    }


def window_score(window, reference):
    n = len(window)

    if any(
        features.get(key, 0.0) > 0.5
        for _, features in window
        for key in MISSING_KEYS
    ):
        return 1_000.0

    mean_scores = []
    variance_scores = []
    for feature in BASE_FEATURES:
        values = [features[feature] for _, features in window]
        std = sqrt(reference["variances"][feature])
        mean_scores.append(
            abs(fmean(values) - reference["means"][feature])
            / (std / sqrt(n))
        )
        window_var = _variance(values)
        variance_scores.append(
            abs(log(window_var / reference["variances"][feature])) * sqrt(n / 2.0)
        )

    correlation_scores = []
    for left, right in PAIR_FEATURES:
        xs = [features[left] for _, features in window]
        ys = [features[right] for _, features in window]
        observed = _corr(xs, ys)
        baseline = reference["correlations"][(left, right)]
        correlation_scores.append(abs(observed - baseline) * sqrt(n))

    return max(
        max(mean_scores),
        max(variance_scores),
        max(correlation_scores),
    )


def quantile(values, q):
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(q * len(ordered))))
    return ordered[index]


def calibrate_threshold(reference, *, window_size: int):
    scores = []
    for block in range(4):
        clean = shuffled(
            make_dataset(70, 110_000_000 + block * 1_000_000),
            seed=114_000_000 + block,
        )
        scores.extend(
            window_score(window, reference)
            for window in chunks(clean, window_size)
        )
    return quantile(scores, 0.98)


def route_windows(dataset, prepared, params, reference, threshold, *, window_size, seed):
    ordered = shuffled(dataset, seed=seed)
    predictions = predict_rows(ordered, prepared, params)
    prediction_by_index = list(zip(ordered, predictions))

    flagged_samples = 0
    accepted = 0
    accepted_correct = 0
    unsafe_accepted_errors = 0
    forced_correct = 0
    flagged_windows = 0
    total_windows = 0

    for start in range(0, len(prediction_by_index), window_size):
        group = prediction_by_index[start : start + window_size]
        if len(group) < window_size:
            continue
        window = [item[0] for item in group]
        is_shift = window_score(window, reference) > threshold
        total_windows += 1
        flagged_windows += int(is_shift)

        for (_, _features), (true_label, prediction) in group:
            correct = prediction == true_label
            forced_correct += int(correct)
            if is_shift:
                flagged_samples += 1
            else:
                accepted += 1
                accepted_correct += int(correct)
                unsafe_accepted_errors += int(not correct)

    total = accepted + flagged_samples
    forced_error = 1.0 - (forced_correct / total)
    residual = unsafe_accepted_errors / total
    exposure_reduction = (
        1.0 - residual / forced_error
        if forced_error > 0.0
        else 0.0
    )

    return {
        "forced_accuracy": forced_correct / total,
        "window_flag_rate": flagged_windows / total_windows,
        "coverage": accepted / total,
        "selective_accuracy": (
            accepted_correct / accepted if accepted else 1.0
        ),
        "unsafe_accepted_error_rate": residual,
        "error_exposure_reduction": exposure_reduction,
    }


@lru_cache(maxsize=1)
def regime_shift_experiment():
    train = make_dataset(160, 120_000_000)
    validation = make_dataset(50, 121_000_000)
    test = make_dataset(100, 122_000_000)

    templates, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates, norm, train_vectors)
    reference = regime_reference(train)
    means = train_means(train)
    window_size = 64
    threshold = calibrate_threshold(reference, window_size=window_size)

    scenarios = {
        "clean": test,
        "common_mode_bias": common_mode_bias(test, seed=123_000_001),
        "noise_inflation": noise_inflation(
            test,
            seed=123_000_002,
            norm=norm,
        ),
        "probe_dropout": probe_dropout(
            test,
            seed=123_000_003,
            train_means=means,
        ),
        "combined_shift": combined_shift(
            test,
            seed=123_000_004,
            norm=norm,
            train_means=means,
        ),
    }

    results = {
        name: route_windows(
            dataset,
            prepared,
            params,
            reference,
            threshold,
            window_size=window_size,
            seed=124_000_000 + index,
        )
        for index, (name, dataset) in enumerate(scenarios.items())
    }

    clean_fpr = results["clean"]["window_flag_rate"]
    target_names = ("common_mode_bias", "noise_inflation", "combined_shift")
    minimum_reduction = min(
        results[name]["error_exposure_reduction"]
        for name in target_names
    )
    regime_gate_effective = (
        clean_fpr < 0.05
        and minimum_reduction > 0.50
    )

    return {
        "threshold": threshold,
        "window_size": window_size,
        "params": params,
        "results": results,
        "clean_window_false_alarm": clean_fpr,
        "minimum_target_error_exposure_reduction": minimum_reduction,
        "regime_gate_effective": regime_gate_effective,
    }


def format_markdown() -> str:
    result = regime_shift_experiment()
    lines = [
        "# CGD-SIM-016 window-level regime-shift detection",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| scenario | forced accuracy | window flag rate | execution coverage | selective accuracy | unsafe accepted errors | error exposure reduction |",
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
        lines.append(
            f"| {name} | {row['forced_accuracy']:.3f} | "
            f"{row['window_flag_rate']:.3f} | {row['coverage']:.3f} | "
            f"{row['selective_accuracy']:.3f} | "
            f"{row['unsafe_accepted_error_rate']:.3f} | "
            f"{row['error_exposure_reduction']:.1%} |"
        )

    lines.extend(
        [
            "",
            f"- window size: {result['window_size']}",
            f"- clean-calibrated regime threshold: {result['threshold']:.3f}",
            f"- clean window false-alarm rate: {result['clean_window_false_alarm']:.3f}",
            (
                "- minimum error-exposure reduction across common-bias, noise, combined: "
                f"{result['minimum_target_error_exposure_reduction']:.1%}"
            ),
            f"- regime gate effective: {result['regime_gate_effective']}",
            "",
            "Why a second detector layer exists:",
            "",
            "~~~text",
            "Plausible Individual Observation != Stable Population Regime",
            "~~~",
            "",
            "SIM-015 catches explicit missingness well but misses shifts whose individual "
            "samples remain locally plausible. SIM-016 treats distributional drift as a "
            "window-level property using mean, variance and selected correlation changes.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
