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


## Loop 8 — longitudinal evidence and dynamic observability

Cross-sectional differences cannot establish whether an internal response
precedes a later output change.

Two published human intervention designs were added as source-bound design
inputs:

- Tang et al. 2003 (PMID 12894070): 9 men, dermal-papilla molecular
  measurement after 4 months of finasteride and photographic outcome at
  12 months. Early IGF-1 change was associated with later outcome.
- Mirmirani et al. 2015 (PMID 25204361): controlled prospective minoxidil
  pilot combining scalp transcriptomics with photographic observation.

These studies do not validate HF01 recoverability. They establish that an
intervention-linked early-state / later-output observation architecture is
possible in humans.

HF-VAL-002 was frozen:

~~~text
M0:
    late output ~ baseline output + baseline covariates

M1:
    late output ~ baseline output + baseline covariates + early state response
~~~

A candidate dynamic probe is promoted only if M1 improves held-out prediction
and transfers across independent intervention-linked data.

## Loop 9 — synthetic early-response probe

HF-SIM-002 asks whether a hidden response can become informative before the
coarse output shows comparable intervention benefit.

Two states start with identical:

~~~text
H0 = 0.50
~~~

but different synthetic structural state.

Under the same upstream control:

~~~text
early checkpoint:

recoverable:
    intervention-linked Delta R = +0.268981
    intervention-linked Delta H = +0.033543

locked:
    intervention-linked Delta R = +0.141960
    intervention-linked Delta H = +0.004952

late checkpoint:

recoverable Delta H = +0.517550
locked Delta H      ~ +0.000000077
~~~

Important negative result:

The locked state still exhibits a positive early regenerative response while
failing to produce meaningful late recovery.

Therefore, even inside the synthetic equations:

~~~text
Early Molecular Response != Recoverability
~~~

Dynamic response is informative but insufficient without state/structural
context.

## Loop 10 — pre-registered minoxidil actuator test

HF-DATA-003 froze a prediction before the repository data run on GSE178510:

~~~text
input:
    minoxidil, 48 h, primary HFDPC 2D culture

primary prediction:
    frozen WNT/regeneration-loss disease axis should move < 0
    if the static disease axis is also a valid monotonic response coordinate
~~~

The final observer ignores the vendor fold-change sign convention and computes
directly:

~~~text
effect(g)
  = log2 MINOXIDIL signal
  - log2 CONTROL signal
~~~

Known-answer CI freezes this convention.

Result:

~~~text
frozen WNT/regeneration-loss mean score = +0.159093
expected                              = < 0
PRIMARY TEST                          = FAIL
~~~

Four of six individual contributions move opposite the disease direction, but
the pre-registered mean remains positive. The failed aggregate prediction is
retained.

This produces a stronger model correction:

~~~text
State Separation Axis != Actuator Response Axis
~~~

The associated publication independently reports Wnt/beta-catenin pathway
effects after minoxidil. Therefore the failure is not interpreted as absence of
WNT biology. It rejects the assumption that the frozen cross-sectional
disease-state projection is automatically a monotonic intervention-response
coordinate.

Disposition:

~~~text
R_state:
    retained as a cross-sectional disease-state candidate

R_response:
    OPEN; must be independently defined/validated from intervention-linked data
~~~

## Loop 11 — normal-model feedback gate

The original awareness question was decomposed:

~~~text
normal/reference presentation
    -> comprehension
    -> learned/behavioral control
    -> fast physiology
    -> follicle state
    -> delayed hair output
~~~

Each arrow is now a separate validation gate.

Human biofeedback and conditioning literature establishes only a general,
context-dependent possibility that learned feedback can alter psychological,
autonomic, endocrine, or immune responses.

It does not establish a hair-follicle route.

HF-VAL-003 therefore compares:

~~~text
A: static educational normal model
B: sham/non-contingent feedback
C: contingent personalized feedback
~~~

The first primary endpoint is a pre-specified fast controllable state, not hair
growth.

A failure at this gate weakens the feedback channel; it is not repaired by
asking the participant to try harder.

## Loop 12 — fail-closed reachability semantics

HF-SIM-003 formalizes decision uncertainty.

