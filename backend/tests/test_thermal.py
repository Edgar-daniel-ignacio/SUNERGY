"""Independent legacy thermal captures plus boundary and physical checks.

Fixtures come from executing original source before the modern kernels existed.
Synthetic conditions are not weather/measurements; equality does not establish
empirical thermal or annual-chain validation.
"""

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from sunergy.regression import (
    CaptureManifest,
    ComparisonOutput,
    QuantitySeries,
    compare_outputs,
)
from sunergy.thermal import (
    FaimanParameters,
    NoctParameters,
    ThermalPoint,
    calculate_thermal,
)
from sunergy.thermal_contracts import ThermalRequest, ThermalResponse

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/legacy/thermal"


def capture() -> tuple[dict[str, Any], dict[str, Any], CaptureManifest]:
    inputs = json.loads((FIXTURE / "captured/inputs.json").read_text("utf-8"))
    outputs = json.loads((FIXTURE / "captured/outputs.json").read_text("utf-8"))
    manifest = CaptureManifest.model_validate_json(
        (FIXTURE / "captured/manifest.json").read_text("utf-8")
    )
    return inputs, outputs, manifest


def request_for_case(inputs: dict[str, Any], case: dict[str, Any]) -> ThermalRequest:
    if case["profile_id"] == "legacy-faiman-v1":
        parameters = {
            "profile_id": case["profile_id"],
            "u0_w_m2_k": case["arguments"][0],
            "u1_w_m2_k_per_m_s": case["arguments"][1],
        }
    else:
        parameters = {
            "profile_id": case["profile_id"],
            "nominal_operating_temperature_c": case["arguments"][0],
        }
    return ThermalRequest.model_validate(
        {
            "parameters": parameters,
            "points": [
                {
                    "record_id": row[0],
                    "poa_global_w_m2": row[1],
                    "ambient_temperature_c": row[2],
                    "wind_speed_m_s": row[3],
                }
                for row in inputs["rows"]
            ],
        }
    )


def comparison(ids: list[str], values: list[float]) -> ComparisonOutput:
    return ComparisonOutput(
        identifiers=ids, quantities={"temperature": QuantitySeries(unit="degC", values=values)}
    )


def test_thermal_capture_provenance_and_wrapper_are_intact() -> None:
    inputs, outputs, manifest = capture()
    assert manifest.capture_id == "legacy-thermal-synthetic-v1"
    assert "synthetic" in manifest.time_convention
    assert (
        manifest.catalog_snapshot,
        manifest.weather_snapshot,
        manifest.measurement_snapshot,
    ) == (
        None,
        None,
        None,
    )
    artifacts = [
        *manifest.source_files,
        manifest.dependency_lock,
        *manifest.inputs,
        *manifest.outputs,
    ]
    for artifact in artifacts:
        assert hashlib.sha256((ROOT / artifact.path).read_bytes()).hexdigest() == artifact.sha256
    wrapper = manifest.model_solver_grid["wrapper"]
    assert isinstance(wrapper, dict) and isinstance(wrapper["path"], str)
    assert hashlib.sha256((ROOT / wrapper["path"]).read_bytes()).hexdigest() == wrapper["sha256"]
    assert inputs == json.loads((FIXTURE / "inputs.json").read_text("utf-8"))
    assert len(outputs["cases"]) == len(inputs["cases"]) == 4


@pytest.mark.parametrize("case_index", range(4))
def test_modern_temperatures_reproduce_independent_capture(case_index: int) -> None:
    inputs, outputs, manifest = capture()
    case = inputs["cases"][case_index]
    expected = outputs["cases"][case_index]
    assert expected["case_id"] == case["case_id"]
    assert expected["profile_id"] == case["profile_id"]
    assert expected["return"] is None
    assert expected["columns"] == ["Poa_global", "temp_air", "wind_speed", case["output_column"]]
    assert [row[:-1] for row in expected["records"]] == [row[1:] for row in inputs["rows"]]
    assert expected["missing_irradiance_failure"]["exception_type"] == "AttributeError"
    request = request_for_case(inputs, case)
    points, parameters = request.to_calculation_inputs()
    unchanged = deepcopy((points, parameters))
    result = calculate_thermal(points, parameters)
    assert (points, parameters) == unchanged
    response = ThermalResponse.from_result(result)
    assert response.legacy_output_column == case["output_column"]
    assert response.profile_id == case["profile_id"]
    assert response.unit == "degC"
    actual = comparison(list(response.identifiers), list(response.temperature_c))
    reference = comparison(expected["identifiers"], [row[-1] for row in expected["records"]])
    assert compare_outputs(reference, actual, manifest.tolerances) == []


