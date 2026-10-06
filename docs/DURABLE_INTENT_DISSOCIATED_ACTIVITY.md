# Durable intent vs active subsystem state

Status: cross-domain mathematical hypothesis only

Source intake: https://note.com/npaka/n/n341b20a052c6

## DCS connection

"Always-on AI" is a useful engineered-system example of the repository's central warning that a global label can hide dissociated subsystem states.

A system may be globally described as "active" while:

```text
objective persistence      ON
scheduler/event listener   ON
planner/model compute      OFF
large context residency    OFF
action capability          gated
verification               dormant until evidence arrives
```

Thus:

```text
Global Always-On Label != Uniform Subsystem Activity
Durable Intent != Active Cognition
Capability Available != Capability Exercised
Wake Trigger != Gate Open
```

## Synthetic model candidate

Extend a generic subsystem vector with:

```text
s = [intent_persistence, observation, planning, execution, verification]
```

Construct two systems that produce the same coarse observation "agent is available":

A. continuously active planner;
B. durable intent + sleeping planner + event-driven wake.

Then test which observations are required to distinguish the latent configurations and their resource costs.

This is intentionally an engineered-systems validation of partial observability. It does not transfer agent mechanisms into biological claims.

Candidate insight:

> **Persistence is itself a subsystem state, not evidence that every control subsystem is awake.**