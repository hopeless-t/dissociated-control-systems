# Formal Correspondence Candidate — DCS and Instrumented AI / Agent Systems

> Status: FORMAL CORRESPONDENCE CANDIDATE  
> Shared physical mechanism: NOT CLAIMED  
> Transfer authority: NONE

## Why this document exists

Several DCS hypotheses now have a mathematical shape that resembles problems
encountered in instrumented AI and agent harnesses.

The resemblance is useful only at the level of formal structure.

~~~text
Analogy != mechanism
Same equation != same substrate
Shared vocabulary != shared causality
~~~

## Common abstract loop

~~~text
input
 -> gated latent state update
 -> output
 -> observation / telemetry
 -> memory update
 -> policy / gain update
 -> next input trajectory
~~~

Biological DCS example:

~~~text
physical / social input
 -> somatic and affective state
 -> behavior / report / physiology
 -> self or partner observation
 -> memory / learning
 -> changed gain / future interaction
~~~

Agent-harness example:

~~~text
prompt / environment event
 -> model + context state
 -> action / response
 -> telemetry / evaluation
 -> persistent memory
 -> routing / policy / harness update
 -> next run
~~~

## Correspondence table

| DCS term | Agent / harness analogue | Boundary |
| --- | --- | --- |
| peripheral / environmental input | prompt, tool result, environment event | not the same physical signal |
| attention / expectation gain | routing, context emphasis, retrieval weighting | no claim of neural attention equivalence |
| latent body/control state | hidden agent/context/runtime state | different substrate and observability |
| expressed behavior | model output / tool action | different semantics |
| self-observation | agent reading its telemetry / state summary | biological self-model is not a log file |
| partner-held memory | external persistent memory / operator notes | human relationship memory has affective meaning |
| post-session review | post-run review | subjective content is not equivalent |
| feedback-respecting partner | adaptive controller / policy updater | consent and trust have no direct software equivalent |
| habituation | trajectory / cache / policy adaptation | analogy only |
| defensive knee | failure / defensive regime switch | no pain analogue implied |
| relationship gate | trust / authority / routing condition | social trust is not API authorization |
| observation re-entry | telemetry exposed back to agent | strongest formal overlap |

## Observation is not neutral

The shared control-theory problem is:

~~~text
measurement can modify trajectory
~~~

DCS examples include mirror self-observation, real-time video, explicit state
labeling, and perceived third-party observation.

Harness examples include exposing evaluator output to the model, showing
intermediate telemetry, repeated critique loops, and persistent memory updates.

Therefore:

~~~text
more observability != automatically better trajectory
~~~

## Reflective loop

~~~text
x_t -> y_t -> Encode(y_t) -> Reenter -> x_{t+1}
~~~

For humans, y_t may be a subjective or physiological observation.

For agents, y_t may be a trace, evaluator result, or structured telemetry.

Candidate general principle:

~~~text
A representation of a state can become a control input
when it is reintroduced into the system that produced it.
~~~

## External memory

HYP-006 adds a dyadic loop:

~~~text
person A experience
 -> person A report
 -> person B memory
 -> person B future policy
 -> person A next experience
~~~

Formal agent analogue:

~~~text
run
 -> evaluation
 -> persistent memory
 -> policy / harness update
 -> next run
~~~

The shared formal problem is credit assignment across time.

## Reward / evaluation distinction

Human pleasure and software reward/evaluation must not be collapsed.

A substrate-neutral abstraction can use:

~~~text
value signal
~~~

but human value may include pleasure, aversion, trust, relationship meaning,
pain, or social reward, while agent evaluation may include task score, verifier
output, preference model, explicit reward, or policy constraint.

The correspondence is:

~~~text
state-dependent value modifies future policy
~~~

not:

~~~text
human pleasure == model reward
~~~

## Context / relationship vs authority

Both domains can use conditions on a transfer function:

~~~text
effective_output = gate(state, input, context) * capability
~~~

But:

~~~text
human consent != software permission
human trust != authentication
~~~

The useful shared discipline is to keep capability, access, authority,
observation, memory, and trajectory state separate.

## Learning under co-occurrence

HYP-006 uses eligibility traces and associative updates:

~~~text
Delta W = eta * eligibility * prediction_error
~~~

Agent systems use different learning and memory mechanisms, but the formal
question is similar:

~~~text
which co-occurring event receives credit for a later value signal?
~~~

## State vectors instead of scalar labels

DCS rejects one scalar "sensitivity" variable.

Agent research similarly becomes brittle when one label such as capable, safe,
correct, stuck, or inactive hides multiple underlying conditions.

The correspondence is methodological:

~~~text
global labels can hide dissociated subsystem states
~~~

## Switching regimes

HYP-006 proposes:

~~~text
subthreshold
neutral
pleasant
erotic
defensive
habituated
~~~

An agent harness may also have:

~~~text
normal execution
uncertain
blocked
recovery
degraded
terminated
~~~

A shared method is:

~~~text
P(q_{t+1} | q_t, input_t, context_t, history_t)
~~~

The regime meanings remain domain-local.

## Harness lessons transferred into DCS

The strongest transfer is experimental discipline:

1. keep latent state separate from observable telemetry;
2. measure observer interference;
3. minimize instrumentation that destroys the trajectory being measured;
4. retain structured event history;
5. compare reference vs treatment;
6. search for knees / regime switches rather than assuming linearity;
7. capture rare states rather than averaging them away;
8. perform failure-state biopsy;
9. predict before observing the held-out run.

## DCS questions transferred back into agent research

DCS suggests questions such as:

- Does showing an agent its own telemetry change its trajectory?
- Can a coarse success/failure label hide different internal access states?
- Does persistent memory alter future gain or routing, not only content?
- Can evaluator identity or authority context change response while task input
  remains identical?
- Are some failures inactive-access states rather than missing capability?

These are research questions, not established transfers.

## Candidate synthetic validation

Freeze a synthetic system with:

~~~text
input
gain
latent state
observable
observer channel
memory
policy update
~~~

Run:

~~~text
A: telemetry hidden from controller
B: telemetry re-entered into controller
~~~

Hold external input constant.

Test:

~~~text
trajectory_A != trajectory_B
~~~

and whether a passive-observation model fails.

This validates only the formal machinery.

## Claim boundary

A successful cross-domain model would not show that human cognition is an LLM,
subjective pleasure is a reward token, partner communication is machine memory,
AI reasoning traces correspond to conscious thought, or the same causal
mechanism exists in brains and software.

The research value is:

> use a shared formal language while keeping domain mechanisms separate.
