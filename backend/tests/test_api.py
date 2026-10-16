from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from sunergy.api import app
from sunergy.application import request_module_iv
from sunergy.contracts import ModuleIVRequest
from sunergy.physics import SimulationUnavailable


@pytest.fixture
def request_data() -> dict[str, Any]:
    # Synthetic boundary input, not a legacy fixture or scientifically verified module.
    return {
        "site": {"latitude_deg": 0, "longitude_deg": 0, "timezone": "Etc/UTC"},
        "module": {
            "kind": "manual",
            "name": "synthetic contract-only module",
            "cell_type": "polySi",
            "cells_in_series": 60,
            "v_mp_v": 30,
            "i_mp_a": 8,
            "v_oc_v": 38,
            "i_sc_a": 9,
            "alpha_sc_a_per_c": 0.004,
            "beta_voc_v_per_c": -0.1,
            "gamma_pmp_percent_per_c": -0.4,
            "reference_irradiance_w_m2": 1000,
            "reference_cell_temperature_c": 25,
        },
        "operating_point": {"effective_irradiance_w_m2": 800, "cell_temperature_c": 40},
        "model_id": "synthetic-unimplemented-v1",
    }


def test_health_is_liveness_and_capabilities_are_explicit() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "service": "sunergy", "version": "0.1.0"}
        assert client.get("/api/v1/capabilities").json() == {
            "module_iv": "not_implemented",
            "legacy_reproduction": "missing_reference_outputs",
            "scientific_verification": "not_performed",
            "measurement_comparison": "not_implemented",
            "calibration": "not_implemented",
        }


def test_valid_forward_request_needs_no_measurement_and_returns_501(
    request_data: dict[str, Any],
) -> None:
    request = ModuleIVRequest.model_validate(request_data)
    with pytest.raises(SimulationUnavailable):
        request_module_iv(request)
    with TestClient(app) as client:
        response = client.post("/api/v1/module-iv", json=request_data)
        assert response.status_code == 501
        assert response.json()["code"] == "module_iv_not_implemented"
        assert "results" not in response.json()


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("site", "latitude_deg", 91),
        ("site", "timezone", "not/a-timezone"),
        ("operating_point", "effective_irradiance_w_m2", -1),
        ("operating_point", "cell_temperature_c", -273.15),
        ("module", "cells_in_series", 1.5),
        ("module", "v_mp_v", 100),
    ],
)
def test_bad_boundaries_are_not_reported_as_valid_simulations(
    request_data: dict[str, Any], section: str, field: str, value: object
) -> None:
    request_data[section][field] = value
    with TestClient(app) as client:
        assert client.post("/api/v1/module-iv", json=request_data).status_code == 422


def test_nonfinite_and_ambiguous_coefficients_rejected(request_data: dict[str, Any]) -> None:
    request_data["module"]["alpha"] = 0.05
    with pytest.raises(ValidationError):
        ModuleIVRequest.model_validate(request_data)
    del request_data["module"]["alpha"]
    request_data["module"]["alpha_sc_a_per_c"] = float("nan")
    with pytest.raises(ValidationError):
        ModuleIVRequest.model_validate(request_data)


def test_catalog_selection_requires_immutable_record(request_data: dict[str, Any]) -> None:
    request_data["module"] = {"kind": "catalog", "source_record": {"record_id": "a"}}
    with pytest.raises(ValidationError):
        ModuleIVRequest.model_validate(request_data)
    request_data["module"]["source_record"].update(source_id="synthetic", snapshot_sha256="a" * 64)
    assert ModuleIVRequest.model_validate(request_data).module.kind == "catalog"
