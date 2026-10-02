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

### [P-EROG-2018] Panagiotopoulou et al.

E. Panagiotopoulou, M. L. Filippetti, A. Gentsch, and A. Fotopoulou.
"Dissociable sources of erogeneity in social touch: Imagining and perceiving
C-Tactile optimal touch in erogenous zones." PLoS ONE 13(8), e0203039 (2018).

DOI: https://doi.org/10.1371/journal.pone.0203039  
PubMed: https://pubmed.ncbi.nlm.nih.gov/30142185/

Role: primary behavioral evidence that imagined and actual affective touch can
both influence pleasantness/arousal ratings, relevant to top-down expectation,
body-region effects, and the need to separate imagined from physical input.

### [P-CT-2020] Sailer, Hausmann, and Croy

U. Sailer, M. Hausmann, and I. Croy. "Pleasantness Only?" Experimental
Psychology 67(4), 224–236 (2020).

DOI: https://doi.org/10.1027/1618-3169/a000492  
PubMed: https://pubmed.ncbi.nlm.nih.gov/33111658/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8820238/

Role: primary psychophysical evidence for an inverted-U relation between
stroking velocity and pleasantness and for limits of a simple CT-afferent-only
interpretation.


## Dynamic erogeneity, interpersonal context, and reflective learning

### [P-EROGMAP-2016] Nummenmaa et al.

L. Nummenmaa, J. T. Suvilehto, E. Glerean, P. Santtila, and J. K. Hietanen.
"Topography of Human Erogenous Zones." Archives of Sexual Behavior 45(5),
1207–1216 (2016).

DOI: https://doi.org/10.1007/s10508-016-0745-z  
PubMed: https://pubmed.ncbi.nlm.nih.gov/27091187/

Role: large body-map study showing broad erogenous maps and context dependence
between partner-sex and masturbation conditions.

### [P-PLEASUREPAIN-2013] Paterson, Amsel, and Binik

L. Q. P. Paterson, R. Amsel, and Y. M. Binik. "Pleasure and pain: the effect
of (almost) having an orgasm on genital and nongenital sensitivity." Journal of
Sexual Medicine 10(6), 1531–1544 (2013).

DOI: https://doi.org/10.1111/jsm.12144  
PubMed: https://pubmed.ncbi.nlm.nih.gov/23551826/

Role: primary evidence that pleasantness and pain thresholds can change without
a corresponding significant change in touch detection threshold.

### [P-AROUSALTOUCH-2007] Jiao et al.

C. Jiao, P. K. Knight, P. Weerakoon, and A. B. Turman. "Effects of visual
erotic stimulation on vibrotactile detection thresholds in men." Archives of
Sexual Behavior 36(6), 787–792 (2007).

DOI: https://doi.org/10.1007/s10508-007-9232-x  
PubMed: https://pubmed.ncbi.nlm.nih.gov/17713850/

Role: primary evidence that sexual arousal can alter vibrotactile detection
thresholds at a non-genital body site.

### [P-SOCIALTOUCH-2015] Suvilehto et al.

J. T. Suvilehto, E. Glerean, R. I. M. Dunbar, R. Hari, and L. Nummenmaa.
"Topography of social touching depends on emotional bonds between humans."
PNAS 112(45), 13811–13816 (2015).

DOI: https://doi.org/10.1073/pnas.1519231112  
PubMed: https://pubmed.ncbi.nlm.nih.gov/26504228/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC4653180/

Role: relationship-specific maps of acceptable social touch; supports modeling
emotional bond as a contextual variable rather than a physical touch property.

### [P-ROMANTICTOUCH-2017] Kreuder et al.

A.-K. Kreuder et al. "How the brain codes intimacy: The neurobiological
substrates of romantic touch." Human Brain Mapping 38, 4525–4534 (2017).

DOI: https://doi.org/10.1002/hbm.23679  
PubMed: https://pubmed.ncbi.nlm.nih.gov/28580708/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC6867116/

Role: randomized fMRI study in which participants believed identical physical
touch came from either their romantic partner or an unfamiliar person; relevant
to perceived-identity and relationship gating.

### [P-RESPONSIVE-2016] Birnbaum et al.

