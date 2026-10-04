# HF01 Convergence V3 — Temporal System Identification

> Purpose: current compact reconstruction of HF01 after biological state splitting,
> assurance-kernel convergence, branch-identifiability analysis, and temporal-linkage
> failure injection.
>
> Clinical authority: **NONE**.
>
> This document supersedes V2 as the shortest current research reconstruction; V2 is
> retained as history.

## 1. Current research question

HF01 does **not** currently ask whether awareness alone regrows hair.

The current question is:

> Can a partially observed human hair-follicle system lose controllability or
> recoverability before visible output reveals it, and can we measure state,
> local response susceptibility, structural context, and later function without
> confusing different biological branches or creating the signal through the
> measurement/probe itself?

The desired chain is:

~~~text
hidden state
  -> calibrated observation
  -> controlled perturbation response
  -> linked later function
  -> only then: recoverability inference
~~~

Every arrow remains independently challengeable.

## 2. Biological state taxonomy V2

Current biological interpretation uses the expanded coordinates:

~~~text
D       upstream DHT-like ligand/input
A_AR    canonical androgen-receptor signaling state
Q       stress / neuroendocrine / context state
R       regenerative-state candidate
P       functional progenitor-compartment/reserve candidate
N       stem-cell / niche-integrity candidate
E       ECM / fibrogenic-remodeling candidate
M       mechanical / contractile-state candidate
F_hyst  synthetic hysteretic structural-lock coordinate only
H       delayed observable hair/function output
~~~

Important separations:

~~~text
D != A_AR != M
R != P != N
E != M != F_hyst
state != response susceptibility != reachability
~~~

`I` immune/microinflammatory context and `V` vascular context are not currently
promoted to uniquely identifiable dynamic coordinates.

None of R/P/N/E/M is a validated clinical scalar biomarker. `F_hyst` remains a
synthetic control variable until human longitudinal path dependence is shown.

## 3. Current biological support

### R — regenerative-state compatibility

Support spans:

1. GSE36169 paired human AGA scalp transcript projection;
2. GSE93766 balding/non-balding DP transcript projection;
3. Lu et al. 2016 human AGA protein/localization/perturbation evidence.

The first two share one frozen transcript-axis projection family. The third is
orthogonal enough to raise the synthetic root-cut for the broad R-compatibility
claim from 1 to 2.

Still blocked:

~~~text
R compatibility != validated R scalar
R state != treatment-response meter
R response != recoverability
~~~

### P — progenitor-state compatibility

Human AGA evidence supports preserved stem-cell markers alongside depleted or
altered progenitor populations, including Garza et al. 2011 and Bazid et al.
2026.

This supports:

~~~text
stem-cell presence != progenitor abundance/competence
~~~

It does not show that one marker uniquely measures P or that marker restoration
restores function.

### E / M / F_hyst — structural split

Current model no longer calls one variable simultaneously fibrosis, contraction,
mechanotransduction and irreversibility.

~~~text
E  = ECM/fibrogenic-remodeling candidate
M  = CTS mechanical/contractile-state candidate
F_hyst = synthetic path-dependent lock
~~~

Li et al. 2026 supplies directional human-HF / humanized-model evidence for:

~~~text
CTS hypercontraction
  -> PIEZO1-associated mechanotransduction
  -> progenitor apoptosis/depletion
  -> ORS/matrix proliferation suppression
  -> HF-growth impairment
~~~

Mechanical inhibition/rescue supports `M -> P/function` as a directional
experimental path. It does **not** establish `M == F_hyst` or full recoverability.

## 4. Parallel androgen-response branches

The 2026 CTS study creates an important branch-identification constraint.
DHT can influence a canonical AR-linked branch and a CTS mechanical branch.
AR knockdown relieved part of DHT-associated growth inhibition but did not abolish
CTS contraction in the reported system, while GPR133/contractility interventions
acted on the mechanical route.

Therefore HF01 no longer treats one undifferentiated `androgen pressure` scalar as
safe for actuator-specific reasoning.

Synthetic local output model:

~~~text
effect ~= alpha * A_AR + mu * M
~~~

Each intervention supplies a measured branch-direction row:

~~~text
[A_AR activity, M activity]
~~~

Known design result:

~~~text
DHT only                    rank 1
more DHT doses same ratio   rank 1
orthogonal branch inputs    rank 2
~~~

More samples along one direction do not identify two branches.

## 5. Rank is not enough

A technically rank-2 intervention design can be nearly parallel and therefore
fragile.

HF-SIM-033 uses:

~~~text
separation = |det(p1,p2)| / (||p1|| ||p2||) = |sin(theta)|
~~~

~~~text
0 -> collinear
1 -> orthogonal
~~~

Therefore nominal intervention labels are insufficient. Actual branch directions
must be estimated from proximal readouts.

Current source-bound readout candidates:

