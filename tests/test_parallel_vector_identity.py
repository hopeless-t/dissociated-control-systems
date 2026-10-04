import pytest

from dissociated_control_systems.parallel_vector_identity import (
    alignment_summary,
    keyed_vector,
    length_only_compatible,
    require_identity_alignment,
)


def test_equal_length_does_not_imply_evidence_identity() -> None:
    effects = keyed_vector(
        "log_hr",
        ["A", "B", "C", "D"],
        [-0.4, -0.1, 0.2, 0.5],
    )
    counts = keyed_vector(
        "n_e",
        ["B", "C", "D", "A"],
        [50, 60, 70, 80],
    )

    assert length_only_compatible(effects, counts) is True
    with pytest.raises(ValueError, match="evidence identity mismatch"):
        require_identity_alignment(effects, counts)


def test_same_identity_order_passes() -> None:
    trial_ids = ["A", "B", "C"]
    effects = keyed_vector("log_hr", trial_ids, [-0.2, 0.0, 0.2])
    se = keyed_vector("se", trial_ids, [0.1, 0.2, 0.3])
    counts = keyed_vector("n_e", trial_ids, [100, 90, 80])
    require_identity_alignment(effects, se, counts)


def test_bognar_style_count_vector_can_pass_length_gate_and_fail_identity_gate() -> None:
    labels = (
        "ZHANG_L_2021",
        "BAO_2019",
        "LU_2021",
        "KIRKEGAARD_2023",
        "TAKANO_2021",
        "GOODWIN_2001",
        "SPIEGEL_2007",
        "EDELMAN_1999",
        "GUO_Z_2013",
        "VANBUTSELE_2018",
        "KISSANE_2007",
        "WANG_J_2019",
        "KUCHLER_1999_2007",
        "KISSANE_2004",
    )
    count_sources = (
        "ZHANG_L_2021",
        "KUCHLER_1999_2007",
        "VANBUTSELE_2018",
        "EDELMAN_1999",
        "CUNNINGHAM_1998",
        "ANDERSEN_2008",
        "BAO_2019",
        "UNKNOWN_POPULATION",
        "GUO_Z_2013",
        "KISSANE_2004",
        "GOODWIN_2001",
        "SPIEGEL_2007",
        "LU_2021",
        "KIRKEGAARD_2023",
    )
    effects = keyed_vector("effect_rows", labels, range(14))
    counts = keyed_vector("displayed_population_counts", count_sources, range(14))

    summary = alignment_summary(effects, [counts])
    assert summary["vectors"]["displayed_population_counts"]["length_only_compatible"] is True
    assert summary["vectors"]["displayed_population_counts"]["identity_aligned"] is False
    assert summary["vectors"]["displayed_population_counts"]["mismatch_count"] == 12


def test_duplicate_trial_ids_fail_closed() -> None:
    with pytest.raises(ValueError, match="unique"):
        keyed_vector("bad", ["A", "A"], [1, 2])
