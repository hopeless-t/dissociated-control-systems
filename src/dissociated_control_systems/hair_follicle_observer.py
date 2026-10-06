"""Synthetic observability analysis for HF01.

The rows below are conceptual measurement sensitivities, not calibrated
biomarker equations. Their purpose is to make under-observation explicit.
"""

from __future__ import annotations

STATE_ORDER = (
    "androgen_pressure",
    "stress_load",
    "regeneration",
    "progenitor_reserve",
    "niche_integrity",
    "structural_lock",
    "hair_output",
)

PROBES: dict[str, tuple[float, ...]] = {
    # Tier 0: output-oriented, non-invasive.
    "visible_output": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
    "trichoscopy_miniaturization": (0.1, 0.0, 0.15, 0.35, 0.0, 0.2, 0.5),
    "phototrichogram_cycle": (0.0, 0.0, 0.5, 0.3, 0.1, 0.0, 0.3),

    # Tier 2/3: contextual or physiology-adjacent.
    "stress_context": (0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    "microvascular_proxy": (0.2, 0.0, 0.1, 0.0, 0.0, 0.35, 0.0),

    # Tier 4: research molecular/structural probes.
    "androgen_pathway": (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    "regeneration_pathway": (0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    "progenitor_panel": (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
    "niche_panel": (0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0),
    "mechanical_structural": (0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0),
}


def matrix_rank(rows: list[tuple[float, ...]], tolerance: float = 1e-10) -> int:
    """Return matrix rank using deterministic Gaussian elimination."""
    if not rows:
        return 0
    matrix = [list(map(float, row)) for row in rows]
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    rank = 0
    col = 0

    while rank < n_rows and col < n_cols:
        pivot = max(range(rank, n_rows), key=lambda r: abs(matrix[r][col]))
        if abs(matrix[pivot][col]) <= tolerance:
            col += 1
            continue

        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][col]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]

        for r in range(n_rows):
            if r == rank:
                continue
            factor = matrix[r][col]
            if abs(factor) <= tolerance:
                continue
            matrix[r] = [
                a - factor * b for a, b in zip(matrix[r], matrix[rank])
            ]

        rank += 1
        col += 1

    return rank


def probe_rank(names: tuple[str, ...] | list[str]) -> int:
    return matrix_rank([PROBES[name] for name in names])


TIER0 = (
    "visible_output",
    "trichoscopy_miniaturization",
    "phototrichogram_cycle",
)

TIER0_PLUS_CONTEXT = TIER0 + ("stress_context",)

TIER0_TO_PHYSIOLOGY = TIER0_PLUS_CONTEXT + ("microvascular_proxy",)

FULL_RESEARCH_SET = TIER0_TO_PHYSIOLOGY + (
    "androgen_pathway",
    "regeneration_pathway",
    "progenitor_panel",
    "niche_panel",
    "mechanical_structural",
)
