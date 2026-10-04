"""Role-level must-pass checkpoints on small projection DAGs.

A visual/implementation node is not itself sacred. What must dominate every
accepted source-to-terminal path is the semantic checkpoint *role*.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ProjectionNode:
    name: str
    role: str | None = None


@dataclass(frozen=True)
class ProjectionEdge:
    source: str
    target: str


def enumerate_paths(
    nodes: Iterable[ProjectionNode],
    edges: Iterable[ProjectionEdge],
    source: str,
    target: str,
) -> tuple[tuple[str, ...], ...]:
    node_names = {node.name for node in nodes}
    if source not in node_names or target not in node_names:
        raise ValueError("source/target must exist")

    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge.source not in node_names or edge.target not in node_names:
            raise ValueError("edge references unknown node")
        adjacency[edge.source].append(edge.target)

    paths: list[tuple[str, ...]] = []

    def visit(current: str, path: tuple[str, ...]) -> None:
        if current == target:
            paths.append(path)
            return
        for nxt in adjacency.get(current, []):
            if nxt in path:
                continue
            visit(nxt, path + (nxt,))

    visit(source, (source,))
    return tuple(paths)


def node_dominators(
    nodes: Iterable[ProjectionNode],
    edges: Iterable[ProjectionEdge],
    source: str,
    target: str,
) -> frozenset[str]:
    """Nodes present on every source->target path."""
    paths = enumerate_paths(nodes, edges, source, target)
    if not paths:
        return frozenset()
    shared = set(paths[0])
    for path in paths[1:]:
        shared.intersection_update(path)
    return frozenset(shared)


def role_dominators(
    nodes: Iterable[ProjectionNode],
    edges: Iterable[ProjectionEdge],
    source: str,
    target: str,
) -> frozenset[str]:
    """Roles represented on every source->target path.

    Different concrete nodes may satisfy the same mandatory semantic role.
    """
    nodes_t = tuple(nodes)
    role_of = {node.name: node.role for node in nodes_t}
    paths = enumerate_paths(nodes_t, edges, source, target)
    if not paths:
        return frozenset()

    role_sets: list[set[str]] = []
    for path in paths:
        role_sets.append(
            {
                role_of[name]
                for name in path
                if role_of[name] is not None
            }
        )

    shared = role_sets[0]
    for roles in role_sets[1:]:
        shared.intersection_update(roles)
    return frozenset(shared)


def paths_missing_required_roles(
    nodes: Iterable[ProjectionNode],
    edges: Iterable[ProjectionEdge],
    source: str,
    target: str,
    required_roles: Iterable[str],
) -> tuple[tuple[str, ...], ...]:
    nodes_t = tuple(nodes)
    role_of = {node.name: node.role for node in nodes_t}
    required = frozenset(required_roles)
    paths = enumerate_paths(nodes_t, edges, source, target)

    invalid = []
    for path in paths:
        present = {
            role_of[name]
            for name in path
            if role_of[name] is not None
        }
        if not required <= present:
            invalid.append(path)
    return tuple(invalid)
