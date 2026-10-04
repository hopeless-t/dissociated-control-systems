from dissociated_control_systems.cognitive_governor import GovernorConfig, monte_carlo, simulate_governor

def test_hysteresis_reduces_switching_in_frozen_seed():
    naive=simulate_governor(GovernorConfig(name="n",mode="naive"),seed=0)
    hyst=simulate_governor(GovernorConfig(name="h",mode="hysteretic"),seed=0)
    assert hyst.switches < naive.switches

def test_bounded_governor_respects_observability_cap():
    row=simulate_governor(GovernorConfig(name="b",mode="bounded"),seed=0)
    assert row.max_observability_amplification <= 4.0 + 1e-12

def test_l3_improves_combined_failure_floor():
    base=simulate_governor(GovernorConfig(name="x",mode="none"),seed=0)
    bounded=simulate_governor(GovernorConfig(name="b",mode="bounded"),seed=0)
    assert bounded.minimum_function > base.minimum_function

def test_dual_track_preserves_more_latent_capability():
    bounded=simulate_governor(GovernorConfig(name="b",mode="bounded"),seed=0)
    dual=simulate_governor(GovernorConfig(name="d",mode="bounded",decline_rate_reduction=0.5),seed=0)
    assert dual.final_capability > bounded.final_capability

def test_monte_carlo_hysteresis_switching_and_tail_floor():
    r=monte_carlo(samples=100)
    assert r["hysteretic_l3"]["mean_switches"] < r["naive_l3"]["mean_switches"]
    assert r["bounded_l3"]["p05_floor"] > r["no_governor"]["p05_floor"]
    assert r["bounded_l3_dual_track"]["mean_final_capability"] > r["bounded_l3"]["mean_final_capability"]
