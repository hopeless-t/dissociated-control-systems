from dissociated_control_systems.projection_checkpoint_graph import (
    ProjectionEdge,
    ProjectionNode,
    node_dominators,
    paths_missing_required_roles,
    role_dominators,
)


def graph():
    nodes = [
        ProjectionNode("hypothesis"),
        ProjectionNode("source_a", role="provenance"),
        ProjectionNode("source_b", role="provenance"),
        ProjectionNode("state_a", role="state_response_typing"),
        ProjectionNode("state_b", role="state_response_typing"),
        ProjectionNode("uncertainty", role="uncertainty"),
        ProjectionNode("reachability", role="reachability"),
        ProjectionNode("claim"),
    ]
    edges = [
        ProjectionEdge("hypothesis", "source_a"),
        ProjectionEdge("hypothesis", "source_b"),
        ProjectionEdge("source_a", "state_a"),
        ProjectionEdge("source_b", "state_b"),
        ProjectionEdge("state_a", "uncertainty"),
        ProjectionEdge("state_b", "uncertainty"),
        ProjectionEdge("uncertainty", "reachability"),
        ProjectionEdge("reachability", "claim"),
    ]
    return nodes, edges


def test_concrete_alternative_nodes_need_not_dominate() -> None:
    nodes, edges = graph()
    dom = node_dominators(nodes, edges, "hypothesis", "claim")

    assert "source_a" not in dom
    assert "source_b" not in dom
    assert "state_a" not in dom
    assert "state_b" not in dom


def test_semantic_roles_can_dominate_despite_alternative_implementations() -> None:
    nodes, edges = graph()
    roles = role_dominators(nodes, edges, "hypothesis", "claim")

    assert {
        "provenance",
        "state_response_typing",
        "uncertainty",
        "reachability",
    } <= roles


def test_required_role_contract_accepts_all_valid_paths() -> None:
    nodes, edges = graph()

    invalid = paths_missing_required_roles(
        nodes,
        edges,
        "hypothesis",
        "claim",
        {
            "provenance",
            "state_response_typing",
            "uncertainty",
            "reachability",
        },
    )

    assert invalid == ()


def test_bypass_edge_exposes_missing_mandatory_role() -> None:
    nodes, edges = graph()
    edges = list(edges) + [
        # Unsafe shortcut skips uncertainty + reachability.
        ProjectionEdge("state_a", "claim"),
    ]

    invalid = paths_missing_required_roles(
        nodes,
        edges,
        "hypothesis",
        "claim",
        {
            "provenance",
            "state_response_typing",
            "uncertainty",
            "reachability",
        },
    )

    assert any(path[-2:] == ("state_a", "claim") for path in invalid)