If every latent state still compatible with evidence is recoverable:

~~~text
RECOVERABLE
~~~

If none are:

~~~text
NONRECOVERABLE
~~~

If candidate states disagree:

~~~text
UNKNOWN
~~~

The matched-H known answer contains one recoverable and one nonrecoverable
latent state with identical H0=0.50.

Therefore:

~~~text
H-only evidence -> UNKNOWN
~~~

New invariant candidates:

~~~text
Observation uncertainty must propagate into reachability uncertainty
UNKNOWN != RECOVERABLE
UNKNOWN != NONRECOVERABLE
Probe value is decision-dependent, not merely descriptive
~~~

## Loop 13 — observation-harness stabilization

Repeated PR synchronization caused the live GEO workflow to re-download
immutable public data and eventually trigger NCBI HTTP 403 rate limiting.

This was classified as:

~~~text
harness / observation transport failure
!= analysis result
!= biological falsification
~~~

Live GEO revalidation is now an explicit manual workflow. Ordinary CI remains
network-independent and tests parsers, sign conventions, and frozen
known-answer contracts.

## Current reduced model

The autonomous loop now distinguishes four different objects that were
initially conflated:

~~~text
1. x_state
   current latent biological state

2. phi_state(y)
   observation features used to estimate that state

3. chi_u(x)
   susceptibility / early response to a declared input

4. Reach(x, U)
   whether the target region is reachable with actuator class U
~~~

These are not interchangeable.

A normal-model UI can help only through the controller side:

~~~text
reference
  -> observation
  -> residual
  -> bounded controller response
  -> measured susceptibility
  -> updated state estimate
  -> reachability decision
~~~

It is not a biological restore image.

## Updated fixed point

### QED inside the declared synthetic model

The current synthetic contracts establish:

1. current visible hair output does not uniquely identify latent state;
2. equal visible output can hide opposite future reachability;
3. early hidden-state response can precede visible-output separation;
4. positive early internal response does not guarantee late recovery;
5. uncertain latent reachability must produce UNKNOWN rather than a confident
   recoverable/nonrecoverable claim.

### Public-data compatible, not QED

Current cross-sectional data support:

~~~text
R_state  regenerative-state candidate
F*       structural-remodeling candidate
~~~

but do not prove biological hysteresis or recoverability.

### Explicitly rejected / weakened

~~~text
whole-scalp androgen transcript abundance == androgen driver state
current vascular transcript panel == local vascular state
cross-sectional disease axis == actuator response axis
normal-model comprehension == biological recovery
early molecular response == recoverability
~~~

### Evidence needed to reopen internal model recursion

The next material model change requires at least one of:

1. longitudinal human data with repeated internal state probe(s), declared input,
   and later hair output;
2. intervention-linked data that independently validates a dynamic response
   coordinate;
3. a sham-controlled personalized-feedback study showing a measurable Gate-1
   physiological effect followed by a follicle-relevant Gate-2 measurement;
4. longitudinal evidence of path dependence that distinguishes structural
   remodeling from true biological hysteresis.

Until such evidence appears, adding another synthetic meta-layer is not
justified.

~~~text
SYNTHETIC INTERNAL LOOP: LOCAL FIXED POINT
CROSS-SECTIONAL BIOLOGICAL LOOP: LOCAL FIXED POINT
DYNAMIC HUMAN RECOVERABILITY: OPEN EVIDENCE BOTTLENECK
NORMAL-MODEL AWARENESS -> HAIR RECOVERY: UNPROVEN
~~~


## Loop 14 — projection-gap hypothesis

A new failure mode was introduced:

~~~text
endpoint model may be coherent
endpoint evidence may be real
but the semantic projection between them may be too sparse for reliable human reconstruction
~~~

HF01 now treats projection density as a first-class design variable.

This does not assume that every disagreement is cognitive friction. The new
question is whether missing intermediate representations explain some failures
of recognition after the empirical bridge itself is already adequate.

## Loop 15 — finite optimal granularity

HF-SIM-004 freezes a cognitive-friction surrogate:

~~~text
J(n) = alpha * D^2 / n + beta * n
~~~

