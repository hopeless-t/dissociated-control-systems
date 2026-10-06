# Cancer Latent-State Digital Twin v0.12 — deadline-aware observation acquisition

Date: 2026-10-06
Status: simulation-stage optimization / falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_11_ADAPTIVE_SEQUENTIAL_ACQUISITION_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/observation_policy.py`
Known-answer tests: `tests/test_observation_policy.py`

## Meta-meta target

v0.11 showed that adaptive observation can reduce expected burden, but that greedy acquisition can fail under complementarity.

v0.12 adds a second failure mode:

```text
High Information Gain != High Decision Value
```

An observation that arrives after the useful decision horizon may be scientifically informative but decision-useless for the current question.

## Synthetic deadline attack

The v0.11 synthetic competing-world model was reused with declared observation delays.

Illustrative synthetic delays:

```text
A+B bundle     delay 3
medium C       delay 1
strong D       delay 8
weak E         delay 1
weak F         delay 1
```

A hard decision horizon of 4 synthetic time units was imposed.

No delay corresponds to a real assay turnaround time.

## Delay-blind acquisition

The first policy selected observations using expected information gain per burden while ignoring whether the result would arrive before the decision deadline.

Approximate evaluation:

```text
AUC                         ~0.942
overall error               ~11.9%
resolved-by-deadline        ~59.8%
error among resolved        ~1.5%
average ordered burden      ~4.41
average burden whose result arrived too late ~2.41
```

The policy often ordered a high-information observation after the remaining decision time was already insufficient.

That burden was incurred in the toy accounting but the information could not affect the current decision.

## Deadline-aware acquisition

A second policy treated time-to-result as an acquisition constraint and considered only observations whose result could arrive before the deadline.

Approximate evaluation:

```text
AUC                         ~0.952
overall error               ~10.8%
resolved-by-deadline        ~65.4%
error among resolved        ~1.9%
average ordered burden      ~2.80
late-result wasted burden   0
```

The result is not that fast tests are universally better.

It is a counterexample to:

```text
Choose The Most Informative Available Observation Regardless Of Arrival Time
```

## Decision-horizon semantics

Observation value must therefore depend on at least:

```text
information content
patient burden
time to result
decision deadline
current posterior ambiguity
availability / failure probability
```

A candidate action `q` is decision-admissible only if:

```text
current_time + delay(q) <= decision_deadline
```

unless the scientific question explicitly concerns a later horizon.

The repository primitive now records observation `delay` and exposes a deterministic deadline-feasibility check.

## Distinguish scientific value from decision value

An observation can occupy one of several states:

```text
scientifically informative + decision timely
scientifically informative + decision late
scientifically weak + timely
scientifically weak + late
```

These must not collapse into one information-gain scalar.

Candidate decomposition:

```text
DecisionValue(q)
    = InformationValue(q)
    * Timeliness(q)
    * RelevanceToCurrentDecision(q)
```

This multiplicative form is conceptual only; hard constraints may be safer when deadlines are strict.

## Sequential policy correction

The acquisition loop becomes:

```text
current evidence
 -> competing worlds
 -> support / semantics validation
 -> declare current decision horizon
 -> generate candidate singleton + bundle observations
 -> reject candidates that cannot return in time
 -> score remaining candidates for conditional discrimination per burden
 -> acquire
 -> update posterior
 -> stop if ambiguity threshold is met or no timely informative observation remains
```

If no timely observation can resolve the ambiguity, the correct output is not forced certainty.

Candidate states include:

```text
TRANSITION_UNRESOLVED
DECISION_HORIZON_INSUFFICIENT
WAITING_FOR_QUALIFIED_OBSERVATION
```

The last state is meaningful only when the decision itself can safely wait.

## Clinical-research implication

The broader branch objective now has three competing resources:

```text
patient burden
information
calendar / decision time
```

Therefore:

```text
Minimum Intervention / Maximum Observability
```

is refined to:

```text
minimum burden
subject to sufficient decision-relevant identifiability
within the useful decision horizon
```

## New constrained optimization

For an observation policy `pi`:

```text
pi* = argmin_pi ExpectedBurden(pi)
```

subject to:

```text
DecisionAmbiguity_pi <= epsilon
FalseConfidenceRate_pi <= alpha
ResultArrival_pi <= DecisionDeadline
SemanticSupport = PASS
ModelSupport sufficient for declared question
```

If the constraints are infeasible, the simulator must report infeasibility / unresolved state rather than silently relaxing them.

## Interaction with v0.11 complementarity

Deadline awareness does not remove the complementarity problem.

A pair of low-delay observations may be jointly decisive even when each is individually weak.

Therefore candidate generation needs both:

- deadline filtering; and
- low-order bundle / complementarity search.

A fast singleton-greedy policy can still miss a valuable fast pair.

## Next falsifiers

1. stochastic turnaround time instead of fixed delay;
2. observation failure / redraw probability;
3. patient-specific burden ceiling driven by host reserve;
4. different decision horizons for different clinical questions;
5. compare myopic, pair-aware, beam-search and exact small-state dynamic programming;
6. quantify regret from waiting for a strong observation versus acting with current uncertainty;
7. model the value of deferring a decision when deferral itself has cost;
8. test whether repeated low-burden monitoring can dominate one delayed strong observation;
9. keep treatment-choice optimization outside this measurement-policy layer;
10. public-data qualification only after acquisition-policy assumptions stabilize.

## Claim boundary

All observations, delays, burden values, thresholds and performance numbers are synthetic. This note is a mathematical research-design result and does not rank real cancer tests, recommend procedures, or guide treatment timing.
