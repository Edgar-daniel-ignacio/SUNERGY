"""Execute the unchanged legacy IV_R function in an isolated offline subprocess.

This tool never imports SUNERGY's modern implementation. AST selection avoids
unrelated Dash imports, CSV deletion and upload handling in the frozen helper.
Real pvlib and Plotly execute the selected body; transparent wrappers record
pvlib calls without modifying arguments, results, grids or arithmetic.
"""

from __future__ import annotations

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
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "legacy/Input_File_DIV_Mac_Informe.py"
LOCK = ROOT / "config/legacy-capture/requirements.txt"
FIT_NAMES = ("I_L_ref", "I_o_ref", "R_s", "R_sh_ref", "a_ref", "Adjust")
DESOTO_NAMES = (
    "photocurrent",
    "saturation_current",
    "resistance_series",
    "resistance_shunt",
    "nNsVth",
)
DISTRIBUTIONS = (
    "pvlib",
    "nrel-pysam",
    "numpy",
    "pandas",
    "scipy",
    "plotly",
    "h5py",
    "certifi",
    "charset-normalizer",
    "idna",
    "narwhals",
    "packaging",
    "python-dateutil",
    "pytz",
    "requests",
    "tzdata",
    "urllib3",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path: Path, provenance: str) -> dict[str, str]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
        "provenance": provenance,
    }


def serializable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    if hasattr(value, "tolist"):
        return serializable(value.tolist())
    return value


