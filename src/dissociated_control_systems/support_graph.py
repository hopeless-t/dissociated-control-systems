"""Acyclic support-graph checks for DCS assurance artifacts."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class SupportNodeKind(str, Enum):
    PRIMITIVE_EVIDENCE = "PRIMITIVE_EVIDENCE"
    DERIVED_EVIDENCE = "DERIVED_EVIDENCE"
    CLAIM = "CLAIM"


@dataclass(frozen=True)
class SupportNode:
    node_id: str
    kind: SupportNodeKind


@dataclass(frozen=True)
class SupportEdge:
    source: str
    target: str


def find_cycles(
    nodes: Iterable[SupportNode],
    edges: Iterable[SupportEdge],
) -> tuple[tuple[str, ...], ...]:
    """Return simple DFS-detected cycles in a small directed support graph."""
    nodes_t = tuple(nodes)
    names = {node.node_id for node in nodes_t}
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge.source not in names or edge.target not in names:
            raise ValueError("edge references unknown support node")
        adjacency[edge.source].append(edge.target)

    state = {name: 0 for name in names}  # 0 unseen, 1 active, 2 done
    stack: list[str] = []
    cycles: set[tuple[str, ...]] = set()

    def canonical_cycle(path: list[str]) -> tuple[str, ...]:
        body = path[:-1]
        rotations = [
            tuple(body[i:] + body[:i])
            for i in range(len(body))
        ]
        best = min(rotations)
        return best + (best[0],)

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for nxt in adjacency.get(node, []):
            if state[nxt] == 0:
                visit(nxt)
            elif state[nxt] == 1:
                idx = stack.index(nxt)
                cycles.add(canonical_cycle(stack[idx:] + [nxt]))
        stack.pop()
        state[node] = 2

    for node in sorted(names):
        if state[node] == 0:
            visit(node)

    return tuple(sorted(cycles))


def primitive_ancestors(
    target: str,
    nodes: Iterable[SupportNode],
    edges: Iterable[SupportEdge],
) -> frozenset[str]:
    """Primitive evidence nodes that can reach target in an acyclic graph."""
    nodes_t = tuple(nodes)
    kind = {node.node_id: node.kind for node in nodes_t}
    names = set(kind)
    if target not in names:
        raise ValueError("target must exist")
    edges_t = tuple(edges)
    if find_cycles(nodes_t, edges_t):
        raise ValueError("primitive ancestry is undefined for cyclic support graph")

    reverse: dict[str, list[str]] = defaultdict(list)
    for edge in edges_t:
        if edge.source not in names or edge.target not in names:
            raise ValueError("edge references unknown support node")
        reverse[edge.target].append(edge.source)

    found: set[str] = set()
    seen: set[str] = set()
    stack = [target]
    while stack:
        current = stack.pop()
        for parent in reverse.get(current, []):
            if parent in seen:
                continue
            seen.add(parent)
            if kind[parent] is SupportNodeKind.PRIMITIVE_EVIDENCE:
                found.add(parent)
            else:
                stack.append(parent)
    return frozenset(found)


def claim_is_grounded(
    target: str,
    nodes: Iterable[SupportNode],
    edges: Iterable[SupportEdge],
) -> bool:
    nodes_t = tuple(nodes)
    edges_t = tuple(edges)
    if find_cycles(nodes_t, edges_t):
        return False
    return bool(primitive_ancestors(target, nodes_t, edges_t))
