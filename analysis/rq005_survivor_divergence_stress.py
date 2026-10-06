"""Fixed-seed noise stress for the RQ-005 synthetic precedence probe.

This is a method stress test, not patient data and not a clinical result.
"""

from __future__ import annotations

import json
import random

from dissociated_control_systems.survivor_divergence import (
    classify_precedence_pattern,
)


WORLDS = {
    "psych_neuroimmune_precedence_candidate": {
        "psychological": [0.0, 0.62, 0.72, 0.72, 0.72, 0.72],
        "neuroendocrine": [0.0, 0.10, 0.62, 0.72, 0.72, 0.72],
        "immune": [0.0, 0.10, 0.20, 0.62, 0.72, 0.72],
        "treatment": [0.0, 0.10, 0.10, 0.10, 0.10, 0.10],
        "tumor": [0.0, 0.10, 0.20, 0.30, 0.62, 0.72],
    },
    "tumor_first_reverse_causality_candidate": {
        "psychological": [0.0, 0.10, 0.10, 0.62, 0.72, 0.72],
        "neuroendocrine": [0.0, 0.10, 0.10, 0.62, 0.72, 0.72],
        "immune": [0.0, 0.10, 0.62, 0.72, 0.72, 0.72],
        "treatment": [0.0, 0.10, 0.10, 0.10, 0.10, 0.10],
        "tumor": [0.0, 0.62, 0.72, 0.72, 0.72, 0.72],
    },
    "treatment_first": {
        "psychological": [0.0, 0.10, 0.20, 0.30, 0.40, 0.40],
        "neuroendocrine": [0.0, 0.10, 0.20, 0.30, 0.40, 0.40],
        "immune": [0.0, 0.10, 0.20, 0.62, 0.72, 0.72],
        "treatment": [0.0, 0.62, 0.72, 0.72, 0.72, 0.72],
        "tumor": [0.0, 0.10, 0.20, 0.62, 0.72, 0.72],
    },
}


def run(
    *,
    noise_sd: float = 0.09,
    trials_per_world: int = 2000,
    seed: int = 14005,
    threshold: float = 0.5,
    persistence: int = 2,
) -> dict[str, object]:
    rng = random.Random(seed)
    per_world: dict[str, dict[str, float | int]] = {}

    for true_label, world in WORLDS.items():
        correct = 0
        ambiguous = 0
        for _ in range(trials_per_world):
            noisy = {
                layer: [
                    value + rng.gauss(0.0, noise_sd)
                    for value in series
                ]
                for layer, series in world.items()
            }
            predicted = classify_precedence_pattern(
                noisy,
                threshold=threshold,
                persistence=persistence,
            )
            correct += predicted == true_label
            ambiguous += predicted == "ambiguous"

        per_world[true_label] = {
            "trials": trials_per_world,
            "accuracy": correct / trials_per_world,
            "ambiguous_rate": ambiguous / trials_per_world,
        }

    return {
        "seed": seed,
        "noise_sd": noise_sd,
        "threshold": threshold,
        "persistence": persistence,
        "worlds": per_world,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
