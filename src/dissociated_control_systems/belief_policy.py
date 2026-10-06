"""Small dependency-free belief-state policy primitives for DCS research.

The helpers support exact synthetic known-answer calculations over finite hidden
states. They are not clinical decision rules and do not encode cancer biology.
"""

from __future__ import annotations

from typing import Callable, Hashable, Mapping


State = Hashable
Outcome = Hashable
Belief = dict[State, float]
ObservationModel = Mapping[State, Mapping[Outcome, float]]


def normalize_belief(weights: Mapping[State, float]) -> Belief:
    values = {state: float(weight) for state, weight in weights.items()}
    if not values:
        raise ValueError("belief must contain at least one state")
    if any(weight < 0.0 for weight in values.values()):
        raise ValueError("belief weights must be >= 0")
    total = sum(values.values())
    if total <= 0.0:
        raise ValueError("belief must have positive total mass")
    return {state: weight / total for state, weight in values.items()}


def validate_observation_model(
    belief: Mapping[State, float],
    model: ObservationModel,
) -> tuple[Outcome, ...]:
    outcomes: set[Outcome] = set()
    for state in belief:
        if state not in model:
            raise ValueError("observation model missing hidden state")
        row = {outcome: float(prob) for outcome, prob in model[state].items()}
        if not row:
            raise ValueError("observation row must contain outcomes")
        if any(prob < 0.0 for prob in row.values()):
            raise ValueError("observation probabilities must be >= 0")
        if abs(sum(row.values()) - 1.0) > 1e-9:
            raise ValueError("observation probabilities must sum to 1 per state")
        outcomes.update(row)
    return tuple(sorted(outcomes, key=repr))


def predictive_outcome_distribution(
    belief: Mapping[State, float],
    model: ObservationModel,
) -> dict[Outcome, float]:
    prior = normalize_belief(belief)
    outcomes = validate_observation_model(prior, model)
    result = {outcome: 0.0 for outcome in outcomes}
    for state, state_prob in prior.items():
        row = model[state]
        for outcome in outcomes:
            result[outcome] += state_prob * float(row.get(outcome, 0.0))
    return result


def bayes_update(
    belief: Mapping[State, float],
    model: ObservationModel,
    outcome: Outcome,
) -> Belief:
    prior = normalize_belief(belief)
    validate_observation_model(prior, model)
    weighted = {
        state: state_prob * float(model[state].get(outcome, 0.0))
        for state, state_prob in prior.items()
    }
    if sum(weighted.values()) <= 0.0:
        raise ValueError("observed outcome has zero predictive probability")
    return normalize_belief(weighted)


def expected_terminal_loss_after_observation(
    belief: Mapping[State, float],
    model: ObservationModel,
    terminal_loss: Callable[[Belief], float],
) -> float:
    predictive = predictive_outcome_distribution(belief, model)
    total = 0.0
    for outcome, probability in predictive.items():
        if probability <= 0.0:
            continue
        posterior = bayes_update(belief, model, outcome)
        total += probability * float(terminal_loss(posterior))
    return total


def expected_two_stage_loss(
    belief: Mapping[State, float],
    first_model: ObservationModel,
    second_model_selector: Callable[[Belief], ObservationModel],
    terminal_loss: Callable[[Belief], float],
) -> float:
    """Evaluate an exact two-stage observe -> route -> observe policy."""

    predictive = predictive_outcome_distribution(belief, first_model)
    total = 0.0
    for outcome, probability in predictive.items():
        if probability <= 0.0:
            continue
        posterior = bayes_update(belief, first_model, outcome)
        second_model = second_model_selector(posterior)
        second_loss = expected_terminal_loss_after_observation(
            posterior,
            second_model,
            terminal_loss,
        )
        total += probability * second_loss
    return total
