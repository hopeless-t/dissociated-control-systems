# RQ-005 Multi-state recurrence/control model

## Why the endpoint must be decomposed

Overall survival is a surface outcome. The same observed OS can be produced by
very different transition paths.

Example known answer:

~~~text
Path A:
  diagnosis -> recurrence at 150 months -> 30 months observed after recurrence

Path B:
  diagnosis -> recurrence at 24 months -> 156 months observed after recurrence

Both:
  OS = 180 months
~~~

Therefore:

~~~text
Same Overall Survival != Same Disease-Control Trajectory
Long-term Survival != Low Recurrence Hazard
~~~

## Minimal observed state graph

~~~text
                    +------------------+
                    | no recorded      |
                    | recurrence       |
                    +------------------+
                           ^
                           |
DIAGNOSIS --------------->| follow-up
   |
   | recurrence
   v
RECURRENT DISEASE --------------------> CANCER DEATH / CENSOR
       |
       +--> durable post-recurrence control
       +--> rapid post-recurrence failure
~~~

The model deliberately separates two clocks:

~~~text
T_R = time diagnosis -> recurrence
T_P = time recurrence -> death/censor

OS = T_R + T_P   when recurrence is observed
~~~

For patients without a recorded recurrence, `OS - RFS` must not be interpreted
as a post-recurrence interval.

## First trajectory ontology

~~~text
R0  no recorded recurrence
R1  late recurrence
R2  early recurrence + durable post-recurrence control
R3  early recurrence + rapid post-recurrence failure
RU  unresolved / insufficient observation
~~~

The thresholds used to project continuous times into R1/R2/R3 are research
projections and must be frozen before group comparison.

Implementation:

- `src/dissociated_control_systems/survivor_multistate.py`
- `tests/test_survivor_multistate.py`

## Competing mechanisms after recurrence

For R2 versus R3, at least the following worlds must compete:

~~~text
W-RX   recurrence topology / metastatic burden explains control
W-TX   treatment sequence / response depth explains control
W-BX   recurrent-tumor biology / evolutionary state explains control
W-IX   immune / metastatic-TME containment explains control
W-DX   dormancy / reactivation dynamics contribute
W-NX   systemic inflammatory / neuroendocrine state contributes
W-PX   psychological / agency state contributes through measured mediators
W-MIX  several layers interact nonlinearly
~~~

No world wins by being narratively attractive.

## External evidence constraining the candidate worlds

A 2025 metastatic-breast-cancer exceptional-responder cohort identified 58
patients with responses lasting more than twice expected PFS. CR/NED was
observed in 69% and was associated with better outcomes than partial response.
This makes depth of response / NED state a high-value observation before adding
more speculative hidden-state explanations.

Reference: PMID 39987798.

A 2026 multicountry Latin American cohort explicitly reset time zero at first
breast-cancer recurrence and reconstructed systemic treatment sequences for up
to six lines. Among 162 patients with documented first recurrence, median
post-recurrence overall survival was 24.0 months (IQR 9.6-45.6). The study also
stress-tested incomplete follow-up using best/worst-case censoring,
inverse-probability-of-censoring weighting, and competing-risk analysis.

This is methodologically aligned with the RQ-005 transition-specific direction:
post-recurrence control should be analyzed from recurrence rather than hidden
inside diagnosis-to-death OS.

Reference: PMID 42095205.

The METABRIC pilot sentinels MB-5566 and MB-4348 have observed
post-recurrence intervals above 181 months. They must not be numerically compared
as if they came from the same cohort or treatment era, but the contrast further
supports treating them as high-information rare residuals.

Recent dormancy reviews emphasize that disseminated tumor-cell dormancy and
reactivation are regulated by tumor-cell-intrinsic programs plus organ-specific
niche, stromal, extracellular-matrix, and immune interactions. The immune TME
can either constrain or facilitate dissemination, dormancy, reactivation, and
outgrowth depending on stage and cell state.

References:

- PMID 40628544
- PMID 39821034
- PMID 41855938
- PMID 42032160

These sources justify dormancy/TME as competing layers. They do not establish
that either mechanism explains the current METABRIC sentinel cases.

## New estimand split

The survivor program now has at least two distinct targets:

~~~text
Estimand A:
  what predicts time to first recurrence?

Estimand B:
  conditional on recurrence, what predicts subsequent control / death?
~~~

A variable may affect A but not B, or B but not A.

This is important for psychological, immune, treatment, and tumor-biology
variables alike. A single coefficient on overall survival can hide opposite or
stage-specific effects.

## Primary real-data direction

The preferred real-data architecture is a multi-state survival model rather
than a binary LTS/STS classifier:

~~~text
0 = diagnosis / disease controlled
1 = recurrence
2 = cancer death

lambda_01(t | z)  recurrence transition hazard
lambda_12(t | z)  post-recurrence death transition hazard
lambda_02(t | z)  optional direct cancer-death transition where justified
~~~

Time-varying state `z(t)` should be used when the data support it.

The current extreme LTS/STS classifier remains a discovery tool for locating
rare residuals, not the endpoint of inference.

## Falsification gates

A proposed R2 durable-control mechanism is downgraded if:

1. it disappears after recurrence site/burden and response depth are modeled;
2. it is visible only in the primary tumor but not in recurrent disease where
   paired observations exist;
3. it is measured after durable control is already established;
4. it cannot distinguish R2 from matched R3 cases;
5. it is cohort-specific and fails held-out replication;
6. it improves OS classification but not the transition it claims to explain.

## Claim ceiling

This model can organize transition paths and identify which observation would
best discriminate competing mechanisms.

It cannot establish an individual prognosis, prove dormancy in a specific
patient, or infer a psychological cancer-control mechanism from survival time.
