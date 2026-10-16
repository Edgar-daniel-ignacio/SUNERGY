"""Thin HTTP transport. Creating/importing this app performs no external I/O."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from sunergy import __version__
from sunergy.application import capabilities, health, request_module_iv
from sunergy.contracts import (
    CapabilityResponse,
    HealthResponse,
    ModuleIVRequest,
    UnavailableResponse,
)
from sunergy.physics import SimulationUnavailable

app = FastAPI(title="SUNERGY scaffold", version=__version__)


@app.get("/health", response_model=HealthResponse, operation_id="getHealth")
def get_health() -> HealthResponse:
    return health()


@app.get("/api/v1/capabilities", response_model=CapabilityResponse, operation_id="getCapabilities")
def get_capabilities() -> CapabilityResponse:
    return capabilities()


@app.post(
    "/api/v1/module-iv",
    status_code=501,
    response_model=UnavailableResponse,
    responses={501: {"model": UnavailableResponse}},
    operation_id="requestModuleIV",
)
def post_module_iv(request: ModuleIVRequest) -> JSONResponse:
    try:
        request_module_iv(request)
    except SimulationUnavailable:
        pass
    return JSONResponse(status_code=501, content=UnavailableResponse().model_dump())
