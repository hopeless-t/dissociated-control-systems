# RQ-005 META-A — Bognár 2024 Figure 2 identity audit

## Status

`OPEN_HIGH_PRIORITY`

This is a provenance audit, not a retraction claim and not a biological result.

## Three independent observations of the pooled OS result

The published record currently contains:

~~~text
Abstract        HR 0.97, 95% CI 0.87-1.08
Figure 2        HR 0.97, 95% CI 0.87-1.08
Results text    HR 1.01, 95% CI 0.95-1.07
~~~

The displayed Figure 2 study HRs and random-effects weights reconstruct a pooled
HR of approximately 0.971 on the log scale, which rounds to the displayed 0.97.

Therefore the figure's summary is arithmetically self-consistent with its
printed effect/weight columns. The main-text 1.01 value remains an unresolved
separate state.

Implementation:

- `src/dissociated_control_systems/meta_forest_audit.py`
- `tests/test_meta_forest_audit.py`

## Trial set visible in Figure 2

The OS panel visually lists 14 study labels:

~~~text
Zhang 2021
Bao 2019
Lu 2021
Kirkegaard 2023
Takano 2021
Goodwin 2001
Spiegel 2007
Edelman 1999
Guo 2013
Vanbutsele 2018
Kissane 2007
Wang 2019
Kuchler 2007
Kissane 2004
~~~

Normalized trial identities are frozen in
`tests/test_meta_trial_sets.py` and
`specs/RQ-005-META-A-RECONCILIATION.json`.

## Row identity conflicts

The figure appears to contain combinations of study label, randomized counts,
and effect values that do not all correspond to the same primary RCT.

### Goodwin 2001

Published primary trial:

~~~text
n = 235
intervention/control = 158/77
univariate HR = 1.06
95% CI = 0.78-1.45
~~~

Reference: Goodwin et al., NEJM 2001, PMID 11742045.

In the 2024 Figure 2 image, the row labelled Goodwin 2001 displays counts
114/113 and an HR around 0.93 rather than the primary-trial values above.

Notably, 114/113 are the randomized counts for the Andersen 2008 trial in the
2026 trial table.

### Kissane 2007

Published primary trial:

~~~text
n = 227
intervention/control = 147/80
univariate HR = 0.92
95% CI = 0.69-1.26
multivariable HR = 1.06
95% CI = 0.74-1.51
~~~

Reference: Kissane et al., Psycho-Oncology 2007, PMID 17385190.

In the 2024 Figure 2 image, the row labelled Kissane 2007 displays 158/77 and
HR 1.06 with CI approximately 0.78-1.45. That count/HR/CI combination matches
the **Goodwin 2001 univariate trial result**, not the Kissane 2007 trial.

### Kuchler 2007

The primary randomized trial enrolled 271 patients.
The 2026 reconciliation table identifies the randomization as 136/135.

Reference: Kuchler et al., JCO 2007, PMID 17602075.

In the 2024 Figure 2 image, the Kuchler row displays counts 214/114. Those are
the randomization counts of the Lu 2021 supportive-care trial.

## Current interpretation

The observations are compatible with several worlds:

~~~text
F0  visual transcription / rendering interpretation error
F1  labels were reordered separately from numeric columns
F2  sample-count columns use an undocumented analysis subset
F3  study/effect rows were joined incorrectly before plotting
F4  the publication figure and source analysis were generated from different
    data snapshots
F5  another explanation not yet observed
~~~

No world is privileged yet.

The exact source data / analysis code for the 2024 paper must be obtained before
calling this a confirmed plotting or data-binding bug.

## Why this matters

A meta-analysis requires identity preservation:

~~~text
Study Label
+ Randomized Population
+ Endpoint
+ Effect Estimate
+ Standard Error / CI
+ Follow-up Publication
= one coherent evidence record
~~~

If those fields become misbound, study-level moderator analysis and trial-level
comparison can become invalid even if the pooled arithmetic still closes.

Hence:

~~~text
Pooled Arithmetic Consistency != Row Identity Consistency
Forest Plot Looks Plausible != Evidence Records Are Correctly Bound
~~~

## Promotion gate

Before using Bognár 2024 study-specific values in META-A:

1. obtain the supplementary/source data;
2. assign stable `trial_id` and publication identity;
3. verify randomized counts against primary trials;
4. verify effect estimate and CI provenance;
5. reproduce the plotted order and pooled result;
6. explain the 0.97 versus 1.01 source split;
7. only then permit trial-level delta decomposition.

## Claim ceiling

This audit says nothing about whether psychosocial intervention prolongs cancer
survival. It only identifies an evidence-provenance problem that must be
resolved before the 2024 summary can be used as a clean quantitative anchor.
