# RQ-005 META-A — 2024 vs 2026 synthesis delta

## Why this comparison matters

Two recent randomized-trial syntheses can be summarized superficially as:

~~~text
2024: no survival effect
2026: small positive overall survival effect
~~~

RQ-005 does not allow that contrast to become a mechanistic conclusion.
The first task is to explain what changed in the evidence and analysis pipeline.

References:

- Bognár et al. 2024, PMID 38853187, DOI 10.1038/s41598-024-63431-y
- Asakawa-Haas et al. 2026, PMID 41673256, DOI 10.1038/s44271-026-00414-x

## First correction — the 2024 paper has an internal OS estimate conflict

The published abstract reports:

~~~text
OS HR = 0.97
95% CI = 0.87-1.08
~~~

The published Results section reports:

~~~text
OS HR = 1.01
95% CI = 0.95-1.07
k = 14
n = 2,683
~~~

RFS is reported consistently as HR 0.99, 95% CI 0.84-1.16.

An earlier preprint also reported the 1.01 estimate, which is a provenance clue
but not sufficient reason to silently choose it as canonical.

Therefore:

~~~text
Published Abstract != Automatically Canonical Result
Same Paper Can Contain An Open Estimate Conflict
~~~

Implementation:

- `src/dissociated_control_systems/meta_reconciliation.py`
- `tests/test_meta_reconciliation.py`
- `specs/RQ-005-META-A-RECONCILIATION.json`

The known-answer test refuses to canonicalize the 2024 OS estimate while the
source conflict remains open.

## Second correction — the title scope is not the eligibility scope

The 2024 title says `early-stage cancer`, but its published Methods state that
eligible participants were adults diagnosed with any cancer who were receiving
cancer or palliative treatment or who were reported as cancer survivors.

The 2026 synthesis explicitly allows primary or metastatic cancer of any type
and any stage.

Thus it is unsafe to reduce the pair to:

~~~text
2024 = early stage only
2026 = all stages
~~~

The actual included trial populations must be reconstructed trial by trial.

## Third correction — effect metric alone cannot explain this pair

The 2026 paper argues that differences among prior meta-analyses often arose
from effect-size choices such as HR versus OR versus RR and from analytic
decisions.

That is a useful global finding about the literature, but it is not a complete
explanation of the 2024-versus-2026 pair because both primary syntheses report
HRs.

Therefore:

~~~text
Effect-Metric Difference = Important Global Moderator
Effect-Metric Difference != Sufficient Pairwise Explanation Here
~~~

## Fourth correction — the data universe changed substantially

The 2024 search was updated through 2024-02-01.
The 2026 search continued through 2025-10-17.

The 2024 Results report 14 OS studies / 2,683 participants.
The 2026 primary synthesis reports 32 RCTs / 5,704 participants.

Before attributing the pooled-estimate change to biology or intervention timing,
META-A must compute:

~~~text
intersection(trials_2024, trials_2026)
2024_only
2026_only
followup_publication_replacements
same_trial_different_effect_source
~~~

## Fifth correction — HR provenance differs within the 2026 synthesis

The 2026 paper reports that its 32 HRs came from multiple routes:

~~~text
16  directly available from RCT reports
 2  inverse HRs from control-group reporting
 4  taken from prior meta-analyses
10  reconstructed from Kaplan-Meier curves
~~~

This does not invalidate the analysis. It does mean that effect-estimate
provenance is itself a state variable in the reconciliation.

A trial appearing in both reviews may still contribute a numerically different
HR because the extraction source, follow-up publication, or reconstruction rule
changed.

## Current ranked discrepancy worlds

~~~text
D1  trial inclusion / search-horizon difference
D2  follow-up publication identity / effect-selection rule
D3  HR extraction or Kaplan-Meier reconstruction difference
D4  unresolved 2024 abstract-vs-body estimate conflict
D5  eligibility / intervention-definition difference
D6  pooling / variance-estimation implementation difference
D7  treatment-era and case-mix difference
~~~

These worlds are not mutually exclusive.

## Required next experiment

After the SHA256-verified 2026 OSF assets become available to an execution
environment:

1. reproduce the authors' reported 2026 primary result unchanged;
2. construct a stable `trial_id` ledger;
3. map every publication/effect estimate to its randomization;
4. reconstruct the 2024 trial set;
5. calculate set overlap and replacements;
6. for shared trials, compare HR values and provenance;
7. rerun a common trial set under one frozen HR extraction rule;
8. change one decision at a time until the pooled-estimate delta is accounted
   for or a residual discrepancy remains.

The target output is a decomposition such as:

~~~text
Delta pooled log(HR)
  = contribution from trial-set changes
  + contribution from follow-up/effect-source changes
  + contribution from extraction/reconstruction changes
  + contribution from model/variance choices
  + unresolved residual
~~~

This is an accounting identity for research debugging, not a causal biological
decomposition.

## Connection back to the survivor question

Only after the review-level discrepancy is reconciled should the resulting
trial features inform the DCS mechanism program.

A trial-level survival effect still does not identify whether any effect passed
through:

- treatment engagement;
- behavior;
- stress physiology;
- immune state;
- social support;
- another mediator;
- or statistical variation.

`hope` remains a non-privileged label.

## Claim ceiling

This lane can explain why two evidence syntheses disagree.
It cannot by itself establish that psychological state controls tumor biology,
that psychotherapy prolongs survival for a particular patient, or that any
survivor's outcome was caused by hope.
