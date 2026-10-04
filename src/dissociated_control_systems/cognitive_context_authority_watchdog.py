"""CGD-SIM-051: event-driven freshness watchdog for context authority.

Synthetic authority-watchdog experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

from .cognitive_context_authority_freshness import (
    CONTEXT_NOISE_BY_EPOCH,
    MAX_EPOCH_SELECTION_REGRET,
    context_authority_freshness_experiment,
)

WATCHDOG_PAIR_SAMPLES = 64
SIGMA_WATCHDOG = 0.01
WATCHDOG_DELTA_THRESHOLD = 0.03
HARD_MAX_AUTHORITY_AGE = 6


def _watchdog_statistic(epoch: int, sigma_context: float) -> float:
    """RMS disagreement between primary and independent context channels."""

    rng = Random(5_400_000_000 + epoch * 100_000)
    squared = []
    for _ in range(WATCHDOG_PAIR_SAMPLES):
        primary_noise = rng.gauss(0.0, sigma_context)
        watchdog_noise = rng.gauss(0.0, SIGMA_WATCHDOG)
        squared.append((primary_noise - watchdog_noise) ** 2)
    return sqrt(fmean(squared))


def _evaluate_watchdog(epochs):
    selected_policy = None
    last_qualification_epoch = None
    qualification_reference = None
    qualifications = 0
    change_triggers = 0
    hard_expiry_triggers = 0
    rows = []

    for evidence in epochs:
        epoch = evidence["epoch"]
        statistic = _watchdog_statistic(epoch, evidence["sigma_context"])

        change_trigger = (
            qualification_reference is not None
            and abs(statistic - qualification_reference) >= WATCHDOG_DELTA_THRESHOLD
        )
        hard_expiry = (
            last_qualification_epoch is not None
            and epoch - last_qualification_epoch >= HARD_MAX_AUTHORITY_AGE
        )
        qualification_due = selected_policy is None or change_trigger or hard_expiry

        trigger_reason = "none"
        if qualification_due:
            if selected_policy is None:
                trigger_reason = "initial"
            elif change_trigger:
                trigger_reason = "watchdog_change"
                change_triggers += 1
            else:
                trigger_reason = "hard_expiry"
                hard_expiry_triggers += 1

            selected_policy = evidence["pilot_policy"]
            last_qualification_epoch = epoch
            qualification_reference = statistic
            qualifications += 1

        heldout = evidence["heldout"]
        selected_auc = (
            heldout["normalized_auc"]
            if selected_policy == "context_normalized"
            else heldout["raw_auc"]
        )
        regret = evidence["best_auc"] - selected_auc
        rows.append(
            {
                "epoch": epoch,
                "sigma_context": evidence["sigma_context"],
                "watchdog_statistic": statistic,
                "qualification_due": qualification_due,
                "trigger_reason": trigger_reason,
                "selected_policy": selected_policy,
                "oracle_policy": evidence["oracle_policy"],
                "selection_regret": regret,
                "stale_authority": selected_policy != evidence["oracle_policy"],
                "contract_violation": regret > MAX_EPOCH_SELECTION_REGRET,
            }
        )

    return {
        "qualifications": qualifications,
        "watchdog_checks": len(rows),
        "change_triggers": change_triggers,
        "hard_expiry_triggers": hard_expiry_triggers,
        "mean_regret": fmean(row["selection_regret"] for row in rows),
        "max_regret": max(row["selection_regret"] for row in rows),
        "stale_authority_epochs": sum(row["stale_authority"] for row in rows),
        "contract_violation_epochs": sum(row["contract_violation"] for row in rows),
        "contract_pass": all(not row["contract_violation"] for row in rows),
        "rows": rows,
    }


@lru_cache(maxsize=1)
def context_authority_watchdog_experiment():
    freshness = context_authority_freshness_experiment()
    epochs = freshness["epochs"]
    watchdog = _evaluate_watchdog(epochs)
    lease1 = freshness["policies"]["lease1"]
    static_once = freshness["policies"]["static_once"]

    return {
        "epochs": epochs,
        "watchdog": watchdog,
        "lease1": lease1,
        "static_once": static_once,
        "qualification_reduction_vs_lease1": (
            1.0 - watchdog["qualifications"] / lease1["qualifications"]
        ),
    }


def format_markdown() -> str:
    result = context_authority_watchdog_experiment()
    watchdog = result["watchdog"]
    lines = [
        "# CGD-SIM-051 event-driven context-authority freshness watchdog",
        "",
        "> Synthetic authority-watchdog experiment only. Clinical authority: NONE.",
        "",
        f"- paired watchdog samples / epoch: {WATCHDOG_PAIR_SAMPLES}",
        f"- independent watchdog noise std: {SIGMA_WATCHDOG:.2f}",
        f"- watchdog delta threshold: {WATCHDOG_DELTA_THRESHOLD:.2f}",
        f"- hard maximum authority age: {HARD_MAX_AUTHORITY_AGE} epochs",
        f"- qualification reduction vs lease1: {result['qualification_reduction_vs_lease1']:.1%}",
        "",
        "The watchdog does not choose the evidence route. It can only revoke the",
        "current authority grant and request the full SIM-049 qualification gate.",
        "",
        "~~~text",
        "watchdog observation != authority decision",
        "watchdog trigger -> requalify -> authority gate decides route",
        "~~~",
        "",
        "| epoch | context noise | watchdog RMS disagreement | trigger | selected route | oracle route | regret | stale |",
        "| ---: | ---: | ---: | --- | --- | --- | ---: | --- |",
    ]

    for row in watchdog["rows"]:
        lines.append(
            f"| {row['epoch']} | {row['sigma_context']:.2f} | "
            f"{row['watchdog_statistic']:.3f} | {row['trigger_reason']} | "
            f"{row['selected_policy']} | {row['oracle_policy']} | "
            f"{row['selection_regret']:.3f} | {row['stale_authority']} |"
        )

    lines.extend(
        [
            "",
            "Summary:",
            "",
            f"- full qualifications: {watchdog['qualifications']} vs {result['lease1']['qualifications']} for lease1",
            f"- watchdog checks: {watchdog['watchdog_checks']}",
            f"- change-triggered qualifications: {watchdog['change_triggers']}",
            f"- hard-expiry qualifications: {watchdog['hard_expiry_triggers']}",
            f"- stale-authority epochs: {watchdog['stale_authority_epochs']}",
            f"- max selection regret: {watchdog['max_regret']:.3f}",
            f"- regret contract pass: {watchdog['contract_pass']}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Freshness Check != Full Requalification",
            "Cheap Independent Change Detection Can Revoke Stale Authority",
            "Watchdog Has Revocation Authority, Not Routing Authority",
            "No Trigger Forever Is Forbidden By Hard Expiry",
            "~~~",
            "",
            "All channel noises, sample counts, thresholds and epoch durations are",
            "synthetic. The independent watchdog is an idealized research channel,",
            "not a validated clinical, caregiver, sensor or home-monitoring method.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
