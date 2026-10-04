"""CGD-SIM-052: common-mode failure attack on the context watchdog.

Synthetic watchdog-identifiability attack only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

from .cognitive_context_authority_gate import _auc, _select_authority
from .cognitive_context_authority_freshness import MAX_EPOCH_SELECTION_REGRET

PILOT_SAMPLES = 8_000
HELDOUT_SAMPLES = 16_000
PAIR_SAMPLES = 64
SIGMA_STATE_ERROR = 0.04
ENVIRONMENT_EVENT_PROBABILITY = 0.10
ENVIRONMENT_SHIFT = 0.12
SIGMA_FUNCTION = 0.02
SIGMA_PRIMARY_CONTEXT = 0.01
SIGMA_WATCHDOG = 0.01
WATCHDOG_DELTA_THRESHOLD = 0.03
HARD_MAX_AUTHORITY_AGE = 6
COMMON_BIAS_BY_EPOCH = (0.0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.0, 0.0, 0.0)


def _sample_route_auc(sample_count: int, seed: int, common_bias: float):
    rng = Random(seed)
    absolute_errors = []
    raw_scores = []
    normalized_scores = []

    for _ in range(sample_count):
        state_error = rng.gauss(0.0, SIGMA_STATE_ERROR)
        environment = 0.0
        if rng.random() < ENVIRONMENT_EVENT_PROBABILITY:
            environment = ENVIRONMENT_SHIFT * (
                1.0 if rng.random() < 0.5 else -1.0
            )
        function_noise = rng.gauss(0.0, SIGMA_FUNCTION)
        primary_noise = rng.gauss(0.0, SIGMA_PRIMARY_CONTEXT)

        absolute_errors.append(abs(state_error))
        raw_scores.append(abs(environment + function_noise - state_error))
        normalized_scores.append(
            abs(function_noise - common_bias - primary_noise - state_error)
        )

    cutoff = sorted(absolute_errors)[int(0.90 * sample_count)]
    labels = [int(value >= cutoff) for value in absolute_errors]
    return {
        "raw_auc": _auc(raw_scores, labels),
        "normalized_auc": _auc(normalized_scores, labels),
    }


def _watchdog_statistic(epoch: int, common_bias: float) -> float:
    """Pairwise disagreement; common bias cancels exactly by construction."""

    rng = Random(5_600_000_000 + epoch * 100_000)
    squared = []
    for _ in range(PAIR_SAMPLES):
        primary = common_bias + rng.gauss(0.0, SIGMA_PRIMARY_CONTEXT)
        watchdog = common_bias + rng.gauss(0.0, SIGMA_WATCHDOG)
        squared.append((primary - watchdog) ** 2)
    return sqrt(fmean(squared))


def _epoch_evidence():
    rows = []
    for epoch, common_bias in enumerate(COMMON_BIAS_BY_EPOCH):
        pilot = _sample_route_auc(
            PILOT_SAMPLES,
            5_700_000_000 + epoch * 100_000,
            common_bias,
        )
        heldout = _sample_route_auc(
            HELDOUT_SAMPLES,
            5_800_000_000 + epoch * 100_000,
            common_bias,
        )
        pilot_policy = _select_authority(pilot)
        oracle_policy = (
            "context_normalized"
            if heldout["normalized_auc"] >= heldout["raw_auc"]
            else "raw_function"
        )
        rows.append(
            {
                "epoch": epoch,
                "common_bias": common_bias,
                "pilot": pilot,
                "heldout": heldout,
                "pilot_policy": pilot_policy,
                "oracle_policy": oracle_policy,
                "best_auc": max(heldout["raw_auc"], heldout["normalized_auc"]),
                "watchdog_statistic": _watchdog_statistic(epoch, common_bias),
            }
        )
    return rows


def _evaluate_pairwise_watchdog(epochs):
    selected_policy = None
    qualification_reference = None
    last_qualification_epoch = None
    qualifications = 0
    change_triggers = 0
    hard_expiry_triggers = 0
    rows = []

    for evidence in epochs:
        epoch = evidence["epoch"]
        statistic = evidence["watchdog_statistic"]
        change_trigger = (
            qualification_reference is not None
            and abs(statistic - qualification_reference) >= WATCHDOG_DELTA_THRESHOLD
        )
        hard_expiry = (
            last_qualification_epoch is not None
            and epoch - last_qualification_epoch >= HARD_MAX_AUTHORITY_AGE
        )
        qualification_due = selected_policy is None or change_trigger or hard_expiry
        reason = "none"
        if qualification_due:
            if selected_policy is None:
                reason = "initial"
            elif change_trigger:
                reason = "watchdog_change"
                change_triggers += 1
            else:
                reason = "hard_expiry"
                hard_expiry_triggers += 1
            selected_policy = evidence["pilot_policy"]
            qualification_reference = statistic
            last_qualification_epoch = epoch
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
                **evidence,
                "trigger_reason": reason,
                "selected_policy": selected_policy,
                "selection_regret": regret,
                "stale_authority": selected_policy != evidence["oracle_policy"],
                "contract_violation": regret > MAX_EPOCH_SELECTION_REGRET,
            }
        )

    return {
        "rows": rows,
        "qualifications": qualifications,
        "change_triggers": change_triggers,
        "hard_expiry_triggers": hard_expiry_triggers,
        "mean_regret": fmean(row["selection_regret"] for row in rows),
        "max_regret": max(row["selection_regret"] for row in rows),
        "stale_authority_epochs": sum(row["stale_authority"] for row in rows),
        "contract_violation_epochs": sum(row["contract_violation"] for row in rows),
        "contract_pass": all(not row["contract_violation"] for row in rows),
    }


def _evaluate_lease1(epochs):
    rows = []
    for evidence in epochs:
        selected_policy = evidence["pilot_policy"]
        heldout = evidence["heldout"]
        selected_auc = (
            heldout["normalized_auc"]
            if selected_policy == "context_normalized"
            else heldout["raw_auc"]
        )
        regret = evidence["best_auc"] - selected_auc
        rows.append(
            {
                "selected_policy": selected_policy,
                "oracle_policy": evidence["oracle_policy"],
                "selection_regret": regret,
                "stale_authority": selected_policy != evidence["oracle_policy"],
            }
        )
    return {
        "qualifications": len(epochs),
        "max_regret": max(row["selection_regret"] for row in rows),
        "stale_authority_epochs": sum(row["stale_authority"] for row in rows),
    }


@lru_cache(maxsize=1)
def common_mode_watchdog_attack():
    epochs = _epoch_evidence()
    return {
        "epochs": epochs,
        "pairwise_watchdog": _evaluate_pairwise_watchdog(epochs),
        "lease1": _evaluate_lease1(epochs),
    }


def format_markdown() -> str:
    result = common_mode_watchdog_attack()
    watchdog = result["pairwise_watchdog"]
    lines = [
        "# CGD-SIM-052 common-mode watchdog failure",
        "",
        "> Synthetic watchdog-identifiability attack only. Clinical authority: NONE.",
        "",
        f"- paired samples / epoch: {PAIR_SAMPLES}",
        f"- primary context noise std: {SIGMA_PRIMARY_CONTEXT:.2f}",
        f"- watchdog noise std: {SIGMA_WATCHDOG:.2f}",
        f"- watchdog delta threshold: {WATCHDOG_DELTA_THRESHOLD:.2f}",
        f"- hard maximum authority age: {HARD_MAX_AUTHORITY_AGE} epochs",
        "- common-mode bias trajectory: 0.00 -> +0.08 -> 0.00",
        "",
        "Identifiability attack:",
        "",
        "~~~text",
        "primary  = environment + B_common + eps_primary",
        "watchdog = environment + B_common + eps_watchdog",
        "primary - watchdog = eps_primary - eps_watchdog",
        "",
        "therefore B_common is invisible to pairwise disagreement",
        "~~~",
        "",
        "| epoch | common bias | watchdog RMS | trigger | selected route | oracle route | raw AUC | normalized AUC | regret | stale |",
        "| ---: | ---: | ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in watchdog["rows"]:
        lines.append(
            f"| {row['epoch']} | {row['common_bias']:.2f} | "
            f"{row['watchdog_statistic']:.3f} | {row['trigger_reason']} | "
            f"{row['selected_policy']} | {row['oracle_policy']} | "
            f"{row['heldout']['raw_auc']:.3f} | {row['heldout']['normalized_auc']:.3f} | "
            f"{row['selection_regret']:.3f} | {row['stale_authority']} |"
        )

    lines.extend(
        [
            "",
            "Summary:",
            "",
            f"- pairwise watchdog full qualifications: {watchdog['qualifications']}",
            f"- change triggers: {watchdog['change_triggers']}",
            f"- hard-expiry triggers: {watchdog['hard_expiry_triggers']}",
            f"- stale-authority epochs: {watchdog['stale_authority_epochs']}",
            f"- max selection regret: {watchdog['max_regret']:.3f}",
            f"- regret contract pass: {watchdog['contract_pass']}",
            f"- lease1 stale-authority epochs: {result['lease1']['stale_authority_epochs']}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Primary And Watchdog Agreement != Joint Correctness",
            "Pairwise Disagreement Cannot Identify Shared Bias",
            "Redundancy Without Independence Can Manufacture False Confidence",
            "Hard Expiry Bounds Persistence But Does Not Detect The Failure",
            "~~~",
            "",
            "All biases, noises, thresholds and epoch durations are synthetic. This",
            "experiment demonstrates an observability limit, not a real monitoring",
            "failure rate or clinical recommendation.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
