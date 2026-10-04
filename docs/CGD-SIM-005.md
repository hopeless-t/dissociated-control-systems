# CGD-SIM-005 — Harness fault localization and repair

> Status: SYNTHETIC WORKING MODEL  
> Biological interpretation: UNVALIDATED  
> Clinical authority: NONE

## Harness hypothesis

The cognitive-control problem is reframed as a fault-tolerant harness:

~~~text
inject / encounter fault
        |
        v
observe residuals
        |
        v
infer fault location
        |
        v
choose bounded repair
        |
        v
re-run probes
        |
        +----> unresolved fault? ---- yes ----+
        |                                     |
        no                                    |
        v                                     |
     stable <---------------------------------+
~~~

The key object is not intelligence in the abstract. It is the mapping:

~~~text
observation -> fault hypothesis -> intervention -> post-intervention residual
~~~

## Passive single-fault diagnosis

For a symptom vector x and candidate fault f:

~~~text
P(f | x) proportional to P(x | f) P(f)
~~~

The harness uses a Gaussian naive-Bayes likelihood over frozen synthetic
features:

~~~text
performance_loss
performance_drop
self_reference_gap
handoff_gap
observer_disagreement
~~~

If posterior confidence is below 0.60, the harness abstains rather than forcing
a repair.

## Why a second harness was needed

A classifier trained on one-fault signatures need not remain valid when two
faults coexist. Mixtures can mask or imitate each other.

The self-improvement step therefore changes the harness rather than adding a
deeper recursive controller:

1. add component-specific probes;
2. learn thresholds from synthetic known-answer healthy/fault distributions;
3. repair only one high-priority component;
4. re-observe after the intervention;
5. diagnose the residual system again.

Active probe signatures:

~~~text
L0 decline        -> independent reference-state drop
L1 calibration    -> self/reference gap
L2 handoff        -> command/receipt gap
observer bias     -> primary/reference disagreement
~~~

This is a repair/re-observation loop, not a one-shot classifier.

## Repair semantics

~~~text
L0 -> slow_root
L1 -> recalibrate
L2 -> redundant_handoff
observer -> redundant_observer
~~~

Each repair has a small synthetic burden.

## Important objective warning

Surface functional performance is not a sufficient repair objective.

Aggressive compensation can make a degraded latent state look functional.
Conversely, a root-side repair can preserve latent capability while surface
function temporarily falls because less compensation is being invoked.

Therefore the experiment separately reports:

- surface function;
- latent capability (synthetic ground truth only);
- calibration residual;
- handoff residual;
- feedback error.

This extends the existing invariant:

~~~text
Functional Success != Preserved Latent Capability
~~~

to a harness rule:

~~~text
Repair Success != Improvement In One Proxy
~~~

## Claim ceiling

This is a synthetic harness experiment. It does not establish a clinical
diagnosis method, a treatment, a biological subsystem decomposition, or a
patient-facing monitoring protocol.
