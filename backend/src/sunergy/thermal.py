"""Captured legacy thermal kernels; no acquisition, Pydantic, HTTP or plotting.

The supported point boundary returns values without changing caller data. It does
not reproduce the legacy mutable NDH wrapper or claim measured cell temperature.
Coefficients are explicit inputs; no scientifically accepted default is selected.
"""

from dataclasses import dataclass
from math import isfinite
from typing import ClassVar, Literal


@dataclass(frozen=True)
class ThermalPoint:
    record_id: str
    poa_global_w_m2: float
    ambient_temperature_c: float
    wind_speed_m_s: float

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("Thermal record identity is required")
        if not all(
            isfinite(value)
            for value in (
                self.poa_global_w_m2,
                self.ambient_temperature_c,
                self.wind_speed_m_s,
            )
        ):
            raise ValueError("Thermal inputs must be finite")
        if (
            self.poa_global_w_m2 < 0
            or self.wind_speed_m_s < 0
            or self.ambient_temperature_c <= -273.15
        ):
            raise ValueError(
                "Nonnegative irradiance/wind and physical ambient temperature required"
            )


@dataclass(frozen=True)
class FaimanParameters:
    profile_id: ClassVar[Literal["legacy-faiman-v1"]] = "legacy-faiman-v1"
    u0_w_m2_k: float
    u1_w_m2_k_per_m_s: float

    def __post_init__(self) -> None:
        if not all(
            isfinite(value) and value > 0 for value in (self.u0_w_m2_k, self.u1_w_m2_k_per_m_s)
        ):
            raise ValueError("Positive finite heat-loss coefficients required by supported profile")


@dataclass(frozen=True)
class NoctParameters:
    profile_id: ClassVar[Literal["legacy-noct-v1"]] = "legacy-noct-v1"
    nominal_operating_temperature_c: float

    def __post_init__(self) -> None:
        if (
            not isfinite(self.nominal_operating_temperature_c)
            or self.nominal_operating_temperature_c <= 20
        ):
            raise ValueError("Supported NOCT profile requires nominal temperature above 20 degC")


@dataclass(frozen=True)
class ThermalResult:
    profile_id: Literal["legacy-faiman-v1", "legacy-noct-v1"]
    legacy_output_column: Literal["TFeinman", "NOCT"]
    identifiers: tuple[str, ...]
    temperature_c: tuple[float, ...]


def calculate_thermal(
    points: tuple[ThermalPoint, ...],
    parameters: FaimanParameters | NoctParameters,
) -> ThermalResult:
    """Evaluate every point in caller order using the selected captured equation.

    `legacy-faiman-v1`: T = Ta + E / (U0 + U1 * wind).
    `legacy-noct-v1`: T = Ta + ((TNMOT - 20) / 800) * E.
    NOCT ignores wind exactly as in the original kernel. No imputation, rounding,
    aggregation, time interpretation, RNG, parameter fitting or calibration.
    """
    if not points or len({point.record_id for point in points}) != len(points):
        raise ValueError("Nonempty thermal points with unique identifiers required")
    values = []
    for point in points:
        if isinstance(parameters, FaimanParameters):
            loss_factor = parameters.u0_w_m2_k + parameters.u1_w_m2_k_per_m_s * point.wind_speed_m_s
            if not isfinite(loss_factor) or loss_factor <= 0:
                raise ValueError("Positive finite combined heat-loss factor required")
            temperature = point.ambient_temperature_c + point.poa_global_w_m2 / loss_factor
        elif isinstance(parameters, NoctParameters):
            temperature = (
                point.ambient_temperature_c
                + ((parameters.nominal_operating_temperature_c - 20) / 800) * point.poa_global_w_m2
            )
        else:
            raise ValueError("Unknown thermal compatibility profile")
        if not isfinite(temperature) or temperature <= -273.15:
            raise ValueError("Thermal result is outside finite physical temperature domain")
        values.append(temperature)
    return ThermalResult(
        parameters.profile_id,
        "TFeinman" if isinstance(parameters, FaimanParameters) else "NOCT",
        tuple(point.record_id for point in points),
        tuple(values),
    )
