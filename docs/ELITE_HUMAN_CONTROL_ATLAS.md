# Elite Human Control Atlas

> Status: OPEN CROSS-DOMAIN RESEARCH PROGRAM  
> Goal: identify reusable control transitions, not celebrate biographies

## Question

Across sport, dance, music, and skilled manual work, elite performers appear to
change different parts of the human control system.

Can these changes be represented in one common state-space language, and can
any of the underlying training principles transfer to ordinary adults without
copying elite loads or risks?

## Working thesis

~~~text
Expertise != one scalar capability increase
~~~

A more useful decomposition is:

~~~text
expertise =
    reshaped controllability
  + reshaped observability
  + reshaped prediction
  + reshaped sensory weighting
  + reshaped variability
  + reshaped policy complexity
  + learned task-specific state space
~~~

Visible performance is a projection of this latent controller.

## Specimen families

The atlas deliberately mixes named elite examples with peer-reviewed skill
domains. Named individuals are hypothesis generators unless the specific
mechanism was directly measured.

### Murofushi lineage — latent-control discovery

Candidate transition sequence:

~~~text
DISCOVER
 -> ACCESS
 -> INDIVIDUATE
 -> AUGMENT-OBS
 -> REINTEGRATE
~~~

Research value:

- unusual probes may reveal previously unused control dimensions;
- self-observation can be augmented with artificial sensory channels;
- newly accessible movement is not automatically task-useful;
- task transfer must be tested separately.

### Ichiro lineage — control-surface pruning

Candidate sequence:

~~~text
DISCOVER
 -> PRUNE
 -> CALIBRATE
 -> AUTOMATIZE
~~~

Research value:

- better performance may require fewer explicit corrections;
- measured proxies should not be treated as the entire athlete state;
- stable high-level state can be more useful than low-level actuator
  micromanagement.

This is a formal interpretation of public coaching / interview material, not a
direct biomechanical measurement of the individual.

### Nakamura lineage — output calibration

Candidate sequence:

~~~text
ANCHOR
 -> CALIBRATE
 -> AUTOMATIZE
 -> ROBUSTIFY
~~~

Research value:

- stable reference frames can reduce mapping uncertainty;
- repeated task-specific practice can refine an inverse map from desired ball
  flight to body / contact configuration;
- stable primitive plus context adaptation may be more useful than perpetual
  form changes.

### Ono lineage — control-surface expansion

Candidate sequence:

~~~text
INDIVIDUATE
 -> SYMMETRIZE
 -> EXPAND
 -> ROBUSTIFY
~~~

Research value:

- temporarily constraining the dominant side can force learning in the weaker
  control branch;
- bilateral action options enlarge the reachable solution set;
- wider solution space may improve recovery from unusual body / ball states.

### Ballet — controlled state-space extension

Candidate sequence:

~~~text
ACCESS
 -> EDGE-EXTEND
 -> REINTEGRATE
 -> AUTOMATIZE
~~~

Critical failure branch:

~~~text
EDGE-EXTEND
 -> COMPENSATED-EXPANSION
~~~

Research value:

- displayed range is not the same as controlled anatomical range;
- training can alter control near end-range;
- compensation must be measured separately from true control expansion.

### Piano / instrumental dexterity — individuation

Primary evidence shows that even musically naive adults can reduce
cross-finger movement covariation after short piano practice.

Candidate transition:

~~~text
COUPLED
 -> INDIVIDUATED
~~~

This is one of the strongest current examples that a control property can move
in ordinary adults over days rather than years.

### Archery — anticipation

Elite / trained archers exhibit postural adjustments before predictable release
perturbations.

Candidate transition:

~~~text
REACTIVE
 -> ANTICIPATORY
~~~

The important variable is not only accuracy but the timing of control relative
to the perturbation.

### Gymnastics — sensory reweighting

Expert gymnasts can use reintroduced proprioceptive information more efficiently
than comparison athletes in perturbation paradigms.

Candidate transition:

~~~text
FIXED / SLOW REWEIGHT
 -> FASTER CONTEXTUAL REWEIGHT
~~~

This turns "balance" into a state-estimation problem rather than one scalar
ability.

### Climbing — affordance and functional variability

Climbing studies show:

- action capability and perceived reach can be separately measured;
- experts can use multiple functionally equivalent movement solutions;
- useful movement variability can coexist with lower exploratory waste.

Candidate transitions:

~~~text
AFFORDANCE-CALIBRATE
VARIABILITY-RESHAPE
ROBUSTIFY
~~~

This warns against treating low total movement variance as a universal
signature of expertise.

### Surgery / skilled manual action — pruning and smoothness

Skill can be reflected in smoother tool trajectories, fewer unnecessary
submovements, shorter path length, or lower jerk.

Candidate sequence:

~~~text
EXPLORATORY MICRO-CORRECTION
 -> PRUNE
 -> SMOOTH / ECONOMIZE
~~~

This domain is useful because the output can often be instrumented precisely.

## Unified controller model

Fast timescale:

~~~text
x_{t+1} = f(x_t, u_t, d_t ; Theta_n)
y_t     = h(x_t)
xhat_t  = E_Theta(y_0:t)
u_t     = pi_Theta(xhat_t, goal_t, context_t)
~~~

Slow timescale:

