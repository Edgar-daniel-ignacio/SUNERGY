"""Use cases shared by HTTP handlers and non-HTTP callers."""

from sunergy import __version__
from sunergy.contracts import CapabilityResponse, HealthResponse, ModuleIVRequest
from sunergy.physics import OperatingCondition, simulate_module_iv


def health() -> HealthResponse:
    """Process liveness only; no claim about scientific readiness or upstream services."""
    return HealthResponse(version=__version__)


def capabilities() -> CapabilityResponse:
    return CapabilityResponse()


def request_module_iv(request: ModuleIVRequest) -> None:
    simulate_module_iv(
        OperatingCondition(
            request.operating_point.effective_irradiance_w_m2,
            request.operating_point.cell_temperature_c,
        ),
        model_id=request.model_id,
    )
