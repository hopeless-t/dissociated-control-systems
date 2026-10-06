from dissociated_control_systems.binding_graph import (
    binding_summary,
    detect_cycle,
    walk_binding_path,
)


def test_long_cross_binding_chain_is_preserved() -> None:
    edges = {
        "WANG": "SPIEGEL",
        "SPIEGEL": "BAO",
        "BAO": "KUCHLER",
        "KUCHLER": "LU",
        "LU": "VANBUTSELE",
        "VANBUTSELE": "KISSANE2004",
        "KISSANE2004": "KIRKEGAARD",
        "KIRKEGAARD": "EDELMAN",
    }
    assert walk_binding_path(edges, "WANG") == (
        "WANG",
        "SPIEGEL",
        "BAO",
        "KUCHLER",
        "LU",
        "VANBUTSELE",
        "KISSANE2004",
        "KIRKEGAARD",
        "EDELMAN",
    )
    summary = binding_summary(edges)
    assert summary["cross_edge_count"] == 8
    assert summary["cycles"] == ()
    assert summary["longest_path"][0] == "WANG"
    assert summary["longest_path"][-1] == "EDELMAN"


def test_cycle_is_reported_without_infinite_walk() -> None:
    edges = {"A": "B", "B": "C", "C": "A"}
    assert detect_cycle(edges, "A") == ("A", "B", "C", "A")
    summary = binding_summary(edges)
    assert summary["cycles"] == (("A", "B", "C", "A"),)


def test_self_binding_is_not_counted_as_cross_binding() -> None:
    summary = binding_summary({"A": "A", "B": "C"})
    assert summary["self_edge_count"] == 1
    assert summary["cross_edge_count"] == 1
    assert summary["self_edges"] == ("A",)
