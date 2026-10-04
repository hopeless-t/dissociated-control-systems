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
