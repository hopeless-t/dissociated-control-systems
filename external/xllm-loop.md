# xLLM-Loop / fixed-point reference intake

Upstream:

- https://github.com/ifm-ai/xllm-loop
- https://www.alphaxiv.org/abs/2610.looped-models-fixed-points
- official paper PDF:
  https://github.com/ifm-ai/xllm-loop/blob/main/papers/part2.pdf

Reference state checked: 2026-10-03.

## Why DCS records it

The Part II work treats a looped model as a dynamical system whose recurrent
state may settle near a fixed point. The reusable research objects for DCS are:

- explicit recurrent state;
- fixed-point residual;
- contraction / perturbation decay;
- convergence depth;
- heterogeneous settling;
- input-conditioning geometry;
- endpoint-versus-trajectory sufficiency.

## Boundary

This is a formal / engineered-system reference. It is not neuroscience
evidence. No claim of shared biological mechanism is imported from the
upstream project.

The upstream repository is Apache-2.0 licensed. DCS does not vendor upstream
code in this intake; it implements only small independent mathematical
known-answer probes.
