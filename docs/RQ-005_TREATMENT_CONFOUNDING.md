# RQ-005 Treatment confounding negative control

## Failure mode

The METABRIC pilot showed chemotherapy recorded more often in the short-survival
contrast than in the long-survival contrast.

That pattern must **not** be interpreted as chemotherapy causing worse
survival.

Higher-risk patients are more likely to receive treatment. This can generate a
pooled association in the opposite direction from the treatment effect within
risk strata.

## Deterministic known answer

Synthetic population:

~~~text
50% low risk
  P(treatment) = 0.10
  survival if untreated = 0.90
  survival if treated   = 0.95

50% high risk
  P(treatment) = 0.90
  survival if untreated = 0.20
  survival if treated   = 0.40
~~~

Treatment is beneficial in both strata:

~~~text
low risk:  +0.05 survival probability
high risk: +0.20 survival probability
standardized average causal RD = +0.125
~~~

But because treated patients are mostly high risk:

~~~text
observed survival among treated   = 0.455
observed survival among untreated = 0.830
naive observational RD            = -0.375
~~~

The naive sign reverses.

Implementation:

- `src/dissociated_control_systems/treatment_confounding.py`
- `tests/test_treatment_confounding.py`

## RQ-005 invariant

~~~text
Treatment Category Association != Treatment Effect
Treatment Selection != Randomized Exposure
More Treatment in STS != Treatment Harm
~~~

## Consequence for the survivor model

Recorded chemotherapy, radiotherapy, or endocrine-therapy indicators can be
used as context/predictors in the retrospective discovery baseline, but they
cannot be promoted to causal treatment coefficients without a design that
addresses at least:

- confounding by indication;
- stage / burden / subtype;
- treatment timing and line;
- dose / duration / discontinuation;
- time-varying treatment assignment;
- immortal-time and landmark structure where relevant;
- treatment response as a post-treatment mediator rather than a baseline
  confounder.

## Meta-loop lesson

When a variable is an action selected in response to state, the action itself
contains information about the underlying state.

This is a DCS-style authority / state distinction:

~~~text
Observed Action
  = policy(state, information, constraints)

therefore

Observed Action
  != exogenous perturbation
~~~

The analysis harness must model the selection policy before interpreting the
action-outcome association.
