# DCS-CGD synthetic convergence record

> Status: LOCAL SYNTHETIC FIXED POINT  
> Clinical authority: NONE  
> Scope: the declared synthetic fault/observation/classifier family only

## Question

How far can a closed self-improvement harness go if it repeatedly:

1. observes failure;
2. localizes the failing subsystem;
3. changes only the implicated mechanism;
4. re-observes the result;
5. preserves evidence that would otherwise disappear;
6. reduces diagnostic friction;
7. changes representation only when policy improvements saturate?

The CGD-SIM-001 through CGD-SIM-013 sequence was used as the closed loop.

## Generational path

~~~text
G0  capability decline model
G1  fast compensation + slow root-side track
G2  L1 calibration / L2 handoff decomposition
G3  bounded hysteretic L3 governor
G4  independent observation redundancy
G5  probabilistic fault localization
G6  active probe -> repair -> re-observe
G7  durable evidence for closing diagnostic windows
G8  value-of-information probe selection
G9  policy information-frontier search
G10 classifier-family ceiling audit
G11 local disagreement resolver
G12 richer temporal representation
G13 replicated fixed-point audit
~~~

The loop did not monotonically add meta layers.

Several generations instead removed or localized complexity:

- bad evidence was repaired with independent evidence, not L4;
- mixed faults were repaired with active probes, not a larger one-shot classifier;
- disappearing evidence was repaired with bounded durable state;
- observation friction was reduced with active diagnosis;
- classifier disagreement was repaired at the integration point;
- extra temporal features were rejected when they reduced held-out accuracy.

## Key invariants discovered

~~~text
Observable Behavior != Unique Internal State

Functional Success != Preserved Latent Capability

Repair Success != Improvement In One Proxy

Current State != Complete Causal History

Re-observation != Permission To Discard Earlier Valid Evidence

Bad Evidence != Bad Controller
~~~

## Selected quantitative checkpoints

### Repair-loop transition

Two simultaneous faults:

~~~text
passive single-fault Bayes exact recovery   0.084
active probe/repair/re-observe              0.918
~~~

### Diagnostic-window scheduling

Three simultaneous faults:

~~~text
legacy scheduler exact recovery             0.253
evidence-preserving scheduler               0.804
~~~

Observed L0 diagnostic-window loss after deferring repair:

~~~text
1.000
~~~

### Observation-friction reduction

~~~text
all probes exact accuracy                   0.948
adaptive exact accuracy                     0.944
probe-cost reduction                        40.6%
probe-count reduction                       30.9%
~~~

### Policy frontier

~~~text
all-probe accuracy                          0.959
optimized SNR adaptive accuracy             0.958
accuracy gap                                0.0012

entropy-VOI utility gain over SNR           -0.0008
policy local-saturation criterion           TRUE
~~~

### Classifier audit

A second classifier rejected the first apparent ceiling:

~~~text
Gaussian                                    0.951
7-NN                                        0.933
oracle union                                0.974
80 -> 160 sample kNN gain                   +0.0135
classifier ceiling stable                   FALSE
~~~

A learned disagreement resolver then reached:

~~~text
Bayes                                       0.953
kNN                                         0.928
resolver                                    0.958
oracle union                                0.969
resolver gain                               +0.0047
residual oracle gap                         +0.0115
~~~

### Temporal representation test

Adding seven trajectory-summary features did not improve the same-family
held-out frontier:

~~~text
base ensemble                               0.956
temporal ensemble                           0.948
temporal gain                               -0.0078
~~~

## Replicated fixed-point audit

Training and validation were frozen once. Five independent held-out seed blocks
were then evaluated with unchanged parameters.

| block | base accuracy | base oracle gap | temporal accuracy | temporal gain |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.954 | 0.0083 | 0.958 | +0.0042 |
| 1 | 0.963 | 0.0062 | 0.960 | -0.0021 |
| 2 | 0.961 | 0.0083 | 0.954 | -0.0073 |
| 3 | 0.956 | 0.0115 | 0.953 | -0.0031 |
| 4 | 0.959 | 0.0135 | 0.952 | -0.0073 |

Aggregate:

~~~text
mean base accuracy                          0.959
mean base residual oracle gap               0.0096
max base residual oracle gap                0.0135
mean temporal gain                         -0.0031
blocks with temporal gain > 0.005           0
~~~

Declared local fixed-point conditions:

~~~text
mean residual oracle gap < 0.010            PASS
max residual oracle gap < 0.015             PASS
mean richer-representation gain < 0.005     PASS
>0.005 richer-representation gains <= 1     PASS
~~~