where:

~~~text
D      semantic/projection distance
alpha  penalty for large jumps
beta   per-stage overhead
n      explanatory transitions
~~~

For positive D, alpha, beta:

~~~text
n* = D * sqrt(alpha / beta)
~~~

and J is strictly convex.

Frozen known answer:

~~~text
D=8, alpha=1, beta=1

direct:       n=1   J=65
optimum:      n=8   J=16
over-detailed n=32  J=34
~~~

The theorem is about the declared surrogate, not human working-memory capacity.

Disposition:

~~~text
too sparse != optimal
too dense  != optimal
adaptive finite depth retained
~~~

## Loop 16 — heterogeneous gradient

A uniform ladder is also too coarse.

For local span j:

~~~text
J_j(n_j) = alpha*w_j*d_j^2/n_j + beta*n_j

n_j* = d_j * sqrt(alpha*w_j/beta)
~~~

where w_j represents declared local difficulty/uncertainty.

This means explanatory density should increase at difficult domain changes and
collapse across familiar/easy transformations.

The same endpoint can therefore be rendered at different depths without
changing the underlying evidence.

## Loop 17 — evidence-preserving edge contracts

A new meta-risk appeared:

> Adding intermediate concepts can make an unsupported causal story feel
> smoother.

HF-SIM-005 therefore assigns each scientific projection edge:

~~~text
SUPPORTED
ASSUMED
UNKNOWN
FALSIFIED
~~~

and propagates the most restrictive endpoint ceiling:

~~~text
all supported                -> GROUNDED
any assumed                  -> MODEL_ONLY
any unknown                  -> UNKNOWN
any required falsified edge  -> FALSIFIED
~~~

Adding more supported explanation steps cannot rescue an assumed or unknown
scientific edge.

New invariant:

~~~text
Explanation Smoothness != Evidence Authority
~~~

## Loop 18 — projection mesh

The single ladder was then rejected as insufficient.

Projection failure is now decomposed into two independent dimensions:

~~~text
E = epistemic gap
    missing measurement / causal / provenance / validation bridge

C = cognitive gap
    bridge exists but is too compressed for reliable human reconstruction
~~~

Controller policy:

~~~text
E low, C low:
    collapse redundant explanation

E low, C high:
    add intermediate representation
    test reconstruction

E high, C low:
    collect/validate evidence
    preserve UNKNOWN
    do not explain around the gap

E high, C high:
    improve evidence and representation separately
~~~

HF-SIM-006 freezes this quadrant logic.

New invariant:

~~~text
Explanatory refinement cannot repair missing empirical evidence
Empirical refinement does not automatically repair comprehension
~~~

## Loop 19 — HF01 concrete projection map

The current R_state path is now explicitly represented as:

~~~text
formal latent candidate
  -> biological interpretation
  -> mechanism family
  -> measurable probe
  -> normalized public-data result
  -> falsification boundary
  -> calibrated human claim
  -> next discriminating probe
~~~

For the current WNT/regeneration candidate:

~~~text
epistemic gap:
    MODERATE
    cross-sectional transfer exists
    longitudinal recoverability is unproven

cognitive gap:
    HIGH if rendered directly as pathway-score -> latent-state headline
~~~

For:

~~~text
normal-model presentation -> hair recovery
~~~

the classification is different:

~~~text
epistemic gap:
    HIGH

cognitive gap:
    LOW-to-MODERATE
~~~

The causal story is easy to narrate, which makes this path especially
susceptible to explanation fluency exceeding evidence authority.

## Loop 20 — adaptive projection validation contract

HF-VAL-004 pre-registers three explanation conditions:

~~~text
direct endpoint projection
fixed intermediate ladder
adaptive projection ladder
~~~

Primary outcomes:

- causal-chain reconstruction;
- claim-boundary retention;
- state-vs-response distinction.

Cost outcomes:

- time to criterion;
- number of exposed stages;
- navigation burden.

The adaptive ladder passes only if it reduces reconstruction error while not
requiring unnecessary explanatory depth.

Stop rule:

> Do not add a projection stage unless it reduces a declared reconstruction or
> calibration error, or is required to expose uncertainty/provenance.

