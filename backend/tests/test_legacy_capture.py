"""Independent legacy artifact integrity; numerical parity is tested separately."""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from sunergy.regression import Artifact, CaptureManifest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/legacy/iv_r"


@pytest.mark.parametrize("capture", ["captured", "captured_alternate"])
def test_independent_capture_provenance_and_every_record_are_preserved(capture: str) -> None:
    directory = FIXTURES / capture
    manifest = CaptureManifest.model_validate_json((directory / "manifest.json").read_text("utf-8"))
    wrapper = Artifact.model_validate(manifest.model_solver_grid["wrapper"])
    artifacts = [
        *manifest.source_files,
        manifest.dependency_lock,
        *manifest.inputs,
        *manifest.outputs,
        wrapper,
    ]
    for artifact in artifacts:
        path = ROOT / artifact.path
        assert path.resolve().is_relative_to(ROOT)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact.sha256, artifact.path
    assert manifest.entrypoint.startswith("Input_File_DIV_Mac_Informe.IV_R")
    assert manifest.catalog_snapshot is None
    assert manifest.weather_snapshot is None
    assert manifest.measurement_snapshot is None
    assert manifest.random_seed is None
    assert manifest.dependencies["pvlib"] == "0.13.1"
    assert manifest.dependencies["nrel-pysam"] == "7.1.0"
    inputs = json.loads((directory / "inputs.json").read_text("utf-8"))
    output = json.loads((directory / "outputs.json").read_text("utf-8"))
    assert [row[0] for row in inputs["conditions"]] == [
        case["condition_id"] for case in output["cases"]
    ]
    assert [row[0] for row in output["table"]["records"]] == [
        case["condition_id"] for case in output["cases"]
    ]
    for case in output["cases"]:
        for name in ("voltage", "current", "reverse_voltage", "reverse_current"):
            assert len(case[name]) == 100
        assert case["voltage"][0] == 0
        assert case["voltage"][-1] == case["singlediode"]["v_oc"]
    assert [case["id"] for case in output["failures"]] == [
        case["id"] for case in inputs["failure_cases"]
    ]


def test_capture_runner_refuses_to_replace_existing_reference() -> None:
    # Exercise the actual CLI guard without requiring legacy dependencies or
    # importing any legacy module into the test/application process.
    run_root = ROOT / ".local/runs"
    run_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="capture-overwrite-check-", dir=run_root) as scratch:
        directory = Path(scratch)
        marker = directory / "preserve.json"
        marker.write_text('{"preserve": true}\n', encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/capture_legacy_iv.py"),
                "--output",
                str(directory),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0
        assert "FileExistsError" in result.stderr
        assert marker.read_text("utf-8") == '{"preserve": true}\n'
        assert sorted(path.name for path in directory.iterdir()) == ["preserve.json"]
