"""Run the frozen Bognar 2024 Figure 2 evidence-binding audit.

The input spec contains transcribed publication rows plus independently sourced
canonical comparator identities. This script classifies identity consistency
and constructs a trial-level count-binding graph. It does not infer why a
mismatch exists.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from dissociated_control_systems.binding_graph import binding_summary
from dissociated_control_systems.evidence_binding import (
    CanonicalEvidence,
    DisplayedEvidence,
    build_canonical_index,
    classify_binding,
)


def _canonical_record(evidence_id: str, payload: dict[str, object]) -> CanonicalEvidence:
    trial_id_raw = payload.get("trial_id", evidence_id)
    if not isinstance(trial_id_raw, str):
        raise ValueError(f"{evidence_id}: trial_id must be a string")

    count_i = payload.get("intervention_n")
    count_c = payload.get("control_n")
    hr = payload.get("hr")
    ci = payload.get("ci95")

    if count_i is not None and not isinstance(count_i, int):
        raise ValueError(f"{evidence_id}: intervention_n must be an integer or null")
    if count_c is not None and not isinstance(count_c, int):
        raise ValueError(f"{evidence_id}: control_n must be an integer or null")

    lower: float | None = None
    upper: float | None = None
    if hr is not None:
        if not isinstance(hr, (int, float)) or isinstance(hr, bool):
            raise ValueError(f"{evidence_id}: hr must be numeric or null")
        if not isinstance(ci, list) or len(ci) != 2:
            raise ValueError(f"{evidence_id}: ci95 required when hr is present")
        lower, upper = float(ci[0]), float(ci[1])

    return CanonicalEvidence(
        trial_id=trial_id_raw,
        intervention_n=count_i,
        control_n=count_c,
        hr=None if hr is None else float(hr),
        lower=lower,
        upper=upper,
        evidence_id=evidence_id,
    )


def run(spec_path: Path) -> dict[str, object]:
    payload = json.loads(spec_path.read_text(encoding="utf-8"))
    rows = payload.get("figure_rows")
    comparators = payload.get("canonical_comparators")
    if not isinstance(rows, list) or not rows:
        raise ValueError("figure_rows must be a non-empty list")
    if not isinstance(comparators, dict) or not comparators:
        raise ValueError("canonical_comparators must be a non-empty object")

    canonical = build_canonical_index(
        _canonical_record(evidence_id, value)
        for evidence_id, value in comparators.items()
        if isinstance(evidence_id, str) and isinstance(value, dict)
    )

    audits: list[dict[str, object]] = []
    count_edges: dict[str, str] = {}
    own_count_rows = 0
    cross_count_rows = 0
    unresolved_count_rows = 0
    ambiguous_count_rows = 0

    for raw in rows:
        if not isinstance(raw, dict):
            raise ValueError("figure row entries must be objects")
        ci = raw.get("ci95")
        if not isinstance(ci, list) or len(ci) != 2:
            raise ValueError("each figure row requires ci95=[lower, upper]")
        row = DisplayedEvidence(
            row_id=f"row-{int(raw['row']):02d}",
            displayed_trial_id=str(raw["label"]),
            intervention_n=int(raw["intervention_n"]),
            control_n=int(raw["control_n"]),
            hr=float(raw["hr"]),
            lower=float(ci[0]),
            upper=float(ci[1]),
        )
        result = classify_binding(row, canonical)
        audits.append(result)

        count_trial_ids = tuple(result["count_match_trial_ids"])
        if row.displayed_trial_id in count_trial_ids:
            own_count_rows += 1
        elif len(count_trial_ids) == 1:
            cross_count_rows += 1
            count_edges[row.displayed_trial_id] = count_trial_ids[0]
        elif len(count_trial_ids) == 0:
            unresolved_count_rows += 1
        else:
            ambiguous_count_rows += 1

    statuses = Counter(str(item["status"]) for item in audits)
    graph = binding_summary(count_edges)
    return {
        "spec_id": payload.get("id"),
        "source": payload.get("source"),
        "row_count": len(audits),
        "count_identity": {
            "own": own_count_rows,
            "cross_unique_trial": cross_count_rows,
            "ambiguous_multiple_trials": ambiguous_count_rows,
            "unresolved": unresolved_count_rows,
        },
        "binding_status_counts": dict(sorted(statuses.items())),
        "rows": audits,
        "unique_count_cross_binding_graph": graph,
        "claim_ceiling": (
            "descriptive provenance audit only; graph structure does not identify "
            "the mechanism that produced a mismatch"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "spec",
        type=Path,
        nargs="?",
        default=Path("specs/RQ-005-META-A-BOGNAR-FIG2-AUDIT.json"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run(args.spec)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
