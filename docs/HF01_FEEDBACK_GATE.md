# HF01 Feedback Gate — From Normal Model to Physiology

> Status: WORKING CAUSAL CONTRACT
> Hair-regrowth claim: NONE
> Clinical authority: NONE

## The original intuition

The motivating question is whether presenting a person with a sufficiently clear normal biological cycle, a degeneration cycle, and a personalized current-state model can help the organism recalibrate toward normal.

HF01 does not collapse this into one arrow.

Instead:

~~~text
M  normal/reference model presentation
↓
A  comprehension / conscious state representation
↓
U  controllable behavior / learned regulation
↓
Q  fast autonomic / neuroendocrine / contextual physiology
↓
R,F*,P,N  follicle-relevant states
↓
H  delayed hair output
~~~

Every arrow is a separate empirical gate.

## Gate 0 — presentation -> comprehension

A clear PowerPoint or interactive model can plausibly improve understanding of the system.
This is an educational/comprehension claim, not a physiological claim.

Passing Gate 0 means only:

~~~text
the person can correctly represent the normal cycle, current estimate,
uncertainty, and actionable variables
~~~

It does not mean the body has changed.

## Gate 1 — comprehension/feedback -> controllable physiology

Human biofeedback literature shows that feedback can alter psychological and, in some settings, autonomic outcomes.

However, sham-controlled results are heterogeneous.

Relevant evidence classes include:

- randomized sham-controlled HRV biofeedback trials;
- systematic/meta-analytic HRV biofeedback evidence;
- human classical-conditioning studies of endocrine and immune responses.

Important boundary:

~~~text
feedback can influence some physiological systems
!=
personalized normal-model feedback will reliably change the specific
physiological variable needed by a hair follicle
~~~

## Gate 2 — fast physiology -> follicle state

Candidate pathways exist in the literature, including stress/neuroendocrine signaling and local follicular responses.

But HF01 has not established that a feedback-induced change in HRV, perceived stress, cortisol, sleep, or another fast variable causes a useful change in AGA regenerative or structural state.

Therefore:

~~~text
Gate 1 success does not imply Gate 2 success
~~~

## Gate 3 — follicle state -> later output

HF-VAL-002 pre-registers the key temporal test:

~~~text
early internal response
    ->
later hair-output trajectory
~~~

The Tang 2003 finasteride/IGF-1 study supplies a small uncontrolled proof-of-concept temporal architecture, but not validation.

## Static slide deck vs closed-loop observer

A static presentation can implement Gate 0.

A DCS observer needs more:

~~~text
reference
  -> current measurement
  -> residual
  -> bounded action
  -> early response
  -> prediction error
  -> model update
~~~

The critical distinction is:

~~~text
explanation != feedback
feedback != actuation
actuation != downstream biological recovery
~~~

## Proposed experimental arms for future validation

Without prescribing any medical intervention, a future feedback study could separate:

~~~text
A: static normal/degeneration educational model
B: non-contingent or sham state feedback
C: contingent personalized state feedback
~~~

The first outcome must be a pre-specified fast physiological/behavioral state, not hair growth.

Only after a Gate-1 effect is established should a study test whether that state change propagates into follicle-relevant measurements.

## Current conclusion

The strongest defensible statement is:

> Making a hidden state legible to the person may improve the human controller, but the physiological plant must still be measured. A normal model is a candidate controller aid, not a biological restore image.

This preserves the CPU analogy while respecting the key difference:

~~~text
CPU rollback loads a known machine state.
Human feedback changes an adaptive controller acting on a living plant.
~~~
