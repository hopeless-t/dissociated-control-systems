# RQ-005 META-A — Bognár preprint-to-final revision transition

## Status

`OBSERVED_TRANSITION / CAUSE_UNRESOLVED`

This document compares two public versions of the same review pipeline without
assuming why they differ.

## Snapshot P — Research Square preprint v1

~~~text
posted:             2023-10-11
search through:     2021-10-18
OS studies:         12
OS participants:    2294
pooled OS HR:       1.01
95% CI:             0.95-1.07
I^2:                3%
~~~

The preprint Figure 2 population-count rows sum exactly to:

~~~text
intervention 1224
control      1070
combined     2294
~~~

Against independently reconstructed trial identities, all 12 displayed
population-count pairs bind to the displayed trial identity.

Frozen source representation:

- `specs/RQ-005-META-A-BOGNAR-PREPRINT-SNAPSHOT.json`

## Snapshot F — Scientific Reports version of record

The published methods state that the search was updated on 2024-02-01 during
the revision process.

The final OS panel reports:

~~~text
OS studies:         14
OS participants:    2683
abstract HR:        0.97 [0.87, 1.08]
Figure 2 HR:        0.97 [0.87, 1.08]
Results-text HR:    1.01 [0.95, 1.07]
~~~

The final Figure 2 population-count rows sum exactly to:

~~~text
intervention 1428
control      1255
combined     2683
~~~

Yet the population-count identities classify as:

~~~text
own trial identity       2 / 14
other known trial       11 / 14
unresolved population    1 / 14
~~~

The unresolved population-size pair is `29/33`; the same numeric pair occurs in
the Andersen randomized trial as recurrence-event counts, not population sizes.
That is recorded only as a cross-semantic collision candidate.

Frozen final representation:

- `specs/RQ-005-META-A-BOGNAR-FIG2-AUDIT.json`

## This is not a pure permutation

Comparing the unique population-count-pair sets:

~~~text
preprint pairs ∩ final pairs = 9
preprint-only pairs          = 3
final-only pairs             = 5
~~~

Therefore a model in which the final publication merely permuted the same
12 count pairs among 14 labels is insufficient.

The final-only observed pairs currently map as:

~~~text
214/114 -> Lu 2021 population size
96/102  -> Kirkegaard 2023 population size
30/36   -> Cunningham 1998 population size
114/113 -> Andersen 2008 randomized population size
29/33   -> exact numeric match to Andersen recurrence-event count
           (different field semantics)
~~~

Lu and Kirkegaard are the two OS labels newly visible in the final 14-study
panel relative to the 12-study preprint. Cunningham and Andersen are not final
OS row labels.

## Competing revision worlds

~~~text
R0  transcription / visual-observation error
R1  labels and numeric columns were ordered independently
R2  one or more columns were joined from a broader master extraction table
R3  population-size and event-count fields were mixed or shifted
R4  figure and manuscript text came from different revision snapshots
R5  analysis was updated but some manuscript text retained the preprint state
R6  documented but not-yet-observed analysis subsets explain the apparent mismatch
R7  another mechanism not yet observed
~~~

Current evidence downgrades a *pure same-membership permutation* explanation,
but does not uniquely select R1-R5.

## DCS interpretation

The revision behaves like a state transition with partially updated observers:

~~~text
preprint state
  -> search / study-set update
  -> final analysis state

but observations disagree:

abstract observer   -> 0.97
figure observer     -> 0.97
results-text observer -> 1.01
row-count identity observer -> degraded binding
~~~

This motivates:

~~~text
Revision Complete != All Observers Converged
Aggregate Total Consistency != Row Identity Consistency
Field Value Match != Field Semantics Match
Population Snapshot != New Randomization
~~~

The analogy is methodological only. It does not establish the editorial or
software mechanism that generated the published state.

## Next falsification gates

1. obtain the final supplementary source/data table without transformation;
2. recover the source row order and field names;
3. test whether the final count sequence is a column from a broader extraction
   table sorted under another field;
4. test whether the `29/33` value originates from an event-count column;
5. reconstruct the updated 14-study analysis from source values;
6. identify which artifact generated the Results-text `1.01`;
7. only after identity repair, use Bognár study-level data in the 2024-vs-2026
   quantitative bridge.

## Claim ceiling

This transition audit concerns evidence provenance only. It does not support a
claim that psychosocial intervention does or does not prolong cancer survival,
and it does not identify a cancer mechanism.
