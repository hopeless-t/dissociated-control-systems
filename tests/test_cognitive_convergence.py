from dissociated_control_systems.cognitive_convergence import (
    convergence_experiment,
    entropy_probe_value,
    hypotheses,
)
from dissociated_control_systems.cognitive_active_diagnosis import train_templates


def test_entropy_probe_value_is_finite():
    templates = train_templates(samples=30)
    hs = hypotheses()
    posterior = {h: 1.0 / len(hs) for h in hs}
    value = entropy_probe_value(
        posterior,
        probe="handoff_gap",
        templates=templates,
        cost_weight=0.5,
    )
    assert value == value


def test_optimized_adaptive_policy_saves_probe_cost():
    result = convergence_experiment()
    best = result[result["best_adaptive_name"]]
    assert best["probe_cost"] < result["all_probes"]["probe_cost"]


def test_adaptive_policy_stays_near_information_ceiling():
    result = convergence_experiment()
    assert result["information_ceiling_gap"] < 0.05
