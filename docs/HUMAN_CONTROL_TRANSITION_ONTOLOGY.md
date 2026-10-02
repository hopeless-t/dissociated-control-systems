# Human Control Transition Ontology

> Status: OPEN RESEARCH ONTOLOGY  
> Domain: motor control / skill learning / human performance  
> Clinical authority: NONE  
> Training prescription authority: NONE

## Purpose

This document names recurring state transitions observed across elite sport,
dance, music, and skilled manual performance.

The goal is not to turn famous performers into anecdotes. The goal is to ask:

> Which latent control property changed, how would we measure that change, and
> what observation would falsify the proposed transition?

The ontology is deliberately substrate-local. A similar mathematical shape in
AI or engineered systems does not establish a shared physical mechanism.

## Two-timescale model

Within one movement:

~~~text
x_{t+1} = f(x_t, u_t, d_t ; Theta_n) + omega_t
y_t     = h(x_t) + v_t
xhat_t  = Estimator_Theta(y_0:t, u_0:t-1)
u_t     = Policy_Theta(xhat_t, goal_t, context_t)
~~~

Training changes the controller itself on the slower episode index n:

~~~text
Theta_{n+1} =
    Learn(
        Theta_n,
        practice_n,
        error_n,
        reward_n,
        feedback_n
    )
~~~

A useful controller state is:

~~~text
Theta = {
    capability_ceiling,
    accessible_control_basis,
    sensory_weights,
    internal_model,
    policy,
    reachable_state_set,
    output_variance_structure,
    observability,
    memory
}
~~~

The visible movement is only a projection of this slower controller state.

## Core transitions

### DISCOVER

~~~text
unmapped control variable
->
recognized / testable control variable
~~~

Candidate signature:

~~~text
posterior uncertainty H(Theta | data) decreases
~~~

This is system identification, not proof of new physical capability.

### ACCESS

~~~text
latent capability
->
voluntarily recruitable capability
~~~

Candidate signature:

~~~text
reachable control directions increase
while physical anatomy is unchanged
~~~

### INDIVIDUATE

~~~text
coupled control
->
more selective component control
~~~

For activation mapping:

~~~text
a = C v
~~~

where off-diagonal terms of C represent coupling.

Candidate signature:

~~~text
norm(C_offdiag) decreases
~~~

without requiring complete anatomical independence.

### REINTEGRATE

~~~text
separated primitives
->
task-specific synergy
~~~

Success requires:

~~~text
task error decreases
while useful component freedom remains
~~~

This prevents the false target of maximizing isolated control for its own sake.

### SYMMETRIZE

~~~text
strong side asymmetry
->
broader bilateral usability
~~~

Candidate metric:

~~~text
abs(J_left - J_right) decreases
~~~

This does not require perfect anatomical symmetry.

### CALIBRATE

~~~text
large mapping error
->
stable input-output mapping
~~~

Candidate metrics:

~~~text
bias decreases
trial-to-trial output variance decreases
target error decreases
~~~

### ANCHOR

~~~text
ambiguous reference frame
->
repeatable task coordinate system
~~~

Candidate signature:

~~~text
reference uncertainty decreases
~~~

Examples include stable contact-point markers or repeatable setup landmarks.

### ANTICIPATE

~~~text
post-error correction
->
pre-event compensation
~~~

Candidate temporal metric:

~~~text
Delta_t =
    control_onset
  - perturbation_onset
~~~

Reactive state:

~~~text
Delta_t > 0
~~~

Anticipatory state:

~~~text
Delta_t < 0
~~~

### REWEIGHT

~~~text
fixed sensory dependence
->
context / reliability-dependent sensory weighting
~~~

State estimator:

~~~text
xhat =
    w_visual * y_visual
  + w_proprio * y_proprio
  + w_vestib * y_vestib
~~~

Transition signature:

~~~text
w_i(t) becomes reliability- and task-dependent
~~~

### AFFORDANCE-CALIBRATE

~~~text
misestimated action capability
->
better agreement between estimated and actual action boundary
~~~

Metric:

~~~text
e_aff =
    abs(
        capability_estimate
      - capability_actual
    )
~~~

The ontology does not assume all experts are better calibrated; this is an
empirical question.

### ROBUSTIFY

~~~text
skill works in narrow condition
->
skill tolerates representative perturbations
~~~

Candidate local signature:

~~~text
sensitivity = d(output_error) / d(disturbance)
~~~

and robustness means lower task-relevant sensitivity over the declared
perturbation range.

### PRUNE

~~~text
many corrective actions / high supervisory load
->
smaller task-relevant control set
~~~

Candidate metrics:

~~~text
action_count down
path_length down
jerk down
cognitive / dual-task cost down
performance preserved or improved
~~~

