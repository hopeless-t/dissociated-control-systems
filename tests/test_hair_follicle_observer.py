from dissociated_control_systems.hair_follicle_observer import (
    FULL_RESEARCH_SET,
    STATE_ORDER,
    TIER0,
    TIER0_PLUS_CONTEXT,
    TIER0_TO_PHYSIOLOGY,
    probe_rank,
)


def test_visible_hair_only_cannot_identify_latent_state() -> None:
    assert probe_rank(("visible_output",)) == 1
    assert len(STATE_ORDER) == 7


def test_noninvasive_observer_remains_rank_deficient() -> None:
    assert probe_rank(TIER0) == 3
    assert probe_rank(TIER0_PLUS_CONTEXT) == 4
    assert probe_rank(TIER0_TO_PHYSIOLOGY) == 5
    assert probe_rank(TIER0_TO_PHYSIOLOGY) < len(STATE_ORDER)


def test_declared_research_probe_set_is_full_rank() -> None:
    assert probe_rank(FULL_RESEARCH_SET) == len(STATE_ORDER)
