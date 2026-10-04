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

## Full-row count identity audit

The publication Figure 2 rows were frozen in:

- `specs/RQ-005-META-A-BOGNAR-FIG2-AUDIT.json`

Canonical comparator records were taken from primary RCT reports and the 2026
Asakawa-Haas trial table where available.

Important identity distinction:

~~~text
Trial identity
!=
Population snapshot identity
~~~

For example, Edelman 1999 has an initial randomized allocation of 62/62 and a
later survival-analysis population of 60/61 after exclusions. Both remain one
trial with two evidence snapshots.

Executable audit:

- `src/dissociated_control_systems/evidence_binding.py`
- `src/dissociated_control_systems/binding_graph.py`
- `analysis/rq005_bognar_fig2_binding_audit.py`
- `tests/test_evidence_binding.py`
- `tests/test_binding_graph.py`

Using exact intervention/control count matching, the frozen 14 rows classify as:

~~~text
count identity matches displayed trial          2 / 14
count identity matches a different known trial 11 / 14
count identity unresolved                       1 / 14
~~~

When effect identity is also considered, the current automated status count is:

~~~text
OWN_IDENTITY_CONSISTENT                 1
COUNT_CROSS_BINDING_CANDIDATE           6
CROSS_BINDING_CANDIDATE                 5
EFFECT_SOURCE_CONFLICT_OR_DERIVATION    1
UNRESOLVED_IDENTITY                     1
~~~

`candidate` is deliberate. Exact count reuse identifies a provenance pattern;
it does not identify the mechanism that created it.

## Count-binding graph

Unique exact cross-trial count matches form a nontrivial directed pattern.
The longest currently observed path is:

~~~text
WANG_J_2019
 -> SPIEGEL_2007
 -> BAO_2019
 -> KUCHLER_1999_2007
 -> LU_2021
 -> VANBUTSELE_2018
 -> KISSANE_2004
 -> KIRKEGAARD_2023
 -> EDELMAN_1999
~~~

This is 8 cross-binding edges spanning 9 trial identities.

Two shorter branches currently include:

~~~text
KISSANE_2007 -> GOODWIN_2001 -> ANDERSEN_2008
TAKANO_2021  -> CUNNINGHAM_1998
~~~

No causal or software-bug interpretation follows from graph length alone.
The graph exists to make a systematic identity pattern falsifiable.

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
F2  sample-count columns use undocumented analysis subsets
F3  study/effect/count fields were joined incorrectly before plotting
F4  publication figure and source analysis came from different data snapshots
F5  a deterministic ordering/permutation rule exists but has not been identified
F6  another explanation not yet observed
~~~

No world is privileged yet.

The exact source data / analysis code for the 2024 paper must be obtained before
calling this a confirmed plotting or data-binding bug.

## Why this matters

A meta-analysis requires identity preservation:

~~~text
Trial identity
+ Population snapshot
+ Endpoint
+ Effect estimate
+ Standard error / CI
+ Follow-up publication
= one coherent evidence record
~~~

If those fields become misbound, study-level moderator analysis and trial-level
comparison can become invalid even if the pooled arithmetic still closes.

Hence:

~~~text
Pooled Arithmetic Consistency != Row Identity Consistency
Aggregate Observable != Correct Internal Binding
Population Snapshot != New Randomization
Forest Plot Looks Plausible != Evidence Records Are Correctly Bound
~~~

## Next falsification tests

The count-binding graph creates concrete tests rather than a visual suspicion:

1. recover the original supplementary/source table order;
2. ask whether the observed cross-binding graph is reproduced by a single
   column-wise sort/permutation;
3. test whether effect columns, count columns, and labels each correspond to a
   different stable ordering;
4. distinguish randomized counts from endpoint-specific analysis counts;
5. verify every apparent match against the primary randomized population;
6. repeat the reconstruction from the authors' raw source artifact if obtained.

If no simple permutation explains the graph, `F1/F5` are downgraded and the
source-snapshot/join worlds gain relative priority.

## Promotion gate

Before using Bognár 2024 study-specific values in META-A:

1. obtain the supplementary/source data;
2. assign stable `trial_id`, population snapshot, and publication identity;
3. verify randomized/analysis counts against primary trials;
4. verify effect estimate and CI provenance;
5. reproduce the plotted order and pooled result;
6. explain the 0.97 versus 1.01 source split;
7. only then permit trial-level delta decomposition.

## Claim ceiling

This audit says nothing about whether psychosocial intervention prolongs cancer
survival. It only identifies an evidence-provenance problem that must be
resolved before the 2024 summary can be used as a clean quantitative anchor.
