from dissociated_control_systems.projection_contract import (
    ClaimCeiling,
    EdgeGrounding,
    ProjectionEdge,
    can_present_as_empirical,
    claim_ceiling,
    unsupported_edges,
)


def edge(name: str, grounding: EdgeGrounding) -> ProjectionEdge:
    return ProjectionEdge(
        source=f"{name}:source",
        target=f"{name}:target",
        grounding=grounding,
        mapping_rule=name,
    )


def test_all_supported_path_can_be_presented_as_grounded() -> None:
    path = [
        edge("a", EdgeGrounding.SUPPORTED),
        edge("b", EdgeGrounding.SUPPORTED),
    ]

    assert claim_ceiling(path) is ClaimCeiling.GROUNDED
    assert can_present_as_empirical(path)


def test_one_assumed_intermediate_caps_path_at_model_only() -> None:
    path = [
        edge("a", EdgeGrounding.SUPPORTED),
        edge("b", EdgeGrounding.ASSUMED),
        edge("c", EdgeGrounding.SUPPORTED),
    ]

    assert claim_ceiling(path) is ClaimCeiling.MODEL_ONLY
    assert not can_present_as_empirical(path)


def test_unknown_edge_propagates_unknown_to_endpoint_claim() -> None:
    path = [
        edge("a", EdgeGrounding.SUPPORTED),
        edge("b", EdgeGrounding.UNKNOWN),
        edge("c", EdgeGrounding.SUPPORTED),
    ]

    assert claim_ceiling(path) is ClaimCeiling.UNKNOWN
    assert unsupported_edges(path)[0].grounding is EdgeGrounding.UNKNOWN


def test_falsified_bridge_falsifies_the_composed_projection() -> None:
    path = [
        edge("a", EdgeGrounding.SUPPORTED),
        edge("b", EdgeGrounding.FALSIFIED),
        edge("c", EdgeGrounding.SUPPORTED),
    ]

    assert claim_ceiling(path) is ClaimCeiling.FALSIFIED


def test_adding_supported_explanation_steps_cannot_rescue_assumption() -> None:
    assumed = edge("assumption", EdgeGrounding.ASSUMED)
    short_path = [
        edge("start", EdgeGrounding.SUPPORTED),
        assumed,
        edge("end", EdgeGrounding.SUPPORTED),
    ]
    longer_path = [
        edge("start", EdgeGrounding.SUPPORTED),
        edge("extra1", EdgeGrounding.SUPPORTED),
        assumed,
        edge("extra2", EdgeGrounding.SUPPORTED),
        edge("end", EdgeGrounding.SUPPORTED),
    ]

    assert claim_ceiling(short_path) is ClaimCeiling.MODEL_ONLY
    assert claim_ceiling(longer_path) is ClaimCeiling.MODEL_ONLY
