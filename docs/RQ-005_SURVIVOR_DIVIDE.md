# RQ-005 Survivor Divide Protocol

## Purpose

Find the earliest reproducible state difference between clinically comparable
patients who later follow exceptional/long-term-survival versus short-survival
trajectories.

**Hope is one candidate variable, not the privileged hypothesis.**

The target is the watershed:

> Which measurable state, transition, interaction, or latent regime first
> separates the trajectories, and does that separation survive controls for
> tumor biology, treatment, baseline disease burden, and reverse causality?

## DCS framing

The protocol imports four DCS invariants:

~~~text
Outcome != Mechanism
Current State != Complete Causal History
Surface Improvement != Root-State Improvement
Observation Channel != Latent State
~~~

Therefore "survivor" is an endpoint label, not an internal-state explanation.

## State vector

For patient i at time t:

~~~text
z_i(t) = [
    B_i(t),   # tumor biology / burden
    M_i(t),   # treatment exposure / effective dose
    I_i(t),   # immune / tumor microenvironment
    N_i(t),   # neuroendocrine / systemic inflammatory state
    H_i(t),   # health behavior / sleep / activity / adherence
    P_i(t),   # psychological / agency / distress / meaning
    C_i       # fixed or slowly varying confounders
]
~~~

No component is assumed dominant in advance.

## Two analysis modes

### Mode A — retrospective contrast

Use matched or stratified long-term/exceptional survivors and short-term
survivors to discover candidate divergence axes.

This mode is useful for finding signals but is vulnerable to survivor-label
leakage, immortal-time effects, collider bias, and reverse causality.

### Mode B — prospective validation

Fit the time-varying state to future hazard/response without feeding a future
survivor label into the predictor.

Candidate form:

~~~text
lambda_i(t)
  = lambda_0(t)
  * exp(
      beta_B B_i(t)
    + beta_M M_i(t)
    + beta_I I_i(t)
    + beta_N N_i(t)
    + beta_H H_i(t)
    + beta_P P_i(t)
    + gamma C_i
  )
~~~

A watershed candidate must survive Mode B before being promoted beyond
exploratory status.

## Survivor State Divergence

For each layer j, compute a pre-declared standardized group difference:

~~~text
D_j(t)
  = standardized_difference(
      X_j(t) | future-LTS,
      X_j(t) | future-STS
    )
~~~

The first persistent divergence is:

~~~text
tau_j
  = min t such that
    |D_j(t)| >= delta
    for K consecutive observations
~~~

delta and K must be frozen before outcome inspection.

A transient spike is not a watershed.

Implementation:
[src/dissociated_control_systems/survivor_divergence.py](../src/dissociated_control_systems/survivor_divergence.py)

## Competing causal worlds

The first model competition must include at least:

~~~text
W0  baseline / no extra divergence
WB  tumor-biology-first
WM  treatment-exposure-first
WI  immune/TME-first
WN  neuroendocrine/inflammation-first
WH  health-behavior/adherence-first
WP  psychological-state-first
WR  reverse causality: tumor response -> later psychological improvement
WX  mixed / latent-regime interaction
~~~

The point is not to choose a favorite world. It is to make each world capable
of defeating the others.

## Imported methods from other research lanes

### Finite RAM Lab

Transfer only the method, not the physical mechanism:

- rare-event census rather than anecdote collection;
- preserve blocks/centers in resampling;
- pre-specified model complexity ladder;
- block-held-out scoring;
- hierarchical and mixture alternatives;
- tail / rare-state biopsy;
- Monte Carlo and posterior-predictive stress;
- inspect the failure specimen before repairing the model.

### DCS fixed-point / recovery lanes

Transfer:

- convergence depth;
- perturbation-return time;
- attractor / basin language only after a measurable dynamical signature;
- hysteresis and path dependence;
- early response != long-term reachability;
- current state != complete causal history.

### DCS observation / meta-loop lanes

Transfer:

- independent observation channels;
- improve evidence architecture before adding deeper controllers;
- active observation by information-per-cost;
- retain perishable evidence windows;
- abstain / UNKNOWN when the state is non-identifiable.

## External evidence already constraining the model

### NCI Exceptional Responders Initiative

111 exceptional responders underwent multi-platform tumor profiling.
Plausible molecular mechanisms were identified in 26/111 (23.4%). The
identified categories included DNA-damage response, intracellular signaling,
immune engagement, and favorable-prognosis alterations.

Interpretation:

~~~text
known tumor mechanism explains some cases
!=
remaining cases are psychological
~~~

The unexplained fraction is a search space, not evidence for any preferred
hypothesis.

The NCI program's primary molecular/clinical data are available through the
Genomic Data Commons / controlled-access dbGaP route.

### Ovarian HGSC long-term survivors

A 2024 international cohort compared:

- LTS >=10 years: n=374
- MTS 5-7.99 years: n=433
- STS 2-4.99 years: n=416

Nine of ten immune-cell subsets were positively associated with long-term
survival versus short-term survival. Intraepithelial CD8 T cells plus
intrastromal B cells showed an approximately five-fold increased odds of LTS,
conditional on the study's analysis.