This is not inactivity. It is lower control complexity at equal or better task
performance.

### AUTOMATIZE

~~~text
high explicit supervisory demand
->
stable performance under reduced conscious supervision
~~~

Candidate signature:

~~~text
dual-task performance cost decreases
~~~

### AUGMENT-OBS

~~~text
poorly observable task state
->
new external observation channel
~~~

Examples include sonification, motion capture, video, force plates, and
instrument telemetry.

For a linearized model:

~~~text
y = C x
~~~

adding a sensor C_a gives:

~~~text
y_aug = [C ; C_a] x
~~~

and may improve observability.

### INTERNALIZE-FB

~~~text
external feedback required
->
performance retained when feedback is removed
~~~

Candidate metric:

~~~text
feedback_off_gap =
    performance_with_feedback
  - performance_without_feedback
~~~

A successful transition reduces this gap after learning.

### PHASE-LOCK

~~~text
force-dominant control
->
timing aligned with target dynamics
~~~

Candidate metrics:

~~~text
phase variance down
energy-transfer efficiency up
~~~

This is appropriate for oscillatory / cyclic tasks and must not be generalized
to all skills.

### WAIT-FOR-INFORMATION

~~~text
minimum reaction latency objective
->
decision timing that trades information against delay
~~~

Candidate optimization:

~~~text
tau_star =
    argmax_tau [
        expected_information_gain(tau)
      - delay_cost(tau)
    ]
~~~

Expertise may therefore include waiting when early evidence is weak.

### VARIABILITY-RESHAPE

~~~text
undifferentiated movement variability
->
task-structured variability
~~~

For task output z = g(x), linearize:

~~~text
J = dg/dx
~~~

Decompose perturbation:

~~~text
delta_x =
    delta_x_null
  + delta_x_task
~~~

where:

~~~text
J delta_x_null = 0
J delta_x_task != 0
~~~

Candidate expert signature:

~~~text
Var(delta_x_task) decreases
while useful Var(delta_x_null) is retained
~~~

Thus:

~~~text
less total variance != universal definition of expertise
~~~

### EDGE-EXTEND

~~~text
control only in central safe state region
->
control maintained closer to anatomical / task boundary
~~~

Define:

~~~text
X_controllable(n)
~~~

as the state set in which task criteria are satisfied.

Candidate success:

~~~text
measure(X_controllable) increases
without hidden compensatory cost
~~~

### TRANSFER

~~~text
trained condition success
->
success in declared neighboring untrained conditions
~~~

Candidate metric:

~~~text
transfer_gap =
    training_condition_performance
  - heldout_condition_performance
~~~

## Failure transitions

### COMPENSATED-EXPANSION

~~~text
displayed range / output increases
but target subsystem did not gain equivalent control
~~~

The visible target is achieved by shifting load or motion into another
subsystem.

This is a central DCS failure mode:

~~~text
same observable output
!=
same latent solution
~~~

### OVERFIT

~~~text
training-condition improvement
without held-out transfer
~~~

### FEEDBACK-DEPENDENT

~~~text
performance improves with augmentation
but collapses when the feedback channel is removed
~~~

### RISK-DOMINANT

~~~text
performance gain is smaller than added injury / failure exposure
~~~

No athletic gain alone qualifies a transition as desirable.

## Qualification ladder

For one declared ability k:

~~~text
U0  UNMAPPED
O1  OBSERVABLE
A2  ACCESSIBLE
I3  INDIVIDUATED
C4  CALIBRATED
R5  ROBUST
T6  TRANSFERABLE
M7  AUTOMATIZED
~~~

This is not a universal developmental sequence. Individual transitions may be
skipped, reversed, or branch into failure states.

## Candidate practice-selection objective

A training probe p can be treated as an experiment:

~~~text
p_star =
    argmax_p [
        alpha * I(Theta ; Y | p)
      + beta  * DeltaTaskPerformance
      + gamma * DeltaTransfer
      + delta * DeltaObservability
      - lambda * Risk
      - mu     * Cost
      - nu     * CognitiveLoad
    ]
~~~

Different expert practices may emphasize different weights rather than use
different mathematics.

## Evidence discipline

A proposed transition requires:

1. a declared before-state;
2. a declared after-state;
3. a measurable observable signature;
4. a plausible alternative explanation;
5. a held-out / perturbation test where relevant;
6. a falsification condition.

Biography is not evidence of mechanism.

Elite performance is not proof that a particular training element caused that
performance.

## General-person boundary

The ontology is intended to extract methods, not copy elite training loads.

The generalizable research question is:

> Which control properties of a healthy ordinary adult can be changed safely,
> how quickly, and how specifically?

Transfer must always be measured separately from training-task improvement.

