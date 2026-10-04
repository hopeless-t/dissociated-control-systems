import pytest

from dissociated_control_systems.meta_trial_sets import compare_trial_sets


BOGNAR_2024_OS = (
    "ZHANG_L_2021",
    "BAO_2019",
    "LU_2021",
    "KIRKEGAARD_2023",
    "TAKANO_2021",
    "GOODWIN_2001",
    "SPIEGEL_2007",
    "EDELMAN_1999",
    "GUO_Z_2013",
    "VANBUTSELE_2018",
    "KISSANE_2007",
    "WANG_J_2019",
    "KUCHLER_1999_2007",
    "KISSANE_2004",
)

ASAKAWA_HAAS_2026 = (
    "LINN_1982",
    "SPIEGEL_1989",
    "ILNYCKYJ_1994",
    "CUNNINGHAM_1998",
    "EDELMAN_1999",
    "MCCORKLE_2000",
    "GOODWIN_2001",
    "FAWZY_1993_2003",
    "KISSANE_2004",
    "BOESEN_2007",
    "KISSANE_2007",
    "KUCHLER_1999_2007",
    "SPIEGEL_2007",
    "ANDERSEN_2008",
    "BAKITAS_2009",
    "ROSS_2009",
    "TEMEL_2010",
    "CHOI_2012",
    "GUO_Z_2013",
    "ZHANG_XD_2013",
    "JULIAO_2015",
    "STAGL_2015",
    "YE_2017",
    "BAO_2019",
    "WANG_J_2019",
    "ZHANG_L_2021",
    "ZHAO_X_2021",
    "ZHOU_SUN_2021",
    "CHEN_L_2022",
    "GUO_Q_2022",
    "HUANG_2022",
    "KIRKEGAARD_2023",
)


def test_bognar_2024_vs_asakawa_haas_2026_trial_set_delta() -> None:
    result = compare_trial_sets(
        BOGNAR_2024_OS,
        ASAKAWA_HAAS_2026,
        left_label="bognar_2024",
        right_label="asakawa_haas_2026",
    )

    assert result.n_shared == 11
    assert result.n_left_only == 3
    assert result.n_right_only == 21
    assert result.left_only == {
        "LU_2021",
        "TAKANO_2021",
        "VANBUTSELE_2018",
    }
    assert result.jaccard == pytest.approx(11 / 35)


def test_duplicate_trial_identity_fails_closed_before_set_math() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        compare_trial_sets(["A", "A"], ["A", "B"])
