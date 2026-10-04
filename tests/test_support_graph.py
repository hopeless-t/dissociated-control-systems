import pytest

from dissociated_control_systems.support_graph import (
    SupportEdge,
    SupportNode,
    SupportNodeKind,
    claim_is_grounded,
    find_cycles,
    primitive_ancestors,
)


def test_direct_primitive_support_is_grounded() -> None:
    nodes = (
        SupportNode("data", SupportNodeKind.PRIMITIVE_EVIDENCE),
        SupportNode("claim", SupportNodeKind.CLAIM),
    )
    edges = (SupportEdge("data", "claim"),)

    assert claim_is_grounded("claim", nodes, edges)
    assert primitive_ancestors("claim", nodes, edges) == frozenset({"data"})


def test_derived_chain_remains_grounded_when_it_reaches_primitive_evidence() -> None:
    nodes = (
        SupportNode("raw", SupportNodeKind.PRIMITIVE_EVIDENCE),
        SupportNode("score", SupportNodeKind.DERIVED_EVIDENCE),
        SupportNode("claim", SupportNodeKind.CLAIM),
    )
    edges = (
        SupportEdge("raw", "score"),
        SupportEdge("score", "claim"),
    )

    assert primitive_ancestors("claim", nodes, edges) == frozenset({"raw"})
    assert claim_is_grounded("claim", nodes, edges)


def test_mutual_claim_support_is_detected_as_cycle() -> None:
    nodes = (
        SupportNode("a", SupportNodeKind.CLAIM),
        SupportNode("b", SupportNodeKind.CLAIM),
    )
    edges = (
        SupportEdge("a", "b"),
        SupportEdge("b", "a"),
    )

    cycles = find_cycles(nodes, edges)

    assert cycles
    assert not claim_is_grounded("a", nodes, edges)


def test_cycle_plus_primitive_evidence_is_still_not_accepted_as_grounded() -> None:
    nodes = (
        SupportNode("raw", SupportNodeKind.PRIMITIVE_EVIDENCE),
        SupportNode("a", SupportNodeKind.DERIVED_EVIDENCE),
        SupportNode("b", SupportNodeKind.CLAIM),
    )
    edges = (
        SupportEdge("raw", "a"),
        SupportEdge("a", "b"),
        SupportEdge("b", "a"),
    )

    assert find_cycles(nodes, edges)
    assert not claim_is_grounded("b", nodes, edges)


def test_primitive_ancestry_refuses_cyclic_graph() -> None:
    nodes = (
        SupportNode("a", SupportNodeKind.CLAIM),
        SupportNode("b", SupportNodeKind.CLAIM),
    )
    edges = (
        SupportEdge("a", "b"),
        SupportEdge("b", "a"),
    )

    with pytest.raises(ValueError):
        primitive_ancestors("a", nodes, edges)
