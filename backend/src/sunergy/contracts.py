"""Provisional external contracts; successful parsing is only schema validation."""

from typing import Annotated, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

NonEmpty = Annotated[str, Field(min_length=1, pattern=r"\S")]
Sha256 = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]


class BoundaryModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Site(BoundaryModel):
    latitude_deg: float = Field(ge=-90, le=90)
    longitude_deg: float = Field(ge=-180, le=180)
    timezone: NonEmpty = Field(description="IANA zone; no inferred current UTC offset")

    @field_validator("timezone")
    @classmethod
    def known_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as error:
            raise ValueError("Use an installed IANA timezone") from error
        return value


class SourceRecord(BoundaryModel):
    source_id: NonEmpty
    snapshot_sha256: Sha256
    record_id: NonEmpty


class ManualModule(BoundaryModel):
    kind: Literal["manual"]
    name: NonEmpty
    cell_type: Literal["monoSi", "multiSi", "polySi", "cis", "cigs", "cdte", "amorphous"]
    cells_in_series: int = Field(gt=0, strict=True)
    v_mp_v: float = Field(gt=0)
    i_mp_a: float = Field(gt=0)
    v_oc_v: float = Field(gt=0)
    i_sc_a: float = Field(gt=0)
    alpha_sc_a_per_c: float = Field(description="Absolute Isc temperature coefficient, A/°C")
    beta_voc_v_per_c: float = Field(description="Absolute Voc temperature coefficient, V/°C")
    gamma_pmp_percent_per_c: float = Field(description="Pmp coefficient, percent/°C, not Vmp")
    reference_irradiance_w_m2: float = Field(gt=0)
    reference_cell_temperature_c: float = Field(gt=-273.15)
    source_record: SourceRecord | None = None

    @model_validator(mode="after")
    def ordered_nameplate_points(self) -> "ManualModule":
        if self.v_mp_v >= self.v_oc_v or self.i_mp_a >= self.i_sc_a:
            raise ValueError("MPP voltage/current must be below open/short circuit values")
        return self


class CatalogModule(BoundaryModel):
    kind: Literal["catalog"]
    source_record: SourceRecord


class OperatingPoint(BoundaryModel):
    effective_irradiance_w_m2: float = Field(ge=0, description="Effective in-plane irradiance")
    cell_temperature_c: float = Field(gt=-273.15, description="Cell, not ambient temperature")


class ModuleIVRequest(BoundaryModel):
    """Reserved point-simulation boundary; no model is implemented yet."""

    site: Site
    module: Annotated[ManualModule | CatalogModule, Field(discriminator="kind")]
    operating_point: OperatingPoint
    model_id: NonEmpty = Field(description="Explicit versioned selection; no production default")
    # Measurements are intentionally absent: optional future evaluation is a separate use case.


class HealthResponse(BoundaryModel):
    status: Literal["ok"] = "ok"
    service: Literal["sunergy"] = "sunergy"
    version: str


class CapabilityResponse(BoundaryModel):
    module_iv: Literal["not_implemented"] = "not_implemented"
    legacy_reproduction: Literal["missing_reference_outputs"] = "missing_reference_outputs"
    scientific_verification: Literal["not_performed"] = "not_performed"
    measurement_comparison: Literal["not_implemented"] = "not_implemented"
    calibration: Literal["not_implemented"] = "not_implemented"


class UnavailableResponse(BoundaryModel):
    code: Literal["module_iv_not_implemented"] = "module_iv_not_implemented"
    message: str = "Module I–V simulation awaits independent legacy capture and implementation."
