# RQ-005 Post-recurrence psychosocial / neuroimmune evidence map

## Why this document exists

RQ-005 initially placed psychological / agency variables late in the
post-recurrence observation ladder so that strong tumor, treatment, response,
and TME competitors would be measured first.

A literature pass shows that a simple fixed ranking is itself too coarse.
There are randomized psychosocial intervention datasets in breast cancer that
reach the recurrence / metastatic transition, and their survival results are
mixed.

Therefore:

~~~text
Psychological Layer Last
!=
Psychological Layer Irrelevant

Randomized Perturbation + Mediator Measurements
!=
Retrospective Survivor Narrative
~~~

## Positive post-recurrence signal

Andersen et al. followed a randomized psychological-intervention trial after
breast-cancer recurrence.

- original regional-breast-cancer trial: n=227 randomized before adjuvant care;
- 62 patients subsequently recurred;
- intent-to-treat post-recurrence analysis reported reduced risk of death for
  the original intervention arm (HR 0.41, p=0.014);
- a biobehavioral subset of 41 recurrent patients was reassessed at recurrence
  and 4, 8, and 12 months;
- psychological/social/adherence/health and immune measures including NK-cell
  cytotoxicity and T-cell proliferation were collected;
- the intervention arm showed better psychological trajectories and higher
  immune indices at 12 months in the reported analysis.

Reference: PMID 20530702.

This is unusually relevant to RQ-005 because it contains:

~~~text
randomized upstream perturbation
+ recurrence event
+ post-recurrence survival
+ repeated candidate mediators
~~~

It still does not identify which mediator, if any, caused a survival effect.
The recurrent subgroup is small and is a post-randomization subset.

## Null metastatic randomized evidence

Other randomized supportive-expressive group therapy trials in metastatic
breast cancer did not reproduce a general survival benefit.

Kissane et al. randomized 227 women with advanced breast cancer and reported no
survival extension from supportive-expressive group therapy: multivariable HR
1.06 (95% CI 0.74-1.51). The intervention did improve several psychosocial
outcomes.

Reference: PMID 17385190.

Goodwin et al. randomized 235 women with metastatic breast cancer and likewise
reported no survival benefit: adjusted HR 1.23 (95% CI 0.88-1.72), while mood
and pain outcomes improved.

Reference: PMID 11742045.

A separate 125-patient randomized supportive-expressive trial also failed to
replicate an overall survival effect, though an exploratory ER-status
interaction was reported.

Reference: PMID 17647221.

## Mediator plausibility without survival proof

Randomized stress-management studies in non-metastatic breast cancer have shown
that psychological interventions can change measurable physiology, including
cortisol and Th1-related immune readouts.

Reference: PMID 18835434.

Observational metastatic-breast-cancer work has also linked depressive
symptoms, diurnal cortisol, and cell-mediated immune measures, and older work
reported flatter diurnal cortisol rhythms associated with shorter survival.

References: PMID 19643176, PMID 10861311.

These observations support measurable mediator paths; they do not prove a
psychological survival mechanism.

## RQ-005 interpretation

The literature currently supports at least four competing explanations for the
mixed trial record:

~~~text
P0  no material survival effect; positive studies are sampling/analytic noise
P1  intervention-specific effect rather than generic "hope"
P2  effect modification by tumor / receptor / treatment state
P3  mediated effect exists only when intervention changes a sufficient
    combination of behavior, neuroendocrine state, and immune state
P4  timing matters: pre-recurrence intervention changes later state, while
    intervention after advanced disease may be too late to alter disease control
P5  survival effect is partly due to treatment engagement / health behavior
    rather than direct neuroimmune control
~~~

No P-world is currently privileged.

## Consequence for value of information

RQ-005 should rank **measurement designs**, not just biological domains.

High-value psychological/neuroimmune evidence can be:

~~~text
randomized perturbation
+ repeated psychological state
+ treatment exposure/adherence
+ cortisol/autonomic/inflammatory measures
+ immune measures
+ recurrence topology / burden
+ transition-specific survival endpoint
~~~

A late survivor narrative without contemporaneous mediator measurements remains
low for causal identification even if emotionally rich.

Thus:

~~~text
Domain Priority != Evidence-Design Priority
~~~

## Proposed replication analysis

If individual-level data from a suitable randomized cohort become available:

1. preserve original randomization as the primary perturbation;
2. avoid conditioning the causal treatment estimate on post-randomization
   recurrence without explicitly handling selection;
3. separately study the recurrent subgroup as a mechanistic cohort;
4. model repeated mediators from recurrence forward;
5. test whether mediator trajectories add information to recurrence site,
   burden, treatment, and subtype;
6. use transition-specific outcome `recurrence -> cancer death/censor`;
7. report total randomized effect separately from exploratory mediation.

## Claim ceiling

Current evidence does not establish that hope, optimism, psychotherapy, or
stress reduction cures metastatic breast cancer.

It does establish that the psychological/neuroimmune layer cannot be dismissed
from RQ-005 solely because stronger tumor and treatment predictors exist.
