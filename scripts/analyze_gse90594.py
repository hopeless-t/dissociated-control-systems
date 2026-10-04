#!/usr/bin/env python3
"""Cross-cohort HF01 axis replication on GEO GSE90594.

The pathway axes are reused unchanged from the GSE36169 pre-registration.
Only the observation design changes: 14 AGA vertex vs 14 healthy vertex.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import http.client
import json
import random
import statistics
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

MATRIX_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE90nnn/GSE90594/"
    "matrix/GSE90594_series_matrix.txt.gz"
)
ANNOT_URL = (
    "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL17nnn/GPL17077/"
    "annot/GPL17077.annot.gz"
)


def fetch_gzip_text(url: str, attempts: int = 5) -> str:
    last_error = None
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "dissociated-control-systems-hf01/0.1"},
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
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
    raise RuntimeError(f"failed to download {url} after {attempts} attempts") from last_error


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
        raise RuntimeError("GSE90594 matrix metadata not found")
    return titles, sample_ids, rows


def parse_annotation(text: str) -> dict[str, list[str]]:
    lines = [
        line.lstrip("\ufeff")
        for line in text.splitlines()
        if line and not line.startswith("#")
    ]
    header_index = None
    normalized = None

    for idx, line in enumerate(lines):
        candidate = next(csv.reader([line], delimiter="\t"))
        norm = [
            h.strip().strip('"').lstrip("\ufeff").lower().replace(" ", "_")
            for h in candidate
        ]
        has_id = any(
            name in norm for name in ("id", "probe_name", "probe_set_id", "id_ref")
        )
        has_symbol = any(
            name in norm
            for name in ("gene_symbol", "gene_symbol_", "gene_assignment")
        )
        if has_id and has_symbol:
            header_index = idx
            normalized = norm
            break

    if header_index is None or normalized is None:
        raise RuntimeError(f"annotation header not found; preview={lines[:5]!r}")

    id_i = next(
        normalized.index(name)
        for name in ("id", "probe_name", "probe_set_id", "id_ref")
        if name in normalized
    )
    symbol_i = next(
        normalized.index(name)
        for name in ("gene_symbol", "gene_symbol_", "gene_assignment")
        if name in normalized
    )

    probe_to_symbols: dict[str, list[str]] = {}
    reader = csv.reader(lines[header_index + 1 :], delimiter="\t")
    for row in reader:
        if len(row) <= max(id_i, symbol_i):
            continue
        probe = row[id_i].strip()
        raw_symbols = row[symbol_i].strip()
        if not probe or not raw_symbols or raw_symbols == "---":
            continue
        symbols = [
            token.strip()
            for token in raw_symbols.replace("///", ";").split(";")
            if token.strip() and token.strip() != "---"
        ]
        if symbols:
            probe_to_symbols[probe] = symbols
    return probe_to_symbols


def classify_samples(titles: list[str]) -> tuple[list[int], list[int]]:
    aga = [i for i, title in enumerate(titles) if "alopecia" in title.lower()]
    healthy = [i for i, title in enumerate(titles) if "healthy" in title.lower()]
    if len(aga) != 14 or len(healthy) != 14:
        raise RuntimeError(
            f"expected 14 AGA and 14 healthy samples; got {len(aga)}, {len(healthy)}"
        )
    return aga, healthy


def gene_values(
    rows: dict[str, list[float]],
    probe_to_symbols: dict[str, list[str]],
) -> dict[str, list[float]]:
    by_gene_probe: dict[str, list[str]] = defaultdict(list)
    for probe, symbols in probe_to_symbols.items():
        if probe not in rows:
            continue
        for symbol in symbols:
            by_gene_probe[symbol].append(probe)

    result: dict[str, list[float]] = {}
    for gene, probes in by_gene_probe.items():
        values = []
        for sample_i in range(len(next(iter(rows.values())))):
            values.append(statistics.fmean(rows[p][sample_i] for p in probes))
        result[gene] = values
    return result


def axis_score(
    genes: dict[str, int],
    values: dict[str, list[float]],
    aga: list[int],
    healthy: list[int],
) -> tuple[float | None, list[str]]:
    available = sorted(g for g in genes if g in values)
    if not available:
        return None, []

    contributions = []
    for gene in available:
        disease = statistics.fmean(values[gene][i] for i in aga)
        control = statistics.fmean(values[gene][i] for i in healthy)
        contributions.append(genes[gene] * (disease - control))
    return statistics.fmean(contributions), available


def bootstrap_axis(
    genes: dict[str, int],
    values: dict[str, list[float]],
    aga: list[int],
    healthy: list[int],
    seed: int = 90594,
    samples: int = 2000,
) -> dict[str, object]:
    score, available = axis_score(genes, values, aga, healthy)
    if score is None:
        return {
            "available_genes": 0,
            "declared_genes": len(genes),
            "mean_signed_delta": None,
            "bootstrap_ci95": None,
            "positive_bootstrap_fraction": None,
        }

    rng = random.Random(seed)
    draws = []
    for _ in range(samples):
        a = [rng.choice(aga) for _ in aga]
        h = [rng.choice(healthy) for _ in healthy]
        draw, _ = axis_score(genes, values, a, h)
        draws.append(draw)

    draws.sort()
    lo = draws[int(0.025 * samples)]
    hi = draws[int(0.975 * samples)]

    return {
        "available_genes": len(available),
        "declared_genes": len(genes),
        "available_gene_names": available,
        "mean_signed_delta": round(score, 6),
        "bootstrap_ci95": [round(lo, 6), round(hi, 6)],
        "positive_bootstrap_fraction": round(
            sum(x > 0 for x in draws) / len(draws), 6
        ),
        "bootstrap_samples": samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--axes", default="specs/HF01_GSE36169_AXES.json")
    parser.add_argument(
        "--output", default="artifacts/hf01/gse90594-result.json"
    )
    args = parser.parse_args()

    axes = json.loads(Path(args.axes).read_text())
    titles, sample_ids, rows = parse_matrix(fetch_gzip_text(MATRIX_URL))
    aga, healthy = classify_samples(titles)
    probe_to_symbols = parse_annotation(fetch_gzip_text(ANNOT_URL))
    values = gene_values(rows, probe_to_symbols)

    results = {
        name: bootstrap_axis(genes, values, aga, healthy)
        for name, genes in axes["axes"].items()
    }

    result = {
        "dataset": "GSE90594",
        "design": "14 AGA vertex vs 14 healthy vertex",
        "platform": "GPL17077",
        "axes_spec_reused_from": "specs/HF01_GSE36169_AXES.json",
        "sample_titles": titles,
        "sample_ids": sample_ids,
        "axes": results,
        "replication_rule": (
            "Directional transfer of a frozen axis is compatibility evidence. "
            "Failure to transfer is retained as a failed prediction, not repaired "
            "by post-hoc gene selection."
        ),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
