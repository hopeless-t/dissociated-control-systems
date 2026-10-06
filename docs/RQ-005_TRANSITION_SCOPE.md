# RQ-005 Transition-specific mechanism scope

## Meta-loop correction

The first post-recurrence world list treated `dormancy/reactivation` too broadly.
That was an overgeneralization.

Classic disseminated-tumor-cell dormancy primarily addresses why clinically
undetectable disseminated cells can remain latent before overt metastatic
recurrence and later reactivate.

That makes it a natural candidate for:

~~~text
DIAGNOSIS / CONTROLLED DISEASE
        ->
OVERT RECURRENCE
~~~

It does **not**, by itself, explain why a patient who has already developed an
early overt recurrence then remains alive for another 15+ years.

Therefore:

~~~text
Mechanism For Recurrence Timing
!=
Mechanism For Post-Recurrence Control
~~~

Implementation:

- `src/dissociated_control_systems/mechanism_scope.py`
- `tests/test_mechanism_scope.py`

The known-answer contract deliberately scopes classic pre-recurrence DTC
dormancy to `diagnosis_to_recurrence` and rejects silently laundering it into
`recurrence_to_cancer_death`.

## Revised mechanism priority by transition

### Transition 0 -> 1: diagnosis/control to first recurrence

High-priority candidates include:

- residual/disseminated tumor-cell state;
- dormancy / reawakening;
- organ-specific niche state;
- immune surveillance / escape;
- primary-tumor biology and dissemination competence;
- treatment effects on residual disease;
- systemic host-state candidates where temporally measured.

### Transition 1 -> 2: overt recurrence to cancer death/censor

For the current early-recurrence durable-control sentinels, prioritize:

1. metastatic site, lesion number, and total recurrent burden;
2. oligometastatic versus polymetastatic topology;
3. systemic treatment sequence and treatment sensitivity;
4. radiologic depth of response / CR / NED state;
5. metastasis-directed local therapy;
6. recurrent-tumor molecular state / subtype evolution;
7. metastatic immune/TME architecture;
8. systemic host-state mediators;
9. psychological/agency variables only through measured mediators and with
   temporal precedence.

Dormancy can re-enter transition 1 -> 2 only under a more specific measured
claim, for example persistent microscopic residual clones entering a dormant
state after eradication/control of overt lesions. That is not the same claim as
classic pre-recurrence dormancy and requires separate evidence.

## External constraint

Recent dormancy reviews describe disseminated cancer cells persisting in
quiescent states before reactivation, with immune, stromal, extracellular-matrix
and organ-niche regulation (PMIDs 39821034, 40628544, 41855938, 42032160).

A 2025 metastatic-breast-cancer exceptional-response cohort instead directly
links durable metastatic outcomes to response state: 69% of 58 exceptional
responders reached CR/NED, and CR/NED had better reported outcomes than partial
response (PMID 39987798).

For the R2 sentinels this currently puts response/topology ahead of generic
`dormancy` in expected observation value.

## New semantic barrier

Every mechanism claim must declare the transition it purports to explain.

~~~text
mechanism claim
  -> declared transition scope
  -> temporally eligible observations
  -> matched competing mechanisms
  -> transition-specific held-out endpoint
  -> calibrated claim
~~~

A mechanism that predicts overall survival but fails on its declared transition
is not accepted as a mechanism for that transition.
