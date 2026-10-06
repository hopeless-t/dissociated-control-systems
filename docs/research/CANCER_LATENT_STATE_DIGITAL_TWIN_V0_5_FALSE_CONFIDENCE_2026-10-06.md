# Cancer Latent-State Digital Twin v0.5 — false-confidence / observation semantics

Date: 2026-10-06
Status: simulation-stage working theory / adversarial checkpoint / not clinical authority
Parents:
- `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_3_ADVERSARIAL_2026-10-06.md`
- `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_4_COUNTERFACTUAL_2026-10-06.md`
Implementation support contract:
- `src/dissociated_control_systems/cancer_observation_contract.py`
- `tests/test_cancer_observation_contract.py`

## Meta-meta target

v0.5 promotes false confidence above average discrimination as the primary safety failure mode.

```text
High AUC != Safe Twin
Correct Rank Ordering != Calibrated Patient-Level Confidence
Model Probability != Permission To Emit High Confidence
```

Define, for confidence threshold `c`:

```text
FalseConfidenceRate(c)
  = P(prediction wrong | reported confidence >= c)
```

Also track the total population mass of high-confidence errors.

## Adversarial campaign C — observation semantics attack

A private deterministic analysis generated 80,000 virtual patients from the same broad v0.3-style family.

An apparent-response cohort was selected by observed day-30 imaging ratio:

```text
0.34 < imaging_30 / imaging_0 < 0.46
```

Cohort size: 26,693.
Held-out test set: 9,343.
Synthetic future-escape prevalence in the held-out nominal path: ~30.4%.

A multi-channel longitudinal logistic classifier was trained only as an attack surface. Features included day-14/day-30/day-60 imaging, ctDNA, resistance-signal, coarse immune, and host-state observations. It is not a proposed clinical model.

### Nominal held-out surface

```text
AUC                         ~0.955
Brier                       ~0.076
high-confidence coverage    ~66.7%
high-confidence error rate  ~2.23%
overall error               ~10.9%
```

The nominal result is deliberately strong so that failure under semantic corruption cannot be dismissed as a weak baseline model.

## Attack classes

### A. ctDNA calibration offset

A +0.40 log shift was applied to every serial ctDNA feature.

```text
AUC                         ~0.955
Brier                       ~0.077
high-confidence error rate  ~2.53%
```

Moderate one-channel calibration bias did not destroy the multi-channel model in this synthetic surface.

### B. resistance-sensor detectability collapse

Resistance observations were multiplied by 0.45 and small values were censored to zero in this adversarial approximation.

```text
AUC                         ~0.951
Brier                       ~0.079
high-confidence error rate  ~2.38%
```

This did not catastrophically fail because other longitudinal channels still carried information.

The modeling lesson is not that censoring is harmless. v0.5 instead replaces exact-zero substitution with explicit interval / below-detection-limit semantics in the repository support contract.

### C. correlated observation bias

A shared patient-level bias was injected across imaging, ctDNA, and immune observations.

```text
AUC                         ~0.955
Brier                       ~0.077
high-confidence error rate  ~2.21%
```

This particular bias family was largely absorbed by the chosen features. It remains a required adversarial class because other covariance structures can be destructive.

### D. time-label corruption

The feature slot called `day60` was replaced by a patient-specific mixture lying between the actual day30 and day60 observations, but was still presented to the model as `day60`.

```text
AUC                         ~0.900
Brier                       ~0.269
mean predicted escape       ~64.5%
true escape prevalence      ~30.4%
high-confidence error rate  ~21.3%
overall error               ~39.5%
```

This was much more destructive than the moderate value-domain perturbations.

### E. combined sensor + timing shift

ctDNA offset, common bias, resistance-detectability loss, censoring, and time-label corruption were combined.

```text
AUC                         ~0.889
Brier                       ~0.343
mean predicted escape       ~72.1%
true escape prevalence      ~30.4%
high-confidence error rate  ~36.3%
overall error               ~47.1%
```

The central failure was severe miscalibration and confident error, not total loss of rank ordering.

## Counterfactual support attack

The exact same nominal predictions were reused while the same day-60 latent states were propagated under different synthetic future treatment inputs.

Under a synthetic future-stop path:

```text
true future-escape prevalence    ~82.9%
AUC of stale nominal predictor   ~0.798
Brier                            ~0.470
high-confidence error rate       ~55.7%
```

The point is structural:

```text
A forecast can remain numerically confident while its intervention semantics are wrong.
```

Therefore `u_future` is part of forecast meaning, not an optional annotation.

## New invariant — semantic corruption dominates value noise in this attack surface

The campaign suggests a stronger debugging priority:

