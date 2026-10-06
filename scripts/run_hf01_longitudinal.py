#!/usr/bin/env python3
"""Emit the HF01 longitudinal synthetic known-answer result."""

from __future__ import annotations

import json

from dissociated_control_systems.hair_follicle_longitudinal import (
    canonical_longitudinal_probe,
)


def main() -> None:
    result = canonical_longitudinal_probe()
    payload = {
        "research_object": "HF-SIM-002",
        "scope": "synthetic-only",
        "matched_initial_visible_output": 0.50,
        "early_steps": 80,
        "late_steps": 2000,
        "arms": {
            name: {
                "early_regeneration_gain": round(
                    arm.early_regeneration_gain, 10
                ),
                "early_output_gain": round(arm.early_output_gain, 10),
                "late_output_gain": round(arm.late_output_gain, 10),
                "early_controlled_regeneration": round(
                    arm.early_controlled.regeneration, 10
                ),
                "early_controlled_output": round(
                    arm.early_controlled.hair_output, 10
                ),
                "late_controlled_output": round(
                    arm.late_controlled.hair_output, 10
                ),
            }
            for name, arm in result.items()
        },
        "claim": (
            "Inside the frozen synthetic model, early intervention-linked "
            "regeneration response separates later recoverability before the "
            "coarse output shows a comparable intervention benefit."
        ),
        "biological_authority": "NONE",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
