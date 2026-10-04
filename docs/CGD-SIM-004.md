# CGD-SIM-004 — Observation-channel stress

> SYNTHETIC WORKING MODEL — CLINICAL AUTHORITY: NONE

## Question

What happens when L3 itself receives a bad "objective" signal?

The bounded L3 + slow-loop architecture from CGD-SIM-003 is kept fixed.
Only observation quality changes.

Frozen stress:

~~~text
primary bias        +0.08
primary dropout      25%
secondary dropout    10%
noise sd              0.03
~~~

Three cases:

1. clean single observer;
2. biased/dropout primary observer;
3. biased primary + independent unbiased secondary observer.

When both observers are present and disagree, the synthetic harness uses the
more conservative estimate. This is a declared safety rule, not a clinical
recommendation.

## Why this matters

If L3 fails only because all of its evidence is wrong or missing, adding L4
does not create new information. The relevant intervention is observation
diversity / independent evidence, not additional recursive control depth.

Therefore this experiment tests a boundary condition for meta-depth:

~~~text
bad controller -> candidate for higher-order governance
bad evidence   -> improve observation architecture first
~~~

## Claim ceiling

A pass establishes only that redundant observation can rescue this declared
synthetic controller from a declared biased/dropout channel. It does not
establish a medical monitoring protocol or diagnostic method.
