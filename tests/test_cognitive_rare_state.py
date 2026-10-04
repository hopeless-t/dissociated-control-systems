from dissociated_control_systems.cognitive_rare_state import (
    THRESHOLD_GRID,
    dataset,
    pooled_rate,
    select_threshold,
    stratum_rates,
)


def test_rare_state_small_census_contract():
    rows = dataset(3, 2_900_000_000)
    threshold, rate = select_threshold(rows)
    assert threshold in THRESHOLD_GRID
    assert 0.0 <= rate <= 1.0
    assert pooled_rate(rows, threshold) == rate


def test_small_census_reports_every_fault_stratum():
    rows = dataset(2, 2_910_000_000)
    threshold, _ = select_threshold(rows)
    rates = stratum_rates(rows, threshold)
    assert len(rates) == 16
    for row in rates.values():
        assert row["total"] == 2
        assert 0.0 <= row["rate"] <= 1.0