### A_AR proximal family

- miR-221 response in human DPC/DSC;
- AR occupancy at the miR-221 promoter by ChIP/ChIP-qPCR.

Source: Li et al. 2023, which reports DHT-associated miR-221 induction, reduction
after AR knockdown, and AR promoter occupancy.

Important:

~~~text
AR abundance != AR activity
miR-221 != unique AR scalar
IGF-1 != AR-specific sensor
~~~

### M proximal family

- p-MLC2 localized to alpha-SMA-positive CTS;
- AFM-derived contractility/mechanics;
- direct intact-follicle contraction/width trajectory under live imaging.

Important:

~~~text
p-MLC2 != tissue contraction by itself
contractile transcript signature != measured mechanics
mechanical response != recoverability
~~~

## 6. State != susceptibility

HF-SIM-036 instantiates the state/response distinction locally:

~~~text
x(u + du) ~= x(u) + chi * du
chi = partial x / partial u
~~~

Two follicles can share the same baseline state while having different or opposite
local response gains.

Therefore:

~~~text
baseline M != M susceptibility
baseline A_AR proxy != AR-response susceptibility
baseline R compatibility != regenerative actuator response
susceptibility != long-horizon recoverability
~~~

The next system-identification design should measure baseline and, only when
appropriately controlled, a small prospectively declared perturbation response.

## 7. Unit continuity — the temporal-linkage failure

A major new failure mode is destructive early measurement.

If day-3 molecular state is measured in one follicle and day-7 function in another,
matching group means do not identify within-follicle prediction.

HF-SIM-034 freezes a deterministic counterexample:

~~~text
early marginal: (0, 1)
late marginal:  (0, 1)

pairing A covariance = +0.25
pairing B covariance = -0.25
~~~

Same marginals, same means, opposite within-unit association.

Therefore:

~~~text
Temporal Order != Unit Linkage
Group Co-movement != Within-unit Prediction
~~~

HF01 now distinguishes:

~~~text
L0 group marginals
L1 donor-linked sibling replicates
L2 same-follicle longitudinal observation
L3 same-participant/region longitudinal observation
~~~

Claim strength may not silently jump between these levels.

## 8. Observer back-action

Same-unit observation introduces another failure mode:

~~~text
Non-destructive != Non-perturbative
~~~

Live fluorescence/confocal imaging can alter physiology through illumination,
fluorophore chemistry, ROS/heat, environmental drift or repeated handling.

HF-SIM-035 therefore requires an equivalence-style back-action gate before a live
observer is treated as passive enough for later-trajectory inference.

PASS requires:

- observer-free/sham control;
- matched environment and handling time;
- later functional endpoint;
- at least one acquisition-dose/frequency challenge;
- a predeclared equivalence margin;
- the full confidence interval for observer effect inside that margin.

~~~text
p > 0.05 != equivalence
~~~

An interval crossing the equivalence boundary stays UNKNOWN.

## 9. Active diagnostic-probe back-action

Susceptibility cannot be measured without an input.

That input can itself push the follicle onto a new trajectory:

~~~text
Active Probe != Passive Observation
~~~

HF-SIM-037 separates diagnostic-input back-action from imaging/observer back-action.

Before an active response is reused to forecast a baseline-like later trajectory,
HF01 requires:

- prospectively frozen challenge magnitude/duration;
- sham challenge;
- predeclared washout interval;
- remeasurement of the relevant state after washout;
- equivalence bound on persistent probe effect;
- later functional control.

If the challenge does not wash out, it may still be scientifically useful as an
intervention experiment, but it is not a neutral diagnostic probe for the original
trajectory.

## 10. Human organ-model bridge

The 2026 human AGA organ model remains an important architecture:

~~~text
input: DHT
internal probes: beta-catenin, IGF-1, TGF-beta1, DKK1, p21, AR, versican, K15
function: growth, cycle/catagen, matrix proliferation, apoptosis
rescue inputs: minoxidil, bicalutamide
~~~

It provides a stronger input -> state -> function bridge than cross-sectional
tissue comparisons.

However, GSE267664 RNA-seq remains quarantined because repository metadata contain
an unresolved human-vs-mm10/reference-build provenance discrepancy. Paper-level
phenotyping remains source-bound; raw/processed RNA claims are blocked until that
provenance issue is independently resolved.

## 11. Assurance kernel fixed point

The visible proof skeleton remains short and claim-conditioned:

~~~text
DESCRIPTIVE:
  PROVENANCE -> UNCERTAINTY

STATE/RESPONSE:
  PROVENANCE -> STATE-vs-RESPONSE -> UNCERTAINTY

REACHABILITY:
  PROVENANCE -> STATE-vs-RESPONSE -> UNCERTAINTY -> REACHABILITY
~~~

The hidden authority kernel additionally requires:

