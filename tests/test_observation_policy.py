from dissociated_control_systems.observation_policy import (
    ObservationCandidate,
    available_before_deadline,
    exhaustive_best_panel,
    greedy_information_per_burden,
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
