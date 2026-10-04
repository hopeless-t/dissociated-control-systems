# CGD-SIM-013 — Replicated local fixed-point audit

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

The previous generations found:

- local controller stability at bounded L3;
- evidence redundancy beats deeper governance when observation is bad;
- active repair/re-observation beats one-shot classification;
- durable evidence is required when diagnostic windows can close;
- value-of-information cuts probe friction with almost no accuracy loss;
- policy selection saturates near the all-probe ceiling;
- classifier changes add only small gains;
- adding naive temporal summary features makes the held-out frontier worse.

CGD-SIM-013 asks whether this apparent wall survives independent held-out seed
blocks.

Training and validation are frozen once. The selected base and temporal
classifier parameters are then applied unchanged to five independent test
blocks.

Declared fixed-point conditions:

~~~text
mean base residual oracle gap < 0.010
max base residual oracle gap  < 0.015
mean temporal gain            < 0.005
blocks with temporal gain > .005 <= 1
~~~

This is deliberately a **local synthetic fixed point**, not a global optimum.
It means the current closed loop has exhausted useful changes within its
declared model, observations, and classifier family.

At that point further "meta-meta" recursion is not evidence-driven. Progress
requires one of:

- new independent evidence;
- a changed generative/world model;
- external empirical validation.

No medical or clinical claim is made.
