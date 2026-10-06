# Cancer Latent-State Digital Twin v0.7 — model support / misspecification

Date: 2026-10-06
Status: simulation-stage falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_6_ENSEMBLE_ABSTENTION_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/cancer_support.py`
Known-answer tests: `tests/test_cancer_support.py`

## Meta-meta target

Attack the failure mode:

```text
all candidate models agree
AND
all candidate models are wrong
```

The research question is no longer only whether uncertainty is large.

It is whether the current forecast question lies inside the validated support of the model family at all.

## Support is not one scalar

v0.7 separates at least four distinct support questions:

```text
1. semantic support
   are observation times, assay lineage, censoring and treatment semantics valid?

2. feature / observation support
   does the observed trajectory lie near the validated observation manifold?

3. transition support
   do recent state transitions behave consistently with the candidate transition family?

4. model-family support
   is there evidence that the actual generating dynamics are represented by the candidate family?
```

Numerical predictive uncertainty is evaluated only after those structural gates.

## Synthetic campaign D — model-family support attack

A new deterministic private analysis trained a nominal longitudinal classifier on 60,000 virtual patients generated from the original simple treatment-response family.

Held-out nominal performance:

```text
AUC                         ~0.966
high-confidence coverage    ~68.4%
high-confidence error       ~1.8%
```

The classifier is only an attack surface, not a clinical model.

Four alternative generating families were then tested.

### Family B — logistic growth

A carrying-capacity term changed the mechanistic family while preserving much of the observed trajectory geometry.

```text
AUC                         ~0.956
high-confidence error       ~2.5%
```

Simple observation-space OOD and transition-residual detectors were close to chance.

Interpretation:

```text
Mechanistic Difference != Necessarily Observable Support Violation
```

A different equation can remain behaviorally equivalent on the measured surface.

### Family C — delayed treatment effect

The treatment effect ramped gradually rather than acting immediately.

```text
AUC                         ~0.938
high-confidence error       ~8.0%
```

Observation-space support distance detected this shift strongly:

```text
OOD detection AUC           ~0.992
transition-residual AUC     ~0.961
```

Using 99th-percentile nominal support thresholds rejected ~82% of this shifted family and reduced high-confidence error among retained high-confidence cases from ~7.8% to ~3.3%.

The cost was large coverage loss.

This demonstrates a real risk-coverage frontier rather than a free correction.

### Family D — immune-switch dynamics

A burden-dependent immune switch / exhaustion term changed transition dynamics.

```text
AUC                         ~0.965
high-confidence error       ~2.0%
```

Feature-support and simple residual detectors again stayed close to chance.

The measured surface was sufficiently similar that the mechanistic change was not meaningfully identifiable from the available observations.

### Family E — hidden future phenotype

This was the central adversarial family.

The patient trajectory was generated to be statistically similar to the nominal family through the full observed horizon, but a hidden aggressive phenotype altered resistant growth after the last observation.

The current observations therefore contained little or no pre-divergence signature of the future concept shift.

Result:

```text
forecast AUC                ~0.854
high-confidence error       ~15.8%
```

But support detectors failed:

```text
observation-space OOD AUC   ~0.505
transition-residual OOD AUC ~0.501
```

In other words, effectively chance.

A support gate based on those statistics rejected only ~1.5% and did not reduce high-confidence error; the retained high-confidence error remained ~16%.

A 12-member bootstrap ensemble also failed to rescue this class materially:

```text
ensemble disagreement error-detection AUC ~0.676
rejecting the top 10% most-disagreeing cases
    -> high-confidence error essentially unchanged (~16%)
```

## Structural no-go — observationally silent concept shift

The Family-E result is not merely an implementation bug.

If two worlds satisfy:

```text
P(z_0:t | world A) = P(z_0:t | world B)
```

for all observations currently available, but differ only in a future hidden transition parameter, then no inference algorithm using only `z_0:t` can uniquely distinguish them before divergence.

Therefore:

```text
No OOD Detector Can Recover Information That Is Not In The Observations
```

and:

```text
Low OOD Score != Validated Future Mechanism
Low Ensemble Disagreement != Model-Family Support
Good Transition Residual != Future Transition Law Identified
```

This is a core DCS non-identifiability result applied to oncology.

## New support taxonomy

The repository primitive returns typed statuses rather than one confidence penalty:

```text
SUPPORTED
SEMANTICS_UNKNOWN
FORECAST_UNDERSPECIFIED
OUT_OF_SUPPORT
TRANSITION_UNRESOLVED
UNCERTAIN
```

Ordering is deliberate:

```text
raw observation
 -> semantic contract
 -> future-intervention declaration
 -> feature / model-family support
 -> transition consistency
 -> predictive uncertainty
 -> forecast