def test_temperature_or_record_order_discrepancy_fails_comparison() -> None:
    _, outputs, manifest = capture()
    case = outputs["cases"][0]
    reference = comparison(case["identifiers"], [row[-1] for row in case["records"]])
    perturbed = reference.model_copy(deep=True)
    perturbed.quantities["temperature"].values[2] += 0.01
    assert compare_outputs(reference, perturbed, manifest.tolerances)
    perturbed = reference.model_copy(deep=True)
    perturbed.identifiers.reverse()
    assert "identifiers/order differ" in compare_outputs(reference, perturbed, manifest.tolerances)


def test_faiman_reference_conditions_and_wind_cooling() -> None:
    # Faiman T=Ta+E/(U0+U1*WS): 700/(25+10*1)=20 K, 700/25=28 K.
    # Formulation: pvlib official faiman documentation; equation checks are
    # separate from a second pvlib call and do not establish empirical accuracy.
    points = (
        ThermalPoint("dark", 0, 20, 1),
        ThermalPoint("calm", 700, 20, 0),
        ThermalPoint("wind", 700, 20, 1),
    )
    result = calculate_thermal(points, FaimanParameters(25, 10))
    assert result.temperature_c == (20, 48, 40)


def test_noct_reference_and_zero_irradiance_and_wind_independence() -> None:
    # At the legacy 800 W/m2, 20 degC reference, output equals supplied TNMOT.
    points = (
        ThermalPoint("dark", 0, -5, 0),
        ThermalPoint("reference", 800, 20, 1),
        ThermalPoint("wind-change", 800, 20, 7),
    )
    assert calculate_thermal(points, NoctParameters(43)).temperature_c == (-5, 43, 43)


@pytest.mark.parametrize(
    "change",
    [
        {"poa_global_w_m2": -1},
        {"wind_speed_m_s": -1},
        {"ambient_temperature_c": -273.15},
        {"ambient_temperature_c": float("nan")},
        {"poa_global_w_m2": float("inf")},
    ],
)
def test_point_boundary_rejects_unsupported_conditions(change: dict[str, float]) -> None:
    inputs, _, _ = capture()
    request = request_for_case(inputs, inputs["cases"][0]).model_dump()
    request["points"][0].update(change)
    with pytest.raises(ValidationError):
        ThermalRequest.model_validate(request)


def test_missing_parameters_records_and_unknown_sandia_profile_fail_explicitly() -> None:
    inputs, _, _ = capture()
    valid = request_for_case(inputs, inputs["cases"][0]).model_dump()
    missing = deepcopy(valid)
    del missing["points"][0]["poa_global_w_m2"]
    with pytest.raises(ValidationError):
        ThermalRequest.model_validate(missing)
    for parameters in (
        {"profile_id": "legacy-faiman-v1", "u0_w_m2_k": 0, "u1_w_m2_k_per_m_s": 6.84},
        {"profile_id": "legacy-faiman-v1", "u0_w_m2_k": 25},
        {"profile_id": "legacy-noct-v1", "nominal_operating_temperature_c": 20},
        {"profile_id": "legacy-sandia-v1"},
    ):
        with pytest.raises(ValidationError):
            ThermalRequest.model_validate({**valid, "parameters": parameters})
    for points in ([], [valid["points"][0], valid["points"][0]]):
        with pytest.raises(ValidationError):
            ThermalRequest.model_validate({**valid, "points": points})


def test_cross_field_heat_loss_overflow_and_nonfinite_result_fail() -> None:
    inputs, _, _ = capture()
    request = request_for_case(inputs, inputs["cases"][0]).model_dump()
    request["parameters"]["u1_w_m2_k_per_m_s"] = 1e308
    with pytest.raises(ValidationError, match="Combined heat-loss"):
        ThermalRequest.model_validate(request)
    with pytest.raises(ValueError, match="heat-loss"):
        calculate_thermal((ThermalPoint("wind", 800, 20, 2),), FaimanParameters(25, 1e308))
    with pytest.raises(ValueError, match="result"):
        calculate_thermal((ThermalPoint("hot", 1e308, 20, 1),), NoctParameters(1e308))


def test_direct_kernel_and_output_boundary_reject_incoherent_records() -> None:
    with pytest.raises(ValueError):
        ThermalPoint("invalid", -1, 20, 1)
    with pytest.raises(ValueError):
        FaimanParameters(0, 6.84)
    with pytest.raises(ValueError):
        NoctParameters(20)
    with pytest.raises(ValueError):
        calculate_thermal((), NoctParameters(43))
    repeated = ThermalPoint("repeated", 800, 20, 1)
    with pytest.raises(ValueError):
        calculate_thermal((repeated, repeated), NoctParameters(43))
    with pytest.raises(ValidationError):
        ThermalResponse(
            profile_id="legacy-noct-v1",
            legacy_output_column="TFeinman",
            identifiers=("point",),
            temperature_c=(43,),
        )
    with pytest.raises(ValidationError):
        ThermalResponse(
            profile_id="legacy-noct-v1",
            legacy_output_column="NOCT",
            identifiers=("point", "missing"),
            temperature_c=(43,),
        )
