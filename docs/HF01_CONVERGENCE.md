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


## Loop 5 — paired human scalp public-data falsification

The frozen axis specification was executed on GSE36169 without post-hoc gene
selection.

Positive control:

~~~text
PTGDS bald-minus-haired mean log2 delta = +1.927634
direction = 5/5
~~~

Frozen-axis outcomes:

~~~text
WNT / regeneration loss       +0.727979   5/5 paired direction
ECM / structural remodeling   +0.739120   5/5 paired direction
hypoxia / oxidative           +0.194802   4/5 paired direction
inflammation                  +0.371793   4/5 paired direction, only 2 genes
androgen transcript axis      -0.058722   2/5 paired direction
vascular transcript axis      -0.144918   2/5 paired direction
~~~

Important model update:

The negative androgen/vascular results are retained. They falsify the stronger
observer assumption that whole-scalp transcript abundance is a direct proxy for
local androgen-driver or dermal-papilla vascular state.

Disposition:

~~~text
R regenerative candidate                 STRENGTHENED
F* structural-remodeling candidate       STRENGTHENED
A bulk-transcript observer               WEAKENED
vascular bulk-transcript observer        REJECTED FOR CURRENT PANEL
~~~

## Loop 6 — observation-cost failure and harness adaptation

An independent GSE90594 transfer was implemented, but the automatic workflow
required the large GPL17077 annotation object. Two executions were terminated
by hosted-runner shutdown signals before analysis completion.

The loop classified this as:

~~~text
observation / infrastructure cost failure
!= biological result
~~~

Rather than repeatedly retrying the same expensive path, HF01 preserved the
frozen script and switched the next automatic transfer test to GSE93766, whose
gene-level Cuffdiff artifact already contains gene identifiers.

This is a harness self-improvement result:

> When an evidence channel is too costly or unstable, first seek an
> information-equivalent lower-friction observation path rather than adding
> more controller recursion.

## Loop 7 — dermal-papilla cell-model transfer

GSE93766 BK0 vs NBK0 was analyzed with the unchanged axis specification.

A first result was discarded because Cuffdiff contrast orientation had not yet
been mechanically verified.

A known-answer test was added:

~~~text
sample_1 = BK0
sample_2 = NBK0
raw log2(value_2/value_1) = +2
=> HF01 bald-minus-nonbald effect = -2
~~~

The corrected public-data workflow and ordinary CI both pass.

Corrected frozen-axis outcomes:

~~~text
androgen / growth suppression
    mean finite signed log2 FC = +1.180584
    direction alignment        = 5/7

WNT / regeneration loss
    mean finite signed log2 FC = +1.163161
    direction alignment        = 4/6

ECM / structural remodeling
    mean finite signed log2 FC = +0.881893
    direction alignment        = 5/6

vascular regression
    mean finite signed log2 FC = -2.190883
    direction alignment        = 1/4

hypoxia / oxidative
    mean finite signed log2 FC = -0.495191
    direction alignment        = 1/5

inflammation
    mean finite signed log2 FC = +0.959649
    direction alignment        = 2/4
~~~

The inflammatory axis is classified as mixed because the mean is driven by
large CCL2/IL6 effects while half of the available genes oppose the declared
direction.

## Cross-dataset convergence

Only two declared axes currently show strong directional transfer across both
very different public-data systems:

~~~text
WNT / regeneration loss
ECM / structural remodeling
~~~

This drives a model reduction.

The biological interpretation should now distinguish:

~~~text
R:
    replicated regenerative-state candidate

F*:
    replicated structural-remodeling candidate

F:
    synthetic structural-lock / hysteresis variable
    NOT biologically validated

A:
    plausible local driver/mechanism state
    observer depends strongly on cell type / measurement channel

V:
    published local vascular mechanism candidate
    current frozen transcript observer rejected

Q, P, N:
    source-supported or hypothesized states not validated by this public-data
    bridge
~~~

## Updated convergence boundary

The strongest biological-compatible statement is now:

> A paired human scalp dataset and a distinct dermal-papilla cell model both
> support pre-registered disease-associated directions for a
> WNT/regeneration-loss axis and an ECM/structural-remodeling axis.

This does **not** prove:

- that the structural axis is a mechanical lock;
- that biological hysteresis exists;
- that awareness or behavior can reverse AGA;
- that a non-invasive observer can estimate R or F* accurately;
- that restoring either axis restores hair.

The next information bottleneck is therefore longitudinal observability, not
another synthetic meta-layer.

## Current fixed point

Synthetic-control layer:

~~~text
CONVERGED V0
~~~

Cross-sectional public-data layer:

~~~text
LOCALLY CONVERGED V1:
    R and F* survive the current transfer tests;
    several broader axes do not.
~~~

Human recoverability / self-calibration layer:

~~~text
OPEN
~~~

Stopping rule for the current loop:

> Do not add further internal complexity until new evidence can discriminate
> structural remodeling from true path-dependent loss of recoverability.

The next high-value evidence is longitudinal or intervention-linked data with
repeated follicle output plus at least one independent structural/regenerative
probe.
