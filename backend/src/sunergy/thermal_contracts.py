"""External contracts for the captured thermal point kernels, separate from API.

All points and parameters are required. Source normalization must already have
explicitly supplied total plane-of-array irradiance, ambient temperature and wind
in these units. These models do not interpret timestamps or fill missing records.
"""

from math import isfinite
from typing import Annotated, Literal

from pydantic import Field, model_validator

from sunergy.contracts import BoundaryModel, NonEmpty
from sunergy.thermal import FaimanParameters, NoctParameters, ThermalPoint, ThermalResult


class ThermalPointInput(BoundaryModel):
    record_id: NonEmpty
    poa_global_w_m2: float = Field(
        ge=0, description="Total incident plane-of-array irradiance W/m2"
    )
    ambient_temperature_c: float = Field(
        gt=-273.15, description="Ambient dry-bulb temperature degC"
    )
    wind_speed_m_s: float = Field(
        ge=0, description="Wind speed at coefficient-reference height, m/s"
    )


class FaimanProfile(BoundaryModel):
    profile_id: Literal["legacy-faiman-v1"]
    u0_w_m2_k: float = Field(gt=0, description="Combined constant heat-loss coefficient W/(m2 K)")
    u1_w_m2_k_per_m_s: float = Field(gt=0, description="Wind heat-loss coefficient W/(m2 K (m/s))")


class NoctProfile(BoundaryModel):
    profile_id: Literal["legacy-noct-v1"]
    nominal_operating_temperature_c: float = Field(
        gt=20, description="Explicit legacy TNMOT/NOCT parameter degC; restricted heat-rise domain"
    )


class ThermalRequest(BoundaryModel):
    parameters: Annotated[FaimanProfile | NoctProfile, Field(discriminator="profile_id")]
    points: tuple[ThermalPointInput, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def coherent_points(self) -> "ThermalRequest":
        if len({point.record_id for point in self.points}) != len(self.points):
            raise ValueError("Thermal record identifiers must be unique")
        if self.parameters.profile_id == "legacy-faiman-v1":
            for point in self.points:
                loss_factor = (
                    self.parameters.u0_w_m2_k
                    + self.parameters.u1_w_m2_k_per_m_s * point.wind_speed_m_s
                )
                if not isfinite(loss_factor) or loss_factor <= 0:
                    raise ValueError("Combined heat-loss factor must be finite and positive")
        return self

    def to_calculation_inputs(
        self,
    ) -> tuple[tuple[ThermalPoint, ...], FaimanParameters | NoctParameters]:
        points = tuple(
            ThermalPoint(
                point.record_id,
                point.poa_global_w_m2,
                point.ambient_temperature_c,
                point.wind_speed_m_s,
            )
            for point in self.points
        )
        parameters: FaimanParameters | NoctParameters
        if self.parameters.profile_id == "legacy-faiman-v1":
            parameters = FaimanParameters(
                self.parameters.u0_w_m2_k,
                self.parameters.u1_w_m2_k_per_m_s,
            )
        else:
            parameters = NoctParameters(self.parameters.nominal_operating_temperature_c)
        return points, parameters


class ThermalResponse(BoundaryModel):
    profile_id: Literal["legacy-faiman-v1", "legacy-noct-v1"]
    legacy_output_column: Literal["TFeinman", "NOCT"]
    unit: Literal["degC"] = "degC"
    identifiers: tuple[NonEmpty, ...] = Field(min_length=1)
    temperature_c: tuple[float, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def aligned_result(self) -> "ThermalResponse":
        if len(set(self.identifiers)) != len(self.identifiers) or len(self.identifiers) != len(
            self.temperature_c
        ):
            raise ValueError("Temperatures must retain all unique identifiers in order")
        expected_column = "TFeinman" if self.profile_id == "legacy-faiman-v1" else "NOCT"
        if self.legacy_output_column != expected_column:
            raise ValueError("Output column must agree with thermal profile")
        if any(value <= -273.15 for value in self.temperature_c):
            raise ValueError("Thermal outputs must be above absolute zero")
        return self

    @classmethod
    def from_result(cls, result: ThermalResult) -> "ThermalResponse":
        return cls(
            profile_id=result.profile_id,
            legacy_output_column=result.legacy_output_column,
            identifiers=result.identifiers,
            temperature_c=result.temperature_c,
        )
