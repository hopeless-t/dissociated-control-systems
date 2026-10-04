# Cross-research transfer audit — 2026-10-04

> Status: RESEARCH INTAKE  
> DCS clinical authority: NONE

## Transfers that materially help CGD

| source | transferable atom | CGD use |
| --- | --- | --- |
| DCS VAL-001 / state model | coarse observation can be non-identifying | never infer one latent state from one coarse behavior |
| DCS observation stress | independent evidence can outperform deeper control | add observation diversity before meta depth |
| DCS OOD / residual lanes | wrong sufficient statistic can hide drift | monitor residual surprise and explicit missingness |
| Finite RAM Lab Evidence Model | Intent -> Execution -> Observation -> Checks -> Evidence | separate probe plan, act, measurement, validation, finding |
| Finite RAM MATH-003/006 | rare-state harvesting + Monte Carlo capture-region localization | enrich rare fault states, biopsy, then prospectively sample |
| Finite RAM MATH-017 | state acquisition > state prediction; accepted-result correctness | predict -> normalize -> verify -> probe -> commit |
| Finite RAM GATE-002 | asymmetric false-action cost implies specificity frontier | intervention admission cannot optimize accuracy alone |
| Finite Tool Surface BENCH-004 | ADMIT / NO / DEFER are distinct | preserve DEFER instead of inventing a negative |
| Finite Tool Surface Council-023 | qualified invocation != authority | qualified probe != intervention authority |
| Harness Component Economics | paired isometric ablation; provenance; UNKNOWN != zero | freeze paired probes and preserve unknown evidence |
| Jev/Cua E120 | Historical Truth != Current Fact; mismatch != root cause | bind evidence freshness and keep localization claims narrow |
| Jev/Cua E124 | risk and coverage are separate | report conditional risk and accepted/deferred coverage separately |
| Jev/Cua E127-E129 | declared dependency closure, immutable binding, freshness lease | bind external probe definitions/data/materials to identities |
| MVCA Transport Survival | Attempt != Operation; reobserve != reexecute; UNKNOWN != permission | stable probe operation IDs and duplicate-intervention resistance |
| Memory Attention Lab | accounting != performance; claim partition | synthetic accuracy != real-world validity/safety |

## Immediate contract shape

Before a probe can participate in a canonical DCS experiment, bind:

~~~text
probe_id
probe_revision
target_dimension
environment_identity
input_contract
observation_contract
paired_control_identity or NOT_APPLICABLE
perturbation_budget or NOT_APPLICABLE
measurement_provenance
missingness_semantics
freshness_lease
risk_coverage_contract
authority = NONE
~~~

For repeated or remote execution:

~~~text
probe_operation_id = stable logical diagnostic operation
probe_attempt_id   = one physical delivery/measurement attempt

lost response -> reobserve durable evidence
lost response != permission to replay intervention
~~~

## Next research consequence

Finite RAM Lab's success-side reframe is particularly valuable:

~~~text
cheap prediction
-> normalize state
-> verify state
-> execute bounded transition
-> commit only with complete receipts
~~~

For DCS this suggests a future probe transaction:

~~~text
admit probe
-> verify current state/evidence freshness
-> acquire bounded observation
-> validate receipts
-> emit ACCEPTED / DEFER / INVALIDATED

INVALIDATED != diagnostic negative
UNKNOWN != permission to repeat an intervention
~~~

## Non-transfer rule

~~~text
Useful control pattern != Shared Physical Mechanism
~~~

These are methodology transfers only until DCS obtains domain-local evidence.
