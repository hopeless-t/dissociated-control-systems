from dissociated_control_systems.cognitive_authority_frontier import (
    authority_frontier_experiment,
    required_specificity,
)


def test_required_specificity_increases_with_harm():
    q = 0.01
    t = 0.8
    values = [required_specificity(q, t, k) for k in (1, 2, 4, 8)]
    assert values == sorted(values)


def test_research_enrichment_can_coexist_with_action_ineligibility():
    result = authority_frontier_experiment()
    assert result["enrichment"] > 5.0
    assert result["biopsy_efficiency_gain"] > 5.0
    assert not any(result["action_eligible"].values())


def test_confusion_matrix_sums_to_population():
    result = authority_frontier_experiment()
    assert (
        result["tp"]
        + result["fp"]
        + result["tn"]
        + result["fn"]
        == 6400
    )
