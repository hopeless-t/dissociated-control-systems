from dissociated_control_systems.cognitive_context_authority_freshness import (
    MAX_EPOCH_SELECTION_REGRET,
    context_authority_freshness_experiment,
)


def test_every_epoch_requalification_preserves_regret_contract():
    result = context_authority_freshness_experiment()
    lease1 = result["policies"]["lease1"]
    assert lease1["contract_pass"]
    assert lease1["max_regret"] <= MAX_EPOCH_SELECTION_REGRET
    assert lease1["stale_authority_epochs"] == 0


def test_one_time_authority_becomes_stale_after_reliability_shift():
    result = context_authority_freshness_experiment()
    static = result["policies"]["static_once"]
    assert not static["contract_pass"]
    assert static["max_regret"] > 0.20
    assert static["stale_authority_epochs"] >= 6


def test_shorter_freshness_leases_reduce_mean_regret():
    result = context_authority_freshness_experiment()
    policies = result["policies"]
    assert policies["static_once"]["mean_regret"] > policies["lease4"]["mean_regret"]
    assert policies["lease4"]["mean_regret"] > policies["lease2"]["mean_regret"]
    assert policies["lease2"]["mean_regret"] > policies["lease1"]["mean_regret"]


def test_qualification_cost_grows_as_lease_shortens():
    result = context_authority_freshness_experiment()
    policies = result["policies"]
    assert policies["static_once"]["qualifications"] == 1
    assert policies["lease4"]["qualifications"] == 3
    assert policies["lease2"]["qualifications"] == 5
    assert policies["lease1"]["qualifications"] == 10


def test_fresh_gate_revokes_and_restores_context_authority():
    result = context_authority_freshness_experiment()
    rows = result["policies"]["lease1"]["rows"]
    assert rows[0]["selected_policy"] == "context_normalized"
    assert all(row["selected_policy"] == "raw_function" for row in rows[1:7])
    assert all(row["selected_policy"] == "context_normalized" for row in rows[7:])
