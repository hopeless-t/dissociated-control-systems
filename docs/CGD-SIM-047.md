# CGD-SIM-047 — Environment-confounded functional sentinel

> Status: SYNTHETIC OBSERVATION-CONFOUNDING TEST  
> Clinical authority: NONE

SIM-045 and SIM-046 showed that an independent functional innovation can be a
useful trigger for objective re-observation when self/informant disagreement is
non-identifying.

Those experiments simplified the functional channel as:

~~~text
F approximately = current state + measurement noise
~~~

The external variable map is richer:

~~~text
F = current state + environment/scaffold + measurement noise
~~~

SIM-047 restores that omitted environment/scaffold term.

## Question

If function changes because support, context or environment changes while
current cognitive state does not, will a raw functional-sentinel trigger
mistake that change for stale cognitive-state evidence?

## Synthetic environment shift

At each simulated specimen an environment event occurs with frozen probability:

~~~text
0%, 1%, 5%, 10%, 20%, 50%
~~~

When present, the functional channel receives a persistent signed offset of
magnitude 0.12 in the unitless synthetic model.

Other frozen values:

~~~text
functional measurement noise std   = 0.02
environment-context noise std       = 0.01
self-bias drift std                 = 0.04
informant-bias drift std            = 0.04
~~~

These values are sensitivity scenarios, not estimates of real home, caregiver,
IADL, assistive-technology or cognitive-test effects.

## Two observation rules

### Raw function innovation

~~~text
score_raw = |function - propagated state prediction|
~~~

This sees both cognitive-state error and environment/scaffold change.

### Context-normalized innovation

An independent context channel observes the environmental contribution with its
own declared noise:

~~~text
score_normalized
  = |function - observed environment context - propagated state prediction|
~~~

The context channel is not assumed perfect.

## Evaluation

The target remains the top 10% of absolute propagated current-state errors.

For each environment-shift probability the experiment reports:

- AUROC of the raw functional sentinel;
- AUROC after context normalization;
- sensitivity and false-positive rate at a fixed 10% trigger coverage;
- the fraction of raw false-positive triggers attributable to specimens with an
  environment shift.

## Hypothesis

As environment/scaffold events become more common, the raw functional sentinel
should lose state-specific information even though it remains an independent
measurement channel.

A sufficiently accurate context observation should recover much of that lost
specificity.

~~~text
Functional Change != Cognitive-State Change
Independent Observation != State-Specific Observation
Environment / Scaffold Is A Latent State, Not Mere Noise
~~~

## DCS implication

The result decides whether the next external-facing observation contract must
bind not only **who/what measured the state**, but also **under which support and
environment context the function was observed**.

This mirrors the wider DCS rule:

~~~text
Observation Without Context Binding Can Be Valid Yet Misapplied
~~~

## Claim ceiling

No real performance-based IADL, digital endpoint, caregiver support state or
home environment is assigned the frozen synthetic offsets/noise values.

The experiment tests confounding structure only. It does not define a clinical
monitoring algorithm or a rule for attributing functional change to cognition.
