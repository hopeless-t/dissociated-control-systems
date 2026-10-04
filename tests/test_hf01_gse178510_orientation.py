import importlib.util
from pathlib import Path


def _load_script():
    path = Path(__file__).parents[1] / "scripts" / "analyze_gse178510.py"
    spec = importlib.util.spec_from_file_location("hf01_gse178510", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gse178510_effect_is_minoxidil_minus_control_log2_signal() -> None:
    module = _load_script()
    text = (
        "CONTROL Bi-weight Avg Signal (log2)\t"
        "MINOXIDIL Bi-weight Avg Signal (log2)\t"
        "Fold Change (linear) (CONTROL vs. MINOXIDIL)\t"
        "Gene Symbol\n"
        "5.0\t6.0\t-2.0\tCTNNB1\n"
    )

    effects, meta = module.parse_gene_effects(text)

    # The ambiguous vendor fold-change field is deliberately ignored.
    assert effects["CTNNB1"] == 1.0
    assert "MINOXIDIL" in meta["effect_convention"]
    assert "CONTROL" in meta["effect_convention"]


def test_gse178510_down_response_has_negative_effect() -> None:
    module = _load_script()
    text = (
        "CONTROL Bi-weight Avg Signal (log2)\t"
        "MINOXIDIL Bi-weight Avg Signal (log2)\t"
        "Fold Change (linear) (CONTROL vs. MINOXIDIL)\t"
        "Gene Symbol\n"
        "7.5\t6.5\t2.0\tDKK1\n"
    )

    effects, _ = module.parse_gene_effects(text)

    assert effects["DKK1"] == -1.0
