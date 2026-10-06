#!/usr/bin/env python3
"""HF01 frozen-axis transfer into GSE93766 balding vs non-balding DP cells.

Uses the GEO-provided Cuffdiff gene-level result for BK0 vs NBK0, avoiding a
large platform-annotation download. Axes remain frozen from GSE36169.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import http.client
import json
import math
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path

URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE93nnn/GSE93766/suppl/"
    "GSE93766_BK0vsNBK0_gene_exp.diff.txt.gz"
)


def fetch_gzip_text(url: str, attempts: int = 5) -> str:
    last_error = None
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "dissociated-control-systems-hf01/0.1"},
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = response.read()
            return gzip.decompress(payload).decode("utf-8", errors="replace")
        except (
            http.client.IncompleteRead,
            urllib.error.URLError,
            TimeoutError,
            OSError,
        ) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1 + attempt)
    raise RuntimeError(f"failed to download {url}") from last_error


def parse_diff(text: str) -> tuple[dict[str, float], dict[str, str]]:
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    if reader.fieldnames is None:
        raise RuntimeError("missing Cuffdiff header")

    fields = {name.lower(): name for name in reader.fieldnames}
    gene_field = next(
        (fields[x] for x in ("gene", "gene_id", "test_id") if x in fields),
        None,
    )
    fold_field = next(
        (
            fields[x]
            for x in (
                "log2(fold_change)",
                "log2_fold_change",
                "log2fc",
            )
            if x in fields
        ),
        None,
    )
    sample1_field = fields.get("sample_1")
    sample2_field = fields.get("sample_2")
    if (
        gene_field is None
        or fold_field is None
        or sample1_field is None
        or sample2_field is None
    ):
        raise RuntimeError(f"unexpected Cuffdiff columns: {reader.fieldnames}")

    gene_to_effects: dict[str, list[float]] = {}
    orientation = None

    for row in reader:
        raw_gene = (row.get(gene_field) or "").strip()
        raw_effect = (row.get(fold_field) or "").strip()
        sample1 = (row.get(sample1_field) or "").strip()
        sample2 = (row.get(sample2_field) or "").strip()
        if not raw_gene or not raw_effect:
            continue

        # Cuffdiff reports log2(value_2 / value_1). Convert every row into the
        # HF01 convention: balding minus non-balding.
        s1_bald = sample1.upper().startswith("BK")
        s1_nonbald = sample1.upper().startswith("NBK")
        s2_bald = sample2.upper().startswith("BK")
        s2_nonbald = sample2.upper().startswith("NBK")
        if s1_bald and s2_nonbald:
            multiplier = -1.0
            orientation = {
                "sample_1": sample1,
                "sample_2": sample2,
                "cuffdiff_definition": "log2(value_2/value_1)",
                "hf01_conversion": "negated to balding-minus-nonbalding",
            }
        elif s1_nonbald and s2_bald:
            multiplier = 1.0
            orientation = {
                "sample_1": sample1,
                "sample_2": sample2,
                "cuffdiff_definition": "log2(value_2/value_1)",
                "hf01_conversion": "already balding-minus-nonbalding",
            }
        else:
            raise RuntimeError(
                f"cannot orient Cuffdiff contrast: sample_1={sample1!r}, "
                f"sample_2={sample2!r}"
            )

        try:
            effect = multiplier * float(raw_effect)
        except ValueError:
            continue

        for gene in raw_gene.replace(",", ";").split(";"):
            gene = gene.strip()
            if gene and gene != "-":
                gene_to_effects.setdefault(gene, []).append(effect)

    if orientation is None:
        raise RuntimeError("no usable Cuffdiff rows")

    effects = {}
    for gene, values in gene_to_effects.items():
        finite = [value for value in values if math.isfinite(value)]
        if finite:
            effects[gene] = statistics.fmean(finite)
            continue
        has_pos = any(value == math.inf for value in values)
        has_neg = any(value == -math.inf for value in values)
        if has_pos and not has_neg:
            effects[gene] = math.inf
        elif has_neg and not has_pos:
            effects[gene] = -math.inf

    return effects, orientation


def summarize_axis(
    genes: dict[str, int],
    effects: dict[str, float],
) -> dict[str, object]:
    available = sorted(gene for gene in genes if gene in effects)
    contributions = {
        gene: genes[gene] * effects[gene]
        for gene in available
    }
    usable_direction = [
        value for value in contributions.values() if not math.isnan(value)
    ]
    finite = [value for value in usable_direction if math.isfinite(value)]
    aligned = sum(value > 0 for value in usable_direction)

    return {
        "declared_genes": len(genes),
        "available_genes": len(available),
        "available_gene_names": available,
        "finite_gene_count": len(finite),
        "median_finite_signed_log2_fold_change": (
            None if not finite else round(statistics.median(finite), 6)
        ),
        "mean_finite_signed_log2_fold_change": (
            None if not finite else round(statistics.fmean(finite), 6)
        ),
        "gene_direction_alignment": (
            None
            if not usable_direction
            else round(aligned / len(usable_direction), 6)
        ),
        "signed_gene_contributions": {
            gene: (
                "Infinity"
                if value == math.inf
                else "-Infinity"
                if value == -math.inf
                else round(value, 6)
            )
            for gene, value in contributions.items()
            if not math.isnan(value)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axes", default="specs/HF01_GSE36169_AXES.json")
    parser.add_argument(
        "--output", default="artifacts/hf01/gse93766-bk0-result.json"
    )
    args = parser.parse_args()

    axes = json.loads(Path(args.axes).read_text())
    effects, orientation = parse_diff(fetch_gzip_text(URL))

    result = {
        "dataset": "GSE93766",
        "contrast": "BK0 vs NBK0",
        "material": "immortalized balding vs non-balding human dermal-papilla aggregates co-cultured with NHEK",
        "source": URL,
        "orientation": orientation,
        "axes_spec_reused_from": "specs/HF01_GSE36169_AXES.json",
        "axes": {
            name: summarize_axis(genes, effects)
            for name, genes in axes["axes"].items()
        },
        "boundary": (
            "Technical-triplicate immortalized-cell data are a cell-model transfer "
            "test, not an independent human cohort and not a clinical validation."
        ),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