This is a strong candidate I/TME divergence axis.

### Stage III triple-negative breast cancer

A 2025 multi-omics cohort compared 36 long-term, 62 moderate-term, and 34
short-term survivors. Long-term survival was associated with fewer metastatic
regional lymph nodes, lower stromal fibrosis, lower Ki67, homologous
recombination-related alterations, and downregulated RTK-RAS signaling.

This is a strong B/tumor-biology competitor that a psychosocial model must
beat rather than ignore.

### Longitudinal breast-cancer biobehavioral data

113 women were followed for five years with 12 repeated assessments. Stress and
depressive symptoms were measured alongside NK-cell cytotoxicity and T-cell
blastogenesis. Change points differed by variable; NK-cell cytotoxicity rose
through approximately 18 months, while psychological measures changed on
different time scales.

This supplies a real template for P/N -> I trajectory modeling without
claiming a survival mechanism.

### Ovarian GOG-218 QOL trajectories

Long-term survivors (n=260, >=8 years) and short-term survivors (n=1115, <5
years) differed in baseline and longitudinal FACT-O-TOI quality-of-life
trajectories.

This makes patient-reported state a legitimate candidate observation channel,
but not a causal explanation by itself.

## First falsification gates

A candidate watershed is rejected or downgraded if any of the following holds:

1. it appears only after the tumor-response divergence;
2. it disappears after matching/adjusting for stage, burden, subtype, and
   treatment;
3. it exists only in retrospective LTS/STS labels and fails prospective
   future-hazard prediction;
4. it is carried by one center/study block and fails block-held-out validation;
5. it depends on one arbitrary threshold or time alignment;
6. the effect reverses under plausible missing-data models;
7. a simpler tumor-biology or treatment-first model predicts held-out data
   equally well or better;
8. the variable is merely another observer of the same latent state and adds
   no conditional information.

## Negative controls

- shuffled temporal order;
- future-value leakage test;
- label-only hope perturbation with no mediator change;
- deliberately delayed psychological measurements;
- center/study label prediction;
- nonpersistent single-time-point spikes;
- matched-baseline placebo axes.

## Rare survivor biopsy

Exceptional survivors are handled like rare specimens:

~~~text
population model
  -> identify model residual/outlier
  -> freeze the case before reinterpretation
  -> reconstruct full causal history
  -> compare against matched controls
  -> test candidate hidden state
  -> replicate in an independent rare case
~~~

A survivor narrative can nominate a variable for measurement.
It cannot close the causal chain.

## Meta-loop

~~~text
observe
 -> compare competing worlds
 -> find largest residual
 -> select the next observation by value-of-information
 -> preserve the pre-repair evidence
 -> refit
 -> block-held-out test
 -> perturb assumptions
 -> biopsy failures
 -> update only the weakest model edge
 -> stop when new observations no longer change model ranking
~~~

This is the proposed convergence criterion for the first RQ-005 phase.

## Claim ceiling

The protocol may discover reproducible predictive or temporal-precedence
signatures.

It cannot, by itself, establish that a psychological state cures cancer,
establish a clinical intervention, or provide an individual prognosis.


## Meta-loop iteration 1 — threshold-crossing fragility

The deterministic precedence examples are easy by construction, so the
classifier was immediately stressed with Gaussian observation noise.

Fixed synthetic stress:

~~~text
seed              14005
trials/world       2000
noise SD           0.09 standardized-effect units
threshold          0.50
persistence        2 observations
~~~

Observed known-world classification accuracy:

~~~text
psych/neuroimmune precedence   0.7935
tumor-first / reverse          0.9195
treatment-first                0.9870
~~~

This is a method failure, not a biological result.

A small threshold/persistence grid can improve apparent accuracy, but selecting
that grid after seeing the same synthetic outcomes would merely move the
overfitting problem one level upward.

Therefore:

~~~text
first persistent divergence time
    = descriptive projection

first persistent divergence time
    != causal estimator
    != primary real-data inference engine
~~~

The real-data primary path is revised toward uncertainty-aware change-point or
state-space estimation coupled to future hazard/response, with threshold
crossings retained only as interpretable projections.

Reproducer:
[analysis/rq005_survivor_divergence_stress.py](../analysis/rq005_survivor_divergence_stress.py)

## Minimum sufficient evidence checkpoints

Borrowing the minimum-checkpoint idea from the hair-follicle DCS lane, every
accepted watershed claim must pass all of these semantic barriers:

~~~text
[PROVENANCE]
      ->
[BASELINE COMPARABILITY]
      ->
[TEMPORAL PRECEDENCE]
      ->
[INDEPENDENT LAYER EVIDENCE]
      ->
[HELD-OUT REPLICATION]
      ->
[UNCERTAINTY / CLAIM CEILING]
~~~

Compression is allowed between checkpoints, never through them.

This guards against a smooth narrative connecting a survivor testimony to an
immune observation when the required intermediate evidence was never measured.
