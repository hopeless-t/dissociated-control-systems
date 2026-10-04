# CGD-SIM-010 — Bayes + kNN ensemble frontier

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

CGD-SIM-009 rejected the previous classifier ceiling:

- the two classifier families disagreed on non-trivial cases;
- their oracle union reached materially above either classifier;
- kNN still improved with more training data.

This experiment combines their posteriors:

~~~text
p_ensemble(h)
  = w * p_bayes(h)
  + (1-w) * p_knn(h)
~~~

Validation selects:

~~~text
k in {3, 5, 7, 11, 15}
w in {0.0, 0.1, ..., 1.0}
~~~

The selected parameters are frozen before held-out testing.

A remaining oracle-union gap measures the maximum complementarity still
available from the two classifier families. It is not a deployable oracle.

The classifier frontier is locally stable only when both:

~~~text
ensemble gain over best single < 0.005
oracle-union gap              < 0.010
~~~

If not, the next self-improvement target is disagreement resolution.

This remains synthetic fault-classification research and has no clinical
diagnostic authority.
