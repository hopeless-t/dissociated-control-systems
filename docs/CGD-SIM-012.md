# CGD-SIM-012 — Temporal evidence frontier

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

CGD-SIM-011 left a small but non-zero classifier disagreement frontier.
Rather than add a deeper controller, this experiment adds genuinely new
trajectory evidence.

The old representation summarized each episode largely as a late-state or
whole-window statistic. The expanded representation adds:

~~~text
reference_drop_early
reference_drop_late
reference_drop_acceleration
self_reference_gap_trend
handoff_gap_trend
observer_disagreement_trend
feedback_error_trend
~~~

The base and temporal representations use the same train/validation/test
seeds, the same Gaussian + kNN classifier families, and the same ensemble
search. Therefore the measured delta isolates representation value more
cleanly than comparing across previous generations.

Declared local convergence:

~~~text
temporal ensemble gain < 0.005
and
temporal oracle-union gap < 0.010
~~~

If this fails because temporal evidence improves accuracy, the previous
frontier was information-starved. The self-improvement loop should then
optimize use of temporal evidence before considering any additional meta layer.

Synthetic research only; no clinical authority.
