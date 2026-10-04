"""CGD-SIM-019: quarantine, recalibrate, validate, restore.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache

from .cognitive_fixed_point import evaluate_block, select_params
from .cognitive_ood_challenge import combined_shift, train_means
from .cognitive_temporal_frontier import BASE_FEATURES, make_dataset

CALIBRATION_SIZES = (5, 10, 20, 40, 80, 160)
RESTORE_VALIDATION_ACCURACY = 0.90


def shifted_dataset(
    *,
    samples: int,
    clean_seed: int,
    shift_seed: int,
    clean_norm,
    clean_means,
):
    clean = make_dataset(samples, clean_seed)
    return combined_shift(
        clean,
        seed=shift_seed,
        norm=clean_norm,
        train_means=clean_means,
    )


@lru_cache(maxsize=1)
def restoration_experiment():
    clean_train = make_dataset(160, 300_000_000)
    clean_validation = make_dataset(50, 301_000_000)

    clean_templates, clean_norm, clean_vectors, clean_params = select_params(
        clean_train,
        clean_validation,
        BASE_FEATURES,
    )
    clean_prepared = (clean_templates, clean_norm, clean_vectors)
    clean_means = train_means(clean_train)

    shifted_validation = shifted_dataset(
        samples=50,
        clean_seed=302_000_000,
        shift_seed=303_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )
    shifted_test = shifted_dataset(
        samples=100,
        clean_seed=304_000_000,
        shift_seed=305_000_000,
        clean_norm=clean_norm,
        clean_means=clean_means,
    )

    frozen_validation = evaluate_block(
        shifted_validation,
        BASE_FEATURES,
        clean_prepared,
        clean_params,
    )
    frozen_test = evaluate_block(
        shifted_test,
        BASE_FEATURES,
        clean_prepared,
        clean_params,
    )

    rows = []
    for index, size in enumerate(CALIBRATION_SIZES):
        shifted_train = shifted_dataset(
            samples=size,
            clean_seed=310_000_000 + index * 2_000_000,
            shift_seed=311_000_000 + index * 2_000_000,
            clean_norm=clean_norm,
            clean_means=clean_means,
        )
        templates, norm, vectors, params = select_params(
            shifted_train,
            shifted_validation,
            BASE_FEATURES,
        )
        prepared = (templates, norm, vectors)
        validation_result = evaluate_block(
            shifted_validation,
            BASE_FEATURES,
            prepared,
            params,
        )
        test_result = evaluate_block(
            shifted_test,
            BASE_FEATURES,
            prepared,
            params,
        )
        authorized = (
            validation_result["ensemble_accuracy"]
            >= RESTORE_VALIDATION_ACCURACY
        )
        rows.append(
            {
                "samples_per_hypothesis": size,
                "total_calibration_samples": size * 16,
                "validation_accuracy": validation_result["ensemble_accuracy"],
                "test_accuracy": test_result["ensemble_accuracy"],
                "test_oracle_gap": test_result["residual_oracle_gap"],
                "k": params[0],
                "bayes_weight": params[1],
                "restore_authorized": authorized,
                "safe_on_test": (
                    test_result["ensemble_accuracy"]
                    >= RESTORE_VALIDATION_ACCURACY
                ),
            }
        )

    authorized_rows = [row for row in rows if row["restore_authorized"]]
    first_authorized = authorized_rows[0] if authorized_rows else None
    false_restore = any(
        row["restore_authorized"] and not row["safe_on_test"]
        for row in rows
    )

    return {
        "restore_threshold": RESTORE_VALIDATION_ACCURACY,
        "frozen_validation_accuracy": frozen_validation["ensemble_accuracy"],
        "frozen_test_accuracy": frozen_test["ensemble_accuracy"],
        "rows": rows,
        "first_authorized": first_authorized,
        "false_restore": false_restore,
    }


def format_markdown() -> str:
    result = restoration_experiment()
    lines = [
        "# CGD-SIM-019 quarantine -> recalibrate -> validate -> restore",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- authority restoration validation threshold: {result['restore_threshold']:.2f}",
        f"- frozen clean model on shifted validation: {result['frozen_validation_accuracy']:.3f}",
        f"- frozen clean model on shifted test: {result['frozen_test_accuracy']:.3f}",
        "",
        "| shifted calibration / hypothesis | total calibration | validation accuracy | held-out test accuracy | test oracle gap | k | Bayes weight | restore authorized |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['samples_per_hypothesis']} | "
            f"{row['total_calibration_samples']} | "
            f"{row['validation_accuracy']:.3f} | "
            f"{row['test_accuracy']:.3f} | "
            f"{row['test_oracle_gap']:.4f} | "
            f"{row['k']} | {row['bayes_weight']:.2f} | "
            f"{row['restore_authorized']} |"
        )

    first = result["first_authorized"]
    if first is None:
        restoration = "none"
    else:
        restoration = (
            f"{first['samples_per_hypothesis']} samples/hypothesis "
            f"({first['total_calibration_samples']} total)"
        )

    lines.extend(
        [
            "",
            f"- first validation-authorized restoration point: {restoration}",
            f"- any false restoration on held-out test: {result['false_restore']}",
            "",
            "Lifecycle under test:",
            "",
            "~~~text",
            "world-model mismatch",
            "  -> lower normal execution authority",
            "  -> quarantine current regime",
            "  -> acquire verified regime-specific evidence",
            "  -> train candidate regime model",
            "  -> validate on independent shifted evidence",
            "  -> restore authority only if validation contract passes",
            "~~~",
            "",
            "A failed restoration is not permission to lower the threshold after seeing "
            "the held-out test. It means the representation or evidence is still "
            "insufficient and the loop must remain fail-closed.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
