# HF01 Convergence Log

> Scope: synthetic-control convergence plus source-bound biological mapping.
> Clinical conclusion: NOT ESTABLISHED.

## Loop 0 — naive hypothesis

Initial question:

> Can awareness/behavior alone restore age- or androgen-associated hair loss?

Failure:

This framing collapses multiple latent mechanisms into one intervention claim
and cannot distinguish observation from actuation.

Disposition: REJECTED AS TOO COARSE.

## Loop 1 — state decomposition

Introduced:

~~~text
A androgen pressure
Q stress/neuroendocrine load
R regenerative competence
P progenitor reserve
N niche integrity
F structural/mechanical lock
H hair output
~~~

Literature mapping provides plausible domain-local candidates for several
variables, while leaving important arrows unvalidated.

Result:

~~~text
H != unique latent state
~~~

Disposition: RETAIN.

## Loop 2 — recoverability / hysteresis

A slow positive-feedback structural state was introduced.

Synthetic validation shows:

- early-state upstream correction can preserve/recover output;
- reachable state-space shrinks as F increases;
- adding regenerative or structural actuator classes expands reachability;
- late locked states can remain locked after upstream disturbance reduction.

Baseline initial-lock thresholds for final H >= 0.50:

~~~text
behavioral + antiandrogen                 0.35
+ regenerative                            0.80
+ structural                              1.00
~~~

These values are coefficient-specific and have no clinical interpretation.

A fixed-seed 300-sample all-coefficient ±20% perturbation retains the core
ordering/hysteresis acceptance rule in >=94% of cases.

Disposition: SYNTHETIC CLAIM RETAINED.

## Loop 3 — observability attack

A conceptual measurement model was added.

~~~text
visible output only                        rank 1 / 7
Tier 0: output + trichoscopy + cycle       rank 3 / 7
Tier 0 + stress/context                    rank 4 / 7
Tier 0 + context + vascular proxy          rank 5 / 7
declared research set                      rank 7 / 7
~~~

The exact ranks depend on declared synthetic sensitivities.

Durable conclusion:

> Coarse visual observation cannot justify claims about the full latent state.

Disposition: RETAIN.

## Loop 4 — output-only prediction attack

Construct two states with identical current visible output:

~~~text
H_left = H_right = 0.50
~~~

but different structural/progenitor/niche state.

Apply the same upstream control to both.

The declared model yields strongly different future output.

Therefore, inside this model:

~~~text
(H_t, u_t) is not a sufficient Markov state for predicting H_future.
~~~

This is a deterministic counterexample to an output-only controller.

Disposition: RETAIN.

## Current synthetic theorem

Within the frozen HF01 equations and parameter family:

1. visible output is not a sufficient latent-state representation;
2. the system can be path dependent;
3. recoverability can decrease before visible output uniquely reveals that loss;
4. upstream correction and structural repair are not interchangeable actuator
   classes;
5. an observer/controller should estimate hidden recoverability, not only
   optimize current visible output.

This is QED **inside the synthetic model only**.

## Biological convergence status

NOT YET QED.

Current human/animal literature is compatible with, but does not prove, the
full HF01 model.

Especially unresolved:

- whether a clinically useful scalar/low-dimensional "structural lock" exists;
- whether human AGA trajectories show enough hysteresis to improve prediction;
- which non-invasive probes estimate P/N/F with useful uncertainty;
- how much Q contributes to AGA rather than other hair-loss phenotypes;
- whether feedback-guided behavioral regulation adds independent follicular
  benefit after ordinary treatment/context is controlled.

## Public-data bridge

The next falsification stage should use public human transcriptomic datasets.

Candidate datasets:

### GSE36169

Five paired frontal-bald / occipital-haired scalp samples from men with AGA.

Use:
- within-person paired contrast;
- test whether pathway axes corresponding to regeneration, ECM/structure,
  inflammation, and vascular support differ consistently.

Risk:
- whole scalp contains multiple compartments;
- occipital tissue is not an identical saved copy of a healthy frontal scalp.

### GSE90594

Fourteen male AGA vertex scalp samples and fourteen healthy-control vertex
samples.

Use:
- external cross-person validation of axes discovered in GSE36169.

Risk:
- cohort/batch/confounding effects;
- not paired within person.

### GSE66663 / GSE93766

Balding vs non-balding dermal-papilla cell models.

Use:
- cell-type-focused test of AR/vascular/regenerative axes.

Risk:
- immortalized/culture systems are not intact scalp;
- technical replication does not substitute for biological cohort size.

## Pre-registered public-data test

Do not fit arbitrary gene sets after seeing labels.

Freeze a small set of literature-derived axes first:

~~~text
androgen / AR axis
WNT-regeneration axis
vascular-support axis
ECM / focal-adhesion / mechanical axis
immune-inflammatory axis
mitochondrial / oxidative-stress axis
~~~

For each dataset:

1. normalize using a dataset-appropriate public method;
2. compute per-sample pathway scores;
3. preserve paired structure where available;
4. estimate signed effect sizes with uncertainty;
5. test transfer of direction across independent datasets;
6. do not call a latent HF01 variable validated unless its axis replicates.

## Biological stop conditions

HF01 should abandon or heavily revise the structural-hysteresis interpretation
if independent public data repeatedly show:

- no reproducible structural/ECM/mechanical signal;
- no gain from latent-state models over output-only models in longitudinal data;
- no path dependence after controlling for androgen/cycle state;
- or the supposed hidden-state variables cannot be estimated with useful
  uncertainty from realistic probes.

## Current converged conclusion

The research question has narrowed from:

> Can a person consciously tell the body to grow hair?

to:

> Can a partially observed follicle system lose recoverability before coarse
> hair output makes that loss obvious, and can a calibrated observer detect that
> transition early enough to select the correct actuator class?

That narrower question is mathematically coherent, executable, falsifiable,
and compatible with current source-bound biological mechanisms.

The synthetic layer is CONVERGED FOR V0.

The biological layer is OPEN and must proceed through public-data and
longitudinal validation rather than stronger narrative claims.