G. E. Birnbaum et al. "Intimately connected: The importance of partner
responsiveness for experiencing sexual desire." Journal of Personality and
Social Psychology 111(4), 530–546 (2016).

DOI: https://doi.org/10.1037/pspi0000069  
PubMed: https://pubmed.ncbi.nlm.nih.gov/27399250/

Role: evidence linking perceived partner responsiveness with sexual desire,
used as an interpersonal-context source rather than a somatosensory-mechanism
source.

### [M-SEXCMM-2022] Mallory

A. B. Mallory. "Dimensions of couples' sexual communication, relationship
satisfaction, and sexual satisfaction: A meta-analysis." Journal of Family
Psychology 36(3), 358–371 (2022).

DOI: https://doi.org/10.1037/fam0000946  
PubMed: https://pubmed.ncbi.nlm.nih.gov/34968095/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9153093/

Role: meta-analysis of 93 studies / 38,499 individuals; supports treating
communication quality as a dyadic variable associated with sexual and
relationship satisfaction.

### [P-COMPLIMENT-2023] Eckstein et al.

M. Eckstein et al. "Neural responses to instructed positive couple interaction:
an fMRI study on compliment sharing." Social Cognitive and Affective
Neuroscience 18(1), nsad005 (2023).

DOI: https://doi.org/10.1093/scan/nsad005  
PubMed: https://pubmed.ncbi.nlm.nih.gov/36852857/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9976881/

Role: romantic-couple fMRI evidence relevant to verbal affective input,
relationship meaning, empathy, and reward-related processing.

### [P-REWARDTACT-2008] Pleger et al.

B. Pleger, F. Blankenburg, C. C. Ruff, J. Driver, and R. J. Dolan. "Reward
facilitates tactile judgments and modulates hemodynamic responses in human
primary somatosensory cortex." Journal of Neuroscience 28(33), 8161–8168
(2008).

DOI: https://doi.org/10.1523/JNEUROSCI.1093-08.2008  
PubMed: https://pubmed.ncbi.nlm.nih.gov/18701678/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC2682779/

Role: primary evidence that reward can modulate tactile judgment and
somatosensory-cortex responses, including effects on a subsequent trial.

### [P-COACT-2004] Hodzic et al.

A. Hodzic, R. Veit, A. A. Karim, M. Erb, and B. Godde. "Improvement and
decline in tactile discrimination behavior after cortical plasticity induced by
passive tactile coactivation." Journal of Neuroscience 24(2), 442–446 (2004).

DOI: https://doi.org/10.1523/JNEUROSCI.3731-03.2004  
PubMed: https://pubmed.ncbi.nlm.nih.gov/14724242/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC6730006/

Role: primary evidence that passive tactile coactivation can induce
somatosensory cortical plasticity and alter discrimination.

### [P-SEXCND-2008] Both et al.

S. Both, M. Spiering, E. Laan, S. Belcome, B. van den Heuvel, and W. Everaerd.
"Unconscious classical conditioning of sexual arousal: evidence for the
conditioning of female genital arousal to subliminally presented sexual
stimuli." Journal of Sexual Medicine 5(1), 100–109 (2008).

DOI: https://doi.org/10.1111/j.1743-6109.2007.00643.x  
PubMed: https://pubmed.ncbi.nlm.nih.gov/17971104/

Role: evidence that human genital responding can show associative conditioning;
does not establish acquired erogeneity of a body region.

### [P-SELFATTN-2004] van Lankveld, van den Hout, and Schouten

J. J. D. M. van Lankveld, M. A. van den Hout, and E. G. W. Schouten. "The
effects of self-focused attention, performance demand, and dispositional sexual
self-consciousness on sexual arousal of sexually functional and dysfunctional
men." Behaviour Research and Therapy 42(8), 915–935 (2004).

DOI: https://doi.org/10.1016/j.brat.2003.07.011  
PubMed: https://pubmed.ncbi.nlm.nih.gov/15178466/

Role: evidence that self-focused attention can alter sexual response in a
person-dependent direction; relevant to observer-state and measurement-
interference hypotheses.

### [P-MIRROR-2012] Ainley et al.

V. Ainley, A. Tajadura-Jiménez, A. Fotopoulou, and M. Tsakiris. "Looking into
myself: changes in interoceptive sensitivity during mirror self-observation."
Psychophysiology 49(11), 1504–1508 (2012).

