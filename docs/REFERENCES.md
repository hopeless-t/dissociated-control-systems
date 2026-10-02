# References and source registry

This repository treats citations as part of the scientific boundary.

## Citation policy

1. Prefer primary research for empirical claims.
2. Mark reviews and hypothesis papers as reviews or hypotheses.
3. Keep safety guidance separate from mechanism claims.
4. Record what role each source plays in this repository.
5. Citation does not mean reproduction.
6. Similarity does not establish direct lineage or a shared mechanism.
7. Reference software is not scientific evidence by itself.

## NREM parasomnia and local state dissociation

### [P-DISSOC-2009] Terzaghi et al.

M. Terzaghi et al. "Evidence of dissociated arousal states during NREM
parasomnia from an intracerebral neurophysiological study." Sleep 32(3),
409–412 (2009).

DOI: https://doi.org/10.1093/sleep/32.3.409  
PubMed: https://pubmed.ncbi.nlm.nih.gov/19294961/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC2647795/

Role: direct intracerebral-EEG precedent for local wake-like motor/cingulate
activity coexisting with sleep-like frontoparietal associative activity during
a confusional arousal.

### [P-HDEEG-2016] Castelnovo et al.

A. Castelnovo et al. "Scalp and Source Power Topography in Sleepwalking and
Sleep Terrors: A High-Density EEG Study." Sleep 39(10), 1815–1825 (2016).

PubMed: https://pubmed.ncbi.nlm.nih.gov/27568805/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC5020364/

Role: high-density EEG evidence relevant to local sleep/arousal differences.

### [P-HDEEG-2026] Valomon et al.

A. Valomon et al. "High-density EEG signature of NREM sleep parasomnia
episodes." Scientific Reports 16, 19414 (2026).

DOI: https://doi.org/10.1038/s41598-026-41601-4  
PubMed: https://pubmed.ncbi.nlm.nih.gov/42045284/

Role: recent hdEEG evidence for a mixed pattern of cortical arousal and sleep
during NREM parasomnia episodes.

## Zolpidem-associated complex sleep behavior

### [P-SRED-2002] Morgenthaler and Silber

T. I. Morgenthaler and M. H. Silber. "Amnestic sleep-related eating disorder
associated with zolpidem." Sleep Medicine 3(4), 323–327 (2002).

PubMed: https://pubmed.ncbi.nlm.nih.gov/14592194/

Role: early case-series evidence for amnestic nocturnal eating associated with
zolpidem.

### [R-SRED-2020] Ho et al.

T. Ho et al. "Sleep-related eating disorder associated with zolpidem: cases
compiled from a literature review." Sleep Medicine X 2, 100019 (2020).

DOI: https://doi.org/10.1016/j.sleepx.2020.100019  
PubMed: https://pubmed.ncbi.nlm.nih.gov/33870172/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8041106/

Role: descriptive synthesis of published zolpidem-associated SRED cases,
including partial/full amnesia and complex meal preparation.

### [I-FDA-CSB] U.S. Food and Drug Administration

Safety communication on serious injuries associated with complex sleep
behaviors from certain insomnia medicines (2019).

https://www.fda.gov/safety/medical-product-safety-information/certain-prescription-insomnia-medicines-new-boxed-warning-due-risk-serious-injuries-caused

Role: safety boundary only; not a mechanism source.

## Paradoxical arousal and disorders of consciousness

This line is clinically distinct from zolpidem-associated parasomnia.

### [R-MESOCIRCUIT-2010] Schiff

N. D. Schiff. "Recovery of consciousness after brain injury: a mesocircuit
hypothesis." Trends in Neurosciences 33(1), 1–9 (2010).

DOI: https://doi.org/10.1016/j.tins.2009.11.002  
PubMed: https://pubmed.ncbi.nlm.nih.gov/19954851/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC2931585/

Role: circuit-level hypothesis for recovery and access to residual functional
capacity after severe brain injury.

### [P-ZOL-METAB-2014] Chatelle et al.

C. Chatelle et al. "Changes in cerebral metabolism in patients with a minimally
conscious state responding to zolpidem." Frontiers in Human Neuroscience 8,
917 (2014).

DOI: https://doi.org/10.3389/fnhum.2014.00917  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC4251320/

Role: small responder study reporting metabolic changes after zolpidem.

## Mathematical and software references

### [M-HMM-1989] Rabiner

L. R. Rabiner. "A Tutorial on Hidden Markov Models and Selected Applications
in Speech Recognition." Proceedings of the IEEE 77(2), 257–286 (1989).

DOI: https://doi.org/10.1109/5.18626

Role: classical reference for partially observed discrete-state systems.

### [S-DYNAMAX] Dynamax

Repository: https://github.com/probml/dynamax

S. W. Linderman et al. "Dynamax: A Python package for probabilistic state
space modeling with JAX." Journal of Open Source Software 10(108), 7069
(2025).

DOI: https://doi.org/10.21105/joss.07069

Role: candidate future state-space inference implementation.

### [S-HMMLEARN] hmmlearn

https://github.com/hmmlearn/hmmlearn

Role: reference implementation for conventional HMM workflows.

### [S-SSM] lindermanlab/ssm

