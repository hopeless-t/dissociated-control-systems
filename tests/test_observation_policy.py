from dissociated_control_systems.observation_policy import (
    ObservationCandidate,
    available_before_deadline,
    cvar_best_panel,
    decision_adjusted_loss,
    exhaustive_best_panel,
    expected_successful_value,
    greedy_information_per_burden,
    panel_fits_burden_ceiling,
    parallel_completion_time,
    robust_best_panel,
    sequential_completion_time,
    worst_case_confidence,
)


def test_greedy_can_miss_complementary_pair():
    candidates = (
        ObservationCandidate("A", 1.0),
        ObservationCandidate("B", 1.0),
        ObservationCandidate("C", 1.0),
    )

    # A and B are individually uninformative but jointly decisive.
    values = {
        (): 0.0,
        ("A",): 0.0,
        ("B",): 0.0,
        ("C",): 4.0,
        ("A", "B"): 10.0,
        ("A", "C"): 4.0,
        ("B", "C"): 4.0,
        ("A", "B", "C"): 10.0,
    }

    def value_fn(panel):
        return values[tuple(sorted(panel))]

    greedy = greedy_information_per_burden(candidates, value_fn, 2.0)
    exact = exhaustive_best_panel(candidates, value_fn, 2.0)

    assert greedy == ("C",)
    assert exact == ("A", "B")
    assert value_fn(exact) > value_fn(greedy)


def test_exhaustive_panel_obeys_budget_and_prefers_lower_burden_on_tie():
    candidates = (
        ObservationCandidate("A", 1.0),
        ObservationCandidate("B", 2.0),
        ObservationCandidate("C", 3.0),
    )

    def value_fn(panel):
        values = {
            (): 0.0,
            ("A",): 5.0,
            ("B",): 5.0,
            ("C",): 8.0,
            ("A", "B"): 8.0,
        }
        return values.get(tuple(sorted(panel)), 0.0)

    assert exhaustive_best_panel(candidates, value_fn, 3.0) == ("A", "B")


def test_information_arriving_after_deadline_is_not_decision_available():
    candidates = (
        ObservationCandidate("fast", burden=2.0, delay=1.0),
        ObservationCandidate("slow-strong", burden=2.0, delay=8.0),
    )

    available = available_before_deadline(
        candidates,
        current_time=0.0,
        decision_deadline=4.0,
    )

    assert tuple(item.name for item in available) == ("fast",)


def test_deadline_before_current_time_has_no_available_observation():
    candidates = (ObservationCandidate("x", burden=1.0, delay=0.0),)
    assert available_before_deadline(candidates, 5.0, 4.0) == ()


def test_parallel_panel_can_finish_when_sequential_panel_misses_deadline():
    panel = (
        ObservationCandidate("A", burden=1.0, delay=3.0),
        ObservationCandidate("B", burden=1.0, delay=3.0),
    )

    assert sequential_completion_time(panel) == 6.0
    assert parallel_completion_time(panel) == 3.0


def test_patient_specific_burden_ceiling_is_hard_constraint():
    panel = (
        ObservationCandidate("A", burden=2.0),
        ObservationCandidate("B", burden=3.0),
    )

    assert panel_fits_burden_ceiling(panel, 5.0)
    assert not panel_fits_burden_ceiling(panel, 4.9)


def test_failure_probability_reduces_expected_information_value():
    reliable = ObservationCandidate("reliable", burden=1.0, success_probability=1.0)
    fragile = ObservationCandidate("fragile", burden=1.0, success_probability=0.5)

    assert expected_successful_value(reliable, 8.0) == 8.0
    assert expected_successful_value(fragile, 8.0) == 4.0


def test_success_probability_is_bounded():
    try:
        ObservationCandidate("bad", burden=1.0, success_probability=1.1)
    except ValueError:
        pass
    else:
        raise AssertionError("success probability outside [0,1] must fail closed")


def test_robust_panel_can_differ_from_nominal_optimum():
    candidates = (
        ObservationCandidate("fragile", burden=1.0),
        ObservationCandidate("robust", burden=1.0),
    )

    def nominal(panel):
        return {("fragile",): 10.0, ("robust",): 7.0}.get(tuple(sorted(panel)), 0.0)

    def shifted(panel):
        return {("fragile",): -2.0, ("robust",): 7.0}.get(tuple(sorted(panel)), 0.0)

    assert exhaustive_best_panel(candidates, nominal, 1.0) == ("fragile",)
    assert robust_best_panel(candidates, (nominal, shifted), 1.0) == ("robust",)


def test_robust_panel_requires_declared_alternative_worlds():
    candidates = (ObservationCandidate("A", burden=1.0),)

    try:
        robust_best_panel(candidates, (), 1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("robust optimization without declared worlds must fail closed")


def test_tail_risk_can_reject_high_mean_fragile_panel():
    candidates = (
        ObservationCandidate("fragile", burden=1.0),
        ObservationCandidate("robust", burden=1.0),
    )

    def common(panel):
        return {("fragile",): 10.0, ("robust",): 6.0}.get(tuple(sorted(panel)), 0.0)

    def rare_bad(panel):
        return {("fragile",): -5.0, ("robust",): 6.0}.get(tuple(sorted(panel)), 0.0)

    def rare_good(panel):
        return {("fragile",): 9.0, ("robust",): 6.0}.get(tuple(sorted(panel)), 0.0)

    assert exhaustive_best_panel(candidates, common, 1.0) == ("fragile",)
    assert cvar_best_panel(
        candidates,
        (common, rare_bad, rare_good),
        (0.70, 0.15, 0.15),
        alpha=0.30,
        burden_budget=1.0,
    ) == ("robust",)


def test_one_unresolved_world_blocks_robust_high_confidence():
    assert worst_case_confidence((0.97, 0.95, 0.61)) == 0.61


def test_worst_case_confidence_requires_declared_worlds():
    try:
        worst_case_confidence(())
    except ValueError:
        pass
    else:
        raise AssertionError("robust confidence without plausible worlds must fail closed")


def test_waiting_cost_can_flip_preferred_observation():
    slow_strong_no_wait_cost = decision_adjusted_loss(
        prediction_loss=0.10,
        burden=1.0,
        delay=5.0,
        burden_weight=0.0,
        delay_weight=0.0,
    )
    fast_weak_no_wait_cost = decision_adjusted_loss(
        prediction_loss=0.20,
        burden=1.0,
        delay=1.0,
        burden_weight=0.0,
        delay_weight=0.0,
    )
    assert slow_strong_no_wait_cost < fast_weak_no_wait_cost

    slow_strong_with_wait_cost = decision_adjusted_loss(
        prediction_loss=0.10,
        burden=1.0,
        delay=5.0,
        delay_weight=0.03,
    )
    fast_weak_with_wait_cost = decision_adjusted_loss(
        prediction_loss=0.20,
        burden=1.0,
        delay=1.0,
        delay_weight=0.03,
    )
    assert fast_weak_with_wait_cost < slow_strong_with_wait_cost


def test_decision_adjusted_loss_rejects_negative_costs():
    try:
        decision_adjusted_loss(0.1, burden=1.0, delay=1.0, delay_weight=-0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative waiting-cost assumptions must fail closed")