DOI: https://doi.org/10.1111/j.1469-8986.2012.01468.x  
PubMed: https://pubmed.ncbi.nlm.nih.gov/22978299/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC3755258/

Role: primary evidence that mirror self-observation can alter interoceptive
sensitivity in some participants; relevant to Self-Observation Re-entry.


## Human control-space reshaping and skill transitions

### [P-FINGER-2014] Furuya, Nakamura, and Nagata

S. Furuya, A. Nakamura, and N. Nagata. "Acquisition of individuated finger
movements through musical practice." Neuroscience (2014).

DOI: https://doi.org/10.1016/j.neuroscience.2014.06.031  
PubMed: https://pubmed.ncbi.nlm.nih.gov/24973654/

Role: primary evidence that four days of piano practice in musically naive
adults reduced movement covariation across fingers, especially ring and little
fingers; supports an INDIVIDUATE transition without claiming complete
anatomical independence.

### [P-ARCHERY-2023] Kuch et al.

A. Kuch, R. Tisserand, F. Durand, T. Monnet, and J.-F. Debril. "Postural
adjustments preceding string release in trained archers." Journal of Sports
Sciences 41(7), 677–685 (2023).

DOI: https://doi.org/10.1080/02640414.2023.2235154  
PubMed: https://pubmed.ncbi.nlm.nih.gov/37470415/

Role: primary evidence for anticipatory postural adjustments before string
release in trained archers; elite archers used earlier anticipatory strategies
more often in this study.

### [P-GYM-2001] Vuillerme, Teasdale, and Nougier

N. Vuillerme, N. Teasdale, and V. Nougier. "The effect of expertise in
gymnastics on proprioceptive sensory integration in human subjects."
Neuroscience Letters 311(2), 73–76 (2001).

DOI: https://doi.org/10.1016/S0304-3940(01)02147-4  
PubMed: https://pubmed.ncbi.nlm.nih.gov/11567781/

Role: primary evidence that expert gymnasts more efficiently used reintroduced
proprioceptive information to reduce postural sway in the declared perturbation
task; supports REWEIGHT as a testable transition.

### [P-CLIMB-2014] Seifert et al.

L. Seifert, L. Wattebled, R. Herault, G. Poizat, D. Adé, N. Gal-Petitfaux,
and K. Davids. "Neurobiological degeneracy and affordance perception support
functional intra-individual variability of inter-limb coordination during ice
climbing." PLoS ONE 9(2), e89865 (2014).

DOI: https://doi.org/10.1371/journal.pone.0089865  
PubMed: https://pubmed.ncbi.nlm.nih.gov/24587084/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC3933688/

Role: primary evidence that expert ice climbers used a wider range of
functional coordination patterns and fewer exploratory actions than beginners;
supports separating functional variability from task-harmful variability.

### [R-MOTORVAR-2024] Marineau et al.

E. Marineau et al. "From Novice to Expert: How Expertise Shapes Motor
Variability in Sports Biomechanics-a Scoping Review." Scandinavian Journal of
Medicine & Science in Sports 34(8), e14706 (2024).

DOI: https://doi.org/10.1111/sms.14706  
PubMed: https://pubmed.ncbi.nlm.nih.gov/39049526/

Role: scoping review showing that most included sport studies reported lower
motor variability in higher-skilled athletes; used together with climbing
evidence to motivate a structured, task-relative variability model.

### [R-BALLET-2021] Kaufmann et al.

J.-E. Kaufmann, R. G. H. H. Nelissen, E. Exner-Grave, and M. G. J. Gademan.
"Does forced or compensated turnout lead to musculoskeletal injuries in
dancers? A systematic review on the complexity of causes." Journal of
Biomechanics 114, 110084 (2021).

DOI: https://doi.org/10.1016/j.jbiomech.2020.110084  
PubMed: https://pubmed.ncbi.nlm.nih.gov/33338756/

Role: systematic review establishing the methodological complexity of forced /
compensated turnout and showing that older evidence did not support a simple
causal conclusion.

### [R-BALLET-2026] Ota et al.