def write_json(path: Path, value: Any) -> None:
    # JSON forbids unlabelled NaN/Infinity; failures must be diagnosed, not hidden.
    path.write_text(
        json.dumps(serializable(value), indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def extract_function() -> tuple[Any, str]:
    """Compile only the original function AST, leaving its operations untouched."""
    inventory = json.loads((ROOT / "docs/evidence/legacy_inventory.json").read_text("utf-8"))
    expected = next(
        row["sha256"]
        for row in inventory["files"]
        if row["path"] == SOURCE.relative_to(ROOT).as_posix()
    )
    if sha256(SOURCE) != expected:
        raise RuntimeError("Frozen legacy source differs from the preservation inventory")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    function = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "IV_R"
    )
    selected = ast.Module(body=[function], type_ignores=[])
    function_text = ast.get_source_segment(source_text, function)
    assert function_text is not None
    return compile(selected, str(SOURCE), "exec"), hashlib.sha256(
        function_text.encode("utf-8")
    ).hexdigest()


def block_network(*args: Any, **kwargs: Any) -> Any:
    raise RuntimeError("Legacy capture forbids live network acquisition")


def execute(inputs: dict[str, Any]) -> dict[str, Any]:
    """Run selected original code with real scientific dependencies and Plotly."""
    np = importlib.import_module("numpy")
    pd = importlib.import_module("pandas")
    pvlib = importlib.import_module("pvlib")
    go = importlib.import_module("plotly.graph_objects")
    compiled, _ = extract_function()
    calls: dict[str, list[dict[str, Any]]] = {}

    def traced(name: str, target: Callable[..., Any]) -> Callable[..., Any]:
        def call(*args: Any, **kwargs: Any) -> Any:
            result = target(*args, **kwargs)
            calls.setdefault(name, []).append(
                {"inputs": serializable(kwargs), "output": serializable(result)}
            )
            return result

        return call

    pvlib_proxy = SimpleNamespace(
        ivtools=SimpleNamespace(
            sdm=SimpleNamespace(fit_cec_sam=traced("fit", pvlib.ivtools.sdm.fit_cec_sam))
        ),
        pvsystem=SimpleNamespace(
            **{
                name: traced(name, getattr(pvlib.pvsystem, name))
                for name in ("calcparams_desoto", "singlediode", "i_from_v", "v_from_i")
            }
        ),
    )
    namespace: dict[str, Any] = {"pvlib": pvlib_proxy, "np": np, "pd": pd, "go": go}
    exec(compiled, namespace)
    frame = pd.DataFrame(inputs["conditions"], columns=inputs["condition_columns"])
    module = dict(inputs["module"])
    before_frame = frame.copy(deep=True)
    before_module = dict(module)
    figure, table = namespace["IV_R"](module, frame)
    if module != before_module or not frame.equals(before_frame):
        raise RuntimeError("Selected legacy execution mutated inputs")
    cases = []
    for index, row in enumerate(inputs["conditions"]):
        desoto = calls["calcparams_desoto"][index]
        iv_call = calls["i_from_v"][index]
        reverse = calls["v_from_i"][index]
        trace = figure.data[index * 2]
        if (
            serializable(trace.x) != iv_call["inputs"]["voltage"]
            or serializable(trace.y) != iv_call["output"]
        ):
            raise RuntimeError("Recorded curve disagrees with original Plotly trace")
        cases.append(
            {
                "condition_id": row[0],
                "desoto_inputs": desoto["inputs"],
                "desoto_parameters": dict(zip(DESOTO_NAMES, desoto["output"], strict=True)),
                "singlediode": calls["singlediode"][index]["output"],
                "voltage": serializable(trace.x),
                "current": serializable(trace.y),
                "reverse_current": reverse["inputs"]["current"],
                "reverse_voltage": reverse["output"],
            }
        )
    # Original rounded table is captured as returned; raw numerical stages above
    # are unrounded. The constructed comparison values are not measurements.
    result = {
        "fit_inputs": calls["fit"][0]["inputs"],
        "fit_parameters": dict(zip(FIT_NAMES, calls["fit"][0]["output"], strict=True)),
        "cases": cases,
        "table": {"columns": list(table.columns), "records": table.values.tolist()},
        "failures": [],
    }
    for failure in inputs.get("failure_cases", []):
        try:
            namespace["IV_R"](module, frame.drop(columns=[failure["drop_column"]]))
        except Exception as error:
            result["failures"].append(
                {"id": failure["id"], "exception_type": type(error).__name__, "message": str(error)}
            )
        else:
            raise RuntimeError(f"Expected failure did not occur: {failure['id']}")
    return result


def worker(inputs_path: Path, output: Path) -> None:
    # Imports initialize only scientific libraries; selected source never performs
    # I/O. Block Python networking before executing its original function body.
    socket.socket.connect = block_network  # type: ignore[method-assign]
    socket.create_connection = block_network
    inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
    result = execute(inputs)
    output_file = output / "outputs.json"
    write_json(output_file, result)
    _, function_hash = extract_function()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    tolerances = {
        "current": {
            "unit": "A",
            "absolute": 1e-9,
            "relative": 1e-9,
            "rationale": (
                "Double-precision same-version deterministic replay; near-zero "
                "floor is 1 nA. Independent recapture is exact on capture host; "
                "cross-platform limits need CI evidence."
            ),
        },
        "voltage": {
            "unit": "V",
            "absolute": 1e-8,
            "relative": 1e-9,
            "rationale": (
                "Double-precision same-version deterministic replay including "
                "Lambert W/Newton internal solves; 10 nV near-zero floor. "
                "Cross-platform limits need CI evidence."
            ),
        },
        "power": {
            "unit": "W",
            "absolute": 1e-7,
            "relative": 1e-9,
            "rationale": (
                "Product of current and voltage, propagating the selected A/V "
                "floors at the selected 250/400 W module scales; no accuracy claim."
            ),
        },
        "saturation_current": {
            "unit": "A",
            "absolute": 1e-20,
            "relative": 1e-9,
            "rationale": (
                "Dark currents are near 1e-10 A in these captures; a 1e-20 A floor "
                "retains sensitivity to relative changes. Same-host replay is exact; "
                "cross-platform limits need CI evidence."
            ),
        },
        "resistance": {
            "unit": "ohm",
            "absolute": 1e-9,
            "relative": 1e-9,
            "rationale": "Same pinned deterministic fit and algebraic rescaling; 1 nano-ohm floor. "
            "Cross-platform limits need CI evidence.",
        },
        "adjust": {
            "unit": "percent",
            "absolute": 1e-9,
            "relative": 1e-9,
            "rationale": "Same pinned SSC deterministic fit; 1e-9 percentage-point floor. "
            "Adjust is captured despite legacy leaving it unused; cross-platform review pending.",
        },
    }
    manifest = {
        "capture_id": inputs.get("capture_id", "legacy-iv-r-manual-v1"),
        "captured_at": datetime.now(UTC).isoformat(),
        "source_revision": revision,
        "source_files": [
            artifact(
                SOURCE, "Unchanged preserved helper; hash checked against legacy_inventory.json"
            )
        ],
        "entrypoint": (
            "Input_File_DIV_Mac_Informe.IV_R (lines 4268-4368), selected original function AST"
        ),
        "python_version": platform.python_version(),
        "platform": platform.platform() + "; " + platform.machine(),
        "dependencies": {name: importlib.metadata.version(name) for name in DISTRIBUTIONS},
        "dependency_lock": artifact(
            LOCK, "Pinned reconstructed capture environment; historical environment unavailable"
        ),
        "inputs": [artifact(inputs_path, inputs["provenance"])],
        "outputs": [
            artifact(
                output_file,
                ("Independently executed original IV_R; no SUNERGY runtime imported"),
            )
        ],
        "catalog_snapshot": None,
        "weather_snapshot": None,
        "measurement_snapshot": None,
        "units_and_coefficients": {
            "module": (
                "Vmax60,Voc: V; Imax,Isc: A; Pmax: W; alpha,beta,deltha: "
                "percent/degC; cells_in_series: count; temp_ref: degC"
            ),
            "condition": (
                "Geff: effective irradiance W/m2; Tcell: cell temperature degC; "
                "Isc,Im: A; Voc,Vm: V; Potencia: W"
            ),
            "fit": (
                "alpha_sc=(alpha/100)*Isc A/degC; beta_voc=(beta/100)*Voc "
                "V/degC; gamma_pmp=deltha percent/degC; forced monoSi and 25 "
                "degC"
            ),
            "desoto": (
                "alpha_sc is raw module alpha, interpreted by pvlib as A/degC "
                "(legacy inconsistency preserved); EgRef=1.121 "
                "eV,dEgdT=-0.0002677 1/K; default irrad_ref=1000 "
                "W/m2,temp_ref=25 degC"
            ),
            "fit_parameters": (
                "I_L_ref,I_o_ref: A; R_s,R_sh_ref: ohm; a_ref: V; Adjust: percent (unused by IV_R)"
            ),
            "desoto_parameters": (
                "photocurrent,saturation_current: A; "
                "resistance_series,resistance_shunt: ohm; nNsVth: V"
            ),
            "curves": (
                "voltage,reverse_voltage: V; current,reverse_current: A; "
                "singlediode i_sc,i_mp,i_x,i_xx: A; v_oc,v_mp: V;p_mp: W"
            ),
            "table": (
                "First five error columns are percentage rounded to 2 decimals; "
                "Irradiancia W/m2 and T_cell degC rounded to 2 decimals by "
                "legacy code"
            ),
        },
        "time_convention": (
            "No time series or location: explicit ordered steady-state G/T "
            "points; no timezone, interval, DST or annual integration"
        ),
        "model_solver_grid": {
            "model": "legacy-IV_R-v1 CEC/SAM fit -> De Soto -> Lambert W",
            "grid": (
                "np.linspace(0,v_oc,100), endpoint=True; ordered current "
                "calculated at every voltage; no resampling"
            ),
            "unused_reverse_grid": (
                "np.linspace(15.948434,0,100) and v_from_i(method='lambertw'); "
                "retained as evidence though not returned by original function"
            ),
            "solver_settings": (
                "pvlib0.13.1 defaults, no additional tolerance supplied; "
                "PySAM7.1.0 SSC SixParsolve defaults"
            ),
            "wrapper": artifact(
                Path(__file__).resolve(),
                (
                    "Inspectable AST selection and transparent real-library call"
                    " recording; no numerical source edit"
                ),
            ),
            "function_source_sha256": function_hash,
            "isolation": (
                "Fresh subprocess and temporary CWD; no full helper/UI import; "
                "socket connect/create_connection blocked; original source "
                "immutable"
            ),
            "review_limits": (
                "Representative selected function only; reconstructed dependency"
                " environment; manually supplied comparison values are not "
                "measurements; no full dashboard, annual, correction or "
                "empirical claim"
            ),
        },
        "random_seed": None,
        "randomness_notes": (
            "Selected IV_R path has no RNG calls; SSC fitting is deterministic "
            "under these pinned dependencies"
        ),
        "capture_method": (
            "scripts/capture_legacy_iv.py --inputs "
            f"{inputs_path.relative_to(ROOT).as_posix()} --output <new-directory-inside-checkout>"
        ),
        "tolerances": tolerances,
        "review_status": (
            "Independently captured and replayed on the capture host; "
            "compatibility thresholds proposed for these cases, cross-platform "
            "verification pending; not scientific or empirical validation"
        ),
    }
    write_json(output / "manifest.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inputs", type=Path, default=ROOT / "tests/fixtures/legacy/iv_r/inputs.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="New directory inside checkout; existing output is never overwritten",
    )
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT) or output == ROOT:
        parser.error("output must be a new directory inside the checkout")
    if args.worker:
        worker(args.inputs.resolve(), output)
        return
    output.mkdir(parents=True, exist_ok=False)
    copied_input = output / "inputs.json"
    shutil.copyfile(args.inputs.resolve(), copied_input)
    run_root = ROOT / ".local/runs"
    run_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="legacy-iv-", dir=run_root) as cwd:
        environment = os.environ.copy()
        # Source execution needs no secrets; remove credential-like variables.
        for name in list(environment):
            if any(marker in name.upper() for marker in ("TOKEN", "SECRET", "API_KEY", "PASSWORD")):
                del environment[name]
        subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker",
                "--inputs",
                str(copied_input),
                "--output",
                str(output),
            ],
            cwd=cwd,
            env=environment,
            check=True,
        )
    print(f"Captured original IV_R to {output.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
