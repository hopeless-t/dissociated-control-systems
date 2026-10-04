# CGD-SIM-033 — Exact random-capture null and causal-selection biopsy

> Status: SYNTHETIC STATISTICAL FOLLOW-UP  
> Clinical authority: NONE

SIM-032 compared one causal targeting run against one same-budget random draw.
The random draw captured zero rare specimens, which makes a ratio look infinite
but is not a stable statistical summary.

SIM-033 freezes the same held-out population and solves the random baseline
exactly.

If:

~~~text
N = total held-out episodes
K = rare specimens
n = causal biopsy budget
X = rare specimens in an equally sized random biopsy
~~~

then:

~~~text
X ~ Hypergeometric(N, K, n)
~~~

The exact tail probability

~~~text
P(X >= causal capture count)
~~~

is the primary null result.

A seeded 100,000-trial simulation samples from the exact discrete CDF only as a
cross-check.

## Selection-set biopsy

SIM-032 also observed slightly higher biopsy precision for causal targeting than
for the true frozen oracle stratum.

That does **not** mean the causal classifier is better than oracle knowledge.
The sets have different sizes.

SIM-033 decomposes:

- causal selections whose true label equals the oracle stratum;
- causal contaminants from other true strata;
- rare specimens carried by each group;
- nonrare oracle-stratum rows pruned by the causal classifier;
- rare oracle-stratum rows pruned by the causal classifier.

This determines whether the precision difference is simple pruning,
contaminant enrichment, or both.

## Boundary

The exact random null evaluates sampling efficiency in this synthetic world.
It does not establish a human-risk classifier or clinical enrichment strategy.