H. Ota, A. Ogura, Y. Kanejima, T. Hidekuma, and K. P. Izawa. "Relationship
between compensated turnout and lower extremity injuries in ballet dancers: A
systematic review." Journal of Bodywork and Movement Therapies 47, 646–651
(2026).

DOI: https://doi.org/10.1016/j.jbmt.2026.05.006  
PubMed: https://pubmed.ncbi.nlm.nih.gov/42264850/

Role: newer systematic review in which three of four included studies reported
significant associations between compensated turnout and lower-extremity
injury, while emphasizing measurement variation and small samples; supports
COMPENSATED-EXPANSION as a research failure state, not a deterministic injury
rule.

### [P-SURGSmooth-2023] Aghazadeh et al.

F. Aghazadeh, B. Zheng, M. Tavakoli, and H. Rouhani. "Motion
Smoothness-Based Assessment of Surgical Expertise: The Importance of Selecting
Proper Metrics." Sensors 23(6), 3146 (2023).

DOI: https://doi.org/10.3390/s23063146  
PubMed: https://pubmed.ncbi.nlm.nih.gov/36991855/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10057623/

Role: primary simulated-surgery evidence that selected smoothness metrics,
including logarithmic dimensionless jerk and 95% motion frequency, can
differentiate skill levels; relevant to PRUNE / smoothness metrics.

### [P-FEEDBACKCTRL-2025] Feulner et al.

B. Feulner, M. G. Perich, L. E. Miller, C. Clopath, and J. A. Gallego.
"A neural implementation model of feedback-based motor learning." Nature
Communications 16, 1805 (2025).

DOI: https://doi.org/10.1038/s41467-024-54738-5  
PubMed: https://pubmed.ncbi.nlm.nih.gov/39979257/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC11842561/

Role: computational / neural-population modeling evidence that an adaptive
feedback controller can support both online correction and trial-by-trial motor
adaptation; used to motivate multiple timescales and policy-update hypotheses,
not as proof of a unique biological architecture.

### [R-UCM-2024] Latash

M. L. Latash. "Terra incognita of the uncontrolled manifold." Journal of
Neurophysiology 132(6), 1729–1743 (2024).

DOI: https://doi.org/10.1152/jn.00394.2024  
PubMed: https://pubmed.ncbi.nlm.nih.gov/39475487/

Role: current review of UCM / motor-abundance analysis; supports task-relative
variance decomposition while emphasizing unresolved mapping from measured
synergies to neural control variables.

### [R-AUGFB-2022] Petancevski et al.

E. L. Petancevski, J. Inns, J. Fransen, and F. M. Impellizzeri. "The effect
of augmented feedback on the performance and learning of gross motor and
sport-specific skills: A systematic review." Psychology of Sport and Exercise
63, 102277 (2022).

DOI: https://doi.org/10.1016/j.psychsport.2022.102277

Role: systematic review supporting augmented feedback as a potentially useful
motor-learning intervention while highlighting unresolved optimal frequency,
timing, duration, and limited negative / null evidence; motivates explicit
feedback-removal and dependency tests.

### [M-CI-RET-2024] Czyż et al.

S. H. Czyż, A. M. Wójcik, P. Solarská, and P. Kiper. "High contextual
interference improves retention in motor learning: systematic review and
meta-analysis." Scientific Reports 14, 15974 (2024).

DOI: https://doi.org/10.1038/s41598-024-65753-3  
PubMed: https://pubmed.ncbi.nlm.nih.gov/38987617/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC11237090/

Role: meta-analysis supporting an average retention benefit of high contextual
interference while showing strong heterogeneity, including much weaker effects
in applied settings; motivates separating random variation from representative
robustification.

### [M-CI-XFER-2024] Czyż, Wójcik, and Solarská

S. H. Czyż, A. M. Wójcik, and P. Solarská. "The effect of contextual
interference on transfer in motor learning - a systematic review and
meta-analysis." Frontiers in Psychology 15, 1377122 (2024).

DOI: https://doi.org/10.3389/fpsyg.2024.1377122  
PubMed: https://pubmed.ncbi.nlm.nih.gov/39205981/  
PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC11349744/

Role: meta-analysis of motor-learning transfer; supports explicit held-out
transfer measurement and cautions against treating laboratory acquisition gains
as general skill improvement.

