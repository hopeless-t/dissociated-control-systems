from dissociated_control_systems.cognitive_observation_stress import ObservationStressConfig, monte_carlo, simulate

def test_primary_bias_increases_gap():
    clean=simulate(ObservationStressConfig(name="c",mode="clean"),seed=0)
    biased=simulate(ObservationStressConfig(name="b",mode="biased_primary"),seed=0)
    assert biased.mean_abs_gap > clean.mean_abs_gap

def test_redundant_observer_recovers_calibration():
    biased=simulate(ObservationStressConfig(name="b",mode="biased_primary"),seed=0)
    redundant=simulate(ObservationStressConfig(name="r",mode="redundant"),seed=0)
    assert redundant.mean_abs_gap < biased.mean_abs_gap
    assert redundant.mean_function > biased.mean_function

def test_observability_invariant_is_preserved():
    for mode in ("clean","biased_primary","redundant"):
        row=simulate(ObservationStressConfig(name=mode,mode=mode),seed=0)
        assert row.max_observability_amplification <= 4.0 + 1e-12

def test_monte_carlo_redundancy_beats_biased_primary():
    r=monte_carlo(samples=100)
    assert r["redundant"]["p05_floor"] > r["biased_primary"]["p05_floor"]
    assert r["redundant"]["mean_abs_gap"] < r["biased_primary"]["mean_abs_gap"]
