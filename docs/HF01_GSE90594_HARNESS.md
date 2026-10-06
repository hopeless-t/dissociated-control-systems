# HF01 GSE90594 Harness Decision

GSE90594 remains scientifically useful, but automatic CI execution is deferred.

Two automatic attempts reached the large GPL17077 annotation transfer and were
terminated by the hosted runner with an external shutdown signal. The same
commit continued to pass ordinary CI and the lightweight GSE36169 job.

This is classified as:

~~~text
infrastructure / observation-cost failure
!=
biological falsification
!=
analysis-code exception
~~~

The autonomous loop therefore changes the observation architecture rather than
repeatedly retrying an expensive path.

Next action:

- keep the frozen GSE90594 analysis script in the repository;
- remove it from mandatory automatic execution;
- use GSE93766's gene-level differential-expression artifact as the next
  lightweight cell-type-focused transfer test;
- return to GSE90594 with cached/minimal probe annotation if the information
  gain justifies the cost.
