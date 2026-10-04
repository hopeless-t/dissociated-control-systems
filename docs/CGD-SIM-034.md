# CGD-SIM-034 — Enrichment utility vs intervention-authority frontier

> Status: SYNTHETIC DECISION-SUPPORT TEST  
> Clinical authority: NONE

SIM-031 through SIM-033 establish that an admitted causal probe can enrich a
rare synthetic silent-overconfidence state for research biopsy.

That success must not be silently converted into authority to act on a person.

SIM-034 imports the asymmetric-loss frontier used in Finite RAM Lab GATE-002 /
VOI-style decision analysis.

Let:

~~~text
q = rare-state prevalence
t = selector sensitivity
s = selector specificity
B = benefit of a correct positive action
kB = harm of a false-positive action
~~~

Ignoring other action costs, positive-action expected value is positive only
when:

~~~text
q*t*B > (1-q)*(1-s)*kB

s > 1 - q*t / ((1-q)*k)
~~~

## Two different uses

### Research enrichment

A low-precision selector may still be excellent when the action is simply:

~~~text
spend extra measurement / biopsy budget
~~~

The cost is additional research work, not direct treatment harm.

### Intervention authority

When a false positive can itself cause harm, low prevalence drives the required
specificity toward one.

Therefore the same selector can be:

~~~text
USEFUL FOR RESEARCH SAMPLING
and simultaneously
NOT ELIGIBLE FOR POSITIVE-ACTION AUTHORITY
~~~

## Claim ceiling

The harm multipliers are scenario parameters, not clinical estimates.

This experiment provides a mathematical separation between specimen-selection
utility and action authority. It does not estimate treatment effects, real
prevalence, or human diagnostic performance.
