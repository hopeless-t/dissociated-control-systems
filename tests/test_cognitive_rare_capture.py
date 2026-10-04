from dissociated_control_systems.cognitive_rare_capture import metrics


def test_capture_metrics_known_answer():
    rows = [
        {"rare": True},
        {"rare": False},
        {"rare": True},
        {"rare": False},
    ]
    result = metrics(rows, [0, 1])
    assert result["biopsy_count"] == 2
    assert result["rare_captured"] == 1
    assert result["rare_total"] == 2
    assert result["rare_recall"] == 0.5
    assert result["biopsy_precision"] == 0.5
    assert result["episodes_per_specimen"] == 2.0


def test_zero_capture_is_explicit_not_success():
    rows = [{"rare": True}, {"rare": False}]
    result = metrics(rows, [])
    assert result["biopsy_count"] == 0
    assert result["rare_captured"] == 0
    assert result["rare_recall"] == 0.0
    assert result["biopsy_precision"] == 0.0
    assert result["episodes_per_specimen"] == float("inf")