~~~text
Theta_{n+1}
=
T(
    Theta_n,
    task_constraints_n,
    perturbations_n,
    feedback_n,
    error_n,
    reward_n
)
~~~

The research target is T: the controller-update operator.

## Control-space representation

Define:

~~~text
Theta = {
    C_phys,      # physical capability ceiling
    B_ctrl,      # accessible motor basis
    O_obs,       # observability
    W_sens,      # sensory weights
    M_pred,      # predictive / forward model
    Pi,          # policy family
    X_ctrl,      # controllable state set
    V_struct,    # variability structure
    H_history    # retained learning / memory
}
~~~

Then different training traditions can be expressed as different deformations:

~~~text
DISCOVER      -> uncertainty(Theta) down
ACCESS        -> rank(B_ctrl) up or reachable directions up
INDIVIDUATE   -> control coupling down
CALIBRATE     -> output bias / variance down
REWEIGHT      -> W_sens becomes context-dependent
EDGE-EXTEND   -> measure(X_ctrl) up
PRUNE         -> effective dimension(Pi) down at preserved performance
AUGMENT-OBS   -> O_obs up
ROBUSTIFY     -> task sensitivity to representative disturbance down
TRANSFER      -> held-out gap down
~~~

## Variability decomposition

For output z = g(x), linearize around the task state:

~~~text
J = dg/dx
~~~

Split movement perturbation:

~~~text
delta_x = delta_x_null + delta_x_task
~~~

with:

~~~text
J delta_x_null = 0
J delta_x_task != 0
~~~

A central atlas hypothesis is:

~~~text
expertise may reduce task-harmful variability
without minimizing all internal variability
~~~

This reconciles domains where experts look highly repeatable with domains such
as climbing where experts retain multiple functionally equivalent solutions.

## General-adult transfer program

The atlas does not assume elite exercise protocols generalize.

A safe validation sequence for ordinary adults can use simple nonclinical tasks:

~~~text
BASELINE
 -> OBSERVE
 -> ACCESS / CALIBRATE
 -> SMALL PERTURBATION
 -> ROBUSTIFY
 -> FEEDBACK OFF
 -> HELD-OUT TRANSFER
 -> RETENTION
~~~

Candidate low-risk tasks include:

- simple bilateral finger sequences;
- non-dominant-hand placement or tracing;
- externally supported balance tasks;
- rhythm / timing tasks;
- safe object-placement or target tasks.

The research outcome is the transition signature, not the difficulty of the
exercise.

## Key falsification questions

The atlas weakens if:

1. proposed transitions cannot be distinguished from generic practice effects;
2. the same observable improvement can be explained entirely by compensation;
3. improvements vanish under representative perturbation;
4. augmented-observation gains do not survive feedback removal;
5. transition metrics do not predict held-out task performance;
6. the ontology fails to reduce explanatory ambiguity compared with generic
   "expert vs novice" labels.

## Current evidence boundary

The strongest cross-domain evidence currently supports:

- short-term finger individuation changes in naive adults;
- anticipatory postural control in archery;
- task-specific sensory reweighting in gymnastics;
- functional movement variability and affordance use in climbing;
- compensated-turnout as a distinct biomechanical concern in ballet;
- smoothness / jerk as measurable dimensions of surgical skill.

Named elite individuals remain case-study / hypothesis-generator entries unless
directly instrumented.

## Related documents

- [HUMAN_CONTROL_TRANSITION_ONTOLOGY.md](HUMAN_CONTROL_TRANSITION_ONTOLOGY.md)
- [MATHEMATICAL_MODEL.md](MATHEMATICAL_MODEL.md)
- [FORMAL_CORRESPONDENCE_AI.md](FORMAL_CORRESPONDENCE_AI.md)

## Deeper atlas rule: specimen != mechanism

The atlas now separates three levels:

~~~text
Level 1  public / measured performance phenotype
Level 2  candidate transition label
Level 3  candidate controller update class
~~~

Example:

~~~text
precise repeated output
 -> CALIBRATE
 -> U-MODEL and/or U-POLICY candidate
~~~

The first line can be directly observed.

The second and third require controlled evidence.

This prevents a famous training anecdote from being promoted into a mechanism.

## Cross-domain comparison vector

Every future atlas specimen should attempt to fill:

~~~text
[
    task_gain,
    transfer,
    retention,
    perturbation_robustness,
    observability,
    controllability,
    feedback_dependency,
    task_harmful_variance,
    control_cost,
    compensation_or_risk
]
~~~

Missing fields remain UNKNOWN rather than being inferred from reputation.

## General-person extraction rule

The atlas should extract a safe principle only when the elite example can be
rewritten as a low-risk control operation.

Examples:

~~~text
elite form:
    extreme task-specific practice

general research abstraction:
    measure one output,
    change one bounded constraint,
    test retention,
    remove feedback,
    test a held-out condition
~~~

The general-person object is therefore the transition method, not the elite
load, range, speed, or volume.

## New cross-domain question

A major open question is whether expert practice differs primarily in the
chosen exercise or in **probe selection**:

~~~text
Which next practice condition is most informative about the current
controller?
~~~

Candidate formalization:

~~~text
probe_star =
    argmax [
        information_gain
      + expected_task_gain
      + expected_transfer
      - risk
      - cost
    ]
~~~

This reframes unusual elite training as possible active system identification,
while leaving causal claims open until measured.
