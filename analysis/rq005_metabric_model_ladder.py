"""RQ-005 METABRIC block-held-out model ladder.

This script uses only the patient-level clinical CSV and tests how far a small
retrospective tumor/clinical baseline can separate strict LTS/STS discovery
labels. COHORT is held out as a block.

It is intentionally not a causal treatment-effect model and not a clinical
prognosis tool.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean

from dissociated_control_systems.survivor_baseline import (
    binary_auc,
    binary_log_loss,
    fit_logistic,
    fixed_horizon_survivor_label,
    predict_logistic,
)


SUBTYPES = ("LumA", "LumB", "Basal", "Her2", "claudin-low", "Normal")

MODELS = {
    "intercept": (),
    "age": ("age",),
    "tumor_basic": (
        "age",
        "npi",
        "nodes",
        "er_negative",
        "her2_gain",
        *(f"subtype:{name}" for name in SUBTYPES),
    ),
    "treatment_context": ("age", "chemotherapy", "hormone", "radiotherapy"),
    "combined": (
        "age",
        "npi",
        "nodes",
        "er_negative",
        "her2_gain",
        "chemotherapy",
        "hormone",
        "radiotherapy",
        *(f"subtype:{name}" for name in SUBTYPES),
    ),
}


def as_float(value: str) -> float | None:
    try:
        return float(value) if value.strip() else None
    except ValueError:
        return None


def feature(row: dict[str, str], name: str) -> float | None:
    if name == "age":
        return as_float(row.get("AGE_AT_DIAGNOSIS", ""))
    if name == "npi":
        return as_float(row.get("NPI", ""))
    if name == "nodes":
        return as_float(row.get("LYMPH_NODES_EXAMINED_POSITIVE", ""))
    if name == "er_negative":
        value = row.get("ER_IHC", "")
        return None if not value else float(value == "Negative")
    if name == "her2_gain":
        value = row.get("HER2_SNP6", "")
        return None if not value else float(value == "GAIN")
    if name == "chemotherapy":
        value = row.get("CHEMOTHERAPY", "")
        return None if not value else float(value == "YES")
    if name == "hormone":
        value = row.get("HORMONE_THERAPY", "")
        return None if not value else float(value == "YES")
    if name == "radiotherapy":
        value = row.get("RADIO_THERAPY", "")
        return None if not value else float(value == "YES")
    if name.startswith("subtype:"):
        value = row.get("CLAUDIN_SUBTYPE", "")
        return None if not value else float(value == name.split(":", 1)[1])
    raise KeyError(name)


def load(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    selected: list[dict[str, object]] = []
    for row in rows:
        months = as_float(row.get("OS_MONTHS", ""))
        if months is None:
            continue
        label = fixed_horizon_survivor_label(
            months,
            row.get("VITAL_STATUS", ""),
        )
        if label is None:
            continue
        selected.append({**row, "_y": int(label == "LTS")})
    return selected


def matrices(
    train: list[dict[str, object]],
    test: list[dict[str, object]],
    names: tuple[str, ...],
) -> tuple[list[list[float]], list[int], list[list[float]], list[int]]:
    means: dict[str, float] = {}
    scales: dict[str, float] = {}

    for name in names:
        values = [
            value
            for row in train
            if (value := feature(row, name)) is not None
        ]
        center = mean(values)
        variance = sum((v - center) ** 2 for v in values) / max(1, len(values) - 1)
        means[name] = center
        scales[name] = variance ** 0.5 or 1.0

    def encode(row: dict[str, object]) -> list[float]:
        encoded = [1.0]
        for name in names:
            value = feature(row, name)
            if value is None:
                value = means[name]
            encoded.append((value - means[name]) / scales[name])
        return encoded

    return (
        [encode(row) for row in train],
        [int(row["_y"]) for row in train],
        [encode(row) for row in test],
        [int(row["_y"]) for row in test],
    )


def run(path: Path) -> dict[str, object]:
    data = load(path)
    cohorts = sorted({str(row.get("COHORT", "")) for row in data if row.get("COHORT")})
    result: dict[str, object] = {
        "n": len(data),
        "cohorts": cohorts,
        "models": {},
    }

    for model_name, names in MODELS.items():
        pooled_y: list[int] = []
        pooled_p: list[float] = []
        folds = []

        for cohort in cohorts:
            train = [row for row in data if str(row.get("COHORT", "")) != cohort]
            test = [row for row in data if str(row.get("COHORT", "")) == cohort]
            if not test:
                continue

            x_train, y_train, x_test, y_test = matrices(train, test, names)
            weights = fit_logistic(x_train, y_train)
            probabilities = list(predict_logistic(x_test, weights))

            pooled_y.extend(y_test)
            pooled_p.extend(probabilities)
            folds.append(
                {
                    "cohort": cohort,
                    "n": len(test),
                    "log_loss": binary_log_loss(y_test, probabilities),
                    "auc": binary_auc(y_test, probabilities),
                }
            )

        result["models"][model_name] = {
            "pooled_n": len(pooled_y),
            "pooled_log_loss": binary_log_loss(pooled_y, pooled_p),
            "pooled_auc": binary_auc(pooled_y, pooled_p),
            "folds": folds,
        }

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("clinical_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.dumps(run(args.clinical_csv), indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
