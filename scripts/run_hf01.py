#!/usr/bin/env python3
"""Emit deterministic HF01 validation results as JSON."""

from __future__ import annotations

import json

from dissociated_control_systems.hair_follicle_model import (
    HFControl,
    canonical_early_state,
    canonical_late_state,
    recoverability_threshold,
    robustness_fraction,
    simulate,
)


def summary() -> dict[str, object]:
    early = canonical_early_state()
    late = canonical_late_state()

    arms = {
        "none": HFControl(),
        "behavioral": HFControl(behavioral=1.0),
        "antiandrogen": HFControl(antiandrogen=1.0),
        "behavioral_plus_antiandrogen": HFControl(
            behavioral=1.0, antiandrogen=1.0
        ),
        "plus_regenerative": HFControl(
            behavioral=1.0, antiandrogen=1.0, regenerative=1.0
        ),
        "plus_structural": HFControl(
            behavioral=1.0, antiandrogen=1.0, structural=1.0
        ),
        "all": HFControl(
            behavioral=1.0,
            antiandrogen=1.0,
            regenerative=1.0,
            structural=1.0,
        ),
    }

    early_outputs = {
        name: round(simulate(early, control).hair_output, 6)
        for name, control in arms.items()
    }
    late_outputs = {
        name: round(simulate(late, control).hair_output, 6)
        for name, control in arms.items()
    }

    thresholds = {
        "behavioral_plus_antiandrogen": recoverability_threshold(
            arms["behavioral_plus_antiandrogen"]
        ),
        "plus_regenerative": recoverability_threshold(arms["plus_regenerative"]),
        "plus_structural": recoverability_threshold(arms["plus_structural"]),
    }

    return {
        "research_object": "HF-VAL-001",
        "claim_scope": "synthetic-model-only",
        "early_final_hair_output": early_outputs,
        "late_final_hair_output": late_outputs,
        "recoverability_threshold_initial_structural_lock": thresholds,
        "robustness": {
            "samples": 300,
            "all_coefficient_perturbation": 0.20,
            "core_claim_fraction": round(
                robustness_fraction(samples=300, perturbation_fraction=0.20), 6
            ),
        },
    }


if __name__ == "__main__":
    print(json.dumps(summary(), indent=2, sort_keys=True))
