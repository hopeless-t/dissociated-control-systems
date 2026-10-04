# RQ-005 META-A — psychosocial survival evidence reconciliation

## Why this lane is separate from mechanism discovery

Psychosocial-intervention survival evidence currently gives apparently
conflicting high-level summaries.

A mechanism model should not resolve that conflict by choosing the paper that
best fits its preferred story.

Therefore:

~~~text
Meta-analytic Summary != Biological Mechanism
Evidence-Synthesis Disagreement != Permission To Pick A Favorite Estimate
~~~

META-A treats the disagreement itself as an object of study.

## 2024 early-stage randomized meta-analysis

Bognár et al. analyzed randomized psychological interventions in early-stage
cancer.

Reported pooled survival endpoints:

~~~text
OS   HR = 0.97, 95% CI 0.87-1.08
RFS  HR = 0.99, 95% CI 0.84-1.16
~~~

Quality-of-life outcomes improved, but the reported pooled OS and RFS effects
were null.

Reference: PMID 38853187.

## 2026 preregistered multiverse meta-analysis

Asakawa-Haas et al. synthesized 32 RCTs / 5,704 participants and reported:

~~~text
overall survival HR = 0.80
95% CI              = 0.71-0.90
I^2                 = 48%
95% prediction interval = 0.49-1.29
~~~

The estimated median-survival benefit from 16 trials was 3.9 months with a 95%
CI of -0.7 to 8.5 months.

The paper reports low average meta-analytic post-hoc power (~17%) and uses a
multiverse analysis to examine how reasonable analytic specifications used in
prior meta-analyses affect the summary conclusion.

Reference: PMID 41673256.

## Immediate Red Team conclusion

The simple explanation:

~~~text
"psychosocial intervention works only if delivered early"
~~~

is not supported as a sufficient explanation for the literature conflict.

The early-stage 2024 synthesis itself reported no OS/RFS benefit. Conversely,
the broader 2026 synthesis reports a positive average effect but a wide
prediction interval crossing the null.

Therefore:

~~~text
Timing Alone != Reconciliation
Positive Overall Meta-Effect != Universal Patient Effect
Null Early-Stage Meta-Effect != Proof Of No Effect In Every Subgroup
~~~

## Reconciliation dimensions

META-A must reconstruct, trial by trial, at least:

1. inclusion/exclusion set;
2. cancer type;
3. stage / recurrent / metastatic status;
4. intervention start relative to diagnosis, surgery, adjuvant therapy, and
   recurrence;
5. intervention components;
6. individual vs group delivery;
7. provider type;
8. active vs attention vs usual-care control;
9. endpoint definition (OS, cancer-specific survival, RFS, PFS);
10. effect-size metric and transformation;
11. follow-up horizon;
12. whether a follow-up publication replaces an earlier report from the same
    trial;
13. risk-of-bias and missingness handling;
14. subgroup / moderator specification;
15. treatment-era differences;
16. whether survival was primary, secondary, or long-term follow-up endpoint.

## Study-identity invariant

Multiple publications from one randomized cohort are not independent trials.

~~~text
Publication != Trial
Follow-Up Paper != New Randomization
~~~

The reconciliation ledger must assign a stable `trial_id` and attach all
publications/effect estimates to that trial before pooling.

This is especially important for trials with an original randomization paper,
long-term survival follow-up, recurrence analysis, and mediator papers.

## Analysis ladder

### META-A0 — trial identity map

Create a publication-to-trial graph and detect duplicated cohorts.

### META-A1 — fixed common endpoint

Where possible, compare the same effect measure on the same endpoint under a
predeclared extraction rule.

### META-A2 — leave-one-trial-out influence

Measure how much each randomized cohort moves the pooled estimate.

### META-A3 — specification multiverse

Vary only defensible predeclared choices such as:

- endpoint hierarchy;
- duplicate-publication selection rule;
- fixed/random effects;
- effect-size conversion method;
- early/recurrent/metastatic scope;
- follow-up horizon rule.

Do not vary choices merely to obtain significance.

### META-A4 — moderator validation

Any apparent stage/timing/intervention-component moderator must be tested with
held-out or sufficiently powered interaction evidence where possible.

A subgroup whose CI differs from zero while another subgroup's CI does not is
not, by itself, evidence that the subgroups differ.

## Connection to the DCS survivor model

META-A supplies priors and evidence constraints to RQ-005, but does not insert a
psychological survival coefficient directly into the tumor model.

The causal chain remains decomposed:

~~~text
randomized intervention
 -> measured psychological / behavioral changes
 -> measured neuroendocrine / immune changes
 -> transition-specific disease outcomes
~~~

Each arrow can fail independently.

## Current fixed point

~~~text
psychosocial interventions improve many psychological/QoL outcomes:
  SUPPORTED

psychosocial interventions have one universal cancer-survival effect:
  NOT SUPPORTED

average survival effect across all eligible RCTs:
  CURRENTLY CONTESTED BY SCOPE / SYNTHESIS CHOICES,
  with a positive 2026 broad synthesis and null 2024 early-stage synthesis

specific biological mediator responsible for any survival effect:
  UNKNOWN

"hope" as the active causal ingredient:
  UNKNOWN / NOT PRIVILEGED
~~~

## Claim ceiling

META-A can explain why quantitative syntheses differ and identify which trial
features deserve mechanistic follow-up.

It cannot prove a psychoneuroimmune cancer-control mechanism from pooled
survival estimates alone.
