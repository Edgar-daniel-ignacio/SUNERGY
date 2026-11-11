"""Capture unchanged Faiman/NOCT legacy functions without importing the legacy UI.

Run in the separately locked legacy environment. Selected original AST bodies
execute against real pandas/pvlib in a fresh subprocess and temporary CWD.
Synthetic point rows establish numerical compatibility, not annual/weather or
empirical validation. No modern SUNERGY code is imported by this runner.
"""

import argparse
import ast
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "legacy/Input_File_DIV_Mac_Informe.py"
LOCK = ROOT / "config/legacy-capture/requirements.txt"
FUNCTIONS = ("Temperature_feinman", "Temperature_NOCT")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path: Path, provenance: str) -> dict[str, str]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": digest(path),
        "provenance": provenance,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def selected_source() -> tuple[Any, dict[str, str]]:
    inventory = json.loads((ROOT / "docs/evidence/legacy_inventory.json").read_text("utf-8"))
    expected = next(
        row["sha256"]
        for row in inventory["files"]
        if row["path"] == SOURCE.relative_to(ROOT).as_posix()
    )
    if digest(SOURCE) != expected:
        raise RuntimeError("Frozen source differs from preservation inventory")
    text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(SOURCE))
    functions = [
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in FUNCTIONS
    ]
    if {node.name for node in functions} != set(FUNCTIONS):
        raise RuntimeError("Expected thermal function selection missing")
    hashes = {}
    for node in functions:
        segment = ast.get_source_segment(text, node)
        if segment is None:
            raise RuntimeError("Original function segment unavailable")
        hashes[node.name] = hashlib.sha256(segment.encode()).hexdigest()
    return compile(ast.Module(body=[*functions], type_ignores=[]), str(SOURCE), "exec"), hashes


def no_network(*args: Any, **kwargs: Any) -> Any:
    raise RuntimeError("Thermal legacy capture forbids network acquisition")


def execute(inputs: dict[str, Any]) -> dict[str, Any]:
    pd = importlib.import_module("pandas")
    pvlib = importlib.import_module("pvlib")
    namespace: dict[str, Any] = {"pvlib": pvlib}
    compiled, _ = selected_source()
    exec(compiled, namespace)
    results = []
    for case in inputs["cases"]:
        frame = pd.DataFrame(inputs["rows"], columns=inputs["row_columns"]).set_index("record_id")
        original = frame.copy(deep=True)
        ndh = {len(frame): [frame]}
        result = namespace[case["function"]](*case["arguments"], ndh)
        if result is not None or ndh[len(frame)][0] is not frame:
            raise RuntimeError("Unexpected legacy return/mutation identity")
        if not frame[original.columns].equals(original):
            raise RuntimeError("Legacy thermal function changed original input columns")
        if list(frame.columns) != [*original.columns, case["output_column"]]:
            raise RuntimeError("Unexpected legacy thermal output structure")
        try:
            missing = original.drop(columns=["Poa_global"])
            namespace[case["function"]](*case["arguments"], {len(missing): [missing]})
        except Exception as error:
            failure = {"exception_type": type(error).__name__, "message": str(error)}
        else:
            raise RuntimeError("Missing irradiance did not fail")
        results.append(
            {
                "case_id": case["case_id"],
                "profile_id": case["profile_id"],
                "identifiers": frame.index.tolist(),
                "columns": list(frame.columns),
                "records": frame.values.tolist(),
                "return": None,
                "mutation": (
                    "Original frame retained; original columns unchanged; output column appended"
                ),
                "missing_irradiance_failure": failure,
            }
        )
    return {"cases": results}


