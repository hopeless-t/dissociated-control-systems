import json
from pathlib import Path

from dissociated_control_systems.evidence_binding import (
    CanonicalEvidence,
    DisplayedEvidence,
    build_canonical_index,
    count_matches,
    cross_semantic_count_matches,
)


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((ROOT / "specs" / name).read_text(encoding="utf-8"))


def canonical_from_final_spec():
    spec = load_json("RQ-005-META-A-BOGNAR-FIG2-AUDIT.json")
    records = []
    for evidence_id, item in spec["canonical_comparators"].items():
        ci = item.get("ci95")
        records.append(
            CanonicalEvidence(
                trial_id=item.get("trial_id", evidence_id),
                intervention_n=item.get("intervention_n"),
                control_n=item.get("control_n"),
                hr=item.get("hr"),
                lower=None if ci is None else ci[0],
                upper=None if ci is None else ci[1],
                evidence_id=evidence_id,
                count_semantics=item.get("count_semantics", "population_size"),
            )
        )
    return build_canonical_index(records)


def displayed_count(row, *, label_key: str):
    return DisplayedEvidence(
        row_id=f"row-{row['row']:02d}",
        displayed_trial_id=row[label_key],
        intervention_n=row["intervention_n"],
        control_n=row["control_n"],
        hr=float(row.get("hr", 1.0)),
        lower=float(row.get("ci95", [0.5, 2.0])[0]),
        upper=float(row.get("ci95", [0.5, 2.0])[1]),
    )


def classify_population_counts(rows, *, label_key: str):
    canonical = canonical_from_final_spec()
    own = cross = unresolved = 0
    for raw in rows:
        row = displayed_count(raw, label_key=label_key)
        matches = count_matches(row, canonical)
        trial_ids = {canonical[evidence_id].trial_id for evidence_id in matches}
        if row.displayed_trial_id in trial_ids:
            own += 1
        elif len(trial_ids) == 1:
            cross += 1
        elif not trial_ids:
            unresolved += 1
        else:
            raise AssertionError("fixture unexpectedly has ambiguous trial count matches")
    return own, cross, unresolved


def test_preprint_population_counts_are_self_bound() -> None:
    preprint = load_json("RQ-005-META-A-BOGNAR-PREPRINT-SNAPSHOT.json")
    rows = preprint["figure_count_rows"]
    assert classify_population_counts(rows, label_key="trial_id") == (12, 0, 0)
    assert sum(row["intervention_n"] for row in rows) == 1224
    assert sum(row["control_n"] for row in rows) == 1070


def test_final_population_count_binding_regresses_after_revision() -> None:
    final = load_json("RQ-005-META-A-BOGNAR-FIG2-AUDIT.json")
    rows = final["figure_rows"]
    assert classify_population_counts(rows, label_key="label") == (2, 11, 1)
    assert sum(row["intervention_n"] for row in rows) == 1428
    assert sum(row["control_n"] for row in rows) == 1255


def test_count_pair_membership_changes_not_just_order() -> None:
    preprint = load_json("RQ-005-META-A-BOGNAR-PREPRINT-SNAPSHOT.json")
    final = load_json("RQ-005-META-A-BOGNAR-FIG2-AUDIT.json")
    pre_pairs = {
        (row["intervention_n"], row["control_n"])
        for row in preprint["figure_count_rows"]
    }
    final_pairs = {
        (row["intervention_n"], row["control_n"])
        for row in final["figure_rows"]
    }
    assert len(pre_pairs & final_pairs) == 9
    assert len(pre_pairs - final_pairs) == 3
    assert len(final_pairs - pre_pairs) == 5


def test_final_29_33_is_cross_semantic_not_population_identity() -> None:
    final = load_json("RQ-005-META-A-BOGNAR-FIG2-AUDIT.json")
    canonical = canonical_from_final_spec()
    raw = next(row for row in final["figure_rows"] if row["label"] == "EDELMAN_1999")
    row = displayed_count(raw, label_key="label")
    assert count_matches(row, canonical) == ()
    assert cross_semantic_count_matches(row, canonical) == (
        "ANDERSEN_2008_RECURRENCE_EVENTS",
    )
