# CGD-SIM-023 — Sequential causal-probe evidence budget

> Status: SYNTHETIC POST-CONVERGENCE EVIDENCE-BUDGET TEST  
> Clinical authority: NONE

SIM-022 restored causal observability across all four fault dimensions, but it
creates a new resource problem: intervention probes are not free.

SIM-023 treats each paired causal probe as an evidence acquisition with cost.

For each fault dimension, clean synthetic training data estimates two
distributions:

~~~text
p(probe | fault absent)
p(probe | fault present)
~~~

Repeated probe observations update a log-likelihood ratio. Acquisition stops
early when the posterior crosses a confidence boundary, otherwise it is capped
at five repeats per dimension.

Validation selects the confidence boundary from a declared grid using:

~~~text
utility = exact_state_accuracy - 0.003 * mean_total_probe_count
~~~

Held-out seeds compare:

- one probe per dimension;
- five fixed probes per dimension;
- sequential stop-when-confident probing.

## Hypothesis

~~~text
More Evidence != Better Policy
~~~

Once sufficient evidence exists, extra interventions are friction.

The evidence-budget policy is considered successful if it remains within 0.01
exact accuracy of fixed-five while reducing mean probe count by at least 30%.

Synthetic engineering result only; no clinical authority.
