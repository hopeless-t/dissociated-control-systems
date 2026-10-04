"""CGD-SIM-015: OOD detection and authority routing.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from statistics import fmean

from .cognitive_fixed_point import select_params
from .cognitive_ood_challenge import (
    combined_shift,
    common_mode_bias,
    noise_inflation,
    probe_dropout,
    train_means,
)
from .cognitive_temporal_frontier import (
    BASE_FEATURES,
    make_dataset,
    precompute,
)


MISSING_KEYS = (
    "_missing_observer_disagreement",
    "_missing_self_reference_gap",
    "_missing_handoff_gap",
)


def clean_global_stats(dataset):
    stats = {}
    for feature in BASE_FEATURES:
        values = [features[feature] for _, features in dataset]
        mean = fmean(values)
        variance = fmean((value - mean) ** 2 for value in values) + 1e-9
        stats[feature] = (mean, variance ** 0.5)
    return stats


def ood_score(features, stats):
    zmax = max(
        abs(features[feature] - stats[feature][0]) / stats[feature][1]
        for feature in BASE_FEATURES
    )
    if any(features.get(key, 0.0) > 0.5 for key in MISSING_KEYS):
        return max(zmax, 1_000.0)
    return zmax


def quantile(values, q):
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(q * len(ordered))))
    return ordered[index]


def select_threshold(clean_validation, stats, *, target_quantile=0.985):
    return quantile(
        [ood_score(features, stats) for _, features in clean_validation],
        target_quantile,
    )


def predict_rows(dataset, prepared, params):
    templates, norm, train_vectors = prepared
    data = precompute(
        dataset,
        BASE_FEATURES,
        templates,
        norm,
        train_vectors,
    )
    predictions = []
    for true_label, bp, knn_by_k in data:
        kp = knn_by_k[params[0]]
        ep = {
            label: (
                params[1] * bp[label]
                + (1.0 - params[1]) * kp[label]
            )
            for label in bp
        }
        prediction = max(ep, key=ep.get)
        predictions.append((true_label, prediction))
    return predictions


def route_metrics(dataset, prepared, params, stats, threshold):
    predictions = predict_rows(dataset, prepared, params)
    accepted = 0
    accepted_correct = 0
    flagged = 0
    unsafe_accepted_errors = 0
    forced_correct = 0

    for ((_, features), (true_label, prediction)) in zip(dataset, predictions):
        correct = prediction == true_label
        forced_correct += int(correct)
        is_ood = ood_score(features, stats) > threshold
        if is_ood:
            flagged += 1
            continue
        accepted += 1
        accepted_correct += int(correct)
        unsafe_accepted_errors += int(not correct)

    total = len(dataset)
    return {
        "forced_accuracy": forced_correct / total,
        "flag_rate": flagged / total,
        "coverage": accepted / total,
        "selective_accuracy": (
            accepted_correct / accepted if accepted else 1.0
        ),
        "unsafe_accepted_error_rate": unsafe_accepted_errors / total,
    }


@lru_cache(maxsize=1)
def authority_routing_experiment():
    train = make_dataset(160, 100_000_000)
    validation = make_dataset(80, 101_000_000)
    test = make_dataset(100, 102_000_000)

    templates, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates, norm, train_vectors)
    stats = clean_global_stats(train)
    threshold = select_threshold(validation, stats)
    means = train_means(train)

    scenarios = {
        "clean": test,
        "common_mode_bias": common_mode_bias(test, seed=103_000_001),
        "noise_inflation": noise_inflation(
            test,
            seed=103_000_002,
            norm=norm,
        ),
        "probe_dropout": probe_dropout(
            test,
            seed=103_000_003,
            train_means=means,
        ),
        "combined_shift": combined_shift(
            test,
            seed=103_000_004,
            norm=norm,
            train_means=means,
        ),
    }

    results = {
        name: route_metrics(
            dataset,
            prepared,
            params,
            stats,
            threshold,
        )
        for name, dataset in scenarios.items()
    }

    clean_false_alarm = results["clean"]["flag_rate"]
    combined = results["combined_shift"]
    forced_error = 1.0 - combined["forced_accuracy"]
    residual_executed_error = combined["unsafe_accepted_error_rate"]
    error_exposure_reduction = (
        1.0 - residual_executed_error / forced_error
        if forced_error > 0.0
        else 0.0
    )

    authority_gate_effective = (
        clean_false_alarm < 0.03
        and error_exposure_reduction > 0.50
    )

    return {
        "threshold": threshold,
        "params": params,
        "results": results,
        "clean_false_alarm": clean_false_alarm,
        "combined_error_exposure_reduction": error_exposure_reduction,
        "authority_gate_effective": authority_gate_effective,
    }


def format_markdown() -> str:
    result = authority_routing_experiment()
    lines = [
        "# CGD-SIM-015 OOD detection and authority routing",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| scenario | forced accuracy | flag rate | execution coverage | selective accuracy | unsafe accepted errors |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
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
            f"{row['flag_rate']:.3f} | {row['coverage']:.3f} | "
            f"{row['selective_accuracy']:.3f} | "
            f"{row['unsafe_accepted_error_rate']:.3f} |"
        )

    lines.extend(
        [
            "",
            f"- clean-calibrated OOD threshold: {result['threshold']:.3f}",
            f"- clean false-alarm rate: {result['clean_false_alarm']:.3f}",
            (
                "- combined-shift executed-error exposure reduction: "
                f"{result['combined_error_exposure_reduction']:.1%}"
            ),
            f"- authority gate effective: {result['authority_gate_effective']}",
            "",
            "Routing rule:",
            "",
            "~~~text",
            "if world_model_mismatch:",
            "    do not silently force a normal-path decision",
            "    lower execution authority",
            "    request external evidence / review / recalibration",
            "~~~",
            "",
            "Important representation rule:",
            "",
            "~~~text",
            "Missing Observation != Observation At Mean",
            "~~~",
            "",
            "SIM-014 showed catastrophic accuracy loss under world-model shift. "
            "SIM-015 tests whether the harness can convert that hidden failure into "
            "an explicit bounded-coverage state instead of confidently continuing.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
