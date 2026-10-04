# HF01 Public-Data Result 003 — GSE178510

> Dataset: GSE178510
> Material: primary human follicle dermal papilla cells, 2D culture
> Input: minoxidil, 48 h
> Status: PRE-REGISTERED PRIMARY PREDICTION EXECUTED
> Clinical authority: NONE

## Measurement correction before final interpretation

The GEO differential-expression file contains an ambiguous vendor fold-change column labeled CONTROL vs. MINOXIDIL.
HF01 does not use that column for the final result.

Instead the observer computes directly:

~~~text
effect(g) = MINOXIDIL Bi-weight Avg Signal(log2)
          - CONTROL Bi-weight Avg Signal(log2)
~~~

A deterministic CI test freezes this sign convention.

## Frozen primary prediction

Before the repository data run, HF01 froze:

~~~text
primary axis: WNT / regeneration loss
expected score after minoxidil: < 0
~~~

Rationale: if the cross-sectional disease axis were also a valid monotonic regenerative-response coordinate, a known hair-growth input should move it opposite the disease-associated direction.

## Result

~~~text
WNT / regeneration-loss mean signed effect = +0.159093
pre-registered expectation                  = < 0
PRIMARY TEST                               = FAIL

gene-direction contributions:
AXIN2      -0.266667
CTNNB1     +2.095000
DKK1       +0.230000
LEF1       -0.277778
SERPINF1   -0.746000
SFRP2      -0.080000

4/6 genes move opposite the disease direction,
but the frozen mean score remains positive.
~~~

The failed primary prediction is retained.

## Other frozen axes — exploratory only

~~~text
androgen/growth suppression   +0.021357
ECM/structural remodeling     -0.237000
hypoxia/oxidative             -0.137833
inflammation                  +0.415625
vascular-regression axis      -0.238000
~~~

No acceptance rule was pre-registered for these secondary axes.

## Why this does not imply that minoxidil fails to engage WNT biology

The associated publication reports stimulation of Wnt/beta-catenin and FGF pathways after minoxidil in cultured dermal papilla cells, including independent gene/protein measurements.

Therefore the failed HF01 prediction is specifically:

~~~text
cross-sectional disease-state projection
    is NOT established as
a monotonic intervention-response coordinate
~~~

It is not:

~~~text
minoxidil does not affect WNT
~~~

## Model update

HF01 now separates two objects:

~~~text
state axis phi(x)
    features useful for distinguishing disease-associated states

response axis chi_u(x)
    state change caused by a declared input u over a declared interval
~~~

A state-separating feature need not have the correct geometry to measure actuator response.

This produces a new DCS invariant candidate:

~~~text
State Separation Axis != Actuator Response Axis
~~~

## Consequence for normal-model feedback

The same warning applies to human feedback.

A variable that tells a person how far they are from a reconstructed normal state is not automatically the variable that should move first when the person changes behavior or receives another bounded input.

HF01 must therefore identify both:

1. state estimation coordinates;
2. response/susceptibility coordinates.

Only their combination can support a recoverability estimate.
