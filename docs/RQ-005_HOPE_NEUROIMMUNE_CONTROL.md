# RQ-005 — Psychological control state, neuroimmune mediation, and tumor dynamics

## Status

**OPEN RESEARCH / SYNTHETIC MODEL ONLY**

This research lane asks whether a change commonly described with words such as
"hope", "resilience", "will to live", or "giving up" can be decomposed into
measurable intermediate states that alter tumor-control dynamics.

It does **not** assume that positive thinking cures cancer.

It does **not** recommend delaying, replacing, or modifying oncology treatment.

## Research question

> Can a psychological state transition alter measurable neuroendocrine,
> behavioral, and immune mediators enough to move a cancer-bearing system
> across a tumor-growth / tumor-control boundary?

The central DCS move is:

~~~text
global label ("hopeful", "hopeless")
    !=
unique internal biological state
~~~

The label is therefore not entered directly into the tumor equation.

## Causal decomposition

~~~mermaid
flowchart LR
    H["latent psychological control state"] --> A["treatment engagement / adherence"]
    H --> R["stress recovery / sleep / activity / social regulation"]

    R --> S["SNS / HPA stress signaling"]
    S --> I["immune suppression / exhaustion"]
    S --> T["tumor-supporting signals"]

    A --> M["effective medical treatment"]
    M --> T
    M --> E["anti-tumor effector activity"]

    I --> E
    E --> T
    T --> I
~~~

Every arrow is a hypothesis class. No arrow is considered established merely
because it appears in the diagram.

## Why the question is scientifically plausible

Recent reviews describe biologically plausible routes from chronic
psychological stress through the sympathetic nervous system (SNS) and HPA axis
to catecholamines and glucocorticoids, with downstream effects on CD8 T cells,
NK cells, myeloid-derived suppressor cells, macrophage polarization,
angiogenesis, metastasis, and therapy response.

At the same time, the National Cancer Institute states that evidence that
stress *directly* affects cancer survival remains weak overall. This distinction
is a core invariant for RQ-005.

Spontaneous regression is real but rare. Case literature supports heterogeneous
mechanisms including immune activation, infection/inflammation, tumor biology,
treatment carry-over, and other factors. A psychological explanation must not
be inferred merely from temporal association.

## Evidence tension that must remain visible

The survival literature is not settled.

- A 2024 systematic review/meta-analysis of randomized psychological
  interventions in early-stage cancer reported no significant overall-survival
  or recurrence-free-survival benefit (OS HR 0.97; RFS HR 0.99).
- A preregistered 2026 systematic review/meta-analysis and multiverse analysis
  of 32 randomized trials reported a small overall survival association
  (HR 0.80, 95% CI 0.71–0.90), but with moderate-to-substantial heterogeneity
  and a wide prediction interval (0.49–1.29).

RQ-005 treats this disagreement as data, not as a nuisance to be averaged away.

## Minimal state model

Let:

~~~text
T(t) = tumor burden
E(t) = anti-tumor effector activity
I(t) = immunosuppressive pressure
S(t) = chronic stress signaling
M(t) = effective medical treatment
~~~

A deliberately minimal tumor equation is:

~~~text
dT/dt =
  T * [
      r * (1 - T/K)
    + beta_s * S
    - k_e * E
    - k_m * M
  ]
~~~

Therefore the instantaneous tumor-control boundary is:

~~~text
k_e * E + k_m * M
>
r * (1 - T/K) + beta_s * S
~~~

Left side: tumor-control pressure.

Right side: tumor-growth pressure.

This inequality is the mathematical object of interest. A psychological state
does not appear directly. It can matter only if it changes measurable
mediators that move the system across this boundary.

## Mediator dynamics

The current synthetic implementation uses **absolute measured/assigned mediator values**, not one-way "boost" variables. This matters: the model is deliberately neutral about whether a psychological state increases, decreases, or leaves adherence and stress recovery unchanged. That mapping is an empirical question.

