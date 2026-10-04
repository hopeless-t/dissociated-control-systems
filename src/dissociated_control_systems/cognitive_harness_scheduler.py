"""CGD-SIM-006: diagnostic-window preserving repair scheduler.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from itertools import combinations
from statistics import fmean

from .cognitive_harness_repair import (
    ACTIVE_PRIORITY,
    FAULTS,
    REPAIR_FOR,
    HarnessState,
    active_detect,
    run_episode,
    train_active_thresholds,
)


def _legacy_recovery(
    fault_set: tuple[str, ...],
    seed: int,
    thresholds: dict[str, tuple[float, float]],
    *,
    max_cycles: int,
) -> tuple[set[str], int]:
    repairs: set[str] = set()
    state: HarnessState | None = None
    cycles = 0
    for cycle in range(max_cycles):
        episode = run_episode(
            frozenset(fault_set),
            seed + cycle * 10_000,
            steps=60,
            state=state,
            repairs=frozenset(repairs),
        )
        state = episode.state
        detected = active_detect(episode.features, thresholds)
        unresolved = [
            fault
            for fault in ACTIVE_PRIORITY
            if fault in detected and REPAIR_FOR[fault] not in repairs
        ]
        cycles += 1
        if not unresolved:
            break
        repairs.add(REPAIR_FOR[unresolved[0]])
    return repairs, cycles


def _evidence_preserving_recovery(
    fault_set: tuple[str, ...],
    seed: int,
    thresholds: dict[str, tuple[float, float]],
    *,
    max_cycles: int,
) -> tuple[set[str], int]:
    """Latch perishable L0 evidence while re-observing other components."""
    repairs: set[str] = set()
    state: HarnessState | None = None
    l0_evidence = False
    cycles = 0

    for cycle in range(max_cycles):
        episode = run_episode(
            frozenset(fault_set),
            seed + cycle * 10_000,
            steps=60,
            state=state,
            repairs=frozenset(repairs),
        )
        state = episode.state
        detected = active_detect(episode.features, thresholds)
        l0_evidence = l0_evidence or ("l0_decline" in detected)
        cycles += 1

        selected: str | None = None
        if (
            "observer_bias" in detected
            and REPAIR_FOR["observer_bias"] not in repairs
        ):
            selected = "observer_bias"
        elif (
            l0_evidence
            and REPAIR_FOR["l0_decline"] not in repairs
        ):
            selected = "l0_decline"
        elif (
            "l2_handoff" in detected
            and REPAIR_FOR["l2_handoff"] not in repairs
        ):
            selected = "l2_handoff"
        elif (
            "l1_calibration" in detected
            and REPAIR_FOR["l1_calibration"] not in repairs
        ):
            selected = "l1_calibration"

        if selected is None:
            break
        repairs.add(REPAIR_FOR[selected])

    return repairs, cycles


def _aggregate(
    *,
    fault_count: int,
    scheduler: str,
    samples: int,
) -> dict[str, float]:
    if fault_count not in (2, 3):
        raise ValueError("fault_count must be 2 or 3")
    if scheduler not in ("legacy", "evidence_preserving"):
        raise ValueError("unknown scheduler")

    thresholds = train_active_thresholds()
    coverage: list[float] = []
    extras: list[float] = []
    cycles: list[float] = []
    exact = 0
    total = 0

    combos = list(combinations(FAULTS[1:], fault_count))
    for combo_index, fault_set in enumerate(combos):
        required = {REPAIR_FOR[fault] for fault in fault_set}
        for sample in range(samples):
            seed = (
                7_000_000
                + fault_count * 1_000_000
                + combo_index * 100_000
                + sample
            )
            if scheduler == "legacy":
                repairs, used = _legacy_recovery(
                    fault_set,
                    seed,
                    thresholds,
                    max_cycles=fault_count + 3,
                )
            else:
                repairs, used = _evidence_preserving_recovery(
                    fault_set,
                    seed,
                    thresholds,
                    max_cycles=fault_count + 3,
                )

            coverage.append(len(repairs & required) / len(required))
            extras.append(len(repairs - required))
            cycles.append(used)
            exact += int(repairs == required)
            total += 1

    return {
        "mean_repair_coverage": fmean(coverage),
        "mean_extra_repairs": fmean(extras),
        "exact_recovery_rate": exact / total,
        "mean_cycles": fmean(cycles),
    }


def diagnostic_window_loss(samples: int = 500) -> float:
    """How often L0 evidence is visible early but gone after other repairs."""
    thresholds = train_active_thresholds()
    lost = 0
    eligible = 0

    fault_sets = (
        ("l0_decline", "l1_calibration", "l2_handoff"),
        ("l0_decline", "l1_calibration", "observer_bias"),
        ("l0_decline", "l2_handoff", "observer_bias"),
    )

    for combo_index, fault_set in enumerate(fault_sets):
        for sample in range(samples):
            seed = 9_000_000 + combo_index * 100_000 + sample
            state: HarnessState | None = None
            repairs: set[str] = set()

            first = run_episode(
                frozenset(fault_set),
                seed,
                steps=60,
                state=state,
                repairs=frozenset(repairs),
            )
            state = first.state
            first_detected = active_detect(first.features, thresholds)
            if "l0_decline" not in first_detected:
                continue
            eligible += 1

            episode = first
            for cycle, fault in enumerate(
                ("observer_bias", "l2_handoff", "l1_calibration"),
                start=1,
            ):
                if fault in fault_set:
                    repairs.add(REPAIR_FOR[fault])
                episode = run_episode(
                    frozenset(fault_set),
                    seed + cycle * 10_000,
                    steps=60,
                    state=state,
                    repairs=frozenset(repairs),
                )
                state = episode.state

            final_detected = active_detect(episode.features, thresholds)
            lost += int("l0_decline" not in final_detected)

    return 0.0 if eligible == 0 else lost / eligible


def run_scheduler_experiment(samples: int = 200) -> dict[str, object]:
    return {
        "legacy_pair": _aggregate(
            fault_count=2,
            scheduler="legacy",
            samples=samples,
        ),
        "preserving_pair": _aggregate(
            fault_count=2,
            scheduler="evidence_preserving",
            samples=samples,
        ),
        "legacy_triple": _aggregate(
            fault_count=3,
            scheduler="legacy",
            samples=samples,
        ),
        "preserving_triple": _aggregate(
            fault_count=3,
            scheduler="evidence_preserving",
            samples=samples,
        ),
        "l0_window_loss": diagnostic_window_loss(samples=samples),
    }


def format_markdown() -> str:
    result = run_scheduler_experiment()
    lines = [
        "# CGD-SIM-006 diagnostic-window preserving scheduler",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| faults | scheduler | repair coverage | extra repairs | exact recovery | mean cycles |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for key, label in (
        ("legacy_pair", "legacy"),
        ("preserving_pair", "evidence-preserving"),
        ("legacy_triple", "legacy"),
        ("preserving_triple", "evidence-preserving"),
    ):
        row = result[key]
        fault_label = "2" if "pair" in key else "3"
        lines.append(
            f"| {fault_label} | {label} | "
            f"{row['mean_repair_coverage']:.3f} | "
            f"{row['mean_extra_repairs']:.3f} | "
            f"{row['exact_recovery_rate']:.3f} | "
            f"{row['mean_cycles']:.3f} |"
        )

    lines.extend(
        [
            "",
            (
                "L0 diagnostic-window loss after deferring its repair: "
                f"{result['l0_window_loss']:.3f}"
            ),
            "",
            "Scheduler rule:",
            "",
            "m_L0(t+1) = m_L0(t) OR detected_L0(t)",
            "",
            "The latched evidence is consumed before later state saturation can "
            "erase the L0 signature. Other components remain re-observation-driven.",
            "",
            "Interpretation ceiling: this is a synthetic scheduling/observability "
            "result, not a clinical monitoring or treatment rule.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
