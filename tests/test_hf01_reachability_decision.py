from dissociated_control_systems.hair_follicle_decision import (
    ReachabilityDecision,
    robust_reachability_decision,
)
from dissociated_control_systems.hair_follicle_longitudinal import (
    matched_visible_states,
)
from dissociated_control_systems.hair_follicle_model import HFControl


def test_equal_visible_output_is_unknown_when_latent_reachability_disagrees() -> None:
    recoverable, locked = matched_visible_states()
    control = HFControl(behavioral=1.0, antiandrogen=1.0)

    decision = robust_reachability_decision(
        [recoverable, locked],
        control=control,
    )

    assert decision is ReachabilityDecision.UNKNOWN


def test_resolved_recoverable_candidate_set_can_be_classified() -> None:
    recoverable, _ = matched_visible_states()
    control = HFControl(behavioral=1.0, antiandrogen=1.0)

    decision = robust_reachability_decision(
        [recoverable],
        control=control,
    )

    assert decision is ReachabilityDecision.RECOVERABLE


def test_resolved_locked_candidate_set_can_be_classified() -> None:
    _, locked = matched_visible_states()
    control = HFControl(behavioral=1.0, antiandrogen=1.0)

    decision = robust_reachability_decision(
        [locked],
        control=control,
    )

    assert decision is ReachabilityDecision.NONRECOVERABLE


def test_empty_evidence_set_is_unknown() -> None:
    control = HFControl(behavioral=1.0, antiandrogen=1.0)

    assert (
        robust_reachability_decision([], control=control)
        is ReachabilityDecision.UNKNOWN
    )