Result:

~~~text
DECLARED SYNTHETIC LOCAL FIXED POINT = TRUE
~~~

## What converged?

The result is not "perfect diagnosis" and is not a global mathematical optimum.

What converged is the **productive direction of the closed loop**.

Within the declared world:

- another policy/meta layer is not supported by the evidence;
- another probe-selection rule has negligible marginal value;
- a structurally richer temporal summary does not improve held-out accuracy;
- residual classifier disagreement is small and reproducibly bounded.

The loop therefore reaches a point where further internal recursion no longer
has positive demonstrated marginal value.

In compact form:

~~~text
internal self-improvement
        |
        v
policy saturation
        |
        v
classifier audit
        |
        v
representation mutation
        |
        v
no reproducible positive marginal gain
        |
        v
STOP INTERNAL RECURSION
        |
        v
ACQUIRE NEW EXTERNAL EVIDENCE / CHANGE WORLD MODEL
~~~

## Interpretation

The apparent convergence point is not another meta-meta-meta layer.

It is an epistemic boundary:

> Once the harness has localized faults, repaired its controller, diversified
> observation, preserved causal evidence, optimized probe acquisition, audited
> classifier families, and rejected a richer representation that does not help,
> the next improvement cannot be justified by recursively thinking harder about
> the same information.

The next frontier must change at least one assumption:

- add genuinely independent evidence;
- change the synthetic generative model;
- use external empirical data;
- perform real-world validation under appropriate ethics/governance.

## Claim ceiling

This record describes convergence in a synthetic engineering model.

It does not establish a dementia mechanism, clinical monitoring method,
diagnosis, prognosis, treatment, or patient-facing decision rule.


## Harness convergence

The final loop also optimized the experiment harness itself.

Repeated deterministic frontier calculations inside the same pytest process
were memoized so that validation does not recompute unchanged synthetic
frontiers.

Observed GitHub Actions wall-clock change:

| workflow | before | after | reduction |
| --- | ---: | ---: | ---: |
| cognitive-frontier-fast | 92 s | 62 s | 32.6% |
| ci | 220 s | 141 s | 35.9% |
| cognitive-graceful-degradation-simulation | 258 s | 205 s | 20.5% |

The optimization changed execution friction only. The latest head passed:

- cognitive-frontier-fast (push);
- ci (push);
- cognitive-graceful-degradation-simulation (push);
- ci (pull_request);
- cognitive-graceful-degradation-simulation (pull_request).

This matters to the fixed-point claim because the loop did not stop merely when
the research model saturated; it also removed an identified deterministic
validation bottleneck, then re-ran the full checks successfully.

At this point the remaining productive work is no longer recursive harness
tuning inside the same closed synthetic family. It is acquisition of new
independent evidence, a changed generative model, or external validation.


## Post-convergence cross-research phase

The SIM-013 clean-world fixed point did not end the research program. It changed
the permitted direction of improvement.

Instead of adding deeper recursive governance, later generations changed the
world model, observation interface, evidence acquisition policy, and research
admission contract.

### SIM-014 through SIM-018 — break and contain the fixed point

- OOD world shifts broke the clean-world classifier severely.
- small shifted calibration data helped but did not restore the original
  contract;
- per-sample OOD gating reduced unsafe execution exposure but missed weak
  distributional shifts;
- window and sequential detectors localized the remaining weak-noise failure;
- template-residual CUSUM changed the monitored sufficient statistic and
  detected weak noise after 14 samples with 97.8% error-exposure reduction and
  zero false alarms in the frozen independent clean-sequence test.

Key lesson:

~~~text
More Recursion != Better Observability
Wrong Sufficient Statistic Can Be The Fault
~~~

### SIM-019 through SIM-021 — fail-closed restoration and factorization

- shifted-regime retraining did not restore exact 16-state recovery even with
  substantial new evidence;
- explicit missingness semantics improved correctness of representation but did
  not solve the full-state limit;
- factorizing the state recovered L0 above the 0.90 contract while keeping
  failed dimensions closed.

Key lesson:

~~~text
Full-State Recovery != Useful Partial-State Recovery
~~~

### SIM-022 through SIM-028 — causal observability and probe pressure

Paired causal probes changed the problem from passive classification to active
system identification.

SIM-022:

~~~text
exact 16-state reconstruction = 0.929
macro per-fault accuracy      = 0.982
~~~

SIM-023, after fixing the comparator to a true 20-probe fixed-five policy:

~~~text
fixed-five exact accuracy = 0.969 at 20 probes
sequential exact accuracy = 0.963 at 5.399 mean probes
probe reduction           = 73.0%
accuracy gap              = 0.0062
~~~

SIM-024/025 established a causal-observability noise/resource knee. Repetition
moved the knee but did not remove it.

SIM-026 localized the noise=0.020 residual failure almost entirely to L2
handoff.

SIM-027 redesigned L2 as a known-command/receipt controlled-input challenge:

~~~text
L2 accuracy = 1.000 at noise 0.020 / 0.040 / 0.080
exact state = 0.984 at 0.020
exact state = 0.930 at 0.040
~~~

SIM-028 then redesigned L1 as a controlled calibration step-response:

~~~text
exact state = 0.996 at noise 0.040
exact state = 0.990 at noise 0.080
exact state = 0.956 at noise 0.120
L1 accuracy ~ 1.000 across the tested range
~~~

The remaining failure moved to another observation channel rather than being
solved by meta recursion.

Key lesson:

~~~text
Passive Observability Failure != Causal Observability Failure
Probe Design Can Move The Information Knee
More Evidence != Better Policy
~~~

### SIM-029 — probe admission

Cross-repository methods were imported from Finite RAM Lab, Finite Tool Surface
Lab, Harness Component Economics, Jev/Cua Lab, MVCA, and Memory Attention Lab.

A naive accuracy-only rule would have admitted four frozen invalid/unqualified
probe candidates.

The explicit contract produced:

~~~text
accuracy-only invalid admissions = 4
contract false admissions        = 0
~~~

Including rejection of a perfect latent-truth oracle.

Key lesson:

~~~text
Diagnostic Accuracy != Probe Admission
Probe Qualification != Execution Authority
Synthetic Admission != Human / Clinical Authorization
~~~

See:

~~~text
docs/CROSS-RESEARCH-TRANSFER-2026-10-04.md
docs/CGD-SIM-029.md
~~~

### SIM-030 — durable probe transaction

The probe lifecycle was converted from one-shot measurement into a fail-closed
transaction.

Frozen fault injection produced:

~~~text
accepted-result correctness                  = 1.000
duplicate interventions under contract       = 0
naive-retry duplicate-intervention scenarios = 1
~~~

A lost response after dispatch remained UNKNOWN with one dispatch despite
multiple physical attempts. A lost response after commit returned the stored
accepted result.

Key lesson:

~~~text
Probe Attempt != Probe Operation
Re-observation != Re-intervention
UNKNOWN != Retry Permission
INVALIDATED != Diagnostic Negative
~~~

### SIM-031 / SIM-032 — rare-state harvesting transfer

Finite RAM Lab rare-state methodology was transferred to the synthetic
silent-overconfidence lane.

SIM-031 held-out result:

~~~text
pooled rare-state incidence          = 0.234%
enriched-stratum incidence           = 2.250%
enrichment ratio                     = 9.60x
95% >=1 specimen pooled              = 1277 episodes
95% >=1 specimen enriched            = 132 episodes
~~~

SIM-032 replaced latent-label targeting with admitted causal-probe targeting.

~~~text
biopsy-all:
    6400 biopsies, 12/12 rare states

causal targeting:
    382 biopsies
    7/12 rare states
    58.3% recall
    1.832% biopsy precision
    94.0% biopsy-load reduction

same-budget random:
    382 biopsies
    0/12 rare states in the frozen run
~~~

Oracle-label targeting remained an explicitly non-admissible upper-bound lane.

Key lesson:

~~~text
Rare-State Enrichment != Permission To Treat
Synthetic Stratum != Human Phenotype
Causal Sampling Can Replace Oracle Sampling In The Synthetic Lane
~~~

## Revised stopping boundary

The post-convergence work adds a second boundary to the SIM-013 fixed point.

The loop may continue internally only when it changes a justified research
dimension such as:

- observation sufficient statistic;
- evidence-acquisition policy;
- bounded probe interface;
- failure-state sampling strategy;
- provenance/admission/recovery contract.

It should stop when improvement requires making the synthetic probe increasingly
oracle-like or embedding the answer into the challenge.

At that point:

~~~text
STOP SYNTHETIC PROBE ESCALATION
    ->
QUALIFY A REAL OBSERVATION CONTRACT
    ->
BIND EXTERNAL EVIDENCE
    ->
DOMAIN-LOCAL VALIDATION
~~~

No current result authorizes human experimentation, diagnosis, treatment, or
clinical decision-making.
