# CGD-SIM-032 — Causal rare-state capture policy

> Status: SYNTHETIC RARE-STATE CAPTURE TEST  
> Clinical authority: NONE

SIM-031 identified and independently confirmed an enriched synthetic stratum
for a rare silent-overconfidence state.

Using the hidden fault-set label directly would be an oracle shortcut and is
forbidden by SIM-029. SIM-032 therefore asks whether the enrichment can be
operationalized using only the already-admitted synthetic causal probes.

## Policies

### Biopsy all

Reference cost ceiling.

### Random same-budget

Biopsy exactly the same number of episodes selected by the causal policy, but
choose them randomly.

### Causal targeting

Use the SIM-022 paired causal probes to infer the four-dimensional fault set.
Biopsy only episodes whose **predicted** fault set equals the stratum frozen by
SIM-031.

### Oracle targeting

Use the true synthetic fault label.

This is reported only as an upper bound and is explicitly
NOT_ADMISSIBLE_LATENT_TRUTH.

## Metrics

- biopsy count and fraction;
- rare-state recall;
- biopsy precision;
- episodes per captured specimen;
- precision enrichment over same-budget random;
- biopsy reduction versus biopsy-all.

The policy is considered useful when it captures at least three held-out rare
specimens, beats same-budget random precision, and reduces biopsy load by at
least 80%.

## Boundary

~~~text
Rare-State Enrichment != Permission To Treat
Synthetic Stratum != Human Phenotype
~~~

The experiment tests research sampling efficiency only.
