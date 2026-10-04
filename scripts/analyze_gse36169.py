#!/usr/bin/env python3
"""Pre-registered paired analysis for GEO GSE36169.

Uses only the Python standard library so the result can run in a clean CI job.
This is exploratory public-data validation, not a clinical model.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import math
import statistics
import urllib.request
from collections import defaultdict
from pathlib import Path

MATRIX_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE36nnn/GSE36169/"
    "matrix/GSE36169_series_matrix.txt.gz"
)
ANNOT_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPLnnn/GPL96/"
    "annot/GPL96.annot.gz"
)


def fetch_gzip_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = response.read()
    return gzip.decompress(payload).decode("utf-8", errors="replace")


def parse_matrix(text: str):
    titles = None
    sample_ids = None
    rows: dict[str, list[float]] = {}

    in_table = False
    for raw in text.splitlines():
        if raw.startswith("!Sample_title"):
            titles = next(csv.reader([raw], delimiter="\t"))[1:]
            titles = [x.strip('"') for x in titles]
        elif raw == "!series_matrix_table_begin":
            in_table = True
        elif raw == "!series_matrix_table_end":
            break
        elif in_table:
            fields = next(csv.reader([raw], delimiter="\t"))
            fields = [x.strip('"') for x in fields]
            if fields[0] == "ID_REF":
                sample_ids = fields[1:]
            else:
                try:
                    rows[fields[0]] = [float(x) for x in fields[1:]]
                except ValueError:
                    continue

    if not titles or not sample_ids:
        raise RuntimeError("GSE36169 matrix metadata not found")
    if len(titles) != len(sample_ids):
        raise RuntimeError("sample title/id length mismatch")
    return titles, sample_ids, rows


def parse_annotation(text: str) -> dict[str, list[str]]:
    probe_to_symbols: dict[str, list[str]] = {}
    lines = [
        line.lstrip("\ufeff")
        for line in text.splitlines()
        if line and not line.startswith("#")
    ]

    header_index = None
    header = None
    normalized = None
    for idx, line in enumerate(lines):
        candidate = next(csv.reader([line], delimiter="\t"))
        norm = [
            h.strip().strip('"').lstrip("\ufeff").lower().replace(" ", "_")
            for h in candidate
        ]
        has_id = any(name in norm for name in ("id", "probe_set_id", "id_ref"))
        has_symbol = any(
            name in norm
            for name in ("gene_symbol", "gene_symbol_", "gene_assignment")
        )
        if has_id and has_symbol:
            header_index = idx
            header = candidate
            normalized = norm
            break

    if header_index is None or header is None or normalized is None:
        preview = lines[:5]
        raise RuntimeError(f"annotation header not found; preview={preview!r}")

    id_i = next(
        normalized.index(name)
        for name in ("id", "probe_set_id", "id_ref")
        if name in normalized
    )
    symbol_i = next(
        normalized.index(name)
        for name in ("gene_symbol", "gene_symbol_", "gene_assignment")
        if name in normalized
    )

    reader = csv.reader(lines[header_index + 1 :], delimiter="\t")
    for row in reader:
        if len(row) <= max(id_i, symbol_i):
            continue
        probe = row[id_i].strip()
        raw_symbols = row[symbol_i].strip()
        if not probe or not raw_symbols or raw_symbols == "---":
            continue
        symbols = []
        for token in raw_symbols.replace("///", ";").split(";"):
            token = token.strip()
            if token and token != "---":
                symbols.append(token)
        if symbols:
            probe_to_symbols[probe] = symbols
    return probe_to_symbols


def classify_samples(titles: list[str]):
    subjects: dict[str, dict[str, int]] = defaultdict(dict)
    for idx, title in enumerate(titles):
        # Expected examples: "Subject 1- Haired", "Subject 1- Bald"
        lower = title.lower()
        if "subject" not in lower:
            continue
        tokens = title.replace("-", " ").split()
        subject = next((t for t in tokens if t.isdigit()), None)
        if subject is None:
            continue
        if "haired" in lower:
            subjects[subject]["haired"] = idx
        elif "bald" in lower:
            subjects[subject]["bald"] = idx

    complete = {
        subject: pair
        for subject, pair in subjects.items()
        if {"haired", "bald"} <= pair.keys()
    }
    if len(complete) != 5:
        raise RuntimeError(f"expected 5 complete pairs, found {complete}")
    return dict(sorted(complete.items(), key=lambda kv: int(kv[0])))


def log2_value(value: float) -> float:
    return math.log2(max(value, 1e-9))


def gene_pair_deltas(
    rows: dict[str, list[float]],
    probe_to_symbols: dict[str, list[str]],
    pairs: dict[str, dict[str, int]],
) -> dict[str, dict[str, float]]:
    by_gene_probe: dict[str, list[str]] = defaultdict(list)
    for probe, symbols in probe_to_symbols.items():
        if probe not in rows:
            continue
        for symbol in symbols:
            by_gene_probe[symbol].append(probe)

    result: dict[str, dict[str, float]] = {}
    for gene, probes in by_gene_probe.items():
        subject_deltas = {}
        for subject, pair in pairs.items():
            probe_deltas = []
            for probe in probes:
                values = rows[probe]
                bald = log2_value(values[pair["bald"]])
                haired = log2_value(values[pair["haired"]])
                probe_deltas.append(bald - haired)
            if probe_deltas:
                subject_deltas[subject] = statistics.fmean(probe_deltas)
        if subject_deltas:
            result[gene] = subject_deltas
    return result


def summarize_axis(
    genes: dict[str, int],
    deltas: dict[str, dict[str, float]],
    subjects: list[str],
) -> dict[str, object]:
    available = {gene: sign for gene, sign in genes.items() if gene in deltas}
    per_subject = {}
    for subject in subjects:
        contributions = [
            sign * deltas[gene][subject]
            for gene, sign in available.items()
            if subject in deltas[gene]
        ]
        if contributions:
            per_subject[subject] = statistics.fmean(contributions)

    values = list(per_subject.values())
    mean_score = statistics.fmean(values) if values else None
    median_score = statistics.median(values) if values else None
    positive_pairs = sum(value > 0 for value in values)

    return {
        "declared_genes": len(genes),
        "available_genes": len(available),
        "available_gene_names": sorted(available),
        "subject_scores": {k: round(v, 6) for k, v in per_subject.items()},
        "mean_signed_log2_delta": None if mean_score is None else round(mean_score, 6),
        "median_signed_log2_delta": None if median_score is None else round(median_score, 6),
        "positive_pair_count": positive_pairs,
        "pair_count": len(values),
        "direction_consistency": (
            None if not values else round(positive_pairs / len(values), 6)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--axes",
        default="specs/HF01_GSE36169_AXES.json",
    )
    parser.add_argument(
        "--output",
        default="artifacts/hf01/gse36169-result.json",
    )
    args = parser.parse_args()

    axes = json.loads(Path(args.axes).read_text())
    matrix_text = fetch_gzip_text(MATRIX_URL)
    annotation_text = fetch_gzip_text(ANNOT_URL)

    titles, sample_ids, rows = parse_matrix(matrix_text)
    pairs = classify_samples(titles)
    probe_to_symbols = parse_annotation(annotation_text)
    deltas = gene_pair_deltas(rows, probe_to_symbols, pairs)
    subjects = list(pairs)

    positive_control = {
        name: summarize_axis(genes, deltas, subjects)
        for name, genes in axes["positive_control_not_validation"].items()
    }
    axis_results = {
        name: summarize_axis(genes, deltas, subjects)
        for name, genes in axes["axes"].items()
    }

    result = {
        "dataset": "GSE36169",
        "design": "5 within-person haired-vs-bald pairs",
        "platform": "GPL96",
        "matrix_url": MATRIX_URL,
        "annotation_url": ANNOT_URL,
        "sample_titles": titles,
        "sample_ids": sample_ids,
        "positive_control_not_validation": positive_control,
        "axes": axis_results,
        "interpretation_rule": {
            "positive_axis_score": (
                "bald-minus-haired expression changes align with the pre-registered "
                "direction for that axis"
            ),
            "negative_axis_score": (
                "changes oppose the pre-registered direction"
            ),
            "validation_boundary": (
                "A directional axis result is exploratory compatibility evidence; "
                "it does not identify a causal HF01 latent state."
            ),
        },
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
