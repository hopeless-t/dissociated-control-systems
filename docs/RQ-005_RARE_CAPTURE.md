# RQ-005 Rare Survivor Capture Plan

## Why this exists

The first METABRIC pilot found a rare trajectory inside the strict high-risk
comparison frame:

~~~text
NPI >= 5.5
strict LTS/STS analyzable cases: 134

early recurrence <=60 months
AND long-term survival >=120 months:
2 cases
~~~

Observed discovery-frame frequency:

~~~text
2 / 134 = 1.49%
~~~

This is **not a population prevalence estimate**.

The denominator excludes patients with insufficient follow-up and uses an
extreme retrospective LTS/STS contrast.

It is useful only for planning rare-state capture under a similar sampling
frame.

## Capture probability

If a rare state occurs independently with probability p, the probability of
seeing at least one specimen in N observations is:

~~~text
P(capture >= 1) = 1 - (1 - p)^N
~~~

Using the pilot point estimate p = 0.0149:

~~~text
N for ~95% probability of >=1 capture ~= 200
~~~

Because only two specimens were observed, p is highly uncertain.

With a simple Beta(1,1) prior:

~~~text
posterior = Beta(3,133)

95% interval for p:
approximately 0.46% to 5.25%
~~~

The corresponding N needed for ~95% probability of >=1 capture spans roughly:

~~~text
p = 0.46%  -> N ~= 649
p = 1.49%  -> N ~= 200
p = 5.25%  -> N ~= 56
~~~

This wide range is itself the result.

## DCS / Finite RAM transfer

Rare survivor research should not use:

~~~text
small cohort
 -> no rare specimen observed
 -> mechanism absent
~~~

Instead:

~~~text
declare target rare-state definition
 -> estimate capture probability
 -> choose sample size / aggregation strategy
 -> preserve cohort blocks
 -> capture specimen
 -> freeze before reinterpretation
 -> matched causal-history biopsy
 -> independent recapture
~~~

This mirrors the Finite RAM Lab rare-event discipline without transferring any
physical mechanism.

## Implication for external cohorts

A cohort can be excellent for average hazard estimation yet still be too small
for rare survivor-state discovery.

Dataset selection therefore needs two scores:

~~~text
population-model value
rare-state capture value
~~~

A study with deep longitudinal measurements on 50 patients may be valuable for
trajectory mechanics but weak for discovering a ~1% state.

A study with thousands of patients but shallow measurements may find the rare
state but not identify its mechanism.

The target architecture is therefore:

~~~text
large shallow census
 -> rare-state localization
 -> smaller deep-observation cohort
 -> mechanistic discrimination
~~~

## Stopping / escalation rule

Do not escalate a null rare-state result into evidence of absence until the
pre-declared capture probability is adequate.

If adequate capture requires an impractical sample size, the correct output is:

UNDERPOWERED_FOR_RARE_STATE_CAPTURE

not:

RARE_STATE_ABSENT
