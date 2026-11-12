"""Legacy reproduction, numerical equation checks and boundary tests are separate."""

import json
from copy import deepcopy
from math import exp, expm1
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from sunergy.api import app
from sunergy.application import reproduce_legacy_iv
from sunergy.compatibility import LegacyIVRequest, LegacyIVResponse
from sunergy.contracts import SourceRecord
from sunergy.fetcher import normalize_legacy_iv_input
from sunergy.model import LegacyCalculationError
from sunergy.regression import CaptureManifest, verify_capture_artifacts
from sunergy.replay import compare_iv_reference, iv_capture_names, replay_iv_capture

ROOT = Path(__file__).resolve().parents[2]
CAPTURES = ROOT / "tests/fixtures/legacy/iv_r"


@pytest.fixture(scope="module", params=iv_capture_names())
def captured(request: pytest.FixtureRequest) -> tuple[CaptureManifest, dict[str, Any], Any]:
    path = CAPTURES / str(request.param)
    manifest = CaptureManifest.model_validate_json((path / "manifest.json").read_text("utf-8"))
    reference = json.loads((path / "outputs.json").read_text("utf-8"))
    result, problems = replay_iv_capture(ROOT, path / "manifest.json")
    assert not problems, problems
    return manifest, reference, result


def test_modern_reproduces_independent_legacy_stages_and_all_returned_points(captured: Any) -> None:
    manifest, reference, result = captured
    assert compare_iv_reference(reference, result, manifest) == []
    assert sum(len(case.voltage_v) for case in result.cases) == 100 * len(reference["cases"])
    assert result.supplied_module.source_cell_type != result.effective_assumptions["cell_type"]
    assert result.fit_inputs["temp_ref"] == 25
    assert (
        result.effective_assumptions["desoto_alpha_sc_legacy_raw"] != result.fit_inputs["alpha_sc"]
    )


@pytest.mark.parametrize("change", ["current", "order", "shape", "table", "quantity", "fit"])
def test_real_reproduction_gate_detects_meaningful_discrepancies(
    captured: Any, change: str
) -> None:
    manifest, reference, original = captured
    result = original.model_copy(deep=True)
    if change == "current":
        result.cases[0].current_a[40] += 0.001
    elif change == "order":
        result.cases.reverse()
    elif change == "shape":
        result.cases[0].voltage_v.pop()
    elif change == "table":
        result.table_columns.reverse()
    elif change == "quantity":
        del result.cases[0].singlediode["p_mp"]
    else:
        result.fit_parameters["I_o_ref"] *= 1.01
    assert compare_iv_reference(reference, result, manifest)


def test_reproduction_does_not_inherit_candidate_units_from_manifest(captured: Any) -> None:
    manifest, reference, result = captured
    changed = manifest.model_copy(deep=True)
    changed.tolerances["current"].unit = "mA"
    assert any(
        "units differ" in problem for problem in compare_iv_reference(reference, result, changed)
    )


@pytest.mark.parametrize("change", ["cases", "parameters", "metric", "table", "label"])
def test_output_contract_rejects_incomplete_or_misaligned_results(
    captured: Any, change: str
) -> None:
    _, _, result = captured
    data = result.model_dump()
    if change == "cases":
        data["cases"] = []
    elif change == "parameters":
        data["cases"][0]["desoto_parameters"] = {}
    elif change == "metric":
        del data["cases"][0]["singlediode"]["p_mp"]
    elif change == "table":
        data["table_records"].pop()
    else:
        data["cases"][0]["condition_id"] = "changed"
    with pytest.raises(ValidationError):
        LegacyIVResponse.model_validate(data)


def test_scientific_solver_residual_and_endpoints(captured: Any) -> None:
    # Independent equation arithmetic, not a second pvlib solver. Supports solver
    # consistency only, not the source coefficient chain or empirical accuracy.
    _, _, result = captured
    for case in result.cases:
        p = case.desoto_parameters
        il, i0 = p["photocurrent"], p["saturation_current"]
        rs, rsh, a = p["resistance_series"], p["resistance_shunt"], p["nNsVth"]
        residuals = [
            i - il + i0 * expm1((v + i * rs) / a) + (v + i * rs) / rsh
            for v, i in zip(case.voltage_v, case.current_a, strict=True)
        ]
        assert max(abs(value) for value in residuals) < 1e-10  # A, observed <4e-14
        assert case.voltage_v[0] == 0
        assert case.voltage_v[-1] == case.singlediode["v_oc"]
        assert abs(case.current_a[-1]) < 1e-10


def test_original_unmet_mpp_audit_target_is_preserved_and_visible(captured: Any) -> None:
    _, reference, result = captured

    def stationarity(parameters: dict[str, float], metrics: dict[str, float]) -> float:
        v, i = metrics["v_mp"], metrics["i_mp"]
        rs, rsh = parameters["resistance_series"], parameters["resistance_shunt"]
        a, i0 = parameters["nNsVth"], parameters["saturation_current"]
        conductance = i0 * exp((v + i * rs) / a) / a + 1 / rsh
        return i - v * conductance / (1 + rs * conductance)

    for original, modern in zip(reference["cases"], result.cases, strict=True):
        expected = stationarity(original["desoto_parameters"], original["singlediode"])
        actual = stationarity(modern.desoto_parameters, modern.singlediode)
        assert actual == pytest.approx(expected, abs=1e-12)
        assert (abs(actual) < 1e-6) == (abs(expected) < 1e-6)
    # The fixed scientific target is an audit result, not a passing accuracy gate.
    # The raw Linux reference fails it; this test characterizes that limitation.
    assert "unmet" in result.scientific_status


