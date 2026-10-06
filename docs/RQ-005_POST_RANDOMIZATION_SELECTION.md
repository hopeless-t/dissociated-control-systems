# RQ-005 Post-randomization recurrence selection

## Problem

A randomized assignment at diagnosis does not automatically remain randomized
inside the subgroup of patients who later recur.

If the intervention changes recurrence probability, then conditioning on
`recurrence = yes` selects a post-randomization subset whose latent-risk
composition can differ between randomized arms.

Therefore:

~~~text
Baseline Randomization
!=
Randomization Within A Post-Randomization Selected Subgroup
~~~

and specifically:

~~~text
Randomized Intervention
 -> recurrence probability
 <- latent disease risk

condition on recurrence
 -> intervention arm and latent risk become associated
~~~

This is a collider / selection problem.

## Synthetic known answer

The deterministic fixture declares two latent risk strata with equal baseline
population weight.

~~~text
LOW risk
  P(recurrence | control)      = 0.20
  P(recurrence | intervention) = 0.20
  post-recurrence survival     = 0.80

HIGH risk
  P(recurrence | control)      = 0.80
  P(recurrence | intervention) = 0.20
  post-recurrence survival     = 0.20
~~~

There is deliberately **no direct post-recurrence intervention term**.
Post-recurrence survival depends only on latent risk.

Yet among patients selected because they recurred:

~~~text
CONTROL recurrent subset
  high-risk fraction = 0.80
  observed post-recurrence survival = 0.32

INTERVENTION recurrent subset
  high-risk fraction = 0.50
  observed post-recurrence survival = 0.50

apparent selected-subset difference = +0.18
~~~

Thus an apparent post-recurrence benefit can appear even when the intervention
has zero direct effect after recurrence in the synthetic world.

Implementation:

- `src/dissociated_control_systems/post_randomization_selection.py`
- `tests/test_post_randomization_selection.py`

## Relevance to psychosocial recurrence studies

The Andersen breast-cancer intervention program is important evidence because
it begins with randomized assignment and includes repeated psychological,
health-behavior, and immune measures.

However, the parent randomized trial reported a reduction in recurrence risk,
while a later analysis studied survival only among the 62 patients who
recurred. Once the analysis conditions on recurrence, the original treatment
arms need not remain exchangeable within that selected subgroup.

The reported post-recurrence association is therefore scientifically valuable,
but it must not be promoted automatically to a clean randomized causal effect
*after recurrence*.

References:

- original randomized survival report: PMID 19016270
- post-recurrence biobehavioral analysis: PMID 20530702

## Analysis hierarchy

For a trial where assignment may affect recurrence:

### A. Preserve the original randomized estimand

Report the original intention-to-treat total effect from randomization on the
pre-specified clinical endpoint without conditioning on recurrence.

### B. Treat the recurrent subgroup as a selected mechanistic cohort

Within patients who recur, repeated mediator and transition measurements can be
highly informative, but the selection ceiling must stay explicit.

At minimum:

- compare baseline risk variables between recurrent randomized arms;
- reconstruct recurrence timing and topology;
- preserve original assignment;
- measure treatment received after recurrence;
- model repeated mediators prospectively from a declared recurrence landmark.

### C. Use causal methods only under explicit assumptions

Depending on the scientific estimand and available data, candidate approaches
include:

- principal-stratification reasoning;
- joint / multi-state modeling of recurrence and death;
- inverse-probability selection weighting when the required selection model is
  defensible;
- sensitivity analysis for unmeasured shared causes of recurrence and
  post-recurrence survival.

No method can manufacture the counterfactual recurrence status that was not
observed; assumptions must remain visible.

## RQ-005 invariant

~~~text
Randomized At Baseline
!=
Randomized Among Recurrences

Post-Randomization Selection
!=
A Neutral Filter
~~~

## Meta-loop consequence

This correction raises the value of the psychosocial randomized literature
without allowing its strongest-looking subgroup result to bypass the same
causal gates imposed on tumor, immune, or treatment hypotheses.

That is the desired RQ-005 behavior:

~~~text
strong evidence design
 -> higher attention
 -> stronger Red Team
 -> narrower calibrated claim
~~~

## Claim ceiling

This known answer demonstrates a possible selection mechanism. It does not show
that selection bias explains the Andersen result, quantify the bias in that
trial, or establish the absence/presence of a post-recurrence psychosocial
effect.
