# CGD-SIM-053 — Failure-mode diversity audit

> Status: SYNTHETIC FAILURE-MODE-DIVERSITY TEST  
> Clinical authority: NONE

SIM-052 showed that a primary context channel and a watchdog can agree while
being jointly wrong when they share a common-mode bias. Pairwise disagreement
cannot identify a term that enters both channels equally.

SIM-053 changes the architecture rather than adding more copies of the same
sensor family.

## Three-channel construction

~~~text
primary context       = environment + B_common + eps_primary
same-family watchdog  = environment + B_common + eps_watchdog
orthogonal audit      = environment + eps_orthogonal
~~~

Therefore:

~~~text
primary - same-family watchdog = eps_primary - eps_watchdog
primary - orthogonal audit      = B_common + eps_primary - eps_orthogonal
~~~

The third channel makes the shared bias observable because it does not share
that failure mode by construction.

## Frozen attack

The common-mode trajectory is inherited from SIM-052:

~~~text
epoch 0:      B_common = 0.00
epoch 1..6:   B_common = +0.08
epoch 7..9:   B_common = 0.00
~~~

The orthogonal audit uses 16 paired samples per epoch with synthetic noise
standard deviation `0.015`. A change in its estimated primary bias of at least
`0.03` revokes the current route authority and requests the existing full
qualification gate.

The audit does **not** choose the route itself.

## Controls

- Negative control: SIM-052 same-family pairwise watchdog.
- Safety reference: full qualification is always available after revocation.
- Hard maximum authority age remains `6` epochs, though the frozen hypothesis
  predicts the orthogonal audit should trigger before it is needed.

## Metrics

- common-mode onset/recovery trigger epochs;
- full qualification count;
- stale-authority epochs;
- maximum selection regret;
- reduction in full qualifications versus an every-epoch gate;
- comparison with the same-family watchdog.

## Frozen hypotheses

The orthogonal audit should detect both the onset and removal of the `+0.08`
common-mode bias, causing full requalification at epochs `1` and `7`.

Expected structure:

~~~text
initial qualification + onset + recovery = 3 full qualifications
~~~

with zero stale-authority epochs in this frozen trajectory.

## New invariants

~~~text
Redundancy != Diversity
N Channels != N Independent Failure Modes
Agreement Is Strong Evidence Only Under Failure-Mode Independence
Orthogonal Audit Can Recover Shared-Bias Observability
Audit Has Revocation Authority, Not Routing Authority
~~~

## Claim ceiling

The orthogonal audit is idealized. In a real system, channels that look
independent can still share data provenance, training distributions,
calibration assumptions, caregivers, environmental conditions, software
stacks, or other hidden causes.

A PASS therefore supports a design principle, not a specific monitoring
technology: add evidence with different failure modes, and keep its authority
limited to revocation/requalification unless routing authority is separately
qualified.
