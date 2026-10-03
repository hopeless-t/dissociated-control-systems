# RQ-VOICE-001 — Voice as a longitudinal control-state sensor

## Status

**OPEN RESEARCH QUESTION — literature intake complete; experiment contract not yet frozen**

This note introduces voice and speech as a candidate **partial-observation channel**
for dissociated control states. It does not claim that voice is a diagnosis, that
a voice change uniquely identifies a cognitive state, or that intentionally
changing speech prevents or reverses neurodegenerative disease.

## Research question

> Can longitudinal voice/speech observations help distinguish changes in latent
> control state, accessibility, and integration from changes in underlying
> capability — and can deliberate state regulation perturb those latent states
> rather than merely alter the observable signal?

The second clause is deliberately stronger than "can a person make their voice
sound different?" The research target is whether a bounded, intentional
intervention changes an independently supported latent-state estimate.

## Source observations

### Diagnosed voice disorder and later cognitive decline

Russo, Hawkshaw, and Sataloff (2026) analyzed TriNetX US Collaborative Health
Network records. Their voice-disorder and matched-control cohorts contained
833,417 patients. Diagnosed voice disorders were associated with elevated
incident cognitive decline relative to controls (HR 1.291, 95% CI 1.155–1.443).
Voice disorder plus hearing loss showed the largest reported association versus
controls (HR 2.038).

This is an observational association. It does not establish that a voice
disorder causes cognitive decline, that treating voice changes cognition, or
that a particular acoustic feature is an early causal mechanism.

### Lightweight speech-based screening

Mekulu, Aqlan, and Yang (2026) used DementiaBank picture-description samples to
build an interpretable 60-second screening model. The final ElasticNet model had
eight non-zero features and reported ROC-AUC 0.858 on a held-out split. At the
reported threshold chosen for at least 90% sensitivity, specificity was 65%.

Important boundary: this study primarily models linguistic and semantic
features extracted from speech/transcripts. It is evidence that a short speech
sample can contain useful information for classification in that dataset; it is
not prospective proof that raw voice acoustics predict future decline in a
general population.

## DCS mapping

Let:

~~~text
z_t  = latent control / accessibility / integration state
c_t  = nuisance and context state
u_t  = deliberate intervention or task instruction
v_t  = observed voice/speech feature vector
q_t  = independent cognitive-task observations
~~~

A minimal observation model is:

~~~text
v_t = h_voice(z_t, c_t, u_t) + epsilon_v
q_t = h_task(z_t, c_t)       + epsilon_q
z_{t+1} ~ p(z_{t+1} | z_t, u_t, c_t)
~~~

Candidate components of `v_t` include, depending on dataset provenance:

~~~text
acoustic:
  F0 / pitch dynamics
  jitter / shimmer
  harmonic-noise measures
  intensity and timing

speech-motor:
  articulation timing
  speaking rate
  pause structure
  hesitation

linguistic:
  lexical diversity
  noun / pronoun / adverb usage
  syntactic complexity
  semantic drift
  repetition

trajectory:
  within-person deviation from baseline
  recovery after perturbation
  persistence / hysteresis
~~~

The preferred target is not population-level "abnormal voice" alone. It is a
longitudinal deviation:

~~~text
Delta v_t = v_t - baseline_person(t)
~~~

with explicit modeling of age, illness, fatigue, sleep, medication exposure,
hearing, respiratory state, microphone/channel effects, language, and task.

## Hypotheses

### HYP-005 — Longitudinal Voice Observability

A multilevel voice/speech trajectory contains information about latent
control-state change that is not recoverable from one coarse behavioral label.

**Falsifier:** after adequate nuisance control, longitudinal voice/speech
features add no reproducible information about independently measured state or
task performance.

### HYP-006 — Volitional State Perturbation

A bounded intentional intervention — for example attention allocation,
metacognitive monitoring, deliberate retrieval strategy, or non-pathological
breathing / speech pacing — can alter a subset of latent control/accessibility
variables.