See [ELITE_HUMAN_CONTROL_ATLAS.md](ELITE_HUMAN_CONTROL_ATLAS.md).

## Transition grammar and update classes

The transition label and the physical / computational update class are separate
objects.

For example:

~~~text
CALIBRATE
~~~

may be achieved by:

~~~text
U-MODEL
U-POLICY
U-WEIGHT
or a mixture
~~~

while:

~~~text
EDGE-EXTEND
~~~

may reflect:

~~~text
U-PHYS
U-BASIS
U-REACH
~~~

or may be a false positive caused by COMPENSATED-EXPANSION.

Therefore each coded transition should carry:

~~~text
transition_label
candidate_update_class
perturbation_fingerprint
retention_result
transfer_result
compensation_check
~~~

### Candidate composition constraints

Useful research paths include:

~~~text
INDIVIDUATE -> REINTEGRATE
AUGMENT-OBS -> INTERNALIZE-FB
CALIBRATE -> ROBUSTIFY
ROBUSTIFY -> TRANSFER
EDGE-EXTEND -> REINTEGRATE
~~~

Failure paths include:

~~~text
AUGMENT-OBS -> FEEDBACK-DEPENDENT
EDGE-EXTEND -> COMPENSATED-EXPANSION
CALIBRATE -> OVERFIT
ROBUSTIFY -> RISK-DOMINANT
~~~

### Non-commutativity question

For transition operators T_A and T_B:

~~~text
T_A(T_B(Theta))
!=
T_B(T_A(Theta))
~~~

is permitted.

The ontology therefore records order, not merely membership.

### Qualification requires perturbation

A high task score is insufficient to qualify a transition.

A candidate transition should survive at least one discriminating probe
appropriate to the claim, such as:

~~~text
feedback removal
sensory perturbation
context shift
mechanical perturbation
dual-task load
held-out transfer
component constraint
~~~

The probe must be specified before observing the result whenever feasible.

## Temporal qualification layer

"Improved" is split into distinct temporal states.

### CORRECT — fast event, not yet learning

~~~text
error occurs
-> online feedback reduces current-trial error
~~~

CORRECT is an execution event rather than evidence that the slow controller
changed.

### ADAPT

~~~text
repeated perturbation
-> next-trial behavior changes systematically
~~~

Candidate signature:

~~~text
behavior_{n+1}
depends on
error_n / perturbation_n
~~~

### CONSOLIDATE

~~~text
session-acquired change
-> retained representation after time without equivalent practice
~~~

Candidate signature requires a delayed test.

### RETAIN

~~~text
learned performance survives declared delay / washout condition
~~~

RETENTION is an observation state and should report the delay and context.

### TRANSFER

~~~text
retained / learned controller property
-> held-out neighboring condition
~~~

The temporal claim ladder is therefore:

~~~text
CORRECT
!=
ADAPT
!=
CONSOLIDATE / RETAIN
!=
TRANSFER
~~~

A study may support one level without supporting the next.

## Dependency-aware coordination transitions

The human-control lane now includes transitions for hidden coupling and
whole-body load distribution.

### LINKAGE-DISCOVER

~~~text
unobserved coordination dependency
->
recognized coordination dependency
~~~

Candidate signature:

~~~text
the learner can predict which proximal / supporting states change with a
declared distal action better than at baseline
~~~

This is an observability transition, not proof of a newly created anatomical
connection.

### SYNERGY-AWARE

~~~text
single-effector mental model
->
distributed coordination model
~~~

The learner represents a task as requiring a linked set of body components
rather than one visible actuator.

### ATTENTIONAL-REPARAMETERIZE

~~~text
many local control instructions
->
smaller task-level / relational control coordinates
~~~

Candidate representation:

~~~text
q in R^n
z in R^k
k << n

q = Phi(z, context, fatigue, task)
~~~

The subjective coordinate is not assumed to be anatomically literal.

### LOAD-ROUTE

~~~text
local load concentration
->
work redistributed across an available coordination graph
~~~

Candidate outcomes include:

~~~text
local peak effort down
task output preserved
time to local fatigue up
off-target compensation bounded
~~~

### BACKPRESSURE-INTEGRATE

~~~text
local fatigue / loss-of-control signal ignored
->
upstream / whole-body policy changes before local failure
~~~

This is the human-control form of the broader HYP-008 backpressure concept.

### Failure states

#### LOCAL-ACTUATOR LOCK

The learner represents a multi-component task as if one visible effector were
the whole controller.

#### LOAD-HOTSPOT

A local subsystem carries disproportionate effort while alternate coordination
routes remain unused or unobserved.

#### CASCADE-COMPENSATION

A degraded subsystem causes sequential compensatory changes in other
subsystems, preserving coarse output while hidden cost rises.

These labels are research abstractions and require domain-local measurement.
