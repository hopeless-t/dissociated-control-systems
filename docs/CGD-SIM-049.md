# CGD-SIM-049 — Context reliability authority gate

> Status: SYNTHETIC CONTEXT-QUALIFICATION TEST  
> Clinical authority: NONE

SIM-048 showed that binding functional evidence to an explicit environment /
scaffold context can rescue a selective re-anchor policy from severe
confounding.

That result creates a new risk: treating the context channel itself as if it
were ground truth.

SIM-049 attacks that assumption.

## Observation model

The synthetic target is the top 10% of absolute propagated state-estimation
error.

A raw functional innovation is contaminated by environment state:

~~~text
score_raw = |environment + function_noise - state_error|
~~~

A context-normalized innovation subtracts an observed context channel:

~~~text
observed_context = environment + context_noise
score_context = |function_noise - context_noise - state_error|
~~~

The environment event process is frozen at:

~~~text
P(environment shift) = 10%
shift magnitude = +/-0.12
~~~

The functional noise standard deviation is frozen at `0.02`.

The context channel is stressed across:

~~~text
sigma_context = 0.00, 0.01, 0.02, 0.04, 0.06, 0.08, 0.12
~~~

All values are unitless scenario parameters.

## Pilot / held-out authority gate

For each context-noise level:

1. generate a pilot set;
2. measure raw and context-normalized AUC for detecting top-10% state error;
3. grant normalization authority only if:

~~~text
pilot AUC_normalized >= pilot AUC_raw + 0.01
~~~

4. freeze the selected evidence route;
5. evaluate on a disjoint held-out set.

The `+0.01` margin is deliberately conservative synthetic friction. It prevents
context normalization from gaining authority merely by tying the raw route.

## Failure model

At low context noise, subtracting context should remove environment
confounding and improve discrimination.

As context noise rises, the subtraction injects its own uncertainty. Eventually
normalization can become worse than leaving the raw functional signal
unadjusted.

The experiment therefore asks two separate questions:

~~~text
Does context binding help?
!=
Does this context channel deserve authority to normalize evidence?
~~~

## Frozen hypotheses

- low-noise context should receive normalization authority;
- authority should be revoked when pilot incremental AUC disappears;
- held-out selection regret should stay small;
- sufficiently noisy context should make normalized discrimination collapse;
- failure of context qualification should route to a fallback rather than
  silently continue correction.

## New invariants

~~~text
Context Observation != Environment State
Context Binding != Context Authority
Normalization Requires Incremental Reliability Evidence
Failed Qualification -> Fail Back, Not Blind Correction
~~~

## Claim ceiling

This experiment does not validate any real caregiver report, home sensor,
digital IADL, environmental context variable or clinical retest rule.

Its purpose is structural: a compensating observation channel must not inherit
authority merely because an earlier synthetic experiment showed that context
can be useful. The context channel needs its own qualification contract.
