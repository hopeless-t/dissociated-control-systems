# RQ-005 METABRIC pilot — first real-data survivor watershed pass

## Status

**EXPLORATORY PILOT / NON-CANONICAL MIRROR**

This pass exercises the RQ-005 survivor-divide method on real METABRIC-derived
clinical rows.

It is **not yet the canonical METABRIC result** because the accessible GitHub
mirror contains 1,897 rows, whereas the current cBioPortal/Zenodo clinical
patient object contains 2,509 patients.

The row-count mismatch is treated as a provenance failure gate, not silently
ignored.

## Source used for the pilot

~~~text
repository: SalvatoreRa/explanaibleAI
path:       tabular_methods/Data/metabric_clin.csv
blob SHA:   fd5a85a76ff51e42862913ae011fda6802c12832
rows:       1,897
~~~

The file reproduces cBioPortal-style METABRIC patient clinical fields.

Current canonical-source cross-check:

~~~text
cBioPortal brca_metabric: 2,509 patients
Zenodo 2026 clinical mirror: 2,509 patient rows
pilot GitHub mirror: 1,897 rows
~~~

Therefore all numerical findings below have ceiling:

REAL_DATA_METHOD_PILOT, not CANONICAL_METABRIC_FINDING.

## Frozen discovery contrast

To avoid assigning outcomes to insufficiently followed censored patients:

~~~text
STS:
  Died of Disease
  AND OS_MONTHS <= 60

LTS:
  OS_MONTHS >= 120

otherwise:
  UNCLASSIFIED
~~~

This gives:

~~~text
LTS            906
STS            324
UNCLASSIFIED   667
~~~

The contrast is retrospective and deliberately extreme.

## First-order divergence

| Variable | LTS | STS | standardized difference |
| --- | ---: | ---: | ---: |
| positive lymph nodes, mean | 1.164 | 4.346 | -0.829 |
| Nottingham prognostic index, mean | 3.803 | 4.769 | -0.895 |
| age at diagnosis, mean | 59.159 | 59.297 | -0.011 |

The age contrast is essentially absent while node burden and NPI show large
group separation.

Subtype composition also differs strongly:

~~~text
LumA        LTS 41.6%   STS 14.2%
Basal       LTS  9.2%   STS 21.6%
HER2-like   LTS  9.2%   STS 21.3%
~~~

These are discovery contrasts, not adjusted causal effects.

## Within-subtype check

The NPI/node-burden separation does not disappear when inspecting major
intrinsic subtypes separately.

Examples:

~~~text
Basal:
  NPI    4.539 LTS vs 4.961 STS
  nodes  1.627 LTS vs 3.614 STS

LumA:
  NPI    3.493 LTS vs 4.176 STS
  nodes  0.989 LTS vs 4.609 STS

LumB:
  NPI    3.952 LTS vs 4.706 STS
  nodes  1.369 LTS vs 3.738 STS

HER2-like:
  NPI    4.016 LTS vs 4.939 STS
  nodes  0.964 LTS vs 5.029 STS
~~~

This strengthens tumor-biology/burden as a serious first competing world.

## Block-held-out model ladder

COHORT was used only as a holdout block, not as a predictive feature.

Pooled leave-one-cohort-out results:

| Model | AUC | log loss |
| --- | ---: | ---: |
| intercept | 0.443* | 0.579 |
| age | 0.432 | 0.582 |
| treatment context | 0.650 | 0.548 |
| tumor / clinical biology | **0.780** | 0.481 |
| combined biology + treatment context | **0.782** | **0.478** |

*Each intercept-only fold has AUC 0.5. The pooled intercept AUC is distorted
by differing base rates across held-out cohorts and must not be interpreted as
ranking ability.

The important comparison is:

~~~text
tumor-basic AUC     0.780
combined AUC        0.782
~~~

Within this crude pilot, adding recorded chemotherapy/hormone/radiotherapy
context to the tumor/clinical baseline adds little discrimination.

This is **not** evidence that treatment does not matter. Treatment assignment is
strongly confounded by indication and treatment variables are too coarse for a
causal treatment model.

## Rare residual biopsy

Using the block-held-out tumor/clinical model:

~~~text
unexpected LTS:
  actual LTS
  AND model p(LTS) < 0.25

unexpected STS:
  actual STS
  AND model p(LTS) > 0.75
~~~

Counts:

~~~text
unexpected LTS   15
unexpected STS   89
~~~

The unexpected-LTS group is especially useful for DCS:

~~~text
mean positive nodes   14.4
mean NPI               5.94
recurrence rate        60%
~~~

compared with all LTS:

~~~text
mean positive nodes    1.16
mean NPI               3.80
recurrence rate        25.4%
~~~

These are high-risk-looking tumors that nevertheless crossed the 10-year
follow-up threshold.

Selected specimens include:

~~~text
MB-7297
  p(LTS)=0.005
  nodes=45
  NPI=6.05
  LumB
  OS=176 months
  Died of Disease
  recurrence at 121.18 months

MB-0589
  p(LTS)=0.049
  nodes=25
  NPI=5.07
  LumB
  OS=125.8 months
  alive at last follow-up
  recurrence at 2.04 months

MB-5566
  p(LTS)=0.183
  nodes=14
  NPI=6.064
  Basal
  OS=234.4 months
  alive at last follow-up
  recurrence at 20.23 months

MB-5294
  p(LTS)=0.194
  nodes=14
  NPI=6.198
  Basal
  OS=195.9 months
  alive at last follow-up
  no recorded recurrence
~~~

These are not "mind-over-cancer" cases.

They are precisely the cases where a coarse clinical biology model is missing
state.

## New DCS interpretation

The first real-data pass suggests a layered decomposition:

~~~text
population:
  tumor burden / subtype explains substantial survivor separation

residual:
  some patients violate that coarse mapping strongly

therefore:
  Outcome != Coarse Tumor State
~~~

The residual may contain:

- unmeasured genomic state;
- treatment detail/timing;
- immune/TME structure;
- metastatic-site biology;
- endocrine state;
- adherence/exposure;
- measurement error;
- hidden selection/provenance effects;
- psychological/neuroendocrine pathways;
- interactions among these.

No one residual mechanism is privileged.

## Meta-loop corrections triggered by this pilot

### 1. Provenance before performance

A model score is not promotable while the input snapshot is version-ambiguous.

New invariant:

~~~text
Model Reproducibility
  requires
Data Snapshot Identity
~~~

### 2. Use residuals as rare specimens

Do not optimize AUC first.

Freeze high-confidence model violations before increasing model complexity.

~~~text
simple baseline
 -> high-residual specimen
 -> causal-history reconstruction
 -> new observation
 -> refit
~~~

### 3. Treatment variables are context, not treatment effects

Observed chemotherapy use is much more common in STS than LTS in this pilot.
That almost certainly contains confounding-by-indication.

Therefore:

~~~text
treatment association
!= treatment harm
~~~

No causal interpretation is allowed without a treatment-aware design.

### 4. Canonical rerun is mandatory

The next METABRIC promotion gate requires rerunning the exact frozen pipeline on
the 2,509-patient canonical clinical snapshot and documenting row-level
inclusion/exclusion deltas relative to the 1,897-row pilot mirror.

## Reproducers

- analysis/rq005_metabric_baseline.py
- analysis/rq005_metabric_model_ladder.py
- src/dissociated_control_systems/survivor_baseline.py

The scripts make no network requests and require the data snapshot to be passed
explicitly.
