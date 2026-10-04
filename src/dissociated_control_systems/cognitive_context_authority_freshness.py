"""CGD-SIM-050: freshness lease for context-normalization authority.

Synthetic authority-freshness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from statistics import fmean

from .cognitive_context_authority_gate import _sample_auc, _select_authority

PILOT_SAMPLES = 8_000
HELDOUT_SAMPLES = 16_000
# Adversarial frozen trajectory: quality degrades immediately after initial
# qualification, remains poor for six epochs, then recovers.
CONTEXT_NOISE_BY_EPOCH = (0.01, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.01, 0.01, 0.01)
LEASES = {
    "static_once": None,
    "lease4": 4,
    "lease2": 2,
    "lease1": 1,
}
MAX_EPOCH_SELECTION_REGRET = 0.02


def _epoch_evidence():
    epochs = []
    for epoch, sigma_context in enumerate(CONTEXT_NOISE_BY_EPOCH):
        pilot = _sample_auc(
            PILOT_SAMPLES,
            5_200_000_000 + epoch * 100_000,
            sigma_context,
        )
        heldout = _sample_auc(
            HELDOUT_SAMPLES,
            5_300_000_000 + epoch * 100_000,
            sigma_context,
        )
        oracle_policy = (
            "context_normalized"
            if heldout["normalized_auc"] >= heldout["raw_auc"]
            else "raw_function"
        )
        epochs.append(
            {
                "epoch": epoch,
                "sigma_context": sigma_context,
                "pilot": pilot,
                "pilot_policy": _select_authority(pilot),
                "heldout": heldout,
                "oracle_policy": oracle_policy,
                "best_auc": max(heldout["raw_auc"], heldout["normalized_auc"]),
            }
        )
    return epochs


def _evaluate_lease(epochs, lease: int | None):
    selected_policy = None
    last_qualification_epoch = None
    qualifications = 0
    rows = []

    for evidence in epochs:
        epoch = evidence["epoch"]
        qualification_due = selected_policy is None
        if (
            lease is not None
            and last_qualification_epoch is not None
            and epoch - last_qualification_epoch >= lease
        ):
            qualification_due = True

        if qualification_due:
            selected_policy = evidence["pilot_policy"]
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
                "sigma_context": evidence["sigma_context"],
                "qualification_due": qualification_due,
                "selected_policy": selected_policy,
                "oracle_policy": evidence["oracle_policy"],
                "selected_auc": selected_auc,
                "best_auc": evidence["best_auc"],
                "selection_regret": regret,
                "stale_authority": selected_policy != evidence["oracle_policy"],
                "contract_violation": regret > MAX_EPOCH_SELECTION_REGRET,
            }
        )

    return {
        "qualifications": qualifications,
        "rows": rows,
        "mean_regret": fmean(row["selection_regret"] for row in rows),
        "max_regret": max(row["selection_regret"] for row in rows),
        "stale_authority_epochs": sum(row["stale_authority"] for row in rows),
        "contract_violation_epochs": sum(row["contract_violation"] for row in rows),
        "contract_pass": all(not row["contract_violation"] for row in rows),
    }


@lru_cache(maxsize=1)
def context_authority_freshness_experiment():
    epochs = _epoch_evidence()
    policies = {
        name: _evaluate_lease(epochs, lease)
        for name, lease in LEASES.items()
    }
    return {
        "epochs": epochs,
        "policies": policies,
    }


def format_markdown() -> str:
    result = context_authority_freshness_experiment()
    lines = [
        "# CGD-SIM-050 context-authority freshness lease",
        "",
        "> Synthetic authority-freshness experiment only. Clinical authority: NONE.",
        "",
        f"- pilot samples / epoch: {PILOT_SAMPLES}",
        f"- held-out samples / epoch: {HELDOUT_SAMPLES}",
        f"- max per-epoch selection-regret contract: <= {MAX_EPOCH_SELECTION_REGRET:.2f}",
        "- frozen context-noise trajectory: 0.01 -> 0.08 -> 0.01",
        "- degradation starts immediately after the initial qualification epoch",
        "",
        "The same SIM-049 pilot gate is reused. The only question is how long an",
        "already-granted normalization authority may remain valid without fresh",
        "qualification evidence.",
        "",
        "Epoch evidence:",
        "",
        "| epoch | context noise | pilot route | held-out raw AUC | held-out normalized AUC | held-out winner |",
        "| ---: | ---: | --- | ---: | ---: | --- |",
    ]

    for epoch in result["epochs"]:
        lines.append(
            f"| {epoch['epoch']} | {epoch['sigma_context']:.2f} | "
            f"{epoch['pilot_policy']} | "
            f"{epoch['heldout']['raw_auc']:.3f} | "
            f"{epoch['heldout']['normalized_auc']:.3f} | "
            f"{epoch['oracle_policy']} |"
        )

    lines.extend(
        [
            "",
            "Lease summary:",
            "",
            "| policy | qualifications | mean regret | max regret | stale-authority epochs | contract-violation epochs | contract |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for name in ("static_once", "lease4", "lease2", "lease1"):
        policy = result["policies"][name]
        lines.append(
            f"| {name} | {policy['qualifications']} | "
            f"{policy['mean_regret']:.3f} | {policy['max_regret']:.3f} | "
            f"{policy['stale_authority_epochs']} | "
            f"{policy['contract_violation_epochs']} | {policy['contract_pass']} |"
        )

    lines.extend(
        [
            "",
            "Key result:",
            "",
            "~~~text",
            "Qualified Once != Qualified Forever",
            "Authority Has Freshness",
            "Reliability Regime Change Can Invalidate A Previously Correct Route",
            "Expired Qualification -> Requalify Or Fail Back",
            "~~~",
            "",
            "The epoch duration, regime changes, lease lengths and regret contract are",
            "synthetic. This is an adversarial authority-lifetime test, not a real",
            "monitoring, reassessment or clinical scheduling recommendation.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
