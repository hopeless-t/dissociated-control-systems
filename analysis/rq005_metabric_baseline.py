"""RQ-005 METABRIC retrospective baseline.

Input is a METABRIC patient clinical CSV with the cBioPortal-style columns.
No network calls are made. The script deliberately uses a strict discovery
contrast rather than treating censored patients as known outcomes.

This is retrospective model discovery, not a clinical prognosis model.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean, median

from dissociated_control_systems.survivor_baseline import (
    fixed_horizon_survivor_label,
    standardized_mean_difference,
)


NUMERIC_FIELDS = (
    "LYMPH_NODES_EXAMINED_POSITIVE",
    "NPI",
    "AGE_AT_DIAGNOSIS",
)


def parse_float(value: str) -> float | None:
    value = value.strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def discovery_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = []
    for row in rows:
        months = parse_float(row.get("OS_MONTHS", ""))
        if months is None:
            continue
        label = fixed_horizon_survivor_label(
            months,
            row.get("VITAL_STATUS", ""),
        )
        if label is None:
            continue
        copy = dict(row)
        copy["_label"] = label
        selected.append(copy)
    return selected


def numeric_summary(
    lts: list[dict[str, str]],
    sts: list[dict[str, str]],
    field: str,
) -> dict[str, object]:
    a = [v for row in lts if (v := parse_float(row.get(field, ""))) is not None]
    b = [v for row in sts if (v := parse_float(row.get(field, ""))) is not None]
    return {
        "field": field,
        "lts_n": len(a),
        "sts_n": len(b),
        "lts_mean": mean(a),
        "sts_mean": mean(b),
        "lts_median": median(a),
        "sts_median": median(b),
        "smd": standardized_mean_difference(a, b),
    }


def categorical_difference(
    lts: list[dict[str, str]],
    sts: list[dict[str, str]],
    field: str,
) -> list[dict[str, object]]:
    values = sorted(
        {
            row.get(field, "")
            for row in lts + sts
            if row.get(field, "")
        }
    )
    l_valid = [row for row in lts if row.get(field, "")]
    s_valid = [row for row in sts if row.get(field, "")]
    result = []
    for value in values:
        lp = sum(row[field] == value for row in l_valid) / len(l_valid)
        sp = sum(row[field] == value for row in s_valid) / len(s_valid)
        result.append(
            {
                "value": value,
                "lts_proportion": lp,
                "sts_proportion": sp,
                "difference": lp - sp,
            }
        )
    return sorted(result, key=lambda item: abs(item["difference"]), reverse=True)


def analyze(path: Path) -> dict[str, object]:
    rows = load_rows(path)
    selected = discovery_rows(rows)
    lts = [row for row in selected if row["_label"] == "LTS"]
    sts = [row for row in selected if row["_label"] == "STS"]

    return {
        "input_rows": len(rows),
        "labels": {
            "LTS": len(lts),
            "STS": len(sts),
            "unclassified": len(rows) - len(selected),
        },
        "cohort_counts": dict(Counter(row.get("COHORT", "") for row in selected)),
        "numeric": [
            numeric_summary(lts, sts, field)
            for field in NUMERIC_FIELDS
        ],
        "claudin_subtype": categorical_difference(
            lts, sts, "CLAUDIN_SUBTYPE"
        ),
        "intclust": categorical_difference(lts, sts, "INTCLUST"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("clinical_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = analyze(args.clinical_csv)
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
