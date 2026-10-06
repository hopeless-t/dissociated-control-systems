# Cancer Latent-State Digital Twin v0.15 — informative missingness / no-result semantics

Date: 2026-10-06
Status: simulation-stage observation-model checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_14_ROBUST_MINIMAX_ACQUISITION_2026-10-06.md`
Implementation contract: `src/dissociated_control_systems/cancer_observation_contract.py`
Known-answer tests: `tests/test_cancer_observation_contract.py`

## Meta-meta target

v0.13 introduced observation success probability.

v0.15 attacks the simplifying assumption:

```text
No Result = Random Missing Data
```

If observation availability depends on latent state, sample quality, assay conditions, collection process, or biological detectability, then missingness itself can change inference.

This is an observation-model problem, not permission to interpret every missing result biologically.

## Synthetic MNAR campaign

A 100,000-patient binary competing-world simulation used:

- weak baseline evidence;
- one moderately informative synthetic marker;
- world-dependent probability that the marker was successfully observed.

Illustrative observation probabilities:

```text
World 1: P(observed) ~0.90
World 0: P(observed) ~0.50
```

The marker value itself was informative when observed.

Two inference modes were compared.

### Missingness ignored

No-result cases contributed no additional evidence.

Approximate result:

```text
AUC             ~0.840
overall error   ~25.3%
```

### Missingness modeled as part of the observation process

The likelihood included both:

```text
P(marker value | world, observed)
```

and:

```text
P(observed / no-result | world)
```

Approximate result:

```text
AUC             ~0.893
overall error   ~18.0%
```

These numbers are synthetic only.

## Structural lesson

The result does **not** mean:

```text
A missing clinical assay result should be treated as disease evidence.
```

It means:

```text
If missingness is not random,
then an inference model that silently treats it as random is misspecified.
```

The correct first task is to classify *why* the observation is absent.

## Canonical no-result taxonomy

The observation contract now distinguishes at least:

```text
measured
below_detection_limit
technical_failure
not_collected
insufficient_material
assay_unavailable
other explicit missing reason
```

An ambiguous bare `NULL` is rejected.

This prevents several invalid collapses:

```text
below detection limit == technical failure        # false
technical failure == not collected                # false
not collected == biologically absent              # false
below detection limit == exact zero                # false
```

## Why this matters for ctDNA-style observations

Current literature emphasizes that detectability is affected by both biological and technical factors, including:

- tumor burden;
- anatomical site;
- shedding / release biology;
- sampling time;
- assay sensitivity;
- clonal hematopoiesis and competing background signals;
- pre-analytical handling.

Therefore a negative or unavailable plasma signal cannot be interpreted safely without knowing which observation pathway produced it.

Relevant orientation sources for later qualification:

- PMID 42705053 (2026): review of ctDNA shedding, clearance and biological determinants of circulating abundance.
- PMID 42217421 (2026): review of biological and analytical limits on ctDNA sensitivity in lung cancer.
- PMID 41906224 (2026): pre-analytical factors affecting ctDNA integrity and concentration.
- PMID 42795008 (2026): review of ctDNA-MRD biology, false negatives, sampling timing and low-shedding histologies in early-stage NSCLC.

These sources support the observation-model caution, not the synthetic numerical results above.

## Missingness mechanism decomposition

Candidate latent missingness model:

```text
R_t = observation-availability indicator
```

with:

```text
P(R_t = 1 | x_t, Phi_t, Omega_t)
```

where:

```text
x_t     latent biological state
Phi_t   sensor / assay law
Omega_t collection + semantic context
```

Then:

```text
P(z_t, R_t | x_t, Phi_t, Omega_t)
```

is the canonical observation likelihood.

This is stronger than modeling only:

```text
P(z_t | x_t)
```

and imputing missing values later.

## MAR / MNAR distinction

The research harness should distinguish at least:

```text
MCAR-like synthetic failure
    missingness independent of state and observed covariates

MAR-like synthetic failure
    missingness explained by recorded context

MNAR-like synthetic failure
    missingness still depends on latent / unrecorded state after conditioning
```

These labels are methodological shorthand. Domain-specific assumptions must be independently justified.

## No-result information is typed, not automatically predictive

The Twin should not directly convert a missing reason into a prognosis.

Instead the missing reason determines which observation model is admissible.

Examples:

```text
technical_failure
    -> retry / assay-quality model may be relevant

not_collected
    -> acquisition-policy / workflow model

below_detection_limit
    -> censored likelihood

insufficient_material
    -> collection / specimen model
```

The biological posterior should change only when the declared generative model warrants it.

## Acquisition-policy consequence

Observation value now includes the probability of obtaining a usable result *and* the semantics of failure.

Candidate expected action value:

```text
E[V(q)] =
    P(measured) * V_measured
  + P(censored) * V_censored
  + P(technical_failure) * V_failure_state
  + P(no_collection) * V_workflow_state
  - burden
  - delay
```

This expression is conceptual.

A simple `raw_information * success_probability` helper remains in the repository only as a falsifiable baseline and explicitly warns that it is invalid when missingness is informative.

## Redraw / re-acquisition implication

Once missing reasons are typed, re-acquisition can be modeled rationally.

For example:

```text
technical failure
    -> repeat may have positive value

assay unavailable
    -> repeat same action may be pointless

below detection limit
    -> repeating immediately may be redundant unless timing or assay changes
```

These are policy categories, not clinical instructions.

## New no-go

```text
Do Not Impute All No-Result States To One Numeric Value
```

and:

```text
Do Not Treat Missingness As Random Without Testing The Missingness Model
```

This joins the earlier no-go:

```text
Below Detection Limit != Zero
```

## v0.15 convergence update

The observation layer now has three separate objects:

```text
1. measured value / censored interval
2. observation-availability process
3. semantic reason for non-measurement
```

The Twin should preserve all three before posterior inference.

## Next falsifiers

1. state-dependent technical failure versus biological low-shedding as competing worlds;
2. correlated failure across assays sharing one specimen / laboratory pipeline;
3. redraw value under deadline and burden constraints;
4. whether repeated technical failure should trigger `OBSERVATION_PIPELINE_OUT_OF_SUPPORT`;
5. model selection when missingness mechanism itself is uncertain;
6. robust policy under MNAR misspecification;
7. staged-batch acquisition with specimen-sharing dependencies;
8. explicit sample-quality latent state;
9. public-data qualification only after the missingness layer stabilizes;
10. maintain strict separation between observation-process inference and treatment decisions.

## Claim boundary

All synthetic missingness rates and performance values are research stress tests. They do not estimate real assay failure rates, diagnostic performance, prognosis, or treatment benefit.
