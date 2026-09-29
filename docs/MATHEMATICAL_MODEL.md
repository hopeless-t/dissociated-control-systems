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