```

A later layer cannot repair an earlier structural failure.

## Important distinction — detectable shift vs unknowable shift

Two classes must stay separate.

### Detectable support shift

Examples:

- timing drift;
- large calibration shift;
- delayed response producing trajectory residuals;
- new observation geometry outside the validated manifold.

These may justify:

```text
OUT_OF_SUPPORT
```

or:

```text
TRANSITION_UNRESOLVED
```

### Observationally silent concept shift

A hidden mechanism can preserve all current observables while changing later dynamics.

This cannot honestly be classified as detected OOD.

Correct behavior is instead to preserve a broader competing-world posterior and state that future transition-law identification is incomplete.

This may require:

- a new orthogonal biomarker;
- longer observation;
- mechanistically informative measurement;
- a clinically justified transition that exposes the difference;
- or an explicit irreducible-uncertainty statement.

## Theory correction — OUT_OF_SUPPORT is evidence-based

Do not emit `OUT_OF_SUPPORT` merely because the model is nervous.

Candidate rule:

```text
OUT_OF_SUPPORT
    requires positive evidence of support violation

UNKNOWN / TRANSITION_UNRESOLVED
    covers insufficient evidence to identify the relevant transition law
```

This prevents `OUT_OF_SUPPORT` from becoming a catch-all label for ignorance.

## Model-risk decomposition

The Twin now tracks at least:

```text
U_total =
    U_state
  + U_transition
  + U_sensor
  + U_semantics
  + U_intervention
  + U_model_form
```

The terms need not be numerically additive; the decomposition is typed.

`U_model_form` is especially important because within-family posterior width can be small even when the entire family is wrong.

## Ensemble correction

Ensemble disagreement estimates only disagreement inside the represented ensemble.

```text
Ensemble Agreement = Agreement Conditional On Candidate Family
```

not:

```text
Ensemble Agreement = Reality Support
```

For future work the ensemble should span genuinely different mechanistic families, but even that cannot solve an observationally silent alternative absent a discriminating observation.

## Observation policy update

The next-observation objective becomes:

```text
q* = argmax_q [
    expected_information_gain_over_competing_worlds(q)
  + lambda * model_discrimination(q)
  + gamma * counterfactual_decision_value(q)
  - mu * burden(q)
  - nu * delay_cost(q)
  - xi * redundancy(q)
]
```

The new term is `model_discrimination`.

The useful question is not only:

> which measurement narrows the current parameter posterior?

but also:

> which measurement best separates currently plausible model families that predict materially different futures?

## Literature alignment

Current medical digital-twin literature independently emphasizes that predictive accuracy alone is insufficient and that validation statements should specify target population, prediction horizon, supported interventions, uncertainty and known failure conditions.

Relevant public references for later qualification:

- PMID 42553720 — `Validating medical digital twins for clinical decision support: beyond predictive accuracy` (2026).
- PMID 39507514 — verifiable cancer digital-twin tissue-level modeling / VVUQ framework.
- npj Digital Medicine 2026, doi:10.1038/s41746-026-02656-9 — input harmonisation, continuous updating, revalidation and UQ in cancer-survivor digital-twin development.
- npj Precision Oncology 2026, doi:10.1038/s41698-026-01344-x — personalized response modeling and need for joint model/measurement uncertainty.

These sources support the validation philosophy, not the numerical results of this synthetic campaign.

## v0.7 convergence update

The architecture is now:

```text
Cancer Twin
=
Canonical Observation Semantics
+ Latent-State Inference
+ Transition-Law Inference
+ Sensor-Law Inference
+ Model-Support Gate
+ Counterfactual Simulator
+ Uncertainty / Abstention
```

The strongest new result is a no-go theorem in practical form:

> If a clinically important future mechanism leaves no distinguishable trace in any observation available before the decision point, no amount of model confidence, ensembling or OOD scoring can identify that mechanism. The research problem must then shift from better prediction to finding a new discriminating observation or declaring irreducible uncertainty.

## Next falsifiers

1. genuinely heterogeneous mechanistic ensemble rather than bootstrap replicas;
2. Bayesian model averaging over candidate dynamics;
3. active observation selection for model-family discrimination;
4. unknown treatment-history segments as latent inputs;
5. interval-censored clone likelihoods;
6. irregular-time native state-space inference;
7. model-form posterior collapse under correlated assay errors;
8. whether negative evidence from repeated measurements can meaningfully lower probability of hidden aggressive worlds;
9. explicit risk-coverage curves for `SUPPORTED` vs abstained cases;
10. test whether the support taxonomy remains stable across non-oncology DCS branches.

## Claim boundary

All numerical values are synthetic stress-test observations from declared toy model families. They are not clinical sensitivity, specificity, prognosis, treatment rules, or evidence for changing patient care.
