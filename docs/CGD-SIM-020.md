# CGD-SIM-020 — Missingness-aware restoration

> Status: SYNTHETIC POST-CONVERGENCE REPRESENTATION REPAIR  
> Clinical authority: NONE

SIM-019 found that even 160 shifted calibration samples per latent hypothesis
did not restore accuracy above 0.511 on validation or 0.479 on held-out test.

That makes "just collect more data" an insufficient explanation.

The next failure is a representation contract violation:

~~~text
Missing Observation != Observation At Mean
~~~

The OOD generator explicitly marks missing observations, but the previous
classifier consumed the imputed clean-mean value as if it had actually been
observed.

SIM-020 propagates missingness into the classifier itself.

## Masked Bayes

A missing probe contributes no likelihood term.

## Masked kNN

A probe contributes to a pairwise distance only when it is observed in both
the query and candidate row. Distance is normalized by the mean number of
usable dimensions rather than treating imputed values as evidence.

The same shifted validation/test split and the same restoration threshold
(0.90 exact validation accuracy) are retained.

If accuracy rises, this is evidence that the prior restoration failure was
caused by information semantics rather than by insufficient sample count.

Synthetic engineering result only; no clinical authority.
