# CGD-SIM-031 — Rare silent-overconfidence harvesting

> Status: SYNTHETIC EXPLORATORY + HELD-OUT CONFIRMATION  
> Clinical authority: NONE

This experiment imports Finite RAM Lab's rare-state workflow into DCS.

The candidate rare state is a large **signed** self-estimate/capability gap while
final capability is already low:

~~~text
signed overconfidence =
    final self estimate - final latent capability

rare candidate =
    final capability <= 0.55
    and
    signed overconfidence >= threshold
~~~

The threshold is not declared to be a human or clinical threshold.

## Two-stage design

### Pilot

Across all 16 synthetic fault subsets:

1. evaluate a frozen threshold grid;
2. choose a non-empty rare threshold near a 2% pooled target;
3. identify the exact fault subset with the highest pilot incidence.

### Held-out

Using disjoint seeds:

1. keep the threshold fixed;
2. keep the selected enrichment stratum fixed;
3. estimate pooled and enriched incidence;
4. compute the sampling count needed for a 95% probability of at least one
   specimen;
5. biopsy the captured states.

The enrichment is considered confirmed only when the held-out selected stratum
contains at least three specimens, exceeds pooled incidence, and has at least a
2x incidence ratio.

## Why this matters

Average diagnostic accuracy can hide a low-frequency state where subjective
state and objective capability diverge sharply.

The research goal is not to call that state a disease. It is to determine
whether the harness can:

~~~text
find
-> enrich
-> capture
-> biopsy
-> prospectively retest
~~~

rare control states rather than averaging them away.
