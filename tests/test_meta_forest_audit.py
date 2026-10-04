import pytest

from dissociated_control_systems.meta_forest_audit import pooled_ratio_from_displayed_weights


def test_bognar_2024_figure2_displayed_values_reconstruct_pooled_hr() -> None:
    hrs = (
        0.51,
        0.65,
        0.68,
        0.68,
        0.83,
        0.93,
        0.93,
        0.96,
        1.00,
        1.03,
        1.06,
        1.12,
        1.15,
        1.35,
    )
    weights = (
        0.6,
        3.6,
        6.7,
        2.6,
        2.7,
        9.9,
        3.9,
        9.8,
        15.1,
        12.2,
        5.9,
        11.8,
        13.1,
        2.1,
    )

    pooled = pooled_ratio_from_displayed_weights(hrs, weights)
    assert pooled == pytest.approx(0.971, abs=0.001)
    assert round(pooled, 2) == 0.97


def test_forest_audit_rejects_weights_that_do_not_close() -> None:
    with pytest.raises(ValueError, match="sum"):
        pooled_ratio_from_displayed_weights([0.8, 1.0], [40.0, 40.0])
