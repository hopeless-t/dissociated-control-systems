#!/usr/bin/env python3
"""Emit HF01 proof-protocol adversarial enumeration."""

from __future__ import annotations

import json

from dissociated_control_systems.projection_attack_surface import (
    full_attack_summary,
)


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "research_object": "HF-SIM-011",
                "scope": "synthetic-protocol-only",
                "reachability_empirical_attack_surface": full_attack_summary(),
                "claim": (
                    "Under the frozen four-role reachability protocol, exhaustive "
                    "subset, ordering, and status attacks each leave exactly one "
                    "accepted canonical configuration."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