The current synthetic implementation adds:

~~~text
dS/dt = stress_input - measured_stress_recovery_rate * S

dI/dt =
    tumor_to_suppression(T)
  + stress_to_suppression * S
  - suppression_clearance * I

dE/dt =
    immune_source
  + treatment_immune_support * M
  - immune_decay * E
  - stress_exhaustion * S * E
  - suppression * I * E
~~~

This is **not calibrated to human cancer**. It is a known-answer harness for
checking whether the proposed causal graph has coherent, falsifiable behavior.

Implementation:
[src/dissociated_control_systems/cancer_control.py](../src/dissociated_control_systems/cancer_control.py)

## HYP-005 — Mediated State-Transition Hypothesis

A psychological control-state change has no special tumor-killing term.

Instead, any clinically meaningful effect must be mediated by one or more
measurable variables such as:

- sustained stress-axis signaling;
- sleep/circadian regularity;
- physical activity and conditioning;
- treatment engagement/adherence;
- nutrition and recovery;
- social support;
- inflammatory signaling;
- CD8/NK state;
- T-cell exhaustion / regulatory-cell balance;
- tumor microenvironment state.

### Falsifier

If intervention-associated changes in the psychological state occur **without**
measurable mediator changes, while tumor outcomes change, the current causal
model is incomplete.

If mediator changes occur but tumor-control outcomes do not shift after
adequate adjustment and power, the proposed pathway is weakened.

## HYP-006 — Basin-Crossing Hypothesis for rare regressions

Rare tumor regression may reflect a nonlinear transition rather than a smooth
linear effect.

A system near the control boundary could be pushed across it by a combination
of factors:

~~~text
tumor immunogenicity
+ treatment carry-over
+ immune reactivation
+ infection/inflammatory trigger
+ reduced suppressive signaling
+ improved effective treatment exposure
-----------------------------------------
= possible state transition
~~~

The hypothesis predicts that "miracle survivor" case reports should show
detectable precursor changes in at least some biological mediators if suitable
samples exist.

Psychological narrative alone is insufficient evidence.

## RQ-005 validation ladder

1. **VAL-A — algebraic known answer**
   Verify that the control-margin sign matches the sign of dT/dt.

2. **VAL-B — mediator separation**
   Show that stress-recovery and treatment-adherence channels can alter the
   trajectory independently, in either direction when their measured values
   differ between groups.

3. **VAL-C — sensitivity / phase map**
   Sweep S, E, M, and I to map the tumor-control boundary and identify knees,
   bistable-like regions, and fragile transition zones.

4. **VAL-D — negative controls**
   Verify structurally that a "hope" or "resilience" label has no direct model
   edge. A label-only perturbation must therefore have exactly zero effect.

5. **PUBLIC-DATA-A — longitudinal biomarker test**
   Use public oncology cohorts with repeated distress/stress measures,
   inflammatory or immune markers, treatment exposure, and clinical outcomes.

6. **PUBLIC-DATA-B — spontaneous-regression biopsy**
   Treat rare regression cases as a case-series state-reconstruction problem,
   not as proof of mind-over-cancer.

7. **META-A — conflicting survival meta-analyses**
   Reproduce sensitivity to endpoint, cancer type, stage, intervention class,
   follow-up duration, and analytic choices.

## Measurement candidates

Psychological / control state:
- validated distress, depression, resilience, meaning, self-efficacy measures;
- ecological momentary assessment where available.

Neuroendocrine:
- cortisol rhythm rather than a single value where possible;
- catecholamine/adrenergic proxies;
- heart-rate variability as an imperfect autonomic proxy.

Immune:
- CD8 T-cell phenotype and exhaustion;
- NK-cell activity;
- Treg/MDSC/TAM-related markers;
- cytokines and CRP;
- spatial or single-cell tumor microenvironment features where available.

