from dissociated_control_systems.skill_compiler import (
    CompiledSkill,
    replay_is_economical,
    select_compiled_skill,
)


def test_compiled_skill_applicability() -> None:
    skill = CompiledSkill(
        name="repose",
        required_tags=frozenset({"cat", "soft_support"}),
        replay_cost=2.0,
        discovery_cost=10.0,
        verification_cost=1.0,
        confidence=0.9,
    )
    assert skill.is_applicable({"cat", "soft_support", "editable"})
    assert not skill.is_applicable({"cat"})


def test_replay_savings_known_answer() -> None:
    skill = CompiledSkill(
        name="repose",
        required_tags=frozenset({"cat"}),
        replay_cost=2.0,
        discovery_cost=10.0,
        verification_cost=1.0,
        confidence=0.9,
    )
    assert skill.total_replay_cost == 3.0
    assert skill.one_replay_savings == 7.0


def test_skill_selection_prefers_confident_applicable_skill() -> None:
    low = CompiledSkill("low", frozenset({"cat"}), 1.0, 10.0, 1.0, 0.7)
    high = CompiledSkill("high", frozenset({"cat"}), 2.0, 10.0, 1.0, 0.9)
    assert select_compiled_skill((low, high), {"cat"}) == high


def test_no_applicable_skill_returns_none() -> None:
    skill = CompiledSkill(
        name="repose",
        required_tags=frozenset({"cat", "soft_support"}),
        replay_cost=2.0,
        discovery_cost=10.0,
        verification_cost=1.0,
        confidence=0.9,
    )
    assert select_compiled_skill((skill,), {"rigid_support"}) is None


def test_amortized_replay_can_be_economical() -> None:
    skill = CompiledSkill("repose", frozenset({"cat"}), 2.0, 10.0, 1.0, 0.9)
    assert replay_is_economical(skill, compile_cost=8.0, expected_uses=2)