```text
Wrong Measurement Meaning > Moderate Measurement Noise
```

for the tested surface.

This is not claimed as a universal oncology law. It means that a Twin should fail closed on uncertain observation semantics before spending effort on increasingly precise values whose time, calibration lineage, censoring status, or treatment context are ambiguous.

## Canonical observation contract

Each observation should carry at least:

```text
modality
observed_at
calibration_id
value OR explicit censored-below-limit state
lower_detection_limit when relevant
```

The current dependency-free repository primitive enforces:

1. actual observation time is explicit;
2. a sample outside the declared timing tolerance cannot silently occupy another time slot;
3. calibration identity changes require an explicit bridge;
4. below-detection-limit observations do not masquerade as exact zero.

## Confidence Permission Gate

Do not transform a statistical probability into a high-confidence Twin statement unless support preconditions are satisfied.

Current synthetic support dimensions:

```text
timing semantics valid
calibration traceable
censoring accounted
treatment history complete
future intervention declared
model support declared
correlated-error model declared
```

Repository rule:

```text
any required support missing
    -> high confidence NOT permitted
```

This is intentionally a hard gate rather than multiplying a probability by arbitrary confidence penalties.

Candidate output contract:

```text
forecast posterior / scenario bundle
support_status
missing_support[]
observation lineage
model-family support
calibration state
```

A useful Twin must be able to return:

```text
FORECAST_UNDERSPECIFIED
OBSERVATION_SEMANTICS_UNKNOWN
CALIBRATION_BRIDGE_REQUIRED
CENSORED_OBSERVATION
OUT_OF_SUPPORT
```

instead of inventing precision.

## Detection-limit correction

The adversarial code that replaces low resistance signal with numeric zero is useful as an attack, but is not an acceptable canonical observation model.

Correct representation is interval-like:

```text
0 <= latent signal < LOD
```

rather than:

```text
latent signal = 0
```

The distinction matters especially when a below-detection resistant clone later expands.

## External-evidence alignment

Current literature reinforces the need to model observation semantics rather than biomarker values alone:

- PMID 42114037 / JCO Precision Oncology 2026: NGS ctDNA assays require analytical validation; low ctDNA abundance and CHIP complicate interpretation.
- PMID 41975767: cross-platform ctDNA comparability depends on measurand definition, pre-analytics, traceability, commutability, and stated uncertainty.
- PMID 42508231: longitudinal ctDNA sensitivity, specificity, and lead-time claims are time-dependent and vulnerable to analysis biases.
- PMID 42657157: serial PDAC ctDNA evidence remains heterogeneous across assay type and sampling windows.
- Nature Reviews Genetics 2026, doi:10.1038/s41576-026-00974-y: liquid biopsy remains limited by analytical validation and variable biological release processes.
- Journal of Computational Physics 2026, article 114937: predictive oncology digital twins require quantified uncertainty for patient-specific decision making.

These sources do not validate the synthetic DCS model; they support treating timing, assay identity, uncertainty, and longitudinal context as first-class measurement semantics.

## v0.5 architecture

The Twin is now explicitly five-part:

```text
x_t       latent biological state
Theta     patient-specific transition law
Phi       observation / sensor law
u         treatment history + declared future path
Omega     observation semantics / support metadata
```

Inference target:

```text
p(x_t, Theta, Phi | z_(0:t), u_(0:t), Omega_(0:t))
```

Forecast target:

```text
p(x_(t+1:T) | posterior_t, declared u_(t+1:T), support)
```

High-confidence output requires the support gate to pass.

## Next falsifiers

1. True missing treatment-history segments rather than future-path substitution.
2. Irregular observation intervals modeled natively instead of slot corruption.
3. Platform drift with imperfect calibration bridges.
4. Interval-censored clone observations and delayed expansion.
5. Non-Gaussian / correlated multi-assay errors.
6. Model-family misspecification where every candidate `F` is wrong.
7. Entire latent parameter regimes held out from training.
8. Selective prediction / abstention curves: coverage versus false-confidence rate.
9. Whether ensemble disagreement detects transition-law OOD before clinical divergence.
10. Whether an information-gain policy can choose the smallest next observation that restores forecast support.

## v0.5 convergence statement

The main safety object is no longer a prediction probability alone.

```text
Credible Forecast
=
posterior
+ transition-law support
+ sensor-law support
+ intervention semantics
+ observation semantics
+ calibrated uncertainty
```

The current simulation suggests that a cancer Twin should be designed to refuse unsupported confidence earlier than it is designed to maximize headline AUC.

## Claim boundary

All numerical values in this note are synthetic stress-test results from the declared toy analysis. They are not clinical performance estimates, diagnostic thresholds, prognosis, or treatment guidance.