Behavior / treatment:
- dose intensity;
- missed/cancelled treatment;
- medication adherence;
- sleep/activity;
- nutrition/weight trajectories.

Clinical:
- RECIST response where appropriate;
- ctDNA;
- progression-free survival;
- overall survival;
- recurrence.

## Major confounders

Any human-data analysis must explicitly model at least:

- tumor type, stage, molecular subtype, tumor burden;
- treatment type and line;
- performance status;
- socioeconomic access;
- smoking/alcohol and other health behaviors;
- infection;
- corticosteroid and immunosuppressive exposure;
- baseline inflammation;
- reverse causality: worsening cancer can itself cause distress and
  neuroendocrine changes.

## Safety boundary

~~~text
Hope != cancer treatment
Psychotherapy != replacement oncology
Stress reduction != guaranteed tumor regression
Case report != causal proof
Synthetic attractor != patient prognosis
Model QED != clinical QED
~~~

This lane is for mechanism discovery and falsification.

## Initial literature anchors

- NCI, **Stress and Cancer**:
  https://www.cancer.gov/about-cancer/coping/feelings/stress-fact-sheet
- Ma Y, Kroemer G. **The cancer-immune dialogue in the context of stress.**
  Nature Reviews Immunology (2024).
  https://www.nature.com/articles/s41577-023-00949-8
- Zhang Y, Kong Y, Zhao S. **Psychological stress and tumor progression:
  Molecular mechanisms and therapeutic implications.** Oncology Letters
  (2026), PMID 42741309.
  https://pubmed.ncbi.nlm.nih.gov/42741309/
- Huang Y, Zhan Y, Zhan Y. **Psychological stress on cancer progression and
  immunosenescence.** Seminars in Cancer Biology (2025), PMID 40348001.
  https://pubmed.ncbi.nlm.nih.gov/40348001/
- Bognár SA et al. **Psychological intervention improves quality of life in
  patients with early-stage cancer: a systematic review and meta-analysis of
  randomized clinical trials.** Scientific Reports (2024), PMID 38853187.
  https://pubmed.ncbi.nlm.nih.gov/38853187/
- **Psychosocial interventions indicate prolonged survival in cancer patients
  in a systematic review, meta-analysis, and multiverse meta-analysis of
  randomized controlled trials.** (2026), PMID 41673256.
  https://pubmed.ncbi.nlm.nih.gov/41673256/
- Medici B et al. **Spontaneous Regression of an Inflammatory Myofibroblastic
  Tumor: A Case Report and a Review of the Literature.** (2024),
  PMID 39474532.
  https://pubmed.ncbi.nlm.nih.gov/39474532/
- Recent SCLC spontaneous-regression case with increased CD8 T cells and
  reduced regulatory T cells, PMID 41234590.
  https://pubmed.ncbi.nlm.nih.gov/41234590/

## Next computational tranche

The next useful result is not a prettier narrative. It is a phase diagram:

~~~text
x-axis: chronic stress signal S
y-axis: effective anti-tumor control k_e E + k_m M
surface: sign and magnitude of dT/dt
~~~

Then add uncertainty bands and Monte Carlo parameter sweeps to identify which
claims survive broad parameter perturbation.


## Meta-improvement log — beneficial-by-construction failure

The first implementation represented the two behavioral channels as
`adherence_boost >= 0` and `recovery_boost >= 0`.

A 10,000-draw synthetic Monte Carlo perturbation then found the "mediated"
arm outperforming the reference arm in 100% of draws.

That result was rejected as evidence.

The experiment exposed a design flaw: the intervention variables could only
move in a beneficial direction, so the apparent robustness was partly
structural.

The model was revised to accept absolute `adherence` and
`stress_recovery_rate` values instead. The psychological-state-to-mediator
mapping is now outside the tumor model and must be learned or tested from
data.

~~~text
Meta-loop rule:

If the model cannot represent the null or an adverse mediator shift,
it is not yet a fair test of the psychological hypothesis.
~~~
