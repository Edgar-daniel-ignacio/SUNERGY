"""Use cases shared by HTTP handlers and non-HTTP callers."""

from sunergy import __version__
from sunergy.compatibility import (
    TABLE_COLUMNS,
    LegacyIVCaseResult,
    LegacyIVRequest,
    LegacyIVResponse,
)
from sunergy.contracts import CapabilityResponse, HealthResponse, ModuleIVRequest
from sunergy.model import (
    LegacyCondition,
    LegacyModuleParameters,
    fit_legacy_iv,
    legacy_fit_inputs,
    solve_legacy_iv,
)
from sunergy.physics import OperatingCondition, simulate_module_iv
from sunergy.thermal import calculate_thermal
from sunergy.thermal_contracts import ThermalRequest, ThermalResponse


def health() -> HealthResponse:
    """Process liveness only; no claim about scientific readiness or upstream services."""
    return HealthResponse(version=__version__)


def capabilities() -> CapabilityResponse:
    return CapabilityResponse()


def request_thermal(request: ThermalRequest) -> ThermalResponse:
    """Validated offline thermal point use case; no annual/weather inference."""
    points, parameters = request.to_calculation_inputs()
    return ThermalResponse.from_result(calculate_thermal(points, parameters))


def request_module_iv(request: ModuleIVRequest) -> None:
    simulate_module_iv(
        OperatingCondition(
            request.operating_point.effective_irradiance_w_m2,
            request.operating_point.cell_temperature_c,
        ),
        model_id=request.model_id,
    )


def reproduce_legacy_iv(request: LegacyIVRequest) -> LegacyIVResponse:
    """Directly callable compatibility use case; no files or HTTP are needed."""
    source = request.module
    module = LegacyModuleParameters(
        source.v_mp_v,
        source.i_mp_a,
        source.v_oc_v,
        source.i_sc_a,
        source.alpha_sc_percent_per_c,
        source.beta_voc_percent_per_c,
        source.gamma_pmp_percent_per_c,
        source.cells_in_series,
    )
    fit = fit_legacy_iv(module)
    results = []
    records: list[list[str | float]] = []
    for case in request.cases:
        result = solve_legacy_iv(
            module,
            fit,
            LegacyCondition(
                case.condition_id,
                case.effective_irradiance_w_m2,
                case.cell_temperature_c,
                (
                    case.comparison_i_sc_a,
                    case.comparison_v_oc_v,
                    case.comparison_i_mp_a,
                    case.comparison_v_mp_v,
                    case.comparison_p_mp_w,
                ),
            ),
        )
        results.append(
            LegacyIVCaseResult(
                condition_id=result.condition_id,
                desoto_parameters=result.parameters,
                desoto_inputs=result.translation_inputs,
                singlediode=result.metrics,
                voltage_v=list(result.voltage_v),
                current_a=list(result.current_a),
            )
        )
        records.append([result.condition_id, *result.error_row])
    return LegacyIVResponse(
        supplied_module=source,
        supplied_cases=request.cases,
        source_record=request.source_record,
        effective_assumptions={
            "cell_type": "monoSi",
            "reference_temperature_c": 25,
            "reference_irradiance_w_m2": 1000,
            "EgRef_eV": 1.121,
            "dEgdT_per_k": -0.0002677,
            "grid_points": 100,
            "solver": "lambertw",
            "desoto_alpha_sc_legacy_raw": source.alpha_sc_percent_per_c,
            "desoto_alpha_interpretation": "Legacy raw percent number passed as A/°C",
            "cec_adjust_usage": "Returned for provenance; ignored by legacy De Soto translation",
        },
        fit_parameters=fit,
        fit_inputs=legacy_fit_inputs(module),
        cases=results,
        table_columns=list(TABLE_COLUMNS),
        table_records=records,
    )
