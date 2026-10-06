"""Graph diagnostics for evidence-identity binding audits.

The graph encodes only observed unique identity matches such as
`displayed_row_trial -> canonical_trial_whose_counts_match`.
It does not infer why a cross-binding exists.
"""

from __future__ import annotations

from collections.abc import Mapping


def normalize_binding_edges(edges: Mapping[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for source, target in edges.items():
        if not isinstance(source, str) or not isinstance(target, str):
            raise TypeError("binding graph identifiers must be strings")
        if not source.strip() or source != source.strip():
            raise ValueError("source identifiers must be non-empty and normalized")
        if not target.strip() or target != target.strip():
            raise ValueError("target identifiers must be non-empty and normalized")
        if source in out:
            raise ValueError(f"duplicate source: {source}")
        out[source] = target
    return out


def walk_binding_path(edges: Mapping[str, str], start: str) -> tuple[str, ...]:
    """Follow one-outgoing-edge binding graph until terminal or first repeat."""

    graph = normalize_binding_edges(edges)
    if start not in graph:
        return (start,)

    path = [start]
    seen = {start}
    node = start
    while node in graph:
        nxt = graph[node]
        path.append(nxt)
        if nxt in seen:
            break
        seen.add(nxt)
        node = nxt
    return tuple(path)


def detect_cycle(edges: Mapping[str, str], start: str) -> tuple[str, ...] | None:
    """Return a closed cycle path reachable from start, else None."""

    path = walk_binding_path(edges, start)
    if len(path) < 2:
        return None
    final = path[-1]
    try:
        first = path.index(final)
    except ValueError:  # pragma: no cover - tuple membership makes this impossible
        return None
    if first == len(path) - 1:
        return None
    return path[first:]


def all_binding_paths(edges: Mapping[str, str]) -> tuple[tuple[str, ...], ...]:
    """Return unique maximal-ish paths sorted by decreasing observed length.

    Paths that are strict suffixes of another path are removed to keep the
    diagnostic concise. A path is descriptive only; length is not evidence of
    mechanism.
    """

    graph = normalize_binding_edges(edges)
    raw = [walk_binding_path(graph, start) for start in graph]
    unique: list[tuple[str, ...]] = []
    for path in sorted(set(raw), key=lambda value: (-len(value), value)):
        if any(
            len(path) < len(other) and tuple(other[-len(path) :]) == path
            for other in unique
        ):
            continue
        unique.append(path)
    return tuple(unique)


def binding_summary(edges: Mapping[str, str]) -> dict[str, object]:
    graph = normalize_binding_edges(edges)
    self_edges = tuple(sorted(source for source, target in graph.items() if source == target))
    cross_edges = tuple(
        sorted((source, target) for source, target in graph.items() if source != target)
    )
    cycles = []
    seen_cycles: set[tuple[str, ...]] = set()
    for start in graph:
        cycle = detect_cycle(graph, start)
        if cycle is None:
            continue
        # canonicalize the closed cycle without changing its orientation
        core = cycle[:-1]
        rotations = [core[i:] + core[:i] for i in range(len(core))]
        canonical_core = min(rotations)
        canonical = canonical_core + (canonical_core[0],)
        if canonical not in seen_cycles:
            seen_cycles.add(canonical)
            cycles.append(canonical)

    paths = all_binding_paths(graph)
    return {
        "edge_count": len(graph),
        "self_edge_count": len(self_edges),
        "cross_edge_count": len(cross_edges),
        "self_edges": self_edges,
        "cross_edges": cross_edges,
        "cycles": tuple(sorted(cycles)),
        "paths": paths,
        "longest_path": paths[0] if paths else (),
    }
