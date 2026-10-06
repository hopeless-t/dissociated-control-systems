# Active Observation Policy for Partially Observable Systems

## Status

Open research note. This is a synthetic/modeling proposal, not a clinical protocol and not a recommendation for human experimentation.

## Core question

Dissociated Control Systems already studies cases where the same coarse observation can correspond to different hidden subsystem states.

The natural next question is:

> If two latent states are observationally confusable, which additional observation would distinguish them most efficiently?

This is an **active observation** problem.

## Passive versus active observation

Passive inference:

```text
existing observations
  -> infer latent-state distribution
```

Active observation:

```text
current latent-state uncertainty
  -> enumerate permitted candidate measurements
  -> estimate expected information gain
  -> choose one bounded measurement
  -> update latent-state distribution
  -> stop or repeat
```

The distinction matters because not every additional variable reduces the ambiguity that matters.

## Information-gain objective

Let hidden subsystem state be `S` and candidate observation be `O_i`.

```text
IG(O_i) = H(S | current evidence)
          - E[H(S | current evidence, O_i)]
```

A pure information-gain policy still ignores measurement cost and whether the resolved uncertainty affects the research decision.

A more complete research score is:

```text
score(O_i) =
    expected_information_gain(O_i)
    * expected_decision_relevance(O_i)
    * reliability(O_i)
    / max(measurement_cost(O_i), epsilon)
```

The exact form should be treated as a testable model, not a frozen truth.

## Connection to VAL-001

VAL-001 establishes latent-state non-identifiability under a coarse observer.

A candidate extension is:

```text
State A -> coarse y
State B -> coarse y

candidate probe p1 -> same distribution under A/B
candidate probe p2 -> sharply different distribution under A/B

=> p2 has greater discriminative value
```

This provides a clean synthetic benchmark for active observation without making claims about biological mechanisms.

## Candidate VAL-002 extension

For a finite hidden-state model:

1. generate state pairs that are intentionally confusable under the baseline observer;
2. define a bounded set of additional synthetic probes;
3. compute exact or enumerable posterior updates;
4. compare observation policies:
   - random probe;
   - cheapest probe;
   - maximum entropy of the raw measurement;
   - maximum expected information gain;
   - decision-relevant information gain;
5. measure probes required to reach a declared posterior-confidence threshold.

## Important distinction

```text
measurement entropy != latent-state information gain
```

A measurement can vary a lot while being useless for distinguishing the states we care about.

Likewise:

```text
latent-state information gain != action value
```

A measurement can identify a hidden difference that does not alter any downstream research decision.

Both distinctions should be explicit in the harness.

## Interaction effects

Two individually weak observations can be jointly decisive.

Therefore test:

```text
IG(O1) low
IG(O2) low
IG(O1, O2) high
```

A greedy one-probe policy may fail in such worlds.

This is especially important for dissociated systems because subsystem relations may be encoded in combinations rather than marginal observations.

## Observation provenance

Every synthetic or public-data observation should retain:

```text
source
measurement definition
sampling time / sequence position
data transformation
missingness state
reliability assumption
model version
```

A posterior without provenance should not be promoted into a canonical claim.

## Stop rules

An active observation loop must stop when:

- the declared posterior-confidence target is reached;
- remaining permitted observations cannot materially separate candidate states;
- observation budget is exhausted;
- model mismatch invalidates the observation-policy assumptions;
- contradictory evidence triggers escalation to a stronger validation path.

Failure to stop is not rigor.

## Medical / human-subject boundary

This document does not propose applying stimuli, withholding care, manipulating medication, inducing symptoms, or running tests on people.

For biological research lanes, active-observation methods may only be applied to appropriately qualified public datasets or to already-authorized study designs governed outside this repository.

The repository's synthetic validation track is the primary target for this proposal.

## Candidate principle

> **When observable behavior is ambiguous, do not collect more data indiscriminately. Seek the smallest permitted observation that separates the competing hidden-state explanations.**
