"""CGD-SIM-024: causal-observability noise knee.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import exp, log, pi
from random import Random
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_intervention_probe import raw_probe

NOISE_LEVELS = (0.0025, 0.005, 0.010, 0.020, 0.040, 0.080)
CONFIDENCE = 0.99
MAX_REPEATS = 5
ACCURACY_TARGET = 0.90


def measured_probe(fault_set, target_fault, seed, noise_std):
    signal = raw_probe(fault_set, target_fault, seed)
    fault_index = FAULT_NAMES.index(target_fault) + 1
    noise_key = int(round(noise_std * 1_000_000))
    rng = Random(
        seed
        ^ (fault_index * 0x9E3779B1)
        ^ (noise_key * 0x85EBCA6B)
    )
    return signal + rng.gauss(0.0, noise_std)


def fit_models(noise_std, samples_per_hypothesis=40):
    models = {}
    for target_index, target_fault in enumerate(FAULT_NAMES):
        groups = {False: [], True: []}
        for hypothesis_index, fault_set in enumerate(hypotheses()):
            for sample in range(samples_per_hypothesis):
                value = measured_probe(
                    fault_set,
                    target_fault,
                    1_100_000_000
                    + target_index * 10_000_000
                    + hypothesis_index * 100_000
                    + sample,
                    noise_std,
                )
                groups[target_fault in fault_set].append(value)

        models[target_fault] = {}
        for present in (False, True):
            values = groups[present]
            mean = fmean(values)
            variance = fmean((x - mean) ** 2 for x in values) + 1e-7
            models[target_fault][present] = (mean, variance)
    return models


def _ll(value, mean, variance):
    return -0.5 * (
        ((value - mean) ** 2) / variance
        + log(2.0 * pi * variance)
    )


def _posterior(llr):
    if llr >= 0:
        return 1.0 / (1.0 + exp(-min(llr, 700.0)))
    e = exp(max(llr, -700.0))
    return e / (1.0 + e)


def classify_dimension(
    fault_set,
    target_fault,
    model,
    seed_base,
    noise_std,
    *,
    policy,
):
    llr = 0.0
    used = 0
    repeats = 1 if policy == "single" else MAX_REPEATS

    for repeat in range(repeats):
        value = measured_probe(
            fault_set,
            target_fault,
            seed_base + repeat * 1_000_000,
            noise_std,
        )
        absent_mean, absent_var = model[False]
        present_mean, present_var = model[True]
        llr += (
            _ll(value, present_mean, present_var)
            - _ll(value, absent_mean, absent_var)
        )
        used += 1

        if policy == "sequential":
            p = _posterior(llr)
            if p >= CONFIDENCE or p <= 1.0 - CONFIDENCE:
                break

    return _posterior(llr) >= 0.5, used


def evaluate_level(noise_std, *, samples_per_hypothesis=60):
    models = fit_models(noise_std)
    output = {}

    for policy in ("single", "sequential", "fixed_five"):
        exact = 0
        total = 0
        bit_correct = []
        total_probes = 0

        for hypothesis_index, fault_set in enumerate(hypotheses()):
            for sample in range(samples_per_hypothesis):
                predicted = set()
                for target_index, target_fault in enumerate(FAULT_NAMES):
                    prediction, used = classify_dimension(
                        fault_set,
                        target_fault,
                        models[target_fault],
                        1_200_000_000
                        + target_index * 100_000_000
                        + hypothesis_index * 1_000_000
                        + sample * 10,
                        noise_std,
                        policy=policy,
                    )
                    truth = target_fault in fault_set
                    bit_correct.append(float(prediction == truth))
                    total_probes += used
                    if prediction:
                        predicted.add(target_fault)

                exact += int(frozenset(predicted) == fault_set)
                total += 1

        output[policy] = {
            "exact_accuracy": exact / total,
            "macro_bit_accuracy": fmean(bit_correct),
            "mean_total_probes": total_probes / total,
        }

    return output


def first_failed_level(rows, policy):
    for row in rows:
        if row[policy]["exact_accuracy"] < ACCURACY_TARGET:
            return row["noise_std"]
    return None


@lru_cache(maxsize=1)
def noise_knee_experiment():
    rows = []
    for noise_std in NOISE_LEVELS:
        result = evaluate_level(noise_std)
        rows.append({"noise_std": noise_std, **result})

    single_knee = first_failed_level(rows, "single")
    sequential_knee = first_failed_level(rows, "sequential")
    fixed_knee = first_failed_level(rows, "fixed_five")

    return {
        "rows": rows,
        "single_knee": single_knee,
        "sequential_knee": sequential_knee,
        "fixed_five_knee": fixed_knee,
    }


def _fmt_knee(value):
    return "beyond grid" if value is None else f"{value:.4f}"


def format_markdown() -> str:
    result = noise_knee_experiment()
    lines = [
        "# CGD-SIM-024 causal-observability noise knee",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- sequential confidence: {CONFIDENCE:.2f}",
        f"- max repeats / dimension: {MAX_REPEATS}",
        f"- exact-state target: {ACCURACY_TARGET:.2f}",
        "",
        "| probe noise std | single exact | single probes | sequential exact | sequential probes | fixed-five exact | fixed-five probes |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['noise_std']:.4f} | "
            f"{row['single']['exact_accuracy']:.3f} | "
            f"{row['single']['mean_total_probes']:.3f} | "
            f"{row['sequential']['exact_accuracy']:.3f} | "
            f"{row['sequential']['mean_total_probes']:.3f} | "
            f"{row['fixed_five']['exact_accuracy']:.3f} | "
            f"{row['fixed_five']['mean_total_probes']:.3f} |"
        )

    lines.extend(
        [
            "",
            f"- single-probe knee (<0.90): {_fmt_knee(result['single_knee'])}",
            f"- sequential knee (<0.90): {_fmt_knee(result['sequential_knee'])}",
            f"- fixed-five knee (<0.90): {_fmt_knee(result['fixed_five_knee'])}",
            "",
            "Interpretation:",
            "",
            "~~~text",
            "measurement pressure increases",
            "    -> one-shot causal observability fails first",
            "    -> bounded repeated evidence can move the failure knee",
            "    -> eventually the information channel itself becomes insufficient",
            "~~~",
            "",
            "This is the causal-probe analogue of a pressure-knee experiment. "
            "It identifies where additional bounded evidence still buys reliability "
            "and where the probe channel itself must change.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
