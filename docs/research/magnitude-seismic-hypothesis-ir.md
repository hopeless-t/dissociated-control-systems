# Magnitude / Seismic lessons for DCS research methodology

## Why this belongs here

Magnitude's Seismic architecture is useful to DCS as a methodological reference: preserve semantics in one canonical layer, separate that meaning from implementation choices, make evidence scope explicit, and do not confuse incomplete search with falsification.

For DCS, the analogous problem is keeping a hypothesis stable while multiple mechanistic explanations, interventions, and measurement methods compete below it.

## 1. Canonicalize the hypothesis, not the favored mechanism

Represent a research claim separately from the mechanism currently believed to explain it.

```text
HypothesisIR
  phenomenon
  population/domain
  observables
  predicted relationships
  boundary conditions
  confounders
  falsifiers
  safety constraints
```

Candidate mechanisms then lower from the same hypothesis:

```text
HypothesisIR
  -> mechanism A
  -> mechanism B
  -> mechanism C
```

A mechanism can fail without forcing the phenomenon definition itself to drift.

## 2. One semantic registry for observables

Avoid redefining the same observable differently across experiments.

Each observable should own:

- operational definition
- units / scale
- sampling method
- uncertainty
- known confounders
- admissible transformations
- provenance

Derived metrics may project from this registry but must not silently replace the underlying meaning.

## 3. Separate model states

Use explicit epistemic states:

```text
Speculative
MechanisticallyPlausible
Testable
Observed
Replicated
Contradicted
Incomplete
OutOfScope
```

`Incomplete` is important: lack of enough evidence or inability to measure a variable is not the same as contradiction.

## 4. Candidate -> evidence -> selection

For each mechanistic explanation:

```text
CandidateMechanism
  assumptions
  predicted observables
  intervention predictions
  failure modes
  required evidence
```

Then evaluate candidates against the same observation set. Do not let each mechanism choose a different success criterion after seeing results.

## 5. Resource and safety constraints are part of admissibility

For human-subject or health-adjacent hypotheses, an intervention can be mathematically interesting but experimentally inadmissible.

Admission should include:

- safety risk
- reversibility
- measurement burden
- privacy
- consent requirements
- cost
- time
- expected information gain

This keeps exploration pressure below the safety and ethics boundary.

## 6. Preserve provenance through transformations

When raw observations become normalized measures, latent variables, or model inputs, keep the chain explicit:

```text
raw observation
  -> preprocessing
  -> derived feature
  -> model variable
  -> inference
```

Each transition should retain enough provenance to reconstruct which assumptions entered where.

## 7. Event/projection approach for research history

Use canonical research events such as:

```text
hypothesis.created
mechanism.proposed
prediction.registered
observation.recorded
analysis.completed
evidence.accepted
hypothesis.revised
```

A paper-style narrative, dashboard, simulation input, or agent context can then be generated as projections rather than becoming competing histories.

## 8. Proposed experiment

Take one existing DCS topic and encode:

1. one stable `HypothesisIR`;
2. at least three competing mechanisms;
3. shared observables;
4. predeclared falsifiers;
5. one evidence table;
6. explicit result states including `Incomplete`.

Then run the pseudo-Council against the same canonical record and compare whether disagreement becomes easier to localize.

## Working invariant

> Preserve the question and the observable semantics while allowing mechanisms, models, and interventions to compete underneath them.

That is the DCS analogue of keeping logical computation stable while allowing multiple physical lowerings.
