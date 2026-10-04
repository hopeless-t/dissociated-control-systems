# CGD-SIM-011 — Learned disagreement resolver

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

CGD-SIM-010 found that simple posterior averaging captured little of the
Bayes/kNN oracle-union headroom.

This experiment touches only the failing integration point.

When Bayes and kNN disagree, validation data learns:

1. pair-specific preferences for recurrent prediction pairs;
2. a confidence fallback of the form

~~~text
choose kNN if
confidence_knn - gamma * confidence_bayes > delta
otherwise choose Bayes
~~~

The resolver never changes agreement cases.

This is an example of the harness principle:

~~~text
localize failure before expanding architecture
~~~

If this still leaves large oracle-union headroom, the next change should be a
new observation channel (for example temporal evidence), not deeper recursive
governance.