~~~text
structured claim semantics
  -> usable evidence witnesses
  -> defeater disposition
  -> acyclic primitive-grounded support graph
  -> explicit trust roots
  -> dependency freshness
  -> authority decision
~~~

The four visible roles are not expanded every time a new internal failure mode is
found. New rigor is absorbed inside the existing semantic barriers when possible.

## 12. Probe selection V2

HF01 no longer uses one universal probe score by default.

Why: one desirable property must not compensate for a missing inferential
necessity. For example, high root-cut gain cannot compensate for missing same-unit
linkage in a within-follicle prediction claim.

Current selection order:

~~~text
1. claim-relative hard eligibility gates
2. Pareto comparison among eligible probes
3. cost only where tradeoffs remain
~~~

Dimensions include:

- structural/evidence independence;
- measured branch separation;
- required unit linkage;
- observer back-action control;
- cost.

For a within-follicle temporal objective, same-follicle linkage and controlled
observer back-action are hard gates.

## 13. HF-VAL-006 — next shortest biological experiment

HF-VAL-006 freezes the current shortest route to a stronger temporal claim in an
ex-vivo human HF system.

Question:

> Does an early, adequately calibrated same-follicle mechanical state or local
> mechanical susceptibility improve prediction of later follicle function beyond
> baseline output, region/intervention information and donor structure?

Gates before primary analysis:

1. live observer back-action PASS;
2. if active probing is used, post-probe recovery/washout PASS;
3. early and late measurements remain attached to the same follicle;
4. donor and scalp region remain hierarchical identifiers.

Model ladder:

~~~text
M0: late output ~ baseline output + region + intervention + donor structure
M1: M0 + early M-state
M2: M1 + early M-susceptibility, only if active-probe recovery passes
~~~

Validation must hold out donors, not merely random follicles.

A PASS would support only:

~~~text
within-follicle temporal predictive information
in the declared ex-vivo human organ system
~~~

It would **not** establish in-vivo human recoverability.

## 14. Current rejection ledger

HF01 currently rejects or blocks:

~~~text
hair appearance -> unique internal state
same group means -> same within-unit relation
more DHT doses -> more branch identifiability
rank 2 -> robust identification
nominal drug selectivity -> measured branch selectivity
non-destructive observation -> no observer effect
small p-value / non-significance -> equivalence
active diagnostic probe -> passive observation
baseline state -> local susceptibility
early response -> recoverability
cross-sectional separator -> treatment-response meter
formal proof trace -> evidence validity without witnesses
absence of recorded defeaters -> absence of defeaters
more datasets -> more independent evidence
~~~

## 15. Current local fixed point

~~~text
Synthetic control / partial observability       LOCAL FIXED POINT
Assurance / projection kernel                   LOCAL FIXED POINT V2
Biological taxonomy D/A_AR/E/M/F_hyst           STRUCTURE UPDATED
R state compatibility                           STRENGTHENED, NOT SCALAR
P progenitor-state compatibility                SOURCE-BOUND HUMAN SUPPORT
M -> P/function directional path                SOURCE-BOUND EXPERIMENTAL SUPPORT
A_AR vs M branch distinction                    BIOLOGICALLY MOTIVATED + SYNTHETIC ID MODEL
Branch identifiability                          DESIGN CONTRACT FROZEN
Within-unit temporal linkage                    FAILURE MODE FROZEN
Observer back-action                            GATE FROZEN, EMPIRICAL PASS NOT YET SHOWN
Active-probe washout                            GATE FROZEN, EMPIRICAL PASS NOT YET SHOWN
Same-follicle early-state -> later-function     HF-VAL-006 PRE-REGISTERED
Biological hysteresis / F_hyst                  OPEN
In-vivo human recoverability                    OPEN
Normal-model feedback -> follicle state         OPEN
Normal-model feedback -> hair recovery          UNPROVEN
Clinical authority                              NONE
~~~

## 16. Next shortest research path

Do not add another meta-layer unless a new failure survives the current kernel.

Highest-information next steps are now:

1. determine whether an intact-HF mechanical observer can meet the observer
   back-action equivalence gate under a predeclared acquisition regime;
2. if local susceptibility is probed, establish or reject post-probe washout
   before using that follicle for baseline-like later prediction;
3. execute or source a donor-linked same-follicle temporal dataset capable of
   comparing M0/M1/M2 under donor-held-out validation;
4. search specifically for discordant same-unit cases: favorable early M/R/P
   response but poor later functional rescue;
5. strengthen P with functional conversion/competence evidence, not merely another
   static marker panel;
6. keep biological reachability and in-vivo recoverability UNKNOWN until the
   temporal/linkage/structural conditions are simultaneously satisfied.

Current optimization target:

> **Maximum inferential separation per biological unit, while preserving unit
> identity and preventing the observer/probe from creating the trajectory being
> predicted.**