def worker(inputs: Path, output: Path) -> None:
    socket.socket.connect = no_network  # type: ignore[method-assign]
    socket.create_connection = no_network
    supplied = json.loads(inputs.read_text("utf-8"))
    result = execute(supplied)
    output_file = output / "outputs.json"
    write_json(output_file, result)
    _, hashes = selected_source()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    manifest = {
        "capture_id": "legacy-thermal-synthetic-v1",
        "captured_at": datetime.now(UTC).isoformat(),
        "source_revision": revision,
        "source_files": [
            artifact(SOURCE, "Unchanged source; checked against preservation inventory")
        ],
        "entrypoint": (
            "Input_File_DIV_Mac_Informe.Temperature_feinman:805-814 and "
            "Temperature_NOCT:817-825; original selected AST bodies"
        ),
        "python_version": platform.python_version(),
        "platform": f"{platform.platform()}; {platform.machine()}",
        "dependencies": {
            str(d.metadata["Name"]): d.version
            for d in sorted(
                importlib.metadata.distributions(), key=lambda d: str(d.metadata["Name"]).lower()
            )
        },
        "dependency_lock": artifact(
            LOCK, "Reconstructed isolated environment; historical versions unavailable"
        ),
        "inputs": [artifact(inputs, supplied["provenance"])],
        "outputs": [
            artifact(
                output_file,
                "Original legacy thermal functions independently executed before modern port",
            )
        ],
        "catalog_snapshot": None,
        "weather_snapshot": None,
        "measurement_snapshot": None,
        "units_and_coefficients": {
            "inputs": "Poa_global W/m2; temp_air degC; wind_speed m/s",
            "faiman": (
                "u0 W/(m2 degC); u1 W/(m2 degC (m/s)); real pvlib.faiman called with "
                "explicit U0/U1; UI values 25,6.84"
            ),
            "noct": (
                "TNMOT degC; TNOCT=Ta+((TNMOT-20)/800)*E; constants 20 degC,800 W/m2; UI "
                "value 43 degC"
            ),
            "outputs": (
                "TFeinman,NOCT degC; names preserve legacy labels, not measured cell temperature"
            ),
        },
        "time_convention": (
            "Ordered synthetic steady-state points; no timestamps, weather integration, "
            "timezone or DST"
        ),
        "model_solver_grid": {
            "model": "legacy-faiman-v1 and legacy-noct-v1; explicit supplied coefficients",
            "wrapper": artifact(
                Path(__file__).resolve(),
                "Inspectable AST selection; no numerical edits or modern imports",
            ),
            "function_source_sha256": hashes,
            "isolation": (
                "Fresh subprocess/temporary CWD; socket connect blocked; full legacy "
                "module not imported"
            ),
            "mutation": (
                "Legacy returns None and appends output to original frame; modern "
                "numerical boundary returns ordered values without mutation"
            ),
            "repeated_calculation": (
                "Each original function repeats calculation for all four sizes without "
                "checking length; preserved capture executes original loops"
            ),
            "excluded": (
                "Sandia not ported: len gate requires 8760/17520/35040/105120 and "
                "selectors 5/6 lack deltaT entries; capture each regime/failure before "
                "port. No annual wrapper, weather acquisition, thermal calibration or "
                "measured cell-temperature claim."
            ),
        },
        "random_seed": None,
        "randomness_notes": "No stochastic operations in selected functions",
        "capture_method": (
            "scripts/capture_legacy_thermal.py --inputs "
            "tests/fixtures/legacy/thermal/inputs.json --output "
            "tests/fixtures/legacy/thermal/captured"
        ),
        "tolerances": {
            "temperature": {
                "unit": "degC",
                "absolute": 1e-12,
                "relative": 1e-12,
                "rationale": (
                    "Double precision scalar arithmetic; 1e-12 degC floor and relative "
                    "scale allow last-bit evaluation differences at these synthetic point "
                    "conditions; no measurement accuracy claim"
                ),
            }
        },
        "review_status": (
            "Independently captured original kernels; representative synthetic conditions "
            "only; historical environment, cross-platform and empirical validation "
            "unavailable"
        ),
    }
    write_json(output / "manifest.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inputs", type=Path, default=ROOT / "tests/fixtures/legacy/thermal/inputs.json"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        parser.error("Output must be a new directory within the checkout")
    if args.worker:
        worker(args.inputs.resolve(), output)
        return
    output.mkdir(parents=True, exist_ok=False)
    copied = output / "inputs.json"
    shutil.copyfile(args.inputs.resolve(), copied)
    run_root = ROOT / ".local/runs"
    run_root.mkdir(parents=True, exist_ok=True)
    environment = {
        name: value
        for name, value in os.environ.items()
        if not any(marker in name.upper() for marker in ("TOKEN", "SECRET", "API_KEY", "PASSWORD"))
    }
    with tempfile.TemporaryDirectory(prefix="legacy-thermal-", dir=run_root) as cwd:
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker",
                "--inputs",
                str(copied),
                "--output",
                str(output),
            ],
            cwd=cwd,
            env=environment,
            check=True,
        )
    print(f"Captured original thermal kernels to {output.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
