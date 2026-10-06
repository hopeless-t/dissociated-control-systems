from dataclasses import replace

from dissociated_control_systems.hair_follicle_model import (
    HFControl,
    simulate,
    state_from_lock,
)


def test_same_visible_output_can_have_opposite_recoverability() -> None:
    # Two states are made visually identical at the coarse H channel.
    # Their latent structural/progenitor/niche states remain different.
    recoverable = replace(state_from_lock(0.20), hair_output=0.50)
    locked = replace(state_from_lock(0.60), hair_output=0.50)

    assert recoverable.hair_output == locked.hair_output

    same_control = HFControl(behavioral=1.0, antiandrogen=1.0)
    recoverable_future = simulate(recoverable, same_control)
    locked_future = simulate(locked, same_control)

    assert recoverable_future.hair_output > 0.60
    assert locked_future.hair_output < 0.20
    assert recoverable_future.structural_lock < 0.05
    assert locked_future.structural_lock > 0.95


def test_output_only_markov_state_is_insufficient_for_declared_model() -> None:
    # If H alone were a sufficient Markov state, equal H plus equal input would
    # require the same deterministic future H. The declared model supplies a
    # counterexample.
    left = replace(state_from_lock(0.20), hair_output=0.50)
    right = replace(state_from_lock(0.60), hair_output=0.50)
    control = HFControl(behavioral=1.0, antiandrogen=1.0)

    left_future = simulate(left, control).hair_output
    right_future = simulate(right, control).hair_output

    assert abs(left_future - right_future) > 0.40
