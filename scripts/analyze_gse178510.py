#!/usr/bin/env python3
"""HF01 actuator-identification test on GSE178510 minoxidil-treated HFDPCs."""

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
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE178nnn/GSE178510/suppl/"
    "GSE178510_2D_minox_vs_2D_Control.txt.gz"
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


def _norm(name: str) -> str:
    return (
        name.strip()
        .strip('"')
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def locate_header(lines: list[str]) -> tuple[int, list[str], list[str]]:
    for idx, line in enumerate(lines[:100]):
        row = next(csv.reader([line], delimiter="\t"))
        norm = [_norm(x) for x in row]
        has_gene = any(
            ("gene" in x and "symbol" in x) or x in ("gene", "genesymbol")
            for x in norm
        )
        has_fc = any("fold" in x and "change" in x for x in norm)
        if has_gene and has_fc:
            return idx, row, norm
    raise RuntimeError(
        "could not locate gene-symbol/fold-change header; "
        f"preview={lines[:8]!r}"
    )


def linear_or_log2_effect(value: float, field_name: str) -> float:
    field = _norm(field_name)
    if "log2" in field:
        return value

    # Transcriptome Analysis Console commonly emits signed linear fold change:
    # +X for up, -X for down. Preserve direction while converting magnitude to
    # log2 scale. Also tolerate ordinary positive ratios in (0,1).
    if value < 0:
        magnitude = abs(value)
        if magnitude == 0:
            return 0.0
        return -math.log2(magnitude)
    if value == 0:
        return 0.0
    return math.log2(value)


def parse_gene_effects(text: str) -> tuple[dict[str, float], dict[str, object]]:
    lines = [line.lstrip("\ufeff") for line in text.splitlines() if line.strip()]
    header_idx, header, norm = locate_header(lines)

    gene_i = next(
        i
        for i, name in enumerate(norm)
        if ("gene" in name and "symbol" in name)
        or name in ("gene", "genesymbol")
    )
    fc_i = next(
        i for i, name in enumerate(norm) if "fold" in name and "change" in name
    )
    fc_field = header[fc_i]

    gene_to_effects: dict[str, list[float]] = {}
    reader = csv.reader(lines[header_idx + 1 :], delimiter="\t")
    for row in reader:
        if len(row) <= max(gene_i, fc_i):
            continue
        raw_genes = row[gene_i].strip().strip('"')
        raw_fc = row[fc_i].strip().strip('"')
        if not raw_genes or not raw_fc:
            continue
        try:
            raw_value = float(raw_fc)
        except ValueError:
            continue
        effect = linear_or_log2_effect(raw_value, fc_field)
        if not math.isfinite(effect):
            continue

        for gene in (
            raw_genes.replace("///", ";").replace(",", ";").split(";")
        ):
            gene = gene.strip()
            if gene and gene not in ("---", "-"):
                gene_to_effects.setdefault(gene, []).append(effect)

    effects = {
        gene: statistics.fmean(values)
        for gene, values in gene_to_effects.items()
        if values
    }
    return effects, {
        "header": header,
        "gene_field": header[gene_i],
        "fold_change_field": fc_field,
        "effect_convention": "minoxidil-minus-control; converted to log2-like signed scale",
    }


def summarize_axis(
    genes: dict[str, int],
    effects: dict[str, float],
) -> dict[str, object]:
    available = sorted(gene for gene in genes if gene in effects)
    contributions = {
        gene: genes[gene] * effects[gene]
        for gene in available
    }
    values = list(contributions.values())
    return {
        "declared_genes": len(genes),
        "available_genes": len(available),
        "available_gene_names": available,
        "mean_signed_effect": (
            None if not values else round(statistics.fmean(values), 6)
        ),
        "median_signed_effect": (
            None if not values else round(statistics.median(values), 6)
        ),
        "negative_direction_fraction": (
            None
            if not values
            else round(sum(v < 0 for v in values) / len(values), 6)
        ),
        "signed_gene_contributions": {
            gene: round(value, 6)
            for gene, value in contributions.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axes", default="specs/HF01_GSE36169_AXES.json")
    parser.add_argument(
        "--prediction",
        default="specs/HF01_GSE178510_PREDICTION.json",
    )
    parser.add_argument(
        "--output",
        default="artifacts/hf01/gse178510-minox-result.json",
    )
    args = parser.parse_args()

    axes = json.loads(Path(args.axes).read_text())
    prediction = json.loads(Path(args.prediction).read_text())
    effects, parser_meta = parse_gene_effects(fetch_gzip_text(URL))

    axis_results = {
        name: summarize_axis(genes, effects)
        for name, genes in axes["axes"].items()
    }
    primary_name = prediction["primary_prediction"]["axis"]
    primary_score = axis_results[primary_name]["mean_signed_effect"]
    primary_pass = primary_score is not None and primary_score < 0

    result = {
        "dataset": "GSE178510",
        "material": "primary human follicle dermal papilla cells, 2D culture",
        "input": "minoxidil, 48 h",
        "source": URL,
        "prediction_spec": "specs/HF01_GSE178510_PREDICTION.json",
        "parser": parser_meta,
        "axes": axis_results,
        "primary_test": {
            "axis": primary_name,
            "expected": "< 0",
            "observed": primary_score,
            "pass": primary_pass,
        },
        "boundary": (
            "Cultured-cell actuator identification only; not a clinical, "
            "recoverability, or consciousness-mediated validation."
        ),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
