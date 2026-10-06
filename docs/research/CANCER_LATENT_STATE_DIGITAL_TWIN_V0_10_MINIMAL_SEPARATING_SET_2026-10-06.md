# Cancer Latent-State Digital Twin v0.10 — minimal sufficient separating set

Date: 2026-10-06
Status: simulation-stage optimization checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_9_WEAK_MARKER_COMPOSITION_2026-10-06.md`

## Meta-meta target

The branch principle is:

```text
Minimum Intervention / Maximum Observability
```

But v0.9 showed that many weak measurements can be redundant.

v0.10 asks a harder optimization question:

> What is the smallest-burden observation set that achieves a declared level of latent-world discrimination?

## Synthetic panel search

Eight abstract candidate observation channels were generated.

They deliberately varied in:

- hidden-world signal strength;
- acquisition burden / synthetic cost;
- independent noise;
- shared nuisance correlation.

The labels below are simulation labels only:

```text
1 strong / expensive channel
2 medium channels
3 independent weak channels
2 correlated low-cost channels
```

All non-empty subsets were enumerated exactly (`2^8 - 1 = 255` candidate panels).

A classifier was trained only to quantify hidden-world separability for the synthetic test.

No candidate represents a real biomarker or clinical procedure.

## Budget frontier

Approximate best hidden-world discrimination under each synthetic burden budget:

```text
budget <= 1    AUC ~0.675
budget <= 2    AUC ~0.718
budget <= 3    AUC ~0.769
budget <= 4    AUC ~0.808
budget <= 5    AUC ~0.827
budget <= 6    AUC ~0.843
budget <= 8    AUC ~0.941
budget <= 10   AUC ~0.953
```

At budget 8, the single strong channel became preferable to every lower-budget composition in this declared synthetic surface.

Even using all seven non-strong channels cost 11 synthetic burden units and achieved only about:

```text
AUC ~0.893
```

while the one strong channel at cost 8 achieved about:

```text
AUC ~0.941
```

This is not a universal claim that an invasive test is better than non-invasive panels.

It is a counterexample to the simpler rule:

```text
Many Low-Burden Measurements Always Dominate One High-Information Measurement
```

## Correct optimization statement

Do not minimize burden without an information constraint.

Candidate formulation:

```text
Q_min = argmin_Q Burden(Q)
subject to:
    ModelAmbiguity(Q) <= epsilon
    TransitionAmbiguity(Q) <= delta
    CounterfactualDecisionAmbiguity(Q) <= kappa
    SupportContract(Q) = PASS
```

Equivalent Lagrangian forms may be useful for exploration, but the constrained statement makes the clinical intent clearer:

> first declare how much unresolved ambiguity is tolerable; then minimize measurement burden.

## Pareto frontier

The Twin should report a typed frontier rather than collapse everything into one arbitrary utility score.

Candidate axes:

```text
patient burden
acquisition delay
model-family discrimination
transition-law discrimination
assay uncertainty
technical nuisance diversity
counterfactual decision value
```

A panel is dominated if another panel is no worse on every required axis and strictly better on at least one.

## Knee detection

A useful operating point may occur near a frontier knee where additional burden produces sharply diminishing information gain.

Candidate local quantity:

```text
MarginalInformationPerBurden
    = Delta model-discrimination / Delta burden
```

The simulation should search for a knee rather than assume a fixed number of tests.

## Strong-measurement exception

v0.9 emphasized composition of weak independent channels.

v0.10 adds the complementary result:

```text
Weak Independent Evidence Can Compose
BUT
A Strong Orthogonal Observation Can Dominate Many Weak Ones
```

Both statements can be true.

The choice is empirical and budget-dependent.

## Sequential rather than all-at-once acquisition

The static panel problem suggests a better clinical-research architecture:

```text
start with lowest-burden informative set
    -> update posterior
    -> if ambiguity below threshold: STOP
    -> else acquire next observation with maximal conditional value
    -> repeat
```

This can reduce expected patient burden relative to ordering the full panel for everyone.

Sequential policy:

```text
q_(t+1) = argmax_q
    ExpectedReductionInDecisionAmbiguity(q | evidence_t)
    / IncrementalBurden(q)
```

subject to safety, timing and support constraints.

## Stopping rule

Candidate stop conditions:

```text
1. required ambiguity threshold satisfied;
2. no remaining qualified observation has positive net decision value;
3. next observation arrives after the useful decision horizon;
4. patient burden exceeds declared ceiling;
5. structural non-identifiability remains despite all admissible observations.
```

Condition 5 must return explicit unresolved uncertainty, not force a recommendation.

## Research-design consequence

The simulator should eventually be able to produce output of the form:

```text
Current competing worlds:
    M1 / M2 / M3

Current decision ambiguity:
    above threshold

Lowest-burden next separating observation:
    property class q7

Expected model-family contraction:
    synthetic estimate + uncertainty

If q7 unavailable:
    next Pareto candidate q3 + q5

If burden ceiling forbids both:
    TRANSITION_UNRESOLVED
```

This keeps the model in an advisory scientific-instrument role.

## v0.10 convergence update

The phrase "minimum intervention" is now formalized as:

```text
minimum measurement burden
subject to sufficient decision-relevant identifiability
```

not:

```text
always choose the least invasive observation regardless of information content
```

The broader loop has therefore become:

```text
latent equivalence class
 -> competing future worlds
 -> support check
 -> candidate observation set
 -> conditional information / nuisance analysis
 -> burden-information Pareto frontier
 -> sequential acquisition
 -> stop when sufficient or explicitly unresolved
```

## Next falsifiers

1. dynamic-programming / greedy sequential acquisition against exact subset optimum;
2. test whether greedy information-per-burden can fail badly under interactions;
3. explicit delay cost and decision deadline;
4. patient-specific burden constraints rather than one global budget;
5. observation availability / assay failure;
6. integrate host-reserve state into measurement-burden tolerance;
7. compare static full-panel acquisition with adaptive sequential acquisition;
8. identify a qualified public dataset only after the simulation architecture stabilizes.

## Claim boundary

All observation channels, burden values and AUCs are synthetic. This note establishes an optimization counterexample and research-design principle only. It does not rank real clinical tests or recommend any cancer diagnostic, monitoring or treatment action.
