# HF01 Control Susceptibility

> Status: WORKING FORMALISM
> Biological validation: OPEN

## State is not enough

Static observability asks:

~~~text
what latent state x generated the current observations?
~~~

Recoverability asks a different question:

~~~text
how does this state respond to a declared input u?
~~~

Define an intervention-linked response operator for probe z:

~~~text
chi_z(x, u, Delta)
  = [z(x_u(Delta)) - z(x_0(Delta))] / ||u||
~~~

where x_u is the trajectory under the declared input and x_0 is the no-input counterfactual.

For late visible output:

~~~text
G_H(x, u, T)
  = [H(x_u(T)) - H(x_0(T))] / ||u||
~~~

Recoverability is a property of state plus dynamics plus available actuator class; it is not a single concentration.

## HF-SIM-002 known-answer example

Two synthetic states begin with identical visible output:

~~~text
H0 = 0.50

recoverable state: F0 = 0.20
locked state:      F0 = 0.60
~~~

Apply the identical upstream control:

~~~text
behavioral = 1
antiandrogen = 1
~~~

At the early checkpoint (80 steps):

~~~text
recoverable:
    intervention-linked Delta R = +0.268981
    intervention-linked Delta H = +0.033543
    controlled R               = 0.629115

locked:
    intervention-linked Delta R = +0.141960
    intervention-linked Delta H = +0.004952
    controlled R               = 0.171071
~~~

At the late checkpoint (2000 steps):

~~~text
recoverable Delta H = +0.517550
locked Delta H      ≈ +0.000000077
~~~

## Important negative result

The locked state still shows a positive early regenerative response:

~~~text
Delta R_early > 0
~~~

while producing essentially no late output recovery.

Therefore even inside the synthetic model:

~~~text
Early Molecular Response != Recoverability
~~~

An early response can be informative, but it must be interpreted jointly with state context such as structural condition.

## Revised observer target

Instead of searching for one magic biomarker, HF01 should estimate a tuple such as:

~~~text
zeta(t) = [
  state estimate,
  intervention susceptibility,
  structural context,
  uncertainty
]
~~~

The eventual target remains:

~~~text
rho(t, U)
  = probability or declared-model indicator that the healthy-output region
    is reachable from the current state using actuator class U
~~~

This is the quantity that a normal-model feedback system would ultimately need to estimate.

## Biological boundary

The equations above are a control formalism.
They do not establish that IGF-1, WNT, ECM, HRV, cortisol, or any other individual probe uniquely represents recoverability.