## Updated architecture

HF01 now has two coupled but non-substitutable planes:

~~~text
SCIENTIFIC PLANE
reality
  -> probe
  -> observable
  -> evidence
  -> latent-state candidate
  -> reachability model

HUMAN PROJECTION PLANE
formal result
  -> intermediate concepts
  -> concrete examples
  -> uncertainty boundary
  -> next discriminating question
~~~

They meet at typed projection edges, but one plane cannot repair the other.

## New local fixed point

The original user direction is now formalized as:

~~~text
Large model-to-reality or model-to-human jumps may create avoidable friction.

Insert intermediate projections only where the local semantic/evidential
curvature justifies them.

Preserve every unsupported scientific edge as ASSUMED/UNKNOWN/FALSIFIED.

Optimize for minimum exposed complexity subject to:
    correct reconstruction
    calibrated uncertainty
    preserved evidence authority
~~~

Current status:

~~~text
projection granularity theorem           SYNTHETIC QED
adaptive heterogeneous allocation        SYNTHETIC QED
evidence-ceiling propagation             SYNTHETIC QED
epistemic/cognitive gap separation       SYNTHETIC QED
human comprehension benefit              OPEN: HF-VAL-004
hair-biological benefit                  NOT IMPLIED / OPEN
~~~


## Loop 21 — minimum sufficient checkpoint set

The user direction was sharpened:

> Do not preserve every intermediate explanation. Preserve only the checkpoints
> whose omission permits the system to break.

HF-SIM-007 formalizes this as a small exact set-cover problem.

Let:

~~~text
F = declared catastrophic failure modes
S_i = failures blocked by checkpoint c_i
~~~

Then choose:

~~~text
C* = argmin |C|
subject to
union(S_i for c_i in C) = F
~~~

A checkpoint is structurally critical when counterfactual deletion exposes a
required failure mode.

A checkpoint is removable when deletion preserves coverage of every declared
failure.

This separates useful information from correctness-critical barriers.

## Loop 22 — mandatory role vs mandatory instance

The set-cover view was still insufficient because two different concrete
checkpoints may implement the same required semantic function.

HF-SIM-008 therefore models the projection as a directed graph.

A concrete node is a dominator only when every accepted source-to-target path
contains that exact node.

More importantly:

> A semantic role is a role-dominator when every accepted path contains some
> node implementing that role.

This permits alternative visualizations or interaction patterns without
allowing the invariant itself to disappear.

Current HF01 role candidates:

~~~text
PROVENANCE
STATE-vs-RESPONSE TYPING
UNCERTAINTY / CLAIM CEILING
REACHABILITY / UNKNOWN
~~~

A bypass path that reaches the endpoint without one of these required roles is
invalid.

## Current compact projection skeleton

The previously long ladder can now compress to:

~~~text
[PROVENANCE]
     ↓
[STATE vs RESPONSE]
     ↓
[UNCERTAINTY]
     ↓
[REACHABILITY or UNKNOWN]
     ↓
calibrated claim
~~~

Mechanistic, molecular, mathematical, and visual detail is expandable between
these barriers.

The barriers themselves may be rendered compactly after the user demonstrates
understanding, but they cannot be bypassed.

## New fixed-point interpretation

Intermediate representations fall into two classes:

~~~text
optimization nodes:
    useful only while they reduce reconstruction friction

correctness barriers:
    must remain functionally present because removing them permits a known
    failure class
~~~

The meta-meta target is therefore:

~~~text
minimum visible path
subject to
all mandatory semantic roles dominating every accepted endpoint path
~~~

This is the current strongest form of the projection-compression hypothesis.

## Updated invariant set

~~~text
More Detail != Better Projection
Explanation Smoothness != Evidence Authority
Endpoint Correctness != Human-Reconstructible Path
Optimization Node != Correctness Barrier
Checkpoint Instance != Checkpoint Role
Compression is allowed between barriers, not through barriers
~~~

The next empirical validation is still HF-VAL-004: test whether an adaptive
minimal path preserves reconstruction and uncertainty with less exposed
explanatory cost than a fixed ladder.
