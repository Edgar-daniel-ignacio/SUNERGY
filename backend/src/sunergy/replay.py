"""Offline IV_R reproduction gate over independently captured intermediate/final results."""

import json
import platform
from importlib.metadata import version
from pathlib import Path
from typing import Any

from sunergy.application import reproduce_legacy_iv
from sunergy.compatibility import LegacyIVResponse
from sunergy.fetcher import load_legacy_iv_input
from sunergy.regression import (
    CaptureManifest,
    ComparisonOutput,
    QuantitySeries,
    compare_outputs,
    verify_capture_artifacts,
)

UNITS = {
    "current": "A",
    "voltage": "V",
    "power": "W",
    "saturation_current": "A",
    "resistance": "ohm",
    "adjust": "percent",
}

PARAMETER_KINDS = {
    "I_L_ref": "current",
    "I_o_ref": "saturation_current",
    "R_s": "resistance",
    "R_sh_ref": "resistance",
    "a_ref": "voltage",
    "Adjust": "adjust",
    "photocurrent": "current",
    "saturation_current": "saturation_current",
    "resistance_series": "resistance",
    "resistance_shunt": "resistance",
    "nNsVth": "voltage",
    "i_sc": "current",
    "v_oc": "voltage",
    "i_mp": "current",
    "v_mp": "voltage",
    "p_mp": "power",
    "i_x": "current",
    "i_xx": "current",
}


def iv_capture_names(*, system: str | None = None, machine: str | None = None) -> tuple[str, str]:
    """Select by observed OS/architecture, never by numerical closeness or fallback."""
    system = platform.system() if system is None else system
    machine = platform.machine() if machine is None else machine
    if machine.lower() not in {"amd64", "x86_64"}:
        raise ValueError("No independent IV_R reference for this processor architecture")
    if system == "Windows":
        return "captured", "captured_alternate"
    if system == "Linux":
        return "captured_linux", "captured_alternate_linux"
    raise ValueError("No independent IV_R reference for this operating system")


def compare_iv_reference(
    reference: dict[str, Any],
    candidate: LegacyIVResponse,
    manifest: CaptureManifest,
) -> list[str]:
    problems: list[str] = []
    for kind, unit in UNITS.items():
        if manifest.tolerances[kind].unit != unit:
            problems.append(f"{kind}: tolerance units differ from model units {unit}")

    def scalars(stage: str, expected: dict[str, float], actual: dict[str, float]) -> None:
        if set(expected) != set(actual):
            problems.append(f"{stage}: quantity names differ")
            actual = {name: actual[name] for name in expected if name in actual}
        tolerances = {name: manifest.tolerances[PARAMETER_KINDS[name]] for name in expected}
        left = ComparisonOutput(
            identifiers=[stage],
            quantities={
                name: QuantitySeries(unit=tolerances[name].unit, values=[value])
                for name, value in expected.items()
            },
        )
        right = ComparisonOutput(
            identifiers=[stage],
            quantities={
                name: QuantitySeries(unit=UNITS[PARAMETER_KINDS[name]], values=[value])
                for name, value in actual.items()
            },
        )
        problems.extend(f"{stage}: {error}" for error in compare_outputs(left, right, tolerances))

    if reference["fit_inputs"] != candidate.fit_inputs:
        problems.append("fit inputs differ")
    scalars("fit", reference["fit_parameters"], candidate.fit_parameters)
    expected_ids = [case["condition_id"] for case in reference["cases"]]
    if expected_ids != [case.condition_id for case in candidate.cases]:
        problems.append("case identifiers/order/count differ")
    for index, (expected, actual) in enumerate(
        zip(reference["cases"], candidate.cases, strict=False)
    ):
        stage = f"case[{index}]/{expected['condition_id']}"
        # Exact source conditions/constants; fitted arguments use their quantity limits.
        fitted = set(
            manifest_name
            for manifest_name in PARAMETER_KINDS
            if manifest_name in expected["desoto_inputs"]
        )
        if {k: v for k, v in expected["desoto_inputs"].items() if k not in fitted} != {
            k: v for k, v in actual.desoto_inputs.items() if k not in fitted
        }:
            problems.append(f"{stage}: translation source inputs differ")
        scalars(
            f"{stage}/translation-fit-inputs",
            {k: v for k, v in expected["desoto_inputs"].items() if k in fitted},
            {k: v for k, v in actual.desoto_inputs.items() if k in fitted},
        )
        scalars(f"{stage}/desoto", expected["desoto_parameters"], actual.desoto_parameters)
        scalars(f"{stage}/metrics", expected["singlediode"], actual.singlediode)
        for name, values, kind in (
            ("voltage", actual.voltage_v, "voltage"),
            ("current", actual.current_a, "current"),
        ):
            tolerance = manifest.tolerances[kind]

            def series(
                data: list[float],
                *,
                quantity: str = name,
                unit: str = UNITS[kind],
            ) -> ComparisonOutput:
                return ComparisonOutput(
                    identifiers=[f"point-{i}" for i in range(len(data))],
                    quantities={quantity: QuantitySeries(unit=unit, values=data)},
                )

            problems.extend(
                f"{stage}/{name}: {error}"
                for error in compare_outputs(
                    series(expected[name]),
                    series(values),
                    {name: tolerance},
                )
            )
    if reference["table"]["columns"] != candidate.table_columns:
        problems.append("table columns/order differ")
    if reference["table"]["records"] != candidate.table_records:
        problems.append("legacy rounded table records/order differ")
    return problems


def replay_iv_capture(root: Path, manifest_path: Path) -> tuple[LegacyIVResponse, list[str]]:
    manifest = CaptureManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    verify_capture_artifacts(root, manifest)
    if not manifest.entrypoint.startswith("Input_File_DIV_Mac_Informe.IV_R (lines 4268-4368)"):
        raise ValueError("Capture entrypoint is not the selected IV_R branch")
    if manifest.model_solver_grid["model"] != "legacy-IV_R-v1 CEC/SAM fit -> De Soto -> Lambert W":
        raise ValueError("Capture model/solver identity differs")
    expected_family = "Windows" if iv_capture_names()[0] == "captured" else "Linux"
    if not manifest.platform.startswith(expected_family):
        raise ValueError("Capture platform differs from the replay platform")
    for package in ("pvlib", "nrel-pysam", "numpy", "pandas", "scipy"):
        if version(package) != manifest.dependencies[package]:
            raise ValueError(f"Replay dependency differs from capture: {package}")
    if len(manifest.inputs) != 1 or len(manifest.outputs) != 1:
        raise ValueError("IV_R replay requires exactly one input and output artifact")
    request = load_legacy_iv_input(
        root / manifest.inputs[0].path,
        expected_sha256=manifest.inputs[0].sha256,
        source_id=manifest.capture_id,
    )
    result = reproduce_legacy_iv(request)
    reference = json.loads((root / manifest.outputs[0].path).read_text(encoding="utf-8"))
    return result, compare_iv_reference(reference, result, manifest)