This hypothesis does **not** assert disease modification.

To count as evidence for latent-state change rather than signal manipulation,
the intervention must alter at least one independent observation channel
(`q_t`, or another pre-registered measure) in the predicted direction.

### HYP-007 — Sensor-Gaming Separability

Deliberately changing voice production can move `v_t` without changing the
relevant latent cognitive state. A valid model must therefore distinguish:

~~~text
voice moved, independent cognition did not
    => observation-channel manipulation candidate

voice and independent measures co-moved reproducibly
    => latent-state perturbation candidate

independent cognition moved, voice did not
    => voice is an incomplete observer for that transition
~~~

This is a central anti-overclaiming test.

## Why this matters to DCS

The DCS framework separates capability from accessibility and observation. Voice
is attractive precisely because it is a cheap, continuous, external signal
generated through a long control chain:

~~~text
latent state
  -> attention / retrieval / planning
  -> language formulation
  -> respiratory / laryngeal / articulatory control
  -> acoustic and linguistic observation
~~~

That chain creates both opportunity and ambiguity. It may expose hidden-state
drift, but it also creates many ways to alter the observation without changing
the state of interest.

The project therefore treats voice as a **sensor candidate**, not as ground
truth.

## "Can conscious control resist decline?"

The scientifically testable version is narrower:

> Are some losses of observed performance partly mediated by modifiable control,
> access, allocation, or integration states, such that deliberate strategies
> can improve resilience or expressed capability even when underlying capacity
> is unchanged?

DCS can test that question.

It cannot currently infer from the cited studies that "mindset" prevents
dementia, reverses neurodegeneration, or changes long-term disease progression.
Those are separate clinical claims requiring independent evidence.

## Experiment path

### Stage A — synthetic identifiability

Extend the DCS synthetic model with two observation channels:

~~~text
voice/speech observer v_t
independent task observer q_t
~~~

Inject:

- latent-state changes;
- nuisance-only changes;
- deliberate observation-channel manipulation;
- genuine latent-state perturbations.

Acceptance criterion: the inference layer must not classify voice-only
manipulation as latent-state recovery.

### Stage B — public-data replication

Use qualified public speech datasets with explicit provenance. Reproduce a
small interpretable baseline before adding complex models.

Pre-register:

- train/test partition rules;
- participant-level leakage prevention;
- nuisance variables;
- feature definitions;
- calibration metrics;
- uncertainty;
- subgroup limitations.

### Stage C — longitudinal model

Only after Stage B, test within-person trajectories when an appropriate public
longitudinal dataset exists.

Primary object:

~~~text
P(z_t | v_0:t, q_0:t, c_0:t)
~~~

rather than a one-shot disease label.

### Stage D — intervention sensitivity

Use synthetic or appropriately governed non-clinical/public data first.

The key contrast is:

~~~text
observation manipulation
vs
latent-state perturbation
vs
capability change
~~~

A future human study would require its own ethics, consent, safety, and clinical
governance. This repository does not authorize medical self-experimentation.

## Failure modes to preserve

- correlation interpreted as causation;
- cross-sectional classifier interpreted as longitudinal predictor;
- voice-disorder diagnosis interpreted as an acoustic biomarker;
- transcript-derived language features described as purely acoustic voice;
- demographic or microphone confounding;
- participant leakage across train/test splits;
- a participant learning to "sound normal" and fooling the sensor;
- short-term task improvement described as neuroprotection;
- disease modification inferred from accessibility improvement.

## References

See [REFERENCES.md](REFERENCES.md):

- [P-VOICE-COG-2026] Russo, Hawkshaw, and Sataloff (2026).
- [P-VOICE-SCREEN-2026] Mekulu, Aqlan, and Yang (2026).

Secondary intake article:

- Nazology, 2026-10-02, "「声」から「認知の低下」を早めに知る手がかり"
  https://nazology.kusuguru.co.jp/archives/200526

The secondary article is an intake pointer, not the canonical scientific
evidence source.
