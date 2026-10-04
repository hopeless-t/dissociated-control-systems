# CGD-SIM-003 — Adaptive L3 governor

> SYNTHETIC WORKING MODEL — CLINICAL AUTHORITY: NONE

## Question

Does DCS need a deeper meta-controller immediately, or can a bounded L3 governor
stabilize L1 calibration failure and L2 handoff failure?

The frozen failure schedule is:

~~~text
t < 30   L1 normal
t >= 30  L1 feedback gain falls from 0.40 to 0.05
t < 60   L2 handoff reliability = 1.00
t >= 60  L2 handoff reliability = 0.35
~~~

L3 sees only synthetic objective feedback and handoff receipts.

Three L3 designs are compared:

1. naive threshold switching;
2. hysteretic switching;
3. hysteretic + hard observability cap.

The bounded controller enforces:

~~~text
A_obs = 1/(1-r)^2 <= 4
~~~

so compensation cannot silently make the latent state arbitrarily unobservable.

A fifth arm combines bounded L3 with the existing slow-loop decline-rate
reduction. This is the full current DCS-CGD stack:

~~~text
L0 latent capability
L1 calibrated estimate
L2 compensation / handoff
L3 bounded adaptive governor
+ slow root-side track
~~~

## Decision rule for L4

L4 is not justified merely because L3 exists.

A deeper governor becomes a candidate only if bounded L3 still shows one or
more of:

- unstable/chattering adaptation that hysteresis cannot control;
- repeated invariant violations;
- non-identifiable L1-vs-L2 failure signatures;
- runaway observability loss;
- adaptation rules that must themselves be changed online.

Until then, adding L4 would increase state-space and identifiability burden
without evidence of necessity.
