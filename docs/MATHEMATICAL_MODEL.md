# Mathematical Model v0.1

> Status: WORKING FORMALISM  
> Biological interpretation: UNVALIDATED  
> Clinical authority: NONE

## State decomposition

Let a system contain n subsystems:

~~~text
s_t = [s_1(t), ..., s_n(t)]
~~~

The first synthetic validation uses four functional dimensions:

~~~text
motor
procedural
executive
memory
~~~

These names are not claims that four biological modules explain human behavior.

## Capability and accessibility

For each subsystem let latent capability be c_i and accessibility be
g_i(s_t, u_t), both bounded to [0,1].

~~~text
e_i(t) = c_i * g_i(s_t, u_t)
~~~

This explicitly represents:

~~~text
represented capability != expressed capability
~~~

The multiplicative gate is a bootstrap model assumption, not a universal law.

## Observation

~~~text
y_t = h(e_t) + epsilon_t
~~~

VAL-001 uses deterministic h and zero noise. Later work may use p(y_t | s_t).

## State transition

~~~text
p(s_{t+1} | s_t, u_t)
~~~

Candidate families include finite-state machines, HMMs, switching state-space
models, and coupled dynamical systems.

## Dissociation index

For n bounded subsystem activations define:

~~~text
D(s) =
    sum_{i<j} |s_i - s_j|
    --------------------------------
    floor(n^2 / 4)
~~~

The denominator is the maximum pairwise-disagreement sum for n values in [0,1].

Thus:

~~~text
0 <= D(s) <= 1
D([1,1,1,1]) = 0
D([1,1,0,0]) = 1
~~~

This is a descriptive statistic, not a consciousness measure.

## Observation degeneracy

For coarse observation function h and observation y:

~~~text
E(y) = {s : h(s) = y}
N(y) = |E(y)|
~~~

If N(y) > 1, the coarse observation cannot uniquely identify latent state.

Future probabilistic work may replace the count with H(S | Y) or posterior
credible sets.

## Claim boundary

A successful fit would establish only compatibility between a declared model
and declared observables. It would not establish that inferred latent states
are literal biological modules, that a drug acts through the fitted transition
matrix, or that a computational analogy shares causal mechanism with a brain.


## Anticipatory internal-control extension

HYP-005 introduces internal and pre-contact control variables in addition to
the physical intervention term.

~~~text
a_t = body-part / spatial attention
e_t = tactile expectation
p_t = declared pre-contact cues
u_t = physical peripheral input
~~~

A discrete-time working form is:

~~~text
x_{t+1} =
    F(x_t)
  + B_a a_t
  + B_e e_t
  + B_p p_t
  + G(a_t, e_t, p_t) B_u u_t
  + eta_t
~~~

This separates two hypotheses:

~~~text
additive preparation:
    B_a or B_e != 0

gain / routing modulation:
    G(a,e,p) != constant
~~~

The model therefore allows a physical-input-free state change:

~~~text
u_t = 0
x_{t+1} != F(x_t)
~~~

without claiming that a peripheral tactile afferent fired.

### Pre-contact residual

For near-body observations:

~~~text
R_observed = R_known + R_residual
~~~

where R_known must explicitly include declared visual, thermal, airflow,
timing, attention, expectation, and multisensory-prediction terms before an
unmodeled residual is interpreted.

### Mechanical-dose / defensive-transition extension

For contact stimulation, candidate physical dose is vector-valued:

~~~text
u = (force, area, force_rate, duration, velocity, frequency, site)
~~~

A minimal net-response model is:

~~~text
U(u) = R_regulatory(u) - lambda * R_defensive(u)
~~~

A knee or regime switch is a model-selection question, not an assumption.
Candidate analyses include segmented regression, switching state-space models,
and transition-probability changes.

See [HYP-005.md](HYP-005.md).


## Dynamic somatic-valuation extension

HYP-006 separates local sensory dimensions that should not be collapsed into
one sensitivity scalar.

~~~text
z_i(t) = [
    D_i(t),  # detection
    I_i(t),  # intensity
    P_i(t),  # pleasantness
    E_i(t),  # erotic salience
    N_i(t)   # nociceptive / aversive value
]
~~~

Physical input is vector-valued:

~~~text
u_i(t) = (
    force,
    area,
    force_rate,
    velocity,
    frequency,
    duration,
    temperature,
    site
)
~~~

A phenomenological peripheral term is:

~~~text
r_i(t) =
    sigmoid(
        (phi_i(u_i(t)) - theta_i)
        / kappa_i
    )
~~~

Control state is explicitly separate:

~~~text
c_t = [
    attention,
    expectation,
    arousal,
    relationship_trust,
    consent_agency,
    mood,
    perceived_threat,
    perceived_observation,
    self_observation
]
~~~

History state:

~~~text
h_t = [
    habituation,
    learned_couplings,
    self_model,
    partner_model,
    recent_interaction_history
]
~~~

A local gain model is:

~~~text
g_i(t) =
    sigmoid(
        beta_i^T c_t
        + gamma_i^T h_t
    )
~~~

with:

~~~text
s_i(t) = g_i(t) * r_i(t)
~~~

and valuation:

~~~text
z_i(t) = V_i(s_i(t), c_t, h_t)
~~~

### Switching regimes

A higher-level latent regime can be represented as:

~~~text
q_t in {
    subthreshold,
    neutral,
    pleasant,
    erotic,
    defensive,
    habituated
}
~~~

with:

~~~text
P(q_{t+1} | q_t, u_t, c_t, h_t)
P(y_t | z_t, q_t)
~~~

This makes "same input, different state transition" an explicit model property.

### Associative update

A minimal eligibility-trace form is:

~~~text
Delta W =
    eta_positive * eligibility * positive_prediction_error
  - eta_negative * eligibility * aversive_prediction_error
  - lambda * habituation
~~~

This is a model family for testing somatic valuation learning, not evidence that
a new erogenous region has been created.

### Observation re-entry

For self-observation:

~~~text
y_t = H(x_t)
o_t = O(y_{t-tau}, perspective)
x_{t+1} = F(x_t, u_t, o_t)
~~~

This permits observation itself to become an intervention when it re-enters the
observed system.

### Dyadic memory

For persons A and B:

~~~text
M_B(t+1) = Update(M_B(t), report_A(t))
u_B(t+1) = Policy_B(M_B(t+1), context_t+1)
x_A(t+2) = F(x_A(t+1), u_B(t+1), c_A(t+1))
~~~

This represents a partner as an observer, external memory, and future input
generator without treating human relationships as software components.

See [HYP-006.md](HYP-006.md).
