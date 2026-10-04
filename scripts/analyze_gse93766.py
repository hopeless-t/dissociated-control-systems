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


def parse_diff(text: str) -> dict[str, float]:
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
    if gene_field is None or fold_field is None:
        raise RuntimeError(f"unexpected Cuffdiff columns: {reader.fieldnames}")

    gene_to_effects: dict[str, list[float]] = {}
    for row in reader:
        raw_gene = (row.get(gene_field) or "").strip()
        raw_effect = (row.get(fold_field) or "").strip()
        if not raw_gene or not raw_effect:
            continue
        try:
            effect = float(raw_effect)
        except ValueError:
            continue
        for gene in raw_gene.replace(",", ";").split(";"):
            gene = gene.strip()
            if gene and gene != "-":
                gene_to_effects.setdefault(gene, []).append(effect)

    return {
        gene: sum(values) / len(values)
        for gene, values in gene_to_effects.items()
        if values
    }


def summarize_axis(
    genes: dict[str, int],
    effects: dict[str, float],
) -> dict[str, object]:
    available = sorted(gene for gene in genes if gene in effects)
    contributions = [genes[gene] * effects[gene] for gene in available]
    score = sum(contributions) / len(contributions) if contributions else None
    aligned = sum(value > 0 for value in contributions)

    return {
        "declared_genes": len(genes),
        "available_genes": len(available),
        "available_gene_names": available,
        "mean_signed_log2_fold_change": (
            None if score is None else round(score, 6)
        ),
        "gene_direction_alignment": (
            None if not contributions else round(aligned / len(contributions), 6)
        ),
        "signed_gene_contributions": {
            gene: round(genes[gene] * effects[gene], 6)
            for gene in available
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
    effects = parse_diff(fetch_gzip_text(URL))

    result = {
        "dataset": "GSE93766",
        "contrast": "BK0 vs NBK0",
        "material": "immortalized balding vs non-balding human dermal-papilla aggregates co-cultured with NHEK",
        "source": URL,
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
