"""CGD-SIM-053: orthogonal audit restores common-mode observability.

Synthetic failure-mode-diversity experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean

from .cognitive_context_authority_freshness import MAX_EPOCH_SELECTION_REGRET
from .cognitive_context_watchdog_common_mode import (
    COMMON_BIAS_BY_EPOCH,
    HARD_MAX_AUTHORITY_AGE,
    SIGMA_PRIMARY_CONTEXT,
    _epoch_evidence,
    common_mode_watchdog_attack,
)

AUDIT_PAIR_SAMPLES = 16
SIGMA_ORTHOGONAL_AUDIT = 0.015
AUDIT_CHANGE_THRESHOLD = 0.03


def _orthogonal_bias_estimate(epoch: int, common_bias: float) -> float:
    """Estimate primary-channel bias against an orthogonal, unshared channel."""

    rng = Random(5_900_000_000 + epoch * 100_000)
    differences = []
    for _ in range(AUDIT_PAIR_SAMPLES):
        primary = common_bias + rng.gauss(0.0, SIGMA_PRIMARY_CONTEXT)
        orthogonal = rng.gauss(0.0, SIGMA_ORTHOGONAL_AUDIT)
        differences.append(primary - orthogonal)
    return fmean(differences)


def _evaluate_orthogonal_audit(epochs):
    selected_policy = None
    qualification_reference = None
    last_qualification_epoch = None
    qualifications = 0
    audit_change_triggers = 0
    hard_expiry_triggers = 0
    rows = []

    for evidence in epochs:
        epoch = evidence["epoch"]
        estimate = _orthogonal_bias_estimate(epoch, evidence["common_bias"])
        audit_change = (
            qualification_reference is not None
            and abs(estimate - qualification_reference) >= AUDIT_CHANGE_THRESHOLD
        )
        hard_expiry = (
            last_qualification_epoch is not None
            and epoch - last_qualification_epoch >= HARD_MAX_AUTHORITY_AGE
        )
        qualification_due = selected_policy is None or audit_change or hard_expiry

        trigger_reason = "none"
        if qualification_due:
            if selected_policy is None:
                trigger_reason = "initial"
            elif audit_change:
                trigger_reason = "orthogonal_audit_change"
                audit_change_triggers += 1
            else:
                trigger_reason = "hard_expiry"
                hard_expiry_triggers += 1

            selected_policy = evidence["pilot_policy"]
            qualification_reference = estimate
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
                "epoch": epoch,
                "common_bias": evidence["common_bias"],
                "audit_bias_estimate": estimate,
                "trigger_reason": trigger_reason,
                "selected_policy": selected_policy,
                "oracle_policy": evidence["oracle_policy"],
                "selection_regret": regret,
                "stale_authority": selected_policy != evidence["oracle_policy"],
                "contract_violation": regret > MAX_EPOCH_SELECTION_REGRET,
            }
        )

    return {
        "rows": rows,
        "qualifications": qualifications,
        "audit_checks": len(rows),
        "audit_change_triggers": audit_change_triggers,
        "hard_expiry_triggers": hard_expiry_triggers,
        "mean_regret": fmean(row["selection_regret"] for row in rows),
        "max_regret": max(row["selection_regret"] for row in rows),
        "stale_authority_epochs": sum(row["stale_authority"] for row in rows),
        "contract_violation_epochs": sum(row["contract_violation"] for row in rows),
        "contract_pass": all(not row["contract_violation"] for row in rows),
    }


@lru_cache(maxsize=1)
def failure_mode_diversity_experiment():
    epochs = _epoch_evidence()
    pairwise = common_mode_watchdog_attack()["pairwise_watchdog"]
    orthogonal = _evaluate_orthogonal_audit(epochs)
    return {
        "epochs": epochs,
        "pairwise": pairwise,
        "orthogonal": orthogonal,
        "qualification_reduction_vs_epochly_gate": 1.0 - orthogonal["qualifications"] / len(epochs),
    }


def format_markdown() -> str:
    result = failure_mode_diversity_experiment()
    orthogonal = result["orthogonal"]
    pairwise = result["pairwise"]
    lines = [
        "# CGD-SIM-053 failure-mode diversity audit",
        "",
        "> Synthetic failure-mode-diversity experiment only. Clinical authority: NONE.",
        "",
        f"- orthogonal audit samples / epoch: {AUDIT_PAIR_SAMPLES}",
        f"- orthogonal audit noise std: {SIGMA_ORTHOGONAL_AUDIT:.3f}",
        f"- audit change threshold: {AUDIT_CHANGE_THRESHOLD:.2f}",
        f"- hard maximum authority age: {HARD_MAX_AUTHORITY_AGE} epochs",
        "- frozen common-mode bias trajectory: 0.00 -> +0.08 -> 0.00",
        f"- full qualification reduction vs every-epoch gate: {result['qualification_reduction_vs_epochly_gate']:.1%}",
        "",
        "The third channel is intentionally outside the primary/watchdog shared-bias",
        "family. It does not route evidence itself. It only estimates whether the",
        "primary context channel has moved relative to an orthogonal reference and",
        "can request a full qualification.",
        "",
        "~~~text",
        "primary context       = environment + B_common + eps_primary",
        "same-family watchdog  = environment + B_common + eps_watchdog",
        "orthogonal audit      = environment + eps_orthogonal",
        "",
        "primary - same-family watchdog -> B_common cancels",
        "primary - orthogonal audit     -> B_common remains observable",
        "~~~",
        "",
        "| epoch | common bias | orthogonal bias estimate | trigger | selected route | oracle route | regret | stale |",
        "| ---: | ---: | ---: | --- | --- | --- | ---: | --- |",
    ]

    for row in orthogonal["rows"]:
        lines.append(
            f"| {row['epoch']} | {row['common_bias']:.2f} | "
            f"{row['audit_bias_estimate']:.3f} | {row['trigger_reason']} | "
            f"{row['selected_policy']} | {row['oracle_policy']} | "
            f"{row['selection_regret']:.3f} | {row['stale_authority']} |"
        )

    lines.extend(
        [
            "",
            "Comparison:",
            "",
            f"- same-family pairwise watchdog: {pairwise['change_triggers']} change triggers, "
            f"{pairwise['stale_authority_epochs']} stale epochs, max regret {pairwise['max_regret']:.3f}",
            f"- orthogonal audit: {orthogonal['audit_change_triggers']} change triggers, "
            f"{orthogonal['stale_authority_epochs']} stale epochs, max regret {orthogonal['max_regret']:.3f}",
            f"- orthogonal full qualifications: {orthogonal['qualifications']} / {len(result['epochs'])}",
            f"- orthogonal hard-expiry triggers: {orthogonal['hard_expiry_triggers']}",
            f"- orthogonal regret contract pass: {orthogonal['contract_pass']}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Redundancy != Diversity",
            "N Channels != N Independent Failure Modes",
            "Agreement Is Strong Evidence Only Under Failure-Mode Independence",
            "Orthogonal Audit Can Recover Shared-Bias Observability",
            "Audit Has Revocation Authority, Not Routing Authority",
            "~~~",
            "",
            "The orthogonal audit is an idealized synthetic channel. A real source",
            "can still share hidden causes, calibration errors or environmental blind",
            "spots. This experiment demonstrates the value of failure-mode diversity,",
            "not the validity of any specific real monitoring modality.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
