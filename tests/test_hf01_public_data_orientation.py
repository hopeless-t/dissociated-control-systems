import importlib.util
from pathlib import Path


def _load_script(name: str, filename: str):
    path = Path(__file__).parents[1] / "scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gse93766_cuffdiff_orientation_is_bald_minus_nonbald() -> None:
    module = _load_script("hf01_gse93766", "analyze_gse93766.py")
    text = (
        "test_id\tgene_id\tgene\tlocus\tsample_1\tsample_2\tstatus\t"
        "value_1\tvalue_2\tlog2(fold_change)\ttest_stat\tp_value\t"
        "q_value\tsignificant\n"
        "x\tx\tDKK1\tchr1\tBK0\tNBK0\tOK\t1\t4\t2.0\t0\t1\t1\tno\n"
    )
    effects, orientation = module.parse_diff(text)

    assert effects["DKK1"] == -2.0
    assert orientation["hf01_conversion"] == "negated to balding-minus-nonbalding"


def test_gse93766_reverse_order_keeps_bald_minus_nonbald() -> None:
    module = _load_script("hf01_gse93766_reverse", "analyze_gse93766.py")
    text = (
        "test_id\tgene_id\tgene\tlocus\tsample_1\tsample_2\tstatus\t"
        "value_1\tvalue_2\tlog2(fold_change)\ttest_stat\tp_value\t"
        "q_value\tsignificant\n"
        "x\tx\tDKK1\tchr1\tNBK0\tBK0\tOK\t1\t4\t2.0\t0\t1\t1\tno\n"
    )
    effects, orientation = module.parse_diff(text)

    assert effects["DKK1"] == 2.0
    assert orientation["hf01_conversion"] == "already balding-minus-nonbalding"
