# CGD-OBS-002 — Preregistered Observational Variable Map

> Status: PROTOCOL FREEZE CANDIDATE  
> Human participant rows processed: NONE  
> Clinical authority: NONE

CGD-OBS-001 found domain-local literature supporting study of self vs
study-partner/informant discrepancy, while raw ADNI/BHR access remains outside
the current execution lane.

OBS-002 freezes the mathematical observation layer before inspecting any
participant-level dataset.

## Orientation

Every input must first be transformed into an impairment-oriented value:

~~~text
larger value = greater impairment
~~~

The transformation/normalization identity must be frozen and versioned. The
protocol may not choose a normalization after inspecting the desired outcome.

## Primary signed quantities

~~~text
S = self-reported impairment
I = informant-reported impairment
O = objective impairment under frozen normalization

D_SI = I - S
D_SO = O - S
D_IO = O - I
~~~

Interpretation:

~~~text
D > 0:
    self channel reports less impairment than comparator

D < 0:
    self channel reports more impairment than comparator
~~~

Do not replace these primary signed variables with absolute gaps. Direction is
scientifically relevant.

For a complete triad:

~~~text
D_SO = D_SI + D_IO
~~~

This becomes a deterministic consistency check.

## Longitudinal endpoints

For visits separated by dt years:

~~~text
slope(D_SI) = (D_SI_followup - D_SI_baseline) / dt
slope(D_SO) = (D_SO_followup - D_SO_baseline) / dt
slope(O)    = (O_followup - O_baseline) / dt
~~~

A candidate pattern such as increasing discrepancy alongside worsening
objective impairment may be tested later, but is not declared causal by this
protocol.

## Missingness

~~~text
missing informant != informant score zero
missing objective != normal objective cognition
partial triad != complete triad
~~~

Dyad-only and self-objective-only observations remain explicit partial states.

Any later analysis must report channel coverage and missingness by group/time,
not only complete-case accuracy.

## Instrument binding

Self and informant values may be directly differenced only when the protocol
has established compatible instrument/domain/scoring semantics.

Objective scores require a frozen normalization identity because raw cognitive
test scores generally do not share the same scale as questionnaire scores.

## Falsification / stop conditions

A later dataset execution must DEFER or invalidate the affected endpoint when:

- scale direction cannot be established;
- self/informant instrument compatibility is not established;
- objective normalization identity is absent or changed post hoc;
- visit chronology is invalid;
- missingness is silently coerced to zero/normal;
- instrument version or scoring rules drift without requalification;
- population scope differs materially from the preregistered claim;
- only an absolute discrepancy is retained and direction is lost.

## DCS mapping boundary

The observed variables are not aliases for synthetic latent state:

~~~text
D_SI != L1 calibration fault
D_SO != anosognosia ground truth
O    != latent capability C(t)
~~~

They are candidate observable projections that may support, contradict, or
leave the DCS model inconclusive.

## Next step

A future CGD-OBS-003 may preregister statistical tests and negative controls
using only this frozen variable contract. Raw participant-level data remain
outside the current lane until source-specific access and AI-use conditions are
compatible.