def test_scientific_translation_scaling_and_preserved_alpha_inconsistency(captured: Any) -> None:
    _, _, result = captured
    for case, supplied in zip(result.cases, result.supplied_cases, strict=True):
        expected = (
            supplied.effective_irradiance_w_m2
            / 1000
            * (
                result.fit_parameters["I_L_ref"]
                + result.supplied_module.alpha_sc_percent_per_c * (supplied.cell_temperature_c - 25)
            )
        )
        assert case.desoto_parameters["photocurrent"] == pytest.approx(expected, abs=1e-12)
        assert case.desoto_inputs["temp_cell"] == supplied.cell_temperature_c
        if supplied.cell_temperature_c != 25:
            corrected = (
                supplied.effective_irradiance_w_m2
                / 1000
                * (
                    result.fit_parameters["I_L_ref"]
                    + float(result.fit_inputs["alpha_sc"]) * (supplied.cell_temperature_c - 25)
                )
            )
            assert abs(expected - corrected) > 1e-3


def input_data() -> dict[str, Any]:
    return json.loads((CAPTURES / "inputs.json").read_text("utf-8"))  # type: ignore[no-any-return]


def test_fetcher_preserves_values_order_and_does_no_imputation() -> None:
    data = input_data()
    original = deepcopy(data)
    request = normalize_legacy_iv_input(data)
    assert data == original
    assert request.module.alpha_sc_percent_per_c == 0.01
    data["module"].reverse()
    with pytest.raises(ValueError, match="keys/order"):
        normalize_legacy_iv_input(data)
    data = input_data()
    data["condition_columns"].remove("Geff")
    with pytest.raises(ValueError, match="columns/order"):
        normalize_legacy_iv_input(data)


def test_unknown_source_schema_and_inconsistent_capture_identity_fail() -> None:
    data = input_data()
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        normalize_legacy_iv_input(data)
    data = input_data()
    data["capture_id"] = "another-capture"
    record = SourceRecord(
        source_id="expected-capture", snapshot_sha256="a" * 64, record_id="module"
    )
    with pytest.raises(ValueError, match="identity"):
        normalize_legacy_iv_input(data, source_record=record)


def test_changed_output_artifact_and_wrong_branch_cannot_be_replayed(tmp_path: Path) -> None:
    original_path = CAPTURES / "captured/manifest.json"
    manifest = CaptureManifest.model_validate_json(original_path.read_text("utf-8"))
    changed = manifest.model_copy(deep=True)
    changed.outputs[0].sha256 = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_capture_artifacts(ROOT, changed)
    changed = manifest.model_copy(deep=True)
    changed.entrypoint = "CurvaIV.IV"
    path = tmp_path / "wrong-branch.json"
    path.write_text(changed.model_dump_json(), encoding="utf-8")
    with pytest.raises(ValueError, match="entrypoint"):
        replay_iv_capture(ROOT, path)


def test_reference_selection_is_explicit_and_never_falls_back() -> None:
    assert iv_capture_names(system="Windows", machine="AMD64") == ("captured", "captured_alternate")
    assert iv_capture_names(system="Linux", machine="x86_64") == (
        "captured_linux",
        "captured_alternate_linux",
    )
    with pytest.raises(ValueError, match="operating system"):
        iv_capture_names(system="Darwin", machine="x86_64")
    with pytest.raises(ValueError, match="architecture"):
        iv_capture_names(system="Linux", machine="arm64")


@pytest.mark.parametrize(
    "field,value",
    [
        ("effective_irradiance_w_m2", 0),
        ("cell_temperature_c", -273.15),
        ("comparison_i_sc_a", float("nan")),
    ],
)
def test_compatibility_boundary_rejects_undefined_or_nonfinite_inputs(
    field: str, value: float
) -> None:
    data = normalize_legacy_iv_input(input_data()).model_dump()
    data["cases"][0][field] = value
    with pytest.raises(ValidationError):
        LegacyIVRequest.model_validate(data)


def test_legacy_missing_comparison_fields_become_explicit_schema_failure() -> None:
    data = normalize_legacy_iv_input(input_data()).model_dump()
    del data["cases"][0]["comparison_i_sc_a"]
    with TestClient(app) as client:
        response = client.post("/api/v1/compatibility/iv-r", json=data)
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    schema = app.openapi()["paths"]["/api/v1/compatibility/iv-r"]["post"]["responses"]
    assert schema["422"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "HTTPValidationError"
    )
    assert schema["400"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "CalculationFailure"
    )


def test_http_and_direct_compatibility_use_the_same_calculation() -> None:
    request = normalize_legacy_iv_input(input_data())
    direct = reproduce_legacy_iv(request)
    with TestClient(app) as client:
        response = client.post("/api/v1/compatibility/iv-r", json=request.model_dump())
    assert response.status_code == 200
    assert response.json() == direct.model_dump()


def test_fit_failure_is_explicit_and_has_no_result(monkeypatch: pytest.MonkeyPatch) -> None:
    def failed_fit(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("synthetic solver failure; never a capture")

    monkeypatch.setattr("sunergy.model.pvlib.ivtools.sdm.fit_cec_sam", failed_fit)
    request = normalize_legacy_iv_input(input_data())
    with pytest.raises(LegacyCalculationError):
        reproduce_legacy_iv(request)
    with TestClient(app) as client:
        response = client.post("/api/v1/compatibility/iv-r", json=request.model_dump())
    assert response.status_code == 400
    assert response.json()["code"] == "legacy_iv_calculation_failed"
    assert "cases" not in response.json()
