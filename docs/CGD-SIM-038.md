# CGD-SIM-038 — External observation structural identifiability

> Status: SYNTHETIC ALGEBRAIC OBSERVATION TEST  
> Clinical authority: NONE

CGD-EXT-001 identified an externally plausible four-channel observation family:

1. participant/self report;
2. informant/study-partner report;
3. objective standardized performance;
4. everyday function under the current environment/scaffold.

SIM-038 asks a narrower mathematical question before any participant-level data
are requested:

> Are self/informant disagreement scores sufficient to separate current state,
> self-model bias, informant bias, and environmental support?

## Minimal structural model

Let:

~~~text
Z = current task-relevant state
A = self-model / awareness bias
B = informant bias / observer context
E = scaffold / environment contribution to daily function
~~~

and define noiseless observation equations:

~~~text
S = Z - A
I = Z + B
O = Z
F = Z + E
~~~

This is not a biological equation set. It is a rank/identifiability thought
model.

## Immediate consequence

With only self and informant reports:

~~~text
I - S = A + B
~~~

Therefore the familiar self/informant discrepancy aliases at least two terms.
It cannot, by itself, establish that the participant's self-model is wrong.

This directly motivates the DCS invariant:

~~~text
Self-Informant Discordance != Pure Awareness Measurement
Informant Report != Ground Truth
~~~

## Rank test

The state vector has four components `[Z, A, B, E]`.

Candidate observation sets are tested by exact rational Gaussian elimination.

Expected structure:

~~~text
self only                         -> underidentified
self + informant                  -> underidentified
self + informant + objective      -> scaffold remains unseparated
self + informant + function       -> current state/scaffold remain aliased
all four channels                 -> full rank in the declared model
~~~

When all four channels are present:

~~~text
Z = O
A = O - S
B = I - O
E = F - O
~~~

Again, this reconstruction is only a property of the frozen synthetic linear
model.

## Why this matters for external data design

Public ADNI documentation exposes self report, study-partner report, objective
cognitive measures and daily-function measures in the same broad study family.
Published discrepancy literature supports the importance of self/informant
disagreement, while public NACC literature shows that informant context can
systematically affect functional ratings.

SIM-038 therefore rejects the shortcut:

~~~text
informant says X
    -> X is objective reality
~~~

and instead prefers triangulation.

## Claim ceiling

A full-rank observation matrix does not imply:

- unbiased real measurements;
- valid scaling across instruments;
- clinical diagnostic accuracy;
- causal interpretation;
- treatment or safety authority.

The next synthetic step should add measurement noise, reporter drift and
repeated observations to determine how the four-channel architecture degrades
away from the ideal rank case.
