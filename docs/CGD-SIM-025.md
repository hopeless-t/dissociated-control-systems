# CGD-SIM-025 — Evidence-budget frontier

> Status: SYNTHETIC POST-CONVERGENCE RESOURCE-FRONTIER TEST  
> Clinical authority: NONE

SIM-024 demonstrated that repeated causal evidence shifts the measurement-noise
knee. With independent measurement noise, however, a sufficiently large repeat
budget can continue averaging noise down.

Therefore "information channel failure" is not yet a sufficient convergence
criterion. Evidence acquisition has to be priced.

SIM-025 evaluates fixed evidence budgets:

~~~text
1, 2, 3, 5, 8, 13 repeats per fault dimension
= 4, 8, 12, 20, 32, 52 total probes
~~~

For every measurement-noise level, it reports:

- exact 16-state accuracy;
- macro per-fault accuracy;
- the smallest budget satisfying exact accuracy >= 0.90;
- the budget maximizing the declared synthetic utility:

~~~text
utility = exact_accuracy - 0.003 * total_probe_count
~~~

## Convergence interpretation

The target is no longer maximal possible accuracy.

It is:

~~~text
minimum evidence that satisfies the reliability contract
~~~

If no declared budget reaches the contract, normal authority remains
fail-closed rather than recursively spending unbounded evidence.

Synthetic engineering result only; no clinical authority.
