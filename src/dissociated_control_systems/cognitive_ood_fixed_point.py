"""CGD-SIM-019: replicated OOD authority-plane audit.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from statistics import fmean

from .cognitive_energy_shift import (
    SAMPLES_PER_HYPOTHESIS,
    baseline_energy,
    calibrate_threshold,
    routed_metrics,
)
from .cognitive_fixed_point import select_params
from .cognitive_ood_challenge import (
    combined_shift,
    common_mode_bias,
    noise_inflation,
    probe_dropout,
    train_means,
)
from .cognitive_regime_shift import regime_reference
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset


@lru_cache(maxsize=1)
def replicated_ood_audit():
    train = make_dataset(160, 330_000_000)
    validation = make_dataset(50, 331_000_000)
    templates, norm, train_vectors, params = select_params(
        train,
        validation,
        BASE_FEATURES,
    )
    prepared = (templates, norm, train_vectors)
    reference = regime_reference(train)
    clean_energy = baseline_energy(train, reference)
    means = train_means(train)
    threshold, _ = calibrate_threshold(reference, clean_energy)

    rows = []
    for block in range(5):
        base_seed = 360_000_000 + block * 2_000_000
        base = make_dataset(SAMPLES_PER_HYPOTHESIS, base_seed)
        scenarios = {
            "clean": base,
            "common_mode_bias": common_mode_bias(
                base,
                seed=base_seed + 100_001,
            ),
            "noise_inflation": noise_inflation(
                base,
                seed=base_seed + 100_002,
                norm=norm,
            ),
            "probe_dropout": probe_dropout(
                base,
                seed=base_seed + 100_003,
                train_means=means,
            ),
            "combined_shift": combined_shift(
                base,
                seed=base_seed + 100_004,
                norm=norm,
                train_means=means,
            ),
        }
        metrics = {
            name: routed_metrics(
                dataset,
                prepared,
                params,
                reference,
                clean_energy,
                threshold,
                seed=base_seed + 200_000 + index,
            )
            for index, (name, dataset) in enumerate(scenarios.items())
        }
        rows.append(
            {
                "block": block,
                "clean_false_alarm": float(
                    metrics["clean"]["detected_at"] is not None
                ),
                "clean_coverage": metrics["clean"]["coverage"],
                "common_reduction": metrics["common_mode_bias"]["error_exposure_reduction"],
                "noise_reduction": metrics["noise_inflation"]["error_exposure_reduction"],
                "noise_detected_at": metrics["noise_inflation"]["detected_at"],
                "dropout_reduction": metrics["probe_dropout"]["error_exposure_reduction"],
                "combined_reduction": metrics["combined_shift"]["error_exposure_reduction"],
            }
        )

    clean_fpr = fmean(row["clean_false_alarm"] for row in rows)
    mean_noise_reduction = fmean(row["noise_reduction"] for row in rows)
    min_noise_reduction = min(row["noise_reduction"] for row in rows)
    mean_common_reduction = fmean(row["common_reduction"] for row in rows)
    mean_combined_reduction = fmean(row["combined_reduction"] for row in rows)
    max_noise_latency = max(
        (
            row["noise_detected_at"]
            if row["noise_detected_at"] is not None
            else SAMPLES_PER_HYPOTHESIS * 16
        )
        for row in rows
    )

    robust = (
        clean_fpr <= 0.10
        and min_noise_reduction > 0.50
        and mean_common_reduction > 0.80
        and mean_combined_reduction > 0.80
    )

    return {
        "rows": rows,
        "threshold": threshold,
        "params": params,
        "clean_fpr": clean_fpr,
        "mean_noise_reduction": mean_noise_reduction,
        "min_noise_reduction": min_noise_reduction,
        "mean_common_reduction": mean_common_reduction,
        "mean_combined_reduction": mean_combined_reduction,
        "max_noise_latency": max_noise_latency,
        "robust": robust,
    }


def format_markdown() -> str:
    result = replicated_ood_audit()
    lines = [
        "# CGD-SIM-019 replicated OOD authority-plane audit",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| block | clean false alarm | common reduction | noise reduction | noise detected at | dropout reduction | combined reduction |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        detected = (
            "none"
            if row["noise_detected_at"] is None
            else str(row["noise_detected_at"])
        )
        lines.append(
            f"| {row['block']} | {row['clean_false_alarm']:.0f} | "
            f"{row['common_reduction']:.1%} | {row['noise_reduction']:.1%} | "
            f"{detected} | {row['dropout_reduction']:.1%} | "
            f"{row['combined_reduction']:.1%} |"
        )

    lines.extend(
        [
            "",
            f"- frozen threshold: {result['threshold']:.3f}",
            f"- frozen classifier params: k={result['params'][0]}, Bayes weight={result['params'][1]:.2f}",
            f"- independent clean block false-alarm rate: {result['clean_fpr']:.3f}",
            f"- mean noise-shift error-exposure reduction: {result['mean_noise_reduction']:.1%}",
            f"- minimum noise-shift error-exposure reduction: {result['min_noise_reduction']:.1%}",
            f"- mean common-bias error-exposure reduction: {result['mean_common_reduction']:.1%}",
            f"- mean combined-shift error-exposure reduction: {result['mean_combined_reduction']:.1%}",
            f"- worst noise detection latency: {result['max_noise_latency']} samples",
            f"- replicated OOD authority plane robust: {result['robust']}",
            "",
            "Interpretation:",
            "",
            "SIM-013 fixed the clean-world internal loop. SIM-014 broke that fixed "
            "point under world-model shift. SIM-015 through SIM-018 built an authority "
            "boundary around that failure. SIM-019 asks whether the boundary survives "
            "independent shifted worlds without retuning.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
