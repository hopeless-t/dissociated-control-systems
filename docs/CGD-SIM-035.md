# CGD-SIM-035 — Oracle fault-partition information ceiling

> Status: SYNTHETIC INFORMATION-BOUND TEST  
> Clinical authority: NONE

SIM-034 showed that the admitted causal selector is useful for research
enrichment but far below the specificity needed for action authority.

A possible response would be to improve fault classification again.

SIM-035 asks whether that can work even in principle.

## Oracle upper bound

Give the policy forbidden information:

~~~text
the exact true four-dimensional synthetic fault subset
~~~

This is not an admissible operational probe. It is an information upper bound.

The held-out population is partitioned into all 16 true fault strata. The
analysis enumerates every non-empty subset of those strata and asks:

- what is the maximum rare-state PPV?
- what is the best specificity at fixed minimum rare-state recall?
- does any fault-stratum subset have positive expected action value under the
  SIM-034 asymmetric-loss model?

There are only 2^16 - 1 candidate non-empty subsets, so exhaustive enumeration
is exact and cheap.

## Interpretation

If even the oracle fault partition cannot create an action-eligible subset,
then:

~~~text
better fault-set classification
!= sufficient information
~~~

The remaining uncertainty is **within** fault strata.

That means the next useful observable must measure a finer current state such
as current capability, current calibration divergence, current task failure, or
another domain-validated state variable.

It does not justify inventing a more powerful synthetic oracle probe.

## Boundary

The synthetic rare-state definition is not a human phenotype.

This experiment identifies an information bottleneck in the declared model,
not a clinical diagnostic limit.
