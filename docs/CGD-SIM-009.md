# CGD-SIM-009 — Classifier ceiling audit

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

## Why audit the ceiling?

CGD-SIM-008 defined the current information ceiling using an all-probe Gaussian
independent-likelihood classifier.

That is only a valid stopping reference if the ceiling is not merely an
artifact of that classifier family.

This experiment compares the same four-probe observations with a structurally
different classifier:

- Gaussian independent-likelihood Bayes;
- standardized 7-nearest-neighbor.

It also measures an oracle union:

~~~text
correct if either classifier is correct
~~~

The oracle union is not deployable. It estimates remaining classifier-family
headroom.

## Stability conditions

The declared observation/classifier ceiling is considered stable only if:

~~~text
abs(knn_accuracy - bayes_accuracy) < 0.005
oracle_union - best_single_accuracy < 0.010
abs(knn_accuracy_160 - knn_accuracy_80) < 0.005
~~~

If this fails, the self-improvement loop should continue at the classifier or
representation layer.

If it passes, policy recursion is no longer the productive direction. The next
possible gain would require genuinely new evidence or a richer temporal state
representation.

## Claim ceiling

Synthetic classifier/observation audit only. No biological or clinical
classification claim is made.
