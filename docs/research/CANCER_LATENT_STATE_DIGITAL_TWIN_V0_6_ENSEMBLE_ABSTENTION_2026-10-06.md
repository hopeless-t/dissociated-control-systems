# Cancer Latent-State Digital Twin v0.6 — ensemble uncertainty is not a semantic validator

Date: 2026-10-06
Status: simulation-stage falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_5_FALSE_CONFIDENCE_2026-10-06.md`

## Question

Can ensemble disagreement alone detect the false-confidence failures exposed in v0.5?

A 12-member bootstrap logistic ensemble was trained on the nominal synthetic apparent-response cohort. The ensemble is only an uncertainty attack surface, not a proposed clinical architecture.

## Error-detection result

Using ensemble standard deviation as an error detector:

```text
nominal surface               error-detection AUC ~0.862
irregular-time corruption     error-detection AUC ~0.747
combined semantic/sensor shift error-detection AUC ~0.713
```

Ensemble disagreement detects some nominal difficult cases, but becomes materially less informative when the whole ensemble shares corrupted input semantics.

## Selective-prediction attack

Examples from the same held-out synthetic set:

### Nominal

Retaining only the 50% lowest-disagreement samples reduced overall error to ~0.75%.

### Irregular-time corruption

Retaining only the 50% lowest-disagreement samples still left:

```text
overall error               ~22.4%
high-confidence error rate  ~19.6%
```

Even retaining only the 25% lowest-disagreement samples left:

```text
overall error               ~8.5%
high-confidence error rate  ~8.5%
```

### Combined sensor + timing shift

Retaining only the 50% lowest-disagreement samples still left:

```text
overall error               ~32.7%
high-confidence error rate  ~31.6%
```

Even retaining only the 25% lowest-disagreement samples left ~15.7% high-confidence error in this attack surface.

These are synthetic numbers, not clinical estimates.

## Structural counterexample — intervention semantics

If the observed history and features are identical but `u_future` is omitted or silently changed, every ensemble member receives the same input vector.

Therefore ensemble agreement cannot, by itself, reveal that the forecast question changed.

Formally:

```text
same feature representation
+ different unrepresented future intervention semantics
-> same ensemble disagreement
+ different true counterfactual outcome
```

This is a structural limitation, not a weakness of bootstrap logistic regression specifically.

## New invariant

```text
Epistemic Disagreement != Input-Semantics Validation
Low Ensemble Variance != Supported Forecast
Abstention By Model Uncertainty != Fail-Closed Semantic Contract
```

The Twin therefore requires two independent gates:

### Gate A — semantic support

Validate:

- actual observation times;
- calibration lineage;
- censoring / detection-limit semantics;
- treatment history;
- declared future intervention path;
- measurement-surface identity.

### Gate B — predictive uncertainty

Only after Gate A passes, evaluate:

- posterior width;
- ensemble disagreement;
- model-family disagreement;
- out-of-support distance;
- calibration / coverage.

A failure in Gate A should not be repaired by a lower numerical confidence score. It should return an explicit unsupported state.

## Confidence architecture

Candidate order:

```text
raw observations
    -> semantic contract validation
    -> support / lineage check
    -> posterior inference
    -> model-family / ensemble uncertainty
    -> scenario propagation
    -> calibrated selective prediction
```

Not:

```text
raw observations
    -> black-box probability
    -> confidence penalty
```

## Implication for information gain

Expected information gain is meaningful only over correctly typed observations.

A mislabeled time point can appear highly informative while moving the posterior in the wrong direction.

Therefore:

```text
Semantic Validity precedes Information Gain
```

and candidate observation selection should optimize only over admissible, traceable measurement actions.

## Next falsifiers

1. Native irregular-time state-space inference using real `delta_t` instead of fixed time slots.
2. Ensemble across genuinely different mechanistic model families, not only bootstrap replicas.
3. Domain-shift detector trained on held-out parameter regimes.
4. Calibration-bridge uncertainty propagated rather than binary pass/fail.
5. Interval-censored clone likelihoods.
6. Missing treatment-history posterior rather than complete-case rejection.
7. Coverage-vs-risk curves under each corruption family.
8. Counterexample search where all model families agree and are wrong.

## Convergence update

v0.6 strengthens the architecture to:

```text
Cancer Twin
=
Semantic Validator
+ Latent-State Estimator
+ Transition-Law Estimator
+ Sensor-Law Estimator
+ Counterfactual Simulator
+ Uncertainty / Abstention Layer
```

The uncertainty layer is last, not first.

## Claim boundary

All numerical values are synthetic stress-test results. They are not estimates of clinical diagnostic or prognostic performance and cannot guide cancer treatment.
