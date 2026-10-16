"""Numerical boundary, independent of Pydantic, HTTP, plotting, and legacy UI."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OperatingCondition:
    effective_irradiance_w_m2: float
    cell_temperature_c: float


class SimulationUnavailable(NotImplementedError):
    """No migrated or scientifically verified model is available."""


def simulate_module_iv(condition: OperatingCondition, *, model_id: str) -> None:
    """Reserved calculation boundary; never manufacture a curve or successful result."""
    raise SimulationUnavailable(f"Model {model_id!r} has no implemented calculation")
