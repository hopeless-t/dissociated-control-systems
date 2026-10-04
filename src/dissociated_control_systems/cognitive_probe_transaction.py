"""CGD-SIM-030: durable probe transaction semantics.

Synthetic research control model only. Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Literal

Terminal = Literal["ACCEPTED", "DEFER", "INVALIDATED", "UNKNOWN"]


@dataclass(frozen=True)
class Scenario:
    name: str
    qualified: bool = True
    freshness_valid: bool = True
    state_invalidated_during_probe: bool = False
    measurement_missing: bool = False
    response_loss_after_dispatch: bool = False
    response_loss_after_commit: bool = False
    duplicate_delivery_attempts: int = 0
    true_diagnostic_positive: bool = True


@dataclass
class LedgerEntry:
    probe_operation_id: str
    status: str = "CREATED"
    attempt_ids: list[str] = field(default_factory=list)
    dispatch_count: int = 0
    stored_terminal: Terminal | None = None
    stored_result: bool | None = None


@dataclass(frozen=True)
class TransactionResult:
    scenario: str
    terminal: Terminal
    result: bool | None
    dispatch_count: int
    attempts: int
    duplicate_intervention: bool
    accepted_result_correct: bool | None


def _attempt_id(operation_id: str, index: int) -> str:
    return f"{operation_id}:attempt:{index}"


def run_transaction(scenario: Scenario) -> TransactionResult:
    operation_id = f"probe:{scenario.name}"
    ledger = LedgerEntry(probe_operation_id=operation_id)

    def new_attempt() -> None:
        ledger.attempt_ids.append(
            _attempt_id(operation_id, len(ledger.attempt_ids) + 1)
        )

    new_attempt()

    if not scenario.qualified:
        ledger.status = "DEFER"
        ledger.stored_terminal = "DEFER"
        return _finish(scenario, ledger)

    ledger.status = "ADMITTED"

    if not scenario.freshness_valid:
        ledger.status = "INVALIDATED"
        ledger.stored_terminal = "INVALIDATED"
        return _finish(scenario, ledger)

    ledger.status = "STATE_VERIFIED"
    ledger.dispatch_count += 1
    ledger.status = "DISPATCHED"

    if scenario.response_loss_after_dispatch:
        # Physical delivery may already have happened. No receipt exists, so the
        # only safe next action is durable re-observation, not a second dispatch.
        ledger.status = "UNKNOWN"
        ledger.stored_terminal = "UNKNOWN"
        for _ in range(scenario.duplicate_delivery_attempts):
            new_attempt()
            # Re-observe same operation only. No redispatch.
        return _finish(scenario, ledger)

    if scenario.state_invalidated_during_probe:
        ledger.status = "INVALIDATED"
        ledger.stored_terminal = "INVALIDATED"
        return _finish(scenario, ledger)

    if scenario.measurement_missing:
        ledger.status = "DEFER"
        ledger.stored_terminal = "DEFER"
        return _finish(scenario, ledger)

    ledger.status = "OBSERVED"
    ledger.stored_result = scenario.true_diagnostic_positive
    ledger.status = "ACCEPTED"
    ledger.stored_terminal = "ACCEPTED"

    if scenario.response_loss_after_commit:
        # Reconnect attempts see the same committed receipt.
        for _ in range(max(1, scenario.duplicate_delivery_attempts)):
            new_attempt()

    for _ in range(
        0 if scenario.response_loss_after_commit else scenario.duplicate_delivery_attempts
    ):
        new_attempt()

    return _finish(scenario, ledger)


def _finish(scenario: Scenario, ledger: LedgerEntry) -> TransactionResult:
    terminal = ledger.stored_terminal or "UNKNOWN"
    result = ledger.stored_result if terminal == "ACCEPTED" else None
    accepted_correct = (
        result == scenario.true_diagnostic_positive
        if terminal == "ACCEPTED"
        else None
    )
    return TransactionResult(
        scenario=scenario.name,
        terminal=terminal,
        result=result,
        dispatch_count=ledger.dispatch_count,
        attempts=len(ledger.attempt_ids),
        duplicate_intervention=ledger.dispatch_count > 1,
        accepted_result_correct=accepted_correct,
    )


def naive_dispatch_count(scenario: Scenario) -> int:
    """Baseline that confuses another physical attempt with retry authority."""
    if not scenario.qualified or not scenario.freshness_valid:
        return 0
    count = 1
    if scenario.response_loss_after_dispatch:
        count += scenario.duplicate_delivery_attempts
    return count


def scenarios() -> tuple[Scenario, ...]:
    return (
        Scenario(name="clean_positive", true_diagnostic_positive=True),
        Scenario(name="clean_negative", true_diagnostic_positive=False),
        Scenario(name="stale_before_probe", freshness_valid=False),
        Scenario(name="invalidated_mid_probe", state_invalidated_during_probe=True),
        Scenario(name="missing_measurement", measurement_missing=True),
        Scenario(
            name="lost_after_dispatch",
            response_loss_after_dispatch=True,
            duplicate_delivery_attempts=3,
        ),
        Scenario(
            name="lost_after_commit",
            response_loss_after_commit=True,
            duplicate_delivery_attempts=3,
            true_diagnostic_positive=True,
        ),
        Scenario(
            name="duplicate_delivery_clean",
            duplicate_delivery_attempts=4,
            true_diagnostic_positive=False,
        ),
        Scenario(name="unqualified_probe", qualified=False),
    )


@lru_cache(maxsize=1)
def transaction_experiment():
    rows = []
    accepted = 0
    accepted_correct = 0
    duplicate_interventions = 0
    naive_duplicate_interventions = 0

    for scenario in scenarios():
        result = run_transaction(scenario)
        naive_count = naive_dispatch_count(scenario)
        rows.append(
            {
                "scenario": result.scenario,
                "terminal": result.terminal,
                "result": result.result,
                "dispatch_count": result.dispatch_count,
                "attempts": result.attempts,
                "duplicate_intervention": result.duplicate_intervention,
                "naive_dispatch_count": naive_count,
            }
        )
        if result.terminal == "ACCEPTED":
            accepted += 1
            accepted_correct += int(result.accepted_result_correct is True)
        duplicate_interventions += int(result.duplicate_intervention)
        naive_duplicate_interventions += int(naive_count > 1)

    accepted_result_correctness = (
        accepted_correct / accepted if accepted else 1.0
    )

    return {
        "rows": rows,
        "accepted_count": accepted,
        "accepted_result_correctness": accepted_result_correctness,
        "duplicate_interventions": duplicate_interventions,
        "naive_duplicate_intervention_scenarios": naive_duplicate_interventions,
    }


def format_markdown() -> str:
    result = transaction_experiment()
    lines = [
        "# CGD-SIM-030 durable probe transaction",
        "",
        "> Synthetic research control model only. Clinical authority: NONE.",
        "",
        f"- accepted results: {result['accepted_count']}",
        (
            "- accepted-result correctness: "
            f"{result['accepted_result_correctness']:.3f}"
        ),
        (
            "- duplicate interventions under transaction contract: "
            f"{result['duplicate_interventions']}"
        ),
        (
            "- scenarios where naive retry would duplicate intervention: "
            f"{result['naive_duplicate_intervention_scenarios']}"
        ),
        "",
        "| scenario | terminal | diagnostic result | physical attempts | probe dispatches | naive dispatches | duplicate intervention |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['scenario']} | {row['terminal']} | {row['result']} | "
            f"{row['attempts']} | {row['dispatch_count']} | "
            f"{row['naive_dispatch_count']} | {row['duplicate_intervention']} |"
        )

    lines.extend(
        [
            "",
            "~~~text",
            "Probe Attempt != Probe Operation",
            "Re-observation != Re-intervention",
            "UNKNOWN != Retry Permission",
            "INVALIDATED != Diagnostic Negative",
            "Missing Measurement != Diagnostic Negative",
            "Response Loss After Commit != Lost Result",
            "~~~",
            "",
            "Transaction lifecycle:",
            "",
            "~~~text",
            "QUALIFY",
            "  -> ADMIT",
            "  -> VERIFY CURRENT STATE / FRESHNESS",
            "  -> DISPATCH ONCE",
            "  -> OBSERVE",
            "  -> ACCEPT / DEFER / INVALIDATE / UNKNOWN",
            "",
            "Only ACCEPTED carries a diagnostic result.",
            "~~~",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