https://github.com/lindermanlab/ssm

Role: reference implementation for state-space and switching models.

### [S-MNE] MNE-Python

https://github.com/mne-tools/mne-python

Role: candidate EEG/MEG analysis stack for later public-data work.

### [S-YASA] YASA

https://github.com/raphaelvallat/yasa

Role: candidate sleep-analysis tooling for later qualified public datasets.

### [S-PMNDRS-MATH] pmndrs/math

Repository: https://github.com/pmndrs/math

Pinned reference commit:

~~~text
98762395c1f34d7d594d31165e8005fd6915c431
~~~

License: MIT.

Upstream describes the library as a small, tree-shakeable, data-oriented math
engine with vectors, matrices, geometry, seeded random generators, noise,
animation helpers, and related primitives.

Role in this repository: optional lightweight calculation / prototyping tool.
It is not scientific evidence, not a canonical dependency, and not a substitute
for independently validated numerical methods when a research contract requires
them.

See [../external/pmndrs-math.md](../external/pmndrs-math.md).

### [S-GPUCAT] gpucat

Repository: https://github.com/isaac-mason/gpucat

Pinned reference commit:

~~~text
d739e5bed1597858a5c1d96f53641b965699cf32
~~~

License: MIT.

Role in this repository: experimental rendering reference for the Dissociated
State Field lineage. The canonical public VIS-001 renderer is Canvas2D after
real-browser testing found a blank WebGL field on the target environment.
gpucat is not scientific evidence and rendered output is not an acceptance
oracle.

See [../external/gpucat.md](../external/gpucat.md).

## Repository-shape provenance

Repository discipline is adapted from:

https://github.com/hopeless-t/topological-spin-lab

and later Catfood Lab research repositories.

Only the reproducibility and evidence discipline is inherited; the scientific
claims are not.


## Somatosensory attention, expectation, and affective touch

### [P-TACTEXP-2010] van Ede, Jensen, and Maris

F. van Ede, O. Jensen, and E. Maris. "Tactile expectation modulates
pre-stimulus beta-band oscillations in human sensorimotor cortex."
NeuroImage 51(2), 867–876 (2010).

DOI: https://doi.org/10.1016/j.neuroimage.2010.02.053  
PubMed: https://pubmed.ncbi.nlm.nih.gov/20188186/

Role: primary MEG evidence that expectation of a tactile event is associated
with pre-stimulus oscillatory modulation in sensorimotor / somatosensory
cortex; supports a central preparatory-state hypothesis.

### [P-SOMATTN-2014] van Ede et al.

F. van Ede et al. "Attentional modulations of somatosensory alpha, beta and
gamma oscillations dissociate between anticipation and stimulus processing."
NeuroImage 97, 134–141 (2014).

PubMed: https://pubmed.ncbi.nlm.nih.gov/24769186/

Role: primary MEG evidence distinguishing anticipatory attention-related
alpha/beta modulation from gamma modulation during tactile stimulus
processing.

### [P-TACTOMIT-2018] Andersen and Lundqvist

L. M. Andersen and D. Lundqvist. "Somatosensory responses to nothing: An MEG
study of expectations during omission of tactile stimulations." NeuroImage 184,
78–89 (2019; online 2018).

DOI: https://doi.org/10.1016/j.neuroimage.2018.09.014  
PubMed: https://pubmed.ncbi.nlm.nih.gov/30213774/

Role: primary evidence that an expected but omitted tactile event can produce a
time-locked central response, source-localized in the study to secondary
somatosensory cortex and insula.

### [P-PPS-2024] Geers, Kozieja, and Coello

L. Geers, P. Kozieja, and Y. Coello. "Multisensory peripersonal space: Visual
looming stimuli induce stronger response facilitation to tactile than auditory
and visual stimulations." Cortex 173, 222–233 (2024).

DOI: https://doi.org/10.1016/j.cortex.2024.01.008  
PubMed: https://pubmed.ncbi.nlm.nih.gov/38430652/

Role: primary evidence relevant to pre-contact visual approach and
multisensory tactile facilitation. Used as a decomposition source, not as proof
of a special non-contact mechanism.

### [P-EROG-2018] Croy et al.

I. Croy et al. "Dissociable sources of erogeneity in social touch: Imagining
and perceiving C-Tactile optimal touch in erogenous zones." PLoS ONE 13(8),
e0201929 (2018).

PubMed: https://pubmed.ncbi.nlm.nih.gov/30142185/

Role: primary behavioral evidence that imagined and actual affective touch can
both influence pleasantness/arousal ratings, relevant to top-down expectation,
body-region effects, and the need to separate imagined from physical input.

### [R-CT-2020] Strauss et al.

T. Strauss et al. "Pleasantness Only? How Sensory and Hedonic Properties of
Gentle Touch Are Processed." Experimental Psychology 67(3), 196–208 (2020).

DOI: https://doi.org/10.1027/1618-3169/a000492  
PubMed: https://pubmed.ncbi.nlm.nih.gov/33111658/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8820238/

Role: review / interpretive source for the group-level inverted-U relation
between stroking velocity and pleasantness and for limits of a simple
CT-afferent-only explanation.
