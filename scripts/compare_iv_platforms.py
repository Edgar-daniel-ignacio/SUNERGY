"""Audit original Windows versus Linux IV_R outputs; never create a numerical oracle."""

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/legacy/iv_r"


def differences(left: list[float], right: list[float]) -> dict[str, Any]:
    if len(left) != len(right):
        raise ValueError("Platform audit cannot drop or align records")
    absolute = [abs(b - a) for a, b in zip(left, right, strict=True)]
    relative = [abs(b - a) / abs(a) for a, b in zip(left, right, strict=True) if a != 0]
    return {
        "records": len(left),
        "unequal_records": sum(a != b for a, b in zip(left, right, strict=True)),
        "max_absolute": max(absolute),
        "max_relative_nonzero_reference": max(relative, default=0),
        "zero_reference_nonzero_candidate": sum(
            a == 0 and b != 0 for a, b in zip(left, right, strict=True)
        ),
    }


def scalar_differences(left: dict[str, float], right: dict[str, float]) -> dict[str, Any]:
    if left.keys() != right.keys():
        raise ValueError("Platform stage quantity names differ")
    return {name: differences([value], [right[name]]) for name, value in left.items()}


def audit() -> dict[str, Any]:
    pairs = []
    for windows, linux in (
        ("captured", "captured_linux"),
        ("captured_alternate", "captured_alternate_linux"),
    ):
        paths = [FIXTURES / name / "outputs.json" for name in (windows, linux)]
        left, right = [json.loads(path.read_text("utf-8")) for path in paths]
        if left["fit_inputs"] != right["fit_inputs"]:
            raise ValueError(
                "Effective source inputs differ; cannot attribute differences to platform"
            )
        if left["table"] != right["table"] or left["failures"] != right["failures"]:
            raise ValueError("Table/failure boundary differs between original platform runs")
        cases = []
        for a, b in zip(left["cases"], right["cases"], strict=True):
            if a["condition_id"] != b["condition_id"]:
                raise ValueError("Case IDs/order differ")
            cases.append(
                {
                    "condition_id": a["condition_id"],
                    "desoto_parameters": scalar_differences(
                        a["desoto_parameters"], b["desoto_parameters"]
                    ),
                    "singlediode": scalar_differences(a["singlediode"], b["singlediode"]),
                    **{
                        name: differences(a[name], b[name])
                        for name in ("voltage", "current", "reverse_voltage", "reverse_current")
                    },
                }
            )
        pairs.append(
            {
                "outputs": [
                    {
                        "path": p.relative_to(ROOT).as_posix(),
                        "sha256": sha256(p.read_bytes()).hexdigest(),
                    }
                    for p in paths
                ],
                "effective_fit_inputs_equal": True,
                "rounded_table_and_failures_equal": True,
                "fit_parameters": scalar_differences(
                    left["fit_parameters"], right["fit_parameters"]
                ),
                "cases": cases,
            }
        )
    return {
        "purpose": (
            "Original-source platform differences, not modern regression or scientific accuracy"
        ),
        "relative_error_note": (
            "Ratios near zero can be large; absolute floors remain essential. "
            "No tolerances changed."
        ),
        "producer": "scripts/compare_iv_platforms.py",
        "pairs": pairs,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    content = json.dumps(audit(), indent=2, allow_nan=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as output:
            output.write(content)
        print(f"Wrote original-source platform audit: {args.output}")
    else:
        print(content, end="")
